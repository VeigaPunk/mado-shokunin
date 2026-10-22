#!/usr/bin/env python3
"""Round-23 C1 mutation harness for .ufo/waves/round-23/repair/truth.py.

The lane repair/ directory is READ ONLY. Every mutant and every scenario lives
under /fast/scratch/hyaku/mado-r23/MutTruth/.

Protocol (L1 note):
  * control first: the unmutated truth.py must produce its DECLARED expected
    verdict on the same scenario input; otherwise that scenario is
    inconclusive for that mutant, never a kill.
  * a mutant is KILLED only when it yields a different WELL-FORMED verdict
    (JSON schema output, or a clean refusal message with no traceback).
  * crashes / timeouts / layout errors are INCONCLUSIVE.
  * restore is verified byte-exactly (sha256) and behaviourally after every run.

Scenarios reset their files before every run, so a scenario that mutates its
own inputs stays deterministic across runs.
"""
import hashlib, json, shutil, subprocess, sys, traceback
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-23/repair")
SCRATCH = Path("/fast/scratch/hyaku/mado-r23/MutTruth")
SCEN = SCRATCH / "scenarios"
PRISTINE_TRUTH = (LANE / "truth.py").read_text()
PRISTINE_EXPECTED_SHA = hashlib.sha256((LANE / "expected.json").read_bytes()).hexdigest()
PRISTINE_TRUTH_SHA = hashlib.sha256(PRISTINE_TRUTH.encode()).hexdigest()
TRUTH_SCHEMA = "mado-r23-repair-truth-v1"


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------------- fixture code --
UNSAFE_OS_USED = (
    "import os\n"
    "import subprocess\n"
    "\n"
    "subprocess.run([\"pacman\", \"-Q\", \"probe-unsafe-os\"])\n"
    "probe_home = os.environ.get(\"HOME\", \"\")\n"
)
UNSAFE_OS_UNUSED = (
    "import os  # imported but never referenced\n"
    "import subprocess\n"
    "\n"
    "subprocess.run([\"pacman\", \"-Q\", \"probe-unsafe-import\"])\n"
)
FORBIDDEN_PRESENT = (
    "import subprocess\n"
    "\n"
    "def run():\n"
    "    subprocess.run([\"pacman\", \"-S\", \"r23-hook-dict\"])\n"
    "    subprocess.run([\"pacman\", \"-S\", \"r23-forbidden-extra\"])\n"
    "\n"
    "run()\n"
)
MULTI_CALL_EXACT = (
    "import subprocess\n"
    "\n"
    "def run():\n"
    "    subprocess.run([\"pacman\", \"-Q\", \"r23-multi-first\"])\n"
    "    subprocess.run([\"pacman\", \"-Q\", \"r23-multi-second\"])\n"
    "\n"
    "run()\n"
)


def tamper_fixture_code(abs_expected_path):
    """A SAFE-looking fixture that rewrites expected.json mid-run.

    safe() only rejects a fixed Name blacklist plus non-subprocess imports, so
    this code passes the gate; it touches nothing outside the scenario dir.
    """
    return (
        "import subprocess\n"
        "\n"
        "_b = __builtins__\n"
        "if not isinstance(_b, dict):\n"
        "    _b = _b.__dict__\n"
        "_open = _b['open']\n"
        "subprocess.run([\"pacman\", \"-Q\", \"probe-midrun-tamper\"])\n"
        "with _open(%r, 'a') as _fh:\n"
        "    _fh.write('\\n')\n" % abs_expected_path
    )


def fixture_jsonl(code, name="probe"):
    rec = {"message": {"content": [{"arguments": {"code": code, "language": "py",
                                                  "reset": False},
                                     "id": name + "-0", "name": "eval", "type": "toolCall"}],
                       "role": "assistant"}, "type": "message"}
    return json.dumps(rec) + "\n"


