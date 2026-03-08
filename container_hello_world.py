from __future__ import annotations

import json

from jobpool_sdk import await_container, function, logging

from _shared import (
    MinimalComputeResources,
    PythonSlim,
    RESULT_JSON_PATH,
    python_command,
)


@function(compute=MinimalComputeResources, containers=[PythonSlim])
def container_hello_world(name: str = "World") -> dict[str, object]:
    """Run a container that logs and returns a greeting."""
    logging.info("starting container_hello_world for %s", name)
    message = f"Hello, {name}, from a container!"
    job = PythonSlim.run_async(
        command=python_command(
            f"""
            import json
            from pathlib import Path

            message = {json.dumps(message)}
            print("container_hello_world says:", message)
            Path({json.dumps(RESULT_JSON_PATH)}).write_text(
                json.dumps({{"message": message}}),
                encoding="utf-8",
            )
            """
        ),
        result_json_path=RESULT_JSON_PATH,
    )
    result = await_container(job)
    logging.info("container_hello_world finished with exit code %s", result.exit_code)
    return {
        "message": result["message"],
        "exit_code": result.exit_code,
    }
