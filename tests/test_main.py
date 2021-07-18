import dataclasses
import sys
from dataclasses import dataclass, field
from typing import List, Union

from typing_extensions import Literal

from pystructopt import _parse, _get_options


@dataclass
class Opt0:
    a: int
    b: str
    c: str = "foo"
    d: bool = False
    ee: List[str] = field(metadata={"short": True}, default_factory=list)
    ff: List[int] = field(metadata={"short": True}, default_factory=list)
    g_g: int = 0
    verbose: int = field(default=0, metadata={"from_occurrences": True, "short": True})


def test_parse0():
    assert dataclasses.is_dataclass(Opt0)
    # fmt: off
    args = [ "--a", "100", "--b", "2", "--d", "-e", "1", "-f", "1", "--ee", "3", "--ff", "10", "--g-g", "1", "-vv"]
    # fmt: on
    opt = _parse(Opt0, args)
    assert opt == Opt0(100, "2", "foo", True, ["1", "3"], [1, 10], 1, verbose=2)


@dataclass
class Opt1:
    a: int
    b: Literal[1, 2]
    c: Union[Literal[1, 2], Literal[3]]
    dd: List[Literal[1, 2, "a"]]


def test_parse1():
    # fmt: off
    args = ["1", "2", "3", "--dd", "1", "--dd", "2", "--dd", "a"]
    # fmt: on
    opt = _parse(Opt1, args)
    assert opt == Opt1(1, 2, 3, [1, 2, "a"])


if sys.version_info >= (3, 9, 0):

    @dataclass
    class Opt100:
        aa: list[int]
        bb: list[str]

    def test_parse_py39():
        args = ["--aa", "1", "--bb", "3", "--aa", "2"]
        opt = _parse(Opt100, args)
        assert opt == Opt100([1, 2], ["3"])
