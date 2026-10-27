#!/usr/bin/env python3
"""verify-claims.py — assert every number in the round-48 seat report against its receipt.

Usage: verify-claims.py <seat-dir> <report.md>
Prints CLAIMS_CHECK passed=N failed=M and one FAIL line per mismatch. Writes nothing.
"""
import sys

CHECKS = [
    # (label, receipt file, exact substring, 1-based line or None)
    ("selftest-69", "00-selftest.txt", "SELFTEST: passed=69/69 failed=0", None),
    ("title-sweep-counts", "00a-title-sweep.txt", "old_pass=2 new_pass=0 lost=2", None),
    ("title-sweep-31", "00a-title-sweep.txt", "files_with_r1=31 values=123", None),
    ("title-family", "00b-title-families.txt", "prefix:example+case", None),
    ("base-128", "01-old-gate-at-base.txt",
     "findings=128 rev=579f694b45c797a9c39761fdb4f9e0a1b71b3585", 131),
    ("v2-149", "02-v2-nomarkers.txt",
     "findings=149 rev=108cce5ea4d0c29f273d0df2dbbeba6188781b38", 152),
    ("triage-passb", "03-triage.txt", "pass-b rc=1 waived=49 rejected=2 kept=100", None),
    ("waived-49-47", "04-with-markers.txt", "SESSION_MATERIAL_WAIVED: findings=49 files=47", 154),
    ("install-100", "04-with-markers.txt",
     "findings=100 rev=0fb5340bbba1ba846418d649d24d9ec74c853ec3", 155),
    ("parity-149", "05-no-waivers.txt",
     "findings=149 rev=0fb5340bbba1ba846418d649d24d9ec74c853ec3", 152),
    ("b-unmarked-finding", "06-b-unmarked.txt",
     "FINDING file=.ufo/waves/round-48/w1/ExecSessionMarker/fixtures/synthetic-clients.json"
     " rule=R1_CLIENT_DUMP count=1", 153),
    ("b-count-101", "06-b-unmarked.txt", "findings=101 rev=57453730066c80539bb5a6d288baed5a5f6a2bea", 156),
    ("a-waiver", "07-a-marked.txt",
     "WAIVER file=.ufo/waves/round-48/w1/ExecSessionMarker/fixtures/synthetic-clients.json"
     " rule=R1_CLIENT_DUMP kind=fixture", 51),
    ("a-count-100", "07-a-marked.txt", "findings=100 rev=76e2e24c489cc43552ed2f954d3d16c3ac570d67", 156),
    ("c-path-reject", "08-c-forged-nonfixture.txt",
     "reason=path-outside-waves", 52),
    ("c-still-counted", "08-c-forged-nonfixture.txt",
     "FINDING file=.ufo/reports/session-clients.json rule=R1_CLIENT_DUMP count=1", 55),
    ("c-count-101", "08-c-forged-nonfixture.txt",
     "findings=101 rev=99d2d3a90f5f9da52f093bcd6d44e9b216f1f5b6", 158),
    ("c2-value-reject", "09-c2-value-not-synthetic.txt",
     "reason=value-not-synthetic:title-not-synthetic", 55),
    ("c2-count-102", "09-c2-value-not-synthetic.txt",
     "findings=102 rev=75a5359b30ec7a510f1528c3aaf634750d099dc1", 160),
    ("f1-draft-waives", "10-f1-control-draft-waives.txt",
     "WAIVER file=.ufo/waves/round-48/w1/ExecSessionMarker/fixtures/forged-real.json"
     " rule=R1_CLIENT_DUMP kind=fixture", 51),
    ("verify-installed", "11-verify-install.txt", "installed sidecars=48", None),
    ("verify-100", "11-verify-install.txt",
     "findings=100 rev=68b834eea5670106e1b5a04534564d854d5ca7d9", 158),
    ("landed-waived", "12-as-landed.txt", "SESSION_MATERIAL_WAIVED: findings=52 files=48", 156),
    ("landed-100", "12-as-landed.txt",
     "findings=100 rev=7031e3839e95c8e0111108d5e15a05eb0209427e", 157),
    ("seat-scan", "13-seatdir-scan.txt", "r5_tokens=0 r4_files=0", None),
]


def main(argv):
    seat, report = argv[1], argv[2]
    passed = failed = 0
    for label, name, needle, line_no in CHECKS:
        with open("%s/receipts/%s" % (seat, name), encoding="utf-8", errors="replace") as handle:
            lines = handle.read().splitlines()
        ok = False
        if line_no is None:
            ok = any(needle in line for line in lines)
        else:
            ok = 0 < line_no <= len(lines) and needle in lines[line_no - 1]
        if ok:
            passed += 1
            print("CLAIM ok %s (%s:%s)" % (label, name, line_no or "-"))
        else:
            failed += 1
            print("CLAIM FAIL %s (%s:%s) expected %r" % (label, name, line_no or "-", needle))
    with open(report, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    for needle in ("passed=69/69", "findings=128", "findings=149", "findings=100",
                   "5745373", "75a5359b", "99d2d3a9", "findings=52 files=48",
                   "value-not-synthetic:title-not-synthetic", "path-outside-waves"):
        if needle in text:
            passed += 1
            print("CLAIM ok report-mentions %r" % needle)
        else:
            failed += 1
            print("CLAIM FAIL report-mentions %r" % needle)
    print("CLAIMS_CHECK passed=%d failed=%d" % (passed, failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
