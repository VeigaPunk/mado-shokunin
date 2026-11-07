#!/usr/bin/env python3
"""Round-96 C1 counter - the TEXT MIME database's magic step: file bytes (+ optional name) -> MIME type
as GLib 2.90.1 g_content_type_guess answers when no reachable mime.cache loads (text database mode).

Frozen predicate PRED-C1-r96-v1 (the same sentence as the declaration and the receipt label):
  TARGET_MET iff, at --rev, tools/mado-mimetext.py is the frozen candidate (tool_sha256 ==
  --expect-tool-sha256, printed tool_pin=ok) and, run under an empty PATH through the audit launcher with
  the structural allowlist (no process, socket, network or non-libc dynamic import), it answers
  (i) every frozen case exactly (correct == cases), with the per-class census equal to the declared
      CLASSES (16 classes, >=8 cases each) and classes == 16/16;
  (ii) every fresh seeded input exactly (fresh == fresh_total, >=120 inputs);
  (iii) every host file over the host's own text database exactly (host == host_total, >=1500 paths, the
      round-95 committed list): the counter copies the eight /usr/share/mime text files named by the
      frozen --host-db manifest to a scratch root, verifies every per-file sha256 and
      mime_cache_in_copy == 0, prints host_db=ok files=8, and no mime.cache is reachable in any dir it
      scores;
  (iv) every frozen mutant is killed and every class kills at least one mutant (killed == mutants,
      class_kills == 16/16);
  (v) the controls stay behind: the do-nothing instrument (the round-95 tool, which refuses text mode)
      0 on the text-mode cases, the fallback-only naive model < cases, the name-only model < cases,
      the memoriser 0 on fresh, and the frozen library-asking forgery (--forgery, sha-pinned)
      rejected by the structural conjunct/audit (audit_denials > 0); and
  (vi) the candidate's --selftest is green (checks=N failed=0).
  rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR, 3 DRAFT (--draft-tool PATH; prints DRAFT_*).

AMENDMENT the L1 must fold into the declaration's counting command (seat R96MExecCounterC1, w1): a new
required argument --expect-tool-sha256 <sha256 of the frozen tools/mado-mimetext.py bytes at the C1
measured rev>; the frozen command line above already carries it.

Case file schema (version 2 envelope): {"version":2,"oracle_src_sha256":...,"glib2":"2.90.1-1",
"classes":[the 16 names, in this order],"cases":[{"id","class","env":{"HOME","XDG_DATA_HOME"|null,
"XDG_DATA_DIRS"},"files":{rel:b64},"inputs":[{"name_b64":null|b64,"data_b64":b64}],
"labels":[[type,0|1]|["UNSUPPORTED",null]]}]}.  The envelope may carry a db_mode field; it is NOT
consulted - each case's mode is derived from its own fixture (L1 contract detail 1): a reachable
loadable mime.cache (regular file, >= 40 bytes, version major 1 minor 1|2 as big-endian u16 at bytes
0..3 - the same rule tools/mado-mimeglob.py load_cache applies) is cache mode; else a reachable
mime/<text file> is text mode; else none.  SETUP_ERROR envelope: version/oracle_sha/glib2 wrong;
classes list != the frozen 16 in order; < 260 cases; an unknown class, a class/id prefix mismatch, or
a class below 8 cases; XDG_DATA_DIRS null; HOME != "{root}/h"; != 1..12 inputs; labels malformed;
an UNSUPPORTED label on a case whose fixture is not cache mode; a supported label on a cache-mode
case.  Fresh cases validate the env/input/label-shape and no-reachable-cache rules only.

Labels: every supported label is re-run against the live oracle at measurement (drift -> SETUP_ERROR);
["UNSUPPORTED", null] labels are structural (the declared cache-mode refusal: the tool must exit 3
for that input), never oracle-run.

The oracle is compiled once from --oracle-src (sha256 pinned) into --scratch-root with
cc -O0 $(pkg-config --cflags --libs gio-2.0); its binary sha256 and `pacman -Q glib2 shared-mime-info`
are printed.  tools/mado-mimeglob.py at --rev is pinned by --expect-mimeglob-sha256 (SETUP_ERROR on
drift).  Every frozen input is pinned by sha256; a mismatch is SETUP_ERROR rc 2.  All materialisation
lives under --scratch-root; label-bearing generator output and the memoriser table live in a sibling
directory outside the audit allowlist so the tool cannot read the scoring labels.  Stdlib only.
ASCII only.

Counted legs and their argv (every tool run under the audit launcher with PATH=<empty dir>):
  frozen leg   python3 -I <launcher> <auditlog> <allow> tools/mado-mimetext.py --json
               [--home H|--home-unset] [--data-home D|--data-home-unset] [--data-dirs L|--data-dirs-unset]
               [--name=NAME] -- FILE...   (one invocation per distinct input name; each
               UNSUPPORTED-labelled input alone: the tool's CLI stops at its first refusal)
  selftest leg same launcher, argv tools/mado-mimetext.py --selftest
  do-nothing   the round-95 tool tools/mado-mimesniff.py (its own sibling mado-mimeglob.py) over the
               text-mode frozen cases only: it must score 0 (it refuses text mode); the none-mode
               census is printed separately
  name_only    round 94's name step (tools/mado-mimeglob.py Resolver.guess, data ignored) over the
               frozen cases: must score < cases
  fresh leg    python3 -I <frozen generator> --seed N --out F [--oracle BIN] [--scratch DIR]; --fresh N
               generations (seeds fresh_seed+i, or N random seeds without --fresh-seed); the generator
               labels every case by its own oracle run; the counter validates every case, re-labels
               with its live oracle and demands agreement (drift -> SETUP_ERROR), then scores the tool
               like the frozen leg (>=120 inputs in total)
  host leg     the eight text files named by the frozen --host-db manifest copied from the manifest's
               source dir into <work>/hostdb/mime/, every per-file sha256 verified and
               mime_cache_in_copy == 0 asserted (prints host_db=ok files=8), then the tool and the live
               oracle over the frozen round-95 host list: per file the data-only pair (name NULL) and
               the own-path-as-name pair; oracle env -i LC_ALL=C HOME=<scratch h>
               XDG_DATA_DIRS=<scratch db>, tool --home <h> --data-home-unset --data-dirs <db>
  mutant leg   the frozen find/replace applied to the pinned tool source (skipped, killed=0, when the
               tool is not the pinned candidate), scored over the frozen cases; killed = at least one
               case wrong
  controls     naive = fallback-only model embedded below (name step round 94, data step zerosize /
               128-byte text-vs-binary fallback, no magic parse, no priority/subclass nuance, no
               refusal surface); memoriser = label-lookup model generated in scratch from the frozen
               labels (sentinel answer on a miss, so it cannot match any oracle answer); forgery = the
               frozen --forgery file written to scratch and run under the launcher: rejected iff the
               audit denies it (audit_denials > 0) or the static conjunct flags it
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

PRED = "PRED-C1-r96-v1"
CLASSES = ("header", "sect", "value", "mask", "word", "range", "indent", "order", "drop", "multi",
           "glob", "alias", "fallback", "zerosize", "mode", "desktop")
MIN_PER_CLASS = 8
MIN_CASES = 260
MIN_FRESH_INPUTS = 120
MIN_HOST_PATHS = 1500
EMPTY_PATH = ""
TOOL = "tools/mado-mimetext.py"
MIMEGLOB = "tools/mado-mimeglob.py"
RN95_TOOL = "tools/mado-mimesniff.py"
GLIB = "2.90.1-1"
UNKNOWN = "application/octet-stream"
MEMO_MISS = "application/x-mado-memoriser-miss"
TOOL_TIMEOUT = 30.0
ORACLE_CASE_TIMEOUT = 10.0     # the case schema: an oracle run over 10 s is UNSUPPORTED
ORACLE_FRESH_TIMEOUT = 30.0
ORACLE_HOST_TIMEOUT = 60.0
FRESH_RUN_TIMEOUT = 600.0
HOST_ORACLE_PAIRS = 1000       # pairs per oracle invocation on the host leg
HOST_TOOL_FILES = 400          # files per tool invocation on the data-only host leg
TEXT_DB_FILES = ("magic", "globs", "globs2", "aliases", "subclasses", "icons", "generic-icons",
                 "XMLnamespaces")
HOST_DB_FILES = 8


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
    """The compiled g_content_type_guess oracle, run as env -i LC_ALL=C + the case/host env.

    argv is pairs "<0 | =NAME>" "<datafile>"; "0" passes filename NULL, "=NAME" passes NAME as
    raw argv bytes.  One "<type>\t<0|1>" line per pair on stdout.
    """

    def __init__(self, binary: str):
        self.binary = binary

    def run_pairs(self, pairs: list[tuple[bytes | None, str]], env_extra: dict[str, str | None],
                  cwd: str, timeout: float) -> list[tuple[str, int]] | None:
        env = {"LC_ALL": "C"}
        for k, v in env_extra.items():
            if v is not None:
                env[k] = v
        args = [os.fsencode(self.binary)]
        for name, df in pairs:
            args.append(b"0" if name is None else b"=" + name)
            args.append(os.fsencode(df))
        try:
            r = subprocess.run(args, capture_output=True, timeout=timeout, env=env, cwd=cwd)
        except (OSError, subprocess.TimeoutExpired):
            return None
        if r.returncode != 0:
            return None
        lines = r.stdout.splitlines()
        if len(lines) != len(pairs):
            return None
        out = []
        for ln in lines:
            m = re.fullmatch(rb"([^\t\r\n]*)\t([01])", ln)
            if not m:
                return None
            out.append((m.group(1).decode("utf-8", "surrogateescape"), int(m.group(2))))
        return out


def case_env(case: dict, root: str) -> dict[str, str | None]:
    """The case's env mapping with {root} substituted; a null value means the variable is unset."""
    e = case.get("env", {})
    out: dict[str, str | None] = {}
    for k in ("HOME", "XDG_DATA_HOME", "XDG_DATA_DIRS"):
        v = e.get(k)
        out[k] = None if v is None else v.replace("{root}", root)
    return out


