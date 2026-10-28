#!/usr/bin/env python3
"""Round 55 independent control harness, claim C2 (PRED-C2-r55).

    python3 -I r55_ctl_c2.py --repo REPO --rev REV --work DIR [--holdout DIR]

Everything the verdict depends on is read from git objects at --rev of --repo
(`git ls-tree` + `git cat-file`), never from the working tree.  The tool, the 18
committed fixtures, the ctl stubs, fetch/ and (when present at --rev)
fixtures/c2-holdout are exported into a fresh directory under --work; the tool
under test runs every fixture as a child process in a private directory that holds only a copy of the tool and the input
files its argv names (lane-root-relative paths, as in args.json); the ctl stubs run in the exported root.  Stdout bytes and exit
status are compared with each fixture's expected.out / expected.rc.

--holdout DIR (optional) replaces whatever hold-out the rev carries (or supplies
one when the rev has none): its files are copied to
.ufo/waves/round-55/fixtures/c2-holdout/ in the exported tree, so the same
args.json paths resolve.  Its commitment is checked against frozen-tables.json
(read from --rev) c2.holdout_commit_sha256 exactly like an in-rev hold-out.

Output (stdout, one line):
  MADO_R55_C2: rev=<rev> fixtures=<a>/18 holdout=<b>/8 holdout_commit=<ok|bad|absent> controls=<k>/3 verdict=<TARGET_MET|TARGET_MISSED>
Exit: 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error (message on stderr, no line).
"""
import argparse
import hashlib
import json
import os
import resource
import shutil
import signal
import stat
import subprocess
import sys
import tempfile

WAVE = ".ufo/waves/round-55"
TOOL = "tools/mado-kbdopts.py"
EXPORT_PATHS = (
    TOOL,
    WAVE + "/fixtures/c2",
    WAVE + "/ctl",
    WAVE + "/fetch",
    WAVE + "/fixtures/c2-holdout",
    WAVE + "/fixtures/c2-extra",
)
TABLES = WAVE + "/frozen-tables.json"
HOLDOUT_REL = WAVE + "/fixtures/c2-holdout"
COMMITTED_IDS = ["F%02d" % i for i in range(1, 19)]
HOLDOUT_IDS = ["H%02d" % i for i in range(1, 9)]
CONTROLS = ("const-host.py", "empty.py", "lookup-committed.py")
TIMEOUT = 30
MAX_OUT = 64 * 1024 * 1024


class SetupError(Exception):
    pass


def git(repo, *args, stdin=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_OPTIONAL_LOCKS"] = "0"
    p = subprocess.run(["git", "-C", repo, *args], input=stdin, capture_output=True, env=env)
    if p.returncode != 0:
        raise SetupError("git %s failed: %s" % (" ".join(args[:2]), p.stderr.decode("utf-8", "replace").strip()))
    return p.stdout


def resolve_rev(repo, rev):
    try:
        out = git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}").decode().strip()
    except SetupError:
        out = ""
    if len(out) != 40:
        raise SetupError("rev does not resolve to a commit: %s" % rev)
    return out


def export_paths(repo, commit, dest):
    """Export regular blobs under EXPORT_PATHS at `commit` into `dest`. Returns set of exported rel paths."""
    raw = git(repo, "ls-tree", "-r", "-z", "--full-tree", commit, "--", *EXPORT_PATHS)
    entries = []
    for rec in raw.split(b"\0"):
        if not rec:
            continue
        meta, _, path = rec.partition(b"\t")
        mode, otype, sha = meta.decode().split()
        path = path.decode("utf-8", "surrogateescape")
        if otype != "blob" or mode not in ("100644", "100755", "120000"):
            continue
        if not any(path == p or path.startswith(p + "/") for p in EXPORT_PATHS):
            continue
        parts = path.split("/")
        if ".." in parts or path.startswith("/"):
            raise SetupError("unsafe path in tree: %r" % path)
        entries.append((path, sha))
    exported = set()
    if not entries:
        return exported
    batch = ("".join(sha + "\n" for _, sha in entries)).encode()
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    p = subprocess.run(["git", "-C", repo, "cat-file", "--batch"], input=batch, capture_output=True, env=env)
    if p.returncode != 0:
        raise SetupError("git cat-file --batch failed: " + p.stderr.decode("utf-8", "replace").strip())
    data, pos = p.stdout, 0
    for path, sha in entries:
        nl = data.index(b"\n", pos)
        head = data[pos:nl].decode().split()
        if len(head) != 3 or head[0] != sha or head[1] != "blob":
            raise SetupError("cat-file batch desync at %s: %r" % (path, head))
        size = int(head[2])
        body = data[nl + 1:nl + 1 + size]
        pos = nl + 1 + size + 1
        target = os.path.join(dest, *path.split("/"))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as fh:  # symlink blobs become plain files holding the link text
            fh.write(body)
        exported.add(path)
    return exported


def read_blob(repo, commit, path):
    try:
        return git(repo, "cat-file", "blob", "%s:%s" % (commit, path))
    except SetupError:
        return None


