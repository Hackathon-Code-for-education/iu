from typing import ClassVar, Any

from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from starlette import status


class CustomHTTPException(HTTPException):
    responses: ClassVar[dict[int | str, dict[str, Any]]]


# --- Authorization exceptions ---- #
class UnauthorizedException(CustomHTTPException):
    """
    HTTP_401_UNAUTHORIZED
    Неверные учетные данные
    """

    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail or self.responses[401]["description"],
        )

    responses = {401: {"description": "Невозможно проверить учетные данные ИЛИ Учетные данные не предоставлены"}}


class NotEnoughPermissionsException(CustomHTTPException):
    """
    HTTP_403_FORBIDDEN
    Доступ запрещен
    """

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail or self.responses[403]["description"],
        )

    responses = {403: {"description": "Недостаточно прав"}}


class InvalidTelegramWidgetHash(CustomHTTPException):
    """
    HTTP_400_BAD_REQUEST
    """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=self.responses[400]["description"],
        )

    responses = {400: {"description": "Invalid Telegram widget hash"}}


# --- Object exceptions ---- #


class ObjectNotFound(CustomHTTPException):
    """
    HTTP_404_NOT_FOUND
    """

    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail or self.responses[404]["description"],
        )

    responses = {404: {"description": "Object with such properties not found"}}


class AlreadyExists(CustomHTTPException):
    """
    HTTP_409_CONFLICT
    Объект уже существует
    """

    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail or self.responses[409]["description"],
        )

    responses = {409: {"description": "Объект уже существует"}}


def unwrap_duplicate_error(e: Exception) -> Exception:
    duplicate_key_error: DuplicateKeyError | None = None
    if isinstance(e, DuplicateKeyError):
        duplicate_key_error = e
    elif e.__context__ is not None and isinstance(e.__context__, DuplicateKeyError):
        duplicate_key_error = e.__context__

    if duplicate_key_error is not None:
        detals = {"keyValue": None}
        if duplicate_key_error.details:
            detals["keyValue"] = duplicate_key_error.details.get("keyValue")
        return AlreadyExists(f"Объект с такими свойствами уже существует: {detals}")
    return e
