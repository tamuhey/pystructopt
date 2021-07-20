import dataclasses
import inspect
import sys
from typing import List, Type, TypeVar

import dataclass_utils  # type: ignore

from ._dataclass_parser import get_options
from ._parse import parse_args

__all__ = ["parse"]

T = TypeVar("T")


def parse(datacls: Type[T]) -> T:
    return _parse(datacls, sys.argv[1:])


def _parse(datacls: Type[T], args: List[str]) -> T:
    if not inspect.isclass(datacls):
        raise ValueError(f"Received not class object: {datacls}")
    if not dataclasses.is_dataclass(datacls):
        raise ValueError(f"Received not dataclass: {datacls}")

    options = get_options(datacls)
    ret = parse_args(args, options)
    return dataclass_utils.into(ret, datacls)
