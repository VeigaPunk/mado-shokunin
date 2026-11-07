#!/usr/bin/env python3
"""Round-93 C2 (L1): write the frozen probe panel for PRED-C2-r93-v1.

  weakenings  — hand weakenings of quality/check-seat-reports.py's selftest: h01..h10 (R93MExecCounterC2's
                generator, HAND rows) and e01..e06 (R93MMutC2 §6 escapes E1-E5 and E8). Each must keep the
                weakened selftest green (rc 0, checks=23 failed=0): a weakening that turns the selftest red is
                not a passing weakening and is refused here.
  neutrals    — strength-preserving edits (comments, a reorder, a lambda-to-def, a tightened want_in, a header comment);
                each keeps the selftest green and changes the tool's bytes, so a gate that flags any byte change
                (the sha-diff forgery) fails them.
  setup       — setup-path probes for the gate mutants: (name, tool edit or kill-set edit, gate flags); the
                counter records the gate's (verdict, rc) on each; no expected value is stated here.
Edits are {id, what, find, replace, all?}; `find` must occur exactly once (or >= 1 with "all": true).
Usage: gen-c2-panel-r93.py --tool quality/check-seat-reports.py --out FILE --scratch DIR
"""
import argparse
import json
import os
import subprocess
import sys

OKLINE = "            ok = rc == want_rc and ids == want_ids and (rc == 2 or got[-1].startswith(f\"SEAT_REPORTS: mode={mode}\"))"

E = [
    ("e01-ids-superset", "ids equality -> superset (R93MMutC2 E1)", "ok = rc == want_rc and ids == want_ids and (rc == 2 or",
     "ok = rc == want_rc and set(ids) >= set(want_ids) and (rc == 2 or"),
    ("e02-rc-off-by-one", "rc equality -> rc or rc+1 (R93MMutC2 E2)", "ok = rc == want_rc and ids == want_ids",
     "ok = rc in (want_rc, want_rc + 1) and ids == want_ids"),
    ("e03-mode-token", "summary mode token -> any mode (R93MMutC2 E3)", "got[-1].startswith(f\"SEAT_REPORTS: mode={mode}\")",
     "\"SEAT_REPORTS: mode=\" in got[-1]"),
    ("e04-ascii-first-line", "ASCII check on the first line only (R93MMutC2 E4)", "all(g.isascii() for g in got)",
     "all(g.isascii() for g in got[:1])"),
    ("e05-want-in-casefold", "want_in compared case-insensitively (R93MMutC2 E5)", "any(want_in in g for g in got)",
     "any(want_in.lower() in g.lower() for g in got)"),
    ("e06-first-fail-only", "only the first failing label is printed (R93MMutC2 E8)",
     "    for n in failed:\n        print(f\"SEAT_REPORTS_SELFTEST_FAIL: {n}\")",
     "    for n in failed[:1]:\n        print(f\"SEAT_REPORTS_SELFTEST_FAIL: {n}\")"),
]

NEUTRAL = [
    ("n01-selftest-comment", "a comment line inside the selftest", "    W = \".ufo/waves/round-7\"\n",
     "    # fixtures live under a round-7 wave directory\n    W = \".ufo/waves/round-7\"\n", False),
    ("n02-reorder-two-cases", "two independent rc2 cases swap places",
     "    case(\"no dispatch for round -> rc2\", {f\"{W}/w1/A.md\": \"x\"}, [7], 2, [])\n"
     "    case(\"bad dispatch json -> rc2\", {f\"{W}/w1-dispatch.json\": \"{\"}, [7], 2, [])\n",
     "    case(\"bad dispatch json -> rc2\", {f\"{W}/w1-dispatch.json\": \"{\"}, [7], 2, [])\n"
     "    case(\"no dispatch for round -> rc2\", {f\"{W}/w1/A.md\": \"x\"}, [7], 2, [])\n", False),
    ("n03-lambda-to-def", "the selftest's dispatch helper becomes an equivalent def",
     "    disp = lambda *ts: json.dumps({\"taskCall\": {\"context\": \"c\", \"tasks\": list(ts)}})\n",
     "    def disp(*ts):\n        return json.dumps({\"taskCall\": {\"context\": \"c\", \"tasks\": list(ts)}})\n", False),
    ("n04-tighten-want-in", "a stricter assertion: the missing case also pins its SR01 text",
     "                                 f\"{W}/w1/A.md\": \"x\"}, [7], 1, [\"SR01\"])",
     "                                 f\"{W}/w1/A.md\": \"x\"}, [7], 1, [\"SR01\"], want_in=\"SR01 missing\")", False),
    ("n05-header-comment", "a comment after the shebang (production prefix)", "#!/usr/bin/env python3\n",
     "#!/usr/bin/env python3\n# neutral edit: no behaviour change\n", False),
    ("n06-blank-lines", "blank lines between selftest cases", "    case(\"empty -> SR02 rc1\",",
     "\n    case(\"empty -> SR02 rc1\",", False),
]


def apply(text: str, find: str, replace: str, every: bool = False) -> str:
    n = text.count(find)
    if n == 0 or (n != 1 and not every):
        raise SystemExit(f"find occurs {n} times: {find[:60]!r}")
    return text.replace(find, replace) if every else text.replace(find, replace, 1)


def green(text: str, scratch: str) -> bool:
    p = os.path.join(scratch, "probe.py")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    env = {"PATH": "/usr/bin", "TMPDIR": scratch, "HOME": scratch}
    r = subprocess.run([sys.executable, "-I", p, "--selftest"], capture_output=True, text=True, timeout=120,
                       cwd=scratch, env=env)
    return r.returncode == 0 and r.stdout.strip().splitlines()[-1] == "SEAT_REPORTS_SELFTEST: checks=23 failed=0"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--seat-weakenings", required=True, help="R93MExecCounterC2's selftest-weakenings-r93.json (h01-h10)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    src = open(a.tool, encoding="utf-8").read()
    seat = json.load(open(a.seat_weakenings, encoding="utf-8"))["weakenings"]
    weak = [{k: w[k] for k in ("id", "what", "find", "replace")} for w in seat if w["id"].startswith("h")]
    weak += [{"id": i, "what": w, "find": f, "replace": r} for i, w, f, r in E]
    neutral = [{"id": i, "what": w, "find": f, "replace": r, "all": al} for i, w, f, r, al in NEUTRAL]
    for w in weak:
        t = apply(src, w["find"], w["replace"])
        if not green(t, a.scratch):
            raise SystemExit(f"weakening {w['id']} turns the selftest red")
    for n in neutral:
        t = apply(src, n["find"], n["replace"], n["all"])
        if not green(t, a.scratch):
            raise SystemExit(f"neutral {n['id']} turns the selftest red")
    out = {"tool": "quality/check-seat-reports.py", "weakenings": weak, "neutrals": neutral}
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(f"GENC2 weakenings={len(weak)} neutrals={len(neutral)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
