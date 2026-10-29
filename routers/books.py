from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models.db_models import BookDB
from pydantic import BaseModel

router = APIRouter()

class BookUpdate(BaseModel):
    title: str
    author: str

class BookCreate(BaseModel):
    title: str
    author: str

@router.post("/books")
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    new_book = BookDB(title=book.title, author=book.author)
    db.add(new_book)
    await db.commit()
    return {"message": f"Книга '{book.title}' добавлена"}

@router.get("/books")
async def get_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookDB))
    books = result.scalars().all()
    return [{"id": b.id, "title": b.title, "author": b.author} for b in books]

@router.get("/books/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookDB).where(BookDB.id == book_id))
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return {"id": book.id, "title": book.title, "author": book.author}

@router.delete("/books/{book_id}")
async def delete_books (book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookDB).where(BookDB.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
        
    await db.delete(book)
    await db.commit()
    return {"message": f"Книга с ID {book_id} удалена"}

@router.put("/books/{book_id}")
async def book_update(book_id: int, book_data: BookUpdate, db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(BookDB).where(BookDB.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    book.author = book_data.author
    book.title = book_data.title
    
    # 4. Сохраняем
    await db.commit()
    
    # 5. Возвращаем результат
    return {"message": f"Книга с ID {book_id} обновлена", "new_title": book.title}