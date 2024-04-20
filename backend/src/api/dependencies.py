__all__ = ["UserIdDep", "OptionalUserIdDep", "UserDep", "ModeratorDep", "get_user", "get_moderator"]

from typing import Annotated
from fastapi import Request, Depends

from src.exceptions import NotEnoughPermissionsException, UnauthorizedException
from src.modules.user.repository import user_repository
from src.storages.mongo.models.user import User
from beanie import PydanticObjectId


async def _get_uid_from_session(request: Request) -> PydanticObjectId:
    uid = await _get_optional_uid_from_session(request)
    if uid is None:
        raise UnauthorizedException("Отсутствует сессия")
    return uid


async def _get_optional_uid_from_session(request: Request) -> PydanticObjectId | None:
    uid = request.session.get("uid")

    if uid is None:
        return None
    uid = PydanticObjectId(uid)
    exists = await user_repository.exists(uid)
    if not exists:
        request.session.clear()
        raise UnauthorizedException("Пользователь не найден")
    return uid


async def get_user(request: Request) -> User:
    user_id = await _get_uid_from_session(request)
    user = await user_repository.read(user_id)
    if user is None:
        raise UnauthorizedException(detail="Пользователь не найден")
    return user


async def get_moderator(user: User = Depends(get_user)) -> User:
    if not user.is_moderator_plus:
        raise NotEnoughPermissionsException("У вас нет модераторских прав")
    return user


UserIdDep = Annotated[PydanticObjectId, Depends(_get_uid_from_session)]
OptionalUserIdDep = Annotated[PydanticObjectId | None, Depends(_get_optional_uid_from_session, use_cache=False)]
UserDep = Annotated[User, Depends(get_user)]
ModeratorDep = Annotated[User, Depends(get_moderator)]
