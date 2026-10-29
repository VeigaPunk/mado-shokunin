#!/usr/bin/env python3
"""R56 C1 control harness (independent of the counter).

    python3 -I r56_ctl_c1.py --repo REPO --rev REV --work DIR [--counter PATH] [--claim c1]

Builds, for the good tree at REV and for each of the ten frozen C1 controls
(registration.md section C1), one scratch git repository (D=$(mktemp -d -p WORK);
git -C "$D" ...) from a `git archive` of the good tree's counter-relevant paths
at REV, applies exactly ONE mutation, commits it with the ctl identity and runs
the counter as a child process (python3 -I, scrubbed GIT_* environment,
TMPDIR=WORK) against it. The harness holds the expectations; the counter is
never told which control it is running.

A control is PASSED when the counter exits 1, prints exactly one parsable
MADO_AUTORELOAD_ENTRY line with verdict=TARGET_MISSED (so no TARGET_MET), and
`missed` contains the control's required leg. `good` is ok when the counter
prints the full green line (30/3/30/30/33/8, TARGET_MET, missed=none) and
exits 0 on the unmutated tree.

stdout: exactly one line
    MADO_R56_CONTROLS: claim=c1 good=<ok|bad> controls=<k>/12 verdict=<OK|FAIL>
stderr: per-control detail (also non-binding observations such as collateral
legs). exit 0 on OK (good=ok and k=10), 1 on FAIL, 2 on setup error (nothing
on stdout). The repo is read only through git objects at REV; every temporary
file is under --work.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TABLES_PATH = ".ufo/waves/round-56/frozen-tables-v2.json"
TABLES_SHA256 = "9511151ac2f72097310780357b4a3018e799691cca11905bf75a7e5f6bd795e2"
COUNTER_PATH = "quality/counters/c1-r56-autoreload-entry.py"
EXTRA_PATHS = ("corpus/README.md", "corpus/SOURCES.md")
CHILD_TIMEOUT = 120
N_CONTROLS = 12
GOOD_COUNTS = {"rows": 30, "hosts": 3, "sources": 30, "scope": 30, "content": 33, "new": 8}

LINE_RE = re.compile(
    r"^MADO_AUTORELOAD_ENTRY: rev=(?P<rev>\S+) rows=(?P<rows>\d+)/30 hosts=(?P<hosts>\d+)/3 "
    r"sources=(?P<sources>\d+)/30 scope=(?P<scope>\d+)/30 content=(?P<content>\d+)/33 "
    r"new_rows=(?P<new>\d+)/8 verdict=(?P<verdict>TARGET_MET|TARGET_MISSED) missed=(?P<missed>\S+)$"
)
LEG_RE = re.compile(
    r"^(?:entry_absent|tables_sha|prov|index|pin_hash|new_rows"
    r"|(?:row|quote|host|source_cell|scope|tok|num|echo):[KH][0-9]{2})$"
)
ROW_RE = re.compile(r"^\|\s*([KH][0-9]{2})\s*\|")
REG_RE = re.compile(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|")
FENCE_RE = re.compile(r"^ {0,3}(```|~~~)")


class Setup(Exception):
    """Cannot run at all (exit 2)."""


class MutationError(Exception):
    """The frozen mutation cannot be applied to this tree (the control fails)."""


# --------------------------------------------------------------------------- env / git

def _env(work: Path) -> dict:
    # No GIT_* variable crosses into any child; HOME and TMPDIR are the work dir.
    return {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": str(work),
        "TMPDIR": str(work),
        "LC_ALL": "C.UTF-8",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_TERMINAL_PROMPT": "0",
    }


def git(work: Path, *args: str, check: bool = True, stdin: bytes | None = None) -> bytes:
    p = subprocess.run(["git", *args], env=_env(work), capture_output=True, input=stdin, cwd=str(work))
    if check and p.returncode != 0:
        raise Setup("git %s failed: %s" % (" ".join(args[:5]), p.stderr.decode("utf-8", "replace").strip()))
    return p.stdout


def ls_present(work: Path, repo: str, rev: str, paths: list[str]) -> set[str]:
    """Which of PATHS (files or directories) exist at REV (any mode: archive carries symlinks too)."""
    present: set[str] = set()
    for p in paths:
        out = git(work, "-C", repo, "ls-tree", "-z", rev, "--", p)
        if out.strip(b"\0"):
            present.add(p)
    return present


def export_good(work: Path, repo: str, rev: str, paths: list[str], dest: Path) -> None:
    """`git archive` of the good tree's counter-relevant paths at REV, extracted with tar (symlinks and modes preserved)."""
    present = sorted(ls_present(work, repo, rev, paths))
    dest.mkdir(parents=True, exist_ok=True)
    if not present:
        return
    tar = git(work, "-C", repo, "archive", "--format=tar", rev, "--", *present)
    p = subprocess.run(["tar", "-x", "-C", str(dest)], input=tar, env=_env(work), capture_output=True)
    if p.returncode != 0:
        raise Setup("tar -x failed: %s" % p.stderr.decode("utf-8", "replace").strip())


