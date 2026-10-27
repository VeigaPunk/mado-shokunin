#!/usr/bin/env python3
"""Differential fuzzer: lsemu.ls_lRL() vs the host's /usr/bin/ls -LRl.

Two environments, same generator and same seeds:
  host     -- files owned by the caller, owner/group are *names*
  sandbox  -- bwrap user namespace, no /etc, so ls prints numeric ids

Usage (from anywhere):
    TMPDIR=/fast/scratch/... python3 fuzz.py --cases 2000 --seed 1 \
        --work /fast/scratch/.../fz --mode both --out receipts/fuzz.txt

Exit status: 0 if every case matched, 1 otherwise.
"""

import argparse
import errno
import os
import random
import shutil
import socket
import stat
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lsemu  # noqa: E402

LS = "/usr/bin/ls"
BASE_ENV = {
    "LC_ALL": "C",
    "LANG": "C",
    "PATH": "/usr/bin:/bin",
    "TZ": "UTC",
    "HOME": "/nonexistent",
}

# deterministic clock discipline: every generated mtime stays at least two
# minutes away from a format boundary, so a 1-2 s clock skew between ls and
# the model cannot flip a case.
SIX = 31556952 // 2                      # 15778476, ls.c
# offsets from the case's build second; nothing lands within two minutes of
# "now", so a one-second clock skew between ls and the model cannot flip a case
RECENT = [(-300, "recent"), (-3600, "recent"), (-86400, "recent"),
          (-30 * 86400, "recent"), (-(SIX - 7200), "recent")]
OLD = [(-(SIX + 7200), "old-time"), (-200 * 86400, "old-time"),
       (-400 * 86400, "old-time"), (-(3 * 365 * 86400), "old-time")]
FUTURE = [(86400, "future"), (2 * 86400, "future")]
FIXED = [(0, "epoch"), (1577934245, "absolute-time")]

NAMES = [
    b"alpha", b"Beta", b"gamma", b"delta", b"Zeta", b"epsilon",
    b"0", b"2", b"10", b"-dash", b"~tilde", b"sp ace", b"two  spaces",
    b"tab\there", b"nl\nhere", b'quote"d', b"quote'd", b"back\\slash",
    b"uni-\xc3\xbc", b"ctl\x01x", b":colon", b"...dots", b"Caps",
    b"a" * 60, b"b" * 200, b".hidden", b".h2", b"S340", b"x y z",
    b"lead\x7fdel", b"per%cent", b"star*", b"pipe|", b"lt<gt>",
    b"invalid-\xff\xfe", b"hi-\x80bit", b"c" * 255, b"=", b"#hash",
    b"~" , b"{brace}", b"ellipsis...", b"tab\tend",
]

MODES = [0o644, 0o600, 0o755, 0o700, 0o4755, 0o2755, 0o1755,
         0o4644, 0o2644, 0o1644, 0o777, 0o666]
SIZES = [0, 1, 5, 511, 4095, 4096, 5000, 65536, 100000]


# --------------------------------------------------------------------------
# tree generator
# --------------------------------------------------------------------------

def _force_rmtree(path):
    """Remove a generated tree even where a directory was chmod'ed read-only."""
    for dirpath, dirnames, _files in os.walk(path):
        for d in dirnames:
            try:
                os.chmod(os.path.join(dirpath, d), 0o755)
            except OSError:
                pass
    try:
        os.chmod(path, 0o755)
    except OSError:
        pass
    shutil.rmtree(path, ignore_errors=True)


def _mtime(rng, base):
    """Absolute epoch + class tag, kept clear of every format boundary."""
    bucket = rng.random()
    if bucket < 0.45:
        off, tag = rng.choice(RECENT)
        return base + off, tag
    if bucket < 0.70:
        off, tag = rng.choice(OLD)
        return base + off, tag
    if bucket < 0.85:
        off, tag = rng.choice(FUTURE)
        return base + off, tag
    epoch, tag = rng.choice(FIXED)
    return epoch, tag


