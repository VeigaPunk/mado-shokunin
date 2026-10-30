# R56W3MutKillC1 — C1 survivor fixture verification

## Result and scope

Attacked item: the C1 counter's claimed kill power against the survivors named by R56W2MutC1CounterA and R56W2MutC1CounterB.

Axes: behavioral discrimination; faithful fixture materialization; exact-byte restoration; frozen-contract preservation.

At scored revision `0f3a54361a9824484d0801679ceb1fd8ac7c32e1`:

- **A's 21 non-equivalent survivors: 21/21 distinguished by their proposed F01–F20 fixtures.**
- B actually names **28**, not 21, non-equivalent survivors, in a separate mutant-ID namespace: **28/28 distinguished**, including its tree-OID CLI case.
- A's two additional verdict-equivalent witnesses, M16/F21 and M53/F22: **2/2 output differentials reproduced**, separately from the sha-valid domain.
- Total: **51/51 proposed mutant/fixture pairs distinguished; zero survivors; zero setup errors in the final run.**
- **51/51 restored-counter runs matched the pristine behavior** on the same fixture content (revision tokens normalized because reconstructed scratch commits have different IDs).

A and B reuse IDs for different edits; `A:M13` and `B:M13`, for example, are different mutants. Every delivered record is namespaced.

**A differential is not necessarily a TARGET_MET→TARGET_MISSED flip.** Some mutants omit a required leg while retaining TARGET_MISSED; others wrongly admit the fixture. Others add a spurious leg or crash. The checklist records both output lines and the exact lost/added legs. No predicate or frozen control count was changed.

## Method and decisive commands

One read-only lane archive, of the counter-relevant paths at the scored revision, was extracted under `/fast/scratch/hyaku/mado-r56/R56W3MutKillC1/base`. A fresh scratch repository was initialized, its toplevel checked, and commits used `user.name=ctl`, `user.email=ctl@ctl`. Fixture repositories were copies of that export, never lane worktrees.

The counter bytes at the old wave-2 revision and scored tip are identical:

```
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 28fc86ac2359ec27406d8a2c63bef82ea6e947ed:quality/counters/c1-r56-autoreload-entry.py | sha256sum
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 0f3a54361a9824484d0801679ceb1fd8ac7c32e1:quality/counters/c1-r56-autoreload-entry.py | sha256sum
2b2ef41b3329edde1b30a88ab13f9430b3522d052186b4eb00ebb154a0301fea  -
```

The entry and registry did change between those revisions, so the fixture edits were reapplied to **tip content**, not the old content. Mutant specifications and fixture transforms were reused from the two reports' delivered Python drivers; this is a reproduction, not an independently authored fixture design.

```
python3 -I /fast/scratch/hyaku/mado-r56/R56W3MutKillC1/kill_c1.py
BASE rc=0 MADO_AUTORELOAD_ENTRY: rev=0ff94937c4e4660eccd1f85ff4463c687087cf06 rows=30/30 hosts=3/3 sources=30/30 scope=30/30 content=33/33 new_rows=8/8 verdict=TARGET_MET missed=none
PAIRS 51  KILLED 51  SURVIVED 0  ERRORS 0
```

Each detector invocation was:

```
python3 -I <pristine-or-mutant-counter> --repo <isolated-fixture-repo> --rev <fixture-commit> --work <seat-scratch-work>
```

The same fixture and revision were passed to pristine and mutant. Baseline expectations came from the reports, not the mutant. Examples:

- A:M05 / A-F01: pristine `TARGET_MISSED missed=row:K01`; mutant `TARGET_MET missed=none`.
- A:M13 and A:M14 / A-F05: pristine `missed=row:K01,quote:K01`; each mutant `missed=row:K01`.
- A:M34 / A-F10: pristine `TARGET_MET`; mutant `TARGET_MISSED missed=tok:K24`.
- A:M37 / A-F11: pristine `TARGET_MET`; mutant `TARGET_MISSED missed=num:H02`.
- A:M28 / A-F09: pristine `scope=20/30`, `scope:K03`…`scope:K12`; mutant `scope=30/30 TARGET_MET`.

```
python3 -I /fast/scratch/hyaku/mado-r56/R56W3MutKillC1/compare_reports.py
MISMATCHES: 0
```

All A pristine must-have/must-not checks held; B's reported baseline/mutant exit-status pairs all reproduced. All 49 tree patches applied successfully to fresh exports. **Limit:** the round-trip routine checks application success and records the resulting tree OID; it does not compare that OID to an independently retained fixture-tree OID. Do not read its `OK` as an additional tree-equality proof.

The cross-fixture matrix exercised all 51 named mutant records against the 49 tree fixtures. It is preserved in `receipts/kill-results.json`; it is supplementary, not a widened target.

## How the kills can land without weakening expectations

Final route checks used the existing harness's LINE_RE, `_need`, `judge_good` and `judge_control`:

```
python3 -I /fast/scratch/hyaku/mado-r56/R56W3MutKillC1/prove_routes_final.py
carrier histogram: {'CONTROL-1': 29, 'NEGATIVE': 17, 'CONTROL-N': 4, 'CLI': 1}
routes proved: 51/51
```

