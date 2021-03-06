# Command line argument parser with dataclass

```python
from typing import List
from pathlib import Path
import pystructopt
from dataclasses import dataclass, field


@dataclass
class Opts:
    # basic optional argument (--opt)
    opt: str

    # short optional argument: -e
    extremelylonglonglongname: str = field(metadata={"short": True})

    # positional argument
    count: int = field(metadata={"positional": True})

    # from occurrences: -vvv -> 3
    verbose: int = field(metadata={"short": True, "from_occurrences": True})

    # multiple values into list
    paths: List[Path]

    # customize option name
    foo: int = field(metadata={"short": "x"})

    # default value
    bar: str = "bar"


opts = pystructopt.parse(Opts)
print(opts)

```

## Installation

`pip install pystructopt`
