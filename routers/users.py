from fastapi import APIRouter, HTTPException
from database import get_db_connection
from models.book import UserCreate

router = APIRouter()

@router.post("/users")
def user_plus(user:UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(name, email) VALUES(?, ?),"(user.name,user.email))
    conn.commit()
    conn.close()
    return {"message": f"Пользователь'{user.name}'добавлен"}

@router.get("/users")
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return [dict(user) for user in users]
