import logging
import typing

from aiogram import types, Dispatcher
from aiogram.types import InlineQueryResultArticle, InlineKeyboardButton, MessageEntity

from tgbot.models.commands import item_commands
from tgbot.models.table import Item


async def empty_query(query: types.InlineQuery):
    items = await item_commands.select_all_items()
    await query.answer(
        results=create_list_item(items),
        cache_time=1
    )


async def select_items(query: types.InlineQuery):
    items = await item_commands.select_items_by_name(query.query)

    await query.answer(
        results=create_list_item(items),
        cache_time=5
    )


def register_inline_query(dp: Dispatcher):
    dp.register_inline_handler(empty_query, text="")
    dp.register_inline_handler(select_items)


def create_list_item(item_list: list[Item]):
    result = [types.InlineQueryResultArticle(
        id=item.id,
        title=item.name,
        thumb_url=item.photo_url,
        description=item.description,
        input_message_content=types.InputMessageContent(
            message_text=f"<i src=\"{item.photo_url}\" alt=\"Эйфелева башня\" title=\"Эйфелева башня\"/>",
            parse_mode="HTML",
        ),
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Regbnm",
                        url="https://t.me/joinchat",
                    )
                ]
            ]
        )
    ) for item in item_list
    ]

    return result
