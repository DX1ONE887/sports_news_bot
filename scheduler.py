import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from config import ADMIN_ID
from news_parser import get_recent_news, filter_news
from database import get_stop_words

scheduler = AsyncIOScheduler()

async def send_news(bot: Bot):
    try:
        all_news = await get_recent_news()
        stop_words = get_stop_words()
        filtered_news = filter_news(all_news, stop_words)
        
        for news in filtered_news:
            message = f"{news['title']}\n\n{news['link']}"
            await bot.send_message(ADMIN_ID, message)
    except Exception as e:
        logging.error(f"Error in scheduler: {e}")

def setup_scheduler(bot: Bot):
    scheduler.add_job(send_news, 'interval', minutes=5, args=(bot,))
    scheduler.start()