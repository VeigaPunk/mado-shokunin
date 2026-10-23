# MutSelftest — round 26, wave w2

**MUTSELFTEST killed=4 survived=6 inconclusive=0** across ten isolated, single-defect probes of the w1 self-test with its original C1-v1/C2 counters. Every pristine and restored run reported `SELFTEST pass=9 total=9`, process exit 0. The six survivors are coverage findings, not changes to the registered predicates.

An additional **pristine C1-v2 compatibility check failed** (`7/9`, exit 1). It is not a killed mutant; the unchanged self-test is not presently a green-baseline detector for the active C1-v2 counter. No C1-v2 mutation coverage is claimed below.

## Scope and method

Axes: behavioral discrimination, single-defect isolation, exact restoration, and host containment.

Scratch root: `/fast/scratch/hyaku/mado-r26/MutSelftest-w2` (called `S` below). Driver: `S/probe.py`.

Ten separate `git clone --quiet --shared --no-checkout` clones were created under `S`, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset. Each received byte-identical copies of the self-test, C1-v1, C1-v2, C2, the pinned oracle, and the pinned round-25 V3 generator. There was exactly one behavior-bearing mutation per clone; neither pinned dependency was mutated. All lane source bytes were left untouched. The only lane write is this report.

The same bounded self-test command was run on pristine, mutated, and restored bytes in each mirror. The command for mirror `M` was:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE \
    -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
    timeout 180 prlimit --as=4000000000 --core=0 -- \
    python3 -B -I "$S/$M/.ufo/waves/round-26/quality/counter-selftest.py" \
    --c1 "$S/$M/.ufo/waves/round-26/c1/count.py" \
    --c2 "$S/$M/.ufo/waves/round-26/c2/count.py" \
    --rev 1b0b91e9 --scratch "$S/$M/runtime"
```

The unwrapped, fully expanded commands and actual combined stdout/stderr are retained in `S/receipts/<M>.<pristine|mutated|restored>.txt`, followed by `PROCESS_EXIT=N`. `-B` prevented stale bytecode from masking restored or mutated source bytes. The detector retained its existing fixed seed, `0badc0de12345678`, in all three states; this is a mutation probe, not a fresh-seed control re-score.

Kill rule: green pristine detector, nonzero mutant detector with a named failed check, and green restored detector. A zero-exit mutant survives even if its own reported check inventory shrinks. No hash-mismatch message was counted as a kill: the self-test intentionally permits counter overrides.

## Kill table

Line numbers refer to the original files under `.ufo/waves/round-26/`. Results are `passed checks / total checks; process exit`.

| Mirror / mutant | Smallest behavior change | Expected behavioral detector | Pristine | Mutated | Restored | Verdict |
|---|---|---|---|---|---|---|
| `c1-drop-bezier` | `c1/count.py:276`: `ok = gn == en and gb == eb` → `ok = gn == en`; BASE drift comparison remains intact | A bezier-only mismatch must miss; no such self-test fixture exists | 9/9; 0 | 9/9; 0 | 9/9; 0 | **SURVIVED** |
| `c2-drop-arg` | `c2/count.py:208`: compare both entry lists after replacing only `arg` with `None`; other fields, multiplicity, and BASE guard remain intact | Existing `c2-one-field` must detect acceptance of the wrong arg | 9/9; 0 | 8/9; 1 | 9/9; 0 | **KILLED** |
| `c1-skip-base-guard` | `c1/count.py:255`: drift condition → `if False:`; both BASE calls still occur | `c1-drift` must require exit 2 and `ORACLE_UNSTABLE` | 9/9; 0 | 8/9; 1 | 9/9; 0 | **KILLED** |
| `c2-skip-base-guard` | `c2/count.py:164`: `if n1 or n2:` → `if False:` | `c2-drift` must require exit 2 and `ORACLE_UNSTABLE` | 9/9; 0 | 8/9; 1 | 9/9; 0 | **KILLED** |
| `c2-embed-min-1000` | `c2/count.py:34`: `EMBED_MIN = 12` → `1000` | `c2-embed` must require an embed hit and rejection | 9/9; 0 | 8/9; 1 | 9/9; 0 | **KILLED** |
| `c1-accept-nonjson` | `c1/count.py:268`: invalid/missing parsed-output branch records `True` instead of `False` | Invalid stdout must fail; no invalid-output self-test fixture exists | 9/9; 0 | 9/9; 0 | 9/9; 0 | **SURVIVED** |
| `c2-accept-nonjson` | `c2/count.py:206`: invalid parsed-output branch records `True` instead of `False` | Invalid stdout must fail; no invalid-output self-test fixture exists | 9/9; 0 | 9/9; 0 | 9/9; 0 | **SURVIVED** |
| `c1-pass-90pct` | `c1/count.py:286`: exact-all rule → `npass * 10 >= 9 * len(built)` | Near-complete but imperfect result must miss; no such self-test fixture exists | 9/9; 0 | 9/9; 0 | 9/9; 0 | **SURVIVED** |
| `c2-pass-90pct` | `c2/count.py:222`: same ≥90% substitution, retaining `embed_hits == 0` | Near-complete, embed-free but imperfect result must miss; no such fixture exists | 9/9; 0 | 9/9; 0 | 9/9; 0 | **SURVIVED** |
| `selftest-drop-embed-assertion` | `quality/counter-selftest.py:336–337`: delete the entire `record("c2-embed", ...)` assertion; retain its scenario execution | Missing mandatory check should be detectable; no fixed check-inventory assertion exists | 9/9; 0 | 8/8; 0 | 9/9; 0 | **SURVIVED** |

The arg mutation was exactly this single-statement replacement, not a second mutation of the pinned V3 module or its diagnostic formatting:

```python
nm, ne, missing, extra = V3.compare([dict(e, arg=None) for e in got], [dict(e, arg=None) for e in exp])
```

The non-JSON mutants are fail-open output-validation branches: they also accept other malformed shapes and tool errors routed through those branches. The self-test's `make_run_tool()` JSON parser itself was not changed.

### Actual kill outputs

From the four `*.mutated.txt` receipts:

```text
# c2-drop-arg
CHECK c2-one-field       FAIL rc=0 cases_pass=51/51 verdict=TARGET_MET
SELFTEST pass=8 total=9
FAILED c2-one-field
exit=1
PROCESS_EXIT=1