def case_roots(case: dict) -> list[str]:
    """Case-relative prefixes of the XDG data roots a reader would consult, derived from the raw
    env templates ('{root}/dh' -> 'dh'; XDG_DATA_HOME unset -> 'h/.local/share')."""
    env = case.get("env", {})
    roots = []
    dh = env.get("XDG_DATA_HOME")
    if dh is not None:
        roots.append(dh)
    else:
        home = env.get("HOME")
        if home is not None:
            roots.append(home.rstrip("/") + "/.local/share")
    dd = env.get("XDG_DATA_DIRS")
    if dd:
        roots.extend(dd.split(":"))
    out = []
    for r in roots:
        if not isinstance(r, str):
            continue
        r = r.replace("{root}", "").strip("/")
        if r:
            out.append(r)
    return out


def _reachable(rel: str, roots: list[str]) -> bool:
    return any(rel == r or rel.startswith(r + "/") for r in roots)


def loadable_cache(data: bytes) -> bool:
    """The GLib/mimeglob cache rule: >= 40 bytes and version major 1, minor 1|2 (big-endian u16
    at bytes 0..3).  A regular file is implied: case files entries are always regular files."""
    return len(data) >= 40 and int.from_bytes(data[0:2], "big") == 1 \
        and int.from_bytes(data[2:4], "big") in (1, 2)


def case_mode(case: dict) -> str:
    """'cache' | 'text' | 'none' derived from the fixture (L1 contract detail 1): a reachable
    loadable mime.cache is cache mode; else a reachable mime/<text file> is text mode; else none."""
    roots = case_roots(case)
    cache = text = False
    for rel, b64 in case.get("files", {}).items():
        if rel.endswith("/") or not _reachable(rel, roots):
            continue
        parts = rel.rsplit("/", 2)
        if len(parts) < 2 or parts[-2] != "mime":
            continue
        if parts[-1] == "mime.cache":
            try:
                data = unb64(b64)
            except Exception:
                data = b""
            if loadable_cache(data):
                cache = True
        elif parts[-1] in TEXT_DB_FILES:
            text = True
    if cache:
        return "cache"
    return "text" if text else "none"


# ---------------------------------------------------------------- case materialisation

def materialise(case: dict, root: str) -> None:
    """Write every file; a key ending in '/' is a directory."""
    for rel, b64 in case.get("files", {}).items():
        p = os.path.join(root, rel)
        if rel.endswith("/"):
            os.makedirs(p, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(unb64(b64))


def case_inputs(case: dict) -> list[tuple[bytes | None, bytes]]:
    out = []
    for x in case.get("inputs", []):
        nb = x.get("name_b64")
        out.append((None if nb is None else unb64(nb), unb64(x["data_b64"])))
    return out


def labels_of(case: dict) -> list[tuple[str, int] | None]:
    """Per input: (type, uncertain) or None for the ["UNSUPPORTED", null] label."""
    out = []
    for t, u in case.get("labels", []):
        out.append(None if t == "UNSUPPORTED" else (t, int(u)))
    return out


def write_input_files(inputs: list[tuple[bytes | None, bytes]], dstdir: str) -> list[str]:
    os.makedirs(dstdir, exist_ok=True)
    paths = []
    for i, (_name, data) in enumerate(inputs):
        p = os.path.join(dstdir, f"in-{i}")
        with open(p, "wb") as fh:
            fh.write(data)
        paths.append(p)
    return paths


def oracle_label_case(oracle: Oracle, case: dict, root: str, dstdir: str,
                      skip_refusals: bool = False) -> list[tuple[str, int] | None]:
    """One oracle run per input (a crash on one input never labels another); None = crashed/timed out.

    With skip_refusals the recorded ["UNSUPPORTED", null] labels are kept as None and NOT oracle-run
    (the oracle answers cache mode where the tool must refuse).  Without it (fresh leg) every input
    is oracle-run regardless of any recorded labels."""
    inputs = case_inputs(case)
    labs = labels_of(case) if skip_refusals else [None] * len(inputs)
    dfs = write_input_files(inputs, dstdir)
    out = []
    for (name, _data), lab, df in zip(inputs, labs, dfs):
        if skip_refusals and lab is None:
            out.append(None)
            continue
        got = oracle.run_pairs([(name, df)], case_env(case, root), root, ORACLE_CASE_TIMEOUT)
        out.append(None if got is None else got[0])
    return out


# ---------------------------------------------------------------- tool run

def tool_env_flags(env: dict[str, str | None]) -> list[str]:
    """Map the case env (HOME / XDG_DATA_HOME / XDG_DATA_DIRS) onto the tool's flags."""
    argv = []
    home = env.get("HOME")
    argv += ["--home", home] if home is not None else ["--home-unset"]
    dh = env.get("XDG_DATA_HOME")
    argv += ["--data-home", dh] if dh is not None else ["--data-home-unset"]
    dd = env.get("XDG_DATA_DIRS")
    argv += ["--data-dirs", dd] if dd is not None else ["--data-dirs-unset"]
    return argv


def run_tool_group(tool: str, name: bytes | None, files: list[str], flags: list[str],
                   cwd: str, timeout: float = TOOL_TIMEOUT, audit: str = "main",
                   allow_extra: str = "") -> tuple[str, list[tuple[str, int]] | None, dict | None]:
    """Run the tool on one name group, under the audit launcher (log `audit`).

    Returns ("ok", answers, meta) | ("unsupported", None, None) on exit 3 | ("crash", None, None)
    otherwise (exit 97 = audit denial, logged and counted by the structural conjunct).
    meta is the parsed JSON envelope minus results (mode/dirs when the tool prints them).
    """
    allow = os.pathsep.join(x for x in (_RUN["allow"], allow_extra) if x)
    argv = [sys.executable, "-I", _RUN["launcher"], audit_log(audit), allow, tool, "--json"] + flags
    if name is not None:
        argv.append("--name=" + name.decode("utf-8", "surrogateescape"))
    argv += ["--"] + files
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout,
                           cwd=cwd, env={"PATH": EMPTY_PATH})
    except (OSError, subprocess.TimeoutExpired):
        return "crash", None, None
    if r.returncode == 3:
        return "unsupported", None, None
    if r.returncode != 0:
        return "crash", None, None
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return "crash", None, None
    res = d.get("results")
    if not isinstance(res, list) or len(res) != len(files):
        return "crash", None, None
    out = []
    for x in res:
        if not isinstance(x, dict) or not isinstance(x.get("type"), str) \
                or x.get("uncertain") not in (0, 1):
            return "crash", None, None
        out.append((x["type"], int(x["uncertain"])))
    meta = {k: v for k, v in d.items() if k != "results"}
    return "ok", out, meta


def score_case(tool: str, case: dict, labels: list[tuple[str, int] | None], work: str,
               timeout: float = TOOL_TIMEOUT, audit: str = "main") -> str:
    """'ok' | 'wrong' | 'crash' for one case against the given labels (None = UNSUPPORTED)."""
    root = tempfile.mkdtemp(prefix="case-", dir=work)
    try:
        materialise(case, root)
        inputs = case_inputs(case)
        dfs = write_input_files(inputs, root + ".data")
        flags = tool_env_flags(case_env(case, root))
        # group input indices by name; UNSUPPORTED labels are scored in their own invocations
        groups: dict[bytes | None, list[int]] = {}
        for i, (name, _data) in enumerate(inputs):
            groups.setdefault(name, []).append(i)
        wrong = crash = False
        for name, idxs in groups.items():
            sup = [i for i in idxs if labels[i] is not None]
            uns = [i for i in idxs if labels[i] is None]
            if sup:
                status, answers, _meta = run_tool_group(tool, name, [dfs[i] for i in sup], flags, root,
                                                        timeout, audit)
                if status == "crash":
                    crash = True
                elif status == "unsupported":
                    wrong = True   # the tool refused a supported input
                elif status == "ok":
                    if answers is None or any(answers[j] != labels[i] for j, i in enumerate(sup)):
                        wrong = True
            for i in uns:      # each must-refuse input alone: the CLI stops at its first refusal
                status, _answers, _meta = run_tool_group(tool, name, [dfs[i]], flags, root, timeout, audit)
                if status == "ok":
                    wrong = True       # the tool answered a must-refuse input
                elif status == "crash":
                    crash = True
                # status == "unsupported" is the required refusal: ok
        if wrong:
            return "wrong"
        if crash:
            return "crash"
        return "ok"
    finally:
        shutil.rmtree(root, ignore_errors=True)
        shutil.rmtree(root + ".data", ignore_errors=True)


def outcomes(tool: str, cases: list[dict], labels: list[list], work: str, jobs: int,
             audit: str = "main") -> list[str]:
    with ThreadPoolExecutor(jobs) as ex:
        return list(ex.map(lambda ca: score_case(tool, ca[0], ca[1], work, TOOL_TIMEOUT, audit),
                           zip(cases, labels)))


# ---------------------------------------------------------------- static conjunct (structural)

_OK_IMPORTS = {"__future__", "argparse", "importlib.util", "json", "os", "struct", "sys", "tempfile"}
_BAD_OS = re.compile(r"^(system|popen|exec\w*|spawn\w*|posix_spawn\w*|fork\w*)$")
_BAD_NAMES = {"eval", "exec", "compile", "__import__", "getattr", "setattr", "delattr", "vars", "globals",
              "locals", "breakpoint", "import_module", "reload"}
_MG_ATTRS = {"Unsupported", "oob", "Resolver", "xdgmime_dirs", "g_path_get_basename", "esc", "_LC_ALL"}


