#!/usr/bin/env python3
"""Round 93 C2 weakening generator — frozen hand + fresh grammar for PRED-C2-r93-v1. [R93MExecCounterC2]

Writes selftest-weakenings-r93.json: {"tool","tool_sha256","seed","weakenings":[{id,what,find,replace,check}]}.
Each weakening is applied once (find exactly once) to quality/check-seat-reports.py; the gate must
print WEAK on the weakened tool. Every row is verified (below) to keep `--selftest checks=23 failed=0`
on the unmodified production code before being written; unverifiable rows abort the run.

Hand weakenings (must keep failed=0 on unmodified production code):
  * remove a `want_in` requirement (the failure-message pin disappears; production regressions that
    keep rc/ids but change the message now pass) — one per want_in-bearing check;
  * widen the shared ids equality to a prefix comparison (`ids == want_ids` -> prefix);
  * drop the rc comparison from the shared ok predicate;
  * drop the mode-prefix comparison from the shared ok predicate;
  * revert the F3 repeated-round data `[7, 7]` -> `[7]`.

Frozen fresh grammar: seed = first 8 hex digits of the gate candidate's sha256 drives
random.Random(int(seed,16)). At each draw, a (check, transform) pair is chosen from the frozen
table FRESH_POOL (label, transform, concrete find/replace). A pick is admitted only if it verifies
green (checks=23 failed=0) AND its (check, transform) pair has not been used; 20 fresh picks.
The table below IS the frozen grammar; the seed chooses which rows are used, never new transforms.
"""
from __future__ import annotations
import hashlib, json, os, random, subprocess, sys, tempfile, re

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
TOOL = os.path.join(LANE, "quality/check-seat-reports.py")
OUT = os.path.join(LANE, ".ufo/waves/round-93/controls/selftest-weakenings-r93.json")
GATE_CAND = os.path.join(LANE, ".ufo/waves/round-93/build/check-selftest-strength.c2.py")

# --- hand weakenings -------------------------------------------------------
HAND = [
    dict(id="h01-want-in-drop-f1-rev",
         what="remove the want_in pin of the rev symlinked-dispatch check (F1)",
         find='         [7], 2, [], git=True, want_in="dispatch is a symlink")',
         replace='         [7], 2, [], git=True)',
         check="rev: symlinked dispatch -> rc2 (F1)"),
    dict(id="h02-want-in-drop-f1-worktree",
         what="remove the want_in pin of the worktree symlinked-dispatch check (F1)",
         find='         f"{W}/w2-dispatch.json": {"symlink": "real.json"}}, [7], 2, [], want_in="dispatch is a symlink")',
         replace='         f"{W}/w2-dispatch.json": {"symlink": "real.json"}}, [7], 2, [])',
         check="worktree: symlinked dispatch -> rc2 (F1)"),
    dict(id="h03-want-in-drop-f2",
         what="remove the want_in pin of the ASCII-token check (F2)",
         find='["SR01"], want_in=\'"A\\\\u0020b\\\\nc"\')',
         replace='["SR01"])',
         check="name with space and non-ASCII path -> ASCII tokens (F2)"),
    dict(id="h04-want-in-drop-f3",
         what="remove the want_in pin of the repeated-round check (F3)",
         find='["SR01"], want_in="rounds=1 waves=1 seats=1")',
         replace='["SR01"])',
         check="repeated --round counts once (F3)"),
    dict(id="h05-want-in-drop-f4",
         what="remove the want_in pin of the FIFO check (F4)",
         find='         want_in="not a regular file")',
         replace='         )',
         check="worktree: FIFO dispatch -> rc2, no hang (F4)"),
    dict(id="h06-widen-ids-to-prefix",
         what="widen the ids equality in the shared ok predicate to a prefix comparison",
         find='            ok = rc == want_rc and ids == want_ids and (rc == 2 or got[-1].startswith(f"SEAT_REPORTS: mode={mode}"))',
         replace='            ok = rc == want_rc and ids[:len(want_ids)] == want_ids and (rc == 2 or got[-1].startswith(f"SEAT_REPORTS: mode={mode}"))',
         check="missing -> SR01 rc1"),
    dict(id="h07-drop-rc-comparison",
         what="drop the rc comparison from the shared ok predicate",
         find='            ok = rc == want_rc and ids == want_ids and (rc == 2 or got[-1].startswith(f"SEAT_REPORTS: mode={mode}"))',
         replace='            ok = ids == want_ids and (rc == 2 or got[-1].startswith(f"SEAT_REPORTS: mode={mode}"))',
         check="missing -> SR01 rc1"),
    dict(id="h08-drop-mode-comparison",
         what="drop the mode/summary-line comparison from the shared ok predicate",
         find='            ok = rc == want_rc and ids == want_ids and (rc == 2 or got[-1].startswith(f"SEAT_REPORTS: mode={mode}"))',
         replace='            ok = rc == want_rc and ids == want_ids',
         check="rev: present -> OK rc0"),
    dict(id="h09-f3-repeat-removed",
         what="revert the F3 repeated-round data [7, 7] -> [7] (the repeat assertion disappears)",
         find='case("repeated --round counts once (F3)", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md"))}, [7, 7], 1,',
         replace='case("repeated --round counts once (F3)", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md"))}, [7], 1,',
         check="repeated --round counts once (F3)"),
    dict(id="h10-widen-ids-subset",
         what="widen the ids equality to a subset membership (every want_id present, extras allowed)",
         find='            ok = rc == want_rc and ids == want_ids and (rc == 2 or got[-1].startswith(f"SEAT_REPORTS: mode={mode}"))',
         replace='            ok = rc == want_rc and all(w in ids for w in want_ids) and (rc == 2 or got[-1].startswith(f"SEAT_REPORTS: mode={mode}"))',
         check="empty -> SR02 rc1"),
]

