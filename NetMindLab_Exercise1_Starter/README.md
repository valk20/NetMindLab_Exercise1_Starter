
# NetMindLab – Exercise 1
## Python Network Explorer + Wireshark + GenAI Verification

Computer Networks – HIT

### Project Overview

This project combines Python-based network diagnostics,
Wireshark packet analysis, and evidence-based GenAI verification.

The Python implementation collects local network information,
runs bounded connectivity diagnostics, calculates network delays,
and saves structured results in JSON format.

The Wireshark and GenAI sections are separate assignment phases
and must be completed according to the official Moodle guide.

## Requirements

- Python 3.10 or newer
- Windows 10/11 or macOS
- Python standard library only
- Wireshark and TShark for packet analysis
- Npcap on Windows
- Wireshark ChmodBPF helper on macOS

## Project Structure

main.py
    Main entry point and integration.

network_explorer/discovery.py
    Local hostname, operating system, IPv4,
    subnet mask, and default gateway discovery.

network_explorer/probes.py
    Ping and traceroute diagnostics.

network_explorer/performance.py
    Transmission, propagation, and nodal delay models.

network_explorer/report.py
    Measurement summary and JSON saving.

tests/
    Unit tests for discovery, probes,
    performance, and reporting.

results/measurements.json
    Generated network measurements.

results/genai_reflection.json
    GenAI verification and reflection template.

## Python Features

### Local Network Discovery

The host_summary() function retrieves:

- Hostname
- Operating system
- Active local IPv4 address
- Subnet mask
- Default gateway

Windows uses PowerShell network commands.

macOS uses route and ifconfig.

Missing information and command failures are handled safely.

### Ping Diagnostics

The ping() function:

- Accepts only allowlisted hosts
- Sends 1–4 ping requests
- Extracts individual RTT samples
- Calculates minimum, average, and maximum RTT
- Determines packet loss percentage
- Handles missing commands, timeouts, and malformed output

### Traceroute Diagnostics

The traceroute() function:

- Uses tracert on Windows
- Uses traceroute on macOS
- Limits tracing to 12 hops
- Extracts hop numbers, addresses, and RTT values
- Records missing responses and timeouts

### Delay Calculations

The project implements:

Transmission delay = packet bits / transmission rate

Propagation delay = distance / propagation speed

Nodal delay = processing + queueing + transmission + propagation

Delay values are expressed in seconds.

Negative delay components are rejected.

### Measurement Reporting

The summarize() function creates a data-driven
text summary of:

- Ping RTT and packet loss
- Traceroute observations
- Timeout and failed measurements
- Calculated delay values

The save_json() function writes the results
to results/measurements.json.

## How to Run

Open a terminal in the project directory containing main.py.

Use the actual registered Moodle group ID in place of NML-G001.

### Run Without Live Probes

Windows:

```powershell
python main.py --group NML-G001
```

macOS:

```bash
python3 main.py --group NML-G001
```

### Run With Bounded Live Probes

Windows:

```powershell
python main.py --group NML-G001 --run-probes
```

macOS:

```bash
python3 main.py --group NML-G001 --run-probes
```

The program creates or updates:

results/measurements.json

## Running Automated Tests

Windows:

```powershell
python -m unittest discover -s tests -v
```

macOS:

```bash
python3 -m unittest discover -s tests -v
```

At the latest completed Windows checkpoint,
35 automated tests passed successfully.

The tests include mocked Windows and macOS
command outputs, normal cases, and error cases.

Mocked macOS tests do not replace testing
on a real macOS computer.

## Safety Restrictions

Only these diagnostic targets are allowed:

- example.com
- 1.1.1.1

Additional restrictions:

- Maximum 4 ping requests per target
- Maximum 1 traceroute per program run
- Maximum 12 traceroute hops
- No network scanning
- No port scanning
- Do not capture unrelated network traffic

## Wireshark Analysis

The packet-analysis phase requires:

- Capturing controlled network traffic
- Identifying DNS, ICMP, TCP, HTTP, IPv4,
  and link-layer information
- Recording frame numbers and relevant fields
- Saving capture.pcapng
- Exporting packets.csv
- Comparing Python measurements with Wireshark evidence

This phase must be documented in the final report.

## GenAI Verification

The GenAI phase requires verification of at least
two technical AI claims using program output,
measurements, packet evidence, or course concepts.

Complete results/genai_reflection.json without
changing its field names or structure.

Do not include personal identifiers in the
GenAI reflection JSON.

## Submission

Follow the official Moodle assignment guide.

The final submission includes completed code,
tests, structured JSON results, Wireshark evidence,
GenAI verification records, and a technical report.

Only one member of the registered Moodle group
submits the final ZIP file.

The official Moodle Word/PDF guide is the
authoritative assignment specification.
