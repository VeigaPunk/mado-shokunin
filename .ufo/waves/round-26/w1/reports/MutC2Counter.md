# MutC2Counter — frozen C2 counter mutation probe

## Verdict

**Six of six mutants KILLED by the full bounded detector; zero inconclusive probes; exact counter bytes restored after every mutant.**

The three requested valid-output doubles alone leave **two survivors**: the BASE-stability guard bypass and acceptance of non-JSON. Explicit BASE drift and non-JSON boundary witnesses kill those mutants. Population assertions are essential: dropping V3 produces `TARGET_MET` at **31/31**, not the registered 51/51.

This probes counter sensitivity, not resolver correctness or a real control meeting C2. PERFECT receives the oracle answer through a test double; it is not a submitted tool implementation. No counter repair, integration, or production-tool edit was made.

## Scope and detector

Axes: predicate fidelity; one small isolated defect at a time; identical detector before/mutated/restored; bounded, host-isolated oracle work.

All mutations were confined to:

`/fast/scratch/hyaku/mado-r26/mut/MutC2Counter/.ufo/waves/round-26/c2/count.py`

The scratch layout also contains byte-identical copies of the pinned oracle and V3 generator. Only this report was written in the lane. `tools/mado-binds.py` and `tools/mado-anims.py` were neither edited nor built.

Detector: `/fast/scratch/hyaku/mado-r26/mut/MutC2Counter/probe.py`, SHA256 `b67828334fab6c065af6506f39b7af65e5615e52424a9afd9e14d7b68708c5c2`. The detector was unchanged throughout. `mutations.json` in the same directory records the six mutations and intended witnesses before the first mutation was applied.

Each of 18 suites runs the same five scenarios:

| Scenario | Injection and expected pristine/restored behavior |
| --- | --- |
| PERFECT | Monkeypatched `O.run_tool` deep-copies the case's selected oracle table. Exactly `51/51`, `embed_hits=0`, `TARGET_MET`, exit 0. |
| NEAR-MISS | PERFECT except the last bind's `arg` in **A29 only** gains `__r26_one_arg_fault__`. All other fields and cases are unchanged. Exactly `50/51`, only A29 fails with `missing=1 extra=1`, exit 1. |
| EMBED | PERFECT output, but the actual `--tool-file` bytes scanned by the counter contain `# omarchy-menu`. This is a real BASE-table **arg of length 12**, inside the required 12–999 range. Exactly `51/51`, `embed_hits=1`, `TARGET_MISSED`, exit 1. |
| BASE-DRIFT | PERFECT plus a deep-copied second BASE oracle result whose first bind's `arg` gains `__r26_base_drift__`. Expected `ORACLE_UNSTABLE (1/1)`, exit 2, no CASE rows, no tool calls. |
| NON-JSON | `O.run_tool` returns `(None, 'stdout is not JSON')` for every case, matching its invalid-JSON boundary contract. Exactly `0/51`, `embed_hits=0`, `TARGET_MISSED`, exit 1. |

Every scored scenario additionally requires exactly **one BASE, 30 ARITH and 20 V3 CASE rows**. The detector checks fixed 51 totals, not merely exit codes or the `TARGET_MET` label. Expected BASE-DRIFT exit 2 is a successful guard-fault witness, not an accidental baseline failure counted as a kill.

The tool double reads `lab` and `exp` from the counter's calling frame; it does not infer labels from sandbox paths. The counter still reads and scans real override file bytes:

- Ordinary bytes: `print("[]")\n`; SHA256 `a3381e95441354d833917bdaf481a5b210edf2b8cda6419b5e1805dfe143fd3b`.
- EMBED bytes: `print("[]")\n# omarchy-menu\n`; SHA256 `ecc32b95fe49e9980346aaa033ef11ca58166b2508ea84f016160d019db0831a`.

### Oracle capture and replay

The first PERFECT scenario captured **52 actual isolated oracle calls**: two independent BASE runs and 50 generated cases. BASE contained 192 binds and both independent results agreed. Subsequent scenarios replay these actual tables by SHA256 of the full case tree, retaining separate `base0` and `base1` cache entries. The ARITH=3 mutant changes the generator's later RNG state; its 20 different V3 trees caused **20 additional real oracle calls**, not guessed expected values. Total: **72 real oracle calls**, 72 bounded cache entries.

All actual calls used the copied, pinned `oracle.py`'s `oracle()` function. No other compositor startup method was used. Build/pin checks remained active. The in-memory `LANE` path was pointed back to the lane solely for the counter's read-only REV lookup; no scratch git repository was needed.

