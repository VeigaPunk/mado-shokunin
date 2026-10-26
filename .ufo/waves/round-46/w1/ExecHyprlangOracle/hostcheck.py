#!/usr/bin/env python3
"""Cross-check the oracle against the lane's live host receipt (receipts/live-devices-host-l1.txt).

Extracts the device names and the reference's per-keyboard expected names from the receipt, runs the oracle on
~/.config/hypr/input.conf for those names and diffs the two. Read-only: it reads the config file and the receipt.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
RECEIPT = os.path.join(LANE, ".ufo/waves/round-46/receipts/live-devices-host-l1.txt")
CONF = os.path.expanduser("~/.config/hypr/input.conf")
NAMES = ("layout", "variant", "options", "model", "rules")


def main():
    root, oracle = sys.argv[1], sys.argv[2]
    os.makedirs(root, exist_ok=True)
    rows = []
    for line in open(RECEIPT, encoding="utf-8"):
        m = re.match(r'MADO_DEV_KEYBOARD: name=("[^"]*") block=(\w+) (.*?) kb_file=(-|\S+) differ=(\S+) verdict=(\w+)', line)
        if m:
            fields = dict(re.findall(r'(\w+)="((?:[^"\\]|\\.)*)"', m.group(3)))
            rows.append({"name": json.loads(m.group(1)), "expected": [json.loads('"%s"' % fields[n]) for n in NAMES],
                         "verdict": m.group(6)})
    for line in open(RECEIPT, encoding="utf-8"):
        m = re.match(r'MADO_DEV_MOUSE: name=("[^"]*") block=(\w+) scroll_factor=(-?[0-9.]+)', line)
        if m:
            rows.append({"name": json.loads(m.group(1)), "mouse": True, "expected_sf": m.group(3)})
    manifest = os.path.join(root, "manifest.txt")
    with open(manifest, "w", encoding="utf-8") as fh:
        fh.write("CASE host %d %d\n%s\n" % (1, len(rows), CONF))
        for r in rows:
            fh.write(r["name"] + "\n")
    out = subprocess.run([oracle, "--manifest", manifest], capture_output=True, text=True, check=True).stdout
    got = {}
    for line in out.splitlines():
        if line.startswith("{"):
            o = json.loads(line)
            if "name" in o:
                got[o["name"]] = o
    bad = 0
    for r in rows:
        o = got[r["name"]]
        if "mouse" in r:
            ok = o["sf"] == r["expected_sf"]
            print("%-8s %-52s reference scrollFactor=%-7s oracle=%s  %s" % (
                "MOUSE", r["name"], r["expected_sf"], o["sf"], "AGREE" if ok else "DIFFER"))
            bad += 0 if ok else 1
        else:
            mine = [o[n] for n in NAMES]
            ok = mine == r["expected"]
            print("%-8s %-52s reference=%s oracle=%s  %s" % (
                "KEYBOARD", r["name"], r["expected"], mine, "AGREE" if ok else "DIFFER"))
            bad += 0 if ok else 1
    print("MADO_HOSTCHECK: devices=%d agree=%d differ=%d config=%s" % (len(rows), len(rows) - bad, bad, CONF))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
