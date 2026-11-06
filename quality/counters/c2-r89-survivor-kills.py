#!/usr/bin/env python3
"""mado round 89 — PRED-C2-r89-v1: do the round-89 supplementary cases kill round 88's routed survivors?

Predicate (declaration section "C2", verbatim): TARGET_MET iff
  (a) the measured tool is correct on every case of B ∪ S, where B = the frozen round-88 case sets
      (mako-cases-r88.json minus c53-summary-tilde-refused, plus containment-cases-r88.json) and S = the
      two round-89 supplementary sets (survivor-cases-c1side-r89.json, survivor-cases-c2side-r89.json);
  (b) every survivor mutant except the declared crash-only RM6C2 is killed over B ∪ S (7 of 7);
  (c) the do-nothing control — the identical scoring over B alone — kills strictly fewer than 7.
A kill is the round-88 semantic kill: on some case the verdict differs AND the mutant produced a
well-formed result there; a crash is not a kill. RM6C2 is scored and printed but never counted: every
case that separates it from the tool makes it recurse until RecursionError (declaration, "RM6C2").

Machinery: the frozen round-88 counters quality/counters/c1-r88-mako-fields.py and
c2-r88-include-containment.py, each loaded only when its sha256 equals its pin (each in turn pins the
round-87 machinery). Their case loaders, materializers, tool runners and verdict functions are used
unchanged; this counter adds the survivor list, the supplementary sets and the B-only control.

Inputs (all read with `git show REV:<path>`): the tool, the survivor list (sha256 MUST equal
--expect-survivors-sha256), both supplementary sets (--expect-c1side-sha256, --expect-c2side-sha256),
both round-88 sets (sha256 MUST equal the frozen round-88 pins below). Writes only inside a generation
directory under --scratch-root, removed on exit.

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
PINS = {
    "c1-r88-mako-fields.py": "3678425addb5f661d3f284ef423e3566446b54714cb2148c5696a8cdfe11cc1f",
    "c2-r88-include-containment.py": "f8e18b7c915fe831e6eaafcd09fad0af9ac23d89514317f131fb1ed409e96767",
}
TOOL_PATH = "tools/mado-mako.py"
SURVIVORS_PATH = ".ufo/waves/round-89/controls/survivor-mutants-r89.json"
C1SIDE_PATH = ".ufo/waves/round-89/controls/survivor-cases-c1side-r89.json"
C2SIDE_PATH = ".ufo/waves/round-89/controls/survivor-cases-c2side-r89.json"
R88_C1_CASES = (".ufo/waves/round-88/controls/mako-cases-r88.json",
                "a0e81b191fb0f80ca352699ede47962c1ac01c1ae8e9e15ccf50b1d7fab4a091")
R88_C2_CASES = (".ufo/waves/round-88/controls/containment-cases-r88.json",
                "8b16c0cb0d73eb2e245b4b543db0a0396c824314cb8dbd26e5ad26214f20d039")
EXCLUDED_B = ("c53-summary-tilde-refused",)
CRASH_ONLY = ("RM6C2-cycle-detected-on-lexical-target",)
DECLARED_SURVIVORS = 8
THIS = os.path.abspath(__file__)


def _load(name):
    path = os.path.join(HERE, name)
    with open(path, "rb") as fh:
        data = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != PINS[name]:
        print(f"MADO_MAKO_SURVIVORS: SETUP_ERROR {name} sha256 {digest} != pinned {PINS[name]}", file=sys.stderr)
        sys.exit(2)
    modname = name[:-3].replace("-", "_")
    spec = importlib.util.spec_from_loader(modname, loader=None, origin=path)
    module = importlib.util.module_from_spec(spec)
    module.__file__ = path
    exec(compile(data, path, "exec"), module.__dict__)
    return module


F = _load("c1-r88-mako-fields.py")  # criteria-side machinery (home_files, notification inputs)
K = _load("c2-r88-include-containment.py")  # containment-side machinery (read roots)
SetupError = F.SetupError
sha256, git, resolve_commit = F.sha256, F.git, F.resolve_commit


def predicate(correct, total, killed_full, killed_base, counted):
    """PRED-C2-r89-v1: correct on all of B ∪ S, all counted survivors killed, B-only control below."""
    return correct == total and killed_full == counted and killed_base < counted


def side_results(tool, fcases, kcases, gen):
    """Verdicts and reasons over the criteria-side then the containment-side cases, in a fixed order."""
    homes = F.materialize(fcases, gen)
    places = K.materialize(kcases, gen)
    fv, fr = F.run_all(tool, fcases, homes, gen)
    kv, kr = K.run_all(tool, kcases, places, gen)
    return fv + kv, fr + kr


def evaluate(tool_text, base_f, base_k, supp_f, supp_k, survivors, scratch_root,
             declared=DECLARED_SURVIVORS, crash_only=CRASH_ONLY):
    if declared is not None and len(survivors) != declared:
        raise SetupError(f"survivors={len(survivors)} but the declaration fixes {declared}")
    for mid, old, _ in survivors:
        if tool_text.count(old) != 1:
            raise SetupError(f"survivor {mid}: anchor occurs {tool_text.count(old)} times in the measured tool")
    for mid in crash_only:
        if mid not in [s[0] for s in survivors]:
            raise SetupError(f"declared crash-only id {mid} is not in the survivor list")
    nb = len(base_f) + len(base_k)
    gen = tempfile.mkdtemp(prefix="mado-mako-r89-surv-", dir=scratch_root)
    try:
        def run(text, name):
            path = os.path.join(gen, name)
            with open(path, "wb") as fh:
                fh.write(text.encode("utf-8"))
            sub = tempfile.mkdtemp(prefix=name + "-", dir=gen)
            return side_results(path, base_f + supp_f, base_k + supp_k, sub)

        cv, cr = run(tool_text, "tool.py")
        ids = [c["id"] for c in base_f + supp_f] + [c["id"] for c in base_k + supp_k]
        # fixed order: base_f, supp_f, base_k, supp_k -> index of the B-only cases
        nf_b, nf = len(base_f), len(base_f) + len(supp_f)
        b_index = set(range(nf_b)) | set(range(nf, nf + len(base_k)))
        lines = [f"case {cid} {'ok' if ok else 'FAIL'} {why}" for cid, ok, why in zip(ids, cv, cr)]
        rows, killed_full, killed_base = [], 0, 0
        for index, (mid, old, new) in enumerate(survivors):
            mv, mr = run(tool_text.replace(old, new, 1), f"survivor-{index}.py")
            pairs = list(zip(mv, mr))
            full = F.semantic_kill(cv, pairs)
            base = F.semantic_kill([cv[i] for i in sorted(b_index)], [pairs[i] for i in sorted(b_index)])
            crashed = [ids[i] for i, (v, r) in enumerate(pairs) if r.startswith(F.CRASH_PREFIXES)]
            counted = mid not in crash_only
            killed_full += full and counted
            killed_base += base and counted
            status = "killed" if full else ("crashed-not-killed" if crashed else "survived")
            rows.append({"id": mid, "status": status, "killed_by_b": base, "counted": counted,
                         "crashed_on": crashed,
                         "differs_on": [ids[i] for i, (v, r) in enumerate(pairs) if v != cv[i]]})
        counted_n = sum(1 for s in survivors if s[0] not in crash_only)
        total = len(ids)
        correct = sum(cv)
        met = predicate(correct, total, killed_full, killed_base, counted_n)
        return {"total": total, "b_cases": nb, "correct": correct, "killed_full": killed_full,
                "killed_base": killed_base, "counted": counted_n, "rows": rows, "lines": lines,
                "verdict": "TARGET_MET" if met else "TARGET_MISSED"}
    finally:
        shutil.rmtree(gen, ignore_errors=True)


def read_at(repo, commit, path, want=None, label=None):
    raw = git(repo, "show", f"{commit}:{path}")
    if want is not None and sha256(raw) != want:
        raise SetupError(f"{label or path} sha256 {sha256(raw)} != expected {want}")
    return raw


def load_k(raw):
    return K.load_cases(raw)


def run(args):
    for name in ("repo", "rev", "scratch_root", "expect_survivors_sha256", "expect_c1side_sha256",
                 "expect_c2side_sha256"):
        if getattr(args, name) is None:
            raise SetupError(f"--{name.replace('_', '-')} is required")
    if not os.path.isdir(args.scratch_root):
        raise SetupError(f"scratch root is not a directory: {args.scratch_root}")
    commit = resolve_commit(args.repo, args.rev)
    surv_raw = read_at(args.repo, commit, SURVIVORS_PATH, args.expect_survivors_sha256, "survivor list")
    f1_raw = read_at(args.repo, commit, C1SIDE_PATH, args.expect_c1side_sha256, "c1side set")
    k1_raw = read_at(args.repo, commit, C2SIDE_PATH, args.expect_c2side_sha256, "c2side set")
    fb_raw = read_at(args.repo, commit, R88_C1_CASES[0], R88_C1_CASES[1], "round-88 mako cases")
    kb_raw = read_at(args.repo, commit, R88_C2_CASES[0], R88_C2_CASES[1], "round-88 containment cases")
    tool_raw = git(args.repo, "show", f"{commit}:{TOOL_PATH}")
    survivors = F.load_mutants(surv_raw)
    base_f = [c for c in F.load_cases(fb_raw) if c["id"] not in EXCLUDED_B]
    base_k = load_k(kb_raw)
    supp_f, supp_k = F.load_cases(f1_raw), load_k(k1_raw)
    all_ids = [c["id"] for c in base_f + supp_f + base_k + supp_k]
    if len(set(all_ids)) != len(all_ids):
        raise SetupError("a case id repeats across B ∪ S")
    if not supp_f or not supp_k:
        raise SetupError("both supplementary sets must be non-empty")
    print(f"counter_sha256={sha256(open(THIS, 'rb').read())} pins={json.dumps(PINS, sort_keys=True)}")
    print(f"tool_sha256={sha256(tool_raw)} commit={commit} survivors_sha256={sha256(surv_raw)} "
          f"c1side_sha256={sha256(f1_raw)} c2side_sha256={sha256(k1_raw)}")
    print(f"B={len(base_f)}+{len(base_k)} S={len(supp_f)}+{len(supp_k)} excluded_from_B={','.join(EXCLUDED_B)}")
    result = evaluate(tool_raw.decode("utf-8"), base_f, base_k, supp_f, supp_k, survivors, args.scratch_root)
    for line in result["lines"]:
        print(line)
    for row in result["rows"]:
        print(f"survivor {row['id']} {row['status']} killed_by_B_only={str(row['killed_by_b']).lower()} "
              f"counted={str(row['counted']).lower()} differs_on={','.join(row['differs_on']) or '-'} "
              f"crashed_on={','.join(row['crashed_on']) or '-'}")
    print(f"MADO_MAKO_SURVIVORS: {result['verdict']} rev={args.rev} cases={result['total']} "
          f"correct={result['correct']} counted={result['counted']} killed={result['killed_full']} "
          f"do_nothing_B_only_killed={result['killed_base']} crash_only={','.join(CRASH_ONLY)} "
          f"tool_sha256={sha256(tool_raw)}")
    return 0 if result["verdict"] == "TARGET_MET" else 1


# ---------------------------------------------------------------- selftest

FIX_CFG = "anchor=bottom-left\n[app-name=Alpha]\nanchor=bottom-center\n"
FIX_F = {"schema": "mako-cases-r88-v1", "cases": [
    {"id": "b-app-exact", "config": ".config/mako/config", "home_files": {".config/mako/config": FIX_CFG},
     "args": {"app-name": "Alpha"}, "expect": {"effective": {"anchor": "bottom-center"}, "refusals": "none"}},
    {"id": "s-app-case", "config": ".config/mako/config", "home_files": {".config/mako/config": FIX_CFG},
     "args": {"app-name": "alpha"}, "expect": {"effective": {"anchor": "bottom-left"}, "refusals": "none"}},
]}
FIX_K = {"schema": "mako-containment-r88-v1", "cases": [
    {"id": "b-inside", "files": {"home/c": "include=~/i\n", "home/i": "width=4\n"}, "config": "home/c",
     "home": "home", "expect": {"effective": {"width": "4"}, "refusals": "none"}},
    {"id": "s-root-is-a-file", "files": {"home/c": "include=@ROOT@/roots/x.ini\n", "roots/x.ini": "width=321\n"},
     "config": "home/c", "home": "home", "read_roots": ["roots/x.ini"],
     "expect": {"effective": {"width": "321"}, "refusals": "none"}},
]}


def selftest(scratch_root=None, tool_path=None):
    """Hermetic checks over the lane tool (working tree, or --tool-file) and two-case fixture sets."""
    checks = []

    def check(name, cond):
        checks.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name}")

    scratch = tempfile.mkdtemp(prefix="mado-mako-r89-surv-selftest-", dir=scratch_root)
    try:
        check("predicate holds at correct=N, killed=all, B-only below", predicate(10, 10, 7, 0, 7))
        check("predicate fails at correct = N-1", not predicate(9, 10, 7, 0, 7))
        check("predicate fails at killed = counted-1", not predicate(10, 10, 6, 0, 7))
        check("predicate fails when the B-only control reaches counted", not predicate(10, 10, 7, 7, 7))
        check("predicate holds when the B-only control is counted-1", predicate(10, 10, 7, 6, 7))
        tool = open(tool_path or os.path.join(HERE, "..", "..", TOOL_PATH), encoding="utf-8").read()
        fc = F.load_cases(json.dumps(FIX_F).encode("utf-8"))
        kc = K.load_cases(json.dumps(FIX_K).encode("utf-8"))
        surv = [("app-casefold", "mismatch = mismatch or self.app_name != value",
                 "mismatch = mismatch or self.app_name.casefold() != value.casefold()"),
                ("root-equality", "if real == root or real.startswith(prefix):", "if real.startswith(prefix):")]
        r = evaluate(tool, fc[:1], kc[:1], fc[1:], kc[1:], surv, scratch, declared=None, crash_only=())
        check("the lane tool is correct on all four fixture cases", r["correct"] == 4 == r["total"])
        check("survivors killed only by S count, B alone kills none -> TARGET_MET",
              r["killed_full"] == 2 and r["killed_base"] == 0 and r["verdict"] == "TARGET_MET")
        check("each survivor is separated on its own side's S case",
              r["rows"][0]["differs_on"] == ["s-app-case"] and r["rows"][1]["differs_on"] == ["s-root-is-a-file"])
        r = evaluate(tool, fc, kc, [], [], surv, scratch, declared=None, crash_only=())
        check("when the separating cases sit in B, the do-nothing conjunct fails",
              r["killed_base"] == 2 and r["verdict"] == "TARGET_MISSED")
        noop = surv + [("noop", "import json\n", "import json\n")]
        r = evaluate(tool, fc[:1], kc[:1], fc[1:], kc[1:], noop, scratch, declared=None, crash_only=())
        check("an equivalent survivor stays survived -> TARGET_MISSED",
              r["rows"][2]["status"] == "survived" and r["verdict"] == "TARGET_MISSED")
        crash = surv + [("import-break", "import json\n", "import json (\n")]
        r = evaluate(tool, fc[:1], kc[:1], fc[1:], kc[1:], crash, scratch, declared=None, crash_only=())
        check("a crashing survivor is crashed-not-killed and blocks TARGET_MET when counted",
              r["rows"][2]["status"] == "crashed-not-killed" and r["verdict"] == "TARGET_MISSED")
        r = evaluate(tool, fc[:1], kc[:1], fc[1:], kc[1:], crash, scratch, declared=None,
                     crash_only=("import-break",))
        check("a declared crash-only id is scored but not counted", r["counted"] == 2
              and r["rows"][2]["counted"] is False and r["verdict"] == "TARGET_MET")
        wrong = dict(FIX_F, cases=[dict(FIX_F["cases"][1], expect={"effective": {"anchor": "center"},
                                                                    "refusals": "none"})])
        r = evaluate(tool, fc[:1], kc[:1], F.load_cases(json.dumps(wrong).encode("utf-8")), kc[1:], surv, scratch,
                     declared=None, crash_only=())
        check("a wrong expectation in S fails the correct-on-all conjunct", r["correct"] == r["total"] - 1
              and r["verdict"] == "TARGET_MISSED")
        for label, survs, declared, conly in (
                ("absent anchor", surv + [("ghost", "NO_SUCH_ANCHOR", "x")], None, ()),
                ("count differs from the declaration", surv, 3, ()),
                ("crash-only id absent from the list", surv, None, ("nope",))):
            try:
                evaluate(tool, fc[:1], kc[:1], fc[1:], kc[1:], survs, scratch, declared=declared, crash_only=conly)
                check(f"{label} is a setup error", False)
            except SetupError:
                check(f"{label} is a setup error", True)
        check("evaluate leaves the scratch root empty", os.listdir(scratch) == [])
        proc = __import__("subprocess").run([sys.executable, "-I", THIS, "--repo", scratch, "--rev", "HEAD"],
                                            capture_output=True, env=F.git_env())
        check("CLI: missing required arguments exit 2", proc.returncode == 2)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    passed = sum(checks)
    print(f"SELFTEST: passed={passed}/{len(checks)}")
    return 0 if passed == len(checks) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="mado round 89 C2 survivor-kill counter")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--expect-survivors-sha256")
    ap.add_argument("--expect-c1side-sha256")
    ap.add_argument("--expect-c2side-sha256")
    ap.add_argument("--scratch-root")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--tool-file", help="selftest only: score this tool file instead of the working tree's")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest(args.scratch_root, args.tool_file)
    try:
        return run(args)
    except SetupError as exc:
        print(f"MADO_MAKO_SURVIVORS: SETUP_ERROR {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
