from beanie import PydanticObjectId
from fastapi import APIRouter

from src.api.dependencies import UserIdDep
from src.exceptions import UnauthorizedException, ObjectNotFound
from src.modules.review.repository import review_repository

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post(
    "/{review_id}/like",
    responses={200: {"description": "Success"}, **ObjectNotFound.responses, **UnauthorizedException.responses},
)
async def like_review(review_id: PydanticObjectId, user_id: UserIdDep) -> bool:
    """
    Поставить лайк/дизлайк отзыву, возвращает True если лайк поставлен, False если убран или 404 если отзыв не найден
    """
    review = await review_repository.read(review_id)

    if review is None:
        raise ObjectNotFound("Отзыв не найден")

    already_liked = user_id in review.liked_by

    if already_liked:
        await review_repository.like_review(review_id, user_id, False)
        return False
    else:
        await review_repository.like_review(review_id, user_id, True)
        return True
