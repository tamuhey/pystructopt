"""Argument parser for List[Option]"""
import getopt
import logging
from collections import defaultdict
from typing import (
    Any,
    DefaultDict,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)


from ._help import get_help, is_help
from ._arg import Arg

logger = logging.getLogger(__name__)


def parse_args(
    args: List[str], options: List[Arg], description: Optional[str]
) -> Union[Dict[str, Any], str]:
    """Parse arguments with `options` and returns { option_name: value } dict or help string."""
    if is_help(args):
        return get_help(options, description)

    _validate_options(options)
    logger.info(f"options: {options}")

    # get argument for `gnu_getopt`
    shortopts, longopts, index = _get_opt_index(options)

    # parse arguments
    opts_, pos_ = getopt.gnu_getopt(args, shortopts, longopts)

    # convert arguments to dict
    opts = _parse_getopt_result(opts_, pos_, index, options)

    # convert to value
    ret: Dict[str, Any] = {}
    tmp = {meta.name: meta for meta in options}
    for k, v in opts.items():
        ret[k] = tmp[k].value_from_strs(v)
    return ret


def _parse_getopt_result(
    opts: List[Tuple[str, str]],
    pos: List[str],
    index: Dict[str, str],
    options: List[Arg],
) -> Dict[str, List[str]]:
    ret: DefaultDict[str, List[str]] = defaultdict(list)
    for k, v in opts:
        name = index[k]
        ret[name].append(v)
    pos_ = _consume_pos_args(pos, options)
    # merge pos into opts
    for k, v2 in pos_.items():
        ret[k].extend(v2)
    return ret


def _validate_options(options: List[Arg]):
    shorts: Set[str] = set()
    longs: Set[str] = set()
    for opt in options:
        opt.validate()
        for flag, name, seen in [
            (opt.short, opt.short_name, shorts),
            (opt.long, opt.long_name, longs),
        ]:
            if not flag:
                continue
            if name in seen:
                raise ValueError(f"Duplicated option: {name}")
            seen.add(name)


def _consume_pos_args(pos: List[str], options: List[Arg]) -> Dict[str, List[str]]:
    ret: DefaultDict[str, List[str]] = defaultdict(list)
    last = None
    for meta in options:
        if not meta.positional:
            continue
        last = meta.name
        if pos:
            ret[meta.name].append(pos[0])
            pos = pos[1:]
        else:
            break
    if pos:
        if not last:
            raise ValueError(f"Unknown positional arguments: {pos}")
        ret[last].extend(pos)
    return ret


def _get_opt_index(options: List[Arg]) -> Tuple[str, List[str], Dict[str, str]]:
    shortopts, index = _get_shortopt(options)
    longopts, index2 = _get_longopt(options)
    # merge index
    index.update(index2)
    return shortopts, longopts, index


def _get_shortopt(options: List[Arg]) -> Tuple[str, Dict[str, str]]:
    """Returns (opt, index). Index contains `shortopt: original name`"""
    index: Dict[str, str] = {}
    ret = ""
    for meta in options:
        if meta.short:
            name = meta.short_name
            ret += name
            if meta.value_required():
                ret += ":"
            index["-" + name] = meta.name
    return ret, index


def _get_longopt(options: List[Arg]) -> Tuple[List[str], Dict[str, str]]:
    index: Dict[str, str] = {}
    ret: List[str] = []
    for meta in options:
        if meta.long:
            name = meta.long_name
            item = name
            if meta.value_required():
                item += "="
            ret.append(item)
            index["--" + name] = meta.name
    return ret, index
