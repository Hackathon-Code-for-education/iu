import datetime
from typing import Annotated, Literal, Self

from beanie import PydanticObjectId
from pydantic import Discriminator, model_validator
from pymongo import IndexModel

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
    name: str
    "Имя пользователя"
    role: UserRole = UserRole.DEFAULT
    "Роль пользователя"
    student_approvement: StudentApprovement | None = None
    "Подтверждения статуса студента"
    # login-pass
    login: str | None = None
    "Логин пользователя (уникальный)"
    password_hash: str | None = None
    "Хэш пароля"
    # telegram
    telegram: TelegramWidgetData | None = None
    "Данные Telegram-аккаунта"

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    @model_validator(mode="after")
    def validate_user_registration(self) -> Self:
        # registered via telegram
        if self.telegram is not None:
            return self

        # reqistered via login-pass
        if self.login is not None and self.password_hash is not None:
            return self

        raise ValueError("Пользователь должен быть зарегистрирован через Telegram или через логин-пароль")


class User(UserSchema, CustomDocument):
    class Settings:
        indexes = [
            IndexModel(
                "login",
                name="login_unique_index",
                unique=True,
                partialFilterExpression={"login": {"$exists": True, "$type": "string"}},
            ),
            IndexModel(
                "telegram.id",
                name="telegram_id_unique_index",
                unique=True,
                partialFilterExpression={"telegram.id": {"$exists": True, "$type": "number"}},
            ),
        ]
