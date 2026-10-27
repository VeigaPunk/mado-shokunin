# Falsify46 — C2 proposition-map completeness

## Attacked item/predicate

C2, coverage axis, the frozen predicate leg **"every material factual proposition is mapped"**
(`.ufo/waves/round-52/claims-frozen.md` §C2; `.ufo/waves/round-52/registration.md` §Frozen
predicates C2), as enforced mechanically by the round-52 draft counter's clause (e)
*"Completeness of the mapping: no unmapped claim row, no orphan proposition, no padding"*.

Attacked instrument: `.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py`,
tested as a frozen snapshot (771 lines, sha256 `43c7ebe9dbb482da22b8bf361f2f43dd0d4bff431307cbae347ae775ab94d95e`,
receipt `Falsify46/receipts/counter-snap.sha256`). The seat file is live and was edited twice
during this wave; findings below bind to the snapshot, not to any later edit.

Two concrete failure modes were executed against seat-local fixtures; both pass the counter
while violating the predicate leg. A negative control confirms the harness is non-vacuous,
and a read-only probe of the frozen base confirms the no-work control still misses.

## Why clause (e) cannot establish completeness (source evidence)

- `cited_rows()` (snapshot lines 596-609) builds the prose row set **only from `S###` ids**
  found on unfenced, non-table, non-marker lines. Any material factual sentence that names a
  pin and line but **no `S###` row** — or no citation at all — is invisible to the
  `row_unmapped` check (`clause_e`, lines 613-642).
- `quote_not_used` (line 639) checks only the reverse direction: quotes *declared in the map*
  must appear in prose. Nothing checks that prose *claims* are in the map.
- `MARKER_RE` (line 112) excludes every line starting `held|ground|lane|round|wave|base|
  verified-at|recheck` from the prose set, so a fresh claim carrying an `S###` id on such a
  line would also escape `row_unmapped` (inspection only, not executed).
- The clause checks row-id set equality (`prose ⊆ prop_rows ⊆ prose`), never claim
  granularity, so omission from the declared map is undetectable above the ≥4 count floor.

## Reproducible setup

All work in `/fast/scratch/hyaku/mado-r52/Falsify46/` (cleaned after the run; receipts copied
to this seat dir):

1. Local clone of the lane repo at base `85d57a818c3707397e21c840b6498b105ba798aa`;
   `git rev-parse --show-toplevel` asserted to equal the clone dir before any fixture commit.
2. `.ufo/waves/round-52/fetch/` in the clone holds the four pin files
   (`Hyprland-legacy-DispatcherTranslator.cpp`, `Hyprland-ConfigActions.cpp`,
   `Hyprland-ConfigActions.hpp`, `Hyprland-KeybindManager.cpp`) copied byte-for-byte from the
   tracked round-51 fetch (same upstream revision `efb50993780079460b0cbed1363e2166a2de1d9f`).
3. Registry rows S370-S373 appended to `corpus/SOURCES.md` (status `mined`, opened
   `2026-10-27`, anchor under the round-52 fetch root with the 40-hex revision, used-by the
   fixture entry); index row appended to `corpus/README.md`.
4. Fixture entry `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md` built from seat
   C2EntryDraft's live `proposition-map.tsv` (sha256 `8a7d5d71…f8c946`, receipt
   `proposition-map-tsv.sha256`; 17 propositions P01-P17, quotes already verified by that
   seat against the same pin bytes). Exact tested bytes preserved in
   `receipts/fixture-entry-baseline.md`.
5. Runner: `TMPDIR=<scratch>/tmp python3 -I counter-snap.py --repo <clone> --rev HEAD
   --entry corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md --work <scratch>/work-<tag>`
   (harness: seat receipts; identical runs reproducible from the committed fixture clone).

## Results

| run | mutation | counter verdict | clause detail |
|---|---|---|---|
| base | none (17 propositions, conforming) | **TARGET_MET** rc=0 | clauses=abcde 5/5; rows_bound=4/17; quotes_bound=17/17 |
| m1 | +1 material claim, pin:line locator, **no S-row** | **TARGET_MET** rc=0 | clauses=abcde 5/5; `prose_rows=4` unchanged |
| m2 | P16 deleted from map **and** prose (pure omission) | **TARGET_MET** rc=0 | clauses=abcde 5/5; `propositions=16` |
| negctl | P01 map quote corrupted (args,4→args,5) | TARGET_MISSED rc=1 | clause_d `P01:quote_not_at_pin`, clause_e `P01:quote_not_used` |
| lane-base | frozen base, entry absent (no-work control) | TARGET_MISSED rc=1 | `a ok=0 entry=absent` — control misses as required |

