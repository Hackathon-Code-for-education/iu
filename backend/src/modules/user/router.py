"""
Модуль для работы с пользователями. Например, позволяет получить данные текущего пользователя.
"""

__all__ = ["router"]

from beanie import PydanticObjectId

from src.api.custom_router_class import EnsureAuthenticatedAPIRouter
from src.api.dependencies import UserDep, ModeratorDep
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
    return ViewUser.model_validate(user.model_dump())


@router.put("/me/set-documents", responses={200: {"description": "Документы успешно загружены"}})
async def set_documents(user: UserDep, documents: list[PydanticObjectId]) -> None:
    """
    Установить документы пользователя
    """
    await user_repository.set_documents(user.id, documents)


@router.put("/me/request-approvement", responses={200: {"description": "Запрос на подтверждение успешно отправлен"}})
async def request_approvement(user: UserDep, organization_id: PydanticObjectId) -> None:
    """
    Отправить запрос на подтверждение
    """
    await user_repository.request_approvement(user.id, organization_id=organization_id)


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
async def get_users_with_pending_approvement(_moder: ModeratorDep) -> list[ViewUser]:
    """
    Получить пользователей с ожидающим подтверждением
    """
    users = await user_repository.read_with_pending_approvement()
    return [ViewUser.model_validate(user.model_dump()) for user in users]


@router.get(
    "/by-id/{user_id}", responses={200: {"description": "Пользователь"}, **NotEnoughPermissionsException.responses}
)
async def get_user_by_id(_moder: ModeratorDep, user_id: PydanticObjectId) -> ViewUser:
    """
    Получить пользователя по идентификатору
    """

    target_user = await user_repository.read(user_id)
    return ViewUser.model_validate(target_user.model_dump())


@router.post(
    "/by-id/{user_id}/approve",
    responses={200: {"description": "Пользователь одобрен или отклонен"}, **NotEnoughPermissionsException.responses},
)
async def approve_user(
    moder: ModeratorDep, user_id: PydanticObjectId, is_approve: bool, comment: str | None = None
) -> ViewUser:
    """
    Одобрить или отклонить пользователя
    """

    target_user = await user_repository.approve_user(
        is_approve=is_approve, user_id=user_id, source_user_id=moder.id, comment=comment or ""
    )
    return ViewUser.model_validate(target_user.model_dump())
