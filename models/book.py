from pydantic import BaseModel

class BookPlus(BaseModel):
    title: str
    author: str