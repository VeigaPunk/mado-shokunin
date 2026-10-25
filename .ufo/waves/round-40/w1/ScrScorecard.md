# ScrScorecard (w1, round 40) — status: DONE

Drafted the SCORECARD round-40 section and the LOG.md round-40 entry as slot files. No measured
after-value was invented; every number not readable in the frozen freeze evidence is a
`<<AFTER …>>` / `<<HASH …>>` slot.

## Behavior

- `.ufo/waves/round-40/w1/ScrScorecard/scorecard-r40.md` — modelled on `SCORECARD.md` `## Round 39`
  (line 2423). Contains: registration/freeze/base intro (freeze `5e7e88525cc539563de7746361b2650802e81809`,
  base `9fc511ddce708327377161202f358ce37dc266ba`), the lowest-axis sentence from the frozen
  `receipts/axis-base.txt`, the 64-seat `w1` shape, a two-row claims table (C1 operability, C2
  coverage) with before→after, the counting commands **verbatim** from `registration.md`, the
  separability/controls paragraph, the harm-watch paragraph, the `### Capabilities (round 40)` table
  with the row `live option-table merge` (first-working round 40), the
  `### Sources, saturation, planned` paragraph (sources/saturation/assimilation/ratio/frontier slots,
  axis re-derivation line) and `### Planned (round 41; intent only)` with two intent items.
- `.ufo/waves/round-40/w1/ScrScorecard/log-r40.md` — modelled on `LOG.md` `## Round 39` (line 2432).
  Bullets: attempt 1 (`MadoR40`, from `w1.ready`), motivating evidence (round-39 planned item 1;
  base tool only had `--getoption FILE`), freeze, wave `w1` (64 seats, dispatch `e2b51d3`), C1 data
  `<<HASH>>`, C2 data `<<HASH>>`, the host finding (angle inheritance), assimilation, considerthese
  proposal 2, errata D2, records.

## Grounded values used (each re-derived by me, read-only)

- Freeze/base receipts: `fixtures=0/13 tool=present verdict=TARGET_MISSED` exit 1; `admitted=0/1
  verdict=TARGET_MISSED` exit 1; `clauses=a:1 b:0 g:1 k:0`; `selftest=71/71` at base;
  `MADO_SELFTEST: 460/460 assertions passed`; axis `56/56`, `51/51`, `12/12`, `mismatched=0`;
  census exit 0 with seven W04 + one W01 — `.ufo/waves/round-40/receipts/{c1-before-base.txt,
  c2-before-base.txt,selftest-base.txt,axis-base.txt,census-before.txt}`.
- Controls (frozen): `CTL_C1: controls=18 correct=18/18` (base `0/13`, reference `13/13` but
  `TARGET_MISSED`, 16 mutants `<13`), `CTL_C2: controls=21 correct=21/21` (20 mutants `0/1`, P
  `1/1`) — `receipts/ctl-c1.txt`, `receipts/ctl-c2.txt`.
- Native capture: `wc -l .ufo/waves/round-40/c1/native-capture.jsonl` → 70; form histogram
  int 44 / float 5 / custom 13 / str 8 (my own count over the committed JSONL).
- Wave shape: `w1-spec.json` has 64 `items`; `w1.ready` names L1 `MadoR40`.
- Prior-record baselines quoted as *before* values: Sources 214, index `indexed=56/56` — from
  `SCORECARD.md` `## Round 39`.

## Provisional values carried, flagged in the draft

The host-finding bullet in `log-r40.md` quotes `rgb(e68e0d)`, `rgba(33ccffee) rgba(00ff99ee) 45deg`
and the live `ffe68e0d 45deg` from the registration's §Provisional facts and **labels them
provisional**, pointing at a `<<AFTER re-derivation seat / receipt>>` slot. The L1 must replace them
with the wave re-derivation before landing; they are not presented as evidence in the draft.

## Gates

- Not run by this seat (scribe; no build/test/lint assignment). The drafts contain the commands to
  run: `python3 -I quality/counters/c1-r40-live.py --repo . --rev <rev>` and
  `python3 -I quality/counters/c2-r40-forms-entry.py --repo . --rev <rev>`, both copied verbatim
  from `registration.md` (byte-for-byte, including the `cd /home/vgpnk/Projects/shokunin/mado-shokunin &&`
  prefix).

## Touched surfaces

- Wrote only: `.ufo/waves/round-40/w1/ScrScorecard/scorecard-r40.md`,
  `.ufo/waves/round-40/w1/ScrScorecard/log-r40.md`, `.ufo/waves/round-40/w1/ScrScorecard.md`
  (this report). No tracked file edited; no config tree, compositor verb, service or fleet path
  written; no git/jj mutation; no scratch left behind.

## Out of scope

- The SCORECARD/LOG integration itself (the L1 is the only integrator).
- Filling the slots, including the provisional host-finding literals.
- Any claim verdict.

## Findings for the L1

1. `registration.md` states the reference tool's host labelling as `62 agreement, 8 agreement*, 0
   mismatch` under the angle-inheritance model; the drafts take the *labels* as a slot and keep the
   70-key denominator (my count of the committed capture).
2. `LOG.md` `## Round 39` records 64 seats dispatched and 60 reports; the round-40 draft's wave
   bullet therefore carries a report-count slot, not a number.
3. The scorecard's `No harm` paragraph lists all five harm-watch items of `registration.md` plus the
   compositor-verb boundary sentence; the `--selftest` floor `n ≥ 79` is stated as a requirement with
   the base 71 as the before value.

## Tooling

- No install or update performed (no pacman, no `uv tool`, no npm). Tools used: `python3 -I`,
  `git log/status` (read-only), coreutils.
