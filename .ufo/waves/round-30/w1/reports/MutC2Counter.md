# MutC2Counter — mutation test of the C2 counter (report only)

Seat: mutation-tester, mado round 30 wave 1. Date: 2026-10-24.
Target of attack: `PRED-C2-r30` as implemented by
`.ufo/waves/round-30/c2/count.py` at data commit
`446dc3966193c81e64896f4880a19a4bd249255b` ("round-30 data"), baseline
`8f51071b5bc44c815eeb5da76bb7f1947994ffb8`.

Scratch copy: `git clone /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mut_c2`
(throwaway; all mutants applied there). The lane itself was never written:
lane `count.py` sha256 stayed
`cbc2941b81264a1ed04978c2680ba5f4fdf9f7db228330a4568480f6c5248d73`, lane
`git status` shows only the untracked wave-1 report tree. No subagents, no
pacman, no tool installs, no compositor/config touch.

Detector (unchanged for pristine, mutated and restored bytes), run from the
clone root:

```
python3 -I .ufo/waves/round-30/c2/count.py 446dc396
```

Verdict rule under test: `TARGET_MET` (exit 0) iff `unresolved_active == 0`
and literal fraction ≥ 0.70. A mutant is **killed** when the detector's
verdict at `446dc396` differs from pristine; **survived** when it does not
(a coverage finding, not a contract change).

## Baseline (pristine bytes)

Pristine sha256 `cbc2941b81264a1ed04978c2680ba5f4fdf9f7db228330a4568480f6c5248d73`
(identical to `git show HEAD:.ufo/waves/round-30/c2/count.py`).

| rev | literal | superseded | active | resolved_active | verdict | exit |
|---|---|---|---|---|---|---|
| `8f51071b` | 28/40 = 0.7000 | `[20]` | 39 | 31 (0.7949) | TARGET_MISSED | 1 |
| `446dc396` | 40/52 = 0.7692 | `[1,2,3,4,5,18,19,20,32,38,39,40]` | 40 | 40 (1.0000) | TARGET_MET | 0 |

Base run names `UNRESOLVED criterion {1,2,3,4,5,38,39,40}: no citation` —
matches the registered control K2.

## Mutants, predicted vs actual (scored at `446dc396`)

| # | Mutation | mutant sha256 | predicted | actual | verdict |
|---|---|---|---|---|---|
| M1 | superseded-set computation dropped (`superseded` stays empty) | `13e655f7…c8c76f` | flip → MISSED | `superseded=[]`, active 52, resolved 44 (0.8462), 8 UNRESOLVED (1–5, 38–40) → **TARGET_MISSED**, exit 1 | **KILLED** |
| M2 | `PATH_RE` existence loop removed (dead paths no longer checked) | `8106acd5…1f7610` | keep → MET (survives) | active 40, resolved 40 (1.0000) → **TARGET_MET**, exit 0; identical to pristine | **SURVIVED** |
| M3a | descending compound treated as a range: `if b:` → `range(a,b+1)` is empty for `M28-1`/`M30-1`, so zero id patterns (vacuous pass) | `0e799964…b2cb2b` | keep → MET (survives; vacuous) | active 40, resolved 40 → **TARGET_MET**, exit 0 | **SURVIVED** |
| M3b | descending compound expanded as an ascending span `min..max` (`M28-1` → M1…M28, `M30-1` → M1…M30) | `6fc40ec2…329524` | flip → MISSED | active 40, resolved 27 (0.6750), 13 UNRESOLVED (33–36, 41–45, 49–52; e.g. `id \bM0*27\b absent in corpus/lessons/round-30.md`) → **TARGET_MISSED**, exit 1 | **KILLED** |
| M4 | anchor-word check removed from the `ANCH_RE` branch | `cfc1fb23…b2ab8` | keep → MET (survives) | active 40, resolved 40 (1.0000) → **TARGET_MET**, exit 0 | **SURVIVED** |

Three of five score as survivors against this detector; two are killed. The
kills are the mutations that remove a *guard whose input shape is present in
the data commit* (superseded rows; ascending-range ids). The survivors each
remove a guard whose triggering shape is absent at `446dc396`.

Notable detail on M1: dropping supersession both inflates the denominator
(52 vs 40) and inflates the numerator (44 vs 40, because grounded-but-
superseded lines 18, 19, 20, 32 re-enter). The denominator effect dominates:
the 8 uncited seed criteria are enough to keep the predicate red. The kill is
therefore robust to the numerator inflation, not accidental.

## Are the survivors real mutants? (discrimination probes)

Survival above means "the data commit does not exercise this guard", not
"the mutation is semantically inert". Three scratch git repos under
`/tmp/probe_*` each commit one synthetic `corpus/QUALITY.md`; pristine and
each survivor mutant were run against the same probe revision.

