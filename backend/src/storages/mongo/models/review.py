import datetime
from enum import StrEnum

from beanie import PydanticObjectId

from src.custom_pydantic import CustomModel
from src.storages.mongo.models.__base__ import CustomDocument


class ReviewRateEnum(StrEnum):
    """Перечисление возможных оценок"""

    BAD = "BAD"
    "Плохо"
    NORMAL = "NORMAL"
    "Нормально"
    GOOD = "GOOD"
    "Хорошо"
    EXCELLENT = "EXCELLENT"
    "Отлично"


class ReviewSchema(CustomModel):
    organization_id: PydanticObjectId
    "Идентификатор организации, к которой относится отзыв"
    user_id: PydanticObjectId
    "Идентификатор пользователя, оставившего отзыв"
    liked_by: list[PydanticObjectId] = []
    "Список пользователей, которым понравился отзыв"
    text: str | None = None
    "Текст отзыва"
    rate: ReviewRateEnum
    "Оценка"
    at: datetime.datetime
    "Дата и время создания отзыва"


class Review(ReviewSchema, CustomDocument):
    pass
