from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Фонд пожертвований для котиков'
    description: str = 'Описание проекта'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    app_author: str
    db_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    path: str
    jwt_lifetime_seconds: int = 3600

    class Config:
        env_file = '.env'


settings = Settings()
