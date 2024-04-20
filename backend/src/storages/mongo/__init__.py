from typing import cast

from beanie import Document, View

from src.storages.mongo.models.user import User
from src.storages.mongo.models.file import File
from src.storages.mongo.models.organization import Organization
from src.storages.mongo.models.scene import Scene

document_models = cast(list[type[Document] | type[View] | str], [User, File, Organization, Scene])
