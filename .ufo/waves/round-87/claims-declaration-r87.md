# mado round 87 — frozen claims declaration (hyaku run 15, attempt 1)

Base `e4875ba5619053cc3f91bb2f4d819e189df4088c` (master at round start, clean). Declared 2026-11-05T05:46-03:00.
Fresh-start state: the three rejected closures before this round are r83, r84, r85 (`corpus/lessons/round-8[3-5]-verifier-spotcheck.md`,
headers read). The latest closure, `round-86-verifier-spotcheck.md`, was read in full; its routed defects R1–R8 are the
inputs to C2 and to the carried-defect list below. Operator authorization "Authorize all" (2026-11-05, Amendment 27) lifts
the pause; no do-nothing control below is waived.

## Axis posture at round start (all measured on this host, 2026-11-05)

| axis | counting command | score |
|---|---|---|
| navigation (coverage) | `python3 -I quality/check-index.py --repo . --rev <HEAD>` (r86 publication) | 107/107 → 10.0 |
| calibration (resolved-active) | axis publication, r86 | 86/86 → 10.0 |
| operability (selftest) | `bash tools/mado-verify.sh --selftest` | 460/460 → 10.0 |
| freshness (file plane) | `bash tools/mado-verify.sh --no-live` (today) | pass=29 fail=0 unknown=0 → 10.0 |

Capability table: last row entered r82; r83–r86 added none. The stagnation window (N=3) is exceeded and every
axis sits at or above the saturation line 9.0. **The stagnation nudge applies:** the round is a frontier/capability move.
C1 is that move. C2 is a calibration move on the lane's own control figures (not a waiver of anything).

## C1 — capability acquisition, axis coverage (frontier → core)

**Surface.** The notification-daemon configuration plane: mako's effective settings for one notification, resolved from
`~/.config/mako/config` (a symlink to the omarchy theme `mako.ini`), its `include=` chain (`core.ini`), and its criteria
sections (`[app-name=…]`, `[urgency=…]`, `[mode=…]` and combined criteria). Not held: no note owns it; `waybar-walker-plane.md`
covers only DND through `makoctl mode`. Source: the host's installed mako 1.11.0 manual
`/usr/share/man/man5/mako.5.gz`, sha256 `f717848f47cc7739d4bddbcc08c133a32e0d7dface7d1769882da1a0150477ba`
(opened 2026-11-05 by the scout seat; registry row S493 is written only from that opening).

**Tool.** `tools/mado-mako.py` — read-only: reads only the regular files its caller names (`--config`, `--home` for `~`);
arguments `--app-name`, `--urgency {low,normal,critical}`, repeatable `--mode`; prints one JSON object of effective values
and a `refusals` list for constructs it does not model. Refuses, never guesses. No `makoctl`, no D-Bus, no process.

**Frozen cases.** `.ufo/waves/round-87/controls/mako-cases-r87.json`, authored by the scout from the pinned manual alone
(not from the tool). Predicate frozen with the file: N ≥ 20 cases, each with its own config fixtures and expected values.

**Named mutants.** M = 10, the list in the counter's `MUTATIONS` (applied to a copy of the tool in scratch, never to the lane).

**Do-nothing controls (executed before scoring, receipts committed):**
- `naive-toplevel`: reads only the `--config` file, ignoring `include=` and every criteria section.
- `globals-include`: follows `include=`, applies global keys, ignores criteria sections.

Counting command (run from the lane root; `REV` = the measured revision):

    python3 -I quality/counters/c1-r87-mako-criteria.py --repo . --rev REV \
      --cases .ufo/waves/round-87/controls/mako-cases-r87.json --scratch-root DIR

Predicate (one sentence, the same in the plan, the counter code and the receipt label): **TARGET_MET iff the candidate
tool's correct count equals N, all M mutants are killed, and both do-nothing controls score strictly below N.**
Score = `10 × tool_correct / N` on this finite case set only. Verdict `TARGET_MISSED` otherwise.
Before (base, no tool): controls only; after: the candidate at the content revision.

## C2 — calibration, axis calibration (self-assessment vs observed state)

**Defect (r86 closure R1, `corpus/lessons/round-86-verifier-spotcheck.md` §2, §6.1).** The r86 entry
(`corpus/knowledge/refusal-records-clause-observations-r86.md:112`) and the SCORECARD r86 C2 row state the held rule scores the
new witness `0/1`. The held r85 counter's own `case_correct` scores the same witness `1/1`. The number came from the r86
counter's model `held_case_correct` (`quality/counters/c2-r86-clause-observations.py:574`), not the held counter.

**Figure set.** `.ufo/waves/round-87/controls/r86-figures-r87.json` (sha256 pinned in the counter), n = 2:
- F1 `held_rule_witness_r86`: stated `0/1`; re-derived by importing `quality/counters/c2-r85-status-classes.py` at
  REV and calling its `case_correct` on `border-size-int` from `.ufo/waves/round-86/controls/c2-cases-r86.json`. Re-derived: `1/1`.
- F2 `flood_r86`: stated `flooding 48/75`, `held 75/75`; re-derived by running `quality/counters/c1-r86-refusal-records.py`
  at its measured revision `3afdb713` with the frozen r86 controls. Must reproduce (the r86 receipt `final-c1-r86.txt`).

