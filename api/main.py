from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .db.database import get_db
from .books import router as books_router
from .users import router as users_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
from .schemas import LoginRequest


app = FastAPI()
app.include_router(books_router)
app.include_router(users_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": f"Welcome {db_user.username}!"}


@app.post("/register")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": f"Welcome {db_user.username}!"}


@app.post("/logout")
async def logout():
    return {"message": "logged out."}


@app.get("/")
async def root():
    return {"message": "Welcome to the True Mans world."}
