#!/usr/bin/env python3
"""Round-95 C1 counter - file bytes + name -> MIME type as GLib 2.90.1 g_content_type_guess answers.

Frozen predicate PRED-C1-r95-v1 (the same sentence as the declaration and the receipt label; w1 amendments folded in
by the L1 before any measurement):
  TARGET_MET iff, at <rev>, tools/mado-mimesniff.py is the frozen candidate and tools/mado-mimeglob.py is round 94's
  bytes (tool_pin=ok), and
  (i) on every frozen case the tool's (type, uncertain) equals the oracle's label for every input (an input labelled
      ["UNSUPPORTED", null] - the oracle run on that input ALONE crashes or hangs - and every input of a case marked
      "expect_refusal": true require exit 3), and the oracle re-run per input at measurement equals the recorded
      label (else SETUP_ERROR); each of the 20 classes zerosize fallback lltext order prio multicache range mask
      nest bounds wrap desktop name1 name0 nameN subclass alias slash mode real holds >= 6 cases (classes=20/20),
      no case carries another class (SETUP_ERROR), and each class's cases make at least one counted mutant wrong
      (class_kills=20/20); every `real` case's mime.cache equals update-mime-database rebuilt from the case's own
      packages/*.xml (real_rebuild=K/K);
  (ii) on 120 fresh cases from the frozen generator, seeded at measurement from os.urandom (seed printed, never
      stored), the tool equals the live oracle;
  (iii) on every readable file of the frozen host list, sniffed (first 4096 bytes) data-only and with its own path
      as the name, under the counter's HOME/XDG environment, the tool equals the live oracle (host DB digests
      printed);
  (iv) every one of the >= 40 counted mutants makes at least one frozen case wrong (a crash is crashed_not_killed);
  (v) each control misses: do-nothing (application/octet-stream, 1), the name-only answer of round 94's
      tools/mado-mimeglob.py (data ignored), a naive sniff (first matching top-level value at its range start, cache
      order, no priority/mask/children/subclass), and the base revision (no tool -> 0) each miss (i); a memoriser
      (the frozen labels, do-nothing elsewhere) misses (ii) (memoriser_fresh < fresh total); the frozen
      sibling-module ctypes forgery (--forgery) is rejected by (vi) (forgery=rejected);
  (vi) static_no_external_resolver=ok (QUALITY 162, refined): the tool's imports are only __future__, argparse,
      importlib.util, json, os, struct, sys, tempfile (selftest fixtures); no name eval/exec/compile/__import__/getattr/setattr/delattr/vars/
      globals/locals/breakpoint; no `.__x__` attribute access; no os.system/popen/exec*/spawn*/posix_spawn*/fork*;
      exactly one importlib.util.spec_from_file_location call, its location argument containing __file__ and the
      constant "mado-mimeglob.py"; the name it is bound to (via module_from_spec) is used only for
      Unsupported, oob, Resolver, xdgmime_dirs, g_path_get_basename, esc, _LC_ALL and _libc.setlocale; and
      audit=ok: every tool run (frozen, fresh, host) runs under an audit-hook launcher that refuses (exit 97,
      logged) any open() outside the run's scratch, the Python installation, /dev/null and (host leg) the host MIME
      directories, any process spawn other than /usr/bin|/usr/sbin ldconfig|gcc|cc|ld|objdump (ctypes.util's libc
      lookup), any socket, and any ctypes.dlopen other than libc; every tool run gets PATH = an empty directory.

Case file schema (version 1): {"version":1,"oracle_src_sha256":"...","glib2":"...","cases":[
 {"id","class","env":{"HOME","XDG_DATA_HOME"|null,"XDG_DATA_DIRS"},"files":{rel:b64},"expect_refusal"?:bool,
  "inputs":[{"name_b64":null|b64,"data_b64":b64}],"labels":[[type,0|1]|["UNSUPPORTED",null]]}]}.
Each input is labelled by its own oracle run (one "<0|=NAME> <datafile>" pair); a crash, a hang (> 10 s) or a
malformed line labels that input ["UNSUPPORTED", null].  XDG_DATA_DIRS unset is forbidden in cases (it would reach
the host databases): SETUP_ERROR.

A frozen case is scored by running the tool once per distinct input name (the tool's --name applies one name to
every FILE of an invocation; inputs that must be refused are run in their own invocations so a refusal cannot mask
supported answers): "ok" when every supported input's (type, uncertain) equals its label and every must-refuse input
makes the tool exit 3; "wrong" when the tool answers anything that differs, refuses a supported input or answers a
must-refuse input; "crash" otherwise (nonzero exit other than 3, timeout, malformed JSON).  "wrong" dominates.

The oracle is compiled once from --oracle-src (sha256 pinned) into --scratch-root with `cc -O1 ... $(pkg-config
--cflags --libs gio-2.0)`; its binary sha256 and `pacman -Q glib2 shared-mime-info` are printed.  Every frozen input
(--cases, --mutants, --fresh-gen, --host-files, --forgery, the tool and mimeglob) is pinned by sha256; a mismatch is
SETUP_ERROR rc 2.  All materialisation lives under --scratch-root; TMPDIR is honoured.  Stdlib only.
rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR, 3 DRAFT (--draft-tool PATH; prints DRAFT_*).
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

PRED = "PRED-C1-r95-v1"
CLASSES = ("zerosize", "fallback", "lltext", "order", "prio", "multicache", "range", "mask",
           "nest", "bounds", "wrap", "desktop", "name1", "name0", "nameN", "subclass", "alias",
           "slash", "mode", "real")
MIN_PER_CLASS = 6
MIN_MUTANTS = 40
MIN_FRESH = 120
EMPTY_PATH = ""
TOOL = "tools/mado-mimesniff.py"
MIMEGLOB = "tools/mado-mimeglob.py"
UNKNOWN = "application/octet-stream"
TOOL_TIMEOUT = 30.0
ORACLE_CASE_TIMEOUT = 10.0     # the case schema: an oracle run over 10 s is UNSUPPORTED
ORACLE_FRESH_TIMEOUT = 30.0
ORACLE_HOST_TIMEOUT = 60.0
FRESH_RUN_TIMEOUT = 600.0
HOST_ORACLE_PAIRS = 1000       # pairs per oracle invocation on the host leg
HOST_TOOL_FILES = 400          # files per tool invocation on the data-only host leg


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


def oracle_label_case(oracle: Oracle, case: dict, root: str, dstdir: str) -> list[tuple[str, int] | None]:
    """One oracle run per input (a crash on one input never labels another); None = crashed/timed out."""
    inputs = case_inputs(case)
    dfs = write_input_files(inputs, dstdir)
    out: list[tuple[str, int] | None] = []
    for (name, _data), df in zip(inputs, dfs):
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
                   allow_extra: str = "") -> tuple[str, list[tuple[str, int]] | None]:
    """Run the tool on one name group, under the audit launcher (log `audit`).

    Returns ("ok", answers) | ("unsupported", None) on exit 3 | ("crash", None) otherwise (exit 97 = audit denial,
    logged and counted by conjunct (vi)).
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
        return "crash", None
    if r.returncode == 3:
        return "unsupported", None
    if r.returncode != 0:
        return "crash", None
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return "crash", None
    res = d.get("results")
    if not isinstance(res, list) or len(res) != len(files):
        return "crash", None
    out = []
    for x in res:
        if not isinstance(x, dict) or not isinstance(x.get("type"), str) \
                or x.get("uncertain") not in (0, 1):
            return "crash", None
        out.append((x["type"], int(x["uncertain"])))
    return "ok", out


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
                status, answers = run_tool_group(tool, name, [dfs[i] for i in sup], flags, root, timeout, audit)
                if status == "crash":
                    crash = True
                elif status == "unsupported":
                    wrong = True   # the tool refused a supported input
                elif status == "ok":
                    if answers is None or any(answers[j] != labels[i] for j, i in enumerate(sup)):
                        wrong = True
            for i in uns:      # each must-refuse input alone: the CLI stops at its first refusal
                status, _answers = run_tool_group(tool, name, [dfs[i]], flags, root, timeout, audit)
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


