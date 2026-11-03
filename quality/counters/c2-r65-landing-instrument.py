#!/usr/bin/env python3
"""PRED-C2-r65 - the landing-counters standing instrument is admitted at --rev.

Frozen contract (`.ufo/waves/round-65/claims-declaration-r65.md`, claim C2; seat
R65ExecC2Counter). Frozen line, printed once on stdout:

    MADO_R65_INSTRUMENT: selftest=<rc> landing=<rc> green=<yes|no> \
        verdict=TARGET_MET|TARGET_MISSED rev=<rev>

TARGET_MET (exit 0) iff, from bytes committed at <rev>:
  (1) `quality/landing-counters.sh` exists at <rev> (`git ls-tree --name-only` names exactly
      one path);
  (2) the instrument and its three named dependencies (quality/check-tool-ledger.py,
      quality/counters/c3-r56-used-by.py, tools/mado-receipt-citecheck.py) extract intact,
      preserving repo-relative paths, into `<scratch>/c2r65-<pid>/wt`;
  (3) `bash <wt>/quality/landing-counters.sh --selftest --scratch-root <work>/st` exits 0;
  (4) `bash <wt>/quality/landing-counters.sh --repo <abs repo> --rev <rev> --scratch-root
      <work>/run` exits 0 and its stdout carries `MADO_LANDING_COUNTERS: GREEN`.

Absence is fail-closed and names the measured state: at base 524fa1f9 the instrument is
absent and the command prints
    MADO_R65_INSTRUMENT: instrument=absent verdict=TARGET_MISSED rev=<rev> rc=1
and exits 1.  Extraction that is incomplete at <rev> likewise fails closed:
    MADO_R65_INSTRUMENT: reason=extraction-incomplete missing=<paths> verdict=TARGET_MISSED \
        rev=<rev>
and exits 1.

Scratch policy (`--scratch-root` is REQUIRED): the argument is resolved to its real path; a
root under /tmp or /var/tmp, or one that is itself a symlink, is refused before anything is
created (exit 2, one line on stderr).  The work dir `<scratch>/c2r65-<pid>/` is created here
and removed in a finally block.  The frozen landing log lives at `<work>/landing.log`; because
the work dir is removed, the two legs' outputs are also retained as evidence sidecars under
the caller's own scratch root (`c2r65-<pid>.selftest.log`, `c2r65-<pid>.landing.log`, plus
`.landing.err.log` only when that leg wrote stderr).  Nothing is written outside the scratch
root; no TMPDIR/mktemp use, no network, and no child process beyond `git`, `tar` and the two
instrument invocations.  Every producer's own rc is captured (QUALITY 26).
"""
import argparse
import os
import shutil
import subprocess
import sys

# Frozen dependency set, in extraction order (the instrument first).
REQUIRED = (
    "quality/landing-counters.sh",
    "quality/check-tool-ledger.py",
    "quality/counters/c3-r56-used-by.py",
    "tools/mado-receipt-citecheck.py",
)
INSTRUMENT = REQUIRED[0]
GREEN = b"MADO_LANDING_COUNTERS: GREEN"
REFUSED_ROOTS = ("/tmp", "/var/tmp")
LEG_TIMEOUT = 1800  # seconds per instrument invocation; a hung leg is rc=124

# Ambient GIT_* variables (GIT_DIR, GIT_WORK_TREE, ...) must not steer object reads away
# from the repo named by --repo: they are stripped from the git calls AND from every leg
# child (round-65 critic B4). The legs otherwise keep the caller's environment.
GIT_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def die(message):
    """Setup refusal: one clear stderr line, no verdict, exit 2."""
    sys.stderr.write("MADO_R65_INSTRUMENT: %s\n" % message)
    raise SystemExit(2)


def git(repo, *args):
    try:
        return subprocess.run(["git", "-C", repo, *args], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, env=GIT_ENV)
    except OSError as exc:
        die("git unavailable: %s" % exc)


