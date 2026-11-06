from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.db_models import NoteDB,UserDB
from auth import get_current_user

router = APIRouter()

@router.post("/notes")
async def create_note(
    note: NoteCreate,  # <--- Модель Pydantic (текст заметки)
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    # Создаем ОБЪЕКТ БАЗЫ ДАННЫХ (NoteDB), а не Pydantic
    new_note = NoteDB(
        text=note.text,  # <--- Берем текст из Pydantic-модели
        user_id=current_user.id
    )
    db.add(new_note)
    await db.commit()
    return {"message": f"Заметка '{note.text}' добавлена пользователю {current_user.name}"}

@router.get("/notes")
async def get_notes(
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)  # <--- UserDB, а не NoteDB!
):
    result = await db.execute(
        select(NoteDB).where(NoteDB.user_id == current_user.id)
    )
    notes = result.scalars().all()  # <--- Переменная notes
    # Возвращаем только id и text
    return [{"id": n.id, "text": n.text} for n in notes]