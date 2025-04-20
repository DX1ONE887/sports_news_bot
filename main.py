import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN, ADMIN_ID
import database
import scheduler

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    text = (
        "Бот запущен! Новости будут приходить каждый час.\n"
        "Доступные команды:\n"
        "/addword [слово] - добавить стоп-слово\n"
        "/addurl [url] - добавить источник\n"
        "/removeword [id] - удалить стоп-слово\n"
        "/removeurl [id] - удалить источник\n"
        "/words - список всех стоп-слов\n"
        "/urls - список всех источников"
    )
    await message.answer(text)

@dp.message_handler(commands=['addword'])
async def add_stop_word(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    word = message.get_args()
    if word:
        database.add_stop_word(word)
        await message.answer(f"✅ Стоп-слово '{word}' добавлено")

@dp.message_handler(commands=['addurl'])
async def add_source(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    url = message.get_args()
    if url:
        database.add_source(url)
        await message.answer(f"✅ Источник '{url}' добавлен")

@dp.message_handler(commands=['removeword'])
async def remove_word(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        word_id = int(message.get_args())
        database.remove_stop_word(word_id)
        await message.answer(f"✅ Стоп-слово с ID {word_id} удалено")
    except:
        await message.answer("❌ Укажите корректный ID слова")

@dp.message_handler(commands=['removeurl'])
async def remove_url(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        url_id = int(message.get_args())
        database.remove_source(url_id)
        await message.answer(f"✅ Источник с ID {url_id} удален")
    except:
        await message.answer("❌ Укажите корректный ID источника")

@dp.message_handler(commands=['words'])
async def list_words(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    words = database.get_all_stop_words()
    if not words:
        await message.answer("📭 Список стоп-слов пуст")
        return
    
    response = "📝 Список стоп-слов:\n" + "\n".join(
        [f"{word[0]}. {word[1]}" for word in words]
    )
    await message.answer(response)

@dp.message_handler(commands=['urls'])
async def list_urls(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    urls = database.get_all_sources()
    if not urls:
        await message.answer("📭 Список источников пуст")
        return
    
    response = "🌐 Список источников:\n" + "\n".join(
        [f"{url[0]}. {url[1]}" for url in urls]
    )
    await message.answer(response)

@dp.message_handler(commands=['add_stop_word'])
async def add_stop_word(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    word = message.get_args()
    if word:
        database.add_stop_word(word)
        await message.answer(f"Стоп-слово '{word}' добавлено")

@dp.message_handler(commands=['add_source'])
async def add_source(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    url = message.get_args()
    if url:
        database.add_source(url)
        await message.answer(f"Источник '{url}' добавлен")

if __name__ == '__main__':
    scheduler.setup_scheduler(bot)
    executor.start_polling(dp, skip_updates=True)