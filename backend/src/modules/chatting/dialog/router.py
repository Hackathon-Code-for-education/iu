from beanie import PydanticObjectId

from src.api.custom_router_class import EnsureAuthenticatedAPIRouter
from src.api.dependencies import UserDep
from src.exceptions import NotEnoughPermissionsException, ObjectNotFound
from src.modules.chatting.dialog.repository import dialog_repository
from src.storages.mongo.models.dialog import Dialog, MessageSchema
from src.utils import aware_utcnow

router = EnsureAuthenticatedAPIRouter(prefix="/dialogs")


@router.post(
    "/leave-dialog",
    responses={200: {"description": "Success"}, **ObjectNotFound.responses, **NotEnoughPermissionsException.responses},
)
async def leave_dialog(user: UserDep, dialog_id: PydanticObjectId) -> None:
    """
    Покинуть диалог
    """
    dialog = await dialog_repository.read(dialog_id)
    if dialog is None:
        raise ObjectNotFound("Dialog not found")
    if user.id not in [dialog.student_id, dialog.enrollee_id]:
        raise NotEnoughPermissionsException("У вас недостаточно прав для покидания этого диалога")
    await dialog_repository.close_dialog(dialog.id)


@router.post(
    "/push-message",
    responses={200: {"description": "Success"}, **ObjectNotFound.responses, **NotEnoughPermissionsException.responses},
)
async def push_message(user: UserDep, dialog_id: PydanticObjectId, message: str) -> None:
    """
    Отправить сообщение в диалог
    """
    dialog = await dialog_repository.read(dialog_id)
    if dialog is None:
        raise ObjectNotFound("Диалог не найден")
    if user.id not in [dialog.student_id, dialog.enrollee_id]:
        raise NotEnoughPermissionsException("У вас недостаточно прав для отправки сообщения в этот диалог")
    _message = MessageSchema(user_id=user.id, text=message, at=aware_utcnow())
    await dialog_repository.push_message(dialog.id, _message)


@router.get(
    "/get-dialog",
    responses={200: {"description": "Success"}, **ObjectNotFound.responses, **NotEnoughPermissionsException.responses},
)
async def get_dialog(user: UserDep, dialog_id: PydanticObjectId) -> Dialog:
    """
    Получить диалог
    """
    dialog = await dialog_repository.read(dialog_id)
    if dialog is None:
        raise ObjectNotFound("Диалог не найден")
    if user.id not in [dialog.student_id, dialog.enrollee_id]:
        raise NotEnoughPermissionsException("У вас недостаточно прав для просмотра этого диалога")
    return dialog


@router.get(
    "/get-my-dialogs",
    responses={200: {"description": "Success"}},
)
async def get_my_dialogs(user: UserDep) -> list[Dialog]:
    """
    Получить мои диалоги
    """
    return await dialog_repository.read_dialogs_for_user(user.id)
