__all__ = ["router"]

from beanie import PydanticObjectId

from src.api.custom_router_class import EnsureAuthenticatedAPIRouter
from src.api.dependencies import UserDep
from src.exceptions import NotEnoughPermissionsException
from src.modules.chatting.chat_queue.repository import chat_queue_repository
from src.modules.chatting.chat_queue.schemas import JoinDialog, OnlineOfQueue, UpdateQueueResponse
from src.modules.chatting.dialog.repository import dialog_repository
from src.modules.chatting.dialog.schemas import CreateDialog

router = EnsureAuthenticatedAPIRouter(prefix="/chat-queue")


@router.post(
    "/update-enrollee-queue/{organization_id}",
    responses={200: {"description": "Success"}},
)
async def update_queue(user: UserDep, organization_id: PydanticObjectId) -> UpdateQueueResponse:
    """
    Обновить своё место в очереди абитуриентов
    """
    pair = chat_queue_repository.update_queue(user.id, organization_id, is_student=False)

    if pair:
        # create dialog if not exists
        dialog = await dialog_repository.create_if_not_exists(
            CreateDialog(
                organization_id=organization_id,
                student_id=pair.student_id,
                enrollee_id=pair.enrollee_id,
            )
        )
        return JoinDialog(dialog_id=dialog.id)

    queue_students_online, queue_enrollees_online = chat_queue_repository.get_queue_lengths(organization_id)

    return OnlineOfQueue(queue_students_online=queue_students_online, queue_enrollees_online=queue_enrollees_online)


@router.post(
    "/update-students-queue/{organization_id}",
    responses={200: {"description": "Success"}, **NotEnoughPermissionsException.responses},
)
async def update_students_queue(user: UserDep, organization_id: PydanticObjectId) -> UpdateQueueResponse:
    """
    Обновить своё место в очереди студентов
    """

    # check approvement
    if not user.is_approved(organization_id):
        raise NotEnoughPermissionsException("У вас недостаточно прав для вступления в очередь ожидания")

    pair = chat_queue_repository.update_queue(user.id, organization_id, is_student=True)

    if pair:
        # create dialog if not exists
        dialog = await dialog_repository.create_if_not_exists(
            CreateDialog(
                organization_id=organization_id,
                student_id=pair.student_id,
                enrollee_id=pair.enrollee_id,
            )
        )
        return JoinDialog(dialog_id=dialog.id)

    queue_students_online, queue_enrollees_online = chat_queue_repository.get_queue_lengths(organization_id)
    return OnlineOfQueue(queue_students_online=queue_students_online, queue_enrollees_online=queue_enrollees_online)


@router.post("/leave-queue/{organization_id}", responses={200: {"description": "Success"}})
async def leave_queue(user: UserDep, organization_id: PydanticObjectId) -> None:
    """
    Покинуть очередь
    """
    chat_queue_repository.leave_queue(user.id, organization_id)
    return None
