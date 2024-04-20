__all__ = ["router"]

from fastapi import Depends, APIRouter

from src.api.crud_routes_factory import setup_based_on_methods

from src.api.dependencies import get_user
from src.modules.organization.repository import organization_repository

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
