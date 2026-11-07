#!/usr/bin/env python3
"""Round-99 C1 counter - the launch spawn environment: the load-time program gate (R1, with the
R1b TryExec pre-check), the Terminal=true terminal selection and prepend (R2), the post-prepend
argv[0] lookup (R3), the Path= working directory (R4) and GIO_LAUNCHED_DESKTOP_FILE (R5), over
g_find_program_for_path (R6).  Sources: gdesktopappinfo.c:1946-2004 (load gate), :2765-2830
(known_terminals + prepend), :3027-3126 (no-terminal error, env set, argv[0] lookup, spawn cwd),
gutils.c:300-500 (g_find_program_for_path), gio-tool-launch.c:116 (arg construction).

Frozen predicate PRED-C1-r99-v1 (verbatim from the declaration):
  TARGET_MET iff  cases_correct == cases_total
              AND classes_covered == classes_total
              AND mutants_killed == mutants_counted
              AND fresh_correct == fresh_total
              AND control_naive_correct  < cases_total
              AND control_held_r98_correct < cases_total
  rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR.  The census atoms (>=16 classes, >=60 cases,
  >=60 counted mutants, the fresh count, the static scan) are printed on the verdict line but are
  NOT predicate conjuncts - the predicate above is the whole frozen contract.

Instrument spawns (this counter is an instrument, not a candidate): it spawns `git` read-only
(rev-parse / cat-file via git show), the measured candidate `python3 -I`, the held round-98 tool
`python3 -I`, the embedded naive control `python3 -I`, and the frozen fresh generator `python3 -I`
(the generator itself may run /usr/bin/gio to measure its labels - it is the oracle's instrument).
The counter never launches a host application, never writes the lane, never mutates git state.

Inputs (all sha256-pinned by --expect-*-sha256; SETUP_ERROR on any mismatch):
  --repo     the lane worktree (git -C target; read-only)
  --rev      the measured revision holding tools/mado-launchenv.py + tools/mado-execargv.py, or
             the literal "worktree" (reads the lane working tree for an uncommitted candidate)
  --base-rev the round-start revision 2cbaa141f42df9dfeee4d207cae6558a4dd59863;
             tools/mado-launchenv.py must be ABSENT there (the declared before-state; present ->
             SETUP_ERROR).  Run with --rev <base-rev> the counter prints
             `SETUP_ERROR ... tools/mado-launchenv.py absent at <base-rev>` and exits 2 (the
             declared separability demonstration).
  --cases    frozen case file (contract 2 schema; envelope + case list)
  --mutants  frozen mutant file (find/replace anchors against the candidate's non-selftest prefix,
             cut at the first `def selftest(` - QUALITY 167)
  --genseed  the frozen fresh-case generator; run inside the counter at measurement time as
             `python3 -I <genseed> --seed HEX --dir D --out F --count 60` (all four flags); it
             writes JSONL case dicts to --out and prints a `FRESH_GEN:` summary plus a
             `FRESH_GEN_PIN gio_sha256=...` line carrying the pinned oracle binary digest.
  --expect-gio-sha256  the installed /usr/bin/gio the labels came from (2.90.1-1:
                       d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462).

Case dict (contract 2, oracle-pinned): {"id","class","path":[PATH entries or null],"files":
{rel: b64},"dirs":[rel],"desktop":{key:value},"args":[rel paths],"expect":{...}} with optional
"modes" ({rel: octal-string} - files land 0755 unless a case pins another mode, so the
g_file_test IS_EXECUTABLE half of R1/R2/R3 stays observable), "desktop_raw" (whole-file bytes
after {root}/{probe} substitution), "rel_desktop": true (the desktop ARGUMENT is the bare
"case.desktop", so GIO_LAUNCHED_DESKTOP_FILE measures as the relative argument, R5) and
"args_rel": true (args passed verbatim, resolved by the launch cwd, not root-joined).  Envelope
(pinned): {"version":1,"round":"r99","oracle":"R99MExecOracle","probe_module":...,
"oracle_sha256":<pin>,"renderer_sha256":<same pin - one file is the one renderer, M98-8>,
"gio_path":"/usr/bin/gio","gio_sha256":<pin>,"glib2":"2.90.1-1","schema_notes":...,
"classes":[...unique...],"cases":[...]}.  Expects carry NO absolute paths: canonical "{root}"
and "{probe}" tokens (probe = <root>/probe.sh), canon'd probe-token-first by the oracle
(launchenv-probe-r99.py canon()); the counter reverses "{root}" onto its root FIRST, then
"{probe}" onto <root>/probe.sh - the exact inverse.  The one exception (gdf-rel): env_gdf is the
literal "case.desktop", no token.

Materialisation is the ORACLE's, never re-implemented (M98-8): the counter importlib-loads
launchenv-probe-r99.py from beside the --cases file, after verifying its sha256 against BOTH
envelope pins (SETUP_ERROR on absence or mismatch), and drives build_root(case, parent),
path_string(case, root) and sub_placeholders.  The counter's --selftest mini universe swaps in
an equivalent internal builder so the selftest stays self-contained.

Case leg (the exact invocation every seat agreed on): build the case root under the scratch tree
(files b64 at 0755 or per `modes`, dirs, probe.sh 0755, the desktop file rendered 0644 by the
oracle renderer with {root}/{probe} substituted, empty h/ HOME), then run the tool as
  python3 -I <tool> <desktop-arg> <args...> --path <PATHSTR> --json
with <desktop-arg> = the bare "case.desktop" for a rel_desktop case else <root>/case.desktop,
args root-joined unless args_rel, cwd = the case root, and env exactly {PATH:"", LC_ALL:"C",
HOME:<root>/h} (the seat-spec letter; the forced-empty process PATH makes a candidate that
sneaks a getenv("PATH") lookup fail the frozen expects).  PATHSTR = the oracle's
path_string(case, root): the case's entries after {root}/{probe} substitution, VERBATIM and
joined with ':' (entries may be "" = an empty PATH entry i.e. the cwd per gutils.c:459-463,
".", "bin" relative, or "{root}/bin" absolute); "path": null omits --path entirely (the two
path-unset cases carry an absolute Exec, so the model answer is PATH-independent).  Success
compares launches, the MULTISET of argv vectors (r98 M98-10: spawn order unobservable, frozen
sorted; no path normalisation either side - "<x>/./p" != "<x>/p" != "<x>/bin//p"), cwd exactly,
and env.GIO_LAUNCHED_DESKTOP_FILE exactly.  A refusal expect needs rc 2 and the exact cause
string; detail is ignored.  Refusal causes are compared opaquely (load, no-terminal,
program-not-found, cwd-failed, no-exec, desktop-file, exec-parse all pass through) - the counter
never remaps a cause, so any taxonomy drift surfaces as a scored mismatch.

Legs: (a) materialise + pin both tools; (b) frozen cases; (c) class census; (d) mutants - each
find applied once to a scratch copy (unique in the non-selftest prefix), a kill needs a NEW wrong
answer vs the candidate's own baseline (r70 rule), crashes are crashed_not_killed, never kills;
(e) fresh - the seeded generator's JSONL re-scored by the same leg; (f) controls - control_naive
(the embedded <=30-line Exec.split() + no-environment model) and control_held_r98 (the committed
tools/mado-execargv.py at the measured revision, scored over the same cases with the environment
fields absent on its side and the comparison strict); (g) the base leg (separability).

Counter --selftest (contract 4): `python3 -I <this file> --selftest [--scratch-root DIR]` builds
a mini universe (a two-commit fixture git repo holding a mini candidate + mini sibling, mini
frozen cases, mini mutant files and a mini generator - all synthesised at selftest time under the
scratch dir because this seat's write scope names no committed fixture path) and asserts stable
check ids, printing MADO_COUNTER_SELFTEST_FAIL: <id> per failing check and
MADO_COUNTER_SELFTEST: checks=N failed=M; exit 0 green / 1 failed / 2 could-not-evaluate.
Stdlib only in this counter; ASCII only.
"""
from __future__ import annotations

import argparse
import ast
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

PRED = "PRED-C1-r99-v1"
PREFIX = "MADO_LAUNCHENV_COUNT:"
ST_PREFIX = "MADO_COUNTER_SELFTEST: "
ST_FAIL = "MADO_COUNTER_SELFTEST_FAIL: "
TOOL = "tools/mado-launchenv.py"
TOOL_NAME = "mado-launchenv.py"
SIBLING = "tools/mado-execargv.py"
SIBLING_NAME = "mado-execargv.py"
RENDERER_NAME = "launchenv-probe-r99.py"
ORACLE_NAME = "R99MExecOracle"
GIO = "/usr/bin/gio"
GLIB = "2.90.1-1"
DESKTOP_FILE = "case.desktop"
MIN_CASES = 60          # declaration: the frozen case file carries >=60 cases
MIN_CLASSES = 16        # declaration: >=16 classes
MIN_MUTANTS = 60        # mutant seat: >=60 counted mutants
MIN_SELFTEST_CHECKS = 12
FRESH_COUNT = "60"
TOOL_TIMEOUT = 30.0
FRESH_RUN_TIMEOUT = 900.0
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
    """Canonical-token reversal, the exact inverse of launchenv-probe-r99.py's canon()
    (canon replaced the probe path first, then the root; reversal does {root} first, then
    {probe}).  Probe = <root>/probe.sh, the one path build_root writes."""
    out = str(text).replace("{root}", root)
    return out.replace("{probe}", probe)