def _fill(root, rel, rng, tags, depth, base):
    """Create entries under root/rel."""
    count = rng.randint(0, 6)
    names = rng.sample(NAMES, min(count, len(NAMES)))
    dirs = []
    for name in names:
        path = os.path.join(root, rel, os.fsdecode(name)) if rel else \
            os.path.join(root, os.fsdecode(name))
        kind = rng.choices(
            ["file", "dir", "link", "fifo", "socket", "hardlink"],
            weights=[50, 22, 18, 4, 3, 3])[0]
        if depth >= 3:
            kind = rng.choices(["file", "link", "fifo", "socket"],
                               weights=[70, 20, 5, 5])[0]
        try:
            if kind == "dir":
                os.mkdir(path)          # permissive while filling
                dirs.append((name, path, rng.choice([0o755, 0o700, 0o1777,
                                                     0o555])))
                tags.add("dir")
            elif kind == "file":
                size = rng.choice(SIZES)
                mode = rng.choice(MODES)
                if rng.random() < 0.12:
                    with open(path, "wb") as fh:      # sparse: st_blocks == 0
                        fh.truncate(rng.choice([1 << 20, 1 << 24]))
                    tags.add("sparse")
                else:
                    with open(path, "wb") as fh:
                        fh.write(b"x" * size)
                os.chmod(path, mode)
                if mode & (stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX):
                    tags.add("special-mode")
                if size >= 65536:
                    tags.add("big-size")
                tags.add("file")
            elif kind == "link":
                target = rng.choices(
                    ["file", "dir", "dangling", "dot", "dotdot", "chain",
                     "sibling-dir", "self"],
                    weights=[30, 20, 20, 5, 8, 7, 5, 5])[0]
                if target == "file" and dirs:
                    tgt = os.path.join(os.pardir, os.fsdecode(dirs[0][0]))
                elif target == "dangling":
                    tgt = "/nonexistent/x"
                    tags.add("dangling")
                elif target == "dot":
                    tgt = "."
                    tags.add("link-dot")
                elif target == "dotdot" and rel:
                    # ".." is only used below the top level: at the top it
                    # would dereference to the fuzzer's own work directory
                    tgt = ".."
                    tags.add("loop")
                elif target == "self":
                    tgt = name
                    tags.add("loop")
                elif target == "chain":
                    tgt = name + b".t"
                    try:
                        os.symlink(b"nowhere", os.path.join(
                            os.path.dirname(path),
                            os.fsdecode(tgt)))
                    except OSError:
                        pass
                    tags.add("link-chain")
                elif target == "sibling-dir" and dirs:
                    # a plain sibling dir keeps the link inside the case tree
                    tgt = os.fsdecode(dirs[0][0])
                    tags.add("link-sibling")
                else:
                    tgt = b"target-" + name
                    tags.add("dangling")
                os.symlink(tgt, path)
                tags.add("symlink")
            elif kind == "fifo":
                os.mkfifo(path)
                tags.add("fifo")
            elif kind == "socket":
                sock = socket.socket(socket.AF_UNIX)
                try:
                    sock.bind(path)
                    tags.add("socket")
                except OSError:
                    os.mkfifo(path)       # AF_UNIX path limit: still a special
                    tags.add("fifo")
                finally:
                    sock.close()
            elif kind == "hardlink":
                src = os.path.join(os.path.dirname(path), "hl-src")
                if not os.path.exists(src):
                    with open(src, "wb") as fh:
                        fh.write(b"hardlink")
                os.link(src, path)
                tags.add("hardlink")
        except OSError as exc:
            if exc.errno not in (errno.EEXIST, errno.ENAMETOOLONG):
                raise

    for name, path, mode in dirs:
        sub = os.path.join(rel, os.fsdecode(name)) if rel else os.fsdecode(name)
        _fill(root, sub, rng, tags, depth + 1, base)
        os.chmod(path, mode)            # only after the children exist


