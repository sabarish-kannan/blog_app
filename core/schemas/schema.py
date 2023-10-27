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


class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    id: str
    owner_id: str
    completion_status: bool = False
