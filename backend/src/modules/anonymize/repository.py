from zlib import crc32

from beanie import PydanticObjectId

from src.modules.review.schemas import AnonymousReview
from src.storages.mongo import Review

# Список прилагательных и существительных
adjectives = ["Неопознанный", "Таинственный", "Загадочный", "Скрытный", "Летучий"]
nouns = [
    "Осьминог",
    "Кракен",
    "Дельфин",
    "Кит",
    "Акула",
    "Нарвал",
    "Медуза",
    "Морж",
    "Пингвин",
    "Черепаха",
    "Лев",
    "Тигр",
    "Дракон",
    "Феникс",
    "Грифон",
    "Единорог",
    "Цербер",
    "Пегас",
    "Вампир",
    "Оборотень",
]


# noinspection PyMethodMayBeStatic
class AnonymRepository:
    def anonymize_caption_for_user(self, user_id: PydanticObjectId) -> str:
        hashed = crc32(str(user_id).encode())
        adjective = adjectives[hashed % len(adjectives)]
        noun = nouns[hashed % len(nouns)]
        return f"{adjective} {noun}"

    def anonymize_review(self, review: Review, user_id: PydanticObjectId | None) -> AnonymousReview:
        return AnonymousReview(
            id=review.id,
            text=review.text,
            rate=review.rate,
            anonymous_name=self.anonymize_caption_for_user(review.user_id),
            mine=review.user_id == user_id,
            likes=len(review.liked_by),
            liked_by_me=user_id in review.liked_by if user_id else None,
            at=review.at,
        )


anonym_repository: AnonymRepository = AnonymRepository()
