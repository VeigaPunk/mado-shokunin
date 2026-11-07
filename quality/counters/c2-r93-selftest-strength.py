#!/usr/bin/env python3
"""Round-93 C2 counter - does a lane gate catch a weakened, still-passing selftest of the seat-report gate?

Frozen predicate PRED-C2-r93-v1 (the same sentence as the declaration and the receipt label):
  TARGET_MET iff, at <rev>, the gate and the kill-set are the frozen candidates (sha256 == --expect-gate-sha256,
  --expect-kills-sha256) and: (i) quality/check-selftest-strength.py on the unmodified
  quality/check-seat-reports.py and the committed kill-set quality/selftest-kills/check-seat-reports.json
  prints OK and exits 0, and the kill-set's tool_sha256 equals the tool's sha256 at <rev>; (ii) for every one
  of the tool's selftest checks (the labels of every case(...) call in its selftest at <rev>, as many as its
  result line's checks=N), the tool with that one check's result forced to pass makes the gate print WEAK and
  exit 1 (neutralised_flagged == checks); (iii) every frozen hand weakening of the panel (an edit that keeps
  the selftest green, checks=N failed=0) makes the gate print WEAK and exit 1 (hand_flagged == hand); (iv)
  every frozen neutral edit of the panel (a strength-preserving byte change that keeps the selftest green)
  leaves the gate at OK, exit 0 (neutral_ok == neutrals); (v) every frozen gate mutant prints a well-formed
  verdict line different in verdict or exit code from the measured gate's on at least one probe of (i)-(iv)
  or of the frozen setup panel (killed == mutants; a mutant whose only differences are missing verdict lines
  is crashed_not_killed); (vi) each control fails (i)-(iv): the do-nothing instrument (the round-92 C2
  counter's selftest leg: flag a variant iff the tool's selftest result line changes) flags fewer than the
  weakenings, an always-OK gate flags none, an always-WEAK gate fails (i), and a gate that flags every byte
  change of the tool (sha-diff) fails (iv); (vii) the gate's --selftest exits 0.

Weakening and neutral variants are checked green before use (the tool's --selftest exits 0 with
checks=N failed=0), else SETUP_ERROR.  The gate runs as `python3 -I <gate> --tool <variant> --kills <kill-set>
--allow-sha-drift` for variants and without the flag for (i).  All work lives under --scratch-root.
rc 0 TARGET_MET, 1 TARGET_MISSED, 2 SETUP_ERROR, 3 DRAFT (--draft-gate/--draft-kills; prints DRAFT_*).
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

PRED = "PRED-C2-r93-v1"
GATE = "quality/check-selftest-strength.py"
TOOL = "quality/check-seat-reports.py"
KILLS = "quality/selftest-kills/check-seat-reports.json"
R92C2 = "quality/counters/c2-r92-gate-defects.py"
NEEDLE = "    results: list[tuple[str, bool]] = []"
RESULT_PREFIX = "SEAT_REPORTS_SELFTEST: "
VERDICT_RE = re.compile(r"^SELFTEST_STRENGTH: (OK|WEAK|SETUP_ERROR)\b")
ALWAYS_OK = "import sys\nprint('SELFTEST_STRENGTH: OK tool=stub kills=0 held=0 survived=0 wrong_check=0')\nsys.exit(0)\n"
ALWAYS_WEAK = "import sys\nprint('SELFTEST_STRENGTH: WEAK tool=stub kills=0 held=0 survived=0 wrong_check=0')\nsys.exit(1)\n"
SHA_DIFF = (
    "import hashlib, json, sys\n"
    "a = sys.argv\n"
    "tool = a[a.index('--tool') + 1]; kills = a[a.index('--kills') + 1]\n"
    "want = json.load(open(kills))['tool_sha256']\n"
    "got = hashlib.sha256(open(tool, 'rb').read()).hexdigest()\n"
    "v = 'OK' if got == want else 'WEAK'\n"
    "print(f'SELFTEST_STRENGTH: {v} tool=stub kills=0 held=0 survived=0 wrong_check=0')\n"
    "sys.exit(0 if v == 'OK' else 1)\n")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_show(repo: str, rev: str, path: str) -> bytes | None:
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def apply(text: str, edit: dict) -> str:
    n = text.count(edit["find"])
    if n == 0 or (n != 1 and not edit.get("all")):
        raise ValueError(f"{edit['id']}: find occurs {n} times")
    return text.replace(edit["find"], edit["replace"]) if edit.get("all") else text.replace(edit["find"], edit["replace"], 1)


def neutralise(text: str, label: str) -> str:
    if text.count(NEEDLE) != 1:
        raise ValueError("neutralisation needle does not occur once")
    return text.replace(NEEDLE, "    class _L(list):\n        def append(self, x):\n"
                        f"            super().append((x[0], True) if x[0] == {label!r} else x)\n"
                        "    results: list[tuple[str, bool]] = _L()", 1)


def labels_of(text: str) -> list[str]:
    body = text[text.index("def selftest("):]
    return re.findall(r'^    case\("((?:[^"\\]|\\.)*)"', body, re.M)


class Run:
    def __init__(self, root: str, timeout: float):
        self.root, self.timeout, self.n = root, timeout, 0

    def dir(self) -> str:
        return tempfile.mkdtemp(prefix="p", dir=self.root)

    def selftest_line(self, tool_text: str) -> tuple[int | None, str]:
        d = self.dir()
        try:
            p = os.path.join(d, "tool.py")
            with open(p, "w", encoding="utf-8", errors="surrogateescape") as fh:
                fh.write(tool_text)
            env = {"PATH": "/usr/bin:/bin", "HOME": d, "TMPDIR": d, "LC_ALL": "C.UTF-8"}
            try:
                r = subprocess.run([sys.executable, "-I", p, "--selftest"], capture_output=True, text=True,
                                   timeout=self.timeout, cwd=d, env=env)
            except subprocess.TimeoutExpired:
                return None, ""
            res = [ln for ln in r.stdout.splitlines() if ln.startswith(RESULT_PREFIX)]
            return r.returncode, (res[-1] if res else "")
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def gate(self, gate_text: str, tool_text: str, kills_text: str, drift: bool, gate_timeout: float = 60,
             extra: list[str] | None = None) -> str:
        """Return 'VERDICT:rc' (VERDICT = OK|WEAK|SETUP_ERROR|NONE)."""
        d = self.dir()
        try:
            g, t, k = (os.path.join(d, n) for n in ("gate.py", "tool.py", "kills.json"))
            for path, body in ((g, gate_text), (t, tool_text), (k, kills_text)):
                with open(path, "w", encoding="utf-8", errors="surrogateescape") as fh:
                    fh.write(body)
            argv = [sys.executable, "-I", g, "--tool", t, "--kills", k, "--scratch-root", os.path.join(d, "s"),
                    "--timeout", str(gate_timeout)] + (["--allow-sha-drift"] if drift else []) + (extra or [])
            env = {"PATH": "/usr/bin:/bin", "HOME": d, "TMPDIR": d, "LC_ALL": "C.UTF-8"}
            try:
                r = subprocess.run(argv, capture_output=True, text=True, timeout=1800, cwd=d, env=env)
            except subprocess.TimeoutExpired:
                return "NONE:timeout"
            v = [m.group(1) for m in (VERDICT_RE.match(ln) for ln in r.stdout.splitlines()) if m]
            return f"{v[-1] if v else 'NONE'}:{r.returncode}"
        finally:
            shutil.rmtree(d, ignore_errors=True)


def setup_panel(tool: str, kills: dict) -> list[tuple[str, str, str, bool, float]]:
    """(id, tool_text, kills_text, drift, gate_timeout): probes of the gate's setup and failure arms."""
    kj = lambda o: json.dumps(o)
    out = []
    out.append(("s01-sha-guard", tool.replace("#!/usr/bin/env python3\n", "#!/usr/bin/env python3\n# drift\n", 1),
                kj(kills), False, 60))
    out.append(("s02-broken-tool", tool.replace("    return 1 if bad else 0", "    return 1", 1), kj(kills), True, 60))
    amb = dict(kills, kills=kills["kills"] + [{"id": "amb", "find": "return", "replace": "return", "must_fail": "x"}])
    out.append(("s03-ambiguous-find", tool, kj(amb), False, 60))
    slow = dict(kills, kills=[{"id": "slow", "find": "    return lines, c",
                               "replace": "    import time\n    time.sleep(600)\n    return lines, c",
                               "must_fail": "all present -> OK rc0"}])
    out.append(("s04-timeout-kill", tool, kj(slow), False, 5))
    loud = dict(kills, kills=[{"id": "loud", "find": "    return lines, c",
                               "replace": "    print('SEAT_REPORTS_SELFTEST_FAIL: all present -> OK rc0')\n"
                                          "    return lines, c", "must_fail": "all present -> OK rc0"}])
    out.append(("s05-fail-line-exit-0", tool, kj(loud), False, 60))
    out.append(("s06-result-line-not-failed0",
                tool.replace("failed={len(failed)}\")", "failed=none\")", 1), kj(kills), True, 60))
    out.append(("s07-checks-pin", tool, kj(dict(kills, selftest_checks=kills.get("selftest_checks", 0) - 1)), False, 60))
    wk = [dict(k) for k in kills["kills"]]
    wk[0]["must_fail"] = ["no such label"]
    out.append(("s08-wrong-check", tool, kj(dict(kills, kills=wk)), False, 60))
    crash = dict(kills, kills=[{"id": "crash", "find": "    return lines, c", "replace": "    return lines, c)",
                                "must_fail": "all present -> OK rc0"}])
    out.append(("s09-crash-kill", tool, kj(crash), False, 60))
    bad = dict(kills, kills=[{"id": "bad", "find": "    return lines, c", "replace": "    return lines, c",
                              "must_fail": 7}])
    out.append(("s10-bad-kill-entry", tool, kj(bad), False, 60))
    one = dict(kills, kills=[dict(kills["kills"][0], must_fail=kills["kills"][0]["must_fail"] + ["extra label"])
                             if isinstance(kills["kills"][0]["must_fail"], list) else kills["kills"][0]])
    out.append(("s11-must-fail-superset", tool, kj(one), False, 60))
    pre = "SEAT_REPORTS_SELFTEST_FAIL: "
    mid = "m " + pre + "q"
    inner = dict(kills, kills=[{"id": "inner", "find": "    return lines, c",
                                "replace": f"    print({('a' * len(pre) + mid)!r})\n    raise SystemExit(1)\n"
                                           "    return lines, c", "must_fail": [mid]}])
    out.append(("s12-fail-prefix-mid-line", tool, kj(inner), False, 60))
    multi = next((k for k in kills["kills"] if isinstance(k["must_fail"], list) and len(k["must_fail"]) > 1), None)
    if multi is not None:
        out.append(("s13-must-fail-subset", tool, kj(dict(kills, kills=[dict(multi, must_fail=multi["must_fail"][1:])])),
                    False, 60))
    out.append(("s14-selftest-rc1-failed0", tool.replace("    return 1 if failed else 0", "    return 1", 1), kj(kills),
                True, 60))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--panel", required=True)
    ap.add_argument("--expect-panel-sha256", required=True)
    ap.add_argument("--mutants", required=True)
    ap.add_argument("--expect-mutants-sha256", required=True)
    ap.add_argument("--expect-r92-counter-sha256", required=True)
    ap.add_argument("--expect-gate-sha256", required=True, help="the frozen gate candidate's sha256")
    ap.add_argument("--expect-kills-sha256", required=True, help="the frozen kill-set candidate's sha256")
    ap.add_argument("--scratch-root", required=True)
    ap.add_argument("--timeout", type=float, default=120)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--draft-gate", help="DRAFT only: this gate file instead of <rev>:" + GATE)
    ap.add_argument("--draft-kills", help="DRAFT only: this kill-set instead of <rev>:" + KILLS)
    a = ap.parse_args()
    draft = bool(a.draft_gate or a.draft_kills)
    sys.stdout.reconfigure(line_buffering=True)
    tag = "DRAFT_" if draft else ""

    def setup(msg: str) -> int:
        print(f"MADO_SELFTEST_STRENGTH: SETUP_ERROR pred={PRED} {msg}")
        return 2

    panel_b = open(a.panel, "rb").read()
    if sha(panel_b) != a.expect_panel_sha256:
        return setup(f"panel sha256 {sha(panel_b)} != pinned")
    mut_b = open(a.mutants, "rb").read()
    if sha(mut_b) != a.expect_mutants_sha256:
        return setup(f"mutants sha256 {sha(mut_b)} != pinned")
    panel, mutants = json.loads(panel_b), json.loads(mut_b)["mutants"]
    r92 = git_show(a.repo, a.rev, R92C2)
    if r92 is None or sha(r92) != a.expect_r92_counter_sha256:
        return setup("round-92 C2 counter at <rev> missing or not the pinned bytes")
    gate_b = open(a.draft_gate, "rb").read() if a.draft_gate else git_show(a.repo, a.rev, GATE)
    kills_b = open(a.draft_kills, "rb").read() if a.draft_kills else git_show(a.repo, a.rev, KILLS)
    tool_b = git_show(a.repo, a.rev, TOOL)
    if gate_b is None or kills_b is None or tool_b is None:
        return setup(f"gate/kill-set/tool absent at {a.rev}")
    gate_t, kills_t = gate_b.decode("utf-8"), kills_b.decode("utf-8")
    tool_t = tool_b.decode("utf-8")
    kills = json.loads(kills_t)
    pin_ok = kills.get("tool_sha256") == sha(tool_b)
    frozen_ok = sha(gate_b) == a.expect_gate_sha256 and sha(kills_b) == a.expect_kills_sha256
    os.makedirs(a.scratch_root, exist_ok=True)
    root = tempfile.mkdtemp(prefix="c2r93-", dir=a.scratch_root)
    run = Run(root, a.timeout)
    try:
        rc0, line0 = run.selftest_line(tool_t)
        m = re.match(r"^SEAT_REPORTS_SELFTEST: checks=(\d+) failed=0$", line0)
        if rc0 != 0 or not m:
            return setup(f"tool selftest at <rev> not green: rc={rc0} {line0!r}")
        checks = int(m.group(1))
        labels = labels_of(tool_t)
        if len(labels) != checks or len(set(labels)) != checks:
            return setup(f"labels enumerated {len(labels)} (unique {len(set(labels))}) != checks={checks}")
        try:
            neut = [(f"N:{lb}", neutralise(tool_t, lb)) for lb in labels]
            hand = [(f"W:{w['id']}", apply(tool_t, w)) for w in panel["weakenings"]]
            nonw = [(f"Z:{n['id']}", apply(tool_t, n)) for n in panel["neutrals"]]
        except ValueError as e:
            return setup(str(e))
        variants = neut + hand + nonw
        with ThreadPoolExecutor(a.workers) as ex:
            lines = list(ex.map(lambda v: run.selftest_line(v[1]), variants))
        for (vid, _), (rc, ln) in zip(variants, lines):
            if rc != 0 or ln != line0:
                return setup(f"variant {vid} does not keep the selftest green: rc={rc} {ln!r}")
        weak = neut + hand
        sp = setup_panel(tool_t, kills)

        jobs = [(tool_t, kills_t, False, 60)] + [(t, kills_t, True, 60) for _, t in variants] + \
               [(t, k, dr, to) for _, t, k, dr, to in sp]

        def vector(gtext: str) -> list[str]:
            with ThreadPoolExecutor(a.workers) as ex:
                return list(ex.map(lambda j: run.gate(gtext, j[0], j[1], j[2], j[3]), jobs))

        def first_difference(gtext: str, base: list[str]) -> tuple[str, int | None, str]:
            """Probe in batches (setup panel first, then (i), then the variants) and stop at the first probe whose
            well-formed verdict differs from the measured gate's: the same set test as a full vector, cheaper."""
            order = list(range(1 + len(variants), len(jobs))) + [0] + list(range(1, 1 + len(variants)))
            none_diff = False
            for k in range(0, len(order), a.workers):
                idx = order[k:k + a.workers]
                with ThreadPoolExecutor(a.workers) as ex:
                    got = list(ex.map(lambda i: run.gate(gtext, *jobs[i]), idx))
                for i, g in zip(idx, got):
                    if g != base[i]:
                        if not g.startswith("NONE:"):
                            return "killed", i, g
                        none_diff = True
            return ("crashed_not_killed" if none_diff else "SURVIVED"), None, ""

        vec = vector(gate_t)
        pos = vec[0]
        vw = vec[1:1 + len(weak)]
        vz = vec[1 + len(weak):1 + len(variants)]
        nflag = sum(v == "WEAK:1" for v in vw[:len(neut)])
        hflag = sum(v == "WEAK:1" for v in vw[len(neut):])
        zok = sum(v == "OK:0" for v in vz)
        for (vid, _), v in zip(variants, vec[1:1 + len(variants)]):
            print(f"probe {vid} {v}")
        for (sid, *_), v in zip(sp, vec[1 + len(variants):]):
            print(f"probe {sid} {v}")
        killed = crashed = 0
        for mu in mutants:
            if gate_t.count(mu["find"]) != 1:
                return setup(f"gate mutant {mu['id']} find occurs {gate_t.count(mu['find'])} times")
            st, at, got = first_difference(gate_t.replace(mu["find"], mu["replace"], 1), vec)
            killed += st == "killed"
            crashed += st == "crashed_not_killed"
            names = [f"(i)"] + [v[0] for v in variants] + [x[0] for x in sp]
            print(f"mutant {mu['id']} {st}" + (f" at {names[at]} {vec[at]}->{got}" if at is not None else ""))
        # controls
        dn = sum(ln != line0 for (_, _), (_, ln) in zip(weak, lines[:len(weak)]))
        ok_t = vector(ALWAYS_OK)
        aok = sum(v == "WEAK:1" for v in ok_t[1:1 + len(weak)])
        weak_t = run.gate(ALWAYS_WEAK, tool_t, kills_t, False)
        sd = vector(SHA_DIFF)
        sd_flag = sum(v == "WEAK:1" for v in sd[1:1 + len(weak)])
        sd_zok = sum(v == "OK:0" for v in sd[1 + len(weak):1 + len(variants)])
        d = run.dir()
        gp = os.path.join(d, "gate.py")
        with open(gp, "w", encoding="utf-8") as fh:
            fh.write(gate_t)
        gs = subprocess.run([sys.executable, "-I", gp, "--selftest"], capture_output=True, text=True,
                            timeout=600, cwd=d, env={"PATH": "/usr/bin:/bin", "HOME": d, "TMPDIR": d})
        gs_ok = gs.returncode == 0
    finally:
        shutil.rmtree(root, ignore_errors=True)
    nw = len(weak)
    met = (frozen_ok and pos == "OK:0" and pin_ok and nflag == len(neut) and hflag == len(hand) and zok == len(nonw)
           and killed == len(mutants) and dn < nw and aok < nw and weak_t != "OK:0"
           and sd_zok < len(nonw) and gs_ok)
    word = ("TARGET_MET" if met else "TARGET_MISSED")
    print(f"MADO_SELFTEST_STRENGTH: {tag}{word} pred={PRED} rev={'draft' if draft else a.rev} checks={checks} "
          f"frozen_pin={'ok' if frozen_ok else 'FAIL'} positive={pos} kill_set_pin={'ok' if pin_ok else 'FAIL'} neutralised_flagged={nflag}/{len(neut)} "
          f"hand_flagged={hflag}/{len(hand)} neutral_ok={zok}/{len(nonw)} mutants={len(mutants)} killed={killed} "
          f"crashed_not_killed={crashed} do_nothing_flagged={dn}/{nw} always_ok_flagged={aok}/{nw} "
          f"always_weak_positive={weak_t} shadiff_flagged={sd_flag}/{nw} shadiff_neutral_ok={sd_zok}/{len(nonw)} "
          f"gate_selftest={'ok' if gs_ok else 'FAIL'} gate_sha256={sha(gate_b)} kills_sha256={sha(kills_b)} "
          f"tool_sha256={sha(tool_b)}")
    if draft:
        return 3
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
