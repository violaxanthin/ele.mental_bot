import time

import logging 
import os
import sys
import asyncio
import apsched

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from flask import Flask
from datetime import datetime, timedelta
load_dotenv()

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

# Configure logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MemoryStorage
storage = MemoryStorage()

# Create objects of Dispatcher and Bot
bot_token = "6944011537:AAEVOkl0qj2vYP7VkaWYq-kZ4xpXHF0qbTs"
bot = Bot(bot_token)
dp = Dispatcher(storage=storage)

# start the flask app
app = Flask(__name__)
@app.route('/')

# Start function
@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    await message.answer(
        text = f'Здравствуйте, {user_full_name}! На связи Ele.Mental – бот самомониторинга. \n\n '
        'Он создан для того, чтобы помочь вам самостоятельно контролировать свое ментальное состояние.\n' 
'Формат чат-бота – дневник, который вам предлагается заполнять в с помощью коротких ответов на вопросы из клинических опросников и шкал, '
'а результаты будут автоматически анализироваться алгоритмами искусственного интеллекта, чтобы сформировать картину стабильности состояния.\n '
'В случае обнаружения признаков изменений в состоянии, вы получите  письменную рекомендацию к посещению доктора. \n' 
'Данные, введенные в формы будут использованы исключительно в рамках исследования и в соответствии с политикой персональных данных Google: https://policies.google.com/privacy \n'
'Перед использованием чат-бота, пожалуйста, обратитесь к медицинскому специалисту.\n\n'
    )
    scheduler.add_job(apsched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=15),
                  kwargs={'bot':bot, 'user_id':user_id})
    scheduler.add_job(apsched.send_message_cron_1, trigger='cron', hour=10, 
                  minute=0, day_of_week='0, 3, 6', start_date=datetime.now(), end_date=datetime.now() + timedelta(days=14),
                  kwargs={'bot':bot, 'user_id':user_id, 'user_full_name':user_full_name})
    scheduler.add_job(apsched.send_message_cron_2, trigger='cron', hour=19,
                  minute=0, day_of_week='0, 3, 6', start_date=datetime.now(), end_date=datetime.now() + timedelta(days=14),
                  kwargs={'bot':bot, 'user_id':user_id})
    scheduler.start()

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(bot_token, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

# Launch polling
if __name__ == '__main__':
    dp.run_polling(bot, allowed_updates=[])
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main()) 