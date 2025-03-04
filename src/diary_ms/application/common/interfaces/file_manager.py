from abc import abstractmethod
from asyncio import Protocol

from src.diary_ms.domain.model.aggregates.diary_card_id import DiaryCardId


def file_path_creator(diary_card_id: DiaryCardId, extension: str = "jpg") -> str:
    return f"{diary_card_id}_image.{extension}"


class FileManager(Protocol):
    @abstractmethod
    def save(self, payload: bytes, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_file_id(self, file_path: str) -> bytes | None:
        raise NotImplementedError

    @abstractmethod
    def delete_object(self, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_folder(self, folder: str) -> None:
        raise NotImplementedError
