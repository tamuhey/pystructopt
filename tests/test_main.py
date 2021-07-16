from pystructopt import parse, _parse
from dataclasses import dataclass
import dataclasses
from dataclass_utils import check_type


@dataclass
class Opt:
    a: int
    b: str
    c: str = "foo"
    d: bool = False


def test_parse():
    assert dataclasses.is_dataclass(Opt)
    args = ["--a", "100", "--b", "2", "--d", "True"]
    opt = _parse(Opt, args)
    assert opt == Opt(100, "2", "foo", True)
