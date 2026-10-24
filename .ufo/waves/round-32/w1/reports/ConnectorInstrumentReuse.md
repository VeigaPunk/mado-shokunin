# ConnectorInstrumentReuse — instrument-reuse scan

Scope searched: `quality/`, `tools/`, `.ufo/waves/round-3*/` (round-30, round-31, round-32).
Question (a): re-derive a published axis score, or compare `SCORECARD.md`'s own axis table to a counter.
Question (b): SOURCES registry schema, used-by resolution, id collisions.
`quality/check-axis-scores.py` is untracked (`git status` `??`; absent from `git ls-files`; `git log -- quality/check-axis-scores.py` empty). It is not a committed prior instrument.

## (a) axis-score candidates

| path | prints | covers C2 staleness? |
|---|---|---|
| `quality/check-index.py` | `MADO_INDEX: <tag> indexed=A/B missing=N dangling=N duplicates=N coverage=X.XXXX/10`; exit 1 on any gap. `--selftest` prints `MADO_INDEX_SELFTEST: A/B assertions passed`. | No. Re-derives the live navigation fraction from `corpus/knowledge/` + `corpus/README.md` only. Never opens `SCORECARD.md`. |
| `.ufo/waves/round-31/c2/count.py` | `counter=c2-grounding-r31-v2 rev=…` then `METRIC literal lines=L/T fraction=…`, `METRIC active=A resolved_active=R fraction=…`, `PRED-C2-r31-v2 verdict=TARGET_MET\|TARGET_MISSED`. | No. Re-derives the live calibration fraction from `corpus/QUALITY.md` + `corpus/lessons/`. Never opens `SCORECARD.md`. |
| `.ufo/waves/round-30/c2/count.py` | `counter=c2-grounding-r30 rev=…` then the same `METRIC active=` / `resolved_active=` lines and `PRED-C2-r30 verdict=…`. Frozen predecessor (r31 docstring: "the r30 counter stays frozen"). | No. Same surface as r31. Does not read the published axis line. |
| `quality/check-population.py` | `exit=<n>`. Compares a `**PRED-<id>**` registration paragraph to a receipt's `PRED-<id>` summary and `CASE` lines. | No. Binds a predicate registration to a counter receipt. Does not parse `Axis table re-derived`. |
| `quality/check-axis-scores.py` (untracked) | `MADO_AXIS_ROW: axis=<name> published=A/B derived=A/B verdict=MATCH\|STALE\|NOT-PUBLISHED\|NOT-RE-DERIVABLE` then `MADO_AXIS: checked=A mismatched=M rev=<sha>`. Exit 1 iff `M>0`. | Yes, for the three axes it names. This is the registration's named counter, present only as an uncommitted worktree file. Do not write a second file. |

Not candidates: `quality/counter-selftest.py` (r26 animation/bind judgement harness; prints `SELFTEST pass=N total=M`), `quality/check-control-receipts.py` (control-receipt order; prints `CONTROL_RECEIPTS verdict=…`), `quality/population-suite.py` (fixtures for the population check), `tools/mado-assessment.py` (assessment-bundle JSON; prints nothing about axes), `tools/mado-verify.sh` (host file-plane rows). Round-32 has no counter script (`dispatch-w1.sh` only).

## C2 — stale published axis score?

**No committed gate detects one.**

The publication C2 names (`Axis table re-derived at … navigation 43/43 … calibration resolved-active 39/40 … operability selftest 9/9`) is never an input of the committed instruments. Each re-derives a live number and stops:

- `quality/check-index.py:15-16` says the gate "says nothing about note truth, freshness, or the semantic accuracy of the row text". Output (`:135-138`) is only `indexed={covered}/{total} … coverage={score:.4f}/10` from knowledge notes vs README rows. A SCORECARD line that still says `43/43` after the index moves is invisible. The selftest line (`:329`) prints `MADO_INDEX_SELFTEST: {passed}/{len(checks)} assertions passed` and does not compare that pair to the published operability cell.
- `.ufo/waves/round-31/c2/count.py:330` prints `METRIC active={act_n} resolved_active={res_n}`. The pass rule (`:341-344`) is `active >= ACTIVE_MIN and not unresolved_active and literal >= 0.70`. A published `39/40` against a live `41/41` is still `TARGET_MET`. The r30 pass rule (`round-30/c2/count.py:208`) is the same shape: live unresolved-set empty and literal `>= 0.70`, no SCORECARD read.
- `quality/check-population.py:30-33` compares "a predicate's registered target" to "its reported metrics and population". The registered target is a `**PRED-**` paragraph, not the SCORECARD axis line.