| Probe input | pristine | M2 | M4 | M3a |
|---|---|---|---|---|
| `1. Dead-path probe (lesson: lessons/round-99.md)` (file absent) | MISSED, exit 1, `missing corpus/lessons/round-99.md` | **MET, exit 0** | MISSED | MISSED |
| `1. Dead-anchor probe (lesson: lessons/round-12.md#not-a-real-anchor M1)` (anchor absent, `M1` present) | MISSED, exit 1, `anchor '#not-a-real-anchor' absent` | MISSED | **MET, exit 0** | MISSED |
| `1. Descending-compound probe (lesson: lessons/round-28.md#mistakes M28-1)` (`M1` present, `M28-1` absent) | MISSED, exit 1, `id \bM28-1\b absent` | MISSED | MISSED | **MET, exit 0** |

Answers to the itemized questions:

1. **(1) denominator inflation:** computed supersession is load-bearing at
   `446dc396`; removing it flips `TARGET_MET → TARGET_MISSED`. 12 superseded
   rows, 8 of them uncited, drive the flip.
2. **(2) does a dead path resolve?** Under M2, yes: a criterion citing
   `lessons/round-99.md` with no such file reports `TARGET_MET` (exit 0)
   where pristine reports `missing corpus/lessons/round-99.md` (exit 1).
   At `446dc396` every plain `lessons/<file>` citation happens to exist, so
   the predicate never exercises this check → survivor.
3. **(3) `M28-1` as range:** the empty-range reading (M3a) **vacuously
   passes** — the id list becomes empty and no id is checked; the
   ascending-span reading (M3b) **fails hard** (spurious ids `M1…M28` /
   `M1…M30`). Descending compounds at the data commit sit on active
   criteria 41–45 (`M30-1`), 49–51 (`M28-1`, `M28-2`, `M28-3`) and 52
   (`M30-2`), plus superseded 38–40 and the criterion-30 header. The lesson
   files literally carry those spellings (`round-28.md` has `M28-1/2/3`,
   `round-30.md` has `M30-1/2`), so pristine resolves them via the literal
   `\bM<a>-<b>\b` branch; M3a deletes exactly those nine active id checks yet
   the verdict stays `TARGET_MET`, while M3b (which turns each compound into
   an ascending span) is killed with 13 unresolved criteria.
4. **(4) anchor check removed:** survives; every anchored citation at
   `446dc396` has its anchor word present, so the check never fires in the
   scored run. The probe shows the removal is detectable on an absent anchor.

## Coverage findings (no contract change requested)

- The registered predicate is exercised end-to-end at the data commit, and
  its two decisive guards (supersession, ascending-range id expansion) are
  each killed by a single-line mutation. That is genuine bite for the
  supersession half of the rubric.
- The file-existence leg, the anchor-word leg, and the descending-compound
  literal leg are **not discriminating at the scored revision**: three
  independent one-line deletions keep `TARGET_MET`. Each leg is exercised
  only on positive inputs (every cited file exists, every anchor word is
  present, every compound id resolves literally), so no active criterion
  would fail if the leg were missing. The registration's kill rule ("any
  UNRESOLVED active criterion") therefore does not by itself guarantee these
  legs work — a future revision can cite a missing file or absent anchor and
  still be credited unless a negative control (a criterion with a dead
  path/anchor) is run. This is reported as a coverage gap, not as a defect
  in the registered claim: at `446dc396` every active citation genuinely
  resolves, and the pristine-vs-probe matrix proves the guards fire when
  triggered.
- Suggested (not applied) guard for a future round: extend the counter's
  control receipt with one negative fixture per leg, as the probes above do.

## Restoration evidence

- Clone working bytes restored from `/tmp/count_pristine.py` after every
  mutant: sha256 `cbc2941b81264a1ed04978c2680ba5f4fdf9f7db228330a4568480f6c5248d73`.
- `git show HEAD:.ufo/waves/round-30/c2/count.py | sha256sum` =
  `cbc2941b81264a1ed04978c2680ba5f4fdf9f7db228330a4568480f6c5248d73` →
  restored bytes equal committed bytes.
- `git status --porcelain` in `/tmp/mut_c2`: empty.
- Post-restore detector: `446dc396 → TARGET_MET, exit 0`;
  `8f51071b → TARGET_MISSED, exit 1` — identical to the pristine baseline.
- Mutant fixtures retained read-only at `/tmp/m{1,2,3a,3b,4}.py` (hashes
  above) for re-scoring; probes at `/tmp/probe_{path,anchor,compound}`.

## Method notes

- Each mutant was a single behavior-bearing edit applied to the pristine
  file in the throwaway clone, scored, then the exact bytes restored before
  the next mutant; no mutant was scored against another mutant's tree.
- Verdicts quoted with their exit status; a baseline failure would have been
  inconclusive, but both baseline runs reproduced the registered values
  exactly (28/40 & 31/39 MISSED at base; 40/52 & 40/40 MET at data).
