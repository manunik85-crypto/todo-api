from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from database import get_db
from models.db_models import TaskDB
from pydantic import BaseModel, Field

router = APIRouter()

# Модель для создания задачи
class TaskCreate(BaseModel):
    title: str = Field(min_lengt=3, descripton="Название задачи")

# 1. POST: Создать задачу
@router.post("/tasks")
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    new_task = TaskDB(title=task.title, completed=False, user_id=task.user_id)
    db.add(new_task)
    await db.commit()
    return {"message": f"Задача '{task.title}' добавлена"}

# 2. GET: Получить все задачи
@router.get("/tasks")
async def get_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDB))
    tasks = result.scalars().all()
    return [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]

# 3. PUT: Отметить задачу выполненной
@router.put("/tasks/{task_id}/complete")
async def complete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDB).where(TaskDB.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
        
    task.completed = True
    await db.commit()
    return {"message": f"Задача с ID {task_id} выполнена"}

# 4. DELETE: Удалить задачу
@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TaskDB).where(TaskDB.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
        
    await db.delete(task)
    await db.commit()
    return {"message": f"Задача с ID {task_id} удалена"}