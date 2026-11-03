#!/usr/bin/env python3
"""PRED-C2-r66: score the committed four-leg landing instrument, not the worktree.

Extract exactly the instrument and its three frozen dependencies from --rev. Run
its selftest and real landing with --round 66 and an explicit receipts path
relative to --repo. TARGET_MET requires both producer rcs zero and the actual
four-leg GREEN contract. Missing artifacts are TARGET_MISSED (1); unsafe setup
is refused (2). Child-marker discrimination belongs to the standing instrument.

Only caller-declared scratch is written. Private work is removed in finally;
selftest/landing stdout and stderr are retained as c2r66-*.log sidecars in that
scratch root. GIT_* is stripped from every child. No archive links are followed.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

REQUIRED = (
    "quality/landing-counters.sh",
    "quality/check-tool-ledger.py",
    "quality/counters/c3-r56-used-by.py",
    "tools/mado-receipt-citecheck.py",
)
INSTRUMENT = REQUIRED[0]
LEG_TIMEOUT = 1800
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
PREFIX = "MADO_R66_INSTRUMENT:"


def die(message):
    sys.stderr.write("%s %s\n" % (PREFIX, message))
    raise SystemExit(2)


def under(path, root):
    return path == root or path.startswith(root + os.sep)


def prepare_scratch(raw):
    # Inspect lexical ancestors before resolving: a symlink must not escape the
    # declared tree, including a symlink followed by a nonexistent suffix.
    absolute = os.path.abspath(raw)
    current = absolute
    while True:
        if os.path.islink(current):
            die("scratch-root refused: symlink component: %s" % current)
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    real = os.path.realpath(absolute)
    if any(under(real, root) for root in ("/tmp", "/var/tmp", "/dev/shm")):
        die("scratch-root refused: tmp-family root: %s" % real)
    try:
        os.makedirs(real, exist_ok=True)
    except OSError as exc:
        die("scratch-root refused: %s" % exc)
    if not os.path.isdir(real) or not os.access(real, os.W_OK | os.X_OK):
        die("scratch-root refused: not a writable directory: %s" % real)
    return real


def git(repo, *args):
    try:
        return subprocess.run(["git", "-C", repo, *args], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=GIT_ENV)
    except OSError as exc:
        die("git unavailable: %s" % exc)


def run_leg(argv, cwd):
    try:
        proc = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=LEG_TIMEOUT, env=GIT_ENV)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or b"", (exc.stderr or b"") + b"\nleg timed out\n"
    except OSError as exc:
        return 127, b"", str(exc).encode("utf-8")


def write_bytes(path, data):
    with open(path, "wb") as handle:
        handle.write(data)


def extract(repo, rev, wt):
    missing = []
    for path in REQUIRED:
        tree = git(repo, "ls-tree", "-z", rev, "--", path)
        entries = tree.stdout.split(b"\0")
        # Only a regular blob at the exact frozen name may become an executable
        # dependency. Writing blobs ourselves avoids archive symlink traversal.
        valid = (tree.returncode == 0 and len(entries) == 2 and not entries[1]
                 and entries[0].split(b"\t", 1)[-1] == path.encode()
                 and entries[0].startswith((b"100644 blob ", b"100755 blob ")))
        if not valid:
            missing.append(path)
            continue
        blob = git(repo, "show", "%s:%s" % (rev, path))
        if blob.returncode:
            missing.append(path)
            continue
        target = os.path.join(wt, path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        write_bytes(target, blob.stdout)
    return missing


def actual_green(out, rev):
    lines = out.splitlines()
    summary = ("MADO_LANDING_COUNTERS: GREEN "
               "(nav=0 usedby=0 ledger=0 citecheck=0 rev=%s)" % rev).encode()
    summaries = [line for line in lines if line.startswith(b"MADO_LANDING_COUNTERS:")]
    return (summaries == [summary]
            and all(lines.count(("LANDING_LEG %s rc=0" % leg).encode()) == 1
                    for leg in ("nav", "usedby", "ledger", "citecheck")))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--rev", required=True)
    parser.add_argument("--scratch-root", required=True)
    args = parser.parse_args(argv)
    if args.rev.startswith("-"):
        die("--rev must not start with '-'")
    repo = os.path.realpath(args.repo)
    scratch = prepare_scratch(args.scratch_root)
    try:
        work = tempfile.mkdtemp(prefix="c2r66-", dir=scratch)
    except OSError as exc:
        die("work-dir refused: %s" % exc)
    evidence = {}
    try:
        wt = os.path.join(work, "wt")
        os.mkdir(wt)
        resolved = git(repo, "rev-parse", "--verify", args.rev + "^{commit}")
        rev = resolved.stdout.decode("ascii", "replace").strip()
        missing = (extract(repo, rev, wt) if resolved.returncode == 0
                   else list(REQUIRED))
        if missing:
            reason = "instrument=absent" if INSTRUMENT in missing else "reason=extraction-incomplete"
            print("%s %s missing=%s verdict=TARGET_MISSED rev=%s rc=1"
                  % (PREFIX, reason, ",".join(missing), args.rev))
            return 1
        instrument = os.path.join(wt, INSTRUMENT)
        receipts = os.path.join(repo, ".ufo", "waves", "round-66", "receipts")
        commands = (
            ("selftest", ["bash", instrument, "--selftest", "--scratch-root",
                          os.path.join(work, "st")]),
            ("landing", ["bash", instrument, "--repo", repo, "--rev", rev,
                         "--round", "66", "--scratch-root", os.path.join(work, "run"),
                         "--citecheck-paths", receipts]),
        )
        results = {}
        for name, command in commands:
            rc, out, err = run_leg(command, work)
            results[name] = (rc, out)
            evidence[name + ".log"] = out
            evidence[name + ".err.log"] = err
            evidence[name + ".command.log"] = (repr(command) + "\nrc=%d\n" % rc).encode()
        st_rc = results["selftest"][0]
        lg_rc, lg_out = results["landing"]
        green = actual_green(lg_out, rev)
        met = st_rc == 0 and lg_rc == 0 and green
        print("%s selftest=%d landing=%d green=%s verdict=%s rev=%s"
              % (PREFIX, st_rc, lg_rc, "yes" if green else "no",
                 "TARGET_MET" if met else "TARGET_MISSED", args.rev))
        return 0 if met else 1
    finally:
        try:
            for name, data in evidence.items():
                target = os.path.join(scratch, os.path.basename(work) + "." + name)
                # Do not overwrite an attacker-precreated evidence symlink.
                with open(target, "xb") as handle:
                    handle.write(data)
        finally:
            shutil.rmtree(work)


if __name__ == "__main__":
    sys.exit(main())
