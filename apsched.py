from aiogram import Bot

# reminders 
async def send_message_cron_2(bot: Bot, user_id: int):
    await bot.send_message(user_id, text='Сейчас самое время заполнить дневник.\n'
                                    'Завершите этот день продуктивно, заполнив состояния.\n\n' 
                                    'https://forms.gle/CUoc4dkXm59UZd6cA')

async def send_message_cron_1(bot: Bot, user_id: int, user_full_name: str):
    await bot.send_message(user_id, f'Доброе утро, {user_full_name}! Приступим к заполнению дневника?\n'
                                    'https://forms.gle/Xa1rsVmDhfVxCfmh9')
