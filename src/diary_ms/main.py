from fastapi import FastAPI

from src.diary_ms.main.web import create_app

app: FastAPI = create_app()