def build_tree(root, rng):
    tags = set()
    base = int(time.time())
    _fill(root, "", rng, tags, 1, base)
    # one pass of deterministic timestamps, deepest last is unnecessary:
    # utime() does not disturb a parent's mtime.
    stacks = [root]
    while stacks:
        cur = stacks.pop()
        try:
            entries = list(os.scandir(cur))
        except OSError:
            continue
        for ent in entries:
            try:
                stamp, tag = _mtime(rng, base)
                tags.add(tag)
                os.utime(ent.path, (stamp, stamp), follow_symlinks=False)
            except OSError:
                pass
            if ent.is_dir(follow_symlinks=False):
                stacks.append(ent.path)
    try:
        stamp, tag = _mtime(rng, base)
        tags.add(tag)
        os.utime(root, (stamp, stamp))
    except OSError:
        pass
    real_root = os.path.realpath(root)
    stack = [root]
    while stack:
        cur = stack.pop()
        for ent in os.scandir(cur):
            if ent.is_symlink():
                tgt = os.path.realpath(ent.path)
                if os.path.exists(tgt) and not (tgt == real_root
                                                or tgt.startswith(real_root + os.sep)):
                    os.unlink(ent.path)
                    tags.add("escaped-link-dropped")
            elif ent.is_dir(follow_symlinks=False):
                stack.append(ent.path)
    if rng.random() < 0.18:
        # a non-trivial ACL makes every mode field in that block 11 columns
        cands = []
        for dirpath, dirnames, filenames in os.walk(root):
            cands += [os.path.join(dirpath, n) for n in filenames[:2]]
            cands += [os.path.join(dirpath, n) for n in dirnames[:2]]
        if cands:
            victim = rng.choice(cands)
            flag = "-d" if os.path.isdir(victim) else None
            cmd = ["setfacl"] + (["-d"] if flag else []) + \
                  ["-m", "u:65534:r", victim]
            if subprocess.run(cmd, capture_output=True).returncode == 0:
                tags.add("acl")
    return tags


def pick_operands(root, rng):
    """Return (operands as bytes, tags)."""
    tags = set()
    # ls parses operands starting with '-' as options (evidenced in the seat
    # report); the resolver only ever passes paths, so such names are excluded
    # as *operands* -- they remain in the trees as entries.
    tops = sorted(n for n in os.listdir(root) if not n.startswith("-"))
    dirs = [n for n in tops if os.path.isdir(os.path.join(root, n))]
    files = [n for n in tops if not os.path.isdir(os.path.join(root, n))]
    ops = []
    if dirs and rng.random() < 0.9:
        ops += rng.sample(dirs, rng.randint(1, min(2, len(dirs))))
    if files and rng.random() < 0.45:
        ops.append(rng.choice(files))
        tags.add("file-operand")
    if dirs and rng.random() < 0.25:
        d = rng.choice(dirs)
        subs = [n for n in os.listdir(os.path.join(root, d))
                if os.path.isdir(os.path.join(root, d, n))]
        if subs:
            ops.append(os.path.join(d, rng.choice(subs)))
            tags.add("nested-operand")
    if dirs and rng.random() < 0.15:
        ops.append(rng.choice(dirs) + "/")
        tags.add("trailing-slash")
    if rng.random() < 0.20:
        ops.append("no-such-operand")
        tags.add("missing-operand")
    if dirs and rng.random() < 0.10:
        ops.append(rng.choice(dirs))
        tags.add("dup-operand")
    if not ops:
        ops = ["."]
        tags.add("dot-operand")
    if rng.random() < 0.08:
        ops.append(os.path.join(root, rng.choice(tops)) if tops else "/nonexistent")
        tags.add("absolute-operand")
    rng.shuffle(ops)
    return [os.fsencode(o) for o in ops], tags


# --------------------------------------------------------------------------
# one case
# --------------------------------------------------------------------------

