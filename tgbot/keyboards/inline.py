from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.callback_dates import start_callback, referer_callback


def create_admin_start_keyboard():
    return InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=
                                [
                                    [
                                        InlineKeyboardButton(
                                            text="Админка",
                                            url="https://t.me/joinchat",
                                        ),
                                        InlineKeyboardButton(
                                            text="Рефералка",
                                            callback_data=start_callback.new()
                                        ),
                                    ],
                                    [
                                        InlineKeyboardButton(
                                            text="Корзина",
                                            callback_data=start_callback.new()
                                        ),
                                        InlineKeyboardButton(
                                            text="Выбрать товар",
                                            callback_data=start_callback.new()
                                        )
                                    ]
                                ]
                                )


def create_user_start_keyboard():
    return InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=
                                [
                                    [
                                        InlineKeyboardButton(
                                            text="Рефералка",
                                            callback_data=start_callback.new()
                                        ),
                                        InlineKeyboardButton(
                                            text="Корзина",
                                            callback_data=start_callback.new()
                                        )
                                    ],
                                    [
                                        InlineKeyboardButton(
                                            text="Выбрать товар",
                                            callback_data=start_callback.new()
                                        )
                                    ]
                                ]
                                )


def create_start_not_referer_keyboard():
    return InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=
                                [
                                    [
                                        InlineKeyboardButton(
                                            text="Подписаться на канал",
                                            url="https://t.me/joinchat"
                                        ),
                                        InlineKeyboardButton(
                                            text="Ввести код",
                                            callback_data="referer:code"
                                        )
                                    ]
                                ]
                                )
