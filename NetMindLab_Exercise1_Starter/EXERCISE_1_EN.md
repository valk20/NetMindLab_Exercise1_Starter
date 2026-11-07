# Exercise 1 - Python Network Explorer + Wireshark + GenAI Verification

**Computer Networks | NetMindLab**  
**Due:** 27 November 2026, 23:00  
**Total:** 100 points  
**Group:** NML-G001 ... NML-G130 | 1-3 students

> **Authoritative assignment specification:** The Exercise 1 Word/PDF guide published on Moodle is the authoritative specification. This file is the matching starter-project companion and summarizes the same requirements.

## Core rule

Evidence comes first. Complete the Python measurements and manual Wireshark analysis before relying on GenAI. GenAI output is not evidence unless you verify it against your code, measurements, packet/frame data, or course concepts.

## Exercise flow

### Part A - Complete the Python Network Explorer

Use this starter project and complete the required TODOs while preserving the public function names, project structure, tests, and safety restrictions.

Required implementation:

- `network_explorer/discovery.py::host_summary()` - active IPv4, subnet mask, default gateway, safe handling of missing values.
- `network_explorer/probes.py::ping()` - RTT samples, packet loss, min/avg/max RTT, robust failure handling.
- `network_explorer/probes.py::traceroute()` - hop number, address, RTT(s), timeout/no-response state.
- `network_explorer/performance.py::nodal_delay()` - `d_proc + d_queue + d_trans + d_prop`, with validation of negative inputs.
- `network_explorer/report.py::summarize()` - concise summary based on actual measurements and failures.
- `tests/` - keep the starter tests and add tests for nodal delay, one ping parsing case, one traceroute parsing case, and at least one failure/edge case.

No required function may remain as `NotImplementedError` in the submitted project. Your completed functions must actually be used by `main.py`.

Run tests:

```powershell
python -m unittest discover -s tests -v
```

Run without live probes:

```powershell
python main.py --group NML-Gxxx
```

Run with bounded probes:

```powershell
python main.py --group NML-Gxxx --run-probes
```

The completed program must create valid `results/measurements.json` with real computed/derived values where applicable.

### Safe Python probe limits

Only these targets are allowlisted:

- `example.com`
- `1.1.1.1`

Limits:

- at most four ping requests per target;
- one traceroute to `example.com` per run;
- maximum 12 hops;
- do not scan networks or ports;
- do not probe the default gateway unless the Wireshark instructions explicitly require it.

## Part B - Wireshark packet analysis

Use Windows 10/11 with Wireshark, Npcap, and TShark. Wi-Fi or Ethernet is acceptable. Monitor mode is not required.

Establish a local baseline with:

```powershell
ipconfig /all
arp -a
nslookup httpforever.com
```

Generate controlled traffic while Wireshark is capturing on the active interface:

```powershell
nslookup httpforever.com
ping <default-gateway>
curl.exe http://httpforever.com/
```

Save the capture as `capture.pcapng`. If HTTP or ICMP is blocked, use the instructor-provided fallback PCAP and state this clearly in the report.

Before using GenAI, manually identify and record packet/frame evidence for:

1. local IPv4 address and active interface;
2. default gateway IPv4 address;
3. DNS server that answered;
4. queried hostname and returned IP;
5. DNS transport protocol and destination port;
6. TCP SYN -> SYN/ACK -> ACK handshake frames;
7. client source port and server destination port;
8. HTTP GET frame;
9. HTTP response status code;
10. source/destination IP addresses for the GET frame;
11. source/destination link-layer addresses for the same frame;
12. why the remote server IP can differ from the Ethernet destination MAC.

Export structured packet data with TShark to `packets.csv` using the command given in the Moodle guide.

## Part C - GenAI verification and reflection

Required sequence:

**Manual answers + program measurements -> structured evidence -> GenAI -> verification -> final human decision**

Use a GenAI tool for at least one meaningful networking task, such as interpreting an unexpected result, explaining ping/route behavior, reviewing a parsing issue, or connecting Python measurements with Wireshark evidence.

For at least two AI technical claims:

1. record initial confidence (1-5) before verification;
2. verify against `measurements.json`, program output/source code, Wireshark frames/fields, `packets.csv`, or course concepts;
3. classify the claim as **Correct**, **Partly correct**, or **Incorrect**;
4. record whether you challenged the AI and whether you asked a follow-up question;
5. record final confidence (1-5);
6. decide **Accept**, **Modify**, or **Reject**;
7. provide a short evidence-based justification;
8. identify any remaining uncertainty and what additional evidence would resolve it.

Complete the supplied:

`results/genai_reflection.json`

Do not change its field names or structure. Use only the Moodle group ID; do not enter student names, email addresses, or other personal identifiers.

## Required report

Submit an integrated **2-4 page technical report** with:

1. Group details: group ID, names, student IDs, date, and capture laptop.
2. Python implementation: completed functions and test results.
3. Python measurements: discovery, ping, traceroute, and delay findings.
4. Wireshark setup and manual analysis with frame numbers and exact fields.
5. Cross-check of at least two Python observations against Wireshark evidence.
6. GenAI-assisted analysis with prompt(s), response summary, and verified claims.
7. GenAI reflection: confidence before/after, challenge/follow-up, Accept/Modify/Reject, uncertainty, and evidence seeking.
8. Conclusion: 2-4 sentences on network evidence and responsible AI use.

## What to submit

Upload one ZIP named:

`NML-Gxxx_Exercise1.zip`

It must contain:

- `main.py`
- completed `network_explorer/`
- `tests/` with starter and required additional tests
- `results/measurements.json`
- completed `results/genai_reflection.json`
- `README.md`
- `report.pdf` (2-4 pages)
- `capture.pcapng` or clearly identified fallback PCAP
- `packets.csv`
- readable Wireshark evidence image
- GenAI prompt(s) and relevant answer(s), in the report appendix or separate PDF/screenshots

Do not include passwords, personal data, virtual environments, `__pycache__`, system files, or unrelated traffic/files.

## Grading - 100 points

| Criterion | Points |
|---|---:|
| Python discovery + safe integration | 10 |
| Ping / RTT / packet loss | 10 |
| Traceroute | 10 |
| Delay model | 10 |
| Tests + JSON + program summary | 15 |
| Wireshark packet analysis | 15 |
| Layering + Python/Wireshark cross-check | 10 |
| GenAI verification + GenAI reflection | 15 |
| Submission quality | 5 |
| **Total** | **100** |

## Pre-submission checklist

- [ ] We used the supplied starter ZIP and completed all required Python TODOs.
- [ ] No required function remains as `NotImplementedError`.
- [ ] All starter tests and our added tests pass.
- [ ] `measurements.json` contains real structured results.
- [ ] We completed the manual Wireshark checkpoint before asking GenAI the same questions.
- [ ] Our report cites packet/frame numbers and exact fields for networking claims.
- [ ] `capture.pcapng` (or fallback PCAP) and `packets.csv` are included.
- [ ] We compared Python observations with Wireshark evidence.
- [ ] We verified at least two AI technical claims.
- [ ] We recorded initial/final confidence and Accept/Modify/Reject decisions.
- [ ] `genai_reflection.json` is complete and uses only the group ID.
- [ ] We identified uncertainty and any additional evidence needed.
- [ ] We did not include passwords, personal data, virtual environments, `__pycache__`, or unrelated traffic/files.
- [ ] All group members and student IDs are listed in the report.
- [ ] Only one group member will upload `NML-Gxxx_Exercise1.zip`.
