#!/usr/bin/env python3
"""mado round 89 — PRED-C1-r89-v1: score tools/mado-mako.py over the summary~/body~ (POSIX ERE) case set.

Predicate (declaration section "C1", verbatim): TARGET_MET iff the candidate tool's correct count equals N,
all M mutants are killed, the 61 carried round-88 cases are present unchanged, and the four controls
(naive-toplevel, globals-include, base-tool, python-re) each score strictly below N.
Score = 10 * tool_correct / N on this finite case set only (score_scope=finite-cases; the verdict, not the
score, says whether the claim is met).

Surface: mako 1.11.0 summary~ and body~ criteria (criteria.c: regcomp(REG_EXTENDED | REG_NOSUB), unanchored
regexec, C locale because mako never calls setlocale), the criteria tokenizer rules the regex values pass
through (backslash escapes the next character inside quotes; only a space separates tokens), and the
"cannot set both summary and summary~" refusal. The round-88 cases are carried except
c53-summary-tilde-refused, whose expectation (summary~ refused) this surface supersedes.

Controls: naive-toplevel and globals-include are the round-87 file readers; base-tool is the tool at
--base-rev (the round-88 resolver, which refuses summary~/body~); python-re is the candidate with its
libc matcher replaced by Python's re (re.compile / search) — the resolution path the round-88 tool named
as wrong. A mutant or forgery anchor that does not occur exactly once in the measured tool is a setup
error (exit 2), never a scored miss.

Machinery (case loading, git, materialization, evaluate, semantic kill, the two file-reading controls) is
the frozen round-88 counter quality/counters/c1-r88-mako-fields.py, loaded only when its sha256 equals
R88_COUNTER_SHA256 (it in turn pins the round-87 machinery). What this counter changes: the case schema
name, N range, mutant list path and count, the carried set (round-88 cases), the fourth control and the
sha pins.

Inputs: --cases (sha256 MUST equal --expect-cases-sha256); tool and mutant list read from REV with
`git show`; the mutant list's sha256 MUST equal --expect-mutants-sha256; the round-88 case file read from
REV MUST equal --expect-r88-cases-sha256; the base-tool control reads the tool from --base-rev. Writes
only inside a generation directory under --scratch-root, removed on exit; honours no fixed /tmp path.

Exit map: 0 TARGET_MET · 1 TARGET_MISSED · 2 setup error (never a verdict).
--selftest: hermetic run under --scratch-root (or TMPDIR); exit 0 iff every assertion holds.
"""

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
R88_COUNTER = os.path.join(HERE, "c1-r88-mako-fields.py")
R88_COUNTER_SHA256 = "3678425addb5f661d3f284ef423e3566446b54714cb2148c5696a8cdfe11cc1f"
SCHEMA = "mako-cases-r89-v1"
N_MIN, N_MAX = 120, 160
DECLARED_MUTANTS = 37
CARRIED_CASES = 61
SUPERSEDED = ("c53-summary-tilde-refused",)
TOOL_PATH = "tools/mado-mako.py"
MUTANTS_PATH = ".ufo/waves/round-89/controls/mako-mutants-r89.json"
R88_CASES_PATH = ".ufo/waves/round-88/controls/mako-cases-r88.json"
PYRE_FORGERY = (
    ("    lib = _libc()\n    buf = ctypes.create_string_buffer(REGEX_T_BYTES)\n"
     "    if lib.regcomp(buf, raw, REG_EXTENDED | REG_NOSUB) != 0:\n        return None\n    return buf\n",
     "    try:\n        return re.compile(pattern)\n    except re.error:\n        return None\n"),
    ('    return _libc().regexec(compiled, text.encode("utf-8", "surrogateescape"), 0, None, 0) == 0\n',
     "    return compiled.search(text) is not None\n"),
    ("    _libc().regfree(compiled)\n", "    return None\n"),
)
THIS = os.path.abspath(__file__)


def _load_r88():
    """Load the round-88 machinery only after its bytes match the pin; execute exactly those bytes."""
    with open(R88_COUNTER, "rb") as fh:
        data = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != R88_COUNTER_SHA256:
        print(f"MADO_MAKO_REGEX: SETUP_ERROR round-88 counter sha256 {digest} != pinned {R88_COUNTER_SHA256}",
              file=sys.stderr)
        sys.exit(2)
    spec = importlib.util.spec_from_loader("c1_r88_mako_fields", loader=None, origin=R88_COUNTER)
    module = importlib.util.module_from_spec(spec)
    module.__file__ = R88_COUNTER
    exec(compile(data, R88_COUNTER, "exec"), module.__dict__)
    module.SCHEMA = SCHEMA  # load_cases reads its module global at call time
    return module, digest


