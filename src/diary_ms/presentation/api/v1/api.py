from fastapi import APIRouter
from fastapi_versioning import versioned_api_route

from .routes import diary_card

api_v1 = APIRouter(route_class=versioned_api_route(1))

api_v1.include_router(diary_card.router)
