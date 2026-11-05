#!/usr/bin/env python3
"""mado round 88 — PRED-C1-r88-v1: score tools/mado-mako.py over the superseding mako case set.

Predicate (declaration section "C1", verbatim): TARGET_MET iff the candidate tool's correct count equals N,
all M mutants are killed, the 22 frozen round-87 cases are carried unchanged, and the four controls
(naive-toplevel, globals-include, base-tool, inputs-ignored) each score strictly below N.
Score = 10 * tool_correct / N on this finite case set only.

Surface: mako 1.11.0 effective settings for one notification — the round-87 surface (config, include=
chain, app-name/urgency/mode criteria) widened to every first-pass exact criteria field the manual lists
(app-icon, summary, body, category, desktop-entry, actionable, expiring; summary~/body~ stay refused) and
to upstream's boolean grammar (types.c parse_boolean) for criteria and style options.

Controls: naive-toplevel and globals-include are the round-87 file readers (never call a tool);
base-tool is the tool at --base-rev (the round-87 resolver; it has no new input flags, so it exits 2 on
every case that passes one — a CLI-surface control, its per-case reasons are printed); inputs-ignored is
the candidate with its new notification inputs discarded (`self.inputs = {}`, `self.flags = {}`): a
resolver that accepts the new flags and resolves nothing new. A tool mutant or forgery anchor that does
not occur exactly once in the measured tool is a setup error (exit 2), never a scored miss.

Machinery (git scrub, case materialization, the two file-reading controls) is the frozen round-87
counter, loaded from quality/counters/c1-r87-mako-criteria.py and refused unless its sha256 equals
R87_COUNTER_SHA256. What this counter changes: the case schema (new notification inputs), N range,
the mutant list path and count, the carried-case check, the base-tool control and both sha pins.

Inputs: --cases (a path; its sha256 MUST equal --expect-cases-sha256), tool and mutant list read from
REV with `git show`, the mutant list's sha256 MUST equal --expect-mutants-sha256; the base-tool control
reads the tool from --base-rev. Writes only inside a generation directory under --scratch-root, removed
on exit. Never writes inside the repository.

Exit map: 0 TARGET_MET · 1 TARGET_MISSED · 2 setup error (never a verdict).
--selftest: hermetic fixture run under --scratch-root (or TMPDIR); exit 0 iff every assertion holds.
"""

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R87_COUNTER = os.path.join(HERE, "c1-r87-mako-criteria.py")
R87_COUNTER_SHA256 = "4d801c30b302ed5972142415012d8f461109459d9c44e85e0badef57a2ed3645"
SCHEMA = "mako-cases-r88-v1"
N_MIN, N_MAX = 40, 64
DECLARED_MUTANTS = 22
CARRIED_CASES = 22
TOOL_PATH = "tools/mado-mako.py"
MUTANTS_PATH = ".ufo/waves/round-88/controls/mako-mutants-r88.json"
R87_CASES_PATH = ".ufo/waves/round-87/controls/mako-cases-r87.json"
STRING_ARGS = ("app-name", "app-icon", "summary", "body", "category", "desktop-entry")
BOOL_ARGS = ("actionable", "expiring")
ARG_NAMES = STRING_ARGS + ("urgency",) + BOOL_ARGS + ("mode",)
FORGERY = (("self.inputs = dict(inputs or {})", "self.inputs = {}"),
           ("self.flags = dict(flags or {})", "self.flags = {}"))
THIS = os.path.abspath(__file__)


def _load_r87():
    """Load the round-87 machinery only after its bytes match the pin; execute exactly those bytes."""
    with open(R87_COUNTER, "rb") as fh:
        data = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != R87_COUNTER_SHA256:
        print(f"MADO_MAKO_FIELDS: SETUP_ERROR round-87 counter sha256 {digest} != pinned {R87_COUNTER_SHA256}",
              file=sys.stderr)
        sys.exit(2)
    spec = importlib.util.spec_from_loader("c1_r87_mako_criteria", loader=None, origin=R87_COUNTER)
    module = importlib.util.module_from_spec(spec)
    module.__file__ = R87_COUNTER
    exec(compile(data, R87_COUNTER, "exec"), module.__dict__)
    return module, digest