def run_case(work, index, rng):
    root = os.path.join(work, "case%05d" % index)
    _force_rmtree(root)
    os.makedirs(root, exist_ok=True)
    tags = build_tree(root, rng)
    ops, otags = pick_operands(root, rng)
    tags |= otags
    env = dict(BASE_ENV)
    exp = subprocess.run([LS, "-LRl"] + [os.fsdecode(o) for o in ops],
                         cwd=root, env=env, capture_output=True)
    # capture the model clock *after* ls ran, so it is never behind ls's
    now = int(time.time())
    got_out, got_err, got_rc = lsemu.ls_lRL_full(ops, now=now, cwd=root)
    detail = None
    if exp.stdout != got_out:
        detail = _first_diff("stdout", exp.stdout, got_out)
        tags.add("FAIL-stdout")
    if exp.stderr != got_err:
        if detail is None:
            detail = _first_diff("stderr", exp.stderr, got_err)
        tags.add("FAIL-stderr")
    if exp.returncode != got_rc:
        if detail is None:
            detail = "rc exp=%d got=%d" % (exp.returncode, got_rc)
        tags.add("FAIL-rc")
    if detail is None:
        _force_rmtree(root)
    return detail, tags


def _first_diff(stream, exp, got):
    e = exp.split(b"\n")
    g = got.split(b"\n")
    for i in range(max(len(e), len(g))):
        a = e[i] if i < len(e) else b"<missing>"
        b = g[i] if i < len(g) else b"<missing>"
        if a != b:
            return "%s line %d\n    exp %r\n    got %r" % (stream, i, a, b)
    return "%s differs only in trailing bytes" % stream


# --------------------------------------------------------------------------
# deterministic suites
# --------------------------------------------------------------------------

def fixed_cases(work):
    """Hand-built cases for classes the random generator hits rarely."""
    results = []
    root = os.path.join(work, "fixed")
    _force_rmtree(root)
    os.makedirs(root, exist_ok=True)

    d = os.path.join(root, "d")
    os.makedirs(d)
    with open(os.path.join(d, "f"), "wb") as fh:
        fh.write(b"x" * 5000)
    os.symlink("/nonexistent", os.path.join(d, "dangle"))
    os.symlink("..", os.path.join(d, "up"))
    os.mkfifo(os.path.join(d, "fifo"))
    os.mkdir(os.path.join(d, "sub"))
    with open(os.path.join(d, "sub", "g"), "wb") as fh:
        fh.write(b"y")
    os.chmod(os.path.join(d, "f"), 0o4755)
    os.mkdir(os.path.join(root, "empty"))
    with open(os.path.join(root, "top"), "wb") as fh:
        fh.close()
    wide = os.path.join(root, "wide")
    os.makedirs(wide)
    for i in range(12):                     # nlink 14: two-digit nlink column
        os.mkdir(os.path.join(wide, "s%02d" % i))
    many = os.path.join(root, "many")
    os.makedirs(many)
    for i in range(40):                     # sort order + width stability
        with open(os.path.join(many, "f%02d" % i), "wb") as fh:
            fh.write(b"z" * (i * 37))
    os.mkdir(os.path.join(root, "locked"))
    with open(os.path.join(root, "locked", "inside"), "wb") as fh:
        fh.write(b"i")
    os.chmod(os.path.join(root, "locked"), 0o000)
    os.symlink("d", os.path.join(root, "dlink"))
    os.symlink("/nonexistent", os.path.join(root, "dbroken"))
    for mode in (0o4755, 0o2755, 0o1755, 0o4644, 0o2644, 0o1644):
        name = os.path.join(d, "m%o" % mode)
        with open(name, "wb") as fh:
            fh.write(b"m")
        os.chmod(name, mode)
    # one deterministic stamp for everything, root last: nothing may be
    # created afterwards or a directory mtime would drift to "now"
    for p in ["d/f", "d/dangle", "d/up", "d/fifo", "d/sub/g", "top", "empty",
              "dlink", "dbroken", "d/m4755", "d/m2755", "d/m1755", "d/m4644",
              "d/m2644", "d/m1644", "d/sub", "d", "locked", "wide", "many",
              "wide"] + ["wide/s%02d" % i for i in range(12)] + \
             ["many/f%02d" % i for i in range(40)] + ["."]:
        try:
            os.utime(os.path.join(root, p), (1577934245, 1577934245),
                     follow_symlinks=False)
        except OSError:
            pass

    cases = [
        (["d"], "dir-with-everything"),
        (["d", "top"], "file-then-dir-widths"),
        (["top", "d"], "operand-order"),
        (["top", "d", "nosuch"], "missing-operand"),
        (["d", "d"], "duplicate-operand"),
        (["dlink", "d"], "symlink-dir-operand"),
        (["dbroken"], "dangling-operand"),
        (["d/"], "trailing-slash"),
        (["empty"], "empty-dir"),
        ([".", "d"], "dot-operand"),
        (["d/up"], "link-to-parent-operand"),
        (["d/nope"], "missing-subpath"),
        (["./d"], "dot-slash-operand"),
        (["locked"], "unreadable-dir"),
        (["locked", "d"], "unreadable-then-readable"),
        (["wide", "d"], "two-digit-nlink"),
        (["many"], "forty-entries"),
    ]
    for ops, label in cases:
        env = dict(BASE_ENV)
        now = int(time.time())
        exp = subprocess.run([LS, "-LRl"] + ops, cwd=root, env=env,
                             capture_output=True)
        got = lsemu.ls_lRL_full([os.fsencode(o) for o in ops], now=now,
                                cwd=root)
        ok = (exp.stdout == got[0] and exp.stderr == got[1]
              and exp.returncode == got[2])
        results.append((label, ok, None if ok else _first_diff(
            "stdout", exp.stdout, got[0])))
    return results


