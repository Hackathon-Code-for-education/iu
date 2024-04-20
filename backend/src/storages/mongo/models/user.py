import datetime
from typing import Annotated, Literal

from beanie import Indexed, PydanticObjectId
from pydantic import Discriminator

from src.custom_pydantic import CustomModel
from src.modules.providers.telegram.schemas import TelegramWidgetData
from src.storages.mongo.models.__base__ import CustomDocument
from src.storages.mongo.schemas import UserRole


class PendingApprovement(CustomModel):
    status: Literal["pending"] = "pending"


class ApprovedApprovement(CustomModel):
    status: Literal["approved"] = "approved"
    moderator_id: PydanticObjectId
    "ID модератора, подтвердившего студента"
    at: datetime.datetime
    "Дата подтверждения студента"
    organization_name: str
    "Наименование организации к которой будет привязан студент (если организация не существует в системе)"
    organization_id: PydanticObjectId | None
    "ID организации к которой будет привязан студент"


class RejectedApprovement(CustomModel):
    status: Literal["rejected"] = "rejected"
    moderator_id: PydanticObjectId
    "ID модератора, отклонившего студента"
    at: datetime.datetime
    "Дата отклонения студента"
    comment: str
    "Комментарий по какой причине отклонен студент"


StudentApprovement = Annotated[PendingApprovement | ApprovedApprovement | RejectedApprovement, Discriminator("status")]


class UserSchema(CustomModel):
    login: Annotated[str, Indexed(unique=True)]
    "Логин пользователя (уникальный)"
    name: str
    "Имя пользователя"
    password_hash: str
    "Хэш пароля"
    role: UserRole = UserRole.DEFAULT
    "Роль пользователя"
    telegram: TelegramWidgetData | None = None
    "Данные Telegram-аккаунта"
    student_approvement: StudentApprovement | None = None
    "Подтверждения статуса студента"

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN


class User(UserSchema, CustomDocument):
    pass
