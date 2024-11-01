from fastapi import FastAPI

from app.diary_ms.core.server import create_app

app: FastAPI = create_app()