def under(path, root):
    root = os.path.realpath(root)
    return path == root or path.startswith(root + os.sep)


def prepare_scratch(raw):
    """Resolve and validate --scratch-root; create it when missing."""
    raw = raw.rstrip("/") or raw
    if os.path.islink(raw):
        die("scratch-root refused: path is itself a symlink: %s" % raw)
    real = os.path.realpath(raw)
    for root in REFUSED_ROOTS:
        if under(real, root):
            die("scratch-root refused: /tmp-family root: %s (real path %s)" % (raw, real))
    try:
        os.makedirs(real, exist_ok=True)
    except OSError as exc:
        die("scratch-root refused: cannot create %s: %s" % (real, exc.strerror or exc))
    if not os.path.isdir(real):
        die("scratch-root refused: not a directory: %s" % real)
    if not os.access(real, os.W_OK | os.X_OK):
        die("scratch-root refused: not writable: %s" % real)
    return real


def make_work(scratch):
    work = os.path.join(scratch, "c2r65-%d" % os.getpid())
    if os.path.lexists(work):
        shutil.rmtree(work, ignore_errors=True)
    try:
        os.makedirs(os.path.join(work, "wt"))
    except OSError as exc:
        die("work-dir refused: cannot create %s: %s" % (work, exc.strerror or exc))
    return work


def run_leg(argv, cwd):
    """Run one instrument invocation; never raise on child failure or timeout."""
    try:
        proc = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=LEG_TIMEOUT, env=GIT_ENV)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        note = b"\nleg exceeded %d s and was killed\n" % LEG_TIMEOUT
        return 124, exc.stdout or b"", (exc.stderr or b"") + note
    except OSError as exc:
        return 127, b"", ("cannot execute %s: %s\n" % (argv[0], exc)).encode("utf-8")


def last_line(*blobs):
    for blob in blobs:
        lines = [ln for ln in blob.decode("utf-8", "replace").splitlines() if ln.strip()]
        if lines:
            return lines[-1].strip()
    return ""


def write_bytes(path, data):
    with open(path, "wb") as handle:
        handle.write(data)


def retain_evidence(work, scratch):
    """Copy the legs' outputs under the caller's scratch root before the work dir dies."""
    pid = os.getpid()
    copies = (
        ("selftest.log", "c2r65-%d.selftest.log" % pid),
        ("landing.log", "c2r65-%d.landing.log" % pid),
        ("landing.err.log", "c2r65-%d.landing.err.log" % pid),
    )
    for src_name, dst_name in copies:
        src = os.path.join(work, src_name)
        if not os.path.isfile(src):
            continue
        with open(src, "rb") as handle:
            data = handle.read()
        if src_name.endswith(".err.log") and not data.strip():
            continue
        write_bytes(os.path.join(scratch, dst_name), data)


