from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    DEFAULT = "default"
