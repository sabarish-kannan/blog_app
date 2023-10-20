import uvicorn
from fastapi import FastAPI
from routes import user, task
from core.models import models
from db import engine

app = FastAPI()
app.include_router(user.router)
app.include_router(task.router)
models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
