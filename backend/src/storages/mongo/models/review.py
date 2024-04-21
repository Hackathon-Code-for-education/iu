import datetime

from beanie import PydanticObjectId
from pydantic import Field

from src.custom_pydantic import CustomModel
from src.storages.mongo.models.__base__ import CustomDocument


class ReviewSchema(CustomModel):
    organization_id: PydanticObjectId
    "Идентификатор организации, к которой относится отзыв"
    user_id: PydanticObjectId
    "Идентификатор пользователя, оставившего отзыв"
    liked_by: list[PydanticObjectId] = []
    "Список пользователей, которым понравился отзыв"
    text: str | None = None
    "Текст отзыва"
    rate: int = Field(..., ge=1, le=5)
    "Оценка"
    at: datetime.datetime
    "Дата и время создания отзыва"


class Review(ReviewSchema, CustomDocument):
    pass
