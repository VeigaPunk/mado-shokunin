#!/usr/bin/env python3
"""Round-98 C1 counter - the launch-argv surface: the sequence of argv vectors GIO 2.90.1 builds
from a desktop entry's Exec key and the file/URI arguments handed to `gio launch`
(expand_application_parameters gdesktopappinfo.c:2700-2750, expand_macro :2580-2700,
expand_macro_single :2507-2555, expand_macro_uri :2557-2578, then g_shell_parse_argv gshell.c).

Frozen predicate PRED-C1-r98-v1 (verbatim from the declaration; the same sentence is the receipt label):
  TARGET_MET iff, at --rev, tools/mado-execargv.py is the frozen candidate
  (tool_sha256 == --expect-tool-sha256, printed tool_pin=ok) and, run under an empty PATH through
  the audit launcher with the structural allowlist (no process, socket, network or non-libc dynamic
  import; no sibling lane module), it answers (i) every frozen case exactly (correct == cases) over
  the declared 20 classes (classes == 20/20, each class >=3 cases, >=70 cases total); (ii) every
  frozen mutant killed (killed == mutants) and every class kills at least one mutant
  (class_kills == 20/20); (iii) every fresh seeded case exactly (fresh == fresh_total, >=40,
  fixtures generated at measurement time by a frozen generator, labels from the same oracle);
  (iv) the oracle is the installed gio (--expect-gio-sha256) and every frozen label was produced
  by this binary at the freeze; (v) the controls stay behind: the naive space-split model scores
  fewer than the total, the no-expansion model fewer, and the memoriser scores 0 on the fresh leg;
  and (vi) the candidate's --selftest is green (checks=N failed=0, N >= 12).
  rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR.

Rulings absorbed mid-wave (L1 + sibling seats, all binding):
  - Declaration rule 7 (launch order unobservable): the compared plane is the launch COUNT and
    the MULTISET of argv vectors - the counter sorts both sides before comparing; the tool prints
    model order.  Frozen and fresh expects are pre-sorted by their producers; the counter's
    multiset compare is order-insensitive either way.
  - The oracle renderer controls/execargv-probe-r98.py is normative: desktop file
    <root>/case.desktop; desktop values written LITERALLY (the case string is already the
    post-GKeyFile-unescape bytes; an optional "desktop_raw" case key replaces the whole file
    after substitution); {probe}/{root} substituted in every desktop value and every arg (in ARGS
    the {probe} placeholder substitutes to the EMPTY string, per gio_argv); key order
    Type/Name/Icon/Exec/Path/Terminal/Hidden; None keys omitted; bools true/false; LF; trailing
    newline.  Frozen expects carry NO absolute paths: canonical "{probe}"/"{root}" tokens; the
    counter reverses the substitution onto its measure-time root ("{probe}" first, then "{root}").
  - Scoring runs the candidate with --json (the lossless projection; raw newlines in argv values
    cannot survive the text grammar).  A refusal is {"error": cause} with cause in
    {no-exec, desktop-file, exec-parse} and rc 2.
  - The cases envelope carries renderer_sha256 (the oracle renderer's sha256); the counter
    requires it (64-hex) and, when the renderer file execargv-probe-r98.py sits next to the cases
    file, verifies the pin against it (SETUP_ERROR on mismatch; renderer_pin=skip when absent).
  - Fresh cases carry class "fresh" (id "fresh-<seed>-NN"); the fresh generator emits JSONL case
    dicts to --out (roots materialise transiently and are removed; the counter rebuilds every
    root itself), a "FRESH_GEN: cases=N ok=A refused=B" summary and a "FRESH_GEN_PIN:
    gio_sha256=..." line on stdout; the counter requires the pinned gio sha256 on a
    FRESH_GEN_PIN line and cross-checks the summary count.

Counter note on the structural clause: the candidate has NO sibling imports (contract 1), so the
static conjunct is a category deny - every import must resolve to a stdlib module
(sys.stdlib_module_names) and the top level must not be a process/socket/network/dynamic-import
module; dynamic-load attributes (spec_from_file_location, exec_module, import_module, ...) and the
name/attr/os-spawn checks are flagged as well.  The audit launcher is the round-95/97 one with one
change: socket.__new__ is denied for EVERY family (this surface has no AF_UNIX fixture, unlike
r97's filetype).  No process spawn, no network, no non-libc dlopen.

Inputs (all sha256-pinned by --expect-*-sha256; SETUP_ERROR on any mismatch):
  --cases    {"version":1,"oracle":"gio launch + probe child argv","gio_sha256":<pin>,
             "glib2":"2.90.1-1","renderer_sha256":<pin>,"classes":[the 20 names in order],
             "cases":[...]}
             case: {"id","class","desktop":{"Name","Icon"|null,"Type","Exec","Path"|null,
                    "Terminal"|null,"Hidden"|null}[,"desktop_raw":"<whole file>"],
                    "args":[{"kind":"file","path":"<rel>"}|{"kind":"uri","uri":"<abs uri>"}],
                    "files":{"<rel>":"<b64>"},
                    "expect":{"launches":N,"argv":[[...],...]} | {"error":"<cause>"}}
             desktop values may be null (the key is then omitted; a null Exec/Type is the measured
             no-exec / desktop-file refusal).  files keys ending "/" are directories; ".." and
             absolute members are rejected.  expect.argv vectors carry argv[0] and the canonical
             {probe}/{root} tokens; the counter substitutes its measure-time root before comparing.
             A refusal case carries {"error": cause} with cause in {no-exec, desktop-file,
             exec-parse} and the tool must exit 2.  The census minimums (>=3 per class, >=70 total,
             >=40 fresh) are VERDICT atoms on the TARGET_MISSED line, not setup gates.
  --mutants  {"version":1,"tool":"tools/mado-execargv.py","candidate_sha256":<pin>,"classes":[...],
             "mutants":[{"id","find","replace","class","expect":"kill"}], "not_observable":[...],
             "equivalents":[...]}; find occurs exactly once in the candidate's non-selftest prefix
             (cut at the first "def selftest(", QUALITY 167), is unique across all three lists,
             class in the 20, id starts "<class>-".  A kill is a parsed wrong answer or a missing
             answer over the frozen cases; a crashing mutant is crashed_not_killed, never a kill.
  --genseed  the frozen fresh-case generator; called inside the counter at measurement time as
             `python3 -I <genseed> --seed HEX --dir D --out F --count 60` (all four flags required;
             its PATH starts /usr/bin so its gio run resolves to the pinned oracle binary).  The
             generator materialises each case root transiently under --dir for its own gio
             measurement and removes it; the JSONL case dicts (with canonical expects) go to --out.
             The counter validates every case and rebuilds every root itself under --scratch-root
             (inside the audit allowlist) before scoring.  The seed is drawn at measurement
             (os.urandom hex, or the MADO_R98_FRESH_SEED environment override for a reproducible
             run) and printed fresh_seed=...

Legs: frozen (candidate under the launcher, one invocation per case, --json parsed, multiset
compare, one MISMATCH <id> expected=... got=... line per miss), fresh, mutant, selftest
(MADO_EXECARGV_SELFTEST: checks=N failed=0, N>=12, rc 0), controls: the THREE DISTINCT models of
the amended predicate (v) - the naive Exec.split() with no field-code expansion and the
field-code model that expands the consuming codes but ignores quoting and iteration (both
embedded <=30-line scripts written by this counter, run through the same launcher and parser as
the candidate) - each strictly fewer than the total on the frozen cases, and the memoriser (frozen
expect keyed by case id; 0 required on fresh).  audit_denials counts candidate-run denials and
must be 0.  Stdlib only in this counter; the counter never writes the lane.  ASCII only.

Counter --selftest (contract 4): `python3 -I <this file> --selftest [--scratch-root DIR]` builds a
mini universe (a two-commit fixture git repo holding a mini candidate, mini frozen/fresh cases,
mini mutant files and a mini generator - all synthesised at selftest time under a temp dir because
this seat's write scope names no committed fixture path) and asserts >=10 stable check ids,
printing MADO_COUNTER_SELFTEST_FAIL: <id> per failing check and
MADO_COUNTER_SELFTEST: checks=N failed=M; exit 0 green / 1 failed / 2 could-not-evaluate.
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
import sysconfig
import tempfile
from concurrent.futures import ThreadPoolExecutor

PRED = "PRED-C1-r98-v1"
PREFIX = "MADO_EXECARGV_COUNT:"
CLASSES = ("plain", "f", "F", "u-file", "u-uri", "u-anchor", "U-mixed", "d", "n", "i", "c", "k",
           "pct", "bad", "nonlocal", "nofuse", "multilaunch", "comment", "quote", "path")
MIN_PER_CLASS = 3
MIN_CASES = 70           # 20 classes x >=3 (amended declaration: >=70 cases total)
MIN_FRESH_CASES = 40
MIN_SELFTEST_CHECKS = 12
TOOL = "tools/mado-execargv.py"
TOOL_NAME = "mado-execargv.py"
RENDERER_NAME = "execargv-probe-r98.py"
GLIB = "2.90.1-1"
GIO = "/usr/bin/gio"
ORACLE_NAME = "gio launch + probe child argv records"
ERROR_CAUSES = ("no-exec", "desktop-file", "exec-parse")
DESKTOP_KEYS = ("Type", "Name", "Icon", "Exec", "Path", "Terminal", "Hidden", "X-GIO-NoFuse")
DESKTOP_FILE = "case.desktop"
PROBE_FILE = "probe.sh"
TOOL_TIMEOUT = 30.0
FRESH_RUN_TIMEOUT = 900.0
FRESH_COUNT = "60"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")

# ---------------------------------------------------------------- small helpers

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: str) -> str:
    with open(p, "rb") as fh:
        return sha(fh.read())


def git_show(repo: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def unb64(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))


def _rel_ok(rel: str) -> bool:
    if not rel or rel.startswith("/") or "\x00" in rel:
        return False
    body = rel.rstrip("/")
    if not body:
        return rel.endswith("/")
    return not any(p in ("..", "") for p in body.split("/"))


def _subst(text: str, root: str, probe: str) -> str:
    """{probe}/{root} substitution, in the oracle's order: {probe} first, then {root}."""
    return str(text).replace("{probe}", probe).replace("{root}", root)


# ---------------------------------------------------------------- case materialisation