def materialize(work: Path, base: Path, name: str, good: Path, mutate) -> tuple[Path, str]:
    """D=$(mktemp -d -p base); git -C D init; copy good tree; apply ONE mutation; commit as ctl; return (D, sha)."""
    d = Path(tempfile.mkdtemp(prefix="scratch-", dir=str(base)))  # neutral name: the counter must not learn which control it runs
    git(work, "-C", str(d), "init", "-q", "-b", "main")
    top = git(work, "-C", str(d), "rev-parse", "--show-toplevel").decode().strip()
    if os.path.realpath(top) != os.path.realpath(str(d)):
        raise Setup("scratch repo toplevel %s != %s" % (top, d))
    shutil.copytree(good, d, symlinks=True, dirs_exist_ok=True)
    if mutate is not None:
        mutate(d)
    git(work, "-C", str(d), "add", "-A")
    git(work, "-C", str(d), "-c", "user.name=ctl", "-c", "user.email=ctl@ctl", "-c", "commit.gpgsign=false",
        "commit", "-q", "--allow-empty", "-m", "ctl scratch commit")
    sha = git(work, "-C", str(d), "rev-parse", "HEAD").decode().strip()
    return d, sha


# ----------------------------------------------------------------- file helpers

def _reg(d: Path, rel: str) -> Path:
    p = d / rel
    if p.is_symlink() or not p.is_file():
        raise MutationError("%s is not a regular file in the good tree" % rel)
    return p


def _read_lines(d: Path, rel: str) -> list[str]:
    return _reg(d, rel).read_bytes().decode("utf-8").split("\n")


def _write_lines(d: Path, rel: str, before: list[str], lines: list[str]) -> None:
    if lines == before:
        raise MutationError("mutation of %s changed nothing" % rel)
    _reg(d, rel).write_bytes("\n".join(lines).encode("utf-8"))


def entry_rows(lines: list[str]) -> dict[str, list[int]]:
    """Rows (id -> line indexes) outside fenced code blocks and HTML comments, first cell K##/H##."""
    rows: dict[str, list[int]] = {}
    fence = None
    in_comment = False
    for i, l in enumerate(lines):
        if in_comment:
            if "-->" in l:
                in_comment = False
            continue
        m = FENCE_RE.match(l)
        if fence is not None:
            if m and m.group(1) == fence:
                fence = None
            continue
        if m:
            fence = m.group(1)
            continue
        r = ROW_RE.match(l)
        if r:
            rows.setdefault(r.group(1), []).append(i)
        k = l.rfind("<!--")
        if k >= 0 and l.find("-->", k) < 0:
            in_comment = True
    return rows


def _row(lines: list[str], rid: str) -> int:
    hits = entry_rows(lines).get(rid, [])
    if len(hits) != 1:
        raise MutationError("row %s present %d times, need exactly 1" % (rid, len(hits)))
    return hits[0]


