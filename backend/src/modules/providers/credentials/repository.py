__all__ = ["CredentialsRepository", "credentials_repository"]

from beanie import PydanticObjectId
from passlib.context import CryptContext

from src.exceptions import UnauthorizedException
from src.logging_ import logger
from src.modules.providers.credentials.schemas import UserCredentialsFromDB


# noinspection PyMethodMayBeStatic
class CredentialsRepository:
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"])

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.PWD_CONTEXT.hash(password)

    async def authenticate_user(self, login: str, password: str) -> PydanticObjectId:
        user_credentials = await self._get_user(login)
        if user_credentials is None:
            raise UnauthorizedException()
        password_verified = await self.verify_password(password, user_credentials.password_hash)
        if not password_verified:
            raise UnauthorizedException()
        return user_credentials.user_id

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        logger.info(f"verifying password {self.PWD_CONTEXT.hash(plain_password)} hashed={hashed_password}")
        return self.PWD_CONTEXT.verify(plain_password, hashed_password)

    async def _get_user(self, login: str) -> UserCredentialsFromDB | None:
        from src.modules.user.repository import user_repository

        user = await user_repository.read_by_login(login)
        if user:
            assert user.password_hash is not None
            return UserCredentialsFromDB(user_id=user.id, password_hash=user.password_hash)
        return None


credentials_repository: CredentialsRepository = CredentialsRepository()
