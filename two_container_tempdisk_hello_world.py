from __future__ import annotations

import json

from jobpool_sdk import TempDisk, await_container, disk_path, function, logging

from _shared import (
    MinimalComputeResources,
    PythonSlim,
    RESULT_JSON_PATH,
    python_command,
)


class ScratchFolder(TempDisk):
    size_gb = 1


@function(compute=MinimalComputeResources, containers=[PythonSlim], disks=[ScratchFolder])
def two_container_tempdisk_hello_world(name: str = "World") -> dict[str, object]:
    """Share a scratch folder between two containers."""
    logging.info("starting two_container_tempdisk_hello_world for %s", name)
    scratch_host_path = disk_path(ScratchFolder)
    scratch_container_path = "/scratch"
    shared_file = f"{scratch_container_path}/greeting.txt"

    writer = PythonSlim.run_async(
        command=python_command(
            f"""
            import json
            from pathlib import Path

            name = {json.dumps(name)}
            message = f"Hello, {{name}}, from container one!"
            output_path = Path({json.dumps(shared_file)})
            output_path.write_text(message + "\\n", encoding="utf-8")
            print("writer stored greeting at", output_path)
            Path({json.dumps(RESULT_JSON_PATH)}).write_text(
                json.dumps({{"message": message, "shared_file": str(output_path)}}),
                encoding="utf-8",
            )
            """
        ),
        result_json_path=RESULT_JSON_PATH,
        mount={ScratchFolder: scratch_container_path},
    )
    writer_result = await_container(writer)

    reader = PythonSlim.run_async(
        command=python_command(
            f"""
            import json
            from pathlib import Path

            input_path = Path({json.dumps(shared_file)})
            message = input_path.read_text(encoding="utf-8").strip()
            consumed = message.upper()
            print("reader loaded greeting from", input_path)
            Path({json.dumps(RESULT_JSON_PATH)}).write_text(
                json.dumps(
                    {{
                        "original_message": message,
                        "consumed_message": consumed,
                        "shared_file": str(input_path),
                    }}
                ),
                encoding="utf-8",
            )
            """
        ),
        result_json_path=RESULT_JSON_PATH,
        mount={ScratchFolder: scratch_container_path},
    )
    reader_result = await_container(reader)

    logging.info(
        "two_container_tempdisk_hello_world finished with exit codes writer=%s reader=%s",
        writer_result.exit_code,
        reader_result.exit_code,
    )
    return {
        "scratch_host_path": scratch_host_path,
        "shared_file": reader_result["shared_file"],
        "writer_message": writer_result["message"],
        "reader_message": reader_result["consumed_message"],
        "writer_exit_code": writer_result.exit_code,
        "reader_exit_code": reader_result.exit_code,
    }