# ---------------------------------------------------------------- static conjunct (vi)

_OK_IMPORTS = {"__future__", "argparse", "importlib.util", "json", "os", "struct", "sys", "tempfile"}
_BAD_OS = re.compile(r"^(system|popen|exec\w*|spawn\w*|posix_spawn\w*|fork\w*)$")
_BAD_NAMES = {"eval", "exec", "compile", "__import__", "getattr", "setattr", "delattr", "vars", "globals",
              "locals", "breakpoint", "import_module", "reload"}
_MG_ATTRS = {"Unsupported", "oob", "Resolver", "xdgmime_dirs", "g_path_get_basename", "esc", "_LC_ALL"}


def static_check(src: bytes) -> list[str]:
    """Findings that make static_no_external_resolver FAIL (empty list = ok); the sentence is conjunct (vi)."""
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


# the audit-hook launcher every tool run goes through (conjunct (vi) audit=ok)
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

def do_nothing_answers(labels_len: int) -> list[tuple[str, int]]:
    return [(UNKNOWN, 1)] * labels_len


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


def naive_magic_matchlet(c, off: int, data: bytes) -> bool:
    """Naive matchlet: the value compared once, at its range start; no mask, no children."""
    rs = c.u32(off)
    vl = c.u32(off + 12)
    vo = c.u32(off + 16)
    if rs + vl > len(data):
        return False
    return data[rs:rs + vl] == c.buf[vo:vo + vl]


