from typing import Type, Union, Any
from pathlib import Path
from typing_extensions import Literal
from pystructopt.utils import from_str
import pytest


@pytest.mark.parametrize(
    "kls,value,expected",
    [
        (int, "1", 1),
        (str, "1", "1"),
        (Literal[1], "1", 1),
        (Literal[1, 2], "1", 1),
        (Union[Literal[1], Literal["a"]], "1", 1),
        (int, "a", None),
        (Literal[1], "2", None),
        (Union[Literal[1], Literal["1"]], "1", 1),
        (Union[Literal[3], Literal["1", 2]], "2", 2),
        (Path, "a", Path("a")),
        (float, "1", 1.0),
    ],
)
def test_from_str(kls: Type[Any], value: Any, expected: Any):
    assert from_str(kls, value) == expected
