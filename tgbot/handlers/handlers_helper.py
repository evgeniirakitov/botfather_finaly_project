from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_dates import buy_item_callback
from tgbot.models.commands import user_commands, item_commands


async def user_with_deeplink(message: types.Message):
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


async def show_item(message: types.Message):
    if await user_commands.select_user(message.from_user.id) is not None:
        item_id = int(message.get_args().split("item")[-1])
        item = await item_commands.select_item(item_id)
        await message.answer_photo(
            photo=item.photo_url,
            caption=f"📫 Артикул: <b>{item.id}</b>\n"
                    f"📌 Название: <b>{item.name}</b>\n"
                    f"💎 Количество: <b>{item.quantity}</b>\n"
                    f"📝 Описание: <b>{item.description}</b>\n"
                    f"💵 Цена: <b>{item.price}</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Купить товар",
                            callback_data=buy_item_callback.new(item_id=item.id),
                        )
                    ]
                ]
            )
        )
    else:
        await message.answer(
            text=f"Пожалуйста зарегестрируйтесь в боте, "
                 f"Введя команду \"\\start\" и код приглашения,"
                 f"либо посетите канал <a href=\"https://t.me/jkl\">Канал</a>",
        )
