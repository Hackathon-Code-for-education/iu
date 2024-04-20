__all__ = ["ViewUser", "CreateUser"]

from beanie import PydanticObjectId

from src.custom_pydantic import CustomModel
from src.modules.providers.credentials.schemas import UserRole
from src.modules.providers.telegram.schemas import TelegramWidgetData
from src.storages.mongo.models.user import StudentApprovement


class ViewUser(CustomModel):
    id: PydanticObjectId
    login: str
    name: str
    role: UserRole = UserRole.DEFAULT
    "Роль пользователя"
    telegram: TelegramWidgetData | None = None
    "Данные Telegram-аккаунта"
    student_approvement: StudentApprovement | None = None

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN


class CreateUser(CustomModel):
    login: str
    password: str
    name: str
