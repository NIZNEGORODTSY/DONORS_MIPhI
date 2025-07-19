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
            [KeyboardButton(text="❓ Задать вопрос")]
        ],
        resize_keyboard=True
    )
