# SportMarket Bot (MVP)

Telegram-бот для продажи спортивного питания.

## Стек
- Python 3.11+
- aiogram 3
- SQLAlchemy 2
- python-dotenv

## Запуск
1. Создать и активировать виртуальное окружение.
2. Установить зависимости:
```bash
pip install -r requirements.txt
```
3. Создать `.env` в корне:
```env
BOT_TOKEN=your_telegram_bot_token
SQLITE_DATABASE_URL=sqlite+aiosqlite:///demo.db
```
4. Запустить бота:
```bash
python -m app.main
```

## Базовый пользовательский сценарий MVP
1. `/start`
2. Открыть каталог
3. Выбрать протеин
4. Добавить товар в корзину
5. Открыть корзину
6. Нажать "Оформить заказ"
7. Открыть раздел "Заказы"
