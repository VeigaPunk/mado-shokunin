# mado round 100 — plan and pre-file amendments

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`, base
`43309e6af9a3b57f1bc839a826bef1f8eb7495e4` (round-99 closure tip, the non-author verifier
spot-check commit). L1 `MadoR100` (attempt 1). Round contract:
`.ufo/waves/round-100/claims-declaration-r100.md`. This file records the round plan and every
amendment made under the pre-file falsification rule (lane addendum §8 / Amendment 59) BEFORE the
report is filed. Nothing in the declaration above its `## Freeze block` is rewritten; the amendments
below narrow what the round files and each names the wave artifact that forced it.

## Round plan (as executed)

Two claims, two distinct axes, causally separable; no exploratory claim.

- **C1 — coverage (the surface it moves: the PATH-unset default branch of the launch load gate).**
  Round 99's A8 residual: `tools/mado-launchenv.py` models `g_find_program_for_path`'s unset-PATH
  default (`/bin:/usr/bin:.`, `gutils.c:370-382`) but no frozen case reaches it — both
  `path-unset` cases carry an absolute `Exec` and return at `gutils.c:331-357` before the PATH
  source is read. This round freezes a `path-default` case class measured against the installed
  `/usr/bin/gio`, plus a seeded fresh leg and a counted mutant population, and proves the model on
  the whole set. Counter `quality/counters/c1-r100-launchenv-path.py`; predicate
  `PRED-C1-r100-v1`; sourced by S533 (`gutils.c`, re-opened this round).
- **C2 — operability (the surface it moves: the cross-round harm watch's per-leg cap and its
  timing evidence).** Round 99's A9 routed defect: the frozen 28-leg panel's 600 s per-leg cap has
  no headroom and the gate records no per-leg timing, so two legs time out under this host's load
  and the panel reports `mismatches=2`. This round makes elapsed time a gate output, re-freezes the
  panel cap at twice the largest leg measured on this host at committed bytes, and re-runs the full
  panel at committed bytes. Counter `quality/counters/c2-r100-harm-watch.py`; predicate
  `PRED-C2-r100-v1`.
- **Frontier step (§2b).** `corpus/SOURCES.md` census before/after; S533 re-opened with a located
  quote (the sourced claim); mistakes mined into `corpus/lessons/round-100.md` `## Mistakes`;
  one `qual`/`recheck` change logged.
- **Assimilation (§10).** `merge/mado/` re-swept for this round's theme; verdict recorded.
- **considerthese (§10).** At most one unimplemented proposal from `considerthese/2026-11-07.md`
  (proposal 3: a library-semantics port carries a small-domain sweep) mined to a `QUALITY.md`
  criterion, grounded by opening the M95-1 evidence it points at.
