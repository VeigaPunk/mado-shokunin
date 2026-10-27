# C2 counter replay — RevC2CounterReplay

Commands were run from `/home/vgpnk/Projects/shokunin/mado-shokunin` with independent isolated scratch subdirectories under `/fast/scratch/hyaku/mado-r51/RevC2CounterReplay/`:

```sh
TMPDIR=/fast/scratch/hyaku/mado-r51/RevC2CounterReplay/base python3 -I quality/counters/c2-r51-dispatch-entry.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 6ca8c559a4a3d6d361101592116eea2bc7452437
# exit 1; clauses_met=0; admitted=0/1; TARGET_MISSED

TMPDIR=/fast/scratch/hyaku/mado-r51/RevC2CounterReplay/data python3 -I quality/counters/c2-r51-dispatch-entry.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev a0e34387b30538372a1bb219eb3ccdc74013d458
# exit 0; clauses_met=4; admitted=1/1; TARGET_MET
```

Observed data-revision evidence: clause a indexed row present; clause b `rows=6/2 pins=6`; clause c `body_shingles=2900 files=66+cand3 max=0.1%`. Recorded highest overlaps: bind-table-r25.md 3 hits / .001; hyprland-bind-key-match-r50.md 2 / .0007; round-49 candidate equivalent 2 / .0007. Clause d reports `held=7/3 lines=8 untargeted=1 tokens=14`; probe JSON enumerates seven held citations. Counter-generated probe is `/fast/scratch/hyaku/mado-r51/RevC2CounterReplay/data/c2-r51-3ase39xj/c2-r51-probe.json`.

Independent receipt/commit identity check: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show -s --format='%H %s' a0e34387b30538372a1bb219eb3ccdc74013d458` returned `a0e34387b30538372a1bb219eb3ccdc74013d458 round-51: land sourced dispatcher surface, C2 rows, quality and lesson`. The counter's own final line also names exactly that revision; shell-captured counter exits were `BASE_EXIT=1 DATA_EXIT=0`.

## Verdict
PASS under the frozen PRED-C2-r51 predicate for both expected revision outcomes. This replay confirms the executable counter's row/pin/index/shingle/held totals and the data-revision identity. It does not establish semantic novelty beyond the frozen lexical shingle test; that limitation is already recorded in registration.md.
