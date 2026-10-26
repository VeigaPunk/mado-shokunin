#!/usr/bin/env python3
"""check-fragments.py — every verdict fragment the round-47 w1 ledger DISPLAYS, tested
verbatim against the locator the same row names (and, failing that, against the whole file).

Read-only: opens the lane files named in FRAGMENTS, writes nothing. Run from anywhere:
    python3 -I check-fragments.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin
Exit 0 always; the point is the line-per-fragment report.
"""
import argparse
import os
import sys

# (row, locator "path:line", fragment as displayed in ledger.md, note)
FRAGMENTS = [
    ("mado-eventq.py", ".ufo/waves/round-38/receipts/eventq-live.txt:8",
     "subscribers=2 overflow=0 write_fail=0 markers_observable=no", "ledger row 2a"),
    ("mado-eventq.py", ".ufo/waves/round-38/receipts/eventq-live.txt:8", "CLEAN", ""),
    ("mado-options.py", ".ufo/waves/round-40/fetch/census-receipt.txt:7",
     "agreement=62 agreement*=8 mismatch=0 config-only=0 live-default=0", ""),
    ("mado-geometry.py", ".ufo/waves/round-44/receipts/live-geometry-host-r44.txt:5",
     "rules=1 clients=3 matched=0 differ=0", ""),
    ("mado-geometry.py", ".ufo/waves/round-44/receipts/live-geometry-host-r44.txt:5",
     "NO_MATCHING_CLIENT", ""),
    ("mado-monitors.py", ".ufo/waves/round-45/receipts/live-monitors-host-r45.txt:8",
     "outputs=1 matched=1 agree=1 differ=0", ""),
    ("mado-monitors.py", ".ufo/waves/round-45/receipts/live-monitors-host-r45.txt:8", "OK", ""),
    ("mado-devices.py", ".ufo/waves/round-46/receipts/live-devices-host-r46.txt:21",
     "keyboards=10 agree=9 virtual=1 mice=4 mice_differ=0 differ=0", ""),
    ("mado-devices.py", ".ufo/waves/round-46/receipts/live-devices-host-r46.txt:21", "OK", ""),
    ("mado-verify.sh", ".ufo/evidence/round-12/after.txt:80",
     "CLEAN (52 pass, 8 notes; file + live planes verified read-only)", ""),
    ("mado-tripwire.py", ".ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt:6",
     "findings", ""),
    ("mado-tripwire.py", ".ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt:6",
     "live_probe 3, vcs_write 164", "row locates the counts at :6"),
    ("mado-binds.py", ".ufo/waves/round-25/evidence/c1-after-v4-ef94763c.txt:5",
     "live=hyprctl binds -j sha256:9a47199e", "displayed with an ellipsis; prefix tested"),
    ("mado-binds.py", ".ufo/waves/round-25/evidence/c1-after-v4-ef94763c.txt:7",
     "ORACLE_CHECK base_vs_live missing=0 extra=0", ""),
    ("mado-binds.py", ".ufo/waves/round-25/evidence/c1-after-v4-ef94763c.txt:50",
     "cases_pass=41/41 verdict=TARGET_MET", ""),
    ("mado-anims.py", ".ufo/waves/round-26/evidence/c1-after-v2-2b3487f7.txt:4",
     "CASES 41/41", "verdict column"),
    ("mado-anims.py", ".ufo/waves/round-26/evidence/c1-after-v2-2b3487f7.txt:7",
     "ORACLE_CHECK base_twice equal nodes=35 beziers=6", ""),
    ("mado-anims.py", ".ufo/waves/round-26/evidence/c1-after-v2-2b3487f7.txt:51",
     "TARGET_MET", ""),
    ("mado-wsrules.py", ".ufo/waves/round-27/evidence/c1-after-20022a65.txt:49",
     "cases_pass=41/41 TARGET_MET", "verdict column; locator computed by grep"),
    ("mado-wsrules.py", ".ufo/waves/round-27/evidence/c1-after-20022a65.txt:6",
     "ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2", ""),
    ("mado-action-plan.py", ".ufo/waves/round-46/w1/ExecHarmBase/receipts/base-registered-gates.txt:2",
     "MADO_PLAN: frozen_match", ""),
]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    a = ap.parse_args(argv)
    bad = 0
    for row, loc, frag, note in FRAGMENTS:
        path, _, lineno = loc.rpartition(":")
        full = os.path.join(a.repo, path)
        try:
            lines = open(full, encoding="utf-8", errors="replace").read().splitlines()
        except OSError as e:
            print("UNREADABLE %-20s %s (%s)" % (row, loc, e))
            bad += 1
            continue
        n = int(lineno)
        line = lines[n - 1] if 0 < n <= len(lines) else ""
        whole = "\n".join(lines)
        if frag in line:
            print("VERBATIM  %-20s %s  %r" % (row, loc, frag))
        elif frag in whole:
            hits = [i + 1 for i, l in enumerate(lines) if frag in l]
            print("ELSEWHERE %-20s %s  %r  (fragment is on line(s) %s, not %d)"
                  % (row, loc, frag, hits, n))
            bad += 1
        else:
            print("ABSENT    %-20s %s  %r  (nowhere in the receipt)%s"
                  % (row, loc, frag, "  [" + note + "]" if note else ""))
            bad += 1
    print("FRAGMENTS total=%d not_verbatim_at_locator=%d" % (len(FRAGMENTS), bad))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
