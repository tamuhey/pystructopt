from typing import Optional, Type, TypeVar, Union, cast

from typing_extensions import Literal, get_args, get_origin

T = TypeVar("T")


def from_str(kls: Type[T], value: str) -> Optional[T]:
    if kls is str:
        return cast(T, value)
    if kls is bool or kls is int:
        try:
            return kls(value)  # type: ignore
        except ValueError:
            return None

    origin = get_origin(kls)
    if origin is Literal:
        return _from_str_lit(kls, value)
    if origin is Union:
        return _from_str_union(kls, value)
    return None


def _from_str_union(kls: Type[T], value: str) -> Optional[T]:
    for arg in get_args(kls):
        ret = from_str(arg, value)
        if ret is not None:
            return ret
    return None


def _from_str_lit(kls: Type[T], value: str) -> Optional[T]:
    for arg in get_args(kls):
        ty = type(arg)
        ret = from_str(ty, value)
        if ret == arg:
            return ret
    return None
