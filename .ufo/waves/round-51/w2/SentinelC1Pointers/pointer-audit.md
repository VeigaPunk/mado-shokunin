# Pointer audit — `quality/tool-ledger.md` at `56026fcb9800370ae04bc65952a6567181c398d0`

Seat: `SentinelC1Pointers` (round 51, wave w2, sentinel). Lane: `mado-shokunin`.
Freeze revision: `56026fcb9800370ae04bc65952a6567181c398d0`. Round base: `6ca8c559a4a3d6d361101592116eea2bc7452437`.
Surface: the accountability-pointer clause of PRED-C1-r51 only. No lane file was edited; every fixture was a
throwaway clone under `/fast/scratch/hyaku/mado-r51/SentinelC1Pointers/`, since deleted.

## Method

`audit.py` (shipped here) reads committed bytes with read-only git (`ls-tree`, `show`) and, for every pipe-table
row of the ledger at the freeze revision:

1. parses the row exactly as the two frozen implementations parse it (counter `parse_rows`, checker
   `parse_rows`/`unfenced`; ledger has no fences, both parsers agree on 82 rows);
2. dereferences every backticked pointer token after stripping a `:<line>` / `:<line>-<line>` suffix;
3. applies the checker's `names_basename` regex (`(?<![A-Za-z0-9._-])<basename>(?![A-Za-z0-9_-])`) and,
   separately, the counter's plain substring test (`base.encode() in bytes`), recording where they diverge;
4. when the token carries a line suffix, tests whether the cited line (or range) itself contains the basename;
5. compares the pointer's mention at the round base against the freeze revision to classify provenance.

Per-row output: `pointer-census.md`. Raw: `pointer-audit.json`. Reproduction: `bash` block at the end.

## Result under the frozen sentence

The frozen predicate requires, per population file, "an accountability pointer naming an existing repo file that
contains the file's basename". Measured at the freeze revision:

| check | value |
|---|---|
| ledger rows / population at rev | 82 / 82 |
| rows missing | 0 |
| rows outside the population | 0 |
| pointer tokens that do not dereference | **0** |
| rows whose pointer file lacks the basename | **0** (checker semantics) |
| rows where only the counter's substring test would pass | 0 |
| rows with a `:<line>` suffix | 79 |
| `:<line>` suffix that does **not** contain the basename on the cited line | **0** |
| distinct pointer files / distinct pointer tokens | 12 / 69 |
| tokens reused by more than one row | 10 (max: `PROVINCE.md:20`, 4 rows) |

Frozen command reproduced at the freeze revision

```
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=56026fcb9800370ae04bc65952a6567181c398d0
exit=0
```

(`receipts/freeze-c1-command.txt`; checker alone: `receipts/freeze-checker.txt`.)

**Pointer clause: PASS. No row in the delivered ledger fails dereference, basename-name, or its own line
annotation.** The findings below are limits of the frozen pointer rule and of the ledger's supporting prose, not
a MISS of the frozen sentence as written.

## Pointer classes (measured, not the header's list)

| class | rows |
|---|---|
| `SCORECARD.md` (capability/claim row) | 42 |
| `PROVINCE.md` (ownership/write scope) | 20 |
| `corpus/lessons/*` (round record; r48 ×4, r44 ×2, r25-spotcheck, r41, r43) | 9 |
| `.ufo/waves/round-N/registration.md` (r51 ×3, r40 ×2, r45 ×2, r44 ×1) | 8 |
| `corpus/QUALITY.md` (criterion registration) | 3 |

62/82 rows (75.6 %) resolve into the two mutable aggregate documents `SCORECARD.md` and `PROVINCE.md`;
38 of the 42 `SCORECARD.md` citations land on a table row, 4 on prose. The header's declared class list also
names `corpus/knowledge/*.md`; no row uses that class (an unused declaration, harmless).

## Self-referential and circular pointers

**No file-level cycle exists.** No pointer target is itself a population instrument: all 82 rows point into
documents (`PROVINCE.md`, `SCORECARD.md`, `corpus/**`, `.ufo/**`), so the instrument→pointer graph is a star into
non-instrument files. The obvious cycle (checker → counter → ledger → checker) is avoided by construction: the
counter `quality/counters/c1-r51-ledger.py` names `check-tool-ledger.py` as `DEFAULT_CHECKER`, and the ledger does
not point back at either instrument.

