# mypy: disable-error-code="assignment"
from src.custom_pydantic import CustomModel


class UpdateFile(CustomModel):
    friendly_name: str | None = None
    must_be_uploaded: bool | None = None
