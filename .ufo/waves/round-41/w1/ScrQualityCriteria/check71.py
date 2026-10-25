#!/usr/bin/env python3
"""check71 - every seat's returned report path resolves inside its own round's wave dir.

QUALITY criterion 71. Reads a wave's `w1-results.json` (or registry) at a revision, parses
each seat's returned `report` path, and requires:
  * the path matches `.ufo/waves/round-<N>/w1/<Seat>.md` for the round being run, and
  * the seat name in the path equals the seat that returned it, and
  * the path exists at the revision (`git cat-file -e`).

Usage: check71.py --repo . --rev <REV> --results <path-in-repo> --round <N> [--results-file <disk>]
Exit 0 = every returned report resolves; 1 = at least one FOREIGN/SEAT-MISMATCH/UNTRACKED.
"""
import argparse
import json
import re
import subprocess
import sys


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--results", required=True)
    ap.add_argument("--round", required=True, type=int)
    ap.add_argument("--results-file", default=None,
                    help="read the results JSON from disk instead of from --rev")
    a = ap.parse_args()

    if a.results_file:
        body = open(a.results_file, encoding="utf-8").read()
    else:
        r = git(a.repo, "show", "%s:%s" % (a.rev, a.results))
        if r.returncode:
            print("MISSING-RESULTS %s at %s" % (a.results, a.rev))
            return 2
        body = r.stdout
    doc = json.loads(body)
    rows = doc.get("results", doc.get("seats", []))

    pat = re.compile(r'^\.ufo/waves/round-%d/w1/([A-Za-z0-9_]+)\.md$' % a.round)
    ok = bad = noparse = noreport = 0
    for row in rows:
        name = row.get("name") or row.get("seat") or "?"
        out = row.get("output")
        if isinstance(out, str):
            try:
                out = json.loads(out)
            except ValueError:
                noparse += 1
                continue
        if not isinstance(out, dict) or not out.get("report"):
            noreport += 1
            continue
        rp = out["report"]
        m = pat.match(rp)
        if not m:
            print("FOREIGN %s returned %s (not under round-%d)" % (name, rp, a.round))
            bad += 1
            continue
        if m.group(1) != name:
            print("SEAT-MISMATCH %s returned %s" % (name, rp))
            bad += 1
            continue
        if git(a.repo, "cat-file", "-e", "%s:%s" % (a.rev, rp)).returncode:
            print("UNTRACKED %s returned %s (absent at %s)" % (name, rp, a.rev))
            bad += 1
            continue
        ok += 1

    print("RESOLVED ok=%d bad=%d unparsed=%d no-report=%d of %d seats"
          % (ok, bad, noparse, noreport, len(rows)))
    if bad:
        print("FAIL %d returned report path(s) do not resolve inside round-%d" % (bad, a.round))
        return 1
    print("PASS every returned report resolves inside round-%d" % a.round)
    return 0


if __name__ == "__main__":
    sys.exit(main())
