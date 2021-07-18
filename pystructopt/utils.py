import inspect
from typing import Any, Literal, Optional, Type, TypeVar, Union, cast, get_args
from typing_extensions import TypeGuard, get_origin

T = TypeVar("T")


def is_same_type(a: Any, b: Type[T]) -> TypeGuard[Type[T]]:
    if a == b:
        return True
    aorigin = get_origin(a) or a
    aargs = get_args(a)
    borigin = get_origin(b) or b
    bargs = get_args(b)
    if not inspect.isclass(a) and aorigin is None:
        # not a class and generics
        return False
    c1 = cast(bool, aorigin is borigin)
    c2 = not aargs or not bargs or aargs == bargs
    return c1 and c2


def from_str(kls: Type[T], value: str) -> Optional[T]:
    if kls is str:
        return cast(T, value)
    if kls is bool or kls is int:
        try:
            return kls(value)
        except ValueError:
            return None

    origin = get_origin(kls)
    if origin is Literal:
        return _from_str_lit(kls, value)
    if origin is Union:
        return _from_str_union(kls, value)


def _from_str_union(kls: Type[T], value: str) -> Optional[T]:
    for arg in get_args(kls):
        ret = from_str(arg, value)
        if ret is not None:
            return ret


def _from_str_lit(kls: Type[T], value: str) -> Optional[T]:
    for arg in get_args(kls):
        ty = type(arg)
        ret = from_str(ty, value)
        if ret == arg:
            return ret
