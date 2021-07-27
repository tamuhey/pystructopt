import dataclasses
import argparse
import inspect
import sys
from typing import Any, Dict, List, Literal, Optional, Type, TypeVar, Union
from dataclasses import dataclass
from typing_extensions import TypeAlias

import dataclass_utils  # type: ignore

__all__ = ["parse"]

T = TypeVar("T")


def parse(datacls: Type[T]) -> T:
    """Entry point - create dataclass instance from command line argument"""
    return parse_args(datacls, sys.argv[1:])


def parse_args(datacls: Type[T], args: List[str]) -> T:
    if not inspect.isclass(datacls):
        raise ValueError(f"Received not class object: {datacls}")
    if not dataclasses.is_dataclass(datacls):
        raise ValueError(f"Received not dataclass: {datacls}")
    return _parse_core(datacls, args)


Action: TypeAlias = Literal[
    "store",
    "store_const",
    "store_true",
    "store_false",
    "append",
    "append_const",
    "count",
    "help",
    "version",
    "extend",
]


@dataclass
class FieldMeta:
    dest: str
    long: Union[bool, str] = True
    short: Union[bool, str] = False
    positional: Union[bool, str] = False
    action: Action = "store"
    nargs: Union[int, Literal["?", "*", "+"]] = 0
    const: Optional[Any] = None
    type: Type[Any] = str
    default: Optional[Any] = None
    choices: Optional[List[str]] = None
    required: bool = False
    help: Optional[str] = None


def _parse_core(datacls: Type[T], args: List[str]) -> T:
    parser = argparse.ArgumentParser()  # TODO: description
    for field in dataclasses.fields(datacls):
        d = {"dest": field.name, **field.metadata}
        meta = dataclass_utils.into(d, FieldMeta)
        name_or_flags = _get_name_or_flags(meta)
        kwargs = dataclasses.asdict(meta)
        del kwargs["short"]
        del kwargs["long"]
        parser.add_argument(*name_or_flags, **kwargs)
    ns = parser.parse_args(args)
    data: Dict[str, Any] = {}
    for field in dataclasses.fields(datacls):
        data[field.name] = getattr(ns, field.name)
    return dataclass_utils.into(data, datacls)


def _get_name_or_flags(field: FieldMeta) -> List[str]:
    ret: List[str] = []

    # short
    if isinstance(field.short, str):
        if len(field.short) != 1:
            raise ValueError(
                f"Length of the short option name must be 1. ({field.short} in {field.dest})"
            )
        ret.append("-" + field.short)
    if field.short == True:
        ret.append("-" + field.dest[0])

    # long
    if isinstance(field.long, str):
        if not field.long:
            raise ValueError(f"Long option name must not be empty. ({field.dest})")
        ret.append("--" + field.long)
    if field.long == True:
        ret.append("--" + field.dest)

    # positional
    if isinstance(field.positional, str):
        if not field.long:
            raise ValueError(f"Positional name must not be empty. ({field.dest})")
        ret.append(field.positional)
    if field.positional == True:
        ret.append(field.dest)

    if not ret:
        raise ValueError("One of Positional or Optional fields must be specified.")
    return ret
