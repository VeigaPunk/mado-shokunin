# ScrConsiderthese — considerthese mining (status: done)

Seat: mine ONE still-unimplemented proposal of `considerthese/2026-10-25.md` (item 10), ground it
through the lane's bar, and draft its landing form. Lane
`/home/vgpnk/Projects/shokunin/mado-shokunin`, freeze
`60c3914154333180450d5da27ba222d5763cc56a`, base
`ab2bfaab661c846d1de9d58c01651cd156a13949`.

**Result.** Proposal 5 ("Verify one fact first-hand per day, read-only") is chosen, re-derived, and
drafted as `QUALITY.md` criterion 69 plus a round-41 `## considerthese` note and an optional
`## Mistakes` entry. Re-deriving its own mined sentence found one number wrong: the reflection says
`corpus/knowledge/` "gained eight entries" over rounds 32-37; the lane's bytes say nine.

## Artifacts (all inside the seat directory; no tracked file edited)

| path | what |
|---|---|
| `.ufo/waves/round-41/w1/ScrConsiderthese/proposal.md` | chosen proposal, why, evidence, exact landing text (sections A-C), reproduction block |
| `.ufo/waves/round-41/w1/ScrConsiderthese/receipts.txt` | every re-derivation command and its observed output, `rc=0` each |
| `.ufo/waves/round-41/w1/ScrConsiderthese/verify-quotes.py` | quote verifier: <=25 words, located, in the source line, in this seat's artifacts |
| `.ufo/waves/round-41/w1/ScrConsiderthese/quotes-receipt.txt` | its output, `MADO_QUOTES: passed=12/12` |

## Behavior

1. Read `considerthese/2026-10-25.md` (proposals 1-6) and the earlier files' proposals; grepped
   `corpus/QUALITY.md`, `SKILL.md`, `PROVINCE.md`, `corpus/lessons/`, `tools/`, `quality/` for each
   proposal's implementation at the freeze.
2. Chose the one open, lane-actionable, command-checkable proposal: **5**.
3. Re-derived every number in the sentence the mining would repeat, from named revisions (read-only
   `git log`/`show`/`ls-tree`/`diff`; no worktree observable, so no criterion-63 witness needed).
4. Drafted the landing text for the L1. A leaf may not edit `corpus/QUALITY.md` or the lesson, so
   nothing is landed.

## Status of the six proposals at base `ab2bfaa` (evidence in `proposal.md`)

| # | Status | Evidence |
|---|---|---|
| 1 | already a criterion (re-mining duplicates): "Every round report states the lane's last-30-commit domain-versus-meta ratio with its command" | `corpus/QUALITY.md:367` (criterion 60) |
| 2 | mined round 40 as a table: "Count dead attempts and dirty closures from the watchdog digests" | `corpus/lessons/round-40.md:146` |
| 3 | served round 39: "(watch M37-5 by name) is served by C1's re-registration" | `corpus/lessons/round-39.md:82`; `corpus/lessons/round-38.md:4` |
| 4 | open but not lane-actionable (a timer and `debug:disable_logs = 0` are host/operator actions) | no trace: `grep -ni 'enabling logs\|log volume\|cost of enabling'` over lessons 37-40, `QUALITY.md`, `SKILL.md` is empty |
| 5 | **open — chosen** | `QUALITY.md` at base: 68 criteria, the only `considerthese` line is criterion 60 (`grep -n considerthese` -> `367:`); `grep -ni 'relay\|first-hand'` empty; `SKILL.md`/`PROVINCE.md` zero; only trace is prose at `corpus/lessons/round-33.md:28` |
| 6 | operator-owned (the reflection's own window) and self-applied in that file | `considerthese/2026-10-25.md:7` "What landed after the last reflection" |

## Gates run by this seat

- Re-derivation receipt: `receipts.txt`, 17 commands, all `rc=0`.
- Quote verifier: `python3 -I .ufo/waves/round-41/w1/ScrConsiderthese/verify-quotes.py` ->
  `MADO_QUOTES: passed=12/12`, exit 0 (`quotes-receipt.txt`).
- No counter, no selftest, no gate of the lane was run: this seat produces a draft, not a claim.

## Findings

**F1 — the mined sentence's entry count is relayed and wrong.** `considerthese/2026-10-25.md:5`
states "In this window `corpus/knowledge/` gained eight entries" (repeated as "8 knowledge entries" in
its carried-items table). First-hand: `git ls-tree -r --name-only 57a772b corpus/knowledge | wc -l`
-> `43`, same at `f6e3247` -> `52`; `git diff -M --name-status 57a772b..f6e3247 -- corpus/knowledge |
grep -c '^A'` -> `9`, `'^D'` -> `0`. By round: 32 (`f591087`) 3, 34 (`fa7ba11`) 1, 35 (`02088b4`) 3,
37 (`3f42425`) 2. The window's other numbers reproduce exactly (68 commits at `:3`; SOURCES
`185` -> `207` and one tool, `tools/mado-eventq.py`, at `:5`; 22 rows added). The number the reflection
says it read first-hand is right; the adjacent relayed one is wrong — the proposal's own case.