R88, R88_DIGEST = _load_r88()
SetupError = R88.SetupError
sha256, git, resolve_commit, canon = R88.sha256, R88.git, R88.resolve_commit, R88.canon


def predicate(n, correct, killed, m, carried, controls):
    """PRED-C1-r89-v1: correct == N, all M killed, carried == 61, every control strictly below N."""
    return (correct == n and killed == m and carried == CARRIED_CASES
            and all(score < n for score in controls.values()))


def carried_count(cases, r88_raw):
    """Round-88 cases present unchanged (canonical JSON), excluding the superseded ids."""
    try:
        prior = json.loads(r88_raw.decode("utf-8"))["cases"]
    except (UnicodeDecodeError, ValueError, KeyError, TypeError) as exc:
        raise SetupError(f"round-88 case file unreadable: {exc}")
    mine = {canon(case["raw"]) for case in cases}
    ids = {case["id"] for case in cases}
    if any(sid in ids for sid in SUPERSEDED):
        raise SetupError("a superseded round-88 case id is present in the round-89 set")
    kept = [entry for entry in prior if entry.get("id") not in SUPERSEDED]
    return sum(canon(entry) in mine for entry in kept), len(kept)


def score(tool_text, base_text, cases, mutants, scratch_root, carried, declared=DECLARED_MUTANTS,
          range_check=True, forgery=PYRE_FORGERY, controls_only=False):
    if range_check and not (N_MIN <= len(cases) <= N_MAX):
        raise SetupError(f"N={len(cases)} is outside {N_MIN}..{N_MAX}")
    result = R88.evaluate(tool_text, base_text, cases, mutants, scratch_root, carried, declared=declared,
                          range_check=False, carried_needed=CARRIED_CASES, forgery=forgery,
                          controls_only=controls_only)
    controls = {"naive-toplevel": result["naive"], "globals-include": result["globals"],
                "base-tool": result["base"], "python-re": result["forged"]}
    met = predicate(result["n"], result["correct"], result["killed"], result["m"], carried, controls)
    result["verdict"] = "TARGET_MET" if met else "TARGET_MISSED"
    result["lines"] = [line.replace("control inputs-ignored ", "control python-re ") for line in result["lines"]]
    return result


def read_inputs(args, need_rev=True):
    for name in ("repo", "base_rev", "cases", "scratch_root") + (("rev", "expect_cases_sha256",
                                                                  "expect_mutants_sha256",
                                                                  "expect_r88_cases_sha256") if need_rev else ()):
        if getattr(args, name, None) is None:
            raise SetupError(f"--{name.replace('_', '-')} is required")
    if not os.path.isdir(args.scratch_root):
        raise SetupError(f"scratch root is not a directory: {args.scratch_root}")
    try:
        with open(args.cases, "rb") as fh:
            cases_raw = fh.read()
    except OSError as exc:
        raise SetupError(f"cases unreadable: {exc}")
    return cases_raw


def run_controls(args):
    """Controls-only receipt before the freeze: naive-toplevel, globals-include, base-tool and python-re
    (derived from --candidate-file); the candidate itself and the mutants are not run."""
    cases_raw = read_inputs(args, need_rev=False)
    if args.candidate_file is None:
        raise SetupError("--candidate-file is required with --controls-only")
    base_commit = resolve_commit(args.repo, args.base_rev)
    with open(args.candidate_file, "rb") as fh:
        candidate_raw = fh.read()
    cases = R88.load_cases(cases_raw)
    base_raw = git(args.repo, "show", f"{base_commit}:{TOOL_PATH}")
    result = score(candidate_raw.decode("utf-8"), base_raw.decode("utf-8"), cases, [], args.scratch_root, 0,
                   declared=None, controls_only=True)
    n = result["n"]
    print(f"cases_sha256={sha256(cases_raw)} cases={n} candidate_file_sha256={sha256(candidate_raw)} "
          f"base_tool_sha256={sha256(base_raw)} base={base_commit} counter_sha256={sha256(open(THIS, 'rb').read())}")
    for line in result["lines"]:
        print(line)
    below = all(v < n for v in (result["naive"], result["globals"], result["base"], result["forged"]))
    print(f"MADO_MAKO_REGEX_CONTROLS: {'BELOW_N' if below else 'CONTROL_REACHES_N'} cases={n} "
          f"naive_correct={result['naive']} globals_include_correct={result['globals']} "
          f"base_tool_correct={result['base']} python_re_correct={result['forged']}")
    return 0 if below else 1


