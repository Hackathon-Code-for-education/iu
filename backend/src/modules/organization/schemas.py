# mypy: disable-error-code="assignment"
from typing import Any

from beanie import PydanticObjectId

from src.storages.mongo.models.organization import OrganizationSchema


class CreateOrganization(OrganizationSchema):
    pass


class UpdateOrganization(OrganizationSchema):
    username: str | None = None
    name: str | None = None
    contacts: Any | None = None
    documents: Any | None = None
    main_scene: PydanticObjectId | None = None
