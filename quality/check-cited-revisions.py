#!/usr/bin/env python3
"""mado — cited-revision probe: every declared (revision, instrument) pair must be true.

Takes one or more caller-supplied pair lists. A pair line is `<hash> <repo-relative path>`
(`#` starts a comment, blank lines ignored); the probe resolves the path's last-change commit
with read-only git and compares. This is the executable form of the record rule that a
"measured at <rev> (its instrument's last change)" sentence names the instrument's real last
change: prose binding is curated into the pair list, so the probe never guesses which path a
revision in a long sentence belongs to.

Contract: MADO_CITED: pairs=P match=M stale=S missing=X verdict=CLEAN|STALE
Exit map: 0 clean (every pair matches) · 1 stale or missing pair · 2 setup/usage error.

Writes nothing; read-only git in the named repository.
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile

HASH = re.compile(r"^[0-9a-f]{7,40}$")


def git(repo, *args):
    proc = subprocess.run(["git", "-C", repo, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout.decode("utf-8", "replace").strip(), proc.stderr.decode("utf-8", "replace").strip()


def last_change(repo, path):
    rc, out, _ = git(repo, "log", "-1", "--format=%H", "--", path)
    if rc != 0 or not out:
        return None
    return out.splitlines()[0]


def parse_pairs(path):
    pairs = []
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2 or not HASH.match(parts[0]):
                raise ValueError("%s:%d is not `<hash> <path>`" % (path, lineno))
            pairs.append((lineno, parts[0], parts[1]))
    return pairs


def check(repo, pair_file):
    rows = []
    for lineno, h, p in parse_pairs(pair_file):
        last = last_change(repo, p)
        if last is None:
            rows.append((lineno, h, p, None, "MISSING"))
        elif last.startswith(h) or h.startswith(last):
            rows.append((lineno, h, p, last, "MATCH"))
        else:
            rows.append((lineno, h, p, last, "STALE"))
    return rows


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
        os.makedirs(repo)
        subprocess.run(["git", "-C", repo, "init", "-q"], check=True)
        subprocess.run(["git", "-C", repo, "config", "user.email", "t@t"], check=True)
        subprocess.run(["git", "-C", repo, "config", "user.name", "t"], check=True)
        with open(os.path.join(repo, "inst.py"), "w") as fh:
            fh.write("x = 1\n")
        subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-qm", "one"], check=True)
        first = git(repo, "rev-parse", "HEAD")[1]
        with open(os.path.join(repo, "inst.py"), "a") as fh:
            fh.write("y = 2\n")
        subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-qm", "two"], check=True)
        last = git(repo, "rev-parse", "HEAD")[1]

        good = os.path.join(td, "good.txt")
        with open(good, "w") as fh:
            fh.write("%s inst.py\n" % last)
        rows = check(repo, good)
        ok(len(rows) == 1 and rows[0][4] == "MATCH", "current revision matches")
        bad = os.path.join(td, "bad.txt")
        with open(bad, "w") as fh:
            fh.write("%s inst.py\n" % first)
        rows = check(repo, bad)
        ok(len(rows) == 1 and rows[0][4] == "STALE", "stale revision is stale")
        missing = os.path.join(td, "missing.txt")
        with open(missing, "w") as fh:
            fh.write("%s nope.py\n" % last)
        rows = check(repo, missing)
        ok(len(rows) == 1 and rows[0][4] == "MISSING", "missing path reported")
        commented = os.path.join(td, "commented.txt")
        with open(commented, "w") as fh:
            fh.write("# a comment\n\n%s inst.py  # inline\n" % last)
        ok(len(check(repo, commented)) == 1, "comments and blanks ignored")
        short = os.path.join(td, "short.txt")
        with open(short, "w") as fh:
            fh.write("%s inst.py\n" % last[:12])
        ok(check(repo, short)[0][4] == "MATCH", "short hash prefix matches")
        broken = os.path.join(td, "broken.txt")
        with open(broken, "w") as fh:
            fh.write("not-a-pair\n")
        try:
            check(repo, broken)
            ok(False, "malformed pair refused")
        except ValueError:
            ok(True, "malformed pair refused")
    print("MADO_CITED_SELFTEST: %d/%d" % (checks, total))
    return 0 if checks == total else 1


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--repo")
    ap.add_argument("--pairs", action="append", default=[])
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.repo or not args.pairs:
        print("MADO_CITED: ERROR (stage=setup usage)")
        return 2
    repo = os.path.abspath(args.repo)
    if git(repo, "rev-parse", "--git-dir")[0] != 0:
        print("MADO_CITED: ERROR (stage=setup not a git repository: %s)" % repo)
        return 2
    total = bad = stale = missing = 0
    for pair_file in args.pairs:
        try:
            rows = check(repo, pair_file)
        except (OSError, ValueError) as exc:
            print("MADO_CITED: ERROR (stage=setup %s)" % exc)
            return 2
        for lineno, h, p, last, verdict in rows:
            total += 1
            bad += 1 if verdict != "MATCH" else 0
            stale += 1 if verdict == "STALE" else 0
            missing += 1 if verdict == "MISSING" else 0
            print("MADO_CITED: pairs=%s line=%d hash=%s path=%s last=%s verdict=%s"
                  % (pair_file, lineno, h, p, (last or "-")[:12], verdict))
    print("MADO_CITED: pairs=%d match=%d stale=%d missing=%d verdict=%s"
          % (total, total - bad, stale, missing, "CLEAN" if bad == 0 else "STALE"))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
