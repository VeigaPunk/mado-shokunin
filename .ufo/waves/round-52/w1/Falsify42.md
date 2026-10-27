# Falsify42 — C1 uniqueness/population falsification

## Deliverables
- `quality/counters/c1-r51-ledger.py` source analysis; frozen control and base receipt analysis.
- No fixture or counter execution performed: source-only restrictions prohibit producer execution, and only the named read-only materials were available for this scoped seat.

## Evidence and attack

Attacked item/predicate: frozen C1 population-row uniqueness, resolvable evidence pointer, non-self pointer, and instrument-specific functional context; specifically whether population accounting is actually unique and whether a pointer resolves as evidence rather than merely containing a basename.

At base `85d57a818c3707397e21c840b6498b105ba798aa`, the supplied receipt reports 82 population / 82 rows, no defects, TARGET_MET (`.ufo/waves/round-52/receipts/c1-base.txt:1-4`). The frozen claim says this previous counter accepts files containing the instrument basename and self-pointers (`claims-frozen.md:5-7`). Source confirms a concrete weakness in that prior check: `pointer_resolves` accepts a candidate token when the referenced file's bytes contain the row path basename anywhere (`quality/counters/c1-r51-ledger.py:196-208`); it does not establish the pointer's cited location or functional relevance. `describe` counts duplicate paths only among parsed rows, and population itself constructs a `sorted(set(pop))` (`:133-148`, `:218-239`), so duplicate filesystem paths are collapsed before population comparison. Thus row uniqueness is measured against a deduplicated population, not raw population enumeration.

The frozen no-work control is two duplicate rows whose Reads field points to `quality/tool-ledger.md` and whose description explicitly says generic self-pointer (`controls/c1-do-nothing.md:1-4`). This is suitable as a negative control for the stated context/self-reference defect, but it cannot test whether population deduplication masks duplicate inventory candidates: its rows duplicate the tool path, not distinct eligible files that collide under population construction. No such mutation/fixture was run or created, consistent with the source-only restrictions.

## Reproducible source inspection

Read-only source locations and results:
- `quality/counters/c1-r51-ledger.py:133-148`: `population()` returns `sorted(set(pop))`.
- `quality/counters/c1-r51-ledger.py:196-208`: pointer passes if the file contains `basename(row_path)` as a byte substring.
- `quality/counters/c1-r51-ledger.py:218-239`: duplicate ledger row paths counted; coverage computed against deduplicated population.
- `quality/counters/c1-r51-ledger.py:415-430`: target requires row count equal to population and no defects.

Reproduced: **No** (no runtime reproduction; source-level bypass opportunity identified). Limitation: the concrete duplicate-path collision requires a fixture or source-tree state containing distinct eligible paths that become equivalent under whatever normalization/identity logic is used; this source code does not normalize eligible path strings, so ordinary Git path enumeration likely cannot produce that collision. The stronger confirmed limitation is that pointer resolution is basename-substring evidence, not location-specific evidence, but that is the already frozen prior deficiency and not proof of a defect in a new counter.

## Axes, proposed bounded move, risks, verification

Affected axis: operability, through better confidence that C1's population uniqueness check distinguishes distinct tracked entries and that its evidence-pointer predicate is not a basename coincidence. No demonstrated harm to coverage. This finding does not establish a failure of an unseen round-52 counter.

Proposed move: add a seat-local adversarial fixture with a synthetic population and two distinct rows, then assert the new counter rejects repeated row identity and a pointer target whose only match is an unrelated basename occurrence; retain the specified production pass and frozen control fail as separate controls. This is a recommendation only, not an edit or claim change.

Risk/contradiction: the base counter's deduplicated population prevents it from serving as evidence that raw path population itself is duplicate-free, while its existing uniqueness check may still correctly reject duplicate ledger rows. No source evidence shows a real Git tree producing duplicate path strings. Do not treat this as a reproduced round-52 counter bypass.

Verification: report is based only on local source bytes and committed control/receipt. No command execution, package query, live read, screenshot, producer execution, scratch artifact, or source mutation. No installs.

## Deliverables
- `.ufo/waves/round-52/w1/Falsify42.md`

Report: `.ufo/waves/round-52/w1/Falsify42.md`
