#!/usr/bin/env python3
"""verify-claims.py — assert every number ExecSessionMarker.md quotes.

Not part of the gate. Reads the receipts this seat produced and checks the
exact strings the report relies on, plus the shape of the install set. Prints
``CHECK ok|FAIL`` lines and a final ``CLAIMS_CHECK`` line; exit 1 on any
failure. No value from the host dump is ever read here.

Usage::

    verify-claims.py --seat <seat dir> [--receipts <dir>]
"""

import argparse
import os
import sys

CHECKS = [
    ("00-selftest.txt", "SELFTEST: passed=63/63 failed=0", "selftest 63/63"),
    ("01-baseline.txt", "SESSION_MATERIAL: files=18371 findings=115", "baseline findings=115"),
    ("01-baseline.txt", "R1_CLIENT_DUMP=29 R2_PROC_TABLE=31 R3_MONITOR_IDENT=53 R4_HOME_LISTING=2",
     "baseline per-rule tally"),
    ("01-baseline.txt", "EXIT rc=1", "baseline exit 1"),
    ("02-new-gate-no-markers.txt", "SESSION_MATERIAL: files=18371 findings=136", "gate findings=136"),
    ("02-new-gate-no-markers.txt", "R5_SERIAL_PROSE=21", "21 prose serials under .ufo/"),
    ("03-triage.txt", "pass-a rc=1 waived=52 rejected=63 kept=84", "as-is pass A counts"),
    ("04-with-markers.txt", "SESSION_MATERIAL_WAIVED: findings=52 files=48", "as-is waived"),
    ("04-with-markers.txt", "SESSION_MATERIAL: files=18419 findings=84", "as-is remaining"),
    ("05-planted-real-dump.txt", "SESSION_MATERIAL: files=18420 findings=86", "planted dump adds two"),
    ("05-planted-real-dump.txt", "PlantedSeat/live-monitors.json rule=R3_MONITOR_IDENT count=1",
     "planted dump R3"),
    ("05-planted-real-dump.txt", "PlantedSeat/live-monitors.json rule=R5_SERIAL_PROSE count=2",
     "planted dump R5"),
    ("06-real-dump-in-marked-file.txt", "SESSION_MATERIAL: files=18420 findings=88",
     "appended dump adds two"),
    ("06-real-dump-in-marked-file.txt", "SESSION_MATERIAL_WAIVED: findings=51 files=47",
     "the waiver is lost"),
    ("06-real-dump-in-marked-file.txt", "reason=sha-mismatch", "appending voids the marker"),
    ("06-real-dump-in-marked-file.txt",
     "C00_shipped/mons.json rule=R3_MONITOR_IDENT count=2", "the finding returns"),
    ("07-registry-names-real-serial.txt", "SESSION_MATERIAL: files=18421 findings=111",
     "registered real serial keeps its findings"),
    ("07-registry-names-real-serial.txt",
     "PlantedSeat/live-monitors.json rule=R3_MONITOR_IDENT reason=value-not-synthetic:serial-not-synthetic",
     "W4b refuses the real serial"),
    ("07-registry-names-real-serial.txt",
     "PlantedSeat/live-monitors.json rule=R5_SERIAL_PROSE reason=serial-rule-not-waivable",
     "R5 never waivable"),
    ("07-registry-names-real-serial.txt",
     "PlantedSeat/live-monitors.json rule=R6_SERIAL_EXACT reason=serial-rule-not-waivable",
     "R6 never waivable"),
    ("08-r6-exact-host-serial.txt", "R6_SERIAL_EXACT=23", "exact-value rule counts 23"),
    ("09-triage-refreshed-copies.txt", "pass-a rc=1 waived=61 rejected=57 kept=78",
     "refreshed-copies pass A counts"),
    ("10-refreshed-with-markers.txt", "SESSION_MATERIAL_WAIVED: findings=61 files=51",
     "refreshed waived"),
    ("10-refreshed-with-markers.txt", "findings=78", "refreshed remaining"),
    ("12-triage-seat-tree.txt", "pass-a rc=1 waived=55 rejected=63 kept=84",
     "seat-tree pass A counts"),
    ("12-triage-seat-tree.txt", "remaining class=real:identity:program-not-synthetic count=27",
     "class program 27"),
    ("12-triage-seat-tree.txt", "remaining class=real:identity:title-not-synthetic count=24",
     "class title 24"),
    ("12-triage-seat-tree.txt", "remaining class=real:identity:serial-not-synthetic count=3",
     "class serial 3"),
    ("12-triage-seat-tree.txt", "remaining class=real:identity:home-user-not-synthetic count=2",
     "class home-user 2"),
    ("12-triage-seat-tree.txt", "remaining class=real:identity:vendor-not-synthetic count=1",
     "class vendor 1"),
    ("12-triage-seat-tree.txt", "remaining class=real:serial count=21", "class prose serial 21"),
    ("12-triage-seat-tree.txt", "remaining class=synthetic:stale-gate-copy count=6",
     "class stale gate copy 6"),
    ("12a-seat-tree-no-markers.txt", "findings=139", "seat tree without markers=139"),
    ("13-seat-tree-with-markers.txt", "SESSION_MATERIAL_WAIVED: findings=55 files=49",
     "install-set waived"),
    ("13-seat-tree-with-markers.txt", "findings=84", "install-set remaining"),
    ("13-seat-tree-with-markers.txt", "EXIT rc=1", "install-set exit 1"),
    ("15-no-waivers-parity.txt", "PARITY ok", "--no-waivers parity"),
    ("16-scope-all.txt", "findings=92", "scope all findings=92"),
    ("16-scope-all.txt", "R5_SERIAL_PROSE=24", "scope all serials=24"),
    ("11-seat-scan.txt", "values=4 hits=0", "seat holds no host value"),
]


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def main(argv=None):
    parser = argparse.ArgumentParser(prog="verify-claims.py")
    parser.add_argument("--seat", required=True)
    args = parser.parse_args(argv)
    seat = os.path.abspath(args.seat)
    receipts = os.path.join(seat, "receipts")

    passed = failed = 0
    for name, needle, label in CHECKS:
        text = read(os.path.join(receipts, name))
        ok = needle in text
        passed += 1 if ok else 0
        failed += 0 if ok else 1
        print("CHECK %s case=%s receipt=%s" % ("ok" if ok else "FAIL", label, name))

    registry = os.path.join(seat, "demo", "registry-round47.txt")
    refreshed = os.path.join(seat, "demo", "registry-round47-refreshed.txt")
    rows = [line for line in read(registry).splitlines() if line and not line.startswith("#")]
    rows_refreshed = [line for line in read(refreshed).splitlines()
                      if line and not line.startswith("#")]
    checks = [
        ("registry rows=49", len(rows) == 49, "rows=%d" % len(rows)),
        ("registry gate-copy rows=1",
         sum(1 for row in rows if row.endswith("kind=gate-copy")) == 1,
         "rows=%d" % sum(1 for row in rows if row.endswith("kind=gate-copy"))),
        ("refreshed registry rows=51", len(rows_refreshed) == 51, "rows=%d" % len(rows_refreshed)),
        ("refreshed superset",
         set(rows).issubset(set(rows_refreshed)), "missing=%d" % len(set(rows) - set(rows_refreshed))),
        ("refreshed-only rows have sidecars",
         all(_sidecar_sha(seat, row.split()[0]) == row.split()[1]
             for row in set(rows_refreshed) - set(rows)),
         "rows=%d" % len(set(rows_refreshed) - set(rows))),
        ("sidecars=49",
         len([p for p in _walk(os.path.join(seat, "demo", "sidecars"))
              if p.endswith(".synthetic")]) == 49,
         "files=%d" % len([p for p in _walk(os.path.join(seat, "demo", "sidecars"))
                           if p.endswith(".synthetic")])),
        ("sidecars-refreshed=2",
         len([p for p in _walk(os.path.join(seat, "demo", "sidecars-refreshed"))
              if p.endswith(".synthetic")]) == 2,
         "files=%d" % len([p for p in _walk(os.path.join(seat, "demo", "sidecars-refreshed"))
                           if p.endswith(".synthetic")])),
        ("every registry row has a sidecar",
         all(os.path.exists(os.path.join(seat, "demo", "sidecars", row.split()[0] + ".synthetic"))
             for row in rows),
         "rows=%d" % len(rows)),
        ("every sidecar's sha matches its row",
         all(_marker_sha(os.path.join(seat, "demo", "sidecars", row.split()[0] + ".synthetic"))
             == row.split()[1] for row in rows),
         "rows=%d" % len(rows)),
    ]
    for label, ok, detail in checks:
        passed += 1 if ok else 0
        failed += 0 if ok else 1
        print("CHECK %s case=%s %s" % ("ok" if ok else "FAIL", label, detail))

    print("CLAIMS_CHECK passed=%d failed=%d" % (passed, failed))
    return 0 if failed == 0 else 1


def _walk(root):
    for base, _dirs, files in os.walk(root):
        for name in files:
            yield os.path.join(base, name)


def _sidecar_sha(seat, relpath):
    for base in ("sidecars", "sidecars-refreshed"):
        path = os.path.join(seat, "demo", base, relpath + ".synthetic")
        if os.path.exists(path):
            return _marker_sha(path)
    return ""


def _marker_sha(path):
    first = read(path).splitlines()[0] if read(path) else ""
    for field in first.split():
        if field.startswith("sha256="):
            return field[len("sha256="):]
    return ""


if __name__ == "__main__":
    sys.exit(main())
