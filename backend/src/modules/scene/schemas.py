# mypy: disable-error-code="assignment"
from typing import Any

from beanie import PydanticObjectId

from src.storages.mongo.models.scene import SceneSchema


class CreateScene(SceneSchema):
    pass


class UpdateScene(SceneSchema):
    organization: PydanticObjectId | None = None
    file: PydanticObjectId | None = None
    meta: Any = None