def _short(obj, limit: int = 480) -> str:
    s = json.dumps(obj, sort_keys=True, ensure_ascii=True)
    return s if len(s) <= limit else s[:limit - 3] + "..."


def non_selftest_prefix(src: str) -> str:
    """The candidate bytes before its selftest block (QUALITY 167: `def selftest(` sits after the
    production path; mutant anchors live in the prefix)."""
    i = src.find("def selftest(")
    return src if i < 0 else src[:i]


# ---------------------------------------------------------------- case materialisation


class CaseError(Exception):
    pass


# The active builder: the oracle module, loaded and sha-pinned by main before any leg runs
# (materialisation is the oracle's, never re-implemented - M98-8).  The --selftest mini
# universe provides an equivalent embedded module (MINI_ORACLE_SRC) so the production load
# path is what the selftest exercises.
_BUILDER = {"mod": None}


def _builder():
    mod = _BUILDER["mod"]
    if mod is None:
        raise CaseError("no oracle builder loaded (main loads it after the renderer pins)")
    return mod


def build_case_root(case: dict, parent: str) -> tuple[str, str, str]:
    return _builder().build_root(case, parent)


def path_string(case: dict, root: str) -> str | None:
    return _builder().path_string(case, root)


def sub_placeholders(text: str, root: str, probe: str) -> str:
    return _builder().sub_placeholders(text, root, probe)


def materialise_case(case: dict, root_unused: str,
                     desktop_name: str) -> tuple[str, str, list[str], str | None]:
    """Build the case tree under <scratch parent>/<case id>; return (root, desktop ARG, tool FILE
    args, PATHSTR-or-None-for-unset).  The desktop argument is the bare name for a rel_desktop
    case (GIO_LAUNCHED_DESKTOP_FILE then measures as the relative argument, R5); args are
    root-joined unless the case is args_rel."""
    parent = os.path.dirname(root_unused.rstrip("/")) or "."
    root, desktop_path, probe = build_case_root(case, parent)
    darg = desktop_name if case.get("rel_desktop") else desktop_path
    args = []
    for a in case.get("args") or []:
        s = sub_placeholders(str(a), root, probe)
        if not case.get("args_rel") and not os.path.isabs(s):
            s = os.path.join(root, s)
        if os.path.isabs(s):
            # a relative args_rel arg resolves against the case cwd at launch time, so only an
            # absolute arg can be escape-checked here
            rp, rr = os.path.realpath(s), os.path.realpath(root)
            if rp != rr and not rp.startswith(rr + os.sep):
                raise CaseError(f"arg {s!r} escapes the case root")
        args.append(s)
    return root, darg, args, path_string(case, root)


def normalise_expect(expect: dict, root: str, probe: str) -> dict:
    """The expect with canonical tokens rewritten onto the measure-time root; argv kept as a list
    of vectors (the caller sorts both sides - M98-10)."""
    if "error" in expect:
        return {"error": expect.get("error")}
    def one(s):
        return _subst(s, root, probe) if isinstance(s, str) else s
    argv = [[one(s) for s in vec] for vec in expect.get("argv", []) if isinstance(vec, list)]
    cwd = expect.get("cwd")
    gdf = expect.get("env_gdf")
    return {"launches": expect.get("launches"), "argv": argv,
            "cwd": one(cwd) if cwd is not None else None,
            "env_gdf": one(gdf) if gdf is not None else None}


# ---------------------------------------------------------------- tool runs and scoring


def parse_launch_json(stdout: str) -> dict:
    """One of {"kind":"answer",...} | {"kind":"error","cause":C} | {"kind":"malformed"}.
    Required for an answer: launches a non-negative int with len(argv) == launches and every
    vector a list of strings; cwd/env are optional (the held r98 tool and the naive control omit
    them -> None).  A missing or malformed answer is "malformed" (a scored wrong answer)."""
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
    env = obj.get("env")
    gdf = env.get("GIO_LAUNCHED_DESKTOP_FILE") if isinstance(env, dict) else None
    cwd = obj.get("cwd")
    return {"kind": "answer", "launches": launches, "argv": argv,
            "cwd": cwd if isinstance(cwd, str) else None,
            "env_gdf": gdf if isinstance(gdf, str) else None}


def run_tool(tool_path: str, tool_args: list[str], cwd: str, home: str,
             timeout: float = TOOL_TIMEOUT) -> tuple[str, str, int]:
    """("ok", stdout, rc) | ("crash", "", rc).  Only rc 0 and the refusal rc 2 are parseable
    output; anything else (a mutant's traceback, a timeout, a signal) is a crash.  Every scored
    run carries --json and the shared-contract env: PATH set EMPTY (a candidate that reads its
    process PATH instead of --path fails the frozen expects), LC_ALL=C, HOME=<root>/h."""
    argv = [sys.executable, "-I", tool_path] + list(tool_args) + ["--json"]
    env = {"PATH": "", "LC_ALL": "C", "HOME": home}
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, cwd=cwd,
                           env=env)
    except (OSError, subprocess.TimeoutExpired):
        return "crash", "", -1
    if r.returncode not in (0, 2):
        return "crash", "", r.returncode
    return "ok", r.stdout, r.returncode


def score_case(tool_path: str, case: dict, parent: str, desktop_name: str,
               mode: str = "candidate") -> tuple[str, dict | None]:
    """('ok'|'wrong', detail).  mode: "candidate" (the launchenv tool: desktop args --path P),
    "held" (the r98 execargv tool: desktop args, no --path), "naive" (the embedded control).
    Comparison is strict on both sides; environment fields the control cannot answer stay None
    and mismatch a real expect.  The case root is the oracle builder's <parent>/<case id>."""
    try:
        root, darg, file_args, pstr = materialise_case(
            case, os.path.join(parent, "_"), desktop_name)
        norm = normalise_expect(case["expect"], root, os.path.join(root, "probe.sh"))
    except Exception:
        return "crash", None
    if mode == "candidate":
        targs = [darg] + file_args + (["--path", pstr] if pstr is not None else [])
    else:
        targs = [darg] + file_args
    try:
        status, out, rc = run_tool(tool_path, targs, root, os.path.join(root, "h"))
    except Exception:
        return "crash", None
    if status == "crash":
        return "crash", {"rc": rc}
    parsed = parse_launch_json(out)
    exp = case["expect"]
    if "error" in exp:
        if rc == 2 and parsed.get("kind") == "error" and parsed.get("cause") == exp["error"]:
            return "ok", None
        return "wrong", {"expected": norm if not isinstance(norm, dict) or "error" not in norm
                         else {"error": exp.get("error")},
                         "got": {"rc": rc, "kind": parsed.get("kind"),
                                 "cause": parsed.get("cause")}}
    if rc != 0 or parsed.get("kind") != "answer":
        return "wrong", {"expected": norm, "got": {"rc": rc, "kind": parsed.get("kind"),
                                                   "cause": parsed.get("cause")}}
    got = {"launches": parsed.get("launches"), "argv": parsed.get("argv"),
           "cwd": parsed.get("cwd"), "env_gdf": parsed.get("env_gdf")}
    if parsed.get("launches") != norm.get("launches"):
        return "wrong", {"expected": norm, "got": got}
    if sorted(parsed.get("argv", [])) != sorted(norm.get("argv", [])):
        return "wrong", {"expected": norm, "got": got}
    if parsed.get("cwd") != norm.get("cwd"):
        return "wrong", {"expected": norm, "got": got}
    if parsed.get("env_gdf") != norm.get("env_gdf"):
        return "wrong", {"expected": norm, "got": got}
    return "ok", None


def run_cases(tool_path: str, cases: list[dict], parent: str, jobs: int,
              desktop_name: str, mode: str = "candidate",
              prefix: str = "case-") -> list[tuple[str, dict | None]]:
    def one(c: dict) -> tuple[str, dict | None]:
        try:
            return score_case(tool_path, c, parent, desktop_name, mode=mode)
        finally:
            shutil.rmtree(os.path.join(parent, str(c.get("id", "case"))), ignore_errors=True)
    with ThreadPoolExecutor(jobs) as ex:
        return list(ex.map(one, cases))


# ---------------------------------------------------------------- validation

ALLOWED_MODE_RE = re.compile(r"^[0-7]{1,4}$")


CASE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")


def _entry_ok(entry: str) -> bool:
    """A PATH-entry / arg string: {root}/{probe} tokens stripped, then root-relative safety
    ("", "." and plain rel entries allowed; no "..", no bare absolute)."""
    body = entry.replace("{root}", "R").replace("{probe}", "P")
    if body.startswith("/"):
        return False
    return not any(part in ("..", "") for part in body.replace("{root}", "R")
                   .replace("{probe}", "P").strip("/").split("/")) or body in ("", ".")