# ------------------------------------------------------------------ scenarios --
class Scenario:
    def __init__(self, name, d, expected_bytes, fixture_bytes, truth_src):
        self.name, self.dir = name, d
        self.expected_bytes = expected_bytes
        self.fixture_bytes = fixture_bytes
        self.truth_src = truth_src

    def reset(self, truth_src=None):
        """Restore inputs (expected.json, fixtures) only.

        truth.py is NOT rewritten here: the caller may have installed a mutant
        into it and expects it to survive into the run.
        """
        (self.dir / "expected.json").write_bytes(self.expected_bytes)
        for fname, blob in self.fixture_bytes.items():
            (self.dir / "fixtures" / fname).write_bytes(blob)
        if truth_src is not None:
            (self.dir / "truth.py").write_text(truth_src)

    def snapshot(self):
        return {"expected_sha256": sha_bytes((self.dir / "expected.json").read_bytes()),
                "fixtures": {f.name: sha_bytes(f.read_bytes())
                             for f in sorted((self.dir / "fixtures").iterdir())},
                "truth_sha256": sha_bytes((self.dir / "truth.py").read_bytes())}


def build_scenario(name, expected_bytes=None, extra_cases=None, tamper_fixture=None,
                   update_expected_sha=True, truth_src=None):
    d = SCEN / name
    shutil.rmtree(d, ignore_errors=True)
    (d / "fixtures").mkdir(parents=True)
    fixture_bytes = {}
    for f in sorted((LANE / "fixtures").iterdir()):
        shutil.copy2(f, d / "fixtures" / f.name)
        fixture_bytes[f.name] = f.read_bytes()

    data = json.loads((LANE / "expected.json").read_text())
    for case in extra_cases or []:
        case = dict(case)
        code = case.pop("code")
        fname = Path(case["fixture"]).name
        blob = fixture_jsonl(code, case["id"]).encode()
        (d / "fixtures" / fname).write_bytes(blob)
        fixture_bytes[fname] = blob
        case["sha256"] = sha_bytes(blob)
        data["cases"].append(case)

    if expected_bytes is None:
        expected_bytes = (json.dumps(data, indent=2) + "\n").encode()
    (d / "expected.json").write_bytes(expected_bytes)

    if tamper_fixture:
        blob = fixture_bytes[tamper_fixture] + b"\n"
        (d / "fixtures" / tamper_fixture).write_bytes(blob)
        fixture_bytes[tamper_fixture] = blob

    src = truth_src if truth_src is not None else PRISTINE_TRUTH
    if update_expected_sha:
        needle = 'EXPECTED_SHA = "%s"' % PRISTINE_EXPECTED_SHA
        assert src.count(needle) == 1
        src = src.replace(needle, 'EXPECTED_SHA = "%s"' % sha_bytes(expected_bytes))
    (d / "truth.py").write_text(src)
    return Scenario(name, d, expected_bytes, fixture_bytes, src)


