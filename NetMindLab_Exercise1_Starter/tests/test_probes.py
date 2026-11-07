
import unittest
import subprocess
from unittest.mock import patch

from network_explorer.probes import ping, traceroute


class PingTests(unittest.TestCase):

    @patch("network_explorer.probes.platform.system", return_value="Windows")
    @patch("network_explorer.probes.subprocess.run")
    def test_windows_ping(self, mock_run, mock_system):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["ping"],
            returncode=0,
            stdout=(
                "Reply from 1.1.1.1: bytes=32 time=10ms TTL=56\n"
                "Reply from 1.1.1.1: bytes=32 time=20ms TTL=56\n"
                "Reply from 1.1.1.1: bytes=32 time=30ms TTL=56\n"
                "Reply from 1.1.1.1: bytes=32 time=40ms TTL=56\n"
                "Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)\n"
            ),
            stderr=""
        )

        result = ping("1.1.1.1")

        self.assertEqual(result["rtt_ms"], [10.0, 20.0, 30.0, 40.0])
        self.assertEqual(result["packet_loss_pct"], 0.0)
        self.assertEqual(result["min_rtt_ms"], 10.0)
        self.assertEqual(result["avg_rtt_ms"], 25.0)
        self.assertEqual(result["max_rtt_ms"], 40.0)
        self.assertEqual(mock_run.call_args.args[0], [
            "ping", "-n", "4", "1.1.1.1"
        ])

    @patch("network_explorer.probes.platform.system", return_value="Darwin")
    @patch("network_explorer.probes.subprocess.run")
    def test_macos_ping(self, mock_run, mock_system):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["ping"],
            returncode=0,
            stdout=(
                "64 bytes from 1.1.1.1: icmp_seq=0 ttl=57 time=12.5 ms\n"
                "64 bytes from 1.1.1.1: icmp_seq=1 ttl=57 time=18.5 ms\n"
                "2 packets transmitted, 2 packets received, 0.0% packet loss\n"
            ),
            stderr=""
        )

        result = ping("1.1.1.1", count=2)

        self.assertEqual(result["rtt_ms"], [12.5, 18.5])
        self.assertEqual(result["packet_loss_pct"], 0.0)
        self.assertEqual(result["avg_rtt_ms"], 15.5)
        self.assertEqual(mock_run.call_args.args[0], [
            "ping", "-c", "2", "1.1.1.1"
        ])

    @patch("network_explorer.probes.platform.system", return_value="Windows")
    @patch("network_explorer.probes.subprocess.run")
    def test_packet_loss(self, mock_run, mock_system):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["ping"],
            returncode=1,
            stdout=(
                "Reply from 1.1.1.1: bytes=32 time=20ms TTL=56\n"
                "Reply from 1.1.1.1: bytes=32 time=30ms TTL=56\n"
                "Request timed out.\n"
                "Request timed out.\n"
                "Packets: Sent = 4, Received = 2, Lost = 2 (50% loss)\n"
            ),
            stderr=""
        )

        result = ping("1.1.1.1")

        self.assertEqual(result["rtt_ms"], [20.0, 30.0])
        self.assertEqual(result["packet_loss_pct"], 50.0)

    @patch("network_explorer.probes.subprocess.run")
    def test_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=["ping"], timeout=25
        )

        result = ping("example.com")

        self.assertEqual(result["rtt_ms"], [])
        self.assertIsNone(result["packet_loss_pct"])
        self.assertIn("error", result)

    @patch("network_explorer.probes.subprocess.run")
    def test_invalid_output(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["ping"],
            returncode=1,
            stdout="Unexpected output",
            stderr=""
        )

        result = ping("example.com")

        self.assertEqual(result["rtt_ms"], [])
        self.assertIsNone(result["packet_loss_pct"])
        self.assertIsNone(result["min_rtt_ms"])
        self.assertIsNone(result["avg_rtt_ms"])
        self.assertIsNone(result["max_rtt_ms"])

    def test_disallowed_host(self):
        with self.assertRaises(ValueError):
            ping("google.com")

    def test_invalid_count(self):
        with self.assertRaises(ValueError):
            ping("example.com", count=5)


class TracerouteTests(unittest.TestCase):

    @patch("network_explorer.probes.platform.system", return_value="Windows")
    @patch("network_explorer.probes.subprocess.run")
    def test_windows_traceroute(self, mock_run, mock_system):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["tracert"],
            returncode=0,
            stdout=(
                "Tracing route to 1.1.1.1\n"
                "  1     2 ms     3 ms     4 ms  192.168.1.1\n"
                "  2    10 ms    12 ms    11 ms  10.0.0.1\n"
                "  3    20 ms    21 ms    19 ms  1.1.1.1\n"
                "Trace complete.\n"
            ),
            stderr=""
        )

        result = traceroute("1.1.1.1")

        self.assertEqual(len(result["hops"]), 3)
        self.assertEqual(result["hops"][0]["hop"], 1)
        self.assertEqual(result["hops"][0]["address"], "192.168.1.1")
        self.assertEqual(result["hops"][0]["rtt_ms"], [2.0, 3.0, 4.0])
        self.assertFalse(result["hops"][0]["timeout"])
        self.assertEqual(mock_run.call_args.args[0], [
            "tracert", "-d", "-h", "12", "-w", "1000", "1.1.1.1"
        ])

    @patch("network_explorer.probes.platform.system", return_value="Darwin")
    @patch("network_explorer.probes.subprocess.run")
    def test_macos_traceroute(self, mock_run, mock_system):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["traceroute"],
            returncode=0,
            stdout=(
                "traceroute to 1.1.1.1, 12 hops max\n"
                " 1  192.168.1.1  2.5 ms\n"
                " 2  10.0.0.1  8.7 ms\n"
                " 3  1.1.1.1  15.2 ms\n"
            ),
            stderr=""
        )

        result = traceroute("1.1.1.1")

        self.assertEqual(len(result["hops"]), 3)
        self.assertEqual(result["hops"][0]["rtt_ms"], [2.5])
        self.assertEqual(result["hops"][2]["address"], "1.1.1.1")
        self.assertEqual(mock_run.call_args.args[0], [
            "traceroute", "-n", "-m", "12",
            "-w", "1", "-q", "1", "1.1.1.1"
        ])

    @patch("network_explorer.probes.subprocess.run")
    def test_traceroute_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd=["tracert"], timeout=65
        )

        result = traceroute("example.com")

        self.assertEqual(result["hops"], [])
        self.assertIn("error", result)

    @patch("network_explorer.probes.platform.system", return_value="Windows")
    @patch("network_explorer.probes.subprocess.run")
    def test_partial_traceroute(self, mock_run, mock_system):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["tracert"],
            returncode=1,
            stdout=(
                "  1     2 ms     3 ms     4 ms  192.168.1.1\n"
                "  2     *        *        *     Request timed out.\n"
                "  3    10 ms     *       12 ms  10.0.0.1\n"
            ),
            stderr=""
        )

        result = traceroute("example.com")

        self.assertEqual(len(result["hops"]), 3)
        self.assertTrue(result["hops"][1]["timeout"])
        self.assertIsNone(result["hops"][1]["address"])
        self.assertEqual(result["hops"][1]["rtt_ms"], [])
        self.assertTrue(result["hops"][2]["timeout"])
        self.assertEqual(result["hops"][2]["rtt_ms"], [10.0, 12.0])

    def test_traceroute_disallowed_host(self):
        with self.assertRaises(ValueError):
            traceroute("google.com")
           


if __name__ == "__main__":
    unittest.main()
