__all__ = ["router"]

from beanie import PydanticObjectId

from src.api.crud_routes_factory import setup_based_on_methods

from src.api.custom_router_class import EnsureAuthenticatedAPIRouter
from src.modules.scene.repository import scene_repository
from src.storages.mongo.models.scene import Scene

router = EnsureAuthenticatedAPIRouter(prefix="/scenes", tags=["Scenes"])

setup_based_on_methods(router, crud=scene_repository)


@router.get(
    "/for-organization/{organization_id}",
    responses={200: {"description": "Сцены организации"}},
)
async def get_scenes_for_organization(organization_id: PydanticObjectId) -> list[Scene]:
    """
    Получить сцены организации
    """
    return await scene_repository.read_for_organization(organization_id)
