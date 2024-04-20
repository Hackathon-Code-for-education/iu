__all__ = ["UserRepository", "user_repository"]

from beanie import PydanticObjectId

from src.modules.providers.telegram.schemas import TelegramWidgetData
from src.storages.mongo import User


# noinspection PyMethodMayBeStatic
class UserRepository:
    async def create_superuser(self, login: str, password: str) -> User:
        from src.modules.providers.credentials.repository import credentials_repository

        user_dict = {
            "login": login,
            "name": "Superuser",
            "password_hash": credentials_repository.get_password_hash(password),
            "role": "admin",
        }

        created_user = await User.model_validate(user_dict).insert()
        return created_user

    async def exists(self, user_id: PydanticObjectId) -> bool:
        user = await User.find({"_id": user_id}).count()
        return user > 0

    async def read(self, user_id: PydanticObjectId) -> User | None:
        user = await User.find_one({"_id": user_id})
        return user

    async def read_by_login(self, login: str) -> User | None:
        user = await User.find_one({"login": login})
        return user

    async def update_telegram(self, user_id: PydanticObjectId, telegram_data: TelegramWidgetData) -> User | None:
        user = await self.read(user_id)
        if user is None:
            return None
        return await user.update({"$set": {"telegram": telegram_data.model_dump()}})

    async def read_by_telegram_id(self, telegram_id: int) -> User | None:
        user = await User.find_one({"telegram.id": telegram_id})
        return user


user_repository: UserRepository = UserRepository()
