import uvicorn
from fastapi import FastAPI
from market.crm_database import init_db

from market.crm.routers import handlers
from fastapi.staticfiles import StaticFiles


async def lifespan(app: FastAPI):
    print("Подключение базы данных:")
    await init_db()
    print("База данных успешно подключена")

    print("Добавляем тестовых пользователей")
    # for user in users:
    #     await user_repo.create_user(user)

    print("Приложение успешно запущено")
    yield
    print("Конец работы программ")


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="market/crm/static"), name="static")

for router in handlers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("market.crm.main:app", host="0.0.0.0", port=8000, reload=True)
