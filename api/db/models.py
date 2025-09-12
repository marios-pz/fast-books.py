from sqlalchemy import DateTime, Integer, String, create_engine
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base, engine


class User(Base):
    __tablename__: str = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    profile_picture_url: Mapped[str] = mapped_column(String)
    bio: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime)


class Book(Base):
    __tablename__: str = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    isbn: Mapped[int] = mapped_column(Integer)


Base.metadata.create_all(engine)
