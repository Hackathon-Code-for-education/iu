import re
from inspect import cleandoc
from types import ModuleType

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute

import src.modules.providers.router
import src.modules.user.router
from src.config import settings

# API version
VERSION = "0.1.0"

# Info for OpenAPI specification
TITLE = "Abitura API"
SUMMARY = "Сервис абитурента"

DESCRIPTION = None

CONTACT_INFO = None

LICENSE_INFO = None


def safe_cleandoc(doc: str | None) -> str:
    return cleandoc(doc) if doc else ""


def doc_from_module(module: ModuleType) -> str:
    return safe_cleandoc(module.__doc__)


TAGS_INFO = [
    {"name": "Users", "description": doc_from_module(src.modules.user.router)},
    {"name": "Providers", "description": doc_from_module(src.modules.providers.router)},
]


def generate_unique_operation_id(route: APIRoute) -> str:
    # Better names for operationId in OpenAPI schema.
    # It is needed because clients generate code based on these names.
    # Requires pair (tag name + function name) to be unique.
    # See fastapi.utils:generate_unique_id (default implementation).
    if route.tags:
        operation_id = f"{route.tags[0]}_{route.name}".lower()
    else:
        operation_id = route.name.lower()
    operation_id = re.sub(r"\W+", "_", operation_id)
    return operation_id


def custom_openapi(app: FastAPI):
    def inner():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=TITLE,
            summary=SUMMARY,
            description=DESCRIPTION,
            version=VERSION,
            contact=CONTACT_INFO,
            license_info=LICENSE_INFO,
            tags=TAGS_INFO,
            servers=[
                {"url": settings.app_root_path, "description": "Current"},
            ],
            routes=app.routes,
            separate_input_output_schemas=True,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return inner