def validate_case(c: dict, fresh: bool, classes: tuple[str, ...]) -> tuple[str, str] | None:
    """Contract-2 rules for one case; None = ok, else (setup_id, detail).  Shared by the frozen
    and fresh sets (fresh cases carry class "fresh").  Causes are opaque strings (the counter
    does not enforce a taxonomy - it compares, it does not judge)."""
    cid = c.get("id", "?")
    cls = c.get("class")
    if fresh and cls is None:
        cls = "fresh"
    allowed = classes if not fresh else classes + ("fresh",)
    if cls not in allowed:
        return (f"setup-case-{cid}-class", f"class {cls!r} not in the frozen class list")
    if not isinstance(cid, str) or not CASE_ID_RE.match(cid):
        return (f"setup-case-{cid}-id", f"id {cid!r} is not a safe case-id string")
    # no <class>- prefix rule: the r99 frozen ids (e.g. xte-plain in term-xte) do not carry one,
    # and contract 2 never demanded it; safety comes from the charset + the unique-id envelope
    # check, and the class binding is the class key itself
    for k in ("rel_desktop", "args_rel"):
        if k in c and not isinstance(c[k], bool):
            return (f"setup-case-{cid}-{k}", f"{k} is not a bool")
    if c.get("desktop_raw") is not None and not isinstance(c["desktop_raw"], str):
        return (f"setup-case-{cid}-desktop", "desktop_raw is not a string or null")
    if c.get("desktop_raw") is None and not isinstance(c.get("desktop"), dict):
        return (f"setup-case-{cid}-desktop", "desktop is not an object")
    for k, v in (c.get("desktop") or {}).items():
        if not isinstance(k, str) or not k:
            return (f"setup-case-{cid}-desktop", "desktop key is not a non-empty string")
        if v is not None and not isinstance(v, (str, bool)):
            return (f"setup-case-{cid}-desktop", f"desktop {k} value is not str/bool/null")
    for rel in c.get("dirs", []):
        if not isinstance(rel, str) or not _rel_ok(rel):
            return (f"setup-case-{cid}-dirs", f"dirs member {rel!r} escapes the case root")
    path = c.get("path", [])
    if path is not None and not isinstance(path, list):
        return (f"setup-case-{cid}-path", "path is not a list or null")
    for rel in path or []:
        if not isinstance(rel, str) or not _entry_ok(rel):
            return (f"setup-case-{cid}-path", f"path entry {rel!r} escapes the case root")
    for a in c.get("args", []):
        if not isinstance(a, str) or not _entry_ok(a):
            return (f"setup-case-{cid}-args", f"arg {a!r} escapes the case root")
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
    modes = c.get("modes")
    if modes is not None:
        if not isinstance(modes, dict):
            return (f"setup-case-{cid}-modes", "modes is not an object")
        for rel, m in modes.items():
            if rel not in files or rel.endswith("/"):
                return (f"setup-case-{cid}-modes", f"modes key {rel!r} is not a files member")
            if not isinstance(m, str) or not ALLOWED_MODE_RE.match(m):
                return (f"setup-case-{cid}-modes", f"modes[{rel!r}] {m!r} is not octal")
    lc = c.get("launch_cwd")
    if lc is not None:
        if not isinstance(lc, str) or not lc:
            return (f"setup-case-{cid}-launch-cwd", "launch_cwd is not a non-empty string")
        if not lc.startswith("/") and not _rel_ok(lc):
            return (f"setup-case-{cid}-launch-cwd", f"launch_cwd {lc!r} escapes the case root")
    exp = c.get("expect")
    if not isinstance(exp, dict):
        return (f"setup-case-{cid}-expect", "expect is not an object")
    if "error" in exp:
        if not isinstance(exp.get("error"), str) or not exp["error"]:
            return (f"setup-case-{cid}-expect", "error cause is not a non-empty string")
        if "argv" in exp or "launches" in exp:
            return (f"setup-case-{cid}-expect", "expect mixes error and launch shapes")
        return None
    launches = exp.get("launches")
    argv = exp.get("argv")
    if not isinstance(launches, int) or launches < 1:
        return (f"setup-case-{cid}-expect", f"launches {launches!r} < 1")
    if not isinstance(argv, list) or len(argv) != launches:
        return (f"setup-case-{cid}-expect", "argv length != launches")
    for vec in argv:
        if not isinstance(vec, list) or not vec or not all(isinstance(x, str) for x in vec):
            return (f"setup-case-{cid}-expect", "argv vector is not a non-empty string list")
    for k in ("cwd", "env_gdf"):
        if k in exp and exp[k] is not None and not isinstance(exp[k], str):
            return (f"setup-case-{cid}-expect", f"{k} is not a string or null")
    return None


def validate_envelope(data: dict, expect_gio_sha: str) -> list[tuple[str, str]]:
    errs: list[tuple[str, str]] = []
    if data.get("version") != 1:
        errs.append(("setup-envelope-version", f"version {data.get('version')!r} != 1"))
    if "round" in data and data.get("round") != "r99":
        errs.append(("setup-envelope-round", f"round {data.get('round')!r} != 'r99'"))
    if data.get("oracle") != ORACLE_NAME:
        errs.append(("setup-envelope-oracle",
                     f"oracle {data.get('oracle')!r} != {ORACLE_NAME!r}"))
    if data.get("gio_sha256") != expect_gio_sha:
        errs.append(("setup-envelope-gio", "case file gio_sha256 != --expect-gio-sha256 (labels "
                                           "came from another binary)"))
    if "glib2" in data and data.get("glib2") != GLIB:
        errs.append(("setup-envelope-glib2", f"glib2 {data.get('glib2')!r} != {GLIB}"))
    cls = data.get("classes")
    if not isinstance(cls, list) or not cls or not all(isinstance(k, str) and k for k in cls) \
            or len(set(cls)) != len(cls):
        errs.append(("setup-envelope-classes", "classes is not a non-empty list of unique strings"))
    rs = data.get("renderer_sha256")
    osa = data.get("oracle_sha256")
    if not isinstance(rs, str) or not HEX64.match(rs):
        errs.append(("setup-envelope-renderer",
                     f"renderer_sha256 {rs!r} is not 64 lowercase hex"))
    if not isinstance(osa, str) or not HEX64.match(osa):
        errs.append(("setup-envelope-oracle-sha256",
                     f"oracle_sha256 {osa!r} is not 64 lowercase hex"))
    elif isinstance(rs, str) and HEX64.match(rs) and rs != osa:
        errs.append(("setup-envelope-renderer",
                     "renderer_sha256 != oracle_sha256 (one file is the one renderer, M98-8)"))
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errs.append(("setup-envelope-cases",
                     f"{len(cases) if isinstance(cases, list) else '?'} cases, need a non-empty list"))
    return errs


def validate_mutants(data: dict, prefix_src: str, classes: tuple[str, ...]) -> list[tuple[str, str]]:
    """Mutant file schema + anchor checks.  Counted mutants carry expect=="kill"; finds are unique
    across all three lists and occur exactly once in the non-selftest prefix."""
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
    for m in muts:
        mid = m.get("id", "?")
        cls = m.get("class")
        find = m.get("find")
        rep = m.get("replace")
        if cls not in classes:
            errs.append(("setup-mutants-class", f"mutant {mid}: class {cls!r} not in the frozen "
                                                f"class list"))
            continue
        if not isinstance(mid, str) or not mid:
            errs.append(("setup-mutants-id", f"mutant id {mid!r} is not a non-empty string"))
        if mid in seen_ids:
            errs.append(("setup-mutants-id", f"mutant id {mid} duplicated"))
        seen_ids.add(mid)
        if m.get("expect") != "kill":
            errs.append(("setup-mutants-expect",
                         f"mutant {mid}: expect {m.get('expect')!r} != 'kill'"))
        if not isinstance(find, str) or not find or not isinstance(rep, str) or find == rep:
            errs.append(("setup-mutants-anchor",
                         f"mutant {mid}: empty find/replace or find==replace"))
            continue
        n = prefix_src.count(find)
        if n != 1:
            errs.append(("setup-mutants-anchor",
                         f"mutant {mid}: find occurs {n} times in the non-selftest code"))
        if len(errs) > 20:
            errs.append(("setup-mutants-many", "...more"))
            return errs
    return errs


# ---------------------------------------------------------------- static scan (informational)

_BAD_OS = re.compile(r"^(system|popen|exec\w*|spawn\w*|posix_spawn\w*|fork\w*)$")
_BAD_NAMES = {"eval", "exec", "compile", "__import__", "import_module", "breakpoint"}
# process / socket / network / non-libc dynamic top-level imports.  importlib is ALLOWED: contract
# 1 has the candidate load its committed sibling by path.  The scan is informational evidence, not
# a predicate conjunct - the r99 predicate carries no structural clause.
_DENY_TOP = {"subprocess", "socket", "ctypes", "urllib", "http", "ftplib", "smtplib", "poplib",
             "imaplib", "nntplib", "telnetlib", "xmlrpc", "ssl", "webbrowser", "multiprocessing",
             "concurrent", "asyncio", "pty", "socketserver", "requests", "aiohttp"}
_STDLIB = set(getattr(sys, "stdlib_module_names", ()))


