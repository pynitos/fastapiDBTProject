from aiogram import Router

from . import states
from .create_medicament import create_medicament_dialog
from .get_medicaments import list_medicaments_dialog, view_medicament_dialog
from .update_medicament import update_medicament_dialog

medicament_router = Router()

medicament_router.include_routers(
    list_medicaments_dialog, view_medicament_dialog, create_medicament_dialog, update_medicament_dialog
)

__all__ = [
    "medicament_router",
    "states",
]