def build_all_scenarios():
    scen = {}

    # S0: the frozen 12-case repair set, byte-exact.
    scen["S0-frozen"] = build_scenario("S0-frozen")

    # S1: expected.json bytes tampered, EXPECTED_SHA constant NOT updated.
    scen["S1-tamper-expected"] = build_scenario(
        "S1-tamper-expected",
        expected_bytes=(LANE / "expected.json").read_bytes() + b"\n",
        update_expected_sha=False)

    # S2: one fixture's bytes tampered, expected.json untouched.
    scen["S2-tamper-fixture"] = build_scenario(
        "S2-tamper-fixture", tamper_fixture="ReturnedGlobalHelper.jsonl")

    # S3: two unsafe fixtures added (one references os, one does not).
    scen["S3-unsafe"] = build_scenario("S3-unsafe", extra_cases=[
        {"id": "ProbeUnsafeOsUsed", "kind": "present", "forbid_any": [],
         "want_present": ["pacman -Q probe-unsafe-os"],
         "fixture": "fixtures/ProbeUnsafeOsUsed.jsonl", "code": UNSAFE_OS_USED},
        {"id": "ProbeUnsafeOsUnused", "kind": "present", "forbid_any": [],
         "want_present": ["pacman -Q probe-unsafe-import"],
         "fixture": "fixtures/ProbeUnsafeOsUnused.jsonl", "code": UNSAFE_OS_UNUSED},
    ])

    # S4: present-kind case whose fixture also executes a forbidden command.
    scen["S4-forbidden-present"] = build_scenario("S4-forbidden-present", extra_cases=[
        {"id": "ProbeForbiddenPresent", "kind": "present",
         "forbid_any": ["pacman -S r23-forbidden-extra"],
         "want_present": ["pacman -S r23-hook-dict"],
         "fixture": "fixtures/ProbeForbiddenPresent.jsonl", "code": FORBIDDEN_PRESENT},
    ])

    # S5: exact-kind case whose fixture executes MORE commands than want lists.
    scen["S5-extra-executed"] = build_scenario("S5-extra-executed", extra_cases=[
        {"id": "ProbeMultiCallExact", "kind": "exact", "forbid_any": [],
         "want": [{"class": "package_query", "command": "pacman -Q r23-multi-first",
                   "evidence": "observed"}],
         "fixture": "fixtures/ProbeMultiCallExact.jsonl", "code": MULTI_CALL_EXACT},
    ])

    # S6: deliberately WRONG expectation copy (want names a command never executed).
    data = json.loads((LANE / "expected.json").read_text())
    for c in data["cases"]:
        if c["id"] == "ReturnedGlobalHelper":
            c["want"][0]["command"] = "pacman -Q r22-nhb-BOGUS"
    scen["S6-wrong-expect-bogus"] = build_scenario(
        "S6-wrong-expect-bogus",
        expected_bytes=(json.dumps(data, indent=2) + "\n").encode())

    # S7: deliberately WRONG expectation copy (duplicate want row: set-subset of truth).
    data = json.loads((LANE / "expected.json").read_text())
    for c in data["cases"]:
        if c["id"] == "ReturnedGlobalHelper":
            c["want"].append(dict(c["want"][0]))
    scen["S7-wrong-expect-duplicate"] = build_scenario(
        "S7-wrong-expect-duplicate",
        expected_bytes=(json.dumps(data, indent=2) + "\n").encode())

    # S8: mid-run tamper: the fixture rewrites expected.json while truth.py runs.
    s8 = build_scenario("S8-midrun-tamper", extra_cases=[
        {"id": "ProbeMidRunTamper", "kind": "present", "forbid_any": [],
         "want_present": ["pacman -Q probe-midrun-tamper"],
         "fixture": "fixtures/ProbeMidRunTamper.jsonl", "code": "PLACEHOLDER"},
    ])
    code = tamper_fixture_code(str((s8.dir / "expected.json").resolve()))
    blob = fixture_jsonl(code, "ProbeMidRunTamper").encode()
    (s8.dir / "fixtures" / "ProbeMidRunTamper.jsonl").write_bytes(blob)
    data = json.loads((s8.dir / "expected.json").read_text())
    for c in data["cases"]:
        if c["id"] == "ProbeMidRunTamper":
            c["sha256"] = sha_bytes(blob)
    eb = (json.dumps(data, indent=2) + "\n").encode()
    (s8.dir / "expected.json").write_bytes(eb)
    s8.expected_bytes = eb
    s8.fixture_bytes["ProbeMidRunTamper.jsonl"] = blob
    src = PRISTINE_TRUTH.replace('EXPECTED_SHA = "%s"' % PRISTINE_EXPECTED_SHA,
                                 'EXPECTED_SHA = "%s"' % sha_bytes(eb))
    s8.truth_src = src
    (s8.dir / "truth.py").write_text(src)
    scen["S8-midrun-tamper"] = s8

    # S9: minimal refusal scenario -- ONE fixture that imports os.
    scen["S9-unsafe-os-only"] = build_scenario("S9-unsafe-os-only", extra_cases=[
        {"id": "ProbeOnlyUnsafeOs", "kind": "present", "forbid_any": [],
         "want_present": ["pacman -Q probe-only-unsafe-os"],
         "fixture": "fixtures/ProbeOnlyUnsafeOs.jsonl",
         "code": "import os\nimport subprocess\n\nsubprocess.run([\"pacman\", \"-Q\", \"probe-only-unsafe-os\"])\n"},
    ])

    # S10: deliberately WRONG expectation copy aimed at the forbid_any check:
    # forbid_any names the command the fixture really executes, while want
    # matches the executed set. Pristine must REJECT (forbidden fired).
    data = json.loads((LANE / "expected.json").read_text())
    for c in data["cases"]:
        if c["id"] == "ReturnedGlobalHelper":
            c["forbid_any"] = ["pacman -Q r22-nhb-module"]
    scen["S10-wrong-expect-forbid"] = build_scenario(
        "S10-wrong-expect-forbid",
        expected_bytes=(json.dumps(data, indent=2) + "\n").encode())

    return scen


