#!/usr/bin/env python3
"""Build .ufo/waves/round-76/w1-spec.json (one v1 wave, 13 seats)."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WAVE = os.path.join(LANE, ".ufo", "waves", "round-76")
REV = "cb713254ee9926e036e594312fdc61b57825526b"
BASE = "c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = GODSPEED + """
Round mado 76, ONE v1 wave (13 seats). Claims: C1 calibration (a successor counter scores the
landing harness's contract OUTCOME field, not only its `mz=` decision: 16 frozen fixture cases,
4 named outcome-rule mutations killed 4/4 where the held mz-only rule kills 0/4) and C2
operability (the guard census counts an interprocedural `del` in a callee and a dynamic-key
`del`: 59 frozen cases, 59/59 vs the held 55/59; population stays 20 readers / 13 guarded / 0
unguarded). The L1 holds the planner seat (the validator rejects `planner` as a swarm role); no
planner is dispatched.

Read FIRST:
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-76/claims-declaration-r76.md
(the frozen claims, predicates, counting commands, kill rules, targets, limits and the
routed-defect dispositions; base c3e0bc5f10b72964d54d18dc9b0706dc308dd1bf, freeze v2
cb713254ee9926e036e594312fdc61b57825526b; label set v3 sha 320f7e6b...).

Committed evidence (re-read, never rewrite):
- `.ufo/waves/round-76/control-baseline-r76.txt`: the pre-freeze do-nothing control (held
  mz-only rule kills 0/4; held round-75 classifier 55/59).
- `.ufo/waves/round-76/receipts/label-derivation-r76.txt`: every label re-derived from the
  harness's own SELFTEST/M-Z/M-R lines, never from the contract row.
- `.ufo/waves/round-76/measurement-c1-r76.txt` -> `MADO_R76_OUTCOME_FIELD: cases=16
  correct=16 mutants=4 killed=4 base_killed=0 verdict=TARGET_MET`, rc 0.
- `.ufo/waves/round-76/measurement-c2-r76.txt` -> `MADO_R76_GUARD_SHAPES: population=20
  readers=13 guarded=13 unguarded=0 controls=59/59 base_controls=55/59 verdict=TARGET_MET`,
  rc 0.

Hard bounds, every seat:
- Your ONLY write directory is /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-76/w1/<your name>/.
  Never edit a committed lane file (production instruments, corpus, SKILL.md, SCORECARD.md,
  LOG.md, README, SOURCES.md); draft only inside your own dir.
- Never run git/jj write commands anywhere (no add/commit/push/checkout/stash, no jj mutation);
  read-only git (`show`, `ls-tree`, `rev-parse`, `status`, `log`, `cat-file`) is fine. Never
  write the fleet repo, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`,
  `scripts/`, `templates/` or MANIFEST.json. Any fixture git repo is created under your scratch
  as `D=$(mktemp -d ...)` with `git -C "$D" init -q`, and `git -C "$D" rev-parse --show-toplevel`
  must equal `$D` before the first commit; never commit with a throwaway identity anywhere else.
- Never message `agent://all`; reply only to your L1 (`MadoR76`) or nothing.
- Scratch: /fast/scratch/hyaku/mado-r76/<your name>/ (create it; pass it explicitly; never use
  /tmp; delete it before you finish, after copying any receipt you cite into your own dir).
- Tooling authorization (operator, 2026-10-19): you may install or upgrade a tool that helps
  this task, first reading /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety
  gate) and recording tool/version/channel/reason in your report. ALL pacman transactions are
  PAUSED host-wide this run: install via `uv tool`/`npx`/an official binary in ~/.local/bin, or
  report that you needed one; never `pacman -Sy/-S/-Syu/-U/-R`, never restart a host service.
- Read-only host posture: do not probe the compositor, session, services, network services or
  ~/.config; no live-config writes; no credential material in any file.
- Every `Report:` trailer path the validator renders is relative to
  /home/vgpnk/Projects/shokunin/mado-shokunin - write it at
  /home/vgpnk/Projects/shokunin/mado-shokunin/<that path>. End your final output with one line
  `Report: <repo-relative path>` naming the file you actually wrote, then a 3-line summary.
"""


def prompt(name, role, body):
    return (GODSPEED + "\nYour name: %s (%s). Your only write directory: %s/w1/%s/. Scratch: "
            "/fast/scratch/hyaku/mado-r76/%s/.\n\n%s" % (name, role, WAVE, name, name, body))


ITEMS = [
    ("R76ScoutChain", "scout", r"""Report what the two successor instruments actually rest on.

