from __future__ import annotations

import base64
import json
import shlex
from textwrap import dedent

from jobpool_sdk import Container, MinimalComputeResources

RESULT_JSON_PATH = "/tmp/jobpool-result.json"


class PythonSlim(Container):
    image = "python:3.12-slim"


def python_command(source: str) -> str:
    script = dedent(source).strip()
    encoded = base64.b64encode(script.encode("utf-8")).decode("ascii")
    bootstrap = (
        "import base64; "
        f"exec(compile(base64.b64decode({encoded!r}).decode('utf-8'), "
        "'<jobpool-container>', 'exec'))"
    )
    return f"python3 -c {shlex.quote(bootstrap)}"


__all__ = [
    "MinimalComputeResources",
    "PythonSlim",
    "RESULT_JSON_PATH",
    "python_command",
]
