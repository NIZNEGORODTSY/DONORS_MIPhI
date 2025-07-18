from aiogram import Bot, Dispatcher
from aiogram.types import Message, BotCommand
from aiogram.filters import Command
import logging
import asyncio
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import config.reader as reader

reader.read_config()

TOKEN = reader.get_param_value('token')

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(f"Привет, {message.from_user.id}! Я твой новый Telegram-бот! 🚀")

@dp.message(Command('menu'))
async def menu_handler(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text='Наш сайт', url='https://google.com')
    builder.button(text='Связаться в Telegram', url='https://google.com')
    await message.answer(
        text='Выбери действие:',
        reply_markup=builder.as_markup()
    )

@dp.message(Command('another_menu'))
async def another_menu_handler(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.button(text='Наш сайт', url='https://google.com')
    builder.button(text='Связаться в Telegram', url='https://google.com')
    await message.answer(
        text='Выбери действие:',
        reply_markup=builder.as_markup()
    )


async def main():
    await bot.set_my_commands([
        BotCommand(command='start', description='Приветствие'),
        BotCommand(command='menu', description='Меню'),
        BotCommand(command='another_menu', description='Другое меню')
    ])
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())