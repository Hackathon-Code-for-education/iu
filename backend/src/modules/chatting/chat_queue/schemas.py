from typing import Literal, Annotated

from pydantic import Discriminator

from src.custom_pydantic import CustomModel
from src.modules.chatting.chat_queue.repository import DialogPair


class JoinDialog(CustomModel):
    type: Literal["join_dialog"] = "join_dialog"
    dialog: DialogPair


class OnlineOfQueue(CustomModel):
    type: Literal["online"] = "online"
    queue_students_online: int
    queue_enrollees_online: int


UpdateQueueResponse = Annotated[OnlineOfQueue | JoinDialog, Discriminator("type")]
