from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml
from beanie import PydanticObjectId
from pydantic import Field, SecretStr, ConfigDict, field_validator, BaseModel

from src.storages.mongo.schemas import UserRole


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class SettingsEntityModel(BaseModel):
    model_config = ConfigDict(use_attribute_docstrings=True, extra="forbid")


class Authentication(SettingsEntityModel):
    allowed_domains: list[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    "Allowed domains for redirecting after authentication"
    session_secret_key: SecretStr
    "Secret key for sessions. Use 'openssl rand -hex 32' to generate keys"


class StaticFiles(SettingsEntityModel):
    mount_path: str = "/static"
    mount_name: str = "static"
    directory: Path = Path("static")

    @field_validator("directory", mode="after")
    def validate_directory(cls, value: Path) -> Path:
        if not value.exists():
            raise ValueError(f"Directory {value} does not exist")
        if not value.is_dir():
            raise ValueError(f"{value} is not a directory")
        return value


class Database(SettingsEntityModel):
    uri: SecretStr
    "Database URI. If not set, will be generated from other settings"


class PredefinedUser(SettingsEntityModel):
    role: UserRole = UserRole.DEFAULT
    name: str
    login: str
    password: str
    student_at_organization_username: str | None = None
    "ID of the organization where the student is approved"


class PredefinedScene(SettingsEntityModel):
    id: PydanticObjectId
    "Scene ID"
    title: str
    "Scene title"
    organization_username: str
    "Organization Username"
    file: PydanticObjectId
    "File ID"
    meta: Any | None = None
    "Meta information for panorama view"
    is_main: bool = False
    "Is main scene"


class Predefined(SettingsEntityModel):
    """Predefined settings. Will be used in setup stage."""

    users: list[PredefinedUser] = []
    "Predefined users"
    scenes: list[PredefinedScene] = []
    "Predefined scenes"
    organizations_file: Path | None = None
    "Path to the organizations file (output of `parse_organizations.py`)"


class Telegram(SettingsEntityModel):
    bot_username: str
    "Bot username for Telegram"
    bot_token: SecretStr
    "Bot token for Telegram"


class Settings(SettingsEntityModel):
    """
    Settings for the application.
    """

    model_config = ConfigDict(json_schema_extra={"title": "Settings"}, extra="ignore")

    environment: Environment = Environment.DEVELOPMENT
    "App environment flag"
    app_root_path: str = "/api"
    "Prefix for the API path (e.g. '/api/v0')"
    database: Database
    "MongoDB database settings"
    predefined: Predefined = Field(default_factory=Predefined)
    "Predefined settings"
    # Static files
    static_files: StaticFiles = Field(default_factory=StaticFiles)
    "Static files settings"
    # Security
    cors_allow_origins: list[str] = Field(default_factory=lambda: ["https://amritb.github.io"])
    "CORS origins, used by FastAPI CORSMiddleware"
    # Authentication
    auth: Authentication
    "Authentication settings"
    telegram: Telegram | None = None
    "Telegram Bot settings for authorization"
    https_only_cookie: bool = False
    "Use HTTPS only for SessionMiddleware"
    secure_prefix_cookie: bool = False
    "Add `__Secure-` prefix to session cookie"
    wildcard_allow_origin_regex: bool = True
    "Allow all origins for CORS"

    @classmethod
    def from_yaml(cls, path: Path) -> "Settings":
        with open(path, "r", encoding="utf-8") as f:
            yaml_config = yaml.safe_load(f)

        return cls.model_validate(yaml_config)

    @classmethod
    def save_schema(cls, path: Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            schema = {"$schema": "https://json-schema.org/draft-07/schema#", **cls.model_json_schema()}
            yaml.dump(schema, f, sort_keys=False)
