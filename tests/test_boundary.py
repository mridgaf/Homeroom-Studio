"""The portability boundary: tools/ must never import from reason_voice/.

The beat generator is DAW-neutral. Reason Voice is allowed to read the
generator's output; the generator must not know Reason exists. See
PACKAGING-GAP-ANALYSIS.md Part 4a.

Parses imports with ast rather than grepping, because several tools/ modules
legitimately mention the string "reason_voice" in a ~/.reason_voice/... state
path. A path is not a dependency.
"""

import ast
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"


def _imported_names(path):
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module


def test_tools_never_import_reason_voice():
    offenders = []
    for py in sorted(TOOLS.glob("*.py")):
        for name in _imported_names(py):
            if name == "reason_voice" or name.startswith("reason_voice."):
                offenders.append("{}: {}".format(py.name, name))
    assert not offenders, (
        "tools/ must stay DAW-neutral, but these import Reason Voice:\n  "
        + "\n  ".join(offenders)
    )
