from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

events_db = [
    {"date": "15.08.2023", "blood_center": "ЦК №1"},
    {"date": "20.08.2023", "blood_center": "ЦК №2"}
]


def get_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="👤 Мой профиль"))
    builder.add(KeyboardButton(text="📅 Ближайшие ДД"))
    builder.add(KeyboardButton(text="ℹ️ О донорстве"))
    builder.add(KeyboardButton(text="❓ Задать вопрос"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_donor_types():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Студент"))
    builder.add(KeyboardButton(text="Сотрудник"))
    builder.add(KeyboardButton(text="Внешний донор"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_consent_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="✅ Даю согласие"))
    builder.add(KeyboardButton(text="❌ Отказаться"))
    return builder.as_markup(resize_keyboard=True)

def get_yes_no_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Да"))
    builder.add(KeyboardButton(text="Нет"))
    return builder.as_markup(resize_keyboard=True)

def get_events_keyboard():
    builder = InlineKeyboardBuilder()
    for event in events_db:
        builder.add(InlineKeyboardButton(
            text=f"{event['date']} - {event['blood_center']}",
            callback_data=f"event_{event['date']}"
        ))
    builder.adjust(1)
    return builder.as_markup()