import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routers import handlers
from app.database import init_db


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

app.mount("/static", StaticFiles(directory="app/api/static"), name="static")

for router in handlers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)
