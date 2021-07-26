import pytest
from pystructopt._parse import Arg


def test_fieldmeta():
    x = Arg.from_dict({"positional": True, "name": "foo", "type": int})
    assert x.positional
    x = Arg.from_dict({"long": "foo", "name": "bar", "type": str, "short": "x"})
    assert x.long_name == "foo"
    assert x.short_name == "x"


@pytest.mark.parametrize("field", [Arg("foo", int, long=False, positional=False)])
def test_validate(field: Arg):
    with pytest.raises(ValueError):
        field.validate()