def static_check(src: bytes) -> list[str]:
    """Findings that make static_no_external_resolver FAIL (empty list = ok); the sentence is the
    structural conjunct: no process, socket, network or non-libc dynamic import; one pinned sibling
    import; no dunder or dynamic attribute access; no os.system/popen/exec*/spawn*/fork*."""
    import ast
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [f"syntax:{e.lineno}"]
    bad: list[str] = []
    parent: dict[int, ast.AST] = {}
    for node in ast.walk(tree):
        for ch in ast.iter_child_nodes(node):
            parent[id(ch)] = node
    spec_calls = []
    module_vars: set[str] = set()      # names bound to module_from_spec(...)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                if al.name not in _OK_IMPORTS:
                    bad.append(f"import:{al.name}:{node.lineno}")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "") != "__future__":
                bad.append(f"import-from:{node.module}:{node.lineno}")
        elif isinstance(node, ast.Name) and node.id in _BAD_NAMES:
            bad.append(f"name:{node.id}:{node.lineno}")
        elif isinstance(node, ast.Attribute):
            if node.attr.startswith("__") and node.attr.endswith("__"):
                bad.append(f"dunder:.{node.attr}:{node.lineno}")
            if node.attr in _BAD_NAMES:
                bad.append(f"attr:{node.attr}:{node.lineno}")
            if isinstance(node.value, ast.Name) and node.value.id == "os" and _BAD_OS.match(node.attr):
                bad.append(f"os.{node.attr}:{node.lineno}")
            if node.attr == "spec_from_file_location":
                call = parent.get(id(node))
                if isinstance(call, ast.Call) and call.func is node:
                    spec_calls.append(call)
                else:
                    bad.append(f"spec_from_file_location-not-called:{node.lineno}")
        elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) \
                and isinstance(node.value.func, ast.Attribute) and node.value.func.attr == "module_from_spec":
            module_vars |= {t.id for t in node.targets if isinstance(t, ast.Name)}
    if len(spec_calls) != 1:
        bad.append(f"spec_from_file_location-calls:{len(spec_calls)}")
    else:
        loc = spec_calls[0].args[1] if len(spec_calls[0].args) > 1 else None
        names = {n.id for n in ast.walk(loc) if isinstance(n, ast.Name)} if loc is not None else set()
        consts = {n.value for n in ast.walk(loc) if isinstance(n, ast.Constant)} if loc is not None else set()
        if "__file__" not in names or "mado-mimeglob.py" not in consts:
            bad.append(f"spec_location-not-sibling-mimeglob:{spec_calls[0].lineno}")
    # functions returning a module variable; names bound to their call results are module names too
    loaders = {f.name for f in ast.walk(tree) if isinstance(f, ast.FunctionDef)
               and any(isinstance(r, ast.Return) and isinstance(r.value, ast.Name) and r.value.id in module_vars
                       for r in ast.walk(f))}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) \
                and isinstance(node.value.func, ast.Name) and node.value.func.id in loaders:
            module_vars |= {t.id for t in node.targets if isinstance(t, ast.Name)}
    if not module_vars:
        bad.append("no-module_from_spec-binding")
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Name) and node.id in module_vars and isinstance(node.ctx, ast.Load)):
            continue
        up = parent.get(id(node))
        if isinstance(up, ast.Attribute) and up.value is node:
            if up.attr in _MG_ATTRS:
                continue
            upp = parent.get(id(up))
            if up.attr == "_libc" and isinstance(upp, ast.Attribute) and upp.attr == "setlocale":
                continue
            bad.append(f"module-attr:{node.id}.{up.attr}:{node.lineno}")
        elif isinstance(up, ast.Return):
            continue
        elif isinstance(up, ast.Call) and isinstance(up.func, ast.Attribute) and up.func.attr == "exec_module" \
                and node in up.args:
            continue
        else:
            bad.append(f"module-use:{node.id}:{node.lineno}")
    return bad


# the audit-hook launcher every tool run goes through (structural conjunct, audit=ok)
LAUNCHER_SRC = r'''import os, sys
_log = os.open(sys.argv[1], os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
_allow = [os.path.realpath(p) for p in sys.argv[2].split(os.pathsep) if p] + ["/dev/null"]
_tool = sys.argv[3]
sys.argv = [_tool] + sys.argv[4:]
_SPAWN_OK = {"ldconfig", "gcc", "cc", "ld", "objdump"}
_busy = [False]


def _deny(ev, arg):
    os.write(_log, ("AUDIT_DENY %s %r\n" % (ev, arg)).encode("utf-8", "backslashreplace"))
    os._exit(97)


def _hook(ev, args):
    if _busy[0]:
        return
    _busy[0] = True
    try:
        if ev == "open":
            p = args[0]
            if isinstance(p, int):
                return
            rp = os.path.realpath(os.fsdecode(p))
            if not any(rp == a or rp.startswith(a + os.sep) for a in _allow):
                _deny(ev, rp)
        elif ev in ("subprocess.Popen", "os.posix_spawn"):
            exe = os.fsdecode(args[0] or (args[1][0] if args[1] else ""))
            rx = os.path.realpath(exe) if os.sep in exe else exe
            if os.path.basename(exe) not in _SPAWN_OK or (os.sep in exe and not rx.startswith(("/usr/bin/", "/usr/sbin/"))):
                _deny(ev, exe)
        elif ev in ("os.system", "os.exec", "os.spawn", "os.fork", "os.forkpty", "pty.spawn", "socket.__new__",
                    "socket.connect", "urllib.Request", "http.client.connect"):
            _deny(ev, args[:1])
        elif ev == "ctypes.dlopen":
            if args[0] is None:
                return
            if not os.path.basename(os.fsdecode(args[0])).startswith("libc.so"):
                _deny(ev, args[0])
    finally:
        _busy[0] = False


sys.addaudithook(_hook)
import runpy  # noqa: E402
runpy.run_path(_tool, run_name="__main__")
'''
_RUN = {"launcher": "", "allow": "", "logs": {}}


def audit_log(kind: str) -> str:
    return _RUN["logs"][kind]


# ---------------------------------------------------------------- controls

_HEX_ESC = re.compile(rb"\\x([0-9a-fA-F]{2})")


def host_file_list(data: bytes) -> list[bytes]:
    """The frozen host file list: '#' lines are the header; every other non-empty line is one
    path whose raw bytes are written as \\xHH escapes (the only non-ASCII form used)."""
    paths = []
    for ln in data.split(b"\n"):
        if not ln or ln.startswith(b"#"):
            continue
        paths.append(_HEX_ESC.sub(lambda m: bytes([int(m.group(1), 16)]), ln))
    return paths


