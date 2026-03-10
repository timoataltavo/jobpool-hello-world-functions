# Hello World Functions

This is a standalone JobPool function repo for training, demos, and basic
end-to-end validation against both local and deployed JobPool environments.

It is intentionally small and self-contained:

- `hello_world`: plain Python function with JobPool logging
- `container_hello_world`: runs a Docker container and returns its result
- `two_container_tempdisk_hello_world`: shares a TempDisk scratch folder across two containers
- `secret_container_hello_world`: injects a fake token into a container
- `spawn_hello_world`: submits `hello_world` as a child run and waits for it

## Files

- `hello_world.py`
- `container_hello_world.py`
- `two_container_tempdisk_hello_world.py`
- `secret_container_hello_world.py`
- `spawn_hello_world.py`
- `_shared.py`
- `tokens.py`

## Install

Create a virtual environment and install the JobPool SDK:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

If you prefer not to install this repo as a package, `pip install jobpool-sdk`
is enough for normal function development.

## Local Usage

Run from this directory:

```bash
jobpool-dev hello_world
jobpool-dev container_hello_world
jobpool-dev two_container_tempdisk_hello_world
jobpool-dev secret_container_hello_world
jobpool-dev spawn_hello_world
```

For the container-based examples, make sure the active `jobpool-dev`
environment includes the Docker extra:

```bash
uv sync --extra docker
```

Optional arguments:

```bash
jobpool-dev hello_world --name Berlin
jobpool-dev container_hello_world --name Container
jobpool-dev two_container_tempdisk_hello_world --name Scratch
jobpool-dev secret_container_hello_world --name Secret
jobpool-dev spawn_hello_world --name Child
```

## Remote Usage

This repo is also meant to be pushed to its own git remote and used with a
deployed JobPool server. A function user can then enqueue runs from a repo ref
instead of from local disk.

The exact CLI depends on the installed JobPool user tooling, but conceptually
you point JobPool at this repo and a commit/tag/branch that contains these
functions.

## Notes

The secret example uses a fake token provider on purpose. It is meant to show
the token API and container secret injection flow, not real secret handling.
