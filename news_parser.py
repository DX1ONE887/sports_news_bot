import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
from database import get_sources
from config import BASE_SOURCES

async def fetch_page(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                content = await response.text()
                with open("debug.html", "w", encoding="utf-8") as f:
                    f.write(content)
                return content
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def parse_news(html: str, url: str):
    soup = BeautifulSoup(html, 'html.parser')
    news_items = []
    
    for item in soup.select('div.news-item'):  # Новый селектор
        try:
            title = item.select_one('div.news-item__title').text.strip()
            link = item.select_one('a.news-item__link')['href']
            time_str = item.select_one('div.news-item__date').text.strip()
            
            # Обработка времени
            try:
                pub_time = datetime.strptime(time_str, "%d.%m.%Y %H:%M")
            except ValueError:
                pub_time = datetime.now()
            
            news_items.append({
                'title': title,
                'link': link,
                'time': pub_time
            })
        except Exception as e:
            logging.error(f"Error parsing: {str(e)[:100]}")
    
    return news_items

async def get_recent_news():
    all_news = []
    sources = BASE_SOURCES + get_sources()
    
    logging.info(f"Проверяем источники: {sources}")
    
    for url in sources:
        html = await fetch_page(url)
        if html:
            parsed = parse_news(html, url)
            logging.info(f"Найдено {len(parsed)} новостей в {url}")
            all_news.extend(parsed)
    
    time_threshold = datetime.now() - timedelta(minutes=5)
    filtered_news = [
        item for item in all_news 
        if item['time'] > time_threshold
    ]
    logging.info(f"Новостей после фильтра времени: {len(filtered_news)}")
    return filtered_news

def filter_news(news_list, stop_words):
    filtered = []
    for news in news_list:
        title_lower = news['title'].lower()
        if not any(word.lower() in title_lower for word in stop_words):
            filtered.append(news)
    return filtered