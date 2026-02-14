

class AppException(Exception):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)
        self._message = message

    @property
    def message(self) -> str:
        return self._message
    