# c1-skip-base-guard
CHECK c1-drift           FAIL rc=1 ORACLE_UNSTABLE=no
      PRED-C1-r26 cases_pass=1/41 verdict=TARGET_MISSED
SELFTEST pass=8 total=9
FAILED c1-drift
exit=1
PROCESS_EXIT=1

# c2-skip-base-guard
CHECK c2-drift           FAIL rc=1 ORACLE_UNSTABLE=no
      PRED-C2-r26 cases_pass=1/51 embed_hits=0 verdict=TARGET_MISSED
SELFTEST pass=8 total=9
FAILED c2-drift
exit=1
PROCESS_EXIT=1

# c2-embed-min-1000
CHECK c2-embed           FAIL rc=0 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
SELFTEST pass=8 total=9
FAILED c2-embed
exit=1
PROCESS_EXIT=1
```

### Survivors and limits

- **Bezier-set omission:** all nine checks still pass. The only C1 bad-table fixture changes a node's `style` (`counter-selftest.py:98–101`), not a bezier. [INFERENCE] A tool with correct nodes but wrong bezier coordinates would distinguish this mutant; that additional witness was not run.
- **Accepting non-JSON (both counters):** both detectors still report 9/9, exit 0. Every generated tool uses `json.dumps(PAYLOAD)` (`:193–200`), so none exercises invalid stdout. No independent invalid-stdout tool was run in this probe.
- **≥90% pass rule (both counters):** both detectors still report 9/9, exit 0. The perfect/one-field fixtures produce all-pass versus zero-pass tables; the embed fixture remains rejected by the retained embed condition. The counter predicates were changed, but the self-test supplies no near-complete result. No independent 40/41 or 50/51 boundary witness was run.
- **Dropped self-test assertion:** the mutant reports exactly `SELFTEST pass=8 total=8`, `exit=0`, `PROCESS_EXIT=0`; the `CHECK c2-embed` row is absent. The denominator comes from `len(CHECKS)` (`:349–355`), rather than an independently required inventory. This deletes a functional assertion, not the unrelated fixture-length Python `assert` at line 113.

These observations do not claim coverage of every bind field, real Hyprland semantics, or C1-v2. No production fix, integration, or predicate change was made.

## Active C1-v2: failed pristine compatibility check

One extra run used the unchanged mirror self-test and pristine `c1/count-v2.py` instead of `c1/count.py`; C2 remained pristine. Receipt: `S/receipts/c1-drop-bezier.v2-baseline.txt`. This run preceded the mutation stage and did not use a mutated input counter.

Actual output:

```text
CHECK c1-perfect         FAIL rc=2 cases_pass=None/None verdict=None
      SETUP_ERROR ORACLE_VERSION nested Hyprland commit None is not efb50993780079460b0cbed1363e2166a2de1d9f
