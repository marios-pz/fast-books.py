from sqlite3 import Date
from sqlalchemy import DateTime, Integer, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.orm import relationship


import os

# Production or dev
database_name: str = os.getenv("POSTGRES_USER", "postgres")
database_password: str = os.getenv("POSTGRES_PASSWORD", "postgres")
database_db: str = os.getenv("POSTGRES_DB_NAME", "fastbooks")
database_host: str = os.getenv("POSTGRES_HOST", "localhost")
db_url = (
    f"postgresql://{database_name}:{database_password}@{database_host}/{database_db}"
)
engine = create_engine(db_url, pool_pre_ping=True, echo=True)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


def get_db():
    db = SessionLocal()  # δημιουργεί νέο session
    try:
        yield db  # το δίνει στο endpoint
    finally:
        db.close()  # κλείνει session μετά το request


class User(Base):
    __tablename__: str = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    profile_url: Mapped[str] = mapped_column(String)
    bio: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime)

    books: Mapped[list["UserBooks"]] = relationship("UserBooks", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"


class Author(Base):
    __tablename__: str = "authors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    bio: Mapped[str] = mapped_column(String)
    profile_url: Mapped[str] = mapped_column(String)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__: str = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    year: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    page_count: Mapped[int] = mapped_column(Integer)
    cover_url: Mapped[str] = mapped_column(String)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship("Author", back_populates="books")

    genres: Mapped[list["BookGenres"]] = relationship(
        "BookGenres", back_populates="book"
    )
    users: Mapped[list["UserBooks"]] = relationship("UserBooks", back_populates="book")


class Genre(Base):
    __tablename__: str = "genres"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    books: Mapped[list["BookGenres"]] = relationship(
        "BookGenres", back_populates="genre"
    )


class BookGenres(Base):
    __tablename__: str = "book_genres"
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), primary_key=True)

    book: Mapped["Book"] = relationship("Book", back_populates="genres")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")


class UserBooks(Base):
    __tablename__: str = "user_books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    status: Mapped[str] = mapped_column(String)  # read, dropped, etc
    # rating: Mapped[int] = mapped_column(Integer)

    user: Mapped["User"] = relationship("User", back_populates="books")
    book: Mapped["Book"] = relationship("Book", back_populates="users")


# Create Tables
Base.metadata.create_all(engine)
