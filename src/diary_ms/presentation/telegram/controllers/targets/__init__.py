# controllers/targets/__init__.py
from aiogram import Router

from .create_target import create_target_dialog
from .get_targets import get_targets_dialog
from .update_target import update_target_dialog
from .view_target import get_target_dialog

targets_router = Router()
targets_router.include_router(create_target_dialog)
targets_router.include_router(get_target_dialog)
targets_router.include_router(get_targets_dialog)
targets_router.include_router(update_target_dialog)

__all__ = ["targets_router"]
