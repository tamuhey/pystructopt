import dataclasses
from dataclasses import dataclass
import inspect
from pystructopt.parse import FieldMeta, parse_args
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)
import dataclass_utils
import argparse
import sys


T = TypeVar("T")


def parse(datacls: Type[T]) -> T:
    return _parse(datacls, sys.argv[1:])


def _parse(datacls: Type[T], args: List[str]) -> T:
    if not inspect.isclass(datacls):
        raise ValueError(f"Received not class object: {datacls}")
    if not dataclasses.is_dataclass(datacls):
        raise ValueError(f"Received not dataclass: {datacls}")

    fields = dataclasses.fields(datacls)
    annots = datacls.__annotations__
    options = {}
    for v in fields:
        meta = {"name": v.name, "type": annots[v.name], **v.metadata}
        ret = dataclass_utils.into(meta, FieldMeta)
        options[v.name] = ret
    ret = parse_args(args, options)
    return dataclass_utils.into(ret, datacls)
