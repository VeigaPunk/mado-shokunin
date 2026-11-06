#!/usr/bin/env python3
"""Round-90 C2 counter — does the lane's receipt-presence check catch the lane's own cite-before-commit records?

Frozen predicate PRED-C2-r90-v1 (declaration, counter and receipt use the same label):
  TARGET_MET iff  `<rev>:quality/check-receipt-presence.py` meets every frozen
  expectation of the set — each lane revision (rc and exact missing citations;
  where given, cited/present counts and file:line locations), each worktree
  fixture (rc and exact missing citations), and the population (the commits of
  the frozen range on which the check exits 1 are exactly the frozen list, and
  it never exits 2) — under BOTH a clean git configuration and one with
  diff.mnemonicPrefix=true and diff.noprefix=true; every frozen mutant of the
  check fails at least one expectation (killed == mutants); and each control
  meets fewer expectations than the set holds (base check, do-nothing OK
  check, smart always-OK, always-MISSING).

The lane repository is only read (the check runs `git show/diff/cat-file/ls-tree`
there).  Fixture repositories live under --scratch-root, are created with
`git -C "$D" init -q`, and their toplevel is asserted before the one fixture
commit (identity fixture <fixture@invalid>, inside the fixture repo only).

rc 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

CHECK = "quality/check-receipt-presence.py"
MISS = re.compile(r"^missing (\S+) -> \S+ (\S+:\d+)$")
SUMMARY = re.compile(r"^RECEIPT_PRESENCE: .*\bcited=(\d+) present=(\d+) .*verdict=(OK|MISSING)$")
ENVS = {
    "clean": {},
    "mnemonic": {"GIT_CONFIG_COUNT": "2", "GIT_CONFIG_KEY_0": "diff.mnemonicPrefix", "GIT_CONFIG_VALUE_0": "true",
                 "GIT_CONFIG_KEY_1": "diff.noprefix", "GIT_CONFIG_VALUE_1": "true"},
}


def sha(p: str) -> str:
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run_check(check: str, args: list[str], envname: str) -> dict:
    env = {"PATH": "/usr/bin", "HOME": "/nonexistent", "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1", **ENVS[envname]}
    r = subprocess.run([sys.executable, "-I", check] + args, capture_output=True, text=True, env=env, timeout=120)
    missing, locs, cited, present = [], [], None, None
    for line in r.stdout.splitlines():
        m = MISS.match(line)
        if m:
            missing.append(m.group(1))
            locs.append(m.group(2))
        s = SUMMARY.match(line)
        if s:
            cited, present = int(s.group(1)), int(s.group(2))
    return {"rc": r.returncode, "missing": sorted(set(missing)), "locs": sorted(set(locs)), "cited": cited,
            "present": present, "wellformed": r.returncode in (0, 1) and cited is not None}


def build_fixture(fx: dict, scratch: str) -> str:
    d = tempfile.mkdtemp(prefix="fx-", dir=scratch)
    g = ["git", "-C", d]
    subprocess.run(g + ["init", "-q"], check=True)
    top = subprocess.run(g + ["rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit(f"fixture toplevel {top} != {d}")
    for p, t in fx["base"].items():
        os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
        open(os.path.join(d, p), "w").write(t)
    subprocess.run(g + ["add", "-A", "-f"], check=True)
    subprocess.run(g + ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "-c", "commit.gpgsign=false",
                        "commit", "-q", "-m", "base"], check=True)
    for p, t in fx["work"].items():
        os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
        open(os.path.join(d, p), "w").write(t)
    for p in fx.get("delete", []):
        os.remove(os.path.join(d, p))
    return d


def matches(out: dict, exp: dict) -> bool:
    if out["rc"] != exp["expect_rc"] or out["missing"] != sorted(exp["expect_missing"]):
        return False
    if (out["cited"] or 0) < exp.get("min_cited", 0):
        return False
    if "expect_cited" in exp and out["cited"] != exp["expect_cited"]:
        return False
    if "expect_present" in exp and out["present"] != exp["expect_present"]:
        return False
    if "expect_locations" in exp and out["locs"] != sorted(exp["expect_locations"]):
        return False
    return True


def evaluate(check: str, spec: dict, repo: str, fixtures: dict[str, str], population: list[str]) -> list[tuple[str, bool, str]]:
    jobs = []
    for envname in ENVS:
        for r in spec["revisions"]:
            jobs.append((f"{r['id']}@{envname}", r, ["--repo", repo, "--rev", r["rev"]], envname))
        for fx in spec["fixtures"]:
            jobs.append((f"{fx['id']}@{envname}", fx, ["--repo", fixtures[fx["id"]], "--worktree", "--base", "HEAD",
                                                       "--round", str(fx["round"]), "--commit-path", *fx["commit_paths"]],
                         envname))
    with ThreadPoolExecutor(8) as ex:
        outs = list(ex.map(lambda j: run_check(check, j[2], j[3]), jobs))
        pop = list(ex.map(lambda h: run_check(check, ["--repo", repo, "--rev", h], "clean"), population))
    res = [(name, matches(o, exp) or ("" if o["wellformed"] else None),
            f"rc={o['rc']} missing={o['missing']} cited={o['cited']} present={o['present']} locs={o['locs']}")
           for (name, exp, _, _), o in zip(jobs, outs)]
    flagged = sorted(h for h, o in zip(population, pop) if o["rc"] == 1)
    errors = sum(1 for o in pop if o["rc"] not in (0, 1))
    want = sorted(spec["population"]["expect_missing_commits"])
    res.append(("POPULATION", (flagged == want and errors == 0) or ("" if errors == 0 else None),
                f"commits={len(population)} flagged={[h[:8] for h in flagged]} rc_other={errors}"))
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--set", required=True)
    ap.add_argument("--mutants", required=True)
    ap.add_argument("--expect-set-sha256", required=True)
    ap.add_argument("--expect-mutants-sha256", required=True)
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--draft-check", help="DRAFT only: score this file instead of <rev>:" + CHECK)
    a = ap.parse_args()

    def setup(msg: str) -> int:
        print(f"MADO_RECEIPT_PRESENCE: SETUP_ERROR {msg}")
        return 2

    if sha(a.set) != a.expect_set_sha256:
        return setup("set sha256 mismatch")
    if sha(a.mutants) != a.expect_mutants_sha256:
        return setup("mutants sha256 mismatch")
    spec = json.load(open(a.set))
    mutants = json.load(open(a.mutants))["mutants"]
    repo = os.path.realpath(a.repo)
    rl = ["git", "-C", repo, "rev-list"] + (["--no-merges"] if spec["population"].get("no_merges") else []) + [spec["population"]["range"]]
    r = subprocess.run(rl, capture_output=True, text=True)
    if r.returncode != 0:
        return setup("population range unreadable")
    population = r.stdout.split()
    if a.draft_check:
        src = open(a.draft_check, "rb").read()
    else:
        r = subprocess.run(["git", "-C", repo, "show", f"{a.rev}:{CHECK}"], capture_output=True)
        if r.returncode != 0:
            return setup(f"{CHECK} absent at {a.rev}")
        src = r.stdout
    os.makedirs(a.scratch_root, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c2r90-", dir=a.scratch_root)
    try:
        fixtures = {fx["id"]: build_fixture(fx, work) for fx in spec["fixtures"]}
        cp = os.path.join(work, "check.py")
        open(cp, "wb").write(src)
        res = evaluate(cp, spec, repo, fixtures, population)
        for i, ok, why in res:
            print(f"expect {i} {'ok' if ok is True else 'FAIL'} {why}")
        n = len(res)
        good = sum(ok is True for _, ok, _ in res)
        text = src.decode()
        killed = 0
        for m in mutants:
            c = text.count(m["find"])
            if c != 1:
                return setup(f"mutant {m['id']} find occurs {c} times")
            mp = os.path.join(work, f"mut-{m['id']}.py")
            open(mp, "w").write(text.replace(m["find"], m["replace"], 1))
            mres = evaluate(mp, spec, repo, fixtures, population)
            # ok is True (met), "" (a well-formed wrong answer) or None (a crash: no verdict line or rc
            # outside 0/1).  A crash is not a kill (QUALITY 148; round-90 w1 R90MConnector §4.1).
            first = next((i for i, ok, _ in mres if ok == ""), None)
            if first is None and any(ok is None for _, ok, _ in mres):
                print(f"mutant {m['id']} crashed-not-killed")
            killed += bool(first)
            print(f"mutant {m['id']} {'killed by ' + first if first else 'survived'} ({m['what']})")
        controls = {}
        for name, body in (
            ("do_nothing", open(os.path.join(os.path.dirname(os.path.realpath(a.set)), "do-nothing-receipt-check.py")).read()),
            ("smart_always_ok", "import sys\nprint('RECEIPT_PRESENCE: mode=rev rev=- records=1 cited=99 present=99 missing=0 verdict=OK')\nsys.exit(0)\n"),
            ("always_missing", "import sys\nprint('RECEIPT_PRESENCE: mode=rev rev=- records=1 cited=1 present=0 missing=1 verdict=MISSING')\nsys.exit(1)\n"),
        ):
            fp = os.path.join(work, f"ctl-{name}.py")
            open(fp, "w").write(body)
            controls[name] = sum(ok is True for _, ok, _ in evaluate(fp, spec, repo, fixtures, population))
        b = subprocess.run(["git", "-C", repo, "show", f"{a.base_rev}:{CHECK}"], capture_output=True)
        if b.returncode != 0:
            controls["base"] = 0
            base_note = "absent"
        else:
            bp = os.path.join(work, "base.py")
            open(bp, "wb").write(b.stdout)
            controls["base"] = sum(ok is True for _, ok, _ in evaluate(bp, spec, repo, fixtures, population))
            base_note = "present"
        detected = sum(ok is True for i, ok, _ in res if i.startswith("D") and i.endswith("@clean"))
        defects = sum(1 for r in spec["revisions"] if r["id"].startswith("D"))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    met = good == n and killed == len(mutants) and all(v < n for v in controls.values())
    verdict = ("DRAFT_" if a.draft_check else "") + ("TARGET_MET" if met else "TARGET_MISSED")
    print(f"MADO_RECEIPT_PRESENCE: {verdict} rev={'draft:' + a.draft_check if a.draft_check else a.rev} "
          f"expectations={n} met={good} defects_detected={detected}/{defects} population={len(population)} "
          f"mutants={len(mutants)} killed={killed} base_check={base_note} base_met={controls['base']} "
          f"do_nothing_met={controls['do_nothing']} smart_always_ok_met={controls['smart_always_ok']} "
          f"always_missing_met={controls['always_missing']} check_sha256={hashlib.sha256(src).hexdigest()}")
    if a.draft_check:
        return 3
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