def static_scan(src: bytes) -> list[str]:
    bad: list[str] = []
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [f"syntax:{e.lineno}"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                top = al.name.split(".", 1)[0]
                if top in _DENY_TOP:
                    bad.append(f"import:{al.name}:{node.lineno}")
                elif _STDLIB and top not in _STDLIB and top != "importlib":
                    bad.append(f"import-nonstdlib:{al.name}:{node.lineno}")
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            top = mod.split(".", 1)[0]
            if mod != "__future__":
                if top in _DENY_TOP:
                    bad.append(f"import-from:{mod}:{node.lineno}")
                elif _STDLIB and top not in _STDLIB and top != "importlib":
                    bad.append(f"import-from-nonstdlib:{mod}:{node.lineno}")
        elif isinstance(node, ast.Name) and node.id in _BAD_NAMES:
            bad.append(f"name:{node.id}:{node.lineno}")
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "os" \
                    and _BAD_OS.match(node.attr):
                bad.append(f"os.{node.attr}:{node.lineno}")
    return bad


# ---------------------------------------------------------------- controls

# control_naive (predicate control 1): the <=30-line Exec.split() + no-environment model.  One
# launch, argv = the Exec value split on whitespace, field codes literal, args ignored, no
# quoting, no GKeyFile unescape, no terminal, no cwd, no env, no refusal except a missing Exec.
NAIVE_SRC = r'''import json, sys

def main():
    av = [x for x in sys.argv[1:] if x != "--json"]
    ex = None
    for line in open(av[0], "rb").read().decode("utf-8", "surrogateescape").splitlines():
        if line.startswith("Exec="):
            ex = line[5:]
            break
    if ex is None:
        sys.stdout.write(json.dumps({"error": "no-exec", "detail": "naive"}) + "\n")
        return 2
    sys.stdout.write(json.dumps({"launches": 1, "argv": [ex.split()]}) + "\n")
    return 0

sys.exit(main())
'''


def build_control(tdir: str, name: str, src: str) -> str:
    p = os.path.join(tdir, name)
    with open(p, "w", encoding="ascii", newline="\n") as fh:
        fh.write(src)
    return p


def score_control(tool_path: str, cases: list[dict], work: str, jobs: int,
                  desktop_name: str) -> int:
    """Correct answers of a control model over the frozen cases (same leg, parser and
    normalisation as the candidate; mode="naive" strips --path)."""
    outs = run_cases(tool_path, cases, work, jobs=jobs, desktop_name=desktop_name,
                     mode="naive", prefix="ctl-")
    return sum(1 for o, _d in outs if o == "ok")


def score_held(sibling_path: str, cases: list[dict], work: str, jobs: int,
               desktop_name: str) -> int:
    """control_held_r98: the committed round-98 tools/mado-execargv.py over the same cases with
    the same strict comparator; its environment fields are absent on its side."""
    outs = run_cases(sibling_path, cases, work, jobs=jobs, desktop_name=desktop_name,
                     mode="held", prefix="held-")
    return sum(1 for o, _d in outs if o == "ok")


# ---------------------------------------------------------------- fresh leg

def fresh_cases(gen_path: str, seed: str, work: str, secret: str, expect_gio_sha: str,
                expect_oracle_sha: str | None = None) -> list[dict]:
    """Run the frozen generator (`python3 -I <genseed> --seed HEX --dir D --out F --count 60`) at
    measurement time; its PATH starts /usr/bin so its gio run resolves to the pinned oracle
    binary.  Requires rc 0, a FRESH_GEN summary whose cases=N matches the JSONL, and a
    FRESH_GEN_PIN line carrying the pinned gio sha256 (and the pinned oracle sha256 when the
    envelope carries one).  The counter rebuilds every fresh root itself before scoring (the
    generator's roots are transient)."""
    gen_dir = os.path.join(work, "freshroots-0")
    gen_out = os.path.join(secret, f"fresh-{seed}.jsonl")
    os.makedirs(gen_dir, exist_ok=True)
    r = subprocess.run([sys.executable, "-I", gen_path, "--seed", seed, "--dir", gen_dir,
                        "--out", gen_out, "--count", FRESH_COUNT], capture_output=True, text=True,
                       timeout=FRESH_RUN_TIMEOUT,
                       env={"PATH": "/usr/bin:/usr/sbin:/bin", "HOME": gen_dir,
                            "LC_ALL": "C", "TMPDIR": gen_dir})
    if r.returncode != 0:
        raise RuntimeError(f"generator rc={r.returncode}: {r.stderr[-400:]}")
    pin_lines = [ln for ln in r.stdout.splitlines() if ln.startswith("FRESH_GEN_PIN")]
    if not pin_lines or expect_gio_sha not in " ".join(pin_lines):
        raise RuntimeError("generator stdout lacks a FRESH_GEN_PIN line carrying the pinned gio "
                           "sha256")
    if expect_oracle_sha and expect_oracle_sha not in " ".join(pin_lines):
        raise RuntimeError("generator FRESH_GEN_PIN line lacks the pinned oracle sha256")
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
        # canon-gap repair: the generator's transient root back to the canonical {root} token
        troot = os.path.join(gen_dir, str(c.get("id")))
        avv = c.get("expect", {})
        if isinstance(avv, dict):
            def rep(s):
                return s.replace(troot, "{root}") if isinstance(s, str) else s
            if isinstance(avv.get("argv"), list):
                avv["argv"] = [[rep(s) for s in vec] for vec in avv["argv"]
                               if isinstance(vec, list)]
            for k in ("cwd", "env_gdf"):
                if isinstance(avv.get(k), str):
                    avv[k] = rep(avv[k])
            for k in ("Exec", "Path", "TryExec"):
                d = c.get("desktop")
                if isinstance(d, dict) and isinstance(d.get(k), str):
                    d[k] = rep(d[k])
        e = validate_case(c, fresh=True, classes=())
        if e is not None:
            raise RuntimeError(f"fresh case violations: {e[0]} {e[1]}")
    return raw


# ---------------------------------------------------------------- main

def main() -> int:
    global MIN_CASES, MIN_CLASSES, MIN_MUTANTS
    ap = argparse.ArgumentParser(
        description="Round-99 C1 counter: scores tools/mado-launchenv.py (the launch spawn "
                    "environment surface) against gio-labelled frozen cases, frozen mutants, a "
                    "fresh seeded generation, the two predicate controls, and the base "
                    "separability leg.  PRED-C1-r99-v1.  rc 0 TARGET_MET / 1 TARGET_MISSED / "
                    "2 SETUP_ERROR.")
    ap.add_argument("--repo", required=True, help="the lane worktree (git -C target; read-only)")
    ap.add_argument("--rev", required=True,
                    help="the measured revision, or 'worktree' for the lane working tree")
    ap.add_argument("--base-rev", required=True,
                    help="the round-start revision (tools/mado-launchenv.py must be absent there)")
    ap.add_argument("--cases", required=True, help="frozen case file (contract 2 schema)")
    ap.add_argument("--expect-cases-sha256", required=True)
    ap.add_argument("--mutants", required=True, help="frozen mutant file (find/replace anchors)")
    ap.add_argument("--expect-mutants-sha256", required=True)
    ap.add_argument("--genseed", required=True, help="frozen fresh-case generator")
    ap.add_argument("--expect-genseed-sha256", required=True)
    ap.add_argument("--expect-tool-sha256", required=True,
                    help="sha256 of the frozen tools/mado-launchenv.py bytes at --rev")
    ap.add_argument("--expect-execargv-sha256", required=True,
                    help="sha256 of the frozen tools/mado-execargv.py bytes at --rev")
    ap.add_argument("--expect-gio-sha256", required=True, help="sha256 of the installed gio")
    ap.add_argument("--scratch-root", required=True,
                    help="directory for the counter's own scratch (created, then removed on exit)")
    ap.add_argument("--mini-scale", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)
    if a.mini_scale:
        MIN_CASES = 2
        MIN_CLASSES = 1
        MIN_MUTANTS = 2

    def setup(detail: str) -> int:
        print(f"{PREFIX} SETUP_ERROR pred={PRED} {detail}")
        return 2

    # ---- 1: pin formats (a malformed pin fails before anything runs)
    pins = [("cases", a.cases, a.expect_cases_sha256),
            ("mutants", a.mutants, a.expect_mutants_sha256),
            ("genseed", a.genseed, a.expect_genseed_sha256)]
    for name, _path, want in pins:
        if not HEX64.match(want):
            return setup(f"id=setup-pin-format --expect-{name}-sha256 {want!r} is not 64 "
                         f"lowercase hex")
    for name, want in (("tool", a.expect_tool_sha256), ("execargv", a.expect_execargv_sha256),
                       ("gio", a.expect_gio_sha256)):
        if not HEX64.match(want):
            return setup(f"id=setup-pin-format --expect-{name}-sha256 {want!r} is not 64 "
                         f"lowercase hex")
    if a.rev != "worktree" and not HEX40.match(a.rev) and not HEX40.match(a.rev.lstrip("g")):
        return setup(f"id=setup-rev-format rev {a.rev!r} is not 40 hex or 'worktree'")
    if not HEX40.match(a.base_rev) and not HEX40.match(a.base_rev.lstrip("g")):
        return setup(f"id=setup-base-rev-format base-rev {a.base_rev!r} is not 40 hex")

    # ---- 2: input existence
    for name, path, _want in pins:
        if not os.path.exists(path):
            return setup(f"id=setup-{name}-missing {path} missing")

    # ---- 3: scratch
    work = secret = None
    try:
        os.makedirs(a.scratch_root, exist_ok=True)
        work = tempfile.mkdtemp(prefix="c1r99-", dir=a.scratch_root)
        secret = tempfile.mkdtemp(prefix="c1r99-labels-", dir=a.scratch_root)
        os.makedirs(os.path.join(work, "cases"), exist_ok=True)
    except OSError as e:
        return setup(f"id=setup-scratch-root {a.scratch_root}: {e}")

    try:
        # ---- 4: input sha pins
        for name, path, want in pins:
            got = sha_file(path)
            if got != want:
                return setup(f"id=setup-{name}-sha256 {path} sha256 {got} != pinned {want}")

        # ---- 5: revisions; the tool must be absent at base (the declared before-state) and
        # present at rev.  With --rev == --base-rev this is the declared separability
        # demonstration: `SETUP_ERROR ... tools/mado-launchenv.py absent at <base-rev>`, exit 2.
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
                         f"(declared before: absent)")
        if a.rev == "worktree":
            try:
                with open(os.path.join(a.repo, TOOL), "rb") as fh:
                    tb = fh.read()
            except OSError:
                tb = None
            try:
                with open(os.path.join(a.repo, SIBLING), "rb") as fh:
                    sb = fh.read()
            except OSError:
                sb = None
        else:
            tb = git_show(a.repo, a.rev, TOOL)
            sb = git_show(a.repo, a.rev, SIBLING)
        if tb is None:
            return setup(f"id=setup-tool-missing-at-rev {TOOL} absent at {a.rev}")
        if sb is None:
            return setup(f"id=setup-sibling-missing-at-rev {SIBLING} absent at {a.rev} (the "
                         f"candidate loads it as its committed sibling)")
        tool_pin = sha(tb) == a.expect_tool_sha256
        if not tool_pin:
            return setup(f"id=setup-tool-sha256 {TOOL} at {a.rev} sha256 {sha(tb)} != "
                         f"--expect-tool-sha256 {a.expect_tool_sha256}")
        sib_pin = sha(sb) == a.expect_execargv_sha256
        if not sib_pin:
            return setup(f"id=setup-execargv-sha256 {SIBLING} at {a.rev} sha256 {sha(sb)} != "
                         f"--expect-execargv-sha256 {a.expect_execargv_sha256}")
        print(f"tool_pin=ok tool_sha256={sha(tb)}")
        print(f"execargv_pin=ok execargv_sha256={sha(sb)}")

        # ---- 6: the oracle is the installed gio
        if not (os.path.isfile(GIO) and os.access(GIO, os.X_OK)):
            return setup(f"id=setup-gio-missing {GIO} missing or not executable")
        gio_sha = sha_file(GIO)
        if gio_sha != a.expect_gio_sha256:
            return setup(f"id=setup-gio-sha256 {GIO} sha256 {gio_sha} != --expect-gio-sha256")
        print(f"gio_pin=ok gio_sha256={gio_sha}")

        # ---- 7: frozen case envelope + per-case schema
        try:
            with open(a.cases, encoding="utf-8") as fh:
                cases_data = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            return setup(f"id=setup-cases-parse {a.cases}: {e}")
        for eid, msg in validate_envelope(cases_data, a.expect_gio_sha256):
            return setup(f"id={eid} {msg}")
        classes = tuple(cases_data["classes"])
        cases = cases_data["cases"]
        ids = [c.get("id") for c in cases if isinstance(c, dict)]
        if len(ids) != len(cases) or len(set(ids)) != len(ids):
            return setup("id=setup-envelope-case-ids missing or duplicated case ids")
        per_class = {k: 0 for k in classes}
        for c in cases:
            e = validate_case(c, fresh=False, classes=classes)
            if e is not None:
                return setup(f"id={e[0]} {e[1]}")
            per_class[c["class"]] += 1
        # ---- 7b: the oracle renderer is the one materialiser (M98-8).  The file must sit next
        # to the cases file and hash to BOTH envelope pins; the counter importlib-loads it and
        # drives build_root / path_string / sub_placeholders from there on.
        rs = cases_data["renderer_sha256"]
        renderer_path = os.path.join(os.path.dirname(os.path.abspath(a.cases)), RENDERER_NAME)
        if not os.path.isfile(renderer_path):
            return setup(f"id=setup-renderer-missing {RENDERER_NAME} not beside the cases file "
                         f"(materialisation is the oracle's, M98-8)")
        rsha = sha_file(renderer_path)
        if rsha != rs or rsha != cases_data["oracle_sha256"]:
            return setup(f"id=setup-renderer-sha256 {renderer_path} sha256 {rsha} != envelope "
                         f"renderer_sha256 {rs} / oracle_sha256 {cases_data['oracle_sha256']}")
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("mado_launchenv_oracle_r99",
                                                          renderer_path)
            oracle_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(oracle_mod)
            for fn in ("build_root", "path_string", "sub_placeholders"):
                if not callable(getattr(oracle_mod, fn, None)):
                    raise RuntimeError(f"oracle module lacks {fn}()")
        except Exception as e:
            return setup(f"id=setup-renderer-load {renderer_path}: {e}")
        _BUILDER["mod"] = oracle_mod
        print(f"renderer_pin=ok renderer_sha256={rsha}")
        desktop_name = DESKTOP_FILE
        print("per_class " + " ".join(f"{k}={per_class[k]}" for k in classes))

        # ---- 8: mutant anchors against the candidate's non-selftest prefix
        try:
            with open(a.mutants, encoding="utf-8") as fh:
                mutants_data = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            return setup(f"id=setup-mutants-parse {a.mutants}: {e}")
        prefix_src = non_selftest_prefix(tb.decode("utf-8", "surrogateescape"))
        for eid, msg in validate_mutants(mutants_data, prefix_src, classes):
            return setup(f"id={eid} {msg}")
        if "candidate_sha256" in mutants_data \
                and mutants_data["candidate_sha256"] != sha(tb):
            return setup(f"id=setup-mutants-candidate-sha256 candidate_sha256 "
                         f"{mutants_data['candidate_sha256']} != tool sha256 {sha(tb)}")
        if "classes" in mutants_data and tuple(mutants_data["classes"]) != classes:
            return setup("id=setup-mutants-classes mutants classes != the frozen class list")
        mutants = mutants_data["mutants"]
        n_no = len(mutants_data.get("not_observable", [])) \
            if isinstance(mutants_data.get("not_observable"), list) else 0
        n_eq = len(mutants_data.get("equivalents", [])) \
            if isinstance(mutants_data.get("equivalents"), list) else 0
        print(f"mutants={len(mutants)} not_observable={n_no} equivalents={n_eq}")

        # ---- place the tools in the scratch tree (never the lane)
        tdir = os.path.join(work, "tools")
        os.makedirs(tdir)
        tool_path = os.path.join(tdir, TOOL_NAME)
        with open(tool_path, "wb") as fh:
            fh.write(tb)
        sibling_path = os.path.join(tdir, SIBLING_NAME)
        with open(sibling_path, "wb") as fh:
            fh.write(sb)

        # ---- static scan of the frozen candidate bytes (informational)
        static_bad = static_scan(tb)
        print("static_findings=" + (",".join(static_bad) or "none"))

        # ---- frozen leg (b): one invocation per case under the shared case leg
        cases_dir = os.path.join(work, "cases")
        os.makedirs(cases_dir, exist_ok=True)
        oc = run_cases(tool_path, cases, cases_dir, jobs=8,
                       desktop_name=desktop_name, mode="candidate", prefix="case-")
        for c, (o, det) in zip(cases, oc):
            if o != "ok":
                print(f"MISMATCH {c['id']} detail={_short({'expected': (det or {}).get('expected')
                                                           if det else None,
                                                           'got': (det or {}).get('got')
                                                           if det else None})}")
        correct = sum(1 for o, _d in oc if o == "ok")
        n = len(cases)
        classes_ok = sum(1 for k in classes
                         if any(c.get("class") == k for c in cases)
                         and all(o == "ok" for c, (o, _d) in zip(cases, oc)
                                 if c.get("class") == k))
        print(f"correct={correct}/{n}")

        # ---- fresh leg (e): one generation, seed drawn at measurement (or MADO_R99_FRESH_SEED);
        # the counter rebuilds every fresh root itself (the generator's roots are transient)
        seed = os.environ.get("MADO_R99_FRESH_SEED") or os.urandom(8).hex()
        try:
            fcases = fresh_cases(a.genseed, seed, work, secret, a.expect_gio_sha256,
                                 cases_data.get("oracle_sha256"))
        except (RuntimeError, subprocess.TimeoutExpired, OSError) as e:
            return setup(f"id=setup-fresh-gen {e}")
        foc = run_cases(tool_path, fcases, cases_dir, jobs=8,
                        desktop_name=desktop_name, mode="candidate", prefix="fresh-")
        fresh_ok = sum(1 for o, _d in foc if o == "ok")
        fresh_total = len(fcases)
        for c, (o, det) in zip(fcases, foc):
            if o != "ok":
                print(f"FRESH_MISMATCH {c.get('id', '?')} detail="
                      f"{_short({'expected': (det or {}).get('expected') if det else None,
                                 'got': (det or {}).get('got') if det else None})}")
        print(f"fresh_seed={seed} fresh={fresh_ok}/{fresh_total}")

        # ---- controls (f): the two predicate controls through the same leg and comparator
        naive_path = build_control(tdir, "mado-launchenv-naive.py", NAIVE_SRC)
        naive_ok = score_control(naive_path, cases, cases_dir, jobs=8,
                                 desktop_name=desktop_name)
        held_ok = score_held(sibling_path, cases, cases_dir, jobs=8,
                             desktop_name=desktop_name)
        print(f"control_naive={naive_ok}/{n} control_held_r98={held_ok}/{n}")

        # ---- mutant leg (d): kills need a NEW wrong answer vs the candidate's own baseline;
        # crashes are crashed_not_killed, never kills
        mutdir = os.path.join(work, "mutants")
        os.makedirs(mutdir)
        # the mutated candidate loads its committed sibling by path: the sibling sits beside it
        with open(os.path.join(mutdir, SIBLING_NAME), "wb") as fh:
            fh.write(sb)
        killed = crashed = survived = 0
        class_kills = {k: 0 for k in classes}
        src_text = tb.decode("utf-8", "surrogateescape")
        for m in mutants:
            mp = os.path.join(mutdir, TOOL_NAME)
            pos = prefix_src.find(m["find"])
            with open(mp, "w", encoding="utf-8") as fh:
                fh.write(src_text[:pos] + m["replace"] + src_text[pos + len(m["find"]):])
            mors = run_cases(mp, cases, cases_dir, jobs=8,
                             desktop_name=desktop_name, mode="candidate", prefix="mut-")
            wrong_ids = [c["id"] for c, (o, _d), (co, _d2) in zip(cases, mors, oc)
                         if o == "wrong" and co == "ok"]
            new_crash = sum(1 for (mo, _d), (co, _d2) in zip(mors, oc)
                            if mo == "crash" and co != "crash")
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
        class_kills_ok = sum(1 for k in classes if class_kills[k] >= 1)
        print("class_kills " + " ".join(f"{k}={class_kills[k]}" for k in classes))
    finally:
        if work is not None:
            shutil.rmtree(work, ignore_errors=True)
        if secret is not None:
            shutil.rmtree(secret, ignore_errors=True)

    cases_census = n >= MIN_CASES
    classes_census = len(classes) >= MIN_CLASSES
    mutants_census = len(mutants) >= MIN_MUTANTS
    # PRED-C1-r99-v1, exactly the declared conjuncts:
    met = (correct == n
           and classes_ok == len(classes)
           and killed == len(mutants)
           and fresh_ok == fresh_total
           and naive_ok < n
           and held_ok < n)
    word = "TARGET_MET" if met else "TARGET_MISSED"
    print(f"{PREFIX} {word} pred={PRED} rev={a.rev} base_rev={a.base_rev} "
          f"tool_sha256={sha(tb)} tool_pin={'ok' if tool_pin else 'FAIL'} "
          f"execargv_sha256={sha(sb)} execargv_pin={'ok' if sib_pin else 'FAIL'} "
          f"gio_sha256={gio_sha} "
          f"cases={n} correct={correct} classes={classes_ok}/{len(classes)} "
          + "per_class " + " ".join(f"{k}={per_class[k]}" for k in classes) + " "
          + f"mutants={len(mutants)} killed={killed}/{len(mutants)} "
          f"crashed_not_killed={crashed} survived={survived} "
          f"class_kills={class_kills_ok}/{len(classes)} "
          f"fresh={fresh_ok}/{fresh_total} fresh_seed={seed} "
          f"census cases={'ok' if cases_census else 'FAIL'} "
          f"classes={'ok' if classes_census else 'FAIL'} "
          f"mutants={'ok' if mutants_census else 'FAIL'} "
          f"static_findings={','.join(static_bad) or 'none'} "
          f"control_naive={naive_ok}/{n} control_held_r98={held_ok}/{n}")
    return 0 if met else 1


