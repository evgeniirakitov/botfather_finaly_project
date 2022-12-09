from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link
from aiogram.utils.markdown import hcode

from tgbot.misc.states import OurState
from tgbot.keyboards.callback_dates import referer_callback


async def create_deeplink(call: types.CallbackQuery):
    await call.answer("Введите код приглашения")

    await OurState.Unauthorized.set()


async def send_deeplink(message: types.Message, state: FSMContext):
    code = message.text
    link = await get_start_link(payload=code)
    if code:
        await message.answer(f"Перейдите по ссылке {link}")
    else:
        await message.answer("Вы не ввели код приглашения")

    await state.reset_state()


def register_echo(dp: Dispatcher):
    dp.register_callback_query_handler(create_deeplink, referer_callback.filter(status="code"))
    dp.register_message_handler(send_deeplink, state=OurState.Unauthorized, content_types=types.ContentTypes.ANY)