# The probe child, byte-identical to the oracle renderer's PROBE_SH (controls/execargv-probe-r98.py):
# one record per spawn under a lock, "@@@ <argc>" / "P0=$0" / "A<i>=<value>" into $0.out.<seq>.
# The counter never runs the probe (the candidate is a model); the script is written only so the
# {probe} substitution has a real path and the canonical expects reverse onto it.
PROBE_SRC = r'''#!/bin/sh
# mado r98 launch probe: write one argv record per spawn to $0.out.<seq>.
# Sequence numbers are taken under a lock, so file order is spawn order.
exec 9>"$0.lock"; flock 9; n=$(cat "$0.seq" 2>/dev/null || echo 0); n=$((n+1)); echo "$n" > "$0.seq"; flock -u 9
{ printf '@@@ %s\n' "$#"; printf 'P0=%s\n' "$0"; i=1; for a in "$@"; do printf 'A%d=%s\n' "$i" "$a"; i=$((i+1)); done; } > "$0.out.$n"
'''


def write_desktop(path: str, desktop: dict, root: str, probe: str) -> None:
    """Serialise the case's desktop dict to [Desktop Entry] key=value lines, LITERAL values (the
    oracle renderer writes the case string as-is: it is already the post-GKeyFile-unescape bytes).
    Key order Type/Name/Icon/Exec/Path/Terminal/Hidden; None keys omitted; bools print
    true/false; {probe}/{root} substituted in every value; LF; trailing newline."""
    lines = ["[Desktop Entry]"]
    for key in DESKTOP_KEYS:
        v = desktop.get(key)
        if v is None:
            continue
        if isinstance(v, bool):
            v = "true" if v else "false"
        else:
            v = str(v)
        lines.append(f"{key}={_subst(v, root, probe)}")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


def resolve_arg_string(arg: dict, root: str) -> str:
    """One case arg to the string the tool (and the oracle's gio launch) receives.  The oracle's
    gio_argv substitutes {probe}/{root} with the probe placeholder EMPTY in args; a file arg is
    os.path.join(root, path) (an absolute substituted path wins); a uri arg is verbatim."""
    if arg.get("kind") == "file":
        p = _subst(str(arg.get("path", "")), root, "")
        return os.path.join(root, p)
    if arg.get("kind") == "uri":
        return _subst(str(arg.get("uri", "")), root, "")
    raise CaseError(f"unknown arg kind {arg.get('kind')!r}")


class CaseError(Exception):
    pass


def materialise_case(case: dict, root: str) -> tuple[str, list[str]]:
    """Build the case tree under root; return (desktop path, tool argv tail).  Files come from the
    base64 map (keys ending '/' are directories); probe.sh is written 0755; the desktop file is
    case.desktop (or the case's desktop_raw whole-file bytes after substitution, None ignored);
    an empty h/ HOME dir is created for fidelity with the freeze env."""
    os.makedirs(root, exist_ok=True)
    os.makedirs(os.path.join(root, "h"), exist_ok=True)
    for rel, b64 in case.get("files", {}).items():
        p = os.path.join(root, rel)
        parent = os.path.dirname(p.rstrip("/"))
        if parent:
            os.makedirs(parent, exist_ok=True)
        if rel.endswith("/"):
            os.makedirs(p, exist_ok=True)
        else:
            with open(p, "wb") as fh:
                fh.write(unb64(b64))
    probe = os.path.join(root, PROBE_FILE)
    with open(probe, "w", encoding="ascii", newline="\n") as fh:
        fh.write(PROBE_SRC)
    os.chmod(probe, 0o755)
    desktop_path = os.path.join(root, DESKTOP_FILE)
    raw = case.get("desktop_raw")
    if raw is not None:
        with open(desktop_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(_subst(str(raw), root, probe))
    else:
        write_desktop(desktop_path, case["desktop"], root, probe)
    argv = [resolve_arg_string(a, root) for a in case.get("args", [])]
    # every file arg must stay under the case root (validation already refused escapes; re-check
    # the resolved form so a lexical escape cannot reach outside)
    for a, s in zip(case.get("args", []), argv):
        if a.get("kind") == "file":
            rp = os.path.realpath(s)
            rr = os.path.realpath(root)
            if rp != rr and not rp.startswith(rr + os.sep):
                raise CaseError(f"file arg {s!r} escapes the case root")
    return desktop_path, argv


# ---------------------------------------------------------------- expect normalisation

def normalise_expect(expect: dict, measure_root: str) -> dict:
    """The expect with the canonical {probe}/{root} tokens rewritten onto the measure-time root
    ({probe} first, then {root}, the oracle's reverse order).  Refusal expects pass through.
    Comparison is a MULTISET (declaration rule 7: launch order is unobservable) - the caller
    sorts both sides."""
    if "error" in expect:
        return {"error": expect.get("error")}
    probe = os.path.join(measure_root, PROBE_FILE)
    argv = [[s.replace("{probe}", probe).replace("{root}", measure_root)
             if isinstance(s, str) else s for s in vec] for vec in expect["argv"]]
    return {"launches": expect.get("launches"), "argv": argv}


def _short(obj, limit: int = 480) -> str:
    s = json.dumps(obj, sort_keys=True, ensure_ascii=True)
    return s if len(s) <= limit else s[:limit - 3] + "..."


# ---------------------------------------------------------------- the audit launcher (every tool run)

LAUNCHER_SRC = r'''import os, socket, sys
_log = os.open(sys.argv[1], os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
_allow = [os.path.realpath(p) for p in sys.argv[2].split(os.pathsep) if p] + ["/dev/null"]
_tool = sys.argv[3]
sys.argv = [_tool] + sys.argv[4:]
_SPAWN_OK = {"ldconfig"}
_BUSY = [False]


def _deny(ev, arg):
    os.write(_log, ("AUDIT_DENY %s %r\n" % (ev, arg)).encode("utf-8", "backslashreplace"))
    os._exit(97)


def _hook(ev, args):
    if _BUSY[0]:
        return
    _BUSY[0] = True
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
        elif ev in ("os.system", "os.exec", "os.spawn", "os.fork", "os.forkpty", "pty.spawn",
                    "socket.connect", "socket.connect_ex", "urllib.Request", "http.client.connect"):
            _deny(ev, args[:1])
        elif ev == "socket.__new__":
            # this candidate has no socket surface at all: every family is denied (r97 admitted
            # AF_UNIX for its filetype fixtures; execargv has none)
            _deny(ev, args[:2])
        elif ev == "ctypes.dlopen":
            if args[0] is None:
                return
            if not os.path.basename(os.fsdecode(args[0])).startswith("libc.so"):
                _deny(ev, args[0])
    finally:
        _BUSY[0] = False


sys.addaudithook(_hook)
import runpy  # noqa: E402
runpy.run_path(_tool, run_name="__main__")
'''
_RUN = {"launcher": "", "allow": "", "logs": {}, "emptypath": ""}


def audit_log(kind: str) -> str:
    return _RUN["logs"][kind]


# ---------------------------------------------------------------- tool runs and scoring

def parse_tool_output(stdout: str) -> dict:
    """One of {"kind":"answer","launches":N,"argv":[[...],...]} | {"kind":"error","cause":C} |
    {"kind":"malformed"}.  Scoring uses --json (lossless: raw newlines in argv values cannot
    survive the text grammar); the object must be the only output.  A missing or malformed answer
    is "malformed" (a scored wrong answer, never a crash)."""
    text = stdout.strip()
    if not text:
        return {"kind": "malformed"}
    try:
        obj = json.loads(text)
    except Exception:
        return {"kind": "malformed"}
    if not isinstance(obj, dict):
        return {"kind": "malformed"}
    if "error" in obj:
        cause = obj.get("error")
        if isinstance(cause, str) and cause:
            return {"kind": "error", "cause": cause}
        return {"kind": "malformed"}
    launches = obj.get("launches")
    argv = obj.get("argv")
    if not isinstance(launches, int) or launches < 0 or not isinstance(argv, list) \
            or len(argv) != launches:
        return {"kind": "malformed"}
    for vec in argv:
        if not isinstance(vec, list) or not all(isinstance(x, str) for x in vec):
            return {"kind": "malformed"}
    return {"kind": "answer", "launches": launches, "argv": argv}


def run_tool(tool_path: str, tool_args: list[str], cwd: str, timeout: float = TOOL_TIMEOUT,
             audit: str = "main", allow: str | None = None, home: str | None = None
             ) -> tuple[str, str, int]:
    """("ok", stdout, rc) | ("crash", "", rc).  Only rc 0 and the refusal rc 2 are parseable output;
    anything else (97 audit denial, a mutant's traceback rc 1, timeout) is a crash.  Every run
    carries --json (the lossless answer projection)."""
    argv = [sys.executable, "-I", _RUN["launcher"], audit_log(audit), allow or _RUN["allow"],
            tool_path] + list(tool_args) + ["--json"]
    env = {"PATH": _RUN["emptypath"], "TMPDIR": cwd, "LC_ALL": "C"}
    if home is not None:
        env["HOME"] = home
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, cwd=cwd,
                           env=env)
    except (OSError, subprocess.TimeoutExpired):
        return "crash", "", -1
    if r.returncode not in (0, 2):
        return "crash", "", r.returncode
    return "ok", r.stdout, r.returncode


def score_case(tool_path: str, case: dict, root: str, audit: str = "main"
               ) -> tuple[str, dict | None]:
    """('ok'|'wrong'|'crash', detail).  A refusal expect needs rc 2 and the exact ERROR cause; an
    argv expect needs rc 0 and the exact launches + the same MULTISET of argv vectors (declaration
    rule 7: launch order is unobservable, so both sides are sorted before comparison).  Material-
    isation failures are crashes; parse mismatches are wrong with a detail dict for the MISMATCH
    line; a nonzero/non-2 rc or timeout is a crash."""
    try:
        desktop_path, tail = materialise_case(case, root)
        norm = normalise_expect(case["expect"], root)
    except Exception:
        return "crash", None
    try:
        status, out, rc = run_tool(tool_path, [desktop_path] + tail, root, audit=audit,
                                   home=os.path.join(root, "h"))
    except Exception:
        return "crash", None
    if status == "crash":
        return "crash", {"expected": norm, "got": {"rc": rc}}
    parsed = parse_tool_output(out)
    exp = case["expect"]
    if "error" in exp:
        if rc == 2 and parsed.get("kind") == "error" and parsed.get("cause") == exp["error"]:
            return "ok", None
        return "wrong", {"expected": norm,
                         "got": {"rc": rc, "kind": parsed.get("kind"),
                                 "cause": parsed.get("cause")}}
    if rc != 0 or parsed.get("kind") != "answer":
        return "wrong", {"expected": norm,
                         "got": {"rc": rc, "kind": parsed.get("kind"),
                                 "cause": parsed.get("cause")}}
    if parsed.get("launches") != norm.get("launches"):
        return "wrong", {"expected": norm,
                         "got": {"rc": rc, "kind": "answer", "launches": parsed.get("launches"),
                                 "argv": parsed.get("argv")}}
    if sorted(parsed.get("argv", [])) != sorted(norm.get("argv", [])):
        return "wrong", {"expected": norm,
                         "got": {"rc": rc, "kind": "answer", "launches": parsed.get("launches"),
                                 "argv": parsed.get("argv")}}
    return "ok", None


