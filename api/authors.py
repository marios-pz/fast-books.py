from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .jwt import verify_jwt
from .database import Author, SessionLocal, get_db


router = APIRouter(
    prefix="/authors", tags=["books"], dependencies=[Depends(verify_jwt)]
)


@router.get("/")
async def get_authors(db: Session = Depends(get_db)):
    authors = db.query(Author).all()
    return authors


# @router.get("/{author_name}")
# async def get_book(item_id: str):
#     return {"item_id": item_id}

# @router.get("/{genre_name}")
# async def get_genre(genre_name: str, db: Session = Depends(get_db)):
#     books = (
#         db.query(Book)
#         .join(BookGenres)
#         .join(Genre)
#         .filter(Genre.name == genre_name)
#         .all()
#     )
#
#     return books