def run(args):
    cases_raw = read_inputs(args)
    commit = resolve_commit(args.repo, args.rev)
    base_commit = resolve_commit(args.repo, args.base_rev)
    if sha256(cases_raw) != args.expect_cases_sha256:
        raise SetupError(f"cases sha256 {sha256(cases_raw)} != expected {args.expect_cases_sha256}")
    cases = R88.load_cases(cases_raw)
    mutants_raw = git(args.repo, "show", f"{commit}:{MUTANTS_PATH}")
    if sha256(mutants_raw) != args.expect_mutants_sha256:
        raise SetupError(f"mutants sha256 {sha256(mutants_raw)} != expected {args.expect_mutants_sha256}")
    mutants = R88.load_mutants(mutants_raw)
    r88_raw = git(args.repo, "show", f"{commit}:{R88_CASES_PATH}")
    if sha256(r88_raw) != args.expect_r88_cases_sha256:
        raise SetupError(f"round-88 cases sha256 {sha256(r88_raw)} != expected {args.expect_r88_cases_sha256}")
    carried, prior_n = carried_count(cases, r88_raw)
    try:
        tool_raw = git(args.repo, "show", f"{commit}:{TOOL_PATH}")
        base_raw = git(args.repo, "show", f"{base_commit}:{TOOL_PATH}")
        tool_text, base_text = tool_raw.decode("utf-8"), base_raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SetupError(f"tool is not UTF-8: {exc}")
    print(f"r88_counter_sha256={R88_DIGEST} counter_sha256={sha256(open(THIS, 'rb').read())}")
    print(f"cases_sha256={sha256(cases_raw)} cases={len(cases)} carried={carried}/{prior_n}")
    print(f"tool_sha256={sha256(tool_raw)} commit={commit} base_tool_sha256={sha256(base_raw)} base={base_commit}")
    print(f"mutants={len(mutants)} mutants_sha256={sha256(mutants_raw)}")
    result = score(tool_text, base_text, cases, mutants, args.scratch_root, carried)
    for line in result["lines"]:
        print(line)
    print(f"controls naive_correct={result['naive']} globals_include_correct={result['globals']} "
          f"base_tool_correct={result['base']} python_re_correct={result['forged']}")
    for entry in result["mutants"]:
        print(f"mutant {entry['id']} {entry['status']}")
    print(
        f"MADO_MAKO_REGEX: {result['verdict']} rev={args.rev} base_rev={args.base_rev} cases={result['n']} "
        f"correct={result['correct']} carried={carried}/{CARRIED_CASES} mutants={result['m']} "
        f"killed={result['killed']} naive_correct={result['naive']} "
        f"globals_include_correct={result['globals']} base_tool_correct={result['base']} "
        f"python_re_correct={result['forged']} score={result['score']:.4f} score_scope=finite-cases "
        f"tool_sha256={sha256(tool_raw)} cases_sha256={sha256(cases_raw)}"
    )
    return 0 if result["verdict"] == "TARGET_MET" else 1


# ---------------------------------------------------------------- selftest

