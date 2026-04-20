from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"


class DashboardHandler(SimpleHTTPRequestHandler):
    backend_url = "http://localhost:8000"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def do_GET(self) -> None:
        if self.path == "/api/metrics":
            self._proxy_metrics()
            return
        super().do_GET()

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def _proxy_metrics(self) -> None:
        target = f"{self.backend_url.rstrip('/')}/metrics"
        try:
            with urlopen(target, timeout=5) as response:
                payload = response.read()
                status = response.status
                content_type = response.headers.get("Content-Type", "application/json")
        except HTTPError as error:
            self._write_json(
                status=error.code,
                payload={"error": "backend_http_error", "detail": f"{error.code} {error.reason}"},
            )
            return
        except URLError as error:
            self._write_json(
                status=HTTPStatus.BAD_GATEWAY,
                payload={"error": "backend_unreachable", "detail": str(error.reason)},
            )
            return

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(payload)

    def _write_json(self, status: int, payload: dict[str, str]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve the custom observability dashboard.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8501)
    parser.add_argument("--backend", default="http://localhost:8000")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    DashboardHandler.backend_url = args.backend
    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"Dashboard available at http://{args.host}:{args.port}")
    print(f"Proxying metrics from {args.backend.rstrip('/')}/metrics")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