def fail_incomplete(rev, missing, note):
    if missing:
        listing = ",".join(missing)
    else:
        listing = "none"
    sys.stderr.write("MADO_R65_INSTRUMENT: extraction diagnostic: %s\n" % note)
    print("MADO_R65_INSTRUMENT: reason=extraction-incomplete missing=%s "
          "verdict=TARGET_MISSED rev=%s" % (listing, rev))
    return 1


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="PRED-C2-r65: run the committed landing-counters instrument at a revision.")
    parser.add_argument("--repo", default=".", help="git repository to read (default: .)")
    parser.add_argument("--rev", required=True, help="revision whose committed bytes are scored")
    parser.add_argument("--scratch-root", required=True,
                        help="caller-declared scratch root (never /tmp or /var/tmp)")
    args = parser.parse_args(argv)

    repo = os.path.realpath(args.repo)
    scratch = prepare_scratch(args.scratch_root)
    work = make_work(scratch)
    try:
        # (1) Instrument presence at the scored revision (object read; never the worktree).
        tree = git(repo, "ls-tree", "--name-only", args.rev, "--", INSTRUMENT)
        names = tree.stdout.decode("utf-8", "replace").splitlines()
        if tree.returncode != 0 or len(names) != 1:
            detail = tree.stderr.decode("utf-8", "replace").strip()
            if detail:
                sys.stderr.write("MADO_R65_INSTRUMENT: ls-tree rc=%d: %s\n"
                                 % (tree.returncode, detail))
            print("MADO_R65_INSTRUMENT: instrument=absent verdict=TARGET_MISSED rev=%s rc=1"
                  % args.rev)
            return 1

        # (2) Extract the instrument and its named dependencies at --rev.
        wt = os.path.join(work, "wt")
        archive = git(repo, "archive", "--format=tar", args.rev, "--", *REQUIRED)
        if archive.returncode != 0:
            missing = [p for p in REQUIRED
                       if git(repo, "cat-file", "-e", "%s:%s" % (args.rev, p)).returncode != 0]
            return fail_incomplete(args.rev, missing,
                                   "git archive rc=%d" % archive.returncode)
        try:
            untar = subprocess.run(["tar", "-x", "-C", wt], input=archive.stdout,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   timeout=LEG_TIMEOUT)
            tar_rc, tar_err = untar.returncode, untar.stderr
        except subprocess.TimeoutExpired:
            tar_rc, tar_err = 124, b"tar exceeded %d s\n" % LEG_TIMEOUT
        except OSError as exc:
            tar_rc, tar_err = 127, ("cannot execute tar: %s\n" % exc).encode("utf-8")
        missing = [p for p in REQUIRED if not os.path.isfile(os.path.join(wt, p))]
        if tar_rc != 0 or missing:
            note = "tar rc=%d%s" % (tar_rc, (": " + tar_err.decode("utf-8", "replace").strip())
                                    if tar_err.strip() else "")
            return fail_incomplete(args.rev, missing, note)

        instrument = os.path.join(wt, INSTRUMENT)
        # (3) Selftest leg: hermetic, scratch under <work>/st.
        st_rc, st_out, st_err = run_leg(
            ["bash", instrument, "--selftest", "--scratch-root", os.path.join(work, "st")],
            cwd=work)
        log = ("# cmd: bash %s --selftest --scratch-root %s\n# rc: %d\n# last: %s\n"
               % (instrument, os.path.join(work, "st"), st_rc,
                  last_line(st_out, st_err))).encode("utf-8")
        log += st_out
        if st_err.strip():
            log += b"\n--- stderr ---\n" + st_err
        write_bytes(os.path.join(work, "selftest.log"), log)

        # (4) Landing leg: the full four-leg run, stdout kept verbatim.
        lg_rc, lg_out, lg_err = run_leg(
            ["bash", instrument, "--repo", repo, "--rev", args.rev,
             "--scratch-root", os.path.join(work, "run")], cwd=work)
        write_bytes(os.path.join(work, "landing.log"), lg_out)
        if lg_err.strip():
            write_bytes(os.path.join(work, "landing.err.log"), lg_err)

        # (5) Verdict: every leg's own rc AND the committed GREEN token.
        green = GREEN in lg_out
        met = st_rc == 0 and lg_rc == 0 and green
        print("MADO_R65_INSTRUMENT: selftest=%d landing=%d green=%s verdict=%s rev=%s"
              % (st_rc, lg_rc, "yes" if green else "no",
                 "TARGET_MET" if met else "TARGET_MISSED", args.rev))
        return 0 if met else 1
    finally:
        try:
            retain_evidence(work, scratch)
        except OSError as exc:
            sys.stderr.write("MADO_R65_INSTRUMENT: evidence-retention failed: %s\n" % exc)
        shutil.rmtree(work, ignore_errors=True)
        if os.path.exists(work):
            sys.stderr.write("MADO_R65_INSTRUMENT: cleanup failed, work dir remains: %s\n" % work)


if __name__ == "__main__":
    sys.exit(main())
