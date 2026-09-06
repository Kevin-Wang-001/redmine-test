"""Unit tests for health_server.py."""

import json
import threading
import unittest
from http.client import HTTPConnection

from health_server import SERVICE_NAME, SERVICE_VERSION, create_server


class HealthServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server()
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.port = cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def _get(self, path):
        conn = HTTPConnection("127.0.0.1", self.port, timeout=5)
        try:
            conn.request("GET", path)
            resp = conn.getresponse()
            body = resp.read()
            return resp.status, resp.getheader("Content-Type"), body
        finally:
            conn.close()

    def test_health_returns_ok(self):
        status, content_type, body = self._get("/health")
        self.assertEqual(status, 200)
        self.assertIn("application/json", content_type)
        self.assertEqual(json.loads(body.decode("utf-8")), {"status": "ok"})

    def test_version_returns_metadata(self):
        status, content_type, body = self._get("/version")
        self.assertEqual(status, 200)
        self.assertIn("application/json", content_type)
        self.assertEqual(
            json.loads(body.decode("utf-8")),
            {"service": SERVICE_NAME, "version": SERVICE_VERSION},
        )

    def test_unknown_path_returns_404(self):
        status, _, body = self._get("/unknown")
        self.assertEqual(status, 404)
        self.assertEqual(json.loads(body.decode("utf-8")), {"error": "not found"})


if __name__ == "__main__":
    unittest.main()
