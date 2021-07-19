import pytest
from pystructopt import FieldMeta


def test_fieldmeta():
    x = FieldMeta.from_dict({"positional": True, "name": "foo", "type": int})
    assert x.positional
    x = FieldMeta.from_dict({"long": "foo", "name": "bar", "type": str, "short": "x"})
    assert x.long_name == "foo"
    assert x.short_name == "x"


@pytest.mark.parametrize("field", [FieldMeta("foo", int, long=False, positional=False)])
def test_validate(field: FieldMeta):
    with pytest.raises(ValueError):
        field.validate()
