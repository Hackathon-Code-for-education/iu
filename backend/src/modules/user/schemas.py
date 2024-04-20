__all__ = ["ViewUser", "CreateUser"]

from beanie import PydanticObjectId

from src.custom_pydantic import CustomModel
from src.modules.providers.credentials.schemas import UserRole


class ViewUser(CustomModel):
    id: PydanticObjectId
    login: str
    name: str
    role: UserRole = UserRole.DEFAULT

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN


class CreateUser(CustomModel):
    login: str
    password: str
    name: str
