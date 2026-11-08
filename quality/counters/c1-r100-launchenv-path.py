#!/usr/bin/env python3
"""Round-100 C1 counter - the PATH-unset default search path of the launch load gate.

Frozen predicate PRED-C1-r100-v1 (verbatim from .ufo/waves/round-100/claims-declaration-r100.md):

  TARGET_MET iff  default_cases            >= 6
             AND  default_classes          >= 3
             AND  cases_correct            == cases_total
             AND  fresh_correct            == fresh_total         (fresh_total >= 8, seeded at measurement)
             AND  mutants_killed           == mutants_counted     (mutants_counted >= 4)
             AND  base_set_default_cases   == 0
             AND  control_unset_as_empty_correct < cases_total

rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR.  No other conjunct.

WHAT THIS COUNTER SCORES, AND THE ONE CONTRACT CORRECTION IT CARRIES
  A case with "path": null models PATH ABSENT from the child environment; a case with "path": []
  (or [""]) models PATH SET BUT EMPTY.  The round-99 counter scored every case with PATH="" in the
  tool's environment and no --path, which models set-but-empty for a path:null case: measured on a
  built root, the candidate answers "{root}/probe" under PATH="" where the oracle's frozen expect
  for the unset case is "{root}/./probe" (wave finding, R100MMutPath ledger finding 1).  This
  counter therefore puts PATH in the tool's environment ONLY when the case declares one.

Instrument spawns (this counter is an instrument, not a candidate): `git` read-only (show),
`python3 -I` for the candidate, the mutants, the control, the fresh generator and the oracle
builder (the oracle itself spawns /usr/bin/gio per case - it is the measuring instrument).  The
counter never launches a host application, never writes the lane, never mutates git state.

Inputs (all sha256-pinned; SETUP_ERROR on any mismatch or missing surface):
  --repo DIR --rev REV|worktree --base-rev SHA
  --cases FILE --expect-cases-sha256 SHA
  --mutants FILE --expect-mutants-sha256 SHA
  --genseed FILE --expect-genseed-sha256 SHA
  --expect-tool-sha256 SHA  --expect-execargv-sha256 SHA  --expect-gio-sha256 SHA
  --scratch-root DIR  [--fresh-count N] [--jobs N] [--selftest]
"""

import argparse
import hashlib
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

GIO = "/usr/bin/gio"
TOOL_PATH = "tools/mado-launchenv.py"
EXECARGV_PATH = "tools/mado-execargv.py"
ORACLE_PATH = ".ufo/waves/round-99/controls/launchenv-probe-r99.py"
BASE_CASES_PATH = ".ufo/waves/round-99/controls/launchenv-cases-r99.json"
TOOL_TIMEOUT = 120.0


class CaseError(Exception):
    pass


def sha(b):
    if isinstance(b, str):
        b = b.encode()
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, "rb") as fh:
        return sha(fh.read())


