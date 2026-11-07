#!/usr/bin/env python3
"""Round-94 C1 counter - file name -> MIME type as GLib 2.90.1 g_content_type_guess answers.

Frozen predicate PRED-C1-r94-v1 (the same sentence as the declaration and the receipt label):
  TARGET_MET iff, at <rev>, tools/mado-mimeglob.py is the frozen candidate (sha256 ==
  --expect-tool-sha256) and (i) on every frozen case the tool's (type, uncertain) equals the
  oracle's, and the oracle re-run at measurement equals the label recorded in the case file
  (else SETUP_ERROR oracle_drift=<ids>); the frozen set holds both modes (text and cache) and
  every class named in the case file; (ii) on N fresh seeded cases from the frozen generator
  (seed printed) the tool equals the live oracle on every name; (iii) on the frozen host name
  list under the host's own environment the tool equals the live oracle on every name; (iv)
  every frozen mutant of the candidate makes at least one frozen case wrong (a mutant that only
  crashes is crashed_not_killed, not killed); (v) each control misses (i): the do-nothing answer
  (application/octet-stream, uncertain 1), the naive extension map (last .ext -> highest-weight
  type in the dirs' globs2, uncertain 0), and the base revision (no tool -> 0 answered).

Frozen amendments before any measurement (round-94 w1 critic R94MCritic C1-F1..F5, folded in by the L1):
  (i) the class clause is the enumerated list CLASSES below: every one of the 20 classes holds >= 6
  frozen cases and no case carries another class (printed classes=20/20); (iv) the frozen mutant file
  holds >= 40 counted mutants; (v) the naive map is scored both exact and ASCII-folded and the stronger
  reading must still miss; (vi) static_no_external_resolver: the tool's source parses, imports none of
  subprocess/socket/multiprocessing/pty/importlib/urllib/http/xmlrpc, calls no os.system/popen/exec*/spawn*/
  posix_spawn*/fork and no eval/exec/compile/__import__, and every ctypes library it names is libc ("c" or
  "libc.so.6"); every tool run gets PATH = an empty scratch directory and no other environment.  The host
  leg prints the sha256 of every mime.cache/globs2 under the host dirs it uses.

A case is correct when, for every name of the case, the tool's (type, uncertain) equals the
oracle label (type string and uncertain 0/1).  A name the tool does not answer (exit 3
UNSUPPORTED, nonzero exit, or no well-formed --json output) counts as wrong, never as answered.
A mutant is killed iff >=1 frozen case yields a well-formed JSON answer that differs from the
label.  A mutant that is not killed but crashes (nonzero exit / no JSON) on a case where the candidate
does not crash is crashed_not_killed; a crash the candidate shares is not the mutant's and does not count.
Any other survivor is survived.
A mutant whose `find` occurs != 1 time in the measured tool is a SETUP_ERROR rc 2.

The oracle is compiled once from --oracle-src (sha256 pinned by --expect-oracle-sha256) into
--scratch-root with `gcc -O1 ... $(pkg-config --cflags --libs gio-2.0)`; its binary sha256 and
`pacman -Q glib2 shared-mime-info` are printed.  Every frozen input (--cases, --mutants,
--fresh-gen, --host-names, --expect-tool-sha256 is checked against the tool bytes) is pinned by
--expect-*-sha256; a mismatch is SETUP_ERROR rc 2.  All materialisation (case fixtures via
{root} substitution and base64 file bytes, fresh cases, host fixtures) lives under
--scratch-root; TMPDIR is honoured for every mkdtemp.  Stdlib only.
rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR, 3 DRAFT (--draft-tool PATH; prints DRAFT_*).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

PRED = "PRED-C1-r94-v1"
CLASSES = ("dirs", "mode", "literal", "simple", "full", "fold", "cs", "deep", "weight", "dupe", "order", "multi",
           "nomatch", "slash", "bytes", "fgets", "v1", "noglobs", "cachefmt", "mixed")
MIN_PER_CLASS = 6
MIN_MUTANTS = 40
_EMPTY_PATH = ""
TOOL = "tools/mado-mimeglob.py"
UNKNOWN = "application/octet-stream"
TOOL_TIMEOUT = 120.0
ORACLE_TIMEOUT = 120.0
FRESH_RUN_TIMEOUT = 600.0


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: str) -> str:
    return sha(open(p, "rb").read())


def git_show(repo: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def unb64(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))


# ---------------------------------------------------------------- oracle

class Oracle:
    """The compiled g_content_type_guess binary, run as env -i LC_ALL=C + the case env."""

    def __init__(self, binary: str):
        self.binary = binary

    def run(self, names: list[bytes], env_extra: dict[str, str | None], cwd: str) -> list[tuple[str, int]] | None:
        env = {"LC_ALL": "C"}
        for k, v in env_extra.items():
            if v is None:
                continue
            env[k] = v
        argv = [self.binary] + [n.decode("utf-8", "surrogateescape") for n in names]
        try:
            r = subprocess.run(argv, capture_output=True, text=True, timeout=ORACLE_TIMEOUT,
                               env=env, cwd=cwd)
        except (OSError, subprocess.TimeoutExpired):
            return None
        if r.returncode != 0:
            return None
        lines = r.stdout.splitlines()
        if len(lines) != len(names):
            return None
        out = []
        for ln in lines:
            m = re.fullmatch(r"([^\t]*)\t([01])", ln)
            if not m:
                return None
            out.append((m.group(1), int(m.group(2))))
        return out


def oracle_env(case: dict, root: str) -> dict[str, str | None]:
    """The case's env mapping with {root} substituted; a null value means the variable is unset."""
    e = case.get("env", {})
    out: dict[str, str | None] = {}
    for k in ("HOME", "XDG_DATA_HOME", "XDG_DATA_DIRS"):
        v = e.get(k)
        out[k] = None if v is None else v.replace("{root}", root)
    # a key absent from the case env means unset too, except HOME which GLib needs
    return out