- **29 single-leg controls:** assert a leg actually lost by the mutant, not merely the row's most obvious leg. A:M12 requires a collateral leg such as `echo:K08` or `source_cell:K08`; asserting only `row:K08` does not kill it. A:M13/M14 require `quote:K01`; A:M18 requires `host:H01`.
- **4 exact-output/leg-set controls:** B:M19/F19, B:M25/F25, B:M29/F29 and B:M50/F50 report a superset of pristine legs. An existence-only `_need` assertion passes on both. The kill requires forbidding the spurious legs or asserting the exact expected set.
- **17 acceptance/selftest cases:** pristine is TARGET_MET, mutant rejects or crashes. These cannot be ordinary `judge_control` negative-tree controls, because that function requires TARGET_MISSED. They need an acceptance assertion. “Accepted by the frozen counter” does not independently prove semantic correctness of the fixture's prose.
- **1 CLI case:** B:M69/F69 passes a tree OID as `--rev`; pristine exits 2, mutant exits 0/TARGET_MET.

A scratch-only extended copy of the harness exercised all single-leg and exact-set control carriers end to end:

```
python3 -I /fast/scratch/hyaku/mado-r56/R56W3MutKillC1/harness_proof.py
PRISTINE with the extended harness: rc=0 MADO_R56_CONTROLS: claim=c1 good=ok controls=44/44 verdict=OK
proved kills: 33/33
```

The number 44 belongs **only to that disposable experiment** (12 existing controls plus 32 distinct fixture controls; A-F05 kills two mutants). The landed frozen harness remains 12 controls. Acceptance/selftest and CLI routes were evaluated from recorded outputs; they were not installed into a modified production selftest suite.

## Findings and severity

1. **Weakens test coverage, not a new claim failure:** the proposed fixtures reproduce the reported missing branch coverage. Existence-only checks are insufficient for the four B exact-set cases above. Input B-F25, for example, yields pristine `missed=row:K05`, mutant `missed=row:K05,quote:K05`; requiring only `row:K05` lets that mutant survive.
2. **Cosmetic evidence annotation errors:** B's `fixtures.py` expectation strings for F06 and F49 say `none (TARGET_MET)`, while its measured report table and this reproduction both show pristine rc 1/TARGET_MISSED. F06's pristine hides K06 onward; F49's pristine loses scope coverage beginning at K05. The measured tables reproduced; the prose annotations should not become executable expectations.
3. **Domain restriction, intentionally unchanged:** A-F21/F22 edit the frozen tables and trip `tables_sha`; they do not establish a kill within sha-valid inputs for A:M16/M53. B-F50 deletes a pin as well as editing the registry. B-F62 is a mode mutation, and B-F69 is CLI-only. These are explicitly marked rather than represented as entry/registry-only fixtures.

No new blocking failure of PRED-C1-r56-v2 was established by this probe. Previously reported numeral-adjacency and short/long S-token behavior is reproduced as frozen-counter behavior, not repaired or redefined.

## Deliverables

All paths below are absolute:

- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3MutKillC1/fixtures/INDEX.tsv` — **51-row runner checklist**, survivor → fixture → observed kill line, route and harness-proof status.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3MutKillC1/fixtures/manifest.json` — full per-pair outputs and final route records, including both A-F05 mutants.
- Same `fixtures/` directory: **49 exact patches**, namespaced metadata files and per-mutant JSON records. B-F69 has metadata but no tree patch.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3MutKillC1/receipts/kill-c1.txt` — decisive detector transcript.
- Same `receipts/`: `kill-results.json`, `harness-proof.txt/json`, `routes-final.txt/json`, `restoration.json`, `hashes.txt`, `compare-reports.txt`.
- `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-56/w3/R56W3MutKillC1/run/` — source drivers and copied report transforms. They retain explicit seat-scratch paths and require recreating the archived base before reuse; they are provenance, not a turnkey installed test suite.

## Restoration, limits and cleanup

```
python3 -I /fast/scratch/hyaku/mado-r56/R56W3MutKillC1/restore_probe.py
RESTORED 51 behavior_matches 51 pristine_sha256 2b2ef41b3329edde1b30a88ab13f9430b3522d052186b4eb00ebb154a0301fea
```

`restoration.json` records each mutated source hash, restored source hash and restored detector output. Source copies were overwritten with the exact pristine bytes before the restored runs. The lane counter was never edited. Final lane status inspection reported **zero tracked changes**; unrelated concurrent untracked wave artifacts were left untouched.

No tools installed or upgraded. No host compositor/config changes, network calls, subagent dispatch or lane git mutations. Python invocations used `python3 -I`. Intermediate scratch-driver errors (commit argument, patch-parent availability, parser/tuple mistakes) were corrected before the final measured runs; no failed baseline was counted as a kill.

Scratch removal is recorded after receipt preservation. No semantic entailment audit, production selftest changes, or frozen-predicate changes were performed.

Self-evaluation: accuracy 4/5 (all claimed differentials and restoration outputs retained; patch equality beyond successful application not independently checked); completeness 4/5 (all named records covered, but acceptance cases not installed into a production suite); clarity 4/5 (directions and domain restrictions explicit); actionability 4/5 (exact patches/checklist provided, drivers need base setup); conciseness 3/5 (extra carrier investigation adds substantial evidence beyond the assigned probe). Improvement applied: final manifest preserves both A-F05 mutant records and labels scratch-only harness counts explicitly.
