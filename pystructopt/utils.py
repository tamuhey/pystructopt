import inspect
from typing import Any, List, Type, TypeVar, get_args
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
    c1 = aorigin is borigin
    c2 = not aargs or not bargs or aargs == bargs
    return c1 and c2