# ---------------------------------------------------------------- case materialisation

def materialise(case: dict, root: str) -> None:
    """Write every file; a key ending in '/' is a directory (a case may name a directory `mime.cache`)."""
    for rel, b64 in case.get("files", {}).items():
        p = os.path.join(root, rel)
        if rel.endswith("/"):
            os.makedirs(p, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(unb64(b64))


def case_names(case: dict) -> list[bytes]:
    return [unb64(s) for s in case.get("names_b64", [])]


def labels_of(case: dict) -> list[tuple[str, int]]:
    return [(t, int(u)) for t, u in case.get("labels", [])]


# ---------------------------------------------------------------- tool run

def tool_argv(tool: str, names: list[bytes], env: dict[str, str | None], root: str) -> list[str]:
    """Map the case env (HOME / XDG_DATA_HOME / XDG_DATA_DIRS) onto the tool's flags."""
    argv = [sys.executable, "-I", tool, "--json"]
    dh = env.get("XDG_DATA_HOME")
    if dh is None:
        argv.append("--data-home-unset")
    else:
        argv += ["--data-home", dh]
    dd = env.get("XDG_DATA_DIRS")
    if dd is None:
        argv.append("--data-dirs-unset")
    else:
        argv += ["--data-dirs", dd]
    home = env.get("HOME")
    if home is None:
        argv.append("--home-unset")
    else:
        argv += ["--home", home]
    argv += ["--"] + [n.decode("utf-8", "surrogateescape") for n in names]
    return argv


def run_tool_json(tool: str, names: list[bytes], env: dict[str, str | None], root: str,
                  timeout: float = TOOL_TIMEOUT) -> dict | None:
    """Run the tool; return the parsed --json object, or None on any failure (crash/unsupported)."""
    try:
        r = subprocess.run(tool_argv(tool, names, env, root), capture_output=True, text=True,
                           timeout=timeout, cwd=root, env={"PATH": _EMPTY_PATH})
    except (OSError, subprocess.TimeoutExpired):
        return None
    if r.returncode != 0:
        return None
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None
    res = d.get("results")
    if not isinstance(res, list) or len(res) != len(names):
        return None
    out = []
    for x in res:
        if not isinstance(x, dict) or not isinstance(x.get("type"), str) \
                or x.get("uncertain") not in (0, 1):
            return None
        out.append((x["type"], int(x["uncertain"])))
    return {"answers": out, "mode": d.get("mode"), "dirs": d.get("dirs")}


def case_score(tool: str, case: dict, work: str) -> str:
    """'ok' | 'wrong' | 'crash' for one frozen case against its recorded labels."""
    root = tempfile.mkdtemp(prefix="case-", dir=work)
    try:
        materialise(case, root)
        env = oracle_env(case, root)
        got = run_tool_json(tool, case_names(case), env, root)
        if got is None:
            return "crash"
        return "ok" if got["answers"] == labels_of(case) else "wrong"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def outcomes(tool: str, cases: list[dict], work: str, jobs: int) -> list[str]:
    with ThreadPoolExecutor(jobs) as ex:
        return list(ex.map(lambda c: case_score(tool, c, work), cases))


# ---------------------------------------------------------------- static conjunct (vi)

_BAD_MODULES = {"subprocess", "socket", "multiprocessing", "pty", "importlib", "urllib", "http", "xmlrpc"}
_BAD_OS = re.compile(r"^(system|popen|exec\w*|spawn\w*|posix_spawn\w*|fork\w*)$")
_LIBC = {"c", "libc.so.6"}


def static_check(src: bytes) -> list[str]:
    """Findings that make static_no_external_resolver FAIL (empty list = ok)."""
    import ast
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [f"syntax:{e.lineno}"]
    bad: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                if al.name.split(".")[0] in _BAD_MODULES:
                    bad.append(f"import:{al.name}:{node.lineno}")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] in _BAD_MODULES:
                bad.append(f"import:{node.module}:{node.lineno}")
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "os" and _BAD_OS.match(node.attr):
                bad.append(f"os.{node.attr}:{node.lineno}")
        elif isinstance(node, ast.Call):
            f = node.func
            name = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else "")
            if name in ("eval", "exec", "compile", "__import__"):
                bad.append(f"{name}:{node.lineno}")
            if name in ("CDLL", "PyDLL", "LoadLibrary", "find_library", "cdll", "dlopen"):
                for arg in node.args:
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str) and arg.value not in _LIBC:
                        bad.append(f"lib:{arg.value}:{node.lineno}")
                    elif isinstance(arg, ast.BoolOp):
                        for v in arg.values:
                            if isinstance(v, ast.Constant) and isinstance(v.value, str) and v.value not in _LIBC:
                                bad.append(f"lib:{v.value}:{node.lineno}")
                            elif not isinstance(v, (ast.Constant, ast.Call)):
                                bad.append(f"lib-nonconst:{node.lineno}")
                    elif not isinstance(arg, (ast.Constant, ast.Call)):
                        bad.append(f"lib-nonconst:{node.lineno}")
        elif isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute) \
                and node.value.attr == "cdll":
            bad.append(f"cdll-subscript:{node.lineno}")
    return bad


