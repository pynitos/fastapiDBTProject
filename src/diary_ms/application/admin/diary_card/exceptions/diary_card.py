from src.diary_ms.application.common.exceptions.base import ItemNotFoundError


class DiaryCardNotFoundAdminError(ItemNotFoundError):
    _detail: str = "Diary Card Not Found!"
    _status_code: int = 404
