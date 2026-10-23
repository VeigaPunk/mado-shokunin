author: mado
date: 2026-10-23

# mado round 28 — registration (frozen before any control or data seat of this round)

Attempt 2. Attempt 1 (2026-10-23T18:00-03, OOM-killed mid-round) left five uncommitted
paths in the lane: two counters and a shortened registration (modified), `c1/synthetic-home/`
and `w1-spec.json` (untracked). Their disposition is stated in *Inherited state* below.
Lane repo: /home/vgpnk/Projects/shokunin/mado-shokunin. Paths without a leading `tools/`,
`quality/`, `corpus/` or `SKILL.md`-class prefix resolve under `.ufo/waves/round-28/`.

Base: lane tip `56ef773a6d7e179004e154628061b44676549175` (round-27 closure admitted;
non-author spotcheck `da33a3ff`).

## Claims

**C1 — operability (sourced: S183): the lane's offline mutation gate closes the named
round-27 blind spots and rotates its held-out set.** Surface moved: the committed suite
`quality/counter-selftest.py` gains behavioural probes for the three surviving `held-c1v2`
classes (`node-subset`, `missing-version-guard`, `extra-output-segment`); a fresh rotated
held-out set H2 and a public reference set are authored, sealed by sha256 list, and scored by
the frozen round-27 counter; the workspace-rule counter gains a round-28 successor
`count-v5.py` with two deterministic non-exact prefix-boolean inputs, whose public
exact-alias tool mutant must fail both; the two Q36 successor survivors gain committed
witness fixtures; the population checker gains open-ended (`green=all`, ratio) targets as
`quality/check-population.py` without touching the frozen round-26 artifact. The new note
`corpus/knowledge/mutation-testing-r28.md` cites S183 for the finite mutation-suite method
and its limits. The command that shows it unmoved: `python3 -I .ufo/waves/round-28/c1/count.py
<REV>` at this registration commit.

**PRED-C1-r28** (frozen): At REV, `python3 -I .ufo/waves/round-28/c1/count.py REV` exits 0
and prints `PRED-C1-r28 verdict=TARGET_MET`. Six legs, each over committed bytes at REV:

1. `h1-rotation` — the frozen round-27 counter `.ufo/waves/round-27/c2/count-v2.py` on the
   round-27 set H1 prints `PRED-C2-r27-v2 … verdict=TARGET_MET` with `h_killed=18/18` and
   each of the three named `held-c1v2` survivors reads `rc=1 KILLED`.
2. `h2-rotate` — the same frozen counter on the committed round-28 set
   `.ufo/waves/round-28/c2/heldout2/` with seal `c2/heldout2-seal.txt` prints
   `verdict=TARGET_MET` under the counter's own frozen rule (`h_valid>=6`, `>=2` per
   subject, `h_killed>=ceil(0.75*h_valid)`).
3. `refpub-kills` — the same counter on the committed public reference set
   `c1/refpub/` with seal `c1/refpub-seal.txt` prints `h_killed==h_valid` with `h_valid>=9`
   and `h_min_per_subject>=2`.
4. `boolword-v5` — `.ufo/waves/round-28/c1/count-v5.py REV --seed 28c1a8c0ffee0001` prints
   `PRED-C1-r28-v5 cases_pass=41/41 boolword_pass=2/2 verdict=TARGET_MET`, exit 0; the same
   command with `--tool-file c1/ref-mutants/exactbool-tool.py` prints `boolword_pass=0/2
   verdict=TARGET_MISSED`, exit 1.
5. `q36-witness` — `bash quality/q36-successor-run.sh` exits 0 against the committed
   checker, and `quality/q36-successor-receipts.txt` names both survivors
   (`Q2-glob-case-sensitive`, `Q5-marker-case-insensitive`) with pristine-rejects and
   mutant-accepts rows.
6. `q37-open-ended` — `python3 -I quality/check-population.py --registration
   .ufo/waves/round-27/registration.md .ufo/waves/round-27/evidence/c2-after-0b53bd86.txt`
   exits 0 and prints `verdict=PASS`; the frozen round-26 artifact
   `.ufo/waves/round-26/quality/check-population.py` keeps sha256 `803e0096…d0f64`.

**C2 — calibration (lowest active scored axis): the round-27 closure's nine routed record
defects are repaired.** Surface moved: the lane's self-assessment records — SKILL.md gate
registry rows (D1), lesson M27-2 (D2), the E01 red-before receipt (D3), the q36-successor
receipts pointer (D4), the SCORECARD harm-watch erratum (D5), the round-27 registration's
C2-measurement record (D6), the w3 seat count (D7), the SKILL.md:631-636 citation (D8), and
the late w4 erratum reports (D9). The command that shows it unmoved:
`python3 -I .ufo/waves/round-28/c2/count.py <REV>` at this registration commit.

**PRED-C2-r28** (frozen): At REV, `python3 -I .ufo/waves/round-28/c2/count.py REV` exits 0
and prints `PRED-C2-r28 verdict=TARGET_MET`; the counter prints `CHECK D1..D9 PASS`. At the
registration commit it prints `D9 PASS` and `D1..D8 FAIL` (8 of 9 unresolved).

