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
from aiogram.fsm.storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler
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
bot_token =  os.getenv("BOT_TOKEN")
logging.info("sleeping of 5 sec")
time.sleep(5)

bot = Bot(bot_token)
dp = Dispatcher(storage=storage)

# Start function
@dp.message(Command(commands=["start"]))
async def start(message: Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    await message.answer(
        text = f'Здравствуйте, {user_full_name}! На связи Ele.Mental – бот самомониторинга. \n\n '
        'Он создан для того, чтобы помочь вам самостоятельно контролировать свое ментальное состояние.\n' 
'Формат чат-бота – дневник, который вам предлагается заполнять в с помощью коротких ответов на вопросы из клинических опросников и шкал, '
' результаты которых будут анализироваться с применением алгоритмов искусственного интеллекта, чтобы сформировать картину стабильности состояния.\n '
'В случае обнаружения признаков изменений в состоянии, вы получите письменную рекомендацию к посещению доктора. \n'
'Для вашего удобства бот будет присылать вам уведомления с опросниками 2 раза в день - утром и вечером. \n'
'Данные, введенные в формы будут использованы исключительно в рамках исследования и в соответствии с политикой персональных данных Google: https://policies.google.com/privacy \n'
'Перед использованием чат-бота, пожалуйста, обратитесь к медицинскому специалисту.'
    ) 
# Schedule first reminder (message '1') at 10:00 every 3 days for 5 times   
    for i in range(5):
        scheduler.add_job(
        apsched.send_message_cron_1,
        trigger='cron',
        hour=1,
        minute=20,
        start_date=datetime.now() + timedelta(days=3 * i),
        kwargs={'bot': bot, 'user_id': user_id, 'user_full_name': user_full_name}
        )
 # Schedule second reminder (message '2') at 19:00 every 3 days for 5 times                
        scheduler.add_job(
        apsched.send_message_cron_2,
        trigger='cron',
        hour=1,
        minute=21,
        start_date=datetime.now() + timedelta(days=3 * i),
        kwargs={'bot': bot, 'user_id': user_id}
        )

        scheduler.start()

@dp.message(Command(commands=["help"]))
async def help(message: Message):
    await message.answer(
        text = 'Нужна помощь? Свяжитесь с нами: @violaxanthin'
    )

# Main function to start polling
async def main():
    await dp.start_polling(bot, allowed_updates=[])

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # Start the bot
    asyncio.run(main())