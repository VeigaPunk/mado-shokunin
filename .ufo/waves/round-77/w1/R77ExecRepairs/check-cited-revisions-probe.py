#!/usr/bin/env python3
"""check-cited-revisions-probe.py — flag a SCORECARD row whose cited revision is not the
instrument's last-change commit (round-76 spot-check D2; round-77 lesson M77-3, seat
R77ExecRepairs).

Two claim shapes are checked against `git log -1 --format=%H -- <instrument>`:

  * "at `<hash>` (its instrument's last change ...)"   — SCORECARD.md:4339's shape
  * "measured at `<hash>`"                              — a reported measurement revision

The instrument path is `--path` when given, else the first `quality/counters/<name>.py`
mentioned in the row text. A claimed hash must be a prefix of the resolved full commit id.

Exit 0 (green): every claim matched the instrument's last-change commit.
Exit 1 (red): at least one claim did not match.
Exit 2: usage error, unreadable row, no instrument path, or no last-change claim — a probe
        that found nothing must never print a green score (round-76 lesson M76-3).

Read-only: one `git log -1` per run; no repo write, no network, no scratch.
"""
import argparse
import os
import re
import subprocess
import sys

TOOL = "check-cited-revisions-probe.py"
PATH_RE = re.compile(r"quality/counters/[A-Za-z0-9_.-]+\.py")
CLAIM_PATTERNS = (
    ("last-change", re.compile(
        r"at\s+[`'\"]?([0-9a-f]{7,40})[`'\"]?\s*\(\s*its\s+instrument['\u2019]?s\s+last\s+change",
        re.IGNORECASE)),
    ("measured-at", re.compile(
        r"measured\s+at\s+[`'\"]?([0-9a-f]{7,40})[`'\"]?", re.IGNORECASE)),
)


class ProbeError(Exception):
    pass


def claims_in(text):
    """All (hash-start, claimed-hash, kind) claims, deduped on the hash position."""
    seen = set()
    claims = []
    for kind, pattern in CLAIM_PATTERNS:
        for m in pattern.finditer(text):
            key = (m.start(1), m.group(1).lower())
            if key in seen:
                continue
            seen.add(key)
            claims.append((m.start(1), m.group(1).lower(), kind))
    return sorted(claims)


def git_last_change(repo, path):
    r = subprocess.run(["git", "-C", repo, "log", "-1", "--format=%H", "--", path],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise ProbeError("git log failed for %s: %s" % (path, r.stderr.strip()[:200]))
    sha = r.stdout.strip()
    if not sha:
        raise ProbeError("%s has no commit touching it" % path)
    return sha


def main(argv):
    parser = argparse.ArgumentParser(prog=TOOL, description=__doc__.splitlines()[0])
    parser.add_argument("--repo", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--path", dest="path")
    args = parser.parse_args(argv)
    try:
        top = subprocess.run(["git", "-C", args.repo, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True)
        if top.returncode != 0:
            raise ProbeError("--repo is not a git work tree: %s" % args.repo)
        repo = top.stdout.strip()
        with open(args.text, encoding="utf-8") as fh:
            text = fh.read()
        path = args.path
        if not path:
            m = PATH_RE.search(text)
            if not m:
                raise ProbeError("no quality/counters/*.py instrument path in the row")
            path = m.group(0)
        claims = claims_in(text)
        if not claims:
            raise ProbeError("no last-change claim in the row (refusing to report green)")
        last = git_last_change(repo, path)
        print("CITED-REVISIONS-PROBE: instrument=%s last_change=%s claims=%d"
              % (path, last, len(claims)))
        mismatched = 0
        for _pos, claimed, kind in claims:
            match = last.startswith(claimed)
            mismatched += 0 if match else 1
            print("CITED-REVISIONS-PROBE: claim hash=%s kind=%s match=%s"
                  % (claimed, kind, "yes" if match else "no"))
        verdict = "green" if mismatched == 0 else "red"
        print("CITED-REVISIONS-PROBE: RESULT %s claims=%d mismatched=%d"
              % (verdict, len(claims), mismatched))
        return 0 if mismatched == 0 else 1
    except (ProbeError, OSError) as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        print("CITED-REVISIONS-PROBE: RESULT error claims=0 mismatched=0")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
