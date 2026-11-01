#!/usr/bin/env python3
"""dwm-crosscheck.py — run the round-62 probe once and the tool once, then
compare the five STABLE fields (census counters churn with desktop activity,
so they are crosschecked only for structural sanity, never for equality).
Exit 0 = all five AGREE; 1 = any DISAGREE."""
import json
import subprocess
import sys

REPO = sys.argv[1]
PS = REPO + "/.ufo/waves/round-62/receipts/dwm-attributes-probe.ps1"
TOOL = REPO + "/tools/mado-win-dwm.py"

probe = subprocess.run(
    ["powershell.exe", "-NoProfile", "-NonInteractive", "-NoLogo",
     "-ExecutionPolicy", "Bypass", "-File", PS],
    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    timeout=120, check=False)
tool = subprocess.run(
    [sys.executable, TOOL],
    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    timeout=120, check=False)

if probe.returncode != 0 or tool.returncode != 0:
    print(f"PROBE_RC={probe.returncode} TOOL_RC={tool.returncode}")
    sys.exit(1)

doc = json.loads(probe.stdout.decode("utf-8"))
verdict, jsonline = tool.stdout.decode("utf-8").splitlines()[0], tool.stdout.decode("utf-8").splitlines()[1]
clean = json.loads(jsonline)

checks = [
    ("composition_enabled", doc["composition_enabled"], clean["composition_enabled"]),
    ("composition_hr", doc["composition_hr"], clean["composition_hr"]),
    ("own_window.source", doc["own_window"]["source"], clean["own_window"]["source"]),
    ("timing.ok", doc["timing"]["ok"], clean["timing"]["ok"]),
    ("timing.hr", doc["timing"]["hr"], clean["timing"]["hr"]),
]
agree = 0
for name, a, b in checks:
    ok = a == b
    agree += ok
    print(f"{'AGREE' if ok else 'DISAGREE'} {name}: probe={a!r} tool={b!r}")
# structural sanity on the churn-prone census (no equality claim)
struct = (
    clean["windows"]["top_level"] >= 1
    and clean["windows"]["cloaked"] <= clean["windows"]["top_level"]
    and clean["windows"]["cloak_app"] + clean["windows"]["cloak_shell"]
        + clean["windows"]["cloak_inherited"] == clean["windows"]["cloaked"]
)
print(f"{'AGREE' if struct else 'DISAGREE'} census_structure: probe_top={doc['windows']['top_level']} tool_top={clean['windows']['top_level']} (churn-prone, structure only)")
print(f"CROSSCHECK: {agree}/5 stable fields AGREE" + ("" if struct else " + census structure DISAGREE"))
sys.exit(0 if agree == 5 and struct else 1)
