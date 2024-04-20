from typing import Any

from beanie import Indexed

from src.custom_pydantic import CustomModel
from src.storages.mongo.models.__base__ import CustomDocument


class OrganizationSchema(CustomModel):
    username: Indexed(str, unique=True)
    "Псевдоним организации (уникальный)"
    name: str
    "Наименование организации"
    contacts: Any = None
    "Контактные данные организации"
    documents: Any = None
    "Документы организации"


class Organization(OrganizationSchema, CustomDocument):
    pass
