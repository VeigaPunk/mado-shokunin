#!/usr/bin/env python3
"""Round 56 C2 control harness (registration section C2, PRED-C2-r56).

    python3 -I r56_ctl_c2.py --repo REPO --rev REV --work DIR [--holdout DIR]

Exports (git archive | tar -x, symlinks preserved) the tool, fixtures/c2, the hold-out, ctl/ and frozen-tables.json at REV
into a scratch directory under --work, runs the tool and the three ctl stubs on every fixture as child processes
(`python3 -I <program> <args>`, cwd = export root, scrubbed environment), compares stdout bytes and exit status with
expected.out / expected.rc, recomputes both tree commitments and prints exactly one line:

    MADO_R56_C2: rev=<rev> fixtures=<a>/18 holdout=<b>/8 holdout_commit=<ok|bad|absent> controls=<k>/3 verdict=<...>

Exit 0 on TARGET_MET, 1 on TARGET_MISSED, 2 on a setup error (reason on stderr, nothing on stdout).
The harness reads git objects at REV only (never the working tree); its only writes are under --work (removed before exit).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

TABLES_SHA256 = "d50d2b7b16506c50cb44358d4284e4f0eb0d14e433594d068a0fbe74c5edf9af"
WAVE = ".ufo/waves/round-56"
TOOL = "tools/mado-watchplan.py"
FIXTURES = WAVE + "/fixtures/c2"
HOLDOUT = WAVE + "/fixtures/c2-holdout"
CTL = WAVE + "/ctl"
TABLES = WAVE + "/frozen-tables.json"
COMMITTED_IDS = ["F%02d" % i for i in range(1, 19)]
HOLDOUT_IDS = ["H%02d" % i for i in range(1, 9)]
CONTROLS = ("const-host", "empty", "lookup-committed")
TIMEOUT = 30
SAFE_PATH = "/usr/local/bin:/usr/bin:/bin"


class Setup(Exception):
    pass


def scrubbed_env(work):
    return {"PATH": SAFE_PATH, "HOME": work, "TMPDIR": work, "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}


def git(repo, work, *args, check=True, text=True):
    p = subprocess.run(["git", "-C", repo] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       env=scrubbed_env(work), stdin=subprocess.DEVNULL)
    if check and p.returncode != 0:
        raise Setup("git %s failed: %s" % (" ".join(args[:2]), p.stderr.decode("utf-8", "replace").strip()))
    return p


def ls_entry(repo, work, rev, path):
    """(mode, type) of path at rev, or None when absent."""
    p = git(repo, work, "ls-tree", "-z", "--full-tree", rev, "--", path, check=True)
    for rec in p.stdout.split(b"\0"):
        if not rec:
            continue
        meta, _, name = rec.partition(b"\t")
        if name.decode("utf-8", "surrogateescape") == path:
            mode, typ, _sha = meta.decode().split()
            return mode, typ
    return None


def pipe_tar(src_cmd, dest, env):
    """src_cmd | tar -x -C dest (symlinks preserved, not dereferenced)."""
    p1 = subprocess.Popen(src_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, stdin=subprocess.DEVNULL)
    p2 = subprocess.Popen(["tar", "-x", "--no-same-owner", "-C", dest, "-f", "-"], stdin=p1.stdout,
                          stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=env)
    p1.stdout.close()
    err2 = p2.stderr.read()
    err1 = p1.stderr.read()
    r2 = p2.wait()
    r1 = p1.wait()
    p1.stderr.close()
    p2.stderr.close()
    if r1 != 0 or r2 != 0:
        raise Setup("export failed: %s %s" % (err1.decode("utf-8", "replace").strip(),
                                              err2.decode("utf-8", "replace").strip()))


def commitment(root):
    """sha256 over '<relpath>\\0<f|l>\\0<sha256 hex of file bytes or link text>\\n' in sorted UTF-8 byte order."""
    ents = []
    for dp, dns, fns in os.walk(root, followlinks=False):
        for n in list(dns):
            full = os.path.join(dp, n)
            if os.path.islink(full):
                dns.remove(n)
                ents.append(full)
        for n in fns:
            ents.append(os.path.join(dp, n))
    rows = []
    for full in ents:
        rel = os.path.relpath(full, root)
        if os.path.islink(full):
            rows.append((os.fsencode(rel), b"l", hashlib.sha256(os.fsencode(os.readlink(full))).hexdigest().encode()))
        elif os.path.isfile(full):
            with open(full, "rb") as f:
                rows.append((os.fsencode(rel), b"f", hashlib.sha256(f.read()).hexdigest().encode()))
    rows.sort(key=lambda r: r[0])
    h = hashlib.sha256()
    for rel, kind, dig in rows:
        h.update(rel + b"\0" + kind + b"\0" + dig + b"\n")
    return h.hexdigest()


def run_program(python, program, args, cwd, env):
    """(stdout bytes, rc) of `python -I program args`; a timeout or spawn failure yields (b'', None)."""
    try:
        p = subprocess.run([python, "-I", program] + args, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=TIMEOUT)
        return p.stdout, p.returncode
    except (subprocess.TimeoutExpired, OSError):
        return b"", None


def fixture_args(fxdir):
    with open(os.path.join(fxdir, "args.json"), "rb") as f:
        raw = json.loads(f.read().decode("utf-8"))
    if not isinstance(raw, list) or not all(isinstance(a, str) for a in raw):
        raise ValueError("args.json is not a list of strings")
    return [a.replace("{FX}", fxdir) for a in raw]


def score(python, program, root, fxroot, ids, env):
    """number of fixtures in ids whose stdout bytes and exit status equal expected.out / expected.rc."""
    passed = 0
    for fid in ids:
        fx = os.path.join(fxroot, fid)
        try:
            args = fixture_args(fx)
            with open(os.path.join(fx, "expected.out"), "rb") as f:
                exp_out = f.read()
            with open(os.path.join(fx, "expected.rc"), "rb") as f:
                exp_rc = int(f.read().decode("ascii").strip())
        except (OSError, ValueError, UnicodeDecodeError):
            continue
        if not os.path.isfile(program):
            continue
        out, rc = run_program(python, program, args, root, env)
        if rc is not None and rc == exp_rc and out == exp_out:
            passed += 1
    return passed


def parse(argv):
    opts = {}
    i = 0
    while i < len(argv):
        k = argv[i]
        if k not in ("--repo", "--rev", "--work", "--holdout") or k in opts or i + 1 >= len(argv):
            raise Setup("usage: --repo REPO --rev REV --work DIR [--holdout DIR]")
        opts[k] = argv[i + 1]
        i += 2
    for k in ("--repo", "--rev", "--work"):
        if k not in opts or not opts[k]:
            raise Setup("usage: --repo REPO --rev REV --work DIR [--holdout DIR]")
    return opts


def harness(opts):
    repo, rev = opts["--repo"], opts["--rev"]
    work = os.path.realpath(opts["--work"])
    os.makedirs(work, exist_ok=True)
    env = scrubbed_env(work)
    python = shutil.which("python3", path=SAFE_PATH)
    if python is None:
        raise Setup("python3 not found")
    git(repo, work, "rev-parse", "--verify", "--quiet", rev + "^{commit}")

    # frozen tables: regular blob at rev with the embedded sha256
    ent = ls_entry(repo, work, rev, TABLES)
    if ent is None or ent[1] != "blob" or ent[0] not in ("100644", "100755"):
        raise Setup("frozen-tables.json is not a regular blob at rev")
    blob = git(repo, work, "cat-file", "blob", "%s:%s" % (rev, TABLES)).stdout
    if hashlib.sha256(blob).hexdigest() != TABLES_SHA256:
        raise Setup("frozen-tables.json sha256 differs from the embedded constant")
    c2 = json.loads(blob.decode("utf-8"))["c2"]

    ex = tempfile.mkdtemp(prefix="c2-export-", dir=work)
    try:
        arch = ["git", "-C", repo, "archive", "--format=tar", rev, "--"]
        tool_ent = ls_entry(repo, work, rev, TOOL)
        tool_present = tool_ent is not None and tool_ent[1] == "blob" and tool_ent[0] in ("100644", "100755")
        paths = [TABLES]
        if tool_present:
            paths.append(TOOL)
        fx_ent = ls_entry(repo, work, rev, FIXTURES)
        if fx_ent is None or fx_ent[1] != "tree":
            raise Setup("fixtures/c2 absent at rev")
        paths.append(FIXTURES)
        ctl_ent = ls_entry(repo, work, rev, CTL)
        if ctl_ent is not None and ctl_ent[1] == "tree":
            paths.append(CTL)
        ho_dir = opts.get("--holdout")
        if ho_dir is None:
            ho_ent = ls_entry(repo, work, rev, HOLDOUT)
            if ho_ent is not None and ho_ent[1] == "tree":
                paths.append(HOLDOUT)
        pipe_tar(arch + paths, ex, env)
        if ho_dir is not None:
            if not os.path.isdir(ho_dir):
                raise Setup("--holdout is not a directory")
            dest = os.path.join(ex, HOLDOUT)
            os.makedirs(dest)
            pipe_tar(["tar", "-c", "-C", os.path.abspath(ho_dir), "-f", "-", "."], dest, env)

        fx_root = os.path.join(ex, FIXTURES)
        ho_root = os.path.join(ex, HOLDOUT)
        ho_present = os.path.isdir(ho_root)
        tool = os.path.join(ex, TOOL)

        a = score(python, tool, ex, fx_root, COMMITTED_IDS, env) if tool_present else 0
        b = score(python, tool, ex, ho_root, HOLDOUT_IDS, env) if (tool_present and ho_present) else 0

        fx_ok = commitment(fx_root) == c2["fixture_commit_sha256"]
        if not ho_present:
            ho_commit = "absent"
        else:
            ho_commit = "ok" if commitment(ho_root) == c2["holdout_commit_sha256"] else "bad"

        ctl_ok = 0
        ctl_dir = os.path.join(ex, CTL)
        ctl_detail = {}
        for name in CONTROLS:
            prog = os.path.join(ctl_dir, name + ".py")
            if not os.path.isfile(prog):
                ctl_detail[name] = None
                continue
            c_pass = score(python, prog, ex, fx_root, COMMITTED_IDS, env)
            h_pass = score(python, prog, ex, ho_root, HOLDOUT_IDS, env) if ho_present else 0
            ctl_detail[name] = (c_pass, h_pass)
            if name == "const-host":
                ok = c_pass + h_pass <= 1
            elif name == "empty":
                ok = c_pass + h_pass == 0
            else:
                ok = c_pass == 18 and h_pass == 0
            ctl_ok += 1 if ok else 0
        sys.stderr.write("r56_ctl_c2: fixture_commit=%s control_scores=%s\n" % ("ok" if fx_ok else "bad", ctl_detail))
        met = (a == 18 and b == 8 and ho_commit == "ok" and fx_ok and ctl_ok == 3)
        line = "MADO_R56_C2: rev=%s fixtures=%d/18 holdout=%d/8 holdout_commit=%s controls=%d/3 verdict=%s" % (
            rev, a, b, ho_commit, ctl_ok, "TARGET_MET" if met else "TARGET_MISSED")
        return line, 0 if met else 1
    finally:
        shutil.rmtree(ex, ignore_errors=True)


def run(argv):
    try:
        opts = parse(list(argv))
        line, rc = harness(opts)
    except Setup as e:
        sys.stderr.write("r56_ctl_c2: setup error: %s\n" % e)
        return 2
    sys.stdout.write(line + "\n")
    sys.stdout.flush()
    return rc


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
