__all__ = ["AuthCredentials", "UserCredentialsFromDB", "UserRole"]

from beanie import PydanticObjectId
from pydantic import Field

from src.custom_pydantic import CustomModel
from src.storages.mongo.schemas import UserRole


class AuthCredentials(CustomModel):
    login: str = Field("admin", description="User login")
    password: str = Field("admin", description="User password")


class UserCredentialsFromDB(CustomModel):
    user_id: PydanticObjectId
    password_hash: str
