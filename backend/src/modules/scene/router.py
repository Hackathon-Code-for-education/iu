__all__ = ["router"]

from src.api.crud_routes_factory import setup_based_on_methods

from src.api.custom_router_class import EnsureAuthenticatedAPIRouter
from src.modules.scene.repository import scene_repository

router = EnsureAuthenticatedAPIRouter(prefix="/scenes", tags=["Scenes"])

setup_based_on_methods(router, crud=scene_repository)