def device_case(work):
    """Device major,minor columns: only real device nodes exercise them."""
    env = dict(BASE_ENV)
    # the sandbox's /dev nodes were created at bwrap start: wait until they are
    # at least a second older than the clock both sides will observe, so the
    # recent/old boundary cannot decide this case
    time.sleep(1.2)
    now = int(time.time())
    out = []
    for path in ("/dev", "/dtmp"):
        if not os.path.isdir(path):
            continue
        ops = [path.encode()]
        exp = subprocess.run([LS, "-LRl", path], cwd=work, env=env,
                             capture_output=True)
        got = lsemu.ls_lRL_full(ops, now=now, cwd=work)
        ok = (exp.stdout == got[0] and exp.returncode == got[2])
        out.append(("devices:" + path, ok, None if ok else _first_diff(
            "stdout", exp.stdout, got[0])))
    return out


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

def run_suite(args):
    os.environ["TZ"] = "UTC"
    time.tzset()
    work = args.work
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)

    mode = "sandbox" if args.inner else args.mode
    lines = []
    lines.append("ls: %s" % subprocess.run([LS, "--version"], capture_output=True,
                                           env=BASE_ENV).stdout.decode().split("\n")[0])
    lines.append("ls sha256: %s" % _sha256(LS))
    lines.append("lsemu sha256: %s" % _sha256(os.path.join(HERE, "lsemu.py")))
    lines.append("mode: %s  cases/seed: %d/%d" % (mode, args.cases, args.seed))
    if args.inner:
        lines.append("sandbox: /etc/passwd present=%s  uid=%d gid=%d"
                     % (os.path.exists("/etc/passwd"), os.getuid(), os.getgid()))
    lines.append("")

    fixed = fixed_cases(work)
    devs = device_case(work) if mode == "sandbox" else []
    fixed_bad = [f for f in fixed + devs if not f[1]]
    lines.append("fixed cases: %d matched, %d failed" %
                 (len(fixed + devs) - len(fixed_bad), len(fixed_bad)))
    for label, ok, detail in fixed + devs:
        lines.append("  %-26s %s" % (label, "match" if ok else "MISMATCH"))
        if detail:
            lines.append("    " + detail.replace("\n", "\n    "))

    rng = random.Random(args.seed)
    tag_stats = {}
    failures = []
    t0 = time.time()
    for i in range(args.cases):
        detail, tags = run_case(work, i, rng)
        for t in tags:
            hit, miss = tag_stats.get(t, (0, 0))
            tag_stats[t] = (hit + (0 if detail else 1), miss + (1 if detail else 0))
        if detail:
            failures.append((i, detail, sorted(tags)))
            if len(failures) >= 25:
                break

    lines.append("")
    lines.append("random cases run: %d  mismatches: %d  seed: %d  seconds: %.1f"
                 % (i + 1, len(failures), args.seed, time.time() - t0))
    for idx, detail, tags in failures:
        lines.append("  case %d tags=%s" % (idx, ",".join(tags)))
        lines.append("    " + detail.replace("\n", "\n    "))
    lines.append("")
    lines.append("per-class coverage (cases, mismatches):")
    for tag in sorted(tag_stats):
        hit, miss = tag_stats[tag]
        lines.append("  %-22s %5d %5d" % (tag, hit, miss))

    report = "\n".join(lines) + "\n"
    with open(args.out, "a") as fh:
        fh.write(report)
    sys.stdout.write(report)
    if not args.inner:            # the inner run leaves its work dir to the outer
        _force_rmtree(work)
    return 0 if (not failures and not fixed_bad) else 1


