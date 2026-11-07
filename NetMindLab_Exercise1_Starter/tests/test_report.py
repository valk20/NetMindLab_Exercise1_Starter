
import unittest
import json
import tempfile
from pathlib import Path

from network_explorer.report import summarize, save_json


class ReportTests(unittest.TestCase):

    def test_complete_summary(self):
        data = {
            "ping": {
                "target": "example.com",
                "rtt_ms": [20, 30, 40],
                "packet_loss_pct": 0
            },
            "traceroute": {
                "target": "example.com",
                "hops": [
                    {
                        "hop": 1,
                        "address": "192.168.1.1",
                        "rtt_ms": [2],
                        "timeout": False
                    }
                ]
            },
            "delays": {
                "nodal_delay_s": 0.01
            }
        }

        result = summarize(data)

        self.assertIn("avg=30.00 ms", result)
        self.assertIn("Packet loss: 0.00%", result)
        self.assertIn("1 hops recorded", result)
        self.assertIn("0.010000 seconds", result)

    def test_missing_measurements(self):
        result = summarize({})

        self.assertIn("No measurements available", result)
        self.assertIn("Ping:", result)
        self.assertIn("Traceroute:", result)

    def test_ping_failure(self):
        data = {
            "ping": {
                "target": "example.com",
                "rtt_ms": [],
                "packet_loss_pct": None,
                "error": "Ping timed out"
            }
        }

        result = summarize(data)

        self.assertIn("No samples available", result)
        self.assertIn("Packet loss: Not available", result)
        self.assertIn("Ping timed out", result)

    def test_traceroute_timeout(self):
        data = {
            "traceroute": {
                "target": "example.com",
                "hops": [
                    {
                        "hop": 1,
                        "address": None,
                        "rtt_ms": [],
                        "timeout": True
                    }
                ]
            }
        }

        result = summarize(data)

        self.assertIn("Hops with missing responses: 1", result)
        self.assertIn("partial/timeout", result)

    def test_save_json(self):
        data = {"ping": {"packet_loss_pct": 25.0}}

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "results" / "measurements.json"

            save_json(data, str(path))

            self.assertTrue(path.exists())

            saved_data = json.loads(
                path.read_text(encoding="utf-8")
            )

            self.assertEqual(saved_data, data)


if __name__ == "__main__":
    unittest.main()
