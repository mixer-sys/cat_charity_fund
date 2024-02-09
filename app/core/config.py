from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Фонд пожертвований для котиков'
    description: str = 'Описание проекта'
    database_url: str
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    app_author: str
    db_url: str = 'postgres://login:password@127.0.0.1:5432/qrkot'
    path: str

    class Config:
        env_file = '.env'


settings = Settings()
