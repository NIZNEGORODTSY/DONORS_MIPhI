from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from handlers import admin, user

from based import gets_admins
from keybord.admin import get_organizer_keyboard

# Настройка логирования

BOT_TOKEN = "8195479409:AAFfZj3V05P5bZD0rCwwWF_a80nX6NObsa4"
ADMINS = gets_admins()
#ADMINS = ''

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота


# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dop = Dispatcher()

# Хэндлеры
@dop.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:
        
        await message.answer("Добро пожаловать в панель организатора!", reply_markup=get_organizer_keyboard())
    else:
        
        await message.answer(
        "👋 Привет! Я бот для доноров крови МИФИ.\n\n"
        "Я помогу тебе:\n"
        "- Узнать о донорстве крови и костного мозга\n"
        "- Зарегистрироваться на донорские дни\n"
        "- Отслеживать свою донорскую историю\n"
        "- Получать важную информацию\n\n"
        "Для начала работы пройди быструю регистрацию!",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)]],
            resize_keyboard=True
        ))
        await state.set_state(user.Registration.phone)
   
    



async def main():
    dop.include_routers(admin.dp)
    dop.include_routers(user.dp)
    await dop.start_polling(bot)
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())