# ================================================================ counter selftest (contract 4)

_ST_IDS = ("st-fixture-build", "st-target-met", "st-result-line-format", "st-tool-pin",
           "st-execargv-pin", "st-cases-pin", "st-gio-pin", "st-setup-missing",
           "st-renderer-missing", "st-base-has-tool", "st-rev-absent-at-base",
           "st-case-mismatch", "st-mutant-survives", "st-mutant-crash",
           "st-fresh-seed-override", "st-fresh-seed-random", "st-controls-behind",
           "st-scratch-clean")

# The mini sibling: the module the mini candidate loads by path (contract 1's sibling load, so
# the selftest exercises the two-file materialisation too).
MINI_SIBLING_SRC = r'''"""mado-execargv mini sibling (counter selftest fixture)."""
MARK = "mini-sibling-v1"


def expand_argv(exec_value, files):
    return exec_value.split() + list(files)
'''

# The mini candidate: a small but genuine launchenv model (crude Exec split via the sibling, the
# Path= cwd, GIO_LAUNCHED_DESKTOP_FILE, a missing-Exec refusal).  It is NOT the frozen candidate;
# it exists so the counter's legs have a correct instrument to score.
MINI_TOOL_SRC = r'''#!/usr/bin/env python3
"""Mini launchenv model for the round-99 counter selftest (not the frozen candidate)."""
import importlib.util
import json
import os
import sys

MARK = "mado-mini-launchenv"


def load_sibling():
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        "mado_mini_execargv", os.path.join(here, "mado-execargv.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_key(path, key):
    data = open(path, "rb").read().decode("utf-8", "surrogateescape")
    for line in data.splitlines():
        if line.startswith(key + "="):
            return line[len(key) + 1:]
    return None


def main():
    av = sys.argv[1:]
    as_json = "--json" in av
    av = [x for x in av if x != "--json"]
    if av and av[0] == "--selftest":
        sys.stdout.write("MADO_LAUNCHENV_SELFTEST: checks=1 failed=0\n")
        return 0
    pth = None
    if "--path" in av:
        i = av.index("--path")
        pth = av[i + 1]
        del av[i:i + 2]
    desktop, files = av[0], av[1:]
    ex = read_key(desktop, "Exec")
    if ex is None:
        if as_json:
            sys.stdout.write(json.dumps({"error": "no-exec", "detail": "mini"}) + "\n")
        return 2
    sib = load_sibling()
    toks = sib.expand_argv(ex, files)
    p = read_key(desktop, "Path")
    cwd = os.getcwd() if not p else p
    if as_json:
        sys.stdout.write(json.dumps({"launches": 1, "cwd": cwd, "terminal": "-",
                                     "argv": [toks],
                                     "env": {"GIO_LAUNCHED_DESKTOP_FILE": desktop}}) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

# The mini fresh generator: the frozen generator's interface --seed/--dir/--out/--count, JSONL
# case dicts on --out, a FRESH_GEN summary and a FRESH_GEN_PIN line carrying the pinned gio
# sha256 (hand-derived labels for the mini subset; roots are transient and removed).
MINI_GEN_SRC = r'''import argparse, base64, json, os, sys

