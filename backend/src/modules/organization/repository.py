__all__ = ["OrganizationRepository", "organization_repository"]

from beanie import PydanticObjectId

from src.modules.organization.schemas import CreateOrganization, UpdateOrganization
from src.storages.mongo.models.organization import Organization
from src.storages.mongo.crud import crud_factory, CRUD

crud: CRUD[Organization, CreateOrganization, UpdateOrganization] = crud_factory(Organization)


# noinspection PyMethodMayBeStatic
class OrganizationRepository:
    async def create(self, data: CreateOrganization) -> Organization:
        return await crud.create(data)

    async def read(self, id: PydanticObjectId) -> Organization | None:
        return await crud.read(id)

    async def read_all(self) -> list[Organization]:
        return await crud.read_all()

    async def update(self, id: PydanticObjectId, data: UpdateOrganization) -> Organization | None:
        return await crud.update(id, data)

    async def delete(self, id: PydanticObjectId) -> bool:
        return await crud.delete(id)


organization_repository: OrganizationRepository = OrganizationRepository()
