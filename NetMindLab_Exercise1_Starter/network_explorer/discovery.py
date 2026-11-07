
"""Local host discovery (no network scanning)."""

import platform
import socket
import subprocess
import json
import ipaddress


def host_summary() -> dict:
    """Discover local IPv4, subnet mask, and default gateway."""

    system = platform.system()

    ipv4 = None
    gateway = None
    subnet_mask = None

    if system == "Windows":
        command = """
$route = Get-NetRoute -DestinationPrefix "0.0.0.0/0" -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Sort-Object @{Expression = { $_.RouteMetric + $_.InterfaceMetric }} |
    Select-Object -First 1

if ($null -ne $route) {
    Get-NetIPConfiguration -InterfaceIndex $route.InterfaceIndex |
    ForEach-Object {
        [PSCustomObject]@{
            IPAddress = $_.IPv4Address.IPAddress
            PrefixLength = $_.IPv4Address.PrefixLength
            Gateway = $_.IPv4DefaultGateway.NextHop
        }
    } |
    ConvertTo-Json
}
"""

        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", command],
                capture_output=True,
                text=True,
                timeout=10
            )
        except (OSError, subprocess.TimeoutExpired):
            result = None

        if result is not None and result.returncode == 0 and result.stdout.strip():
            try:
                ipv4_info = json.loads(result.stdout)
            except json.JSONDecodeError:
                ipv4_info = None
        else:
            ipv4_info = None

        if isinstance(ipv4_info, dict):
            ipv4 = ipv4_info.get("IPAddress")
            gateway = ipv4_info.get("Gateway")
            prefix = ipv4_info.get("PrefixLength")

            if isinstance(prefix, int) and 0 <= prefix <= 32:
                network = ipaddress.IPv4Network(f"0.0.0.0/{prefix}")
                subnet_mask = str(network.netmask)

    elif system == "Darwin":
        try:
            route_result = subprocess.run(
                ["route", "-n", "get", "default"],
                capture_output=True,
                text=True,
                timeout=10
            )
        except (OSError, subprocess.TimeoutExpired):
            route_result = None

        interface = None

        if route_result is not None and route_result.returncode == 0:
            for line in route_result.stdout.splitlines():
                if line.strip().startswith("gateway:"):
                    gateway = line.split(":", 1)[1].strip()
                elif line.strip().startswith("interface:"):
                    interface = line.split(":", 1)[1].strip()

        interface_result = None

        if interface is not None:
            try:
                interface_result = subprocess.run(
                    ["ifconfig", interface],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            except (OSError, subprocess.TimeoutExpired):
                interface_result = None

        if interface_result is not None and interface_result.returncode == 0:
            for line in interface_result.stdout.splitlines():
                parts = line.strip().split()

                if len(parts) >= 2 and parts[0] == "inet":
                    try:
                        ipv4 = str(ipaddress.IPv4Address(parts[1]))
                    except ValueError:
                        continue

                    if "netmask" in parts:
                        mask_index = parts.index("netmask") + 1

                        if mask_index < len(parts):
                            mask_value = parts[mask_index]

                            try:
                                mask_number = int(mask_value, 16)
                                subnet_mask = str(
                                    ipaddress.IPv4Address(mask_number)
                                )
                            except ValueError:
                                subnet_mask = None

                    break

    return {
        "hostname": socket.gethostname(),
        "os": system,
        "ipv4": ipv4,
        "subnet_mask": subnet_mask,
        "default_gateway": gateway,
    }
