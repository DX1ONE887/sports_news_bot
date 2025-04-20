# test_parser.py
from news_parser import fetch_page, parse_news
import asyncio

async def main():
    url = "https://www.sports.ru/football/news/top/"
    html = await fetch_page(url)
    if html:
        news = parse_news(html, url)
        print(f"Найдено: {len(news)} новостей")
        for item in news[:3]:
            print(f"{item['time']} | {item['title']}")

asyncio.run(main())