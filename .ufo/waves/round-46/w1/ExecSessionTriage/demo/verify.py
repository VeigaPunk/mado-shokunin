#!/usr/bin/env python3
"""Verify every count, line and locator this seat's report cites.

Greps the seat's own receipts and the gate copy; prints one line per check and
exits 1 if any check fails. Quoted receipt lines must appear verbatim here and
in the receipt; code locators are computed with a search, never typed blind.
"""

import collections
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEAT = os.path.dirname(HERE)
RECEIPTS = os.path.join(SEAT, "receipts")
GATE = os.path.join(SEAT, "check-session-material.py")
TRIAGE = os.path.join(SEAT, "triage.tsv")
LANE = os.path.abspath(os.path.join(SEAT, "..", "..", "..", "..", ".."))
REV = "4d22eeb66c2835af8aaa3fac6ad838fa616aa663"

failures = []
checks = [0]


def check(name, ok, detail=""):
    checks[0] += 1
    print("%s %s%s" % ("ok" if ok else "FAIL", name, (" " + detail) if detail else ""))
    if not ok:
        failures.append(name)


def read(name):
    with open(os.path.join(RECEIPTS, name), encoding="utf-8") as handle:
        return handle.read()


def count(text, prefix):
    return sum(1 for line in text.splitlines() if line.startswith(prefix))


def summary(text):
    lines = [line for line in text.splitlines() if line.startswith("SESSION_MATERIAL:")]
    return lines[-1] if lines else ""


baseline = read("01-baseline.txt")
copy_baseline = read("01b-baseline-copy-nowaivers.txt")
check("baseline-97-findings", count(baseline, "FINDING") == 97,
      "found=%d" % count(baseline, "FINDING"))
check("baseline-summary", summary(baseline).endswith("findings=97 rev=4d22eeb66c2835af8aaa3fac6ad838fa616aa663"),
      summary(baseline))
check("copy-nowaivers-identical-to-tracked", baseline == copy_baseline)

newgate = read("03-newgate-baseline.txt")
check("newgate-baseline-97", count(newgate, "FINDING") == 97)

marked49 = read("04-marked-49.txt")
check("marked49-waived-49", "SESSION_MATERIAL_WAIVED: findings=49 files=47" in marked49)
check("marked49-findings-48", summary(marked49).endswith("findings=48 rev=%s"
      % re.search(r"rev=([0-9a-f]{40})", summary(marked49)).group(1)))
check("marked49-exit-1", marked49.rstrip().endswith("exit=1"))

tracked = read("04b-tracked-gate-on-marked.txt")
check("tracked-gate-ignores-markers", summary(tracked).endswith("findings=97 rev=%s"
      % re.search(r"rev=([0-9a-f]{40})", summary(tracked)).group(1)))

allmark = read("05-marked-all-synthetic.txt")
check("allmark-waived-still-49", "SESSION_MATERIAL_WAIVED: findings=49 files=47" in allmark)
check("allmark-rejected-33", count(allmark, "WAIVER_REJECTED") == 33,
      "rejected=%d" % count(allmark, "WAIVER_REJECTED"))
check("allmark-findings-still-48", summary(allmark).endswith(
    "findings=48 rev=%s" % re.search(r"rev=([0-9a-f]{40})", summary(allmark)).group(1)))
reasons = collections.Counter(
    line.rsplit("reason=", 1)[1] for line in allmark.splitlines()
    if line.startswith("WAIVER_REJECTED"))
check("allmark-reasons", reasons == {"value-not-synthetic:title-not-synthetic": 21,
                                     "value-not-synthetic:program-not-synthetic": 12},
      str(dict(reasons)))

planted = read("06-planted-real-dump.txt")
check("planted-rejected",
      "WAIVER_REJECTED file=.ufo/waves/round-46/w1/ExecSessionTriage/fixtures/planted/"
      "mons.json rule=R3_MONITOR_IDENT reason=value-not-synthetic:serial-not-synthetic"
      in planted)
check("planted-finding-kept",
      "FINDING file=.ufo/waves/round-46/w1/ExecSessionTriage/fixtures/planted/"
      "mons.json rule=R3_MONITOR_IDENT count=1" in planted)
check("planted-findings-49", summary(planted).endswith(
    "findings=49 rev=%s" % re.search(r"rev=([0-9a-f]{40})", summary(planted)).group(1)))

tampered = read("07-tampered-waived-fixture.txt")
check("tamper-sha-mismatch",
      "rule=R3_MONITOR_IDENT reason=sha-mismatch" in tampered
      and "C00_shipped" in tampered)
check("tamper-waived-drops-to-48",
      "SESSION_MATERIAL_WAIVED: findings=48 files=46" in tampered)
check("tamper-findings-51", summary(tampered).endswith(
    "findings=51 rev=%s" % re.search(r"rev=([0-9a-f]{40})", summary(tampered)).group(1)))

nowaivers = read("08-no-waivers.txt")
check("nowaivers-99", summary(nowaivers).endswith(
    "findings=99 rev=%s" % re.search(r"rev=([0-9a-f]{40})", summary(nowaivers)).group(1)))
check("nowaivers-no-waiver-lines", "WAIVER" not in nowaivers)

selftest = read("00-selftest.txt")
check("selftest-34-34", "SELFTEST: passed=34/34 failed=0" in selftest)

with open(TRIAGE, encoding="utf-8") as handle:
    rows = [line.rstrip("\n").split("\t") for line in handle][1:]
classes = collections.Counter(row[3] for row in rows)
check("triage-97", len(rows) == 97, "rows=%d" % len(rows))
check("triage-classes", classes == {"REAL": 15, "SYNTHETIC": 82}, str(dict(classes)))
round45 = [row for row in rows if row[0].startswith(".ufo/waves/round-45/")]
check("triage-round45-all-synthetic",
      len(round45) == 49 and all(row[3] == "SYNTHETIC" for row in round45),
      "n=%d" % len(round45))
check("triage-no-real-in-round45", not any(row[3] == "REAL" for row in round45))

with open(GATE, encoding="utf-8") as handle:
    gate = handle.read()
for needle in ("SYNTHETIC-MATERIAL v1 kind=", "MARKER_SUFFIX = \".synthetic\"",
               "SESSION_MATERIAL_WAIVED:", "registry-in-ufo", "path-outside-waves",
               "--no-waivers", "value-not-synthetic", "gate-source-mismatch"):
    check("gate-has %s" % needle, needle in gate)

marker_line = [index + 1 for index, line in enumerate(gate.splitlines())
               if "MARKER_RE = re.compile(" in line]
check("gate-marker-locator", bool(marker_line), "line=%r" % marker_line)

oracle_files = subprocess.run(
    ["git", "-C", LANE, "ls-tree", "-r", "--name-only", REV, "--",
     ".ufo/waves/round-43/w1/ExecOracleGkeep"],
    check=True, capture_output=True, text=True).stdout.split()
titles = []
for relpath in oracle_files:
    if not relpath.endswith((".json", ".txt")):
        continue
    blob = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (REV, relpath)],
                          check=True, capture_output=True).stdout.decode("utf-8", "replace")
    titles.extend(re.findall(r'"(?:initialT|t)itle"\s*:\s*"([^"]*)"', blob))
check("oracle-titles-all-probe",
      len(set(titles)) == 1 and titles[0] == "gkeep-oracle-probe",
      "values=%d distinct=%d" % (len(titles), len(set(titles))))

print("VERIFY: checks=%d failed=%d" % (checks[0], len(failures)))
sys.exit(1 if failures else 0)
