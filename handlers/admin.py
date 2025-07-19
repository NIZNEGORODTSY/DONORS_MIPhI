from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import pandas as pd
import io

from keybord.admin import get_broadcast_categories_keyboard
from keybord.admin import get_info_sections_keyboard
from keybord.admin import get_organizer_keyboard
from keybord.admin import get_donor_type_keyboard
from keybord.admin import get_yes_no_keyboard

from core import add_donor

from keybord.user import choose_group

donors_db = []
events_db = []
questions_db = []

dp = Router()


class DonorForm(StatesGroup):
    full_name = State()
    uggroup = State()
    student_group = State()
    event_date = State()


class EventForm(StatesGroup):
    date = State()
    blood_center = State()


class AnswerForm(StatesGroup):
    question_id = State()
    answer = State()


class BroadcastForm(StatesGroup):
    category = State()
    message = State()


class EditInfoForm(StatesGroup):
    section = State()
    new_text = State()


@dp.message(F.text == "📝 Добавить донора")
async def add_donor_start(message: Message, state: FSMContext):
    await message.answer("Выберите способ добавления:", reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить вручную"), KeyboardButton(text="Загрузить список")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard=True
    ))


@dp.message(F.text == "Добавить вручную")
async def add_donor_manually(message: Message, state: FSMContext):
    await state.set_state(DonorForm.full_name)
    await message.answer("Введите ФИО донора:", reply_markup=types.ReplyKeyboardRemove())


