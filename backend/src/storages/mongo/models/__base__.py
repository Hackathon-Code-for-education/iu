__all__ = ["CustomDocument", "CustomLink"]

import datetime
from typing import Type, Any, TypeVar, Annotated, Union

from beanie import Document, PydanticObjectId, Link
from beanie.odm.utils.parsing import parse_obj
from beanie.odm.registry import DocsRegistry
from bson import DBRef
from pydantic import (
    Field,
    ConfigDict,
    GetCoreSchemaHandler,
    WithJsonSchema,
    GetJsonSchemaHandler,
    TypeAdapter,
    BaseModel,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
from pydantic_core.core_schema import ValidationInfo
from typing_extensions import TypedDict, get_args

MongoDbIdSchema = {
    "type": "string",
    "format": "objectid",
    "example": "5eb7cf5a86d9755df3a6c593",
}
MongoDbId = Annotated[
    PydanticObjectId,
    WithJsonSchema(
        MongoDbIdSchema,
        mode="serialization",
    ),
]


class CustomDocument(Document):
    model_config = ConfigDict(json_schema_serialization_defaults_required=True)

    id: MongoDbId = Field(  # type: ignore[assignment]
        default=None, description="MongoDB document ObjectID", serialization_alias="id"
    )

    class Settings:
        keep_nulls = False
        max_nesting_depth = 1
        bson_encoders = {datetime.time: lambda x: x.isoformat()}

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        __core_schema: CoreSchema,
        __handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        schema = super().__get_pydantic_json_schema__(__core_schema, __handler)
        if __handler.mode == "serialization":
            if "required" in schema and "id" not in schema["required"]:
                schema["required"].append("id")
            if "required" not in schema:
                schema["required"] = ["id"]
        return schema


D = TypeVar("D", bound=Document)


class _Reference(TypedDict):
    id: str


reference_type_adapter = TypeAdapter(_Reference)


class CustomLink(Link[D]):
    @classmethod
    def build_validation(cls, handler, source_type):
        def validate(v: Union[DBRef, D, dict, BaseModel], validation_info: ValidationInfo):
            document_class = DocsRegistry.evaluate_fr(get_args(source_type)[0])

            if isinstance(v, DBRef):
                return cls(ref=v, document_class=document_class)
            if isinstance(v, Link):
                return v
            if isinstance(v, dict) and v.keys() == {"id", "collection"}:
                return cls(
                    ref=DBRef(
                        collection=v["collection"],
                        id=TypeAdapter(document_class.model_fields["id"].annotation).validate_python(v["id"]),
                    ),
                    document_class=document_class,
                )
            if isinstance(v, dict) and v.keys() == {"id"}:
                return cls(
                    ref=DBRef(
                        collection=document_class.get_collection_name(),
                        id=TypeAdapter(document_class.model_fields["id"].annotation).validate_python(v["id"]),
                    ),
                    document_class=document_class,
                )
            if isinstance(v, dict) or isinstance(v, BaseModel):
                return parse_obj(document_class, v)
            new_id = TypeAdapter(document_class.model_fields["id"].annotation).validate_python(v)
            ref = DBRef(collection=document_class.get_collection_name(), id=new_id)
            return cls(ref=ref, document_class=document_class)

        return validate

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Type[Any], handler: GetCoreSchemaHandler) -> CoreSchema:
        # document_class = DocsRegistry.evaluate_fr(get_args(source_type)[0])
        # document_class: Type[Document]

        serialization_schema = core_schema.plain_serializer_function_ser_schema(
            lambda instance: cls.serialize(instance),
            return_schema=core_schema.typed_dict_schema({"id": core_schema.typed_dict_field(core_schema.str_schema())}),
        )

        source_type_link_ref = source_type.__name__ + "Link"

        schema = core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(cls.build_validation(handler, source_type)),
            json_schema=core_schema.with_default_schema(core_schema.str_schema(), default="5eb7cf5a86d9755df3a6c593"),
            ref=source_type_link_ref,
            serialization=serialization_schema,
        )

        return schema

    @classmethod
    def serialize(cls, value: Union["Link", Document]) -> _Reference:  # type: ignore[override]
        if isinstance(value, Link):
            return _Reference(id=value.ref.id.__str__())
        else:
            assert value.id is not None
            return _Reference(id=value.id.__str__())
