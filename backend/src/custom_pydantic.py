from pydantic import BaseModel, ConfigDict


class CustomModel(BaseModel):
    model_config = ConfigDict(use_attribute_docstrings=True, json_schema_serialization_defaults_required=True)
