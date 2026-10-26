#!/usr/bin/env python3
"""check79.py - a pointer to a run names a committed receipt that carries the run.

Two pointer shapes are checked in a prose file (a round report, LOG.md, a
registration, a lesson):

  R1  `<observation> is recorded in <target>` - the target must name a receipt
      path; a prose section (`LOG.md Round 42`) is PROSE: a lead for a reader,
      not a receipt a later reader can re-run after the worktree is gone.
  R2  every backticked `receipts/<name>` token - the path must exist at the
      receipts revision and its bytes must carry
        (a) a command line marked `$ `,
        (b) the command's output (a non-empty line that is not a command, an
            `exit=` line or a comment),
        (c) the exit status (`^exit=<int>`).

The prose file is read from its own repository/revision (a lane report may quote
lane receipts, a fleet report quotes the lane's receipts), so the two sides take
separate `--repo/--rev` pairs.  Read-only over git objects; no worktree read, no
index lock.

Exit 0 when every pointer is OK, 1 on any non-OK pointer, 2 on setup errors.

Usage: python3 -I check79.py --prose-repo DIR --prose-rev REV
                             --receipts-repo DIR --receipts-rev REV PATH [PATH ...]
"""
import argparse
import re
import subprocess
import sys

RECORDED = re.compile(r"recorded in ([^;)]+)")
BACKTICK_RECEIPT = re.compile(r"`((?:\.ufo/waves/round-\d+/)?receipts/[\w.-]+\.(?:txt|json|jsonl|log))`")
RECEIPT_RE = re.compile(r"((?:\.ufo/waves/round-\d+/)?receipts/[\w.-]+\.(?:txt|json|jsonl|log))")


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr.strip()


def resolve_round(prose_path, path):
    if path.startswith(".ufo/"):
        return path
    m = re.search(r"round-(\d+)", prose_path)
    return ".ufo/waves/round-%s/%s" % (m.group(1), path) if m else path


def check_receipt(repo, rev, path):
    rc, _, err = git(repo, "cat-file", "-e", "%s:%s" % (rev, path))
    if rc != 0:
        tail = err.splitlines()[-1] if err else "absent"
        return "ABSENT", "not in %s:%s (%s)" % (rev[:9], path, tail)
    rc, body, err = git(repo, "show", "%s:%s" % (rev, path))
    if rc != 0:
        return "ABSENT", "unreadable at %s:%s" % (rev[:9], path)
    lines = body.splitlines()
    has_cmd = any(l.startswith("$ ") for l in lines)
    has_exit = any(re.match(r"^exit=\d+", l) for l in lines)
    has_out = any(l.strip() and not l.startswith(("$ ", "exit=", "#")) for l in lines)
    missing = [n for n, ok in (("command", has_cmd), ("output", has_out), ("exit", has_exit)) if not ok]
    if missing:
        return "INCOMPLETE", "missing " + ",".join(missing)
    return "OK", "command+output+exit"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--prose-repo", required=True)
    ap.add_argument("--prose-rev", required=True)
    ap.add_argument("--receipts-repo", required=True)
    ap.add_argument("--receipts-rev", required=True)
    ap.add_argument("paths", nargs="+")
    a = ap.parse_args(argv)

    total = bad = 0
    for path in a.paths:
        rc, body, err = git(a.prose_repo, "show", "%s:%s" % (a.prose_rev, path))
        if rc != 0:
            print("SETUP_ERROR prose %s at %s: %s" % (path, a.prose_rev[:9], err))
            return 2
        for n, line in enumerate(body.splitlines(), 1):
            seen = set()
            for m in RECORDED.finditer(line):
                target = m.group(1).strip()
                rm = RECEIPT_RE.search(target)
                total += 1
                if not rm:
                    bad += 1
                    print("POINTER %s:%d target=%r verdict=PROSE why=names a prose section, not a receipt"
                          % (path, n, target[:70]))
                    continue
                seen.add(rm.group(1))
            if re.search(r"recorded|watch|ran\b|run\b|measured|observed|logged", line, re.I):
                for m in BACKTICK_RECEIPT.finditer(line):
                    seen.add(m.group(1))
            for raw in sorted(seen):
                total += 1
                resolved = resolve_round(path, raw)
                verdict, why = check_receipt(a.receipts_repo, a.receipts_rev, resolved)
                bad += verdict != "OK"
                print("POINTER %s:%d receipt=%s verdict=%s why=%s"
                      % (path, n, resolved, verdict, why))
    print("CHECK79: pointers=%d non_ok=%d verdict=%s" % (total, bad, "FAIL" if bad else "OK"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
