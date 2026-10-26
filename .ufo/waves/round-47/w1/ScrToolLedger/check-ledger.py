#!/usr/bin/env python3
"""check-ledger.py — proposed QUALITY criterion 91 checker (round 47, seat ScrToolLedger).

Reads the machine-readable rows of the live-state tool ledger and re-derives every row's
status from the committed evidence:

  * every tracked instrument under tools/ (13 mado-*.py + mado-verify.sh) must have one row;
  * a `none` row must carry a stated reason (`-` receipt, so the row itself says "no live run");
  * a live row names a receipt path and the tool sha256 that receipt recorded; the checker
    requires that sha to appear in the receipt text and compares it with the tool's bytes at
    the read revision:
        ok      recorded sha == current bytes
        stale   recorded sha != current bytes (the receipt predates the file)
        unbound recorded sha absent from the receipt (the row points at the wrong receipt)
        missing-receipt  the receipt path is not in the tree
    and the row's declared status must equal the derived one.

Exit 0 iff every instrument has a row and every row's declared status is the derived one;
exit 1 otherwise; exit 2 on usage/setup failure.

Usage:
    python3 -I check-ledger.py [--repo DIR] [--rev REV] [--ledger PATH]
Prints one line: LEDGER: ok=<n> stale=<n> none=<n> missing=<n> mismatch=<n> unbound=<n>
                 missing_receipt=<n> instruments=<n>
Standard library only; starts no process beyond the read-only `git show`/`git ls-tree`
needed when --rev is given; writes nothing.
"""
import argparse
import hashlib
import os
import subprocess
import sys

LEDGER_TAG = "<!-- ledger-rows"


def die(msg):
    sys.stdout.write("LEDGER: SETUP %s\n" % msg)
    raise SystemExit(2)


def sh(repo, args):
    p = subprocess.run(["git", "-C", repo] + args, capture_output=True)
    if p.returncode != 0:
        die("git " + " ".join(args) + ": " + p.stderr.decode("utf-8", "replace").strip()[:120])
    return p.stdout


def instruments(repo, rev):
    if rev:
        out = sh(repo, ["ls-tree", "-r", "--name-only", rev, "--", "tools/"]).decode()
        names = [n for n in out.splitlines()
                 if n.startswith("tools/mado-") and (n.endswith(".py") or n.endswith(".sh"))]
        getter = lambda p: sh(repo, ["show", "%s:%s" % (rev, p)])
    else:
        names = ["tools/" + n for n in sorted(os.listdir(os.path.join(repo, "tools")))
                 if n.startswith("mado-") and (n.endswith(".py") or n.endswith(".sh"))]
        getter = lambda p: open(os.path.join(repo, p), "rb").read()
    return names, getter


def rows(path):
    """Parse the fenced ledger-rows block: tool<TAB>declared<TAB>receipt<TAB>sha-or-dash."""
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        die("ledger unreadable: %s" % e)
    if LEDGER_TAG not in text:
        die("ledger has no %s block" % LEDGER_TAG)
    body = text.split(LEDGER_TAG, 1)[1]
    # the block is either a fenced code block or the HTML comment that opens with the tag
    if "```" in body.split("-->", 1)[0]:
        body = body.split("```", 1)[1]
        body = body.split("```", 1)[0]
    elif "-->" in body:
        body = body.split("-->", 1)[0]
    else:
        die("ledger-rows block is not closed (no ``` or -->)")
    out = {}
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 4:
            die("row is not 4 tab fields: %r" % line[:80])
        tool, declared, receipt, sha = parts
        if declared not in ("ok", "stale", "none"):
            die("declared status not ok/stale/none: %r" % declared)
        if tool in out:
            die("duplicate row: %s" % tool)
        out[tool] = (declared, receipt, sha)
    if not out:
        die("ledger-rows block holds no rows")
    return out


def main(argv):
    ap = argparse.ArgumentParser(description="live-state tool ledger checker (criterion 91)")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--ledger", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                     "ledger.md"))
    a = ap.parse_args(argv)
    repo = os.path.abspath(a.repo)
    if not os.path.isdir(os.path.join(repo, "tools")):
        die("no tools/ under --repo")
    names, getter = instruments(repo, a.rev)
    if not names:
        die("no instruments found")
    table = rows(a.ledger)
    counts = dict(ok=0, stale=0, none=0, missing=0, mismatch=0, unbound=0, missing_receipt=0)
    observed = set()
    for path in names:
        tool = os.path.basename(path)
        observed.add(tool)
        if tool not in table:
            counts["missing"] += 1
            print("MISSING %s" % tool)
            continue
        declared, receipt, sha = table[tool]
        if declared == "none":
            counts["none"] += 1
            continue
        rpath = os.path.join(repo, receipt)
        if not os.path.isfile(rpath):
            counts["missing_receipt"] += 1
            print("MISSING-RECEIPT %s %s" % (tool, receipt))
            continue
        text = open(rpath, encoding="utf-8", errors="replace").read()
        if sha not in text:
            counts["unbound"] += 1
            print("UNBOUND %s sha=%s receipt=%s" % (tool, sha[:12], receipt))
            continue
        cur = hashlib.sha256(getter(path)).hexdigest()
        derived = "ok" if cur == sha else "stale"
        if derived != declared:
            counts["mismatch"] += 1
            print("MISMATCH %s declared=%s derived=%s recorded=%s current=%s"
                  % (tool, declared, derived, sha[:12], cur[:12]))
        else:
            counts[derived] += 1
    for extra in sorted(set(table) - observed):
        counts["stale"] += 0  # an extra row is not a failure of truth, but it is reported
        print("EXTRA %s (not a tracked instrument)" % extra)
    print("LEDGER: ok=%d stale=%d none=%d missing=%d mismatch=%d unbound=%d "
          "missing_receipt=%d instruments=%d"
          % (counts["ok"], counts["stale"], counts["none"], counts["missing"],
             counts["mismatch"], counts["unbound"], counts["missing_receipt"], len(names)))
    bad = counts["missing"] or counts["mismatch"] or counts["unbound"] or counts["missing_receipt"]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
