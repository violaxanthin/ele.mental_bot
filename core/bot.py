import time

import logging 
import os
import sys

import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

from aiogram.fsm.storage.memory import MemoryStorage
 
from apscheduler.schedulers.asyncio import AsyncIOScheduler
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
from handlers import apsched
from datetime import datetime, timedelta
load_dotenv()

from aiogram import BaseMiddleware

class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

# Configure logging
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()

# Создаем объекты бота и диспетчера
bot_token = os.getenv("BOT_TOKEN")
bot = Bot(bot_token)
dp = Dispatcher(storage=storage)

#Старт бота и запуск напоминаний
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
'Перед использованием чат-бота, пожалуйста, обратитесь к медицинскому специалисту.\n\n'
    )
    scheduler.add_job(apsched.send_message_time, trigger='date', run_date=datetime.now() + timedelta(seconds=15),
                  kwargs={'bot':bot, 'user_id':user_id})
    scheduler.add_job(apsched.send_message_cron_1, trigger='cron', hour=10, 
                  minute=0, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=14),
                  kwargs={'bot':bot, 'user_id':user_id, 'user_full_name':user_full_name})
    scheduler.add_job(apsched.send_message_cron_2, trigger='cron', hour=19,
                  minute=0, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=14),
                  kwargs={'bot':bot, 'user_id':user_id})
    scheduler.start()



async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(bot_token, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

# Запускаем поллинг
if __name__ == '__main__':
    dp.run_polling(bot, allowed_updates=[])
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())