CHECK c1-one-field       FAIL rc=2 cases_pass=None/None verdict=None
      SETUP_ERROR ORACLE_VERSION nested Hyprland commit None is not efb50993780079460b0cbed1363e2166a2de1d9f
SELFTEST pass=7 total=9
FAILED c1-perfect,c1-one-field
exit=1
PROCESS_EXIT=1
```

Cause visible in source: `FakeOracle.__call__` returns the same synthetic animation table for every requested verb (`counter-selftest.py:146–153`), including `version`. C1-v2 requires a version object containing the pinned commit (`c1/count-v2.py:336–339`); the table is not that object. The self-test also defaults/pins C1-v1 (`counter-selftest.py:52,55`). **C1-v2 mutation results would be inconclusive with this unchanged failing baseline; none were counted as kills.**

## Hashes and exact restoration

Full original hashes below are also the final hashes, both in every restored mirror and in the lane (`lane-before.json` / `lane-after.json`). `restoration.json` records byte-for-byte comparison with the saved pristine copies for all six files in all ten mirrors: every `exact_bytes_restored` is `true`.

| ID | Source | Bytes | Before = restored = lane after SHA-256 |
|---|---|---:|---|
| A | `c1/count.py` | 13851 | `f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd` |
| B | `c2/count.py` | 10924 | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` |
| S | `quality/counter-selftest.py` | 15488 | `0754f5013800a1f61a04259b1a4bbbbee389788b251a1b831fd82994385b642a` |
| V2 | `c1/count-v2.py` | 18537 | `4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428` |
| O | `harness/oracle.py` | 11556 | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` |
| V3 | `.ufo/waves/round-25/c1/count-v3.py` | 38921 | `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375` |

Paths in the first five rows are relative to `.ufo/waves/round-26/`. In the following table, an ID in both outer columns means the full original hash above applies before and after the mutation.

| Mirror | Before | Mutant SHA-256 | After |
|---|---|---|---|
| `c1-drop-bezier` | A | `a95864cd037dd85c754ab120c7c82045c134c5332a6327e03c3b8b5762d0b747` | A |
| `c2-drop-arg` | B | `20700abfe874e824e98d6ea1d29904b361bc65a3bf60e804ff1e74b73f999d69` | B |
| `c1-skip-base-guard` | A | `8c0ac19f68b8831a3a414c90e96565223956333f605118ee1c327e19cd9b0d71` | A |
| `c2-skip-base-guard` | B | `a9727feee024a57af85b3ee4b5a726121fae4250938053aba25b6068448974ca` | B |
| `c2-embed-min-1000` | B | `fcbce4b6ea5753df72c6488f4cc9728f28629a10605ef3b0cc7c1645d73a6937` | B |
| `c1-accept-nonjson` | A | `245b99496f9412a795093368566e4101809a64ce17d17075ec520218b8d5d2a6` | A |
| `c2-accept-nonjson` | B | `e6a983ef36e51eda768204e09f64f336312dda8e0df4fe5f319878e2d3812632` | B |
| `c1-pass-90pct` | A | `a1ee1ee23476f55553b09abfce9b27a5c1fa6b1097a18fbb4db009ed67a1f10e` | A |
| `c2-pass-90pct` | B | `314be3f402a53a212eb809057d4ae2c9a72b334d9bf02e8024769a3c57ee378a` | B |
| `selftest-drop-embed-assertion` | S | `00424b619e2019ecee345d2ab820c85d34b187ae19a7303b11869d44ed4bbf04` | S |

The driver restored saved bytes in a `finally` block after the mutant stage, including after the four expected failing detector results. Final driver output:

```text
RESTORE exact=10/10
```

After separately rerunning the same detector against every restored mirror:

```text
restored c2-drop-arg SELFTEST pass=9 total=9 PROCESS_EXIT=0
restored c1-skip-base-guard SELFTEST pass=9 total=9 PROCESS_EXIT=0
restored c1-drop-bezier SELFTEST pass=9 total=9 PROCESS_EXIT=0
restored c2-skip-base-guard SELFTEST pass=9 total=9 PROCESS_EXIT=0
restored c1-accept-nonjson SELFTEST pass=9 total=9 PROCESS_EXIT=0
restored c2-embed-min-1000 SELFTEST pass=9 total=9 PROCESS_EXIT=0
restored c2-accept-nonjson SELFTEST pass=9 total=9 PROCESS_EXIT=0
restored c1-pass-90pct SELFTEST pass=9 total=9 PROCESS_EXIT=0
restored c2-pass-90pct SELFTEST pass=9 total=9 PROCESS_EXIT=0
restored selftest-drop-embed-assertion SELFTEST pass=9 total=9 PROCESS_EXIT=0
LANE exact_sources_unchanged=True
```

## Commands and retained evidence

Exact driver invocations, in execution order (the extra v2 baseline ran concurrently with the end of the pristine batch; no source was mutated until that batch completed):

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 180 prlimit --as=4000000000 --core=0 -- python3 -B -I /fast/scratch/hyaku/mado-r26/MutSelftest-w2/probe.py setup
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 --core=0 -- python3 -B -I /fast/scratch/hyaku/mado-r26/MutSelftest-w2/probe.py pristine
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 240 prlimit --as=4000000000 --core=0 -- python3 -B -I /fast/scratch/hyaku/mado-r26/MutSelftest-w2/probe.py v2-baseline
# Apply the ten isolated mutations recorded above with the edit tool.
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 --core=0 -- python3 -B -I /fast/scratch/hyaku/mado-r26/MutSelftest-w2/probe.py mutated
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 600 prlimit --as=4000000000 --core=0 -- python3 -B -I /fast/scratch/hyaku/mado-r26/MutSelftest-w2/probe.py restored
```

