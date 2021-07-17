from typing import List
from pystructopt import parse, _parse
from dataclasses import dataclass, field
import dataclasses
from dataclass_utils import check_type


@dataclass
class Opt0:
    a: int
    b: str
    c: str = "foo"
    d: bool = False
    ee: List[str] = field(metadata={"short": True}, default_factory=list)
    ff: List[int] = field(metadata={"short": True}, default_factory=list)


def test_parse():
    assert dataclasses.is_dataclass(Opt0)
    args = [
        "--a",
        "100",
        "--b",
        "2",
        "--d",
        "-e",
        "1",
        "-f",
        "1",
        "--ee",
        "3",
        "--ff",
        "10",
    ]
    opt = _parse(Opt0, args)
    assert opt == Opt0(100, "2", "foo", True, ["1", "3"], [1, 10])
