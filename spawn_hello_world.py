from __future__ import annotations

from jobpool_sdk import await_function, function, logging

from hello_world import hello_world


@function
def spawn_hello_world(name: str = "World") -> dict[str, object]:
    """Submit hello_world as a child run, then wait for and return its result."""
    logging.info("submitting child hello_world run for %s", name)
    child_run_id = hello_world.run_async(name=name)
    child_result = await_function(child_run_id)
    if not child_result.success:
        logging.error("child hello_world run failed: %s", child_result.error)
        return {
            "child_run_id": child_run_id,
            "success": False,
            "error": child_result.error,
        }
    logging.info("child hello_world run %s finished", child_run_id)
    return {
        "child_run_id": child_run_id,
        "success": True,
        "message": child_result["message"],
    }
