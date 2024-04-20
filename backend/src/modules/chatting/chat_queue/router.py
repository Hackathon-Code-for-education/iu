__all__ = ["router"]

from beanie import PydanticObjectId

from src.api.custom_router_class import EnsureAuthenticatedAPIRouter
from src.api.dependencies import UserDep
from src.exceptions import NotEnoughPermissionsException
from src.modules.chatting.chat_queue.repository import chat_queue_repository
from src.modules.chatting.chat_queue.schemas import JoinDialog, OnlineOfQueue, UpdateQueueResponse

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

    if pair is not None:
        return JoinDialog(dialog=pair)

    queue_students_online, queue_enrollees_online = chat_queue_repository.get_queue_lengths(organization_id)

    return OnlineOfQueue(queue_students_online=queue_students_online, queue_enrollees_online=queue_enrollees_online)


@router.post(
    "/update-students-queue",
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

    if pair is not None:
        return JoinDialog(dialog=pair)

    queue_students_online, queue_enrollees_online = chat_queue_repository.get_queue_lengths(organization_id)

    return OnlineOfQueue(queue_students_online=queue_students_online, queue_enrollees_online=queue_enrollees_online)
