__all__ = ["online_repository"]

import datetime

from beanie import PydanticObjectId

from src.utils import aware_utcnow

TIMEOUT = datetime.timedelta(minutes=5)


class OnlineRepository:
    _online: dict[PydanticObjectId, datetime.datetime]

    def __init__(self):
        self._online = {}

    def i_am_online(self, user_id: PydanticObjectId):
        self._online[user_id] = aware_utcnow()

    def get_online_users(self) -> list[PydanticObjectId]:
        now = aware_utcnow()
        return [user_id for user_id, last_seen in self._online.items() if now - last_seen < TIMEOUT]


online_repository: OnlineRepository = OnlineRepository()
