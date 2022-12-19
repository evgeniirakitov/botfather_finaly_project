from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tgbot.keyboards.callback_dates import admin_callback, referral_callback, select_item_callback, basket_callback, \
    add_item_callback, delete_item_callback, confirm_buying_callback_balance, confirm_buying_callback_you_kasa


def create_admin_start_keyboard():
    return InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=
                                [
                                    [
                                        InlineKeyboardButton(
                                            text="Админка",
                                            callback_data=admin_callback.new(),
                                        ),
                                        InlineKeyboardButton(
                                            text="Рефералка",
                                            callback_data=referral_callback.new("notcode")
                                        ),
                                    ],
                                    [
                                        InlineKeyboardButton(
                                            text="Корзина",
                                            callback_data=basket_callback.new()
                                        ),
                                        InlineKeyboardButton(
                                            text="Выбрать товар",
                                            switch_inline_query_current_chat=""
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
                                            callback_data=referral_callback.new("notcode")
                                        ),
                                        InlineKeyboardButton(
                                            text="Корзина",
                                            callback_data=basket_callback.new()
                                        )
                                    ],
                                    [
                                        InlineKeyboardButton(
                                            text="Выбрать товар",
                                            switch_inline_query_current_chat=""
                                        )
                                    ]
                                ]
                                )


def create_admin_panel_keyboard():
    return InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=
                                [
                                    [
                                        InlineKeyboardButton(
                                            text="Добавить товар",
                                            callback_data=add_item_callback.new()
                                        ),
                                        InlineKeyboardButton(
                                            text="Удалить товар",
                                            callback_data=delete_item_callback.new()
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


def create_confirm_buying_keyboard():
    return InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=
                                [
                                    [
                                        InlineKeyboardButton(
                                            text="💰 Оплатить с баланса",
                                            callback_data=confirm_buying_callback_balance.new()
                                        ),
                                        InlineKeyboardButton(
                                            text="💳 Оплатить ЮKassa",
                                            callback_data=confirm_buying_callback_you_kasa.new()
                                        )
                                    ],
                                    [
                                        InlineKeyboardButton(
                                            text="Отмена",
                                            switch_inline_query_current_chat=""
                                        )
                                    ]
                                ]
                                )