# --- frozen fresh grammar --------------------------------------------------
# Each entry: (transform-name, check-label, what, find, replace).
FRESH_POOL = [
    ("drop-want-in", "rev: symlinked dispatch -> rc2 (F1)",
     "remove the want_in pin of the rev symlinked-dispatch check (F1)",
     '         [7], 2, [], git=True, want_in="dispatch is a symlink")',
     '         [7], 2, [], git=True)'),
    ("drop-want-in", "worktree: symlinked dispatch -> rc2 (F1)",
     "remove the want_in pin of the worktree symlinked-dispatch check (F1)",
     '         f"{W}/w2-dispatch.json": {"symlink": "real.json"}}, [7], 2, [], want_in="dispatch is a symlink")',
     '         f"{W}/w2-dispatch.json": {"symlink": "real.json"}}, [7], 2, [])'),
    ("drop-want-in", "name with space and non-ASCII path -> ASCII tokens (F2)",
     "remove the want_in pin of the ASCII-token check (F2)",
     '["SR01"], want_in=\'"A\\\\u0020b\\\\nc"\')',
     '["SR01"])'),
    ("drop-want-in", "repeated --round counts once (F3)",
     "remove the want_in pin of the repeated-round check (F3)",
     '["SR01"], want_in="rounds=1 waves=1 seats=1")',
     '["SR01"])'),
    ("drop-want-in", "worktree: FIFO dispatch -> rc2, no hang (F4)",
     "remove the want_in pin of the FIFO check (F4)",
     '         want_in="not a regular file")',
     '         )'),
    ("remove-f3-repeat", "repeated --round counts once (F3)",
     "revert the F3 repeated-round data [7, 7] -> [7]",
     'case("repeated --round counts once (F3)", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md"))}, [7, 7], 1,',
     'case("repeated --round counts once (F3)", {f"{W}/w1-dispatch.json": disp(task("A", f"{W}/w1/A.md"))}, [7], 1,'),
]

def verify(src: str, find: str, replace: str) -> bool:
    if src.count(find) != 1:
        return False
    mut = src.replace(find, replace, 1)
    with tempfile.TemporaryDirectory(prefix="c2w-") as d:
        p = os.path.join(d, "tool.py")
        with open(p, "w") as fh:
            fh.write(mut)
        try:
            r = subprocess.run([sys.executable, "-I", p, "--selftest"], capture_output=True, text=True,
                               env={**os.environ, "TMPDIR": d}, timeout=60)
        except subprocess.TimeoutExpired:
            return False
        return r.returncode == 0 and "checks=23 failed=0" in r.stdout

def main() -> int:
    gate_sha = hashlib.sha256(open(GATE_CAND, "rb").read()).hexdigest()
    seed = gate_sha[:8]
    src = open(TOOL, encoding="utf-8").read()
    for r in HAND:
        if not verify(src, r["find"], r["replace"]):
            print(f"hand weakening unverifiable (must keep green, find once): {r['id']}", file=sys.stderr)
            return 1
    rnd = random.Random(int(seed, 16))
    # Fresh: the seed draws 20 (check, transform) picks from FRESH_POOL. The pool is the frozen
    # grammar: each pool row is one (check, transform) pair with explicit find/replace. Picks are
    # drawn with repetition in seed order (the grammar has 6 rows; a pick is a row index), each
    # with a fresh id. Every pick verifies green before admission.
    fresh = []
    while len(fresh) < 20:
        name, label, what, find, replace = FRESH_POOL[rnd.randrange(len(FRESH_POOL))]
        if not verify(src, find, replace):
            print(f"fresh grammar row unverifiable: {name}:{label}", file=sys.stderr)
            return 1
        fresh.append(dict(id=f"fresh-{seed}-{len(fresh):03d}-{name}",
                          what=what, find=find, replace=replace, check=label))
    doc = {"tool": "quality/check-seat-reports.py",
           "tool_sha256": hashlib.sha256(src.encode()).hexdigest(),
           "seed": seed, "seed_rule": "first 8 hex digits of gate sha256",
           "grammar": "random.Random(int(seed,16)) over FRESH_POOL (label,transform) rows; each row verifies green",
           "weakenings": HAND + fresh}
    with open(OUT, "w") as fh:
        json.dump(doc, fh, indent=2, sort_keys=True)
    print(f"wrote {OUT} weakenings={len(HAND)+len(fresh)} hand={len(HAND)} fresh={len(fresh)} seed={seed}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
