class AppError(Exception):
    _detail: str = "Domain Error."
    _status_code: int = 500

    def __init__(self, detail: str | None = None, status_code: int = 500):
        if detail:
            self._detail = detail
        if status_code:
            self._status_code = status_code

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def detail(self) -> str:
        return self._detail


class DomainError(AppError):
    pass


class DomainValueError(DomainError):
    _detail: str = "Incorrect Value."
    _status_code: int = 400