def _cells(line: str, rid: str) -> list[str]:
    if not (line.startswith("| ") and line.endswith(" |")):
        raise MutationError("row %s not in `| a | b |` form" % rid)
    cells = line[2:-2].split(" | ")
    if len(cells) != 5:
        raise MutationError("row %s has %d cells, need 5" % (rid, len(cells)))
    return cells


def _join(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


# ----------------------------------------------------------------- mutations
# Each mutation takes (scratch dir, ctx) and edits regular files in place.

def m_entry_absent(d: Path, ctx) -> None:
    _reg(d, ctx["entry"]).unlink()


def m_junk(d: Path, ctx) -> None:
    lines = _read_lines(d, ctx["entry"])
    before = list(lines)
    rows = entry_rows(lines)
    for rid in ctx["k_ids"]:
        idx = rows.get(rid, [])
        if len(idx) != 1:
            raise MutationError("row %s present %d times, need exactly 1" % (rid, len(idx)))
        cells = _cells(lines[idx[0]], rid)
        if rid.startswith("K"):
            cells[1] = "placeholder proposition text for row %s, not a claim about any source line" % rid
        else:
            cells[1] = "placeholder host proposition %s, not a read" % rid
        lines[idx[0]] = _join(cells)
    _write_lines(d, ctx["entry"], before, lines)


def m_false_number(d: Path, ctx) -> None:
    lines = _read_lines(d, ctx["entry"])
    before = list(lines)
    i = _row(lines, "K04")
    cells = _cells(lines[i], "K04")
    cells[1] = cells[1] + " The value is capped at 200 by this call."
    lines[i] = _join(cells)
    _write_lines(d, ctx["entry"], before, lines)


def m_cross_pin_source(d: Path, ctx) -> None:
    lines = _read_lines(d, ctx["entry"])
    before = list(lines)
    i = _row(lines, "K10")
    cells = _cells(lines[i], "K10")
    if cells[2] != "S383":
        raise MutationError("K10 cites %r, expected S383" % cells[2])
    cells[2] = "S385"
    lines[i] = _join(cells)
    _write_lines(d, ctx["entry"], before, lines)


def m_scope_swap(d: Path, ctx) -> None:
    reg = _read_lines(d, "corpus/SOURCES.md")
    regb = list(reg)
    if any(REG_RE.match(l) and REG_RE.match(l).group(1) == "S399" for l in reg):
        raise MutationError("registry already holds S399")
    src = [i for i, l in enumerate(reg) if REG_RE.match(l) and REG_RE.match(l).group(1) == "S383"]
    if len(src) != 1:
        raise MutationError("registry holds S383 %d times, need exactly 1" % len(src))
    s = reg[src[0]]
    lead = s[: len(s) - len(s.lstrip(" "))]
    body = s.strip()
    if not (body.startswith("|") and body.endswith("|")):
        raise MutationError("S383 row is not pipe-delimited")
    cells = body[1:-1].split("|")
    if len(cells) != 11:
        raise MutationError("S383 row has %d cells, need 11" % len(cells))
    cells[0] = " S399 "
    cells[3] = " A "            # tier
    cells[5] = " ConfigWatcher.cpp:1-10 "  # anchor: excludes K10's line 67
    cells[7] = " mined "        # status
    cells[8] = " 2026-10-28 "   # opened
    cells[10] = " %s " % ctx["entry"]  # used-by names the entry
    reg.insert(src[0] + 1, lead + "|" + "|".join(cells) + "|")
    _write_lines(d, "corpus/SOURCES.md", regb, reg)

    lines = _read_lines(d, ctx["entry"])
    before = list(lines)
    i = _row(lines, "K10")
    row = _cells(lines[i], "K10")
    if row[2] != "S383":
        raise MutationError("K10 cites %r, expected S383" % row[2])
    row[2] = "S399"
    lines[i] = _join(row)
    _write_lines(d, ctx["entry"], before, lines)


def m_prov_dangling(d: Path, ctx) -> None:
    lines = _read_lines(d, ctx["entry"])
    before = list(lines)
    hits = [i for i, l in enumerate(lines[:15]) if l.startswith("source:")]
    if not hits:
        raise MutationError("no `source:` line in the first 15 lines")
    lines[hits[0]] = lines[hits[0]] + ", S999"
    _write_lines(d, ctx["entry"], before, lines)


def m_dropped_row(d: Path, ctx) -> None:
    lines = _read_lines(d, ctx["entry"])
    before = list(lines)
    del lines[_row(lines, "K17")]
    _write_lines(d, ctx["entry"], before, lines)


def m_edited_quote(d: Path, ctx) -> None:
    lines = _read_lines(d, ctx["entry"])
    before = list(lines)
    i = _row(lines, "K05")
    cells = _cells(lines[i], "K05")
    q = cells[4]
    if len(q) < 3 or q[0] != "`" or q[-1] != "`":
        raise MutationError("K05 quote cell is not backtick-delimited: %r" % q)
    # ONE character inside the quote cell: the last quoted character (identifier tokens stay intact).
    last = q[-2]
    cells[4] = q[:-2] + ("." if last != "." else ",") + "`"
    lines[i] = _join(cells)
    _write_lines(d, ctx["entry"], before, lines)


def m_pin_byte(d: Path, ctx) -> None:
    rel = ctx["pin_dir"] + "/Hyprland-ConfigWatcher.cpp"
    p = _reg(d, rel)
    data = bytearray(p.read_bytes())
    if not data:
        raise MutationError("pin is empty")
    # ONE byte of line 1 (no frozen row quotes line 1); keep length, newlines and the encoding class.
    nb = data[0] ^ 0x01
    if nb in (0x0A, 0x0D) or nb >= 0x80 or data[0] >= 0x80 or data[0] == 0x0A:
        raise MutationError("first byte %r cannot be flipped safely" % bytes(data[:1]))
    data[0] = nb
    p.write_bytes(bytes(data))


def m_new_row_missing(d: Path, ctx) -> None:
    reg = _read_lines(d, "corpus/SOURCES.md")
    regb = list(reg)
    hits = [i for i, l in enumerate(reg) if REG_RE.match(l) and REG_RE.match(l).group(1) == "S390"]
    if len(hits) != 1:
        raise MutationError("registry holds S390 %d times, need exactly 1" % len(hits))
    del reg[hits[0]]
    _write_lines(d, "corpus/SOURCES.md", regb, reg)


def m_quote_echo(d: Path, ctx) -> None:
    """registration-v2 E5 control 11: every K and H proposition whose frozen quote has >=30 characters becomes `<quote> echoed ...`."""
    lines = _read_lines(d, ctx["entry"])
    before = list(lines)
    rows = entry_rows(lines)
    n = 0
    for rid in ctx["k_ids"] + ctx["h_ids"]:
        idx = rows.get(rid, [])
        if len(idx) != 1:
            raise MutationError("row %s present %d times, need exactly 1" % (rid, len(idx)))
        cells = _cells(lines[idx[0]], rid)
        q = cells[4]
        if len(q) >= 2 and q[0] == "`" and q[-1] == "`" and len(q) - 2 >= 30:
            cells[1] = q[1:-1] + " echoed on this line, no analysis added here"
            lines[idx[0]] = _join(cells)
            n += 1
    if n == 0:
        raise MutationError("no row with a quote of >=30 characters")
    _write_lines(d, ctx["entry"], before, lines)


def m_anchor_past_eof(d: Path, ctx) -> None:
    """registration-v2 E5 control 12: the anchor cell of S383 becomes `ConfigWatcher.cpp:1-9999`."""
    reg = _read_lines(d, "corpus/SOURCES.md")
    regb = list(reg)
    hits = [i for i, l in enumerate(reg) if REG_RE.match(l) and REG_RE.match(l).group(1) == "S383"]
    if len(hits) != 1:
        raise MutationError("registry holds S383 %d times, need exactly 1" % len(hits))
    s = reg[hits[0]]
    lead = s[: len(s) - len(s.lstrip(" "))]
    body = s.strip()
    cells = body[1:-1].split("|")
    if len(cells) != 11:
        raise MutationError("S383 row has %d cells, need 11" % len(cells))
    cells[5] = " ConfigWatcher.cpp:1-9999 "
    reg[hits[0]] = lead + "|" + "|".join(cells) + "|"
    _write_lines(d, "corpus/SOURCES.md", regb, reg)


def _need_echo(rec):
    if not any(l.startswith("echo:") for l in rec["legs"]):
        return "no echo:<id> leg in missed=%s" % rec["missed"]
    return None


# ----------------------------------------------------------------- expectations (held here, never given to the counter)
# check(rec) -> None when the control is caught as registered, else the reason.
# rec["legs"] is the list of missed legs; rec["content"] the e in content=e/33.

def _need(leg: str):
    def check(rec):
        if leg not in rec["legs"]:
            return "required leg %s not in missed=%s" % (leg, rec["missed"])
        return None
    return check


def _need_junk(rec):
    if not {"tok:H01", "tok:H02", "tok:H03"} <= set(rec["legs"]):
        return "H rows not junked: %s" % rec["missed"]
    if not any(l.startswith("tok:") for l in rec["legs"]):
        return "no tok:<id> leg in missed=%s" % rec["missed"]
    if rec["content"] >= 33:
        return "content=%d/33, need a shortfall (e<33)" % rec["content"]
    return None


# (id, name, mutation, required-leg text, check, collateral legs the registration itself names)
CONTROLS = [
    ("C1-CTL-01", "entry-absent", m_entry_absent, "entry_absent", _need("entry_absent"), ()),
    ("C1-CTL-02", "junk-placeholders", m_junk, "tok:<id> + content<33", _need_junk, ()),
    ("C1-CTL-03", "false-number", m_false_number, "num:K04", _need("num:K04"), ()),
    ("C1-CTL-04", "cross-pin-source", m_cross_pin_source, "source_cell:K10", _need("source_cell:K10"), ()),
    ("C1-CTL-05", "scope-swap", m_scope_swap, "scope:K10", _need("scope:K10"), ("source_cell:K10",)),
    ("C1-CTL-06", "provenance-dangling", m_prov_dangling, "prov", _need("prov"), ()),
    ("C1-CTL-07", "dropped-row", m_dropped_row, "row:K17", _need("row:K17"), ()),
    ("C1-CTL-08", "edited-quote", m_edited_quote, "row:K05", _need("row:K05"), ("quote:K05", "source_cell:K05")),
    ("C1-CTL-09", "pin-byte", m_pin_byte, "pin_hash", _need("pin_hash"), ()),
    ("C1-CTL-10", "new-row-missing", m_new_row_missing, "new_rows", _need("new_rows"), ("source_cell:K##",)),
    ("C1-CTL-11", "quote-echo", m_quote_echo, "echo:<id>", _need_echo, ()),
    ("C1-CTL-12", "anchor-past-eof", m_anchor_past_eof, "scope:K03", _need("scope:K03"), ("scope:K##",)),
]


# ----------------------------------------------------------------- counter run

def run_counter(work: Path, counter: Path, d: Path, sha: str, name: str):
    """-> (returncode, record|None, error|None, nonempty stderr text)."""
    w = Path(tempfile.mkdtemp(prefix="cwork-", dir=str(work)))
    try:
        try:
            p = subprocess.run(
                [sys.executable, "-I", str(counter), "--repo", str(d), "--rev", sha, "--work", str(w)],
                cwd=str(w), env=_env(work), capture_output=True, timeout=CHILD_TIMEOUT,
            )
        except subprocess.TimeoutExpired:
            return None, None, "counter timed out after %ds" % CHILD_TIMEOUT, ""
        except OSError as e:
            return None, None, "counter did not start: %s" % e, ""
    finally:
        shutil.rmtree(w, ignore_errors=True)
    err = p.stderr.decode("utf-8", "replace").strip()
    out = p.stdout.decode("utf-8", "replace")
    lines = [l for l in out.split("\n") if l.strip()]
    if len(lines) != 1:
        return p.returncode, None, "counter stdout has %d non-empty lines, need exactly 1" % len(lines), err
    m = LINE_RE.match(lines[0])
    if not m:
        return p.returncode, None, "counter line unparsable: %r" % lines[0][:200], err
    missed = m["missed"]
    legs = [] if missed == "none" else missed.split(",")
    if missed != "none" and not all(LEG_RE.match(x) for x in legs):
        return p.returncode, None, "counter missed= has a leg outside the registered grammar: %r" % missed[:200], err
    rec = {k: m[k] for k in ("rev", "verdict", "missed")}
    for k in ("rows", "hosts", "sources", "scope", "content", "new"):
        rec[k] = int(m[k])
    rec["legs"] = legs
    return p.returncode, rec, None, err


def judge_good(sha: str, rc, rec, err) -> str | None:
    """None when the counter printed the full green line on the unmutated tree, else the reason."""
    if err:
        return err
    if rec["rev"] != sha:
        return "rev=%s, passed %s" % (rec["rev"], sha)
    if rec["verdict"] != "TARGET_MET" or rec["missed"] != "none":
        return "verdict=%s missed=%s" % (rec["verdict"], rec["missed"])
    got = {k: rec[k] for k in GOOD_COUNTS}
    if got != GOOD_COUNTS:
        return "counts %r, need %r" % (got, GOOD_COUNTS)
    if rc != 0:
        return "exit status %s, need 0" % rc
    return None


def judge_control(sha: str, rc, rec, err, check) -> str | None:
    """None when the counter caught the control exactly as registered, else the reason."""
    if err:
        return err
    if rec["rev"] != sha:
        return "rev=%s, passed %s" % (rec["rev"], sha)
    if rec["verdict"] == "TARGET_MET":
        return "verdict=TARGET_MET (mutant admitted)"
    if rc != 1:
        return "exit status %s, need 1 on a verdict miss" % rc
    return check(rec)


# ---------------------------------------------------------------------- run

def parse(argv):
    ap = argparse.ArgumentParser(prog="r56_ctl_c1", add_help=False)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--counter")
    ap.add_argument("--claim", choices=["c1"])
    try:
        return ap.parse_args(argv)
    except SystemExit:
        raise Setup("usage: --repo R --rev REV --work DIR [--counter PATH] [--claim c1]")


def run(argv) -> int:
    try:
        return _run(argv)
    except Setup as e:
        sys.stderr.write("MADO_R56_CONTROLS setup error: %s\n" % e)
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
    rev = git(work, "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}").decode().strip()

    # frozen tables: blob at REV must hold the embedded sha256, else this is not the frozen round
    meta = git(work, "-C", repo, "ls-tree", "-z", rev, "--", TABLES_PATH)
    if not meta.strip(b"\0"):
        raise Setup("%s absent at %s" % (TABLES_PATH, rev))
    mode, typ, rest = meta.split(b"\0")[0].decode().split(" ", 2)
    if typ != "blob" or mode not in ("100644", "100755"):
        raise Setup("%s is not a regular blob at %s" % (TABLES_PATH, rev))
    tables = git(work, "-C", repo, "cat-file", "blob", rest.split("\t")[0])
    if hashlib.sha256(tables).hexdigest() != TABLES_SHA256:
        raise Setup("%s at %s does not hash to the frozen %s" % (TABLES_PATH, rev, TABLES_SHA256))
    try:
        c1 = json.loads(tables)["c1"]
        ctx = {
            "entry": c1["entry"],
            "pin_dir": c1["pin_dir"],
            "k_ids": [r["id"] for r in c1["k"]],
            "h_ids": [r["id"] for r in c1["h"]],
        }
    except (ValueError, KeyError, TypeError) as e:
        raise Setup("frozen-tables.json c1 unreadable: %r" % e)
    if len(ctx["k_ids"]) != 30 or len(ctx["h_ids"]) != 3:
        raise Setup("frozen-tables.json c1 holds %d K / %d H rows, need 30 / 3" % (len(ctx["k_ids"]), len(ctx["h_ids"])))

    good = work / "good-tree"
    export_good(work, repo, rev, [ctx["entry"], TABLES_PATH, ctx["pin_dir"], *EXTRA_PATHS], good)

    cdir = work / "counter"
    cdir.mkdir()
    counter = cdir / "c1-counter.py"
    counter_missing = False
    if a.counter:
        try:
            counter.write_bytes(Path(a.counter).read_bytes())
        except OSError as e:
            raise Setup("--counter unreadable: %s" % e)
    else:
        if COUNTER_PATH in ls_present(work, repo, rev, [COUNTER_PATH]):
            tar = git(work, "-C", repo, "archive", "--format=tar", rev, "--", COUNTER_PATH)
            p = subprocess.run(["tar", "-x", "-C", str(cdir), "--strip-components=2"], input=tar,
                               env=_env(work), capture_output=True)
            exported = cdir / Path(COUNTER_PATH).name
            if p.returncode != 0 or not exported.is_file() or exported.is_symlink():
                raise Setup("cannot export %s at %s" % (COUNTER_PATH, rev))
            exported.rename(counter)
        else:
            counter_missing = True
            sys.stderr.write("counter %s absent at %s: good=bad, every control fails\n" % (COUNTER_PATH, rev))

    base = work / "repos"
    base.mkdir()

    good_ok = False
    if not counter_missing:
        d, sha = materialize(work, base, "good", good, None)
        rc, rec, err, serr = run_counter(work, counter, d, sha, "good")
        why = judge_good(sha, rc, rec, err)
        good_ok = why is None
        sys.stderr.write("good: %s%s\n" % ("ok" if good_ok else "bad", "" if good_ok else " - " + why))

    # Controls run in a random order and the log is printed in canonical order, so nothing the counter can see
    # (paths, commit message, run order) identifies the control it is running.
    import random
    log: dict[str, list[str]] = {}
    order = list(CONTROLS)
    random.SystemRandom().shuffle(order)
    passed = 0
    for cid, name, mut, required, check, collateral in order:
        msgs = log.setdefault(cid, [])
        if counter_missing:
            msgs.append("%s %s: FAIL - no counter\n" % (cid, name))
            continue
        try:
            d, sha = materialize(work, base, name, good, lambda dd, m=mut: m(dd, ctx))
        except MutationError as e:
            msgs.append("%s %s: FAIL - mutation not applicable: %s\n" % (cid, name, e))
            continue
        rc, rec, err, serr = run_counter(work, counter, d, sha, name)
        why = judge_control(sha, rc, rec, err, check)
        if why is None:
            passed += 1
            msgs.append("%s %s: ok (required %s) - counter missed=%s\n" % (cid, name, required, _clip(rec["legs"])))
            extra = [l for l in rec["legs"] if not _expected_leg(l, required, collateral)]
            if extra:
                msgs.append("  note: collateral legs beyond the registered ones: %s\n" % _clip(extra))
        else:
            msgs.append("%s %s: FAIL - %s\n" % (cid, name, why))
    for cid in sorted(log):
        sys.stderr.write("".join(log[cid]))

    # The denominator is the frozen 10, never len(CONTROLS): a dropped control cannot pass.
    verdict = "OK" if good_ok and passed == N_CONTROLS and len(CONTROLS) == N_CONTROLS else "FAIL"
    sys.stdout.write("MADO_R56_CONTROLS: claim=c1 good=%s controls=%d/%d verdict=%s\n"
                     % ("ok" if good_ok else "bad", passed, N_CONTROLS, verdict))
    sys.stdout.flush()
    return 0 if verdict == "OK" else 1


def _clip(legs: list, n: int = 8) -> str:
    return ",".join(legs[:n]) + (",...(+%d more)" % (len(legs) - n) if len(legs) > n else "")


def _expected_leg(leg: str, required: str, collateral: tuple) -> bool:
    if leg == required or leg in collateral:
        return True
    if required.startswith("tok:") and leg.startswith("tok:"):
        return True
    if "source_cell:K##" in collateral and leg.startswith("source_cell:K"):
        return True
    return False


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
