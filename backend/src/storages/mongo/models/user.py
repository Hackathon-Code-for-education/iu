from typing import Annotated

from beanie import Indexed

from src.custom_pydantic import CustomModel
from src.storages.mongo.models.__base__ import CustomDocument
from src.storages.mongo.schemas import UserRole


class UserSchema(CustomModel):
    login: Annotated[str, Indexed(unique=True)]
    "Логин пользователя (уникальный)"
    name: str
    "Имя пользователя"
    password_hash: str
    "Хэш пароля"
    role: UserRole = UserRole.DEFAULT
    "Роль пользователя"

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN


class User(UserSchema, CustomDocument):
    pass
