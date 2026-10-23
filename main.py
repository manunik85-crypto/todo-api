from fastapi import FastAPI
from database import init_db, init_db2
from routers import tasks, books
from routers import tasks, books, users 

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()
    init_db2()

# Подключаем наши роутеры к основному приложению
app.include_router(tasks.router)
app.include_router(books.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "API работает!"}