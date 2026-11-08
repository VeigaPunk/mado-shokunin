#!/usr/bin/env python3
"""Round-100 C1 counter - the PATH-unset default search path of the launch load gate.

Surface under measurement: `g_find_program_for_path` (gutils.c:370-382) resolves a bare
program through the literal search path `/bin:/usr/bin:.` when the `PATH` variable is
ABSENT from the environment (not when it is present and empty).  tools/mado-launchenv.py
models that branch as DEFAULT_SEARCH_PATH, and the round's `path-default` class of frozen
cases measures it against the installed /usr/bin/gio (glib2 2.90.1-1).

Frozen predicate PRED-C1-r100-v1 (verbatim from the declaration):
  TARGET_MET iff  default_cases            >= 6
              AND  default_classes          >= 3
              AND  cases_correct            == cases_total
              AND  fresh_correct            == fresh_total        (fresh_total >= 8, seeded at measurement)
              AND  mutants_killed           == mutants_counted    (mutants_counted >= 4)
              AND  base_set_default_cases   == 0                  (the do-nothing control, measured on the r99 case file)
              AND  control_unset_as_empty_correct < cases_total   (the misreading the branch guards against)
  rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR.  The predicate above is the whole frozen
  contract: no other conjunct is scored, and the census atoms (per-class counts, the static
  scan, the base-leg behavioural evidence) are printed as evidence, never as conjuncts.

Instrument, not candidate (spawn list): this counter spawns `git` read-only
(`rev-parse`, `show`), the measured candidate and its mutants/control through `python3 -I`,
and the frozen fresh generator through `python3 -I`.  The generator may itself run the pinned
/usr/bin/gio to measure its labels (it is the oracle's instrument).  The counter never
launches a host application, never writes the lane, and never mutates git state.

The one leg that differs from round 99: a `path: null` case means PATH is ABSENT from the
child environment.  The candidate leg therefore runs such a case with NO `PATH` key in the
child env and NO `--path` (contract 1: no --path and no PATH = PATH unset), while every other
case runs with a deliberately empty process PATH plus `--path <entries>` (an empty PATH entry
is then the case's own set-but-empty PATH).  Without this the unset branch is unobservable and
the mutant m2 (unset treated as empty) could never be killed.

Inputs (all sha256-pinned; SETUP_ERROR on any mismatch or missing input):
  --repo                 the lane worktree (git -C target; read-only)
  --rev                  the measured revision, or the literal "worktree"
  --base-rev             the round-start revision 43309e6a...; tools/mado-launchenv.py must be
                         PRESENT there (the declared before-state: the branch is modelled at
                         base and exercised by zero frozen cases).  Absent -> SETUP_ERROR.
  --cases                frozen r100 case file (contract 2 envelope)
  --expect-cases-sha256  pin of that file
  --mutants              frozen r100 mutant file (find/replace anchors against the candidate's
                         non-selftest prefix, cut at the first `def selftest(` - QUALITY 167)
  --expect-mutants-sha256 pin of that file
  --genseed              frozen r100 fresh-case generator
  --expect-genseed-sha256 pin of that file
  --expect-tool-sha256    pin of tools/mado-launchenv.py at --rev
  --expect-execargv-sha256 pin of tools/mado-execargv.py at --rev
  --expect-gio-sha256     pin of the installed /usr/bin/gio
  --base-cases           the round-99 case file for the do-nothing control (default:
                         <repo>/.ufo/waves/round-99/controls/launchenv-cases-r99.json)
  --expect-base-cases-sha256 optional pin of that file (checked when given)
  --scratch-root         counter scratch (created; removed on exit)

Materialisation is the ORACLE's, never re-implemented (M98-8): the counter importlib-loads
launchenv-probe-r99.py from beside the --cases file (falling back to the round-99 controls
directory), verifies its sha256 against BOTH envelope pins (renderer_sha256 and
oracle_sha256), and drives build_root(case, parent), path_string(case, root) and
sub_placeholders from there the whole run.

Mutant population = the frozen file's mutants plus four REQUIRED probes that the round
mandates (m1 default without the trailing dot, m2 unset-as-empty, m3 working-dir join
disabled, m4 empty-entry rule collapsed), de-duplicated on the exact (find, replace) pair.
A kill needs a NEW wrong answer against the candidate's own baseline on at least one case
(r70 rule); a crash is `crashed_not_killed`, never a kill.  A required probe whose anchor is
absent from the candidate prefix cannot be built: it stays counted and uncounted-as-killed,
so the run reports TARGET_MISSED (never a green from an unbuildable mutant).

control_unset_as_empty: a copy built from the candidate PREFIX (cut at `def selftest(`) with
the unset branch replaced by `path = ''`, plus the candidate tail so the copy is runnable.
It is scored through the same case leg over the frozen cases; the predicate requires it to
lose at least one case.

base_set_default_cases: the do-nothing control.  It reads the round-99 case file and counts
cases whose class starts with `path-default`; doing nothing in this round leaves that count
at 0.  As additional evidence (never a conjunct) the counter also scores the BASE revision's
tool over the round-99 cases and reports how many of them change answer when that tool's
unset branch is read as empty (`base_branch_sensitive_cases`): the frozen statement says
zero, and this leg measures it.

Counter --selftest (contract 4): builds a complete mini universe under the scratch dir (a
fixture git repo whose base commit already carries the mini candidate, a mini sibling, mini
frozen cases with the three path-default discriminator classes, mini mutant files, a mini
fresh generator, a round-99-style base case file) and asserts stable check ids, printing
MADO_COUNTER_SELFTEST_FAIL: <id> per failing check and
MADO_COUNTER_SELFTEST: checks=N failed=M; exit 0 green / 1 failed / 2 could-not-evaluate.

Stdlib only; ASCII only.
"""
from __future__ import annotations

import argparse
import ast
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

PRED = "PRED-C1-r100-v1"
PREFIX = "MADO_C1_R100:"
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
CLASS_PREFIX = "path-default"
BASE_CASES_DEFAULT = ".ufo/waves/round-99/controls/launchenv-cases-r99.json"
MIN_DEFAULT_CASES = 6
MIN_DEFAULT_CLASSES = 3
MIN_FRESH = 8
MIN_MUTANTS = 4
FRESH_COUNT = 8
TOOL_TIMEOUT = 30.0
FRESH_RUN_TIMEOUT = 900.0
JOBS = 8
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")

# The four mutant probes the round mandates.  Each is (id, find, replace, defect); the anchor
# must occur exactly once in the candidate's non-selftest prefix.  They are part of the counted
# population, so `mutants_killed == mutants_counted` covers "each required mutant is killed".
REQUIRED_PROBES = (
    {"id": "req-m1-default-no-trailing-dot",
     "find": "DEFAULT_SEARCH_PATH = '/bin:/usr/bin:.'",
     "replace": "DEFAULT_SEARCH_PATH = '/bin:/usr/bin'",
     "defect": "default-path-dot-dropped"},
    {"id": "req-m2-unset-as-empty",
     "find": "    if path is None:\n        path = DEFAULT_SEARCH_PATH\n",
     "replace": "    if path is None:\n        path = ''\n",
     "defect": "unset-treated-as-empty"},
    {"id": "req-m3-working-dir-join-disabled",
     "find": "        if working_dir is not None and not _is_abs(startp):\n"
             "            startp = _join2(working_dir, startp)",
     "replace": "        if False:\n            startp = _join2(working_dir, startp)",
     "defect": "relative-candidate-join-dropped"},
    {"id": "req-m4-empty-entry-collapsed",
     "find": "        if entry == '':\n            startp = program\n        else:\n"
             "            startp = entry + '/' + program",
     "replace": "        if entry == '':\n            startp = entry + '/' + program\n"
                "        else:\n            startp = entry + '/' + program",
     "defect": "empty-entry-rule-collapsed"},
)

# control_unset_as_empty: the misreading the branch guards against (unset read as empty).
CONTROL_FIND = "    if path is None:\n        path = DEFAULT_SEARCH_PATH\n"
CONTROL_REPLACE = "    if path is None:\n        path = ''\n"
CONTROL_NAME = "mado-launchenv-unset-as-empty.py"

# ---------------------------------------------------------------- small helpers


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: str) -> str:
    with open(p, "rb") as fh:
        return sha(fh.read())


def git_show(repo: str, rev: str, path: str):
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
    """Canonical-token reversal, the exact inverse of the oracle's canon() (canon replaced the
    probe path first, then the root; reversal does {root} first, then {probe})."""
    out = str(text).replace("{root}", root)
    return out.replace("{probe}", probe)


def _short(obj, limit: int = 480) -> str:
    s = json.dumps(obj, sort_keys=True, ensure_ascii=True, default=str)
    return s if len(s) <= limit else s[:limit - 3] + "..."


def non_selftest_prefix(src: str) -> str:
    """The candidate bytes before its selftest block (QUALITY 167: `def selftest(` sits after
    the production path; mutant anchors live in the prefix)."""
    i = src.find("def selftest(")
    return src if i < 0 else src[:i]


def class_is_default(cls) -> bool:
    return isinstance(cls, str) and cls.startswith(CLASS_PREFIX)


# ---------------------------------------------------------------- case materialisation

class CaseError(Exception):
    pass


# The active builder: the oracle module, loaded and sha-pinned by main before any leg runs
# (materialisation is the oracle's, never re-implemented - M98-8).  The --selftest mini
# universe provides an equivalent embedded module so the production load path is exercised.
_BUILDER = {"mod": None}


def _builder():
    mod = _BUILDER["mod"]
    if mod is None:
        raise CaseError("no oracle builder loaded (main loads it after the renderer pins)")
    return mod


def build_case_root(case: dict, parent: str):
    return _builder().build_root(case, parent)


def path_string(case: dict, root: str):
    return _builder().path_string(case, root)


def sub_placeholders(text: str, root: str, probe: str) -> str:
    return _builder().sub_placeholders(text, root, probe)


