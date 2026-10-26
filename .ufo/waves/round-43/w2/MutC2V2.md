# Seat MutC2V2 — report (round 43, w2, inline v1)

**Assignment.** Mutation-test the eight v2 tightenings of `quality/counters/c2-r43-gkeep-entry-v2.py`
(d+ unique occurrence, d+ comment stripping per extension, e+ raw-URL prefix, g+ every-naming-line
bound, i+ exact package path, i+ flip word, i+ BAD_LOC in entry, i+ all-PINS cited): ≥ 2 weakening
mutants per condition, each scored with (a) the v2 controls runner, (b) the forge/more forgery
harnesses — copies in my scratch pointed at the mutant, frozen `ctl/` never edited — and (c) the
landed data commit `1959770657f1f8665097c1aed4be6c1cbb07139f` (must stay admitted). A mutant no
control kills is a missing control; name the input that would.

**Verdict.** 16 mutants (2 per tightening), all scored on all four detectors. **10 killed, 6
survive the entire registered battery** — six missing controls, each with the killing input named
*and demonstrated* (pristine rejects the input via exactly the clause under test; the mutant
admits it). All 16 mutants keep the landed data at `admitted=1/1 verdict=TARGET_MET` exit 0: every
mutant is a pure weakening, and the landed entry exercises every tightening. Full matrix, inputs
and evidence paths: `.ufo/waves/round-43/w2/MutC2V2/matrix.md`.

## Findings, ranked

1. **Six missing controls around PRED-C2-r43-v2** (survivors V2-2b, V2-3b, V2-4b, V2-6b, V2-7b,
   V2-8b). The battery has no fixture for: a GATE quote living only inside a `#` comment of a
   `.py`/`.conf` receipt; a raw URL with the right host+repo but a **wrong commit**; a >120-char
   entry line naming an id without its quote; a REFUSE reason whose flip token is only embedded
   (`whenever`); the `zenn.dev`/`qiita.com` BAD_LOC markers (the battery exercises only 中文,
   `amgsk.dev`, `t.co`); and partial pin coverage (7 of 10 PINS cited — the battery has only
   all-10 (P) and 3 (X3)). Each input is demonstrated in `MutC2V2/evidence/logs/probe-kills.txt`
   (pristine rc=1 with the clause under test at 0; mutant rc=0 admitted=1/1). These are coverage
   gaps of the battery, not holes in the landed data.
2. **The runner's 74 controls alone would declare 14 of 16 mutants surviving** (only V2-5b is
   killed inside the runner, by A06+A07). The kills for d+ (B1, C1), e+ (G1, G2), g+ (E1), i+
   flip (F2), i+ entry-BAD_LOC (X2) and i+ all-PINS (X3) all come from the forge/more fixtures.
   Reason found and demonstrated: the frozen runner's `patched_counter` inserts fixture receipt
   hashes before the original PINS entries, and a later duplicate dict key wins, so any
   patched-kind control that edits a pinned receipt (N04, N05, H09, H11, H13, W14, W15) is
   rejected by `pin_ok` regardless of the clause it names — the runner carries no receipt-content
   teeth. Harness observation, not one of the 16 mutants; no verdict above changes (every
   attributed kill uses a fixture with unedited receipt bytes, so it is a genuine clause kill).
3. **The eight tightenings are otherwise well-controlled**: unique occurrence (killed twice by
   forge B1 — its quote sits at 4 lines of `Hyprland-WindowRuleApplicator.cpp`), C++ comment
   stripping (C1; C2 additionally held by unique-occurrence since its comment quote occurs
   twice), the raw-URL prefix (G1+G2), the every-naming-line bound (E1), the exact package path
   (F1 for the dir prefix, A06+A07 for the STAGED membership), the flip word (F2), BAD_LOC in the
   entry (X2) and all-PINS (X3). w1's CritC2Cheat tightenings are real teeth where fixtures
   exist; the six shapes above are where they are not yet exercised.
4. **Real-data stability**: every mutant scores `1959770657f1f8665097c1aed4be6c1cbb07139f` at
   `admitted=1/1 verdict=TARGET_MET` exit 0 (`MutC2V2/evidence/logs/V2-*-realdata.txt`) — no
   mutant false-rejects the landed entry, so none of the six survivors is a data risk; they are
   purely battery-coverage findings for the non-author closure to weigh.

## Method and fidelity

- Pristine copy of the counter byte-identical to the frozen file (sha256
  `9a83407062d165661d211a714ce06b381391c7c4574c91c71eb54689dde1d028` on both paths; unchanged
  after every run). Baselines on the copies reproduce all four frozen receipts exactly
  (`CTL_C2: controls=74 correct=74/74` exit 0; forge 6/15; more X1 admitted / X2,X3 rejected +
  probes; real data 1/1) before any mutation.
- Mutants are one-edit deltas of the pristine copy; per-mutant diffs:
  `MutC2V2/evidence/diffs/V2-*.diff`; harness-copy diffs (only `LANE`/`COUNTER`/`CTL`/`WORK`/
  `SEAT` rewired): `evidence/diffs/harness-*.diff`.
- Fixture repos built by the frozen controls' own helpers (`git -C "$D" init -q`, toplevel
  asserted `== $D`, throwaway identity via `-c`, never written to any config) under
  `TMPDIR=/fast/scratch/hyaku/mado-r43/MutC2V2/...`; no git call outside a fixture dir; no
  mutating git in the lane or fleet.
- Restoration evidence: `git -C <lane> status --porcelain` over `quality/counters`,
  `.ufo/waves/round-43/ctl`, `.ufo/waves/round-43/fetch`, `registration-v2.md` is empty; frozen
  counter sha256 identical before and after. Nothing written outside my seat dir and my scratch.
- Scratch `/fast/scratch/hyaku/mado-r43/MutC2V2` deleted after the evidence was copied into the
  seat dir (logs, probe driver, diffs, hashes). A tree left on disk would be my own defect; none
  remains.

## Impacted axes

- **Coverage (C2)** — the six missing controls sit exactly on C2's sourced-assimilation teeth;
  until they are fixtures, the battery under-reports how much weakening PRED-C2-r43-v2 tolerates
  while still scoring the landed data TARGET_MET.
- **Calibration** — the pin-shadowing observation (finding 2) means the runner's `controls=74`
  headline overstates its independent teeth; the forge/more fixtures carry the receipt-content
  load. No axis is harmed by this seat: no counter, control, receipt or registration byte changed.

## Evidence inventory (all under `.ufo/waves/round-43/w2/MutC2V2/`)

- `evidence/logs/` — 69 files: `base-{realdata,runner,forge,more}.txt` (4), per mutant
  `V2-*-{runner,forge,more,realdata}.txt` (64), plus `probe-kills.txt`.
- `evidence/probe.py` — the missing-control demonstrator (control P + one delta per input; scored
  against pristine and the mutant; last-wins PINS patcher documented inline).
- `evidence/diffs/` — 16 mutant diffs + 3 harness-copy diffs; `evidence/hashes.txt` — sha256 of
  pristine copy, all mutants, harness copies, probe.

Not run: any host compositor read, any oracle, any package transaction, no pacman. Tools: system
`python3 3.14.8`, `git 2.56.0` — nothing installed, no tool state changed.

Report: .ufo/waves/round-43/w2/MutC2V2.md
