import re
from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.enums import ParseMode

from keybord.user import get_consent_keyboard, get_main_menu_keyboard, choose_group, get_phone_number_keyboard, \
    get_detailed_information

from core import check_user_by_phone, get_user, add_fio, get_user_history, add_ugroup, add_question, \
    get_upcoming_events, add_registration, add_user, get_questions_by_user

from scripts import is_valid_russian_phone, compare_date, display_history, validate_full_name, generate_donor_advice, \
    get_daily_weather, display_weather, get_restrictions

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
    detailed_information = State()


class Questions(StatesGroup):
    waiting_for_question = State()


class SignUpForDonation(StatesGroup):
    waiting_for_date = State()


@dp.message(F.text == '🔐Аутентификация')
async def authorization(message: Message, state: FSMContext):
    await message.answer("Введите ваш номер телефона...", reply_markup=get_phone_number_keyboard())
    await state.set_state(AuthState.waiting_for_phone)


@dp.message(AuthState.waiting_for_phone)  # Хэндлер для состояния
async def process_phone(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    # phone_number = '+7 934 324 5456'
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
            add_user(phone_number, message.from_user.id)
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
    fio = message.text
    add_fio(message.from_user.id, fio)
    await message.answer('Данные успешно изменены! Добро пожаловать в меню: /menu',
                         reply_markup=get_main_menu_keyboard())
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
        await message.answer("Поздравляем! Теперь вы можете спасать жизни!", reply_markup=get_main_menu_keyboard())
        await state.clear()
    if text == "🤲Внешний донор":
        add_ugroup(message.from_user.id, "Внешний донор")
        await message.answer("Поздравляем! Теперь вы можете спасать жизни!", reply_markup=get_main_menu_keyboard())
        await state.clear()


@dp.message(RegisterState.student_group)
async def student_group(message: Message, state: FSMContext):
    text = message.text
    add_ugroup(message.from_user.id, text)
    await message.answer("Поздравляем! Теперь вы можете спасать жизни!", reply_markup=get_main_menu_keyboard())
    await state.clear()


@dp.message(F.text == "📋 Мои данные")
async def show_profile(message: Message, state: FSMContext):
    name = get_user(message.from_user.id)
    history = get_user_history(name.Id)
    date1 = name.LastGavr
    date2 = name.LastFMBA
    date_res, place = compare_date(date1, date2)
    NAME = name.Fio
    AMOUNT = name.SumCount
    REGISTRY = name.Registry
    if AMOUNT is None:
        AMOUNT = 0
    if REGISTRY is None:
        REGISTRY = 0
    await message.answer(f"""<b>ФИО</b>: {NAME}
<b>Количество донаций:</b> {AMOUNT}
<b>Дата последней донации:</b> {date_res}
<b>Место последней донации:</b> {place}
<b>Регистрация в регистре ДМК:</b> {REGISTRY}
<b>История донаций:</b> 
{display_history(history)}""", parse_mode=ParseMode.HTML)
    await state.clear()


@dp.message(F.text == "📅 Записаться на донацию")
async def sign_up_for_donation(message: Message, state: FSMContext):
    await message.answer("Выберите дату и место, указав номер события из списка.")
    data = get_upcoming_events()
    events = ''
    for event in data:
        events += f'{event.Id})Место: {event.DonPlace}, дата и время: {event.DonDate}.\n'
    await message.answer(events)

    await state.set_state(SignUpForDonation.waiting_for_date)


@dp.message(SignUpForDonation.waiting_for_date)
async def waiting_for_date(message: Message, state: FSMContext):
    data = get_upcoming_events()
    max_id = 1
    for event in data:
        max_id += 1

    chose = message.text
    if chose.isdigit() and 1 <= int(chose) <= max_id:
        res = ''
        MAX = 0
        for event in data:
            if event.Id == int(chose):
                res = f'место: {event.DonPlace}, дата и время: {event.DonDate}.'
        await message.answer(f"Вы выбрали:\n{res}", reply_markup=get_main_menu_keyboard())
        uid = get_user(message.from_user.id).Id
        add_registration(chose, uid)
        await message.answer(f"Вы записаны✅", reply_markup=get_main_menu_keyboard())
        # ЗДЕСЬ БУДЕТ ФУНЦКИЯ ДЛЯ ДОБАВЛЕНИЯ ЗАПИСИ В БД
    else:
        await message.answer('Проверьте правильность введённых данных')


@dp.message(F.text == "ℹ️ Информация о донорстве")
async def info_about_donation(message: Message, state: FSMContext):
    await message.answer('Выберите нужный раздел', reply_markup=get_detailed_information())
    await state.set_state(InfoState.detailed_information)


@dp.message(InfoState.detailed_information)
async def info_about_donation(message: Message, state: FSMContext):
    text = message.text
    if text == "🔙Вернуться в меню":
        await message.answer("Добро пожаловать в меню!", reply_markup=get_main_menu_keyboard())
        await state.clear()
        text = ""
    await message.answer(get_restrictions(f"{text}"))


@dp.message(F.text == "🌤 Рекомендации для доноров на сегодня")
async def show_information(message: Message, state: FSMContext):
    advice = generate_donor_advice(get_daily_weather())
    weather = display_weather(get_daily_weather())
    await message.answer(advice + '\n' + weather)
    await state.clear()


@dp.message(F.text == "❓ Задать вопрос")
async def show_information(message: Message, state: FSMContext):
    await message.answer("Напишите ваш вопрос.")
    await state.set_state(Questions.waiting_for_question)


@dp.message(Questions.waiting_for_question)
async def waiting_for_questions(message: Message, state: FSMContext):
    question = message.text
    uid = get_user(message.from_user.id).Id
    add_question(uid, question)
    await state.clear()
    await message.answer("Спасибо за вопрос! Наши админы ответят в ближайшее время.",
                         reply_markup=get_main_menu_keyboard())


@dp.message(F.text == "Ответы на ваши вопросы")
async def show_profile(message: Message, state: FSMContext):
    #Возвращает 408,409
    y = get_questions_by_user(get_user(message.from_user.id).Id)
    k=1
    for i in y:
        if (i.HasReply == 1) and (i.IsSeen == 0):
            await message.answer(str(k)+"\n"+i.Answer, reply_markup=get_main_menu_keyboard())
            k+=1
            #print(get_question(x).Id, get_question(x).Uid, get_question(x).QuestionMsg, get_question(x).HasReply, get_question(x).IsSeen, get_question(x).Answer)
    await state.clear()


@dp.message(Command('menu'))
async def another_menu_handler(message: Message):
    await message.answer(
        text='Выбери действие:',
        reply_markup=get_main_menu_keyboard()
    )
