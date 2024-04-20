# noinspection PyUnreachableCode

__all__ = ["router"]

from fastapi import APIRouter

router = APIRouter(prefix="/online", tags=["Online"])

# noinspection PyUnreachableCode
if False:  # disable as not needed now
    from beanie import PydanticObjectId
    from src.api.dependencies import UserDep
    from src.modules.online.repository import online_repository
    from src.modules.user.repository import user_repository

    @router.post(
        "/i-am-online",
        responses={200: {"description": "Success"}},
    )
    async def i_am_online(user: UserDep) -> None:
        """
        Отметить пользователя как онлайн
        """
        online_repository.i_am_online(user.id)
        return None

    @router.get("/get-online-users", responses={200: {"description": "Success"}})
    async def get_online_users(organization_id: PydanticObjectId | None = None) -> int:
        """
        Получить список онлайн пользователей
        """
        online = online_repository.get_online_users()

        if organization_id is not None:
            online = await user_repository.filter_user_ids_belongs_to_organization(
                organization_id=organization_id, user_ids=online
            )

        return len(online)
