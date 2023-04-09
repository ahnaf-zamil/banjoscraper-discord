# BanjoScrapper for Discord

A Discord webhook-based notification system for Twitter.

## About

Well, Twitter just announced that they are not gonna keep the API free. So a lot of bots (especially
Twitter notification bots) died. I'm talking about the bots that send every tweet of a person to a Discord
channel, those don't work now. So I took it upon myself to make a scraper-based app to do the job.

## Technologies

- Selenium (with Chrome driver)
- BeautifulSoup
- SQLAlchemy (with SQlite)
- DiscordWebhook

## Usage

Just install the requirements and create a `.env` file from the `.env.example`. Put your Webhook URL
in `.env` and save it.

Now open your terminal and run

```bash
python app.py
```

Have fun!

## Screenshots

![Screnshot #1](https://cdn.discordapp.com/attachments/795877321201549322/1094614279161909319/image.png)
![Screnshot #2](https://cdn.discordapp.net/attachments/795877321201549322/1094663127678861522/image.png)

## License

MIT License

Copyright (c) 2023 K.M Ahnaf Zamil

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
