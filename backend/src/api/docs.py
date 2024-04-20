import re

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute

from src.config import settings

# API version
VERSION = "0.1.0"

# Info for OpenAPI specification
TITLE = "AbiTour API"
SUMMARY = "Сервис абитурента"

DESCRIPTION = None

CONTACT_INFO = {"url": "https://t.me/one_zero_eight"}
LICENSE_INFO = {"name": "MIT License"}

TAGS_INFO = [
    {"name": "Users", "description": "Модуль для работы с пользователями"},
    {"name": "Providers", "description": "Модуль для работы с провайдерами авторизации"},
    {"name": "Files", "description": "Модуль для работы с файлами"},
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
