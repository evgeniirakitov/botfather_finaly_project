import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ContentType, InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.handlers import handlers_helper
from tgbot.keyboards.callback_dates import admin_callback, add_item_callback
from tgbot.keyboards.inline import create_admin_start_keyboard, create_admin_panel_keyboard, \
    create_start_not_referer_keyboard
from tgbot.misc.states import NewItem
from tgbot.models.commands import user_commands, referrals_commands, item_commands
from tgbot.models.table import Item


async def admin_start(message: Message):
    name = message.from_user.first_name
    if await user_commands.select_user(int(message.from_user.id)) is None:

        await message.answer(text=f"Привет, {name}! Ты перешел без реферальной ссылки.\n"
                                  f"Чтобы изпользовать этого бота, ты можешь ввести код приглашения,\n"
                                  f"либо перейти по реферальной ссылке, если она имеется,\n"
                                  f"либо подписаться на канал",
                             reply_markup=create_start_not_referer_keyboard())

    else:
        await message.answer(text=f"Hello, {name}!\n"
                                  f" Приветствую тебя в нашем магазине",
                             reply_markup=create_admin_start_keyboard())


async def admin_start_deeplink(message: Message):
    name = message.from_user.first_name
    await handlers_helper.user_with_deeplink(message)
    await message.answer(text=f"Hello, {name}! Приветствую тебя в нашем магазине\n"
                              f"Ты админ, и тебе доступна админ панель по кнопке \"Админка\""
                              f"Также ты можешь посмотреть своих рефералов по кнопке \"Рефералка\"",
                         reply_markup=create_admin_start_keyboard())


async def show_item(message: Message):
    await handlers_helper.show_item(message)


async def admin_panel(call: CallbackQuery):
    bot = call.message.bot
    cid = call.message.chat.id
    mid = call.message.message_id
    await bot.edit_message_text('Выберите действие', cid, mid, reply_markup=create_admin_panel_keyboard())


async def add_item(call: CallbackQuery):
    bot = call.message.bot
    cid = call.message.chat.id
    mid = call.message.message_id
    await bot.edit_message_text("Введите название товара или нажмите /cancel", cid, mid)
    await NewItem.Name.set()


async def enter_name(message: Message, state: FSMContext):
    name = message.text
    item = Item()
    item.name = name
    await message.answer(f"Название {name}\n"
                         f"Пришлите фото товара или нажмите /cancel")
    await NewItem.Photo.set()
    await state.update_data(item=item)


async def enter_photo(message: Message, state: FSMContext):
    photo_url = message.text
    data = await state.get_data()
    item: Item = data.get("item")
    item.photo_url = photo_url
    await message.answer_photo(
        photo=photo_url,
        caption=f"Название: {item.name}\n"
                f"Пришлите мне описание товара, или нажмите /cancel"
    )
    await NewItem.Description.set()
    await state.update_data(item=item)


async def enter_description(message: Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    item: Item() = data.get("item")
    item.description = description
    await message.answer_photo(
        photo=item.photo_url,
        caption=f"Название: {item.name}\n"
                f"Описание: {item.description}\n"
                f"Пришлите мне количество товара, или нажмите /cancel"
    )
    await NewItem.Quantity.set()
    await state.update_data(item=item)


async def enter_quantity(message: Message, state: FSMContext):
    data = await state.get_data()
    item: Item = data.get("item")
    try:
        quantity = int(message.text)
    except ValueError:
        await message.answer("Неверное значение, пришлите число")
        return

    item.quantity = quantity

    await message.answer_photo(
        photo=item.photo_url,
        caption=f"Название: {item.name}\n"
                f"Описание: {item.description}\n"
                f"Колличество: {item.quantity}\n"
                f"Пришлите мне стоимость товара, или нажмите /cancel"
    )
    await NewItem.Price.set()
    await state.update_data(item=item)


async def enter_price(message: Message, state: FSMContext):
    data = await state.get_data()
    item: Item = data.get("item")
    try:
        price = int(message.text)
    except ValueError:
        await message.answer("Неверное значчение, пришлите число")
        return

    item.price = price

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Да",
                callback_data="confirm"
            )],
            [InlineKeyboardButton(
                text="Ввести заново",
                callback_data="change"
            )]
        ]
    )
    await message.answer_photo(
        photo=item.photo_url,
        caption=f"Название: {item.name}\n"
                f"Описание: {item.description}\n"
                f"Колличество: {item.quantity}\n"
                f"Цена: {item.price}\n"
                f"Подтверждаете? Нажмите /cancel, чтобы отменить",
        reply_markup=markup
    )
    await state.update_data(item=item)
    await NewItem.Confirm.set()


async def change_price(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Введите заново цену товара")
    await NewItem.Price.set()


async def confirm_price(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item: Item = data.get("item")
    await item_commands.add_item(item.name, item.description, item.price, item.price, item.photo_url)
    await call.message.answer("Товар удачно создан")

    await state.reset_state()


async def adding_cancel(message: Message, state: FSMContext):
    await message.answer(
        text="Вы отменили создание товара",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="Выйти в главное меню?",
                    url=f"https://t.me/finaly_rakitov_bot?start={message.from_user.id}"
                )]
            ]
        )
    )
    await state.reset_state()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start_deeplink, CommandStart(deep_link=re.compile(r"^[0-9]{3,7}$")), state="*",
                                is_admin=True)
    dp.register_message_handler(show_item, CommandStart(deep_link=re.compile(r"^[item]{3,14}")), is_admin=True)
    dp.register_message_handler(adding_cancel, commands=["cancel"], state=NewItem, is_admin=True)
    dp.register_callback_query_handler(admin_panel, admin_callback.filter(), is_admin=True)
    dp.register_callback_query_handler(add_item, add_item_callback.filter(), is_admin=True)
    dp.register_callback_query_handler(change_price, text_contains="change", state=NewItem.Confirm, is_admin=True)
    dp.register_callback_query_handler(confirm_price, text_contains="confirm", state=NewItem.Confirm, is_admin=True)
    dp.register_message_handler(enter_name, state=NewItem.Name, is_admin=True)
    dp.register_message_handler(enter_photo, state=NewItem.Photo, is_admin=True)
    dp.register_message_handler(enter_description, state=NewItem.Description, is_admin=True)
    dp.register_message_handler(enter_quantity, state=NewItem.Quantity, is_admin=True)
    dp.register_message_handler(enter_price, state=NewItem.Price, is_admin=True)
    dp.register_message_handler(admin_start, CommandStart(), state="*", is_admin=True)
