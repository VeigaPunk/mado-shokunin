#!/usr/bin/env python3
"""Score the round-47 do-nothing/cheat controls against a counter draft.

    run-controls.py --counter C --work DIR [--claim C1|C2] [--lane DIR] [--base REV]
                    [--nonce N] [--reference PATH] [--dry-run] [--keep]

For every control in c1/ (each a tools/mado-terminal.py candidate) or c2/ (each a bundle of
files/appends), the runner commits it on its own clone of the lane at the round base and runs the
counter on that revision, so a control can never touch the lane.  Stdout is two shapes only:

    CTL_C1 <name> <TARGET_MET|TARGET_MISSED|SETUP_FAIL>
    CTL_C1 VERDICT: PASS|FAIL (controls scoring TARGET_MET: k of n; reference met: 0|1)

(CTL_C2 for the C2 bundle set.)  PASS means every cheat control was rejected *and* the positive
control was admitted.  Per-control counter output is kept in DIR/out-<name>.txt.

The counter is called with the round-46 interface --repo/--rev/--work/--nonce (C1) or
--repo/--rev/--work plus --base when the counter offers it (C2); options the counter's --help does
not list are not passed, and any extra argument can be added with --counter-arg.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
DEFAULT_BASE = "60edb66e2f1cb90acc6e9442fc93ded0ca42d750"

# Which controls are expected to be rejected.  The positive control is scored separately and is
# what "reference met" reports.
C1_EXPECT_MISS = [
    "STUB", "CONST", "DELEGATE", "SUBPROC", "EMBED-SH", "CTYPES-EXEC", "FIRSTLINE",
    "NOVALIDATE", "NODESKTOP", "REVERSED-DIRS", "CACHE-READ", "SELFTEST-LIE", "FIXTURE-READ",
    "TYPE-CHECK",
]
C2_EXPECT_MISS = ["BASE", "EMPTY", "FORGED-QUOTE", "BRANCH-URL", "INDEX-NOT-CHAIN",
                  "RECEIPT-ABSENT"]


def run(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)


def git(clone, *args):
    return run(["git", "-C", clone] + list(args))


def clone_at(lane, base, dest):
    shutil.rmtree(dest, ignore_errors=True)
    proc = run(["git", "clone", "-q", "--shared", "--no-checkout", lane, dest])
    if proc.returncode != 0:
        raise SystemExit("clone failed: %s" % proc.stderr.strip())
    top = git(dest, "rev-parse", "--show-toplevel").stdout.strip()
    if os.path.realpath(top) != os.path.realpath(dest):
        raise SystemExit("clone toplevel %r is not %r" % (top, dest))
    proc = git(dest, "checkout", "-q", "--detach", base)
    if proc.returncode != 0:
        raise SystemExit("checkout %s failed: %s" % (base, proc.stderr.strip()))
    return dest


def commit(clone, message):
    git(clone, "add", "-A")
    proc = git(clone, "-c", "user.name=controls-seat",
               "-c", "user.email=controls@scratch.invalid", "commit", "-q", "-m", message)
    if proc.returncode != 0:
        raise SystemExit("commit failed: %s" % proc.stderr.strip())
    return git(clone, "rev-parse", "HEAD").stdout.strip()


def counter_help(counter):
    proc = run([sys.executable, "-I", counter, "--help"])
    return proc.stdout + proc.stderr


def counter_options(counter):
    text = counter_help(counter)
    opts = set()
    for token in text.replace("=", " ").split():
        if token.startswith("--"):
            opts.add(token.split()[0].strip("',"))
    return opts


def counter_argv(counter, claim, repo, work, base, nonce, extra):
    """Only pass options the counter's --help advertises (the C2 counter takes no --work)."""
    have = counter_options(counter)
    argv = [sys.executable, "-I", counter]
    if "--repo" in have:
        argv += ["--repo", repo]
    if "--rev" in have:
        argv += ["--rev", "HEAD"]
    if "--work" in have:
        argv += ["--work", work]
    if claim == "C1" and "--nonce" in have:
        argv += ["--nonce", str(nonce)]
    if "--base" in have:
        argv += ["--base", base]
    argv += extra
    return argv


