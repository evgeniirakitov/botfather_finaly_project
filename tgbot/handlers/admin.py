import logging
import re

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from tgbot.keyboards.inline import create_admin_start_keyboard, create_start_not_referer_keyboard


async def admin_start_deeplink(message: Message):
    name = message.from_user.first_name
    referer = message.get_args()
    await message.answer(text=f"Hello, {name}! Приветствую тебя в нашем магазине\n"
                              f"Ты админ, и тебе доступна админ панель по кнопке \"Админка\"",
                         reply_markup=create_admin_start_keyboard())


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start_deeplink, CommandStart(deep_link=re.compile(r"^[0-9]{3,7}$")), state="*",
                                is_admin=True)
