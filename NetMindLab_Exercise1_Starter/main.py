
"""Entry point: python main.py --group NML-G001 [--run-probes]"""

import argparse
from datetime import datetime, timezone

from network_explorer.discovery import host_summary
from network_explorer.performance import (
    nodal_delay,
    propagation_delay,
    transmission_delay,
)
from network_explorer.probes import ALLOWED_HOSTS, ping, traceroute
from network_explorer.report import save_json, summarize


def build_delay_models() -> dict:
    """Build the Chapter 1 delay-model section."""

    transmission_s = transmission_delay(12_000, 10_000_000)
    propagation_s = propagation_delay(100_000)

    nodal_s = nodal_delay(
        processing_s=0.0005,
        queueing_s=0.0010,
        transmission_s=transmission_s,
        propagation_s=propagation_s,
    )

    return {
        "processing_s": 0.0005,
        "queueing_s": 0.0010,
        "transmission_s": transmission_s,
        "propagation_s": propagation_s,
        "nodal_s": nodal_s,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="NetMindLab Exercise 1"
    )

    parser.add_argument(
        "--group",
        required=True,
        help="Registered group ID, e.g. NML-G001"
    )

    parser.add_argument(
        "--run-probes",
        action="store_true",
        help="Perform bounded public network diagnostics"
    )

    args = parser.parse_args()

    if not (
        args.group.startswith("NML-G")
        and len(args.group) == 8
        and args.group[5:].isdigit()
        and 1 <= int(args.group[5:]) <= 130
    ):
        parser.error("--group must be NML-G001 through NML-G130")

    data = {
        "schema_version": "1.0",
        "group_id": args.group,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "host": host_summary(),
        "measurements": {
            "ping": [],
            "traceroute": None
        },
        "delay_models": build_delay_models(),
    }

    if args.run_probes:
        data["measurements"]["ping"] = [
            ping(host) for host in ALLOWED_HOSTS
        ]

        data["measurements"]["traceroute"] = traceroute(
            "example.com"
        )

    data["summary"] = summarize(data)

    save_json(data)

    print("Wrote results/measurements.json")
    print(data["summary"])


if __name__ == "__main__":
    main()
