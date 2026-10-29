from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
# 1. Настройка подключения
# ВАЖНО: замени "твой_пароль" на тот пароль, который ты придумал при установке PostgreSQL!
# "postgres" — это имя пользователя по умолчанию.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:m20A12n2006@localhost:5432/postgres")

engine = create_async_engine(DATABASE_URL, echo=True)

# 2. Создаем фабрику сессий (через нее мы будем общаться с базой)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 3. Базовый класс для всех наших моделей
class Base(DeclarativeBase):
    pass

# 4. Функция для получения сессии (пригодится в эндпоинтах)
async def get_db():
    async with async_session() as session:
        yield session