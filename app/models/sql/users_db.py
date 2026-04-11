import aiosqlite

from aiogram.types import User as TgUser
from app.models.sql.config_db import logger, DATA_BASE_NAME

class UsersManager:
    def __init__(self):
        self.db_name = DATA_BASE_NAME

    async def init_db(self):
        try:
            async with aiosqlite.connect(self.db_name) as db:
                # telegram_id = id пользователя из Telegram
                await db.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             telegram_id INTEGER UNIQUE NOT NULL,
                             first_name TEXT,
                             last_name TEXT,
                             is_active BOOLEAN DEFAULT TRUE,
                             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                """)

                await db.commit()

        except aiosqlite.Error as e:
            logger.error(f"Database error: {e}")

    async def create_user(self, tg_user: TgUser):
        """Добавление пользоватеяля в базу данных"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("""
                    INSERT INTO Users (telegram_id, first_name, last_name, updated_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP) 
                """, (
                    tg_user.id,
                    tg_user.first_name,
                    tg_user.last_name
                ))

                await db.commit()

        except aiosqlite.IntegrityError as e:
            logger.error(f"Unique error: {e}")

        except aiosqlite.Error as e:
            logger.error(f"Error: {e}")

    async def exists_user_by_telegram_id(self, telegram_id: int) -> bool:
        """Проверка существует ли пользоваетль в БД"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                cursor = await db.execute("SELECT telegram_id FROM Users WHERE telegram_id = ?", (telegram_id,))

                result = await cursor.fetchone()

                """Возращаем True если пользоваетель есть в БД, иначе"""
                return True if result else False

        except aiosqlite.Error as e:
            logger.error(f"Ошибка чтения данных: {e}")

    async def update_user(self, tg_user: TgUser):
        """Обновление данных пользователя"""
        try:
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute("UPDATE Users SET first_name = ?, last_name = ?, updated_at = CURRENT_TIMESTAMP WHERE telegram_id = ?", 
                                 (tg_user.first_name, tg_user.last_name, tg_user.id)
                                 )

                await db.commit()

        except aiosqlite.Error as e:
            logger.error(f"Ошибка обновления данных: {e}")


users_manager = UsersManager()