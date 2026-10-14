# WWKD plan — mado round 10 (ufo-round-plan-v1)

Design lane: PREP-M10 (2026-10-14; round-9 32-lane wave, width 32; mado
round-9 work in flight). Everything below was read at design time by this
lane — freeze 2026-10-14T20:04Z — not taken from a record; every pin is
re-measured at dispatch. Where this draft and the landed round-9 artifacts
disagree, the landed bytes are the authority. **Final-round frame:** this
is the arc's last plan — the round it plans is the tenth, and its charter
is the ten-round synthesis and the gate's standing-use note; no round-11
plan follows from this lane. Round-9 clauses (a9) theme plane as gate rows
/ (b9) walker live rows / (c9) census closure + receipts are this plan's
precondition set, checked at dispatch from the round-9 record, never
assumed; a clause that did not land is a finding the synthesis records —
round 10 does not re-attempt it.

Design-time state (measured, read-only; re-measure at dispatch):
- HEAD `12c8f08a35537b7d53b8e0252459dec16e550079` ("probation round 8
  (training r7): see LOG", commit 16:55:09 −03:00 = 19:55:09Z). The arc:
  mint `74d3b7b`; rounds 1–8 `65a2254` / `e1e1bb7` / `f9f58c0` /
  `3d9ba45` / `eead56b` / `c8f6667` / `0c20a76` / `12c8f08`. `git status
  --porcelain` at freeze reads the round-9 in-flight set below, not empty.
- Gate `tools/mado-verify.sh` **committed** revision sha256
  `7da4ec5013583c91942538986b05e7243b3edeb8e3dd37b54f6b65a9225f2f4f`,
  2,887 L / 131,612 B, mtime 16:29:03 −03:00 — the revision every number
  below was executed against (logs `/tmp/w9-prepm10/`): `--selftest` →
  `MADO_SELFTEST: 217/217 assertions passed`, rc 0; `--no-live` →
  `MADO_VERIFY: CLEAN (20 pass, 3 notes)`, `counts: pass=20 fail=0
  unknown=0 skip=8 note=3`; live → `MADO_VERIFY: CLEAN (43 pass, 7 notes)`,
  `counts: pass=43 fail=0 unknown=0 skip=0 note=7`; boundary
  `bb2639d9a980…` in both verdict runs; `--regression` → `MADO_REGRESSION:
  PASS (case=mado-verify-hardened; target=d2bcdb31daea5d68…db62)`, rc 0 in
  32.0 s, `match=10/10`, flips 0, control GREEN, `MUTATE_RESTORE: OK`; the
  gate sha was identical before and after every run.
- Gate census at the committed revision [OBS]: 162 `row` + 6 `row_from_rc`
  sites; per-plane over all sites omarchy 56 / hypr-live 57 / hypr 23 /
  waybar 17 / terms 10 / gate 3 / walker 2; 51 distinct row ids / 7 plane
  ids (omarchy 11 · hypr-live 21 · hypr 9 · waybar 4 · terms 4 · walker 1 ·
  gate 1); the selftest helper plane regexes carry seven ids at `:357`,
  `:361`, `:376-380`; theme rows 0 (`live.theme.current` NOTE only);
  walker live = `live.walker.version` + `live.walker.services`. The suite
  asserts 22 of 51 row ids at the round-8 append (all 11 new ones
  `omarchy.*`) — re-count at dispatch.
- Gate ladder [OBS, re-derivable; this lane's freeze re-derivation proved
  the method]: `git show <commit>:tools/mado-verify.sh` → round 5
  `eead56b` `d7edaab4bf108625…` / 1,098 L; round 6 `c8f6667`
  `c4c1afb75dd1c8aa…` / 1,186 L; round 7 `0c20a76` `90d50cdd4d18410b…` /
  1,755 L; round 8 `12c8f08` `7da4ec5013583c91…` / 2,887 L. Kill ladder:
  the round-5 revision 4/10 (40 %) → `c4c1afb7…` 10/10 → `90d50cdd…` 10/10
  → `7da4ec50…` 10/10 (AUD-M8 C1/C3, VER-M8 erratum — plus this lane's own
  freeze `--regression` PASS above).
- Round-8 landed/unlanded split [OBS; landed SKILL append `:908-1097` and
  re-measured on the gate at freeze]: (b) the `omarchy` plane (11 rows;
  OM1–OM8 hermetic stub scenarios) and the receipt modes (`--snapshot` /
  `--snapshot-diff`; S1–S10) landed; (a) the hypr-live stub scenarios
  J/K/L **did not land** (no `hyprctl` PATH stub; 0 of 21 hypr-live ids
  asserted); (c) the assertion floor **did not land** — `VERSION_STR` at
  `:68` still reads `v1 (round 5 / M5-2)`, the base `--help` still omits
  `--regression`/`--snapshot`/`--snapshot-diff` (mode helps print them),
  the two exit-2 arms are unasserted, the boundary prefix is unasserted,
  and the `row_from_rc` rc-6 arm is still dead code. These are the
  residual ledger the standing-use note must carry.
- Round-9 work in flight at freeze [OBS point sample; **content NOT
  consumed** — resolved at dispatch from its record]: `tools/mado-verify.sh`
  modified in the worktree (+198/−7 vs HEAD; 3,078 L; sha
  `cbc0f5f7f32ad2a5…`; mtime 17:02:56 −03:00); untracked
  `corpus/knowledge/walker-deep-r9.md` (397 L / 24,361 B, mtime 17:03:27)
  and `plans/round-9-record-draft.md` (706 L / 46,247 B, mtime 17:02:51);
  scratch `/tmp/w9-mado-m9-2`, `…-m93`, `…-m94`. No round-9 artifact
  committed at freeze.
- Corpus inventory [OBS]: 17 committed notes in `corpus/knowledge/`
  (`git ls-tree HEAD corpus/knowledge/ | wc -l`), `corpus/lessons/` 0
  entries (ninth round); `corpus/README.md` 19 L / 12,709 B /
  `2dd274f5e270e65b…` — 8 note rows, 9 notes unrowed (r4 ×2, r5 ×1, r6
  ×3, r7 ×2, r8 ×1); `SCORECARD.md` 20 L / 9,079 B / `de0960be17d03b0a…`
  (rounds 4–7 abbreviated at `:16-19`, round 8 one-line); `LOG.md` 299 L /
  22,498 B / `156e03033cfed8d1…`; `SKILL.md` 1,097 L / 83,184 B /
  `32f32605e1e7d646…`; `corpus/QUALITY.md` 8 L / `1923c94f49788ade…`;
  `PROVINCE.md` `7aad7b86…`, `MINT.md` `4408f667…`, `SHONEN.md` 12 L /
  `edace65e…` (byte-identical since `c03c249`, 4/4 `[x]`).
- Round-8 record family at freeze [OBS]: `plans/round-8-record-draft.md`
  657 L / 42,881 B / `b46d4c4cb9d5cb5e…` (committed with the round-8
  landing); `reports/r8-aud-m8.md` 127 L / 11,881 B / `4d8cd1cb163d810e…`;
  `reports/r8-ver-m8.md` 156 L / 9,997 B / `a96795039520e86a…`;
  `corpus/knowledge/gate-mutation-sweep-r8.md` 178 L / 10,946 B /
  `9d6435f5cdd52561…`; `plans/round-9.plan.md` 231 L / 15,136 B /
  `8630c91a75a2eb43…`. The committed round-7 draft's ⟨PENDING⟩ count is 13.
- Debt carried into round 10 [OBS]: `corpus/lessons/` 0; README 9 unrowed
  notes (+ round-9's and round-10's to come); `SCORECARD.md:16-19`
  abbreviated; `walker-deep.md` §10/§11 errata owed (sha
  `0982ba066c72575a…` unchanged since round 7 — round-9's in-flight
  `walker-deep-r9.md` is a new file, not an append to it; what it is is
  resolved from the round-9 record); round-7 draft ⟨PENDING⟩ 13 unfilled
  after round 8's §4f fill text was drafted, not applied.
- Operator channel `.ufo/l0-questions.md` (21,539 B, mtime 14:05:52
  −03:00): zero `mado` lines at freeze (`grep -i`, shape-only) — no
  operator question owed an answer.
- Sibling harness (read-only): `tameshi-shokunin/tools/mutate-and-run.sh`
  61,632 B / `cf41efaa8be5f52d…242c75` — unchanged since the round-8
  freeze; every freeze run printed it as provenance, not gated.

Candidate decision: post-round-9 candidates — (1) the ten-round synthesis
and the gate's standing-use note (this round's charter: fold nine landed
rounds into a re-derivable whole, and hand the gate over with its limits
named); (2) the carried gate residuals (J/K/L, the assertion floor, rc-6);
(3) record debt (README, SCORECARD, lessons, walker-deep errata, round-7
⟨PENDING⟩); (4) a new frontier. (1) is the claim — the only candidate that
needs the arc's end to exist. (2) is classified by (a)(vi) and recorded by
name in (b)(vi); it closes only under the full discipline if a lane
carries it, never as the headline. (3) rides the record, not the move.
(4) is declined: the final round names gaps, it does not open ground.

