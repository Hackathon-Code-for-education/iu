from typing import TypeVar, Type, Any, Mapping, Union, Generic, cast

from beanie import Document, PydanticObjectId
from beanie.exceptions import RevisionIdWasChanged
from beanie.odm.operators.find.comparison import In
from beanie.odm.operators.update.general import Set
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError

from src.exceptions import AlreadyExists

D = TypeVar("D", bound=Document)
Projection = TypeVar("Projection", bound=BaseModel)
Create = TypeVar("Create", bound=BaseModel, contravariant=True)
Update = TypeVar("Update", bound=BaseModel)


class IdOnlyProjection(BaseModel):
    id: PydanticObjectId


class CRUD(Generic[D, Create, Update]):
    fetch_links: bool
    document_class: Type[D]

    def __init__(self, document_class: Type[D], fetch_links: bool):
        self.document_class = document_class
        self.fetch_links = fetch_links

    async def create(self, data: Create) -> D:
        _ = self.document_class.model_validate(data, from_attributes=True)
        return await self.document_class.create(_)

    async def create_many(self, data: list[Create]) -> list[PydanticObjectId]:
        _ = [self.document_class.model_validate(item, from_attributes=True) for item in data]
        return (await self.document_class.insert_many(_)).inserted_ids

    async def read(
        self, id: PydanticObjectId, *, projection_model: type[Projection] | None = None
    ) -> Projection | D | None:
        return await self.document_class.find_one(
            self.document_class.id == id, fetch_links=self.fetch_links, projection_model=projection_model
        )

    async def read_by(
        self, *criterias: Union[Mapping[str, Any], bool], projection_model: type[Projection] | None = None
    ) -> Projection | D | None:
        _res = await self.document_class.find_one(
            *criterias, fetch_links=self.fetch_links, projection_model=projection_model
        )
        if projection_model is None:
            return cast(D, _res)
        return cast(Projection, _res)

    async def read_many(self, obj_ids: list[PydanticObjectId]) -> dict[PydanticObjectId, D | None]:
        objs = await self.document_class.find_many(In(self.document_class.id, obj_ids)).to_list()
        mapping = dict.fromkeys(obj_ids)
        for existing_obj in objs:
            assert existing_obj.id is not None
            mapping[existing_obj.id] = existing_obj
        return mapping

    async def read_all(self, *, projection_model: type[Projection] | None = None) -> list[D] | list[Projection]:
        _res = await self.document_class.all(projection_model=projection_model).to_list()
        if projection_model is None:
            return cast(list[D], _res)
        return cast(list[Projection], _res)

    async def update(self, id: PydanticObjectId, data: Update) -> D | None:
        obj = await self.document_class.find_one({"_id": id})
        if obj is None:
            return None
        try:
            updated = await obj.update(Set(data.model_dump(exclude_unset=True)))
        except RevisionIdWasChanged as e:
            if e.__context__ is not None and isinstance(e.__context__, DuplicateKeyError):
                duplicate_key_error = e.__context__

                detals = {"keyValue": None}
                if duplicate_key_error.details:
                    detals["keyValue"] = duplicate_key_error.details.get("keyValue")
                raise AlreadyExists(f"Объект с такими свойствами уже существует: {detals}")
            raise e
        return updated

    async def delete(self, id: PydanticObjectId) -> bool:
        obj = await self.document_class.find_one({"_id": id})
        if obj is None:
            return False
        delete_result = await obj.delete()
        return delete_result.deleted_count > 0


def crud_factory(document_class: Type[D], fetch_links: bool = False) -> CRUD:
    return CRUD(document_class, fetch_links=fetch_links)
