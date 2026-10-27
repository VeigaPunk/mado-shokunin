# C1/C2 causal-separability attack

## Axes
Coverage and operability. The frozen claims declare these axes causally separable; this probe asks whether either counter's measured artifact/population depends on the other claim.

## Exact-revision probes
All commands used the lane at `/home/vgpnk/Projects/shokunin/mado-shokunin`, isolated work directories below `/fast/scratch/hyaku/mado-r51/ConnectorC1C2Overlap/`, and the frozen artifact paths. The scratch guard had 467G available (42% used) before probes. No install or lane mutation was performed.

1. **C1 at freeze, with C2 entry absent:**

```sh
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r51-ledger.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 56026fcb9800370ae04bc65952a6567181c398d0 --work /fast/scratch/hyaku/mado-r51/ConnectorC1C2Overlap/freeze
```

Observed exit 0; final line `C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=56026fcb9800370ae04bc65952a6567181c398d0`. At this exact revision `git cat-file -e <rev>:corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` fails (absent). This agrees with `.ufo/waves/round-51/w2/RevC1CounterRev.md` and confirms C1 does not require the C2 entry. C1's population is the paths under `tools/`, `quality/*.py`, and `quality/counters/*.py`; its checker verifies rows/pointers, not corpus content.

2. **C2 at data, with no ledger dependency in its required clauses:**

```sh
TMPDIR=/fast/scratch/hyaku/mado-r51/ConnectorC1C2Overlap/c2-data python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r51-dispatch-entry.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev a0e34387b30538372a1bb219eb3ccdc74013d458 --work /fast/scratch/hyaku/mado-r51/ConnectorC1C2Overlap/c2-data
```

Observed exit 0; `a ok=1`, `b ok=1 rows=6/2 pins=6`, `c ok=1 ... max=0.1%`, `d ok=1 held=7/3`, final line `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=a0e34387b30538372a1bb219eb3ccdc74013d458`. C2 evaluates the entry, README, source rows/pins, base/candidate novelty comparison, and held citations. C1's ledger is not a clause or required input to this counter. Important precision: the requested phrase “C2 at base without ledger must miss” is observed: at base, both C2 entry and `quality/tool-ledger.md` are absent, and C2 returns the expected MISS. This is not an isolated deletion experiment against the data revision; the predicate's own base control is an absent-entry control.

```sh
TMPDIR=/fast/scratch/hyaku/mado-r51/ConnectorC1C2Overlap/c2-base python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r51-dispatch-entry.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin --rev 6ca8c559a4a3d6d361101592116eea2bc7452437 --work /fast/scratch/hyaku/mado-r51/ConnectorC1C2Overlap/c2-base
```

Exit 1; `a ok=0 entry=absent`, remaining clauses skipped, final line `C2_R51: clauses=abcd clauses_met=0 admitted=0/1 verdict=TARGET_MISSED rev=6ca8c559a4a3d6d361101592116eea2bc7452437`. At base `quality/tool-ledger.md` is also absent, as independently shown by the C1 base receipt `.ufo/waves/round-51/w1/ExecLedgerCounter/receipts/base-and-setup.txt` (population 79; exit 1).

3. **C1 base reciprocal control:** same C1 command with `--rev 6ca8c559a4a3d6d361101592116eea2bc7452437 --work .../base` returned exit 1 and `C1_R51: verdict=TARGET_MISSED ledger=absent population=79 rev=6ca8c559a4a3d361101592116eea2bc7452437`.

## Overlap and shared-failure assessment

**No direct predicate coupling found.** C1's assessed population excludes `corpus/` and its boolean success is independent of dispatcher entry presence; direct freeze probe proves a C1 pass with the C2 entry absent. C2 does not mention or read `quality/tool-ledger.md` as a criterion, and its base MISS occurs while ledger is absent. C2's coverage evidence is not counted as an instrument row by C1; C1 does include the C2 *counter script* as one of its quality/counters population paths, but that is inventory of a tool file, not a dependency on C2's data, sources, pins, or verdict. Conversely, C2's frozen base comparison and citations use the C2 knowledge/candidate domain, not C1 ledger rows.

There is a shared *execution substrate*, not a shared acceptance condition: both scripts resolve a repo/revision and use scratch paths, so an invalid revision/repository or unusable scratch can block either measurement (setup failure), but does not convert one claim's artifact into evidence for the other. C1's population includes its own checker/counter and the C2 counter; source changes could therefore affect their measured tool inventory/count, yet no C2 data path is involved. This is a narrow structural overlap, not evidence of coupling in the frozen predicates.

**Control limitation:** “C2 at base without ledger” proves C2's declared base MISS and ledger absence simultaneously; it does not prove C2 would remain MET if the ledger alone were deleted from the data revision. That stronger one-variable counterfactual is outside the requested exact-revision base test and would require a scratch-revision mutation. The current C2 contract itself lists no ledger condition. Keep this distinction explicit rather than treating co-absence at base as an independent deletion-control.

## Verdict under frozen predicates

- **C1 at freeze with C2 entry absent: PASS** (`TARGET_MET`, exit 0).
- **C2 at base while ledger absent: PASS as the prescribed base control** (`TARGET_MISSED`, exit 1); not an isolated ledger-removal experiment.
- **Cross-claim coupling: none observed in the frozen acceptance predicates.** Shared setup failures are possible; no shared content failure mode was demonstrated.

## Evidence pointers

- Frozen exact sentences: `.ufo/waves/round-51/claims.md` lines 23–37 (C1), 51–69 (C2).
- Exact-revision registration and known residuals: `.ufo/waves/round-51/registration.md` lines 7–25.
- This seat's direct replay outputs are preserved in `/fast/scratch/hyaku/mado-r51/ConnectorC1C2Overlap/` for `freeze`, `base`, `c2-data`, and `c2-base`.
- Independent C1 freeze replay: `.ufo/waves/round-51/w2/RevC1CounterRev/c1-counter-replay.md`; C1 population audit: `.ufo/waves/round-51/w2/RevC1Population/population-audit.md`.
- C2 data receipt: `.ufo/waves/round-51/receipts/c2-at-data.txt`; C2 base receipt: `.ufo/waves/round-51/w1/ExecCounterC2/receipt-base.txt`.
- Counter scope: `quality/counters/c1-r51-ledger.py` lines 128–152, 211–248; `quality/counters/c2-r51-dispatch-entry.py` lines 9–20, 56–58.

## Deliverables
- `claim-separability.md` — this analysis.

Report: `.ufo/waves/round-51/w2/ConnectorC1C2Overlap.md`
