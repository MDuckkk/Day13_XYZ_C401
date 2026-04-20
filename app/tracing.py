from __future__ import annotations
import os
from typing import Any


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))


# Only attempt Langfuse import when keys are actually configured
if tracing_enabled():
    try:
        from langfuse.decorators import observe, langfuse_context  # type: ignore
    except Exception:
        tracing_enabled = lambda: False  # noqa: E731
        observe = None
        langfuse_context = None
else:
    observe = None
    langfuse_context = None


# Fallback no-op implementations
if observe is None:
    def observe(*args: Any, **kwargs: Any):  # type: ignore
        def decorator(func):
            return func
        return decorator


if langfuse_context is None:
    class _DummyContext:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None
        def update_current_observation(self, **kwargs: Any) -> None:
            return None
    langfuse_context = _DummyContext()
