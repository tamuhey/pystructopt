# Command line argument parser with dataclass

```python
@dataclass
class Opts:
    # basic optional argument
    opt: str

    # short optional argument: -e
    extremelylonglonglongname: str = field(metadata={"short": True})

    # positional argument
    count: int = field(metadata={"positional": True})

    # -vvv -> 3
    verbose: int = field(
        metadata={"short": True, "from_occurrences": True, "positional": False}
    )

    # multiple value
    paths: List[Path] = field(metadata={"short": True})

    # customize option name
    foo: int = field(metadata={"short": True, "short_name": "x"})

    # default value
    bar: str = "bar"


opts: Opts = pystructopt.parse(Opts)
print(opts.verbose)
```

## Installation

`pip install pystructopt`
