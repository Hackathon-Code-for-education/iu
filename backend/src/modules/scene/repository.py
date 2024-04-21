__all__ = ["SceneRepository", "scene_repository"]

from beanie import PydanticObjectId

from src.config import settings
from src.logging_ import logger
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

    async def read_for_organization(self, organization_id: PydanticObjectId) -> list[Scene]:
        return await Scene.find({"organization": organization_id}).to_list()

    async def exists(self, scene_id: PydanticObjectId) -> bool:
        scene = await Scene.find({"_id": scene_id}).count()
        return scene > 0

    async def create_predefined_scenes(self):
        from src.modules.organization.repository import organization_repository

        for scene in settings.predefined.scenes:
            if await self.exists(scene.id):
                continue
            organization_username = scene.organization_username
            organization_id = await organization_repository.read_id_by_username(organization_username)
            if organization_id is None:
                logger.error(f"Organization with username={organization_username} not found")
                continue

            await Scene(
                id=scene.id,  # type: ignore[call-arg]
                organization=organization_id,
                title=scene.title,
                meta=scene.meta,
                file=scene.file,
            ).insert()

            logger.info(f"Scene {scene.title} <{scene.id}> created")


scene_repository: SceneRepository = SceneRepository()
