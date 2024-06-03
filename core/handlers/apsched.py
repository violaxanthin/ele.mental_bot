from aiogram import Bot
from aiogram.types import Message
import os

# токен бота, полученный у @BotFather
bot_token = os.getenv("BOT_TOKEN")

# reminders и ID для получения уведомлений о запуске
async def send_message_time(bot: Bot):
    await bot.send_message({user_id}, f'Введенные данные необходимы исключительно в целях исследования.\n '
                           'Для вашего удобства бот будет присылать вам уведомления с опросниками 2 раза в день - утром и вечером. \n'
                           'Рекомендация: старайтесь не пропускать уведомления и заполнять дневник регулярно.\n\n'
                           'Для этого перейдите по ссылке на гугл-форму:\n\n' 
                           'https://forms.gle/Xa1rsVmDhfVxCfmh9')

async def send_message_cron_1(bot: Bot):
    await bot.send_message({user_id}, f'Доброе утро, {user_full_name}! Приступим к заполнению дневника?\n'
                           'https://forms.gle/Xa1rsVmDhfVxCfmh9')
    
async def send_message_cron_2(bot: Bot):
    await bot.send_message({user_id}, f'Сейчас самое время заполнить дневник.\n'
                           'Завершите этот день продуктивно, заполнив состояния.\n\n' 
                           'https://forms.gle/CUoc4dkXm59UZd6cA')