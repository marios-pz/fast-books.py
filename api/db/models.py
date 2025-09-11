from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

db_url = "sqlite:///books.db"
engine = create_engine(db_url)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__: str = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)


class Book(Base):
    __tablename__: str = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    isbn: Mapped[int] = mapped_column(Integer)


Base.metadata.create_all(engine)
