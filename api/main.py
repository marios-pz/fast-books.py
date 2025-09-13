from fastapi import FastAPI
from .books import router as books_router
from .users import router as users_router
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

load_dotenv()

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


@app.get("/")
async def root():
    return {"message": "Welcome to the True Mans world."}
