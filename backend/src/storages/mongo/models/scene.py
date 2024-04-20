from typing import Any

from beanie import PydanticObjectId

from src.custom_pydantic import CustomModel
from src.storages.mongo.models.__base__ import CustomDocument


class SceneSchema(CustomModel):
    organization: PydanticObjectId
    file: PydanticObjectId
    meta: Any | None = None


class Scene(SceneSchema, CustomDocument):
    pass
