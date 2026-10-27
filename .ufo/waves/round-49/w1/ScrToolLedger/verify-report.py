#!/usr/bin/env python3
"""verify-report.py - check the row table and the quoted fragments of ScrToolLedger.md
against the git objects at the base revision.

The report is prose; this is the part of it that must be true of the repository. It
reads the report's row table (lines starting with `| ` followed by a `mado-` tool) and
each claim below, and prints one `OK`/`FAIL` line per assertion; exit 1 on any FAIL.

Python 3 stdlib only; reads git objects, writes nothing, starts no host program.
"""

import os
import re
import subprocess
import sys

BASE = "03e4ae76aff7a4be59cb69970dd553baa319695a"
HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(os.path.dirname(HERE), "ScrToolLedger.md")

# (label, path at BASE, 1-based line, fragment that must be on that line)
QUOTES = [
    ("F1 globals committed digests",
     ".ufo/waves/round-41/w1/ExecLiveHost/live-census.txt", 5,
     "61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0"),
    ("F2 monitors r46 digest",
     ".ufo/waves/round-46/w1/ExecW2Monitors/live-runs.txt", 3,
     "2f007417ae9efa43c7c3e5bcf8e88710fb6cd6c856e49b4084c742a7ecff5609"),
    ("F2 eventq r39 census digest",
     ".ufo/waves/round-39/w1/ExecEventqSnapshot/eventq-live-census.txt", 2,
     "tool_sha256=436f550e9939a783b7b95d154d099b788ad9daaed2282e19de89413e39371f24"),
    ("F3 citation index quotes the geometry verdict",
     ".ufo/waves/round-46/w1/ScrErrata/receipts/f3-skill-clients.txt", 0,
     "MADO_GEOMETRY:"),
    ("F4 binds before-control is TARGET_MISSED",
     ".ufo/waves/round-25/evidence/c1-before-v4-41cc04c8.txt", 49,
     "cases_pass=0/41"),
    ("F4 wsrules before-control is TARGET_MISSED",
     ".ufo/waves/round-27/evidence/c1v4-before-543f0445.txt", 49,
     "verdict=TARGET_MISSED"),
    ("F5 round-47 ledger claims 14 instruments",
     ".ufo/waves/round-47/w1/ScrToolLedger/ledger.md", 106, "14"),
    ("F6 eventq receipt keeps lagging/missing_client",
     ".ufo/waves/round-38/receipts/eventq-live.txt", 8,
     "lagging=0 missing_client=-"),
    ("F8 devices newest live run reads the compositor",
     ".ufo/waves/round-46/w1/ExecIndepA/receipts/host-diff.txt", 0,
     "hyprctl devices -j"),
]


REPO = None


def git(*args):
    p = subprocess.run(["git", "-C", REPO or HERE] + list(args), capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout


def main():
    fails = 0

    def out(ok, label, extra=""):
        nonlocal fails
        if not ok:
            fails += 1
        sys.stdout.write("%s %s%s\n" % ("OK  " if ok else "FAIL", label,
                                        (" " + extra) if extra else ""))

    global REPO
    top = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"],
                         capture_output=True)
    if top.returncode != 0:
        sys.stdout.write("FAIL not a git repository\n")
        return 1
    REPO = top.stdout.decode().strip()

    # the round-47 ledger's instrument count row, and the terminal omission
    r47 = git("show", "%s:.ufo/waves/round-47/w1/ScrToolLedger/ledger.md" % BASE)
    out(r47 is not None and b"mado-terminal" not in r47,
        "F5 round-47 ledger has no mado-terminal row")
    out(r47 is not None and b"| 14 | tracked instruments" in r47,
        "F5 round-47 ledger claims 14 tracked instruments")
    names = git("ls-tree", "-r", "--name-only", BASE, "--", "tools/").decode().split()
    out(len(names) == 15, "F5 base has 15 tools", "(%d)" % len(names))

    # quoted fragments
    names_out = None
    for label, path, line, fragment in QUOTES:
        blob = git("show", "%s:%s" % (BASE, path))
        if blob is None:
            out(False, label, "missing " + path)
            continue
        lines = blob.decode("utf-8", "replace").splitlines()
        if line == 0:
            line = next((n for n, l in enumerate(lines, 1) if fragment in l), 0)
            if line == 0:
                out(False, label, "fragment absent from " + path)
                continue
        if line > len(lines):
            out(False, label, "line %d beyond end of %s" % (line, path))
            continue
        got = lines[line - 1]
        ok = fragment in got
        if label.startswith("F3"):
            ok = ok and b"mado-monitors.py" in blob
        out(ok, label, "%s:%d" % (path, line))

    # the row table: path, locator line, digest prefix
    with open(REPORT, encoding="utf-8") as fh:
        text = fh.read()
    rows = 0
    for line in text.splitlines():
        if not line.startswith("| `mado-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        tool = cells[0].strip("`")
        loc = cells[2].strip("`")
        digest_cell = cells[4]
        m = re.match(r"^(\.ufo/\S+):(\d+)$", loc)
        if not m:
            out(False, "%s row locator" % tool, loc)
            continue
        path, lineno = m.group(1), int(m.group(2))
        rows += 1
        blob = git("show", "%s:%s" % (BASE, path))
        out(blob is not None, "%s receipt exists at base" % tool, path)
        if blob is None:
            continue
        lines = blob.decode("utf-8", "replace").splitlines()
        out(lineno <= len(lines) and lines[lineno - 1].strip() != "",
            "%s locator line is non-empty" % tool, "%s:%d" % (path, lineno))
        dm = re.search(r"`([0-9a-f]{8})`", digest_cell)
        if dm:
            out(dm.group(1) in blob.decode("utf-8", "replace"),
                "%s digest prefix in receipt" % tool, dm.group(1))
        else:
            out("none recorded" in digest_cell,
                "%s digest column states none" % tool)
    out(rows == 12, "row table has 12 rows", "(%d)" % rows)

    sys.stdout.write("REPORT-CLAIMS %s rows=%d fails=%d\n"
                     % ("ok" if fails == 0 else "FAILED", rows, fails))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
