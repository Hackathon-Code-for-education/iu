import datetime

from beanie import PydanticObjectId
from pydantic import Field

from src.custom_pydantic import CustomModel
from src.storages.mongo.models.__base__ import CustomDocument


class MessageSchema(CustomModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    "ID сообщения"
    user_id: PydanticObjectId
    "ID пользователя, отправившего сообщение"
    text: str
    "Текст сообщения"
    at: datetime.datetime
    "Дата отправки сообщения"


class DialogSchema(CustomModel):
    organization_id: PydanticObjectId
    "ID организации"
    student_id: PydanticObjectId
    "ID студента"
    enrollee_id: PydanticObjectId
    "ID абитуриента"
    messages: list[MessageSchema] = []
    "Сообщения в диалоге"
    closed: bool = False
    "Закрыт ли диалог"
    title: str | None = None
    "Название диалога"


class Dialog(DialogSchema, CustomDocument):
    pass
