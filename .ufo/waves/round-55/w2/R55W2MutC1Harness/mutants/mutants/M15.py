#!/usr/bin/env python3
"""R55 C1 control harness (independent of the counter).

    python3 -I r55_ctl_c1.py --repo REPO --rev REV --work DIR [--counter PATH]

Builds, for the good tree at REV and for each of the seven frozen C1 controls
(registration.md section C1), a scratch git repository holding only the paths a
counter needs, runs the counter as a child process against it, and compares the
counter's single MADO_KBD_ENTRY line to the verdict and leg THIS harness holds.
A missing, extra or unparsable counter line, a wrong exit status or a missing
required leg is a failed control (M54-6: an always-green counter scores 0/7).

stdout: exactly one line
    MADO_R55_CONTROLS: claim=c1 good=<ok|bad> controls=<k>/7 verdict=<OK|FAIL>
stderr: per-control detail. exit 0 on OK, 1 on FAIL, 2 on setup error.
Reads REPO only through git objects at REV; every temporary file is under --work.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FROZEN_PATH = ".ufo/waves/round-55/frozen-tables-v2.json"
COUNTER_PATH = "quality/counters/c1-r55-kbd-entry.py"
EXTRA_PATHS = ("corpus/README.md", "corpus/SOURCES.md")
CHILD_TIMEOUT = 120

LINE_RE = re.compile(
    r"^MADO_KBD_ENTRY: rev=(?P<rev>\S+) rows=(?P<rows>\d+)/18 hosts=(?P<hosts>\d+)/6 "
    r"sources=(?P<sa>\d+)/(?P<sb>\d+) new_rows=(?P<new>\d+)/3 "
    r"verdict=(?P<verdict>TARGET_MET|TARGET_MISSED) missed=(?P<missed>\S+)$"
)
LEG_RE = re.compile(r"^(?:[a-z_]+|(?:row|anchor|quote|source_cell|host):[KH][0-9]{2})$")
ID_LEG_RE = re.compile(r"^(?:row|anchor|quote|source_cell|host):([KH][0-9]{2})$")


class Setup(Exception):
    """Cannot run at all (exit 2)."""


class MutationError(Exception):
    """The frozen mutation cannot be applied to this tree (control fails)."""


# --------------------------------------------------------------------------- git

def _env(work: Path) -> dict:
    return {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": str(work),
        "TMPDIR": str(work),
        "LC_ALL": "C.UTF-8",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
    }


def git(work: Path, *args: str, cwd: str | None = None, check: bool = True) -> bytes:
    p = subprocess.run(["git", *args], cwd=cwd, env=_env(work), capture_output=True)
    if check and p.returncode != 0:
        raise Setup("git %s failed: %s" % (" ".join(args[:4]), p.stderr.decode("utf-8", "replace").strip()))
    return p.stdout


def read_tree(work: Path, repo: str, rev: str, paths: list[str]) -> dict[str, bytes]:
    """Needed paths of the tree at REV, via git objects only. Missing paths are simply absent."""
    out = git(work, "-C", repo, "ls-tree", "-r", "-z", rev, "--", *paths)
    tree: dict[str, bytes] = {}
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, _, name = rec.partition(b"\t")
        mode, typ, oid = meta.decode().split()
        if typ != "blob" or mode not in ("100644", "100755"):
            continue
        tree[name.decode("utf-8")] = git(work, "-C", repo, "cat-file", "blob", oid)
    return tree


def materialize(work: Path, base: Path, name: str, tree: dict[str, bytes]) -> tuple[Path, str]:
    d = Path(tempfile.mkdtemp(prefix=name + "-", dir=str(base)))
    git(work, "init", "-q", "-b", "main", str(d))
    top = git(work, "-C", str(d), "rev-parse", "--show-toplevel").decode().strip()
    if os.path.realpath(top) != os.path.realpath(str(d)):
        raise Setup("scratch repo toplevel %s != %s" % (top, d))
    for rel, data in tree.items():
        f = d / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(data)
    git(work, "-C", str(d), "add", "-A")
    git(work, "-C", str(d), "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "-c", "commit.gpgsign=false",
        "commit", "-q", "--allow-empty", "-m", "ctl " + name)
    sha = git(work, "-C", str(d), "rev-parse", "HEAD").decode().strip()
    return d, sha


# ----------------------------------------------------------------- mutations

def _lines(data: bytes) -> list[str]:
    return data.decode("utf-8").split("\n")


def _row_index(lines: list[str], rid: str) -> int:
    hits = [i for i, l in enumerate(lines) if re.match(r"^\|\s*%s\s*\|" % re.escape(rid), l)]
    if len(hits) != 1:
        raise MutationError("row %s present %d times, need exactly 1" % (rid, len(hits)))
    return hits[0]


def _edit_entry(tree: dict[str, bytes], entry: str, fn) -> dict[str, bytes]:
    if entry not in tree:
        raise MutationError("entry absent from good tree")
    lines = _lines(tree[entry])
    fn(lines)
    out = dict(tree)
    out[entry] = "\n".join(lines).encode("utf-8")
    if out[entry] == tree[entry]:
        raise MutationError("mutation changed nothing")
    return out


def m_absent(tree, ctx):
    if ctx["entry"] not in tree:
        raise MutationError("entry absent from good tree")
    out = dict(tree)
    del out[ctx["entry"]]
    return out


def m_spliced(tree, ctx):
    def fn(lines):
        i = _row_index(lines, "K04")
        old, new = "std::max(0, REPEATRATE);", "std::max(0, REPEATRATE) ;"
        if lines[i].count(old) != 1:
            raise MutationError("K04 row lacks exactly one %r" % old)
        lines[i] = lines[i].replace(old, new)
    return _edit_entry(tree, ctx["entry"], fn)


def m_anchor(tree, ctx):
    def fn(lines):
        i = _row_index(lines, "K01")
        cells = lines[i].split("|")
        hit = [j for j, c in enumerate(cells) if re.search(r":1220\s*$", c)]
        if len(hit) != 1:
            raise MutationError("K01 row has %d anchor cells ending :1220" % len(hit))
        cells[hit[0]] = re.sub(r":1220(\s*)$", r":1219\1", cells[hit[0]])
        lines[i] = "|".join(cells)
    return _edit_entry(tree, ctx["entry"], fn)


def m_source(tree, ctx):
    def fn(lines):
        i = _row_index(lines, "K10")
        cells = lines[i].split("|")
        if len(cells) < 6 or not re.fullmatch(r"\s*S[0-9]{3}\s*", cells[3]):
            raise MutationError("K10 row cell 3 is not an S-id: %r" % (cells[3:4],))
        if cells[3].strip() == "S316":
            raise MutationError("K10 already cites S316")
        cells[3] = " S316 "
        lines[i] = "|".join(cells)
    return _edit_entry(tree, ctx["entry"], fn)


def m_dropped(tree, ctx):
    def fn(lines):
        del lines[_row_index(lines, "K17")]
    return _edit_entry(tree, ctx["entry"], fn)


def m_host(tree, ctx):
    def fn(lines):
        i = _row_index(lines, "H02")
        old, new = "`repeat_delay = 250`", "`repeat_delay = 300`"  # the backticked quote cell only (the proposition cell may repeat the text)
        if lines[i].count(old) != 1:
            raise MutationError("H02 row lacks exactly one %r" % old)
        lines[i] = lines[i].replace(old, new)
    return _edit_entry(tree, ctx["entry"], fn)


def m_pin(tree, ctx):
    pin = "Hyprland-IKeyboard.cpp"
    pf = ctx["pin_dir"] + "/" + pin
    if FROZEN_PATH not in tree or pf not in tree:
        raise MutationError("frozen-tables.json or %s absent from good tree" % pf)
    txt = tree[FROZEN_PATH].decode("utf-8")
    h = ctx["pin_sha256"][pin]
    if txt.count(h) != 1:
        raise MutationError("frozen-tables.json holds %s %d times, need 1" % (h, txt.count(h)))
    nib = "0" if h[0] != "0" else "1"
    txt = txt.replace(h, nib + h[1:])
    out = dict(tree)
    out[FROZEN_PATH] = txt.encode("utf-8")
    out[pf] = tree[pf] + b" "
    return out


# (id, name, mutation, required leg, owned ids [id-legs the counter may legitimately name])
CONTROLS = [
    ("C1-CTL-1", "absent", m_absent, "entry_absent", None),
    ("C1-CTL-2", "spliced-quote", m_spliced, "quote:K04", {"K04"}),
    ("C1-CTL-3", "shifted-anchor", m_anchor, "anchor:K01", {"K01"}),
    ("C1-CTL-4", "wrong-source", m_source, "source_cell:K10", {"K10"}),
    ("C1-CTL-5", "dropped-row", m_dropped, "row:K17", {"K17"}),
    ("C1-CTL-6", "host-forged", m_host, "host:H02", {"H02"}),
    ("C1-CTL-7", "pin-tamper", m_pin, "pin_hash", {"K08", "K09"}),
]


# ----------------------------------------------------------------- counter run

def run_counter(work: Path, counter: Path, d: Path, sha: str, name: str):
    w = Path(tempfile.mkdtemp(prefix="cwork-" + name + "-", dir=str(work)))
    try:
        p = subprocess.run(
            [sys.executable, "-I", str(counter), "--repo", str(d), "--rev", sha, "--work", str(w)],
            cwd=str(w), env=_env(work), capture_output=True, timeout=CHILD_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return None, None, "counter timed out after %ds" % CHILD_TIMEOUT
    except OSError as e:
        return None, None, "counter did not start: %s" % e
    out = p.stdout.decode("utf-8", "replace")
    lines = [l for l in out.split("\n") if l.strip()]
    if len(lines) != 1:
        return p.returncode, None, "counter stdout has %d non-empty lines, need exactly 1" % len(lines)
    m = LINE_RE.match(lines[0])
    if not m:
        return p.returncode, None, "counter line unparsable: %r" % lines[0][:200]
    missed = m["missed"]
    legs = [] if missed == "none" else missed.split(",")
    if missed != "none" and not all(LEG_RE.match(x) for x in legs):
        return p.returncode, None, "counter missed= unparsable: %r" % missed[:200]
    return p.returncode, {**m.groupdict(), "legs": legs}, None


def judge_good(sha: str, rc, rec, err) -> str | None:
    """None when the counter printed the full green line on the unmutated tree, else the reason."""
    return None  # MUTANT M15a: good-tree check dropped
    if err:
        return err
    if rec["rev"] != sha:
        return "rev=%s, passed %s" % (rec["rev"], sha)
    if rec["verdict"] != "TARGET_MET" or rec["missed"] != "none":
        return "verdict=%s missed=%s" % (rec["verdict"], rec["missed"])
    if (rec["rows"], rec["hosts"], rec["new"]) != ("18", "6", "3") or rec["sa"] != rec["sb"] or int(rec["sa"]) < 1:
        return "counts rows=%s hosts=%s sources=%s/%s new_rows=%s not 18/6/n=n/3" % (
            rec["rows"], rec["hosts"], rec["sa"], rec["sb"], rec["new"])
    if rc != 0:
        return "exit status %s, need 0" % rc
    return None


def judge_control(sha: str, rc, rec, err, required: str, owned) -> str | None:
    """None when the counter caught the control exactly as registered, else the reason."""
    if err:
        return err
    if rec["rev"] != sha:
        return "rev=%s, passed %s" % (rec["rev"], sha)
    if rec["verdict"] != "TARGET_MISSED":
        return "verdict=%s (mutant admitted)" % rec["verdict"]
    if rc != 1:
        return "exit status %s, need 1 on a verdict miss" % rc
    legs = rec["legs"]
    if required not in legs:
        return "required leg %s not in missed=%s" % (required, rec["missed"])
    if False:  # MUTANT M15b: owned check dropped
        if "entry_absent" in legs:
            return "entry_absent named for a tree whose entry exists"
        for leg in legs:
            m = ID_LEG_RE.match(leg)
            if m and m[1] not in owned:
                return "leg %s names a row the mutation did not touch" % leg
    return None


# ---------------------------------------------------------------------- run

def parse(argv):
    ap = argparse.ArgumentParser(prog="r55_ctl_c1", add_help=False)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--counter")
    ap.add_argument("--claim", choices=["c1"])
    try:
        return ap.parse_args(argv)
    except SystemExit:
        raise Setup("usage: --repo R --rev REV --work DIR [--counter PATH]")


def run(argv) -> int:
    try:
        return _run(argv)
    except Setup as e:
        sys.stderr.write("MADO_R55_CONTROLS setup error: %s\n" % e)
        return 2


def _run(argv) -> int:
    a = parse(list(argv))
    repo = os.path.realpath(a.repo)
    work0 = Path(a.work)
    work0.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="c1h-", dir=str(work0.resolve())))
    try:
        return _body(a, repo, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def _body(a, repo: str, work: Path) -> int:
    import json

    rev = git(work, "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}").decode().strip()
    ft = read_tree(work, repo, rev, [FROZEN_PATH])
    if FROZEN_PATH not in ft:
        raise Setup("%s absent at %s" % (FROZEN_PATH, rev))
    try:
        c1 = json.loads(ft[FROZEN_PATH])["c1"]
        ctx = {"entry": c1["entry"], "pin_dir": c1["pin_dir"], "pin_sha256": c1["pin_sha256"]}
    except (ValueError, KeyError, TypeError) as e:
        raise Setup("frozen-tables.json c1 unreadable: %r" % e)

    tree = read_tree(work, repo, rev, [ctx["entry"], FROZEN_PATH, ctx["pin_dir"], *EXTRA_PATHS])

    cdir = work / "counter"
    cdir.mkdir()
    counter = cdir / "c1-counter.py"
    counter_missing = False
    if a.counter:
        src = Path(a.counter)
        try:
            counter.write_bytes(src.read_bytes())
        except OSError as e:
            raise Setup("--counter unreadable: %s" % e)
    else:
        got = read_tree(work, repo, rev, [COUNTER_PATH])
        if COUNTER_PATH in got:
            counter.write_bytes(got[COUNTER_PATH])
        else:
            counter_missing = True
            sys.stderr.write("counter %s absent at %s: good=bad, every control fails\n" % (COUNTER_PATH, rev))

    base = work / "repos"
    base.mkdir()

    # good tree
    good_ok = False
    if not counter_missing:
        d, sha = materialize(work, base, "good", tree)
        rc, rec, err = run_counter(work, counter, d, sha, "good")
        why = judge_good(sha, rc, rec, err)
        good_ok = why is None
        sys.stderr.write("good: %s%s\n" % ("ok" if good_ok else "bad", "" if good_ok else " - " + why))

    passed = 0
    for cid, name, mut, required, owned in CONTROLS:
        if counter_missing:
            sys.stderr.write("%s %s: FAIL - no counter\n" % (cid, name))
            continue
        try:
            mtree = mut(tree, ctx)
        except MutationError as e:
            sys.stderr.write("%s %s: FAIL - mutation not applicable: %s\n" % (cid, name, e))
            continue
        d, sha = materialize(work, base, cid.lower(), mtree)
        rc, rec, err = run_counter(work, counter, d, sha, cid.lower())
        why = judge_control(sha, rc, rec, err, required, owned)
        if why is None:
            passed += 1
            sys.stderr.write("%s %s: ok - counter missed=%s\n" % (cid, name, ",".join(rec["legs"])))
        else:
            sys.stderr.write("%s %s: FAIL - %s\n" % (cid, name, why))

    verdict = "OK" if good_ok and passed == len(CONTROLS) else "FAIL"
    sys.stdout.write("MADO_R55_CONTROLS: claim=c1 good=%s controls=%d/7 verdict=%s\n"
                     % ("ok" if good_ok else "bad", passed, verdict))
    sys.stdout.flush()
    return 0 if verdict == "OK" else 1


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
