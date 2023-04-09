from typing import List
from selenium import webdriver
from bs4 import BeautifulSoup, Tag
from dateutil import parser as date_parser
import time

TWITTER_PREFIX = "https://twitter.com/"


class TwitterScraper:
    def __init__(self, driver: webdriver.Chrome, delay: int = 5):
        self.driver = driver
        self.delay = delay

    def fetch_page_source(self, username: str) -> str:
        self.driver.get(TWITTER_PREFIX + username)
        time.sleep(self.delay)
        return self.driver.page_source

    @staticmethod
    def _check_retweet(section):
        return "Retweeted" in str(section.select_one("a"))

    @staticmethod
    def _get_pfp(section):
        if not section.select_one("img"):
            return ""
        return section.select_one("img")["src"]

    @staticmethod
    def _get_tweet_text(section):
        return section.select_one("div").text

    @staticmethod
    def _get_tweet_image(section):
        images: List[str] = []
        if section:
            for i in section.find_all("img"):
                src = i["src"]
                if not "profile_images" in src:
                    images.append(i["src"])
        return images

    @staticmethod
    def _parse_author_info(author_info):
        x = (
            author_info.select_one("div > div")
            .findChildren("div", recursive=False)[0]
            .findChildren("div", recursive=False)[0]
            .findChildren("div", recursive=False)[0]
            .findChildren("div", recursive=False)
        )

        username_link = x[0].select_one("a")
        link_time = x[1].find_all("a")[1]
        post_id = link_time["href"].replace(username_link["href"] + "/status/", "")
        post_time = date_parser.parse(link_time.find("time")["datetime"])

        return {
            "post": {"time": int(post_time.timestamp()), "id": post_id},
            "author": {
                "name": username_link.text,
                "link": TWITTER_PREFIX + username_link["href"].replace("/", ""),
                "handle": username_link["href"].replace("/", ""),
            },
        }

    @classmethod
    def _extract_data(cls, article: Tag) -> dict:
        data = {"author": {}, "tweet": {}}
        # Dividing tweet article into 2 sections: Retweet status and Main tweet content
        sections = article.select_one("div > div").findChildren("div", recursive=False)
        data["retweet"] = cls._check_retweet(sections[0])

        main_tweet = sections[1]
        # Dividing main tweet into 2 sections: Profile picture and Content
        sections = main_tweet.findChildren("div", recursive=False)
        data["author"]["avatar"] = cls._get_pfp(sections[0])

        content = sections[1]
        # Dividing content into 5 sections: Author name, Tweet text, retweeted post/images (if any), likes and other
        # stats
        sections = content.findChildren("div", recursive=False)

        tweet_text_section = sections[1]
        tweet_image_section = sections[2]
        data["tweet"]["text"] = cls._get_tweet_text(tweet_text_section)
        data["tweet"]["images"] = cls._get_tweet_image(tweet_image_section)

        author_info = sections[0]
        author_data = cls._parse_author_info(author_info)
        data["author"].update(author_data["author"])
        data["tweet"].update(author_data["post"])

        return data

    @classmethod
    def get_one_tweet_preview(cls, tweet_index: int, page_source: str):
        html = BeautifulSoup(page_source, "html.parser")
        articles = html.find_all("article")
        return cls._extract_data(articles[tweet_index])
