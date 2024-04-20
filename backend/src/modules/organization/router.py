__all__ = ["router"]

from fastapi import Depends, APIRouter

from src.api.crud_routes_factory import setup_based_on_methods

from src.api.dependencies import get_user
from src.exceptions import ObjectNotFound
from src.modules.organization.repository import organization_repository
from src.storages.mongo import Organization

router = APIRouter(prefix="/organizations", tags=["Organizations"])

_user_dep = Depends(get_user)

setup_based_on_methods(
    router,
    crud=organization_repository,
    dependencies={
        "create": _user_dep,
        "update": _user_dep,
        "delete": _user_dep,
    },
)


@router.get(
    "/by-username/{username}", responses={200: {"description": "Organization info"}, **ObjectNotFound.responses}
)
async def get_by_username(username: str) -> Organization:
    organization = await organization_repository.read_by_username(username)
    if organization is None:
        raise ObjectNotFound(f"Организация с username={username} не найдена")
    return organization