# ---------------------------------------------------------------- controls

def do_nothing_answers(names: list[bytes]) -> list[tuple[str, int]]:
    return [(UNKNOWN, 1) for _ in names]


def globs2_entries(root: str, env: dict[str, str | None]) -> list[tuple[int, str, str]]:
    """Read every globs2 the case env's xdgmime dir list resolves (in dir order); entries are
    (weight, mime, glob-pattern-bytes-as-text)."""
    dh = env.get("XDG_DATA_HOME")
    first = dh if dh is not None else os.path.join(env.get("HOME") or "/", ".local/share")
    dd = env.get("XDG_DATA_DIRS")
    raw = dd if dd is not None else "/usr/local/share/:/usr/share/"
    dirs = [first + "/mime/"] + [d + "/mime/" for d in raw.split(":") if d]
    out = []
    for d in dirs:
        p = d + "/globs2"
        if not os.path.exists(p):
            continue
        try:
            data = open(p, "rb").read()
        except OSError:
            continue
        for chunk in data.split(b"\n"):
            if not chunk or chunk.startswith(b"#"):
                continue
            parts = chunk.split(b":")
            if len(parts) < 3:
                continue
            try:
                w = int(parts[0])
                mime = parts[1].decode("utf-8", "surrogateescape")
                pat = parts[2].decode("utf-8", "surrogateescape")
            except ValueError:
                continue
            out.append((w, mime, pat))
    return out


