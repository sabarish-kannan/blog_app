from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status


class Authenticate:
    def __init__(self):
        self.secret_key = (
            "9fd6b7d52e3fefaa126c7e476a7a28e0996a64a902453dc8d679cfbab86a75db"
        )
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )

    def hash_password(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str):
        return self.pwd_context.verify(password, hashed_password)

    def create_jwt_token(
        self, data_for_jwt: dict, expire_minutes: int | None = None
    ):
        data_to_encode = data_for_jwt.copy()
        if expire_minutes:
            expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )
            data_to_encode.update({"exp": expire})
            jwt_token = jwt.encode(
                data_to_encode, key=self.secret_key, algorithm=self.algorithm
            )
            return jwt_token

        def decode_jwt_token(self, token: str):
            try:
                payload = jwt.decode(
                    token, key=self.secret_key, algorithms=self.algorithm
                )
                return payload
            except JWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid access token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
