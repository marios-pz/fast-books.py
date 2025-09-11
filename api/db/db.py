from sqlalchemy.orm import Session, sessionmaker
from .models import engine, User, Book


SessionLocal = sessionmaker(bind=engine)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def add_user(session: Session, name: str, password: str) -> User | None:
    user = User(name=name, password=password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def search_user(session: Session, name: str, password: str):
    user = session.query(User).where(User.name == name and User.password == password)
    if not user:
        return None
    return user


def add_book():
    pass
