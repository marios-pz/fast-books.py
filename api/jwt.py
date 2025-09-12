import os
import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHMS = ["HS256"]

security = HTTPBearer()


def generate_jwt(payload: dict[str, str]):
    token = jwt.encode(
        payload=payload,
        key=JWT_SECRET,
    )
    return token


def verify_jwt(creds: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHMS)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