def load_mg(mimeglob_path: str):
    spec = importlib.util.spec_from_file_location("mado_mimeglob_pin", mimeglob_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def name_only_answers(mg, case: dict, root: str) -> list[tuple[str, int] | None] | str:
    """Control (v): round 94's tools/mado-mimeglob.py name-only answer (data ignored).

    A None name is g_content_type_guess(NULL, NULL, 0) = (application/octet-stream, 1); a named
    input is Resolver.guess (exactly what round 94's tool prints).  A refusal (Unsupported) is
    per-input None, matching an UNSUPPORTED label; a Resolver that cannot be built refuses all.
    """
    env = case_env(case, root)
    try:
        resolver = mg.Resolver(mg.xdgmime_dirs(env.get("XDG_DATA_HOME"), env.get("HOME"),
                                               env.get("XDG_DATA_DIRS")))
    except mg.Unsupported:
        return "REFUSE"
    out = []
    for name, _data in case_inputs(case):
        if name is None:
            out.append((UNKNOWN, 1))
            continue
        try:
            g = resolver.guess(name)
        except mg.Unsupported:
            out.append(None)
            continue
        out.append((g["type"], g["uncertain"]))
    return out


def naive_looks_binary(data: bytes) -> bool:
    return any(b < 32 and b not in (9, 10, 13) for b in data[:128])


def naive_answers(mg, case: dict, root: str) -> list[tuple[str, int] | None] | str:
    """Control (v): the fallback-only model - the name step is round 94's, the data step is only the
    zerosize / 128-byte text-vs-binary fallback; no magic parse, no priority or subclass nuance, and no
    refusal surface (a cache-refusal case is answered, which is a miss by construction)."""
    env = case_env(case, root)
    try:
        resolver = mg.Resolver(mg.xdgmime_dirs(env.get("XDG_DATA_HOME"), env.get("HOME"),
                                               env.get("XDG_DATA_DIRS")))
    except mg.Unsupported:
        return "REFUSE"
    out = []
    for name, data in case_inputs(case):
        if name is not None and name.endswith(b"/"):
            out.append(("inode/directory", 1))
            continue
        try:
            types = resolver.guess(name)["types"] if name is not None else []
        except mg.Unsupported:
            out.append(("application/x-mado-naive-refused", 1))
            continue
        if len(data) == 0:
            sniffed = "application/x-zerosize"
        elif naive_looks_binary(data):
            sniffed = UNKNOWN
        else:
            sniffed = "text/plain"
        if not types:
            out.append((sniffed, 1 if sniffed == UNKNOWN else 0))
        elif len(types) == 1:
            out.append((types[0], 0))
        elif sniffed == "application/x-zerosize":
            out.append((sniffed, 0))
        else:
            out.append((types[0], 1))
    return out


def control_ok(answers, labels) -> bool:
    """A control satisfies (i) on a case iff every input matches its label; None answers (a
    control refusal) match UNSUPPORTED labels only."""
    if answers == "REFUSE":
        return all(l is None for l in labels)
    if not isinstance(answers, list) or len(answers) != len(labels):
        return False
    for a, l in zip(answers, labels):
        if l is None:
            if a is not None:
                return False
        elif a is None or a != l:
            return False
    return True


def score_control(scorer, cases: list[dict], labels: list[list], work: str, jobs: int) -> int:
    def one(ca):
        c, lab = ca
        root = tempfile.mkdtemp(prefix="ctl-", dir=work)
        try:
            materialise(c, root)
            return control_ok(scorer(c, root), lab)
        finally:
            shutil.rmtree(root, ignore_errors=True)
    with ThreadPoolExecutor(jobs) as ex:
        return sum(1 for ok in ex.map(one, zip(cases, labels)) if ok)


def score_name_only(mg, cases: list[dict], labels: list[list], work: str, jobs: int) -> int:
    return score_control(lambda c, root: name_only_answers(mg, c, root), cases, labels, work, jobs)


def case_fingerprint(case: dict) -> str:
    """The memoriser's case identity (L1 fix, review F2): mode + the env triple after {root}
    substitution + digests of the files layout and the input list.  A fresh case can never collide
    with a frozen one (its fixtures differ), and two frozen cases that share an input still get
    their own labels because the rest of the case is in the key."""
    env = case_env(case, "")
    h = hashlib.sha256()
    h.update(case_mode(case).encode("ascii") + b"\x00")
    for k in ("HOME", "XDG_DATA_HOME", "XDG_DATA_DIRS"):
        v = env.get(k)
        h.update(k.encode("ascii") + b"=" + (v.encode("utf-8", "surrogateescape")
                                             if v is not None else b"<unset>") + b"\x00")
    for rel in sorted(case.get("files", {})):
        h.update(rel.encode("utf-8", "surrogateescape") + b"\x01" + sha(unb64(case["files"][rel]))
                 .encode("ascii") + b"\x02")
    for x in case.get("inputs", []):
        h.update((x.get("name_b64") or "").encode("ascii") + b"\x03" + x["data_b64"].encode("ascii")
                 + b"\x04")
    return h.hexdigest()


def memoriser_model_path(cases: list[dict], secret: str) -> str:
    """Generate the label-lookup model OUTSIDE the audit allowlist (secret dir) from the frozen
    labels, keyed by case_fingerprint; a miss answers the sentinel (never a real type), so the
    model cannot match any oracle answer it has not memorised."""
    table = {}
    for c in cases:
        table[case_fingerprint(c)] = [[None if l is None else l[0], None if l is None else int(l[1])]
                                      for l in labels_of(c)]
    p = os.path.join(secret, "memo-model.json")
    with open(p, "w", encoding="ascii") as fh:
        json.dump(table, fh, sort_keys=True)
    return p


def memoriser_answers(table: dict, case: dict) -> list[tuple[str, int] | None]:
    labs = table.get(case_fingerprint(case))
    n = len(case_inputs(case))
    if labs is None or len(labs) != n:
        return [(MEMO_MISS, 1)] * n
    return [(None if l[0] is None else (l[0], int(l[1]))) for l in labs]


# ---------------------------------------------------------------- fresh leg

def fresh_cases(gen_path: str, seed: int, secret: str, work: str, oracle_bin: str,
                oracle: Oracle, tag: int) -> tuple[list[dict], list[list]]:
    """Run the frozen generator (`--seed N --out F [--oracle BIN] [--scratch DIR]`; it labels every
    case by its own oracle run), validate every case, then re-label with the counter's live oracle
    and demand agreement (drift -> RuntimeError -> SETUP_ERROR).  gen_out and the generator's own
    scratch live under `secret`, OUTSIDE the audit allowlist, so the tool cannot read the labels."""
    gen_out = os.path.join(secret, f"fresh-{seed}-{tag}.json")
    gen_scratch = os.path.join(secret, f"genscratch-{tag}")
    os.makedirs(gen_scratch, exist_ok=True)
    r = subprocess.run([sys.executable, "-I", gen_path, "--seed", str(seed), "--out", gen_out,
                        "--oracle", oracle_bin, "--scratch", gen_scratch],
                       capture_output=True, text=True, timeout=FRESH_RUN_TIMEOUT)
    if r.returncode != 0:
        raise RuntimeError(f"fresh generator rc={r.returncode}: {r.stderr[-400:]}")
    try:
        data = json.load(open(gen_out, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise RuntimeError(f"fresh generator output unreadable: {e}")
    cases = data["cases"] if isinstance(data, dict) else data
    if not isinstance(cases, list) or not cases:
        raise RuntimeError("fresh generator output has no cases")
    for ln in r.stdout.splitlines():
        if ln.startswith("magictext-fresh-r96:"):
            print("fresh gen " + ln)
    errs = []
    for c in cases:
        errs += validate_case_env(c, fresh=True)
    if errs:
        raise RuntimeError("fresh generator case violations: " + "; ".join(errs[:5]))

    def label(c: dict):
        root = tempfile.mkdtemp(prefix="freshcase-", dir=work)
        try:
            materialise(c, root)
            return oracle_label_case(oracle, c, root, root + ".odata", skip_refusals=True)
        finally:
            shutil.rmtree(root, ignore_errors=True)
            shutil.rmtree(root + ".odata", ignore_errors=True)

    with ThreadPoolExecutor(min(16, os.cpu_count() or 4)) as ex:
        labs = list(ex.map(label, cases))
    drift = [c.get("id", "?") for c, rec, liv in zip(cases, [labels_of(c) for c in cases], labs)
             if any(rec_i is not None and liv_i != rec_i for rec_i, liv_i in zip(rec, liv))]
    if drift:
        raise RuntimeError("fresh generator label drift: " + ",".join(drift[:10]))
    return cases, labs


# ---------------------------------------------------------------- host leg

def build_host_db(manifest_path: str, work: str) -> tuple[str, int]:
    """Rebuild the host's TEXT database in scratch from the frozen --host-db manifest: copy every
    file the manifest names from its source dir into <work>/hostdb/mime/, verify each per-file
    sha256, assert the manifest's mime_cache_in_copy == 0 and that no mime.cache landed."""
    try:
        manifest = json.load(open(manifest_path, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise RuntimeError(f"host-db manifest unreadable: {e}")
    files = manifest.get("files")
    if not isinstance(files, list) or len(files) != HOST_DB_FILES:
        raise RuntimeError(f"host-db manifest files != {HOST_DB_FILES}")
    if manifest.get("assertions", {}).get("mime_cache_in_copy") != 0:
        raise RuntimeError("host-db manifest mime_cache_in_copy != 0")
    srcdir = manifest.get("source", {}).get("dir")
    if not isinstance(srcdir, str) or not srcdir:
        raise RuntimeError("host-db manifest has no source.dir")
    db = os.path.join(work, "hostdb")
    os.makedirs(os.path.join(db, "mime"))
    for ent in files:
        name = ent.get("name")
        want = ent.get("sha256")
        if not isinstance(name, str) or "/" in name or not isinstance(want, str):
            raise RuntimeError(f"host-db manifest bad entry {ent!r}")
        src = os.path.join(srcdir, name)
        if not os.path.isfile(src):
            raise RuntimeError(f"host text file {src} missing")
        data = open(src, "rb").read()
        if sha(data) != want:
            raise RuntimeError(f"host text file {src} sha256 != manifest pin")
        with open(os.path.join(db, "mime", name), "wb") as fh:
            fh.write(data)
    if "mime.cache" in os.listdir(os.path.join(db, "mime")):
        raise RuntimeError("built host DB holds a mime.cache")
    return db, len(files)


def host_leg(tool: str, paths: list[bytes], work: str, jobs: int, dbdir: str, hdir: str,
             oracle: Oracle) -> tuple[int, int, int]:
    """(correct, total, readable).  Every readable file sniffed (first 4096 bytes) data-only and
    with its own path as the name, over the scratch text database (no mime.cache anywhere)."""
    host_env = {"HOME": hdir, "XDG_DATA_HOME": None, "XDG_DATA_DIRS": dbdir}
    hdata = tempfile.mkdtemp(prefix="hostdata-", dir=work)
    try:
        files = []          # (path_bytes, scratch_file)
        for i, p in enumerate(paths):
            try:
                with open(os.fsdecode(p), "rb") as fh:
                    data = fh.read(4096)
            except OSError:
                continue
            sp = os.path.join(hdata, f"h{i}")
            with open(sp, "wb") as fh:
                fh.write(data)
            files.append((p, sp))
        n = len(files)
        htot = 2 * n
        if n == 0:
            return 0, 0, 0
        # oracle labels: pairs (None, data) and (path, data) per file, chunked
        pairs = []
        for p, sp in files:
            pairs.append((None, sp))
            pairs.append((p, sp))
        labels: list[tuple[str, int]] = []
        for i in range(0, len(pairs), HOST_ORACLE_PAIRS):
            chunk = pairs[i:i + HOST_ORACLE_PAIRS]
            got = oracle.run_pairs(chunk, host_env, hdata, ORACLE_HOST_TIMEOUT)
            if got is None:
                raise RuntimeError("host leg: oracle produced no answer")
            labels += got
        flags = tool_env_flags(host_env)
        # data-only: name NULL for every file, chunked
        correct = 0
        for i in range(0, n, HOST_TOOL_FILES):
            chunk = files[i:i + HOST_TOOL_FILES]
            status, answers, _meta = run_tool_group(tool, None, [sp for _p, sp in chunk], flags, hdata,
                                                    timeout=TOOL_TIMEOUT * 4, audit="main")
            if status == "ok" and answers is not None:
                for j, (_p, _sp) in enumerate(chunk):
                    if answers[j] == labels[2 * (i + j)]:
                        correct += 1
        # own path as the name: one invocation per file
        def one(arg):
            k, (p, sp) = arg
            status, answers, _meta = run_tool_group(tool, p, [sp], flags, hdata, timeout=TOOL_TIMEOUT * 4,
                                                    audit="main")
            if status == "ok" and answers is not None and answers[0] == labels[2 * k + 1]:
                return 1
            return 0
        with ThreadPoolExecutor(jobs) as ex:
            correct += sum(ex.map(one, enumerate(files)))
        return correct, htot, n
    finally:
        shutil.rmtree(hdata, ignore_errors=True)


# ---------------------------------------------------------------- validation

def validate_case_env(c: dict, fresh: bool = False) -> list[str]:
    """Per-case rules that do not depend on the frozen census (shared with the fresh leg)."""
    errs = []
    cid = c.get("id", "?")
    env = c.get("env", {})
    if set(env) - {"HOME", "XDG_DATA_HOME", "XDG_DATA_DIRS"}:
        errs.append(f"case {cid}: unknown env keys {sorted(set(env) - {'HOME', 'XDG_DATA_HOME', 'XDG_DATA_DIRS'})}")
    if env.get("XDG_DATA_DIRS") is None:
        errs.append(f"case {cid}: XDG_DATA_DIRS unset is forbidden in cases (it reaches the host DBs)")
    if env.get("HOME") != "{root}/h":
        errs.append(f"case {cid}: HOME {env.get('HOME')!r} != '{{root}}/h'")
    inputs = c.get("inputs", [])
    labels = c.get("labels", [])
    if not isinstance(inputs, list) or not (1 <= len(inputs) <= 12):
        errs.append(f"case {cid}: {len(inputs) if isinstance(inputs, list) else '?'} inputs, need 1..12")
        return errs
    if not isinstance(labels, list) or len(inputs) != len(labels):
        errs.append(f"case {cid}: {len(inputs)} inputs vs {len(labels) if isinstance(labels, list) else '?'} labels")
        return errs
    for i, lab in enumerate(labels):
        if not (isinstance(lab, list) and len(lab) == 2):
            errs.append(f"case {cid}: label {i} malformed")
            break
        t, u = lab
        if t == "UNSUPPORTED":
            if u is not None:
                errs.append(f"case {cid}: UNSUPPORTED label {i} has uncertain {u!r}")
                break
        elif not (isinstance(t, str) and u in (0, 1)):
            errs.append(f"case {cid}: label {i} malformed")
            break
    mode = case_mode(c)
    if fresh and mode == "cache":
        errs.append(f"case {cid}: fresh case holds a reachable loadable mime.cache (refusal cases are frozen-set-only)")
        mode = "none"
    has_sup = any(isinstance(lab, list) and lab[0] == "UNSUPPORTED" for lab in labels)
    has_ok = any(isinstance(lab, list) and lab[0] != "UNSUPPORTED" for lab in labels)
    if mode == "cache" and has_ok:
        errs.append(f"case {cid}: reachable loadable mime.cache but a supported label (must be a refusal case)")
    if mode != "cache" and has_sup:
        errs.append(f"case {cid}: UNSUPPORTED label on a {mode}-mode fixture (the declared refusal needs a loadable mime.cache)")
    return errs


def validate_cases(cases_data: dict, expect_oracle_sha: str) -> list[str]:
    """Envelope + per-case sanity of the frozen case file; SETUP_ERROR messages (empty = ok)."""
    errs = []
    if cases_data.get("version") != 2:
        errs.append(f"case file version {cases_data.get('version')!r} != 2")
    if cases_data.get("oracle_src_sha256") != expect_oracle_sha:
        errs.append("case file oracle_src_sha256 != pinned oracle source")
    if cases_data.get("glib2") != GLIB:
        errs.append(f"case file glib2 {cases_data.get('glib2')!r} != {GLIB}")
    if cases_data.get("classes") != list(CLASSES):
        errs.append("case file classes != the frozen 16 in declaration order")
    cases = cases_data.get("cases")
    if not isinstance(cases, list) or len(cases) < MIN_CASES:
        return errs + [f"case file holds {len(cases) if isinstance(cases, list) else '?'} cases, contracted >= {MIN_CASES}"]
    per_class = {k: sum(1 for c in cases if c.get("class") == k) for k in CLASSES}
    for c in cases:
        cid = c.get("id", "?")
        cls = c.get("class")
        if cls not in CLASSES:
            errs.append(f"case {cid}: class {cls!r} not in the frozen 16")
            continue
        if not isinstance(cid, str) or not cid.startswith(cls + "-") \
                or not cid[len(cls) + 1:len(cls) + 2].isdigit():
            errs.append(f"case {cid}: id does not start with '{cls}-NN-'")
        errs += validate_case_env(c, fresh=False)
        if len(errs) > 20:
            errs.append("...more")
            break
    for k in CLASSES:
        if per_class[k] < MIN_PER_CLASS:
            errs.append(f"class {k} has {per_class[k]} cases < {MIN_PER_CLASS}")
    return errs


# ---------------------------------------------------------------- main

_ORACLE_BIN = ""
_MG = None


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
    ap.add_argument("--host-list", required=True)
    ap.add_argument("--expect-host-list-sha256", required=True)
    ap.add_argument("--host-db", required=True, help="frozen host text-DB manifest (8 files + pins)")
    ap.add_argument("--expect-host-db-sha256", required=True)
    ap.add_argument("--expect-tool-sha256", required=True,
                    help="sha256 of the frozen tools/mado-mimetext.py bytes at --rev (declaration amendment)")
    ap.add_argument("--expect-mimeglob-sha256", required=True)
    ap.add_argument("--forgery", required=True, help="frozen library-asking forgery (must be rejected)")
    ap.add_argument("--expect-forgery-sha256", required=True)
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--fresh", type=int, default=1,
                    help="fresh generations to run and score (seeds fresh_seed+i, else random)")
    ap.add_argument("--fresh-seed", type=int, default=None, help="fix the first fresh seed (default: random)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--draft-tool", help="DRAFT only: score this file instead of <rev>:" + TOOL)
    ap.add_argument("--check-only", action="store_true",
                    help="validate pins and inputs, then exit (no oracle, no legs)")
    a = ap.parse_args()
    draft = bool(a.draft_tool)
    sys.stdout.reconfigure(line_buffering=True)

    def setup(msg: str) -> int:
        print(f"MADO_MAGICTEXT_COUNT: SETUP_ERROR pred={PRED} {msg}")
        return 2

    # ---- revs
    for name, rev in (("rev", a.rev), ("base-rev", a.base_rev)):
        r = subprocess.run(["git", "-C", a.repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}"],
                           capture_output=True)
        if r.returncode != 0:
            return setup(f"{name} {rev} not a commit in {a.repo}")

    # ---- pin every frozen input
    pins = [("cases", a.cases, a.expect_cases_sha256),
            ("mutants", a.mutants, a.expect_mutants_sha256),
            ("oracle-src", a.oracle_src, a.expect_oracle_sha256),
            ("fresh-gen", a.fresh_gen, a.expect_fresh_gen_sha256),
            ("host-list", a.host_list, a.expect_host_list_sha256),
            ("host-db", a.host_db, a.expect_host_db_sha256),
            ("forgery", a.forgery, a.expect_forgery_sha256)]
    for name, path, want in pins:
        if not os.path.exists(path):
            return setup(f"{name} {path} missing")
        got = sha_file(path)
        if got != want:
            return setup(f"{name} sha256 {got} != pinned {want}")

    # ---- the tool and its pinned name-step sibling
    mimeglob_b = git_show(a.repo, a.rev, MIMEGLOB)
    if mimeglob_b is None:
        return setup(f"{MIMEGLOB} absent at {a.rev}")
    if sha(mimeglob_b) != a.expect_mimeglob_sha256:
        return setup(f"{MIMEGLOB} at {a.rev} sha256 != --expect-mimeglob-sha256")
    rn95_b = git_show(a.repo, a.rev, RN95_TOOL)
    if rn95_b is None:
        return setup(f"{RN95_TOOL} (do-nothing instrument) absent at {a.rev}")
    base_tool_b = git_show(a.repo, a.base_rev, TOOL)
    if base_tool_b is not None:
        return setup(f"{TOOL} already present at base-rev {a.base_rev} (declared before: absent)")
    print("base: tools/mado-mimetext.py absent at base-rev (declared before 0/0)")
    if a.draft_tool:
        tool_b = open(a.draft_tool, "rb").read()
    else:
        tool_b = git_show(a.repo, a.rev, TOOL)
        if tool_b is None:
            return setup(f"{TOOL} absent at {a.rev}")
    tool_pin = sha(tool_b) == a.expect_tool_sha256
    src = tool_b.decode("utf-8", "surrogateescape")

    cases_data = json.load(open(a.cases, encoding="utf-8"))
    errs = validate_cases(cases_data, a.expect_oracle_sha256)
    if errs:
        return setup("; ".join(errs[:5]))
    cases = cases_data["cases"]
    recorded_labels = [labels_of(c) for c in cases]
    case_modes = [case_mode(c) for c in cases]
    mutants_data = json.load(open(a.mutants, encoding="utf-8"))
    mutants = mutants_data["mutants"]
    equiv = mutants_data.get("equivalent_not_counted", [])
    for m in mutants:   # the mutants are anchored to the frozen candidate bytes
        if src.count(m["find"]) != 1:
            return setup(f"mutant {m['id']} find occurs {src.count(m['find'])} times")
    per_class = {k: sum(1 for c in cases if c.get("class") == k) for k in CLASSES}

    if a.check_only:
        print(f"MADO_MAGICTEXT_COUNT: CHECK_ONLY ok pred={PRED} "
              f"cases={len(cases)} mutants={len(mutants)} equiv={len(equiv)} "
              f"tool_pin={'ok' if tool_pin else 'FAIL'} classes={len(CLASSES)}")
        return 0

    if a.fresh < 1:
        return setup("--fresh must be >= 1")
    os.makedirs(a.scratch_root, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c1r96-", dir=a.scratch_root)
    secret = tempfile.mkdtemp(prefix="c1r96-labels-", dir=a.scratch_root)
    global _ORACLE_BIN, _MG, EMPTY_PATH
    static_bad: list[str] = []
    try:
        # ---- compile the oracle
        if shutil.which("cc") is None or shutil.which("pkg-config") is None:
            return setup("cc/pkg-config missing")
        _ORACLE_BIN = os.path.join(work, "oracle")
        cflags = subprocess.run(["pkg-config", "--cflags", "gio-2.0"],
                                capture_output=True, text=True).stdout.split()
        libs = subprocess.run(["pkg-config", "--libs", "gio-2.0"],
                              capture_output=True, text=True).stdout.split()
        rc = subprocess.run(["cc", "-O0", "-o", _ORACLE_BIN, a.oracle_src] + cflags + libs,
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

        # ---- place the tool, the pinned mimeglob and the round-95 do-nothing tool in a fresh tools/ dir
        tdir = os.path.join(work, "tools")
        os.makedirs(tdir)
        tool_path = os.path.join(tdir, "mado-mimetext.py")
        with open(tool_path, "wb") as fh:
            fh.write(tool_b)
        with open(os.path.join(tdir, "mado-mimeglob.py"), "wb") as fh:
            fh.write(mimeglob_b)
        with open(os.path.join(tdir, "mado-mimesniff.py"), "wb") as fh:
            fh.write(rn95_b)
        _MG = load_mg(os.path.join(tdir, "mado-mimeglob.py"))
        EMPTY_PATH = tempfile.mkdtemp(prefix="emptypath-", dir=work)
        import sysconfig
        _RUN["launcher"] = os.path.join(work, "launcher.py")
        with open(_RUN["launcher"], "w", encoding="utf-8") as fh:
            fh.write(LAUNCHER_SRC)
        pyroots = sorted({os.path.realpath(p) for k, p in sysconfig.get_paths().items()
                          if k in ("stdlib", "platstdlib", "purelib", "platlib")})
        _RUN["allow"] = os.pathsep.join([os.path.realpath(work)] + pyroots)
        for k in ("main", "mutant", "do-nothing", "selftest", "forgery"):
            _RUN["logs"][k] = os.path.join(work, f"audit-{k}.log")
            open(_RUN["logs"][k], "w").close()
        print("audit_allow=" + _RUN["allow"])

        # ---- static conjunct
        static_bad = static_check(tool_b)
        print("static_findings=" + (",".join(static_bad) or "none"))

        # ---- selftest leg (vi): green, failed=0, no sibling import needed on this path
        st = subprocess.run([sys.executable, "-I", _RUN["launcher"], audit_log("selftest"), _RUN["allow"],
                             tool_path, "--selftest"],
                            capture_output=True, text=True, timeout=TOOL_TIMEOUT,
                            cwd=work, env={"PATH": EMPTY_PATH})
        st_fail_lines = [ln for ln in st.stdout.splitlines() if ln.startswith("MADO_MIMETEXT_SELFTEST_FAIL:")]
        st_res = re.search(r"^MADO_MIMETEXT_SELFTEST: checks=(\d+) failed=(\d+)\s*$", st.stdout, re.M)
        st_checks = int(st_res.group(1)) if st_res else -1
        st_failed = int(st_res.group(2)) if st_res else -1
        selftest_ok = st.returncode == 0 and st_failed == 0 and not st_fail_lines and st_checks >= 1
        print(f"selftest rc={st.returncode} checks={st_checks} failed={st_failed} "
              f"fail_lines={len(st_fail_lines)} ok={selftest_ok}")
        for ln in st_fail_lines[:6]:
            print("selftest " + ln)

        # ---- class coverage of the frozen set (census gate; validation already SETUP_ERRORs < 8)
        classes_ok = sum(1 for k in CLASSES if per_class[k] >= MIN_PER_CLASS)
        print("per_class " + " ".join(f"{k}={per_class[k]}" for k in CLASSES))
        print("case_modes " + " ".join(f"{m}={case_modes.count(m)}" for m in ("text", "none", "cache")))

        # ---- frozen leg: oracle drift check on supported labels, then tool answers
        def oracle_label(c: dict):
            root = tempfile.mkdtemp(prefix="ocase-", dir=work)
            try:
                materialise(c, root)
                return oracle_label_case(oracle, c, root, root + ".odata", skip_refusals=True)
            finally:
                shutil.rmtree(root, ignore_errors=True)
                shutil.rmtree(root + ".odata", ignore_errors=True)

        with ThreadPoolExecutor(a.workers) as ex:
            live = list(ex.map(oracle_label, cases))
        drift = [c["id"] for c, rec, liv in zip(cases, recorded_labels, live)
                 if any(r is not None and l != r for r, l in zip(rec, liv))]
        if drift:
            return setup("oracle_drift=" + ",".join(drift[:20]))

        oc = outcomes(tool_path, cases, recorded_labels, work, a.workers)
        res = [o == "ok" for o in oc]
        for c, o in zip(cases, oc):
            if o != "ok":
                print(f"case {c['id']} {o.upper()}")
        correct = sum(res)
        n = len(cases)

        # ---- fresh leg (ii): --fresh generations, all cases pooled
        fcases: list[dict] = []
        flabs: list[list] = []
        seeds = []
        for i in range(a.fresh):
            seed = (a.fresh_seed + i) if a.fresh_seed is not None \
                else int.from_bytes(os.urandom(4), "big")
            seeds.append(seed)
            try:
                cs, ls = fresh_cases(a.fresh_gen, seed, secret, work, _ORACLE_BIN, oracle, i)
            except RuntimeError as e:
                return setup(f"fresh leg: {e}")
            fcases += cs
            flabs += ls
        foc = outcomes(tool_path, fcases, flabs, work, a.workers)
        f_in_tot = sum(len(c.get("inputs", [])) for c in fcases)
        f_in_ok = sum(len(c.get("inputs", [])) for c, o in zip(fcases, foc) if o == "ok")
        for c, o in zip(fcases, foc):
            if o != "ok":
                print(f"fresh case {c.get('id', '?')} {o.upper()}")
        print(f"fresh seeds={seeds} gens={a.fresh} cases={len(fcases)} ok={sum(o == 'ok' for o in foc)} "
              f"inputs={f_in_ok}/{f_in_tot}")

        # ---- host leg (iii): the host's own text database, rebuilt in scratch from the manifest
        try:
            dbdir, host_db_n = build_host_db(a.host_db, work)
        except RuntimeError as e:
            return setup(f"host leg: {e}")
        host_db_ok = host_db_n == HOST_DB_FILES
        print(f"host_db=ok files={host_db_n}" if host_db_ok
              else f"host_db=FAIL files={host_db_n}")
        for fn in TEXT_DB_FILES:
            print(f"host_db mime/{fn} sha256={sha_file(os.path.join(dbdir, 'mime', fn))}")
        host_paths = host_file_list(open(a.host_list, "rb").read())
        print(f"host list paths={len(host_paths)}")
        hdir = os.path.join(work, "hosth")
        os.makedirs(hdir)
        hcorrect, htot, hread = host_leg(tool_path, host_paths, work, a.workers, dbdir, hdir, oracle)
        print(f"host readable={hread} pairs={htot} correct={hcorrect}")

        # ---- mutant leg (iv)
        killed = crashed = survived = 0
        if not tool_pin:
            print("mutant leg skipped: the mutants are anchored to the frozen candidate and the tool is not it (killed=0)")
        mutdir = os.path.join(work, "mutants")
        os.makedirs(mutdir)
        with open(os.path.join(mutdir, "mado-mimeglob.py"), "wb") as fh:
            fh.write(mimeglob_b)
        class_kills = {k: 0 for k in CLASSES}
        for m in (mutants if tool_pin else []):
            mp = os.path.join(mutdir, f"mut-{m['id']}.py")
            with open(mp, "w", encoding="utf-8") as fh:
                fh.write(src.replace(m["find"], m["replace"], 1))
            mors = outcomes(mp, cases, recorded_labels, work, a.workers, audit="mutant")
            wrong_ids = [c["id"] for c, o in zip(cases, mors) if o == "wrong"]
            for k in {c["class"] for c, o in zip(cases, mors) if o == "wrong"}:
                class_kills[k] += 1
            new_crash = any(mo == "crash" and co != "crash" for mo, co in zip(mors, oc))
            if wrong_ids:
                killed += 1
                status = f"killed by {wrong_ids[0]} (+{len(wrong_ids) - 1})"
            elif new_crash:
                crashed += 1
                status = f"crashed-not-killed ({sum(mo == 'crash' and co != 'crash' for mo, co in zip(mors, oc))} new crash cases)"
            else:
                survived += 1
                status = "survived"
            print(f"mutant {m['id']} {status}")
        class_kills_ok = sum(1 for k in CLASSES if class_kills[k] >= 1)
        print("class_kills " + " ".join(f"{k}={class_kills[k]}" for k in CLASSES))

        # ---- controls (v)
        text_idx = [i for i, m in enumerate(case_modes) if m == "text"]
        none_idx = [i for i, m in enumerate(case_modes) if m == "none"]
        cache_idx = [i for i, m in enumerate(case_modes) if m == "cache"]
        dn_cases = [cases[i] for i in text_idx]
        dn_labels = [recorded_labels[i] for i in text_idx]
        dnoc = outcomes(os.path.join(tdir, "mado-mimesniff.py"), dn_cases, dn_labels, work,
                        a.workers, audit="do-nothing")
        dn_text_correct = sum(o == "ok" for o in dnoc)
        dn_text_n = len(dn_cases)
        dn_none_cases = [cases[i] for i in none_idx]
        dn_none_labels = [recorded_labels[i] for i in none_idx]
        dnoc_none = outcomes(os.path.join(tdir, "mado-mimesniff.py"), dn_none_cases, dn_none_labels,
                             work, a.workers, audit="do-nothing") if dn_none_cases else []
        dn_none_correct = sum(o == "ok" for o in dnoc_none)
        print(f"control do_nothing text={dn_text_correct}/{dn_text_n} "
              f"none={dn_none_correct}/{len(dn_none_cases)} cache_cases={len(cache_idx)}")
        no_correct = score_name_only(_MG, cases, recorded_labels, work, a.workers)
        print(f"control name_only correct={no_correct}/{n}")
        nv_correct = score_control(lambda c, root: naive_answers(_MG, c, root),
                                   cases, recorded_labels, work, a.workers)
        print(f"control naive (fallback-only) correct={nv_correct}/{n}")
        memo_path = memoriser_model_path(cases, secret)
        memo_table = json.load(open(memo_path, encoding="ascii"))
        memo_frozen = score_control(lambda c, root: memoriser_answers(memo_table, c),
                                    cases, recorded_labels, work, a.workers)
        memo_fresh = score_control(lambda c, root: memoriser_answers(memo_table, c),
                                   fcases, flabs, work, a.workers)
        print(f"control memoriser frozen={memo_frozen}/{n} fresh={memo_fresh}/{len(fcases)} "
              f"model={memo_path}")
        fdir = os.path.join(work, "forgery")
        os.makedirs(fdir)
        with open(os.path.join(fdir, "mado-mimetext.py"), "wb") as fh:
            fh.write(open(a.forgery, "rb").read())
        with open(os.path.join(fdir, "mado-mimeglob.py"), "wb") as fh:
            fh.write(mimeglob_b)
        forgery_src_b = open(a.forgery, "rb").read()
        forgery_static = static_check(forgery_src_b)
        outcomes(os.path.join(fdir, "mado-mimetext.py"), cases[:3], recorded_labels[:3], work, 1,
                 audit="forgery")
        forgery_audit = sum(1 for _ in open(audit_log("forgery"), encoding="utf-8", errors="replace"))
        forgery_rejected = forgery_audit > 0 or bool(forgery_static)
        print(f"control forgery static={','.join(forgery_static) or 'none'} audit_denials={forgery_audit} "
              f"rejected={forgery_rejected}")
        audit_lines = open(audit_log("main"), encoding="utf-8", errors="replace").read().splitlines()
        for ln in audit_lines[:20]:
            print("audit " + ln)
        audit_main = len(audit_lines)
    finally:
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(secret, ignore_errors=True)

    vi_ok = not static_bad and audit_main == 0
    met = (tool_pin and correct == n and classes_ok == len(CLASSES)
           and f_in_ok == f_in_tot and f_in_tot >= MIN_FRESH_INPUTS
           and host_db_ok and hcorrect == htot and hread >= MIN_HOST_PATHS
           and killed == len(mutants) and class_kills_ok == len(CLASSES)
           and vi_ok and selftest_ok
           and dn_text_correct == 0 and nv_correct < n and no_correct < n
           and memo_fresh == 0 and forgery_rejected)
    word = ("DRAFT_" if draft else "") + ("TARGET_MET" if met else "TARGET_MISSED")
    print(f"MADO_MAGICTEXT_COUNT: {word} pred={PRED} "
          f"rev={'draft:' + a.draft_tool if draft else a.rev} base_rev={a.base_rev} "
          f"tool_sha256={sha(tool_b)} tool_pin={'ok' if tool_pin else 'FAIL'} "
          f"mimeglob_sha256={sha(mimeglob_b)} cases={n} correct={correct} "
          f"classes={classes_ok}/{len(CLASSES)} "
          + "per_class " + " ".join(f"{k}={per_class[k]}" for k in CLASSES) + " "
          + f"fresh={f_in_ok}/{f_in_tot} fresh_cases={len(fcases)} "
          f"host={hcorrect}/{htot} host_paths={hread} "
          f"mutants={len(mutants)} killed={killed} crashed_not_killed={crashed} "
          f"class_kills={class_kills_ok}/{len(CLASSES)} "
          f"static_no_external_resolver={'ok' if vi_ok else 'FAIL'} audit_denials={audit_main} "
          f"selftest={'ok' if selftest_ok else 'FAIL'} checks={st_checks} failed={st_failed} "
          f"controls do_nothing_text={dn_text_correct}/{dn_text_n} "
          f"do_nothing_none={dn_none_correct}/{len(dn_none_cases)} "
          f"naive={nv_correct} name_only={no_correct} base=0 memoriser_fresh={memo_fresh} "
          f"forgery={'rejected' if forgery_rejected else 'ACCEPTED'} "
          f"host_db={'ok' if host_db_ok else 'FAIL'} files={host_db_n} "
          f"oracle_sha256={oracle_sha}")
    if draft:
        return 3
    return 0 if met else 1


# ===== mado counter self-invocation (added round-97 C2, seat R97MExecC2b) =====================
# Contract-4 self-invocation for this counter: `python3 -I <this file> --selftest
# [--fixtures DIR]` runs the counter's own main() over the committed fixture tree
# .ufo/waves/round-97/selftest-fixtures-v2/ and asserts, per check, an exit code and a
# stable finding id.  Fixture resolution: explicit --fixtures/--fixture-dir is terminal
# (an absent or unparseable tree there fails the checks, never falls back); without the
# flag the tree is derived from this file's own location (parents[2]/.ufo/waves/round-97/
# selftest-fixtures-v2, then the legacy selftest-fixtures), never from the cwd.  Fail
# lines are `MADO_COUNTER_SELFTEST_FAIL: <id>`; the result line is
# `MADO_COUNTER_SELFTEST: checks=N failed=0`; exit 0 green / 1 failed.  The mini runs
# rebind this module's census thresholds to the fixture scale; the production path (the
# code above this block) is byte-identical to the base counter.  Strip protocol: delete
# everything from the marker line to EOF and append exactly
#     if __name__ == "__main__":
#         sys.exit(main())
# to recover the base production bytes (the report prints added/removed line counts).

_ST_FAIL_PREFIX = "MADO_COUNTER_SELFTEST_FAIL: "
_ST_IDS = ("st-fixture-dir", "st-tool-pin", "st-gate-target-met", "st-setup-missing-input",
           "st-setup-wrong-pin", "st-setup-wrong-rev", "st-target-missed-case",
           "st-target-missed-mutant", "st-result-line-format", "st-scratch-clean")
_ST_FIXTURE_SUBDIRS = ("selftest-fixtures-v2", "selftest-fixtures")
_ST_PINS_REL = "pins.json"
_ST_PIN_REQUIRED = ("c1/mado-mimetext.py", "c1/mado-mimeglob.py", "c1/mado-mimesniff.py",
                    "c1/cases-mini.json", "c1/mutants-mini.json", "c1/mutants-mini2.json",
                    "c1/freshgen.py", "c1/hostdb-manifest.json", "c1/hostlist.txt",
                    "c1/bugtool-mutation.json",
                    "common/mimesniff-oracle-r95.c", "common/forgery-ctypes-r96.py",
                    "common/canary.txt", "common/canary.png", "common/canary.pk")
# unique weakening anchors, one per check (each name occurs once in this block)
_ST_GREEN_RC_WANT = 0                        # st-gate-target-met (rc anchor, unique)
_ST_GREEN_MARK = "TARGET_MET"                # st-gate-target-met (mark anchor, unique)
_ST_LINE_RC_WANT = 0                         # st-result-line-format (rc anchor, unique)
_ST_LINE_PREFIX = "MADO_MAGICTEXT_COUNT: TARGET_MET pred=PRED-C1-r96-v1 "
_ST_LINE_TOKENS = ("tool_pin=ok", "cases=2 correct=2", "selftest=ok", "audit_denials=0")
_ST_MISSING_RC_WANT = 2                      # st-setup-missing-input (rc anchor, unique)
_ST_MISSING_MARK = "SETUP_ERROR"             # st-setup-missing-input (mark anchor, unique)
_ST_PINRUN_RC_WANT = 2                       # st-setup-wrong-pin (rc anchor, unique)
_ST_PINRUN_MARK = "SETUP_ERROR"              # st-setup-wrong-pin (mark anchor, unique)
_ST_BADREV_RC_WANT = 2                       # st-setup-wrong-rev (rc anchor, unique)
_ST_BADREV_MARK = "SETUP_ERROR"              # st-setup-wrong-rev (mark anchor, unique)
_ST_WRONGPIN_TOKEN = "0" * 64                # st-setup-wrong-pin
_ST_BADREV_TOKEN = "0" * 40                  # st-setup-wrong-rev
_ST_MISSED_CASE_RC_WANT = 1                 # st-target-missed-case (rc anchor, unique)
_ST_MISSED_CASE_MARK = "TARGET_MISSED"      # st-target-missed-case (mark anchor, unique)
_ST_MISSED_MUT_RC_WANT = 1                  # st-target-missed-mutant (rc anchor, unique)
_ST_MISSED_MUT_MARK = "TARGET_MISSED"       # st-target-missed-mutant (mark anchor, unique)
_ST_MINI_REBIND = {"MIN_CASES": 2, "MIN_PER_CLASS": 1, "CLASSES": ("mini",),
                   "MIN_FRESH_INPUTS": 2, "MIN_HOST_PATHS": 3, "HOST_DB_FILES": 2,
                   "TEXT_DB_FILES": ("globs2", "magic")}


class _STOut:
    """stdout stand-in for in-process main() runs (main reconfigures line buffering)."""

    def __init__(self):
        import io
        self._buf = io.StringIO()

    def reconfigure(self, *args, **kwargs):
        return None

    def write(self, text):
        return self._buf.write(text)

    def flush(self):
        return None

    def getvalue(self):
        return self._buf.getvalue()


def _st_resolve_fixtures(explicit):
    if explicit is not None:
        p = os.path.abspath(explicit)
        return p if os.path.isdir(p) else None
    node = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        for sub in _ST_FIXTURE_SUBDIRS:
            p = os.path.join(node, ".ufo", "waves", "round-97", sub)
            if os.path.isdir(os.path.join(p, "c1")):
                return p
        nxt = os.path.dirname(node)
        if nxt == node:
            break
        node = nxt
    return None


def _st_run_main(argv, rebind):
    """One in-process production run: sys.argv + rebound census thresholds, stdout captured."""
    saved = {k: globals()[k] for k in rebind}
    old_argv, old_out = sys.argv, sys.stdout
    out = _STOut()
    try:
        globals().update(rebind)
        sys.argv = ["c1-r96-magictext"] + [str(a) for a in argv]
        sys.stdout = out
        rc = main()
        return rc, out.getvalue()
    finally:
        sys.stdout = old_out
        sys.argv = old_argv
        globals().update(saved)
        globals()["_ORACLE_BIN"] = ""
        globals()["_MG"] = None
        globals()["EMPTY_PATH"] = ""


def _st_git(args, cwd):
    return subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True)


def _st_build_repo(root, fixtures, mimetext_b):
    d = tempfile.mkdtemp(prefix="strepo-", dir=root)
    if _st_git(["init", "-q"], d).returncode != 0:
        raise RuntimeError("fixture repo git init failed")
    top = _st_git(["rev-parse", "--show-toplevel"], d)
    if os.path.realpath(top.stdout.strip()) != os.path.realpath(d):
        raise RuntimeError("fixture repo toplevel mismatch")
    tdir = os.path.join(d, "tools")
    os.makedirs(tdir)
    for name in ("mado-mimeglob.py", "mado-mimesniff.py"):
        with open(os.path.join(tdir, name), "wb") as fh:
            fh.write(open(os.path.join(fixtures, "c1", name), "rb").read())
    if _st_git(["add", "-A"], d).returncode != 0:
        raise RuntimeError("fixture repo add failed")
    if _st_git(["-c", "user.name=mado-selftest", "-c", "user.email=selftest@mado",
                "commit", "-q", "-m", "base"], d).returncode != 0:
        raise RuntimeError("fixture repo base commit failed")
    with open(os.path.join(tdir, "mado-mimetext.py"), "wb") as fh:
        fh.write(mimetext_b)
    _st_git(["add", "-A"], d)
    if _st_git(["-c", "user.name=mado-selftest", "-c", "user.email=selftest@mado",
                "commit", "-q", "-m", "candidate"], d).returncode != 0:
        raise RuntimeError("fixture repo candidate commit failed")
    base_rev = _st_git(["rev-parse", "HEAD~1"], d).stdout.strip()
    rev = _st_git(["rev-parse", "HEAD"], d).stdout.strip()
    return d, base_rev, rev


def _st_c1_argv(repo, base_rev, rev, scr, fixtures, mutants_rel, expect_tool_sha):
    def fx(rel):
        return os.path.join(fixtures, rel)

    hostlist = os.path.join(repo, "hostlist.txt")
    with open(hostlist, "w", encoding="utf-8") as fh:
        fh.write(open(fx("c1/hostlist.txt"), encoding="utf-8").read().replace("{FIXTURES}", fixtures))
    manifest = os.path.join(repo, "hostdb-manifest.json")
    with open(manifest, "w", encoding="utf-8") as fh:
        fh.write(open(fx("c1/hostdb-manifest.json"), encoding="utf-8").read().replace("{FIXTURES}", fixtures))
    mutp = fx(mutants_rel)
    sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
    return ["--repo", repo, "--rev", rev, "--base-rev", base_rev,
            "--cases", fx("c1/cases-mini.json"), "--expect-cases-sha256", sha(fx("c1/cases-mini.json")),
            "--mutants", mutp, "--expect-mutants-sha256", sha(mutp),
            "--oracle-src", fx("common/mimesniff-oracle-r95.c"),
            "--expect-oracle-sha256", sha(fx("common/mimesniff-oracle-r95.c")),
            "--fresh-gen", fx("c1/freshgen.py"), "--expect-fresh-gen-sha256", sha(fx("c1/freshgen.py")),
            "--host-list", hostlist, "--expect-host-list-sha256", sha(hostlist),
            "--host-db", manifest, "--expect-host-db-sha256", sha(manifest),
            "--expect-tool-sha256", expect_tool_sha,
            "--expect-mimeglob-sha256", sha(fx("c1/mado-mimeglob.py")),
            "--forgery", fx("common/forgery-ctypes-r96.py"),
            "--expect-forgery-sha256", sha(fx("common/forgery-ctypes-r96.py")),
            "--scratch-root", scr, "--workers", "8"]


def _mado_counter_selftest(argv):
    fixtures_arg = None
    for i, tok in enumerate(argv):
        if tok in ("--fixtures", "--fixture-dir") and i + 1 < len(argv):
            fixtures_arg = argv[i + 1]
            break
    checks = []

    def add(cid, ok):
        checks.append((cid, bool(ok)))

    fixtures = _st_resolve_fixtures(fixtures_arg)
    print("FIXTURES: " + (fixtures if fixtures else "UNRESOLVED"))
    add("st-fixture-dir", fixtures is not None
        and os.path.isfile(os.path.join(fixtures, _ST_PINS_REL)))
    pins_ok = False
    pins = {}
    if fixtures is not None:
        try:
            doc = json.load(open(os.path.join(fixtures, _ST_PINS_REL), encoding="utf-8"))
            pins = doc["files"]
            pins_ok = isinstance(pins, dict)
        except (OSError, ValueError, KeyError):
            pins_ok = False
    pin_bad = []
    for rel in _ST_PIN_REQUIRED:
        want = pins.get(rel)
        p = os.path.join(fixtures or ".", rel)
        try:
            got = hashlib.sha256(open(p, "rb").read()).hexdigest()
        except OSError:
            pin_bad.append(rel)
            continue
        if not isinstance(want, str) or got != want:
            pin_bad.append(rel)
    add("st-tool-pin", pins_ok and not pin_bad)

    fx_bytes = lambda rel: open(os.path.join(fixtures, rel), "rb").read() if fixtures else b""
    tool_sha = lambda: hashlib.sha256(fx_bytes("c1/mado-mimetext.py")).hexdigest()

    if fixtures is not None and pins_ok:
        base = tempfile.mkdtemp(prefix="stc1-")
        try:
            tool_b = fx_bytes("c1/mado-mimetext.py")
            repo, base_rev, rev = _st_build_repo(base, fixtures, tool_b)
            # ---- green scene: feeds st-gate-target-met, st-result-line-format, st-scratch-clean
            scr = os.path.join(base, "run-green")
            os.makedirs(scr)
            try:
                grc, gout = _st_run_main(_st_c1_argv(repo, base_rev, rev, scr, fixtures,
                                                     "c1/mutants-mini.json", tool_sha()),
                                         _ST_MINI_REBIND)
            except Exception:
                grc, gout = None, ""
            add("st-gate-target-met", grc == _ST_GREEN_RC_WANT and _ST_GREEN_MARK in gout)
            glines = [ln for ln in gout.splitlines() if ln.startswith(_ST_LINE_PREFIX[:24])]
            glast = glines[-1] if glines else ""
            add("st-result-line-format", grc == _ST_LINE_RC_WANT and glast.startswith(_ST_LINE_PREFIX)
                and all(tok in glast for tok in _ST_LINE_TOKENS))
            add("st-scratch-clean", grc is not None and os.path.isdir(scr) and os.listdir(scr) == [])
            # ---- setup scenes (fast: they stop at pins/rev verification)
            scr2 = os.path.join(base, "run-missing")
            os.makedirs(scr2)
            av = _st_c1_argv(repo, base_rev, rev, scr2, fixtures, "c1/mutants-mini.json", tool_sha())
            ai = av.index("--cases") + 1
            av[ai] = os.path.join(scr2, "missing-cases.json")
            try:
                rc, out = _st_run_main(av, _ST_MINI_REBIND)
            except Exception:
                rc, out = None, ""
            add("st-setup-missing-input", rc == _ST_MISSING_RC_WANT and _ST_MISSING_MARK in out)
            scr3 = os.path.join(base, "run-pin")
            os.makedirs(scr3)
            av = _st_c1_argv(repo, base_rev, rev, scr3, fixtures, "c1/mutants-mini.json", tool_sha())
            ai = av.index("--expect-mimeglob-sha256") + 1
            av[ai] = _ST_WRONGPIN_TOKEN
            try:
                rc, out = _st_run_main(av, _ST_MINI_REBIND)
            except Exception:
                rc, out = None, ""
            add("st-setup-wrong-pin", rc == _ST_PINRUN_RC_WANT and _ST_PINRUN_MARK in out)
            scr4 = os.path.join(base, "run-rev")
            os.makedirs(scr4)
            av = _st_c1_argv(repo, base_rev, _ST_BADREV_TOKEN, scr4, fixtures,
                             "c1/mutants-mini.json", tool_sha())
            try:
                rc, out = _st_run_main(av, _ST_MINI_REBIND)
            except Exception:
                rc, out = None, ""
            add("st-setup-wrong-rev", rc == _ST_BADREV_RC_WANT and _ST_BADREV_MARK in out)
            # ---- missed scene 1: a deliberately mismatched tool (the bugtool mutation applied;
            # its anchor is absent from both mutants files, so their finds stay unique)
            bugmu = json.loads(fx_bytes("c1/bugtool-mutation.json").decode("ascii"))
            bug_b = tool_b.replace(bugmu["find"].encode("ascii"), bugmu["replace"].encode("ascii"), 1)
            if bug_b != tool_b:
                repo2, base2, rev2 = _st_build_repo(base, fixtures, bug_b)
                scr5 = os.path.join(base, "run-missed-case")
                os.makedirs(scr5)
                try:
                    rc, out = _st_run_main(_st_c1_argv(repo2, base2, rev2, scr5, fixtures,
                                                       "c1/mutants-mini.json", tool_sha()),
                                           _ST_MINI_REBIND)
                except Exception:
                    rc, out = None, ""
                add("st-target-missed-case", rc == _ST_MISSED_CASE_RC_WANT and _ST_MISSED_CASE_MARK in out)
            else:
                add("st-target-missed-case", False)
            # ---- missed scene 2: a surviving (no-op) mutant in the mutant file
            scr6 = os.path.join(base, "run-missed-mut")
            os.makedirs(scr6)
            try:
                rc, out = _st_run_main(_st_c1_argv(repo, base_rev, rev, scr6, fixtures,
                                                   "c1/mutants-mini2.json", tool_sha()),
                                       _ST_MINI_REBIND)
            except Exception:
                rc, out = None, ""
            add("st-target-missed-mutant", rc == _ST_MISSED_MUT_RC_WANT and _ST_MISSED_MUT_MARK in out)
        except Exception:
            for cid in ("st-gate-target-met", "st-result-line-format", "st-scratch-clean",
                        "st-setup-missing-input", "st-setup-wrong-pin", "st-setup-wrong-rev",
                        "st-target-missed-case", "st-target-missed-mutant"):
                if cid not in [c for c, _ in checks]:
                    add(cid, False)
        finally:
            shutil.rmtree(base, ignore_errors=True)
    else:
        for cid in ("st-gate-target-met", "st-result-line-format", "st-scratch-clean",
                    "st-setup-missing-input", "st-setup-wrong-pin", "st-setup-wrong-rev",
                    "st-target-missed-case", "st-target-missed-mutant"):
            add(cid, False)

    failed = [cid for cid, ok in checks if not ok]
    for cid in failed:
        print(_ST_FAIL_PREFIX + cid)
    print("MADO_COUNTER_SELFTEST: checks=%d failed=%d" % (len(checks), len(failed)))
    return 0 if not failed else 1


if __name__ == "__main__":  # replaces the base guard verbatim; production argv path unchanged
    if "--selftest" in sys.argv[1:]:
        sys.exit(_mado_counter_selftest(sys.argv[1:]))
    sys.exit(main())