R87, R87_DIGEST = _load_r87()
SetupError = R87.SetupError
git, git_env, resolve_commit, sha256 = R87.git, R87.git_env, R87.resolve_commit, R87.sha256
canon, safe_relpath, load_mutants, materialize = R87.canon, R87.safe_relpath, R87.load_mutants, R87.materialize
tool_verdict, control_score, naive_values, globals_values = (
    R87.tool_verdict, R87.control_score, R87.naive_values, R87.globals_values)


def check_r87_pin():
    if R87_DIGEST != R87_COUNTER_SHA256:
        raise SetupError(f"round-87 counter sha256 {R87_DIGEST} != pinned {R87_COUNTER_SHA256}")


def load_cases(raw):
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise SetupError(f"cases file is not JSON: {exc}")
    if not isinstance(doc, dict) or doc.get("schema") != SCHEMA:
        raise SetupError(f"cases schema is not {SCHEMA}")
    entries = doc.get("cases")
    if not isinstance(entries, list) or not entries:
        raise SetupError("cases must be a non-empty list")
    cases, ids = [], set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise SetupError("case is not an object")
        cid = entry.get("id")
        if not isinstance(cid, str) or not R87.ID_RE.match(cid) or cid in ids:
            raise SetupError(f"bad or duplicate case id {cid!r}")
        ids.add(cid)
        config = safe_relpath(entry.get("config"), f"{cid}.config")
        files = entry.get("home_files")
        if not isinstance(files, dict):
            raise SetupError(f"{cid}.home_files must be an object")
        home_files = {}
        for rel, content in files.items():
            safe_relpath(rel, f"{cid}.home_files")
            if isinstance(content, str):
                home_files[rel] = content
            elif isinstance(content, dict) and set(content) == {"symlink_to"}:
                home_files[rel] = {"symlink_to": safe_relpath(content["symlink_to"], f"{cid}.symlink")}
            else:
                raise SetupError(f"{cid}.home_files[{rel}]: must be text or {{symlink_to}}")
        args = entry.get("args", {})
        if not isinstance(args, dict) or not set(args) <= set(ARG_NAMES):
            raise SetupError(f"{cid}.args: unknown or non-object args")
        strings = {}
        for name in STRING_ARGS:
            value = args.get(name)
            if value is not None and not isinstance(value, str):
                raise SetupError(f"{cid}.args.{name} must be a string")
            if name == "app-name" and value == "":
                raise SetupError(f"{cid}.args.app-name must be non-empty")
            if value is not None:
                strings[name] = value
        urgency = args.get("urgency")
        if urgency is not None and urgency not in R87.URGENCY:
            raise SetupError(f"{cid}.args.urgency must be one of {R87.URGENCY}")
        flags = {}
        for name in BOOL_ARGS:
            value = args.get(name)
            if value is not None and value not in ("true", "false"):
                raise SetupError(f"{cid}.args.{name} must be 'true' or 'false'")
            if value is not None:
                flags[name] = value
        modes = args.get("mode", [])
        if isinstance(modes, str):
            modes = [modes]
        if not isinstance(modes, list) or not all(isinstance(m, str) for m in modes):
            raise SetupError(f"{cid}.args.mode must be a string or list of strings")
        expect = entry.get("expect")
        if not isinstance(expect, dict) or not isinstance(expect.get("effective"), dict):
            raise SetupError(f"{cid}.expect.effective must be an object")
        refusals = expect.get("refusals")
        if refusals not in ("none", "present"):
            raise SetupError(f"{cid}.expect.refusals must be 'none' or 'present'")
        cases.append({
            "id": cid,
            "config": config,
            "home_files": home_files,
            "app_name": strings.get("app-name"),
            "urgency": urgency,
            "modes": modes,
            "strings": strings,
            "flags": flags,
            "effective": expect["effective"],
            "refusals": refusals,
            "raw": entry,
        })
    return cases


def carried_count(cases, r87_raw):
    """Count round-87 frozen cases present in the r88 set as canonically equal JSON objects."""
    try:
        r87 = json.loads(r87_raw.decode("utf-8"))["cases"]
    except (UnicodeDecodeError, ValueError, KeyError, TypeError) as exc:
        raise SetupError(f"round-87 case file unreadable: {exc}")
    mine = {canon(case["raw"]) for case in cases}
    return sum(canon(entry) in mine for entry in r87), len(r87)


