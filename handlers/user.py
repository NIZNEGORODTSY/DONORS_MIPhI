import re
from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

from keybord.user import events_db
from keybord.user import get_consent_keyboard
from keybord.user import get_donor_types
from keybord.user import get_events_keyboard
from keybord.user import get_main_menu
from keybord.user import get_yes_no_keyboard

donors_db = {}

questions_db = []
user_sessions = {}  # Для хранения временных данных пользователей

dp = Router()

# Классы состояний
class Registration(StatesGroup):
    phone = State()
    full_name = State()
    donor_type = State()
    group_number = State()
    consent = State()

class Question(StatesGroup):
    text = State()

class EventRegistration(StatesGroup):
    date = State()
    confirm = State()

# Клавиатуры


# Хэндлеры


@dp.message(Registration.phone, F.contact)
async def process_phone(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Пожалуйста, отправьте ваш номер телефона с помощью кнопки.")
        return
    
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    
    # Сохраняем номер в сессии пользователя
    user_sessions[message.from_user.id] = {"phone": phone}
    
    # Проверяем, есть ли пользователь в базе
    if phone in donors_db:
        donor = donors_db[phone]
        await message.answer(
            f"Мы вас узнали! Это вы: {donor['full_name']}?",
            reply_markup=get_yes_no_keyboard()
        )
        await state.set_state(Registration.consent)
    else:
        await message.answer(
            "Введите ваше ФИО полностью (например: Иванов Иван Иванович):",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(Registration.full_name)

@dp.message(Registration.full_name)
async def process_full_name(message: Message, state: FSMContext):
    # Валидация ФИО
    if not re.fullmatch(r'^[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+\s[А-ЯЁ][а-яё]+$', message.text):
        await message.answer("Пожалуйста, введите ФИО в правильном формате (например: Иванов Иван Иванович):")
        return
    
    await state.update_data(full_name=message.text)
    await message.answer(
        "Выберите вашу категорию:",
        reply_markup=get_donor_types()
    )
    await state.set_state(Registration.donor_type)

@dp.message(Registration.donor_type, F.text.in_(["Студент", "Сотрудник", "Внешний донор"]))
async def process_donor_type(message: Message, state: FSMContext):
    await state.update_data(donor_type=message.text)
    
    if message.text == "Студент":
        await message.answer("Введите номер вашей учебной группы:")
        await state.set_state(Registration.group_number)
    else:
        await message.answer(
            "Пожалуйста, подтвердите согласие на обработку персональных данных и получение рассылки:",
            reply_markup=get_consent_keyboard()
        )
        await state.set_state(Registration.consent)

@dp.message(Registration.group_number)
async def process_group_number(message: Message, state: FSMContext):
    await state.update_data(group_number=message.text)
    await message.answer(
        "Пожалуйста, подтвердите согласие на обработку персональных данных и получение рассылки:",
        reply_markup=get_consent_keyboard()
    )
    await state.set_state(Registration.consent)

@dp.message(Registration.consent, F.text == "✅ Даю согласие")
async def process_consent_yes(message: Message, state: FSMContext):
    data = await state.get_data()
    phone = data['phone']
    
    # Сохраняем донора в "базу"
    donors_db[phone] = {
        "full_name": data.get('full_name'),
        "donor_type": data['donor_type'],
        "group_number": data.get('group_number', None),
        "donations": [],
        "bmd_registry": False,
        "consent": True,
        "user_id": message.from_user.id  # Добавляем ID пользователя
    }
    
    await message.answer(
        "Регистрация завершена! Теперь вы можете пользоваться всеми функциями бота.",
        reply_markup=get_main_menu()
    )
    await state.clear()

@dp.message(Registration.consent, F.text == "❌ Отказаться")
async def process_consent_no(message: Message, state: FSMContext):
    await message.answer(
        "Вы отказались от обработки персональных данных. Бот не может работать без вашего согласия.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()

@dp.message(F.text == "👤 Мой профиль")
async def show_profile(message: Message):
    # Получаем телефон из сессии пользователя
    user_data = user_sessions.get(message.from_user.id, {})
    phone = user_data.get("phone")
    
    if not phone or phone not in donors_db:
        await message.answer("Вы не зарегистрированы. Нажмите /start для регистрации.")
        return
    
    donor = donors_db[phone]
    last_donation = donor['donations'][-1] if donor['donations'] else None
    
    profile_text = (
        f"👤 <b>Ваш профиль</b>\n\n"
        f"ФИО: {donor['full_name']}\n"
        f"Категория: {donor['donor_type']}\n"
    )
    
    if donor['donor_type'] == "Студент":
        profile_text += f"Учебная группа: {donor.get('group_number', 'не указана')}\n"
    
    profile_text += (
        f"Количество донаций: {len(donor['donations'])}\n"
    )
    
    if last_donation:
        profile_text += (
            f"Последняя донация: {last_donation['date']} ({last_donation['blood_center']})\n"
        )
    
    profile_text += (
        f"В регистре ДКМ: {'Да' if donor['bmd_registry'] else 'Нет'}\n\n"
        f"<i>Для просмотра полной истории донаций нажмите кнопку ниже</i>"
    )
    
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📜 История донаций", callback_data="donation_history"))
    
    await message.answer(profile_text, reply_markup=builder.as_markup())

@dp.callback_query(F.data == "donation_history")
async def show_donation_history(callback: types.CallbackQuery):
    # Получаем телефон из сессии пользователя
    user_data = user_sessions.get(callback.from_user.id, {})
    phone = user_data.get("phone")
    
    if not phone or phone not in donors_db:
        await callback.answer("Вы не зарегистрированы.")
        return
    
    donor = donors_db[phone]
    
    if not donor['donations']:
        await callback.answer("У вас еще нет донаций.")
        return
    
    history_text = "📜 <b>Ваша история донаций:</b>\n\n"
    for donation in donor['donations']:
        history_text += f"📅 {donation['date']} - {donation['blood_center']}\n"
    
    await callback.message.answer(history_text)

@dp.message(F.text == "📅 Ближайшие ДД")
async def show_upcoming_events(message: Message):
    if not events_db:
        await message.answer("На данный момент нет запланированных донорских дней.")
        return
    
    events_text = "📅 <b>Ближайшие донорские дни:</b>\n\n"
    for event in events_db:
        events_text += f"📌 {event['date']} - {event['blood_center']}\n"
    
    events_text += "\nВыберите дату для регистрации:"
    
    await message.answer(events_text, reply_markup=get_events_keyboard())

@dp.callback_query(F.data.startswith("event_"))
async def register_for_event(callback: types.CallbackQuery, state: FSMContext):
    date = callback.data.split("_")[1]
    
    # Получаем телефон из сессии пользователя
    user_data = user_sessions.get(callback.from_user.id, {})
    phone = user_data.get("phone")
    
    if not phone or phone not in donors_db:
        await callback.answer("Вы не зарегистрированы.")
        return
    
    donor = donors_db[phone]
    
    if donor['donor_type'] == "Внешний донор":
        await callback.message.answer(
            "Для внешних доноров требуется дополнительная регистрация. "
            "Пожалуйста, пройдите по ссылке: https://example.com/registration",
            reply_markup=get_main_menu()
        )
    else:
        await state.update_data(date=date)
        await callback.message.answer(
            f"Вы хотите зарегистрироваться на {date}?",
            reply_markup=get_yes_no_keyboard()
        )
        await state.set_state(EventRegistration.confirm)
    await callback.answer()

@dp.message(EventRegistration.confirm, F.text == "Да")
async def confirm_event_registration(message: Message, state: FSMContext):
    data = await state.get_data()
    date = data['date']
    
    # Получаем телефон из сессии пользователя
    user_data = user_sessions.get(message.from_user.id, {})
    phone = user_data.get("phone")
    
    if phone and phone in donors_db:
        # Добавляем запись о регистрации
        event = next((e for e in events_db if e['date'] == date), None)
        if event:
            donors_db[phone]['donations'].append({
                "date": date,
                "blood_center": event['blood_center'],
                "completed": False  # Пометка о том, что донор еще не явился
            })
    
    await message.answer(
        f"Вы успешно зарегистрированы на {date}!",
        reply_markup=get_main_menu()
    )
    await state.clear()

@dp.message(EventRegistration.confirm, F.text == "Нет")
async def cancel_event_registration(message: Message, state: FSMContext):
    await message.answer(
        "Регистрация отменена.",
        reply_markup=get_main_menu()
    )
    await state.clear()

@dp.message(F.text == "ℹ️ О донорстве")
async def show_info_menu(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🧑‍⚕️ О донорстве крови", callback_data="info_blood"))
    builder.add(InlineKeyboardButton(text="🦴 О донорстве костного мозга", callback_data="info_bmd"))
    builder.add(InlineKeyboardButton(text="🏫 О донациях в МИФИ", callback_data="info_mifi"))
    builder.adjust(1)
    
    await message.answer(
        "ℹ️ <b>Информация о донорстве:</b>\n\n"
        "Выберите интересующий вас раздел:",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith("info_"))
async def show_info(callback: types.CallbackQuery):
    info_type = callback.data.split("_")[1]
    
    if info_type == "blood":
        text = (
            "🧑‍⚕️ <b>О донорстве крови:</b>\n\n"
            "Донорство крови — это добровольная сдача крови и её компонентов для последующего "
            "переливания нуждающимся больным или получения медицинских препаратов.\n\n"
            "<b>Требования к донору:</b>\n"
            "- Возраст от 18 лет\n"
            "- Вес более 50 кг\n"
            "- Отсутствие противопоказаний\n\n"
            "<b>Подготовка к донации:</b>\n"
            "- За 2 дня исключить алкоголь\n"
            "- Накануне хорошо выспаться\n"
            "- Утром легкий завтрак\n"
            "- Пить больше жидкости"
        )
    elif info_type == "bmd":
        text = (
            "🦴 <b>О донорстве костного мозга:</b>\n\n"
            "Донорство костного мозга — это возможность спасти жизнь человеку с заболеваниями "
            "кроветворной системы.\n\n"
            "<b>Процесс вступления в регистр:</b>\n"
            "1. Сдача пробирки крови на типирование\n"
            "2. Внесение данных в Национальный регистр\n"
            "3. Ожидание совпадения с пациентом\n\n"
            "<b>Процедура донации:</b>\n"
            "- Может быть выполнена через периферические вены (80% случаев)\n"
            "- Или путем пункции тазовой кости под наркозом"
        )
    elif info_type == "mifi":
        text = (
            "🏫 <b>О донациях в МИФИ:</b>\n\n"
            "В НИЯУ МИФИ регулярно проводятся донорские дни с привлечением "
            "сотрудников и студентов.\n\n"
            "<b>Процесс донации:</b>\n"
            "1. Регистрация через бота или на месте\n"
            "2. Анкетирование и медосмотр\n"
            "3. Сдача крови (около 15 минут)\n"
            "4. Отдых и легкий перекус\n\n"
            "Ближайший ДД: 15.08.2023 в ЦК №1"
        )
    
    await callback.message.answer(text, reply_markup=get_main_menu())
    await callback.answer()

@dp.message(F.text == "❓ Задать вопрос")
async def start_question(message: Message, state: FSMContext):
    await message.answer(
        "Напишите ваш вопрос организаторам:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(Question.text)

@dp.message(Question.text)
async def process_question(message: Message, state: FSMContext):
    # Получаем телефон из сессии пользователя
    user_data = user_sessions.get(message.from_user.id, {})
    phone = user_data.get("phone")
    
    if phone and phone in donors_db:
        donor_name = donors_db[phone]['full_name']
    else:
        donor_name = "Анонимный пользователь"
    
    # Сохраняем вопрос
    questions_db.append({
        "user_id": message.from_user.id,
        "user_name": donor_name,
        "phone": phone,
        "text": message.text,
        "date": datetime.now().strftime("%d.%m.%Y %H:%M")
    })
    
    await message.answer(
        "Ваш вопрос отправлен организаторам. Ответ придет вам в этом чате.",
        reply_markup=get_main_menu()
    )
    await state.clear()