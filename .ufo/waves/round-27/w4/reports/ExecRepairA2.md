# ExecRepairA2 — round 27 wave w4, C2 repair seat (suite A, independent design)

CANDIDATE /fast/scratch/hyaku/mado-r27/repair/ExecRepairA2/candidate-counter-selftest.py
sha256:aa0e14d160b8429b945f12329e5673a1d484986d1b617a05920a92e77a1d4898
(base: committed quality/counter-selftest.py sha256:7fd94b0431849d1be7dc99e120c2f5bd0105c6a1d122e9cd1a3327d30ef3c587)

## What this seat did

An independent repair of suite A (`quality/counter-selftest.py`, the gate over the round-26
counters `c1/count-v2.py` and `c2/count.py`). The three named survivors of the round-27
measurement-1 receipt (`H/HeldC2:HeldC2-extra-disjunction`, `H/HeldC2:HeldC2-unstable-conjunction`,
`H/HeldC2:HeldC2-embed-boundary`, all `suite=A rc=0 SURVIVED`) are mutants of the round-26
**bind** counter `.ufo/waves/round-26/c2/count.py`. The held-out directory
`/fast/scratch/hyaku/mado-r27/heldout/` was **never read** by this seat; the only signal used
is the three public class names in `evidence/c2-after-48b9434a.txt`.

The committed suite's blind spots were located by building my own class mutants and running
the committed suite against them: **11 of 12 of my class mutants survived** the committed
suite, confirming the gap without any held-out bytes. (The twelfth, `a2-unstable-conjunction-eq`,
is caught by the committed suite already; it is kept in the set as a control.)

## Per-class evidence

Every class mutant is a copy of the pristine bind counter
(`.ufo/waves/round-26/c2/count.py`, sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8)
with one text substitution. The mutation rows are in `mutants.json`; the subject copies live
next to the pristine counter in the sandbox clone so the counter's own sha-pinned imports
still resolve.

### Class 1 — extra-disjunction

The counter's per-case verdict is `verdict[lab] = (nm == 0 and ne == 0, info, len(exp))`
(`nm` = missing count, `ne` = extra count). A disjunction here accepts a table that carries
entries the truth does not have. The committed suite's per-field probes cannot see this: a
changed field makes one entry missing **and** one entry extra at the same time, so both
counts stay non-zero and the mutant's disjunction never changes the verdict.

New checks: `c2-extra-one`, `c2-extra-two` (the tool reports one / two entries too many),
`c2-missing-one` (the tool omits one entry). Each breaks exactly one side of the conjunction.

| mutant | change | committed suite | repaired suite |
|---|---|---|---|
| `a2-extra-disjunction-or` | `nm == 0 and ne == 0` → `nm == 0 or ne == 0` | **SURVIVED** (48/48) | KILLED — FAILED c2-extra-one, c2-extra-two, c2-missing-one |
| `a2-extra-disjunction-or-swap` | → `ne == 0 or nm == 0` | **SURVIVED** (48/48) | KILLED — FAILED c2-extra-one, c2-extra-two, c2-missing-one |
| `a2-extra-disjunction-le1` | → `nm == 0 and (ne == 0 or ne == 1)` | **SURVIVED** (48/48) | KILLED — FAILED c2-extra-one |
| `a2-extra-disjunction-le` | → `nm == 0 and ne <= 1` | **SURVIVED** (48/48) | KILLED — FAILED c2-extra-one |

### Class 2 — unstable-conjunction

The counter guards the two BASE oracle runs with `n1, n2 = V3.compare(base, r2["binds"])[:2]`
followed by `if n1 or n2:` → `die("ORACLE_UNSTABLE ...")`. A conjunction here (`n1 and n2`)
still fires on the committed suite's drift probe, because that probe replaces one field, which
differs in **both** directions at once (one entry missing and one extra), so both counts are
non-zero. A second run whose table differs by one *added* entry leaves exactly one of the two
counts non-zero, and there the conjunction does not fire.

New check: `c2-drift-superset` — the second BASE oracle run returns the truth plus one
extra entry.

