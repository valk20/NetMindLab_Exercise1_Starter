# NetMindLab - Exercise 1 Starter

This is an **incomplete student starter**, not a finished solution.

Exercise 1 combines:

1. Python Network Explorer implementation,
2. Wireshark packet analysis,
3. GenAI verification and structured reflection.

**The Exercise 1 Word/PDF guide published on Moodle is the authoritative assignment specification.**  
`EXERCISE_1_EN.md` in this ZIP is the matching starter-project companion.

## Requirements

- Python 3.10+; standard library only for the Python project.
- Windows 10/11 recommended.
- Wireshark, Npcap, and TShark are required for the packet-analysis part.
- Work in your registered `NML-Gxxx` Moodle group (1-3 students).

## Python run commands

```powershell
python main.py --group NML-G001
python -m unittest discover -s tests -v
```

For bounded live diagnostics:

```powershell
python main.py --group NML-G001 --run-probes
```

The program writes `results/measurements.json`. The starter also includes `results/genai_reflection.json`, which you complete manually after the required GenAI verification task.

## Required Python work - quick map

- `network_explorer/discovery.py` -> active IPv4, subnet mask, default gateway
- `network_explorer/probes.py::ping()` -> RTT samples, packet loss, min/avg/max RTT analysis
- `network_explorer/probes.py::traceroute()` -> hop/address/RTT/timeout parsing
- `network_explorer/performance.py::nodal_delay()` -> four-component nodal delay + validation
- `network_explorer/report.py::summarize()` -> concise data-driven summary
- `tests/` -> add tests for parsing, nodal delay, and failure/edge cases
- integration -> complete the TODOs so `nodal_s` and `summary` contain real values

## Safety

Do not change the allowlist in `probes.py`: `example.com` and `1.1.1.1` only. Keep the supplied ping/traceroute bounds. Do not scan networks or ports.

## Wireshark + GenAI

The assignment also requires manual Wireshark analysis, `capture.pcapng`, `packets.csv`, packet/frame evidence, a Python/Wireshark cross-check, and verification of at least two GenAI technical claims. Complete `results/genai_reflection.json` without changing its field names and without entering student names or other personal identifiers.

See the Moodle Word/PDF guide and `EXERCISE_1_EN.md` for the complete workflow, rubric, deliverables, and checklist.
