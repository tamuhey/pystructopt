import dataclasses
from typing import Any, List, Type

from ._parse import FieldMeta


def get_options(datacls: Type[Any]) -> List[FieldMeta]:
    fields = dataclasses.fields(datacls)
    annots = datacls.__annotations__
    options: List[FieldMeta] = []
    for v in fields:
        meta = {"name": v.name, "type": annots[v.name], **v.metadata}
        ret = FieldMeta.from_dict(meta)
        options.append(ret)
    return options