GIO_SHA = "GIOSHA"
ORACLE_SHA = "GENORACLE"

PROG = b"#!/bin/sh\ntrue\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--count", required=True)
    a = ap.parse_args()
    n = max(1, min(int(a.count), 4))
    lines = []
    root = os.path.abspath(a.dir)
    for i in range(n):
        cid = "fresh-%s-%02d" % (a.seed[:8], i)
        d = os.path.join(root, cid)
        os.makedirs(os.path.join(d, "bin"), exist_ok=True)
        os.makedirs(os.path.join(d, "h"), exist_ok=True)
        os.makedirs(os.path.join(d, "work"), exist_ok=True)
        with open(os.path.join(d, "bin", "prog.sh"), "wb") as f:
            f.write(PROG)
        os.chmod(os.path.join(d, "bin", "prog.sh"), 0o755)
        argname = "f%d.txt" % i
        with open(os.path.join(d, argname), "wb") as f:
            f.write(("F%d %s\n" % (i, a.seed)).encode())
        with open(os.path.join(d, "case.desktop"), "w") as f:
            f.write("[Desktop Entry]\nType=Application\nName=Mini\n"
                    "Exec={root}/bin/prog.sh\nPath={root}/work\n".replace("{root}", d))
        case = {"id": cid, "class": "fresh",
                "path": ["bin"],
                "files": {"bin/prog.sh": base64.b64encode(PROG).decode("ascii"),
                          argname: base64.b64encode(("F%d %s\n" % (i, a.seed)).encode())
                          .decode("ascii")},
                "dirs": ["work"],
                "desktop": {"Type": "Application", "Name": "Mini",
                            "Exec": "{root}/bin/prog.sh", "Path": "{root}/work"},
                "args": [argname],
                "expect": {"launches": 1,
                           "argv": [["{root}/bin/prog.sh", "{root}/" + argname]],
                           "cwd": "{root}/work",
                           "env_gdf": "{root}/case.desktop"},
                "label": "ok"}
        lines.append(json.dumps(case))
    with open(a.out, "w") as f:
        f.write("\n".join(lines) + "\n")
    sys.stdout.write("FRESH_GEN: cases=%d ok=%d refused=0\n" % (n, n))
    sys.stdout.write("FRESH_GEN_PIN: gio_sha256=%s oracle_sha256=%s glib2=2.90.1-1\n"
                     % (GIO_SHA, ORACLE_SHA))
    return 0


