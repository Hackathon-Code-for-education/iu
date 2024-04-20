__all__ = ["EnsureAuthenticatedAPIRouter"]

from fastapi import APIRouter, Depends

from src.api.dependencies import get_user
from src.exceptions import UnauthorizedException


class EnsureAuthenticatedAPIRouter(APIRouter):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dependencies.append(Depends(get_user))
        self.responses.update({**UnauthorizedException.responses})
