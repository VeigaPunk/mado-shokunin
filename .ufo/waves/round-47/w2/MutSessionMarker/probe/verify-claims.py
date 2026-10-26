#!/usr/bin/env python3
"""MutSessionMarker: assert every number quoted in the report against the
receipts. Usage: python3 -I probe/verify-claims.py <seat-dir>"""
import os
import sys

SEAT = sys.argv[1]
R = os.path.join(SEAT, "receipts")
RAW = os.path.join(R, "raw")
GATE_SHA = "a4a0a084e745f511048d5be445bed4959a18b5d64798a55da06c74cc0d08e9c9"
C00 = ".ufo/waves/round-45/w1/RevengerOmarchy/fixtures/w/C00_shipped/mons.json"
PR = ".ufo/waves/round-47/w2/MutScratch/planted"
FR = ".ufo/waves/round-47/w2/MutScratch/fixtures"


def must(path, needle):
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    if needle not in text:
        raise SystemExit("missing %r in %s" % (needle, path))
    return text


def must_raw(name, needle):
    return must(os.path.join(RAW, name), needle)


# 0: gate sha pinned before and after restoration
t = must(os.path.join(R, "00-gate-pristine-sha.txt"), GATE_SHA)
assert t.count(GATE_SHA) == 2, "gate sha should appear twice (before/after)"

# 1: selftest
must(os.path.join(R, "01-selftest.txt"), "SELFTEST: passed=63/63 failed=0")

# 2: pristine battery summary + per-state PASS
b = must(os.path.join(R, "02-pristine-battery.txt"), "DETECTOR PASS passed=6 failed=0")
for case in ("S0-base", "S1-unmarked", "S2a-cleanwaive", "S2b-tampered",
             "S34-realcontent", "S5-proseserial"):
    must(os.path.join(R, "02-pristine-battery.txt"), "CASE %s PASS" % case)

# per-state raw receipts
must_raw("S0-base.txt",
         "SESSION_MATERIAL_RULES: R1_CLIENT_DUMP=29 R2_PROC_TABLE=31 "
         "R3_MONITOR_IDENT=53 R4_HOME_LISTING=2 R5_SERIAL_PROSE=21")
must_raw("S0-base.txt", "SESSION_MATERIAL: files=18371 findings=136")
must_raw("S1-unmarked.txt",
         "FINDING file=%s/clients-live.json rule=R1_CLIENT_DUMP count=2 " % PR)
must_raw("S1-unmarked.txt",
         "FINDING file=%s/proc-table.txt rule=R2_PROC_TABLE count=2 " % PR)
must_raw("S1-unmarked.txt",
         "FINDING file=%s/monitors-live.json rule=R3_MONITOR_IDENT count=1 " % PR)
must_raw("S1-unmarked.txt", "SESSION_MATERIAL: files=18374 findings=139")
must_raw("S2a-cleanwaive.txt",
         "WAIVER file=%s rule=R3_MONITOR_IDENT kind=fixture" % C00)
must_raw("S2a-cleanwaive.txt", "SESSION_MATERIAL_WAIVED: findings=1 files=1")
must_raw("S2a-cleanwaive.txt", "SESSION_MATERIAL: files=18375 findings=138")
must_raw("S2b-tampered.txt",
         "WAIVER_REJECTED file=%s rule=R3_MONITOR_IDENT reason=sha-mismatch" % C00)
must_raw("S2b-tampered.txt",
         "FINDING file=%s rule=R3_MONITOR_IDENT count=2 " % C00)
must_raw("S2b-tampered.txt", "SESSION_MATERIAL: files=18375 findings=139")
must_raw("S34-realcontent.txt",
         "WAIVER_REJECTED file=%s/real-content.json rule=R1_CLIENT_DUMP "
         "reason=value-not-synthetic:title-not-synthetic" % FR)
