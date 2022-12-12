import re

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from tgbot.keyboards.inline import create_start_not_referer_keyboard, create_user_start_keyboard


async def user_start(message: Message):
    name = message.from_user.first_name
    await message.answer(text=f"Привет, {name}! Ты перешел без реферальной ссылки.\n"
                              f"Чтобы изпользовать этого бота, ты можешь ввести код приглашения,\n"
                              f"либо перейти по реферальной ссылке, если она имеется,\n"
                              f"либо подписаться на канал",
                         reply_markup=create_start_not_referer_keyboard())


async def user_start_deeplink(message: Message):
    name = message.from_user.first_name
    referrer = message.get_args()
    await message.answer(text=f"Hello, {name}!\n"
                              f" Приветствую тебя в нашем магазине",
                         reply_markup=create_user_start_keyboard())


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start_deeplink, CommandStart(deep_link=re.compile(r"^[0-9]{3,7}$")), state="*")
    dp.register_message_handler(user_start, CommandStart(), state="*")
