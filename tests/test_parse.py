import pytest
from pystructopt import FieldMeta


@pytest.mark.parametrize("field", [FieldMeta("foo", int, long=True, positional=True)])
def test_validate(field: FieldMeta):
    with pytest.raises(ValueError):
        field.validate()
