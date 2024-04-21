__all__ = ["ReviewRepository", "review_repository"]

import pymongo
from beanie import PydanticObjectId

from src.modules.review.schemas import CreateReview
from src.storages.mongo.models.review import Review
from src.utils import aware_utcnow


# noinspection PyMethodMayBeStatic
class ReviewRepository:
    async def create(self, data: CreateReview) -> Review:
        return await Review(
            organization_id=data.organization_id,
            user_id=data.user_id,
            text=data.text,
            rate=data.rate,
            at=aware_utcnow(),
        ).insert()

    async def read(self, id: PydanticObjectId) -> Review | None:
        return await Review.get(id)

    async def read_for_organization(self, organization_id: PydanticObjectId) -> list[Review]:
        return await Review.find({"organization_id": organization_id}, sort=[("at", pymongo.DESCENDING)]).to_list()

    async def read_for_me(self, user_id: PydanticObjectId) -> list[Review]:
        return await Review.find({"user_id": user_id}, sort=[("at", pymongo.DESCENDING)]).to_list()

    # async def update(self, id: PydanticObjectId, data: UpdateReview) -> Review | None:
    #     return await crud.update(id, data)

    # async def delete(self, id: PydanticObjectId) -> bool:
    #     return await crud.delete(id)

    async def like_review(self, review_id: PydanticObjectId, user_id: PydanticObjectId, like: bool) -> None | bool:
        review = await Review.get(review_id)
        if review is None:
            return None

        if like:
            await review.update({"$addToSet": {"liked_by": user_id}})
            return True
        else:
            await review.update({"$pull": {"liked_by": user_id}})
            return False


review_repository: ReviewRepository = ReviewRepository()