Evidence under `S`:

- `receipts/`: 30 pristine/mutated/restored detector receipts plus one pristine-v2 compatibility receipt; each contains its actual command and process exit.
- `runs-pristine.json`, `runs-mutated.json`, `runs-restored.json`: every result, failed-check text, receipt path, receipt SHA-256, and byte count.
- `hashes-pristine.json`, `hashes-mutated.json`, `hashes-restored.json`: six source hashes per mirror per stage.
- `restoration.json`: pre-restoration and post-restoration hashes plus exact-byte comparisons.
- `lane-before.json`, `lane-after.json`, `setup.json`, `v2-baseline.json`, and `pristine/`: source provenance and untouched saved bytes.

Host containment: `df -h /fast` reported 146G available before writes. All executable work was timeout-bounded and memory-capped; at most three offline self-tests ran in the stage driver, plus the separate short v2 compatibility run during the pristine batch. Display-instance variables were removed. The self-test monkeypatched oracle/build/snapshot/tool surfaces before executing counter scenarios; no Hyprland instance, live-compositor command, network fetch, service, or persistent process was started. Receipt `HOST_SAFETY` counts are synthetic zeroes, not a host coredump measurement. All launched commands and their finite children completed. No tool or package was installed or updated; no subagent or second agent runtime was invoked.

**Final verdict: 4 KILLED, 6 SURVIVED; all ten scratch mirrors exactly restored. Active C1-v2 self-test readiness: INCONCLUSIVE because the pristine detector fails.**
