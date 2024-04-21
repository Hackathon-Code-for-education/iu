__all__ = ["FileRepository", "files_repository", "upload_file_from_fastapi"]

import datetime
from pathlib import Path

import magic
import pyvips
from anyio import open_file
from beanie import PydanticObjectId
from beanie.odm.operators.find.comparison import Eq
from fastapi import UploadFile

from src.config import settings
from src.exceptions import ObjectNotFound
from src.logging_ import logger
from src.modules.files.schemas import UpdateFile
from src.storages.mongo.models.file import File


# noinspection PyMethodMayBeStatic
class FileRepository:
    async def get(self, obj_id: PydanticObjectId) -> File | None:
        obj = await File.find_one(File.id == obj_id)
        return obj

    async def get_all(self) -> list[File]:
        return await File.all().to_list()

    async def get_all_for_cars(self) -> list[File]:
        return await File.find(Eq(File.must_be_uploaded, True)).to_list()

    async def update(self, obj_id: PydanticObjectId, data: UpdateFile) -> File | None:
        return await File.find(File.id == obj_id).update({"$set": data.model_dump()})

    async def delete(self, obj_id: PydanticObjectId) -> bool:
        result = await File.find(File.id == obj_id).delete()
        if not result:
            return False
        return result.deleted_count > 0

    async def upload(self, file: bytes, path: Path, friendly_name: str | None = None) -> File | None:
        obj_id = PydanticObjectId(path.stem)
        type_ = magic.Magic(mime=True).from_buffer(file)
        size = len(file)
        async with await open_file(path, "wb") as buffer:
            await buffer.write(file)
        file_updated_at = datetime.datetime.fromtimestamp(path.stat().st_mtime)
        obj = File(
            id=obj_id,  # type: ignore[call-arg]
            friendly_name=friendly_name,
            type=type_,
            size=size,
            file_updated_at=file_updated_at,
        )
        return await obj.insert()

    async def insert_all_existing_files(self) -> None:
        for path in settings.static_files.directory.rglob("*"):
            if path.is_file():
                id_ = PydanticObjectId(path.stem)
                obj = await self.get(id_)
                type_ = magic.Magic(mime=True).from_file(path)
                size = path.stat().st_size
                file_updated_at = datetime.datetime.fromtimestamp(path.stat().st_mtime)
                if obj is None:
                    logger.info(f"Inserting file {path}")
                    obj = File(
                        id=id_,  # type: ignore[call-arg]
                        type=type_,
                        size=size,
                        file_updated_at=file_updated_at,
                    )
                    await obj.insert()
                else:
                    if obj.type != type_ or obj.size != size:
                        logger.info(f"Updating file {path}")
                        await File.find(File.id == id_).update(
                            {"$set": {"type": type_, "size": size, "file_updated_at": file_updated_at}}
                        )

    async def check_existing_files(self) -> None:
        from_database = await self.get_all()
        from_database = {file.id for file in from_database}
        # check if all files from database are in static
        existing_in_filesystem = {
            PydanticObjectId(path.stem) for path in settings.static_files.directory.rglob("*") if path.is_file()
        }
        for file_id in from_database - existing_in_filesystem:
            logger.warning(f"File {file_id} is in database but not in static")


files_repository: FileRepository = FileRepository()


async def upload_file_from_fastapi(upload_file_obj: UploadFile) -> File:
    content_type = upload_file_obj.content_type
    bytes_ = await upload_file_obj.read()
    # convert to webp
    if content_type in ("image/jpeg", "image/png"):
        image = pyvips.Image.new_from_buffer(bytes_, "")
        bytes_ = image.write_to_buffer(".webp")

    obj_id = PydanticObjectId()
    path_to_upload = settings.static_files.directory / str(obj_id)
    friendly_name = upload_file_obj.filename
    file_obj = await files_repository.upload(bytes_, path_to_upload, friendly_name=friendly_name)

    if file_obj is None:
        raise ObjectNotFound(f"Возникла ошибка во время загрузки файла: `{path_to_upload}`")

    return file_obj
