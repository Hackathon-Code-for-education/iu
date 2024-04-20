from beanie import PydanticObjectId

from src.modules.chatting.dialog.schemas import CreateDialog
from src.storages.mongo.models.dialog import Dialog, MessageSchema


# noinspection PyMethodMayBeStatic
class DialogRepository:
    async def create(self, obj: CreateDialog) -> Dialog:
        if obj.title is None:
            from src.modules.organization.repository import organization_repository

            organization = await organization_repository.read(obj.organization_id)
            title = f"{organization.name} - Студент X"
            obj.title = title
        return await Dialog.model_validate(obj.model_dump()).insert()

    async def read(self, obj_id: PydanticObjectId) -> Dialog | None:
        return await Dialog.find_one({"_id": obj_id})

    async def read_dialogs_for_user(self, user_id: PydanticObjectId) -> list[Dialog]:
        objs = await Dialog.find({"$or": [{"student_id": user_id}, {"enrollee_id": user_id}]}).to_list()
        return objs

    async def push_message(self, dialog_id: PydanticObjectId, message: MessageSchema) -> None:
        await Dialog.find({"_id": dialog_id}).update({"$push": {"messages": message.model_dump()}})

    async def close_dialog(self, dialog_id) -> None:
        await Dialog.find({"_id": dialog_id}).update({"$set": {"closed": True}})


dialog_repository: DialogRepository = DialogRepository()
