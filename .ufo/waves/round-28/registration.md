author: mado
date: 2026-10-23

# mado round 28 — registration (frozen before any control or data seat of this round)

Base: lane tip `da33a3ffb3d2004c0d8d8f526e3d0cba1bdabf79` (round-27 closure: admitted;
spotcheck `da33a3ff`). Paths below resolve under `.ufo/waves/round-28/` unless they start
with `tools/`, `quality/` or `corpus/`. Lane repo: /home/vgpnk/Projects/shokunin/mado-shokunin.

## Claims

**C1 — operability: the lane's offline gate set closes the round-27 routed blind spots.**
Surface moved: `quality/counter-selftest.py` (suite A over the round-26 counters) keeps its
committed round-27 checks (48 → the landed 56) and gains (a) the ExecRepairA1 predicate set
adopted from the round-27 w4 audit (`c2-drift-extra`, `c2-drift-missing`, `c2-one-missing`,
`c2-one-extra`, `c2-two-missing`, `c2-two-extra`, `c2-embed-at-min`, `c2-embed-below-min`),
(b) probes that kill the three surviving sealed `held-c1v2` classes (`node-subset`,
`missing-version-guard`, `extra-output-segment`), (c) probes that kill tolerance disjuncts of
size ≥3 (`or nm == 3`, `or ne == 3`) and (d) probes that kill exact-string BOOLWORD
acceptance (ExactBool blind spot). `quality/check-population.py` becomes the extended
round-28 population checker (open-ended `green=all`/ratio targets; the round-26 artifact at
`.ufo/waves/round-26/quality/check-population.py` stays frozen). `quality/` gains the
Q36-successor witness fixtures and `q36-successor-receipts.txt` (the two case/marker-case
survivors die on committed witnesses). The command that shows it unmoved: any one of the
composite counter's legs below at a REV that lacks the repair.

**PRED-C1-r28**: At REV, running `python3 -I .ufo/waves/round-28/c1/count.py REV` exits 0
and prints `PRED-C1-r28 verdict=TARGET_MET`; the six legs, each on committed bytes at REV:

- h1-rotation — `python3 -I .ufo/waves/round-27/c2/count-v2.py REV --heldout
  /fast/scratch/hyaku/mado-r27/heldout --seal .ufo/waves/round-27/c2/heldout-seal.txt`
  prints `PRED-C2-r27-v2 … verdict=TARGET_MET` (green=17/17, w_killed=15/15,
  h_killed=15/18) and the CASE lines for `held-c1v2-node-subset`,
  `held-c1v2-missing-version-guard`, `held-c1v2-extra-output-segment` each read
  `rc=1 KILLED`.
- h2-rotate — the same counter with `--heldout /fast/scratch/hyaku/mado-r28/heldout2
  --seal .ufo/waves/round-28/c2/heldout2-seal.txt` prints `verdict=TARGET_MET` under its
  frozen rule (h_killed ≥ ceil(0.75·h_valid), h_valid ≥ 6, ≥2 per subject).
- refpub-kills — the same counter with `--heldout /fast/scratch/hyaku/mado-r28/refpub
  --seal .ufo/waves/round-28/c1/refpub-seal.txt` prints `h_killed=h_valid` (all valid
  public reference rows die), with at least 9 valid rows and at least 2 per subject.
