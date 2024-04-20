"""
Модуль для работы с пользователями. Например, позволяет получить данные текущего пользователя.
"""

__all__ = ["router"]


from src.api.custom_router_class import EnsureAuthenticatedAPIRouter
from src.api.dependencies import UserDep
from src.modules.user.schemas import ViewUser

router = EnsureAuthenticatedAPIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    responses={200: {"description": "User info"}},
)
async def get_me(user: UserDep) -> ViewUser:
    """
    Получить данные текущего пользователя
    """
    return ViewUser.model_validate(user, from_attributes=True, strict=False)
