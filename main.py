from fastapi import FastAPI
from routes import user, task

app = FastAPI()
app.include_router(user.router)
