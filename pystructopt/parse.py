import getopt
from collections import defaultdict
from dataclasses import dataclass
from typing import (
    Any,
    DefaultDict,
    Dict,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    Union,
)

import dataclass_utils

from .utils import is_same_type

FieldType = Union[str, int, bool, List[str], List[int]]


@dataclass
class FieldMeta:
    name: str
    type: Type[FieldType]
    long_name: Optional[str] = None
    short_name: Optional[str] = None
    positional: bool = True
    short: bool = False
    long: bool = True
    from_occurrences: bool = False

    @classmethod
    def from_dict(cls, meta: Mapping[str, Any]) -> "FieldMeta":
        return dataclass_utils.into(meta, cls)

    def get_long_name(self) -> str:
        return self.long_name or self.name

    def get_short_name(self) -> str:
        if self.short_name:
            ret = self.short_name
        if self.long_name:
            ret = self.long_name[0]
        ret = self.name[0]
        return ret

    def value_required(self) -> bool:
        if not self.is_optional:
            raise ValueError(f"Unreachable")

        if self.from_occurrences:
            return False
        if self.type is bool:
            return False
        return True

    @property
    def is_optional(self) -> bool:
        return self.short or self.long

    def validate(self):
        if not self.positional and (not self.is_optional):
            raise ValueError("Specify either positional or optional argument")

        if self.from_occurrences:
            if self.positional:
                raise ValueError(
                    "Cannot use `from_occurrences` for positional argument"
                )
            if self.type is not int:
                raise ValueError(
                    "The type of a field with `from_occurrences` must be `int`"
                )

    def value_from_list(self, value: List[str]) -> FieldType:
        if self.type is bool:
            if value != [""]:
                raise ValueError(
                    f"No field must be specified for `{self.name}`, got {value}"
                )
            return True
        elif self.type is int:
            if self.from_occurrences:
                if any(v != "" for v in value):
                    raise ValueError(f"Field {self.name} takes no value, got {value}.")
                return len(value)  # type: ignore
            else:
                return int(self._expect_one(value))
        elif self.type is str:
            return self._expect_one(value)

        elif is_same_type(self.type, List[str]):
            return value
        elif is_same_type(self.type, List[int]):
            return [int(x) for x in value]
        else:
            raise ValueError(f"Unsupported type: {self.type}")

    def _expect_one(self, value: List[str]) -> str:
        if len(value) != 1:
            raise ValueError(f"Field {self.name} takes exactly one value, got {value}")
        return value[0]


def parse_args(args: List[str], options: Dict[str, FieldMeta]) -> Dict[str, FieldType]:
    shortopts, index = _get_shortopt(options)
    longopts, index2 = _get_longopt(options)
    # merge index
    index.update(index2)

    opts_, pos_ = getopt.gnu_getopt(args, shortopts, longopts)

    # convert to dict
    opts: DefaultDict[str, List[str]] = defaultdict(list)
    for k, v in opts_:
        name = index[k]
        opts[name].append(v)
    pos = _consume_pos(pos_, options)

    # merge
    for k, v in pos.items():
        name = index[k]
        opts[name].extend(v)
    ret = {}
    for k, v in opts.items():
        ret[k] = options[k].value_from_list(v)
    return ret


def _consume_pos(pos: List[str], options: Dict[str, FieldMeta]) -> Dict[str, List[str]]:
    ret = defaultdict(list)
    last = None
    for k, meta in options.items():
        if not meta.positional:
            continue
        last = k
        if pos:
            ret[k].append(pos[0])
            pos = pos[1:]
        else:
            break
    if pos:
        if not last:
            raise ValueError(f"Unknown positional arguments: {pos}")
        ret[last].extend(pos)
    return ret


def _get_shortopt(options: Dict[str, FieldMeta]) -> Tuple[str, Dict[str, str]]:
    index = {}
    ret = ""
    for k, meta in options.items():
        if meta.short:
            name = meta.get_short_name()
            ret += name
            if meta.value_required():
                ret += ":"
            index["-" + name] = k
    return ret, index


def _get_longopt(options: Dict[str, FieldMeta]) -> Tuple[List[str], Dict[str, str]]:
    index = {}
    ret = []
    for k, meta in options.items():
        if meta.long:
            name = meta.get_long_name()
            item = name
            if meta.value_required():
                item += "="
            ret.append(item)
            index["--" + name] = k
    return ret, index