def naive_magic_first(caches: list, data: bytes) -> str | None:
    """Naive sniff: first matching top-level matchlet in cache order; no priority across caches."""
    mg = _MG
    for c in caches:
        try:
            lo = c.u32(24)
            if mg.oob(lo, 1, 12, c.size):
                continue
            n = c.u32(lo)
            off = c.u32(lo + 8)
            if mg.oob(off, n, 16, c.size):
                continue
            for j in range(n):
                e = off + 16 * j
                mo = c.u32(e + 4)
                nm = c.u32(e + 8)
                mlo = c.u32(e + 12)
                if mg.oob(mlo, nm, 32, c.size):
                    continue
                for k in range(nm):
                    if naive_magic_matchlet(c, mlo + 32 * k, data):
                        return c.cstr(mo).decode("utf-8", "surrogateescape")
        except mg.Unsupported:
            continue
    return None


def naive_looks_like_text(data: bytes) -> bool:
    return not any(b < 8 or 14 <= b < 32 or b == 127 for b in data)


def naive_guess(name: bytes | None, data: bytes, resolver, caches: list) -> tuple[str, int] | None:
    """Control (v): the naive sniff - first matching top-level value at its range start, cache
    order, no priority/mask/children/subclass.  The name step is round 94's (the parenthetical
    naivifies only the magic evaluation, the cache priority and the subclass tie-break; the
    prio >= 80 sniffed-wins rule is dropped with the priority, so any non-UNKNOWN sniff wins)."""
    mg = _MG
    if name is not None and name.endswith(b"/"):
        return ("inode/directory", 1)
    try:
        types = resolver.guess(name)["types"] if name is not None else []
    except mg.Unsupported:
        return None
    if len(types) == 1:
        return (types[0], 0)
    if len(data) == 0:
        sniffed = "application/x-zerosize"
    else:
        m = naive_magic_first(caches, data)
        if m is not None:
            sniffed = m
        elif any(b < 32 and b not in (9, 10, 13) for b in data[:128]):
            sniffed = UNKNOWN
        else:
            sniffed = "text/plain"
    if sniffed == UNKNOWN and naive_looks_like_text(data):
        sniffed = "text/plain"
    if name is not None and sniffed == "application/x-desktop":
        sniffed = "text/plain"
    if not types:
        return (sniffed, 1 if sniffed == UNKNOWN else 0)
    if sniffed != UNKNOWN:
        return (sniffed, 0)
    return (types[0], 1)


def naive_answers(mg, case: dict, root: str) -> list[tuple[str, int] | None] | str:
    env = case_env(case, root)
    dirs = mg.xdgmime_dirs(env.get("XDG_DATA_HOME"), env.get("HOME"), env.get("XDG_DATA_DIRS"))
    try:
        resolver = mg.Resolver(dirs)
    except mg.Unsupported:
        return "REFUSE"
    caches = []
    for d in dirs:
        cp = d + "mime.cache"
        if os.path.exists(cp):
            c = mg.load_cache(cp)
            if c is not None:
                caches.append(c)
    out = []
    for name, data in case_inputs(case):
        out.append(naive_guess(name, data, resolver, caches))
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


