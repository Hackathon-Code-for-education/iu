__all__ = ["router"]

from src.exceptions import UnauthorizedException
from src.modules.providers.credentials.schemas import AuthCredentials

from fastapi import APIRouter, Request

router = APIRouter(prefix="/credentials")


# by-tag
@router.post(
    "/credentials",
    responses={200: {"description": "Авторизация пользователя"}, **UnauthorizedException.responses},
)
async def by_credentials(credentials: AuthCredentials, request: Request) -> None:
    """
    Авторизация пользователя по логину и паролю. Возвращает обёрнутый JWT токен.
    """
    from src.modules.providers.credentials.repository import credentials_repository

    user_id = await credentials_repository.authenticate_user(password=credentials.password, login=credentials.login)
    request.session.clear()
    request.session["uid"] = str(user_id)
