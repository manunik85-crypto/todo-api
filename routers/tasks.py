from fastapi import APIRouter, HTTPException
from database import get_db_connection
from models.book import BookPlus

# Создаем роутер (как маленький сервер внутри основного)
router = APIRouter()

@router.post("/books")  # <--- Обрати внимание, тут @router, а не @app
def book_plus(book: BookPlus):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (book.title, book.author))
    conn.commit()
    conn.close()
    return {"message": f"Книга '{book.title}' добавлена"}

@router.get("/books")   # <--- Тут тоже @router
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return [dict(book) for book in books]