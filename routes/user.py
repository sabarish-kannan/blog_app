"""Handle all the user routes."""


from fastapi import APIRouter, Depends, status, Request, Response
from core.schemas.schema import UserCreate, UserLogin, UserUpdate
from db import Session
from authentication import Authenticate, get_user_data
from core.models import models
from validate import validate_password, validate_user_name


router = APIRouter(prefix="/users", tags=["user"])


def get_db() -> None:
    """Initiate DB connection.

    Yields:
        Session: DB to do operations.
    """
    try:
        db = Session()
        yield db
    finally:
        db.close()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate, response: Response, db: Session = Depends(get_db)
) -> dict:
    """Signup a user.

    Args:
        user_data (UserCreate): user data to create user
        response (Response): response to send
        db (Session, optional):
            database session. Defaults to Depends(get_db).

    Returns:
        dict: user creation message
    """
    if (
        db.query(models.User).filter_by(email=user_data.email).first()
        is not None
    ):
        response.status_code = status.HTTP_409_CONFLICT
        return {
            "msg": "There ia already an account associated with this email"
        }
    validate_password(user_data.password)
    validate_user_name(user_data.user_name)
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


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)) -> dict:
    """Login the user.

    Args:
        user_data (UserLogin):  user data to login user
        db (Session, optional):
            database session. Defaults to Depends(get_db).

    Returns:
        dict: jwt token and loggin message
    """
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


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_user_data)],
)
def update_profile(
    request: Request,
    user_data: UserUpdate,
    response: Response,
    db: Session = Depends(get_db),
) -> dict:
    """Update the user profile.

    Args:
        request (Request): request received
        user_data (UserUpdate):  user data to update user
        response (Response): response to send
        db (Session, optional):
            database session. Defaults to Depends(get_db).

    Returns:
        dict: update status message
    """
    user_email = request.state.user_data["email"]
    user_to_update = db.query(models.User).filter_by(email=user_email)
    updated_user = {}
    if user_data.user_name is None and user_data.password is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {"msg": "No changes to update"}
    if user_data.user_name is not None:
        validate_user_name(user_data.user_name)
        updated_user["user_name"] = user_data.user_name
    if user_data.password is not None:
        validate_password(user_data.password)
        hashed_password = Authenticate().hash_password(user_data.password)
        updated_user["password"] = hashed_password
    user_to_update.update(updated_user)
    db.commit()
    return {"msg": "User Profile updated successfully"}


@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_user_data)],
)
def delete_user(
    request: Request,
    db: Session = Depends(get_db),
) -> dict:
    """Delete a user.

    Args:
        request (Request): request received
        db (Session, optional):
            database session. Defaults to Depends(get_db).

    Returns:
        dict: deleted message
    """
    user_email = request.state.user_data["email"]
    user_to_delete = db.query(models.User).filter_by(email=user_email)
    user_name = user_to_delete.first().user_name
    user_to_delete.delete()
    db.commit()
    return {"msg": f"User '{user_name}' deleted successfully"}
