from __future__ import annotations

import time
import uuid

from starlette.types import ASGIApp, Receive, Scope, Send
from structlog.contextvars import bind_contextvars, clear_contextvars


class CorrelationIdMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        clear_contextvars()

        headers = dict(scope.get("headers", []))
        raw_id = headers.get(b"x-request-id", b"").decode()
        correlation_id = raw_id if raw_id else f"req-{uuid.uuid4().hex[:8]}"

        bind_contextvars(correlation_id=correlation_id)

        # Gắn vào scope["state"] để request.state.correlation_id hoạt động
        if "state" not in scope:
            scope["state"] = {}
        scope["state"]["correlation_id"] = correlation_id

        start = time.perf_counter()

        async def send_with_headers(message):
            if message["type"] == "http.response.start":
                elapsed = int((time.perf_counter() - start) * 1000)
                headers_list = list(message.get("headers", []))
                headers_list.append((b"x-request-id", correlation_id.encode()))
                headers_list.append((b"x-response-time-ms", str(elapsed).encode()))
                message = {**message, "headers": headers_list}
            await send(message)

        await self.app(scope, receive, send_with_headers)