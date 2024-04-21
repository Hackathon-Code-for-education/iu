from typing import Any

from beanie import PydanticObjectId
from pydantic import ConfigDict
from pymongo import IndexModel

from src.custom_pydantic import CustomModel
from src.storages.mongo.models.__base__ import CustomDocument


class EducationalProgramSchema(CustomModel):
    in_registry_id: str
    "Идентификатор образовательной программы в реестре"
    edu_level_name: str
    "Наименование уровня образования"
    program_name: str
    "Наименование образовательной программы"
    program_code: str | None = None
    "Код образовательной программы"
    ugs_name: str | None = None
    "Наименование направления подготовки"
    ugs_code: str | None = None
    "Код направления подготовки"
    edu_normative_period: str | None = None
    "Нормативный срок обучения"
    qualification: str | None = None
    "Квалификация выпускника"


class ContactsSchema(CustomModel):
    model_config = ConfigDict(extra="allow")

    post_address: str | None = None
    "Почтовый адрес"
    phone: str | None = None
    "Телефон"
    fax: str | None = None
    "Факс"
    email: str | None = None
    "Электронная почта"
    website: str | None = None
    "Сайт"
    ogrn: str | None = None
    "ОГРН"
    inn: str | None = None
    "ИНН"
    kpp: str | None = None
    "КПП"


class OrganizationSchema(CustomModel):
    username: str
    "Псевдоним организации (уникальный)"
    name: str
    "Наименование организации"
    full_name: str
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
    educational_programs: list[EducationalProgramSchema] = []
    "Образовательные программы организации"


class Organization(OrganizationSchema, CustomDocument):
    class Settings:
        indexes = [
            IndexModel([("username", 1)], unique=True),
            IndexModel([("in_registry_id", 1)]),
        ]
