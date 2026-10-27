# C2 README index mutation results

Scope: frozen clause (a), data revision `a0e34387b30538372a1bb219eb3ccdc74013d458`, frozen counter. Pristine baseline exited 0 / TARGET_MET.

| Mutant | README SHA-256 | Detector result | Verdict |
|---|---|---|---|
| `no_entry_path` | `not captured` | `exit=0`; `C2_R51: a ok=1 index_row=`knowledge/hyprland-dispatcher-dispatch-r51.md` (MADO-R51...`; `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=a0e34387b30538372a1bb219eb3ccdc74013d458` | **SURVIVED** |
| `substring_path` | `not captured` | `exit=0`; `C2_R51: a ok=1 index_row=`knowledge/hyprland-dispatcher-dispatch-r51.md` (MADO-R51...`; `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=a0e34387b30538372a1bb219eb3ccdc74013d458` | **SURVIVED** |
| `duplicate_row` | `not captured` | `exit=0`; `C2_R51: a ok=1 index_row=`knowledge/hyprland-dispatcher-dispatch-r51.md` (MADO-R51...`; `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=a0e34387b30538372a1bb219eb3ccdc74013d458` | **SURVIVED** |
| `comment_only` | `not captured` | `exit=0`; `C2_R51: a ok=1 index_row=`knowledge/hyprland-dispatcher-dispatch-r51.md` (MADO-R51...`; `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=a0e34387b30538372a1bb219eb3ccdc74013d458` | **SURVIVED** |

Expected: each bad form yields clauses_met<4 / TARGET_MISSED, exit 1. Actual: all four return exit 0, a ok=1, clauses_met=4, TARGET_MET. Clause-(a) coverage misses; no lane source/predicate altered.

Pristine README SHA-256: `e71e8f73317950f70104314a3e423896feeb149bc565df27fe58d0cef28267d2`; restored hash: `e71e8f73317950f70104314a3e423896feeb149bc565df27fe58d0cef28267d2`; byte equality: `True`. Restored detector exit 0; final line `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=a0e34387b30538372a1bb219eb3ccdc74013d458`. Raw outputs retained in scratch outputs/.
