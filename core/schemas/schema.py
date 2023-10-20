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


class TasksBase(BaseModel):
    title: str
    description: str | None = None
    completion_status: bool = False


class CreateTask(TasksBase):
    id: str
    owner_id: str
