import datetime
from hmac import new
from fastapi import Depends, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from .jwt import generate_jwt
from .database import get_db, User
from .schemas import LoginRequest


def search_user(db: Session, email: str):
    return db.query(User).filter_by(email=email).first()


def verify_password(password_a: str, password_b: str) -> bool:
    return password_a == password_b  # TODO: replace with bcrypt


router = APIRouter()


@router.post("/register")
def register(response: Response, user: LoginRequest, db: Session = Depends(get_db)):
    existing = search_user(db, user.email)
    if existing:
        raise HTTPException(
            status_code=400, detail="email already registered on this app"
        )

    date = datetime.datetime.utcnow()
    new_user = User(
        name=user.username,
        password=user.password,  # TODO: hash this before saving
        email=user.email,
        profile_url="https://static.wikia.nocookie.net/idkcatmemes/images/a/af/Evillarry.png/revision/latest?cb=20241123231920",
        bio="About me",
        created_at=date,
    )

    db.add(new_user)
    db.commit()

    token = generate_jwt(
        {"sub": str(new_user.id), "username": new_user.name, "email": new_user.email}
    )

    response.set_cookie("fastbooks_token", token, httponly=True, samesite="lax")

    return {"message": f"Welcome {user.username}!"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("fastbooks_token")
    return {"message": "logged out."}
