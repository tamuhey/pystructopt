import inspect
from typing import Any, List, Type, TypeVar
from typing_extensions import TypeGuard, get_origin

T = TypeVar("T")


def is_same_type(a: Any, b: Type[T]) -> TypeGuard[Type[T]]:
    if a == b:
        return True
    if not inspect.isclass(a) and get_origin(a) is None:
        return False
    return True
