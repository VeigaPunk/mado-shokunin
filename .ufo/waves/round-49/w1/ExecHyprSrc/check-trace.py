#!/usr/bin/env python3
"""Cross-check every `| ID | file:line | quote |` row in trace.md against locators.json.

This is what makes the typed table numbers safe: each row must name the same
file, the same line and the same quote that locate.py computed from the pins.
Run: python3 check-trace.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROW = re.compile(r"^\|\s*([A-Z]\d\d)\s*\|\s*`([^`:]+):(\d+)`\s*\|\s*`(.+?)`\s*\|")


def main() -> int:
    recs = {r["id"]: r for r in json.loads((HERE / "locators.json").read_text(encoding="utf-8"))}
    text = (HERE / "trace.md").read_text(encoding="utf-8")
    seen = []
    fail = []
    for lineno, line in enumerate(text.splitlines(), 1):
        m = ROW.match(line)
        if not m:
            continue
        eid, fname, num, quote = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        seen.append(eid)
        rec = recs.get(eid)
        if rec is None:
            fail.append(f"trace.md:{lineno} {eid}: no such locator id")
            continue
        if rec["file"] != fname:
            fail.append(f"trace.md:{lineno} {eid}: file {fname} != {rec['file']}")
        if rec["line"] != num:
            fail.append(f"trace.md:{lineno} {eid}: line {num} != computed {rec['line']}")
        if rec["quote"] not in quote:
            fail.append(f"trace.md:{lineno} {eid}: quote differs from computed {rec['quote']!r}")
    missing = sorted(set(recs) - set(seen))
    for eid in missing:
        fail.append(f"{eid}: computed but not cited in trace.md")
    for f in fail:
        print("FAIL", f)
    print(f"TRACE_ROWS_CHECKED {len(seen)}/{len(recs)}")
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
