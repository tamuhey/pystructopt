import sys
from typing import List, Literal, Union
from pystructopt.utils import from_str, is_same_type
import pytest


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (List[int], list, True),
        (set, list, False),
        (int, str, False),
        (List[str], List[int], False),
    ],
)
def test_is_same_class(a, b, expected):
    assert is_same_type(a, b) == expected


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
    ],
)
def test_from_str(kls, value, expected):
    assert from_str(kls, value) == expected


if sys.version_info >= (3, 9, 0):

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (List[int], list[int], True),
            (List, list, True),
            (List, list[int], True),
            (set, list[int], False),
        ],
    )
    def test_is_same_class39(a, b, expected):
        assert is_same_type(a, b) == expected
