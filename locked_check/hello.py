from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests
from jobpool_sdk import function


@function
def locked_hello(name: str = "World") -> dict[str, object]:
    """Greet, and report how the executor venv was built.

    ``requests_version`` is the version the venv holds (the committed uv.lock pins
    a lowest-direct release, so a locked install is distinguishable from a fresh
    resolve) and ``resolution`` is the worker's own record of the strategy it chose.
    """
    venv = os.environ.get("VIRTUAL_ENV") or sys.prefix
    record_path = Path(venv) / ".jobpool_resolution.json"
    try:
        resolution = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        resolution = None
    return {
        "message": f"Hello, {name}!",
        "requests_version": requests.__version__,
        "venv": venv,
        "resolution": resolution,
    }
