__all__ = ["OrganizationRepository", "organization_repository", "parse_certificates_to_organizations"]

from beanie import PydanticObjectId

from scripts.parse_organizations import Certificates
from src.modules.organization.schemas import CreateOrganization, UpdateOrganization, CompactOrganization
from src.storages.mongo.models.organization import Organization, ContactsSchema, EducationalProgramSchema
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

    async def read_id_by_username(self, username: str) -> PydanticObjectId | None:
        org = await Organization.find({"username": username}).aggregate([{"$project": {"_id": 1}}]).to_list()
        return org[0]["_id"] if org else None

    async def get_id_registry_mapping(self) -> dict[PydanticObjectId, str]:
        organizations = await Organization.find().aggregate([{"$project": {"_id": 1, "in_registry_id": 1}}]).to_list()
        return {org["_id"]: org["in_registry_id"] for org in organizations}

    async def get_username_mapping(self) -> dict[str, PydanticObjectId]:
        organizations = await Organization.find().aggregate([{"$project": {"_id": 1, "username": 1}}]).to_list()
        return {org["username"]: org["_id"] for org in organizations}

    async def create_many(self, data: list[CreateOrganization]) -> list[PydanticObjectId]:
        return await crud.create_many(data)


organization_repository: OrganizationRepository = OrganizationRepository()


async def parse_certificates_to_organizations(organizations: Certificates) -> list[CreateOrganization]:
    id_registry_mapping = await organization_repository.get_id_registry_mapping()
    username_mapping = await organization_repository.get_username_mapping()
    not_existing_ids = []

    for org in organizations.certificates:
        if org.in_registry_id not in id_registry_mapping and org.in_registry_id not in username_mapping:
            not_existing_ids.append(org.in_registry_id)

    not_existing_organizations = (org for org in organizations.certificates if org.in_registry_id in not_existing_ids)
    create_ = (
        CreateOrganization(
            in_registry_id=org.in_registry_id,
            username=org.in_registry_id,
            name=org.actual_education_organization.short_name or org.actual_education_organization.full_name,
            full_name=org.actual_education_organization.full_name,
            contacts=ContactsSchema(
                email=org.actual_education_organization.email,
                phone=org.actual_education_organization.phone,
                website=org.actual_education_organization.website,
                fax=org.actual_education_organization.fax,
                post_address=org.actual_education_organization.post_address,
                inn=org.actual_education_organization.inn,
                kpp=org.actual_education_organization.kpp,
                ogrn=org.actual_education_organization.ogrn,
            ),
            region_name=org.region_name,
            federal_district_name=org.federal_district_name,
            educational_programs=[
                EducationalProgramSchema(
                    in_registry_id=_.in_registry_id,
                    edu_level_name=_.edu_level_name,
                    program_name=_.program_name,
                    program_code=_.program_code,
                    ugs_name=_.ugs_name,
                    ugs_code=_.ugs_code,
                    edu_normative_period=_.edu_normative_period,
                    qualification=_.qualification,
                )
                for _ in org.educational_programs
            ],
        )
        for org in not_existing_organizations
        if org.actual_education_organization
    )
    return list(create_)
