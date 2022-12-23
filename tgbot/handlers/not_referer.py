from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link

from tgbot.keyboards.callback_dates import referral_callback
from tgbot.keyboards.inline import create_admin_start_keyboard
from tgbot.misc.states import OurState
from tgbot.models.commands import user_commands


async def create_deeplink(call: types.CallbackQuery):
    bot = call.message.bot
    cid = call.message.chat.id
    mid = call.message.message_id
    await bot.edit_message_text('Введите код приглашения', cid, mid)

    await OurState.Unauthorized.set()


async def send_deeplink(message: types.Message, state: FSMContext):
    code = message.text
    link = await get_start_link(payload=code)
    if await user_commands.select_user(int(code)) is not None:
        await message.answer(text=f"Hello, {message.from_user.first_name}!\n"
                                  f" Приветствую тебя в нашем магазине",
                             reply_markup=create_admin_start_keyboard())
    else:
        await message.answer("Вы ввели не корректный код приглашения")

    await state.reset_state()


def register_echo(dp: Dispatcher):
    dp.register_callback_query_handler(create_deeplink, referral_callback.filter(status="code"))
    dp.register_message_handler(send_deeplink, state=OurState.Unauthorized, content_types=types.ContentTypes.ANY)