def materialise_case(case: dict, parent_hint: str, desktop_name: str):
    """Build the case tree under <scratch parent>/<case id>; return (root, desktop ARG, tool
    FILE args, PATHSTR-or-None-for-unset).  The desktop argument is the bare name for a
    rel_desktop case; args are root-joined unless the case is args_rel."""
    parent = os.path.dirname(parent_hint.rstrip("/")) or "."
    root, desktop_path, probe = build_case_root(case, parent)
    darg = desktop_name if case.get("rel_desktop") else desktop_path
    args = []
    for a in case.get("args") or []:
        s = sub_placeholders(str(a), root, probe)
        if not case.get("args_rel") and not os.path.isabs(s):
            s = os.path.join(root, s)
        if os.path.isabs(s):
            rp, rr = os.path.realpath(s), os.path.realpath(root)
            if rp != rr and not rp.startswith(rr + os.sep):
                raise CaseError("arg %r escapes the case root" % s)
        args.append(s)
    return root, darg, args, path_string(case, root)


def normalise_expect(expect: dict, root: str, probe: str) -> dict:
    """The expect with canonical tokens rewritten onto the measure-time root; argv kept as a
    list of vectors (the caller sorts both sides - M98-10)."""
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
    """One of {"kind":"answer",...} | {"kind":"error","cause":C} | {"kind":"malformed"}."""
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


def run_tool(tool_path: str, tool_args: list, cwd: str, home: str, path_unset: bool,
             timeout: float = TOOL_TIMEOUT):
    """("ok", stdout, rc) | ("crash", "", rc).  rc 0 and the refusal rc 2 are parseable.

    path_unset=True models contract 1's PATH-absent process: the child env carries NO PATH key
    and no --path is passed for that case.  Otherwise the child env carries PATH="" (a poison:
    a candidate that reads its own PATH instead of --path fails the frozen expects) and the
    caller passes --path."""
    argv = [sys.executable, "-I", tool_path] + list(tool_args) + ["--json"]
    env = {"LC_ALL": "C", "HOME": home}
    if not path_unset:
        env["PATH"] = ""
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, cwd=cwd,
                           env=env)
    except (OSError, subprocess.TimeoutExpired):
        return "crash", "", -1
    if r.returncode not in (0, 2):
        return "crash", "", r.returncode
    return "ok", r.stdout, r.returncode


