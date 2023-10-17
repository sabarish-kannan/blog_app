from fastapi import APIRouter, Depends
from core.schemas.schema import UserCreate, UserBase
from db import Session
from typing import Annotated
from authentication import Authenticate
from core.models import database

router = APIRouter(prefix="/user", tags=["user"])


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserBase)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    hashed_password = Authenticate().hash_password(user_data.password)
    db_user = database.User(
        email=user_data.email,
        user_name=user_data.user_name,
        password=user_data.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserBase(**db_user)


@router.get("/", response_model=list[UserBase])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(database.User).all()