def naive_case_answers(case: dict, root: str, fold: bool) -> list[tuple[str, int]]:
    """Declaration control (v): last `.ext` -> highest-weight type among the dirs' globs2 `*.ext` entries,
    uncertain 0.  The declaration does not say whether the extension is case-folded, so both readings are
    scored (fold=False exact, fold=True ASCII-folded) and the gate takes the stronger one."""
    env = oracle_env(case, root)
    idx: dict[str, list[tuple[int, str]]] = {}
    for w, mime, pat in globs2_entries(root, env):
        if pat.startswith("*."):
            key = pat[1:].lower() if fold else pat[1:]
            idx.setdefault(key, []).append((w, mime))
    out = []
    for n in case_names(case):
        base = n.decode("utf-8", "surrogateescape").rsplit("/", 1)[-1]
        ext = "." + base.rsplit(".", 1)[-1] if "." in base else ""
        if fold:
            ext = ext.lower()
        cand = idx.get(ext)
        out.append((max(cand, key=lambda t: t[0])[1] if cand else UNKNOWN, 0))
    return out


def score_naive(cases: list[dict], work: str, jobs: int) -> tuple[int, int]:
    def one(c: dict) -> tuple[bool, bool]:
        root = tempfile.mkdtemp(prefix="naive-", dir=work)
        try:
            materialise(c, root)
            lab = labels_of(c)
            return (naive_case_answers(c, root, False) == lab, naive_case_answers(c, root, True) == lab)
        finally:
            shutil.rmtree(root, ignore_errors=True)
    with ThreadPoolExecutor(jobs) as ex:
        rs = list(ex.map(one, cases))
    return sum(r[0] for r in rs), sum(r[1] for r in rs)


_HEX_ESC = re.compile(rb"\\x([0-9a-fA-F]{2})")


def host_name_list(data: bytes) -> list[bytes]:
    """The frozen host name list: '#' lines are the header; every other non-empty line is one name whose
    raw bytes are written as \\xHH escapes (the only non-ASCII form the file uses). No duplicates allowed."""
    names = []
    for ln in data.split(b"\n"):
        if not ln or ln.startswith(b"#"):
            continue
        names.append(_HEX_ESC.sub(lambda m: bytes([int(m.group(1), 16)]), ln))
    if len(set(names)) != len(names):
        raise ValueError("host name list has duplicate names")
    return names



# ---------------------------------------------------------------- fresh leg