def score_case(tool_path: str, case: dict, parent_hint: str,
               desktop_name: str):
    """('ok'|'wrong'|'crash', detail).  One leg for the candidate, every mutant and the control:
    desktop argument, file arguments, --path for a set PATH, and the PATH-absent child env for a
    `path: null` case."""
    try:
        root, darg, file_args, pstr = materialise_case(case, parent_hint, desktop_name)
        norm = normalise_expect(case["expect"], root, os.path.join(root, "probe.sh"))
    except Exception as e:
        return "crash", {"setup": str(e)[:120]}
    path_unset = case.get("path", []) is None
    targs = [darg] + file_args
    if pstr is not None:
        targs += ["--path", pstr]
    try:
        status, out, rc = run_tool(tool_path, targs, root, os.path.join(root, "h"), path_unset)
    except Exception:
        return "crash", None
    if status == "crash":
        return "crash", {"rc": rc}
    parsed = parse_launch_json(out)
    exp = case["expect"]
    if "error" in exp:
        if rc == 2 and parsed.get("kind") == "error" and parsed.get("cause") == exp["error"]:
            return "ok", None
        return "wrong", {"expected": {"error": exp.get("error")},
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


def run_cases(tool_path: str, cases: list, parent: str, jobs: int,
              desktop_name: str) -> list:
    def one(c: dict):
        try:
            return score_case(tool_path, c, os.path.join(parent, "_"), desktop_name)
        finally:
            shutil.rmtree(os.path.join(parent, str(c.get("id", "case"))), ignore_errors=True)
    with ThreadPoolExecutor(jobs) as ex:
        return list(ex.map(one, cases))


# ---------------------------------------------------------------- validation

ALLOWED_MODE_RE = re.compile(r"^[0-7]{1,4}$")
CASE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")


def _entry_ok(entry: str) -> bool:
    """A PATH-entry / arg string: {root}/{probe} tokens stripped, then root-relative safety
    (\"\", \".\" and plain rel entries allowed; no \"..\", no bare absolute)."""
    body = entry.replace("{root}", "R").replace("{probe}", "P")
    if body.startswith("/"):
        return False
    return not any(part in ("..", "") for part in body.strip("/").split("/")) \
        or body in ("", ".")


def validate_case(c: dict, fresh: bool, classes: tuple):
    """Contract-2 rules for one case; None = ok, else (setup_id, detail)."""
    cid = c.get("id", "?")
    cls = c.get("class")
    if fresh and cls is None:
        cls = "fresh"
    allowed = tuple(classes) if not fresh else tuple(classes) + ("fresh",)
    if cls not in allowed and not (fresh and isinstance(cls, str)
                                   and cls.startswith("fresh")):
        return ("setup-case-%s-class" % cid, "class %r not in the frozen class list" % (cls,))
    if not isinstance(cid, str) or not CASE_ID_RE.match(cid):
        return ("setup-case-%s-id" % cid, "id %r is not a safe case-id string" % (cid,))
    for k in ("rel_desktop", "args_rel"):
        if k in c and not isinstance(c[k], bool):
            return ("setup-case-%s-%s" % (cid, k), "%s is not a bool" % k)
    if c.get("desktop_raw") is not None and not isinstance(c["desktop_raw"], str):
        return ("setup-case-%s-desktop" % cid, "desktop_raw is not a string or null")
    if c.get("desktop_raw") is None and not isinstance(c.get("desktop"), dict):
        return ("setup-case-%s-desktop" % cid, "desktop is not an object")
    for k, v in (c.get("desktop") or {}).items():
        if not isinstance(k, str) or not k:
            return ("setup-case-%s-desktop" % cid, "desktop key is not a non-empty string")
        if v is not None and not isinstance(v, (str, bool)):
            return ("setup-case-%s-desktop" % cid, "desktop %s value is not str/bool/null" % k)
    for rel in c.get("dirs", []):
        if not isinstance(rel, str) or not _rel_ok(rel):
            return ("setup-case-%s-dirs" % cid, "dirs member %r escapes the case root" % (rel,))
    path = c.get("path", [])
    if path is not None and not isinstance(path, list):
        return ("setup-case-%s-path" % cid, "path is not a list or null")
    for rel in path or []:
        if not isinstance(rel, str) or not _entry_ok(rel):
            return ("setup-case-%s-path" % cid, "path entry %r escapes the case root" % (rel,))
    for a in c.get("args", []):
        if not isinstance(a, str) or not _entry_ok(a):
            return ("setup-case-%s-args" % cid, "arg %r escapes the case root" % (a,))
    files = c.get("files", {})
    if not isinstance(files, dict):
        return ("setup-case-%s-files" % cid, "files is not an object")
    for rel, b64 in files.items():
        if not isinstance(rel, str) or not _rel_ok(rel):
            return ("setup-case-%s-escape" % cid, "files member %r escapes the case root" % (rel,))
        if not rel.endswith("/"):
            try:
                unb64(b64)
            except Exception:
                return ("setup-case-%s-b64" % cid, "files member %r is not base64" % (rel,))
    modes = c.get("modes")
    if modes is not None:
        if not isinstance(modes, dict):
            return ("setup-case-%s-modes" % cid, "modes is not an object")
        for rel, m in modes.items():
            if rel not in files or rel.endswith("/"):
                return ("setup-case-%s-modes" % cid,
                        "modes key %r is not a files member" % (rel,))
            if not isinstance(m, str) or not ALLOWED_MODE_RE.match(m):
                return ("setup-case-%s-modes" % cid, "modes[%r] %r is not octal" % (rel, m))
    exp = c.get("expect")
    if not isinstance(exp, dict):
        return ("setup-case-%s-expect" % cid, "expect is not an object")
    if "error" in exp:
        if not isinstance(exp.get("error"), str) or not exp["error"]:
            return ("setup-case-%s-expect" % cid, "error cause is not a non-empty string")
        if "argv" in exp or "launches" in exp:
            return ("setup-case-%s-expect" % cid, "expect mixes error and launch shapes")
        return None
    launches = exp.get("launches")
    argv = exp.get("argv")
    if not isinstance(launches, int) or launches < 1:
        return ("setup-case-%s-expect" % cid, "launches %r < 1" % (launches,))
    if not isinstance(argv, list) or len(argv) != launches:
        return ("setup-case-%s-expect" % cid, "argv length != launches")
    for vec in argv:
        if not isinstance(vec, list) or not vec or not all(isinstance(x, str) for x in vec):
            return ("setup-case-%s-expect" % cid, "argv vector is not a non-empty string list")
    for k in ("cwd", "env_gdf"):
        if k in exp and exp[k] is not None and not isinstance(exp[k], str):
            return ("setup-case-%s-expect" % cid, "%s is not a string or null" % k)
    return None


def validate_envelope(data: dict, expect_gio_sha: str) -> list:
    errs = []
    if data.get("version") != 1:
        errs.append(("setup-envelope-version", "version %r != 1" % (data.get("version"),)))
    if "round" in data and data.get("round") not in ("r100", "r99"):
        errs.append(("setup-envelope-round", "round %r is not r100/r99" % (data.get("round"),)))
    if data.get("oracle") != ORACLE_NAME:
        errs.append(("setup-envelope-oracle",
                     "oracle %r != %r" % (data.get("oracle"), ORACLE_NAME)))
    if data.get("gio_sha256") != expect_gio_sha:
        errs.append(("setup-envelope-gio", "case file gio_sha256 != --expect-gio-sha256 (labels "
                                           "came from another binary)"))
    if "glib2" in data and data.get("glib2") != GLIB:
        errs.append(("setup-envelope-glib2", "glib2 %r != %s" % (data.get("glib2"), GLIB)))
    cls = data.get("classes")
    if not isinstance(cls, list) or not cls or not all(isinstance(k, str) and k for k in cls) \
            or len(set(cls)) != len(cls):
        errs.append(("setup-envelope-classes",
                     "classes is not a non-empty list of unique strings"))
    rs = data.get("renderer_sha256")
    osa = data.get("oracle_sha256")
    if not isinstance(rs, str) or not HEX64.match(rs):
        errs.append(("setup-envelope-renderer", "renderer_sha256 %r is not 64 lowercase hex"
                     % (rs,)))
    if not isinstance(osa, str) or not HEX64.match(osa):
        errs.append(("setup-envelope-oracle-sha256",
                     "oracle_sha256 %r is not 64 lowercase hex" % (osa,)))
    elif isinstance(rs, str) and HEX64.match(rs) and rs != osa:
        errs.append(("setup-envelope-renderer",
                     "renderer_sha256 != oracle_sha256 (one file is the one renderer, M98-8)"))
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errs.append(("setup-envelope-cases", "%s cases, need a non-empty list"
                     % (len(cases) if isinstance(cases, list) else "?")))
    return errs


def validate_mutants(data: dict, prefix_src: str, classes: tuple) -> list:
    """Mutant file schema + anchor checks.  Counted mutants carry expect=="kill"; finds are
    unique across all three lists and occur exactly once in the non-selftest prefix."""
    errs = []
    if "version" in data and data.get("version") != 1:
        errs.append(("setup-mutants-version", "version %r != 1" % (data.get("version"),)))
    if "tool" in data and data.get("tool") != TOOL:
        errs.append(("setup-mutants-tool", "tool %r != %r" % (data.get("tool"), TOOL)))
    muts = data.get("mutants")
    if not isinstance(muts, list) or not muts:
        errs.append(("setup-mutants-empty", "no mutants"))
        return errs
    all_finds = []
    for key in ("mutants", "not_observable", "equivalents"):
        lst = data.get(key, [])
        if not isinstance(lst, list):
            errs.append(("setup-mutants-list", "%s is not a list" % key))
            continue
        for m in lst:
            f = m.get("find") if isinstance(m, dict) else None
            if isinstance(f, str) and f:
                all_finds.append(f)
    if len(all_finds) != len(set(all_finds)):
        errs.append(("setup-mutants-anchor", "a find anchor is duplicated across mutant lists"))
    seen_ids = set()
    for m in muts:
        mid = m.get("id", "?")
        cls = m.get("class")
        find = m.get("find")
        rep = m.get("replace")
        if cls not in classes:
            errs.append(("setup-mutants-class",
                         "mutant %s: class %r not in the frozen class list" % (mid, cls)))
            continue
        if not isinstance(mid, str) or not mid:
            errs.append(("setup-mutants-id", "mutant id %r is not a non-empty string" % (mid,)))
        if mid in seen_ids:
            errs.append(("setup-mutants-id", "mutant id %s duplicated" % mid))
        seen_ids.add(mid)
        if m.get("expect") != "kill":
            errs.append(("setup-mutants-expect",
                         "mutant %s: expect %r != 'kill'" % (mid, m.get("expect"))))
        if not isinstance(find, str) or not find or not isinstance(rep, str) or find == rep:
            errs.append(("setup-mutants-anchor",
                         "mutant %s: empty find/replace or find==replace" % mid))
            continue
        n = prefix_src.count(find)
        if n != 1:
            errs.append(("setup-mutants-anchor",
                         "mutant %s: find occurs %d times in the non-selftest code" % (mid, n)))
        if len(errs) > 20:
            errs.append(("setup-mutants-many", "...more"))
            return errs
    return errs


# ---------------------------------------------------------------- static scan (informational)

_BAD_OS = re.compile(r"^(system|popen|exec\w*|spawn\w*|posix_spawn\w*|fork\w*)$")
_BAD_NAMES = {"eval", "exec", "compile", "__import__", "import_module", "breakpoint"}
_DENY_TOP = {"subprocess", "socket", "ctypes", "urllib", "http", "ftplib", "smtplib", "poplib",
             "imaplib", "nntplib", "telnetlib", "xmlrpc", "ssl", "webbrowser", "multiprocessing",
             "concurrent", "asyncio", "pty", "socketserver", "requests", "aiohttp"}
_STDLIB = set(getattr(sys, "stdlib_module_names", ()))


def static_scan(src: bytes) -> list:
    bad = []
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return ["syntax:%s" % e.lineno]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                top = al.name.split(".", 1)[0]
                if top in _DENY_TOP:
                    bad.append("import:%s:%s" % (al.name, node.lineno))
                elif _STDLIB and top not in _STDLIB and top != "importlib":
                    bad.append("import-nonstdlib:%s:%s" % (al.name, node.lineno))
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            top = mod.split(".", 1)[0]
            if mod != "__future__":
                if top in _DENY_TOP:
                    bad.append("import-from:%s:%s" % (mod, node.lineno))
                elif _STDLIB and top not in _STDLIB and top != "importlib":
                    bad.append("import-from-nonstdlib:%s:%s" % (mod, node.lineno))
        elif isinstance(node, ast.Name) and node.id in _BAD_NAMES:
            bad.append("name:%s:%s" % (node.id, node.lineno))
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "os" \
                    and _BAD_OS.match(node.attr):
                bad.append("os.%s:%s" % (node.attr, node.lineno))
    return bad


# ---------------------------------------------------------------- source surgery

def apply_mutation(src: str, prefix_src: str, find: str, replace: str):
    """Return (mutated source, None) or (None, reason).  The anchor must occur exactly once in
    the non-selftest prefix; the replacement lands there and the tail is kept byte-identical."""
    n = prefix_src.count(find)
    if n != 1:
        return None, "anchor occurs %d times in the non-selftest prefix" % n
    pos = src.find(find)
    if pos < 0:
        return None, "anchor absent from the whole source"
    return src[:pos] + replace + src[pos + len(find):], None


def build_control(src: str, prefix_src: str):
    """control_unset_as_empty: the candidate prefix (cut at `def selftest(`) with the unset
    branch read as empty, plus the untouched tail so the copy is runnable."""
    if prefix_src.count(CONTROL_FIND) != 1:
        return None, "unset branch anchor occurs %d times in the prefix" \
            % prefix_src.count(CONTROL_FIND)
    head = prefix_src.replace(CONTROL_FIND, CONTROL_REPLACE)
    return head + src[len(prefix_src):], None


def build_mutant(src: str, prefix_src: str, m: dict):
    return apply_mutation(src, prefix_src, m["find"], m["replace"])


# ---------------------------------------------------------------- fresh leg

def fresh_cases(gen_path: str, seed: str, work: str, secret: str, expect_gio_sha: str,
                expect_oracle_sha, count: int) -> list:
    """Run the frozen generator (`python3 -I <genseed> --seed HEX --dir D --out F --count N`)
    at measurement time; its PATH is pinned to /usr/bin so a gio run resolves to the pinned
    oracle binary.  Requires rc 0, a FRESH_GEN summary whose cases=N matches the JSONL, and a
    FRESH_GEN_PIN line carrying the pinned gio sha256 (and the pinned oracle sha256 when the
    envelope carries one).  The counter rebuilds every fresh root itself."""
    gen_dir = os.path.join(work, "freshroots-0")
    gen_out = os.path.join(secret, "fresh-%s.jsonl" % seed)
    os.makedirs(gen_dir, exist_ok=True)
    r = subprocess.run([sys.executable, "-I", gen_path, "--seed", seed, "--dir", gen_dir,
                        "--out", gen_out, "--count", str(count)], capture_output=True,
                       text=True, timeout=FRESH_RUN_TIMEOUT,
                       env={"PATH": "/usr/bin:/usr/sbin:/bin", "HOME": gen_dir,
                            "LC_ALL": "C", "TMPDIR": gen_dir})
    if r.returncode != 0:
        raise RuntimeError("generator rc=%d: %s" % (r.returncode, r.stderr[-400:]))
    pin_lines = [ln for ln in r.stdout.splitlines() if ln.startswith("FRESH_GEN_PIN")]
    if not pin_lines or expect_gio_sha not in " ".join(pin_lines):
        raise RuntimeError("generator stdout lacks a FRESH_GEN_PIN line carrying the pinned "
                           "gio sha256")
    if expect_oracle_sha and expect_oracle_sha not in " ".join(pin_lines):
        raise RuntimeError("generator FRESH_GEN_PIN line lacks the pinned oracle sha256")
    summary = [ln for ln in r.stdout.splitlines() if ln.startswith("FRESH_GEN:")]
    case_lines = []
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
            raise RuntimeError("generator case line is not JSON: %r: %s" % (ln[:80], e))
    if not raw:
        raise RuntimeError("generator produced no case lines (--out and stdout both empty)")
    m = None
    for ln in summary:
        m = re.search(r"cases=(\d+)", ln) or m
    if m is not None and int(m.group(1)) != len(raw):
        raise RuntimeError("FRESH_GEN summary cases=%s != %d case lines"
                           % (m.group(1), len(raw)))
    for c in raw:
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
            d = c.get("desktop")
            if isinstance(d, dict):
                for k in ("Exec", "Path", "TryExec"):
                    if isinstance(d.get(k), str):
                        d[k] = rep(d[k])
        e = validate_case(c, fresh=True, classes=())
        if e is not None:
            raise RuntimeError("fresh case violations: %s %s" % e)
    return raw


# ---------------------------------------------------------------- main

def main() -> int:
    global MIN_DEFAULT_CASES, MIN_DEFAULT_CLASSES, MIN_FRESH, MIN_MUTANTS
    ap = argparse.ArgumentParser(
        description="Round-100 C1 counter: scores tools/mado-launchenv.py (the PATH-unset "
                    "default search path of the launch load gate) against gio-labelled frozen "
                    "cases, frozen + mandated mutants, a fresh seeded generation, the "
                    "unset-as-empty control and the round-99 do-nothing control.  "
                    "PRED-C1-r100-v1.  rc 0 TARGET_MET / 1 TARGET_MISSED / 2 SETUP_ERROR.")
    ap.add_argument("--repo", required=True, help="the lane worktree (git -C target; read-only)")
    ap.add_argument("--rev", required=True,
                    help="the measured revision, or 'worktree' for the lane working tree")
    ap.add_argument("--base-rev", required=True,
                    help="the round-start revision (the tool must be PRESENT there)")
    ap.add_argument("--cases", required=True, help="frozen r100 case file (contract 2)")
    ap.add_argument("--expect-cases-sha256", required=True)
    ap.add_argument("--mutants", required=True, help="frozen r100 mutant file")
    ap.add_argument("--expect-mutants-sha256", required=True)
    ap.add_argument("--genseed", required=True, help="frozen fresh-case generator")
    ap.add_argument("--expect-genseed-sha256", required=True)
    ap.add_argument("--expect-tool-sha256", required=True,
                    help="sha256 of tools/mado-launchenv.py at --rev")
    ap.add_argument("--expect-execargv-sha256", required=True,
                    help="sha256 of tools/mado-execargv.py at --rev")
    ap.add_argument("--expect-gio-sha256", required=True, help="sha256 of the installed gio")
    ap.add_argument("--base-cases", default=None,
                    help="the round-99 case file for the do-nothing control "
                         "(default: <repo>/%s)" % BASE_CASES_DEFAULT)
    ap.add_argument("--expect-base-cases-sha256", default=None,
                    help="optional pin of the round-99 case file")
    ap.add_argument("--fresh-count", default=str(FRESH_COUNT),
                    help="cases requested from the fresh generator (default %d)" % FRESH_COUNT)
    ap.add_argument("--jobs", type=int, default=JOBS, help="case-leg threads (default 8)")
    ap.add_argument("--scratch-root", required=True,
                    help="directory for the counter's own scratch (created, then removed)")
    ap.add_argument("--mini-scale", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)
    if a.mini_scale:
        MIN_DEFAULT_CASES = 1
        MIN_DEFAULT_CLASSES = 1
        MIN_FRESH = 1
        MIN_MUTANTS = 1

    def setup(detail: str) -> int:
        print("%s SETUP_ERROR pred=%s %s" % (PREFIX, PRED, detail))
        return 2

    # ---- 1: pin formats (a malformed pin fails before anything runs)
    pins = [("cases", a.cases, a.expect_cases_sha256),
            ("mutants", a.mutants, a.expect_mutants_sha256),
            ("genseed", a.genseed, a.expect_genseed_sha256)]
    for name, _path, want in pins:
        if not HEX64.match(want):
            return setup("id=setup-pin-format --expect-%s-sha256 %r is not 64 lowercase hex"
                         % (name, want))
    for name, want in (("tool", a.expect_tool_sha256),
                       ("execargv", a.expect_execargv_sha256),
                       ("gio", a.expect_gio_sha256)):
        if not HEX64.match(want):
            return setup("id=setup-pin-format --expect-%s-sha256 %r is not 64 lowercase hex"
                         % (name, want))
    if a.expect_base_cases_sha256 is not None \
            and not HEX64.match(a.expect_base_cases_sha256):
        return setup("id=setup-pin-format --expect-base-cases-sha256 %r is not 64 lowercase hex"
                     % (a.expect_base_cases_sha256,))
    if a.rev != "worktree" and not HEX40.match(a.rev):
        return setup("id=setup-rev-format rev %r is not 40 hex or 'worktree'" % (a.rev,))
    if not HEX40.match(a.base_rev):
        return setup("id=setup-base-rev-format base-rev %r is not 40 hex" % (a.base_rev,))
    if a.jobs < 1:
        return setup("id=setup-jobs-format --jobs %d < 1" % a.jobs)
    if not a.fresh_count.isdigit() or int(a.fresh_count) < 1:
        return setup("id=setup-fresh-count --fresh-count %r is not a positive integer"
                     % (a.fresh_count,))

    # ---- 2: input existence (the base case file is a conjunct input: absence refuses)
    base_cases = a.base_cases or os.path.join(a.repo, BASE_CASES_DEFAULT)
    for name, path, _want in pins:
        if not os.path.exists(path):
            return setup("id=setup-%s-missing %s missing" % (name, path))
    if not os.path.exists(base_cases):
        return setup("id=setup-base-cases-missing %s missing (the do-nothing control has no "
                     "case file; pass --base-cases or check out the round-99 controls)"
                     % base_cases)

    # ---- 3: scratch
    work = secret = None
    try:
        os.makedirs(a.scratch_root, exist_ok=True)
        work = tempfile.mkdtemp(prefix="c1r100-", dir=a.scratch_root)
        secret = tempfile.mkdtemp(prefix="c1r100-labels-", dir=a.scratch_root)
        os.makedirs(os.path.join(work, "cases"), exist_ok=True)
    except OSError as e:
        return setup("id=setup-scratch-root %s: %s" % (a.scratch_root, e))

    try:
        # ---- 4: input sha pins
        for name, path, want in pins:
            got = sha_file(path)
            if got != want:
                return setup("id=setup-%s-sha256 %s sha256 %s != pinned %s"
                             % (name, path, got, want))
        if a.expect_base_cases_sha256 is not None:
            got = sha_file(base_cases)
            if got != a.expect_base_cases_sha256:
                return setup("id=setup-base-cases-sha256 %s sha256 %s != pinned %s"
                             % (base_cases, got, a.expect_base_cases_sha256))

        # ---- 5: revisions.  The tool is PRESENT at base (the declared before-state) and must
        # be exactly the pinned bytes at --rev.  With --rev == --base-rev this still scores the
        # base bytes, so the BEFORE state is measurable, not asserted.
        for name, rev in (("rev", a.rev), ("base-rev", a.base_rev)):
            if rev == "worktree":
                continue
            r = subprocess.run(["git", "-C", a.repo, "rev-parse", "--verify", "--quiet",
                                rev + "^{commit}"], capture_output=True)
            if r.returncode != 0:
                return setup("id=setup-%s-not-commit %s is not a commit in %s"
                             % (name, rev, a.repo))
        base_tool_b = git_show(a.repo, a.base_rev, TOOL)
        if base_tool_b is None:
            return setup("id=setup-base-tool-absent %s absent at base-rev %s (declared "
                         "before-state: the branch is modelled there)" % (TOOL, a.base_rev))
        base_sib_b = git_show(a.repo, a.base_rev, SIBLING)
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
            return setup("id=setup-tool-missing-at-rev %s absent at %s" % (TOOL, a.rev))
        if sb is None:
            return setup("id=setup-sibling-missing-at-rev %s absent at %s (the candidate loads "
                         "it as its committed sibling)" % (SIBLING, a.rev))
        tool_sha = sha(tb)
        sib_sha = sha(sb)
        if tool_sha != a.expect_tool_sha256:
            return setup("id=setup-tool-sha256 %s at %s sha256 %s != --expect-tool-sha256 %s"
                         % (TOOL, a.rev, tool_sha, a.expect_tool_sha256))
        if sib_sha != a.expect_execargv_sha256:
            return setup("id=setup-execargv-sha256 %s at %s sha256 %s != --expect-execargv-sha256 "
                         "%s" % (SIBLING, a.rev, sib_sha, a.expect_execargv_sha256))
        print("tool_pin=ok tool_sha256=%s" % tool_sha)
        print("execargv_pin=ok execargv_sha256=%s" % sib_sha)
        print("base_tool_sha256=%s base_execargv_sha256=%s"
              % (sha(base_tool_b), sha(base_sib_b) if base_sib_b is not None else "-"))

        # ---- 6: the oracle is the installed gio
        if not (os.path.isfile(GIO) and os.access(GIO, os.X_OK)):
            return setup("id=setup-gio-missing %s missing or not executable" % GIO)
        gio_sha = sha_file(GIO)
        if gio_sha != a.expect_gio_sha256:
            return setup("id=setup-gio-sha256 %s sha256 %s != --expect-gio-sha256"
                         % (GIO, gio_sha))
        print("gio_pin=ok gio_sha256=%s" % gio_sha)

        # ---- 7: frozen case envelope + per-case schema
        try:
            with open(a.cases, encoding="utf-8") as fh:
                cases_data = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            return setup("id=setup-cases-parse %s: %s" % (a.cases, e))
        for eid, msg in validate_envelope(cases_data, a.expect_gio_sha256):
            return setup("id=%s %s" % (eid, msg))
        classes = tuple(cases_data["classes"])
        cases = cases_data["cases"]
        ids = [c.get("id") for c in cases if isinstance(c, dict)]
        if len(ids) != len(cases) or len(set(ids)) != len(ids):
            return setup("id=setup-envelope-case-ids missing or duplicated case ids")
        per_class = {k: 0 for k in classes}
        for c in cases:
            e = validate_case(c, fresh=False, classes=classes)
            if e is not None:
                return setup("id=%s %s" % e)
            per_class[c["class"]] += 1
        total = len(cases)
        default_cases = sum(1 for c in cases if class_is_default(c.get("class")))
        default_classes = len({c["class"] for c in cases if class_is_default(c.get("class"))})
        default_null = sum(1 for c in cases
                           if class_is_default(c.get("class")) and c.get("path", []) is None)

        # ---- 7b: the oracle renderer is the one materialiser (M98-8).  It must hash to BOTH
        # envelope pins; the counter importlib-loads it and drives build_root / path_string /
        # sub_placeholders from there on.  Search: beside the cases file, then the round-99
        # controls directory (the declaration names that file as the only renderer).
        rs = cases_data["renderer_sha256"]
        cands = [os.path.join(os.path.dirname(os.path.abspath(a.cases)), RENDERER_NAME),
                 os.path.join(a.repo, ".ufo", "waves", "round-99", "controls", RENDERER_NAME)]
        renderer_path = None
        for p in cands:
            if os.path.isfile(p) and sha_file(p) == rs:
                renderer_path = p
                break
        if renderer_path is None:
            return setup("id=setup-renderer-missing %s not found beside the cases file or in the "
                         "round-99 controls (materialisation is the oracle's, M98-8)"
                         % RENDERER_NAME)
        if renderer_path != cands[0] and os.path.dirname(os.path.abspath(a.cases)) != \
                os.path.dirname(renderer_path):
            print("renderer_from=%s" % renderer_path)
        if rs != cases_data["oracle_sha256"]:
            return setup("id=setup-renderer-sha256 renderer_sha256 != oracle_sha256")
        try:
            spec = importlib.util.spec_from_file_location("mado_launchenv_oracle_r99",
                                                          renderer_path)
            oracle_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(oracle_mod)
            for fn in ("build_root", "path_string", "sub_placeholders"):
                if not callable(getattr(oracle_mod, fn, None)):
                    raise RuntimeError("oracle module lacks %s()" % fn)
        except Exception as e:
            return setup("id=setup-renderer-load %s: %s" % (renderer_path, e))
        _BUILDER["mod"] = oracle_mod
        print("renderer_pin=ok renderer_sha256=%s" % rs)
        desktop_name = DESKTOP_FILE
        print("per_class " + " ".join("%s=%d" % (k, per_class[k]) for k in classes))
        print("default_cases=%d default_classes=%d default_null_path_cases=%d"
              % (default_cases, default_classes, default_null))

        # ---- 8: mutant anchors against the candidate's non-selftest prefix
        try:
            with open(a.mutants, encoding="utf-8") as fh:
                mutants_data = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            return setup("id=setup-mutants-parse %s: %s" % (a.mutants, e))
        src_text = tb.decode("utf-8", "surrogateescape")
        prefix_src = non_selftest_prefix(src_text)
        for eid, msg in validate_mutants(mutants_data, prefix_src, classes):
            return setup("id=%s %s" % (eid, msg))
        if "candidate_sha256" in mutants_data \
                and mutants_data["candidate_sha256"] != tool_sha:
            return setup("id=setup-mutants-candidate-sha256 candidate_sha256 %s != tool sha256 "
                         "%s" % (mutants_data["candidate_sha256"], tool_sha))
        if "classes" in mutants_data and tuple(mutants_data["classes"]) != classes:
            return setup("id=setup-mutants-classes mutants classes != the frozen class list")
        file_mutants = list(mutants_data["mutants"])
        # the mandated population: file mutants + the four required probes, deduped on the
        # exact (find, replace) pair
        population = []
        seen_pairs = set()
        for m in list(file_mutants) + [dict(p, expect="kill", class_="required")
                                       for p in REQUIRED_PROBES]:
            key = (m["find"], m["replace"])
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            population.append(m)
        n_no = len(mutants_data.get("not_observable", [])) \
            if isinstance(mutants_data.get("not_observable"), list) else 0
        n_eq = len(mutants_data.get("equivalents", [])) \
            if isinstance(mutants_data.get("equivalents"), list) else 0
        print("mutants_file=%d required=4 dedup_population=%d not_observable=%d equivalents=%d"
              % (len(file_mutants), len(population), n_no, n_eq))

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

        # ---- frozen leg: one invocation per case under the shared case leg
        cases_dir = os.path.join(work, "cases")
        os.makedirs(cases_dir, exist_ok=True)
        oc = run_cases(tool_path, cases, cases_dir, a.jobs, desktop_name)
        for c, (o, det) in zip(cases, oc):
            if o != "ok":
                print("MISMATCH %s detail=%s" % (c["id"], _short(det)))
        correct = sum(1 for o, _d in oc if o == "ok")
        print("cases_total=%d cases_correct=%d" % (total, correct))

        # ---- fresh leg: one generation, seed drawn at measurement (or MADO_R100_FRESH_SEED)
        seed = os.environ.get("MADO_R100_FRESH_SEED") or os.urandom(8).hex()
        try:
            fcases = fresh_cases(a.genseed, seed, work, secret, a.expect_gio_sha256,
                                 cases_data.get("oracle_sha256"), int(a.fresh_count))
        except (RuntimeError, subprocess.TimeoutExpired, OSError) as e:
            return setup("id=setup-fresh-gen %s" % e)
        foc = run_cases(tool_path, fcases, cases_dir, a.jobs, desktop_name)
        fresh_ok = sum(1 for o, _d in foc if o == "ok")
        fresh_total = len(fcases)
        for c, (o, det) in zip(fcases, foc):
            if o != "ok":
                print("FRESH_MISMATCH %s detail=%s" % (c.get("id", "?"), _short(det)))
        print("fresh_seed=%s fresh=%d/%d" % (seed, fresh_ok, fresh_total))

        # ---- mutant leg: a kill needs a NEW wrong answer vs the candidate's own baseline;
        # crashes are crashed_not_killed, never kills
        mutdir = os.path.join(work, "mutants")
        os.makedirs(mutdir)
        with open(os.path.join(mutdir, SIBLING_NAME), "wb") as fh:
            fh.write(sb)
        killed = crashed = survived = unbuildable = 0
        for m in population:
            msrc, why = build_mutant(src_text, prefix_src, m)
            if msrc is None:
                unbuildable += 1
                print("mutant %s unbuildable (%s)" % (m["id"], why))
                continue
            mp = os.path.join(mutdir, TOOL_NAME)
            with open(mp, "w", encoding="utf-8") as fh:
                fh.write(msrc)
            mors = run_cases(mp, cases, cases_dir, a.jobs, desktop_name)
            wrong_ids = [c["id"] for c, (o, _d), (co, _d2) in zip(cases, mors, oc)
                         if o == "wrong" and co == "ok"]
            new_crash = sum(1 for (mo, _d), (co, _d2) in zip(mors, oc)
                            if mo == "crash" and co != "crash")
            if wrong_ids:
                killed += 1
                status = "killed by %s (+%d)" % (wrong_ids[0], len(wrong_ids) - 1)
            elif new_crash:
                crashed += 1
                status = "crashed_not_killed (%d new crash cases)" % new_crash
            else:
                survived += 1
                status = "survived"
            print("mutant %s %s" % (m["id"], status))
        counted = len(population)
        print("mutants_counted=%d mutants_killed=%d crashed_not_killed=%d survived=%d "
              "unbuildable=%d" % (counted, killed, crashed, survived, unbuildable))

        # ---- control_unset_as_empty: the misreading the branch guards against
        csrc, cwhy = build_control(src_text, prefix_src)
        if csrc is None:
            control_ok = -1
            print("control_unset_as_empty unbuildable (%s)" % cwhy)
        else:
            cpath = os.path.join(tdir, CONTROL_NAME)
            with open(cpath, "w", encoding="utf-8") as fh:
                fh.write(csrc)
            coc = run_cases(cpath, cases, cases_dir, a.jobs, desktop_name)
            control_ok = sum(1 for o, _d in coc if o == "ok")
            print("control_unset_as_empty=%d/%d" % (control_ok, total))

        # ---- base leg: the do-nothing control on the round-99 case file, plus behavioural
        # evidence (never a conjunct): how many round-99 cases change answer when the BASE
        # revision's tool reads an unset PATH as empty.
        try:
            with open(base_cases, encoding="utf-8") as fh:
                base_data = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            return setup("id=setup-base-cases-parse %s: %s" % (base_cases, e))
        bcases = base_data.get("cases")
        if not isinstance(bcases, list) or not bcases \
                or not all(isinstance(c, dict) and isinstance(c.get("id"), str)
                           and isinstance(c.get("class"), str) for c in bcases):
            return setup("id=setup-base-cases-shape %s has no usable cases list" % base_cases)
        base_set = sum(1 for c in bcases if class_is_default(c.get("class")))
        bper = {}
        for c in bcases:
            bper[c["class"]] = bper.get(c["class"], 0) + 1
        print("base_cases=%d base_classes=%d base_set_default_cases=%d"
              % (len(bcases), len(bper), base_set))

        base_ok = base_total = -1
        sens = -1
        sens_note = "ok"
        try:
            bdir = os.path.join(work, "basetools")
            os.makedirs(bdir)
            btool = os.path.join(bdir, TOOL_NAME)
            with open(btool, "wb") as fh:
                fh.write(base_tool_b)
            if base_sib_b is not None:
                with open(os.path.join(bdir, SIBLING_NAME), "wb") as fh:
                    fh.write(base_sib_b)
            bsrc = base_tool_b.decode("utf-8", "surrogateescape")
            bprefix = non_selftest_prefix(bsrc)
            bcontrol, bwhy = build_control(bsrc, bprefix)
            if bcontrol is None:
                sens_note = "unavailable:%s" % bwhy
            else:
                bctl = os.path.join(bdir, CONTROL_NAME)
                with open(bctl, "w", encoding="utf-8") as fh:
                    fh.write(bcontrol)
                bo = run_cases(btool, bcases, cases_dir, a.jobs, desktop_name)
                bco = run_cases(bctl, bcases, cases_dir, a.jobs, desktop_name)
                base_total = len(bcases)
                base_ok = sum(1 for o, _d in bo if o == "ok")
                sens = sum(1 for c, (o, _d), (co, _d2) in zip(bcases, bo, bco)
                           if o == "ok" and co != "ok")
        except Exception as e:  # informational leg: degrade loudly, never silently
            sens_note = "unavailable:%s" % str(e)[:80]
        print("base_cases_correct=%d/%d base_branch_sensitive_cases=%s"
              % (base_ok, base_total, sens if sens >= 0 else sens_note))
    finally:
        if work is not None:
            shutil.rmtree(work, ignore_errors=True)
        if secret is not None:
            shutil.rmtree(secret, ignore_errors=True)

    # ---- PRED-C1-r100-v1: exactly the seven declared conjuncts, and no other
    met = [
        ("default_cases", default_cases >= MIN_DEFAULT_CASES),
        ("default_classes", default_classes >= MIN_DEFAULT_CLASSES),
        ("cases", correct == total),
        ("fresh", fresh_ok == fresh_total and fresh_total >= MIN_FRESH),
        ("mutants", killed == counted and counted >= MIN_MUTANTS),
        ("base_set", base_set == 0),
        ("control", 0 <= control_ok < total),
    ]
    ok = all(v for _k, v in met)
    print("%s %s pred=%s rev=%s base_rev=%s "
          "tool_sha256=%s tool_pin=ok execargv_sha256=%s execargv_pin=ok "
          "gio_sha256=%s gio_pin=ok "
          "cases_total=%d cases_correct=%d "
          "default_cases=%d default_classes=%d default_null_path_cases=%d "
          "fresh_total=%d fresh_correct=%d/%d fresh_seed=%s "
          "mutants_counted=%d mutants_killed=%d/%d crashed_not_killed=%d survived=%d "
          "unbuildable=%d "
          "base_set_default_cases=%d "
          "control_unset_as_empty_correct=%d/%d "
          "met=%s static_findings=%s base_cases_correct=%d/%d "
          "base_branch_sensitive_cases=%s"
          % (PREFIX, "TARGET_MET" if ok else "TARGET_MISSED", PRED, a.rev, a.base_rev,
             tool_sha, sib_sha, gio_sha, total, correct,
             default_cases, default_classes, default_null, fresh_total, fresh_ok,
             fresh_total, seed,
             counted, killed, counted, crashed, survived, unbuildable,
             base_set, control_ok, total,
             ",".join("%s:%d" % (k, 1 if v else 0) for k, v in met),
             ",".join(static_bad) or "none",
             base_ok if base_ok >= 0 else -1, base_total if base_total >= 0 else -1,
             sens if sens >= 0 else sens_note))
    return 0 if ok else 1


# ================================================================ counter selftest

_ST_IDS = ("st-fixture-build", "st-target-met", "st-result-line-format",
           "st-conjuncts-listed", "st-tool-pin", "st-execargv-pin", "st-cases-pin",
           "st-mutants-pin", "st-genseed-pin", "st-gio-pin", "st-setup-missing",
           "st-renderer-missing", "st-base-tool-absent", "st-rev-not-commit",
           "st-case-mismatch", "st-mutant-survives", "st-mutant-crash",
           "st-required-probe-unbuildable", "st-base-set-control-fails",
           "st-default-cases-floor", "st-fresh-seed-override", "st-fresh-seed-random",
           "st-unset-branch-discriminated", "st-scratch-clean")

# The mini sibling: the module the mini candidate would load by path (contract 1's sibling
# load).  The mini candidate does not need it, but the counter requires and pins it.
MINI_SIBLING_SRC = r'''"""mado-execargv mini sibling (counter selftest fixture)."""
MARK = "mini-sibling-r100"


def expand_argv(exec_value, files):
    return exec_value.split() + list(files)
'''

# The mini candidate: the candidate's real find_program (the exact anchors the four required
# probes mutate) plus a minimal load-time gate and JSON surface.  It is NOT the frozen
# candidate; it exists so the counter's legs have a correct instrument to score.
MINI_TOOL_SRC = r'''#!/usr/bin/env python3
"""Mini launchenv model for the round-100 counter selftest (not the frozen candidate)."""
import json
import os
import sys

MARK = "mado-mini-launchenv-r100"
PROCESS_PATH = object()

DEFAULT_SEARCH_PATH = '/bin:/usr/bin:.'

SIBLING_NAME = 'mado-execargv.py'


def _is_abs(p):
    return p.startswith('/')


def _join2(a, b):
    out = str(a)
    while len(out) > 1 and out.endswith('/'):
        out = out[:-1]
    if out and not out.endswith('/') and not b.startswith('/'):
        out += '/'
    return out + b


def _exec_file(p):
    return os.access(p, os.X_OK) and not os.path.isdir(p)


def find_program(program, path, working_dir):
    original_program = program
    if working_dir is not None and not _is_abs(program):
        program = _join2(working_dir, program)
    if _is_abs(program) or '/' in original_program:
        if _exec_file(program):
            if _is_abs(program):
                return program
            return _join2(os.getcwd(), program)
        if _is_abs(original_program):
            return None
    program = original_program
    if path is None:
        path = DEFAULT_SEARCH_PATH
    i = 0
    n = len(path)
    while True:
        j = path.find(':', i)
        end = n if j < 0 else j
        entry = path[i:end]
        if entry == '':
            startp = program
        else:
            startp = entry + '/' + program
        if working_dir is not None and not _is_abs(startp):
            startp = _join2(working_dir, startp)
        if _exec_file(startp):
            if _is_abs(startp):
                return startp
            return _join2(os.getcwd(), startp)
        if j < 0:
            break
        i = j + 1
    return None


def read_values(path):
    vals = {}
    try:
        data = open(path, 'rb').read().decode('utf-8', 'surrogateescape')
    except OSError:
        return None
    for line in data.splitlines():
        if '=' in line and not line.startswith('[') and not line.startswith('#'):
            k, v = line.split('=', 1)
            vals[k] = v
    return vals


def main():
    av = sys.argv[1:]
    as_json = '--json' in av
    av = [x for x in av if x != '--json']
    if av and av[0] == '--selftest':
        sys.stdout.write('MADO_LAUNCHENV_SELFTEST: checks=1 failed=0\n')
        return 0
    path_env = PROCESS_PATH
    if '--path' in av:
        i = av.index('--path')
        path_env = av[i + 1]
        del av[i:i + 2]
    if not av:
        return 2
    desktop, files = av[0], av[1:]
    vals = read_values(desktop)
    if vals is None:
        if as_json:
            sys.stdout.write(json.dumps({'error': 'desktop-file', 'detail': 'unreadable'}) + '\n')
        return 2
    wd = vals.get('Path')
    exec_v = vals.get('Exec')
    if exec_v is None:
        if as_json:
            sys.stdout.write(json.dumps({'error': 'no-exec', 'detail': 'missing'}) + '\n')
        return 2
    static = exec_v.split()
    if path_env is PROCESS_PATH:
        path_env = os.environ.get('PATH')
    if not static:
        if as_json:
            sys.stdout.write(json.dumps({'error': 'no-exec', 'detail': 'empty'}) + '\n')
        return 2
    found = find_program(static[0], path_env, wd)
    if found is None:
        if as_json:
            sys.stdout.write(json.dumps({'error': 'load', 'detail': 'exec-argv0'}) + '\n')
        return 2
    argv = [found] + static[1:] + list(files)
    cwd = wd if wd else os.getcwd()
    if as_json:
        sys.stdout.write(json.dumps({'launches': 1, 'terminal': '-', 'cwd': cwd,
                                     'argv': [argv],
                                     'env': {'GIO_LAUNCHED_DESKTOP_FILE': desktop}}) + '\n')
    return 0


def selftest():
    return 0


if __name__ == '__main__':
    sys.exit(main())
'''

# The mini fresh generator: the frozen generator's interface --seed/--dir/--out/--count, JSONL
# case dicts on --out, a FRESH_GEN summary and a FRESH_GEN_PIN line carrying the pinned gio
# sha256 (hand-derived labels; roots are transient and removed).
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
    n = max(1, min(int(a.count), 2))
    lines = []
    root = os.path.abspath(a.dir)
    for i in range(n):
        cid = "fresh-%s-%02d" % (a.seed[:8], i)
        d = os.path.join(root, cid)
        os.makedirs(os.path.join(d, "h"), exist_ok=True)
        with open(os.path.join(d, "prog.sh"), "wb") as f:
            f.write(PROG)
        os.chmod(os.path.join(d, "prog.sh"), 0o755)
        if i == 0:
            case = {"id": cid, "class": "fresh",
                    "path": None,
                    "files": {"prog.sh": base64.b64encode(PROG).decode("ascii")},
                    "desktop": {"Type": "Application", "Name": "M",
                                "Exec": "prog.sh"},
                    "expect": {"launches": 1,
                               "argv": [["{root}/./prog.sh"]],
                               "cwd": "{root}",
                               "env_gdf": "{root}/case.desktop"},
                    "label": "unset-default-dot"}
        else:
            case = {"id": cid, "class": "fresh",
                    "path": ["bin"],
                    "files": {"bin/prog.sh": base64.b64encode(PROG).decode("ascii")},
                    "dirs": ["work"],
                    "desktop": {"Type": "Application", "Name": "M",
                                "Exec": "{root}/bin/prog.sh", "Path": "{root}/work"},
                    "expect": {"launches": 1,
                               "argv": [["{root}/bin/prog.sh"]],
                               "cwd": "{root}/work",
                               "env_gdf": "{root}/case.desktop"},
                    "label": "plain"}
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
# pinned by both envelope pins, so the production load-and-verify path is what the selftest
# exercises.
MINI_ORACLE_SRC = r'''"""Mini oracle builder (counter selftest fixture; same surface as
launchenv-probe-r99.py build_root/path_string/sub_placeholders)."""
import base64
import os
import shutil

ORACLE_TAG = "ORACLETAG"


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
    modes = case.get("modes") or {}
    for rel, octal in sorted(modes.items()):
        os.chmod(os.path.join(root, rel), int(octal, 8))
    probe = os.path.join(root, "probe.sh")
    with open(probe, "w", encoding="ascii", newline="\n") as fh:
        fh.write("#!/bin/sh\ntrue\n")
    os.chmod(probe, 0o755)
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

MINI_CLASSES = ["path-default-unset-vs-empty", "path-default-vs-ambient",
                "path-default-dot-real", "plain"]


def _b64(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("ascii")


def _mini_frozen_cases() -> list:
    """The mini frozen cases: three path-default discriminator classes (each one kills a
    different required probe) plus two plain cases."""
    prog = _b64("#!/bin/sh\ntrue\n")
    return [
        # dot-real: bare program at the launch working directory (== process cwd), PATH absent.
        # kills m1 (no trailing dot) and m2 (unset as empty)
        {"id": "pd-dot", "class": "path-default-dot-real", "path": None,
         "files": {"prog.sh": prog},
         "desktop": {"Type": "Application", "Name": "M", "Exec": "prog.sh"},
         "expect": {"launches": 1, "argv": [["{root}/./prog.sh"]],
                    "cwd": "{root}", "env_gdf": "{root}/case.desktop"}},
        # vs-ambient: a case-private bin dir reached through a RELATIVE PATH entry, so the
        # walk's working-dir join is load-bearing.  kills m3
        {"id": "pd-ambient", "class": "path-default-vs-ambient", "path": ["bin"],
         "files": {"work/bin/prog.sh": prog},
         "desktop": {"Type": "Application", "Name": "M", "Exec": "prog.sh",
                     "Path": "{root}/work"},
         "expect": {"launches": 1, "argv": [["{root}/work/bin/prog.sh"]],
                    "cwd": "{root}/work", "env_gdf": "{root}/case.desktop"}},
        # unset-vs-empty: PATH set but EMPTY (one empty entry = cwd).  kills m4
        {"id": "pd-empty", "class": "path-default-unset-vs-empty", "path": [""],
         "files": {"prog.sh": prog},
         "desktop": {"Type": "Application", "Name": "M", "Exec": "prog.sh"},
         "expect": {"launches": 1, "argv": [["{root}/prog.sh"]],
                    "cwd": "{root}", "env_gdf": "{root}/case.desktop"}},
        # the same fixture with a working directory that differs from the process cwd: the
        # default dot entry joins to the working dir, so the bare program is NOT found (the
        # discriminator the "trailing dot" class is built from)
        {"id": "pd-empty-vs-dot", "class": "path-default-unset-vs-empty", "path": None,
         "files": {"prog.sh": prog},
         "dirs": ["work"],
         "desktop": {"Type": "Application", "Name": "M", "Exec": "prog.sh",
                     "Path": "{root}/work"},
         "expect": {"error": "load"}},
        {"id": "plain-01", "class": "plain", "path": ["bin"],
         "files": {"bin/prog.sh": prog},
         "dirs": ["work"],
         "desktop": {"Type": "Application", "Name": "M", "Exec": "{root}/bin/prog.sh",
                     "Path": "{root}/work"},
         "expect": {"launches": 1, "argv": [["{root}/bin/prog.sh"]],
                    "cwd": "{root}/work", "env_gdf": "{root}/case.desktop"}},
        {"id": "plain-02", "class": "plain", "path": [""],
         "files": {"prog.sh": prog},
         "desktop": {"Type": "Application", "Name": "M", "Exec": "nosuch-prog"},
         "expect": {"error": "load"}},
    ]


def _mini_plain_cases() -> list:
    """A case file with NO path-default class: the default-cases floor must miss."""
    return [c for c in _mini_frozen_cases() if c["class"] == "plain"]


def _mini_bad_cases() -> list:
    """The frozen mini cases with one label corrupted: correct answers, a wrong label -> a miss."""
    cases = _mini_frozen_cases()
    cases[5]["expect"] = {"error": "no-exec"}
    return cases


def _mini_base_cases() -> list:
    """The round-99-style base case file: absolute Exec + absolute Path, so no case depends on
    the unset-default branch.  base_set_default_cases must measure 0 here."""
    prog = _b64("#!/bin/sh\ntrue\n")
    return [
        {"id": "pu-abs-root", "class": "path-unset", "path": None,
         "files": {"prog.sh": prog},
         "desktop": {"Type": "Application", "Name": "M", "Exec": "{root}/prog.sh"},
         "expect": {"launches": 1, "argv": [["{root}/prog.sh"]],
                    "cwd": "{root}", "env_gdf": "{root}/case.desktop"}},
        {"id": "pu-abs-work", "class": "path-unset", "path": None,
         "files": {"prog.sh": prog},
         "desktop": {"Type": "Application", "Name": "M", "Exec": "{root}/prog.sh",
                     "Path": "{root}/work"},
         "expect": {"launches": 1, "argv": [["{root}/prog.sh"]],
                    "cwd": "{root}/work", "env_gdf": "{root}/case.desktop"}},
    ]


def _mini_base_cases_fail() -> list:
    """A base case file that DOES carry a path-default case: the do-nothing control must miss."""
    cases = _mini_base_cases()
    extra = dict(cases[0])
    extra["id"] = "pd-preexisting"
    extra["class"] = "path-default-dot-real"
    cases.append(extra)
    return cases


def _mini_mutants(kind: str, tool_sha: str, classes) -> dict:
    base = {"version": 1, "tool": TOOL, "candidate_sha256": tool_sha,
            "classes": list(classes),
            "mutants": [
                {"id": "plain-01-cwd-dropped",
                 "find": "    wd = vals.get('Path')\n",
                 "replace": "    wd = None\n", "class": "plain", "expect": "kill"},
                {"id": "dot-return-relative",
                 "find": "            return _join2(os.getcwd(), startp)",
                 "replace": "            return startp",
                 "class": "path-default-dot-real", "expect": "kill"}],
            "not_observable": [], "equivalents": []}
    if kind == "survive":
        base["mutants"].append({"id": "mark-unused",
                                "find": 'MARK = "mado-mini-launchenv-r100"',
                                "replace": 'MARK = "mado-mini-launchenv-r100x"',
                                "class": "plain", "expect": "kill"})
    elif kind == "crash":
        base["mutants"].append({"id": "plain-02-syntax",
                                "find": "def read_values(path):",
                                "replace": "def read_values(path key):",
                                "class": "plain", "expect": "kill"})
    return base


def _st_git(args: list, cwd: str):
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)


def _st_write(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, bytes):
        with open(path, "wb") as fh:
            fh.write(data)
    else:
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(data)


def _st_build_repo(fx: str, tag: str, tool_src: str, tool_at_base: bool) -> dict:
    """A two-commit fixture repo whose base commit already carries the mini candidate (the
    round-100 before-state).  With tool_at_base=False the base commit has no tool at all."""
    repo = os.path.join(fx, "repo-" + tag)
    os.makedirs(repo)
    _st_git(["init", "-q"], repo)
    if tool_at_base:
        # the base commit carries a behaviourally identical tool so the round-100 before-state
        # (the branch is modelled at base) is real AND the candidate commit has a diff to land
        base_src = tool_src.replace('MARK = "mado-mini-launchenv-r100"',
                                    'MARK = "mado-mini-launchenv-r100-base"')
        _st_write(os.path.join(repo, TOOL), base_src.encode("utf-8"))
        _st_write(os.path.join(repo, SIBLING), MINI_SIBLING_SRC.encode("utf-8"))
    else:
        _st_write(os.path.join(repo, "README"), "mini base\n")
    _st_git(["add", "-A"], repo)
    _st_git(["-c", "user.name=mado-selftest", "-c", "user.email=selftest@mado",
             "commit", "-q", "-m", "base"], repo)
    _st_write(os.path.join(repo, TOOL), tool_src.encode("utf-8"))
    _st_write(os.path.join(repo, SIBLING), MINI_SIBLING_SRC.encode("utf-8"))
    _st_git(["add", "-A"], repo)
    _st_git(["-c", "user.name=mado-selftest", "-c", "user.email=selftest@mado",
             "commit", "-q", "-m", "candidate"], repo)
    top = _st_git(["rev-parse", "--show-toplevel"], repo).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(repo):
        raise RuntimeError("fixture repo toplevel %s != %s" % (top, repo))
    return {"repo": repo, "rev": _st_git(["rev-parse", "HEAD"], repo).stdout.strip(),
            "base_rev": _st_git(["rev-parse", "HEAD~1"], repo).stdout.strip(),
            "tool_sha": sha(tool_src.encode("utf-8"))}


def _st_build_fixtures(root: str, gio_sha: str) -> dict:
    fx = os.path.join(root, "fixtures")
    os.makedirs(fx)
    r1 = _st_build_repo(fx, "green", MINI_TOOL_SRC, tool_at_base=True)
    r2 = _st_build_repo(fx, "nobase", MINI_TOOL_SRC, tool_at_base=False)
    # a candidate whose DEFAULT_SEARCH_PATH literal is rewritten, so the m1 required probe has
    # no anchor and cannot be built
    broken = MINI_TOOL_SRC.replace("DEFAULT_SEARCH_PATH = '/bin:/usr/bin:.'",
                                   "DEFAULT_SEARCH_PATH = '/bin' + ':/usr/bin:.'")
    r3 = _st_build_repo(fx, "noanchor", broken, tool_at_base=True)

    def dump(name: str, obj) -> tuple:
        p = os.path.join(fx, name)
        _st_write(p, json.dumps(obj, indent=1, sort_keys=True) + "\n")
        return p, sha_file(p)

    oracle_src = MINI_ORACLE_SRC.replace("ORACLETAG", "mini-oracle-r100")
    renderer_sha = sha(oracle_src.encode("utf-8"))
    _st_write(os.path.join(fx, RENDERER_NAME), oracle_src)
    env = {"version": 1, "round": "r100", "oracle": ORACLE_NAME, "gio_sha256": gio_sha,
           "glib2": GLIB, "renderer_sha256": renderer_sha, "oracle_sha256": renderer_sha,
           "classes": MINI_CLASSES}
    cases_path, cases_sha = dump("cases-mini.json", dict(env, cases=_mini_frozen_cases()))
    bad_path, bad_sha = dump("cases-mini-bad.json", dict(env, cases=_mini_bad_cases()))
    floor_path, floor_sha = dump("cases-mini-floor.json", dict(env, cases=_mini_plain_cases()))
    nr = os.path.join(fx, "norenderer")
    os.makedirs(nr, exist_ok=True)
    norenderer_path, norenderer_sha = dump(os.path.join("norenderer", "cases-mini.json"),
                                           dict(env, cases=_mini_frozen_cases()))
    tool_sha = sha(MINI_TOOL_SRC.encode("utf-8"))
    muts_path, muts_sha = dump("mutants-mini.json",
                               _mini_mutants("kill", tool_sha, MINI_CLASSES))
    muts2_path, muts2_sha = dump("mutants-mini2.json",
                                 _mini_mutants("survive", tool_sha, MINI_CLASSES))
    muts3_path, muts3_sha = dump("mutants-mini3.json",
                                 _mini_mutants("crash", tool_sha, MINI_CLASSES))
    # a mutant file written for the noanchor candidate (candidate_sha256 binds the bytes)
    muts4_path, muts4_sha = dump("mutants-mini-noanchor.json",
                                 _mini_mutants("kill", r3["tool_sha"], MINI_CLASSES))
    base_path, base_sha = dump("base-cases-mini.json",
                               {"version": 1, "round": "r99", "oracle": ORACLE_NAME,
                                "gio_sha256": gio_sha, "glib2": GLIB,
                                "renderer_sha256": renderer_sha,
                                "oracle_sha256": renderer_sha,
                                "classes": ["path-unset"], "cases": _mini_base_cases()})
    basef_path, basef_sha = dump("base-cases-mini-fail.json",
                                 {"version": 1, "round": "r99", "oracle": ORACLE_NAME,
                                  "gio_sha256": gio_sha, "glib2": GLIB,
                                  "renderer_sha256": renderer_sha,
                                  "oracle_sha256": renderer_sha,
                                  "classes": ["path-unset", "path-default-dot-real"],
                                  "cases": _mini_base_cases_fail()})
    gen_path = os.path.join(fx, "launchenv-fresh-mini.py")
    _st_write(gen_path, MINI_GEN_SRC.replace("GIOSHA", gio_sha)
              .replace("GENORACLE", renderer_sha))
    return {"repo": r1["repo"], "rev": r1["rev"], "base_rev": r1["base_rev"],
            "repo_nobase": r2["repo"], "rev_nobase": r2["rev"],
            "base_rev_nobase": r2["base_rev"],
            "repo_noanchor": r3["repo"], "rev_noanchor": r3["rev"],
            "base_rev_noanchor": r3["base_rev"], "tool_sha_noanchor": r3["tool_sha"],
            "tool_sha": tool_sha,
            "sibling_sha": sha(MINI_SIBLING_SRC.encode("utf-8")),
            "norenderer": norenderer_path, "norenderer_sha": norenderer_sha,
            "gio_sha": gio_sha, "cases": cases_path, "cases_sha": cases_sha,
            "bad_cases": bad_path, "bad_cases_sha": bad_sha,
            "floor_cases": floor_path, "floor_cases_sha": floor_sha,
            "mutants": muts_path, "mutants_sha": muts_sha,
            "mutants2": muts2_path, "mutants2_sha": muts2_sha,
            "mutants3": muts3_path, "mutants3_sha": muts3_sha,
            "mutants_noanchor": muts4_path, "mutants_noanchor_sha": muts4_sha,
            "base_cases": base_path, "base_cases_sha": base_sha,
            "base_cases_fail": basef_path, "base_cases_fail_sha": basef_sha,
            "genseed": gen_path, "genseed_sha": sha_file(gen_path)}


def _mado_counter_selftest(argv: list) -> int:
    scratch = None
    for i, tok in enumerate(argv):
        if tok == "--scratch-root" and i + 1 < len(argv):
            scratch = argv[i + 1]
    try:
        if scratch:
            os.makedirs(scratch, exist_ok=True)
            root = tempfile.mkdtemp(prefix="c1r100-selftest-", dir=scratch)
        else:
            root = tempfile.mkdtemp(prefix="c1r100-selftest-")
    except OSError as e:
        print("%scould-not-evaluate scratch: %s" % (ST_PREFIX, e))
        return 2
    checks = []
    failed = []

    def check(cid: str, ok: bool) -> None:
        checks.append(cid)
        if not ok:
            failed.append(cid)
            print(ST_FAIL + cid)

    try:
        if not (os.path.isfile(GIO) and os.access(GIO, os.X_OK)):
            print("%scould-not-evaluate %s missing" % (ST_PREFIX, GIO))
            return 2
        gio_sha = sha_file(GIO)
        try:
            fx = _st_build_fixtures(root, gio_sha)
        except Exception as e:
            print("%scould-not-evaluate fixtures: %s" % (ST_PREFIX, e))
            return 2
        check("st-fixture-build", all(os.path.exists(fx[k]) for k in
                                      ("repo", "cases", "mutants", "genseed", "base_cases")))

        self_path = os.path.abspath(__file__)

        def run_mini(tag: str, repo=None, rev=None, base_rev=None, cases=None,
                     cases_sha=None, mutants=None, mutants_sha=None, tool_sha=None,
                     sib_sha=None, gio=None, base_cases=None, base_cases_sha=None,
                     env_extra=None, extra=()) -> tuple:
            scr = os.path.join(root, "scr-" + tag)
            os.makedirs(scr, exist_ok=True)
            env = dict(os.environ)
            env.pop("MADO_R100_FRESH_SEED", None)
            if env_extra:
                env.update(env_extra)
            cmd = [sys.executable, "-I", self_path,
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
                   "--base-cases", base_cases or fx["base_cases"],
                   "--expect-base-cases-sha256", base_cases_sha or fx["base_cases_sha"],
                   "--scratch-root", scr, "--mini-scale"] + list(extra)
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=300,
                               cwd=root, env=env)
            return r.returncode, r.stdout + r.stderr

        def result_line(out: str) -> str:
            return next((ln for ln in out.splitlines() if ln.startswith(PREFIX)), "")

        rc, out = run_mini("green")
        line = result_line(out)
        fm = re.search(r"fresh_correct=(\d+)/(\d+)", line)
        dm = re.search(r"mutants_killed=(\d+)/(\d+)", line)
        check("st-target-met", rc == 0 and "TARGET_MET" in line and "cases_correct=6" in line
              and dm is not None and dm.group(1) == dm.group(2)
              and fm is not None and fm.group(1) == fm.group(2))
        check("st-result-line-format",
              line.startswith(PREFIX + " TARGET_MET pred=" + PRED + " "))
        check("st-conjuncts-listed", all(k in line for k in
                                         ("default_cases=", "default_classes=",
                                          "cases_correct=", "fresh_correct=",
                                          "mutants_killed=", "base_set_default_cases=",
                                          "control_unset_as_empty_correct=")))
        check("st-unset-branch-discriminated",
              "default_cases=4" in line and "default_null_path_cases=2" in line
              and re.search(r"control_unset_as_empty_correct=(-?\d+)/", line) is not None
              and int(re.search(r"control_unset_as_empty_correct=(-?\d+)/",
                                line).group(1)) < 6)

        rc, out = run_mini("badtool", tool_sha="0" * 64)
        check("st-tool-pin", rc == 2 and "SETUP_ERROR" in out)
        rc, out = run_mini("badsib", sib_sha="1" * 64)
        check("st-execargv-pin", rc == 2 and "SETUP_ERROR" in out)
        rc, out = run_mini("badcases", cases_sha="2" * 64)
        check("st-cases-pin", rc == 2 and "SETUP_ERROR" in out)
        rc, out = run_mini("badmutants", mutants_sha="3" * 64)
        check("st-mutants-pin", rc == 2 and "SETUP_ERROR" in out)
        # the genseed pin is checked through a wrong --expect-genseed-sha256
        scr = os.path.join(root, "scr-badgen")
        os.makedirs(scr, exist_ok=True)
        cmd = [sys.executable, "-I", self_path,
               "--repo", fx["repo"], "--rev", fx["rev"], "--base-rev", fx["base_rev"],
               "--cases", fx["cases"], "--expect-cases-sha256", fx["cases_sha"],
               "--mutants", fx["mutants"], "--expect-mutants-sha256", fx["mutants_sha"],
               "--genseed", fx["genseed"], "--expect-genseed-sha256", "4" * 64,
               "--expect-tool-sha256", fx["tool_sha"],
               "--expect-execargv-sha256", fx["sibling_sha"],
               "--expect-gio-sha256", gio_sha,
               "--base-cases", fx["base_cases"],
               "--scratch-root", scr, "--mini-scale"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=root)
        check("st-genseed-pin", r.returncode == 2 and "SETUP_ERROR" in r.stdout)
        rc, out = run_mini("badgio", gio="5" * 64)
        check("st-gio-pin", rc == 2 and "SETUP_ERROR" in out)
        rc, out = run_mini("missing", cases=os.path.join(os.path.dirname(fx["cases"]),
                                                         "no-such.json"),
                           cases_sha="6" * 64)
        check("st-setup-missing", rc == 2 and "SETUP_ERROR" in out)
        rc, out = run_mini("norenderer", cases=fx["norenderer"],
                           cases_sha=fx["norenderer_sha"])
        check("st-renderer-missing", rc == 2 and "setup-renderer-missing" in out)
        rc, out = run_mini("nobase", repo=fx["repo_nobase"], rev=fx["rev_nobase"],
                           base_rev=fx["base_rev_nobase"])
        check("st-base-tool-absent", rc == 2 and "setup-base-tool-absent" in out)
        rc, out = run_mini("notcommit", rev="9" * 40)
        check("st-rev-not-commit", rc == 2 and "setup-rev-not-commit" in out)

        rc, out = run_mini("badcase", cases=fx["bad_cases"], cases_sha=fx["bad_cases_sha"])
        line = result_line(out)
        check("st-case-mismatch", rc == 1 and "TARGET_MISSED" in line
              and "cases_correct=5" in line)

        rc, out = run_mini("survive", mutants=fx["mutants2"], mutants_sha=fx["mutants2_sha"])
        line = result_line(out)
        check("st-mutant-survives", rc == 1 and "TARGET_MISSED" in line
              and "survived=1" in line)

        rc, out = run_mini("crash", mutants=fx["mutants3"], mutants_sha=fx["mutants3_sha"])
        line = result_line(out)
        check("st-mutant-crash", rc == 1 and "TARGET_MISSED" in line
              and "crashed_not_killed=1" in line)

        rc, out = run_mini("noanchor", repo=fx["repo_noanchor"], rev=fx["rev_noanchor"],
                           base_rev=fx["base_rev_noanchor"],
                           tool_sha=fx["tool_sha_noanchor"],
                           mutants=fx["mutants_noanchor"],
                           mutants_sha=fx["mutants_noanchor_sha"])
        line = result_line(out)
        check("st-required-probe-unbuildable", rc == 1 and "TARGET_MISSED" in line
              and "unbuildable=1" in line)

        rc, out = run_mini("basefail", base_cases=fx["base_cases_fail"],
                           base_cases_sha=fx["base_cases_fail_sha"])
        line = result_line(out)
        check("st-base-set-control-fails", rc == 1 and "TARGET_MISSED" in line
              and "base_set_default_cases=1" in line)

        rc, out = run_mini("floor", cases=fx["floor_cases"], cases_sha=fx["floor_cases_sha"])
        line = result_line(out)
        check("st-default-cases-floor", rc == 1 and "TARGET_MISSED" in line
              and "default_cases=0" in line and "met=default_cases:0" in line)

        seed_hex = "0a1b2c3d4e5f6071"
        rc, out = run_mini("seedenv", env_extra={"MADO_R100_FRESH_SEED": seed_hex})
        check("st-fresh-seed-override", rc == 0 and ("fresh_seed=%s" % seed_hex) in out)
        rc, out = run_mini("seedrand")
        m = re.search(r"fresh_seed=([0-9a-f]+)", out)
        check("st-fresh-seed-random", rc == 0 and m is not None and len(m.group(1)) == 16)

        leftover = [d for d in os.listdir(os.path.join(root, "scr-green"))
                    if d.startswith("c1r100-")]
        check("st-scratch-clean", leftover == [])
    finally:
        shutil.rmtree(root, ignore_errors=True)

    for cid in _ST_IDS:
        if cid not in checks:
            failed.append(cid)
            print(ST_FAIL + cid)
    print("%schecks=%d failed=%d" % (ST_PREFIX, len(checks), len(failed)))
    return 0 if not failed else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(_mado_counter_selftest(sys.argv[1:]))
    sys.exit(main())
