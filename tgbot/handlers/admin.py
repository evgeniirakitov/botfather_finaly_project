import re
from typing import List

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from tgbot.keyboards.inline import create_admin_start_keyboard
from tgbot.models.commands import user_commands, referrals_commands


async def admin_start_deeplink(message: Message):
    name = message.from_user.first_name
    referrer = int(message.get_args())
    if await user_commands.select_user(referrer) is None:
        await message.answer("Вы ввели не корректный код приглашения!")
    else:
        await user_commands.update_user(referrer, balance=10)
        if await user_commands.select_user(message.from_user.id) is None:
            await user_commands.add_user(
                id=message.from_user.id,
                name=message.from_user.full_name,
                email="",
                balance=0,
                user_name=message.from_user.username,
                referrer=referrer
            )
        referrals = list(map(str, await referrals_commands.select_referrals(referrer)))
        print(f"{referrals=}")

        await message.answer(text=f"Hello, {name}! Приветствую тебя в нашем магазине\n"
                                  f"Ты админ, и тебе доступна админ панель по кнопке \"Админка\"",
                             reply_markup=create_admin_start_keyboard())


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start_deeplink, CommandStart(deep_link=re.compile(r"^[0-9]{3,7}$")), state="*",
                                is_admin=True)
