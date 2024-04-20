__all__ = ["app"]

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

import src.logging_  # noqa: F401
from src.api import docs
from src.api.docs import generate_unique_operation_id
from src.api.lifespan import lifespan
from src.api.routers import routers
from src.config import settings
from src.config_schema import Environment

# App definition
app = FastAPI(
    root_path=settings.app_root_path,
    root_path_in_servers=False,
    title=docs.TITLE,
    generate_unique_id_function=generate_unique_operation_id,
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    docs_url=None,
    redoc_url=None,
    swagger_ui_oauth2_redirect_url=None,
)

app.openapi = docs.custom_openapi(app)  # type: ignore

# CORS settings
if settings.cors_allow_origins:
    # noinspection PyTypeChecker
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origin_regex=".*" if settings.environment == Environment.DEVELOPMENT else None,
    )

# Authorization
same_site = "lax"
session_cookie = "__Secure-abitura-session" if settings.environment == Environment.PRODUCTION else "abitura-session"
# noinspection PyTypeChecker
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.auth.session_secret_key.get_secret_value(),
    session_cookie=session_cookie,
    max_age=14 * 24 * 60 * 60,  # 14 days, in seconds
    path=settings.app_root_path or "/",
    same_site=same_site,
    https_only=settings.environment == Environment.PRODUCTION,
    domain=None,
)

# Static files
if settings.static_files is not None:
    from starlette.staticfiles import StaticFiles

    app.mount(
        settings.static_files.mount_path,
        StaticFiles(directory=settings.static_files.directory),
        name=settings.static_files.mount_name,
    )

# Mock utilities
if settings.environment == Environment.DEVELOPMENT:
    from fastapi_mock import MockUtilities  # type: ignore

    MockUtilities(app, return_example_instead_of_500=True)


# Redirect root to docs
@app.get("/", tags=["Root"], include_in_schema=False)
async def redirect_to_docs(request: Request):
    return RedirectResponse(url=request.url_for("swagger_ui_html"))


# noinspection PyUnresolvedReferences
@app.get("/docs", tags=["System"], include_in_schema=False)
async def swagger_ui_html(request: Request):
    root_path = request.scope.get("root_path", "").rstrip("/")

    openapi_url = root_path + app.openapi_url

    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="https://api.innohassle.ru/swagger/swagger-ui-bundle.js",
        swagger_css_url="https://api.innohassle.ru/swagger/swagger-ui.css",
        swagger_favicon_url="https://api.innohassle.ru/swagger/favicon.png",
        swagger_ui_parameters={"tryItOutEnabled": True, "persistAuthorization": True, "filter": True},
    )


for router in routers:
    app.include_router(router)