**A document-level cycle does exist, and 3/82 rows resolve only because of round-51 registration prose.** The three
instruments that implement PRED-C1-r51 take `.ufo/waves/round-51/registration.md` as their accountability
pointer:

| ledger line | instrument | pointer | witness line |
|---|---|---|---|
| 117 | `quality/check-tool-ledger.py` | `.ufo/waves/round-51/registration.md` | line 11, "Frozen implementation: `quality/counters/c1-r51-ledger.py` + `quality/check-tool-ledger.py`" |
| 118 | `quality/counters/c1-r51-ledger.py` | `.ufo/waves/round-51/registration.md` | line 9 (the predicate sentence, which *is* the counter's obligation) and line 11 |
| 119 | `quality/counters/c2-r51-dispatch-entry.py` | `.ufo/waves/round-51/registration.md` | line 17, "Frozen implementation: `quality/counters/c2-r51-dispatch-entry.py`" |

Provenance evidence:

- All five files — `quality/tool-ledger.md`, `quality/check-tool-ledger.py`, both counters, and
  `.ufo/waves/round-51/registration.md` — are first added by the **same commit** `56026fcb`
  (`git log --diff-filter=A`). The ledger and its witness for these three rows land atomically; there is no
  earlier revision at which the pointer resolves.
- Those are the only **non-wave** witnesses that exist. `git grep -zF` over `PROVINCE.md SCORECARD.md corpus
  quality tools` at the freeze finds, besides the ledger itself, only the instruments' own files
  (`receipts` reproduced below): no ownership record, no capability row and no knowledge/criterion text names
  `quality/check-tool-ledger.py`, `quality/counters/c1-r51-ledger.py` or
  `quality/counters/c2-r51-dispatch-entry.py`.
- The remaining 79 rows are durable across the round: every pointer file that exists at the round base already
  names its instrument's basename at the base (79/79), so only these three rows are freeze-time inventions.

The cycle is therefore: `registration.md` declares the predicate → the instruments implement and score it →
the ledger certifies the instruments → the ledger's witness for the instruments is `registration.md`. The
witness is the claim statement, and it is written by the same wave that is scored. Under the frozen wording this
is compliant (registration is an existing tracked file that contains the basenames); as accountability it is
self-certification, and it is the exact class this seat was asked to isolate.

## Pointer-integrity holes in the frozen rule (advisory, reproduced)

These are properties of the frozen implementations, demonstrated on clones of the lane at `56026fcb` with one
ledger rewrite committed; the delivered ledger does not exploit them.

| # | finding | fixture | result |
|---|---|---|---|
| F1 | **Self-pointer is a valid pointer.** `quality/tool-ledger.md` is a blob and every row's basename occurs in its own row, so pointing every row at the ledger satisfies both implementations. | `receipts/fixture-allself.txt`, `receipts/fixture-allself-counter.txt` | all 82 rows repointed to `quality/tool-ledger.md`: checker `bad_pointer=0 verdict=TARGET_MET` exit 0; frozen counter `bad_pointer=0 verdict=TARGET_MET` exit 0 |
| F2 | **A longer dotted filename counts as "naming" the instrument.** The checker's negative lookahead excludes `[A-Za-z0-9_-]` but not `.`, contradicting its docstring "as a name, not as a fragment of a longer filename". | `receipts/fixture-dotted.txt` | target containing only `check-tool-ledger.py.orig` → `bad_pointer=0 verdict=TARGET_MET` |
| F3 | **`:<line>` is never validated** (both implementations strip it). An out-of-range anchor passes. | `receipts/fixture-anchor.txt` | `SCORECARD.md:999999` → `bad_pointer=0 verdict=TARGET_MET` |
| F4 | **Counter and checker disagree on fragments.** Counter's own metric is a substring test, the checker's is name-bounded. | `receipts/fixture-fragprefix.txt`, `receipts/fixture-fragprefix-counter.txt` | target containing only `xcheck-tool-ledger.py`: counter prints `bad_pointer=0`, checker prints `bad_pointer=1`; final verdict MISS only because the counter's `max` clause requires the checker to agree |

F1 makes the pointer clause unfalsifiable in principle (it can never discriminate a genuine witness from the
ledger's own bytes). F2–F4 are single-line defects each; F4 is currently masked by the agreement clause, so it
would bite only if the checker were relaxed.

## Data-artifact evidence defect

The ledger header states: "Five superseded v1 counters have no lane-level document naming them; their
registration is the only tracked file that does, and it is recorded rather than papered over." That sentence is
false for all five rows it describes. Each superseded counter is named, with its supersession reason, by its own
v2 successor — a lane-level tracked instrument:

```
quality/counters/c1-r40-live-v2.py:4        "v2 re-registers PRED-C1-r40-v1 (quality/counters/c1-r40-live.py, frozen 5e7e885)"
quality/counters/c1-r44-geometry-states-v2.py:5  "... quality/counters/c1-r44-geometry-states.py), because wave w1 found:"
quality/counters/c2-r45-monitor-entry-v2.py:5    "... quality/counters/c2-r45-monitor-entry.py). Why: wave w1/CritC2Forgery had nine"
```

and the same holds for `c2-r40-forms-entry.py` and `c1-r45-monitors.py` (`code` grep over
`PROVINCE.md SCORECARD.md corpus quality tools`). So the five registration pointers are a *choice* to avoid
instrument→instrument edges, not the only available witness; the wording overstates. This is an evidence
statement inside the scored artifact, not a predicate failure.

## Severity

| severity | finding |
|---|---|
| medium | F1 — self-pointer satisfies the frozen pointer clause under both implementations (clause is vacuous; delivered ledger does not use it) |
| low–medium | 3/82 rows (3.7 %) — exactly the three instruments that carry C1's own machinery — resolve only through round-51 registration prose created in the same commit as the ledger; no independent lane-level witness exists |
| low | header claim "registration is the only tracked file" falsified for 5/5 superseded counters (v2 successors name them) |
| low | F2 — dotted longer filename accepted as naming; F3 — anchors unvalidated (all 79 currently accurate); F4 — counter's own pointer metric is substring-based |

## Smallest remediations (future amendment — not applied)

1. Reject `quality/tool-ledger.md` and the row's own file as pointer tokens (one predicate in `pointer_tokens`
   in both implementations); closes F1 and the self-file variant.
2. For files under `quality/`, require at least one pointer target outside `.ufo/` and outside
   `quality/tool-ledger.md`; closes the round-51 registration-only class for future rows.
3. Change the checker's lookahead to `(?![A-Za-z0-9_.-])` (one character); closes F2.
4. When a `:<line>` suffix is present, require it to name the basename on that line; closes F3 and makes the
   ledger header's annotation claim enforceable.
5. Have the counter reuse the checker's `names_basename` instead of `base.encode() in bytes`, or drop the claim
   that it measures pointers independently; closes F4.
6. Point the five superseded rows at their v2 successors with the supersession note, or reword the header.

## Reproduction

```
# pointer census (read-only git; writes nothing)
TMPDIR=/fast/scratch/hyaku/mado-r51/SentinelC1Pointers \
  python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-51/w2/SentinelC1Pointers/audit.py

# frozen command at the freeze revision (scratch clone, no lane writes)
cd /home/vgpnk/Projects/shokunin/mado-shokunin
TMPDIR=<scratch> python3 -I quality/counters/c1-r51-ledger.py \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
  --rev 56026fcb9800370ae04bc65952a6567181c398d0 --work <scratch>

# fixture method per finding: git clone --shared <lane> <scratch>/repo &&
#   git -C <scratch>/repo checkout --detach 56026fcb && assert toplevel == repo dir,
#   rewrite one pointer cell, commit with a fixture identity, then run
#   python3 -I <repo>/quality/check-tool-ledger.py --repo <repo> --rev HEAD
```

Receipts: `receipts/freeze-c1-command.txt`, `receipts/freeze-checker.txt`,
`receipts/pointer-audit-summary.txt`, `receipts/fixture-{allself,allself-counter,dotted,anchor,fragprefix,fragprefix-counter}.txt`.
