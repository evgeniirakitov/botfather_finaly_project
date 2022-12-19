import logging
import typing

from aiogram import types, Dispatcher
from aiogram.types import InlineQueryResultArticle, InlineKeyboardButton, MessageEntity

from tgbot.models.commands import item_commands, user_commands
from tgbot.models.table import Item


async def empty_query(query: types.InlineQuery):
    if await user_commands.select_user(query.from_user.id) is not None:
        items = await item_commands.select_first_two_items()
        await query.answer(
            results=create_list_item(items),
            cache_time=1
        )

    else:
        await query.answer(
            results=[],
            cache_time=5,
            switch_pm_text="Бот не доступен, пожалуйста авторизуйтесь",
            switch_pm_parameter="connect_user"
        )
        return


async def select_items(query: types.InlineQuery):
    if await user_commands.select_user(query.from_user.id) is not None:
        items = await item_commands.select_items_by_name(query.query)

        await query.answer(
            results=create_list_item(items),
            cache_time=5
        )

    else:
        await query.answer(
            results=[],
            cache_time=5,
            switch_pm_text="Бот не доступен, пожалуйста авторизуйтесь",
            switch_pm_parameter="connect_user"
        )
        return


def register_inline_query(dp: Dispatcher):
    dp.register_inline_handler(empty_query, text="")
    dp.register_inline_handler(select_items)


def create_list_item(item_list: list[Item]):
    result = [types.InlineQueryResultArticle(
        id=item.id,
        title=item.name,
        thumb_url=item.photo_url,
        description=f"{item.price} руб",
        input_message_content=types.InputTextMessageContent(
            message_text=f"<a href=\"{item.photo_url}\">ноут</a>",
            parse_mode="HTML"
        ),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Показать товар",
                        url=f"https://t.me/finaly_rakitov_bot?start=item{item.id}"
                    )
                ]
            ]
        )
    ) for item in item_list
    ]

    return result