def verdict_of(proc):
    """The last `verdict=` token wins; the exit status decides when the counter never got there
    (0 met, 1 missed, 2 setup error in both round-47 drafts)."""
    import re
    text = (proc.stdout or "") + "\n" + (proc.stderr or "")
    for line in reversed(text.splitlines()):
        m = re.search(r"verdict=(TARGET_MET|TARGET_MISSED|MISSED)", line)
        if m:
            return "TARGET_MET" if m.group(1) == "TARGET_MET" else "TARGET_MISSED"
    if proc.returncode == 2:
        return "SETUP_FAIL"
    if proc.returncode == 0:
        return "TARGET_MET"
    if proc.returncode == 1:
        return "TARGET_MISSED"
    return "SETUP_FAIL"


def score_c1(args, controls, reference):
    results = []
    out_dir = args.work
    os.makedirs(out_dir, exist_ok=True)
    names = list(controls)
    if reference:
        names.append("REFERENCE")
    for i, name in enumerate(names):
        repo = os.path.join(args.work, "clone-%s" % name.replace("/", "_"))
        work = os.path.join(args.work, "w-%s" % name.replace("/", "_"))
        os.makedirs(work, exist_ok=True)
        src = reference if name == "REFERENCE" else controls[name]
        if args.dry_run:
            print("# C1 %s: cp %s -> %s/tools/mado-terminal.py; %s"
                  % (name, src, repo, " ".join(counter_argv(args.counter, "C1", repo, work,
                                                             args.base, args.nonce,
                                                             args.counter_arg))))
            continue
        clone = clone_at(args.lane, args.base, repo)
        os.makedirs(os.path.join(clone, "tools"), exist_ok=True)
        shutil.copyfile(src, os.path.join(clone, "tools", "mado-terminal.py"))
        os.chmod(os.path.join(clone, "tools", "mado-terminal.py"), 0o755)
        rev = commit(clone, "control %s" % name)
        argv = counter_argv(args.counter, "C1", clone, work, args.base, args.nonce,
                            args.counter_arg)
        proc = run(argv)
        verdict = verdict_of(proc)
        with open(os.path.join(out_dir, "out-%s.txt" % name.replace("/", "_")), "w") as fh:
            fh.write("$ %s\nrev=%s\n%s\n--- stderr\n%s\n"
                     % (" ".join(argv), rev, proc.stdout, proc.stderr))
        results.append((name, verdict))
        if not args.keep:
            shutil.rmtree(clone, ignore_errors=True)
    return results


