from typing import Any

from src.custom_pydantic import CustomModel
from src.storages.mongo import File, Organization
from src.storages.mongo.models.__base__ import CustomDocument, CustomLink


class SceneSchema(CustomModel):
    organization: CustomLink[Organization]
    file: CustomLink[File]
    meta: Any | None = None


class Scene(SceneSchema, CustomDocument):
    pass