sys.exit(main())
'''

# The mini oracle builder: the same surface launchenv-probe-r99.py exposes to the counter
# (build_root / path_string / sub_placeholders).  It is written beside the mini cases file and
# pinned by the mini envelope's renderer_sha256 == oracle_sha256, so the selftest drives the
# production load-and-verify path.
MINI_ORACLE_SRC = r'''"""Mini oracle builder (counter selftest fixture; same surface as
launchenv-probe-r99.py build_root/path_string/sub_placeholders)."""
import base64
import os
import shutil

ORACLE_SHA = "ORACLESHA"


def sub_placeholders(text, root, probe):
    return str(text).replace("{probe}", probe).replace("{root}", root)


def path_string(case, root):
    entries = case.get("path", [])
    if entries is None:
        return None
    probe = os.path.join(root, "probe.sh")
    return ":".join(sub_placeholders(e, root, probe) for e in entries)


def build_root(case, parent):
    root = os.path.join(parent, case["id"])
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, "h"))
    for rel in sorted(case.get("files") or {}):
        dst = os.path.join(root, rel)
        pd = os.path.dirname(dst)
        if pd:
            os.makedirs(pd, exist_ok=True)
        with open(dst, "wb") as fh:
            fh.write(base64.b64decode(case["files"][rel]))
        os.chmod(dst, 0o755)
    for rel in case.get("dirs") or []:
        os.makedirs(os.path.join(root, rel), exist_ok=True)
    probe = os.path.join(root, "probe.sh")
    desktop_path = os.path.join(root, "case.desktop")
    if case.get("desktop_raw") is not None:
        data = sub_placeholders(case["desktop_raw"], root, probe).encode("ascii")
    else:
        lines = ["[Desktop Entry]"]
        for key, v in (case.get("desktop") or {}).items():
            if v is None:
                continue
            if isinstance(v, bool):
                v = "true" if v else "false"
            lines.append("%s=%s" % (key, sub_placeholders(v, root, probe)))
        data = ("\n".join(lines) + "\n").encode("ascii")
    with open(desktop_path, "wb") as fh:
        fh.write(data)
    return root, desktop_path, probe
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


MINI_CLASSES = ["plain", "args"]


def _mini_frozen_cases() -> list[dict]:
    """Four frozen mini cases with canonical {root} tokens, covering the desktop-argument and
    args forms the counter leg must reproduce (rel_desktop, args_rel)."""
    return [
        {"id": "plain-01-mini", "class": "plain", "path": ["bin"],
         "files": {"bin/prog.sh": _b64("#!/bin/sh\ntrue\n")},
         "dirs": ["work"],
         "desktop": {"Type": "Application", "Name": "Mini",
                     "Exec": "{root}/bin/prog.sh", "Path": "{root}/work"},
         "args": [],
         "rel_desktop": True,
         "expect": {"launches": 1, "argv": [["{root}/bin/prog.sh"]],
                    "cwd": "{root}/work", "env_gdf": "case.desktop"}},
        {"id": "plain-02-mini", "class": "plain", "path": ["bin"],
         "files": {"bin/prog.sh": _b64("#!/bin/sh\ntrue\n")},
         "dirs": ["work"],
         "desktop": {"Type": "Application", "Name": "Mini",
                     "Exec": "{root}/bin/prog.sh", "Path": "{root}/work"},
         "args": [],
         "expect": {"launches": 1, "argv": [["{root}/bin/prog.sh"]],
                    "cwd": "{root}/work", "env_gdf": "{root}/case.desktop"}},
        {"id": "args-01-mini", "class": "args", "path": ["bin"],
         "files": {"bin/prog.sh": _b64("#!/bin/sh\ntrue\n"), "f1.txt": _b64("F\n")},
         "dirs": [],
         "desktop": {"Type": "Application", "Name": "Mini",
                     "Exec": "{root}/bin/prog.sh x y"},
         "args": ["f1.txt"],
         "expect": {"launches": 1,
                    "argv": [["{root}/bin/prog.sh", "x", "y", "{root}/f1.txt"]],
                    "cwd": "{root}", "env_gdf": "{root}/case.desktop"}},
        {"id": "args-02-mini", "class": "args", "path": ["bin"],
         "files": {"bin/prog.sh": _b64("#!/bin/sh\ntrue\n"), "f2.txt": _b64("G\n")},
         "dirs": [],
         "desktop": {"Type": "Application", "Name": "Mini",
                     "Exec": "{root}/bin/prog.sh"},
         "args": ["f2.txt"],
         "args_rel": True,
         "expect": {"launches": 1,
                    "argv": [["{root}/bin/prog.sh", "f2.txt"]],
                    "cwd": "{root}", "env_gdf": "{root}/case.desktop"}},
    ]


def _mini_bad_cases() -> list[dict]:
    """The frozen mini cases with one label corrupted: the candidate answers correctly, the label
    is wrong, so the frozen leg reports correct=3 and TARGET_MISSED."""
    cases = _mini_frozen_cases()
    cases[1]["expect"]["cwd"] = "{root}/WRONG"
    return cases


def _mini_mutants(kind: str, tool_sha: str) -> dict:
    base = {"version": 1, "tool": TOOL, "candidate_sha256": tool_sha, "classes": MINI_CLASSES,
            "mutants": [
                {"id": "plain-01-cwd-dropped",
                 "find": "    cwd = os.getcwd() if not p else p\n",
                 "replace": "    cwd = None\n", "class": "plain", "expect": "kill"},
                {"id": "args-01-args-dropped",
                 "find": "    toks = sib.expand_argv(ex, files)\n",
                 "replace": "    toks = sib.expand_argv(ex, [])\n",
                 "class": "args", "expect": "kill"}],
            "not_observable": [], "equivalents": []}
    if kind == "survive":
        base["mutants"].append({"id": "plain-02-mark-unused",
                                "find": 'MARK = "mado-mini-launchenv"',
                                "replace": 'MARK = "mado-mini-launchenvx"',
                                "class": "plain", "expect": "kill"})
    elif kind == "crash":
        base["mutants"].append({"id": "args-02-syntax",
                                "find": "def read_key(path, key):",
                                "replace": "def read_key(path key):",
                                "class": "args", "expect": "kill"})
    return base


def _st_build_repo(fx: str, tool_at_base: bool) -> dict:
    """A two-commit fixture repo; with tool_at_base the candidate already sits in the base commit
    (the separability violation fixture)."""
    repo = os.path.join(fx, "repo" + ("-base" if tool_at_base else ""))
    os.makedirs(repo)
    _st_git(["init", "-q"], repo)
    if tool_at_base:
        # the separability-violation fixture: a DIFFERENT candidate already sits in the base
        # commit, so the base leg must refuse (and the repo still gains a second commit)
        base_src = MINI_TOOL_SRC.replace('MARK = "mado-mini-launchenv"',
                                         'MARK = "mado-mini-base"')
        _st_write(os.path.join(repo, TOOL), base_src.encode("utf-8"))
        _st_write(os.path.join(repo, SIBLING), MINI_SIBLING_SRC.encode("utf-8"))
    else:
        _st_write(os.path.join(repo, "README"), "mini base\n")
    _st_git(["add", "-A"], repo)
    _st_git(["-c", "user.name=mado-selftest", "-c", "user.email=selftest@mado",
             "commit", "-q", "-m", "base"], repo)
    _st_write(os.path.join(repo, TOOL), MINI_TOOL_SRC.encode("utf-8"))
    _st_write(os.path.join(repo, SIBLING), MINI_SIBLING_SRC.encode("utf-8"))
    _st_git(["add", "-A"], repo)
    _st_git(["-c", "user.name=mado-selftest", "-c", "user.email=selftest@mado",
             "commit", "-q", "-m", "candidate"], repo)
    top = _st_git(["rev-parse", "--show-toplevel"], repo).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise RuntimeError(f"fixture repo toplevel {top} != {repo}")
    return {"repo": repo, "rev": _st_git(["rev-parse", "HEAD"], repo).stdout.strip(),
            "base_rev": _st_git(["rev-parse", "HEAD~1"], repo).stdout.strip()}


