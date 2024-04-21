import datetime

from beanie import PydanticObjectId
from pydantic import Field

from src.custom_pydantic import CustomModel
from src.storages.mongo import Review


class CreateReview(CustomModel):
    organization_id: PydanticObjectId
    "Идентификатор организации, к которой относится отзыв"
    user_id: PydanticObjectId
    "Идентификатор пользователя, оставившего отзыв"
    text: str | None = None
    "Текст отзыва"
    rate: int = Field(..., ge=1, le=5)
    "Оценка"


class AnonymousReview(CustomModel):
    id: PydanticObjectId
    "Идентификатор отзыва"
    text: str | None
    "Текст отзыва"
    rate: int = Field(..., ge=1, le=5)
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


class ReviewWithOrganizationInfo(Review):
    organization_name: str
    organization_username: str
