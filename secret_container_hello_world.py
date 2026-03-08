from __future__ import annotations

import json

from jobpool_sdk import await_container, function, logging

from _shared import (
    MinimalComputeResources,
    PythonSlim,
    RESULT_JSON_PATH,
    python_command,
)
from tokens import fake_service_token


@function(
    compute=MinimalComputeResources,
    containers=[PythonSlim],
    tokens=[fake_service_token],
)
def secret_container_hello_world(name: str = "World") -> dict[str, object]:
    """Inject a fake token into a container and use it in the greeting."""
    logging.info("starting secret_container_hello_world for %s", name)
    job = PythonSlim.run_async(
        command=python_command(
            f"""
            import json
            from pathlib import Path

            token = Path("/run/secrets/service_token").read_text(encoding="utf-8").strip()
            message = "Hello, {name}, from a token-aware container!"
            print("secret_container_hello_world says:", message)
            print("token source: /run/secrets/service_token")
            Path({json.dumps(RESULT_JSON_PATH)}).write_text(
                json.dumps({{"message": message, "token": token}}),
                encoding="utf-8",
            )
            """
        ),
        result_json_path=RESULT_JSON_PATH,
        tokens={fake_service_token: "service_token"},
    )
    result = await_container(job)
    logging.info(
        "secret_container_hello_world finished with exit code %s",
        result.exit_code,
    )
    return {
        "message": result["message"],
        "token": result["token"],
        "exit_code": result.exit_code,
    }
