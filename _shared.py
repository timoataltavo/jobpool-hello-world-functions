from __future__ import annotations

import json
from textwrap import dedent

from jobpool_sdk import Container, MinimalComputeResources

RESULT_JSON_PATH = "/tmp/jobpool-result.json"


class PythonSlim(Container):
    image = "python:3.12-slim"


def python_command(source: str) -> str:
    script = dedent(source).strip()
    return f"python -c {json.dumps(script)}"


__all__ = [
    "MinimalComputeResources",
    "PythonSlim",
    "RESULT_JSON_PATH",
    "python_command",
]
