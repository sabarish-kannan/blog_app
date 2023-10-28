"""Handle all Tasks routes."""


from fastapi import APIRouter, Depends, Request, status, Response
from core.schemas.schema import TaskBase, TaskSend
from db import Session
from authentication import get_user_data, authorize
from core.models import models
from datetime import datetime
from fastapi.security import HTTPBearer


security = HTTPBearer()
router = APIRouter(
    prefix="/tasks",
    dependencies=[Depends(get_user_data)],
    tags=["tasks"],
)


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


@router.get("/", response_model=list[TaskSend], status_code=status.HTTP_200_OK)
def get_my_tasks(
    request: Request,
    db: Session = Depends(get_db),
) -> list[TaskSend]:
    """Get all the user tasks.

    Args:
        request (Request): request received
        db (Session, optional):
            database session. Defaults to Depends(get_db).

    Returns:
        list[TaskSend]: list of tasks
    """
    user_data = request.state.user_data
    return db.query(models.Tasks).filter_by(owner_id=user_data["email"]).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_task(
    request: Request,
    task_data: TaskBase,
    db: Session = Depends(get_db),
) -> dict:
    """Add a task.

    Args:
        request (Request): request received
        task_data (TaskBase): task to add
        db (Session, optional):
            database session. Defaults to Depends(get_db).
    Returns:
        dict: task added message
    """
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


@router.patch("/{task_id}", status_code=status.HTTP_200_OK)
def change_completion_status(
    request: Request,
    task_id: str,
    response: Response,
    completion_status: bool = True,
    db: Session = Depends(get_db),
) -> dict:
    """Change Task status.

    Args:
        request (Request): request received
        task_id (str): task id to change status
        response (Response): response to send
        completion_status (bool, optional):
            task completion status. Defaults to True.
        db (Session, optional):
            database session. Defaults to Depends(get_db).

    Returns:
        dict: status updated message
    """
    user_data = request.state.user_data
    task_to_update = db.query(models.Tasks).filter_by(id=task_id)
    task_to_check = task_to_update.first()
    if task_to_check:
        title = task_to_check.title
        authorize(task_to_check, user_data)
        task_to_update.update({"completion_status": completion_status})
        db.commit()
        completion_status = "completed" if completion_status else "pending"
        return {
            "msg": f"Task '{title}' marked as {completion_status} successfully"
        }
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"msg": "No such task exist"}


@router.put("/", status_code=status.HTTP_200_OK)
def update_task(
    request: Request,
    task_data: TaskSend,
    response: Response,
    db: Session = Depends(get_db),
) -> dict:
    """Update a task.

    Args:
        request (Request): request received
        task_data (TaskSend): task data to update
        response (Response): response to send
        db (Session, optional):
            database session. Defaults to Depends(get_db).

    Returns:
        dict: task updated message
    """
    user_data = request.state.user_data
    task_to_update = db.query(models.Tasks).filter_by(id=task_data.id)
    task_to_check = task_to_update.first()
    if task_to_check:
        title = task_to_check.title
        authorize(task_to_check, user_data)
        task_to_update.update(
            {
                "title": task_data.title,
                "description": task_data.description,
                "completion_status": task_data.completion_status,
            }
        )
        db.commit()
        return {"msg": f"Task '{title}' updated successfully"}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"msg": "No such task exist"}


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    request: Request,
    task_id: str,
    response: Response,
    db: Session = Depends(get_db),
) -> dict:
    """Delete a task.

    Args:
        request (Request): request received
        task_id (str): task id to change status
        response (Response): response to send
        db (Session, optional):
            database session. Defaults to Depends(get_db).

    Returns:
        dict: task deleted message
    """
    user_data = request.state.user_data
    task_to_update = db.query(models.Tasks).filter_by(id=task_id)
    task_to_check = task_to_update.first()
    if task_to_check:
        title = task_to_check.title
        authorize(task_to_check, user_data)
        task_to_update.delete()
        db.commit()
        return {"msg": f"Task '{title}' deleted successfully"}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"msg": "No such task exist"}