def fresh_cases(gen_path: str, seed: int, n: int, work: str) -> tuple[list[dict], list[list[tuple[str, int]]]]:
    """Run the frozen generator to an unlabelled case file, then label every name with the oracle."""
    gen_out = os.path.join(work, f"fresh-{seed}.json")
    env = dict(os.environ, TMPDIR=work)
    r = subprocess.run([sys.executable, "-I", gen_path, "--seed", str(seed), "--n", str(n),
                        "--out", gen_out, "--scratch-root", work],
                       capture_output=True, text=True, timeout=FRESH_RUN_TIMEOUT, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"fresh generator rc={r.returncode}: {r.stderr[-400:]}")
    try:
        data = json.load(open(gen_out, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise RuntimeError(f"fresh generator output unreadable: {e}")
    cases = data["cases"] if isinstance(data, dict) else data
    oracle = Oracle(_ORACLE_BIN)

    def label(c: dict):
        root = tempfile.mkdtemp(prefix="freshcase-", dir=work)
        try:
            materialise(c, root)
            env = oracle_env(c, root)
            got = oracle.run(case_names(c), env, root)
            return got
        finally:
            shutil.rmtree(root, ignore_errors=True)

    with ThreadPoolExecutor(min(16, os.cpu_count() or 4)) as ex:
        labs = list(ex.map(label, cases))
    if any(l is None for l in labs):
        raise RuntimeError("fresh leg: oracle produced no answer for a case")
    return cases, labs


def score_fresh(tool: str, cases: list[dict], labs: list[list[tuple[str, int]]],
                work: str, jobs: int) -> tuple[int, int]:
    """(correct, total) where a case is correct iff every name's (type, uncertain) matches."""
    def one(arg):
        c, lab = arg
        root = tempfile.mkdtemp(prefix="freshscore-", dir=work)
        try:
            materialise(c, root)
            env = oracle_env(c, root)
            got = run_tool_json(tool, case_names(c), env, root)
            if got is None:
                return False
            return got["answers"] == lab
        finally:
            shutil.rmtree(root, ignore_errors=True)
    with ThreadPoolExecutor(jobs) as ex:
        res = list(ex.map(one, zip(cases, labs)))
    return sum(res), len(res)


# ---------------------------------------------------------------- main

_ORACLE_BIN = ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--expect-cases-sha256", required=True)
    ap.add_argument("--mutants", required=True)
    ap.add_argument("--expect-mutants-sha256", required=True)
    ap.add_argument("--oracle-src", required=True)
    ap.add_argument("--expect-oracle-sha256", required=True)
    ap.add_argument("--fresh-gen", required=True)
    ap.add_argument("--expect-fresh-gen-sha256", required=True)
    ap.add_argument("--host-names", required=True)
    ap.add_argument("--expect-host-names-sha256", required=True)
    ap.add_argument("--expect-tool-sha256", required=True)
    ap.add_argument("--fresh", type=int, default=40, help="fresh cases to generate and label")
    ap.add_argument("--fresh-seed", type=int, default=None, help="fix the fresh seed (default: random)")
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--draft-tool", help="DRAFT only: score this file instead of <rev>:" + TOOL)
    a = ap.parse_args()
    draft = bool(a.draft_tool)
    sys.stdout.reconfigure(line_buffering=True)

    def setup(msg: str) -> int:
        print(f"MADO_MIMEGLOB_COUNT: SETUP_ERROR pred={PRED} {msg}")
        return 2

    # ---- pin every frozen input
    pins = [("cases", a.cases, a.expect_cases_sha256),
            ("mutants", a.mutants, a.expect_mutants_sha256),
            ("oracle-src", a.oracle_src, a.expect_oracle_sha256),
            ("fresh-gen", a.fresh_gen, a.expect_fresh_gen_sha256),
            ("host-names", a.host_names, a.expect_host_names_sha256)]
    for name, path, want in pins:
        if not os.path.exists(path):
            return setup(f"{name} {path} missing")
        got = sha_file(path)
        if got != want:
            return setup(f"{name} sha256 {got} != pinned {want}")

    cases_data = json.load(open(a.cases, encoding="utf-8"))
    cases = cases_data["cases"]
    if cases_data.get("oracle_src_sha256") != a.expect_oracle_sha256:
        return setup("case file oracle_src_sha256 != pinned oracle source")
    mutants = json.load(open(a.mutants, encoding="utf-8"))["mutants"]

    # ---- compile the oracle
    if shutil.which("gcc") is None or shutil.which("pkg-config") is None:
        return setup("gcc/pkg-config missing")
    os.makedirs(a.scratch_root, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c1r94-", dir=a.scratch_root)
    global _ORACLE_BIN
    try:
        _ORACLE_BIN = os.path.join(work, "oracle")
        cflags = subprocess.run(["pkg-config", "--cflags", "gio-2.0"],
                                capture_output=True, text=True).stdout.split()
        libs = subprocess.run(["pkg-config", "--libs", "gio-2.0"],
                              capture_output=True, text=True).stdout.split()
        rc = subprocess.run(["gcc", "-O1", "-o", _ORACLE_BIN, a.oracle_src] + cflags + libs,
                            capture_output=True, text=True).returncode
        if rc != 0:
            return setup("oracle compile failed")
        oracle_sha = sha_file(_ORACLE_BIN)
        print(f"oracle_binary_sha256={oracle_sha}")
        pq = subprocess.run(["pacman", "-Q", "glib2", "shared-mime-info"],
                            capture_output=True, text=True)
        print("pacman -Q glib2 shared-mime-info:")
        print(pq.stdout.strip() or pq.stderr.strip())

        oracle = Oracle(_ORACLE_BIN)

        # ---- frozen leg: oracle drift check + tool answers
        def oracle_label(c: dict):
            root = tempfile.mkdtemp(prefix="ocase-", dir=work)
            try:
                materialise(c, root)
                return oracle.run(case_names(c), oracle_env(c, root), root)
            finally:
                shutil.rmtree(root, ignore_errors=True)

        with ThreadPoolExecutor(a.workers) as ex:
            live = list(ex.map(oracle_label, cases))
        drift = [c["id"] for c, lab, live_l in zip(cases, (labels_of(c) for c in cases), live)
                 if live_l is None or live_l != lab]
        if drift:
            return setup("oracle_drift=" + ",".join(drift[:20]))

        # mode coverage of the frozen set
        modes = {c.get("mode") for c in cases}
        classes = {c.get("class") for c in cases}
        if not ({"text", "cache"} <= modes):
            return setup(f"frozen set lacks both modes: {sorted(modes)}")
        if None in classes or "" in classes:
            return setup("frozen set has a case without a class")
        unknown = sorted(c for c in classes if c not in CLASSES)
        if unknown:
            return setup(f"frozen set has classes outside the frozen list: {unknown}")
        per_class = {k: sum(1 for c in cases if c.get("class") == k) for k in CLASSES}
        classes_ok = sum(1 for k in CLASSES if per_class[k] >= MIN_PER_CLASS)
        print("per_class " + " ".join(f"{k}={per_class[k]}" for k in CLASSES))

        # the tool under test
        tool_b = open(a.draft_tool, "rb").read() if a.draft_tool else git_show(a.repo, a.rev, TOOL)
        if tool_b is None:
            return setup(f"{TOOL} absent at {a.rev}")
        tool_pin = sha(tool_b) == a.expect_tool_sha256
        static_bad = static_check(tool_b)
        print("static_findings=" + (",".join(static_bad) or "none"))
        global _EMPTY_PATH
        _EMPTY_PATH = tempfile.mkdtemp(prefix="emptypath-", dir=work)
        tp = os.path.join(work, "tool.py")
        with open(tp, "wb") as fh:
            fh.write(tool_b)

        oc = outcomes(tp, cases, work, a.workers)
        res = [o == "ok" for o in oc]
        answered = sum(o != "crash" for o in oc)
        for c, o in zip(cases, oc):
            if o != "ok":
                print(f"case {c['id']} {o.upper()}")
        correct = sum(res)
        by_mode: dict[str, list[bool]] = {}
        for c, ok in zip(cases, res):
            by_mode.setdefault(c.get("mode", "?"), []).append(ok)
        n = len(cases)

        # ---- fresh leg
        seed = a.fresh_seed if a.fresh_seed is not None else int.from_bytes(os.urandom(4), "big")
        try:
            fcases, flabs = fresh_cases(a.fresh_gen, seed, a.fresh, work)
        except RuntimeError as e:
            return setup(f"fresh leg: {e}")
        fcorrect, ftot = score_fresh(tp, fcases, flabs, work, a.workers)
        print(f"fresh seed={seed} cases={ftot} correct={fcorrect}")

        # ---- host leg
        host_names = host_name_list(open(a.host_names, "rb").read())
        host_env = {"HOME": os.environ.get("HOME", "/"),
                    "XDG_DATA_HOME": os.environ.get("XDG_DATA_HOME"),
                    "XDG_DATA_DIRS": os.environ.get("XDG_DATA_DIRS")}
        print(f"host env HOME={host_env['HOME']!r} XDG_DATA_HOME={host_env['XDG_DATA_HOME']!r} "
              f"XDG_DATA_DIRS={host_env['XDG_DATA_DIRS']!r} names={len(host_names)}")
        hd = [(host_env["XDG_DATA_HOME"] if host_env["XDG_DATA_HOME"] is not None
               else host_env["HOME"] + "/.local/share")]
        hd += [d for d in (host_env["XDG_DATA_DIRS"] if host_env["XDG_DATA_DIRS"] is not None
                           else "/usr/local/share/:/usr/share/").split(":") if d]
        for d in hd:
            for fn in ("mime.cache", "globs2"):
                p = os.path.join(d, "mime", fn)
                if os.path.isfile(p):
                    print(f"host_db {p} sha256={sha_file(p)}")
        hroot = tempfile.mkdtemp(prefix="host-", dir=work)
        try:
            # names are raw lines; the tool decodes argv via the filesystem encoding (surrogateescape)
            hcorrect = 0
            htot = len(host_names)
            # chunk the names so no argv/JSON payload approaches ARG_MAX
            CH = 2000
            for i in range(0, htot, CH):
                chunk = host_names[i:i + CH]
                lv = oracle.run(chunk, host_env, hroot)
                gt = run_tool_json(tp, chunk, host_env, hroot, timeout=TOOL_TIMEOUT * 4)
                if lv is None:
                    return setup("host leg: oracle produced no answer")
                if gt is not None:
                    hcorrect += sum(1 for g, l in zip(gt["answers"], lv) if g == l)
        finally:
            shutil.rmtree(hroot, ignore_errors=True)

        # ---- mutant leg
        src = tool_b.decode("utf-8")
        killed = crashed = survived = 0
        if not tool_pin:
            print("mutant leg skipped: the mutants are anchored to the frozen candidate and the tool is not it (killed=0)")
        for m in (mutants if tool_pin else []):
            if src.count(m["find"]) != 1:
                return setup(f"mutant {m['id']} find occurs {src.count(m['find'])} times")
            mp = os.path.join(work, f"mut-{m['id']}.py")
            with open(mp, "w", encoding="utf-8") as fh:
                fh.write(src.replace(m["find"], m["replace"], 1))
            mors = outcomes(mp, cases, work, a.workers)
            first = next((c["id"] for c, o in zip(cases, mors) if o == "wrong"), None)
            # a crash the candidate does not have is the mutant's own crash; crashes shared with the candidate are not
            new_crash = any(mo == "crash" and co != "crash" for mo, co in zip(mors, oc))
            if first:
                killed += 1
                status = f"killed by {first}"
            elif new_crash:
                crashed += 1
                status = f"crashed-not-killed ({sum(mo == 'crash' and co != 'crash' for mo, co in zip(mors, oc))} new crash cases)"
            else:
                survived += 1
                status = "survived"
            print(f"mutant {m['id']} {status}")

        # ---- controls
        dn_correct = 0
        for c in cases:
            root = tempfile.mkdtemp(prefix="dn-", dir=work)
            try:
                materialise(c, root)
                if do_nothing_answers(case_names(c)) == labels_of(c):
                    dn_correct += 1
            finally:
                shutil.rmtree(root, ignore_errors=True)
        naive_exact, naive_folded = score_naive(cases, work, a.workers)
        naive_correct = max(naive_exact, naive_folded)
        base_tool = git_show(a.repo, a.base_rev, TOOL)
        if base_tool is None:
            base_correct = 0
            print("base: tool absent at base-rev (answered=0)")
        else:
            bp = os.path.join(work, "base.py")
            with open(bp, "wb") as fh:
                fh.write(base_tool)
            base_res = outcomes(bp, cases, work, a.workers)
            base_correct = sum(o == "ok" for o in base_res)
            print(f"base: tool present, correct={base_correct}")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    met = (tool_pin and correct == n and answered == n and fcorrect == ftot and hcorrect == htot
           and killed == len(mutants) and len(mutants) >= MIN_MUTANTS and classes_ok == len(CLASSES)
           and not static_bad and dn_correct < n and naive_correct < n and base_correct < n)
    word = ("DRAFT_" if draft else "") + ("TARGET_MET" if met else "TARGET_MISSED")
    print(f"MADO_MIMEGLOB_COUNT: {word} pred={PRED} rev={'draft:' + a.draft_tool if draft else a.rev} "
          f"tool_pin={'ok' if tool_pin else 'FAIL'} cases={n} correct={correct} answered={answered} "
          f"text={sum(by_mode.get('text', []))}/{len(by_mode.get('text', []))} "
          f"cache={sum(by_mode.get('cache', []))}/{len(by_mode.get('cache', []))} "
          f"mixed={sum(by_mode.get('mixed', []))}/{len(by_mode.get('mixed', []))} "
          f"classes={classes_ok}/{len(CLASSES)} static_no_external_resolver={'FAIL' if static_bad else 'ok'} "
          f"fresh={fcorrect}/{ftot} fresh_seed={seed} host={hcorrect}/{htot} "
          f"mutants={len(mutants)} killed={killed} crashed_not_killed={crashed} survived={survived} "
          f"do_nothing_correct={dn_correct} naive_correct={naive_correct} "
          f"naive_exact_correct={naive_exact} naive_folded_correct={naive_folded} "
          f"base_correct={base_correct} "
          f"oracle_sha256={oracle_sha} tool_sha256={sha(tool_b)}")
    if draft:
        return 3
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
