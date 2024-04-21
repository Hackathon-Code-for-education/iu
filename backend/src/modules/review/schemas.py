import datetime

from beanie import PydanticObjectId

from src.custom_pydantic import CustomModel
from src.storages.mongo.models.review import ReviewRateEnum


class CreateReview(CustomModel):
    organization_id: PydanticObjectId
    "Идентификатор организации, к которой относится отзыв"
    user_id: PydanticObjectId
    "Идентификатор пользователя, оставившего отзыв"
    text: str | None = None
    "Текст отзыва"
    rate: ReviewRateEnum
    "Оценка"


class AnonymousReview(CustomModel):
    id: PydanticObjectId
    "Идентификатор отзыва"
    text: str | None
    "Текст отзыва"
    rate: ReviewRateEnum
    "Оценка"
    anonymous_name: str
    "Имя анонимного пользователя"
    mine: bool
    "Отзыв оставлен мной"
    likes: int
    "Количество лайков"
    liked_by_me: bool | None
    "Поставлен ли лайк мной"
    at: datetime.datetime
    "Дата и время создания отзыва"
