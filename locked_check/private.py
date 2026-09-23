from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from jobpool_sdk import function


@function
def private_hello(name: str = "World") -> dict[str, object]:
    """Report the mlops-components version the venv holds and how the venv was built.

    ``mlops-components`` is published only on altavo-pypi, so a successful import
    means the dependency install authenticated against that index with the
    credential the run (or its endpoint) carried.
    """
    from importlib import metadata

    venv = os.environ.get("VIRTUAL_ENV") or sys.prefix
    try:
        resolution = json.loads((Path(venv) / ".jobpool_resolution.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        resolution = None
    try:
        mlops_version = metadata.version("mlops-components")
    except metadata.PackageNotFoundError:
        mlops_version = None
    return {
        "message": f"Hello, {name}!",
        "mlops_components_version": mlops_version,
        "venv": venv,
        "resolution": resolution,
    }
