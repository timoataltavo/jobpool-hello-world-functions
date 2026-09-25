from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from jobpool_core.types import ComputeResources
from jobpool_sdk import function


class OneGpu(ComputeResources):
    """Ask for one GPU so the run lands on a dev Lambda GPU pool: the shared northeurope
    CPU quota can be exhausted by prod, and the check only needs some dev worker whose
    pool forwards no package feed."""

    gpus = 1


@function(compute=OneGpu)
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
