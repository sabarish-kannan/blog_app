from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    user_name: str
    password: str


class UserLogin(UserBase):
    password: str


class UserToSend(UserBase):
    user_name: str


class Tasks(BaseModel):
    id: int
    title: str
    description: str | None = None
    completion_status: bool = False
    owner_id: str
