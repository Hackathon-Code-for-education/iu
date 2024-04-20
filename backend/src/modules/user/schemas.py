__all__ = ["ViewUser", "CreateUser"]

from pydantic import Field

from src.custom_pydantic import CustomModel
from src.storages.mongo.models.user import User


class ViewUser(User):
    password_hash: str | None = Field(exclude=True)


class CreateUser(CustomModel):
    name: str
    login: str
    password: str
