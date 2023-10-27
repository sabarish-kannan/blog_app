from fastapi import APIRouter, Depends
from core.schemas.schema import UserCreate, UserToSend, UserLogin
from db import Session
from authentication import Authenticate
from core.models import models


router = APIRouter(prefix="/users", tags=["user"])


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()


@router.post("/signup")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    hashed_password = Authenticate().hash_password(user_data.password)
    db_user = models.User(
        email=user_data.email,
        user_name=user_data.user_name,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "msg": "user created successfully",
    }


@router.post("/login")
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=user_data.email).first()

    if user:
        auth = Authenticate()
        if auth.verify_password(user_data.password, user.password):
            token = auth.create_jwt_token(
                {"email": user.email, "user_name": user.user_name}, 30
            )
            return {"msg": "logged in successfully", "jwt_token": token}
        return {
            "msg": "Invalid credentials",
        }
    else:
        return {
            "msg": "Invalid credentials",
        }
