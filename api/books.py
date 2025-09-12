from fastapi import Depends, APIRouter
from .jwt import verify_jwt
from .db.database import SessionLocal


router = APIRouter(prefix="/books", tags=["books"], dependencies=[Depends(verify_jwt)])


@router.get("/{book_id}")
async def get_book(item_id: str, db=Depends(SessionLocal)):
    return {"item_id": item_id}


@router.delete("/{book_id}")
async def get_book(item_id: str, db=Depends(SessionLocal)):
    return {"item_id": item_id}
