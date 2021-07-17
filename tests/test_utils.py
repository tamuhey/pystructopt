from typing import List
from pystructopt.utils import is_same_type
import pytest


@pytest.mark.parametrize("a,b,expected", [(List[int], list, True)])
def test_is_same_class(a, b, expected):
    assert is_same_type(a, b) == expected
    ...