| mutant | change | committed suite | repaired suite |
|---|---|---|---|
| `a2-unstable-conjunction-and` | `if n1 or n2:` → `if n1 and n2:` | **SURVIVED** (48/48) | KILLED — FAILED c2-drift-superset |
| `a2-unstable-conjunction-ne` | → `if n1 != 0 and n2 != 0:` | **SURVIVED** (48/48) | KILLED — FAILED c2-drift-superset |
| `a2-unstable-conjunction-eq` | → `if n1 == n2:` | KILLED (23/48) | KILLED — FAILED c2-perfect, c2-field-*, … |

### Class 3 — embed-boundary

The counter scans the base table for embed-eligible strings with
`if isinstance(e.get(f), str) and len(e[f]) >= EMBED_MIN` and `EMBED_MIN = 12`, then counts
those strings found in the tool's bytes. The committed suite's embed probes use a 40-character
string, which is eligible under any threshold near 12, so a threshold moved by one character
in either direction is invisible. The two sides of the boundary must be pinned separately: a
string of exactly 12 characters must be a hit, a string of exactly 11 characters must not be.

New checks: `c2-embed-at-threshold` / `c2-embed-below-threshold` (arg field) and
`c2-embed-desc-at-threshold` / `c2-embed-desc-below-threshold` (description field).

| mutant | change | committed suite | repaired suite |
|---|---|---|---|
| `a2-embed-boundary-gt` | `>= EMBED_MIN` → `> EMBED_MIN` | **SURVIVED** (48/48) | KILLED — FAILED c2-embed-at-threshold, c2-embed-desc-at-threshold |
| `a2-embed-boundary-ge1` | → `>= EMBED_MIN + 1` | **SURVIVED** (48/48) | KILLED — FAILED c2-embed-at-threshold, c2-embed-desc-at-threshold |
| `a2-embed-boundary-min13` | `EMBED_MIN = 12` → `13` | **SURVIVED** (48/48) | KILLED — FAILED c2-embed-at-threshold, c2-embed-desc-at-threshold |
| `a2-embed-boundary-min11` | `EMBED_MIN = 12` → `11` | **SURVIVED** (48/48) | KILLED — FAILED c2-embed-below-threshold, c2-embed-desc-below-threshold |
| `a2-embed-boundary-min10` | `EMBED_MIN = 12` → `10` | **SURVIVED** (48/48) | KILLED — FAILED c2-embed-below-threshold, c2-embed-desc-below-threshold |

### Full class sweep (12 mutants)

```
SUMMARY total=19 unexpected=0        # out/verify/results.json — 12 class mutants + 6 benign edits + pristine
```

All 12 class mutants exit non-zero under the repaired suite; the pristine counter and all
six behaviour-preserving edits exit 0.

### Behaviour-preserving edits stay green

Six benign edits of the bind counter (`benign.json`): the verdict rewritten by De Morgan and
by an identity negation, the instability guard rewritten by De Morgan and by an identity
negation, the embed test rewritten by De Morgan, and a comment insertion. All six exit 0 with
`SELFTEST pass=56 total=56` under the repaired suite — the new checks are behavioural and
do not pin the subject's bytes, so an equivalent rewrite is still recognised as correct.

## Green + W transcript

### Green runs (9 rows: pristine and both public behaviour-preserving edits per subject)

```
GREEN count-v2.py            pristine  suite=A rc=0 SELFTEST pass=56 total=56
GREEN count-v2.py            comment   suite=A rc=0 SELFTEST pass=56 total=56
GREEN count-v2.py            assign    suite=A rc=0 SELFTEST pass=56 total=56
GREEN count.py               pristine  suite=A rc=0 SELFTEST pass=56 total=56
GREEN count.py               comment   suite=A rc=0 SELFTEST pass=56 total=56
GREEN count.py               assign    suite=A rc=0 SELFTEST pass=56 total=56
GREEN check-population.py    pristine  suite=B rc=0
GREEN check-population.py    comment   suite=B rc=0
GREEN check-population.py    assign    suite=B rc=0
```

### W mutants — 15/15 exit non-zero

Suite A judges the two counters, suite B judges the population checker; each W mutant is
applied to its own subject and the suite that judges that subject is run
(`out/verify_w/w-results.json`).

