# Command line argument parser with dataclass

```python
@dataclass
class Opts:
    position1: str

    # optional argument
    count: int = field(metadata={"short": True, "long": True})

    # -vvv -> 3
    verbose: int = field(metadata={"short": True, "from_occurrences": True})

    # multiple value
    paths: List[Path] = field(metadata={"short": True})


opts = pystructopt.parse(Opts)
```

## Installation

`pip install pystructopt`
