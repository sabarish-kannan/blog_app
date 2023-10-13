from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    user_name: str
    password: str


class Tasks(BaseModel):
    id: int
    title: str
    description: str | None = None
    completion_status: bool = False
    owner_id: str