- a1-predicates — the committed suite bytes contain the eight named A1 probe constants and
  REQUIRED entries (`c2-drift-extra`, `c2-drift-missing`, `c2-one-missing`,
  `c2-one-extra`, `c2-two-missing`, `c2-two-extra`, `c2-embed-at-min`,
  `c2-embed-below-min`) and do not contain the softened `got < total` predicate for the
  four one/two-missing/extra checks (A1's `got == 0`/`total == 51` form).
- q36-witness — `bash .ufo/waves/round-28/quality/q36-successor-run.sh` exits 0 and
  `quality/q36-successor-receipts.txt` names both surviving case mutants.
- q37-open-ended — `python3 -I quality/check-population.py --registration
  .ufo/waves/round-27/registration.md .ufo/waves/round-27/evidence/c2-after-0b53bd86.txt`
  exits 0 (default verdict PASS), and the round-26 frozen artifact sha256 is unchanged.

**C2 — calibration: the round-27 closure's nine routed record defects are repaired.**
Surface moved: the lane's self-assessment records (SKILL.md gate registry rows, lesson
M27-2 text, the E01 red-before receipt, the q36-successor receipts dead pointer, the
harm-watch omission, the registration's C2-measurement record, the w3 seat-count
discrepancy, the SKILL.md:631-636 citation, the uncommitted w4 erratum report). A defect is
resolved when a named closure-ledger row lists its fix and the exact check of the frozen
counter passes. Before (frozen counter at the register commit): 8 of 9 unresolved.
After: 0 unresolved. The command that would show it unmoved: the frozen counter below at a
REV before the record fixes.

We PRED-C2-r28**: At REV, `python3 -I .ufo/waves/round-28/c2/count.py REV` exits 0 and
prints `PRED-C2-r28 verdict=TARGET_MET`; the nine named defect checks each pass (see the
counter's source for the exact per-defect predicate and its evidence path).

**C3 — coverage (lowest non-retired scored axis), sourced: U6 (kernel-input → Wayland
debugging ladder) gains an admitted, sourced knowledge entry.** Surface moved:
`corpus/knowledge/input-event-ladder-r28.md` opens with `source:` citing a `mined` row
opened this round (S183+) and names `covers: U6`; `corpus/knowledge/` sourced entries
grow from 3/7 → 4/7 U-items. The command that would show it unmoved: the round-12 C3
counting loop at a REV without the entry.

## Kill rule and controls (before data)

A control that meets a target under its frozen counter forces redesign of that claim before
data (or the claim is declared exploratory). Controls are scored with two seeds; receipts
under `controls/`:

- C1: `StubGreen` (suite A always exits 0 — must MISS h1/h2/refpub), `RejectLike` (suite A
  exits 1 unless a subject also fails every probe — must MISS greens), `CtlGitCheat`
  (demonstrates the frozen counter's sandbox exposes `.git`, so a suite could diff a subject
  against its pristine bytes — recorded as the accepted r28-residual cheat, not a target).
- C2: DoNothing = the counter at the register commit with no record repairs (8/9).
- C3: DoNothing = the counter at a REV without the entry.

## Data rule and inherited state

- The uncommitted lane-authored file `.ufo/waves/round-27/w4/reports/RevRepair.md`
  (audit +166/-33) and `.ufo/waves/round-27/w4/reports/ExecRepairA1.md` land as erratum
  commits under this round's entry before any measurement (PROTOCOL inherited-state rule).
- Suite A candidate builders work from the public class names and the round-27 audit; they
  never read `/fast/scratch/hyaku/mado-r27/heldout`, `/fast/scratch/hyaku/mado-r28/heldout2`
  or `/fast/scratch/hyaku/mado-r28/refpub`. The first file returned at the expected path
  lands unmodified and is measured.
- A repair or extension is a fix only when it is shown able to fail: each candidate lands
  with committed red-before receipts and a green-after run under the frozen counter.

## Host safety

Every suite run stays inside the frozen counter's bubblewrap sandbox (`env -i
PATH=/usr/bin`, `--no-local` clones, 300s timeout, 4GB RLIMIT_AS). No compositor state,
config tree or sibling repo is written. The live session is only read with `hyprctl -j`
query verbs.

## Saturation / axes (kept from round 12)

Saturation line 9.0 on every scored sub-axis; stagnation window N=3. Lowest non-retired
scored sub-axis at base: coverage / sourced-current-art ground 4.2857 (3/7 U-items).