**Failure mode 1 — row-less claim escapes the map (m1, reproduced: yes).** Appended chain
sentence (diff: `receipts/m1.diff`): *"A repeat dispatch passes the identical rebuilt
`modifiedArgs` buffer to the second delegate call rather than re-reading the argument
(Hyprland-legacy-DispatcherTranslator.cpp:620)."* This is a true, source-backed material fact
(it sits inside the seat's own P04 span 619-622), but it maps to no opened-this-round `S###`
row, no pin-path/revision entry and no ≤25-word map quote — exactly what the frozen predicate
requires of every material factual proposition. Clause (e) reports `prose_rows=4 prop_rows=4`
and admits the entry 5/5. **The counter's "complete mapping" is coverage of row-ids that happen
to be mentioned, not of the claims the entry makes.**

**Failure mode 2 — omission is undetectable (m2, reproduced: yes).** Deleted proposition P16
("A written selector that resolves nothing and an empty selector end in different delivery
paths…", S371, `Hyprland-ConfigActions.cpp:1578-1579`) from both the map table and the prose
(diff: `receipts/m2.diff`). The counter cannot know the entry should contain 17 propositions;
with 16 remaining (≥4, distinct rows 4, no duplicates, all quotes used) it admits the entry
5/5. Semantic completeness rests entirely on the outside non-author reviewer the predicate
already names — the counter contributes nothing to the omission direction.

**Negative control (reproduced: yes).** Corrupting a single map quote flips clause_d
(`quote_not_at_pin`) and clause_e (`quote_not_used`): the harness can fail, and the counter
does catch broken row/pin/quote bindings. The two holes above are therefore specific to
completeness, not to a generally inert instrument.

## Distinction from sibling seats

Falsify30 (same target) inspected the **round-51** counter's line-granularity `bind_row` and
ran no fixture. This seat executed the actual **round-52 draft** counter against a conforming
fixture clone and demonstrated two distinct, reproducible completeness holes at the
row-citation scope (claim escape) and at the map-set scope (claim omission), with green
mutated runs and a red control.

## Axis impact and dissent

- **Coverage:** the predicate leg "every material factual proposition is mapped" is only
  half-machine-checkable. A C2 pass does not evidence that leg; the outside review must sweep
  prose claims claim-by-claim (including pin-only citations and marker lines), not just
  spot-check mapped rows. Recommended, not required, for the predicate text (frozen): the
  predicate already delegates entailment to the reviewer — this attack shows the delegation
  also silently covers completeness.
- **Operability:** no harm demonstrated; the counter is runnable, base-sensitive, and
  red/green discriminating for bindings. Suggested cheap hardening for the draft counter
  (does not touch the frozen predicate): flag prose locator citations (`Pin.cpp:N`) and code
  quotes that are not echoed by any map row, so claim-escape costs a clause.
- No frozen claim or predicate was edited; no tracked lane file was written; the lane repo was
  only read and probed read-only (base probe receipt `receipts/lane-base-probe.log`).

## Limitations

- The attacked counter is an uncommitted seat draft mid-iteration; the snapshot binds the
  findings. The clause-(e) design (row-set equality over `cited_rows`) was stable across both
  observed edits, so the holes likely persist, but re-running against the landed counter is
  the integrator's check.
- The fixture registry rows S370-S373 are stand-ins with the real pins and the real
  proposer's quotes; they were never appended to the lane's `corpus/SOURCES.md` (that edit
  belongs to the data seat).
- M1's injected claim was verified by inspection against the pin bytes (lines 619-622) but no
  new quote row was added to any map; that is the point of the attack, not an oversight.
- Source-only round: no package queries, host reads, producers, or fetches; the four pins were
  already local and tracked.

## Deliverables

- This report: `.ufo/waves/round-52/w1/Falsify46.md`
- Receipts dir: `.ufo/waves/round-52/w1/Falsify46/receipts/` — `base.log`, `m1.log`,
  `m2.log`, `negctl.log`, `lane-base-probe.log`, `summary.txt`, `m1.diff`, `m2.diff`,
  `fixture-entry-baseline.md` (tested entry bytes), `counter-snap.sha256`,
  `proposition-map-tsv.sha256`
- Scratch `/fast/scratch/hyaku/mado-r52/Falsify46/` removed after receipt copy; no tooling
  installed; no tooling updates needed.

## Report

Report: `.ufo/waves/round-52/w1/Falsify46.md`