- **Record repairs (not claims):** round-99 spot-check routed defects 1 (the off-by-one pointer in
  `corpus/lessons/round-99.md` M99-3 and `corpus/QUALITY.md` 172), 2 (attack-share arithmetic in
  SCORECARD/report), 4 (C1 A8 residual — this round's C1), 5 (unreceipted measured line practice).
- **Wave:** one v1 wave `w1`, 15 seats, band 8–16; ≥25 % attack roles. No planner seat in the wave —
  the L1 holds the canonical planner seat (`PROTOCOL` orchestrator ruling 2026-10-19); the bounded
  planning data-walk rides the two scouts and the connector. No residual call expected.

## Pre-file amendments (Amendment 59)

(empty until the wave returns; each amendment names its triggering artifact under
`.ufo/waves/round-100/`)

## Pre-file amendments (Amendment 59)

Each amendment is the choice "amend the frozen claim down to the enforceable property, citing the
artifact", taken before the report is filed. The frozen text above is not rewritten; the narrowed
sentence is what the round files, and it is quoted in the report and the SCORECARD row.

### A1 — C1's three prose separations are not conjuncts, and separation 3 is false as worded

- **Trigger:** `.ufo/waves/round-100/w1/R100MReviewC1.md` §1a (C1 verdict `falsifies-wording`) and
  `.ufo/waves/round-100/w1/R100MCriticClaims.md` §1.4/F1, §1.5.3.
- **What was false:** the declaration's separation 3 said a bare program in the launch working
  directory is "not found by the same fixture under `PATH=""` when the working directory differs
  from the process cwd". The oracle always launches with cwd = the case root and `Path=` moves only
  the *child's* cwd, so the walk's cwd is the root in both arms: `PATH=""` (one empty entry = the
  process cwd) finds the program too. Measured: `pd-dot-root` (`path: null`) and `pd-empty-root`
  (`path: []`) both launch — they differ only in the argv0 shape (`{root}/./probe` vs
  `{root}/probe`), which is what the frozen labels carry.
- **Narrowed wording (filed):** "the new class separates the unset default from an empty `PATH` by
  the argv0 shape the `.` entry produces (`{root}/./probe` against `{root}/probe`) and from a
  case-private `PATH` by found-vs-`load`-refusal; the *order* of the default's three entries is not
  separable on this surface (no reachable fixture distinguishes `.`-first from `bin/usrbin`-first
  without spawning a host binary)."

### A2 — C1's before-state locator named a line range that does not hold the literal

- **Trigger:** `.ufo/waves/round-100/w1/R100MReviewC1.md` §1b/§8; re-measured by the L1.
- **Measured:** the literal `path = "/bin:/usr/bin:.";` is at `gutils.c:388` (block `:376-389`); the
  absolute-or-slash short-circuit is `:332-357` with the exec/IS_DIR test at `:339-340`; the walk's
  exec test is `:486-487`. Fetch re-opened 2026-11-08, HTTP 200, sha256 `65086c29…3771`.
- **Narrowed wording (filed):** "…`g_find_program_for_path`'s PATH source and its literal default
  (`gutils.c:376-389`, the assignment at `:388`)". No claim conjunct referenced the pointer.

### A3 — the numeric conjuncts do not bound "every case reaches the branch"; the mutants do

- **Trigger:** `.ufo/waves/round-100/w1/R100MReviewC1.md` §2 (verdict `falsifies-number`) and
  `R100MCriticClaims.md` §1.4/F1, §1.5.1/1.5.2/1.5.5.
- **What the counter enforces:** `default_cases`/`default_classes` count *labels* in the pinned case
  file (by the `path-default` prefix), not reachability; the mutant population is anchored anywhere
  in the candidate, not necessarily on the default branch; the fresh leg's class composition is
  unconstrained.
- **Narrowed wording (filed):** "answers every case in agreement with the frozen labels in the
  pinned case file, including a seeded fresh leg and a counted mutant population. The class's
  binding to the branch is carried by the wave's measured mutant matrix, not by this predicate:
  `m1` (default without its trailing `.`), `m2` (unset treated as empty), `m3` (working-dir join
  removed), `m4` (empty entry read as `/bin`), `m5` (IS_DIR half dropped) and `m6` (relative hit
  normalised) are each killed by at least one case
  (`.ufo/waves/round-100/controls/launchenv-mutants-r100-probe.txt`), and `m1`/`m2` survive the
  round-99 case set alone — the measured gap proof."

### A4 — `base_set_default_cases == 0` is a label count, not a reachability proof

- **Trigger:** `R100MCriticClaims.md` §1.4/F3 (and `R100MReviewC1.md` §4).
- **Narrowed wording (filed):** "at the base revision the round-99 case file carries no
  `path-default` label (0 cases) and its two `path-unset` cases give an absolute `Exec`
  (`{root}/probe.sh`), which returns at `gutils.c:332-357` before the PATH source is read; that
  inspection, not the conjunct, is the before-state."

### A5 — the count of two source rows, not a "default" claim

- **Trigger:** `R100MCriticClaims.md` §1.5.7.
- **Narrowed wording (filed):** the round's surface is "the PATH-unset default branch **as exercised
  by frozen cases**"; the branch was already modelled at base (`tools/mado-mime.py:466`, and the
  launchenv tool's own model), so the axis move is the measured case class, never "the branch was
  unknown".

### B1 — C2's "measured elapsed" is a printed field; its truth is carried by the selftest

- **Trigger:** `.ufo/waves/round-100/w1/R100MReviewC2.md` §(b) residual 1 and
  `R100MCriticClaims.md` §2.3.1.
- **Narrowed wording (filed):** "`quality/harm-watch.py` prints an `elapsed_ms` field per leg on the
  human `LEG` line and in `--json`; that the value measures the leg (non-negative, integer,
  monotone across a fast/slow fixture, ≥ the cap on a timeout leg) is carried by the gate's own
  selftest, not by this predicate."

### B2 — the cap is relative to the receipt's values, and the predicate has no upper bound

- **Trigger:** `R100MReviewC2.md` residual 1 (HIGH: the timing pass's own cap was undeclared) and
  `R100MCriticClaims.md` §2.3.2/2.3.3.
- **Narrowed wording (filed):** "`timeout_s` is at least twice the largest `elapsed_ms` value
  recorded in the wave's timing receipt; that receipt's own per-leg cap is `--timeout 7200`
  (pinned in its header), its revision is `43309e6a` and its 28 rows are the timed ids. The
  predicate neither bounds `timeout_s` from above nor requires the receipt's values to equal the
  counter's own run."

### B3 — the 600 s control is a derivation, and the panel is "a 28-leg panel of this census shape"

- **Trigger:** `R100MCriticClaims.md` §2.3.4/2.3.6.
- **Narrowed wording (filed):** "the frozen 600 s cap would be too small for the legs the receipt
  lists (`r92_gate_defects` at 708,014 ms); no 600-second run is delivered by this counting command.
  The panel is a 28-leg frozen panel whose leg rows are byte-identical to the round-99 panel's
  (only `timeout_s` differs), verified by a parsed row comparison."

### B4 — "at committed bytes" is `--rev`, not a worktree reading

- **Trigger:** `R100MCriticClaims.md` §2.3.5.
- **Narrowed wording (filed):** "the counter's own full-panel run at `--rev`
  `219e14f4a89075005b3c4dfa87651356b1e9719c` (committed; the gate bytes are read with `git show`)
  reports `mismatch=0`, and the gate/panel/timing pins were re-derived from that revision
  (`R100MReviewC2.md` residual 4)."

### B5 — one run is an event, not a durability property

- **Trigger:** `R100MReviewC2.md` §(a) and residual 3 (HIGH).
- **Narrowed wording (filed):** the sentence is event-scoped and stays so: "this round's full-panel
  run at the measured revision reports `mismatch=0`"; no claim is made that a later run under a
  different load stays green, and the 2× headroom is the mitigation, not a guarantee.
