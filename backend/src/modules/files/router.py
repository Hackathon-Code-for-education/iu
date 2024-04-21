"""
Модуль для работы с файлами и /static.
"""

__all__ = ["router"]

import os

from beanie import PydanticObjectId
from fastapi import UploadFile, BackgroundTasks

from src.api.custom_router_class import EnsureAuthenticatedAPIRouter
from src.exceptions import ObjectNotFound
from src.config import settings
from src.modules.files.repository import files_repository, upload_file_from_fastapi
from src.modules.files.schemas import UpdateFile
from src.storages.mongo import File

router = EnsureAuthenticatedAPIRouter(prefix="/files", tags=["Files"])


@router.post("/upload", responses={201: {"description": "Файл успешно загружен"}}, status_code=201)
async def upload_file(upload_file_obj: UploadFile) -> File:
    """
    Загрузить файл в static.
    """
    return await upload_file_from_fastapi(upload_file_obj)


@router.get(
    "/",
    responses={200: {"description": "Список файлов"}},
    status_code=200,
)
async def get_all_files() -> list[File]:
    """
    Получить список всех файлов.
    """

    files = await files_repository.get_all()
    return files


@router.get(
    "/{obj_id}",
    responses={200: {"description": "Файл"}, **ObjectNotFound.responses},
    status_code=200,
)
async def get_file(obj_id: PydanticObjectId) -> File:
    """
    Получить файл по его id.
    """

    file = await files_repository.get(obj_id)
    if file is None:
        raise ObjectNotFound("File not found")

    return file


@router.delete(
    "/{obj_id}",
    responses={200: {"description": "Файл удалён"}, **ObjectNotFound.responses},
    status_code=200,
)
async def delete_file(background_tasks: BackgroundTasks, obj_id: PydanticObjectId) -> bool:
    file = await files_repository.get(obj_id)

    if file is None:
        raise ObjectNotFound("File not found")
    path = settings.static_files.directory / str(file.id)
    background_tasks.add_task(os.remove, path)
    return await files_repository.delete(file.id)


@router.patch(
    "/{obj_id}",
    responses={200: {"description": "Файл обновлён успешно"}, **ObjectNotFound.responses},
    status_code=200,
)
async def update_file(
    data: UpdateFile,
    obj_id: PydanticObjectId,
) -> File:
    """
    Обновить файл. В том числе, переместить его в другую директорию или переименовать.
    """

    updated = await files_repository.update(obj_id, data)
    if updated is None:
        raise ObjectNotFound("Файл не найден")

    return updated
