from fastapi import FastAPI

from app.diary_ms.main import app as diary_app

app: FastAPI = FastAPI()

app.mount('/diary', diary_app)