def selftest(scratch_root=None, candidate=None):
    checks = []

    def check(name, cond):
        checks.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name}")

    scratch = tempfile.mkdtemp(prefix="mado-mako-r89-selftest-", dir=scratch_root)
    try:
        check("round-88 machinery loads at its pinned sha256", R88_DIGEST == R88_COUNTER_SHA256)
        check("load_cases reads the round-89 schema name", R88.SCHEMA == SCHEMA)
        fixture = json.loads(json.dumps(R88.FIXTURE_CASES))
        fixture["schema"] = SCHEMA
        cases = R88.load_cases(json.dumps(fixture).encode("utf-8"))
        check("fixture cases load under the round-89 schema", len(cases) == 4)
        try:
            R88.load_cases(json.dumps(R88.FIXTURE_CASES).encode("utf-8"))
            check("a round-88 schema name is a setup error", False)
        except SetupError:
            check("a round-88 schema name is a setup error", True)
        prior = {"cases": [fixture["cases"][1], {"id": SUPERSEDED[0], "x": 1}]}
        carried, total = carried_count(cases, json.dumps(prior).encode("utf-8"))
        check("carried count skips the superseded id and finds the unchanged case", (carried, total) == (1, 1))
        edited = json.loads(json.dumps(prior))
        edited["cases"][0]["expect"]["effective"]["anchor"] = "center"
        check("carried count refuses an edited prior case",
              carried_count(cases, json.dumps(edited).encode("utf-8"))[0] == 0)
        bad = json.loads(json.dumps(fixture))
        bad["cases"][0]["id"] = SUPERSEDED[0]
        try:
            carried_count(R88.load_cases(json.dumps(bad).encode("utf-8")), json.dumps(prior).encode("utf-8"))
            check("a superseded id inside the new set is a setup error", False)
        except SetupError:
            check("a superseded id inside the new set is a setup error", True)
        controls = {"naive-toplevel": 0, "globals-include": 0, "base-tool": 0, "python-re": 0}
        c = CARRIED_CASES
        check("predicate holds when every conjunct holds", predicate(5, 5, 2, 2, c, controls))
        check("predicate fails at correct = N-1", not predicate(5, 4, 2, 2, c, controls))
        check("predicate fails at killed = M-1", not predicate(5, 5, 1, 2, c, controls))
        check("predicate fails at carried = 60", not predicate(5, 5, 2, 2, c - 1, controls))
        for name in controls:
            check(f"predicate fails when {name} reaches N", not predicate(5, 5, 2, 2, c, dict(controls, **{name: 5})))
            check(f"predicate holds when {name} is N-1", predicate(5, 5, 2, 2, c, dict(controls, **{name: 4})))
        tool_path = candidate or os.path.join(HERE, "..", "..", TOOL_PATH)
        tool = open(tool_path, encoding="utf-8").read()
        check("the tool under selftest carries the libc matcher (pass --candidate-file before landing)",
              "posix_ere_compile" in tool)
        if "posix_ere_compile" in tool:
            check("each python-re forgery anchor occurs once in the working-tree tool",
                  all(tool.count(old) == 1 for old, _ in PYRE_FORGERY))
            forged = tool
            for old, new in PYRE_FORGERY:
                forged = forged.replace(old, new, 1)
            check("the python-re forgery compiles", compile(forged, "forged", "exec") is not None)
        try:
            score("x", "x", cases, [], scratch, c)
            check("N outside 120..160 is a setup error", False)
        except SetupError as exc:
            check("N outside 120..160 is a setup error", "outside" in str(exc))
        res = score(R88.FIXTURE_TOOL, R88.FIXTURE_TOOL.replace("SECTION_WINS = True", "SECTION_WINS = False", 1),
                    cases, [("section-ignored", "SECTION_WINS = True", "SECTION_WINS = False")], scratch, c,
                    declared=None, range_check=False, forgery=R88.FIXTURE_FORGERY)
        check("score() over the round-88 fixture: N/N, mutant killed, controls below N -> TARGET_MET",
              res["correct"] == 4 and res["killed"] == 1 and res["verdict"] == "TARGET_MET")
        check("control lines are relabelled python-re",
              sum(line.startswith("control python-re ") for line in res["lines"]) == 4
              and not any(line.startswith("control inputs-ignored ") for line in res["lines"]))
        res = score(R88.FIXTURE_TOOL, R88.FIXTURE_TOOL, cases, [], scratch, c, declared=None, range_check=False,
                    forgery=R88.FIXTURE_FORGERY)
        check("a base tool reaching N -> TARGET_MISSED", res["verdict"] == "TARGET_MISSED")
        check("score() leaves the scratch root empty", os.listdir(scratch) == [])
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    passed = sum(checks)
    print(f"SELFTEST: passed={passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="mado round 89 C1 mako summary~/body~ counter")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--cases")
    ap.add_argument("--expect-cases-sha256")
    ap.add_argument("--expect-mutants-sha256")
    ap.add_argument("--expect-r88-cases-sha256")
    ap.add_argument("--scratch-root")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--controls-only", action="store_true")
    ap.add_argument("--candidate-file")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest(args.scratch_root, args.candidate_file)
    try:
        return run_controls(args) if args.controls_only else run(args)
    except SetupError as exc:
        print(f"MADO_MAKO_REGEX: SETUP_ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
