"""Schemas for request and responses."""


from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base model for user."""

    email: EmailStr


class UserCreate(UserBase):
    """model for creating user."""

    user_name: str
    password: str


class UserLogin(UserBase):
    """model for logging in user."""

    password: str


class UserToSend(UserBase):
    """model to send and receiving user."""

    user_name: str


class UserUpdate(BaseModel):
    """model to update user."""

    user_name: str = None
    password: str = None


class TaskBase(BaseModel):
    """Base model for tasks."""

    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    """model to create task."""

    id: str
    owner_id: str
    completion_status: bool = False


class TaskSend(TaskBase):
    """model to send and receive task."""

    id: str
    completion_status: bool
