__all__ = ["SceneRepository", "scene_repository"]

from beanie import PydanticObjectId

from src.modules.scene.schemas import CreateScene, UpdateScene
from src.storages.mongo.models.scene import Scene
from src.storages.mongo.crud import crud_factory, CRUD

crud: CRUD[Scene, CreateScene, UpdateScene] = crud_factory(Scene)


# noinspection PyMethodMayBeStatic
class SceneRepository:
    async def create(self, data: CreateScene) -> Scene:
        return await crud.create(data)

    async def read(self, id: PydanticObjectId) -> Scene | None:
        return await crud.read(id)

    async def read_all(self) -> list[Scene]:
        return await crud.read_all()

    async def update(self, id: PydanticObjectId, data: UpdateScene) -> Scene | None:
        return await crud.update(id, data)

    async def delete(self, id: PydanticObjectId) -> bool:
        return await crud.delete(id)


scene_repository: SceneRepository = SceneRepository()
