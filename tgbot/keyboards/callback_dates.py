from aiogram.utils.callback_data import CallbackData

admin_callback = CallbackData("admin")

referral_callback = CallbackData("referer", "status")

select_item_callback = CallbackData("select_item")

basket_callback = CallbackData("basket")

add_item_callback = CallbackData("add_item")
delete_item_callback = CallbackData("delete_item")

buy_item_callback = CallbackData("buy_item", "item_id")

confirm_buying_callback_balance = CallbackData("confirm_buying_balance")
confirm_buying_callback_you_kasa = CallbackData("confirm_buying_you_kasa")

confirm_cancel_adding = CallbackData("confirm_cancel_adding")