def _sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--work", default=None)
    ap.add_argument("--out", default=os.path.join(HERE, "receipts", "fuzz.txt"))
    ap.add_argument("--mode", choices=["host", "sandbox", "both"], default="both")
    ap.add_argument("--inner", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--append", action="store_true",
                    help="append to --out instead of starting a fresh receipt")
    ap.add_argument("--host-seed", type=int, default=None,
                    help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    args.out = os.path.abspath(args.out)

    if args.work is None:
        base = os.environ.get("TMPDIR") or "/tmp"
        args.work = os.path.join(base, "lsemu-fuzz")
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)

    if args.inner:
        return run_suite(args)

    if args.mode == "host":
        return run_suite(args)

    if args.mode == "sandbox":
        return _sandbox(args)

    # both: host then sandbox with a derived seed
    if os.path.exists(args.out) and not args.append:
        os.remove(args.out)
    rc1 = run_suite(args)
    sargs = argparse.Namespace(**vars(args))
    sargs.seed = args.seed + 100000
    sargs.mode = "sandbox"
    rc2 = _sandbox(sargs)
    _force_rmtree(args.work)
    return 0 if rc1 == 0 and rc2 == 0 else 1


def _sandbox(args):
    work = args.work
    os.makedirs(work, exist_ok=True)
    # the seat directory is mounted read-only inside bwrap: the inner run
    # writes its receipt into the work dir and the outer run appends it
    inner_out = os.path.join(work, "sandbox-receipt.txt")
    if os.path.exists(inner_out):
        os.remove(inner_out)
    # a regular file next to the device nodes: exercises the size-column
    # interplay between "major, minor" and plain sizes
    with open(os.path.join(work, "reg7"), "wb") as fh:
        fh.write(b"1234567")
    cmd = [
        "bwrap", "--unshare-all", "--die-with-parent",
        "--tmpfs", "/",
        "--ro-bind", "/usr", "/usr",
        "--ro-bind", "/lib", "/lib",
        "--ro-bind", "/lib64", "/lib64",
        "--ro-bind", "/bin", "/bin",
        "--dev", "/dev",
        "--tmpfs", "/dtmp",
        "--ro-bind", "/dev/loop-control", "/dtmp/lc",
        "--ro-bind", "/dev/kmsg", "/dtmp/kmsg",
        "--ro-bind", "/dev/null", "/dtmp/null",
        "--ro-bind", os.path.join(work, "reg7"), "/dtmp/reg",
        "--tmpfs", "/tmp",
        "--bind", work, work,
        "--ro-bind", HERE, HERE,
        "--chdir", work,
        "/usr/bin/python3", os.path.join(HERE, "fuzz.py"),
        "--inner", "--cases", str(args.cases), "--seed", str(args.seed),
        "--work", work, "--out", inner_out,
    ]
    rc = subprocess.run(cmd, cwd=work).returncode
    if os.path.exists(inner_out):
        with open(inner_out, "rb") as src, open(args.out, "ab") as dst:
            dst.write(src.read())
        os.remove(inner_out)
    return rc


if __name__ == "__main__":
    sys.exit(main())