def run_tool(tool, case, home, gen):
    argv = [sys.executable, "-I", tool, "--config", os.path.join(home, case["config"]), "--home", home]
    for name in STRING_ARGS:
        if name in case["strings"]:
            argv += ["--" + name, case["strings"][name]]
    if case["urgency"] is not None:
        argv += ["--urgency", case["urgency"]]
    for name in BOOL_ARGS:
        if name in case["flags"]:
            argv += ["--" + name, case["flags"][name]]
    for mode in case["modes"]:
        argv += ["--mode", mode]
    env = {"PATH": os.environ.get("PATH", ""), "TMPDIR": gen, "HOME": home,
           "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    try:
        return subprocess.run(argv, env=env, cwd=home, capture_output=True, timeout=R87.RUN_TIMEOUT)
    except subprocess.TimeoutExpired:
        return None


CRASH_PREFIXES = ("timeout", "exit=", "bad-json", "not-object", "no-effective", "no-refusals-list")


def semantic_kill(candidate, mutant):
    """A mutant is killed only when, on some case, its verdict differs AND it produced a well-formed
    result there (exit 0, JSON object with effective and refusals): a crash is not a kill."""
    return any(cv != mv and not mr.startswith(CRASH_PREFIXES)
               for cv, (mv, mr) in zip(candidate, mutant))


def predicate(n, correct, killed, m, carried, carried_needed, controls):
    """PRED-C1-r88-v1: correct == N, all M killed, carried == 22, every control strictly below N."""
    return (correct == n and killed == m and carried == carried_needed
            and all(score < n for score in controls.values()))


def run_all(tool, cases, homes, gen):
    verdicts, reasons = [], []
    for case in cases:
        ok, reason = tool_verdict(case, run_tool(tool, case, homes[case["id"]], gen))
        verdicts.append(ok)
        reasons.append(reason)
    return verdicts, reasons


def evaluate(tool_text, base_text, cases, mutants, scratch_root, carried,
             declared=DECLARED_MUTANTS, range_check=True, carried_needed=CARRIED_CASES, forgery=FORGERY,
             controls_only=False):
    n = len(cases)
    if range_check and not (N_MIN <= n <= N_MAX):
        raise SetupError(f"N={n} is outside {N_MIN}..{N_MAX}")
    if declared is not None and len(mutants) != declared:
        raise SetupError(f"mutants={len(mutants)} but the declaration fixes M={declared}")
    for mid, old, _ in ([] if controls_only else mutants):
        if tool_text.count(old) != 1:
            raise SetupError(f"mutant {mid}: anchor occurs {tool_text.count(old)} times in the measured tool")
    forged_text = tool_text
    for old, new in forgery:
        if forged_text.count(old) != 1:
            raise SetupError(f"forgery anchor {old!r} occurs {forged_text.count(old)} times in the measured tool")
        forged_text = forged_text.replace(old, new, 1)
    gen = tempfile.mkdtemp(prefix="mado-mako-r88-", dir=scratch_root)
    try:
        tool = os.path.join(gen, "tool.py")
        with open(tool, "wb") as fh:
            fh.write(tool_text.encode("utf-8"))
        base_tool = os.path.join(gen, "base-tool.py")
        with open(base_tool, "wb") as fh:
            fh.write(base_text.encode("utf-8"))
        homes = materialize(cases, gen)
        if controls_only:
            verdicts, reasons = [False] * n, ["not-run"] * n
            lines = []
        else:
            verdicts, reasons = run_all(tool, cases, homes, gen)
            lines = [f"case {c['id']} {'ok' if ok else 'FAIL'} {why}" for c, ok, why in zip(cases, verdicts, reasons)]
        correct = sum(verdicts)
        base_verdicts, base_reasons = run_all(base_tool, cases, homes, gen)
        base_correct = sum(base_verdicts)
        forged = os.path.join(gen, "inputs-ignored.py")
        with open(forged, "wb") as fh:
            fh.write(forged_text.encode("utf-8"))
        forged_verdicts, forged_reasons = run_all(forged, cases, homes, gen)
        forged_correct = sum(forged_verdicts)
        lines += [f"control base-tool {c['id']} {'ok' if ok else 'FAIL'} {why}"
                  for c, ok, why in zip(cases, base_verdicts, base_reasons)]
        lines += [f"control inputs-ignored {c['id']} {'ok' if ok else 'FAIL'} {why}"
                  for c, ok, why in zip(cases, forged_verdicts, forged_reasons)]
        naive = control_score(cases, homes, lambda cfg, home: naive_values(cfg))
        globals_ = control_score(cases, homes, globals_values)
        results, killed = [], 0
        for index, (mid, old, new) in enumerate([] if controls_only else mutants):
            mutant = os.path.join(gen, f"mutant-{index}.py")
            with open(mutant, "wb") as fh:
                fh.write(tool_text.replace(old, new, 1).encode("utf-8"))
            mverdicts, mreasons = run_all(mutant, cases, homes, gen)
            hit = semantic_kill(verdicts, list(zip(mverdicts, mreasons)))
            crashed = any(r.startswith(CRASH_PREFIXES) for r in mreasons)
            killed += hit
            status = "killed" if hit else ("crashed-not-killed" if crashed else "survived")
            results.append({"id": mid, "status": status, "killed": hit})
        m = len(mutants)
        met = predicate(n, correct, killed, m, carried, carried_needed,
                        {"naive-toplevel": naive, "globals-include": globals_, "base-tool": base_correct,
                         "inputs-ignored": forged_correct})
        return {"n": n, "correct": correct, "mutants": results, "m": m, "killed": killed,
                "naive": naive, "globals": globals_, "base": base_correct, "forged": forged_correct,
                "carried": carried,
                "score": 10.0 * correct / n, "verdict": "TARGET_MET" if met else "TARGET_MISSED",
                "lines": lines}
    finally:
        shutil.rmtree(gen, ignore_errors=True)


def run_controls(args):
    """Controls-only receipt (before the freeze): naive-toplevel, globals-include, base-tool and
    inputs-ignored (derived from --candidate-file); the candidate itself and the mutants are not run."""
    check_r87_pin()
    for name in ("repo", "base_rev", "cases", "scratch_root", "candidate_file"):
        if getattr(args, name) is None:
            raise SetupError(f"--{name.replace('_', '-')} is required with --controls-only")
    base_commit = resolve_commit(args.repo, args.base_rev)
    with open(args.cases, "rb") as fh:
        cases_raw = fh.read()
    with open(args.candidate_file, "rb") as fh:
        candidate_raw = fh.read()
    cases = load_cases(cases_raw)
    base_raw = git(args.repo, "show", f"{base_commit}:{TOOL_PATH}")
    result = evaluate(candidate_raw.decode("utf-8"), base_raw.decode("utf-8"), cases, [], args.scratch_root, 0,
                      declared=None, carried_needed=CARRIED_CASES, forgery=FORGERY, controls_only=True)
    n = result["n"]
    print(f"cases_sha256={sha256(cases_raw)} cases={n} candidate_file_sha256={sha256(candidate_raw)} "
          f"base_tool_sha256={sha256(base_raw)} base={base_commit} counter_sha256={sha256(open(THIS, 'rb').read())}")
    for line in result["lines"]:
        print(line)
    below = all(v < n for v in (result["naive"], result["globals"], result["base"], result["forged"]))
    print(f"MADO_MAKO_FIELDS_CONTROLS: {'BELOW_N' if below else 'CONTROL_REACHES_N'} cases={n} "
          f"naive_correct={result['naive']} globals_include_correct={result['globals']} "
          f"base_tool_correct={result['base']} inputs_ignored_correct={result['forged']}")
    return 0 if below else 1


def run(args):
    check_r87_pin()
    for name in ("repo", "rev", "base_rev", "cases", "scratch_root", "expect_cases_sha256",
                 "expect_mutants_sha256", "expect_r87_cases_sha256"):
        if getattr(args, name) is None:
            raise SetupError(f"--{name.replace('_', '-')} is required")
    if not os.path.isdir(args.scratch_root):
        raise SetupError(f"scratch root is not a directory: {args.scratch_root}")
    commit = resolve_commit(args.repo, args.rev)
    base_commit = resolve_commit(args.repo, args.base_rev)
    try:
        with open(args.cases, "rb") as fh:
            cases_raw = fh.read()
    except OSError as exc:
        raise SetupError(f"cases unreadable: {exc}")
    if sha256(cases_raw) != args.expect_cases_sha256:
        raise SetupError(f"cases sha256 {sha256(cases_raw)} != expected {args.expect_cases_sha256}")
    cases = load_cases(cases_raw)
    mutants_raw = git(args.repo, "show", f"{commit}:{MUTANTS_PATH}")
    if sha256(mutants_raw) != args.expect_mutants_sha256:
        raise SetupError(f"mutants sha256 {sha256(mutants_raw)} != expected {args.expect_mutants_sha256}")
    mutants = load_mutants(mutants_raw)
    r87_raw = git(args.repo, "show", f"{commit}:{R87_CASES_PATH}")
    if sha256(r87_raw) != args.expect_r87_cases_sha256:
        raise SetupError(f"round-87 cases sha256 {sha256(r87_raw)} != expected {args.expect_r87_cases_sha256}")
    carried, r87_n = carried_count(cases, r87_raw)
    try:
        tool_raw = git(args.repo, "show", f"{commit}:{TOOL_PATH}")
        tool_text = tool_raw.decode("utf-8")
        base_raw = git(args.repo, "show", f"{base_commit}:{TOOL_PATH}")
        base_text = base_raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SetupError(f"tool is not UTF-8: {exc}")
    print(f"r87_counter_sha256={R87_DIGEST} counter_sha256={sha256(open(THIS, 'rb').read())}")
    print(f"cases_sha256={sha256(cases_raw)} cases={len(cases)} carried={carried}/{r87_n}")
    print(f"tool_sha256={sha256(tool_raw)} commit={commit} base_tool_sha256={sha256(base_raw)} base={base_commit}")
    print(f"mutants={len(mutants)} mutants_sha256={sha256(mutants_raw)}")
    result = evaluate(tool_text, base_text, cases, mutants, args.scratch_root, carried,
                      declared=DECLARED_MUTANTS, carried_needed=CARRIED_CASES, forgery=FORGERY)
    for line in result["lines"]:
        print(line)
    print(f"controls naive_correct={result['naive']} globals_include_correct={result['globals']} "
          f"base_tool_correct={result['base']} inputs_ignored_correct={result['forged']}")
    for entry in result["mutants"]:
        print(f"mutant {entry['id']} {entry['status']}")
    print(
        f"MADO_MAKO_FIELDS: {result['verdict']} rev={args.rev} base_rev={args.base_rev} cases={result['n']} "
        f"correct={result['correct']} carried={result['carried']}/{CARRIED_CASES} mutants={result['m']} "
        f"killed={result['killed']} naive_correct={result['naive']} "
        f"globals_include_correct={result['globals']} base_tool_correct={result['base']} "
        f"inputs_ignored_correct={result['forged']} "
        f"score={result['score']:.4f} tool_sha256={sha256(tool_raw)} cases_sha256={sha256(cases_raw)}"
    )
    return R87.exit_for(result["verdict"])


# ---------------------------------------------------------------- selftest

FIXTURE_TOOL = R87.FIXTURE_TOOL.replace(
    '    ap.add_argument("--mode", action="append", default=[])\n',
    '    ap.add_argument("--mode", action="append", default=[])\n'
    '    ap.add_argument("--category")\n'
    '    ap.add_argument("--actionable", choices=["true", "false"])\n', 1).replace(
    '    args = ap.parse_args()\n',
    '    args = ap.parse_args()\n'
    '    USE_INPUTS = True\n'
    '    if USE_INPUTS and (args.category == "drop" or args.actionable == "false") and args.app_name:\n'
    '        args.app_name = None\n', 1)
FIXTURE_FORGERY = (("    USE_INPUTS = True", "    USE_INPUTS = False"),)

FIXTURE_CASES = {
    "schema": SCHEMA,
    "cases": [
        {"id": "include-global", "config": ".config/mako/config",
         "home_files": {".config/mako/config": "include=~/.config/mako/core.ini\nanchor=top-right\n",
                        ".config/mako/core.ini": "default-timeout=5000\n"},
         "args": {"category": "x", "actionable": "true"},
         "expect": {"effective": {"anchor": "top-right", "default-timeout": "5000"}, "refusals": "none"}},
        {"id": "section-override", "config": ".config/mako/config",
         "home_files": {".config/mako/config": "anchor=top-right\n[app-name=slack]\nanchor=bottom-left\n"},
         "args": {"app-name": "slack"},
         "expect": {"effective": {"anchor": "bottom-left"}, "refusals": "none"}},
        {"id": "input-decides", "config": ".config/mako/config",
         "home_files": {".config/mako/config": "anchor=top-right\n[app-name=slack]\nanchor=bottom-left\n"},
         "args": {"app-name": "slack", "category": "drop"},
         "expect": {"effective": {"anchor": "top-right"}, "refusals": "none"}},
        {"id": "flag-decides", "config": ".config/mako/config",
         "home_files": {".config/mako/config": "anchor=top-right\n[app-name=slack]\nanchor=bottom-left\n"},
         "args": {"app-name": "slack", "actionable": "false"},
         "expect": {"effective": {"anchor": "top-right"}, "refusals": "none"}},
    ],
}


def selftest_run(scratch):
    """In-process run() over a fixture git repo with the round constants scaled to the fixture."""
    import contextlib
    import io
    g = globals()
    saved = {k: g[k] for k in ("N_MIN", "N_MAX", "DECLARED_MUTANTS", "CARRIED_CASES", "FORGERY")}
    fixture = tempfile.mkdtemp(prefix="fixture-", dir=scratch)
    ok = True
    try:
        env = git_env()
        subprocess.run(["git", "-C", fixture, "init", "-q"], env=env, check=True)
        top = subprocess.run(["git", "-C", fixture, "rev-parse", "--show-toplevel"], env=env,
                             capture_output=True, text=True, check=True).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(fixture):
            return False
        cases_raw = json.dumps(FIXTURE_CASES).encode("utf-8")
        mutants_raw = json.dumps({"mutants": [{"id": "section-ignored", "old": "SECTION_WINS = True",
                                               "new": "SECTION_WINS = False"}]}).encode("utf-8")
        r87_raw = json.dumps({"cases": [FIXTURE_CASES["cases"][1]]}).encode("utf-8")
        wrong = FIXTURE_TOOL.replace("SECTION_WINS = True", "SECTION_WINS = False", 1)

        def commit(tool_text, message):
            for rel, data in ((TOOL_PATH, tool_text.encode("utf-8")), (MUTANTS_PATH, mutants_raw),
                              (R87_CASES_PATH, r87_raw)):
                path = os.path.join(fixture, rel)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as fh:
                    fh.write(data)
            subprocess.run(["git", "-C", fixture, "add", "-A"], env=env, check=True)
            subprocess.run(["git", "-C", fixture, "-c", "user.name=mado-selftest", "-c",
                            "user.email=selftest@invalid", "commit", "-q", "-m", message], env=env, check=True)
            return resolve_commit(fixture, "HEAD")

        base = commit(wrong, "base")
        head = commit(FIXTURE_TOOL, "candidate")
        cases_path = os.path.join(scratch, "fixture-cases-run.json")
        with open(cases_path, "wb") as fh:
            fh.write(cases_raw)
        g.update(N_MIN=1, N_MAX=10, DECLARED_MUTANTS=1, CARRIED_CASES=1, FORGERY=FIXTURE_FORGERY)
        good = dict(repo=fixture, rev=head, base_rev=base, cases=cases_path, scratch_root=scratch,
                    expect_cases_sha256=sha256(cases_raw), expect_mutants_sha256=sha256(mutants_raw),
                    expect_r87_cases_sha256=sha256(r87_raw))
        with contextlib.redirect_stdout(io.StringIO()) as out:
            rc = run(argparse.Namespace(**good))
        ok &= rc == 0 and "MADO_MAKO_FIELDS: TARGET_MET" in out.getvalue()
        for key in ("expect_cases_sha256", "expect_mutants_sha256", "expect_r87_cases_sha256"):
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    run(argparse.Namespace(**dict(good, **{key: "0" * 64})))
                ok = False
            except SetupError:
                pass
    finally:
        g.update(saved)
        shutil.rmtree(fixture, ignore_errors=True)
    return ok


def selftest(scratch_root=None):
    checks = []

    def check(name, cond):
        checks.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name}")

    scratch = tempfile.mkdtemp(prefix="mado-mako-r88-selftest-", dir=scratch_root)
    try:
        check("round-87 machinery loads at its pinned sha256", globals()["R87_DIGEST"] == R87_COUNTER_SHA256)
        raw = json.dumps(FIXTURE_CASES).encode("utf-8")
        cases = load_cases(raw)
        check("fixture cases load with the new notification inputs", len(cases) == 4
              and cases[0]["strings"] == {"category": "x"} and cases[0]["flags"] == {"actionable": "true"})
        bad = json.loads(raw)
        bad["cases"][0]["args"]["actionable"] = "yes"
        try:
            load_cases(json.dumps(bad).encode("utf-8"))
            check("boolean input outside true/false is a setup error", False)
        except SetupError:
            check("boolean input outside true/false is a setup error", True)
        bad["cases"][0]["args"] = {"colour": "x"}
        try:
            load_cases(json.dumps(bad).encode("utf-8"))
            check("unknown arg name is a setup error", False)
        except SetupError:
            check("unknown arg name is a setup error", True)

        r87_doc = {"cases": [FIXTURE_CASES["cases"][1]]}
        carried, total = carried_count(cases, json.dumps(r87_doc).encode("utf-8"))
        check("carried count finds an unchanged prior case", (carried, total) == (1, 1))
        changed = json.loads(json.dumps(r87_doc))
        changed["cases"][0]["expect"]["effective"]["anchor"] = "center"
        carried, _ = carried_count(cases, json.dumps(changed).encode("utf-8"))
        check("carried count refuses an edited prior case", carried == 0)

        mutants = [("section-ignored", "SECTION_WINS = True", "SECTION_WINS = False")]
        wrong = FIXTURE_TOOL.replace("SECTION_WINS = True", "SECTION_WINS = False", 1)
        kw = dict(declared=None, range_check=False, carried_needed=1, forgery=FIXTURE_FORGERY)
        before = sorted(os.listdir(scratch))
        good = evaluate(FIXTURE_TOOL, wrong, cases, mutants, scratch, 1, **kw)
        check("correct fixture tool scores N/N and kills the mutant",
              good["correct"] == 4 and good["killed"] == 1)
        check("base-tool control (the mutant as base) scores below N", good["base"] < 4)
        check("inputs-ignored forgery scores below N when an input decides a case", good["forged"] < 4)
        check("all conjuncts hold -> TARGET_MET", good["verdict"] == "TARGET_MET")
        check("per-case control reasons are printed for both tool controls",
              sum(line.startswith("control base-tool ") for line in good["lines"]) == 4
              and sum(line.startswith("control inputs-ignored ") for line in good["lines"]) == 4)
        check("evaluate leaves the scratch root as it found it", sorted(os.listdir(scratch)) == before)
        same = evaluate(FIXTURE_TOOL, FIXTURE_TOOL, cases, mutants, scratch, 1, **kw)
        check("base tool scoring N (do-nothing reaches target) -> TARGET_MISSED",
              same["base"] == 4 and same["verdict"] == "TARGET_MISSED")
        noop = dict(kw, forgery=(("OK_TOKEN = \"v1\"", "OK_TOKEN = \"v1\""),))
        blind = evaluate(FIXTURE_TOOL, wrong, cases, mutants, scratch, 1, **noop)
        check("inputs-ignored forgery reaching N -> TARGET_MISSED",
              blind["forged"] == 4 and blind["verdict"] == "TARGET_MISSED")
        short = evaluate(FIXTURE_TOOL, wrong, cases, mutants, scratch, 0, **kw)
        check("a missing carried case -> TARGET_MISSED", short["verdict"] == "TARGET_MISSED")
        survivor = evaluate(FIXTURE_TOOL, wrong, cases, mutants + [("noop", "OK_TOKEN = \"v1\"", "OK_TOKEN = \"v2\"")],
                            scratch, 1, **kw)
        check("a surviving mutant -> TARGET_MISSED", survivor["verdict"] == "TARGET_MISSED")
        for label, bad_mutants, bad_forgery in (
                ("absent mutant anchor", mutants + [("ghost", "NO_SUCH_ANCHOR", "x")], FIXTURE_FORGERY),
                ("absent forgery anchor", mutants, (("NO_SUCH_ANCHOR", "x"),))):
            try:
                evaluate(FIXTURE_TOOL, wrong, cases, bad_mutants, scratch, 1, **dict(kw, forgery=bad_forgery))
                check(f"{label} is a setup error, not a scored miss", False)
            except SetupError:
                check(f"{label} is a setup error, not a scored miss", True)
        try:
            evaluate(FIXTURE_TOOL, wrong, cases, mutants, scratch, 1, declared=1, carried_needed=1,
                     forgery=FIXTURE_FORGERY)
            check("N outside the declared range is a setup error (M matches)", False)
        except SetupError as exc:
            check("N outside the declared range is a setup error (M matches)", "outside" in str(exc))
        try:
            evaluate(FIXTURE_TOOL, wrong, cases, mutants, scratch, 1, **dict(kw, declared=2))
            check("M different from the declared count is a setup error (N unchecked)", False)
        except SetupError as exc:
            check("M different from the declared count is a setup error (N unchecked)", "declaration" in str(exc))
        bad = evaluate(wrong, wrong, cases, [], scratch, 1, **kw)
        check("a tool wrong on one case is not TARGET_MET", bad["correct"] == 3 and bad["verdict"] == "TARGET_MISSED")
        for name in ("--category", "--actionable"):
            dropped = FIXTURE_TOOL.replace('    ap.add_argument("' + name + '"', '    ap.add_argument("' + name + '-x"', 1)
            gone = evaluate(dropped, wrong, cases, [], scratch, 1, **kw)
            check(f"a tool that never receives {name} misses a case", gone["correct"] < 4)
        crash = [("import-break", "import json\n", "import json (\n")]
        crashed = evaluate(FIXTURE_TOOL, wrong, cases, crash, scratch, 1, **kw)
        check("a mutant that crashes on every case is not counted killed",
              crashed["killed"] == 0 and crashed["mutants"][0]["status"] == "crashed-not-killed")
        controls = {"naive-toplevel": 0, "globals-include": 0, "base-tool": 0, "inputs-ignored": 0}
        check("predicate holds when every conjunct holds", predicate(5, 5, 2, 2, 22, 22, controls))
        check("predicate fails at correct = N-1", not predicate(5, 4, 2, 2, 22, 22, controls))
        check("predicate fails at killed = M-1", not predicate(5, 5, 1, 2, 22, 22, controls))
        check("predicate fails at carried = 21", not predicate(5, 5, 2, 2, 21, 22, controls))
        for name in controls:
            check(f"predicate fails when {name} reaches N", not predicate(5, 5, 2, 2, 22, 22, dict(controls, **{name: 5})))
            check(f"predicate holds when {name} is N-1", predicate(5, 5, 2, 2, 22, 22, dict(controls, **{name: 4})))
        saved = globals()["R87_DIGEST"]
        globals()["R87_DIGEST"] = "0" * 64
        try:
            check_r87_pin()
            check("check_r87_pin refuses a digest that differs from the pin", False)
        except SetupError:
            check("check_r87_pin refuses a digest that differs from the pin", True)
        finally:
            globals()["R87_DIGEST"] = saved
        check("run() honours every sha pin", selftest_run(scratch))
        ctl = evaluate(FIXTURE_TOOL, wrong, cases, mutants, scratch, 1, **dict(kw, controls_only=True))
        check("controls-only mode runs neither the candidate nor the mutants",
              ctl["correct"] == 0 and ctl["mutants"] == [] and ctl["base"] < 4 and ctl["forged"] < 4
              and not any(line.startswith("case ") for line in ctl["lines"]))
        proc = subprocess.run([sys.executable, "-I", THIS, "--repo", scratch, "--rev", "HEAD"],
                              capture_output=True, env=git_env())
        check("CLI: missing required arguments exit 2", proc.returncode == 2)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    passed = sum(checks)
    print(f"SELFTEST: passed={passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="mado round 88 C1 mako fields counter")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--cases")
    ap.add_argument("--expect-cases-sha256")
    ap.add_argument("--expect-mutants-sha256")
    ap.add_argument("--expect-r87-cases-sha256")
    ap.add_argument("--scratch-root")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--controls-only", action="store_true")
    ap.add_argument("--candidate-file")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest(args.scratch_root)
    try:
        return run_controls(args) if args.controls_only else run(args)
    except SetupError as exc:
        print(f"MADO_MAKO_FIELDS: SETUP_ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