**F2 — criterion 60 is unapplied in rounds 37-40.** `grep -rn 'last-30\|domain-versus-meta'
corpus/lessons/round-3[7-9].md corpus/lessons/round-40.md LOG.md` returns only the round-36 lines
(`LOG.md:2222`, `corpus/lessons/round-36.md:219`); no round-37..40 record states the ratio criterion 60
requires. Reported as an observation for the round-41 verifier; not re-mined here.

**F3 — the round-40 lesson's closure sentence overstates.** `corpus/lessons/round-40.md:166` says
"the proposals 1 and 3-6 of the same file stay open"; proposal 3 was served in round 39
(`corpus/lessons/round-39.md:82`) and proposal 1 already has criterion 60. Only 4, 5 and 6 were open,
and 6 is operator-owned. This is itself a relayed status claim, the class F1 belongs to.

## Quotes lifted (all verified by `verify-quotes.py`: <=25 words, located, in the source line, in these artifacts)

| # | quote | location |
|---|---|---|
| 1 | In this window `corpus/knowledge/` gained eight entries | `considerthese/2026-10-25.md:5` |
| 2 | everything else is relayed from spot-checks | `considerthese/2026-10-25.md:50` |
| 3 | I could pick one cited source line each day and re-open it. | `considerthese/2026-10-25.md:50` |
| 4 | What landed after the last reflection | `considerthese/2026-10-25.md:7` |
| 5 | proposal 5 (verify one cited fact first-hand) was | `corpus/lessons/round-33.md:28` |
| 6 | Count dead attempts and dirty closures from the watchdog digests | `corpus/lessons/round-40.md:146` |
| 7 | is served by C1's re-registration | `corpus/lessons/round-39.md:82` |
| 8 | v3 re-grounding counter discriminating the round-37 v2 cribs | `corpus/lessons/round-38.md:4` |
| 9 | Every round report states the lane's last-30-commit domain-versus-meta ratio with its command | `corpus/QUALITY.md:367` |
| 10 | TARGET MET on junk | `corpus/lessons/round-32-verifier-spotcheck.md:35` |
| 11 | the proposals 1 and 3-6 of the same file stay open | `corpus/lessons/round-40.md:166` |
| 12 | 8 knowledge entries | `considerthese/2026-10-25.md:38` |

## Out of scope / not done

- Not landed: `corpus/QUALITY.md` criterion 69, the `## considerthese` note, the `## Mistakes` entry
  (leaf write scope; text is in `proposal.md` sections A-C for the L1).
- Proposal 4 refused as a mining target: its two halves are an operator ask (a schedule) and a host
  config change (`debug:disable_logs = 0`), both outside this lane's write scope and the wave's
  host-safety rules. It remains open and is not counted as served.
- No host command beyond read-only `git`/`grep`: no journal read, no compositor or socket access, no
  package transaction.
- No tool installed or updated; the lane's `git` and `grep` sufficed.

## Limits

- Only the mined sentence was re-derived. The reflection's spot-check-derived numbers stay relayed
  here by construction (e.g. the round-32 junk-control verdict is carried by
  `corpus/lessons/round-32-verifier-spotcheck.md:35`).
- The proposed criterion is prose with a reader-run command, not a counter: it can require a
  `relayed:` label, it cannot prove the label honest. That residual is stated in `proposal.md`.
- Whether the L1 lands it as 69 depends on the round-41 mistake numbering (`M41-n` placeholder).
