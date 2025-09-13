from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .jwt import verify_jwt
from .database import Book, BookGenres, Genre, SessionLocal, get_db


router = APIRouter(
    prefix="/genres", tags=["genres"], dependencies=[Depends(verify_jwt)]
)


@router.get("/{genre_name}")
async def get_genre(genre_name: str, db: Session = Depends(get_db)):
    books = (
        db.query(Book)
        .join(BookGenres)
        .join(Genre)
        .filter(Genre.name == genre_name)
        .all()
    )

    return books
