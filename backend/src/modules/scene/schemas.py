# mypy: disable-error-code="assignment"
from typing import Any

from src.storages.mongo import Organization, File
from src.storages.mongo.models.__base__ import CustomLink
from src.storages.mongo.models.scene import SceneSchema


class CreateScene(SceneSchema):
    pass


class UpdateScene(SceneSchema):
    organization: CustomLink[Organization] | None = None
    file: CustomLink[File] | None = None
    meta: Any | None = None
