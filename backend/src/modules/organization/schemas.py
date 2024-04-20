# mypy: disable-error-code="assignment"

from src.storages.mongo.models.organization import OrganizationSchema


class CreateOrganization(OrganizationSchema):
    pass


class UpdateOrganization(OrganizationSchema):
    name: str | None = None
