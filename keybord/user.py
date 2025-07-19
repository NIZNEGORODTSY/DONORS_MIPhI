from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


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
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="📋 Мои данные"))
    builder.add(KeyboardButton(text="📅 Записаться на донацию"))
    builder.add(KeyboardButton(text="ℹ️ Информация о донорстве"))
    builder.add(KeyboardButton(text="🌤 Погодные советы"))
    builder.add(KeyboardButton(text="❓ Задать вопрос"))
    builder.add(KeyboardButton(text="Ответы на ваши вопросы"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_auth_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔐Аутентификация")]
        ],
        resize_keyboard=True
    )


def get_phone_number_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱Поделиться номером",
                            request_contact=True)]
        ],
        resize_keyboard=True
    )


def get_detailed_information():
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="Требования к донорам"))
    builder.add(KeyboardButton(text="Подготовка к донации"))
    builder.add(KeyboardButton(text="Рацион донора"))
    builder.add(KeyboardButton(text="Абсолютные противопоказания"))
    builder.add(KeyboardButton(text="Временные противопоказания"))
    builder.add(KeyboardButton(text="Важность ДКМ"))
    builder.add(KeyboardButton(text="Как вступить в регистр ДКМ"))
    builder.add(KeyboardButton(text="Процедура донации"))
    builder.add(KeyboardButton(text="Процедура сдачи крови в МИФИ"))
    builder.add(KeyboardButton(text="🔙Вернуться в меню"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
