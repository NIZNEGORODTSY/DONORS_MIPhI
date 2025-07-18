from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, BotCommand, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
import logging
import asyncio
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import config.reader as reader
import sys
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Contact
)
import asyncio

from core import check_admin, check_user_by_phone, get_user, add_fio, get_user_history, add_ugroup

from scripts import is_valid_russian_phone, compare_date, display_history, validate_full_name, generate_donor_advice, get_daily_weather

reader.read_config()

TOKEN = reader.get_param_value('token')

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


class AuthState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_answer = State()
    waiting_for_right_fio = State()


class RegisterState(StatesGroup):
    fio = State()
    group = State()
    student_group = State()
    final = State


class InfoState(StatesGroup):
    main_state = State()


def get_consent_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Да, всё верно")],
            [KeyboardButton(text="❌ Нет, неверно")]
        ],
        resize_keyboard=True
    )


def choose_group():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎓Студент")],
            [KeyboardButton(text="💼Сотрудник")],
            [KeyboardButton(text="🤲Внешний донор")],
        ],
        resize_keyboard=True
    )


def get_main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Мои данные")],
            [KeyboardButton(text="📅 Записаться на донацию")],
            [KeyboardButton(text="ℹ️ Информация о донорстве")],
            [KeyboardButton(text="❓ Задать вопрос")]
        ],
        resize_keyboard=True
    )


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
    if is_valid_russian_phone(phone_number):
        res = check_admin(message.from_user.id)
        if res is False: #БААААААААААААААААГ
            await message.answer('Добро пожаловать в админ-панель')
        else:
            res = check_user_by_phone(phone_number)
            if res:
                name = get_user(message.from_user.id)
                await message.answer(f'Добро пожаловать, {name.Fio}! Проверьте правильность ваших данных.',
                                     reply_markup=get_consent_keyboard())

                await state.set_state(AuthState.waiting_for_answer)
            else:
                await message.answer("Чтобы создать аккаунт, напишите ваше ФИО")
                await state.set_state(RegisterState.fio)
    else:
        await message.answer('Проверьте правильность введённых данных!')


@dp.message(AuthState.waiting_for_answer)
async def waiting_for_answer(message: Message, state: FSMContext):
    text = message.text
    if text == '❌ Нет, неверно':
        await message.answer('Введите верный вариант...')
        await state.set_state(AuthState.waiting_for_right_fio)
    else:
        await message.answer('Отлично! Добро пожаловать в меню: /menu')
        await state.clear()


@dp.message(AuthState.waiting_for_right_fio)
async def waiting_for_right_fio(message: Message, state: FSMContext):
    text = message.text
    add_fio(message.from_user.id, text)
    await message.answer('Данные успешно изменены! Добро пожаловать в меню: /menu')
    await state.clear()


@dp.message(RegisterState.fio)
async def register_fio(message: Message, state: FSMContext):
    fio = message.text
    if validate_full_name(fio):
        add_fio(message.from_user.id, fio)
        await message.answer("Кто вы?", reply_markup=choose_group())
        await state.set_state(RegisterState.group)
    else:
        await message.answer('Проверьте правильность введённых данных!')


@dp.message(RegisterState.group)
async def define_group(message: Message, state: FSMContext):
    text = message.text
    if text == "🎓Студент":
        await message.answer("Напишите номер вашей группы")
        state.set_state(RegisterState.student_group)
    if text == "💼Сотрудник":
        add_ugroup(message.from_user.id, "Сотрудник")
        await message.answer("Поздравляем! Теперь вы можете спасать жизни!")
        await state.clear()
    if text == "🤲Внешний донор":
        add_ugroup(message.from_user.id, "Внешний донор")
        await message.answer("Поздравляем! Теперь вы можете спасать жизни!")
        await state.clear()
    pass


@dp.message(RegisterState.student_group)
async def student_group(message: Message, state: FSMContext):
    text = message.text
    add_ugroup(message.from_user.id, text)
    await message.answer("Поздравляем! Теперь вы можете спасать жизни!")
    await state.clear()


@dp.message(F.text == "📋 Мои данные")
async def show_profile(message: Message):
    name = get_user(message.from_user.id)
    history = get_user_history(name.Id)
    date1 = name.LastGavr
    date2 = name.LastFMBA
    date_res, place = compare_date(date1, date2)
    await message.answer(f"""<b>ФИО</b>: {name.Fio}
<b>Количество донаций:</b> {name.SumCount}
<b>Дата последней донации:</b> {date_res}
<b>Место последней донации:</b> {place}
<b>Регистрация в регистре ДМК:</b> {name.Registry}
<b>История донаций:</b> 
{display_history(history)}""", parse_mode=ParseMode.HTML)


@dp.message(F.text == "ℹ️ Информация о донорстве")
async def show_information(message: Message):
    await message.answer(generate_donor_advice(get_daily_weather()))


@dp.message(Command('menu'))
async def another_menu_handler(message: Message):
    await message.answer(
        text='Выбери действие:',
        reply_markup=get_main_menu_keyboard()
    )


async def main():
    await bot.set_my_commands([
        BotCommand(command='start', description='Приветствие'),
        BotCommand(command='menu', description='Меню'),
        BotCommand(command='authenticate', description='идентификация')
    ])

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
