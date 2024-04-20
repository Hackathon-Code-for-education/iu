from src.custom_pydantic import CustomModel
from src.storages.mongo.models.__base__ import CustomDocument


class OrganizationSchema(CustomModel):
    name: str
    "Наименование организации"


class Organization(OrganizationSchema, CustomDocument):
    pass