def _st_build_fixtures(root: str, gio_sha: str) -> dict:
    fx = os.path.join(root, "fixtures")
    os.makedirs(fx)
    r1 = _st_build_repo(fx, tool_at_base=False)
    r2 = _st_build_repo(fx, tool_at_base=True)

    def dump(name: str, obj) -> tuple[str, str]:
        p = os.path.join(fx, name)
        _st_write(p, json.dumps(obj, indent=1, sort_keys=True) + "\n")
        return p, sha_file(p)

    # the mini oracle builder sits beside the mini cases and is pinned by BOTH envelope pins,
    # so the production load-and-verify path is what every mini run exercises
    oracle_src = MINI_ORACLE_SRC.replace("ORACLESHA", "mini-oracle-r99")
    renderer_sha = sha(oracle_src.encode("utf-8"))
    _st_write(os.path.join(fx, RENDERER_NAME), oracle_src)
    env = {"version": 1, "round": "r99", "oracle": ORACLE_NAME, "gio_sha256": gio_sha,
           "glib2": GLIB, "renderer_sha256": renderer_sha, "oracle_sha256": renderer_sha,
           "classes": MINI_CLASSES}
    cases_path, cases_sha = dump("cases-mini.json", dict(env, cases=_mini_frozen_cases()))
    bad_path, bad_sha = dump("cases-mini-bad.json", dict(env, cases=_mini_bad_cases()))
    # a cases copy with NO renderer beside it: materialisation must refuse (M98-8)
    nr = os.path.join(fx, "norenderer")
    os.makedirs(nr, exist_ok=True)
    norenderer_path, norenderer_sha = dump(os.path.join("norenderer", "cases-mini.json"),
                                           dict(env, cases=_mini_frozen_cases()))
    muts_path, muts_sha = dump("mutants-mini.json", _mini_mutants("kill", sha(
        MINI_TOOL_SRC.encode("utf-8"))))
    muts2_path, muts2_sha = dump("mutants-mini2.json", _mini_mutants("survive", sha(
        MINI_TOOL_SRC.encode("utf-8"))))
    muts3_path, muts3_sha = dump("mutants-mini3.json", _mini_mutants("crash", sha(
        MINI_TOOL_SRC.encode("utf-8"))))
    gen_path = os.path.join(fx, "launchenv-fresh-mini.py")
    _st_write(gen_path, MINI_GEN_SRC.replace("GIOSHA", gio_sha)
              .replace("GENORACLE", renderer_sha))
    return {"repo": r1["repo"], "rev": r1["rev"], "base_rev": r1["base_rev"],
            "repo_base_tool": r2["repo"], "rev_base_tool": r2["rev"],
            "base_rev_base_tool": r2["base_rev"],
            "tool_sha": sha(MINI_TOOL_SRC.encode("utf-8")),
            "sibling_sha": sha(MINI_SIBLING_SRC.encode("utf-8")),
            "norenderer": norenderer_path, "norenderer_sha": norenderer_sha,
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
            root = tempfile.mkdtemp(prefix="c1r99-selftest-", dir=scratch)
        else:
            root = tempfile.mkdtemp(prefix="c1r99-selftest-")
    except OSError as e:
        print(f"{ST_PREFIX}could-not-evaluate scratch: {e}")
        return 2
    checks: list[str] = []
    failed: list[str] = []

    def check(cid: str, ok: bool) -> None:
        checks.append(cid)
        if not ok:
            failed.append(cid)
            print(ST_FAIL + cid)

    try:
        if not (os.path.isfile(GIO) and os.access(GIO, os.X_OK)):
            print(f"{ST_PREFIX}could-not-evaluate {GIO} missing")
            return 2
        gio_sha = sha_file(GIO)
        try:
            fx = _st_build_fixtures(root, gio_sha)
        except Exception as e:
            print(f"{ST_PREFIX}could-not-evaluate fixtures: {e}")
            return 2
        check("st-fixture-build", all(os.path.exists(fx[k]) for k in
                                      ("repo", "cases", "mutants", "genseed")))

        self_path = os.path.abspath(__file__)

        def run_mini(tag: str, repo=None, rev=None, base_rev=None, cases=None, cases_sha=None,
                     mutants=None, mutants_sha=None, tool_sha=None, sib_sha=None,
                     gio=None, env_extra=None) -> tuple[int, str]:
            scr = os.path.join(root, f"scr-{tag}")
            os.makedirs(scr, exist_ok=True)
            env = dict(os.environ)
            if env_extra:
                env.update(env_extra)
            r = subprocess.run(
                [sys.executable, "-I", self_path,
                 "--repo", repo or fx["repo"], "--rev", rev or fx["rev"],
                 "--base-rev", base_rev or fx["base_rev"],
                 "--cases", cases or fx["cases"],
                 "--expect-cases-sha256", cases_sha or fx["cases_sha"],
                 "--mutants", mutants or fx["mutants"],
                 "--expect-mutants-sha256", mutants_sha or fx["mutants_sha"],
                 "--genseed", fx["genseed"], "--expect-genseed-sha256", fx["genseed_sha"],
                 "--expect-tool-sha256", tool_sha or fx["tool_sha"],
                 "--expect-execargv-sha256", sib_sha or fx["sibling_sha"],
                 "--expect-gio-sha256", gio or gio_sha,
                 "--scratch-root", scr, "--mini-scale"],
                capture_output=True, text=True, timeout=300, cwd=root, env=env)
            return r.returncode, r.stdout + r.stderr

        def result_line(out: str) -> str:
            return next((ln for ln in out.splitlines() if ln.startswith(PREFIX)), "")

        rc, out = run_mini("green")
        line = result_line(out)
        fm = re.search(r"fresh=(\d+)/(\d+)", line)
        check("st-target-met", rc == 0 and "TARGET_MET" in line and "correct=4" in line
              and "killed=2/2" in line and fm is not None and fm.group(1) == fm.group(2)
              and "classes=2/2" in line)
        check("st-result-line-format",
              line.startswith(PREFIX + " TARGET_MET pred=" + PRED + " "))

        rc, out = run_mini("badtool", tool_sha="0" * 64)
        check("st-tool-pin", rc == 2 and "SETUP_ERROR" in out)
        rc, out = run_mini("badsib", sib_sha="1" * 64)
        check("st-execargv-pin", rc == 2 and "SETUP_ERROR" in out)
        rc, out = run_mini("badcases", cases_sha="2" * 64)
        check("st-cases-pin", rc == 2 and "SETUP_ERROR" in out)
        rc, out = run_mini("badgio", gio="3" * 64)
        check("st-gio-pin", rc == 2 and "SETUP_ERROR" in out)
        rc, out = run_mini("missing", cases=os.path.join(os.path.dirname(fx["cases"]),
                                                         "no-such.json"),
                           cases_sha="0" * 64)
        check("st-setup-missing", rc == 2 and "SETUP_ERROR" in out)
        rc, out = run_mini("norenderer", cases=fx["norenderer"], cases_sha=fx["norenderer_sha"])
        check("st-renderer-missing", rc == 2 and "setup-renderer-missing" in out)
        # the separability violation: the tool already present at base
        rc, out = run_mini("basetool", repo=fx["repo_base_tool"], rev=fx["rev_base_tool"],
                           base_rev=fx["base_rev_base_tool"])
        check("st-base-has-tool", rc == 2 and "setup-base-has-tool" in out)
        # the declared separability demonstration: scoring at the base revision itself
        rc, out = run_mini("atbase", rev=fx["base_rev"])
        check("st-rev-absent-at-base", rc == 2 and "SETUP_ERROR" in out
              and f"{TOOL} absent at {fx['base_rev']}" in out)

        rc, out = run_mini("badcase", cases=fx["bad_cases"], cases_sha=fx["bad_cases_sha"])
        line = result_line(out)
        check("st-case-mismatch", rc == 1 and "TARGET_MISSED" in line and "correct=3" in line)

        rc, out = run_mini("survive", mutants=fx["mutants2"], mutants_sha=fx["mutants2_sha"])
        line = result_line(out)
        check("st-mutant-survives", rc == 1 and "TARGET_MISSED" in line and "survived=1" in line)

        rc, out = run_mini("crash", mutants=fx["mutants3"], mutants_sha=fx["mutants3_sha"])
        line = result_line(out)
        check("st-mutant-crash", rc == 1 and "TARGET_MISSED" in line
              and "crashed_not_killed=1" in line)

        seed_hex = "0a1b2c3d4e5f6071"
        rc, out = run_mini("seedenv", env_extra={"MADO_R99_FRESH_SEED": seed_hex})
        check("st-fresh-seed-override", rc == 0 and f"fresh_seed={seed_hex}" in out)
        rc, out = run_mini("seedrand")
        m = re.search(r"fresh_seed=([0-9a-f]+)", out)
        check("st-fresh-seed-random", rc == 0 and m is not None and len(m.group(1)) == 16)

        cm = re.search(r"control_naive=(\d+)/(\d+) control_held_r98=(\d+)/(\d+)", out)
        check("st-controls-behind",
              bool(cm) and int(cm.group(1)) < int(cm.group(2))
              and int(cm.group(3)) < int(cm.group(4)))

        # scratch cleanliness: the green run's scratch dir holds no leftover c1r99-* work dirs
        leftover = [d for d in os.listdir(os.path.join(root, "scr-green"))
                    if d.startswith("c1r99-")]
        check("st-scratch-clean", leftover == [])
    finally:
        shutil.rmtree(root, ignore_errors=True)

    for cid in _ST_IDS:
        if cid not in checks:
            failed.append(cid)
            print(ST_FAIL + cid)
    print(f"{ST_PREFIX}checks={len(checks)} failed={len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(_mado_counter_selftest(sys.argv[1:]))
    sys.exit(main())