def run_cases(tool_path: str, cases: list[dict], work: str, jobs: int, audit: str = "main",
              prefix: str = "case-") -> list[tuple[str, dict | None]]:
    def one(c: dict) -> tuple[str, dict | None]:
        safe = re.sub(r"[^A-Za-z0-9_.-]", "_", str(c.get("id", "case")))[:80]
        root = tempfile.mkdtemp(prefix=safe + "-", dir=work)
        try:
            return score_case(tool_path, c, root, audit)
        finally:
            shutil.rmtree(root, ignore_errors=True)
    with ThreadPoolExecutor(jobs) as ex:
        return list(ex.map(one, cases))


# ---------------------------------------------------------------- validation

def validate_case(c: dict, fresh: bool) -> tuple[str, str] | None:
    """Contract-2 rules for one case; None = ok, else (setup_id, detail).  Shared by the frozen and
    fresh sets (fresh cases carry class "fresh").  expect is either {"error": <cause>} or
    {"launches": N, "argv": [[...], ...]} with launches == len(argv) >= 1 and every vector a
    non-empty list of strings.  Desktop Type/Name/Exec may be null (the oracle measures the
    resulting refusal); Icon/Path str|null, Terminal/Hidden bool|null."""
    cid = c.get("id", "?")
    cls = c.get("class")
    if fresh and cls is None:
        cls = "fresh"   # the generator's JSONL carries no class key; fresh cases are class "fresh"
    allowed = CLASSES if not fresh else CLASSES + ("fresh",)
    if cls not in allowed:
        return (f"setup-case-{cid}-class", f"class {cls!r} not in the allowed set")
    if not isinstance(cid, str) or not cid.startswith(cls + "-"):
        return (f"setup-case-{cid}-id", f"id {cid!r} does not start with '{cls}-'")
    desktop = c.get("desktop")
    if not isinstance(desktop, dict):
        return (f"setup-case-{cid}-desktop", "desktop is not an object")
    extra = set(desktop) - set(DESKTOP_KEYS)
    if extra:
        return (f"setup-case-{cid}-desktop", f"desktop keys outside the contract: {sorted(extra)}")
    for k in ("Type", "Name", "Icon", "Path", "Exec"):
        v = desktop.get(k)
        if v is not None and not isinstance(v, str):
            return (f"setup-case-{cid}-desktop", f"{k} {v!r} is not a string or null")
    for k in ("Terminal", "Hidden"):
        v = desktop.get(k)
        if v is not None and not isinstance(v, bool):
            return (f"setup-case-{cid}-desktop", f"{k} {v!r} is not a bool or null")
    v = desktop.get("X-GIO-NoFuse")
    if v is not None and not isinstance(v, (str, bool)):
        return (f"setup-case-{cid}-desktop", f"X-GIO-NoFuse {v!r} is not a string/bool or null")
    if c.get("desktop_raw") is not None and not isinstance(c["desktop_raw"], str):
        return (f"setup-case-{cid}-desktop", "desktop_raw is not a string or null")
    args = c.get("args")
    if not isinstance(args, list):
        return (f"setup-case-{cid}-args", "args is not a list")
    for i, a in enumerate(args):
        if not isinstance(a, dict) or a.get("kind") not in ("file", "uri"):
            return (f"setup-case-{cid}-args", f"arg {i} malformed")
        if a["kind"] == "file":
            p = a.get("path")
            if not isinstance(p, str) or not p:
                return (f"setup-case-{cid}-args", f"file arg {i} path empty")
            body = p.replace("{root}", "R").replace("{probe}", "P")
            if body.startswith("/") and not (p.startswith("{root}") or p.startswith("{probe}")):
                return (f"setup-case-{cid}-args", f"file arg {i} path {p!r} is absolute")
            if any(part in ("..", "") for part in body.strip("/").split("/")):
                return (f"setup-case-{cid}-args", f"file arg {i} path {p!r} escapes")
        else:
            if not isinstance(a.get("uri"), str) or not a["uri"]:
                return (f"setup-case-{cid}-args", f"uri arg {i} empty")
    files = c.get("files", {})
    if not isinstance(files, dict):
        return (f"setup-case-{cid}-files", "files is not an object")
    for rel, b64 in files.items():
        if not isinstance(rel, str) or not _rel_ok(rel):
            return (f"setup-case-{cid}-escape", f"files member {rel!r} escapes the case root")
        if not rel.endswith("/"):
            try:
                unb64(b64)
            except Exception:
                return (f"setup-case-{cid}-b64", f"files member {rel!r} is not base64")
    exp = c.get("expect")
    if not isinstance(exp, dict):
        return (f"setup-case-{cid}-expect", "expect is not an object")
    if "error" in exp:
        if exp.get("error") not in ERROR_CAUSES:
            return (f"setup-case-{cid}-expect",
                    f"error cause {exp.get('error')!r} not in {ERROR_CAUSES}")
        if "argv" in exp or "launches" in exp:
            return (f"setup-case-{cid}-expect", "expect mixes error and argv shapes")
    else:
        launches = exp.get("launches")
        argv = exp.get("argv")
        if not isinstance(launches, int) or launches < 1:
            return (f"setup-case-{cid}-expect", f"launches {launches!r} < 1")
        if not isinstance(argv, list) or len(argv) != launches:
            return (f"setup-case-{cid}-expect", "argv length != launches")
        for vec in argv:
            if not isinstance(vec, list) or not vec or not all(isinstance(x, str) for x in vec):
                return (f"setup-case-{cid}-expect", "argv vector is not a non-empty string list")
    return None


def validate_cases(data: dict, expect_gio_sha: str) -> list[tuple[str, str]]:
    """Envelope + per-case schema (SETUP_ERROR).  The census minimums are score atoms, not schema.
    renderer_sha256 (the oracle renderer's pin, carried in the header) is required 64-hex."""
    errs: list[tuple[str, str]] = []
    if data.get("version") != 1:
        errs.append(("setup-envelope-version", f"version {data.get('version')!r} != 1"))
    if data.get("oracle") != ORACLE_NAME:
        errs.append(("setup-envelope-oracle", f"oracle {data.get('oracle')!r} != {ORACLE_NAME!r}"))
    if data.get("gio_sha256") != expect_gio_sha:
        errs.append(("setup-envelope-gio", "case file gio_sha256 != --expect-gio-sha256 (labels "
                                           "came from another binary)"))
    if data.get("glib2") != GLIB:
        errs.append(("setup-envelope-glib2", f"glib2 {data.get('glib2')!r} != {GLIB}"))
    rs = data.get("renderer_sha256")
    if not isinstance(rs, str) or not HEX64.match(rs):
        errs.append(("setup-envelope-renderer",
                     f"renderer_sha256 {rs!r} is not 64 lowercase hex"))
    if data.get("classes") != list(CLASSES):
        errs.append(("setup-envelope-classes", "classes != the frozen 20 in declaration order"))
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errs.append(("setup-envelope-cases",
                     f"{len(cases) if isinstance(cases, list) else '?'} cases, need a non-empty list"))
        return errs
    for c in cases:
        e = validate_case(c, fresh=False)
        if e is not None:
            errs.append(e)
        if len(errs) > 20:
            errs.append(("setup-envelope-many", "...more"))
            return errs
    return errs


def validate_mutants(data: dict, prefix_src: str) -> list[tuple[str, str]]:
    """Mutant file schema + anchor checks against the candidate's non-selftest prefix.  Counted
    mutants carry expect=="kill"; finds are unique across all three lists (mutants,
    not_observable, equivalents); candidate_sha256/classes are checked by the caller."""
    errs: list[tuple[str, str]] = []
    if "version" in data and data.get("version") != 1:
        errs.append(("setup-mutants-version", f"version {data.get('version')!r} != 1"))
    if "tool" in data and data.get("tool") != TOOL:
        errs.append(("setup-mutants-tool", f"tool {data.get('tool')!r} != {TOOL}"))
    muts = data.get("mutants")
    if not isinstance(muts, list) or not muts:
        errs.append(("setup-mutants-empty", "no mutants"))
        return errs
    all_finds: list[str] = []
    for key in ("mutants", "not_observable", "equivalents"):
        lst = data.get(key, [])
        if not isinstance(lst, list):
            errs.append(("setup-mutants-list", f"{key} is not a list"))
            continue
        for m in lst:
            f = m.get("find") if isinstance(m, dict) else None
            if isinstance(f, str) and f:
                all_finds.append(f)
    if len(all_finds) != len(set(all_finds)):
        errs.append(("setup-mutants-anchor", "a find anchor is duplicated across mutant lists"))
    seen_ids: set[str] = set()
    seen_finds: set[str] = set()
    for m in muts:
        mid = m.get("id", "?")
        cls = m.get("class")
        find = m.get("find")
        rep = m.get("replace")
        if cls not in CLASSES:
            errs.append(("setup-mutants-class", f"mutant {mid}: class {cls!r} not in the frozen 20"))
            continue
        if not isinstance(mid, str) or not mid.startswith(cls + "-"):
            errs.append(("setup-mutants-id", f"mutant {mid}: id does not start with '{cls}-'"))
        if mid in seen_ids:
            errs.append(("setup-mutants-id", f"mutant id {mid} duplicated"))
        seen_ids.add(mid)
        if m.get("expect") != "kill":
            errs.append(("setup-mutants-expect", f"mutant {mid}: expect {m.get('expect')!r} != 'kill'"))
        if not isinstance(find, str) or not find or not isinstance(rep, str) or find == rep:
            errs.append(("setup-mutants-anchor", f"mutant {mid}: empty find/replace or find==replace"))
            continue
        n = prefix_src.count(find)
        if n != 1:
            errs.append(("setup-mutants-anchor",
                         f"mutant {mid}: find occurs {n} times in the non-selftest code"))
        if find in seen_finds:
            errs.append(("setup-mutants-anchor", f"mutant {mid}: find duplicated across mutants"))
        seen_finds.add(find)
        if len(errs) > 20:
            errs.append(("setup-mutants-many", "...more"))
            return errs
    return errs


def non_selftest_prefix(src: str) -> str:
    """The candidate bytes before its selftest block (QUALITY 167: the selftest sits after the
    production path; mutant anchors live in the prefix)."""
    i = src.find("def selftest(")
    return src if i < 0 else src[:i]


# ---------------------------------------------------------------- structural conjunct (static)

_BAD_OS = re.compile(r"^(system|popen|exec\w*|spawn\w*|posix_spawn\w*|fork\w*)$")
_BAD_NAMES = {"eval", "exec", "compile", "__import__", "getattr", "setattr", "delattr", "vars",
              "globals", "locals", "breakpoint", "import_module", "reload"}
