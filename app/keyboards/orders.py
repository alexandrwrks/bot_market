from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_user_orders():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Заказ номер ...", callback_data="order_btn1")
    keyboard.button(text="Назад", callback_data="back_one_start")

    return keyboard.adjust(1).as_markup()