def apply_bundle(bundle, clone):
    files = os.path.join(bundle, "files")
    if os.path.isdir(files):
        for base, _dirs, names in os.walk(files):
            for name in names:
                src = os.path.join(base, name)
                rel = os.path.relpath(src, files)
                dest = os.path.join(clone, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copyfile(src, dest)
    appends = os.path.join(bundle, "append")
    if os.path.isdir(appends):
        for base, _dirs, names in os.walk(appends):
            for name in names:
                src = os.path.join(base, name)
                rel = os.path.relpath(src, appends)
                dest = os.path.join(clone, rel)
                with open(src, "r", encoding="utf-8") as fh:
                    text = fh.read()
                with open(dest, "a", encoding="utf-8") as fh:
                    fh.write(text)


def score_c2(args, bundles, reference):
    results = []
    os.makedirs(args.work, exist_ok=True)
    items = [(name, bundles[name]) for name in bundles]
    if reference:
        items.append(("REFERENCE", reference))
    for name, bundle in items:
        repo = os.path.join(args.work, "clone-%s" % name)
        work = os.path.join(args.work, "w-%s" % name)
        os.makedirs(work, exist_ok=True)
        if args.dry_run:
            print("# C2 %s: copy %s -> %s; %s"
                  % (name, bundle, repo,
                     " ".join(counter_argv(args.counter, "C2", repo, work, args.base,
                                           args.nonce, args.counter_arg))))
            continue
        clone = clone_at(args.lane, args.base, repo)
        apply_bundle(bundle, clone)
        rev = commit(clone, "control %s" % name)
        argv = counter_argv(args.counter, "C2", clone, work, args.base, args.nonce,
                            args.counter_arg)
        proc = run(argv)
        verdict = verdict_of(proc)
        with open(os.path.join(args.work, "out-%s.txt" % name), "w") as fh:
            fh.write("$ %s\nrev=%s\n%s\n--- stderr\n%s\n"
                     % (" ".join(argv), rev, proc.stdout, proc.stderr))
        results.append((name, verdict))
        if not args.keep:
            shutil.rmtree(clone, ignore_errors=True)
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--claim", choices=("C1", "C2", "auto"), default="auto")
    ap.add_argument("--lane", default=DEFAULT_LANE)
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--nonce", type=int, default=47)
    ap.add_argument("--reference", default=None,
                    help="positive-control candidate (C1: a mado-terminal.py; C2: a bundle dir)")
    ap.add_argument("--controls", default=HERE,
                    help="directory holding c1/ and c2/ (default: this script's directory)")
    ap.add_argument("--counter-arg", action="append", default=[],
                    help="extra counter argument (repeatable)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--keep", action="store_true", help="keep the per-control clones")
    args = ap.parse_args()

    if not os.path.isfile(args.counter):
        sys.stderr.write("run-controls: no counter at %s\n" % args.counter)
        return 2
    base_name = os.path.basename(args.counter)
    claim = args.claim
    if claim == "auto":
        claim = "C2" if base_name.startswith("c2") else ("C1" if base_name.startswith("c1")
                                                         else None)
        if claim is None:
            sys.stderr.write("run-controls: cannot infer the claim from %r; pass --claim\n"
                             % base_name)
            return 2
    if git(args.lane, "cat-file", "-e", args.base).returncode != 0:
        sys.stderr.write("run-controls: base %s is not in %s\n" % (args.base, args.lane))
        return 2

    os.makedirs(args.work, exist_ok=True)

    if claim == "C1":
        cdir = os.path.join(args.controls, "c1")
        controls = {}
        for name in C1_EXPECT_MISS:
            path = os.path.join(cdir, name + ".py")
            if not os.path.isfile(path):
                sys.stderr.write("run-controls: missing control %s\n" % path)
                return 2
            controls[name] = path
        reference = args.reference or os.path.join(cdir, "REF-MINI.py")
        if not args.dry_run and not os.path.isfile(reference):
            reference = None
        results = score_c1(args, controls, reference)
        prefix = "CTL_C1"
        expect = C1_EXPECT_MISS
    else:
        cdir = os.path.join(args.controls, "c2")
        bundles = {}
        for name in C2_EXPECT_MISS:
            path = os.path.join(cdir, name)
            if not os.path.isdir(path):
                sys.stderr.write("run-controls: missing bundle %s\n" % path)
                return 2
            bundles[name] = path
        reference = args.reference or os.path.join(cdir, "REF")
        if not args.dry_run and not os.path.isdir(reference):
            reference = None
        results = score_c2(args, bundles, reference)
        prefix = "CTL_C2"
        expect = C2_EXPECT_MISS

    if args.dry_run:
        return 0

    bad = 0
    total = 0
    reference_met = 0
    setup_failed = 0
    lines = []
    for name, verdict in results:
        lines.append("%s %s %s" % (prefix, name, verdict))
        if name == "REFERENCE":
            reference_met = 1 if verdict == "TARGET_MET" else 0
            continue
        total += 1
        if verdict == "TARGET_MET":
            bad += 1
        if verdict == "SETUP_FAIL":
            setup_failed += 1
    for line in lines:
        print(line)
    ok = bad == 0 and reference_met == 1 and setup_failed == 0
    print("%s VERDICT: %s (controls scoring TARGET_MET: %d of %d; reference met: %d)"
          % (prefix, "PASS" if ok else "FAIL", bad, total, reference_met))
    with open(os.path.join(args.work, "run-controls.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
        fh.write("%s VERDICT: %s (controls scoring TARGET_MET: %d of %d; reference met: %d)\n"
                 % (prefix, "PASS" if ok else "FAIL", bad, total, reference_met))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
