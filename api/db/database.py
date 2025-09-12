from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

db_url = "sqlite:///books.db"
engine = create_engine(db_url, pool_pre_ping=True, echo=True)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()  # δημιουργεί νέο session
    try:
        yield db  # το δίνει στο endpoint
    finally:
        db.close()  # κλείνει session μετά το request
