__all__ = ["router"]

from beanie import PydanticObjectId
from fastapi import Depends, APIRouter, UploadFile

from scripts.parse_organizations import Certificates, CertificateOut
from src.api.crud_routes_factory import setup_based_on_methods

from src.api.dependencies import get_moderator, UserDep, OptionalUserIdDep
from src.exceptions import ObjectNotFound, NotEnoughPermissionsException, UnauthorizedException
from src.modules.anonymize.repository import anonym_repository
from src.modules.organization.repository import organization_repository
from src.modules.organization.schemas import CreateOrganization, UpdateOrganization, PostReview
from src.modules.review.repository import review_repository
from src.modules.review.schemas import CreateReview, AnonymousReview
from src.storages.mongo import Organization
from src.storages.mongo.models.organization import ContactsSchema, EducationalProgramSchema
from src.storages.mongo.models.review import Review
from src.storages.mongo.schemas import UserRole

router = APIRouter(prefix="/organizations", tags=["Organizations"])

_moder_dep = Depends(get_moderator)

setup_based_on_methods(
    router,
    crud=organization_repository,
    dependencies={
        "create": _moder_dep,
        "update": _moder_dep,
        "delete": _moder_dep,
    },
)


@router.get(
    "/by-username/{username}", responses={200: {"description": "Organization info"}, **ObjectNotFound.responses}
)
async def get_by_username(username: str) -> Organization:
    organization = await organization_repository.read_by_username(username)
    if organization is None:
        raise ObjectNotFound(f"Организация с username={username} не найдена")
    return organization


@router.post(
    "/{organization_id}/reviews/",
    responses={
        200: {"description": "Success"},
        **NotEnoughPermissionsException.responses,
        **ObjectNotFound.responses,
        **UnauthorizedException.responses,
    },
)
async def post_review(data: PostReview, user: UserDep, organization_id: PydanticObjectId) -> Review:
    """
    Оставить отзыв организации
    """
    organization = await organization_repository.read(organization_id)
    if organization is None:
        raise ObjectNotFound(f"Организация с id={organization_id} не найдена")
    # check approvement
    if not user.is_approved(organization_id):
        raise NotEnoughPermissionsException(
            "У вас недостаточно прав для оставления отзыва на эту организацию (не студент)"
        )

    return await review_repository.create(
        CreateReview(organization_id=data.organization_id, user_id=user.id, text=data.text, rate=data.rate)
    )


@router.get(
    "/{organization_id}/reviews/",
    responses={200: {"description": "Success"}, **ObjectNotFound.responses},
)
async def get_reviews(organization_id: PydanticObjectId, user_id: OptionalUserIdDep) -> list[AnonymousReview]:
    """
    Получить отзывы об организации
    """
    organization = await organization_repository.read(organization_id)
    if organization is None:
        raise ObjectNotFound(f"Организация с id={organization_id} не найдена")
    reviews = await review_repository.read_for_organization(organization_id)
    return [anonym_repository.anonymize_review(review, user_id) for review in reviews]


@router.post(
    "/import",
    responses={
        201: {"description": "Организации успешно созданы, если не существовали"},
        **NotEnoughPermissionsException.responses,
    },
    status_code=201,
)
async def import_organizations(upload_file_obj: UploadFile, user: UserDep) -> list[PydanticObjectId]:
    """
    Импортировать организации из JSON дампа (результат скрипта `parse_organizations.py`)
    """
    if user.role != UserRole.ADMIN:
        raise NotEnoughPermissionsException("У вас недостаточно прав для загрузки организаций")

    bytes_ = await upload_file_obj.read()
    organizations = Certificates.model_validate_json(bytes_)
    id_registry_mapping = await organization_repository.get_id_registry_mapping()

    not_existing_ids = set(org.in_registry_id for org in organizations.certificates) - set(id_registry_mapping.values())
    not_existing_organizations = (org for org in organizations.certificates if org.in_registry_id in not_existing_ids)

    create_ = (
        CreateOrganization(
            in_registry_id=org.in_registry_id,
            username=org.in_registry_id,
            name=org.actual_education_organization.short_name or org.actual_education_organization.full_name,
            full_name=org.actual_education_organization.full_name,
            contacts=ContactsSchema(
                email=org.actual_education_organization.email,
                phone=org.actual_education_organization.phone,
                website=org.actual_education_organization.website,
                fax=org.actual_education_organization.fax,
                post_address=org.actual_education_organization.post_address,
                inn=org.actual_education_organization.inn,
                kpp=org.actual_education_organization.kpp,
                ogrn=org.actual_education_organization.ogrn,
            ),
            region_name=org.region_name,
            federal_district_name=org.federal_district_name,
            educational_programs=[
                EducationalProgramSchema(
                    in_registry_id=_.in_registry_id,
                    edu_level_name=_.edu_level_name,
                    program_name=_.program_name,
                    program_code=_.program_code,
                    ugs_name=_.ugs_name,
                    ugs_code=_.ugs_code,
                    edu_normative_period=_.edu_normative_period,
                    qualification=_.qualification,
                )
                for _ in org.educational_programs
            ],
        )
        for org in not_existing_organizations
        if org.actual_education_organization
    )

    return await organization_repository.create_many(list(create_))


@router.post(
    "/import/{organization_id}",
    responses={
        201: {"description": "Организации успешно созданы, если не существовали"},
        **NotEnoughPermissionsException.responses,
    },
    status_code=201,
)
async def import_specific_organization(
    org: CertificateOut, user: UserDep, organization_id: PydanticObjectId
) -> Organization | None:
    """
    Импортировать организации из JSON дампа (результат скрипта `parse_organizations.py`)
    """
    if user.role != UserRole.ADMIN:
        raise NotEnoughPermissionsException("У вас недостаточно прав для загрузки организаций")

    update_ = UpdateOrganization(
        in_registry_id=org.in_registry_id,
        username=org.in_registry_id,
        name=org.actual_education_organization.short_name or org.actual_education_organization.full_name,
        full_name=org.actual_education_organization.full_name,
        contacts=ContactsSchema(
            email=org.actual_education_organization.email,
            phone=org.actual_education_organization.phone,
            website=org.actual_education_organization.website,
            fax=org.actual_education_organization.fax,
            post_address=org.actual_education_organization.post_address,
            inn=org.actual_education_organization.inn,
            kpp=org.actual_education_organization.kpp,
            ogrn=org.actual_education_organization.ogrn,
        ),
        region_name=org.region_name,
        federal_district_name=org.federal_district_name,
        educational_programs=[
            EducationalProgramSchema(
                in_registry_id=_.in_registry_id,
                edu_level_name=_.edu_level_name,
                program_name=_.program_name,
                program_code=_.program_code,
                ugs_name=_.ugs_name,
                ugs_code=_.ugs_code,
                edu_normative_period=_.edu_normative_period,
                qualification=_.qualification,
            )
            for _ in org.educational_programs
        ],
    )

    return await organization_repository.update(organization_id, update_)
