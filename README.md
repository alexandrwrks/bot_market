# SportMarket Bot (MVP)

Telegram-бот для продажи спортивного питания.

## Стек
- Python 3.11+
- aiogram v3
- SQLAlchemy v2
- pydantic v2
- Alembic
- Docker

## Запуск
1. Создать и активировать виртуальное окружение:
```bash
uv init
```
2. Установить зависимости:
```bash
uv sync
```
3. Создать `.env` в корне:
```env
BOT_TOKEN=bot_token
SQLITE_DATABASE_URL=sqlite_url

DB_HOST=db_host
DB_PORT=db_port
DB_USER=db_user_name
DB_PASSWORD=db_password
DB_NAME=db_name

REDIS_HOST=redis_host
REDIS_PORT=redis_port

ADMIN_IDS=list_of_user_ids
```
4. Запустить бота:
```bash
python -m crm.main
```

## Базовый пользовательский сценарий MVP
1. `/start`
2. Открыть каталог
3. Выбрать категорию
4. Выбрать товар → написать количество
5. Добавить товар в корзину
6. Открыть корзину
7. Нажать "Оформить заказ"
8. Открыть раздел "Заказы"
