"""
Модуль для работы с пользователями. Например, позволяет получить данные текущего пользователя.
"""

__all__ = ["router"]

from src.api.custom_router_class import EnsureAuthenticatedAPIRouter
from src.api.dependencies import UserDep
from src.exceptions import NotEnoughPermissionsException
from src.modules.user.repository import user_repository
from src.modules.user.schemas import ViewUser
from fastapi import Request

router = EnsureAuthenticatedAPIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    responses={200: {"description": "Данные пользователя"}},
)
async def get_me(user: UserDep) -> ViewUser:
    """
    Получить данные текущего пользователя
    """
    return ViewUser.model_validate(user, from_attributes=True, strict=False)


@router.post(
    "/logout",
    responses={200: {"description": "Выход из аккаунта"}},
)
async def logout(request: Request) -> None:
    """
    Выход из аккаунта
    """
    request.session.clear()


@router.get(
    "/with-pending-approvement",
    responses={
        200: {"description": "Пользователи с ожидающим подтверждением"},
        **NotEnoughPermissionsException.responses,
    },
)
async def get_users_with_pending_approvement(user: UserDep) -> list[ViewUser]:
    """
    Получить пользователей с ожидающим подтверждением
    """

    if not user.is_admin:
        raise NotEnoughPermissionsException("У вас нет модераторских прав")

    users = await user_repository.read_with_pending_approvement()
    return [ViewUser.model_validate(user, from_attributes=True, strict=False) for user in users]
