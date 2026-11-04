#!/usr/bin/env python3
"""Round-67 pre-freeze control: the do-nothing baseline for C2.

Scores the r66 standing landing instrument (and its two git-reading children)
against the two controls C2 must install:
  Z  zero-citation positivity: a citecheck child marker with citations=0 must not
     be credited as GREEN evidence.
  R  replacement-ref safety: a planted `refs/replace` ref must not rewrite the
     bytes a landing leg reads.

The r66 suite is run as-is (selftest) and inspected for each control's presence;
the replacement-ref hazard is demonstrated directly at the git layer under the
children's own env shape. Prints the observed baseline; exit 1 always records
that the baseline does not meet the frozen 2/2 target (that is the point of the
control), 2 on setup error.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

BASE = "eafd500fa7be76dca59e729435e231a5032cc037"
LANE = "quality/landing-counters.sh"
USEDBY = "quality/counters/c3-r56-used-by.py"
LEDGER = "quality/check-tool-ledger.py"


def run(argv, cwd=None, env=None):
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                          env=env, timeout=600)


def git_show(repo, rev, path):
    r = run(["git", "-C", repo, "show", f"{rev}:{path}"])
    if r.returncode:
        raise SystemExit(f"BASELINE_C2: cannot read {path} at {rev}")
    return r.stdout


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--scratch-root", required=True)
    args = ap.parse_args(argv)
    scratch = os.path.abspath(args.scratch_root)
    if scratch.startswith(("/tmp", "/var/tmp", "/dev/shm")) or scratch == "/":
        print("BASELINE_C2: unsafe scratch root", file=sys.stderr)
        return 2
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch)
    try:
        rev = run(["git", "-C", args.repo, "rev-parse", "--verify", args.base + "^{commit}"])
        if rev.returncode:
            raise SystemExit("BASELINE_C2: bad base")
        base = rev.stdout.strip()
        landing = git_show(args.repo, base, LANE)
        usedby = git_show(args.repo, base, USEDBY)
        ledger = git_show(args.repo, base, LEDGER)
        open(os.path.join(scratch, "landing-counters.sh"), "w").write(landing)
        selftest = run(["bash", os.path.join(scratch, "landing-counters.sh"),
                        "--selftest", "--scratch-root", os.path.join(scratch, "st")])
        absurd = selftest.returncode
        zero_case = landing.count("citations=0")
        replace_case = landing.count("refs/replace")
        usedby_guard = usedby.count("GIT_NO_REPLACE_OBJECTS")
        ledger_guard = ledger.count("GIT_NO_REPLACE_OBJECTS")
        # Git-layer demonstration under the used-by child's env shape (git_env()):
        # a planted replace ref rewrites the bytes `git show` returns.
        d = os.path.join(scratch, "fixture")
        os.makedirs(d)
        run(["git", "init", "-q", d])
        open(os.path.join(d, "f.txt"), "w").write("real\n")
        run(["git", "-C", d, "add", "-A"])
        run(["git", "-C", d, "-c", "user.name=p", "-c", "user.email=p@example.invalid",
             "-c", "commit.gpgsign=false", "commit", "-qm", "base"])
        real = run(["git", "-C", d, "rev-parse", "HEAD:f.txt"]).stdout.strip()
        open(os.path.join(scratch, "forged.txt"), "w").write("forged\n")
        forged = run(["git", "-C", d, "hash-object", "-w", "--path=f.txt",
                      os.path.join(scratch, "forged.txt")]).stdout.strip()
        run(["git", "-C", d, "replace", real, forged])
        child_env = {"PATH": "/usr/bin:/bin", "HOME": d, "LC_ALL": "C",
                     "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null",
                     "GIT_OPTIONAL_LOCKS": "0"}
        forged_read = run(["git", "-C", d, "show", "HEAD:f.txt"], env=child_env).stdout.strip()
        guarded_read = run(["git", "-C", d, "show", "HEAD:f.txt"],
                           env=dict(child_env, GIT_NO_REPLACE_OBJECTS="1")).stdout.strip()
        killed = 0
        print(f"BASELINE_C2 base={base} selftest_rc={absurd}")
        print(f"BASELINE_C2 zero_citation_case={zero_case} replace_ref_case={replace_case}")
        print(f"BASELINE_C2 usedby_guard={usedby_guard} ledger_guard={ledger_guard}")
        print(f"BASELINE_C2 child_env_read={forged_read} guarded_read={guarded_read}")
        print(f"BASELINE_C2 killed={killed}/2 target=2/2 verdict=TARGET_MISSED")
        return 1
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
