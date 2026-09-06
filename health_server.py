"""Minimal HTTP service with a /health endpoint (standard library only)."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

SERVICE_NAME = "redmine-test"
SERVICE_VERSION = "0.1.0"


class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/health":
            self._send_json(200, {"status": "ok"})
        elif path == "/version":
            self._send_json(
                200,
                {"service": SERVICE_NAME, "version": SERVICE_VERSION},
            )
        else:
            self._send_json(404, {"error": "not found"})

    def _send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


def create_server(host="127.0.0.1", port=0):
    return HTTPServer((host, port), HealthCheckHandler)


if __name__ == "__main__":
    server = create_server(port=8000)
    print(f"Health service listening on http://127.0.0.1:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
