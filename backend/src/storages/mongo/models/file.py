import datetime

from src.custom_pydantic import CustomModel
from src.storages.mongo.models.__base__ import CustomDocument


class FileSchema(CustomModel):
    friendly_name: str | None = None
    "Название файла (для отображения пользователю)"
    must_be_uploaded: bool = False
    "Должен ли файл быть загружен на гольф-кар (по умолчанию - нет)"
    type: str | None = None
    "Тип файла (например, image/png)"
    size: int | None = None
    "Размер файла в байтах"
    file_updated_at: datetime.datetime | None = None
    "Дата последнего обновления файла"


class File(FileSchema, CustomDocument):
    pass
