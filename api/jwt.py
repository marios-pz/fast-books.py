import os
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from http import HTTPStatus
from datetime import datetime, timedelta

JWT_SECRET = os.getenv("JWT_SECRET", "changeme")  # fallback for dev
JWT_ALGORITHMS = ["HS256"]

security = HTTPBearer()


def generate_jwt(payload: dict[str, str]) -> str:
    expire = datetime.now() + timedelta(minutes=15)
    payload.update({"exp": expire})
    token = jwt.encode(
        payload=payload,
        key=JWT_SECRET,
        algorithm=JWT_ALGORITHMS[0],
    )
    return token


def verify_jwt(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHMS)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token")
