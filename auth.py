from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.db_models import UserDB
from passlib.context import CryptContext
from datetime import datetime, timedelta

# 1. Настройка для хеширования паролей
# bcrypt — это алгоритм, который превращает пароль в "кашу" (хеш)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для превращения пароля в хеш
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Функция для проверки пароля (сравнивает введенный пароль с хешем из базы)
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# 2. Настройки для JWT-токена
SECRET_KEY = "твой_секретный_ключ_ни_кому_не_говори"  # В реальном проекте это должна быть случайная строка
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Токен живет 30 минут

# Функция для создания токена
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Говорим FastAPI, где искать токен (в заголовке /login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Вот наша функция-охранник
async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
):
    # 1. Готовим ошибку, если что-то не так
    credentials_exception = HTTPException(
        status_code=401, 
        detail="Не удалось проверить токен"
    )
    
    try:
        # 2. Расшифровываем токен (проверяем подпись и время)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 3. Достаем ID пользователя (тот самый sub)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        # Если токен просрочен или подпись неверна — ошибка
        raise credentials_exception
    
    # 4. Ищем пользователя в базе по этому ID
    result = await db.execute(select(UserDB).where(UserDB.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
        
    # 5. Возвращаем пользователя! Теперь мы знаем, кто пришел
    return user


    
                           

