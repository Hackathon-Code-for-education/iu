__all__ = ["EnsureAuthenticatedAPIRouter"]

from fastapi import APIRouter


class EnsureAuthenticatedAPIRouter(APIRouter):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # TODO: Implement authentication on frontend
        # self.dependencies.append(Depends(get_user))
        # self.responses.update({**UnauthorizedException.responses})