The frozen snapshot has 79 files, digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`; full-tree replay key `055b9b770328d0fc5aee552967a897a004d89de8d2fc6736294222a70506719f`. Seed: `c2de7ec70a26`. Resolved REV: `05319e0fed2ce25cf0a883380af2763a85fd4936`.

## Kill table

Line anchors below refer to pristine `c2/count.py`; each change was restored before the next mutation.

| ID | Smallest applied defect | Decisive actual mutant output | Expected detector | Verdict |
| --- | --- | --- | --- | --- |
| M1 | `:34` `EMBED_MIN = 12` → `1000` | EMBED: `51/51 embed_hits=0 verdict=TARGET_MET`, exit 0 | EMBED must produce one hit and exit 1 | KILLED |
| M2 | `:164` `if n1 or n2:` → `if False:` | BASE-DRIFT: `ORACLE_CHECK base_twice equal binds=192`; `51/51 embed_hits=0 verdict=TARGET_MET`, exit 0 | Drift must abort before scoring with exit 2 | KILLED |
| M3 | After `:57`, insert `V3.FIELDS.remove("arg")` | NEAR-MISS: `51/51 embed_hits=0 verdict=TARGET_MET`, exit 0. BASE-DRIFT also incorrectly passes. | A29's changed 18th field must fail; exactly `50/51`, exit 1 | KILLED |
| M4 | `:33` `V3_PER_TYPE = 2` → `0` | PERFECT: `31/31 embed_hits=0 verdict=TARGET_MET`, exit 0; population BASE=1, ARITH=30, V3=0 | Fixed 51 and 20 V3 rows, irrespective of the mutant's self-reported denominator | KILLED |
| M5 | `:32` `NARITH = 30` → `3` | PERFECT and NEAR-MISS: `24/24 embed_hits=0 verdict=TARGET_MET`, exit 0; A29 is absent | Fixed 30 ARITH rows; A29 near-miss must be exercised and rejected | KILLED |
| M6 | `:206` malformed-output verdict `False` → `True` | NON-JSON: `CASE BASE PASS ... stdout is not JSON`; `51/51 embed_hits=0 verdict=TARGET_MET`, exit 0 | Invalid JSON must fail all 51 cases, exit 1 | KILLED |

### Complete observed outcome matrix

Cells are `cases_pass ; embed_hits ; exit`. `U;2` means the expected `ORACLE_UNSTABLE` setup error with no scoring. Exit 0 cells above are `TARGET_MET`; scored exit 1 cells are `TARGET_MISSED`.

| Bytes | PERFECT | NEAR-MISS | EMBED | BASE-DRIFT | NON-JSON |
| --- | --- | --- | --- | --- | --- |
| Every pristine/restored suite | 51/51;0;0 | 50/51;0;1 | 51/51;1;1 | U;2 | 0/51;0;1 |
| M1 | 51/51;0;0 | 50/51;0;1 | 51/51;0;0 | U;2 | 0/51;0;1 |
| M2 | 51/51;0;0 | 50/51;0;1 | 51/51;1;1 | 51/51;0;0 | 0/51;0;1 |
| M3 | 51/51;0;0 | 51/51;0;0 | 51/51;1;1 | 51/51;0;0 | 0/51;0;1 |
| M4 | 31/31;0;0 | 30/31;0;1 | 31/31;1;1 | U;2 | 0/31;0;1 |
| M5 | 24/24;0;0 | 24/24;0;0 | 24/24;1;1 | U;2 | 0/24;0;1 |
| M6 | 51/51;0;0 | 50/51;0;1 | 51/51;1;1 | U;2 | 51/51;0;0 |

### Survivors and reasons

- **Full five-scenario detector:** none survived. No baseline or restoration suite failed.
- **Only PERFECT / NEAR-MISS / EMBED, even with exact counts:** M2 and M6 survived. Stable BASE replay never exercises instability rejection, and these three doubles always return valid parsed tables. Their substantive outcomes are identical to pristine under that subset. This is a coverage finding, not permission to weaken C2.
- **An exit/label-only consumer of those three scenarios:** M4 also survives; all three exit codes still match despite dropping the complete V3 family. The observed 31/31 receipt demonstrates why fixed denominator and family assertions are necessary. This is a mutant/consumer witness, not a cheap shape meeting the frozen 51/51 predicate.
- Scope limit: NON-JSON injects the existing `O.run_tool` failure tuple. It tests the counter's handling, not the harness's subprocess JSON decoder. Replay likewise does not independently validate Hyprland or the oracle implementation.

## Pristine → mutated → restored evidence

Let **H** be `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8`, the registered frozen counter SHA256. Each suite records hashes both before and after execution; they were equal within every suite.

| Mutant | Before SHA256 | Mutated SHA256 | Restored SHA256 | Detector checks: before / mutant / restored |
| --- | --- | --- | --- | --- |
| M1 | H | `fcbce4b6ea5753df72c6488f4cc9728f28629a10605ef3b0cc7c1645d73a6937` | H | 5/5 / 4/5 / 5/5 |
| M2 | H | `a9727feee024a57af85b3ee4b5a726121fae4250938053aba25b6068448974ca` | H | 5/5 / 4/5 / 5/5 |
| M3 | H | `5506d3a1331134ce038ac78de273595aa1d5b7248ff2e02a2a162f11e20a9157` | H | 5/5 / 3/5 / 5/5 |
| M4 | H | `5e789317ad1c307e10656e55ddb6bdf020a6a21a433dba64e86f95ee97ee9fd1` | H | 5/5 / 1/5 / 5/5 |
| M5 | H | `5747b3dfc3a7973e908572c3d944a596087f1fa6ab6bbe3522e6ade132d8dca0` | H | 5/5 / 1/5 / 5/5 |
| M6 | H | `e6a983ef36e51eda768204e09f64f336312dda8e0df4fe5f319878e2d3812632` | H | 5/5 / 4/5 / 5/5 |

All six pristine suite commands and all six restored suite commands exited **0**. All six mutant detector commands exited **1**, as intended. For every mutant, all five restored raw counter receipts have exactly the same SHA256 as their corresponding pristine receipt—not just matching final counts. There were no accidental ORACLE_FAIL, pin failures, or harness exceptions.

Final hashes of the scratch counter, scratch pristine backup, and untouched lane counter all equal H. The scratch and lane oracle both remain `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441`; scratch and lane V3 generator both remain `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`.

## Commands and receipt locations

Initial space check, cwd `/home/vgpnk/Projects/shokunin`:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 prlimit --as=4000000000 df -h /fast
```

