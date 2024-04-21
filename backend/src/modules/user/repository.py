__all__ = ["UserRepository", "user_repository"]

from beanie import PydanticObjectId

from src.config import settings
from src.exceptions import AlreadyExists, ObjectNotFound
from src.logging_ import logger
from src.modules.organization.repository import organization_repository
from src.modules.providers.telegram.schemas import TelegramWidgetData
from src.storages.mongo import User
from src.storages.mongo.models.user import PendingApprovement, ApprovedApprovement, RejectedApprovement
from src.utils import aware_utcnow


# noinspection PyMethodMayBeStatic
class UserRepository:
    async def create_predefined_users(self):
        from src.modules.providers.credentials.repository import credentials_repository

        for user in settings.predefined.users:
            # check by login
            _user_by_login = await self.read_by_login(user.login)
            if _user_by_login is not None:
                continue
            user_dict = {
                "login": user.login,
                "name": user.name,
                "password_hash": credentials_repository.get_password_hash(user.password),
                "role": user.role,
            }
            if user.student_at_organization_username:
                organization = await organization_repository.read_by_username(user.student_at_organization_username)
                if organization:
                    user_dict["student_approvement"] = ApprovedApprovement(
                        organization_id=organization.id, at=aware_utcnow()
                    )
                else:
                    logger.error(f"Organization with username={user.student_at_organization_username} not found")

            await User.model_validate(user_dict).insert()

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

    async def filter_user_ids_belongs_to_organization(
        self, organization_id: PydanticObjectId, user_ids: list[PydanticObjectId]
    ) -> list[PydanticObjectId]:
        if not user_ids:
            return []
        users = await User.find(
            {"_id": {"$in": user_ids}, "student_approvement.organization_id": organization_id}
        ).to_list()
        return [user.id for user in users]

    async def set_documents(self, user_id: PydanticObjectId, document_ids: list[PydanticObjectId]) -> User | None:
        user = await self.read(user_id)
        if user is None:
            return None
        return await user.update({"$set": {"documents": document_ids}})

    async def request_approvement(
        self, user_id: PydanticObjectId, organization_id: PydanticObjectId, file_obj_id: PydanticObjectId | None = None
    ) -> User | None:
        user = await self.read(user_id)
        if user is None:
            return None

        _approvement = PendingApprovement(organization_id=organization_id, attachment=file_obj_id)
        return await user.update({"$set": {"student_approvement": _approvement}})

    async def approve_user(
        self, user_id: PydanticObjectId, source_user_id: PydanticObjectId, is_approve: bool, comment: str = ""
    ) -> User:
        user = await self.read(user_id)
        if user is None:
            raise ObjectNotFound("Пользователь не найден")
        _prev_approvement = user.student_approvement

        if _prev_approvement is None:
            raise ObjectNotFound("Пользователь не запрашивал подтверждения")

        if not isinstance(_prev_approvement, PendingApprovement):
            raise AlreadyExists("Пользователь уже одобрен или отклонен")

        _approvement: ApprovedApprovement | RejectedApprovement
        if is_approve:
            _approvement = ApprovedApprovement(
                organization_id=_prev_approvement.organization_id,
                moderator_id=source_user_id,
                at=aware_utcnow(),
            )
        else:
            _approvement = RejectedApprovement(
                organization_id=_prev_approvement.organization_id,
                moderator_id=source_user_id,
                at=aware_utcnow(),
                comment=comment,
            )

        user.student_approvement = _approvement
        await user.save()
        return user


user_repository: UserRepository = UserRepository()
