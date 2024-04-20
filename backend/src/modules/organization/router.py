__all__ = ["router"]


from src.api.crud_routes_factory import setup_based_on_methods

from src.api.custom_router_class import EnsureAuthenticatedAPIRouter
from src.modules.organization.repository import organization_repository

router = EnsureAuthenticatedAPIRouter(prefix="/organizations", tags=["Organizations"])

setup_based_on_methods(router, crud=organization_repository)
