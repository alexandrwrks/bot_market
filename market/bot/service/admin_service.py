from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from market.bot.config import settings
from market.utils import logger


class AdminNotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def notify_new_order(self, order, user) -> None:
        text = (
            "🛒 <b>Новый заказ</b>\n\n"
            f"ID заказа: <code>{order.id}</code>\n"
            f"Пользователь: {user.full_name}\n"
            f"Telegram ID: <code>{user.telegram_id}</code>\n"
            f"Телефон: {order.phone}\n"
            f"Сумма: {order.total_price} ₽"
        )

        for admin_id in settings.ADMIN_IDS:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=text,
                    parse_mode="HTML",
                )

            except TelegramAPIError:
                logger.exception("Ошибка отправки сообщений админам")
