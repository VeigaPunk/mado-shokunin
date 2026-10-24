# ExecFreezeSmoke — independent re-run of the freeze smoke at `451e8b3c`

RUNNER item. Read-only: no lane file was written except this report; scratch
outputs lived under `/tmp/efs`. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`, tip at run time
`92d3c8676f4801b2ed2692cf45280796c166c88c` (the data commit had already
landed), smoke revision
`451e8b3c7ee3a422bfcc0251ebbc92ace0815ce9`.

## Provenance of what was run

| Input | Value |
|---|---|
| Literal fence source | `SCORECARD.md` lines 70–89 as committed at freeze (`git show 451e8b3c:SCORECARD.md`), extracted verbatim; exactly one `REV="${REV:` block exists at that revision |
| Fence script SHA-256 | `8b59b503805396b514cb4e009981d6a1837a7898c368afff68e25eb5704a7b88` — identical to the erratum-documented script hash (`SCORECARD.md:194`), so the block ran unchanged |
| C2 counter | `.ufo/waves/round-30/c2/count.py`, worktree blob `74a4859d6ab2921900082b093ce315594972c708` = freeze blob (byte-identical) |
| C3 gate | `quality/check-index.py`, worktree blob `df01b20fa2c45ddee954da1841e2519f7e7abd4d` = freeze blob (byte-identical) |
| Corpus state under measurement | `corpus/QUALITY.md` blob `7568c7cc…` and `corpus/README.md` blob `3f6761d6…` are the same at base `8f51071b` and at freeze `451e8b3c` — the freeze smoke measures the base corpus bytes |
| Interpreter | Python 3.14.8, `-I` isolation on both Python invocations |
| Hermeticity | all three read committed bytes (`git show`/`ls-tree` at the named rev); none depends on the dirty worktree. `--rev` mode of the gate is read-only (its only `open(…,"w")` calls are inside `selftest()`'s `TemporaryDirectory`) |

## Commands and full outputs

Commands, verbatim, from the lane root:

```
REV=451e8b3c7ee3a422bfcc0251ebbc92ace0815ce9 bash /tmp/efs/fence.sh
python3 -I .ufo/waves/round-30/c2/count.py 451e8b3c
python3 -I quality/check-index.py --rev 451e8b3c7ee3a422bfcc0251ebbc92ace0815ce9 --repo .
```

Full stdout (stderr empty for all three), exit codes recorded in-line. This
block is the retained evidence for this item:

```
=== freeze smoke at 451e8b3c ===
--- C1 fence at freeze ---
revision=451e8b3c7ee3a422bfcc0251ebbc92ace0815ce9 indexed=41/43 missing=2 dangling=0 duplicates=0 coverage=9.5349/10
missing: knowledge/mutation-testing-r28.md
missing: knowledge/workspace-rules-r27.md
EXIT=1
--- C2 at freeze ---
counter=c2-grounding-r30 rev=451e8b3c
METRIC literal lines=28/40 fraction=0.7000
METRIC superseded=[20]
METRIC active=39 resolved_active=31 fraction=0.7949
UNRESOLVED criterion 1: no citation
UNRESOLVED criterion 2: no citation
UNRESOLVED criterion 3: no citation
UNRESOLVED criterion 4: no citation
UNRESOLVED criterion 5: no citation
UNRESOLVED criterion 38: no citation
UNRESOLVED criterion 39: no citation
UNRESOLVED criterion 40: no citation
LINE 20 superseded excluded
PRED-C2-r30 verdict=TARGET_MISSED
EXIT=1
--- C3 at freeze ---
MADO_INDEX: rev=451e8b3c7ee3a422bfcc0251ebbc92ace0815ce9 indexed=41/43 missing=2 dangling=0 duplicates=0 coverage=9.5349/10
missing: knowledge/mutation-testing-r28.md
missing: knowledge/workspace-rules-r27.md
EXIT=1
```

Per-counter stdout line counts and hashes: C1 3 lines
`159921178fa9394a0b8423d6fd1fde7f81b1c9bd014d4debefab1949ef86daf4`; C2 14
lines `59da6de3f36b54d021c3213d86840594faf021db0744b7b8c47bfa99c48951d8`; C3 3
lines `c15937b0ec3d9b6bd6ded5b8e255b1ce7d5274dde08c9652da07ac91abb13d80`.
Exit codes 1 / 1 / 1.

## Byte-for-byte diff against `evidence/freeze-smoke-451e8b3c.txt`

**Result: not byte-identical.** The receipt holds 14 lines; the re-run
transcript holds 27. Twelve stdout lines are absent from the receipt and one
recorded exit line has no counterpart. `diff -U0` against my transcript:

| Receipt (evidence) line | Re-run transcript line(s) | Difference |
|---|---|---|
| 3 (C1 `revision=…` line) | 3 | equal |
| — | 4–5 | absent from receipt: both `missing: knowledge/…` rows |
| 4 (`EXIT=1`, C1) | 6 | equal in value |
| 5 (`--- C2 at freeze ---`) | 7 | equal |
| — | 8–17 | absent from receipt: `counter=…`, the three `METRIC …` lines, and `UNRESOLVED criterion {1,2,3,4,5,38}` |
| 6–9 | 18–21 | equal (UNRESOLVED 39, UNRESOLVED 40, LINE 20, verdict) |
| — | 22 | absent from receipt: C2 `EXIT=1` (the receipt records no C2 exit code at all) |
| 10 | 23 | equal |
| 11–13 | 24–26 | equal (C3 is recorded in full) |
| 14 (`EXIT=1`, C3) | 27 | equal in value |

Reconstruction check: taking C1's first line, C2's last four lines matching
`^(UNRESOLVED|LINE|PRED)` with no exit line, and C3's complete stdout plus
`EXIT=1` reproduces the committed receipt byte-for-byte —
`sha256 58cbea87c671f010bc2a8b143a7bd777434fc28ab929045e6029cce135be3155`,
identical to the receipt's own hash. So the divergence is a **fixed
receipt-side truncation** (C1 → first line only, C2 → last four lines, C3 →
untruncated), not a difference in counter behavior.

**Semantic comparison: every recorded field agrees.** `revision`/`rev` full
40-hex, `indexed=41/43 missing=2 dangling=0 duplicates=0 coverage=9.5349/10`,
both missing note names, literal `28/40 fraction=0.7000`, `superseded=[20]`,
`active=39 resolved_active=31 fraction=0.7949`, unresolved set
`{1,2,3,4,5,38,39,40}`, `LINE 20 superseded excluded`,
`PRED-C2-r30 verdict=TARGET_MISSED`, and all three exit codes = 1.

## Repeatability and write-freedom

- Two consecutive runs of all three commands produced identical bytes
  (`c1 c5a0761b…`, `c2 629871d7…`, `c3 c15937b0…` on both runs); deterministic.
- `git status --porcelain` was unchanged before and after the runs: only the
  pre-existing untracked `.ufo/waves/round-30/w1/` directory. No lane file,
  index entry, corpus byte, or jj/git state was touched.
- No tool was installed or upgraded for this item.

### Post-run worktree mutation (not attributable to this item)

Measured after my last tool call (runs finished ~04:04; status clean at that
point): `quality/q36-successor-receipts.txt` now shows `M`, mtime
`2026-10-24 04:06:46 -0300`, 4 lines changed, and the diff replaces only two
ephemeral run tokens — `/tmp/mado-r28-q36-ge5zx30t` → `g3nfq53x` and
`/fast/scratch/…/run.gR7SQoLa` → `run.Kv8n49Ha`. Every `rc=`, `expected=` and
`PASS` field is unchanged. Raised by `RevC1Fence`; confirmed here read-only.
This is outside both my item's commands (all three counters are read-only) and
the registered write scope; I did not restore it.

## Adjacent observations (measured, not claims of this item)

- Invoking the gate with the short rev (`--rev 451e8b3c`) prints
  `rev=451e8b3c`; the gate labels output with the rev string as passed
  (`quality/check-index.py:215`) and does not resolve to 40-hex. The committed
  receipt used the full hash. Values are identical either way.
- Invoking the fence with `REV=451e8b3c` prints `revision=451e8b3c`; the
  receipt likewise used the full hash.
- At freeze the knowledge tree holds 43 notes and `corpus/README.md` 41 rows,
  independently counted from the committed tree, matching the fence's
  denominators.

## Risks / blockers

1. The receipt's `freeze-smoke-451e8b3c.txt` is **not present in the freeze
   tree** (`git cat-file -e 451e8b3c:…` fails); it first appears in the records
   commit (`92d3c86`, also `c75df6e`). The smoke receipt is therefore
   retrospective, not committed alongside the freeze.
2. Asymmetric recording: C1 drops the two `missing:` rows it itself printed,
   while C3 keeps the same two rows; C2 drops its `METRIC` header (which carries
   the `28/40`, `[20]`, `31/39` values) and six of its eight unresolved rows.
   Only the C3 section is a complete capture.
3. Consequence: a literal `cmp` acceptance of this smoke cannot pass. The
   defensible criterion is semantic equality plus the documented truncation
   filter above, which reproduces the receipt exactly.
4. No semantic divergence and no gate/counter defect was found; the freeze
   state is red by design on all three counters (pre-data), consistent with the
   registration's base claim for C2's unresolved set `{1..5, 38..40}`.
