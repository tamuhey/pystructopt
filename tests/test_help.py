from pystructopt._help import _get_flag_str, _get_opt_str, _get_arg_str
from pystructopt._arg import Arg
import pytest


@pytest.mark.parametrize(
    "arg, width, indent,expected",
    [
        (
            Arg("foo", bool, True, True, help="aaaaaaaaaaaaaaaaaaaaa"),
            10,
            8,
            """
-f, --foo
        aaaaaaaaaa
        aaaaaaaaaa
        a""",
        ),
        (
            Arg("foo", bool, True, False, help="aaaaaaaaaaaaaaaaaaaaa"),
            10,
            8,
            """
    --foo
        aaaaaaaaaa
        aaaaaaaaaa
        a""",
        ),
    ],
)
def test_get_flag_str(arg: Arg, expected: str, width: int, indent: int):
    ret = _get_flag_str(arg, width, indent).strip("\n")
    assert ret == expected.strip("\n")


@pytest.mark.parametrize(
    "arg, width, indent,expected",
    [
        (
            Arg("foo", int, True, True, help="aaaaaaaaaaaaaaaaaaaaa"),
            10,
            8,
            """
-f, --foo <foo>
        aaaaaaaaaa
        aaaaaaaaaa
        a""",
        ),
    ],
)
def test_get_opt_str(arg: Arg, expected: str, width: int, indent: int):
    ret = _get_opt_str(arg, width, indent)
    print(ret.strip())
    assert ret == expected.strip()


@pytest.mark.parametrize(
    "arg, width, indent,expected",
    [
        (
            Arg("foo", int, True, True, help="aaaaaaaaaaaaaaaaaaaaa"),
            10,
            8,
            """
<foo>
        aaaaaaaaaa
        aaaaaaaaaa
        a""",
        ),
    ],
)
def test_get_arg_str(arg: Arg, expected: str, width: int, indent: int):
    ret = _get_arg_str(arg, width, indent)
    print(ret.strip())
    assert ret == expected.strip()
