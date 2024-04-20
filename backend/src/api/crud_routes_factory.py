# mypy: disable-error-code="attr-defined"

__all__ = ["setup_based_on_methods"]

import inspect
from typing import Optional, Any

from fastapi import APIRouter
from fastapi.params import Depends
from pymongo.errors import DuplicateKeyError

from src.exceptions import ObjectNotFound
from src.exceptions import AlreadyExists
from src.typing_ import make_not_optional

DEFAULT_ROUTES = {
    "create": "/",
    "read_by": "/by",
    "read": "/{id}",
    "read_all": "/",
    "update": "/{id}",
    "delete": "/{id}",
}

DEFAULT_RESPONSES: dict[str, dict[int | str, dict[str, Any]]] = {
    "create": {201: {"description": "Объект успешно создан"}, **AlreadyExists.responses},
    "read_by": {200: {"description": "Возвращён объект по фильтру"}, **ObjectNotFound.responses},
    "read": {200: {"description": "Возвращён объект"}, **ObjectNotFound.responses},
    "read_all": {200: {"description": "Возвращены список всех объектов"}},
    "update": {200: {"description": "Объект успешно обновлён"}, **ObjectNotFound.responses, **AlreadyExists.responses},
    "delete": {200: {"description": "Объект успешно удалён"}, **ObjectNotFound.responses},
}


def setup_based_on_methods(
    router: APIRouter,
    crud: Any,
    routes: Optional[dict[str, str]] = None,
    responses: Optional[dict[str, dict[int | str, dict[str, Any]]]] = None,
    dependencies: Optional[dict[str, list[Depends] | Depends]] = None,
):
    routes = DEFAULT_ROUTES if routes is None else DEFAULT_ROUTES | routes
    responses = DEFAULT_RESPONSES if responses is None else DEFAULT_RESPONSES | responses
    dependencies = dependencies or {}
    # make all dependencies list
    dependencies = {k: [v] if not isinstance(v, list) else v for k, v in dependencies.items()}

    # check if crud has `create` method and not abstract
    if hasattr(crud, "create") and not inspect.isabstract(crud.create):

        async def _create(*args, **kwargs) -> Any:
            try:
                return await crud.create(*args, **kwargs)
            except DuplicateKeyError as e:
                raise AlreadyExists(str(e.details))

        _create.__signature__ = inspect.signature(crud.create)

        router.add_api_route(
            path=routes["create"],
            endpoint=_create,
            responses=responses["create"],
            dependencies=dependencies.get("create", []),
            methods=["POST"],
            status_code=201,
        )

    # check if crud has `read_by` method and not abstract
    if hasattr(crud, "read_by") and not inspect.isabstract(crud.read_by):

        async def _read_by(*args, **kwargs) -> Any:
            obj = await crud.read_by(*args, **kwargs)
            if obj is None:
                raise ObjectNotFound()
            return obj

        _read_by.__signature__ = _make_not_optional_return(inspect.signature(crud.read_by))
        router.add_api_route(
            path=routes["read_by"],
            endpoint=_read_by,
            responses=responses["read_by"],
            dependencies=dependencies.get("read_by", []),
            methods=["GET"],
        )

    # check if crud has `read` method
    if hasattr(crud, "read") and not inspect.isabstract(crud.read):

        async def _read(*args, **kwargs) -> Any:
            obj = await crud.read(*args, **kwargs)
            if obj is None:
                raise ObjectNotFound()
            return obj

        _read.__signature__ = _make_not_optional_return(inspect.signature(crud.read))
        router.add_api_route(
            path=routes["read"],
            endpoint=_read,
            responses=responses["read"],
            dependencies=dependencies.get("read", []),
            methods=["GET"],
            response_model=_read.__signature__.return_annotation,
        )

    # check if crud has `read_all` method
    if hasattr(crud, "read_all") and not inspect.isabstract(crud.read_all):
        router.add_api_route(
            path=routes["read_all"],
            endpoint=crud.read_all,
            responses=responses["read_all"],
            dependencies=dependencies.get("read_all", []),
            methods=["GET"],
        )

    # check if crud has `update` method
    if hasattr(crud, "update") and not inspect.isabstract(crud.update):

        async def _update(*args, **kwargs) -> Any:
            try:
                obj = await crud.update(*args, **kwargs)
                if obj is None:
                    raise ObjectNotFound()
                return obj
            except DuplicateKeyError as e:
                raise AlreadyExists(str(e.details))

        _update.__signature__ = _make_not_optional_return(inspect.signature(crud.update))

        router.add_api_route(
            path=routes["update"],
            endpoint=_update,
            responses=responses["update"],
            dependencies=dependencies.get("update", []),
            methods=["PATCH"],
        )

    # check if crud has `delete` method
    if hasattr(crud, "delete") and not inspect.isabstract(crud.delete):

        async def _delete(*args, **kwargs) -> Any:
            obj = await crud.delete(*args, **kwargs)
            if not obj:
                raise ObjectNotFound()
            return obj

        _delete.__signature__ = _make_not_optional_return(inspect.signature(crud.delete))

        router.add_api_route(
            path=routes["delete"],
            endpoint=_delete,
            responses=responses["delete"],
            dependencies=dependencies.get("delete", []),
            methods=["DELETE"],
        )


def _make_not_optional_return(signature: inspect.Signature) -> inspect.Signature:
    signature_to_set = None
    return_annotation = signature.return_annotation

    if return_annotation is not inspect.Signature.empty:
        return_annotation = make_not_optional(return_annotation)
        signature_to_set = signature.replace(return_annotation=return_annotation)

    return signature_to_set or signature
