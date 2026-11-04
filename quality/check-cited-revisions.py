#!/usr/bin/env python3
"""mado — cited-revision probe: a row that cites a revision as an instrument's last change
must cite the commit that actually last changed that instrument.

Reads one caller-supplied row/record file (`--text`) and an optional `--path`; without a path it
takes the first `quality/counters/<name>.py` mentioned in the text. Two claim shapes are checked
against `git log -1 --format=%H -- <instrument>`:

  * "at `<hash>` (its instrument's last change ...)"   — the round-76 SCORECARD row shape (D2)
  * "measured at `<hash>`"                              — a reported measurement revision

A claimed hash must be a prefix of the resolved full commit id. Exit 0 green (every claim
matched), 1 red (at least one mismatch), 2 error — including "no claim found", because a probe
that found nothing must never print a green score (round-76 lesson M76-3).

Read-only: one `git log -1` per run; no repo write, no network, no scratch.
Usage: python3 -I quality/check-cited-revisions.py --repo . --text ROW.md [--path P]
       python3 -I quality/check-cited-revisions.py --selftest
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

TOOL = "check-cited-revisions.py"
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


def evaluate(repo, text, path=None):
    if not path:
        m = PATH_RE.search(text)
        if not m:
            raise ProbeError("no quality/counters/*.py instrument path in the row")
        path = m.group(0)
    claims = claims_in(text)
    if not claims:
        raise ProbeError("no last-change claim in the row (refusing to report green)")
    last = git_last_change(repo, path)
    rows = [(claimed, kind, last.startswith(claimed)) for _pos, claimed, kind in claims]
    return path, last, rows


def selftest():
    checks = total = 0

    def ok(cond, label):
        nonlocal checks, total
        total += 1
        if cond:
            checks += 1
        else:
            print("MADO_CITED_SELFTEST_FAIL: %s" % label)

    with tempfile.TemporaryDirectory() as td:
        repo = os.path.join(td, "repo")
        os.makedirs(os.path.join(repo, "quality", "counters"))
        subprocess.run(["git", "-C", repo, "init", "-q"], check=True)
        subprocess.run(["git", "-C", repo, "config", "user.email", "t@t"], check=True)
        subprocess.run(["git", "-C", repo, "config", "user.name", "t"], check=True)
        target = os.path.join(repo, "quality", "counters", "x.py")
        with open(target, "w") as fh:
            fh.write("x = 1\n")
        subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-qm", "one"], check=True)
        first = git_last_change(repo, "quality/counters/x.py")
        with open(target, "a") as fh:
            fh.write("y = 2\n")
        subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-qm", "two"], check=True)
        last = git_last_change(repo, "quality/counters/x.py")

        def run(text, path=None):
            argv = [sys.executable, "-I", os.path.abspath(__file__), "--repo", repo, "--text", text]
            if path:
                argv += ["--path", path]
            return subprocess.run(argv, capture_output=True, text=True)

        f_red = os.path.join(td, "red.md")
        with open(f_red, "w") as fh:
            fh.write("at `%s` (its instrument's last change) quality/counters/x.py\n" % first)
        f_green = os.path.join(td, "green.md")
        with open(f_green, "w") as fh:
            fh.write("measured at `%s` quality/counters/x.py\n" % last)
        f_empty = os.path.join(td, "empty.md")
        with open(f_empty, "w") as fh:
            fh.write("no claim here\n")
        r = run(f_red)
        ok(r.returncode == 1 and "RESULT red" in r.stdout, "red row is red")
        r = run(f_green)
        ok(r.returncode == 0 and "RESULT green" in r.stdout, "green row is green")
        r = run(f_empty)
        ok(r.returncode == 2, "no claim is an error, not green")
        ok(evaluate(repo, open(f_red).read())[0] == "quality/counters/x.py", "path from text")
        ok(evaluate(repo, open(f_green).read(), "quality/counters/x.py")[1] == last, "explicit path")
        try:
            evaluate(repo, "measured at `deadbeef` no path\n")
            ok(False, "missing instrument path refused")
        except ProbeError:
            ok(True, "missing instrument path refused")
    print("MADO_CITED_SELFTEST: %d/%d" % (checks, total))
    return 0 if checks == total else 1


def main(argv):
    parser = argparse.ArgumentParser(prog=TOOL, description=__doc__.splitlines()[0])
    parser.add_argument("--repo")
    parser.add_argument("--text")
    parser.add_argument("--path", dest="path")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.repo or not args.text:
        print("CITED-REVISIONS-PROBE: RESULT error claims=0 mismatched=0 (usage)")
        return 2
    try:
        top = subprocess.run(["git", "-C", args.repo, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True)
        if top.returncode != 0:
            raise ProbeError("--repo is not a git work tree: %s" % args.repo)
        repo = top.stdout.strip()
        with open(args.text, encoding="utf-8") as fh:
            text = fh.read()
        path, last, rows = evaluate(repo, text, args.path)
        print("CITED-REVISIONS-PROBE: instrument=%s last_change=%s claims=%d"
              % (path, last, len(rows)))
        mismatched = 0
        for claimed, kind, match in rows:
            mismatched += 0 if match else 1
            print("CITED-REVISIONS-PROBE: claim hash=%s kind=%s match=%s"
                  % (claimed, kind, "yes" if match else "no"))
        print("CITED-REVISIONS-PROBE: RESULT %s claims=%d mismatched=%d"
              % ("green" if mismatched == 0 else "red", len(rows), mismatched))
        return 0 if mismatched == 0 else 1
    except (ProbeError, OSError) as exc:
        sys.stderr.write("%s: %s\n" % (TOOL, exc))
        print("CITED-REVISIONS-PROBE: RESULT error claims=0 mismatched=0")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