Axis move: calibration + operability — ONE move, three ordered stages: the
arc is distilled into a re-derivable synthesis (a); the gate receives its
standing-use contract with the residual/limit ledger (b); the record
family closes the arc and commits the handoff (c). Every number in (a)/(b)
carries the command that produced it at the landed revision; a number that
cannot be re-derived is tagged, never recited.

Claim:
(a) **The ten-round synthesis** — `corpus/knowledge/ten-round-synthesis.md`
    (self-label M10-1; `source:` / `verified-at:` / `recheck:` per
    CORPUS.md). Sections, all measured at the landed revision:
    (i) the arc ledger — mint + rounds 1–10: axis move, landed artifacts
        (name / `wc -l` / bytes / sha), gate revision, selftest count,
        verdicts, the verifying seats as the records name them (VER-M3 …
        VER-M8, AUD-M6 … AUD-M8), record-debt movement — one row per
        round, each cell carrying the command or record line behind it;
    (ii) the gate ladder — line counts and shas re-derived per arc commit
        from the git blobs (the four design-time values above prove the
        method works); selftest counts re-run per revision where the
        revision is still faithful at dispatch, else cited [OBS-record]
        with its source; the landed revision's whole row re-run; the kill
        ladder's receipts (4/10 → 10/10 ×3 → round 9's) and the pin
        lineage (`c4c1afb7…a5171` → `d2bcdb31…db62` → round 9's landed
        target, with the marker families named);
    (iii) the invariants — the boundary hash every verdict run prints, the
        read-only substrate record, the scratch-only discipline, the
        single-writer rule — each with the rounds that measured it;
    (iv) the three trends (LEARNING.md) over the arc — expansion, quality,
        discernment — a verdict each with its evidence, the harm-side
        facts named as such (the lessons ledger at 0; any round-9 clause
        that did not land);
    (v) the gap ledger — every surface the arc never made verdict-bearing
        (rendered UI, socket protocol, idle transitions, dispatcher
        behaviour, waybar module text, hyprsunset/hypridle stop-cause,
        tree-wide omarchy cleanliness, the exit-flatten harness boundary)
        — each with why it stays unknown (no read surface / by constraint
        / harness-side);
    (vi) the classification — every open item from the round records 1–9
        (and round 9's resolution) as closed (evidence) / operator-owned
        (named) / unknown (named); counts per class, every item named; no
        item is left unclassified — "carried" does not exist in the final
        round.
    A number that cannot be re-derived is tagged [OBS-record] with its
    source line or dropped. The synthesis cites records and landed
    artifacts, never design-time plan numbers except where a record cites
    them.
(b) **The gate's standing-use note** —
    `corpus/knowledge/gate-standing-use.md` (self-label M10-2), plus the
    SKILL.md final append (a short section pointing to it, carrying the
    quick invocation table). Substance, measured against the landed
    revision:
    (i) custody — the gate is the lane's single-writer verdict instrument:
        every edit carries the lane identity, a LOG entry, and the
        widening discipline below; it is never edited to match reality;
    (ii) the invocation map — every mode with its contract, quoted from
        the landed `--help` and mode helps: default live / `--no-live` /
        `--root DIR` / `--selftest` / `--regression [--keep]` /
        `--snapshot FILE` / `--snapshot-diff OLD NEW` / `--help`; env
        `MADO_VERIFY_ROOT`, `MADO_VERIFY_LIVE=auto|yes|no`,
        `MADO_VERIFY_HARNESS`;
    (iii) the verdict vocabulary — `MADO_VERIFY: CLEAN|DIVERGED` (exit
        0/1/2), `MADO_SELFTEST`, `MADO_REGRESSION: PASS|FAIL|SETUP`,
        `MADO_SNAPSHOT: WRITTEN|REFUSED`, `MADO_DIFF:
        SAME|DETAIL-CHANGED|CHANGED|SETUP`; row classes PASS/FAIL/UNKNOWN/
        SKIP/NOTE; UNKNOWN never CLEAN; NOTE never flips the verdict;
    (iv) the standing cadence — when to run what (post-change live run;
        pre-commit `--selftest`; gate edits → re-cut + `MADO_REGRESSION:
        PASS`; drift watch → snapshot pair + `--snapshot-diff`; a receipt
        names its revision), each line carrying the round that
        established it;
    (v) the maintenance rules with their ancestry — round-6 rule 2 (no
        widening without a covering mutant), round-7 rule 1 (every
        widening carries `MADO_REGRESSION: PASS` at the widened revision;
        the printed `REGRESSION_RECUT` is the remedy; the excision pin's
        marker families), pins never edited to match reality (a MOVED pin
        is reported first), exemptions by name, the harness read-only
        boundary (the exit-flatten family stays a recommendation to
        tameshi, never a patch);
    (vi) the residual and limit ledger — what the gate does not prove
        (stub scenarios prove row logic, never live values; rendered UI /
        socket protocol / idle transitions UNKNOWN by constraint; the
        file plane fails closed on a missing tree) and every open residual
        at the landed revision (J/K/L, the assertion floor, the rc-6 arm,
        `VERSION_STR`, base-help discoverability, any round-9 exemption) —
        each re-checked by grep at dispatch, quoted open/closed, and left
        to the operator where open. The note never upgrades a residual
        into a promise.
(c) **The record family** — the arc's closure, append-only:
    - `corpus/README.md` — every note row owed at dispatch (at freeze: the
      9 unrowed notes; round-9's claim names the r7 ×2 + r8 rows), each
      re-measured at apply time; a `## Known gaps` section from (a)(v);
      row count before → after.
    - `SCORECARD.md` — the abbreviated rounds 4–7 rows replaced from the
      committed record drafts' ready text (re-measured at apply time),
      rounds 8–10 rows, and a final row naming the standing gate revision
      and the synthesis.
    - `LOG.md` — the round-10 final entry carrying the commands; the
      arc-end statement (probation 4/4 `[x]` since round 5; promotion is
      the operator/gate decision, never self-declared).
    - `corpus/lessons/round-10.md` chartered with its `## Gate` section
      (candidates, admits, rejects with reasons) and a non-author
      spot-check (≥1 admit, ≥1 reject; a lane's own subagent does not
      count; `LEARNING.md:38-43`) — or the refusal recorded as the arc's
      named failure with its reason and owner; first entry in nine rounds
      if it lands.
    - `walker-deep.md` §10/§11 errata append if round 9 did not land an
      equivalent (substance = `walker-live-surface.md` §5 ledger,
      append-only); the round-7 draft's 13 ⟨PENDING⟩ closed as an
      appended erratum if still owed.
    - `AGENTS.md` — one appended pointer line to (b) (standing rules
      surface; no rule changes).

Ordering: (a)/(b) consume the round-9 landed revision — (a9)/(b9)/(c9)
resolved at dispatch from the round-9 record (which theme/walker rows
landed, or the recorded not-landed; the helper-regex widening; the re-cut
`MADO_REGRESSION: PASS` and its target; the receipt lines quoted in its
record; its README rows; `corpus/lessons/round-9.md` attempted). A clause
that did not land is a finding for (a)(iv)/(vi) and (b)(vi) — round 10
opens no gate edit of its own. Residual closures (the help text, the
version string, the exit-2 arms, rc-6, J/K/L) are not this round's claim;
if one lands anyway it carries the full discipline (covering mutant,
re-cut, `MADO_REGRESSION: PASS`, selftest count before → after) and is
named in both (a) and (b); whatever stays open ships named in (b)(vi) and
the operator handoff. (c) rides (a)/(b); the final commit lands last and
carries the arc-end statement.

Anti-claim: the synthesis is a distillation, not a new measurement — every
number carries its command and date at the landed revision; a number that
cannot be re-derived is tagged [OBS-record] with its source or dropped,
never recited as measured; records are never rewritten — a debt that never
landed is reported as never landed, corrections are appended; the
standing-use note cannot upgrade the gate — a NOTE stays non-verdict, an
UNKNOWN stays unknown, a stub scenario proves row logic never live values,
and the verdict stays `bash tools/mado-verify.sh`; no compositor/session
mutation (no launcher open, no socket connect, no `omarchy theme set`, no
restart); substrates read-only, secrets shape-only; the tameshi harness
and sibling repos are read-only — a needed change is a recommendation to
that lane; no `git status`/`git fetch` on the omarchy checkout; snapshots
and receipts stay in scratch, never committed; the final round opens no
new frontier — surfaces never covered are named as gaps, not promised;
promotion is never self-declared.

Measure: the synthesis lands (lines / bytes / sha; per-ledger-row command
or source; the classification counts per class); the gate ladder
re-derived per arc commit (`git show <commit>:tools/mado-verify.sh |
sha256sum`; the landed revision's row re-run) and the kill/pin lineage
quoted from receipts; the standing-use note lands and its mode map matches
the landed `--help` / mode helps (quoted, rc measured); the residual
ledger's open/closed state per item with its grep; the final runs at the
landed revision (`--selftest` count; `--no-live` and live counts;
`--regression` receipt + target sha; a snapshot pair → `MADO_DIFF:
SAME|CHANGED` worked example, scratch only); the record family before →
after (README rows 8 → 8+N; SCORECARD rows; lessons 0 → 1 or the recorded
refusal; round-7 ⟨PENDING⟩ 13 → closure; `walker-deep.md` sha before →
after); the boundary invariants quoted before/after every run (gate sha;
the config-plane combined hash); the three trend verdicts with their
evidence lines; the operator channel (0 `mado` lines at freeze — a
mid-round filing is named, never answered here).

Open unknowns at draft: whether round 9 lands (a9)/(b9)/(c9) and under
which gate sha — the landed revision is the ladder's last row and the
note's row inventory; whether the round-9 re-cut leaves
`MADO_REGRESSION: PASS`, and what `PIN_MADO`/`TABLE_MADO` then carry;
whether round-9's record quotes its receipt lines (scratch does not
survive); whether the theme spec's installed-consumer rows landed as
NOTE or verdict rows, whether the socket rows were exercised hermetically
or exempted by name, and whether `walker-deep.md` §10/§11 found its
append; whether the record debt moves at all (README rows, SCORECARD
stubs, lessons, round-7 ⟨PENDING⟩); whether a non-author seat exists for
the final lessons entry; whether each historical gate revision still runs
its `--selftest` faithfully at dispatch (toolchain / fixture drift — if
not, its row cites the record value tagged); whether the sibling harness
moves mid-round again (receipts pin it; provenance, not gated); whether
the operator's L0 files a mado entry mid-round (none at freeze); whether
the final commit's reviewers accept the round-7 ⟨PENDING⟩ closure riding
round 10 if round 9 leaves it owed; whether the T6-1 recorded case stays
the right replay after round-9's re-cut (the round-9 record's target is
the authority).

Write scope (execution): one output file per lane as assigned; the gate is
single-writer (no gate edit is this round's claim); scratch
`/tmp/w10-<lane>-*`; substrates (`~/.config`, `~/.local`, the omarchy
checkout, the tameshi harness) read-only; secrets shape-only; snapshots
and receipts stay in scratch. This design lane wrote only this file;
scratch `/tmp/w9-prepm10/`.