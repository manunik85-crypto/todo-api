from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


# Таблица задач
class TaskDB(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserDB"] = relationship(back_populates="tasks") # <--- ВОТ ЭТА СТРОКА
    user: Mapped["UserDB"] = relationship(back_populates="tasks") # <--- ВОТ ЭТА СТРОКА

# Таблица книг
class BookDB(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))

# Таблица пользователей 
class UserDB(Base):
    __tablename__="users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    tasks: Mapped[list["TaskDB"]] = relationship(back_populates="user")