from fastapi import Depends, APIRouter
from .jwt import verify_jwt


router = APIRouter(dependencies=[Depends(verify_jwt)])


# def add_user(session: Session, name: str, password: str) -> User | None:
#     user = User(name=name, password=password)
#
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user
#
#
# def search_user(session: Session, name: str, password: str):
#     user = session.query(User).filter_by(name=name, password=password).first()
#     if not user:
#         return None
#     return user
