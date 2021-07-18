import dataclasses
import inspect
from pystructopt.parse import FieldMeta, parse_args
from typing import (
    Any,
    Dict,
    List,
    Type,
    TypeVar,
)
import dataclass_utils
import sys


T = TypeVar("T")


def parse(datacls: Type[T]) -> T:
    return _parse(datacls, sys.argv[1:])


def _parse(datacls: Type[T], args: List[str]) -> T:
    if not inspect.isclass(datacls):
        raise ValueError(f"Received not class object: {datacls}")
    if not dataclasses.is_dataclass(datacls):
        raise ValueError(f"Received not dataclass: {datacls}")

    options = _get_options(datacls)
    ret = parse_args(args, options)
    return dataclass_utils.into(ret, datacls)


def _get_options(datacls: Type[Any]) -> Dict[str, FieldMeta]:
    fields = dataclasses.fields(datacls)
    annots = datacls.__annotations__
    options: Dict[str, FieldMeta] = {}
    print(fields)
    print(annots)
    for v in fields:
        meta = {"name": v.name, "type": annots[v.name], **v.metadata}
        ret = dataclass_utils.into(meta, FieldMeta)
        options[v.name] = ret
    return options
