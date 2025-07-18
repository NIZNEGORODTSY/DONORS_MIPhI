from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, BotCommand
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
import logging
import asyncio
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import config.reader as reader
import sys

from core import check_admin

reader.read_config()

TOKEN = reader.get_param_value('token')

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


class AuthState(StatesGroup):
    waiting_for_phone = State()


@dp.message(Command("start"))
async def start_command(message: Message):
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

    await message.answer("Давайте начнём! Для регистрации нажмите /authenticate или выбери раздел в меню ↓")


@dp.message(Command('authenticate'))
async def authorization(message: Message, state: FSMContext):
    await message.answer("Введите ваш номер телефона...")
    await state.set_state(AuthState.waiting_for_phone)


@dp.message(AuthState.waiting_for_phone)  # Хэндлер для состояния
async def process_phone(message: Message, state: FSMContext):
    phone_number = message.text  # Получаем введённый номер
    res = check_admin(message.from_user.id)
    if res:
        await message.answer('Добро пожаловать в админ-панель')
    else:
        pass
    await state.clear()


@dp.message(Command('menu'))
async def menu_handler(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text='Наш сайт', url='https://google.com')
    builder.button(text='Связаться в Telegram', url='https://google.com')
    await message.answer(
        text='Выбери действие:',
        reply_markup=builder.as_markup()
    )


@dp.message(Command('another_menu'))
async def another_menu_handler(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text='Наш сайт', url='https://google.com')
    builder.button(text='Связаться в Telegram', url='https://google.com')
    await message.answer(
        text='Выбери действие:',
        reply_markup=builder.as_markup()
    )


async def main():
    await bot.set_my_commands([
        BotCommand(command='start', description='Приветствие'),
        BotCommand(command='menu', description='Меню'),
        BotCommand(command='another_menu', description='Другое меню'),
        BotCommand(command='authenticate', description='идентификация')
    ])

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
