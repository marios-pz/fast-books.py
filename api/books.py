from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .jwt import verify_jwt
from .database import SessionLocal


router = APIRouter(prefix="/books", tags=["books"], dependencies=[Depends(verify_jwt)])


@router.get("/{book_id}")
async def get_book(item_id: str):
    return {"item_id": item_id}


@router.delete("/{book_id}")
async def delete_book(item_id: str):
    return {"item_id": item_id}
