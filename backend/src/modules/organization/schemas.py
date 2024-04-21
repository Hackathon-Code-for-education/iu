# mypy: disable-error-code="assignment"
from typing import Any

from beanie import PydanticObjectId
from pydantic import Field

from src.custom_pydantic import CustomModel
from src.storages.mongo.models.__base__ import MongoDbId
from src.storages.mongo.models.organization import OrganizationSchema, ContactsSchema, EducationalProgramSchema


class CreateOrganization(OrganizationSchema):
    pass


class UpdateOrganization(OrganizationSchema):
    username: str | None = None
    "Псевдоним организации (уникальный)"
    name: str | None = None
    "Наименование организации"
    full_name: str | None = None
    "Полное наименование организации"
    contacts: ContactsSchema | None = None
    "Контактные данные организации"
    documents: Any = None
    "Документы организации"
    main_scene: PydanticObjectId | None = None
    "Основная сцена организации"
    logo: PydanticObjectId | None = None
    "Логотип организации"
    in_registry_id: str | None = None
    "Идентификатор организации в реестре"
    region_name: str | None = None
    "Наименование региона"
    federal_district_name: str | None = None
    "Наименование федерального округа"
    educational_programs: list[EducationalProgramSchema] | None = None
    "Образовательные программы организации"


class CompactOrganization(CustomModel):
    id: MongoDbId = Field(
        ..., description="MongoDB document ObjectID", serialization_alias="id", validation_alias="_id"
    )
    username: str
    "Псевдоним организации (уникальный)"
    name: str
    "Наименование организации"
    logo: PydanticObjectId | None = None
    "Логотип организации"
