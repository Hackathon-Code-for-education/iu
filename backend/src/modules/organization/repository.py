__all__ = ["OrganizationRepository", "organization_repository"]

from beanie import PydanticObjectId

from src.modules.organization.schemas import CreateOrganization, UpdateOrganization, CompactOrganization
from src.storages.mongo.models.organization import Organization
from src.storages.mongo.crud import crud_factory, CRUD

crud: CRUD[Organization, CreateOrganization, UpdateOrganization] = crud_factory(Organization)


# noinspection PyMethodMayBeStatic
class OrganizationRepository:
    async def create(self, data: CreateOrganization) -> Organization:
        return await crud.create(data)

    async def read(self, id: PydanticObjectId) -> Organization | None:
        return await crud.read(id)

    async def read_all(self) -> list[CompactOrganization]:
        return await crud.read_all(projection_model=CompactOrganization)

    async def update(self, id: PydanticObjectId, data: UpdateOrganization) -> Organization | None:
        return await crud.update(id, data)

    async def delete(self, id: PydanticObjectId) -> bool:
        return await crud.delete(id)

    async def read_by_username(self, username: str) -> Organization | None:
        return await Organization.find_one({"username": username})

    async def get_id_registry_mapping(self) -> dict[PydanticObjectId, str]:
        organizations = await Organization.find().aggregate([{"$project": {"_id": 1, "in_registry_id": 1}}]).to_list()
        return {org["_id"]: org["in_registry_id"] for org in organizations}

    async def create_many(self, data: list[CreateOrganization]) -> list[PydanticObjectId]:
        return await crud.create_many(data)


organization_repository: OrganizationRepository = OrganizationRepository()
