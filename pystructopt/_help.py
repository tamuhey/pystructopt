"""Help string"""
import textwrap


from typing import List, Optional, Tuple
from ._arg import Arg
import string

TEMPLATE = string.Template(
    """${header}

USAGE:
${usage}

FLAGS:
${flags}

OPTIONS:
${options}

ARGS:
${args}
"""
)

_INDENTS = [4, 8]
_FIELD_HELP_WIDTH = 70


def get_help(args: List[Arg], cmd: str, header: Optional[str]) -> str:
    ret = TEMPLATE.safe_substitute(header=header or "")
    return ret


def _get_usage(arg: List[Arg], cmd: str) -> str:
    template = f"{cmd} [FLAGS/OPTIONS]"


def _get_flag_str(
    arg: Arg, help_width: int = _FIELD_HELP_WIDTH, help_indent: int = _INDENTS[1]
) -> str:
    ret = _get_flag_line(arg)
    if arg.help:
        ret += "\n"
        ret += _get_help_str(arg.help, help_width, help_indent)
    return ret


def _get_opt_str(
    arg: Arg, help_width: int = _FIELD_HELP_WIDTH, help_indent: int = _INDENTS[1]
) -> str:
    ret = _get_flag_line(arg).rstrip()
    if arg.value_required():
        ret += f" <{arg.long_name}>"
    if arg.help:
        ret += "\n"
        ret += _get_help_str(arg.help, help_width, help_indent)
    return ret


def _get_arg_str(
    arg: Arg, help_width: int = _FIELD_HELP_WIDTH, help_indent: int = _INDENTS[1]
) -> str:
    ret = f"<{arg.long_name}>"
    if arg.help:
        ret += "\n"
        ret += _get_help_str(arg.help, help_width, help_indent)
    return ret


def _get_help_str(help_str: str, help_width: int, help_indent: int) -> str:
    ret = "\n".join(textwrap.wrap(help_str, help_width))
    ret = textwrap.indent(ret, " " * help_indent)
    return ret


def _get_flag_line(arg: Arg) -> str:
    ret = ""
    if arg.short:
        ret += "-" + arg.short_name + ", "
    else:
        ret += " " * 4
    if arg.long:
        ret += "--" + arg.long_name
    return ret


def is_help(args: List[str]) -> bool:
    return "--help" in args


def _get_opt_field(arg: Arg) -> Tuple[Optional[str], Optional[str]]:
    short, long = None, None
    if arg.short:
        short = arg.short_name
    if arg.long:
        long = arg.long_name
    return short, long
