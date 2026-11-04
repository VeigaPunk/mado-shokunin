#!/usr/bin/env python3
"""Build .ufo/waves/round-75/w1-spec.json (one v1 wave, 13 seats)."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
WAVE = os.path.join(LANE, ".ufo", "waves", "round-75")
REV = "def73656c94f0e88bd671cfb4a65124338261722"
BASE = "b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6"

GODSPEED = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = GODSPEED + """
Round mado 75, ONE v1 wave (13 seats). Claims: C1 calibration (the successor landing harness
credits the M-Z kill and greens the outcome only on the run's own echo of a per-run challenge;
the held round-72 harness credits 6/11 frozen fixture modes) and C2 operability (the guard census
counts key-carrying copies bound to any name and treats `del env[KEY]` as a cancellation; the
held round-74 classifier misses six of forty-seven frozen cases). The L1 holds the planner seat
(the validator rejects `planner` as a swarm role); no planner is dispatched.

Read FIRST:
/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-75/claims-declaration-r75.md
(the frozen claims, predicates, counting commands, kill rules, targets, limits; base
b149d2ece1a6d75f5738aa8bf4a9493f1a9c7da6, freeze+instruments
def73656c94f0e88bd671cfb4a65124338261722).

Committed receipts (re-read, never rewrite):
- `.ufo/waves/round-75/control-baseline-r75.txt` (held legs: C1 6/11, C2 41/47).
- `.ufo/waves/round-75/measurement-c1-r75.txt` -> `MADO_R75_HARNESS_WITNESS: cases=11
  correct=11 base_correct=6 verdict=TARGET_MET`, rc 0.
- `.ufo/waves/round-75/measurement-c2-r75.txt` -> `MADO_R75_GUARD_SHAPES: population=20
  readers=13 guarded=13 unguarded=0 controls=47/47 base_controls=41/47 verdict=TARGET_MET`, rc 0.

Hard bounds, every seat:
- Your ONLY write directory is /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-75/w1/<your name>/.
  Never edit a committed lane file (production instruments, corpus, SKILL.md, SCORECARD.md,
  LOG.md, README, SOURCES.md); draft only inside your own dir.
- Never run git/jj write commands anywhere (no add/commit/push/checkout/stash, no jj mutation);
  read-only git (`show`, `ls-tree`, `rev-parse`, `status`, `log`, `cat-file`) is fine. Never write
  the fleet repo, a sibling lane, `.ufo/state/`, `.ufo/watchdog.log`, `.scratch/`, `scripts/`,
  `templates/` or MANIFEST.json. Any fixture git repo is created under your scratch as
  `D=$(mktemp -d ...)` with `git -C "$D" init -q`, and `git -C "$D" rev-parse --show-toplevel`
  must equal `$D` before the first commit; never commit with a throwaway identity anywhere else.
- Never message `agent://all`; reply only to your L1 (`MadoR75`) or nothing.
- Scratch: /fast/scratch/hyaku/mado-r75/<your name>/ (create it; pass it explicitly; never use
  /tmp; delete it before you finish, after copying any receipt you cite into your own dir).
- Tooling authorization (operator, 2026-10-19): you may install or upgrade a tool that helps this
  task, first reading /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate) and
  recording tool/version/channel/reason in your report. ALL pacman transactions are PAUSED
  host-wide this run: install via `uv tool`/`npx`/an official binary in ~/.local/bin, or report
  that you needed one; never `pacman -Sy/-S/-Syu/-U/-R`, never restart a host service.
- Read-only host posture: do not probe the compositor, session, services, network services or
  ~/.config; no live-config writes; no credential material in any file.
- Every `Report:` trailer path the validator renders is relative to
  /home/vgpnk/Projects/shokunin/mado-shokunin - write it at
  /home/vgpnk/Projects/shokunin/mado-shokunin/<that path>. End your final output with one line
  `Report: <repo-relative path>` naming the file you actually wrote, then a 3-line summary.
