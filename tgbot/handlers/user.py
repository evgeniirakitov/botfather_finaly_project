import logging
import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery, LabeledPrice, ShippingQuery, PreCheckoutQuery

from tgbot.handlers import handlers_helper
from tgbot.keyboards.callback_dates import referral_callback, buy_item_callback, confirm_buying_callback_balance, \
    confirm_buying_callback_you_kasa
from tgbot.keyboards.inline import create_start_not_referer_keyboard, create_user_start_keyboard, \
    create_confirm_buying_keyboard
from tgbot.misc.states import Purchase
from tgbot.models.commands import item_commands, user_commands
from tgbot.models.invoice import Invoice
from tgbot.models.table import Item


async def user_start(message: Message):
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
                             reply_markup=create_user_start_keyboard())


async def user_start_deeplink(message: Message):
    name = message.from_user.first_name
    await handlers_helper.user_with_deeplink(message)
    await message.answer(text=f"Hello, {name}!\n"
                              f" Приветствую тебя в нашем магазине",
                         reply_markup=create_user_start_keyboard())


async def show_item(message: Message):
    await handlers_helper.show_item(message)


async def show_referrals(call: CallbackQuery):
    user_id = int(call.from_user.id)
    referrals = await user_commands.select_referrals(user_id)
    count_referrals = len(referrals)
    balance = await user_commands.get_balance(user_id)
    message = f"Имя = "
    for item in referrals:
        message = message.join(f"{item.name}\n")
        message = message.join(f"User_name = {item.user_name}")

    await call.message.answer(
        text=f"У Вас {count_referrals} рефералов \n"
             f"Ваш реферальный баланс равен {balance}"
    )


async def buy_item(call: CallbackQuery, state: FSMContext):
    data = call.data.split(":")[-1]
    logging.info(f"data = {data}")
    item = await item_commands.select_item(int(data))
    bot = call.message.bot
    cid = call.message.chat.id
    mid = call.message.message_id
    await call.message.answer("✏️ Укажите колличество товара")
    await Purchase.Quantity.set()
    await state.update_data(item=item)


async def enter_quantity_item(message: Message, state: FSMContext):
    data = await state.get_data()
    item: Item = data.get("item")
    logging.info(f"data_quantity = {data}")
    try:
        client_quantity = int(message.text)
        if client_quantity > item.quantity:
            await message.answer(text=f"❌ Ошибка!\n"
                                      f"📝 Не хватает товара на складе\n"
                                      f"В наличии {item.quantity} шт")
            return
        await message.answer(text=f"Укажите адрес доставки\n"
                                  f"Город, улицу, дом")

        await Purchase.Shipping.set()
        await state.update_data(item=item)


    except ValueError:
        await message.answer(text=f"❌ Ошибка!\n"
                                  f"📝 Укажите верное количество товара")
        return


async def enter_shipping(message: Message, state: FSMContext):
    data = await state.get_data()
    item: Item = data.get("item")
    client_shipping = message.text
    logging.info(f"client_shipping: {client_shipping}")
    balance = await user_commands.get_balance(message.from_user.id)
    await message.answer(text=f"✅ Отлично!\n"
                              f"Осталось оплатить товар!\n"
                              f"\n"
                              f"💰 Ваш баланс: {balance} ₽",
                         reply_markup=create_confirm_buying_keyboard()
                         )
    invoice = Invoice(
        title=item.name,
        description=item.description,
        currency="RUB",
        prices=[
            LabeledPrice(
                label=item.name,
                amount=int(item.price * 100)
            )
        ],
        start_parameter=f"create_invoice_{item.id}",
        photo_url=item.photo_url,
    )

    await Purchase.Confirm.set()
    await state.update_data(invoice=invoice)


async def buying_you_kasa(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    invoice: Invoice = data.get("invoice")
    bot = call.message.bot

    await bot.send_invoice(call.message.chat.id, **invoice.generate_invoice(), payload="123456")


async def choose_shipping(query: ShippingQuery):
    bot = query.bot
    await bot.answer_shipping_query(
        shipping_query_id=query.id,
        ok=True
    )


async def process_pre_checkout_query(query: PreCheckoutQuery):
    bot = query.bot
    await bot.answer_pre_checkout_query(
        pre_checkout_query_id=query.id,
        ok=True
    )
    await bot.send_message(chat_id=query.from_user.id, text="Все хорошо, покупка  прошла успешно")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start_deeplink, CommandStart(deep_link=re.compile(r"^[0-9]{3,7}$")), state="*")
    dp.register_message_handler(show_item, CommandStart(deep_link=re.compile(r"^[item]{3,14}")))
    dp.register_message_handler(user_start, CommandStart(), state="*")
    dp.register_callback_query_handler(show_referrals, referral_callback.filter(status="notcode"))
    dp.register_callback_query_handler(buy_item, buy_item_callback.filter())
    dp.register_message_handler(enter_quantity_item, state=Purchase.Quantity)
    dp.register_message_handler(enter_shipping, state=Purchase.Shipping)
    dp.register_callback_query_handler(enter_shipping, confirm_buying_callback_balance.filter(), state=Purchase.Confirm)
    dp.register_callback_query_handler(buying_you_kasa, confirm_buying_callback_you_kasa.filter(),
                                       state=Purchase.Confirm)
    dp.register_shipping_query_handler(choose_shipping)
    dp.register_pre_checkout_query_handler(process_pre_checkout_query)
