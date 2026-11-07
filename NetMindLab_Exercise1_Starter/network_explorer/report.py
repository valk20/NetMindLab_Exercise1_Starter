"""Save measurements; student extends with analysis and interpretation."""
import json
from pathlib import Path


def save_json(data: dict, path: str = "results/measurements.json") -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def summarize(data: dict) -> str:
    """TODO: summarize observed RTT/loss, traceroute and modelled delays."""
    raise NotImplementedError("Student task: write a concise textual summary")
