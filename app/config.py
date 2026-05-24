from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ADMIN_IDS: list[int]

    class Config:
        env_file = ".env"


settings = Settings()