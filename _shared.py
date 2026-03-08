from __future__ import annotations

import json
import shlex
from textwrap import dedent

from jobpool_sdk import Container, MinimalComputeResources

RESULT_JSON_PATH = "/tmp/jobpool-result.json"


class PythonSlim(Container):
    image = "python:3.12-slim"


def python_command(source: str) -> str:
    script = dedent(source).strip()
    python_exec = f"exec python3 -c {shlex.quote(script)}"
    return f"/bin/sh -lc {shlex.quote(python_exec)}"


__all__ = [
    "MinimalComputeResources",
    "PythonSlim",
    "RESULT_JSON_PATH",
    "python_command",
]
