from enum import StrEnum
from pathlib import Path

import yaml
from pydantic import Field, SecretStr, ConfigDict, field_validator

from src.custom_pydantic import CustomModel


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Authentication(CustomModel):
    allowed_domains: list[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    "Allowed domains for redirecting after authentication"
    session_secret_key: SecretStr
    "Secret key for sessions. Use 'openssl rand -hex 32' to generate keys"


class StaticFiles(CustomModel):
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


class Database(CustomModel):
    uri: SecretStr
    "Database URI. If not set, will be generated from other settings"


class Predefined(CustomModel):
    """Predefined settings. Will be used in setup stage."""

    first_superuser_login: str = "admin"
    "Login for the first superuser"
    first_superuser_password: str = "admin"
    "Password for the first superuser"


class Telegram(CustomModel):
    bot_username: str
    "Bot username for Telegram"
    bot_token: SecretStr
    "Bot token for Telegram"


class Settings(CustomModel):
    """
    Settings for the application.
    """

    model_config = ConfigDict(json_schema_extra={"title": "Settings"}, extra="ignore")

    environment: Environment = Environment.DEVELOPMENT
    "App environment flag"
    app_root_path: str = ""
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
