# CritC2Coverage — C2 coverage attack

**Result:** PASS under the exact frozen PRED-C2-r51 sentence; important distinction: this is source-grounded implementation-mechanism coverage, not measured runtime behavior. See [coverage judgment](CritC2Coverage/coverage-judgment.md).

Counterexample/evidence: The arc gap ledger `corpus/knowledge/arc-synthesis.md:298-300` names dispatcher behaviour as UNKNOWN given the no-keystroke-injection constraint; older entries expressly record that no dispatcher was fired (`dispatcher-semantics-r25.md:72-74`; `dispatcher-surface-and-request-grammar-r26.md:130-131`). The new entry provides nontrivial pinned facts—parse-time handler validation, 71-name map/forwarder, press-time invocation and special submap/pass paths, selected argument grammars, and `hyprctl dispatch` routing—but itself records that no key event, socket request, reload or dispatch occurred (`hyprland-dispatcher-dispatch-r51.md:88-243,284-300`). Its Limits also bound five inspected argument readers and explicitly mark some consequences `[INF]`. Thus it closes an implementation-source gap while the broader runtime-effect gap remains open; indexing and lexical novelty are not semantic sufficiency.

The exact predicate's source rows/pins, held facts, baseline comparison and counter receipt are described in the frozen data and evidence: `corpus/SOURCES.md:313-318`, entry `:14-24,26-53,55-68`, and `../receipts/c2-at-data.txt`. No predicate/artifact change recommended. Future runtime-coverage claims need separately authorized behavioral evidence; do not generalize the host config-file branch to every installation.

## Deliverables
- `.ufo/waves/round-51/w2/CritC2Coverage/coverage-judgment.md`
- `.ufo/waves/round-51/w2/CritC2Coverage.md`

Report: `.ufo/waves/round-51/w2/CritC2Coverage.md`
