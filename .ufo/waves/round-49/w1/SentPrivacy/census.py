#!/usr/bin/env python3
"""census.py - what the live round-49 tree carries vs what the gate sees.

Read-only.  Prints per-class counts and gate rule ids only: no path, no value,
no account name is ever written to stdout.  Home paths are reported as a shape
(``/home/U/...``) and the account name as a bare count.
"""

import importlib.util
import json
import os
import re
import sys

GATE = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/check-session-material.py"
TREE = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-49"
EXTRA = ["tools/mado-keysym.py",
         "corpus/knowledge/hyprland-bind-key-match-r49.md",
         "quality/counters/c2-r49-bind-entry.py",
         "quality/counters/c1-r49-keysym.py"]
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"

spec = importlib.util.spec_from_file_location("csm", GATE)
csm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csm)

ACCOUNT = os.path.basename(os.path.expanduser("~"))
HOME_PATH = re.compile(r"/home/[A-Za-z0-9._-]+")
TILDE = re.compile(r"~/")
BIND_OBJ = re.compile(r'"(?:description|arg|dispatcher)"\s*:')
DEVICE_OBJ = re.compile(r'"address"\s*:')
KEYMAP = re.compile(r"xkb_keymap\s*\{")
OWNER_ROW = re.compile(r"^-[-dlbcps][rwxsStT-]{9}[+.]?\s+\d+\s+\S+\s+\S+\s")
SS_ROW = re.compile(r"users:\(\(")
CLIENT_TITLE = re.compile(r'"initialTitle"\s*:|"title"\s*:')


def walk(root):
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            yield os.path.join(dirpath, name)


def text_of(path):
    try:
        with open(path, "rb") as fh:
            data = fh.read(32 << 20)
    except OSError:
        return None
    return csm.decode(data)


def main():
    files = list(walk(TREE))
    for rel in EXTRA:
        p = os.path.join(LANE, rel)
        if os.path.exists(p):
            files.append(p)
    rows = []
    tot = {"files": 0, "home_path_files": 0, "home_path_lines": 0,
           "distinct_home_paths": 0, "tilde_files": 0, "tilde_lines": 0,
           "bind_obj_files": 0, "device_obj_files": 0, "keymap_files": 0,
           "owner_row_files": 0, "account_hits": 0,
           "gate_files": 0, "gate_findings": 0}
    rule_tally = {"R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0}
    distinct = set()
    for path in files:
        text = text_of(path)
        if text is None:
            continue
        tot["files"] += 1
        rel = os.path.relpath(path, LANE)
        hits = csm.scan_blob(text.encode("utf-8", "replace"), 10)
        if hits:
            tot["gate_files"] += 1
            tot["gate_findings"] += len(hits)
            for rule, _c, _d in hits:
                rule_tally[rule[:2]] += 1
        home_lines = [ln for ln in text.splitlines() if HOME_PATH.search(ln)]
        if home_lines:
            tot["home_path_files"] += 1
            tot["home_path_lines"] += len(home_lines)
            for ln in home_lines:
                distinct.add(HOME_PATH.search(ln).group(0))
        tilde_lines = [ln for ln in text.splitlines() if TILDE.search(ln)]
        if tilde_lines:
            tot["tilde_files"] += 1
            tot["tilde_lines"] += len(tilde_lines)
        if BIND_OBJ.search(text):
            tot["bind_obj_files"] += 1
        if DEVICE_OBJ.search(text):
            tot["device_obj_files"] += 1
        if KEYMAP.search(text):
            tot["keymap_files"] += 1
        if any(OWNER_ROW.match(ln) for ln in text.splitlines()):
            tot["owner_row_files"] += 1
        tot["account_hits"] += text.count(ACCOUNT) if len(ACCOUNT) > 2 else 0
        cls = ",".join(sorted({r[:2] for r, _c, _d in hits})) or "-"
        if home_lines or tilde_lines or hits:
            rows.append({"file": rel, "bytes": len(text), "home_lines": len(home_lines),
                         "tilde_lines": len(tilde_lines), "gate": cls})
    tot["distinct_home_paths"] = len(distinct)
    out = {"tree": TREE, "account_name_hits": tot.pop("account_hits"),
           "totals": tot, "rule_tally_by_file": rule_tally, "per_file": rows}
    print(json.dumps({k: out[k] for k in ("totals", "rule_tally_by_file",
                                          "account_name_hits")}, indent=2))
    print("files_with_home_or_tilde_or_finding:")
    for r in rows:
        print("  %-70s bytes=%-7d home_lines=%-3d tilde_lines=%-3d gate=%s"
              % (r["file"], r["bytes"], r["home_lines"], r["tilde_lines"], r["gate"]))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "census.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