# dynamic-load / interpreter-mutating attributes: the candidate has no sibling module and no
# dynamic import need, so any of these is a structural finding
_BAD_ATTRS = {"spec_from_file_location", "module_from_spec", "exec_module", "SourceFileLoader",
              "spec_from_loader", "SourceLoader", "import_module", "reload", "__import__",
              "run_path", "run_module"}
# process / socket / network / dynamic-import top-level modules: the structural allowlist's deny
# side.  Everything else must resolve to a stdlib module (sys.stdlib_module_names); a non-stdlib
# import is a sibling-lane or third-party module and is flagged.
_DENY_TOP = {"subprocess", "socket", "ctypes", "urllib", "http", "ftplib", "smtplib", "poplib",
             "imaplib", "nntplib", "telnetlib", "xmlrpc", "ssl", "webbrowser", "multiprocessing",
             "concurrent", "asyncio", "threading", "pty", "signal", "mmap", "readline", "curses",
             "tkinter", "ensurepip", "venv", "pip", "setuptools", "distutils", "runpy",
             "zipimport", "antigravity", "socketserver", "requests", "aiohttp"}
_STDLIB = set(getattr(sys, "stdlib_module_names", ()))


def static_check(src: bytes) -> list[str]:
    """Findings that make static_structural FAIL (empty list = ok): every import resolves to a
    stdlib top level outside the process/socket/network/dynamic deny set; from-imports only from
    __future__ or a stdlib module; no dynamic-load attributes; no eval/exec/compile/getattr family;
    no dunder attribute access; no os.system/popen/exec*/spawn*/fork*."""
    import ast
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [f"syntax:{e.lineno}"]
    bad: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                top = al.name.split(".", 1)[0]
                if top in _DENY_TOP:
                    bad.append(f"import:{al.name}:{node.lineno}")
                elif _STDLIB and top not in _STDLIB:
                    bad.append(f"import-nonstdlib:{al.name}:{node.lineno}")
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            top = mod.split(".", 1)[0]
            if mod != "__future__":
                if top in _DENY_TOP:
                    bad.append(f"import-from:{mod}:{node.lineno}")
                elif _STDLIB and top not in _STDLIB:
                    bad.append(f"import-from-nonstdlib:{mod}:{node.lineno}")
        elif isinstance(node, ast.Name) and node.id in _BAD_NAMES:
            bad.append(f"name:{node.id}:{node.lineno}")
        elif isinstance(node, ast.Attribute):
            if node.attr.startswith("__") and node.attr.endswith("__"):
                bad.append(f"dunder:.{node.attr}:{node.lineno}")
            if node.attr in _BAD_ATTRS or (node.attr in _BAD_NAMES and node.attr != "compile"):
                # "compile" as an attribute is legitimate (re.compile); the builtin needs eval/exec
                # to matter, and both stay flagged.  Bare compile( is caught by the Name branch.
                bad.append(f"attr:{node.attr}:{node.lineno}")
            if isinstance(node.value, ast.Name) and node.value.id == "os" \
                    and _BAD_OS.match(node.attr):
                bad.append(f"os.{node.attr}:{node.lineno}")
    return bad


# ---------------------------------------------------------------- controls

# The naive space-split model (<=30 lines): Exec.split(), one launch, field codes literal, no
# quoting, no GKeyFile unescape, no iteration.  Written by this counter; run through the launcher.
NAIVE_SRC = r'''import json, sys

def main():
    av = sys.argv[1:]
    js = "--json" in av
    av = [x for x in av if x != "--json"]
    data = open(av[0], "rb").read().decode("utf-8", "surrogateescape")
    ex = None
    for line in data.splitlines():
        if line.startswith("Exec="):
            ex = line[5:]
            break
    if ex is None:
        if js:
            sys.stdout.write(json.dumps({"error": "no-exec", "detail": "naive"}) + "\n")
        else:
            sys.stdout.write("MADO_EXECARGV: ERROR no-exec detail=naive\n")
        return 2
    toks = ex.split()
    if js:
        sys.stdout.write(json.dumps({"launches": 1, "argv": [toks]}) + "\n")
    else:
        sys.stdout.write("MADO_EXECARGV: launches=1\nLAUNCH 1: argc=%d\n" % len(toks))
        for i, t in enumerate(toks):
            sys.stdout.write("ARGV[1][%d]=%s\n" % (i, t))
    return 0

sys.exit(main())
'''

# The field-code model (<=30 lines, amended predicate (v)): expands the consuming field codes
# (%f/%u/%d/%n one argument; %F/%U/%D/%N every remaining argument; %% literal; every other %X
# nothing) but ignores quoting (values appended raw, the result split on whitespace) and
# iteration (exactly one launch).  Non-local URIs drop %f/%F/%d/%n/%D/%N and keep %u/%U as the
# URI itself; file:// URIs map to their path with query/fragment cut.  One launch always.
FIELD_SRC = r'''import json, os, sys
def main():
    av = [x for x in sys.argv[1:] if x != "--json"]
    desktop, rest = av[0], list(av[1:])
    ex = next((ln[5:] for ln in open(desktop, "rb").read().decode("utf-8", "surrogateescape").splitlines()
               if ln.startswith("Exec=")), None)
    if ex is None:
        sys.stdout.write(json.dumps({"error": "no-exec", "detail": "fieldcode"}) + "\n"); return 2
    def pof(a):
        if "://" not in a: return a
        if not a.startswith("file://"): return None
        return a[7:].split("#", 1)[0].split("?", 1)[0]
    out, i = "", 0
    while i < len(ex):
        if ex[i] != "%" or i + 1 >= len(ex): out += ex[i]; i += 1; continue
        c = ex[i + 1]; i += 2
        if c == "%": out += "%"
        elif c in "fudnFUDN":
            n = 1 if c in "fudn" else len(rest); vals, rest = rest[:n], rest[n:]
            ps = []
            for v in vals:
                p = pof(v)
                if c in "uU": q = p if p is not None else v
                elif c in "fF": q = p or ""
                elif c in "dD": q = os.path.dirname(p) if p else ""
                else: q = os.path.basename(p) if p else ""
                ps.append(q)
            out += " ".join(x for x in ps if x)
    sys.stdout.write(json.dumps({"launches": 1, "argv": [out.split()]}) + "\n"); return 0
sys.exit(main())
'''


def build_control(tdir: str, name: str, src: str) -> str:
    p = os.path.join(tdir, name)
    with open(p, "w", encoding="ascii", newline="\n") as fh:
        fh.write(src)
    return p


def score_control(tool_path: str, cases: list[dict], work: str, jobs: int, audit: str) -> int:
    """Correct answers of a control model over the frozen cases (same launcher, parser and
    normalisation as the candidate)."""
    outs = run_cases(tool_path, cases, work, jobs=jobs, audit=audit, prefix="ctl-")
    return sum(1 for o, _d in outs if o == "ok")


def memo_table(cases: list[dict]) -> dict:
    return {str(c.get("id")): c.get("expect") for c in cases}


def memo_score(table: dict, cases: list[dict]) -> int:
    """The memoriser: the frozen expect keyed by case id; a miss answers a sentinel that can never
    equal a real expect.  Fresh case ids never collide with the frozen table, so fresh scores 0."""
    n = 0
    for c in cases:
        hit = table.get(str(c.get("id")))
        if hit is not None and hit == c.get("expect"):
            n += 1
    return n


# ---------------------------------------------------------------- fresh leg

def fresh_cases(gen_path: str, seed: str, work: str, secret: str, tag: int,
                expect_gio_sha: str) -> list[dict]:
    """Run the frozen generator (`python3 -I <genseed> --seed HEX --dir D --out F --count 60`, all
    four flags required) at measurement time; its PATH starts /usr/bin so its gio run resolves to
    the pinned oracle binary.  The generator materialises each case root transiently under --dir
    for its own gio measurement and removes it; the JSONL case dicts (canonical expects, class
    "fresh") go to --out.  The counter reads the case dicts, requires the FRESH_GEN summary count
    and a FRESH_GEN_PIN line carrying the pinned gio sha256, validates every case, and returns the
    dicts - the counter rebuilds every root itself before scoring (roots are NOT read from --dir)."""
    gen_dir = os.path.join(work, f"freshroots-{tag}")
    gen_out = os.path.join(secret, f"fresh-{seed}-{tag}.jsonl")
    os.makedirs(gen_dir, exist_ok=True)
    r = subprocess.run([sys.executable, "-I", gen_path, "--seed", seed, "--dir", gen_dir,
                        "--out", gen_out, "--count", FRESH_COUNT], capture_output=True, text=True,
                       timeout=FRESH_RUN_TIMEOUT,
                       env={"PATH": "/usr/bin:/usr/sbin:/bin", "HOME": gen_dir,
                            "LC_ALL": "C", "TMPDIR": gen_dir})
    if r.returncode != 0:
        raise RuntimeError(f"generator rc={r.returncode}: {r.stderr[-400:]}")
    # the oracle pin: a FRESH_GEN_PIN line must carry the pinned gio sha256 (the fresh labels are
    # only as good as the binary that produced them)
    pin_lines = [ln for ln in r.stdout.splitlines() if ln.startswith("FRESH_GEN_PIN")]
    if not pin_lines or expect_gio_sha not in " ".join(pin_lines):
        raise RuntimeError("generator stdout lacks a FRESH_GEN_PIN line carrying the pinned gio "
                           "sha256")
    summary = [ln for ln in r.stdout.splitlines() if ln.startswith("FRESH_GEN:")]
    case_lines: list[str] = []
    if os.path.exists(gen_out):
        with open(gen_out, encoding="utf-8") as fh:
            case_lines = [ln for ln in fh.read().splitlines() if ln.strip().startswith("{")]
    if not case_lines:
        case_lines = [ln for ln in r.stdout.splitlines() if ln.strip().startswith("{")]
    raw = []
    for ln in case_lines:
        try:
            raw.append(json.loads(ln))
        except json.JSONDecodeError as e:
            raise RuntimeError(f"generator case line is not JSON: {ln[:80]!r}: {e}")
    if not raw:
        raise RuntimeError("generator produced no case lines (--out and stdout both empty)")
    m = None
    for ln in summary:
        m = re.search(r"cases=(\d+)", ln) or m
    if m is not None and int(m.group(1)) != len(raw):
        raise RuntimeError(f"FRESH_GEN summary cases={m.group(1)} != {len(raw)} case lines")
    for c in raw:
        e = validate_case(c, fresh=True)
        if e is not None:
            raise RuntimeError(f"fresh case violations: {e[0]} {e[1]}")
        # label/expect consistency: the generator's label summarises the oracle outcome
        lab = c.get("label")
        exp = c.get("expect", {})
        if lab == "ok" and "error" in exp:
            raise RuntimeError(f"fresh case {c.get('id')}: label ok but expect is a refusal")
        if isinstance(lab, str) and lab.startswith("refusal:"):
            cause = lab.split(":", 1)[1]
            if exp.get("error") != cause:
                raise RuntimeError(f"fresh case {c.get('id')}: label {lab!r} != expect error "
                                   f"{exp.get('error')!r}")
        # canon-gap repair: the generator's canon() only rewrites the case root when it prefixes
        # the value, so an attached field code ("end%f") leaves "<transient-root>/f2.txt" absolute
        # mid-string.  The counter knows the transient root (gen_dir/<case id>) and rewrites it
        # back to the canonical tokens - same semantics, faithful to the measured label.
        troot = os.path.join(gen_dir, str(c.get("id")))
        tprobe = os.path.join(troot, PROBE_FILE)
        avv = exp.get("argv")
        if isinstance(avv, list):
            exp["argv"] = [[s.replace(tprobe, "{probe}").replace(troot, "{root}")
                            if isinstance(s, str) else s for s in vec]
                           for vec in avv if isinstance(vec, list)]
    return raw


