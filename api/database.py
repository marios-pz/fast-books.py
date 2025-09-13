from sqlalchemy import DateTime, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase
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


# Create Tables
Base.metadata.create_all(engine)
