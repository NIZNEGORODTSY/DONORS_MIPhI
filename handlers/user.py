import re
from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.enums import ParseMode

from keybord.user import get_consent_keyboard, get_main_menu_keyboard, choose_group

from core import check_user_by_phone, get_user, add_fio, get_user_history, add_ugroup

from scripts import is_valid_russian_phone, compare_date, display_history, validate_full_name, generate_donor_advice, get_daily_weather, display_weather

dp = Router()


class AuthState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_answer = State()
    waiting_for_right_fio = State()


class RegisterState(StatesGroup):
    fio = State()
    group = State()
    final = State()
    student_group = State()


class InfoState(StatesGroup):
    main_state = State()


@dp.message(Command('authenticate'))
async def authorization(message: Message, state: FSMContext):
    await message.answer("Введите ваш номер телефона...")
    await state.set_state(AuthState.waiting_for_phone)


@dp.message(AuthState.waiting_for_phone)  # Хэндлер для состояния
async def process_phone(message: Message, state: FSMContext):
    phone_number = message.text  # Получаем введённый номер
    if is_valid_russian_phone(phone_number):
        # res = check_admin(message.from_user.id)
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
        await message.answer('Отлично! Добро пожаловать в меню:', reply_markup=get_main_menu_keyboard())
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
        await state.set_state(RegisterState.student_group)
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
async def show_profile(message: Message, state: FSMContext):
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
    await state.clear()


@dp.message(F.text == "🌤 Рекомендации для доноров на сегодня")
async def show_information(message: Message, state: FSMContext):
    advice = generate_donor_advice(get_daily_weather())
    weather = display_weather(get_daily_weather())
    await message.answer(advice + '\n' + weather)
    await state.clear()


@dp.message(Command('menu'))
async def another_menu_handler(message: Message):
    await message.answer(
        text='Выбери действие:',
        reply_markup=get_main_menu_keyboard()
    )
