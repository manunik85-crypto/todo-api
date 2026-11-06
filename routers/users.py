from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.db_models import UserDB
from pydantic import BaseModel
from auth import verify_password, create_access_token, get_password_hash
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str  

@router.post("/users")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = UserDB(
        name=user.name, 
        email=user.email, 
        password=get_password_hash(user.password)  # <--- Хешируем пароль!
    )
    db.add(new_user)
    await db.commit()
    return {"message": f"Пользователь {user.name} добавлен"}


@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserDB))
    users = result.scalars().all()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]

from auth import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # 1. Ищем пользователя по email (в форме будет поле username, но мы будем использовать его как email)
    result = await db.execute(select(UserDB).where(UserDB.email == form_data.username))
    user = result.scalar_one_or_none()
    
    # 2. Если пользователя нет или пароль неверный — ошибка 401
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    
    # 3. Создаем токен и отдаем его
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}