# ---------------------------------------------------------------- main

def main() -> int:
    global CLASSES, MIN_PER_CLASS, MIN_CASES, MIN_FRESH_CASES, MIN_SELFTEST_CHECKS, FRESH_COUNT
    ap = argparse.ArgumentParser(
        description="Round-98 C1 counter: scores tools/mado-execargv.py (the launch-argv surface) "
                    "against gio-labelled frozen cases, frozen mutants, a fresh seeded generation, "
                    "controls, and the candidate's --selftest.  PRED-C1-r98-v1.  "
                    "rc 0 TARGET_MET / 1 TARGET_MISSED / 2 SETUP_ERROR.")
    ap.add_argument("--repo", required=True, help="the lane worktree (git -C target)")
    ap.add_argument("--rev", required=True, help="the measured revision holding the frozen candidate")
    ap.add_argument("--base-rev", required=True,
                    help="the round-start revision (tools/mado-execargv.py must be absent there)")
    ap.add_argument("--cases", required=True, help="frozen case file (contract 2 schema)")
    ap.add_argument("--expect-cases-sha256", required=True)
    ap.add_argument("--mutants", required=True, help="frozen mutant file (find/replace anchors)")
    ap.add_argument("--expect-mutants-sha256", required=True)
    ap.add_argument("--genseed", required=True, help="frozen fresh-case generator")
    ap.add_argument("--expect-genseed-sha256", required=True)
    ap.add_argument("--expect-tool-sha256", required=True,
                    help="sha256 of the frozen tools/mado-execargv.py bytes at --rev")
    ap.add_argument("--expect-gio-sha256", required=True, help="sha256 of the installed /usr/bin/gio")
    ap.add_argument("--scratch-root", required=True,
                    help="directory for the counter's own scratch (created, then removed on exit)")
    ap.add_argument("--mini-scale", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)
    if a.mini_scale:
        # counter --selftest fixture scale: the mini universe declares two classes and tiny census
        CLASSES = ("f", "F")
        MIN_PER_CLASS = 1
        MIN_CASES = 2
        MIN_FRESH_CASES = 2
        MIN_SELFTEST_CHECKS = 1
        FRESH_COUNT = "2"

    def setup(detail: str) -> int:
        print(f"{PREFIX} SETUP_ERROR pred={PRED} {detail}")
        return 2

    # ---- 1: pin formats (a malformed pin fails before anything runs)
    pins = [("cases", a.cases, a.expect_cases_sha256),
            ("mutants", a.mutants, a.expect_mutants_sha256),
            ("genseed", a.genseed, a.expect_genseed_sha256)]
    for name, _path, want in pins:
        if not HEX64.match(want):
            return setup(f"id=setup-pin-format --expect-{name}-sha256 {want!r} is not 64 lowercase hex")
    for name, rev in (("rev", a.rev), ("base-rev", a.base_rev)):
        if not HEX40.match(rev) and not HEX40.match(rev.lstrip("g")):
            return setup(f"id=setup-rev-format {name} {rev!r} is not 40 hex")
    # ---- 2: input existence
    for name, path, _want in pins:
        if not os.path.exists(path):
            return setup(f"id=setup-{name}-missing {path} missing")
    # ---- 3: scratch
    work = secret = None
    try:
        os.makedirs(a.scratch_root, exist_ok=True)
        work = tempfile.mkdtemp(prefix="c1r98-", dir=a.scratch_root)
        secret = tempfile.mkdtemp(prefix="c1r98-labels-", dir=a.scratch_root)
        os.makedirs(os.path.join(work, "cases"), exist_ok=True)
    except OSError as e:
        return setup(f"id=setup-scratch-root {a.scratch_root}: {e}")
    try:
        # ---- 4: input sha pins
        for name, path, want in pins:
            got = sha_file(path)
            if got != want:
                return setup(f"id=setup-{name}-sha256 {path} sha256 {got} != pinned {want}")
        # ---- 5: revisions; the tool must be absent at base (the declared before-state).
        # --rev worktree reads the lane's working tree (the candidate may be uncommitted at
        # integration time); any other value must be a commit.
        for name, rev in (("rev", a.rev), ("base-rev", a.base_rev)):
            if name == "rev" and rev == "worktree":
                continue
            r = subprocess.run(["git", "-C", a.repo, "rev-parse", "--verify", "--quiet",
                                rev + "^{commit}"], capture_output=True)
            if r.returncode != 0:
                return setup(f"id=setup-{'rev' if name == 'rev' else 'base-rev'}-not-commit "
                             f"{rev} is not a commit in {a.repo}")
        base_tool_b = git_show(a.repo, a.base_rev, TOOL)
        if base_tool_b is not None:
            return setup(f"id=setup-base-has-tool {TOOL} already present at base-rev {a.base_rev} "
                         "(declared before: absent)")
        print(f"base: {TOOL} absent at base-rev {a.base_rev} (declared before 0/0)")
        # ---- 6: materialise the frozen candidate into scratch (never the lane) and pin it
        if a.rev == "worktree":
            try:
                with open(os.path.join(a.repo, TOOL), "rb") as fh:
                    tb = fh.read()
            except OSError:
                tb = None
        else:
            tb = git_show(a.repo, a.rev, TOOL)
        if tb is None:
            return setup(f"id=setup-tool-missing-at-rev {TOOL} absent at {a.rev}")
        tool_pin = sha(tb) == a.expect_tool_sha256
        if not tool_pin:
            return setup(f"id=setup-tool-sha256 {TOOL} at {a.rev} sha256 {sha(tb)} "
                         f"!= --expect-tool-sha256 {a.expect_tool_sha256}")
        print(f"tool_pin=ok tool_sha256={sha(tb)}")
        # ---- 7: the oracle is the installed gio
        if not (os.path.isfile(GIO) and os.access(GIO, os.X_OK)):
            return setup(f"id=setup-gio-missing {GIO} missing or not executable")
        gio_sha = sha_file(GIO)
        if gio_sha != a.expect_gio_sha256:
            return setup(f"id=setup-gio-sha256 {GIO} sha256 {gio_sha} != --expect-gio-sha256")
        print(f"gio_pin=ok gio_sha256={gio_sha}")
        # ---- 8: frozen case envelope + census
        try:
            with open(a.cases, encoding="utf-8") as fh:
                cases_data = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            return setup(f"id=setup-cases-parse {a.cases}: {e}")
        for eid, msg in validate_cases(cases_data, a.expect_gio_sha256):
            return setup(f"id={eid} {msg}")
        # ---- 8b: the renderer pin - the cases header's renderer_sha256 binds the labels to the
        # oracle renderer bytes; when the renderer file sits next to the cases file, verify it
        rs = cases_data["renderer_sha256"]
        renderer_path = os.path.join(os.path.dirname(os.path.abspath(a.cases)), RENDERER_NAME)
        if os.path.isfile(renderer_path):
            rsha = sha_file(renderer_path)
            if rsha != rs:
                return setup(f"id=setup-renderer-sha256 {renderer_path} sha256 {rsha} != cases "
                             f"header renderer_sha256 {rs}")
            print(f"renderer_pin=ok renderer_sha256={rsha}")
        else:
            print(f"renderer_pin=skip renderer_sha256={rs} (renderer file not beside cases)")
        cases = cases_data["cases"]
        per_class = {k: sum(1 for c in cases if c.get("class") == k) for k in CLASSES}
        print("per_class " + " ".join(f"{k}={per_class[k]}" for k in CLASSES))
        # ---- 9: mutant anchors against the candidate's non-selftest prefix
        try:
            with open(a.mutants, encoding="utf-8") as fh:
                mutants_data = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            return setup(f"id=setup-mutants-parse {a.mutants}: {e}")
        prefix_src = non_selftest_prefix(tb.decode("utf-8", "surrogateescape"))
        for eid, msg in validate_mutants(mutants_data, prefix_src):
            return setup(f"id={eid} {msg}")
        if "candidate_sha256" in mutants_data \
                and mutants_data["candidate_sha256"] != sha(tb):
            return setup(f"id=setup-mutants-candidate-sha256 candidate_sha256 "
                         f"{mutants_data['candidate_sha256']} != tool sha256 {sha(tb)}")
        if "classes" in mutants_data and mutants_data["classes"] != list(CLASSES):
            return setup("id=setup-mutants-classes mutants classes != the frozen 20")
        mutants = mutants_data["mutants"]
        n_no = len(mutants_data.get("not_observable", [])) \
            if isinstance(mutants_data.get("not_observable"), list) else 0
        n_eq = len(mutants_data.get("equivalents", [])) \
            if isinstance(mutants_data.get("equivalents"), list) else 0
        print(f"mutants={len(mutants)} not_observable={n_no} equivalents={n_eq}")

        # ---- place the tool, launcher, audit allow
        tdir = os.path.join(work, "tools")
        os.makedirs(tdir)
        tool_path = os.path.join(tdir, TOOL_NAME)
        with open(tool_path, "wb") as fh:
            fh.write(tb)
        _RUN["launcher"] = os.path.join(work, "launcher.py")
        with open(_RUN["launcher"], "w", encoding="ascii") as fh:
            fh.write(LAUNCHER_SRC)
        pyroots = sorted({os.path.realpath(p) for k, p in sysconfig.get_paths().items()
                          if k in ("stdlib", "platstdlib", "purelib", "platlib")})
        _RUN["allow"] = os.pathsep.join([os.path.realpath(work)] + pyroots)
        _RUN["emptypath"] = tempfile.mkdtemp(prefix="emptypath-", dir=work)
        for k in ("main", "mutant", "selftest", "control"):
            _RUN["logs"][k] = os.path.join(work, f"audit-{k}.log")
            open(_RUN["logs"][k], "w").close()
        print("audit_allow=" + _RUN["allow"])

        # ---- structural conjunct on the frozen candidate bytes
        static_bad = static_check(tb)
        print("static_findings=" + (",".join(static_bad) or "none"))

        # ---- selftest leg (vi): green, failed=0, checks>=12, no FAIL lines
        st = subprocess.run([sys.executable, "-I", _RUN["launcher"], audit_log("selftest"),
                             _RUN["allow"], tool_path, "--selftest"],
                            capture_output=True, text=True, timeout=TOOL_TIMEOUT,
                            cwd=work, env={"PATH": _RUN["emptypath"], "TMPDIR": work,
                                           "LC_ALL": "C"})
        st_fail = [ln for ln in st.stdout.splitlines()
                   if ln.startswith("MADO_EXECARGV_SELFTEST_FAIL:")]
        st_res = re.search(r"^MADO_EXECARGV_SELFTEST: checks=(\d+) failed=(\d+)\s*$",
                           st.stdout, re.M)
        st_checks = int(st_res.group(1)) if st_res else -1
        st_failed = int(st_res.group(2)) if st_res else -1
        selftest_ok = st.returncode == 0 and st_failed == 0 and not st_fail \
            and st_checks >= MIN_SELFTEST_CHECKS
        print(f"selftest rc={st.returncode} checks={st_checks} failed={st_failed} "
              f"fail_lines={len(st_fail)} ok={selftest_ok}")
        for ln in st_fail[:6]:
            print("selftest " + ln)

        # ---- frozen leg (i): one invocation per case under the launcher, empty PATH, HOME=<root>/h
        cases_dir = os.path.join(work, "cases")
        oc = run_cases(tool_path, cases, cases_dir, jobs=8, audit="main", prefix="case-")
        for c, (o, det) in zip(cases, oc):
            if o != "ok":
                print(f"MISMATCH {c['id']} expected={_short(det['expected']) if det else '?'} "
                      f"got={_short(det['got']) if det else '?'}")
        correct = sum(1 for o, _d in oc if o == "ok")
        n = len(cases)
        classes_ok = sum(1 for k in CLASSES
                         if any(c.get("class") == k for c in cases)
                         and all(o == "ok" for c, (o, _d) in zip(cases, oc) if c.get("class") == k))

        # ---- fresh leg (iii): one generation, seed drawn at measurement (or MADO_R98_FRESH_SEED);
        # the counter rebuilds every fresh root itself (the generator's roots are transient)
        seed = os.environ.get("MADO_R98_FRESH_SEED") or os.urandom(8).hex()
        try:
            fcases = fresh_cases(a.genseed, seed, work, secret, 0, a.expect_gio_sha256)
        except (RuntimeError, subprocess.TimeoutExpired, OSError) as e:
            return setup(f"id=setup-fresh-gen {e}")
        foc = run_cases(tool_path, fcases, cases_dir, jobs=8, audit="main", prefix="fresh-")
        fresh_ok = sum(1 for o, _d in foc if o == "ok")
        fresh_total = len(fcases)
        for c, (o, det) in zip(fcases, foc):
            if o != "ok":
                print(f"FRESH_MISMATCH {c.get('id', '?')} expected="
                      f"{_short(det['expected']) if det else '?'} "
                      f"got={_short(det['got']) if det else '?'}")
        print(f"fresh_seed={seed} fresh={fresh_ok}/{fresh_total}")
        table = memo_table(cases)
        memo_fresh = memo_score(table, fcases)
        memo_frozen = memo_score(table, cases)
        print(f"control memoriser frozen={memo_frozen}/{n} fresh={memo_fresh}/{fresh_total}")

        # ---- controls (v): the three DISTINCT embedded models through the same launcher/parser
        naive_path = build_control(tdir, "mado-execargv-naive.py", NAIVE_SRC)
        field_path = build_control(tdir, "mado-execargv-fieldcode.py", FIELD_SRC)
        naive_ok = score_control(naive_path, cases, work, jobs=8, audit="control")
        field_ok = score_control(field_path, cases, work, jobs=8, audit="control")
        print(f"control_naive={naive_ok}/{n} control_fieldcode={field_ok}/{n}")

        # ---- mutant leg (ii): kills are parsed wrong answers or missing answers; crashes are not
        mutdir = os.path.join(work, "mutants")
        os.makedirs(mutdir)
        killed = crashed = survived = 0
        class_kills = {k: 0 for k in CLASSES}
        src_text = tb.decode("utf-8", "surrogateescape")
        for m in mutants:
            mp = os.path.join(mutdir, TOOL_NAME)
            with open(mp, "w", encoding="utf-8") as fh:
                fh.write(src_text.replace(m["find"], m["replace"], 1))
            mors = run_cases(mp, cases, cases_dir, jobs=8, audit="mutant", prefix="mut-")
            wrong_ids = [c["id"] for c, (o, _d), (co, _d2) in zip(cases, mors, oc)
                         if o == "wrong" and co == "ok"]   # a kill needs a NEW wrong answer
            new_crash = sum(1 for (mo, _d), (co, _d2) in zip(mors, oc) if mo == "crash" and co != "crash")
            if wrong_ids:
                killed += 1
                for k in {c["class"] for c, (o, _d), (co, _d2) in zip(cases, mors, oc)
                          if o == "wrong" and co == "ok"}:
                    class_kills[k] += 1
                status = f"killed by {wrong_ids[0]} (+{len(wrong_ids) - 1})"
            elif new_crash:
                crashed += 1
                status = f"crashed_not_killed ({new_crash} new crash cases)"
            else:
                survived += 1
                status = "survived"
            print(f"mutant {m['id']} {status}")
        class_kills_ok = sum(1 for k in CLASSES if class_kills[k] >= 1)
        print("class_kills " + " ".join(f"{k}={class_kills[k]}" for k in CLASSES))

        audit_main = 0
        for k in ("main", "mutant", "selftest", "control"):
            audit_main += len(open(audit_log(k), encoding="utf-8",
                                   errors="replace").read().splitlines())
        main_only = len(open(audit_log("main"), encoding="utf-8",
                             errors="replace").read().splitlines())
        print(f"audit_denials={main_only} audit_denials_all_runs={audit_main}")
        for ln in open(audit_log("main"), encoding="utf-8", errors="replace").read().splitlines()[:20]:
            print("audit " + ln)
    finally:
        if work is not None:
            shutil.rmtree(work, ignore_errors=True)
        if secret is not None:
            shutil.rmtree(secret, ignore_errors=True)

    static_ok = not static_bad
    cases_census = n >= MIN_CASES and all(per_class[k] >= MIN_PER_CLASS for k in CLASSES)
    fresh_census = fresh_total >= MIN_FRESH_CASES
    met = (tool_pin and static_ok and main_only == 0
           and cases_census and correct == n and classes_ok == len(CLASSES)
           and killed == len(mutants) and class_kills_ok == len(CLASSES)
           and fresh_ok == fresh_total and fresh_census and memo_fresh == 0
           and naive_ok < n and field_ok < n and selftest_ok)
    word = "TARGET_MET" if met else "TARGET_MISSED"
    print(f"{PREFIX} {word} pred={PRED} rev={a.rev} base_rev={a.base_rev} "
          f"tool_sha256={sha(tb)} tool_pin={'ok' if tool_pin else 'FAIL'} "
          f"gio_sha256={gio_sha} "
          f"cases={n} correct={correct} classes={classes_ok}/{len(CLASSES)} "
          + "per_class " + " ".join(f"{k}={per_class[k]}" for k in CLASSES) + " "
          + f"mutants={len(mutants)} killed={killed}/{len(mutants)} crashed_not_killed={crashed} "
          f"survived={survived} class_kills={class_kills_ok}/{len(CLASSES)} "
          f"fresh={fresh_ok}/{fresh_total} fresh_seed={seed} "
          f"census cases={'ok' if cases_census else 'FAIL'} fresh={'ok' if fresh_census else 'FAIL'} "
          f"static_structural={'ok' if static_ok else 'FAIL'} audit_denials={main_only} "
          f"control_naive={naive_ok}/{n} control_fieldcode={field_ok}/{n} "
          f"memoriser_frozen={memo_frozen}/{n} memoriser_fresh={memo_fresh}/{fresh_total} "
          f"selftest={'ok' if selftest_ok else 'FAIL'} checks={st_checks} failed={st_failed}")
    return 0 if met else 1


