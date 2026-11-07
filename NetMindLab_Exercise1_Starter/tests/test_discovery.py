import unittest
from unittest.mock import patch
from subprocess import CompletedProcess

from network_explorer.discovery import host_summary


class DiscoveryTests(unittest.TestCase):

    def test_host_summary_fields(self):
        result = host_summary()

        self.assertIsInstance(result, dict)

        self.assertIn("hostname", result)
        self.assertIn("os", result)
        self.assertIn("ipv4", result)
        self.assertIn("subnet_mask", result)
        self.assertIn("default_gateway", result)

    @patch("network_explorer.discovery.subprocess.run")
    def test_powershell_failure(self, mock_run):
        mock_run.side_effect = OSError("PowerShell unavailable")

        result = host_summary()

        self.assertIsNone(result["ipv4"])
        self.assertIsNone(result["subnet_mask"])
        self.assertIsNone(result["default_gateway"])

    @patch("network_explorer.discovery.subprocess.run")
    def test_invalid_json(self, mock_run):
        mock_run.return_value = CompletedProcess(
            args=["powershell"],
            returncode=0,
            stdout="This is not valid JSON",
            stderr=""
        )

        result = host_summary()

        self.assertIsNone(result["ipv4"])
        self.assertIsNone(result["subnet_mask"])
        self.assertIsNone(result["default_gateway"])

        
    @patch("network_explorer.discovery.platform.system", return_value="Darwin")
    @patch("network_explorer.discovery.subprocess.run")
    def test_macos_discovery(self, mock_run, mock_system):
        mock_run.side_effect = [
            CompletedProcess(
                args=["route"],
                returncode=0,
                stdout="gateway: 192.168.1.1\ninterface: en0\n",
                stderr=""
            ),
            CompletedProcess(
                args=["ifconfig"],
                returncode=0,
                stdout="inet 192.168.1.25 netmask 0xffffff00\n",
                stderr=""
            )
        ]

        result = host_summary()

        self.assertEqual(result["os"], "Darwin")
        self.assertEqual(result["ipv4"], "192.168.1.25")
        self.assertEqual(result["subnet_mask"], "255.255.255.0")
        self.assertEqual(result["default_gateway"], "192.168.1.1")
