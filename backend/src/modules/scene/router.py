__all__ = ["router"]

from beanie import PydanticObjectId
from fastapi import Depends, APIRouter

from src.api.crud_routes_factory import setup_based_on_methods

from src.api.dependencies import get_user
from src.modules.scene.repository import scene_repository
from src.storages.mongo.models.scene import Scene

router = APIRouter(prefix="/scenes", tags=["Scenes"])

_user_dep = Depends(get_user)

setup_based_on_methods(
    router,
    crud=scene_repository,
    dependencies={
        "create": _user_dep,
        "update": _user_dep,
        "delete": _user_dep,
    },
)


@router.get(
    "/for-organization/{id}",
    responses={200: {"description": "Сцены организации"}},
)
async def get_scenes_for_organization(id: PydanticObjectId) -> list[Scene]:
    """
    Получить сцены организации
    """
    return await scene_repository.read_for_organization(id)
