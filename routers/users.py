from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.db_models import UserDB
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    email: str

@router.post("/users")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = UserDB(name=user.name, email=user.email)
    db.add(new_user)
    await db.commit()
    return {"message": f"Пользователь '{user.name}' добавлен"}

@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserDB))
    users = result.scalars().all()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]