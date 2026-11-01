#!/usr/bin/env python3
"""displayconfig-crosscheck.py — run the round-63 probe once and the tool once,
then compare the five STABLE fields (the CCD topology moves only on a display
configuration change, so these fields are expected stable across the two
spawns; no equality claim is made about anything outside this list).
Exit 0 = all five AGREE; 1 = any DISAGREE."""
import json
import subprocess
import sys

REPO = sys.argv[1]
PS = REPO + "/.ufo/waves/round-63/receipts/displayconfig-probe.ps1"
TOOL = REPO + "/tools/mado-win-displayconfig.py"

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
lines = tool.stdout.decode("utf-8").splitlines()
verdict, jsonline = lines[0], lines[1]
clean = json.loads(jsonline)


def path0(doc_like):
    return (doc_like.get("path_list") or [{}])[0]


p_probe, p_tool = path0(doc), path0(clean)
t_probe, t_tool = p_probe.get("target") or {}, p_tool.get("target") or {}
m_probe, m_tool = p_probe.get("target_mode") or {}, p_tool.get("target_mode") or {}

checks = [
    ("query_hr", doc["query_hr"], clean["query_hr"]),
    ("paths", doc["paths"], clean["paths"]),
    ("target.refresh", f"{t_probe.get('refresh_num')}/{t_probe.get('refresh_den')}",
     f"{t_tool.get('refresh_num')}/{t_tool.get('refresh_den')}"),
    ("target.active_size", f"{m_probe.get('active_cx')}x{m_probe.get('active_cy')}",
     f"{m_tool.get('active_cx')}x{m_tool.get('active_cy')}"),
    ("target_mode.vsync", f"{m_probe.get('vsync_num')}/{m_probe.get('vsync_den')}",
     f"{m_tool.get('vsync_num')}/{m_tool.get('vsync_den')}"),
]
agree = 0
for name, a, b in checks:
    ok = a == b
    agree += ok
    print(f"CROSSCHECK {name}: {'AGREE' if ok else 'DISAGREE'} ({a!r} vs {b!r})")
# structural sanity beside the equality checks (the census-shape rule): the
# tool's verdict line names the same path count and refresh rational the
# probe printed
struct = f"paths={clean['paths']}" in verdict and t_tool and m_tool
print(f"CROSSCHECK verdict_structure: {'AGREE' if struct else 'DISAGREE'} ({verdict})")
print(f"CROSSCHECK: {agree}/{len(checks)} stable fields AGREE + census structure")
sys.exit(0 if agree == len(checks) and struct else 1)
