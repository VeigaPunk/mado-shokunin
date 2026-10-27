# C2 README index check

Axis: coverage (C2 sourced dispatcher-dispatch entry); operability only insofar as index gate behavior is relevant.

## Commands and results

From `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
python3 -I quality/check-index.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 6ca8c559a4a3d6d361101592116eea2bc7452437
# MADO_INDEX: rev=6ca8c559a4a3d6d361101592116eea2bc7452437 indexed=66/66 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
python3 -I quality/check-index.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev a0e34387b30538372a1bb219eb3ccdc74013d458
# MADO_INDEX: rev=a0e34387b30538372a1bb219eb3ccdc74013d458 indexed=67/67 missing=0 dangling=0 duplicates=0 coverage=10.0000/10
python3 -I quality/check-index-rows.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev a0e34387b30538372a1bb219eb3ccdc74013d458
# MADO_INDEX_ROWS: rev=a0e34387b30538372a1bb219eb3ccdc74013d458 rows=67 errors=0 warns=3
```

Counts rise 66/66 → 67/67, all indexed, with no missing, dangling, or duplicate rows. The separate fidelity instrument is present and reports no errors. Its three warnings are pre-existing unrelated glob citations: `window-rule-effects-getprop.md`, `config-drift-r12.md`, and `rule-attribution-r24.md`.

## Independent C2 row inspection

`corpus/README.md:78` names `knowledge/hyprland-dispatcher-dispatch-r51.md` and labels it MADO-R51-1, round 51, Hyprland dispatcher execution. Its summary describes validation/storage of the dispatcher field, key-press-time lookup, submap/pass cases, and `hyprctl dispatch` request routing, explicitly distinguishing the round-50 key-match account. The source pointer says S364–S369 and held bind/parser grounding. This is the correct dispatcher-dispatch surface rather than another bind-match entry. The round-51 frozen claim requires at least two pinned mined source rows S364–S379 and three held citations; README shorthand is not by itself proof of those claims. The frozen counter is the authority for those predicates, not the row-fidelity gate.

**Assessment under the frozen index observation:** PASS for C2's requirement that the entry exists and is indexed (checker gives 67/67; README row observed). No bad wording or source-ID mismatch observed in the index row. This does not establish the other C2 source/pin/novelty/held-citation clauses.
