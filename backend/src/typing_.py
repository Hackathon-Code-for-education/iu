import typing
from types import NoneType, UnionType


def is_optional(annotation):
    is_union = typing.get_origin(annotation) is typing.Union or typing.get_origin(annotation) is UnionType

    return is_union and NoneType in typing.get_args(annotation)


def make_not_optional(annotation):
    is_union = typing.get_origin(annotation) is typing.Union or typing.get_origin(annotation) is UnionType

    if is_union:
        union_args = typing.get_args(annotation)
        if NoneType in union_args:
            union_args = tuple(arg for arg in union_args if arg is not NoneType)

            if len(union_args) == 1:
                annotation = union_args[0]
            else:
                annotation = typing.Union[union_args]
    return annotation
