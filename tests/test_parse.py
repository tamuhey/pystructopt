import pytest
from pystructopt import FieldMeta


def test_fieldmeta():
    x = FieldMeta.from_dict({"positional": True, "name": "foo", "type": int})
    assert x.positional


@pytest.mark.parametrize("field", [FieldMeta("foo", int, long=False, positional=False)])
def test_validate(field: FieldMeta):
    with pytest.raises(ValueError):
        field.validate()
