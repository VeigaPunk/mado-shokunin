#!/usr/bin/env python3
"""hole-probes.py — build the ledger mutations this counter must reject, and score them.

Seat C1CounterDesign (mado round 52, w1).  Draft helper.  Each probe starts from the
production ledger at the frozen base revision and injects exactly one defect class that
the round-52 C1 claim names; the counter must exit 1 and name the defect.  The probes
are written under a scratch directory and are never committed to the lane.

    python3 -I hole-probes.py --repo <lane> --rev <rev> --counter <counter.py> --work <scratch>

Exit 0 = every probe was rejected with the expected signal; 1 = a probe passed (false
green) or failed without its signal; 2 = setup error.
"""
import argparse
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
LEDGER_REL = "quality/tool-ledger.md"
LINE = re.compile(r":\d+(?:-\d+)?$")


def git(repo, *args):
    proc = subprocess.run(("git", "-C", repo) + args, capture_output=True)
    if proc.returncode != 0:
        raise SystemExit("git %s failed: %s" % (
            " ".join(args), proc.stderr.decode("utf-8", "replace")[:300]))
    return proc.stdout


def rows_of(text):
    """[(index, cells)] for every pipe-table row whose first cell names a path."""
    rows = []
    fenced = False
    for index, raw in enumerate(text.splitlines()):
        line = raw.strip()
        if line.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        first = LINE.sub("", cells[0].strip().strip("`*_ "))
        if not first or "/" not in first or first.startswith(":"):
            continue
        rows.append((index, cells))
    return rows


def rebuild(rows):
    return "\n".join("| " + " | ".join(cells) + " |" for _index, cells in rows) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="C1-r52 counter hole probes")
    ap.add_argument("--repo", default=LANE)
    ap.add_argument("--rev", default="85d57a818c3707397e21c840b6498b105ba798aa")
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", required=True)
    args = ap.parse_args(argv)

    repo = os.path.abspath(args.repo)
    counter = os.path.abspath(args.counter)
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    rev = git(repo, "rev-parse", "--verify", args.rev + "^{commit}").decode().strip()
    ledger = git(repo, "show", "%s:%s" % (rev, LEDGER_REL)).decode("utf-8", "replace")
    rows = rows_of(ledger)
    if not rows:
        print("no ledger rows at %s" % rev, file=sys.stderr)
        return 2

    def first_index(pred):
        for index, cells in rows:
            if pred(cells):
                return index
        return None

    def probe_ledger_self():
        out = []
        for index, cells in rows:
            cells = list(cells)
            cells[2] = " `quality/tool-ledger.md` "
            out.append((index, cells))
        return rebuild(out)

    def probe_row_self():
        out = []
        for index, cells in rows:
            cells = list(cells)
            cells[2] = " `%s` " % cells[0].strip().strip("`")
            out.append((index, cells))
        return rebuild(out)

    def probe_peer():
        """One row points at a sibling instrument's file instead of a document."""
        target = None
        for _index, cells in rows:
            if cells[0].strip().strip("`").startswith("quality/counters/"):
                target = cells[0].strip().strip("`")
                break
        out = []
        for index, cells in rows:
            cells = list(cells)
            if target and cells[0].strip().strip("`") == "tools/mado-geometry.py":
                cells[2] = " `%s` " % target
            out.append((index, cells))
        return rebuild(out)

    def probe_cross_description():
        """Each row carries the NEXT row's description: every description is bound to
        a different instrument than the one it describes."""
        out = []
        descs = [cells[1] for _index, cells in rows]
        for n, (index, cells) in enumerate(rows):
            cells = list(cells)
            cells[1] = " %s " % descs[(n + 1) % len(descs)]
            out.append((index, cells))
        return rebuild(out)

    def probe_omnibus():
        """Every row points at one shared file that names many basenames."""
        out = []
        for index, cells in rows:
            cells = list(cells)
            cells[2] = " `SCORECARD.md` "
            out.append((index, cells))
        return rebuild(out)

    def probe_laundered_self_pointer():
        """One row's pointer names the ledger AND an accountable document.

        A second document must not launder a circular accountability claim.
        """
        out = []
        for index, cells in rows:
            cells = list(cells)
            if cells[0].strip().strip("`") == "tools/mado-geometry.py":
                cells[2] = " `quality/tool-ledger.md` and `SCORECARD.md` "
            out.append((index, cells))
        return rebuild(out)

    probes = [
        ("ledger-self-pointer", probe_ledger_self(), "self_pointer"),
        ("row-self-pointer", probe_row_self(), "self_pointer"),
        ("peer-instrument-pointer", probe_peer(), "bad_pointer"),
        ("cross-description", probe_cross_description(), "generic_desc"),
        ("omnibus-pointer", probe_omnibus(), "bad_pointer"),
        ("laundered-self-pointer", probe_laundered_self_pointer(), "self_pointer"),
    ]

    failed = 0
    for name, text, expect in probes:
        path = os.path.join(work, "probe-%s.md" % name)
        with open(path, "w") as fh:
            fh.write(text)
        proc = subprocess.run([sys.executable, "-I", counter, "--repo", repo, "--rev", rev,
                               "--work", work, "--ledger", path],
                              capture_output=True, text=True)
        out = proc.stdout
        final = out.strip().splitlines()[-1] if out.strip() else ""
        fields = dict(re.findall(r"\b([a-z_]+)=([^\s`]+)", final))
        value = fields.get(expect)
        ok = proc.returncode == 1 and value is not None and value not in ("0", "absent")
        print("probe=%-26s expect=%-12s exit=%s %s=%s verdict=%s -> %s" % (
            name, expect, proc.returncode, expect, value,
            fields.get("verdict", "?"), "REJECTED" if ok else "FALSE-GREEN"))
        if not ok:
            failed += 1
        print("  final: %s" % final)
    print("HOLE_PROBES: %d/%d rejected" % (len(probes) - failed, len(probes)))
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
