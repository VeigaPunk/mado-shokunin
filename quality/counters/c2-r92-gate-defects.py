#!/usr/bin/env python3
"""Round-92 C2 counter — does quality/check-seat-reports.py close the five round-91 residual defects (F1-F5)?

Frozen predicate PRED-C2-r92-v1 (declaration, counter and receipt use the same label):
  TARGET_MET iff `<rev>:quality/check-seat-reports.py` meets every fixture of the frozen battery (exit
  code; the multiset of SR ids; every `contains` substring present in stdout; every named summary field;
  where named, the whitespace field count of every SR line and the stdout line count; stdout pure ASCII;
  finished within --timeout seconds — a hang meets nothing), so met == fixtures; meets every fresh fixture the
  counter generates over the F1-F5 vocabulary from seed = the first 8 hex digits of the measured check's sha256,
  expectations taken from the generator's own choices (fresh_met == fresh); its `--selftest` exits 0
  and prints `SEAT_REPORTS_SELFTEST: checks=N failed=0`; every frozen mutant of the check meets fewer
  fixtures or changes the selftest result line (killed == mutants); each control meets fewer fixtures
  than the battery holds (the base revision's check, always-OK, always-refuse-as-symlink); and the
  round-91 frozen counter (PRED-C2-r91-v1, its own pinned set and mutants), read from `<rev>` and pinned by
  sha256, prints TARGET_MET for the same revision (no regression on the 59 round-91 expectations, 55 mutants and
  60 fresh fixtures); a SETUP_ERROR of that leg is this counter's setup error, not a miss.
Every scored check runs inside a bwrap sandbox (host read-only, the lane repository hidden, only the work dir
writable, no network): the battery and its expectations are not readable by the check (R92MCritic §4).

The lane repository is only read (`git show`; the check's own `git ls-tree/cat-file` on fixtures).
Fixture trees and throwaway fixture repositories live under --scratch-root.
rc 0 TARGET_MET, 1 TARGET_MISSED, 2 setup error, 3 draft run (--draft-check).
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

CHECK = "quality/check-seat-reports.py"
PRED = "PRED-C2-r92-v1"
SUM = re.compile(r"^SEAT_REPORTS: mode=\S+ rev=\S+ rounds=(\d+) waves=(\d+) seats=(\d+) trailered=(\d+) present=(\d+) "
                 r"missing=(\d+) empty=(\d+) unsafe=(\d+) untrailed=(\d+) verdict=(OK|MISSING)$")
FIELDS = ("rounds", "waves", "seats", "trailered", "present", "missing", "empty", "unsafe", "untrailed")
ALWAYS_OK = ("import sys\nprint('SEAT_REPORTS: mode=rev rev=x rounds=1 waves=1 seats=1 trailered=1 present=1 missing=0 "
             "empty=0 unsafe=0 untrailed=0 verdict=OK')\nsys.exit(0)\n")
ALWAYS_REFUSE = ("import sys\nprint('SEAT_REPORTS: SETUP_ERROR x: dispatch is a symlink, not a regular file')\n"
                 "sys.exit(2)\n")


def sha(p: str) -> str:
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def git_show(repo: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def build(fx: dict, root: str, outside: str) -> str | None:
    """Materialise one fixture under root/tree; for rev mode commit it in a throwaway repo there."""
    d = os.path.join(root, "tree")
    os.makedirs(d)
    sibling = d + "-sibling"  # shares the repository path as a string prefix but lies outside it
    os.makedirs(sibling)
    with open(os.path.join(sibling, "A.md"), "w") as fh:
        fh.write("sibling report\n")
    for rel, spec in fx["files"].items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if "fifo" in spec:
            os.mkfifo(p)
        elif "dir" in spec:
            os.makedirs(p, exist_ok=True)
        elif "symlink" in spec:
            os.symlink(spec["symlink"].replace("{OUTSIDE}", outside).replace("{SIBLING}", sibling), p)
        else:
            if "json" in spec:
                data = json.dumps(spec["json"], ensure_ascii=False).encode("utf-8")
            elif "raw" in spec:
                data = spec["raw"].encode("utf-8")
            else:
                data = spec["text"].encode("utf-8")
            with open(p, "wb") as fh:
                fh.write(data)
    if fx["mode"] == "rev":
        env = {"PATH": "/usr/bin", "HOME": root, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
        g = ["git", "-C", d]
        subprocess.run(g + ["init", "-q"], check=True, env=env, capture_output=True)
        top = subprocess.run(g + ["rev-parse", "--show-toplevel"], capture_output=True, text=True, env=env).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            return None
        subprocess.run(g + ["add", "-A"], check=True, env=env, capture_output=True)
        for rel, spec in fx.get("gitlinks", {}).items():  # a 160000 entry at a path (no submodule checkout)
            subprocess.run(g + ["update-index", "--add", "--cacheinfo", f"160000,{spec},{rel}"], check=True, env=env,
                           capture_output=True)
        subprocess.run(g + ["-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "-c", "commit.gpgsign=false",
                            "commit", "-q", "-m", "fixture"], check=True, env=env, capture_output=True)
    return d


SANDBOX: list[str] = []


def sandbox_argv(lane: str, work: str) -> list[str]:
    return [shutil.which("bwrap") or "bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
            "--tmpfs", os.path.dirname(work), "--bind", work, work, "--tmpfs", lane, "--unshare-net",
            "--die-with-parent", "--"]


def run_check(check: str, d: str, fx: dict, timeout: int) -> dict | None:
    args = ["--repo", d] + (["--rev", "HEAD"] if fx["mode"] == "rev" else ["--worktree"]) + fx["args"]
    env = {"PATH": "/usr/bin", "HOME": "/nonexistent", "LC_ALL": "C", "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_CONFIG_GLOBAL": "/dev/null"}
    try:
        r = subprocess.run(SANDBOX + [sys.executable, "-I", check] + args, capture_output=True, env=env,
                           timeout=timeout, cwd=d)
    except subprocess.TimeoutExpired:
        return None
    return {"rc": r.returncode, "out": r.stdout}


def meets(res: dict | None, e: dict) -> bool:
    if res is None:
        return False
    raw = res["out"]
    if not raw.isascii():
        return False
    out = raw.decode("ascii")
    lines = out.splitlines()
    if res["rc"] != e["rc"]:
        return False
    ids = sorted(ln.split()[0] for ln in lines if re.match(r"^SR0[1-9] ", ln))
    if ids != e["ids"]:
        return False
    if any(c not in out for c in e.get("contains", [])):
        return False
    if "summary" in e:
        s = next((SUM.match(ln) for ln in lines if SUM.match(ln)), None)
        if s is None:
            return False
        got = dict(zip(FIELDS, (int(x) for x in s.groups()[:9])))
        if any(got[k] != v for k, v in e["summary"].items()):
            return False
    if "fields" in e and any(len(ln.split()) != e["fields"] for ln in lines if re.match(r"^SR0[1-3] ", ln)):
        return False
    if "lines" in e and len(lines) != e["lines"]:
        return False
    return True


def fresh_battery(seed: int, n: int) -> list[dict]:
    """Held-out leg over the F1-F5 vocabulary; every expectation follows from what the generator chose to write."""
    import random
    rnd = random.Random(seed)
    out = []
    for k in range(n):
        rd = rnd.randint(100, 999)
        W_ = f".ufo/waves/round-{rd}"
        mode = rnd.choice(["worktree", "rev"])
        files: dict = {}
        gitlinks: dict = {}
        nwaves = rnd.randint(1, 3)
        waves = rnd.sample(["w1", "w2", "w3", "r1", "x9"], nwaves)
        seats = present = missing = unsafe = 0
        ids: list[str] = []
        bad_by_wave: dict = {}  # wave -> rc-2 message substring when its dispatch is not a regular file
        names_odd = False
        for w in waves:
            kind = rnd.random()
            if kind < 0.12:
                files[f"{W_}/{w}-real.json"] = {"json": {"taskCall": {"context": "c", "tasks": [
                    {"name": "S", "task": f"Report: {W_}/{w}/S.md\n"}]}}}
                files[f"{W_}/{w}-dispatch.json"] = {"symlink": f"{w}-real.json"}
                bad_by_wave[w] = "dispatch is a symlink"
                continue
            if kind < 0.18 and mode == "worktree":
                files[f"{W_}/{w}-dispatch.json"] = {"fifo": True}
                bad_by_wave[w] = "not a regular file"
                continue
            if kind < 0.22:
                if mode == "rev":
                    files[f"{W_}/{w}-dispatch.json/inner"] = {"text": "x"}
                else:
                    files[f"{W_}/{w}-dispatch.json"] = {"dir": True}
                bad_by_wave[w] = "not a regular file"
                continue
            tasks = []
            for i in range(rnd.randint(1, 3)):
                nm = rnd.choice([f"S{i}", f"Seat {i}", f"S{i}\tx", f"S\u00e9{i}", f"S{i}\nSR01 x"])
                names_odd = names_odd or not all(33 <= ord(ch) <= 126 for ch in nm)
                st = rnd.choice(["present", "missing", "outside", "inside-link"])
                rp = f"{W_}/{w}/{i}.md"
                if st == "outside":
                    rp = f"{W_}/{w}-out/{i}.md"
                    files[f"{W_}/{w}-out"] = {"symlink": "{OUTSIDE}"}
                    if mode == "worktree":
                        unsafe += 1
                        ids.append("SR03")
                    else:
                        missing += 1
                        ids.append("SR01")
                elif st == "inside-link":
                    files[f"{W_}/{w}-real/{i}.md"] = {"text": "r"}
                    files[f"{W_}/{w}-alias{i}"] = {"symlink": f"{w}-real"}
                    rp = f"{W_}/{w}-alias{i}/{i}.md"
                    if mode == "worktree":
                        present += 1
                    else:
                        missing += 1
                        ids.append("SR01")
                elif st == "present":
                    files[rp] = {"text": "x"}
                    present += 1
                else:
                    missing += 1
                    ids.append("SR01")
                seats += 1
                tasks.append({"name": nm, "task": f"Report: write your scoped findings to {rp}"})
            files[f"{W_}/{w}-dispatch.json"] = {"json": {"taskCall": {"context": "c", "tasks": tasks}}}
        # the check walks a round's waves in sorted order and stops at the first unusable dispatch
        bad = bad_by_wave[min(bad_by_wave)] if bad_by_wave else None
        reps = rnd.choice([1, 2, 3])
        args = ["--round", str(rd)] * reps
        if bad:
            e = {"rc": 2, "ids": [], "contains": [bad]}
        else:
            e = {"rc": 1 if ids else 0, "ids": sorted(ids), "contains": [],
                 "summary": {"rounds": 1, "waves": nwaves, "seats": seats, "present": present, "missing": missing,
                             "unsafe": unsafe}}
            if ids:
                e["fields"] = 5
            e["lines"] = len(ids) + 1
        item = {"id": f"fresh-{seed:08x}-{k:03d}", "class": "fresh", "mode": mode, "files": files, "args": args,
                "expect": e}
        if gitlinks:
            item["gitlinks"] = gitlinks
        out.append(item)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--battery", required=True)
    ap.add_argument("--mutants", required=True)
    ap.add_argument("--expect-battery-sha256", required=True)
    ap.add_argument("--expect-mutants-sha256", required=True)
    ap.add_argument("--r91-argv", required=True, help="JSON file: argv of the round-91 C2 counter without --rev/"
                    "--scratch-root/--draft-check (its own pins inside)")
    ap.add_argument("--expect-r91-argv-sha256", required=True)
    ap.add_argument("--expect-r91-counter-sha256", required=True,
                    help="sha256 of quality/counters/c2-r91-seat-reports.py as read from <rev>")
    ap.add_argument("--fresh", type=int, default=60)
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--draft-check")
    a = ap.parse_args()
    lane = os.path.realpath(a.repo)
    scratch = os.path.realpath(a.scratch_root)

    def setup(msg: str) -> int:
        print(f"MADO_GATE_DEFECTS: SETUP_ERROR {msg}")
        return 2

    if scratch == lane or scratch.startswith(lane + os.sep):
        return setup("--scratch-root must lie outside the lane repository")
    for p, want in ((a.battery, a.expect_battery_sha256), (a.mutants, a.expect_mutants_sha256),
                    (a.r91_argv, a.expect_r91_argv_sha256)):
        try:
            got = sha(p)
        except OSError as e:
            return setup(f"cannot read {p}: {e}")
        if got != want:
            return setup(f"sha256 mismatch {p}: {got} != {want}")
    battery = json.load(open(a.battery, encoding="utf-8"))["fixtures"]
    mutants = json.load(open(a.mutants, encoding="utf-8"))["mutants"]
    r91_argv = json.load(open(a.r91_argv, encoding="utf-8"))["argv"]
    if a.fresh < 1:
        return setup("--fresh must be at least 1 (the fresh leg is part of the predicate)")
    if shutil.which("bwrap") is None:
        return setup("bwrap not found")
    os.makedirs(scratch, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c2r92-", dir=scratch)
    global SANDBOX
    SANDBOX = sandbox_argv(lane, work)
    try:
        if a.draft_check:
            check_bytes = open(a.draft_check, "rb").read()
            label = f"draft:{a.draft_check}"
        else:
            check_bytes = git_show(lane, a.rev, CHECK)
            if check_bytes is None:
                return setup(f"{CHECK} absent at {a.rev}")
            label = a.rev
        base_bytes = git_show(lane, a.base_rev, CHECK)

        def write_check(name: str, b: bytes) -> str:
            d = os.path.join(work, "k-" + hashlib.sha256((name + str(os.getpid())).encode()).hexdigest()[:12])
            os.makedirs(d, exist_ok=True)
            p = os.path.join(d, "check-seat-reports.py")
            with open(p, "wb") as fh:
                fh.write(b)
            return p

        fresh = fresh_battery(int(hashlib.sha256(check_bytes).hexdigest()[:8], 16), a.fresh)
        allfx = battery + fresh
        trees = []
        for i, fx in enumerate(allfx):
            root = os.path.join(work, f"b{i:03d}")
            outside = os.path.join(root, "outside")
            os.makedirs(outside)
            with open(os.path.join(outside, "A.md"), "w") as fh:
                fh.write("outside report\n")
            d = build(fx, root, outside)
            if d is None:
                return setup(f"{fx['id']}: fixture repository is not its own toplevel")
            trees.append(d)

        def score_all(check: str) -> list[bool]:
            with ThreadPoolExecutor(max_workers=8) as ex:
                res = list(ex.map(lambda i: run_check(check, trees[i], allfx[i], a.timeout), range(len(allfx))))
            return [meets(r, fx["expect"]) for r, fx in zip(res, allfx)]

        def score(check: str) -> list[bool]:
            return score_all(check)[:len(battery)]

        def selftest(check: str) -> str:
            try:
                r = subprocess.run(SANDBOX + [sys.executable, "-I", check, "--selftest"], capture_output=True, timeout=60,
                                   env={"PATH": "/usr/bin", "HOME": "/nonexistent", "LC_ALL": "C",
                                        "GIT_CONFIG_NOSYSTEM": "1", "TMPDIR": work})
            except subprocess.TimeoutExpired:
                return "timeout"
            last = (r.stdout.decode("utf-8", "replace").strip().splitlines() or [""])[-1]
            return f"rc={r.returncode}:{last}"

        cand = write_check("candidate", check_bytes)
        res_all = score_all(cand)
        res = res_all[:len(battery)]
        fres = res_all[len(battery):]
        fresh_met = sum(fres)
        for fx, ok in zip(fresh, fres):
            if not ok:
                print(f"fresh {fx['id']} MISSED")
        n = len(battery)
        met = sum(res)
        classes: dict[str, list[int]] = {}
        for fx, ok in zip(battery, res):
            print(f"fixture {fx['id']} {'ok' if ok else 'MISSED'}")
            classes.setdefault(fx["class"], [0, 0])
            classes[fx["class"]][0] += ok
            classes[fx["class"]][1] += 1
        st = selftest(cand)
        st_ok = bool(re.fullmatch(r"rc=0:SEAT_REPORTS_SELFTEST: checks=\d+ failed=0", st))

        text = check_bytes.decode("utf-8")
        killed = 0
        for m in mutants:
            if text.count(m["find"]) != 1:
                return setup(f"mutant {m['id']}: find occurs {text.count(m['find'])} times")
            mp = write_check(f"m-{m['id']}", text.replace(m["find"], m["replace"]).encode())
            mres = score_all(mp)
            mm = sum(mres[:n])
            mst = selftest(mp)
            k = mm < n or sum(mres[n:]) < len(fresh) or mst != st
            killed += k
            print(f"mutant {m['id']} {'killed' if k else 'SURVIVED'} met={mm} selftest={'same' if mst == st else 'differs'}")

        ctl = {"base": sum(score(write_check("base", base_bytes))) if base_bytes is not None else 0,
               "always_ok": sum(score(write_check("aok", ALWAYS_OK.encode()))),
               "always_refuse": sum(score(write_check("aref", ALWAYS_REFUSE.encode())))}

        # no-regression leg: the round-91 frozen counter on the same revision (or the same draft bytes)
        # the round-91 counter's code is read from <rev> and pinned (R92MCritic §6.6); its data paths stay lane-relative
        r91_bytes = git_show(lane, a.rev, r91_argv[0])
        if r91_bytes is None or hashlib.sha256(r91_bytes).hexdigest() != a.expect_r91_counter_sha256:
            return setup(f"{r91_argv[0]} at {a.rev} absent or not the pinned bytes")
        r91_path = os.path.join(work, "r91-counter.py")
        with open(r91_path, "wb") as fh:
            fh.write(r91_bytes)
        r91 = [sys.executable, "-I", r91_path] + r91_argv[1:] + ["--rev", a.rev, "--scratch-root",
                                                                os.path.join(work, "r91")]
        if a.draft_check:
            r91 += ["--draft-check", a.draft_check]
        rr = subprocess.run(r91, capture_output=True, text=True, cwd=lane)
        r91_line = next((ln for ln in rr.stdout.splitlines() if ln.startswith("MADO_SEAT_REPORTS:")), "absent")
        if "SETUP_ERROR" in r91_line or r91_line == "absent":
            return setup(f"round-91 leg: {r91_line}")
        r91_ok = r91_line.split()[1:2] == (["DRAFT_TARGET_MET"] if a.draft_check else ["TARGET_MET"])
    finally:
        shutil.rmtree(work, ignore_errors=True)

    ok = (met == n and fresh_met == len(fresh) and st_ok and killed == len(mutants) and all(v < n for v in ctl.values())
          and r91_ok)
    verdict = ("DRAFT_TARGET_MET" if ok else "DRAFT_TARGET_MISSED") if a.draft_check else (
        "TARGET_MET" if ok else "TARGET_MISSED")
    ctxt = " ".join(f"{k}={v[0]}/{v[1]}" for k, v in sorted(classes.items()))
    print(f"MADO_GATE_DEFECTS: {verdict} pred={PRED} rev={label} base_rev={a.base_rev} fixtures={n} met={met} {ctxt} "
          f"fresh={fresh_met}/{len(fresh)} "
          f"selftest={'ok' if st_ok else 'FAIL'}:{st.split(':', 1)[-1]} mutants={len(mutants)} killed={killed} "
          + " ".join(f"{k}_met={v}" for k, v in ctl.items())
          + f" r91_counter={'TARGET_MET' if r91_ok else 'NOT_MET'} check_sha256={hashlib.sha256(check_bytes).hexdigest()}")
    print(f"r91: {r91_line}")
    if a.draft_check:
        return 3
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
