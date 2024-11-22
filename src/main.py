from fastapi import FastAPI

from src.diary_ms.main.web import diary_app

app: FastAPI = FastAPI()

app.mount("/diary", diary_app)