must_raw("S34-realcontent.txt",
         "WAIVER_REJECTED file=%s/real-content.json rule=R2_PROC_TABLE "
         "reason=value-not-synthetic:program-not-synthetic" % FR)
must_raw("S34-realcontent.txt",
         "WAIVER_REJECTED file=%s/real-content.json rule=R3_MONITOR_IDENT "
         "reason=value-not-synthetic:serial-not-synthetic" % FR)
must_raw("S34-realcontent.txt",
         "WAIVER_REJECTED file=%s/not-a-gate-copy.json rule=R1_CLIENT_DUMP "
         "reason=gate-source-mismatch" % FR)
must_raw("S34-realcontent.txt",
         "FINDING file=%s/real-content.json rule=R2_PROC_TABLE count=2 " % FR)
must_raw("S34-realcontent.txt", "SESSION_MATERIAL: files=18379 findings=143")
must_raw("S5-proseserial.txt",
         "WAIVER_REJECTED file=%s/prose-serial.md rule=R5_SERIAL_PROSE "
         "reason=serial-rule-not-waivable" % FR)
must_raw("S5-proseserial.txt",
         "FINDING file=%s/prose-serial.md rule=R5_SERIAL_PROSE count=1 " % FR)
must_raw("S5-proseserial.txt", "SESSION_MATERIAL: files=18381 findings=144")

# 3: M1 killed
m1 = must(os.path.join(R, "03-mutant-M1.txt"), "DETECTOR FAIL passed=1 failed=3")
for case in ("S2b-tampered", "S34-realcontent", "S5-proseserial"):
    must(os.path.join(R, "03-mutant-M1.txt"), "CASE %s FAIL" % case)
must_raw("m1-S2b-tampered.txt",
         "WAIVER file=%s rule=R3_MONITOR_IDENT kind=fixture" % C00)
must_raw("m1-S34-realcontent.txt",
         "WAIVER file=%s/real-content.json rule=R1_CLIENT_DUMP kind=fixture" % FR)
must_raw("m1-S5-proseserial.txt",
         "WAIVER file=%s/prose-serial.md rule=R5_SERIAL_PROSE kind=fixture" % FR)

# 4: M2 killed
m2 = must(os.path.join(R, "04-mutant-M2.txt"), "DETECTOR FAIL passed=1 failed=4")
for case in ("S2a-cleanwaive", "S2b-tampered", "S34-realcontent", "S5-proseserial"):
    must(os.path.join(R, "04-mutant-M2.txt"), "CASE %s FAIL" % case)
def must_not_raw(name, needle):
    with open(os.path.join(RAW, name), encoding="utf-8") as handle:
        text = handle.read()
    if needle in text:
        raise SystemExit("unexpected %r in %s" % (needle, name))

must_not_raw("m2-S2a-cleanwaive.txt", "WAIVER file=")
must_not_raw("m2-S2a-cleanwaive.txt", "SESSION_MATERIAL_WAIVED:")
must_not_raw("m2-S2a-cleanwaive.txt",
             "WAIVER_REJECTED file=%s rule=R3_MONITOR_IDENT" % C00)
must_not_raw("m2-S34-realcontent.txt",
             "WAIVER_REJECTED file=%s/real-content.json rule=R3_MONITOR_IDENT" % FR)
must_not_raw("m2-S34-realcontent.txt",
             "FINDING file=%s/real-content.json rule=R3_MONITOR_IDENT" % FR)
must_raw("m2-S1-unmarked.txt",
         "FINDING file=%s/monitors-live.json rule=R3_MONITOR_IDENT count=1 " % PR)

# 5: restoration parity
p = must(os.path.join(R, "05-restored-parity.txt"), "DETECTOR PASS passed=2 failed=0")
for case in ("S2b-tampered", "S34-realcontent"):
    must(os.path.join(R, "05-restored-parity.txt"), "CASE %s PASS" % case)

print("CLAIMS_CHECK passed")