The only file that does the comparison is the untracked draft `quality/check-axis-scores.py`. `published_fractions` (`:36-52`) keeps the last `Axis table re-derived` line. `compare` (`:55-77`) sets `verdict = "STALE"` when the published fraction differs from the re-derived fraction. `main` (`:241`) prints `MADO_AXIS: checked=%d mismatched=%d`. It re-derives by running committed bytes of `quality/check-index.py` and `.ufo/waves/round-31/c2/count.py` (`derive`, `:108-141`). It does not exist at the round base `256222890d935212874a09751ff9b7869943c2d7`. Adopting this file is the C2 instrument; a second gate would diverge from it.

## (b) SOURCES schema / used-by / id-collision candidates

| path | prints | covers a malformed or dangling appended SOURCES row? |
|---|---|---|
| `quality/check-index-rows.py` | `MADO_INDEX_ROWS: <tag> rows=N errors=N warns=N` plus `ERROR cited-s-undefined: S### …`, `ERROR cited-path-missing: …`, `ERROR row-cells: …`, `ERROR row-outside-map: …`. WARN lines do not change the exit. | No. Limit quoted below. |
| `quality/check-index.py` | `dangling=N` and `dangling: knowledge/<name>` when a README row names a note absent from `corpus/knowledge/`. | No. Does not read `corpus/SOURCES.md` (`:18`). `dangling` (`:120`) is README row names minus knowledge notes. |
| `tools/mado-verify.sh` row `hypr.root.sources_resolve` | `PASS declared targets exist, member set exact` or `FAIL unresolved:… non-regular:… missing:… extra:…`. | No. Name collision. The row resolves `hyprland.conf` `source=` targets as regular files under `$ROOT` (`:3004-3008`), not `corpus/SOURCES.md` cells. |
| fleet `scripts/sources-census.sh` `validate` | TSV `lane<TAB>E01…E12\|W01…W04\|ok`. Exit 0 on clean or warnings, 1 on E-codes. Outside the three searched trees (operator script, not a lane copy). Listed because it is the gate that implements (b), and registration item 10.4 already calls it. | Partial. E01/E03/E11 catch field-count, duplicate id, and a missing used-by path. Insufficient for the C1 append contract; limits quoted below. |

No script under `quality/`, `tools/`, or `.ufo/waves/round-3*/` parses the 11-column registry, resolves `used-by`, or detects id collisions. Round-30/31 `c2/count.py` resolve `lessons/` citations, not SOURCES rows.

## C1 append — malformed or dangling appended row?

**No gate inside the searched trees detects one.**

Nearest in-tree gate: `quality/check-index-rows.py`. It reads `corpus/SOURCES.md` only to build an id set:

```
def source_ids(sources):
    return set(re.findall(r"^\|\s*(S\d{3})\s*\|", sources, re.M))
```

(`check-index-rows.py:195-196`). A row whose first cell is still `| S186 |` is a defined id whatever the other ten cells are. The `set` collapses a duplicate id, so a collision is not an error. `used-by` is never read. The word "dangling" in this file is a README row whose knowledge note is absent, and the gate explicitly does not own it (`:262`: "dangling row: the completeness gate owns this finding"). `check-index.py`'s dangling finding is that same README-vs-knowledge gap, not a SOURCES append.

**Yes, outside the trees: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate`.** Header contract (`:24-29`): `E01` malformed row (`NF!=13`), `E03` duplicate id, `E11` used-by path missing on disk. Do not reimplement those three inside the lane. It is still insufficient for this round's append, on these lines:

- `:16` — exit `0` means "clean or warnings". `:32` — "W03 mined row with used-by = — (warnings do not affect clean lanes)". A mined append whose `used-by` is the em dash is dangling in the closure sense and still exits 0.
- `:566` — E11 is `[ ! -e "$dir/$path" ]`. The path exists or it does not. The check does not open the file, so a `used-by` path that exists but does not cite the row passes, and a citing entry omitted from `used-by` passes unless the cell is exactly `—` (W03, non-failing).
- `:559` — `[ "$status" = mined ] || continue`. A non-mined row with a dangling `used-by` is not E11.
- `:501` — `--file` sets the resolution root to `dirname(file)/..`. Used-by paths resolve only when the file sits at `<root>/corpus/SOURCES.md`. A bare append fragment resolves them against the wrong directory.
- `:641` — `else if (id in seen)`. E03 is duplicates inside the one file under validation. A collision between the live registry and an unmerged `SOURCES.append.md` is invisible until both row sets are in that file.

Registration item 10.4 already requires this census on the scratch mirror before the first append. Item 10.1's `comm -12` collision guard is the pre-merge check E03 cannot see. Neither is a reason to add a lane-local schema gate.
