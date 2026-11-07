
"""Save measurements and summarize observed results."""

import json
from pathlib import Path


def save_json(data: dict, path: str = "results/measurements.json") -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def summarize(data: dict) -> str:
    """Summarize ping, traceroute, delays, and missing measurements."""

    lines = ["Network Measurement Summary"]

    measurements = data.get("measurements")
    if not isinstance(measurements, dict):
        measurements = data

    # PING
    ping_data = measurements.get("ping")

    if isinstance(ping_data, dict):
        ping_results = [ping_data]
    elif isinstance(ping_data, list):
        ping_results = ping_data
    else:
        ping_results = []

    if not ping_results:
        lines.append("Ping: No measurements available.")

    for result in ping_results:
        if not isinstance(result, dict):
            lines.append("Ping: Invalid measurement.")
            continue

        target = result.get("target", "unknown")
        samples = result.get("rtt_ms")

        if not isinstance(samples, list):
            samples = []

        rtt = [
            value for value in samples
            if isinstance(value, (int, float))
            and not isinstance(value, bool)
        ]

        lines.append(f"Ping target: {target}")

        if rtt:
            lines.append(
                f"RTT: min={min(rtt):.2f} ms, "
                f"avg={sum(rtt) / len(rtt):.2f} ms, "
                f"max={max(rtt):.2f} ms"
            )
        else:
            lines.append("RTT: No samples available.")

        loss = result.get("packet_loss_pct")

        if isinstance(loss, (int, float)) and not isinstance(loss, bool):
            lines.append(f"Packet loss: {loss:.2f}%")
        else:
            lines.append("Packet loss: Not available.")

        if result.get("error"):
            lines.append(f"Ping error: {result['error']}")

        if result.get("exit_code") not in (None, 0):
            lines.append(
                f"Ping exit code: {result['exit_code']}"
            )

    # TRACEROUTE
    trace_data = measurements.get("traceroute")

    if isinstance(trace_data, dict):
        trace_results = [trace_data]
    elif isinstance(trace_data, list):
        trace_results = trace_data
    else:
        trace_results = []

    if not trace_results:
        lines.append("Traceroute: No measurements available.")

    for result in trace_results:
        if not isinstance(result, dict):
            lines.append("Traceroute: Invalid measurement.")
            continue

        target = result.get("target", "unknown")
        hops = result.get("hops")

        if not isinstance(hops, list):
            hops = []

        lines.append(
            f"Traceroute to {target}: {len(hops)} hops recorded."
        )

        timeout_count = sum(
            1 for hop in hops
            if isinstance(hop, dict) and hop.get("timeout")
        )

        lines.append(
            f"Hops with missing responses: {timeout_count}"
        )

        for hop in hops:
            if not isinstance(hop, dict):
                continue

            number = hop.get("hop", "?")
            address = hop.get("address") or "unknown"
            rtt = hop.get("rtt_ms", [])

            status = (
                "partial/timeout"
                if hop.get("timeout")
                else "response recorded"
            )

            lines.append(
                f"Hop {number}: {address}, RTT={rtt}, {status}"
            )

        if result.get("error"):
            lines.append(
                f"Traceroute error: {result['error']}"
            )

        if result.get("exit_code") not in (None, 0):
            lines.append(
                f"Traceroute exit code: {result['exit_code']}"
            )

    # DELAY MODELS
    delay_data = data.get("delay_models")

    if delay_data is None:
        delay_data = data.get("delays", data.get("delay_model"))

    if isinstance(delay_data, dict):
        lines.append("Delay model:")

        found = False

        for key, value in delay_data.items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                lines.append(f"{key}: {value:.6f} seconds")
                found = True
            elif value is None:
                lines.append(f"{key}: Not available.")

        if not found:
            lines.append("No calculated delay values available.")
    else:
        lines.append("Delay model: No measurements available.")

    return "\n".join(lines)
