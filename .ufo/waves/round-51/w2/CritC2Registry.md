# CritC2Registry — C2 source-registry attack

**Frozen result:** S364–S369 pass the SOURCES row-shape and metadata checks at data revision `a0e34387b30538372a1bb219eb3ccdc74013d458`: 11 columns, no literal pipes in cells, unique IDs, correct tier/scope/status/opened/recheck/used-by values. The frozen source census exits 0 and emits 22 W04 duplicate-URL-across-scopes warnings plus one unrelated W01 warning; no structural/error codes. Three warnings come from the six new rows: S364, S366, and S368. The row-draft statement “exactly two new warnings” is therefore a count/provenance miss (it omitted S366's existing HyprCtl.cpp URL collision), though the warning is surfaced rather than misreported as clean by the census and the C2 predicate does not require zero W04.

Detailed evidence, exact commands, warning classes, and the suggested future correction are in `.ufo/waves/round-51/w2/CritC2Registry/registry-audit.md`.

## Deliverables
- `.ufo/waves/round-51/w2/CritC2Registry/registry-audit.md` — requested audit.

Report: `.ufo/waves/round-51/w2/CritC2Registry.md`
