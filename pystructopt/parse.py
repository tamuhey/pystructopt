import getopt
import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, DefaultDict, Dict, List, Mapping, Tuple, Type, Union

import dataclass_utils  # type: ignore
from typing_extensions import get_args, get_origin

from .utils import from_str

logger = logging.getLogger(__name__)


@dataclass
class FieldMeta:
    name: str
    type: Type[Any]
    long: Union[bool, str] = True
    short: Union[bool, str] = False
    positional: bool = False
    from_occurrences: bool = False

    @classmethod
    def from_dict(cls, meta: Mapping[str, Any]) -> "FieldMeta":
        return dataclass_utils.into(meta, cls)

    @property
    def long_name(self) -> str:
        if isinstance(self.long, str):
            ret = self.long
        else:
            ret = self.name
        return ret.replace("_", "-")

    @property
    def short_name(self) -> str:
        if isinstance(self.short, str):
            ret = self.short
        else:
            ret = self.long_name[0]
        return ret

    def value_required(self) -> bool:
        if not self.optional:
            raise ValueError(f"Unreachable")

        if self.from_occurrences:
            return False
        if self.type is bool:
            return False
        return True

    @property
    def optional(self) -> bool:
        return bool(self.short or self.long)

    def validate(self):
        if not (self.positional or self.optional):
            raise ValueError("Specify either positional or optional argument")

        if self.from_occurrences:
            if self.positional:
                raise ValueError(
                    "Cannot use `from_occurrences` with positional argument"
                )
            if self.type is not int:
                raise ValueError(
                    "The type of a field with `from_occurrences` must be `int`"
                )

    def value_from_strs(self, value: List[str]) -> Any:
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
        elif get_origin(self.type) is list:
            rets: List[Any] = []
            types = get_args(self.type)
            if len(types) == 1:
                ty = types[0]
            elif len(types) >= 2:
                raise ValueError(f"Unreachable: {self.type}")
            else:
                ty = Any
            for v in value:
                w = from_str(ty, v)
                if w is None:
                    raise ValueError(f"Error in converting `{v}` to {self.type}")
                rets.append(w)
            return rets
        else:
            v = self._expect_one(value)
            ret = from_str(self.type, v)
            if ret is None:
                raise ValueError(f"Error in converting `{v}` to {self.type}")
            return ret

    def _expect_one(self, value: List[str]) -> str:
        if len(value) != 1:
            raise ValueError(f"Field {self.name} takes exactly one value, got {value}")
        return value[0]


def parse_args(args: List[str], options: Dict[str, FieldMeta]) -> Dict[str, Any]:
    for name, fieldmeta in options.items():
        try:
            fieldmeta.validate()
        except ValueError as e:
            raise ValueError(f"Error in `{name}`.") from e
    logger.info(f"options: {options}")
    shortopts, index = _get_shortopt(options)
    longopts, index2 = _get_longopt(options)
    # merge index
    index.update(index2)
    logger.info(f"index: {index}")

    logger.info(f"short: {shortopts}")
    logger.info(f"long : {longopts}")
    opts_, pos_ = getopt.gnu_getopt(args, shortopts, longopts)

    # convert to dict
    opts: DefaultDict[str, List[str]] = defaultdict(list)
    for k, v in opts_:
        name = index[k]
        opts[name].append(v)
    pos = _consume_pos(pos_, options)
    logger.info(f"opts: {opts}")
    logger.info(f"pos: {pos}")

    # merge
    for k, v2 in pos.items():
        opts[k].extend(v2)
    ret: Dict[str, Any] = {}
    for k, v3 in opts.items():
        ret[k] = options[k].value_from_strs(v3)
    return ret


def _consume_pos(pos: List[str], options: Dict[str, FieldMeta]) -> Dict[str, List[str]]:
    ret: DefaultDict[str, List[str]] = defaultdict(list)
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
    """Index contains `shortopt: original name`"""
    index: Dict[str, str] = {}
    ret = ""
    for k, meta in options.items():
        if meta.short:
            name = meta.short_name
            ret += name
            if meta.value_required():
                ret += ":"
            index["-" + name] = k
    return ret, index


def _get_longopt(options: Dict[str, FieldMeta]) -> Tuple[List[str], Dict[str, str]]:
    index: Dict[str, str] = {}
    ret: List[str] = []
    for k, meta in options.items():
        if meta.long:
            name = meta.long_name
            item = name
            if meta.value_required():
                item += "="
            ret.append(item)
            index["--" + name] = k
    return ret, index
