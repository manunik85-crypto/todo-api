import asyncio
from database import engine, Base
from models.db_models import TaskDB, BookDB, UserDB

async def reset_db():
    async with engine.begin() as conn:
        # Удаляем все таблицы, которые знает наша база
        await conn.run_sync(Base.metadata.drop_all)
        # Создаем их заново (уже с новой колонкой user_id)
        await conn.run_sync(Base.metadata.create_all)
    print("База данных успешно пересоздана!")

asyncio.run(reset_db())