Counting command:

    python3 -I quality/counters/c2-r87-control-fidelity.py --repo . --rev REV \
      --figures .ufo/waves/round-87/controls/r86-figures-r87.json --scratch-root DIR

Predicate: **TARGET_MET iff n = 2 and every figure is reconciled — it reproduces at REV, or an append-only correction block
(a `Correction (round 87)` heading in the same file, naming the figure id and its re-derived value) exists.** Score
`10 × reconciled / n`. Before (base): F1 unreconciled → 5.0 `TARGET_MISSED`. After: both reconciled → 10.0 `TARGET_MET`.
Doing nothing scores 5.0. The r86 sentence is not rewritten; the correction is appended (CORPUS.md corrections rule).

## Frontier step (CORPUS.md §2b, all four items)

1. `corpus/SOURCES.md`: one row S493 for the mako 1.11.0 manual, opened 2026-11-05 (the scout's Gate quote ≤25 words; the
   sha above; tier A, scope = mako config grammar on this host version). SOURCES census before/after recorded in the lesson.
2. Census before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0 (425/427 era; the
   current row count is re-derived by the lesson). Round-end exit 0 is required.
3. Mistake mined: M87-1 — the r86 held-rule figure came from the lane's own model rather than the held counter
   (class `number-drift`; evidence `round-86-verifier-spotcheck.md` §2; captured-by `none` — the r86 selftest pinned the model
   to itself, `c2-r86-clause-observations.py:736-737`; fix = C2 + the selftest-pinning control).
4. Sourced claim: C1 rests on S493 (opened this round).

Quality criterion 146 (from `considerthese/2026-11-04.md` proposal 7, "mark each figure as relayed or re-measured"): the
lesson adds it, citing the reflection and date. It is not a third claim; it is a QUALITY criterion.

## Carried defects (routed by r86; not claims this round)

R2 (stored baselines) is absorbed by C2's sha-pinned figure file and C1's pinned case file. R7/R8 (forgery classes; count-only
clause observation) are routed to r88 unless the wave shows a cheap control. Assimilation: none (merge package holds no mako
theme; `host-producer-outputs-r29` is already held).

## Declared claim count and shape

2 claims, distinct axes (coverage; calibration), causally separable (C1 needs no C2 change; C2 reads only r86 bytes and the
held r85 counter). No exploratory claim. Wave: ONE v1 wave of 12 seats (band 8–16). Attack share: reviewer 2, critic 1,
mutation-tester 1 = 4/12 (33 %). Connector seats: 1. Planner: the L1 (MadoR87).

## Errata (appended after the wave settled; before any formal scoring at the measured revision)

Predicates, kill rules, targets, controls and the do-nothing definitions are unchanged. The corrections below change only
labels, pins and the measured command. Each was found by a wave seat and checked by the L1 against the bytes.

1. **Manual pin (C1).** The declared digest `f717848f…` is the sha256 of the DECOMPRESSED manual text (`zcat … | sha256sum`).
   The installed container `/usr/share/man/man5/mako.5.gz` hashes to `17ffc88c9950ba83a60a8d5bdf4cb528ca994adc6ba58e9386a81617b9db1670`
   (critic C1-pin; scout §1). Both are pinned here: container `17ffc88c…`, text `f717848f…`.
2. **Surface basis (C1).** "Not held" is withdrawn. `corpus/knowledge/waybar-walker-plane.md` §4 records the mako include chain and
   criteria by hand (OBS). No note resolved effective values; the resolver is the first to do so (critic C1).
3. **F2 stated text (C2).** `flooding 48/75 vs held 75/75` is line-wrapped in SCORECARD.md (lines 5062-5063). The stated text is now
   `48/75 vs held 75/75` (SCORECARD.md:5063); the re-derivation (running the r86 counter) is unchanged (ReviewFidelity R87RF-D1).
4. **Case file (C1).** During the wave the scout rewrote `controls/mako-cases-r87.json` (22 cases, lowercase ids, the counter's
   `app-name`/`mode` keys, C13 path `.config/mako/config`). Findings on the earlier 23-case bytes (Sentinel F1/F2, ReviewMako G1,
   MutTester D1/D2) are void for the final file. Final sha256 `0a9558743a721f70bb64b48d188b375f1468a140b00ca75ac93ab59c316d5fe3`.
   This file is the frozen case set for the measured run.
5. **Candidate tool, before scoring.** The tool is the candidate, not a frozen artifact. Fixed: an implicit `$HOME` fallback for
   `~/` includes (refused: `--home` is required); bare `none` and `invoke-default-action` accept no trailing words; refusal wording.
   The ten mutant `old` anchors were re-checked: each occurs exactly once after the fixes.
6. **Measured command (C2).** The declared command omits the R2 pin. The measured runs pass
   `--expect-figures-sha256` set to the figure file's sha256 at the measured revision.
7. **Named limits (not repaired; the predicate is unchanged).** Correction blocks are checked for the figure id and the literal value,
   not their reasoning (critic C2-after). The r86 selftest pinning the model (`c2-r86-clause-observations.py:736-737`) is outside the
   predicate and routed to round 88. The frozen case set does not exercise casefold, prefix, include-cycle or symlinked-config cases
   (MutTester D4-D6), routed as a superseding set.