**Lowest-axis selection.** The latest bounded calibration score is the literal
lesson-citation rubric 26/35 = 7.4286 (SCORECARD.md:1621-1623, round 24); coverage's U1–U7
source route is 7/7 = 10.0000 at its finite documentary ceiling and stays a harm watch
(SCORECARD.md:702, 776, 836); operability's hermetic pass fraction is 10.0000. Calibration is
the lowest active scored axis, so C2 works it. C1 is the operability claim that also carries
this round's sourced frontier work; it is not a coverage claim (no U-item moves).

## Kill rule and controls (before data)

A control that meets a target under its frozen counter forces redesign of that claim before
data. Receipts under `controls/`:

- `K1StubGreen` (`controls/K1StubGreen-suite-a.py`) — a suite-A file that always exits 0. It
  skips the claimed work (no probe is written). Scored with the frozen round-27 counter on
  H1: must MISS (`TARGET_MISSED`, `w_killed=0/15` and `h_killed=0/18`), because it can kill
  no mutant. Receipt `controls/K1StubGreen-h1.txt`.
- `K1RejectLike` (`controls/K1RejectLike-suite-a.py`) — a suite-A file that always exits 1.
  Scored the same way: must MISS (green rows fail, so the predicate is never met). Receipt
  `controls/K1RejectLike-h1.txt`.
- `K1Baseline` — the frozen counter on H1 with the committed suite: the before value of leg 1
  (`h_killed=15/18`, the three named survivors). Receipt `controls/K1Baseline-h1.txt`.
- `K2DoNothing` (C2) — the frozen C2 counter at this registration commit with no record
  repair: prints `D1..D8 FAIL`, `D9 PASS`, `verdict=TARGET_MISSED`. Receipt
  `controls/K2DoNothing.txt`.

## Data rule

- Suite-A candidate: the first candidate returned by the named suite executor lands
  unmodified (byte-identical to its returned path, `cmp`-checked) and is measured once; there
  is no second candidate. If it misses, the round is an honest stop for leg 1.
- H2 and the public reference set are authored by mutation-tester seats from public subject
  bytes (`.ufo/waves/round-26/{c1/count-v2.py,c2/count.py,quality/check-population.py}`)
  only. No seat may read `/fast/scratch/hyaku/mado-r27/heldout` (H1), the H1 seal's
  contents beyond the three public survivor ids, or another seat's returned row.
- The sets are sealed by a committed sha256 list (`c2/heldout2-seal.txt`,
  `c1/refpub-seal.txt`) before the deciding run; the frozen counter re-verifies the seal.
  They are committed after that run, so the closure can re-derive every leg from committed
  bytes. Leg 1 alone depends on the inherited ephemeral H1 directory; that boundary is stated
  in the claim and in the report.
- `count-v5.py` may read only the committed synthetic HOME
  `c1/synthetic-home/.config/hypr/hyprland.conf`; the operator's live `$HOME` is never read.
- The counterparty rule for the source: S183's row is written only after its URL is opened
  this round; the lesson `## Gate` records URL, access date and a ≤25-word located quote.

## Inherited state from attempt 1 (re-verified before reuse)

| path | attempt-1 state | disposition |
|---|---|---|
| `.ufo/waves/round-28/c1/count.py` | modified vs `56ef773` | **kept**, re-verified leg by leg; its `a1-predicates` text-marker leg was **discarded** (the eight ExecRepairA1 probe names it greps for do not exist in the landed suite, so the leg could only be satisfied by renaming probes to match a checker) |
| `.ufo/waves/round-28/c2/count.py` | modified vs `56ef773` | **kept**, with D9's placeholder sha prefixes replaced by the full committed hashes |
| `.ufo/waves/round-28/registration.md` | modified (shortened) | **discarded and rewritten** (both prior texts carried the unbuildable text-marker leg) |
| `.ufo/waves/round-28/c1/synthetic-home/` | untracked | **kept** (bytes re-read; the only HOME count-v5 may use) |
| `.ufo/waves/round-28/w1-spec.json` | untracked | **kept**, validated under policy v1 and dispatched as wave 1 this round |
| `/fast/scratch/hyaku/mado-r28/{build,records,refpub,heldout2,reports}` | empty directories | nothing reused |

## Host safety

Every suite run stays inside the frozen counter's sandbox (`env -i PATH=/usr/bin`,
`--no-local` clones, per-run parent dirs, 4 GB `RLIMIT_AS`). No compositor state, config tree
or sibling repo is written. Live session reads, if any, are `hyprctl -j` query verbs only.
Pacman transactions are paused host-wide; no tool install is planned; an install through
`uv tool`/official binary would be recorded in the report.

## Saturation / axes (kept from round 12)

Saturation line 9.0 on every scored sub-axis; stagnation window N=3 rounds without a
capability row. This round's C1, if it lands, enters one capability row
(`rotating held-out mutation gate`); no axis is retired or split.
