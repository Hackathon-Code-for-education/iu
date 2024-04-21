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
