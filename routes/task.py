from fastapi import APIRouter, Depends, Header, Request
from core.schemas.schema import TaskBase, TaskCreate
from db import Session
from authentication import Authenticate, get_user_data
from core.models import models
from datetime import datetime
from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


security = HTTPBearer()
router = APIRouter(
    prefix="/tasks",
    dependencies=[Depends(get_user_data)],
    tags=["tasks"],
)


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()


@router.get("/")
def get_my_tasks(
    request: Request,
    db: Session = Depends(get_db),
):
    user_data = request.state.user_data
    return db.query(models.Tasks).filter_by(owner_id=user_data["email"]).all()


@router.post("/")
def add_task(
    request: Request,
    task_data: TaskBase,
    db: Session = Depends(get_db),
):
    user_data = request.state.user_data
    task_to_add = models.Tasks(
        id=f"{task_data.title} {datetime.now()}",
        title=task_data.title,
        description=task_data.description,
        owner_id=user_data["email"],
        completion_status=False,
    )
    db.add(task_to_add)
    db.commit()
    db.refresh(task_to_add)
    return {
        "msg": f"task '{task_data.title}' added successfully",
    }


@router.patch("/{task_id}")
def mark_task_as_done(
    request: Request,
    task_id: str,
    db: Session = Depends(get_db),
):
    task_to_complete = db.query(models.Tasks).filter_by(id=task_id)
    completed_task = task_to_complete.copy(update=update_data)
    db.query(models.Tasks).filter_by(id=task_id).update(
        task_to_complete.dict()
    )
    if task_to_complete is None:
        return {"msg": "No such task exist"}
