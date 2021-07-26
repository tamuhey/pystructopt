"""Create Option list from dataclass definition"""
import dataclasses
from typing import Any, List, Type

from ._parse import Arg


def get_options(datacls: Type[Any]) -> List[Arg]:
    fields = dataclasses.fields(datacls)
    annots = datacls.__annotations__
    options: List[Arg] = []
    for v in fields:
        meta = {"name": v.name, "type": annots[v.name], **v.metadata}
        ret = Arg.from_dict(meta)
        options.append(ret)
    return options
