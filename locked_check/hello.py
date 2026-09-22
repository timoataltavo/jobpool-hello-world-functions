from __future__ import annotations

import requests
from jobpool_sdk import function


@function
def locked_hello(name: str = "World") -> dict[str, str]:
    """Greet, and report the requests version the executor venv installed from uv.lock."""
    return {"message": f"Hello, {name}!", "requests_version": requests.__version__}
