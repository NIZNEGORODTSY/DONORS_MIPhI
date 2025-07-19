from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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
            [KeyboardButton(text="🌤 Рекомендации для доноров на сегодня")],
            [KeyboardButton(text="❓ Задать вопрос")],
            [KeyboardButton(text="Ответы на ваши вопросы")]
        ],
        resize_keyboard=True
    )


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

