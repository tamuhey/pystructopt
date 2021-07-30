from dataclasses import dataclass
from typing_extensions import get_args, get_origin
import dataclass_utils
from typing import Any, List, Mapping, Optional, Type, Union
from ._utils import from_str


@dataclass(frozen=True)
class Arg:
    """Read-only dataclass for each command line option"""

    name: str
    # value type of this option
    type: Type[Any]

    # long option name or flag
    long: Union[bool, str] = True
    # short option name or flag
    short: Union[bool, str] = False
    # wheter to enable positional argument
    positional: bool = False
    # parse based on occurrences (e.g. -vvv -> 3)
    from_occurrences: bool = False
    # help string
    help: Optional[str] = None

    @classmethod
    def from_dict(cls, meta: Mapping[str, Any]) -> "Arg":
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
        err = None
        if not (self.positional or self.optional):
            err = "Specify either positional or optional argument"

        if self.from_occurrences:
            if self.positional:
                err = "Cannot use `from_occurrences` with positional argument"
            if self.type is not int:
                err = "The type of a field with `from_occurrences` must be `int`"
        if err:
            raise ValueError(f"Error in {self.name}: {err}")

    def value_from_strs(self, value: List[str]) -> Any:
        """Create value from list of arguments."""
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
            # just take one value
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
            # Any type can be constructed from str, e.g. `Path`
            v = self._expect_one(value)
            ret = from_str(self.type, v)
            if ret is None:
                raise ValueError(f"Error in converting `{v}` to {self.type}")
            return ret

    def _expect_one(self, value: List[str]) -> str:
        if len(value) != 1:
            raise ValueError(f"Field {self.name} takes exactly one value, got {value}")
        return value[0]
