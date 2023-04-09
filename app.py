from app.scraper import TwitterScraper, TWITTER_PREFIX
from app.db import Base, TweetSent

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from discord_webhook import DiscordWebhook, DiscordEmbed

import time
import traceback
import os
import dotenv

dotenv.load_dotenv()

WEBHOOK_URL = os.environ["WEBHOOK_URL"]

db_engine = create_engine("sqlite:///data.db", echo=True)
session = Session(db_engine)
Base.metadata.create_all(db_engine)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
scraper = TwitterScraper(driver, delay=10)


def run():
    while True:
        try:
            source = scraper.fetch_page_source("tanteiwamou_")
            try:
                data = scraper.get_one_tweet_preview(0, source)
            except:
                traceback.print_exc()
                continue

            result = session.query(TweetSent).filter_by(id=int(data["tweet"]["id"])).first()
            print(
                f"Latest tweet is {data['tweet']['id']}, record {'exists' if result else 'does not exist'} in database")
            if not result:
                # This tweet has not been sent via webhook, send it and add record
                hook = DiscordWebhook(url=WEBHOOK_URL)
                embed = DiscordEmbed(title="Retweet" if data["retweet"] else "Link",
                                     description=data["tweet"]["text"][:2000],
                                     url=data["author"]["link"] + f"/status/{data['tweet']['id']}")
                embed.set_author(
                    name=data["author"]["name"] + f"  (@{data['author']['link'].replace(TWITTER_PREFIX + '/', '')})",
                    url=data["author"]["link"], icon_url=data["author"]["avatar"])
                embed.set_color(color=11393254)
                embed.set_timestamp(data["tweet"]["time"])
                embed.set_footer(text="Powered by BanjoScraper for Discord")

                images = data["tweet"]["images"]
                if len(images):
                    embed.set_image(url=images[0])

                hook.add_embed(embed)
                hook.execute()
                new_tweet = TweetSent(id=int(data["tweet"]["id"]),
                                      tweet_time=data["tweet"]["time"],
                                      author_handle=data["author"]["handle"],
                                      message_id=int(hook.id))
                session.add(new_tweet)
                session.commit()

            time.sleep(10)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    run()