from pathlib import Path
import string


readme_tmp = string.Template(Path("./README_tmp.md").read_text())
ret = readme_tmp.substitute({"basic_py": Path("./examples/basic.py").read_text()})
Path("./README.md").write_text(ret)