1. Read `quality/counters/c1-r76-landing-controls.py` and `quality/counters/c1-r76-outcome-field.py`
   at """ + REV + """ (read-only `git show`) and report, with file:line anchors: where the challenge
   is drawn (and that the draw always contains an a-f letter), the witness grammar, the named
   `outcome_green` rule, how the contract row is assembled, how the four mutants are patched and
   why each anchor must occur exactly once, and every place the frozen round-72 harness still
   passes through unchanged.
2. Read `quality/counters/c2-r76-shapes.py` at the same revision and list the delta sites against
   `c2-r75-shapes.py` (`git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff """ + BASE + """ """ + REV + """ -- quality/counters/` is read-only and may help). Name the D3 (interprocedural) and D4
   (dynamic-key) code paths by line, and say which flows they are absent from.
3. Name every place the declaration's frozen sentence and the code disagree on target, predicate,
   denominator or kill rule - a disagreement is the finding, not a style note.
4. Write `findings.md`: claim | declaration sentence | code anchor | agree/disagree, plus what is
   NOT modelled so the round's declared limits stay honest."""),
    ("R76ScoutPopulation", "scout", r"""Re-derive the C2 population and audit the twelve new cases for runtime reachability.

1. Without using the lane gate, re-derive the census population at """ + REV + """: list
   `quality/check-*.py` (`git ls-tree -r --name-only <rev> -- quality`), count the files, count
   how many contain `GIT_NO_REPLACE_OBJECTS`, and report population / readers / guarded by reading
   the bytes. Compare with the committed receipt `.ufo/waves/round-76/measurement-c2-r76.txt`.
2. For each of the twelve round-76 cases in `.ufo/waves/round-76/controls/c2-cases-r76.json`
   (names starting `callee-` or `dynamic-key-`), report whether the source is runtime-reachable
   as written (a `del` on a key the mapping actually has, no NameError path, no dead branch as
   the only delete). Flag any fixture whose label pins a syntactic ordering rather than a
   reachable state - the round-75 M75-3 class.
3. Check the four positives for false-positive risk: does the new D3/D4 rule credit a mapping
   that is NOT the one launched (a copy, a rebinding after the call), or a callee that receives a
   different argument?
4. Write `population.md` and `reachability.md` in your dir."""),
    ("R76ExecC1", "executor", r"""Independently drive claim C1's frozen counting command and report what actually happens.

1. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r76-outcome-field.py
   --repo . --rev """ + REV + """ --base-rev """ + BASE + """ --controls
   .ufo/waves/round-76/controls/c1-outcome-cases-r76.json --scratch-root
   /fast/scratch/hyaku/mado-r76/R76ExecC1/run`. Save full stdout+stderr and the exit code; the
   last line must equal the declaration's contract sentence.
2. Drive the successor harness on the real lane once:
   `python3 -I quality/counters/c1-r76-landing-controls.py --repo . --rev """ + REV + """ --scratch-root <your scratch>/real`; record the `MADO_R76_*` evidence lines, the contract
   row and the exit code, and explain `selftest=`, `mz=`, `mr=`, `killed=`, `witness=`.
3. Run both selftests and record both tallies and exit codes.
4. Re-derive the outcome labels yourself for three cases (`right`, `always-red`,
   `green-absent`) from the harness's own `MADO_R76_SELFTEST` and `MADO_R76_MUTANT M-Z/M-R`
   lines only, and say whether they equal the frozen labels in
   `.ufo/waves/round-76/controls/c1-outcome-cases-r76.json`.
5. Report a table: command | rc | contract line | unexpected output. A dead or absent leg is the
   finding; never repair it - write the exact error text."""),
    ("R76ExecC2", "executor", r"""Independently drive claim C2's frozen counting command and hand-check its labels.

1. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r76-shapes.py
   --repo . --rev """ + REV + """ --base-rev """ + BASE + """ --controls
   .ufo/waves/round-76/controls/c2-cases-r76.json --scratch-root
   /fast/scratch/hyaku/mado-r76/R76ExecC2/run`. Save stdout+stderr and the exit code.
2. Hand-check the twelve new cases against the classifier directly: import the module (read-only)
   and call `has_guard(src)` on each; report every case whose measured `(reader, guard)` differs
   from the frozen expectation.
3. Build four of the twelve cases as *executable* fixtures in your scratch (a throwaway git repo
   per the context rule), run them with `python3 -c` and report whether the delete actually
   removes the key at runtime - the reachability the frozen set claims.
4. Report a table: command | rc | contract line | per-case disagreements. Never repair the
   instrument; write exact output."""),
    ("R76ExecGate", "executor", r"""Reproduce the round's no-harm and routed-defect evidence with exact tallies.

1. `bash tools/mado-verify.sh --selftest` (record the full tail and rc; the target is 460/460).
2. `python3 -I quality/check-index.py --repo . --rev """ + REV + """` (target 93/93 at base; the
   round's entries are not committed yet, so also run it at """ + BASE + """ and say both).
3. `python3 -I quality/check-tool-ledger.py --repo . --rev """ + REV + """` (base 133 rows, 0
   uncovered; the three new instruments are not yet in the ledger - report the uncovered count
   and name the three files).
4. `python3 -I quality/check-axis-scores.py --repo . --rev """ + REV + """` and
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`;
   record both rc and the line counts.
5. Verify the frozen instruments are byte-identical between """ + BASE + """ and """ + REV + """:
   `git rev-parse <rev>:<path>` for `tools/mado-verify.sh`, `quality/landing-counters.sh`,
   `quality/check-tool-ledger.py`, `quality/counters/c1-r75-*.py`, `c2-r75-shapes.py`.
6. Write `gate.txt` with command, rc and tail for each; a mismatch is the finding."""),
    ("R76ScribeEntries", "scribe", r"""Draft the two knowledge entries the round admits, grounded only in committed evidence.

1. Read the declaration, both measurement receipts, the label-derivation receipt and the two
   predecessor entries (`corpus/knowledge/harness-witness-credit-r75.md`,
   `corpus/knowledge/guard-carrier-copy-del-r75.md`).
2. Draft `entry-outcome-field.md`: what the contract outcome field is, why a counter must score
   it separately from `mz=`, the negative result (an echo-dropping outcome mutation is
   unobservable because the M-Z kill already requires the echo), the four observable mutations
   and their separators, the deterministic case-changing challenge, and the declared limits. Every
   factual claim cites a committed path:line or a receipt line.
3. Draft `entry-interprocedural-del.md`: D3 and D4, the twelve new cases with their labels, the
   negatives (dead branch, param rebinding, never called, after launch, other key, other
   constant, rebound name), and the limits (line order, simple call shape, env-named flows only).
4. Keep each entry under 200 lines, use tables, and mark inference `[INF]`. Write both files in
   your dir; the L1 integrates them."""),
    ("R76ScribeLesson", "scribe", r"""Draft the round-76 lesson skeleton and propose QUALITY criteria.

1. Read `corpus/lessons/round-75.md` (shape: Outcome, Mistakes with class/evidence/captured-by/fix,
   Gate) and `corpus/QUALITY.md` criteria 120-127.
2. Draft `lesson-skeleton.md` with: Outcome (both claims' measured receipts), Mistakes seeded from
   the round's own record - M76-1 (label set v1 modelled `verdict=` as summary-green only), M76-2
   (v2 kept an echo-dropping mutation the harness makes unobservable), M76-3 (the derivation
   regex required a trailing-field match and silently returned no lines) - each with class,
   evidence pointer, captured-by and a fix that can fail; and a Gate placeholder listing what the
   round must admit (at least one admit and one reject for the non-author closure).
3. Propose at most three QUALITY criteria: (a) a frozen separator must be reachable through the
   field that is scored; (b) a label derivation must read only the instrument's own evidence lines,
   never its contract row; (c) every quoted tally names an operative regex/regex-free command.
   Each criterion cites its lesson id and states the red state it catches.
4. Do not write into `corpus/`; draft in your dir."""),
    ("R76RevC1", "reviewer", r"""Attack claim C1's instrument, its labels and its evidence. Falsification, not approval.

1. Read `quality/counters/c1-r76-outcome-field.py` and `c1-r76-landing-controls.py` at """ + REV + """,
   the frozen declaration, the control set, the derivation receipt and the measurement receipt.
2. Try to make the counter wrong: (a) a mutant that changes `mz` AND the outcome - is it killed?
   is `base_killed` still 0? (b) a candidate harness that prints a second, later contract row - which
   row wins? (c) a case whose label makes the counter report TARGET_MET with a broken rule; (d)
   `--base-rev` a revision where the held counter is absent - what does the counter print?
3. Re-derive three labels independently of the counter from the harness's evidence lines.
4. Report every finding with severity (P1/P2/advisory), a reproducible snippet, and the exact
   expected/observed values. Do not repair anything."""),
    ("R76RevC2", "reviewer", r"""Attack claim C2's classifier and its twelve new cases. Falsification, not approval.

1. Read `quality/counters/c2-r76-shapes.py` at """ + REV + """ (D3/D4 paths), the frozen control set
   and the measurement receipt.
2. Write adversarial fixtures in your scratch that SHOULD be guarded but the new rules may cancel:
   (a) a callee that deletes the key from a *copy* then the caller launches the original; (b) a
   callee called with a different mapping than the one launched; (c) a `del env[k]` where `k` is
   bound once to the key but the delete is inside a dead branch; (d) a callee defined in a nested
   scope or called through an attribute; (e) a dynamic key bound once but shadowed by a parameter.
   Report the classifier's verdict and whether it is the right verdict.
3. Check the four positives cannot be satisfied by a classifier that ignores the delete (i.e. the
   labels really require the new rule).
4. Report findings with severity, snippet and expected/observed. Do not repair."""),
    ("R76Critic", "critic", r"""Falsify the round's claim *framing*, not only its code.

1. Read the declaration, the base SCORECARD's `Planned (round 76)` list, both control sets, the
   pre-freeze control receipt and both measurement receipts.
2. Answer with evidence: (a) does `killed=4/4` actually discriminate, or would a trivially wrong
   counter also reach it? (b) is `base_killed=0` structural boilerplate (the mutants only touch
   the outcome helper) rather than a control? (c) does the label derivation depend on the
   candidate's contract row anywhere? (d) is the negative result ("echo-dropping mutation
   unobservable") true for every reachable fixture, or is there a counterexample shape? (e) is
   C2's `base_controls=55/59` a real do-nothing control or a construction of the new cases?
   (f) does either claim satisfy §9's "a do-nothing control cannot reach it"?
3. Name what the round does NOT certify, in the terms a closure would use.
4. Write `critic.md`: question | verdict | evidence | what would change the verdict."""),
    ("R76Mutant", "mutation-tester", r"""Mutation-test the two new rule branches against the frozen sets.

1. Copy the committed counters to your scratch (read-only `git show`), then apply your OWN
   mutations beyond the four frozen ones: (a) `outcome_green` returning a constant; (b) the
   witness grammar narrowed back to 16; (c) `last_witness` scanning forward; (d) D3 matching any
   positional argument regardless of the callee's parameter; (e) D4 resolving a name bound twice.
   For each: does the frozen case set catch it (score < target)? Record score and the separating
   case names.
2. Report survivors: a mutation that still reaches the target is a named gap, not a failure to
   hide.
3. Do not edit the committed instruments; run mutated copies from your scratch."""),
    ("R76Conn", "connector", r"""Cross-link the round's new ground to what the lane and its siblings hold.

1. Read `corpus/README.md`'s index rows and `corpus/SOURCES.md` for the round-75 rows S450-S454,
   plus the lane's two predecessor entries. Name the exact rows each new entry should cite and
   whether a `used-by` cell must be extended (CORPUS rule 2, old -> new).
2. Sweep siblings read-only for overlap: grep `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/knowledge`
   (and `quality/counters`) for `outcome field`, `witness`, `GIT_NO_REPLACE_OBJECTS`,
   `del env[`, `interprocedural`. Report any sibling that already holds this ground, with paths.
3. Produce the provenance crosswalk the round-75 plan asked for: for each of the two claims,
   generation | receipt | evidence mode (re-executed vs evidence-verified) | remaining limit.
4. Write `crosswalk.md` and `siblings.md`. Never write outside your dir."""),
    ("R76Sentinel", "sentinel", r"""Adversarial security and hygiene review of the round's artifacts.

1. Scratch discipline: inspect the counter sources for hardcoded `/tmp` roots, symlink following,
   `mkdtemp` before a validated root, and any write outside `--scratch-root`; report file:line.
2. Secret and privacy: grep the round's committed receipts and instruments for anything that could
   be credential or session material (`token`, `secret`, `password`, `BEARER`, `ss -`, `journalctl`,
   process tables); report matches with paths. The challenge value must never be printed by the
   harness - verify `describe_env` redacts it and that the contract row carries no value.
3. Child environment: read `child_env`/`git_env` in both counters and say whether `BASH_ENV`,
   `LD_PRELOAD`, `PYTHONPATH` or a caller-provided `MADO_LANDING_NONCE` can influence a fixture.
4. Fixture safety: does any counter or fixture write outside its scratch, commit with a throwaway
   identity elsewhere, or spawn `bash` with an inherited environment?
5. Report findings with severity (P1/P2/advisory) and the exact mitigating line."""),
]


def main():
    items = []
    for name, role, body in ITEMS:
        items.append({"name": name, "role": role, "prompt": prompt(name, role, body)})
    spec = {"wave": "w1", "reportDir": ".ufo/waves/round-76/w1", "context": CONTEXT,
            "items": items}
    path = os.path.join(WAVE, "w1-spec.json")
    with open(path, "w") as fh:
        json.dump(spec, fh, indent=1)
    print(path, len(items))


if __name__ == "__main__":
    main()