Observed `/fast`: 804G size, 619G used, **185G available**. Scratch directories were created with `mkdir -p`; `cp` copied the three frozen files to their matching relative paths under `MutC2Counter/`, and copied `c2/count.py` to `MutC2Counter/count.pristine.py`. No git/jj write command was run. The detector performs only the frozen counter's read-only `git rev-parse` operation against the lane.

Exact per-suite invocation, cwd `/fast/scratch/hyaku/mado-r26/mut/MutC2Counter` (`STAGE` replaced by the literals below):

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 900 prlimit --as=4000000000:8000000000 python3 -I -B probe.py STAGE
```

Actual order:

```text
m1-pristine
m1-mutant
m1-restored
m2-pristine
m2-mutant
m2-restored
m3-pristine
m3-mutant
m3-restored
m4-pristine
m4-mutant
m4-restored
m5-pristine
m5-mutant
m5-restored
m6-pristine
m6-mutant
m6-restored
```

Restored/pristine adjacent invocations for M1/M2 through M5/M6 were joined with `&&`; mutations and restorations were separate surgical `edit` operations. Each mutation was reversed immediately after its detector returned, including expected nonzero returns. No detector invocation rewrites counter bytes.

Evidence root: `/fast/scratch/hyaku/mado-r26/mut/MutC2Counter/`.

- `receipts/<STAGE>-<SCENARIO>.txt`: **90 verbatim counter stdout receipts**, including each `exit=` line; 418,725 bytes total. Scenarios are `PERFECT`, `NEAR-MISS`, `EMBED`, `BASE-DRIFT`, `NON-JSON`.
- `<STAGE>.json`: 18 suite records with expected/actual outcomes, before/after counter hashes, raw receipt hashes, populations, tool hashes, and real/replayed oracle-call counts.
- `oracle-cache/*.json`: bounded real oracle tables, keyed by the complete case tree; BASE has two independent entries.
- `snapshot/`, `snapshot-meta.json`: fixed four-root input snapshot and its identity.
- `probe.py`, `mutations.json`, `count.pristine.py`: detector, mutation specification, and exact original bytes.

Decisive receipts: `m1-mutant-EMBED.txt`, `m2-mutant-BASE-DRIFT.txt`, `m3-mutant-NEAR-MISS.txt`, `m4-mutant-PERFECT.txt`, `m5-mutant-NEAR-MISS.txt`, `m6-mutant-NON-JSON.txt`, all under `receipts/`.

Every emitted HOST_SAFETY line was exactly:

```text
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
```

The oracle's normal `finally` path terminates and waits for each sandbox process group; all 72 calls returned, and every started detector process exited. No service was started. Outer memory limits were soft 4 GB/hard 8 GB so the pinned oracle could establish its own 8 GB limit, per L1's safety correction. Cache entries are capped at 128, each table at 2 MB, and each receipt at 500 KB. No tools were installed or updated.

Only the assigned mutation probe was run; no lane builds, linters, implementation tests, or production control scores were run.
