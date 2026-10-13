from datetime import timedelta, datetime, timezone
from fastapi import HTTPException

from pwdlib import PasswordHash
import jwt

from src.config import settings


class AuthService:
    password_hash = PasswordHash.recommended()

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= ({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")


    def hash_password(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)