# -------------------------------------------------------------------- mutants --
def mut_drop_forbid(src):
    """M1: drop the forbid_any check from both verdict branches."""
    assert src.count(" and not forbidden") == 2
    return src.replace(" and not forbidden", "")


def mut_subset_exact(src):
    """M2: exact cases compare as subsets (<=) instead of equality (==)."""
    old = 'passed = sorted(executed) == sorted(w["command"] for w in case["want"])'
    new = 'passed = set(w["command"] for w in case["want"]) <= set(executed)'
    assert src.count(old) == 1
    return src.replace(old, new)


def mut_wrong_call(src):
    """M3: the recording fake captures the PREVIOUS subprocess call's argv."""
    old = 'def run(argv, *a, **k):\n    calls.append(" ".join(argv))'
    new = ('_prev = [None]\n'
           'def run(argv, *a, **k):\n'
           '    calls.append(" ".join(_prev[0]) if _prev[0] is not None else " ".join(argv))\n'
           '    _prev[0] = argv')
    assert src.count(old) == 1
    return src.replace(old, new)


def mut_wrong_scope(src):
    """M3b: recorder resolves argv from the CALLER'S MODULE GLOBALS, not the argument."""
    old = 'calls.append(" ".join(argv))'
    new = 'calls.append(" ".join(sys._getframe(1).f_globals.get("argv", argv)))'
    assert src.count(old) == 1
    return src.replace(old, new)


def mut_wrong_arg(src):
    """M3c: recorder keeps only the last argv element instead of the whole command."""
    old = 'calls.append(" ".join(argv))'
    new = 'calls.append(" ".join(argv[-1:]))'
    assert src.count(old) == 1
    return src.replace(old, new)


def mut_skip_safe_gate(src):
    """M4: skip the safe() gate entirely; unsafe fixtures are executed."""
    old = ('        if not safe(code):\n'
           '            results.append(dict(id=case["id"], passed=False, error="unsafe_fixture"))\n'
           '            continue\n')
    assert src.count(old) == 1
    return src.replace(old, "")


def mut_skip_import_branch(src):
    """M4b: safe() still runs but no longer rejects non-subprocess imports."""
    old = ('            if names != ["subprocess"]:\n'
           '                return False\n')
    assert src.count(old) == 1
    return src.replace(old, "")


def mut_skip_expected_sha(src):
    """M5a: skip the expected.json snapshot-tamper check."""
    old = ('    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA:\n'
           '        raise SystemExit("snapshot_tampered: expected.json")\n')
    assert src.count(old) == 1
    return src.replace(old, "")


def mut_skip_fixture_sha(src):
    """M5b: skip the per-fixture snapshot-tamper check (keeps the file parseable)."""
    old = ('        if hashlib.sha256((ROOT / case["fixture"]).read_bytes()).hexdigest() != case["sha256"]:\n'
           '            raise SystemExit("snapshot_tampered: " + case["id"])\n')
    new = ('        if hashlib.sha256((ROOT / case["fixture"]).read_bytes()).hexdigest() != case["sha256"]:\n'
           '            pass\n')
    assert src.count(old) == 1
    return src.replace(old, new)


def mut_skip_recheck(src):
    """M5c: skip the end-of-run re-verification load() call."""
    old = '    load()\n    ok = sum(r["passed"] for r in results)'
    new = '    ok = sum(r["passed"] for r in results)'
    assert src.count(old) == 1
    return src.replace(old, new)


