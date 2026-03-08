from __future__ import annotations

from jobpool_sdk import TokenContext, token


@token(name="fake_service_token")
def fake_service_token(ctx: TokenContext) -> str:
    """Return a deterministic fake token for training and test runs."""
    return f"fake-token-for-{ctx.function_name}"