"""


def prompt(name, body):
    return (GODSPEED + "\nYour name: %s. Your only write directory: %s/w1/%s/. Scratch: "
            "/fast/scratch/hyaku/mado-r75/%s/.\n\n%s" % (name, WAVE, name, name, body))


ITEMS = [
    ("R75ScoutChain", "scout", r"""Read the chain and report what the round's instruments actually rest on.

1. Read `quality/counters/c1-r75-landing-controls.py`, `quality/counters/c1-r75-harness-witness.py`
   and `quality/landing-counters.sh` (the round-75 generation) and report: where the challenge is
   drawn, how it reaches the child, where the echo is parsed, and every place the frozen round-72
   harness's behaviour still passes through unchanged. Cite file:line for each.
2. Read `quality/counters/c2-r75-shapes.py` and report the exact delta sites against
   `c2-r74-shapes.py` (`git -C /home/vgpnk/Projects/shokunin/mado-shokunin diff """ + BASE + """ """ + REV + """ -- quality/counters/` is read-only and may help). Name the two new rule
   branches by line.
3. Report any line where the declaration's frozen sentence and the code disagree (target,
   predicate, denominator, kill rule) - a disagreement is the finding, not a style note.
4. Write `findings.md` in your dir: claim | declaration sentence | code anchor | agree/disagree,
   plus what is NOT modelled (so the round's declared limits stay honest)."""),
    ("R75ScoutSources", "scout", r"""Open the two sources the round's C2 claim rests on, three fetches each.

1. CPython v3.14.8 `Doc/reference/simple_stmts.rst` from
   `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/reference/simple_stmts.rst`
   (the `del` statement section). Fetch three times into your scratch, prove byte-identity
   (`sha256sum`), record byte length and digest, and locate the sentence that says deletion of a
   subscription is passed to the primary object. Quote <=25 words with line numbers (markup
   stripped) and count words with `python3 -c 'print(len(q.split()))'`.
2. CPython v3.14.8 `Doc/library/stdtypes.rst` from
   `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/stdtypes.rst` (the
   `dict(mapping, **kwargs)` paragraph). Same three-fetch proof and a <=25-word located quote.
3. Report both digests, lengths, line spans and word counts in `sources.md`, plus one sentence
   each on why it grounds the C2 branch (`del env[KEY]`; `dict(env, KEY="1")`). Grep
   `corpus/SOURCES.md` for the same two URLs and name any existing row before the L1 appends."""),
    ("R75ExecC1", "executor", r"""Independently drive claim C1's frozen counting command and report what actually happens.

1. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r75-harness-witness.py
   --repo . --rev """ + REV + """ --base-rev """ + BASE + """ --controls
   .ufo/waves/round-75/controls/c1-harness-cases-r75.json --scratch-root
   /fast/scratch/hyaku/mado-r75/R75ExecC1/run`. Save full stdout+stderr and the exit code in your
   dir; the last line must match the declaration's contract sentence.
2. Drive the successor harness on the real lane once:
   `python3 -I quality/counters/c1-r75-landing-controls.py --repo . --rev """ + REV + """ --scratch-root <your scratch>/real`; record the `MADO_R75_*` evidence lines, the contract
   line and the exit code, and explain what `selftest=`, `mz=`, `mr=` and `witness=` report.
3. Run the successor harness `--selftest` and record its tally and exit code.
4. Report a table: command | rc | contract line | unexpected output. A dead or absent leg is the
   finding; never repair it - write the exact error text."""),
    ("R75ExecC2", "executor", r"""Independently drive claim C2's frozen counting command and hand-check its labels.

1. `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r75-shapes.py
   --repo . --rev """ + REV + """ --base-rev """ + BASE + """ --controls
   .ufo/waves/round-75/controls/c2-cases-r75.json --scratch-root
   /fast/scratch/hyaku/mado-r75/R75ExecC2/run`. Save full stdout+stderr and the exit code; quote
   the contract line and the per-reader census.
2. Run `--selftest` with and without `--controls` and record both tallies.
3. Hand-check the eleven appended cases named `copy-*` and `del-*`: for each, state in one line why
   the label is right or wrong (does the child genuinely receive the guard key? does the delete
   genuinely remove it?). Flag any case whose source does not match its label; never edit the
   frozen file.
4. Prove the frozen carry: compare the first 36 cases of the r75 controls with
   `.ufo/waves/round-74/controls/c2-cases-r74.json` (name/src/labels) and report the mismatch
   count."""),
    ("R75ExecGate", "executor", r"""Reproduce the round's no-harm and routed-defect evidence with exact tallies.

1. `bash tools/mado-verify.sh --selftest` in the lane: record the `MADO_SELFTEST` line and rc;
   confirm the gate blob is byte-identical at `""" + BASE + """` and `""" + REV + """`
   (`git rev-parse <rev>:tools/mado-verify.sh`).
2. `python3 -I quality/counters/c1-r74-witness-rule.py --selftest --scratch-root <scratch>/r74`:
   record the tally; confirm `SKILL.md` and `LOG.md` say 21/21 while the rule prints 23/23 (the
   round-74 closure D1).
3. `python3 -I quality/counters/c2-r74-shapes.py --selftest --controls
   .ufo/waves/round-74/controls/c2-cases-r74.json --scratch-root <scratch>/r74c2` and the r75
   form with its controls; record both tallies.
4. Routed `/tmp` scratch at `tools/mado-verify.sh:418`: quote the exact line and prove the
   red-before state by running the gate selftest with `TMPDIR=<your scratch>/tmp` and reporting
   where the scratch tree is actually created (`find` both). Never edit the gate.
5. Report every tally with its command and rc; a mismatch between a closure's claimed number and
   the observed one is the finding."""),
    ("R75ScribeEntries", "scribe", r"""Draft the two knowledge entries the round admits, grounded only in committed evidence.

1. Read the declaration, both measurement receipts, the two new counters and the two harnesses.
   Read two existing entries as the shape bar: `corpus/knowledge/replay-witness-credit-r74.md` and
   `corpus/knowledge/guard-carrier-twohop-environ-alias-r74.md`.
2. Draft `corpus/knowledge/harness-witness-credit-r75.md` (C1): the successor harness's rule, the
   eleven frozen modes and the separation (11/11 vs 6/11), what the challenge authenticates and
   what it does not, and the declared limits. Cite the measurement receipt and the freeze commit;
   leave the S-row citation to the L1 (the sources scout's `sources.md` names them).
3. Draft `corpus/knowledge/guard-carrier-copy-del-r75.md` (C2): the two rule deltas, the eleven
   appended cases grouped by shape, the population 20/13/13/0 and the controls 47/47 vs 41/47,
   and the limits (line order, literal key, one scope).
4. Both drafts open with `source:`, `verified-at:` and `recheck:` lines in the house shape; keep
   each claim falsifiable and quote only committed numbers. Write `entry-c1.md` and `entry-c2.md`
   in your own dir; never write `corpus/`."""),
    ("R75ScribeLesson", "scribe", r"""Draft the round-75 lesson skeleton the L1 will finish.

1. Read `corpus/lessons/round-74.md` (shape and tone) and the round-74 closure's routed defects
   (`corpus/lessons/round-74-verifier-spotcheck.md` §6).
2. Draft `lesson-r75.md` with: header (author/date/base/frozen declaration/controls digests/
   measured content), `## Outcome and boundaries` (both claims with their contract lines), a
   `## Mistakes` table whose evidence cells are marked `<L1>` for rows (a) the stale 21/21 tally
   that survived a round (D1), (b) the unlanded post-repair selftest receipts (D2), (c) the S446
   quote count 23 vs 21 (D3), (d) the declaration's stale seat count (D4), (e) the pre-freeze
   plumbing-run disclosure, (f) any defect your own read finds.
3. Draft `## Gate` with the two source URLs, the fetch/quote duties for S453/S454 (the sources
   scout's `sources.md` carries the numbers), one candidate reject stanza, and the spot-check
   handover sentence (the round's seats are the lane's own; the closure spot-checks).
4. Write `lesson-r75.md` in your dir; never write `corpus/lessons/`."""),
    ("R75RevC1", "reviewer", r"""Attack claim C1's instrument and its evidence. Falsification, not approval.

1. Read `quality/counters/c1-r75-landing-controls.py` and
   `quality/counters/c1-r75-harness-witness.py` line by line against the declaration's C1
   sentence. Hunt for: credit granted without the echo; a genuine run refused; the pin's scope
   (what it does and does not freeze); whether `witness=` can lie; whether the contract line's
   verdict can disagree with the kill decision; whether the child env really strips the ambient
   `MADO_LANDING_NONCE`.
2. Drive the frozen counter once yourself (command in the declaration) and compare its per-case
   table with the mode labels: name any case whose label the fixture source does not justify.
3. Mutate nothing in the lane; run probes on copies under your scratch. Record every hypothesis
   with the command and its output.
4. Write `review.md`: findings P1/P2/advisory with file:line and the exact observation; end with
   a one-line verdict `C1: falsified | survives with defects | survives`."""),
    ("R75RevC2", "reviewer", r"""Attack claim C2's classifier. Falsification, not approval.

1. Read `quality/counters/c2-r75-shapes.py` (the two delta branches and the dominance loops) and
   the frozen forty-seven cases. Hunt for: a label the successor gets right by accident; an idiom
   the any-name rule now over-credits (the declaration says a mapping handed as `env=` counts -
   check `usage_lines` for non-env names handed positionally); a `del` that cancels the wrong store
   (dead branches, other scopes, rebinding order); a case where held and successor agree but the
   label is wrong.
2. Drive the frozen counter once yourself and read the per-case legs; independently re-derive two
   negatives and two positives with `python3` importing the committed counter (`git show
   """ + REV + """:quality/counters/c2-r75-shapes.py` into your scratch).
3. Verify the population claim: enumerate `quality/check-*.py` at the freeze rev yourself and
   re-run the reader/guard classification; report any file the counter inspects differently.
4. Write `review.md`: P1/P2/advisory, file:line, exact observation, and one-line verdict
   `C2: falsified | survives with defects | survives`."""),
    ("R75Critic", "critic", r"""Falsify the round's claim *framing*, not only its code.

1. Read the declaration, the base SCORECARD's `Planned (round 75)` list and the round-74 lesson's
   declared limits. Answer with evidence pointers: (a) is C1 a new finite denominator or a
   re-scoring of the round-74 rule on new inputs? (b) does C1's denominator (eleven fixture modes)
   exercise the harness's own decision, or only the rule inside it? (c) is C2's forty-seven-case
   set a new carrier class or padding? (d) can a do-nothing control reach either target (the
   baseline receipt says 6/11 and 41/47 - re-derive the numbers)? (e) does any claim use a
   universal clause its counter does not enumerate?
2. Check the lowest-axis obligation and the stagnation-nudge statement against `SCORECARD.md`'s
   axis table at the base rev - is "no axis is distinctly lowest" re-derivable?
3. Check the no-harm obligations: does the instrument amendment change any held caller's output
   when `MADO_LANDING_NONCE` is absent? (`git diff """ + BASE + """ """ + REV + """ -- quality/landing-counters.sh`,
   then run the landing instrument's `--selftest` on the new generation and record the tally.)
4. Write `critique.md`: one verdict per question (a)-(e) with exact evidence, and every claim
   sentence that overreaches its counter."""),
    ("R75Mutant", "mutation-tester", r"""Mutation-test the two new rule branches against the frozen sets.

1. Copy the committed counters (`git show """ + REV + """:<path>`) into your scratch; never edit the
   lane.
2. C1 mutants, each applied exactly once to the copy: (M1) drop the witness term from `credit`;
   (M2) drop the witness term from the outcome/contract verdict; (M3) accept a witness prefix
   instead of a byte-exact match; (M4) accept the FIRST parsed witness instead of the last. For
   each, run the C1 counter against a scratch fixture carrying the mutant harness at a scratch
   commit and report which frozen cases separate it (name the flips).
3. C2 mutants: (M1) drop the `del` cancellation; (M2) restore the env-named restriction on guard
   constructions; (M3) drop the rebinding branch for non-env names; (M4) treat a `del` of any key
   as a cancellation. Report each mutant's control score against 47/47.
4. Report a table mutant | recipe | controls | killed(yes/no) | the case(s) that separated it.
   Any mutant the frozen sets do NOT separate is a finding: name the missing negative."""),
    ("R75Conn", "connector", r"""Cross-link the round's new ground to what the lane already holds.

1. Read `corpus/README.md`'s index rows for the round-72..74 instrument entries and the two new
   drafts the scribe writes (if present). List every existing knowledge entry that makes a claim
   the round's two new entries will touch: the witness rule (r74), the carrier grammar (r70-r74),
   the landing harness (r68-r72).
2. For each overlap say whether the new entry *extends* (no edit needed), *supersedes* (a new
   row/entry is owed), or *contradicts* (a defect to name). Name the exact heading/row.
3. Scan `.ufo/waves/round-75/` for instruments or receipts that no claim or report section will
   cite (orphans) and name them.
4. Check `considerthese/` for one still-unimplemented proposal that fits this round's claims or
   the next round's ground: quote the proposal line, its file and date; say implemented/not and
   why it does or does not fit. Never edit it.
5. Write `crosslinks.md` with the three lists and the proposal line."""),
    ("R75Sentinel", "sentinel", r"""Adversarial security and hygiene review of the round's artifacts.

1. Scratch discipline: inspect the three new instruments for hardcoded `/tmp`, `mkdtemp(dir=...)`
   defaults, unvalidated scratch, symlink following, and writes outside the declared scratch. The
   round-75 hard rule is that a committed tool must honour `TMPDIR`/an explicit scratch argument.
   Check `tools/mado-verify.sh:418` (the carried defect) and whether the round's amendment adds
   any new scratch surface.
2. Secret material: does any new instrument or receipt print or persist a challenge, a token, an
   environment value beyond the fixed witness? Look at `MADO_R75_CHALLENGE` (does it print the
   nonce?), the child env allowlist, and the fixture receipts. The credential-material bar: secret
   values, session tokens, cookies, `op://` refs never appear.
3. Process hygiene: fixture git repos must be created under scratch with `-C "$D"` and a verified
   toplevel; no throwaway-identity commit may be reachable in the lane or the fleet repo. Prove
   the lane's git log has no `t <t@t>`-style author from this round
   (`git -C /home/vgpnk/Projects/shokunin/mado-shokunin log --format='%an <%ae> %s'`).
4. The harness's import mechanism: can a fixture repo plant a hostile `c1-r72-landing-controls.py`
   and have the wrapper execute it? The pin answers it - verify the pin check runs BEFORE the load
   and that the pin value matches the committed generation.
5. Write `sentinel.md`: findings P1/P2/advisory with exact paths/commands, plus the three checks
   you could not run and why."""),
]

SPEC = {
    "wave": "w1",
    "reportDir": ".ufo/waves/round-75/w1",
    "context": CONTEXT,
    "items": [{"name": n, "role": r, "prompt": prompt(n, body)} for n, r, body in ITEMS],
}

if __name__ == "__main__":
    os.makedirs(WAVE, exist_ok=True)
    with open(os.path.join(WAVE, "w1-spec.json"), "w", encoding="utf-8") as fh:
        json.dump(SPEC, fh, indent=1)
        fh.write("\n")
    roles = {}
    for item in SPEC["items"]:
        roles[item["role"]] = roles.get(item["role"], 0) + 1
    print(json.dumps({"items": len(SPEC["items"]), "roles": roles}, sort_keys=True))
