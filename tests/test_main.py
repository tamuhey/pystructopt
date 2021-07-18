from typing import List
import sys
from pystructopt import _parse
from dataclasses import dataclass, field
import dataclasses


@dataclass
class Opt0:
    a: int
    b: str
    c: str = "foo"
    d: bool = False
    ee: List[str] = field(metadata={"short": True}, default_factory=list)
    ff: List[int] = field(metadata={"short": True}, default_factory=list)
    g_g: int = 0


def test_parse0():
    assert dataclasses.is_dataclass(Opt0)
    # fmt: off
    args = [ "--a", "100", "--b", "2", "--d", "-e", "1", "-f", "1", "--ee", "3", "--ff", "10", "--g-g", "1"]
    # fmt: on
    opt = _parse(Opt0, args)
    assert opt == Opt0(100, "2", "foo", True, ["1", "3"], [1, 10], 1)


#  @dataclass
#  class Opt1:
#      a: int
#      b: str
#      c: str = "foo"
#      d: bool = False
#      ee: List[str] = field(metadata={"short": True}, default_factory=list)
#      ff: List[int] = field(metadata={"short": True}, default_factory=list)
#
#
#  def test_parse1():
#      assert dataclasses.is_dataclass(Opt0)
#      # fmt: off
#      args = [ "--a", "100", "--b", "2", "--d", "-e", "1", "-f", "1", "--ee", "3", "--ff", "10", ]
#      # fmt: on
#      opt = _parse(Opt0, args)
#      assert opt == Opt0(100, "2", "foo", True, ["1", "3"], [1, 10])


if sys.version_info >= (3, 9, 0):

    @dataclass
    class Opt1:
        aa: list[int]
        bb: list[str]

    def test_parse_py39():
        args = ["--aa", "1", "--bb", "3", "--aa", "2"]
        opt = _parse(Opt1, args)
        assert opt == Opt1([1, 2], ["3"])
