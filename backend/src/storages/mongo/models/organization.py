from typing import Any, Annotated

from beanie import Indexed, PydanticObjectId

from src.custom_pydantic import CustomModel
from src.storages.mongo.models.__base__ import CustomDocument


class OrganizationSchema(CustomModel):
    username: Annotated[str, Indexed(unique=True)]
    "Псевдоним организации (уникальный)"
    name: str
    "Наименование организации"
    contacts: Any = None
    "Контактные данные организации"
    documents: Any = None
    "Документы организации"
    main_scene: PydanticObjectId | None = None
    "Основная сцена организации"
    logo: PydanticObjectId | None = None
    "Логотип организации"


class Organization(OrganizationSchema, CustomDocument):
    pass
