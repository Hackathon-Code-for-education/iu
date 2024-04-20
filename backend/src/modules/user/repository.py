__all__ = ["UserRepository", "user_repository"]

from beanie import PydanticObjectId

from src.exceptions import AlreadyExists
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

    async def create_telegram(self, telegram_data: TelegramWidgetData) -> User:
        # check if exists
        _user_by_tg = await self.read_by_telegram_id(telegram_data.id)
        if _user_by_tg is not None:
            raise AlreadyExists("Пользователь с таким telegram id уже существует")
        user = await User(name=telegram_data.first_name, telegram=telegram_data).insert()
        return user

    async def update_telegram(self, user_id: PydanticObjectId, telegram_data: TelegramWidgetData) -> User | None:
        user = await self.read(user_id)
        if user is None:
            return None
        return await user.update({"$set": {"telegram": telegram_data.model_dump()}})

    async def read_by_telegram_id(self, telegram_id: int) -> User | None:
        user = await User.find_one({"telegram.id": telegram_id})
        return user

    async def read_with_pending_approvement(self) -> list[User]:
        users = await User.find({"student_approvement.status": "pending"}).to_list()
        return users


user_repository: UserRepository = UserRepository()
