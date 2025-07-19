from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, BotCommand
from aiogram.enums import ParseMode
import config.reader as reader
import logging

from handlers import admin, user

from core import get_admins
from keybord.admin import get_organizer_keyboard

# Настройка логирования

TOKEN = reader.get_param_value('token')
ADMINS = get_admins()
ADMINS = ''

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота


# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dop = Dispatcher()


# Хэндлеры
@dop.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    if str(message.from_user.id) in ADMINS:

        await message.answer("Добро пожаловать в панель организатора!", reply_markup=get_organizer_keyboard())
    else:

        await message.answer(f"""Здравствуйте, {message.from_user.full_name}! 👋 Я — помощник донорского центра МИФИ.

        Моя цель:
✅ Упростить запись на Дни Донора
✅ Рассказать о донорстве крови и костного мозга
✅ Напоминать о важных датах и результатах анализов

Что вы можете сделать?
🔹 Записаться на сдачу крови за 2 минуты
🔹 Узнать требования к донорам и подготовку
🔹 Проверить свою историю донаций
🔹 Задать вопрос организаторам""")

        await message.answer(f"""<b><i>Условия использования</i></b>
------------------------------------
<b>Персональные данные</b>
Используя этого бота, вы соглашаетесь на обработку ваших персональных данных (ФИО, контакты, данные донорской анкеты) для записи на донацию и взаимодействия с донорским центром МИФИ.

<b>Рассылка</b>
Бот может присылать вам уведомления о записи, результатах анализов, донорских акциях и важных событиях центра. Вы можете отписаться в любой момент через команду /stop.

<b>Конфиденциальность</b>
Ваши данные хранятся защищённо и не передаются третьим лицам без вашего согласия.

        !!!Продолжая использование, вы подтверждаете согласие с этими условиями!!!""", parse_mode=ParseMode.HTML)
        await bot.set_my_commands([
            BotCommand(command='start', description='Приветствие'),
            BotCommand(command='menu', description='Меню'),
            BotCommand(command='another_menu', description='Другое меню'),
            BotCommand(command='authenticate', description='идентификация')
        ])
        await message.answer("Давайте начнём! Для регистрации нажмите /authenticate или выбери раздел в меню ↓")


async def main():
    dop.include_routers(admin.dp)
    dop.include_routers(user.dp)
    await dop.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