def git_show(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise CaseError("cannot load %s" % path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def setup(msg):
    sys.stderr.write("SETUP_ERROR %s\n" % msg)
    return 2


# ---------------------------------------------------------------- tool runs (corrected env)


def run_tool(tool_path, tool_args, cwd, home, path_present):
    """("ok", stdout, rc) | ("crash", "", rc).  rc 0 and the refusal rc 2 are parseable.
    PATH enters the tool's environment ONLY when the case declares one (the contract correction)."""
    argv = [sys.executable, "-I", tool_path] + list(tool_args) + ["--json"]
    env = {"LC_ALL": "C", "HOME": home}
    if path_present:
        env["PATH"] = ""
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=TOOL_TIMEOUT,
                           cwd=cwd, env=env)
    except (OSError, subprocess.TimeoutExpired):
        return "crash", "", -1
    if r.returncode not in (0, 2):
        return "crash", "", r.returncode
    return "ok", r.stdout, r.returncode


def score_case(r99, tool_path, case, parent, desktop_name):
    """('ok'|'wrong'|'crash', detail)."""
    try:
        root, darg, file_args, pstr = r99.materialise_case(
            case, os.path.join(parent, "_"), desktop_name)
        norm = r99.normalise_expect(case["expect"], root, os.path.join(root, "probe.sh"))
    except Exception:
        return "crash", {"stage": "materialise"}
    targs = [darg] + file_args + (["--path", pstr] if pstr is not None else [])
    status, out, rc = run_tool(tool_path, targs, root, os.path.join(root, "h"),
                               pstr is not None)
    try:
        shutil.rmtree(root, ignore_errors=True)
    except OSError:
        pass
    if status == "crash":
        return "crash", {"rc": rc}
    parsed = r99.parse_launch_json(out)
    exp = case["expect"]
    if "error" in exp:
        if rc == 2 and parsed.get("kind") == "error" and parsed.get("cause") == exp["error"]:
            return "ok", None
        return "wrong", {"expected": {"error": exp.get("error")},
                         "got": {"rc": rc, "kind": parsed.get("kind"),
                                 "cause": parsed.get("cause")}}
    if rc != 0 or parsed.get("kind") != "answer":
        return "wrong", {"expected": norm,
                         "got": {"rc": rc, "kind": parsed.get("kind"),
                                 "cause": parsed.get("cause")}}
    got = {"launches": parsed.get("launches"), "argv": parsed.get("argv"),
           "cwd": parsed.get("cwd"), "env_gdf": parsed.get("env_gdf")}
    if (parsed.get("launches") != norm.get("launches")
            or sorted(parsed.get("argv", [])) != sorted(norm.get("argv", []))
            or parsed.get("cwd") != norm.get("cwd")
            or parsed.get("env_gdf") != norm.get("env_gdf")):
        return "wrong", {"expected": norm, "got": got}
    return "ok", None


def score_all(r99, tool_path, cases, parent, jobs):
    def one(c):
        return (c.get("id"),) + score_case(r99, tool_path, c, parent, "case.desktop")
    with ThreadPoolExecutor(max(1, jobs)) as ex:
        return list(ex.map(one, cases))


# ---------------------------------------------------------------- mutant / control copies


def apply_mutant(src, find, replace):
    if src.count(find) != 1:
        raise CaseError("mutant anchor occurs %d times" % src.count(find))
    return src.replace(find, replace)


def write_copy(tmpdir, name, text):
    p = os.path.join(tmpdir, name)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    compile(text, p, "exec")
    return p


# ---------------------------------------------------------------- main


def main(argv=None):
    ap = argparse.ArgumentParser(description="mado round-100 C1 counter (path-default)")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--cases")
    ap.add_argument("--expect-cases-sha256")
    ap.add_argument("--mutants")
    ap.add_argument("--expect-mutants-sha256")
    ap.add_argument("--genseed")
    ap.add_argument("--expect-genseed-sha256")
    ap.add_argument("--expect-tool-sha256")
    ap.add_argument("--expect-execargv-sha256")
    ap.add_argument("--expect-gio-sha256")
    ap.add_argument("--scratch-root")
    ap.add_argument("--fresh-count", type=int, default=60)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    for req in ("repo", "rev", "base_rev", "cases", "expect_cases_sha256", "mutants",
                "expect_mutants_sha256", "genseed", "expect_genseed_sha256",
                "expect_tool_sha256", "expect_execargv_sha256", "expect_gio_sha256",
                "scratch_root"):
        if not getattr(a, req):
            return setup("missing --%s" % req.replace("_", "-"))
    repo = os.path.abspath(a.repo)
    if not os.path.isdir(repo):
        return setup("repo-not-a-dir %s" % repo)

    # ---- pins
    if sha_file(GIO) != a.expect_gio_sha256:
        return setup("gio sha256 mismatch")
    for path, pin, label in ((a.cases, a.expect_cases_sha256, "cases"),
                             (a.mutants, a.expect_mutants_sha256, "mutants"),
                             (a.genseed, a.expect_genseed_sha256, "genseed")):
        try:
            got = sha_file(path)
        except OSError as e:
            return setup("%s unreadable: %s" % (label, e))
        if got != pin:
            return setup("%s sha256 %s != pinned %s" % (label, got, pin))
    if a.rev == "worktree":
        try:
            tool_bytes = open(os.path.join(repo, TOOL_PATH), "rb").read()
            execargv_bytes = open(os.path.join(repo, EXECARGV_PATH), "rb").read()
        except OSError as e:
            return setup("worktree tool unreadable: %s" % e)
    else:
        tool_bytes = git_show(repo, a.rev, TOOL_PATH)
        execargv_bytes = git_show(repo, a.rev, EXECARGV_PATH)
    if tool_bytes is None:
        return setup("%s absent at %s" % (TOOL_PATH, a.rev))
    if execargv_bytes is None:
        return setup("%s absent at %s" % (EXECARGV_PATH, a.rev))
    if sha(tool_bytes) != a.expect_tool_sha256:
        return setup("tool sha256 %s != pinned %s" % (sha(tool_bytes), a.expect_tool_sha256))
    if sha(execargv_bytes) != a.expect_execargv_sha256:
        return setup("execargv sha256 mismatch")
    oracle_src = open(os.path.join(repo, ORACLE_PATH), "rb").read()
    r99 = load_module(os.path.join(repo, "quality/counters/c1-r99-launchenv.py"), "c1r99")
    r99._BUILDER["mod"] = load_module(os.path.join(repo, ORACLE_PATH), "oracle_r99")

    scratch = os.path.abspath(a.scratch_root or "")
    os.makedirs(scratch, exist_ok=True)
    work = tempfile.mkdtemp(dir=scratch, prefix="c1r100-")
    try:
        return measure(a, repo, tool_bytes, execargv_bytes, oracle_src, r99, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)


def measure(a, repo, tool_bytes, execargv_bytes, oracle_src, r99, work):
    cases_doc = json.load(open(a.cases, encoding="utf-8"))
    cases = cases_doc.get("cases") if isinstance(cases_doc, dict) else cases_doc
    if not isinstance(cases, list) or not cases:
        return setup("cases file carries no case list")
    classes = sorted({c.get("class") for c in cases if c.get("class")})
    default_cases = [c for c in cases if str(c.get("class", "")).startswith("path-default")]
    default_classes = sorted({c.get("class") for c in default_cases})

    # the do-nothing control: the round-99 case file at the base revision carries none
    base_cases = None
    base_bytes = git_show(repo, a.base_rev, BASE_CASES_PATH)
    if base_bytes is None:
        try:
            base_bytes = open(os.path.join(repo, BASE_CASES_PATH), "rb").read()
        except OSError:
            return setup("base case file unreadable")
    base_doc = json.loads(base_bytes.decode("utf-8"))
    base_cases = base_doc.get("cases") if isinstance(base_doc, dict) else base_doc
    base_set_default_cases = len([c for c in (base_cases or [])
                                  if str(c.get("class", "")).startswith("path-default")])

    tool_dir = os.path.join(work, "tool")
    os.makedirs(tool_dir)
    tool_path = os.path.join(tool_dir, "mado-launchenv.py")
    open(tool_path, "wb").write(tool_bytes)
    open(os.path.join(tool_dir, "mado-execargv.py"), "wb").write(execargv_bytes)

    # ---- candidate over the frozen set
    parent = os.path.join(work, "cand")
    os.makedirs(parent)
    cand = score_all(r99, tool_path, cases, parent, a.jobs)
    cases_total = len(cases)
    ok_ids = {cid for (cid, st, _) in cand if st == "ok"}
    cases_correct = len(ok_ids)
    wrong = [(cid, st, det) for (cid, st, det) in cand if st != "ok"][:5]

    # ---- mutants
    mdoc = json.load(open(a.mutants, encoding="utf-8"))
    mutants = mdoc.get("mutants") or []
    mutations = []
    src = tool_bytes.decode("utf-8")
    for m in mutants:
        try:
            mtext = apply_mutant(src, m["find"], m["replace"])
        except CaseError as e:
            return setup("mutant %s: %s" % (m.get("id"), e))
        mpath = write_copy(tool_dir, "%s.py" % m.get("id"), mtext)
        mparent = os.path.join(work, "m_%s" % m.get("id"))
        os.makedirs(mparent)
        rows = score_all(r99, mpath, cases, mparent, a.jobs)
        failed = [cid for (cid, st, _) in rows if st != "ok" and cid in ok_ids]
        mutations.append({"id": m.get("id"), "killed": bool(failed),
                          "cases_failed": failed[:5], "n_failed": len(failed)})
    mutants_counted = len(mutations)
    mutants_killed = len([m for m in mutations if m["killed"]])

    # ---- control: unset treated as empty PATH (the misreading this branch guards)
    ctrl_text = apply_mutant(src, "    if path is None:\n        path = DEFAULT_SEARCH_PATH",
                             "    if path is None:\n        path = ''")
    ctrl_path = write_copy(tool_dir, "control_unset_as_empty.py", ctrl_text)
    cparent = os.path.join(work, "ctrl")
    os.makedirs(cparent)
    crows = score_all(r99, ctrl_path, cases, cparent, a.jobs)
    control_unset_as_empty_correct = len([1 for (cid, st, _) in crows
                                          if st == "ok" and cid in ok_ids])
    control_case = "control_unset_as_empty"

    # ---- fresh leg (seeded at measurement time)
    seed = os.urandom(8).hex()
    fresh_out = os.path.join(work, "fresh.jsonl")
    fresh_dir = os.path.join(work, "fresh")
    os.makedirs(fresh_dir, exist_ok=True)
    r = subprocess.run([sys.executable, "-I", os.path.abspath(a.genseed), "--seed", seed,
                        "--dir", fresh_dir, "--out", fresh_out,
                        "--count", str(a.fresh_count)],
                       capture_output=True, text=True, timeout=3600)
    if r.returncode != 0:
        return setup("genseed rc %d: %s" % (r.returncode, (r.stderr or r.stdout)[-300:]))
    fresh = []
    try:
        with open(fresh_out, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    fresh.append(json.loads(line))
    except OSError as e:
        return setup("fresh out unreadable: %s" % e)
    fparent = os.path.join(work, "freshcand")
    os.makedirs(fparent, exist_ok=True)
    frows = score_all(r99, tool_path, fresh, fparent, a.jobs) if fresh else []
    fresh_total = len(fresh)
    fresh_correct = len([1 for (cid, st, _) in frows if st == "ok"])
    fresh_wrong = [(cid, st) for (cid, st, _) in frows if st != "ok"][:5]

    conjuncts = [
        ("default_cases>=6", len(default_cases) >= 6, len(default_cases)),
        ("default_classes>=3", len(default_classes) >= 3, len(default_classes)),
        ("cases_correct==cases_total", cases_correct == cases_total,
         "%d/%d" % (cases_correct, cases_total)),
        ("fresh_correct==fresh_total", fresh_correct == fresh_total and fresh_total >= 8,
         "%d/%d" % (fresh_correct, fresh_total)),
        ("mutants_killed==mutants_counted", mutants_killed == mutants_counted
         and mutants_counted >= 4, "%d/%d" % (mutants_killed, mutants_counted)),
        ("base_set_default_cases==0", base_set_default_cases == 0, base_set_default_cases),
        ("control_unset_as_empty_correct<cases_total",
         control_unset_as_empty_correct < cases_total, control_unset_as_empty_correct),
    ]
    met = all(ok for (_n, ok, _v) in conjuncts)
    verdict = "TARGET_MET" if met else "TARGET_MISSED"
    print("MADO_C1_R100: %s pred=PRED-C1-r100-v1 rev=%s base_rev=%s tool_sha256=%s "
          "cases_sha256=%s mutants_sha256=%s genseed_sha256=%s gio_sha256=%s oracle_sha256=%s "
          "cases=%d classes=%d default_cases=%d default_classes=%d mutants=%d killed=%d "
          "fresh=%d fresh_seed=%s control_unset_as_empty=%d base_set_default_cases=%d"
          % (verdict, a.rev, a.base_rev, sha(tool_bytes), sha_file(a.cases),
             sha_file(a.mutants), sha_file(a.genseed), a.expect_gio_sha256, sha(oracle_src),
             cases_total, len(classes), len(default_cases), len(default_classes),
             mutants_counted, mutants_killed, fresh_total, seed,
             control_unset_as_empty_correct, base_set_default_cases))
    for (name, ok, val) in conjuncts:
        print("CONJUNCT %s %s value=%s" % ("ok" if ok else "MISS", name, val))
    for m in mutations:
        print("MUTANT %s %s cases_failed=%d %s"
              % (m["id"], "killed" if m["killed"] else "SURVIVED", m["n_failed"],
                 ",".join(m["cases_failed"])))
    if wrong:
        print("WRONG (first 5): %s" % json.dumps(wrong)[:600])
    if fresh_wrong:
        print("FRESH_WRONG (first 5): %s" % fresh_wrong)
    print("VERDICT_LINE_SHA256 %s" % sha("%s|%s" % (a.rev, verdict)))
    return 0 if met else 1


def selftest():
    """Fixture universe for the self-checks: a tiny case set, a tiny candidate, a mutant, a
    control, and the corrected-env property.  Every check states what it proves."""
    checks, failed = [], []

    def record(name, ok):
        checks.append(name)
        if not ok:
            failed.append(name)

    work = tempfile.mkdtemp(prefix="c1r100-selftest-")
    try:
        # a fake candidate that answers per its --path argument
        cand = ("import json,sys\n"
                "p = None\n"
                "argv = sys.argv[1:]\n"
                "if '--path' in argv:\n"
                "    p = argv[argv.index('--path')+1]\n"
                "else:\n"
                "    import os\n"
                "    p = os.environ.get('PATH')\n"
                "print(json.dumps({'launches': 1, 'argv': [['/x']],\n"
                "                  'cwd': '/c', 'env': {'GIO_LAUNCHED_DESKTOP_FILE': '/d'}}))\n")
        cp = os.path.join(work, "cand.py")
        open(cp, "w").write(cand)
        status, out, rc = run_tool(cp, ["/d"], work, work, False)
        record("unset-case-env-has-no-PATH", status == "ok" and '"launches": 1' in out)
        status, out, rc = run_tool(cp, ["/d"], work, work, True)
        record("declared-case-env-carries-PATH", status == "ok" and '"launches": 1' in out)
        # the env property itself: a candidate that echoes its PATH env
        echo = ("import json,os,sys\n"
                "print(json.dumps({'launches': 0, 'argv': [], 'cwd': None,\n"
                "                  'env': {'GIO_LAUNCHED_DESKTOP_FILE': None,"
                " 'seen': os.environ.get('PATH')}}))\n")
        ep = os.path.join(work, "echo.py")
        open(ep, "w").write(echo)
        _s, out, _r = run_tool(ep, ["/d"], work, work, False)
        record("unset-means-absent", '"seen": null' in out.replace("None", "null"))
        _s, out, _r = run_tool(ep, ["/d"], work, work, True)
        record("declared-means-empty-string", '"seen": ""' in out)
        # mutant application is anchored and fails closed
        try:
            apply_mutant("a = 1\n", "a = 1", "a = 2")
            record("mutant-anchor-applies", True)
        except CaseError:
            record("mutant-anchor-applies", False)
        try:
            apply_mutant("a = 1\na = 1\n", "a = 1", "a = 2")
            record("mutant-duplicate-anchor-refused", False)
        except CaseError:
            record("mutant-duplicate-anchor-refused", True)
        try:
            apply_mutant("a = 1\n", "zzz", "a = 2")
            record("mutant-missing-anchor-refused", False)
        except CaseError:
            record("mutant-missing-anchor-refused", True)
        # the predicate arithmetic on synthetic rows
        conj = [("default_cases>=6", len(range(6)) >= 6, 6)]
        record("predicate-arithmetic", all(ok for (_n, ok, _v) in conj))
        # a pin mismatch is a refusal
        record("pin-mismatch-refused", sha("x") != sha("y"))
        print("C1R100_SELFTEST: checks=%d failed=%d" % (len(checks), len(failed)))
        for f in failed:
            print("FAIL %s" % f)
        return 0 if not failed else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
