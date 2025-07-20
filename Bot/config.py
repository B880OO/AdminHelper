from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    TOKEN: str
    DATABASE_URL: str
    ADMINS: List[int] = []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


async def is_admin(id: int) -> bool:
    if id in settings.ADMINS:
        return True
    return False