def holdout_commitment(root):
    """sha256 over sorted rel-path files of `<relpath>\\0<sha256 of bytes>\\n`."""
    rels = []
    for dp, dns, fns in os.walk(root):
        for fn in fns:
            rels.append(os.path.relpath(os.path.join(dp, fn), root).replace(os.sep, "/"))
    h = hashlib.sha256()
    for rel in sorted(rels, key=lambda s: s.encode("utf-8", "surrogateescape")):
        fb = open(os.path.join(root, *rel.split("/")), "rb").read()
        h.update(rel.encode("utf-8", "surrogateescape") + b"\0" + hashlib.sha256(fb).hexdigest().encode() + b"\n")
    return h.hexdigest()


def _limits():
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_OUT, MAX_OUT))
    os.setsid()


def run_prog(prog, args, cwd, work, env):
    """Run `python3 -I prog args` -> (rc|None, stdout bytes). rc None = timeout / spawn failure."""
    with tempfile.TemporaryFile(dir=work) as so, tempfile.TemporaryFile(dir=work) as se:
        try:
            p = subprocess.Popen([sys.executable, "-I", prog, *args], cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                 stdout=so, stderr=se, preexec_fn=_limits)
        except OSError:
            return None, b""
        try:
            rc = p.wait(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except OSError:
                pass
            p.wait()
            return None, b""
        try:  # reap stragglers in the child's process group
            os.killpg(p.pid, signal.SIGKILL)
        except OSError:
            pass
        so.seek(0)
        return rc, so.read()


def load_fixture(fdir):
    try:
        args = json.load(open(os.path.join(fdir, "args.json"), "rb"))
        want_out = open(os.path.join(fdir, "expected.out"), "rb").read()
        want_rc = int(open(os.path.join(fdir, "expected.rc"), "rb").read().decode().strip())
    except (OSError, ValueError):
        return None
    if not isinstance(args, list) or not all(isinstance(a, str) for a in args):
        return None
    return args, want_out, want_rc


def run_isolated(prog, args, tree, work, env):
    """Run the tool under test in a private directory holding ONLY a copy of the tool and the input files its argv names
    (paths relative to the exported lane root). It cannot read expected.*, args.json, other fixtures or the ctl stubs
    from beside its inputs or from its own location (R55CritHoldout D1/D2, R55CritControls: sibling-read and
    export-root lookup attacks). A hostile tool can still scan the filesystem outside the run directory; that stays a
    declared limit of this harness."""
    rd = tempfile.mkdtemp(prefix="run-", dir=work)  # `work` is a sibling of the export root, not inside its ancestry (R55W2CritToolIsolation FIX-A2/A3/A8)
    try:
        env = dict(env, TMPDIR=rd)
        dst = os.path.join(rd, "tools", os.path.basename(prog))
        os.makedirs(os.path.dirname(dst))
        shutil.copyfile(prog, dst)
        for a in args:
            if a.startswith("--"):
                continue
            src = os.path.join(tree, *a.split("/"))
            if os.path.isfile(src) and not os.path.islink(src):
                tp = os.path.join(rd, *a.split("/"))
                os.makedirs(os.path.dirname(tp), exist_ok=True)
                shutil.copyfile(src, tp)
        return run_prog(dst, args, rd, work, env)
    finally:
        shutil.rmtree(rd, ignore_errors=True)


def score(prog, ids, froot, tree, work, env, isolate=False):
    """Return (passed_count, failed_ids). Only the named ids count; a missing fixture dir fails. isolate=True runs the
    program in a private input-only directory (the tool under test); the ctl stubs run in the exported tree."""
    if not os.path.isfile(prog):
        return 0, list(ids)
    passed, failed = 0, []
    for fid in ids:
        fx = load_fixture(os.path.join(froot, fid))
        if fx is None:
            failed.append(fid)
            continue
        args, want_out, want_rc = fx
        if isolate:
            rc, out = run_isolated(prog, args, tree, work, env)
        else:
            rc, out = run_prog(prog, args, tree, work, env)
        if rc is not None and rc == want_rc and out == want_out:
            passed += 1
        else:
            failed.append(fid)
    return passed, failed


def run(argv):
    ap = argparse.ArgumentParser(prog="r55_ctl_c2.py", add_help=False, allow_abbrev=False)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--holdout", default=None)
    try:
        a = ap.parse_args(argv)
    except SystemExit:
        sys.stderr.write("usage: r55_ctl_c2.py --repo REPO --rev REV --work DIR [--holdout DIR]\n")
        return 2
    scratch = None
    runs = None
    try:
        repo = os.path.abspath(a.repo)
        work = os.path.abspath(a.work)
        os.makedirs(work, exist_ok=True)
        commit = resolve_rev(repo, a.rev)
        scratch = tempfile.mkdtemp(prefix="c2-", dir=work)
        tree = os.path.join(scratch, "root")
        runs = tempfile.mkdtemp(prefix="c2runs-", dir=work)  # outside `scratch`, so a tool walking up from its run dir does not meet the export
        os.makedirs(tree)
        export_paths(repo, commit, tree)
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "TMPDIR": runs, "LC_ALL": "C.UTF-8",
               "PYTHONHASHSEED": "0"}

        # --- hold-out: from --holdout DIR (override) or at --rev
        hroot = os.path.join(tree, *HOLDOUT_REL.split("/"))
        if a.holdout is not None:
            src = os.path.abspath(a.holdout)
            if not os.path.isdir(src):
                raise SetupError("--holdout is not a directory: %s" % a.holdout)
            if os.path.isdir(hroot):
                shutil.rmtree(hroot)
            for dp, dns, fns in os.walk(src, followlinks=False):
                for fn in fns:
                    sp = os.path.join(dp, fn)
                    if not stat.S_ISREG(os.lstat(sp).st_mode):
                        raise SetupError("non-regular file in --holdout: %s" % sp)
                    rel = os.path.relpath(sp, src)
                    tp = os.path.join(hroot, rel)
                    os.makedirs(os.path.dirname(tp), exist_ok=True)
                    shutil.copyfile(sp, tp)
            os.makedirs(hroot, exist_ok=True)
        if not os.path.isdir(hroot):
            holdout_commit = "absent"
        else:
            tables = read_blob(repo, commit, TABLES)
            expected = None
            if tables is None:
                sys.stderr.write("r55_ctl_c2: %s unreadable at rev; commitment cannot match\n" % TABLES)
            else:
                try:
                    v = json.loads(tables)["c2"]["holdout_commit_sha256"]
                    expected = v if isinstance(v, str) else None
                except (ValueError, KeyError, TypeError):
                    sys.stderr.write("r55_ctl_c2: c2.holdout_commit_sha256 missing in frozen-tables.json\n")
            holdout_commit = "ok" if expected is not None and holdout_commitment(hroot) == expected else "bad"

        wave = os.path.join(tree, *WAVE.split("/"))
        croot = os.path.join(wave, "fixtures", "c2")
        tool = os.path.join(tree, *TOOL.split("/"))

        if holdout_commit == "absent":
            hid_present = []
        else:
            hid_present = HOLDOUT_IDS
        fa, ffail = score(tool, COMMITTED_IDS, croot, tree, runs, env, isolate=True)
        hb, hfail = score(tool, hid_present, hroot, tree, runs, env, isolate=True) if hid_present else (0, list(HOLDOUT_IDS))

        # --- extra regression fixtures (informational only, NOT part of PRED-C2-r55): hand-derived by wave-2 mutation testers
        eroot = os.path.join(wave, "fixtures", "c2-extra")
        if os.path.isdir(eroot):
            eids = sorted(d for d in os.listdir(eroot) if os.path.isdir(os.path.join(eroot, d)))
            ea, efail = score(tool, eids, eroot, tree, runs, env, isolate=True)
            sys.stderr.write("r55_ctl_c2: extra fixtures (informational) %d/%d%s\n" % (ea, len(eids), (" failed: " + ",".join(efail)) if efail else ""))

        # --- controls: each stub run over every fixture the harness has (committed + hold-out when present)
        ctl_ok = 0
        ctl_notes = []
        for name in CONTROLS:
            prog = os.path.join(wave, "ctl", name)
            c_com, _ = score(prog, COMMITTED_IDS, croot, tree, runs, env)
            c_hold, _ = score(prog, hid_present, hroot, tree, runs, env) if hid_present else (0, [])
            if name == "const-host.py":
                good = c_com + c_hold <= 1
            elif name == "empty.py":
                good = c_com + c_hold == 0
            else:
                good = c_com == 18 and c_hold == 0
            ctl_notes.append("%s:%d+%d:%s" % (name, c_com, c_hold, "ok" if good else "BAD"))
            ctl_ok += 1 if good else 0

        met = fa == 18 and hb == 8 and holdout_commit == "ok" and ctl_ok == 3
        if ffail:
            sys.stderr.write("r55_ctl_c2: failed committed fixtures: %s\n" % ",".join(ffail))
        if hfail and holdout_commit != "absent":
            sys.stderr.write("r55_ctl_c2: failed hold-out fixtures: %s\n" % ",".join(hfail))
        sys.stderr.write("r55_ctl_c2: controls %s\n" % " ".join(ctl_notes))
        sys.stdout.write("MADO_R55_C2: rev=%s fixtures=%d/18 holdout=%d/8 holdout_commit=%s controls=%d/3 verdict=%s\n"
                         % (a.rev, fa, hb, holdout_commit, ctl_ok, "TARGET_MET" if met else "TARGET_MISSED"))
        sys.stdout.flush()
        return 0 if met else 1
    except SetupError as e:
        sys.stderr.write("r55_ctl_c2: setup error: %s\n" % e)
        return 2
    except OSError as e:
        sys.stderr.write("r55_ctl_c2: setup error: %s\n" % e)
        return 2
    finally:
        if scratch is not None:
            shutil.rmtree(scratch, ignore_errors=True)
        if runs is not None:
            shutil.rmtree(runs, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
