#!/usr/bin/env python3
"""Round-91 C2 counter — does the lane's seat-report check catch the lane's own lost seat reports?

Frozen predicate PRED-C2-r91-v1 (declaration, counter and receipt use the same label):
  TARGET_MET iff `<rev>:quality/check-seat-reports.py` meets every frozen
  expectation of the set — each lane-round expectation (run `--rev <frozen rev>
  --round N`: exit code and the exact set of SR01/SR02/SR03/SR04 findings as
  (id, wave, seat, path); seats/trailered counts), the `--all` expectation
  (exit code, SR01 count, seats), and each fixture (worktree, or a throwaway git
  repository read with `--rev HEAD`: exit code, the finding ids as a multiset,
  and the summary fields the fixture names) — meets every fresh fixture the
  counter generates from seed = the first 8 hex digits of the measured check's
  sha256 (expected findings taken from the generator's own choices; fresh ==
  fresh_met); its `--selftest` exits 0 and prints
  `SEAT_REPORTS_SELFTEST: checks=N failed=0`; every frozen mutant of the check
  fails at least one frozen expectation or changes the selftest result line
  (killed == mutants); and each control meets fewer expectations than the set
  holds (the base revision's check — absent = 0 —, always-OK, always-MISSING,
  and quality/check-receipt-presence.py run with the same arguments).

The lane repository is only read (`git show`, and the check's own `git
ls-tree/cat-file`).  Fixture trees and fixture repositories live under
--scratch-root.  Every scored check (candidate, mutant, control) is the same
file name in an opaque directory.
rc 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error, 3 draft run (--draft-check).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import random
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

CHECK = "quality/check-seat-reports.py"
PRED = "PRED-C2-r91-v1"
JOBS = 8
FIND = re.compile(r"^(SR0[1-4]) (missing|empty|unsafe|untrailed) round-(\d+)/(\S+) (\S+)(?: (\S+))?$")
SUM = re.compile(r"^SEAT_REPORTS: mode=\S+ rev=\S+ rounds=(\d+) waves=(\d+) seats=(\d+) trailered=(\d+) present=(\d+) "
                 r"missing=(\d+) empty=(\d+) unsafe=(\d+) untrailed=(\d+) verdict=(OK|MISSING)$")
FIELDS = ("rounds", "waves", "seats", "trailered", "present", "missing", "empty", "unsafe", "untrailed")

ALWAYS_OK = "import sys\nprint('SEAT_REPORTS: mode=rev rev=x rounds=1 waves=1 seats=0 trailered=0 present=0 missing=0 " \
            "empty=0 unsafe=0 untrailed=0 verdict=OK')\nsys.exit(0)\n"
ALWAYS_MISSING = "import sys\nprint('SEAT_REPORTS: mode=rev rev=x rounds=1 waves=1 seats=0 trailered=0 present=0 " \
                 "missing=1 empty=0 unsafe=0 untrailed=0 verdict=MISSING')\nsys.exit(1)\n"


def sha(p: str) -> str:
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def git_show(repo: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def run_check(check: str, args: list[str]) -> tuple[int, list[tuple], dict | None]:
    env = {"PATH": "/usr/bin", "HOME": "/nonexistent", "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1"}
    try:
        r = subprocess.run([sys.executable, "-I", check] + args, capture_output=True, text=True, env=env, timeout=600)
    except subprocess.TimeoutExpired:
        return -1, [], None
    finds, summ = [], None
    for line in r.stdout.splitlines():
        m = FIND.match(line)
        if m:
            finds.append((m.group(1), m.group(4), m.group(5), m.group(6), int(m.group(3))))
        s = SUM.match(line)
        if s:
            summ = {k: int(v) for k, v in zip(FIELDS, s.groups()[:9])}
            summ["verdict"] = s.group(10)
    return r.returncode, finds, summ


def materialise(files: dict, root: str, dirs: list[str] | None = None) -> None:
    for rel in dirs or []:
        os.makedirs(os.path.join(root, rel), exist_ok=True)
    for rel, body in files.items():
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if isinstance(body, dict) and "symlink" in body:
            os.symlink(body["symlink"], p)
            continue
        with open(p, "wb") as fh:
            fh.write(body.encode("utf-8") if isinstance(body, str) else bytes(body))


def expectations(st: dict, lane: str, work: str) -> list[tuple[str, list[str], callable]]:
    """[(id, args, judge(rc, finds, summ) -> bool)]"""
    out = []
    for e in st["revisions"]:
        want = {(k, w, s, p) for k, lst in (("SR01", e.get("missing", [])), ("SR02", e.get("empty", [])),
                                           ("SR03", e.get("unsafe", []))) for w, s, p in lst}
        want |= {("SR04", w, s, None) for w, s in e.get("untrailed", [])}

        def judge(rc, finds, summ, e=e, want=want):
            got = {(f[0], f[1], f[2], f[3]) for f in finds}
            if rc != e["rc"] or got != want:
                return False
            for k in ("seats", "trailered"):
                if k in e and (summ is None or summ[k] != e[k]):
                    return False
            return True
        out.append((e["id"], ["--repo", lane, "--rev", e["rev"], "--round", str(e["round"])], judge))
    a = st.get("all")
    if a:
        def judge_all(rc, finds, summ, a=a):
            return rc == a["rc"] and sum(1 for f in finds if f[0] == "SR01") == a["sr01"] and \
                (summ is not None and summ["seats"] == a["seats"] and summ["missing"] == a["sr01"])
        out.append((a["id"], ["--repo", lane, "--rev", a["rev"], "--all"], judge_all))
    for fx in st["fixtures"]:
        root = os.path.join(work, "fx-" + fx["id"])
        os.makedirs(root)
        materialise(fx["files"], root, fx.get("dirs"))
        if "args" in fx:
            scope = list(fx["args"])  # verbatim scope arguments (may be empty, or conflicting: setup-error probes)
        else:
            scope = ["--all"] if fx.get("rounds") is None else [x for n in fx["rounds"] for x in ("--round", str(n))]
        if fx.get("git"):
            # rev mode on a throwaway repository: committed once under a fixture identity, inside root only
            g = ["git", "-C", root]
            subprocess.run(g + ["init", "-q"], check=True)
            top = subprocess.run(g + ["rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
            if os.path.realpath(top) != os.path.realpath(root):
                raise RuntimeError(f"fixture toplevel {top} != {root}")
            subprocess.run(g + ["add", "-A"], check=True)
            subprocess.run(g + ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "-c",
                                "commit.gpgsign=false", "commit", "-q", "-m", "fixture"], check=True)
            args = ["--repo", root, "--rev", "HEAD"] + scope
        else:
            args = ["--repo", root, "--worktree"] + scope

        def judge_fx(rc, finds, summ, fx=fx):
            if rc != fx["rc"] or sorted(f[0] for f in finds) != sorted(fx["ids"]):
                return False
            for k, v in (fx.get("summary") or {}).items():
                if summ is None or summ.get(k) != v:
                    return False
            return True
        out.append((fx["id"], args, judge_fx))
    return out


def met_count(check: str, exps) -> tuple[int, list[str]]:
    with ThreadPoolExecutor(max_workers=JOBS) as ex:
        res = list(ex.map(lambda e: (e[0], e[2](*run_check(check, e[1]))), exps))
    failed = [eid for eid, ok in res if not ok]
    return len(res) - len(failed), failed


SELFTEST = re.compile(r"^SEAT_REPORTS_SELFTEST: checks=(\d+) failed=(\d+)$", re.M)


def selftest_line(check: str) -> tuple[int, str | None]:
    r = subprocess.run([sys.executable, "-I", check, "--selftest"], capture_output=True, text=True, timeout=300,
                       env={"PATH": "/usr/bin", "HOME": "/nonexistent", "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1",
                            "TMPDIR": os.path.dirname(check)})
    m = SELFTEST.search(r.stdout)
    return r.returncode, (m.group(0) if m else None)


def fresh_fixtures(seed: int, n: int) -> list[dict]:
    """Held-out leg: random dispatch/report trees whose expected findings come from the generator's own choices
    (what it decided to write), never from running a check.  Seeded by the measured check's sha256."""
    rnd = random.Random(seed)
    states = ["present", "present", "missing", "empty", "symlink", "abs", "dotdot", "untrailed", "plain-present",
              "plain-missing", "prose", "dir", "inline", "trailing", "dotname"]
    out = []
    for k in range(n):
        files: dict = {}
        ids: list[str] = []
        summ = dict.fromkeys(("seats", "trailered", "present", "missing", "empty", "unsafe", "untrailed"), 0)
        rounds = rnd.sample(range(100, 999), rnd.randint(1, 3))
        chosen = rounds if rnd.random() < 0.5 else None
        wave_n = 0
        for rd in rounds:
            for wi in range(rnd.randint(1, 2)):
                wave = rnd.choice(["w", "r", "a"]) + str(wi + 1) + rnd.choice(["", "x"])
                base = f".ufo/waves/round-{rd}"
                tasks = []
                for si in range(rnd.randint(1, 4)):
                    name = "S" + "".join(rnd.choice("abcdefgh") for _ in range(5)) + str(si)
                    rel = f"{base}/{wave}/{name}.md"
                    st = rnd.choice(states)
                    summ["seats"] += 1
                    text = f"Own: {name}\n"
                    if st in ("untrailed", "prose", "inline", "trailing"):
                        text += {"untrailed": "no report line\n", "prose": "Report: goes to the usual place\n",
                                 "inline": f"see: Report: write your scoped findings to {rel}\n",
                                 "trailing": f"Report: write your scoped findings to {rel} (see note)\n"}[st]
                        if st in ("inline", "trailing"):
                            files[rel] = "x"
                        summ["untrailed"] += 1
                        ids.append("SR04")
                    else:
                        summ["trailered"] += 1
                        target = {"abs": "/etc/hostname", "dotdot": f"{base}/{wave}/../{wave}/{name}.md",
                                  "dotname": f"{base}/{wave}/{name}..md"}.get(st, rel)
                        if st.startswith("plain"):
                            text += f"\nReport: {target}\n"
                        else:
                            text += f"\nReport: write your scoped findings to {target}"
                        if st in ("present", "plain-present", "dotname"):
                            files[target] = "report " + name
                            summ["present"] += 1
                        elif st == "empty":
                            files[target] = ""
                            summ["empty"] += 1
                            ids.append("SR02")
                        elif st in ("missing", "plain-missing"):
                            summ["missing"] += 1
                            ids.append("SR01")
                        elif st == "dir":
                            files[target + "/inner"] = "x"
                            summ["missing"] += 1
                            ids.append("SR01")
                        elif st == "symlink":
                            files[f"{base}/{wave}/{name}.real"] = "x"
                            files[target] = {"symlink": f"{name}.real"}
                            summ["unsafe"] += 1
                            ids.append("SR03")
                        else:  # abs, dotdot
                            files[f"{base}/{wave}/{name}.md"] = "x"
                            summ["unsafe"] += 1
                            ids.append("SR03")
                    tasks.append({"name": name, "agent": "scout", "task": text})
                files[f"{base}/{wave}-dispatch.json"] = json.dumps({"taskCall": {"context": "c", "tasks": tasks}})
                wave_n += 1
        bad = summ["missing"] + summ["empty"] + summ["unsafe"] + summ["untrailed"]
        summ.update(rounds=len(rounds), waves=wave_n)
        args = ["--all"] if chosen is None else [x for r in chosen for x in ("--round", str(r))]
        out.append({"id": f"fresh-{seed}-{k:03d}", "files": files, "args": args, "rc": 1 if bad else 0,
                    "ids": ids, "summary": summ, "git": rnd.random() < 0.3})
    return out


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
    ap.add_argument("--draft-check")
    ap.add_argument("--fresh", type=int, default=60)
    a = ap.parse_args()
    lane = os.path.realpath(a.repo)

    def setup(msg: str) -> int:
        print(f"MADO_SEAT_REPORTS: SETUP_ERROR {msg}")
        return 2

    for p, want in ((a.set, a.expect_set_sha256), (a.mutants, a.expect_mutants_sha256)):
        try:
            got = sha(p)
        except OSError as e:
            return setup(f"cannot read {p}: {e}")
        if got != want:
            return setup(f"sha256 mismatch {p}: {got} != {want}")
    st = json.load(open(a.set, encoding="utf-8"))
    mutants = json.load(open(a.mutants, encoding="utf-8"))["mutants"]
    os.makedirs(a.scratch_root, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c2r91-", dir=a.scratch_root)
    if a.fresh < 1:
        return setup("--fresh must be at least 1 (the fresh leg is part of the predicate)")
    try:
        if a.draft_check:
            cb = open(a.draft_check, "rb").read()
            label = f"draft:{a.draft_check}"
        else:
            cb = git_show(lane, a.rev, CHECK)
            if cb is None:
                return setup(f"{CHECK} absent at {a.rev}")
            label = a.rev
        exps = expectations(st, lane, work)
        total = len(exps)
        seed = int(hashlib.sha256(cb).hexdigest()[:8], 16)
        fresh = expectations({"revisions": [], "fixtures": fresh_fixtures(seed, a.fresh)}, lane, work)

        def w(name: str, b: bytes) -> str:
            # same file name in an opaque directory for candidate, mutants and controls (no role from the path)
            d = os.path.join(work, "t-" + hashlib.sha256((name + str(os.getpid())).encode()).hexdigest()[:12])
            os.makedirs(d, exist_ok=True)
            p = os.path.join(d, "check-seat-reports.py")
            with open(p, "wb") as fh:
                fh.write(b)
            return p

        cand = w("candidate", cb)
        met, failed = met_count(cand, exps)
        for f in failed:
            print(f"expectation {f} FAILED")
        fresh_met, ffailed = met_count(cand, fresh)
        for f in ffailed:
            print(f"fresh {f} FAILED")
        st_rc, st_line = selftest_line(cand)
        st_ok = st_rc == 0 and st_line is not None and st_line.endswith(" failed=0")
        text = cb.decode("utf-8")
        killed = 0
        for m in mutants:
            if text.count(m["find"]) != 1:
                return setup(f"mutant {m['id']}: find occurs {text.count(m['find'])} times")
            mp = w("m-" + m["id"], text.replace(m["find"], m["replace"]).encode())
            mm, _ = met_count(mp, exps)
            mst = selftest_line(mp)
            k = mm < total or mst != (st_rc, st_line)
            killed += k
            print(f"mutant {m['id']} {'killed' if k else 'SURVIVED'} met={mm} selftest={'same' if mst == (st_rc, st_line) else 'differs'}")
        base = git_show(lane, a.base_rev, CHECK)
        ctl = {"base": met_count(w("base", base), exps)[0] if base is not None else 0,
               "always_ok": met_count(w("ok", ALWAYS_OK.encode()), exps)[0],
               "always_missing": met_count(w("miss", ALWAYS_MISSING.encode()), exps)[0]}
        rp = git_show(lane, a.rev if not a.draft_check else "HEAD", "quality/check-receipt-presence.py")
        ctl["receipt_presence"] = met_count(w("rp", rp), exps)[0] if rp is not None else 0
    finally:
        shutil.rmtree(work, ignore_errors=True)
    ok = (met == total and fresh_met == len(fresh) and st_ok and killed == len(mutants)
          and all(v < total for v in ctl.values()))
    verdict = ("DRAFT_TARGET_MET" if ok else "DRAFT_TARGET_MISSED") if a.draft_check else (
        "TARGET_MET" if ok else "TARGET_MISSED")
    print(f"MADO_SEAT_REPORTS: {verdict} pred={PRED} rev={label} base_rev={a.base_rev} expectations={total} met={met} "
          f"fresh={fresh_met}/{len(fresh)} fresh_seed={seed} selftest={'ok' if st_ok else 'FAIL'}:{st_line} "
          f"mutants={len(mutants)} killed={killed} "
          + " ".join(f"{k}_met={v}" for k, v in ctl.items()) + f" check_sha256={hashlib.sha256(cb).hexdigest()}")
    if a.draft_check:
        return 3
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
