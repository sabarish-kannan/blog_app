from fastapi import APIRouter, Depends, Header
from core.schemas.schema import Tasks
from db import Session, engine
from authentication import Authenticate
from core.models import models


router = APIRouter(prefix="/tasks", tags=["user"])


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()


@router.post("/add")
def get_all_tasks(header: Header(), db: Session = Depends(get_db)):
    token = header["Bearer"]
    pass
