import inspect
from typing import Any, Type, TypeVar, Union, cast

from typing_extensions import Literal, get_args, get_origin

T = TypeVar("T")


class ParseError(ValueError):
    def __init__(self, kls: Type[Any], value: str):
        self.kls = kls
        self.value = value

    def __str__(self) -> str:
        return f"Cannot convert `{self.value}` to {self.kls}"


def from_str(kls: Type[T], value: str) -> T:
    if kls is str:
        return cast(T, value)
    if inspect.isclass(kls):
        try:
            return kls(value)  # type: ignore
        except ValueError:
            raise ParseError(kls, value)

    origin = get_origin(kls)
    if origin is Literal:
        return _from_str_lit(kls, value)
    if origin is Union:
        return _from_str_union(kls, value)
    raise ParseError(kls, value)


def _from_str_union(kls: Type[T], value: str) -> T:
    for arg in get_args(kls):
        try:
            return from_str(arg, value)
        except ParseError:
            continue
    raise ParseError(kls, value)


def _from_str_lit(kls: Type[T], value: str) -> T:
    for arg in get_args(kls):
        ty = type(arg)
        try:
            ret = from_str(ty, value)
            if ret == arg:
                return ret
        except ParseError:
            continue
    raise ParseError(kls, value)
