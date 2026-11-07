"""Bounded, allowlisted diagnostics only; no scanning."""
import platform
import subprocess
import re

ALLOWED_HOSTS = ("example.com", "1.1.1.1")


def _validate_host(host: str) -> None:
    if host not in ALLOWED_HOSTS:
        raise ValueError(f"Target not allowed: {host}")



def ping(host: str, count: int = 4) -> dict:
    """Run bounded ping and parse RTT and packet loss."""
    _validate_host(host)

    if not 1 <= count <= 4:
        raise ValueError("count must be 1..4")

    windows = platform.system() == "Windows"
    flag = "-n" if windows else "-c"

    try:
        result = subprocess.run(
            ["ping", flag, str(count), host],
            capture_output=True,
            text=True,
            errors="replace",
            timeout=25,
            check=False,
        )

    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "target": host,
            "command": "ping",
            "error": str(exc),
            "rtt_ms": [],
            "packet_loss_pct": None,
            "min_rtt_ms": None,
            "avg_rtt_ms": None,
            "max_rtt_ms": None,
        }

    output = result.stdout

    # Extract RTT only from individual ping replies.
    reply_lines = [
        line
        for line in output.splitlines()
        if "Reply from" in line or "bytes from" in line
    ]

    rtt_ms = []

    for line in reply_lines:
        match = re.search(
            r"\btime\s*[=<]\s*(\d+(?:[.,]\d+)?)\s*ms",
            line,
            re.IGNORECASE,
        )

        if match:
            value = match.group(1).replace(",", ".")
            rtt_ms.append(float(value))

    # Read packet loss from Windows or macOS summary.
    loss_match = re.search(
        r"(\d+(?:[.,]\d+)?)\s*%\s*(?:packet\s+loss|loss)",
        output,
        re.IGNORECASE,
    )

    packet_loss_pct = None

    if loss_match:
        packet_loss_pct = float(
            loss_match.group(1).replace(",", ".")
        )
    else:
        # Fallback: calculate from packet counts.
        windows_counts = re.search(
            r"Sent\s*=\s*(\d+).*?"
            r"Received\s*=\s*(\d+)",
            output,
            re.IGNORECASE | re.DOTALL,
        )

        mac_counts = re.search(
            r"(\d+)\s+packets?\s+transmitted,\s*"
            r"(\d+)\s+(?:packets?\s+)?received",
            output,
            re.IGNORECASE,
        )

        counts = windows_counts or mac_counts

        if counts:
            sent = int(counts.group(1))
            received = int(counts.group(2))

            if sent > 0:
                packet_loss_pct = (
                    (sent - received) / sent
                ) * 100

    # Calculate RTT statistics.
    min_rtt = min(rtt_ms) if rtt_ms else None
    max_rtt = max(rtt_ms) if rtt_ms else None
    avg_rtt = (
        sum(rtt_ms) / len(rtt_ms)
        if rtt_ms else None
    )

    return {
        "target": host,
        "command": "ping",
        "exit_code": result.returncode,
        "raw_output": output[-12000:],
        "error": result.stderr[-2000:],
        "rtt_ms": rtt_ms,
        "packet_loss_pct": packet_loss_pct,
        "min_rtt_ms": min_rtt,
        "avg_rtt_ms": avg_rtt,
        "max_rtt_ms": max_rtt,
    }




def traceroute(host: str) -> dict:
    """Run a bounded traceroute and parse hops and timeouts."""
    _validate_host(host)

    windows = platform.system() == "Windows"

    cmd = (
        ["tracert", "-d", "-h", "12", "-w", "1000", host]
        if windows
        else ["traceroute", "-n", "-m", "12", "-w", "1", "-q", "1", host]
    )

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=65,
            check=False,
        )

    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "target": host,
            "command": "traceroute",
            "error": str(exc),
            "hops": [],
        }

    hops = []

    for line in result.stdout.splitlines():
        hop_match = re.match(r"^\s*(\d+)\s+(.+)$", line)

        if not hop_match:
            continue

        hop_number = int(hop_match.group(1))

        if not 1 <= hop_number <= 12:
            continue

        hop_text = hop_match.group(2)

        # Extract RTT values in milliseconds.
        rtt_ms = []

        for match in re.finditer(
            r"(<\s*)?(\d+(?:[.,]\d+)?)\s*ms\b",
            hop_text,
            re.IGNORECASE,
        ):
            if match.group(1):
                # Keep values reported as <1 ms separately.
                continue

            rtt_ms.append(
                float(match.group(2).replace(",", "."))
            )

        below_1ms_count = len(
            re.findall(
                r"<\s*1\s*ms\b",
                hop_text,
                re.IGNORECASE,
            )
        )

        # Find the router's IPv4 or IPv6 address.
        address = None

        for word in hop_text.split():
            candidate = word.strip("[](),")

            try:
                import ipaddress
                address = str(ipaddress.ip_address(candidate))
                break
            except ValueError:
                continue

        # A star means that a probe received no response.
        timed_out = "*" in hop_text

        if not rtt_ms and below_1ms_count == 0:
            timed_out = True

        hops.append({
            "hop": hop_number,
            "address": address,
            "rtt_ms": rtt_ms,
            "rtt_below_1ms_count": below_1ms_count,
            "timeout": timed_out,
        })

    return {
        "target": host,
        "command": "traceroute",
        "exit_code": result.returncode,
        "raw_output": result.stdout[-18000:],
        "error": result.stderr[-2000:],
        "hops": hops,
    }