def score_name_only(mg, cases: list[dict], labels: list[list], work: str, jobs: int) -> int:
    def one(ca):
        c, lab = ca
        root = tempfile.mkdtemp(prefix="no-", dir=work)
        try:
            materialise(c, root)
            return control_ok(name_only_answers(mg, c, root), lab)
        finally:
            shutil.rmtree(root, ignore_errors=True)
    with ThreadPoolExecutor(jobs) as ex:
        return sum(1 for ok in ex.map(one, zip(cases, labels)) if ok)


def score_naive(mg, cases: list[dict], labels: list[list], work: str, jobs: int) -> int:
    def one(ca):
        c, lab = ca
        root = tempfile.mkdtemp(prefix="nv-", dir=work)
        try:
            materialise(c, root)
            return control_ok(naive_answers(mg, c, root), lab)
        finally:
            shutil.rmtree(root, ignore_errors=True)
    with ThreadPoolExecutor(jobs) as ex:
        return sum(1 for ok in ex.map(one, zip(cases, labels)) if ok)


def score_do_nothing(labels: list[list]) -> int:
    return sum(1 for lab in labels
               if all(l == (UNKNOWN, 1) for l in lab))


# ---------------------------------------------------------------- fresh leg

def fresh_cases(gen_path: str, seed: int, n: int, work: str, oracle: Oracle) -> tuple[list[dict], list[list]]:
    """Run the frozen generator to an unlabelled case file, then label every case with the oracle."""
    gen_out = os.path.join(work, f"fresh-{seed}.json")
    env = dict(os.environ, TMPDIR=work)
    r = subprocess.run([sys.executable, "-I", gen_path, "--seed", str(seed), "--count", str(n),
                        "--out", gen_out],
                       capture_output=True, text=True, timeout=FRESH_RUN_TIMEOUT, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"fresh generator rc={r.returncode}: {r.stderr[-400:]}")
    try:
        data = json.load(open(gen_out, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise RuntimeError(f"fresh generator output unreadable: {e}")
    cases = data["cases"] if isinstance(data, dict) else data
    if len(cases) != n:
        raise RuntimeError(f"fresh generator made {len(cases)} cases, asked {n}")

    def label(c: dict):
        root = tempfile.mkdtemp(prefix="freshcase-", dir=work)
        try:
            materialise(c, root)
            return oracle_label_case(oracle, c, root, root + ".odata")
        finally:
            shutil.rmtree(root, ignore_errors=True)
            shutil.rmtree(root + ".odata", ignore_errors=True)

    with ThreadPoolExecutor(min(16, os.cpu_count() or 4)) as ex:
        labs = list(ex.map(label, cases))
    return cases, labs


# ---------------------------------------------------------------- host leg

def host_leg(tool: str, paths: list[bytes], work: str, jobs: int) -> tuple[int, int, int]:
    """(correct, total, readable).  Every readable file sniffed (first 4096 bytes) data-only and
    with its own path as the name, under the counter's HOME/XDG environment."""
    host_env = {"HOME": os.environ.get("HOME"),
                "XDG_DATA_HOME": os.environ.get("XDG_DATA_HOME"),
                "XDG_DATA_DIRS": os.environ.get("XDG_DATA_DIRS")}
    hroot = tempfile.mkdtemp(prefix="host-", dir=work)
    hdata = tempfile.mkdtemp(prefix="hostdata-", dir=work)
    host_allow = os.pathsep.join(_MG.xdgmime_dirs(host_env["XDG_DATA_HOME"], host_env["HOME"],
                                                  host_env["XDG_DATA_DIRS"]))
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
        oracle = Oracle(_ORACLE_BIN)
        oenv = {"LC_ALL": "C"}
        for k, v in host_env.items():
            if v is not None:
                oenv[k] = v
        # oracle labels: pairs (None, data) and (path, data) per file, chunked
        pairs = []
        for p, sp in files:
            pairs.append((None, sp))
            pairs.append((p, sp))
        labels: list[tuple[str, int]] = []
        for i in range(0, len(pairs), HOST_ORACLE_PAIRS):
            chunk = pairs[i:i + HOST_ORACLE_PAIRS]
            got = oracle.run_pairs(chunk, oenv, hroot, ORACLE_HOST_TIMEOUT)
            if got is None:
                raise RuntimeError("host leg: oracle produced no answer")
            labels += got
        flags = tool_env_flags(host_env)
        # data-only: name NULL for every file, chunked
        correct = 0
        for i in range(0, n, HOST_TOOL_FILES):
            chunk = files[i:i + HOST_TOOL_FILES]
            status, answers = run_tool_group(tool, None, [sp for _p, sp in chunk], flags, hroot,
                                             timeout=TOOL_TIMEOUT * 4, audit="main", allow_extra=host_allow)
            if status == "ok" and answers is not None:
                for j, (_p, _sp) in enumerate(chunk):
                    if answers[j] == labels[2 * (i + j)]:
                        correct += 1
        # own path as the name: one invocation per file
        def one(arg):
            k, (p, sp) = arg
            status, answers = run_tool_group(tool, p, [sp], flags, hroot, timeout=TOOL_TIMEOUT * 4,
                                             audit="main", allow_extra=host_allow)
            if status == "ok" and answers is not None and answers[0] == labels[2 * k + 1]:
                return 1
            return 0
        with ThreadPoolExecutor(jobs) as ex:
            correct += sum(ex.map(one, enumerate(files)))
        return correct, htot, n
    finally:
        shutil.rmtree(hroot, ignore_errors=True)
        shutil.rmtree(hdata, ignore_errors=True)


# ---------------------------------------------------------------- main

_ORACLE_BIN = ""
_MG = None


def validate_cases(cases_data: dict, expect_oracle_sha: str) -> list[str]:
    """Envelope + per-case sanity; returns a list of SETUP_ERROR messages (empty = ok)."""
    errs = []
    if cases_data.get("version") != 1:
        errs.append(f"case file version {cases_data.get('version')!r} != 1")
    if cases_data.get("oracle_src_sha256") != expect_oracle_sha:
        errs.append("case file oracle_src_sha256 != pinned oracle source")
    cases = cases_data.get("cases")
    if not isinstance(cases, list) or not cases:
        return errs + ["case file has no cases"]
    for c in cases:
        cid = c.get("id", "?")
        if c.get("class") not in CLASSES:
            errs.append(f"case {cid}: class {c.get('class')!r} not in the frozen 20")
        if "expect_refusal" in c and not isinstance(c["expect_refusal"], bool):
            errs.append(f"case {cid}: expect_refusal is not a bool")
        env = c.get("env", {})
        if env.get("XDG_DATA_DIRS") is None:
            errs.append(f"case {cid}: XDG_DATA_DIRS unset is forbidden in cases")
        inputs = c.get("inputs", [])
        labels = c.get("labels", [])
        if not inputs:
            errs.append(f"case {cid}: no inputs")
        if len(inputs) != len(labels):
            errs.append(f"case {cid}: {len(inputs)} inputs vs {len(labels)} labels")
            continue
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
    return errs


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
    ap.add_argument("--host-files", required=True)
    ap.add_argument("--expect-host-files-sha256", required=True)
    ap.add_argument("--expect-tool-sha256", required=True)
    ap.add_argument("--expect-mimeglob-sha256", required=True)
    ap.add_argument("--forgery", required=True, help="frozen sibling-module forgery (must be rejected by (vi))")
    ap.add_argument("--expect-forgery-sha256", required=True)
    ap.add_argument("--fresh", type=int, default=MIN_FRESH, help="fresh cases to generate and label")
    ap.add_argument("--fresh-seed", type=int, default=None, help="fix the fresh seed (default: random)")
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--draft-tool", help="DRAFT only: score this file instead of <rev>:" + TOOL)
    ap.add_argument("--check-only", action="store_true",
                    help="validate pins and inputs, then exit (no oracle, no legs)")
    a = ap.parse_args()
    draft = bool(a.draft_tool)
    sys.stdout.reconfigure(line_buffering=True)

    def setup(msg: str) -> int:
        print(f"MADO_MIMESNIFF_COUNT: SETUP_ERROR pred={PRED} {msg}")
        return 2

    # ---- pin every frozen input
    pins = [("cases", a.cases, a.expect_cases_sha256),
            ("mutants", a.mutants, a.expect_mutants_sha256),
            ("oracle-src", a.oracle_src, a.expect_oracle_sha256),
            ("fresh-gen", a.fresh_gen, a.expect_fresh_gen_sha256),
            ("host-files", a.host_files, a.expect_host_files_sha256),
            ("forgery", a.forgery, a.expect_forgery_sha256)]
    for name, path, want in pins:
        if not os.path.exists(path):
            return setup(f"{name} {path} missing")
        got = sha_file(path)
        if got != want:
            return setup(f"{name} sha256 {got} != pinned {want}")

    cases_data = json.load(open(a.cases, encoding="utf-8"))
    errs = validate_cases(cases_data, a.expect_oracle_sha256)
    if errs:
        return setup("; ".join(errs[:5]))
    cases = cases_data["cases"]
    recorded_labels = [labels_of(c) for c in cases]
    # what the tool must answer: every input of an expect_refusal case must be refused (exit 3)
    score_labels = [[None] * len(lab) if c.get("expect_refusal") else lab for c, lab in zip(cases, recorded_labels)]
    mutants_data = json.load(open(a.mutants, encoding="utf-8"))
    mutants = mutants_data["mutants"]
    equiv = mutants_data.get("equivalent_not_counted", [])

    # ---- the tool and the pinned name-step module
    mimeglob_b = git_show(a.repo, a.rev, MIMEGLOB)
    if mimeglob_b is None:
        return setup(f"{MIMEGLOB} absent at {a.rev}")
    mimeglob_pin = sha(mimeglob_b) == a.expect_mimeglob_sha256
    if a.draft_tool:
        tool_b = open(a.draft_tool, "rb").read()
    else:
        tool_b = git_show(a.repo, a.rev, TOOL)
        if tool_b is None:
            return setup(f"{TOOL} absent at {a.rev}")
    tool_pin = sha(tool_b) == a.expect_tool_sha256 and mimeglob_pin
    src = tool_b.decode("utf-8", "surrogateescape")
    for m in (mutants if tool_pin else []):   # the mutants are anchored to the frozen bytes only
        if src.count(m["find"]) != 1:
            return setup(f"mutant {m['id']} find occurs {src.count(m['find'])} times")

    if a.check_only:
        print(f"MADO_MIMESNIFF_COUNT: CHECK_ONLY ok pred={PRED} "
              f"cases={len(cases)} mutants={len(mutants)} "
              f"tool_pin={'ok' if tool_pin else 'FAIL'} classes={len(CLASSES)}")
        return 0

    os.makedirs(a.scratch_root, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c1r95-", dir=a.scratch_root)
    global _ORACLE_BIN, _MG, EMPTY_PATH
    try:
        # ---- compile the oracle
        if shutil.which("cc") is None or shutil.which("pkg-config") is None:
            return setup("cc/pkg-config missing")
        _ORACLE_BIN = os.path.join(work, "oracle")
        cflags = subprocess.run(["pkg-config", "--cflags", "gio-2.0"],
                                capture_output=True, text=True).stdout.split()
        libs = subprocess.run(["pkg-config", "--libs", "gio-2.0"],
                              capture_output=True, text=True).stdout.split()
        rc = subprocess.run(["cc", "-O1", "-o", _ORACLE_BIN, a.oracle_src] + cflags + libs,
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

        # ---- place the tool and the pinned mimeglob in a fresh tools/ dir
        tdir = os.path.join(work, "tools")
        os.makedirs(tdir)
        tool_path = os.path.join(tdir, "mado-mimesniff.py")
        with open(tool_path, "wb") as fh:
            fh.write(tool_b)
        with open(os.path.join(tdir, "mado-mimeglob.py"), "wb") as fh:
            fh.write(mimeglob_b)
        _MG = load_mg(os.path.join(tdir, "mado-mimeglob.py"))
        EMPTY_PATH = tempfile.mkdtemp(prefix="emptypath-", dir=work)
        import sysconfig
        _RUN["launcher"] = os.path.join(work, "launcher.py")
        with open(_RUN["launcher"], "w", encoding="utf-8") as fh:
            fh.write(LAUNCHER_SRC)
        pyroots = sorted({os.path.realpath(p) for k, p in sysconfig.get_paths().items()
                          if k in ("stdlib", "platstdlib", "purelib", "platlib")})
        _RUN["allow"] = os.pathsep.join([os.path.realpath(work)] + pyroots)
        for k in ("main", "mutant", "base", "forgery"):
            _RUN["logs"][k] = os.path.join(work, f"audit-{k}.log")
            open(_RUN["logs"][k], "w").close()
        print("audit_allow=" + _RUN["allow"])

        # ---- real class: each mime.cache is update-mime-database's rebuild of the case's own packages/*.xml
        real_cases = [c for c in cases if c.get("class") == "real"]
        real_ok = 0
        for c in real_cases:
            caches = [r for r in c["files"] if r.endswith("/mime.cache")]
            okc = bool(caches)
            for r in caches:
                mdir = r[:-len("mime.cache")]
                pk = {k: v for k, v in c["files"].items() if k.startswith(mdir + "packages/") and k.endswith(".xml")}
                if not pk:
                    okc = False
                    break
                rb = tempfile.mkdtemp(prefix="realrb-", dir=work)
                for k, v in pk.items():
                    p = os.path.join(rb, k[len(mdir):])
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    with open(p, "wb") as fh:
                        fh.write(unb64(v))
                ur = subprocess.run(["update-mime-database", rb], capture_output=True,
                                    env={"PATH": "/usr/bin", "LC_ALL": "C"})
                got = open(os.path.join(rb, "mime.cache"), "rb").read() if ur.returncode == 0 else b""
                okc = okc and got == unb64(c["files"][r])
            real_ok += okc
        print(f"real_rebuild={real_ok}/{len(real_cases)}")

        # ---- class coverage of the frozen set
        per_class = {k: sum(1 for c in cases if c.get("class") == k) for k in CLASSES}
        classes_ok = sum(1 for k in CLASSES if per_class[k] >= MIN_PER_CLASS)
        print("per_class " + " ".join(f"{k}={per_class[k]}" for k in CLASSES))

        # ---- frozen leg: oracle drift check, then tool answers
        def oracle_label(c: dict):
            root = tempfile.mkdtemp(prefix="ocase-", dir=work)
            try:
                materialise(c, root)
                return oracle_label_case(oracle, c, root, root + ".odata")
            finally:
                shutil.rmtree(root, ignore_errors=True)
                shutil.rmtree(root + ".odata", ignore_errors=True)

        with ThreadPoolExecutor(a.workers) as ex:
            live = list(ex.map(oracle_label, cases))
        drift = [c["id"] for c, rec, liv in zip(cases, recorded_labels, live) if liv != rec]
        if drift:
            return setup("oracle_drift=" + ",".join(drift[:20]))

        oc = outcomes(tool_path, cases, score_labels, work, a.workers)
        res = [o == "ok" for o in oc]
        for c, o in zip(cases, oc):
            if o != "ok":
                print(f"case {c['id']} {o.upper()}")
        correct = sum(res)
        n = len(cases)

        # ---- static conjunct (vi)
        static_bad = static_check(tool_b)
        print("static_findings=" + (",".join(static_bad) or "none"))

        # ---- fresh leg
        seed = a.fresh_seed if a.fresh_seed is not None else int.from_bytes(os.urandom(4), "big")
        try:
            fcases, flabs = fresh_cases(a.fresh_gen, seed, a.fresh, work, oracle)
        except RuntimeError as e:
            return setup(f"fresh leg: {e}")
        foc = outcomes(tool_path, fcases, flabs, work, a.workers)
        fcorrect = sum(o == "ok" for o in foc)
        ftot = len(foc)
        for c, o in zip(fcases, foc):
            if o != "ok":
                print(f"fresh case {c.get('id', '?')} {o.upper()}")
        print(f"fresh seed={seed} cases={ftot} correct={fcorrect}")

        # ---- host leg
        host_paths = host_file_list(open(a.host_files, "rb").read())
        print(f"host files={len(host_paths)} env HOME={os.environ.get('HOME', '/')!r} "
              f"XDG_DATA_HOME={os.environ.get('XDG_DATA_HOME')!r} "
              f"XDG_DATA_DIRS={os.environ.get('XDG_DATA_DIRS')!r}")
        dirs = _MG.xdgmime_dirs(os.environ.get("XDG_DATA_HOME"), os.environ.get("HOME"),
                                os.environ.get("XDG_DATA_DIRS"))
        for d in dirs:
            for fn in ("mime.cache", "globs2"):
                p = d + fn
                if os.path.isfile(p):
                    print(f"host_db {p} sha256={sha_file(p)}")
        hcorrect, htot, hread = host_leg(tool_path, host_paths, work, a.workers)
        print(f"host readable={hread} pairs={htot} correct={hcorrect}")

        # ---- mutant leg
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
            mors = outcomes(mp, cases, score_labels, work, a.workers, audit="mutant")
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

        # ---- controls
        dn_correct = score_do_nothing(score_labels)
        print(f"control do_nothing correct={dn_correct}/{n}")
        no_correct = score_name_only(_MG, cases, score_labels, work, a.workers)
        print(f"control name_only correct={no_correct}/{n}")
        nv_correct = score_naive(_MG, cases, score_labels, work, a.workers)
        print(f"control naive correct={nv_correct}/{n}")
        memo_fresh = sum(1 for lab in flabs if lab and all(x == (UNKNOWN, 1) for x in lab))
        print(f"control memoriser frozen={n}/{n} fresh={memo_fresh}/{ftot}")
        fdir = os.path.join(work, "forgery")
        os.makedirs(fdir)
        fsrc = open(a.forgery, "rb").read()
        with open(os.path.join(fdir, "mado-mimesniff.py"), "wb") as fh:
            fh.write(fsrc)
        with open(os.path.join(fdir, "mado-mimeglob.py"), "wb") as fh:
            fh.write(mimeglob_b)
        forgery_static = static_check(fsrc)
        outcomes(os.path.join(fdir, "mado-mimesniff.py"), cases[:3], score_labels[:3], work, 1, audit="forgery")
        forgery_audit = sum(1 for _ in open(audit_log("forgery"), encoding="utf-8", errors="replace"))
        forgery_rejected = bool(forgery_static) and forgery_audit > 0
        print(f"control forgery static={','.join(forgery_static) or 'none'} audit_denials={forgery_audit} "
              f"rejected={forgery_rejected}")
        base_tool = git_show(a.repo, a.base_rev, TOOL)
        if base_tool is None:
            base_correct = 0
            print("base: tool absent at base-rev (answered=0)")
        else:
            bdir = os.path.join(work, "base")
            os.makedirs(bdir)
            bp = os.path.join(bdir, "mado-mimesniff.py")
            with open(bp, "wb") as fh:
                fh.write(base_tool)
            with open(os.path.join(bdir, "mado-mimeglob.py"), "wb") as fh:
                fh.write(mimeglob_b)
            boc = outcomes(bp, cases, score_labels, work, a.workers, audit="base")
            base_correct = sum(o == "ok" for o in boc)
            print(f"base: tool present, correct={base_correct}/{n}")
        audit_lines = open(audit_log("main"), encoding="utf-8", errors="replace").read().splitlines()
        for ln in audit_lines[:20]:
            print("audit " + ln)
        audit_main = len(audit_lines)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    vi_ok = not static_bad and audit_main == 0
    met = (tool_pin and correct == n and fcorrect == ftot and ftot >= MIN_FRESH
           and hcorrect == htot and htot > 0 and killed == len(mutants) and len(mutants) >= MIN_MUTANTS
           and classes_ok == len(CLASSES) and class_kills_ok == len(CLASSES)
           and real_ok == len(real_cases) and len(real_cases) > 0 and vi_ok
           and dn_correct < n and no_correct < n and nv_correct < n and base_correct < n
           and memo_fresh < ftot and forgery_rejected)
    word = ("DRAFT_" if draft else "") + ("TARGET_MET" if met else "TARGET_MISSED")
    print(f"MADO_MIMESNIFF_COUNT: {word} pred={PRED} "
          f"rev={'draft:' + a.draft_tool if draft else a.rev} "
          f"tool_pin={'ok' if tool_pin else 'FAIL'} cases={n} correct={correct} "
          f"classes={classes_ok}/{len(CLASSES)} fresh={fcorrect}/{ftot} host={hcorrect}/{htot} "
          f"mutants={len(mutants)} killed={killed} crashed_not_killed={crashed} "
          f"class_kills={class_kills_ok}/{len(CLASSES)} real_rebuild={real_ok}/{len(real_cases)} "
          f"static_no_external_resolver={'ok' if vi_ok else 'FAIL'} audit_denials={audit_main} "
          f"controls do_nothing={dn_correct} name_only={no_correct} naive={nv_correct} base={base_correct} "
          f"memoriser_fresh={memo_fresh}/{ftot} forgery={'rejected' if forgery_rejected else 'ACCEPTED'} "
          f"oracle_sha256={oracle_sha} tool_sha256={sha(tool_b)} mimeglob_sha256={sha(mimeglob_b)}")
    if draft:
        return 3
    return 0 if met else 1



if __name__ == "__main__":
    sys.exit(main())