```
W c1-drop-bezier             suite=A rc=1    KILLED
W c1-accept-nonjson          suite=A rc=1    KILLED
W c1-pass-90pct              suite=A rc=1    KILLED
W c1-skip-base-guard         suite=A rc=1    KILLED
W c2-accept-nonjson          suite=A rc=1    KILLED
W c2-pass-90pct              suite=A rc=1    KILLED
W c2-skip-base-guard         suite=A rc=1    KILLED
W c2-embed-min-1000          suite=A rc=1    KILLED
W c2-drop-arg                suite=A rc=1    KILLED
W q37-M1-ignore-registered   suite=B rc=1    KILLED
W q37-M2-case-anywhere       suite=B rc=1    KILLED
W q37-M3-drop-denominator    suite=B rc=1    KILLED
W q37-M4-first-pred-only     suite=B rc=1    KILLED
W q37-M5-case-plus-one       suite=B rc=1    KILLED
W q37-M6-unreadable-exit-0   suite=B rc=1    KILLED
W_SUMMARY killed=15/15
```

### Frozen round-27 C2 counter v2 with this candidate

`python3 -I .ufo/waves/round-27/c2/count-v2.py 86f7355… --suite-a-file <candidate> --jobs 6`
(receipt `out/counter-verified.txt`):

```
SUITE A override:…/candidate-counter-selftest.py at quality/counter-selftest.py sha256:aa0e14d1…
SUITE B quality/population-suite.py@86f7355baed9 sha256:99e7d876c1fcf2585354a22eff9d1c674c902ad1108e19ea50c9caa49eb3046c
CASE GREEN pristine                                     suite=A rc=0 PASS | exit=0
CASE GREEN pristine                                     suite=B rc=0 PASS | exit=0
CASE GREEN comment:count-v2.py                          suite=A rc=0 PASS | exit=0
CASE GREEN assign:count-v2.py                           suite=A rc=0 PASS | exit=0
CASE GREEN comment:count.py                             suite=A rc=0 PASS | exit=0
CASE GREEN assign:count.py                              suite=A rc=0 PASS | exit=0
CASE GREEN comment:check-population.py                  suite=B rc=0 PASS | exit=0
CASE GREEN assign:check-population.py                   suite=B rc=0 PASS | exit=0
CASE W     W:c1-drop-bezier                             suite=A rc=1 KILLED | exit=1
CASE W     W:c1-accept-nonjson                          suite=A rc=1 KILLED | exit=1
CASE W     W:c1-pass-90pct                              suite=A rc=1 KILLED | exit=1
CASE W     W:c1-skip-base-guard                         suite=A rc=1 KILLED | exit=1
CASE W     W:c2-accept-nonjson                          suite=A rc=1 KILLED | exit=1
CASE W     W:c2-pass-90pct                              suite=A rc=1 KILLED | exit=1
CASE W     W:c2-skip-base-guard                         suite=A rc=1 KILLED | exit=1
CASE W     W:c2-embed-min-1000                          suite=A rc=1 KILLED | exit=1
CASE W     W:c2-drop-arg                                suite=A rc=1 KILLED | exit=1
CASE W     W:q37-M1-ignore-registered                   suite=B rc=1 KILLED | exit=1
CASE W     W:q37-M2-case-anywhere                       suite=B rc=1 KILLED | exit=1
CASE W     W:q37-M3-drop-denominator                    suite=B rc=1 KILLED | exit=1
CASE W     W:q37-M4-first-pred-only                     suite=B rc=1 KILLED | exit=1
CASE W     W:q37-M5-case-plus-one                       suite=B rc=1 KILLED | exit=1
CASE W     W:q37-M6-unreadable-exit-0                   suite=B rc=1 KILLED | exit=1
PRED-C2-r27-v2 green=8/8 b_valid=0 w_killed=15/15 h_killed=0/0 h_need=0 h_valid=0 h_min_per_subject=0 invalid=0 verdict=TARGET_MISSED
```

The run above carries **no** `--heldout`/`--seal`, so `h_valid=0` and the overall verdict is
TARGET_MISSED by construction; the H rows are the L1's to measure at the new revision. The
green (8/8) and W (15/15) figures are what this seat is responsible for.

## Diff summary vs the committed suite

`diff -u` against the committed `quality/counter-selftest.py`: **5 hunks, 119 lines added,
2 lines removed** (both removed lines are docstring text; no code, no check, no CLI option
was removed). `out/diff.patch`.