MUTANTS = [
    ("M1-drop-forbid", mut_drop_forbid,
     "drop the forbid_any check from both verdict branches"),
    ("M2-subset-exact", mut_subset_exact,
     "exact cases: subset comparison (<=) instead of equality (==)"),
    ("M3-wrong-call", mut_wrong_call,
     "recording fake captures the previous subprocess call's argv"),
    ("M3b-wrong-scope", mut_wrong_scope,
     "recorder resolves argv from the caller's module globals, not the argument"),
    ("M3c-wrong-arg", mut_wrong_arg,
     "recorder keeps only the last argv element"),
    ("M4-skip-safe-gate", mut_skip_safe_gate,
     "skip the safe() gate: unsafe fixtures get executed"),
    ("M4b-skip-import-branch", mut_skip_import_branch,
     "safe() keeps running but no longer rejects non-subprocess imports"),
    ("M5a-skip-expected-sha", mut_skip_expected_sha,
     "skip the expected.json snapshot-tamper check"),
    ("M5b-skip-fixture-sha", mut_skip_fixture_sha,
     "skip the per-fixture snapshot-tamper check"),
    ("M5c-skip-recheck", mut_skip_recheck,
     "skip the end-of-run re-verification load() call"),
]


# ------------------------------------------------------------------- detector --
def run_truth(scn, truth_src=None):
    """Install truth_src into the scenario, reset inputs, run. Returns (verdict, raw)."""
    scn.reset(truth_src)
    try:
        p = subprocess.run([sys.executable, "-I", str(scn.dir / "truth.py")],
                           capture_output=True, text=True, cwd=str(scn.dir), timeout=180)
    except subprocess.TimeoutExpired:
        return {"kind": "inconclusive", "reason": "timeout"}, {"exit": None}
    stdout, stderr, rc = p.stdout, p.stderr, p.returncode
    parsed = None
    try:
        parsed = json.loads(stdout)
    except Exception:
        parsed = None
    raw = {"exit": rc, "stdout": stdout, "stderr": stderr,
           "sha256": sha_bytes((scn.dir / "truth.py").read_bytes())}
    if parsed is None:
        # Any Python-level failure (traceback, SyntaxError, IndentationError,
        # NameError, ...) is INCONCLUSIVE, never a well-formed refusal.
        crash_markers = ("Traceback (most recent call last)", "Error:", "error:")
        if any(mk in stderr for mk in crash_markers) or rc in (2,):
            return {"kind": "inconclusive", "reason": "crash",
                    "stderr": stderr.strip()[:300]}, raw
        if rc == 0:
            return {"kind": "inconclusive", "reason": "no-json-output"}, raw
        # clean refusal (SystemExit with a plain message) is well-formed
        return {"kind": "refusal", "exit": rc, "stderr": stderr.strip()[:300]}, raw
    if parsed.get("schema") != TRUTH_SCHEMA:
        return {"kind": "inconclusive", "reason": "unexpected-schema"}, raw
    return {"kind": "json", "exit": rc, "passed": parsed.get("passed"),
            "total": parsed.get("total"),
            "cases": {r["id"]: [r["passed"], r.get("error"), r.get("executed")]
                      for r in parsed.get("results", [])}}, raw


def same_verdict(a, b):
    return a == b


# Declared expected control verdicts, written from truth.py's documented
# contract BEFORE the mutants were run (not copied from observed output).
EXPECTED_CONTROL = {
    "S0-frozen": {"kind": "json", "exit": 0, "passed": 12, "total": 12},
    "S1-tamper-expected": {"kind": "refusal", "stderr_contains": "snapshot_tampered: expected.json"},
    "S2-tamper-fixture": {"kind": "refusal", "stderr_contains": "snapshot_tampered: ReturnedGlobalHelper"},
    "S3-unsafe": {"kind": "json", "case_error": {"ProbeUnsafeOsUsed": "unsafe_fixture",
                                                 "ProbeUnsafeOsUnused": "unsafe_fixture"}},
    "S4-forbidden-present": {"kind": "json", "case_failed": ["ProbeForbiddenPresent"]},
    "S5-extra-executed": {"kind": "json", "case_failed": ["ProbeMultiCallExact"]},
    "S6-wrong-expect-bogus": {"kind": "json", "case_failed": ["ReturnedGlobalHelper"]},
    "S7-wrong-expect-duplicate": {"kind": "json", "case_failed": ["ReturnedGlobalHelper"]},
    "S8-midrun-tamper": {"kind": "refusal", "stderr_contains": "snapshot_tampered: expected.json"},
    "S9-unsafe-os-only": {"kind": "json", "case_error": {"ProbeOnlyUnsafeOs": "unsafe_fixture"}},
    "S10-wrong-expect-forbid": {"kind": "json", "case_failed": ["ReturnedGlobalHelper"]},
}


