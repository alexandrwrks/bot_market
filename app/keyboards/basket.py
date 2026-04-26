from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_user_basket():
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="Состав корзины", callback_data="basket_composition_btn")
    keyboard.button(text="Очистить", callback_data="clear_btn")
    keyboard.button(text="Каталог", callback_data="catalog_btn")
    keyboard.button(text="Оформить заказ", callback_data="confirm_order_btn")

    return keyboard.adjust(1, 2, 1).as_markup()
