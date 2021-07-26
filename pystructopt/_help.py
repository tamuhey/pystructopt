"""Help string"""


from typing import List
from ._parse import Arg
import string

TEMPLATE = string.Template(
    """
${header}

Arguments:
"""
)


def get_help(args: List[Arg], header: str) -> str:
    ret = TEMPLATE.safe_substitute(header=header)
    opt_field = list(map(_get_opt_field, args))
    max_len = max(map(len, opt_field))
    for (arg, opt) in zip(args, opt_field):
        ret += f"  {opt: <{max_len}} {arg.help or ''}"
    return ret


def _get_opt_field(arg: Arg) -> str:
    opts = ""
    if arg.short:
        opts += arg.short_name
    if arg.long:
        if opts:
            opts += ", " + arg.long_name
        else:
            opts += arg.long_name
    return opts
