from typing import Literal, Annotated

from beanie import PydanticObjectId
from pydantic import Discriminator

from src.custom_pydantic import CustomModel


class JoinDialog(CustomModel):
    type: Literal["join_dialog"] = "join_dialog"
    dialog_id: PydanticObjectId


class OnlineOfQueue(CustomModel):
    type: Literal["online"] = "online"
    queue_students_online: int
    queue_enrollees_online: int


UpdateQueueResponse = Annotated[OnlineOfQueue | JoinDialog, Discriminator("type")]
