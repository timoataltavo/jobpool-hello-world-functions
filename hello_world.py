from __future__ import annotations

from jobpool_sdk import function, logging


@function
def hello_world(name: str = "World") -> dict[str, str]:
    """Log and return a basic greeting."""
    logging.info("hello_world started for %s", name)
    message = f"Hello, {name}!"
    logging.info("hello_world returning %s", message)
    return {"message": message}