@dp.message(DonorForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(DonorForm.uggroup)
    await message.answer("Выберите тип донора:", reply_markup=choose_group())


@dp.message(DonorForm.uggroup, F.text.in_(["💼Сотрудник", "🤲Внешний донор", "🎓Студент"]))
async def process_donor_type(message: Message, state: FSMContext):
    text = message.text
    if text == "💼Сотрудник":
        await state.update_data(donor_type='Сотрудник')
        await message.answer("Зарегистрирован ли в ДКМ?")
        await state.set_state(DonorForm.event_date)
    elif text == "🤲Внешний донор":
        await state.update_data(donor_type='Внешний донор')
        await message.answer("Зарегистрирован ли в ДКМ?")
        await state.set_state(DonorForm.event_date)
    elif text == '🎓Студент':
        await message.answer("Напишите номер вашей группы")
        await state.set_state(DonorForm.student_group)
    

@dp.message(DonorForm.student_group)
async def student_group(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(donor_type=text)
    await message.answer("Зарегистрирован ли в ДКМ?")
    await state.set_state(DonorForm.event_date)


@dp.message(DonorForm.event_date)
async def process_event_date(message: Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    add_donor(data['full_name'], data['donor_type'], text)
    await message.answer(f"Донор успешно добавлен!", reply_markup=get_organizer_keyboard())
    await state.clear()


@dp.message(F.text == "📅 Создать мероприятие")
async def create_event_start(message: Message, state: FSMContext):
    await state.set_state(EventForm.date)
    await message.answer("Введите дату мероприятия (в формате ДД.ММ.ГГГГ):", reply_markup=types.ReplyKeyboardRemove())


@dp.message(EventForm.date)
async def process_event_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(EventForm.blood_center)
    await message.answer("Введите название центра крови:")


@dp.message(EventForm.blood_center)
async def process_event_blood_center(message: Message, state: FSMContext):
    data = await state.update_data(blood_center=message.text)
    await state.clear()

    # Сохраняем мероприятие в "базу"
    events_db.append(data)

    await message.answer(f"Мероприятие на {data['date']} в {data['blood_center']} создано!",
                         reply_markup=get_organizer_keyboard())


@dp.message(F.text == "❓ Вопросы от пользователей")
async def show_questions(message: Message):
    if not questions_db:
        await message.answer("Нет новых вопросов.")
        return

    for i, question in enumerate(questions_db):
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="Ответить", callback_data=f"answer_{i}"))
        await message.answer(f"Вопрос #{i + 1}:\n{question['text']}", reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith("answer_"))
async def answer_question(callback: types.CallbackQuery, state: FSMContext):
    question_id = int(callback.data.split("_")[1])
    await state.set_state(AnswerForm.answer)
    await state.update_data(question_id=question_id)
    await callback.message.answer("Введите ваш ответ:")


@dp.message(AnswerForm.answer)
async def process_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    question_id = data['question_id']
    answer = message.text

    # Здесь должен быть код для отправки ответа пользователю
    question = questions_db[question_id]
    await message.answer(f"Ответ на вопрос от {question['user']} отправлен!")

    # Удаляем вопрос из списка
    questions_db.pop(question_id)
    await state.clear()


@dp.message(F.text == "📢 Рассылка")
async def start_broadcast(message: Message, state: FSMContext):
    await state.set_state(BroadcastForm.category)
    await message.answer("Выберите категорию для рассылки:", reply_markup=get_broadcast_categories_keyboard())


@dp.message(BroadcastForm.category)
async def process_broadcast_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(BroadcastForm.message)
    await message.answer("Введите сообщение для рассылки:", reply_markup=types.ReplyKeyboardRemove())


@dp.message(BroadcastForm.message)
async def process_broadcast_message(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data['category']

    # Здесь должен быть код для реальной рассылки
    # Временно просто показываем результат
    await message.answer(f"Рассылка для категории '{category}' выполнена!\nСообщение: {message.text}")
    await state.clear()


@dp.message(F.text == "📄 Редактировать информацию")
async def edit_info_start(message: Message, state: FSMContext):
    await state.set_state(EditInfoForm.section)
    await message.answer("Выберите раздел для редактирования:", reply_markup=get_info_sections_keyboard())


@dp.message(EditInfoForm.section)
async def process_info_section(message: Message, state: FSMContext):
    await state.update_data(section=message.text)
    await state.set_state(EditInfoForm.new_text)
    await message.answer(f"Введите новый текст для раздела '{message.text}':", reply_markup=types.ReplyKeyboardRemove())


@dp.message(EditInfoForm.new_text)
async def process_new_info_text(message: Message, state: FSMContext):
    data = await state.get_data()
    section = data['section']

    # Здесь должен быть код для сохранения новой информации
    await message.answer(f"Раздел '{section}' успешно обновлен!", reply_markup=get_organizer_keyboard())
    await state.clear()


@dp.message(F.text == "📁 Загрузить статистику")
async def upload_stats(message: Message):
    await message.answer("Пожалуйста, загрузите файл Excel со статистикой:")


@dp.message(F.document)
async def handle_document(message: Message):
    doc = message.document
    if doc.file_name.endswith('.xlsx') or doc.file_name.endswith('.xls'):
        await message.answer(f"Файл успешно загружен! Обработано записей.")
    else:
        await message.answer("Пожалуйста, загрузите файл в формате Excel (.xlsx или .xls)")


@dp.message(F.text == "📊 Статистика")
async def show_stats(message: Message):
    await message.answer("https://datalens.yandex/g7boh897u39y1")


@dp.callback_query(F.data == "export_stats")
async def export_stats(callback: types.CallbackQuery):
    # Создаем DataFrame с данными
    data = []
    for donor in donors_db:
        data.append({
            "ФИО": donor['full_name'],
            "Дата акции": donor['event_date'],
            "Центр крови": donor['blood_center'],
            "Тип донора": donor['donor_type'],
            "Сдал кровь": "Да" if donor['donated_blood'] else "Нет",
            "Сдал пробирку": "Да" if donor['donated_tube'] else "Нет"
        })

    df = pd.DataFrame(data)

    # Создаем Excel файл в памяти
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Статистика')

    output.seek(0)

    # Отправляем файл
    await callback.message.answer_document(
        types.BufferedInputFile(output.read(), filename="donor_stats.xlsx"),
        caption="Статистика по донорам"
    )


@dp.message(F.text == "Назад")
async def back_to_menu(message: Message):
    await message.answer("Главное меню:", reply_markup=get_organizer_keyboard())