# ================================================================ counter selftest (contract 4)
#
# `python3 -I <this file> --selftest [--scratch-root DIR]` builds a mini universe at selftest time
# (this seat's write scope names no committed fixture path, so the fixtures are synthesised under a
# temp dir instead of committed) and asserts stable check ids.  Fail lines are
# MADO_COUNTER_SELFTEST_FAIL: <id>; the result line is MADO_COUNTER_SELFTEST: checks=N failed=M;
# exit 0 green / 1 failed / 2 could-not-evaluate.

_ST_FAIL_PREFIX = "MADO_COUNTER_SELFTEST_FAIL: "
_ST_IDS = ("st-fixture-build", "st-target-met", "st-result-line-format", "st-tool-pin",
           "st-cases-pin", "st-gio-pin", "st-setup-missing", "st-case-mismatch",
           "st-mutant-survives", "st-mutant-crash", "st-fresh-seed-override",
           "st-fresh-seed-random", "st-memoriser-fresh-zero", "st-controls-behind",
           "st-selftest-leg", "st-scratch-clean")

# The mini candidate: a small but genuine execargv model covering the mini universe's subset
# (%f/%u/%d/%n one-arg codes, %F/%U/%D/%N list codes, %%, unknown codes, the no-substitution
# append, the launch iteration, GKeyFile unescape, g_shell_quote, the shell token grammar).  It is
# NOT the frozen candidate; it exists so the counter's legs have a correct instrument to score.
MINI_TOOL_SRC = r'''#!/usr/bin/env python3
"""Mini execargv model for the round-98 counter selftest (not the frozen candidate)."""
import json
import os
import sys

ONE = ("f", "u", "d", "n")
ALL = ("F", "U", "D", "N")
MARK = "mado-mini"
_UNESC = {"s": " ", "n": "\n", "t": "\t", "r": "\r", "\\": "\\"}


def read_exec(path):
    data = open(path, "rb").read().decode("utf-8", "surrogateescape")
    in_group = False
    for line in data.splitlines():
        line = line.strip()
        if line.startswith("["):
            in_group = line == "[Desktop Entry]"
            continue
        if in_group and line.startswith("Exec="):
            v = line[5:]
            out, i = [], 0
            while i < len(v):
                if v[i] == "\\" and i + 1 < len(v):
                    out.append(_UNESC.get(v[i + 1], v[i + 1]))
                    i += 2
                else:
                    out.append(v[i])
                    i += 1
            return "".join(out)
    return None


def shell_quote(v):
    return "'" + v.replace("'", "'\\''") + "'"


def shell_tokens(s):
    toks, cur, i, started = [], [], 0, False
    while i < len(s):
        c = s[i]
        if c in " \t\n":
            if started:
                toks.append("".join(cur))
                cur = []
                started = False
            i += 1
        elif c == "'":
            started = True
            i += 1
            while i < len(s) and s[i] != "'":
                cur.append(s[i])
                i += 1
            if i < len(s):
                i += 1
        elif c == '"':
            started = True
            i += 1
            while i < len(s) and s[i] != '"':
                if s[i] == "\\" and i + 1 < len(s):
                    cur.append(s[i + 1])
                    i += 2
                else:
                    cur.append(s[i])
                    i += 1
            if i < len(s):
                i += 1
        elif c == "\\" and i + 1 < len(s):
            started = True
            cur.append(s[i + 1])
            i += 2
        else:
            started = True
            cur.append(c)
            i += 1
    if started:
        toks.append("".join(cur))
    return toks


def expand(execv, args):
    launches = []
    remaining = list(args)
    given = bool(args)
    while True:
        out, consumed, i = [], 0, 0
        while i < len(execv):
            c = execv[i]
            if c == "%" and i + 1 < len(execv):
                code = execv[i + 1]
                if code == "%":
                    out.append("%")
                elif code in ONE:
                    if remaining:
                        out.append(shell_quote(remaining.pop(0)))
                        consumed += 1
                elif code in ALL:
                    vals = remaining
                    remaining = []
                    consumed += len(vals)
                    if vals:
                        out.append(" ".join(shell_quote(v) for v in vals))
                i += 2
                continue
            out.append(c)
            i += 1
        if consumed == 0 and remaining and given:
            out.append(" " + shell_quote(remaining.pop(0)))
        text = "".join(out)
        toks = shell_tokens(text)
        if not toks:
            break
        launches.append(toks)
        if not remaining:
            break
    return launches


def main():
    argv = sys.argv[1:]
    as_json = "--json" in argv
    argv = [x for x in argv if x != "--json"]
    if argv and argv[0] == "--selftest":
        return selftest()
    desktop = argv[0]
    files = argv[1:]
    execv = read_exec(desktop)
    if execv is None:
        if as_json:
            sys.stdout.write(json.dumps({"error": "no-exec", "detail": "mini"}) + "\n")
        else:
            sys.stdout.write("MADO_EXECARGV: ERROR no-exec detail=mini\n")
        return 2
    launches = expand(execv, files)
    if as_json:
        sys.stdout.write(json.dumps({"launches": len(launches), "argv": launches}) + "\n")
        return 0
    sys.stdout.write("MADO_EXECARGV: launches=%d\n" % len(launches))
    for k, toks in enumerate(launches, 1):
        sys.stdout.write("LAUNCH %d: argc=%d\n" % (k, len(toks)))
        for i, t in enumerate(toks):
            sys.stdout.write("ARGV[%d][%d]=%s\n" % (k, i, t))
    return 0


def selftest():
    failed = 0
    checks = []

    def check(cid, cond):
        nonlocal failed
        checks.append(cid)
        if not cond:
            failed += 1
            sys.stdout.write("MADO_EXECARGV_SELFTEST_FAIL: %s\n" % cid)

    check("q1", shell_quote("a'b") == "'a'\\''b'")
    check("t1", shell_tokens("a 'b c' d") == ["a", "b c", "d"])
    lv = expand("/p %f", ["/x/y.txt"])
    check("e1", lv == [["/p", "/x/y.txt"]])
    lv2 = expand("/p %f", ["/a", "/b"])
    check("e2", len(lv2) == 2 and lv2[0] == ["/p", "/a"] and lv2[1] == ["/p", "/b"])
    check("e3", expand("/p %%", []) == [["/p", "%"]])
    sys.stdout.write("MADO_EXECARGV_SELFTEST: checks=5 failed=%d\n" % failed)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
'''

