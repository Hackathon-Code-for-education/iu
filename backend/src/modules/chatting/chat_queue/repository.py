import datetime

from beanie import PydanticObjectId

from src.custom_pydantic import CustomModel
from src.utils import aware_utcnow

TIMEOUT = datetime.timedelta(seconds=30)


class ChatQueueItem(CustomModel):
    organization_id: PydanticObjectId
    students_queue: dict[PydanticObjectId, datetime.datetime] = {}
    enrollees_queue: dict[PydanticObjectId, datetime.datetime] = {}


class DialogPair(CustomModel):
    organization_id: PydanticObjectId
    student_id: PydanticObjectId
    enrollee_id: PydanticObjectId


class ChatQueueRepository:
    _queue: dict[PydanticObjectId, ChatQueueItem]
    _stashed: dict[PydanticObjectId, DialogPair]

    def __init__(self):
        self._queue = dict()

    def get_queue_lengths(self, organization_id: PydanticObjectId) -> tuple[int, int]:
        if organization_id not in self._queue:
            return 0, 0

        queue = self._queue[organization_id]
        return len(queue.students_queue), len(queue.enrollees_queue)

    def remove_outdated(self):
        now = aware_utcnow()
        to_be_removed = set()
        for queue in self._queue.values():
            queue.students_queue = {
                user_id: last_seen for user_id, last_seen in queue.students_queue.items() if now - last_seen < TIMEOUT
            }
            queue.enrollees_queue = {
                user_id: last_seen for user_id, last_seen in queue.enrollees_queue.items() if now - last_seen < TIMEOUT
            }

            if not queue.students_queue and not queue.enrollees_queue:
                to_be_removed.add(queue.organization_id)

        for organization_id in to_be_removed:
            self._queue.pop(organization_id)

    def update_queue(
        self, user_id: PydanticObjectId, organization_id: PydanticObjectId, is_student: bool = True
    ) -> DialogPair | None:
        if organization_id not in self._queue:
            self._queue[organization_id] = ChatQueueItem(organization_id=organization_id)

        queue = self._queue[organization_id]

        # check for collision
        if user_id in queue.students_queue and user_id in queue.enrollees_queue:
            queue.students_queue.pop(user_id, None)
            queue.enrollees_queue.pop(user_id, None)

        if is_student:
            queue.students_queue[user_id] = aware_utcnow()
        else:
            queue.enrollees_queue[user_id] = aware_utcnow()

        self.remove_outdated()
        return self.get_pair(user_id, organization_id, is_student)

    def get_pair(
        self, user_id: PydanticObjectId, organization_id: PydanticObjectId, is_student: bool = True
    ) -> DialogPair | None:
        if organization_id not in self._queue:
            return None

        queue = self._queue[organization_id]

        if is_student:
            enrollee_id = next(iter(queue.enrollees_queue), None)
            if enrollee_id is None:
                return None
            return DialogPair(organization_id=organization_id, student_id=user_id, enrollee_id=enrollee_id)
        else:
            student_id = next(iter(queue.students_queue), None)
            if student_id is None:
                return None
            return DialogPair(organization_id=organization_id, student_id=student_id, enrollee_id=user_id)

    def remove_dialog_pair(self, dialog_pair: DialogPair):
        if dialog_pair.organization_id not in self._queue:
            return

        queue = self._queue[dialog_pair.organization_id]
        queue.students_queue.pop(dialog_pair.student_id, None)
        queue.enrollees_queue.pop(dialog_pair.enrollee_id, None)

    def leave_queue(self, user_id: PydanticObjectId, organization_id: PydanticObjectId) -> None:
        if organization_id not in self._queue:
            return

        queue = self._queue[organization_id]
        queue.students_queue.pop(user_id, None)
        queue.enrollees_queue.pop(user_id, None)


chat_queue_repository: ChatQueueRepository = ChatQueueRepository()