def check_control(name, v, exp):
    """True iff the unmutated truth.py produced its DECLARED expected verdict."""
    if exp is None:
        return False
    if exp["kind"] != v.get("kind"):
        return False
    if exp["kind"] == "refusal":
        return exp["stderr_contains"] in v.get("stderr", "")
    if exp["kind"] == "json":
        for key in ("exit", "passed", "total"):
            if key in exp and v.get(key) != exp[key]:
                return False
        for cid, err in (exp.get("case_error") or {}).items():
            row = v.get("cases", {}).get(cid)
            if not row or row[1] != err:
                return False
        for cid in exp.get("case_failed") or []:
            row = v.get("cases", {}).get(cid)
            if not row or row[0] is not False:
                return False
    return True


def flip_class(pv, mv):
    if pv["kind"] == "json" and mv["kind"] == "json":
        if mv["passed"] > pv["passed"]:
            return "false-accept"
        if mv["passed"] < pv["passed"]:
            return "false-reject"
        return "verdict-differs"
    if pv["kind"] == "refusal" and mv["kind"] == "json":
        return "false-accept"
    if pv["kind"] == "json" and mv["kind"] == "refusal":
        return "false-reject"
    return "shape-differs"


def main():
    scen = build_all_scenarios()
    receipts = {"schema": "mado-r23-muttruth-v1",
                "lane_truth_sha256": PRISTINE_TRUTH_SHA,
                "lane_expected_sha256": PRISTINE_EXPECTED_SHA,
                "python": sys.version.split()[0],
                "protocol": ("control first: pristine verdict must equal the declared "
                             "expected control verdict; kill requires a different "
                             "well-formed mutant verdict; crashes/timeouts are "
                             "inconclusive; kill rate = killed/(killed+survived)"),
                "scenarios": {}, "mutants": []}

    # ---------------- control 0: the lane's own frozen set, unmutated ----------
    lane_control = {}
    try:
        p = subprocess.run([sys.executable, "-I", str(LANE / "truth.py")],
                           capture_output=True, text=True, cwd=str(LANE), timeout=180)
        pr = json.loads(p.stdout)
        lane_control = {"exit": p.returncode, "passed": pr.get("passed"),
                        "total": pr.get("total"),
                        "schema": pr.get("schema"),
                        "expected_sha256": pr.get("expected_sha256"),
                        "stderr": p.stderr.strip()[:300]}
    except Exception as exc:
        lane_control = {"error": repr(exc)}
    receipts["lane_control"] = lane_control

    # ---------------- per-scenario control (pristine) -------------------------
    control = {}
    for name, scn in scen.items():
        v, raw = run_truth(scn, scn.truth_src)
        exp = EXPECTED_CONTROL.get(name)
        exp_ok = check_control(name, v, exp)
        control[name] = {"verdict": v, "raw": raw, "snapshot": scn.snapshot(),
                         "expected_control": exp, "control_ok": exp_ok}
        receipts["scenarios"][name] = {"control_verdict": v,
                                       "control_expected": exp,
                                       "control_ok": exp_ok,
                                       "control_exit": raw.get("exit"),
                                       "control_stderr": (raw.get("stderr") or "").strip()[:300],
                                       "scenario_snapshot": scn.snapshot()}

    for mname, mfn, mdesc in MUTANTS:
        entry = {"id": mname, "description": mdesc, "killed": [], "survived": [],
                 "inconclusive": [], "kills_frozen_set": [], "details": {},
                 "restore_bytes_ok": 0, "restore_total": 0, "restore_verified": True}
        for sname, scn in scen.items():
            ctl = control[sname]
            base_src = scn.truth_src
            try:
                mut_src = mfn(base_src)
            except AssertionError as exc:
                entry["details"][sname] = {"error": "mutation-did-not-apply: %r" % exc}
                entry["inconclusive"].append(sname)
                continue
            if mut_src == base_src:
                entry["details"][sname] = {"error": "mutation was a no-op"}
                entry["inconclusive"].append(sname)
                continue
            try:
                compile(mut_src, "<mutant>", "exec")
            except SyntaxError as exc:
                entry["details"][sname] = {"error": "mutant does not compile: %r" % exc}
                entry["inconclusive"].append(sname)
                continue
            mut_sha = sha_bytes(mut_src.encode())
            mv, mraw = run_truth(scn, mut_src)
            # restore exact pristine bytes and re-verify behaviour
            rv, rraw = run_truth(scn, base_src)
            restored_sha = sha_bytes((scn.dir / "truth.py").read_bytes())
            entry["restore_total"] += 1
            ok = (restored_sha == sha_bytes(base_src.encode())
                  and same_verdict(rv, ctl["verdict"]))
            entry["restore_bytes_ok"] += int(restored_sha == sha_bytes(base_src.encode()))
            entry["restore_verified"] = entry["restore_verified"] and ok

            detail = {"mutant_sha256": mut_sha, "mutant_verdict": mv,
                      "mutant_exit": mraw.get("exit"),
                      "mutant_stderr": (mraw.get("stderr") or "").strip()[:300],
                      "restored_sha256": restored_sha,
                      "restore_verified": ok}
            if ctl["verdict"]["kind"] == "inconclusive":
                detail["outcome"] = "inconclusive"
                detail["reason"] = "control on same input was not well-formed: %s" % ctl["verdict"].get("reason")
                entry["inconclusive"].append(sname)
            elif not ctl["control_ok"]:
                detail["outcome"] = "inconclusive"
                detail["reason"] = ("control on same input did not match its declared "
                                     "expected verdict: %s" % ctl["expected_control"])
                entry["inconclusive"].append(sname)
            elif mv["kind"] == "inconclusive":
                detail["outcome"] = "inconclusive"
                detail["reason"] = "mutant run not well-formed: %s" % mv.get("reason")
                entry["inconclusive"].append(sname)
            elif same_verdict(mv, ctl["verdict"]):
                detail["outcome"] = "survived"
                entry["survived"].append(sname)
            else:
                detail["outcome"] = "killed"
                detail["flip"] = flip_class(ctl["verdict"], mv)
                entry["killed"].append(sname)
                if sname == "S0-frozen":
                    entry["kills_frozen_set"].append(sname)
            entry["details"][sname] = detail
        k, s = len(entry["killed"]), len(entry["survived"])
        entry["kill_rate"] = (k / (k + s)) if (k + s) else None
        receipts["mutants"].append(entry)

    tot_k = sum(len(m["killed"]) for m in receipts["mutants"])
    tot_s = sum(len(m["survived"]) for m in receipts["mutants"])
    tot_i = sum(len(m["inconclusive"]) for m in receipts["mutants"])
    receipts["summary"] = {"killed": tot_k, "survived": tot_s, "inconclusive": tot_i,
                            "kill_rate": (tot_k / (tot_k + tot_s)) if (tot_k + tot_s) else None}

    out = SCRATCH / "receipts" / "matrix.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipts, indent=1))
    print(json.dumps({"summary": receipts["summary"],
                      "lane_control": lane_control,
                      "mutants": {m["id"]: {"killed": m["killed"], "survived": m["survived"],
                                           "inconclusive": m["inconclusive"],
                                           "kill_rate": m["kill_rate"],
                                           "restore": "%d/%d bytes, verified=%s" % (
                                               m["restore_bytes_ok"], m["restore_total"],
                                               m["restore_verified"])}
                                  for m in receipts["mutants"]}}, indent=1))
    print("receipts:", out)


if __name__ == "__main__":
    main()
