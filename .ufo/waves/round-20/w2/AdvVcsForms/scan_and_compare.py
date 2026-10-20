#!/usr/bin/env python3
"""Scan each AdvVcsForms fixture with the repaired tool; compare to ground truth."""
import json, os, subprocess, sys

TOOL = "/tmp/mado-r20w2-AdvVcsForms/tools/mado-tripwire.py"
DIR = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-20/w2/AdvVcsForms/fixtures"

manifest = {c["case"]: c for c in json.load(open(os.path.join(DIR, "manifest.json")))}
rows = []
for name in sorted(manifest):
    path = os.path.join(DIR, name + ".jsonl")
    p = subprocess.run([sys.executable, "-I", TOOL, "--scan", path],
                       capture_output=True, text=True)
    # second line is the JSON payload
    payload = json.loads(p.stdout.splitlines()[1])
    finds = [(f["class"], f["rule"], f["evidence"]) for f in payload["findings"]]
    truth = manifest[name]["truth"]
    write_found = any(c == "vcs_write" for c, _, _ in finds)
    if truth == "write":
        verdict = "OK-write" if write_found else "FN-miss"
    elif truth == "nowrite":
        verdict = "FP-flagged" if write_found else "OK-clean"
    else:
        verdict = "boundary-write" if write_found else "boundary-clean"
    rows.append((name, truth, verdict, finds, p.returncode))
for r in rows:
    print("%-36s truth=%-8s %-14s rc=%s %s" % (r[0], r[1], r[2], r[4], r[3]))
bad = [r for r in rows if r[2].startswith("FP") or r[2].startswith("FN")]
print("\nDIVERGENCES:", len(bad))
for r in bad:
    print(" ", r[0], r[1], r[2], r[3])
