from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder



def get_organizer_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="📝 Добавить донора"))
    builder.add(KeyboardButton(text="📊 Статистика"))
    builder.add(KeyboardButton(text="📅 Создать мероприятие"))
    builder.add(KeyboardButton(text="❓ Вопросы от пользователей"))
    builder.add(KeyboardButton(text="📢 Рассылка"))
    builder.add(KeyboardButton(text="📄 Редактировать информацию"))
    builder.add(KeyboardButton(text="📁 Загрузить статистику"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_donor_type_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Внутренний донор"))
    builder.add(KeyboardButton(text="Внешний донор"))
    return builder.as_markup(resize_keyboard=True)

def get_yes_no_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Да"))
    builder.add(KeyboardButton(text="Нет"))
    return builder.as_markup(resize_keyboard=True)

def get_broadcast_categories_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Зарегистрированные на ближайшую дату"))
    builder.add(KeyboardButton(text="Не зарегистрировались на ближайшие даты"))
    builder.add(KeyboardButton(text="Зарегистрировались, но не пришли"))
    builder.add(KeyboardButton(text="Сдавшие пробирку для ДКМ"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def get_info_sections_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="О донорстве"))
    builder.add(KeyboardButton(text="Как подготовиться"))
    builder.add(KeyboardButton(text="Частые вопросы"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)