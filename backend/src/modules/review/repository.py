__all__ = ["ReviewRepository", "review_repository"]

from beanie import PydanticObjectId, SortDirection

from src.modules.review.schemas import CreateReview, ReviewWithOrganizationInfo
from src.storages.mongo import Organization
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
        return await Review.find(
            {"organization_id": organization_id}, sort=[("at", SortDirection.DESCENDING)]
        ).to_list()

    async def read_for_me(self, user_id: PydanticObjectId) -> list[ReviewWithOrganizationInfo]:
        reviews = await Review.find({"user_id": user_id}, sort=[("at", SortDirection.DESCENDING)]).to_list()
        ids = set(review.organization_id for review in reviews)
        organizations = await Organization.find_many({"_id": {"$in": list(ids)}}).to_list()
        org_dict = {org.id: org for org in organizations}

        return [
            ReviewWithOrganizationInfo(
                **review.model_dump(),
                organization_name=org_dict[review.organization_id].name,
                organization_username=org_dict[review.organization_id].username,
            )
            for review in reviews
        ]

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
