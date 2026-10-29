from pydantic import BaseModel

class BookPlus(BaseModel):
    title: str
    author: str

class UserCreate(BaseModel):
    name: str
    email: str

class BookUpdate(BaseModel):
    title: str
    author: str