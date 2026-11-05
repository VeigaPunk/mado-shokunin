#!/usr/bin/env python3
"""mado round 88 — PRED-C2-r88-v1: score the include= containment stance of tools/mado-mako.py.

Predicate (declaration section "C2", verbatim): TARGET_MET iff the candidate tool's correct count equals
K, all declared containment mutants are killed, and both controls — the base tool (round base, do-nothing)
and the refuse-all-includes forgery derived from the candidate — score strictly below K.
Score = 10 * tool_correct / K on this finite case set only.

Stance under test (lane stance, not a mako rule): an include= target is read only when its fully
resolved path (realpath: every symlink and `..` resolved) lies inside a declared read root — --home and
each --read-root; otherwise it is refused before it is stat'ed or opened. The --config file itself is
named by the caller and is not subject to the roots.

Case schema `mako-containment-r88-v1`: each case owns a scratch root R; `files` maps paths relative to R
to text (`@ROOT@` is replaced by realpath(R)) or {"symlink_to": path relative to R}; `config` and `home`
and every `read_roots` entry are paths relative to R. Expectations reuse the round-87 verdict rule:
`expect.effective` subset equality plus `expect.refusals` none|present.

Inputs: --cases (sha256 MUST equal --expect-cases-sha256); tool and mutant list read from REV with
`git show` (mutant sha256 MUST equal --expect-mutants-sha256); base tool from --base-rev. Writes only in
a generation directory under --scratch-root, removed on exit; never writes inside the repository.

A tool mutant or forgery anchor that does not occur exactly once in the measured tool is a setup error
(exit 2), never a scored miss. Per-case reasons of both controls are printed. The base tool has no
--read-root option, so it exits 2 on every case that declares a read root (a CLI-surface failure, printed
as such).

Exit map: 0 TARGET_MET · 1 TARGET_MISSED · 2 setup error (never a verdict).
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
SCHEMA = "mako-containment-r88-v1"
K_MIN, K_MAX = 12, 32
DECLARED_MUTANTS = 7
TOOL_PATH = "tools/mado-mako.py"
MUTANTS_PATH = ".ufo/waves/round-88/controls/containment-mutants-r88.json"
FORGERY_OLD = "if not self.within_roots(real):"
FORGERY_NEW = "if True:"
THIS = os.path.abspath(__file__)


def _load_r87():
    """Load the round-87 machinery only after its bytes match the pin; execute exactly those bytes."""
    with open(R87_COUNTER, "rb") as fh:
        data = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != R87_COUNTER_SHA256:
        print(f"MADO_MAKO_CONTAINMENT: SETUP_ERROR round-87 counter sha256 {digest} != pinned {R87_COUNTER_SHA256}",
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
safe_relpath, load_mutants, tool_verdict = R87.safe_relpath, R87.load_mutants, R87.tool_verdict


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
        files = entry.get("files")
        if not isinstance(files, dict) or not files:
            raise SetupError(f"{cid}.files must be a non-empty object")
        out_files = {}
        for rel, content in files.items():
            safe_relpath(rel, f"{cid}.files")
            if isinstance(content, str):
                out_files[rel] = content
            elif isinstance(content, dict) and set(content) == {"symlink_to"}:
                out_files[rel] = {"symlink_to": safe_relpath(content["symlink_to"], f"{cid}.symlink")}
            else:
                raise SetupError(f"{cid}.files[{rel}]: must be text or {{symlink_to}}")
        config = safe_relpath(entry.get("config"), f"{cid}.config")
        home = safe_relpath(entry.get("home"), f"{cid}.home")
        roots = entry.get("read_roots", [])
        if not isinstance(roots, list):
            raise SetupError(f"{cid}.read_roots must be a list")
        roots = [safe_relpath(r, f"{cid}.read_roots") for r in roots]
        expect = entry.get("expect")
        if not isinstance(expect, dict) or not isinstance(expect.get("effective"), dict):
            raise SetupError(f"{cid}.expect.effective must be an object")
        if expect.get("refusals") not in ("none", "present"):
            raise SetupError(f"{cid}.expect.refusals must be 'none' or 'present'")
        cases.append({"id": cid, "files": out_files, "config": config, "home": home, "roots": roots,
                      "effective": expect["effective"], "refusals": expect["refusals"]})
    return cases


def materialize(cases, gen):
    places = {}
    for case in cases:
        root = os.path.join(gen, "case-" + case["id"])
        os.makedirs(root)
        real_root = os.path.realpath(root)
        for rel, content in case["files"].items():
            path = os.path.join(root, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if isinstance(content, dict):
                os.symlink(os.path.join(real_root, content["symlink_to"]), path)
            else:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(content.replace("@ROOT@", real_root))
        os.makedirs(os.path.join(root, case["home"]), exist_ok=True)
        places[case["id"]] = real_root
    return places


def run_tool(tool, case, root, gen):
    home = os.path.join(root, case["home"])
    argv = [sys.executable, "-I", tool, "--config", os.path.join(root, case["config"]), "--home", home]
    for rel in case["roots"]:
        argv += ["--read-root", os.path.join(root, rel)]
    env = {"PATH": os.environ.get("PATH", ""), "TMPDIR": gen, "HOME": home,
           "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
    try:
        return subprocess.run(argv, env=env, cwd=home, capture_output=True, timeout=R87.RUN_TIMEOUT)
    except subprocess.TimeoutExpired:
        return None


def run_all(tool, cases, places, gen):
    verdicts, reasons = [], []
    for case in cases:
        ok, reason = tool_verdict(case, run_tool(tool, case, places[case["id"]], gen))
        verdicts.append(ok)
        reasons.append(reason)
    return verdicts, reasons


CRASH_PREFIXES = ("timeout", "exit=", "bad-json", "not-object", "no-effective", "no-refusals-list")


def semantic_kill(candidate, mutant):
    """Killed only when, on some case, the verdict differs AND the mutant produced a well-formed
    result there (exit 0, JSON object with effective and refusals): a crash is not a kill."""
    return any(cv != mv and not mr.startswith(CRASH_PREFIXES)
               for cv, (mv, mr) in zip(candidate, mutant))


def predicate(k, correct, killed, m, controls):
    """PRED-C2-r88-v1: correct == K, all M killed, every control strictly below K."""
    return correct == k and killed == m and all(score < k for score in controls.values())


def write(path, text):
    with open(path, "wb") as fh:
        fh.write(text.encode("utf-8"))


def evaluate(tool_text, base_text, cases, mutants, scratch_root, declared=DECLARED_MUTANTS, range_check=True,
             controls_only=False):
    k = len(cases)
    if range_check and not (K_MIN <= k <= K_MAX):
        raise SetupError(f"K={k} is outside {K_MIN}..{K_MAX}")
    if declared is not None and len(mutants) != declared:
        raise SetupError(f"mutants={len(mutants)} but the declaration fixes M={declared}")
    if tool_text.count(FORGERY_OLD) != 1:
        raise SetupError(f"forgery anchor {FORGERY_OLD!r} occurs {tool_text.count(FORGERY_OLD)} times")
    for mid, old, _ in ([] if controls_only else mutants):
        if tool_text.count(old) != 1:
            raise SetupError(f"mutant {mid}: anchor occurs {tool_text.count(old)} times in the measured tool")
    gen = tempfile.mkdtemp(prefix="mado-contain-r88-", dir=scratch_root)
    try:
        places = materialize(cases, gen)
        tool = os.path.join(gen, "tool.py")
        write(tool, tool_text)
        if controls_only:
            verdicts, reasons, lines = [False] * k, ["not-run"] * k, []
        else:
            verdicts, reasons = run_all(tool, cases, places, gen)
            lines = [f"case {c['id']} {'ok' if ok else 'FAIL'} {why}" for c, ok, why in zip(cases, verdicts, reasons)]
        base = os.path.join(gen, "base-tool.py")
        write(base, base_text)
        base_verdicts, base_reasons = run_all(base, cases, places, gen)
        base_correct = sum(base_verdicts)
        forgery = os.path.join(gen, "refuse-all-includes.py")
        write(forgery, tool_text.replace(FORGERY_OLD, FORGERY_NEW, 1))
        forgery_verdicts, forgery_reasons = run_all(forgery, cases, places, gen)
        forgery_correct = sum(forgery_verdicts)
        lines += [f"control base-tool {c['id']} {'ok' if ok else 'FAIL'} {why}"
                  for c, ok, why in zip(cases, base_verdicts, base_reasons)]
        lines += [f"control refuse-all-includes {c['id']} {'ok' if ok else 'FAIL'} {why}"
                  for c, ok, why in zip(cases, forgery_verdicts, forgery_reasons)]
        results, killed = [], 0
        for index, (mid, old, new) in enumerate([] if controls_only else mutants):
            mutant = os.path.join(gen, f"mutant-{index}.py")
            write(mutant, tool_text.replace(old, new, 1))
            mverdicts, mreasons = run_all(mutant, cases, places, gen)
            hit = semantic_kill(verdicts, list(zip(mverdicts, mreasons)))
            crashed = any(r.startswith(CRASH_PREFIXES) for r in mreasons)
            killed += hit
            status = "killed" if hit else ("crashed-not-killed" if crashed else "survived")
            results.append({"id": mid, "status": status, "killed": hit})
        correct = sum(verdicts)
        m = len(mutants)
        met = predicate(k, correct, killed, m, {"base-tool": base_correct, "refuse-all-includes": forgery_correct})
        return {"k": k, "correct": correct, "mutants": results, "m": m, "killed": killed,
                "base": base_correct, "forgery": forgery_correct, "score": 10.0 * correct / k,
                "verdict": "TARGET_MET" if met else "TARGET_MISSED", "lines": lines}
    finally:
        shutil.rmtree(gen, ignore_errors=True)


def run_controls(args):
    """Controls-only receipt (before the freeze): base-tool and refuse-all-includes (derived from
    --candidate-file); the candidate itself and the mutants are not run."""
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
    result = evaluate(candidate_raw.decode("utf-8"), base_raw.decode("utf-8"), cases, [], args.scratch_root,
                      declared=None, controls_only=True)
    k = result["k"]
    print(f"cases_sha256={sha256(cases_raw)} cases={k} candidate_file_sha256={sha256(candidate_raw)} "
          f"base_tool_sha256={sha256(base_raw)} base={base_commit} counter_sha256={sha256(open(THIS, 'rb').read())}")
    for line in result["lines"]:
        print(line)
    below = result["base"] < k and result["forgery"] < k
    print(f"MADO_MAKO_CONTAINMENT_CONTROLS: {'BELOW_K' if below else 'CONTROL_REACHES_K'} cases={k} "
          f"base_tool_correct={result['base']} refuse_all_includes_correct={result['forgery']}")
    return 0 if below else 1


def run(args):
    if R87_DIGEST != R87_COUNTER_SHA256:
        raise SetupError(f"round-87 counter sha256 {R87_DIGEST} != pinned {R87_COUNTER_SHA256}")
    for name in ("repo", "rev", "base_rev", "cases", "scratch_root", "expect_cases_sha256",
                 "expect_mutants_sha256"):
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
    try:
        tool_raw = git(args.repo, "show", f"{commit}:{TOOL_PATH}")
        base_raw = git(args.repo, "show", f"{base_commit}:{TOOL_PATH}")
        tool_text, base_text = tool_raw.decode("utf-8"), base_raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SetupError(f"tool is not UTF-8: {exc}")
    print(f"r87_counter_sha256={R87_DIGEST} counter_sha256={sha256(open(THIS, 'rb').read())}")
    print(f"cases_sha256={sha256(cases_raw)} cases={len(cases)}")
    print(f"tool_sha256={sha256(tool_raw)} commit={commit} base_tool_sha256={sha256(base_raw)} base={base_commit}")
    print(f"mutants={len(mutants)} mutants_sha256={sha256(mutants_raw)}")
    result = evaluate(tool_text, base_text, cases, mutants, args.scratch_root, declared=DECLARED_MUTANTS)
    for line in result["lines"]:
        print(line)
    print(f"controls base_tool_correct={result['base']} refuse_all_includes_correct={result['forgery']}")
    for entry in result["mutants"]:
        print(f"mutant {entry['id']} {entry['status']}")
    print(
        f"MADO_MAKO_CONTAINMENT: {result['verdict']} rev={args.rev} base_rev={args.base_rev} "
        f"cases={result['k']} correct={result['correct']} mutants={result['m']} killed={result['killed']} "
        f"base_tool_correct={result['base']} refuse_all_includes_correct={result['forgery']} "
        f"score={result['score']:.4f} tool_sha256={sha256(tool_raw)} cases_sha256={sha256(cases_raw)}"
    )
    return R87.exit_for(result["verdict"])


# ---------------------------------------------------------------- selftest

FIXTURE_TOOL = '''#!/usr/bin/env python3
import argparse, json, os
CHECK = True


class Roots:
    def __init__(self, roots):
        self.roots = roots

    def within_roots(self, real):
        return not CHECK or any(real == r or real.startswith(r.rstrip("/") + "/") for r in self.roots)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config"); ap.add_argument("--home")
    ap.add_argument("--read-root", action="append", default=[])
    a = ap.parse_args()
    self = Roots([os.path.realpath(a.home)] + [os.path.realpath(r) for r in a.read_root])
    eff, ref = {}, []
    for line in open(a.config).read().splitlines():
        k, _, v = line.partition("=")
        if k == "include":
            t = os.path.join(a.home, v[2:]) if v.startswith("~/") else v
            real = os.path.realpath(t)
            if not self.within_roots(real):
                ref.append("outside")
                continue
            for l2 in open(real).read().splitlines():
                k2, _, v2 = l2.partition("=")
                eff[k2] = v2
        elif k:
            eff[k] = v
    print(json.dumps({"effective": eff, "refusals": ref}))


main()
'''

FIXTURE_CASES = [
    {"id": "escape", "files": {"home/c": "include=~/i\n", "home/i": {"symlink_to": "out/s"}, "out/s": "w=6\n"},
     "config": "home/c", "home": "home", "expect": {"effective": {}, "refusals": "present"}},
    {"id": "inside", "files": {"home/c": "include=~/i\n", "home/i": "w=4\n"},
     "config": "home/c", "home": "home", "expect": {"effective": {"w": "4"}, "refusals": "none"}},
    {"id": "declared", "files": {"home/c": "include=@ROOT@/out/s\n", "out/s": "w=6\n"},
     "config": "home/c", "home": "home", "read_roots": ["out"],
     "expect": {"effective": {"w": "6"}, "refusals": "none"}},
]


def selftest_run(scratch, tool_text, base_text):
    """In-process run() over a fixture git repo with the round constants scaled to the fixture."""
    import contextlib
    import io
    g = globals()
    saved = {k: g[k] for k in ("K_MIN", "K_MAX", "DECLARED_MUTANTS")}
    fixture = tempfile.mkdtemp(prefix="fixture-", dir=scratch)
    ok = True
    try:
        env = git_env()
        subprocess.run(["git", "-C", fixture, "init", "-q"], env=env, check=True)
        top = subprocess.run(["git", "-C", fixture, "rev-parse", "--show-toplevel"], env=env,
                             capture_output=True, text=True, check=True).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(fixture):
            return False
        cases_raw = json.dumps({"schema": SCHEMA, "cases": FIXTURE_CASES}).encode("utf-8")
        mutants_raw = json.dumps({"mutants": [{"id": "check-off", "old": "CHECK = True",
                                               "new": "CHECK = False"}]}).encode("utf-8")

        def commit(text, message):
            for rel, data in ((TOOL_PATH, text.encode("utf-8")), (MUTANTS_PATH, mutants_raw)):
                path = os.path.join(fixture, rel)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as fh:
                    fh.write(data)
            subprocess.run(["git", "-C", fixture, "add", "-A"], env=env, check=True)
            subprocess.run(["git", "-C", fixture, "-c", "user.name=mado-selftest", "-c",
                            "user.email=selftest@invalid", "commit", "-q", "-m", message], env=env, check=True)
            return resolve_commit(fixture, "HEAD")

        base = commit(base_text, "base")
        head = commit(tool_text, "candidate")
        cases_path = os.path.join(scratch, "fixture-cases-run.json")
        with open(cases_path, "wb") as fh:
            fh.write(cases_raw)
        g.update(K_MIN=1, K_MAX=10, DECLARED_MUTANTS=1)
        good = dict(repo=fixture, rev=head, base_rev=base, cases=cases_path, scratch_root=scratch,
                    expect_cases_sha256=sha256(cases_raw), expect_mutants_sha256=sha256(mutants_raw))
        with contextlib.redirect_stdout(io.StringIO()) as out:
            rc = run(argparse.Namespace(**good))
        ok &= rc == 0 and "MADO_MAKO_CONTAINMENT: TARGET_MET" in out.getvalue()
        for key in ("expect_cases_sha256", "expect_mutants_sha256"):
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

    scratch = tempfile.mkdtemp(prefix="mado-contain-r88-selftest-", dir=scratch_root)
    try:
        check("round-87 machinery loads at its pinned sha256", R87_DIGEST == R87_COUNTER_SHA256)
        cases = load_cases(json.dumps({"schema": SCHEMA, "cases": FIXTURE_CASES}).encode("utf-8"))
        check("fixture cases load", len(cases) == 3)
        try:
            load_cases(json.dumps({"schema": SCHEMA, "cases": [dict(FIXTURE_CASES[0], home="../x")]}).encode())
            check("a home outside the case root is a setup error", False)
        except SetupError:
            check("a home outside the case root is a setup error", True)
        anchored = FIXTURE_TOOL
        unchecked = anchored.replace("CHECK = True", "CHECK = False", 1)
        before = sorted(os.listdir(scratch))
        mutants = [("check-off", "CHECK = True", "CHECK = False")]
        good = evaluate(anchored, unchecked, cases, mutants, scratch, declared=None, range_check=False)
        check("containing fixture tool scores K/K", good["correct"] == 3)
        check("the check-off mutant is killed", good["killed"] == 1)
        check("base control (no containment) scores below K", good["base"] < 3)
        check("all conjuncts hold -> TARGET_MET", good["verdict"] == "TARGET_MET")
        check("evaluate leaves the scratch root as it found it", sorted(os.listdir(scratch)) == before)
        same = evaluate(anchored, anchored, cases, mutants, scratch, declared=None, range_check=False)
        check("base equal to candidate (do-nothing reaches K) -> TARGET_MISSED", same["verdict"] == "TARGET_MISSED")
        only_escape = [cases[0]]
        forged = evaluate(anchored, unchecked, only_escape, [], scratch, declared=None, range_check=False)
        check("without positive cases refuse-all forgery reaches K -> TARGET_MISSED",
              forged["forgery"] == 1 and forged["verdict"] == "TARGET_MISSED")
        try:
            evaluate(FIXTURE_TOOL.replace(FORGERY_OLD, "if not self.within_roots(real) :", 1), unchecked,
                     cases, mutants, scratch, declared=None, range_check=False)
            check("missing forgery anchor is a setup error", False)
        except SetupError:
            check("missing forgery anchor is a setup error", True)
        try:
            evaluate(anchored, unchecked, cases, mutants + [("ghost", "NO_SUCH_ANCHOR", "x")], scratch,
                     declared=None, range_check=False)
            check("absent mutant anchor is a setup error, not a scored miss", False)
        except SetupError:
            check("absent mutant anchor is a setup error, not a scored miss", True)
        check("per-case control reasons are printed", sum(l.startswith("control ") for l in good["lines"]) == 6)
        wrong_tool = anchored.replace("eff[k2] = v2", "eff[k2] = v2 + 'x'", 1)
        one_wrong = evaluate(wrong_tool, unchecked, cases, [], scratch, declared=None, range_check=False)
        check("a tool wrong on a case is not TARGET_MET", one_wrong["correct"] < 3
              and one_wrong["verdict"] == "TARGET_MISSED")
        noop = evaluate(anchored, unchecked, cases, mutants + [("noop", "import argparse, json, os",
                                                                "import argparse, json, os  # noop")],
                        scratch, declared=None, range_check=False)
        check("a surviving mutant -> TARGET_MISSED", noop["killed"] == 1 and noop["verdict"] == "TARGET_MISSED")
        crash = evaluate(anchored, unchecked, cases, [("import-break", "import argparse, json, os",
                                                      "import argparse, json, os (")],
                         scratch, declared=None, range_check=False)
        check("a mutant that crashes on every case is not counted killed",
              crash["killed"] == 0 and crash["mutants"][0]["status"] == "crashed-not-killed")
        try:
            evaluate(anchored, unchecked, cases, mutants, scratch, declared=1)
            check("K outside the declared range is a setup error (M matches)", False)
        except SetupError as exc:
            check("K outside the declared range is a setup error (M matches)", "outside" in str(exc))
        try:
            evaluate(anchored, unchecked, cases, mutants, scratch, declared=2, range_check=False)
            check("M different from the declared count is a setup error (K unchecked)", False)
        except SetupError as exc:
            check("M different from the declared count is a setup error (K unchecked)", "declaration" in str(exc))
        controls = {"base-tool": 0, "refuse-all-includes": 0}
        check("predicate holds when every conjunct holds", predicate(5, 5, 2, 2, controls))
        check("predicate fails at correct = K-1", not predicate(5, 4, 2, 2, controls))
        check("predicate fails at killed = M-1", not predicate(5, 5, 1, 2, controls))
        for name in controls:
            check(f"predicate fails when {name} reaches K", not predicate(5, 5, 2, 2, dict(controls, **{name: 5})))
            check(f"predicate holds when {name} is K-1", predicate(5, 5, 2, 2, dict(controls, **{name: 4})))
        check("run() honours every sha pin", selftest_run(scratch, anchored, unchecked))
        ctl = evaluate(anchored, unchecked, cases, mutants, scratch, declared=None, range_check=False,
                       controls_only=True)
        check("controls-only mode runs neither the candidate nor the mutants",
              ctl["correct"] == 0 and ctl["mutants"] == [] and ctl["base"] < 3 and ctl["forgery"] < 3
              and not any(line.startswith("case ") for line in ctl["lines"]))
        proc = subprocess.run([sys.executable, "-I", THIS, "--repo", scratch], capture_output=True, env=git_env())
        check("CLI: missing required arguments exit 2", proc.returncode == 2)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    passed = sum(checks)
    print(f"SELFTEST: passed={passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="mado round 88 C2 include containment counter")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--cases")
    ap.add_argument("--expect-cases-sha256")
    ap.add_argument("--expect-mutants-sha256")
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
        print(f"MADO_MAKO_CONTAINMENT: SETUP_ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
