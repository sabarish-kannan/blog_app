from fastapi import APIRouter, Depends, Header
from core.schemas.schema import TasksBase, CreateTask
from db import Session
from authentication import Authenticate
from core.models import models
from datetime import datetime
from typing import Annotated


router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()


# @router.post("/")
# def add_task(
#     header: Header(), task_data: TasksBase, db: Session = Depends(get_db)
# ):
#     token = header["Bearer"][7:]
#     auth = Authenticate()
#     user_data = auth.decode_jwt_token(token)
#     task_to_add = task_data.dict()
#     task_to_add["id"] = f"{task_data.title} {datetime.now()}"
#     task_to_add["owner_id"] = user_data.email
#     task_to_add = CreateTask(task_to_add)
#     db.add(task_to_add)
#     db.commit()
#     db.refresh(task_to_add)
#     return {
#         "msg": f"task '{task_data.title}' added successfully",
#     }


@router.get("/")
def get_my_tasks(
    authorization: Annotated[str, Header()], db: Session = Depends(get_db)
):
    token = authorization[7:]
    auth = Authenticate()
    user_data = auth.decode_jwt_token(token)
    return db.query(models.Tasks).filter_by(owner_id=user_data["email"]).all()
