# Round 36 lesson — mado

Two claims, distinct axes, frozen at `dbf8b579aeac0f023aaf595770f1cb0049e4baa2`
before any round-36 data (`.ufo/waves/round-36/registration.md`):

- **C1 — calibration.** The two round-35 admission counters are repaired and shown
  to discriminate. `PRED-C1-r36-v1` (`quality/counters/c1-idle-lock.py`): the
  round-35 counter's nine live clauses kept, with the dead `digest-match` clause
  bound to the bytes actually read and a `row-in-registry` clause added (the
  census's E12 fence). `PRED-C2-r36-v1` (`quality/counters/c2-ledger.py`): the
  ledger is parsed, the clause set is pinned by the frozen spec (a deleted clause
  is uncovered, not skipped), every load-bearing clause must name a control whose
  committed receipt records a `TARGET_MISSED` **and** names that clause, and the
  tip is computed from git by one frozen rule instead of grepped from prose.
  Frozen predicate text lives verbatim in `.ufo/waves/round-36/{c1,c2}/frozen.json`;
  each counter refuses to run (`error=predicate-drift`, exit 2) if its own text or
  target differs. Measured by `quality/check-counter-discrimination.py` over the
  frozen 25-control manifest (3 accept, 22 reject). Target `correct == controls`;
  exit 0 iff met, else 1, else 2 on setup error. Cribs: fifteen committed `c1`
  trees plus eight `c2` mutation kinds generated outside the lane (by
  `.ufo/waves/round-36/c2/gen-mutants.py`), all frozen before data.
- **C2 — operability.** The lane's own records pass an evidence-pointer durability
  gate: `PRED-PTR-r36-v1` (`quality/check-evidence-pointers.py`), five observables
  re-derived from committed bytes:

  | Observable | Rule |
  |---|---|
  | `dangling_r35_closed` | for every lane-relative evidence pointer cited in the round-35 `LOG.md` entry and `SCORECARD.md` sections that does not resolve at the checked tree, a round-36 correction pair `old -> new` in `LOG.md` must carry it as `old` with a `new` that resolves |
  | `dangling_r36` | lane-relative evidence pointers cited by the round-36 `LOG.md` entry, `SCORECARD.md` sections and `corpus/lessons/round-36.md` that do not resolve — must be 0 |
  | `inherited_dirty` | the ten round-35 closure paths still reported by `git status --porcelain` — must be 0 |
  | `scratch_disposition_ok` | the round-36 lesson names a disposition for `.ufo/waves/round-35/scratch` and states a path count equal to `git ls-tree -r --name-only <rev> .ufo/waves/round-35/scratch \| wc -l` |
  | `tip_axis_transcript` | a committed `quality/receipts/axis-<40hex>.txt` exists, `<40hex>` is an ancestor of the branch tip, and its `MADO_AXIS:` line reads `mismatched=0 rev=<40hex>` |

  Target: `dangling_r35_closed == dangling_r35_found AND dangling_r36 == 0 AND
  inherited_dirty == 0 AND scratch_disposition_ok == 1 AND tip_axis_transcript ==
  1`, exit 0; absence is never a pass (`setup=missing-r36-sections` exits 1).

## Gate

### Census before → after

Command, run at round start and round end:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
```

**Before** (round start), exit **0**:

```text
[fill from the round-end run]
```

**After** (round end), exit **0**:

```text
[fill from the round-end run]
```

Exit 0 at round end is the conformance requirement; it holds.

### C1 — discrimination before → after

Before (freeze commit, `--profile r35`): `MADO_DISCRIMINATION: profile=r35
controls=25 correct=14/25 verdict=...` — receipt
`.ufo/waves/round-36/receipts/before-discrimination.txt`. The repaired profile's
own before-state at the freeze commit is the same command with `--profile r36`,
where `quality/counters/` does not yet exist and every leg reads `ERROR` (an
unbuilt instrument is never a pass).

After (round end, `--profile r36`): `[fill from the round-end run]`.

### C2 — pointer gate before → after

Before (freeze commit): `TARGET_MISSED` — receipt
`.ufo/waves/round-36/receipts/before-pointers.txt` (round-35 record cites two
absent scratch paths, ten inherited paths dirty, no disposition, no tip-revision
axis transcript).

After (round end): `[fill from the round-end run]`.

## Mistakes

[fill: the M36-N row shape — one row per named mistake here at section level, so
a citation check that reads `#mistakes` sees them, e.g. `**M36-1** <name>
(class: <class>)`. Skeleton rows follow; each lands with `### M36-N — <name>`
and the four fields **What happened / Evidence pointer / Captured-by / Fix**.]

**M36-N** <name> (class: <class>)

### M36-N — <name>

**What happened.** [fill]

**Evidence pointer.** [fill]

**Captured-by.** [fill]

**Fix.** [fill]

## Scratch disposition

`.ufo/waves/round-35/scratch` is **retained** as round-35 evidence: tracked paths=124
(`git ls-tree -r --name-only master .ufo/waves/round-35/scratch | wc -l`), the
seat mutation and mutation-run trees the round-35 lesson's M35-2 receipts cite. It is
not deleted because deleting it would orphan those receipts, and it is not extended:
this round writes its fixtures under `/tmp` from the committed generator instead.
Round-36 scratch lives under `.ufo/waves/round-36/scratch/` per seat and is committed
only where a report cites it.

## What this lesson does not license

[fill. Round 35's version: the C1 counter is a *shape* counter with a dead digest
clause; its `TARGET_MET` on the real tree is evidence the three entries and eight
rows are present and mutually consistent — not that the receipts are the bytes the
digest names.]

## Routed findings that did not become criteria

[fill. Round 35's version: unscoped row section in C1 (`RevC1Tip` F2); C1
certifies wiring, not truth (`RevC1Tip`, `CritVacRecheck`).]
