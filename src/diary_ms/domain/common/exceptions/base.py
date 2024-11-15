class DomainError(Exception):
    _status_code: int = 500
    _detail: str = 'Domain Error.'

    def __init__(self, detail: str | None = None, status_code: int = 500):
        if detail:
            self._detail = detail
        if status_code:
            self._status_code = status_code

    @property
    def status_code(self):
        return self._status_code

    @property
    def detail(self):
        return self._detail


class DomainValueError(DomainError):
    _status_code: int = 400
    _detail: str = 'Incorrect Value.'
