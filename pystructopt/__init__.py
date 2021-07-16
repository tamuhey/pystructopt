import dataclasses
import inspect
from typing import Any, Dict, Iterator, List, Mapping, Optional, Sequence, Type, TypeVar
import dataclass_utils
import sys


T = TypeVar("T")


def parse(datacls: Type[T]) -> T:
    return _parse(datacls, sys.argv[1:])


@dataclasses.dataclass
class FieldMeta:
    positional: bool = True
    short: bool = False
    long: bool = False

    @classmethod
    def parse(cls, data: Mapping[str, Any]):
        ret = dataclass_utils.into(data, cls)
        ret._validate()
        return ret

    def _validate(self):
        pass


def _parse(datacls: Type[T], args: List[str]) -> T:
    if not inspect.isclass(datacls):
        raise ValueError(f"Received not class object: {datacls}")
    if not dataclasses.is_dataclass(datacls):
        raise ValueError(f"Received not dataclass: {datacls}")
    fields = {
        v.name: FieldMeta.parse(v.metadata or {}) for v in dataclasses.fields(datacls)
    }
    parsed = {}
    _parse_explicit_fields(fields, args, parsed)
    annots = datacls.__annotations__
    for k, v in parsed.items():
        ty = annots[k]
        parsed[k] = _convert(v, ty)
    ret = dataclass_utils.into(parsed, datacls)
    return ret


def _convert(v: str, ty: Type[Any]):
    if ty is bool:
        # TODO: more validation
        return v.lower() == "true"
    elif ty is int:
        return int(v)
    return v


def _parse_explicit_fields(
    fields: Dict[str, FieldMeta], args: List[str], parsed: Dict[str, Any]
) -> List[str]:
    ret = []
    it = iter(args)
    for arg in it:
        if arg.startswith("--"):
            name = _to_field_name(arg[2:])
            _insert_field_value(it, name, parsed)
        elif arg.startswith("-"):
            if not len(arg):
                raise ValueError(f"Please split value and field name: {arg}")
            name = _to_field_name(arg[1:])
            _insert_field_value(it, name, parsed)
        else:
            raise ValueError("Positional argument is not supported")
    return ret


def _insert_field_value(it: Iterator[str], name: str, parsed: Dict[str, Any]):
    try:
        value = next(it)
    except StopIteration:
        raise ValueError(f"No value field is not supported: {name}")
    if name in parsed:
        raise ValueError(f"Multiple optional field is not supported: {name}")
    parsed[name] = value


def _to_field_name(name: str) -> str:
    if name.startswith("-"):
        raise ValueError(f"Invalid field name: {name}")
    # TODO: more validation
    return name.replace("-", "_")