# The mini fresh generator: mimics the frozen generator's interface --seed/--dir/--out/--count,
# JSONL case dicts on --out, a FRESH_GEN summary line and a FRESH_GEN_PIN line carrying the pinned
# gio sha256 (hand-derived labels for the mini subset; roots are transient and removed).
MINI_GEN_SRC = r'''import argparse, base64, json, os, sys

PROBE = r"""#!/bin/sh
# mado r98 launch probe: write one argv record per spawn to $0.out.<seq>.
# Sequence numbers are taken under a lock, so file order is spawn order.
exec 9>"$0.lock"; flock 9; n=$(cat "$0.seq" 2>/dev/null || echo 0); n=$((n+1)); echo "$n" > "$0.seq"; flock -u 9
{ printf '@@@ %s\n' "$#"; printf 'P0=%s\n' "$0"; i=1; for a in "$@"; do printf 'A%d=%s\n' "$i" "$a"; i=$((i+1)); done; } > "$0.out.$n"
"""
GIO_SHA = "GIOSHA"

SPEC = [
    ("f-01-fresh", "f", "{probe} %f", [{"kind": "file", "path": "c.txt"}], {"c.txt": b"C\n"}),
    ("F-01-fresh", "F", "{probe} %F", [{"kind": "file", "path": "d.txt"}, {"kind": "file", "path": "e.txt"}],
     {"d.txt": b"D\n", "e.txt": b"E\n"}),
]


def build(root, cid, exec_t, args, files):
    d = os.path.join(root, cid)
    os.makedirs(d, exist_ok=True)
    os.makedirs(os.path.join(d, "h"), exist_ok=True)
    probe = os.path.join(d, "probe.sh")
    with open(probe, "w") as f:
        f.write(PROBE)
    os.chmod(probe, 0o755)
    for rel, data in files.items():
        p = os.path.join(d, rel)
        if os.path.dirname(p):
            os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
    desktop = os.path.join(d, "case.desktop")
    with open(desktop, "w") as f:
        f.write("[Desktop Entry]\nType=Application\nName=Mini\nExec="
                + exec_t.replace("{probe}", probe).replace("{root}", d) + "\n")
    return d, probe


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--count", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.dir)
    os.makedirs(root, exist_ok=True)
    lines = []
    for i, (cid, cls, ex, args, files) in enumerate(SPEC):
        d, probe = build(root, "case-%03d" % i, ex, args, files)
        # hand-derived expect for the mini subset, canonical {probe}/{root} tokens
        toks = [os.path.join("{root}", arg["path"]) for arg in args]
        if "%F" in ex:
            launches = [["{probe}"] + toks]
        else:
            launches = [["{probe}", t] for t in toks]
        case = {"id": cid, "index": i, "class": cls,
                "desktop": {"Name": "Mini", "Icon": None, "Type": "Application",
                            "Exec": ex, "Path": None, "Terminal": None, "Hidden": None},
                "args": args,
                "files": {rel: base64.b64encode(data).decode("ascii") for rel, data in files.items()},
                "expect": {"launches": len(launches), "argv": launches},
                "label": "ok"}
        lines.append(json.dumps(case))
    out = "\n".join(lines) + "\n"
    with open(a.out, "w") as f:
        f.write(out)
    sys.stdout.write("FRESH_GEN: cases=%d ok=%d refused=0\n" % (len(lines), len(lines)))
    sys.stdout.write("FRESH_GEN_PIN gio_sha256=%s glib2=2.90.1-1\n" % GIO_SHA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def _st_git(args: list[str], cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)


def _st_write(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, bytes):
        with open(path, "wb") as fh:
            fh.write(data)
    else:
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(data)


def _b64(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("ascii")


def _mini_desktop(exec_t: str) -> dict:
    return {"Name": "Mini", "Icon": None, "Type": "Application", "Exec": exec_t,
            "Path": None, "Terminal": None, "Hidden": None}


def _mini_frozen_cases() -> list[dict]:
    """Two frozen mini cases (one per rebound class).  expect argv vectors carry the canonical
    {probe}/{root} tokens; the counter's normalisation rewrites them onto the measure root."""
    return [
        {"id": "f-01-mini", "class": "f", "desktop": _mini_desktop("{probe} %f"),
         "args": [{"kind": "file", "path": "a.txt"}, {"kind": "file", "path": "b.txt"}],
         "files": {"a.txt": _b64("A\n"), "b.txt": _b64("B\n")},
         "expect": {"launches": 2,
                    "argv": [["{probe}", "{root}/a.txt"], ["{probe}", "{root}/b.txt"]]}},
        {"id": "F-01-mini", "class": "F", "desktop": _mini_desktop("{probe} pre %F post"),
         "args": [{"kind": "file", "path": "a.txt"}, {"kind": "file", "path": "b.txt"}],
         "files": {"a.txt": _b64("A\n"), "b.txt": _b64("B\n")},
         "expect": {"launches": 1,
                    "argv": [["{probe}", "pre", "{root}/a.txt", "{root}/b.txt", "post"]]}},
    ]


def _mini_bad_cases() -> list[dict]:
    """The frozen mini cases with the F case's expect argv corrupted: the candidate answers
    correctly, the label is wrong, so the frozen leg must report correct=1 and TARGET_MISSED."""
    cases = _mini_frozen_cases()
    cases[1]["expect"]["argv"][0][3] = "{root}/WRONG.txt"
    return cases


def _mini_mutants(kind: str, tool_sha: str) -> dict:
    base = {"version": 1, "tool": TOOL, "candidate_sha256": tool_sha, "classes": ["f", "F"],
            "mutants": [
                {"id": "f-01-one-arg-consumes-all",
                 "find": "                        out.append(shell_quote(remaining.pop(0)))\n"
                         "                        consumed += 1",
                 "replace": "                        vals = remaining\n"
                            "                        remaining = []\n"
                            "                        consumed += len(vals)\n"
                            "                        if vals:\n"
                            "                            out.append(\" \".join(shell_quote(v) for v in vals))",
                 "class": "f", "expect": "kill"},
                {"id": "F-01-list-consumes-one",
                 "find": "                    vals = remaining\n"
                         "                    remaining = []",
                 "replace": "                    vals = remaining[:1]\n"
                            "                    remaining = remaining[1:]",
                 "class": "F", "expect": "kill"}],
            "not_observable": [], "equivalents": []}
    if kind == "survive":
        base["mutants"].append({"id": "f-02-mark-unused", "find": 'MARK = "mado-mini"',
                                "replace": 'MARK = "mado-minx"', "class": "f", "expect": "kill"})
    elif kind == "crash":
        base["mutants"].append({"id": "f-03-syntax", "find": "def shell_tokens(s):",
                                "replace": "def shell_tokens(s", "class": "f", "expect": "kill"})
    return base


def _st_build_fixtures(root: str, gio_sha: str) -> dict:
    """Build the mini universe; returns every path and pin the mini runs need."""
    fx = os.path.join(root, "fixtures")
    repo = os.path.join(fx, "repo")
    os.makedirs(repo)
    _st_git(["init", "-q"], repo)
    _st_write(os.path.join(repo, "README"), "mini base\n")
    _st_git(["add", "-A"], repo)
    _st_git(["-c", "user.name=mado-selftest", "-c", "user.email=selftest@mado",
             "commit", "-q", "-m", "base"], repo)
    tool_bytes = MINI_TOOL_SRC.encode("utf-8")
    tool_sha = sha(tool_bytes)
    _st_write(os.path.join(repo, "tools", TOOL_NAME), tool_bytes)
    _st_git(["add", "-A"], repo)
    _st_git(["-c", "user.name=mado-selftest", "-c", "user.email=selftest@mado",
             "commit", "-q", "-m", "candidate"], repo)
    top = _st_git(["rev-parse", "--show-toplevel"], repo).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise RuntimeError(f"fixture repo toplevel {top} != {repo}")
    rev = _st_git(["rev-parse", "HEAD"], repo).stdout.strip()
    base_rev = _st_git(["rev-parse", "HEAD~1"], repo).stdout.strip()

    def dump(name: str, obj) -> tuple[str, str]:
        p = os.path.join(fx, name)
        _st_write(p, json.dumps(obj, indent=1, sort_keys=True) + "\n")
        return p, sha_file(p)

    # the renderer stub sits beside the mini cases so the renderer pin verifies against it
    renderer_stub = b"# mini renderer stub\n"
    renderer_sha = sha(renderer_stub)
    _st_write(os.path.join(fx, RENDERER_NAME), renderer_stub)
    cases_env = {"version": 1, "oracle": ORACLE_NAME, "gio_sha256": gio_sha, "glib2": GLIB,
                 "renderer_sha256": renderer_sha, "classes": ["f", "F"]}
    cases_path, cases_sha = dump("cases-mini.json", dict(cases_env, cases=_mini_frozen_cases()))
    bad_path, bad_sha = dump("cases-mini-bad.json", dict(cases_env, cases=_mini_bad_cases()))
    muts_path, muts_sha = dump("mutants-mini.json", _mini_mutants("kill", tool_sha))
    muts2_path, muts2_sha = dump("mutants-mini2.json", _mini_mutants("survive", tool_sha))
    muts3_path, muts3_sha = dump("mutants-mini3.json", _mini_mutants("crash", tool_sha))
    gen_path = os.path.join(fx, "execargv-fresh-mini.py")
    _st_write(gen_path, MINI_GEN_SRC.replace("GIOSHA", gio_sha))
    # (renderer stub already written above, before the cases envelope pins it)
    return {"repo": repo, "rev": rev, "base_rev": base_rev, "tool_sha": tool_sha,
            "gio_sha": gio_sha, "cases": cases_path, "cases_sha": cases_sha,
            "bad_cases": bad_path, "bad_cases_sha": bad_sha,
            "mutants": muts_path, "mutants_sha": muts_sha,
            "mutants2": muts2_path, "mutants2_sha": muts2_sha,
            "mutants3": muts3_path, "mutants3_sha": muts3_sha,
            "genseed": gen_path, "genseed_sha": sha_file(gen_path)}


def _mado_counter_selftest(argv: list[str]) -> int:
    scratch = None
    for i, tok in enumerate(argv):
        if tok == "--scratch-root" and i + 1 < len(argv):
            scratch = argv[i + 1]
    try:
        if scratch:
            os.makedirs(scratch, exist_ok=True)
            root = tempfile.mkdtemp(prefix="c1r98-selftest-", dir=scratch)
        else:
            root = tempfile.mkdtemp(prefix="c1r98-selftest-")
    except OSError as e:
        print(f"MADO_COUNTER_SELFTEST: could-not-evaluate scratch: {e}")
        return 2
    checks: list[str] = []
    failed: list[str] = []

    def check(cid: str, ok: bool) -> None:
        checks.append(cid)
        if not ok:
            failed.append(cid)
            print(_ST_FAIL_PREFIX + cid)

    try:
        # the oracle pin is the installed gio (the mini cases envelope binds to it)
        if not (os.path.isfile(GIO) and os.access(GIO, os.X_OK)):
            print("MADO_COUNTER_SELFTEST: could-not-evaluate /usr/bin/gio missing")
            return 2
        gio_sha = sha_file(GIO)
        try:
            fx = _st_build_fixtures(root, gio_sha)
        except Exception as e:
            print(f"MADO_COUNTER_SELFTEST: could-not-evaluate fixtures: {e}")
            return 2
        check("st-fixture-build", all(os.path.exists(fx[k]) for k in
                                      ("repo", "cases", "mutants", "genseed")))

        self_path = os.path.abspath(__file__)

        def run_mini(tag: str, cases=None, cases_sha=None, mutants=None, mutants_sha=None,
                     tool_sha=None, env_extra=None) -> tuple[int, str]:
            scr = os.path.join(root, f"scr-{tag}")
            os.makedirs(scr, exist_ok=True)
            env = dict(os.environ)
            if env_extra:
                env.update(env_extra)
            r = subprocess.run(
                [sys.executable, "-I", self_path,
                 "--repo", fx["repo"], "--rev", fx["rev"], "--base-rev", fx["base_rev"],
                 "--cases", cases or fx["cases"],
                 "--expect-cases-sha256", cases_sha or fx["cases_sha"],
                 "--mutants", mutants or fx["mutants"],
                 "--expect-mutants-sha256", mutants_sha or fx["mutants_sha"],
                 "--genseed", fx["genseed"], "--expect-genseed-sha256", fx["genseed_sha"],
                 "--expect-tool-sha256", tool_sha or fx["tool_sha"],
                 "--expect-gio-sha256", gio_sha,
                 "--scratch-root", scr, "--mini-scale"],
                capture_output=True, text=True, timeout=300, cwd=root, env=env)
            return r.returncode, r.stdout + r.stderr

        def result_line(out: str) -> str:
            return next((ln for ln in out.splitlines() if ln.startswith(PREFIX)), "")

        rc, out = run_mini("green")
        line = result_line(out)
        check("st-target-met", rc == 0 and "TARGET_MET" in line and "correct=2" in line
              and "killed=2/2" in line and "fresh=2/2" in line)
        check("st-result-line-format",
              line.startswith(PREFIX + " TARGET_MET pred=" + PRED + " "))

        rc, out = run_mini("badpin", tool_sha="0" * 64)
        check("st-tool-pin", rc == 2 and "SETUP_ERROR" in out)
        rc, out = run_mini("badcases", cases_sha="1" * 64)
        check("st-cases-pin", rc == 2 and "SETUP_ERROR" in out)
        # wrong gio pin needs a dedicated run (run_mini fixes the gio pin)
        scr = os.path.join(root, "scr-badgio")
        os.makedirs(scr, exist_ok=True)
        r = subprocess.run(
            [sys.executable, "-I", self_path,
             "--repo", fx["repo"], "--rev", fx["rev"], "--base-rev", fx["base_rev"],
             "--cases", fx["cases"], "--expect-cases-sha256", fx["cases_sha"],
             "--mutants", fx["mutants"], "--expect-mutants-sha256", fx["mutants_sha"],
             "--genseed", fx["genseed"], "--expect-genseed-sha256", fx["genseed_sha"],
             "--expect-tool-sha256", fx["tool_sha"], "--expect-gio-sha256", "2" * 64,
             "--scratch-root", scr, "--mini-scale"],
            capture_output=True, text=True, timeout=300, cwd=root, env=dict(os.environ))
        check("st-gio-pin", r.returncode == 2 and "SETUP_ERROR" in r.stdout)
        scr = os.path.join(root, "scr-missing")
        os.makedirs(scr, exist_ok=True)
        r = subprocess.run(
            [sys.executable, "-I", self_path,
             "--repo", fx["repo"], "--rev", fx["rev"], "--base-rev", fx["base_rev"],
             "--cases", os.path.join(os.path.dirname(fx["cases"]), "no-such.json"),
             "--expect-cases-sha256", "0" * 64,
             "--mutants", fx["mutants"], "--expect-mutants-sha256", fx["mutants_sha"],
             "--genseed", fx["genseed"], "--expect-genseed-sha256", fx["genseed_sha"],
             "--expect-tool-sha256", fx["tool_sha"], "--expect-gio-sha256", gio_sha,
             "--scratch-root", scr, "--mini-scale"],
            capture_output=True, text=True, timeout=300, cwd=root, env=dict(os.environ))
        check("st-setup-missing", r.returncode == 2 and "SETUP_ERROR" in r.stdout)

        rc, out = run_mini("badcase", cases=fx["bad_cases"], cases_sha=fx["bad_cases_sha"])
        line = result_line(out)
        check("st-case-mismatch", rc == 1 and "TARGET_MISSED" in line and "correct=1" in line)

        rc, out = run_mini("survive", mutants=fx["mutants2"], mutants_sha=fx["mutants2_sha"])
        line = result_line(out)
        check("st-mutant-survives", rc == 1 and "TARGET_MISSED" in line and "survived=1" in line)

        rc, out = run_mini("crash", mutants=fx["mutants3"], mutants_sha=fx["mutants3_sha"])
        line = result_line(out)
        check("st-mutant-crash", rc == 1 and "TARGET_MISSED" in line
              and "crashed_not_killed=1" in line)

        seed_hex = "0a1b2c3d4e5f6071"
        rc, out = run_mini("seedenv", env_extra={"MADO_R98_FRESH_SEED": seed_hex})
        check("st-fresh-seed-override", rc == 0 and f"fresh_seed={seed_hex}" in out)
        rc, out = run_mini("seedrand")
        m = re.search(r"fresh_seed=([0-9a-f]+)", out)
        check("st-fresh-seed-random", rc == 0 and m is not None and len(m.group(1)) == 16)

        check("st-memoriser-fresh-zero", "memoriser_fresh=0/2" in out)
        cm = re.search(r"control_naive=(\d+)/(\d+) control_fieldcode=(\d+)/(\d+)", out)
        check("st-controls-behind",
              bool(cm) and int(cm.group(1)) < int(cm.group(2))
              and int(cm.group(3)) < int(cm.group(4)))
        check("st-selftest-leg", "selftest=ok" in out and "checks=5" in out)

        # scratch cleanliness: the green run's scratch dir must hold no leftover c1r98-* work dirs
        leftover = [d for d in os.listdir(os.path.join(root, "scr-green"))
                    if d.startswith("c1r98-")]
        check("st-scratch-clean", leftover == [])
    finally:
        shutil.rmtree(root, ignore_errors=True)

    for cid in _ST_IDS:
        if cid not in checks:
            failed.append(cid)
            print(_ST_FAIL_PREFIX + cid)
    print("MADO_COUNTER_SELFTEST: checks=%d failed=%d" % (len(checks), len(failed)))
    return 0 if not failed else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(_mado_counter_selftest(sys.argv[1:]))
    sys.exit(main())