* CLI unchanged: `--c1 PATH --c2 PATH --rev REV` (plus the pre-existing `--scratch`, `--keep`).
* `REQUIRED` grows from 47 to 55 entries; `TOTAL` is `len(REQUIRED) + 1` as before, so the
  fixed-inventory gate still catches a silently deleted check.
* Executed check inventory: committed 48 → repaired 56, **no check deleted**, the 48
  committed checks keep their names and their order; the 8 new checks are appended.
* The suite stays behavioural: no subject hash, AST or byte pattern is pinned, no mutant
  text is blocklisted, and nothing about the process, path, environment or timing is
  inspected. The only `sha256` use is printing the suite's own digest and the subjects' for
  traceability.
* Docstring: the check list and count were updated (the committed file's own count line said
  "45 behavioural probes" while it ran 47; the repaired file's line matches its runtime
  `len(REQUIRED)` = 55).

## Determinism and safety

* The repaired suite was run five times against the pristine counter and the three
  unstable-conjunction mutants: identical exit codes every time (`out/stab`).
* The suite is offline: no Hyprland, no compositor, no display, no network, no `/dev/dri`.
  The counters' `check_build`/`coredumps`/`snapshot`/`oracle`/`run_tool` are all replaced with
  synthetic fakes, so no compositor, `hyprctl`, `tinywl` or `coredumpctl` call happens. All
  scratch lives in one `mkdtemp` under `TMPDIR` and is removed at the end.
* The candidate runs correctly inside the counter's own bubblewrap sandbox
  (`/home` and `/fast` hidden except the run directory, cleared environment): the frozen
  counter's own run above exercises exactly that path.
* No Hyprland was started by this seat. Hyprland coredump count on the host: unchanged by
  this seat (no compositor was launched).
* No tool or package was installed or updated by this seat (none was needed).
* **The lane was never mutated.** All runs used a `--no-local` clone under
  `/fast/scratch/hyaku/mado-r27/repair/ExecRepairA2/clone`; the lane's `git status` shows
  only other seats' work (`SCORECARD.md`, `.ufo/waves/round-27/drafts/report-notes.md`,
  `.ufo/waves/round-27/w3/`, `.ufo/waves/round-27/w4/`). The one file this seat wrote in
  the lane is this report.

## Artefacts (all under /fast/scratch/hyaku/mado-r27/repair/ExecRepairA2/)

| path | what |
|---|---|
| `candidate-counter-selftest.py` | the repaired suite (sha256:aa0e14d1…) |
| `mutants.json` / `benign.json` | the 12 class mutants (4 extra-disjunction, 3 unstable-conjunction, 5 embed-boundary) and 6 benign edits, as `{"id","class","file","old","new","subject_copy","subject_sha256"}` rows |
| `make_mutants.py` | builds both families from the pristine counter |
| `run_suite.py` | runs a suite over the mutants and the benign edits (`out/verify/results.json`) |
| `run_w.py` | applies each W row and runs the suite that judges its subject (`out/verify_w/w-results.json`) |
| `out/verify/`, `out/verify_w/`, `out/counter-verified.txt`, `out/diff.patch` | receipts |
| `out/base_ext/` | the committed suite over the same 19 subjects (the "before" evidence: 11 survivors) |

## Limits and risks

* The held-out set was not read. This seat proves its three named classes are killed by its
  own class designs; it cannot certify the L1's sealed H rows. If the sealed
  `HeldC2-embed-boundary` mutant shifts the threshold by more than one character, the
  11/12-character probes may not reach it; the probes are placed exactly on the documented
  boundary (EMBED_MIN = 12) so any shift of one is caught, and shifts of two or more are
  caught by the other side of the pair.
* The repaired suite's extra probes widen the C2 subject's behaviour surface slightly: they
  assert that a table with one extra entry, two extra entries or one missing entry is a
  mismatch. A counter that legitimately accepted such a table would now fail — the
  round-26 counter does not, and the pristine counter passes all 56 checks.
* The `c2-drift-superset` probe depends on the counter comparing the two BASE runs with a
  multiset difference; if a future counter compared them as ordered lists, the probe would
  still fire (the added entry changes the length), so the probe is robust to that change.
* Suite B (`quality/population-suite.py`) is outside this seat's scope and was not modified;
  its six W kills are reproduced here only as part of the 15/15 figure.

Report: .ufo/waves/round-27/w4/reports/ExecRepairA2.md
