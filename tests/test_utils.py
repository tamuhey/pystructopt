import sys
from typing import List
from pystructopt.utils import is_same_type
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
