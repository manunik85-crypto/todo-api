from fastapi import FastAPI
from routers import tasks, books, users

app = FastAPI()

# startup() можно вообще удалить

app.include_router(tasks.router)
app.include_router(books.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "API работает!"}