# MutEvidence — partly falsified: 10/12 mutants killed; two evidence-total defects survive both requested detectors

## Scope and axes

Assigned mutation probe only, against `28c68378eccbd5f227cdc28a62406ff390e3540a`. This report challenges detector coverage of evidence markers, lead retention, purity exemptions, and reset bindings; it does **not** adjudicate the round or integrate a tool change.

Axes named: **behavioral discrimination**, **observed/lead fidelity**, **pure-data precision**, **exact restoration**, and **host isolation**. Twelve independent one-line mutants were tested. Work ran through a four-worker local Python pool, without subagent dispatch or another agent runtime.

**Result:** the precision counter detects all ten row/lead/purity/reset mutants. The eleven existing suites detect four of those ten. Both requested detectors miss two non-equivalent mutants that zero the emitted evidence totals. Those survivors are coverage gaps, not permission to weaken the totals contract. The claimed pristine `172/175` and existing-suite `247/247` were reproduced; neither numeric result is falsified by this probe.

## Pinned acquisition and execution

The isolated clone was created with these commands, actually run:

```sh
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r20w2-MutEvidence
git -C /tmp/mado-r20w2-MutEvidence remote remove origin
git -C /tmp/mado-r20w2-MutEvidence checkout -q --detach 28c6837
```

- Target tool: `/tmp/mado-r20w2-MutEvidence/tools/mado-tripwire.py`, SHA-256 **`9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`**.
- Counter: committed `a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-20/tw-precision.py`, copied to `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-20/tw-precision.py`; SHA-256 `bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7`.
- Precision suite pin: **`f3da50488661509ce5d144c90f7780f8088e0903`**, supplied explicitly on every counter invocation.
- Eleven existing suites: committed bytes at target `28c6837`, including its round-20 expectation corrections; their expectation hashes are below.
- Interpreter observed: Python **3.14.8**. Actual child interpreter path was `/usr/bin/python`; every parser/counter invocation used `-I`.
- Source specimens: `/tmp/mado-r20w2-MutEvidence/mutation-lab/M01/tool.py` through `/tmp/mado-r20w2-MutEvidence/mutation-lab/M12/tool.py`.
- Each precision mutation was committed only as an immutable scratch Git object, using its specimen as the sole changed blob at `tools/mado-tripwire.py`. The counter reads committed bytes, so merely editing an uncommitted specimen would not have tested a mutant. Temporary indices, HOME, and Git configuration were redirected under the scratch clone; no push occurred.
- All fixture commands remained **transcript data parsed by the tripwire**, never executed. In particular, package-manager and host-operation strings appearing in outputs below are classifier findings, not executed host commands.

The bounded detector per subject was:

```text
/usr/bin/python -I /tmp/mado-r20w2-MutEvidence/.ufo/waves/round-20/tw-precision.py REV --suite-rev f3da50488661509ce5d144c90f7780f8088e0903
/usr/bin/python -I TOOL --selftest SUITE
```

`REV` is the exact scratch commit in the mutant table below; `TOOL` is its absolute specimen path; each of the eleven absolute `SUITE` paths below was supplied separately. Baseline used `REV=28c68378eccbd5f227cdc28a62406ff390e3540a` and `/tmp/mado-r20w2-MutEvidence/mutation-lab/pristine.py`. After all specimens were restored and byte-compared, the restored control used that same pristine committed blob for the counter and `/tmp/mado-r20w2-MutEvidence/mutation-lab/M01/tool.py` for the eleven selftests.

**Controls were shared, not inflated:** one complete pristine control, twelve complete mutant runs, then one complete restored control. All twelve specimens started from identical bytes and all twelve were individually confirmed byte-identical after restoration. This is 14 counter invocations plus 154 selftest invocations, **168 requested detector commands**. Outer bounds were 360 seconds per precision invocation and 300 seconds per selftest; no timeout, parse error, or abnormal detector failure occurred. An initial attempt to launch the pristine driver asynchronously was rejected by the global background-job cap before execution; the probe was instead run synchronously through Python subprocesses.

## Baseline rule: pre-existing failures are not mutant kills

Pristine and restored precision outputs both reported:

```text
P 66/66; S 17/17; W 21/22; H 51/52; L 17/18
172/175; score 9.8286; counter exit 0
```

These three precision expectations already fail in pristine bytes, and remain unsuitable as mutant-kill evidence:

```text
W-CaseWrapperForms-class-method-instance
L-AdoptW2-AdvHelperFn-b14
H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help
```

Every kill recorded below has at least one **different case that passes pristine, fails under the mutant, and passes restored**. No pre-existing failure was counted as a kill. The restored precision case objects matched the pristine case objects exactly. All eleven pristine and restored selftests passed.

The counter exits `0` when evaluation succeeds even if cases fail (`/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-20/tw-precision.py:229-241`); all fourteen counter processes returned `0`. Therefore counter process exit alone would discriminate none of these mutants. The results here compare its actual per-case verdicts, not just exit status or an assumed all-green aggregate.

## Mutants and actual requested-detector outcomes

Source lines below refer to `/tmp/mado-r20w2-MutEvidence/tools/mado-tripwire.py` at `28c6837`. Each specimen changed **only the single stated line**. “New precision failures” excludes the three pristine failures above. No baseline failure became a pass in any mutant.

| ID | Line | Single behavior change | Precision passed / 175 | New precision failures | Existing cases passed / 247 | Verdict under requested detectors |
|---|---:|---|---:|---:|---:|---|
| M01 | 2063 | Always assign `evidence = "observed"`. | 151 | 21 | 243 | **killed** |
| M02 | 2063 | Always assign `evidence = "lead"`. | 127 | 45 | 241 | **killed** |
| M03 | 2065 | Require `evidence != "lead"` before retaining a unique hit. | 151 | 21 | 243 | **killed** |
| M04 | 2064 | Deduplicate by `(cls, rule)` instead of `(cls, rule, evidence)`. | 171 | 1 | 247 | **killed by precision; legacy survivor** |
| M05 | 1397 | Remove `"frozenset"` from `PURE_ARG_CALLS`. | 168 | 4 | 247 | **killed by precision; legacy survivor** |
| M06 | 1397 | Remove `"list"` from `PURE_ARG_CALLS`. | 171 | 1 | 247 | **killed by precision; legacy survivor** |
| M07 | 1409 | Remove `"collections"` from `PURE_STDLIB_MODULES`. | 165 | 7 | 247 | **killed by precision; legacy survivor** |
| M08 | 1414 | Remove `"shlex.join"` from `PURE_STDLIB_EXACT`. | 166 | 6 | 247 | **killed by precision; legacy survivor** |
| M09 | 1404 | Add opaque helper name `"run_record"` to `PURE_ARG_CALLS`. | 170 | 2 | 244 | **killed** |
| M10 | 2114 | Change observed total from `sum(1 ...)` to `sum(0 ...)`. | 172 | 0 | 247 | **survived — missing total assertion** |
| M11 | 2116 | Change lead total from `sum(1 ...)` to `sum(0 ...)`. | 172 | 0 | 247 | **survived — missing total assertion** |
| M12 | 2050 | On reset, use `binding_envs.setdefault("py", {})` instead of replacing bindings with `{}`. | 170 | 2 | 247 | **killed by precision; legacy survivor** |

Thus the requested combined detector has **10 killed, 2 survived** for this assigned set. The three pristine-failing precision expectations are inconclusive as individual mutation oracles; they do not turn into three additional mutant kills.

### Discriminating precision output excerpts

These are extracted `want`/`got` facts from the actual counter JSON, not re-executed fixture code. For each named case in this table, pristine and restored `got` equal the stated `want`.

`Q1(E)` abbreviates exactly `{"class":"package_query","rule":"pacman:-Q","line":1,"evidence":E}`; `Q3(E)` is the same row at line 3. Empty findings are `[]`.

| Mutant | Case | Expected detector result | Actual mutant output |
|---|---|---|---|
| M01 | `L-CaseLeadsInvisible-run-record` | exit 1, `[Q1("lead")]` | exit 1, `[Q1("observed")]`, `pass:false` |
| M02 | `S-CaseShadowing-print-lambda-spawn` | exit 1, `[Q1("observed")]` | exit 1, `[Q1("lead")]`, `pass:false` |
| M03 | `L-CaseLeadsInvisible-run-record` | exit 1, `[Q1("lead")]` | exit 0, `[]`, `pass:false` |
| M04 | `L-AdoptW2-AdvHelperFn-c03` | exit 1, `[Q1("lead"),Q1("observed")]` | exit 1, `[Q1("observed")]`, `pass:false` |
| M05 | `P-CasePureBuiltins-frozenset-direct` | exit 0, `[]` | exit 1, `[Q1("lead")]`, `pass:false` |
| M06 | `P-CasePureCallables-plain-class-init` | exit 0, `[]` | exit 1, `[Q1("lead")]`, `pass:false` |
| M07 | `P-CasePureCollections-deque` | exit 0, `[]` | exit 1, `[Q1("lead")]`, `pass:false` |
| M08 | `P-CasePureFormatters-shlex-join` | exit 0, `[]` | exit 1, two line-1 `host_mutation` leads, rules `pacman:-S` and `sudo`; `pass:false` |
| M09 | `L-CaseLeadsInvisible-run-record` | exit 1, `[Q1("lead")]` | exit 0, `[]`, `pass:false` |
| M12 | `L-CasePureCrossCell-reset-clears-helper` | exit 1, `[Q3("lead")]` | exit 0, `[]`, `pass:false` |

The mixed observed-plus-lead pin is real: `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-20/precision/expected.json:2782` names c03 and pins both rows. The pure-set and reset pins are independently located at that same file's lines 20, 398, and 664. **M04 did not survive the new suite**; c03 specifically kills omission of evidence from the dedup key.

### Eleven existing suites: actual outputs and hashes

Every absolute path below was used with `--selftest` for pristine, **every mutant**, and the restored shared control. All expectation hashes were obtained from target-commit bytes and matched the copies used. Counts are registered case entries, not an assertion of independent fixture populations.

| Absolute suite path | Pristine / restored summary | SHA-256 of `expected.json` |
|---|---|---|
| `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-17/tripwire/core` | `SELFTEST_SUMMARY: 9/9 passed failed=[]` | `e8aff6efb9ce06eefac457d8dc8afa79405f2167c426f2c23900bc314b06b920` |
| `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-17/tripwire/compound` | `SELFTEST_SUMMARY: 16/16 passed failed=[]` | `eef778eac31181f9c76519ff7a0b01c368e2f5255c12791e13c0f0fc7ce065e2` |
| `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-17/tripwire/hardening` | `SELFTEST_SUMMARY: 33/33 passed failed=[]` | `2d63cd7dfb6c4fdf2ee5f548547b6a8397f603db070abd22dd26c0dc83c30b80` |
| `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-17/tripwire/w2-regressions` | `SELFTEST_SUMMARY: 30/30 passed failed=[]` | `8a98c12b706203b710e9075117e0883987a453da4fa59ba156894de86b9ebd2e` |
| `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-18/tripwire/frozen` | `SELFTEST_SUMMARY: 31/31 passed failed=[]` | `61741eae60cc8eb5f657c6feb9d447d8363715ecad618a2524e98aeb08fdba66` |
| `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-18/tripwire/r18-failsafe` | `SELFTEST_SUMMARY: 1/1 passed failed=[]` | `2bdacc98d259ced11017a6e49280423c694f2c314b236d92201a36a9ab729fee` |
| `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-19/tripwire/r19-bashcvar` | `SELFTEST_SUMMARY: 45/45 passed failed=[]` | `e72a97def0c67617984962c4b3276b6127862daa4d48f9dabd5ae845437abbe5` |
| `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-19/tripwire/r19-frozen-f1f2` | `SELFTEST_SUMMARY: 13/13 passed failed=[]` | `c1f1fcf397e2093bd92cb24a05ff7a001a1a704949f5dd512e4ce566999d5534` |
| `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-19/tripwire/r19-helperfn` | `SELFTEST_SUMMARY: 34/34 passed failed=[]` | `91e247912827aa5848a7ce87ef7c59273c6681d737f6456d87180f251ded3644` |
| `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-19/tripwire/r19-installers` | `SELFTEST_SUMMARY: 18/18 passed failed=[]` | `7bdb0a0c2eb40296fa9acb7b6d02d131c5d0d6a17782bc23fb8491a59de69b2b` |
| `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-19/tripwire/r19-vcs` | `SELFTEST_SUMMARY: 17/17 passed failed=[]` | `8a5e3ffd5b46a2bc62b6e65abdf3b744443cd11f32d18dcf429d1b9c044b0e31` |

All mutant suites passed except these five executions (ordinary expectation failures, exit 1):

```text
M01 r19-helperfn:
SELFTEST_SUMMARY: 30/34 passed failed=['py-helper-defined-after-call', 'py-lead-cross-cell-literal', 'py-lead-two-calls', 'py-lead-nonliteral-var']

M02 r19-bashcvar:
SELFTEST_SUMMARY: 44/45 passed failed=['r19-class-body-deferred-clean']
M02 r19-helperfn:
SELFTEST_SUMMARY: 29/34 passed failed=['py-helper-nonliteral-arg', 'py-helper-redefined', 'py-helper-vararg', 'py-helper-default-nonliteral', 'py-lead-defined-nonliteral']

M03 r19-helperfn:
SELFTEST_SUMMARY: 30/34 passed failed=['py-helper-defined-after-call', 'py-lead-cross-cell-literal', 'py-lead-two-calls', 'py-lead-nonliteral-var']

M09 r19-helperfn:
SELFTEST_SUMMARY: 31/34 passed failed=['py-helper-defined-after-call', 'py-lead-cross-cell-literal', 'py-lead-nonliteral-var']
```

Actual discriminating selftest lines include:

```text
M01:
CASE py-lead-cross-cell-literal FAIL want=(1, [('package_query', 'pacman:-Q', 1, '', 'lead')]) got=(1, [('package_query', 'pacman:-Q', 1, '', 'observed')])
M02:
CASE r19-class-body-deferred-clean FAIL want=(1, [('package_query', 'pacman:-Q', 1, '', 'observed')]) got=(1, [('package_query', 'pacman:-Q', 1, '', 'lead')])
M03 / M09:
CASE py-lead-cross-cell-literal FAIL want=(1, [('package_query', 'pacman:-Q', 1, '', 'lead')]) got=(0, [])
```

Execution totals, counted from the captured detector results:

| Phase | Detector commands | Precision case evaluations passing / run | Existing case evaluations passing / run | Timeouts |
|---|---:|---:|---:|---:|
| Shared pristine | 12 | 172/175 | 247/247 | 0 |
| Twelve mutants | 144 | 1954/2100 | 2947/2964 | 0 |
| Shared restored | 12 | 172/175 | 247/247 | 0 |

These are **5908 repeated registered case evaluations**, not 5908 independent cases. The mutant phase has 127/132 passing existing-suite executions. Six row/purity/reset mutants caught by precision survive all eleven existing suites; the new suite supplies real discriminatory coverage beyond `247/247`.

## Surviving defects: emitted totals are not asserted

**M10 and M11 are non-equivalent survivors.** The existing fixture already contains both evidence types, but neither requested detector checks the aggregate totals against the finding rows:

- Counter row normalization/comparison: `/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-20/tw-precision.py:77-100,179-201` compares class/rule/line/evidence and exit, not `observed_findings` or `lead_findings`.
- Selftest comparison: `/tmp/mado-r20w2-MutEvidence/tools/mado-tripwire.py:2533-2542` likewise checks rows and exit but not those totals.
- The tool documents the two totals at `/tmp/mado-r20w2-MutEvidence/tools/mado-tripwire.py:106-107`, computes them at lines 2114-2116, and emits them at line 2119.

A supplementary **count-consistency observation**, separate from the requested mutation verdict, was run before mutation, on M10/M11, and again on both restored specimens. It used this exact committed fixture, SHA-256 **`9b1738616b9ab6eaa5a77b3cdd21c34098b097ecb630d35dc5e0c057959f39c5`**:

`/tmp/mado-r20w2-MutEvidence/.ufo/waves/round-20/precision/CaseAdoptW2--AdoptW2-AdvHelperFn-c03.jsonl:1`

Its eval code is transcript data:

```python
import subprocess
def go():
    return subprocess.run(['pacman','-Q','a'])
go(); log_argv(['pacman','-Q','b'])
```

The supplementary command shape, actually expanded for pristine, M10, M11, restored M10, and restored M11, was:

```text
/usr/bin/python -I TOOL --scan /tmp/mado-r20w2-MutEvidence/.ufo/waves/round-20/precision/CaseAdoptW2--AdoptW2-AdvHelperFn-c03.jsonl
```

`TOOL` was `/tmp/mado-r20w2-MutEvidence/mutation-lab/pristine.py`, `/tmp/mado-r20w2-MutEvidence/mutation-lab/M10/tool.py`, or `/tmp/mado-r20w2-MutEvidence/mutation-lab/M11/tool.py` as appropriate. Every scan printed `MADO_TRIPWIRE: findings`, returned the expected exit 1, and retained the same two rows: one observed and one lead, both `package_query/pacman:-Q`, JSONL line 1. Actual output fields were:

| Bytes scanned | Observed rows | Lead rows | `observed_findings` | `lead_findings` | Totals equal row counts? | SHA-256 of complete stdout |
|---|---:|---:|---:|---:|---|---|
| pristine | 1 | 1 | 1 | 1 | yes | `261a9e05fd932ed814a5c765239c85e47233b38a1163b5173db105b3ba3e5629` |
| M10 | 1 | 1 | **0** | 1 | **no** | `64fa21c94f317ee4994d7b41eeecc6e64da0ad88613c1ea25190a5d7a322e338` |
| M11 | 1 | 1 | 1 | **0** | **no** | `0a95a2f179cf2b83067d5a4080c5f3f7f61bb0c793ea1670081a6b3f730ce54c` |
| restored M10 | 1 | 1 | 1 | 1 | yes | `261a9e05fd932ed814a5c765239c85e47233b38a1163b5173db105b3ba3e5629` |
| restored M11 | 1 | 1 | 1 | 1 | yes | `261a9e05fd932ed814a5c765239c85e47233b38a1163b5173db105b3ba3e5629` |

Thus adding assertions for the two documented equations would discriminate both survivors using **existing committed fixture bytes**:

```text
observed_findings == number of finding rows whose evidence is "observed"
lead_findings     == number of finding rows whose evidence is "lead"
```

This is a scoped detector-gap finding only. The requested-detector verdict remains **survived** for M10/M11; the extra observation does not retroactively make the registered suites kill them. Pristine totals were correct in this probe; the finding is not an assertion that the shipped tool already emits the mutant totals.

## Mutation hashes and exact restoration

Common **before** and **restored** SHA-256 for every specimen:

```text
9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c
```

The smallest behavior changes are fully specified above, permitting reconstruction from the committed target even after scratch cleanup. Scratch commit IDs below are local experiment objects, not lane commits.

| ID | Mutated SHA-256 | Exact scratch commit used by `tw-precision.py` | Restored exact bytes? |
|---|---|---|---|
| M01 | `6b616c3d16d790393c2bb6b3853a8e5909bcc9a76cc21d3bb6b68f067f9d813f` | `352a78e2e8f0c4f05c2060ab44cc82f33e10bf64` | yes |
| M02 | `e53c0b3dcb28777e358a0f3bfc5f92ce60657e4f7155fca3beccd8227e98f43a` | `b92b9a1e66f0408ac5989c2e0bc812d8ccf19432` | yes |
| M03 | `b38ca7be03e6dfcbb82034ce309d425c365cc42ed00fbd50315695445658bca4` | `8b79e6fc6e927bdfa9517596822828337ef52a64` | yes |
| M04 | `d869aa7504b6e65db5d68d313dee92eb74824375f11b2c69281993ecc74d5a9d` | `9f5d741e010da35e019a1523c51938066cca86da` | yes |
| M05 | `4cafc5be4b0a885dc2e458ef4df03a63df64aafba762da3f29f0d1b6b07ebc4e` | `d88f1a8776729a03b72d8fbdba1d58da4aeeb07f` | yes |
| M06 | `38043aea9bf622b6b851e5b2c4a7247f13657d9b857045059fb49bf24f0f93a9` | `ffdbcb2627a08d30fe504de0d2cf0850efd6136e` | yes |
| M07 | `7927abf68cf3ac090e1028d3d2db429a7c2cbccae4fbe37ce237117bbb095b51` | `6ff25171a6082ddcdb7b7644a1cf94c04278c1d5` | yes |
| M08 | `2a5177b7b3d7244b9d1eef45c0fde72048302e563b395791b9e05472dd0d7a5d` | `f0e8c98240ae8c62dce72af187d7c13bfc906771` | yes |
| M09 | `e3ec2c459682cc534fb749dbe9fb21ea10fd55e6cff9c6bd28537fa774ea543b` | `a7f69862b19a3464b60856ce9c138ea9b64fc102` | yes |
| M10 | `968d1ecc46c7579b3386878867b9b49adec8b479c068760ea4d584a52b54413f` | `c0efea12fda6f2dc8560257c2eeeef602918fcda` | yes |
| M11 | `98f296d9cc1b7811033ccd3d82c687b42c0e78b282abbf871cba8f0a2cb6b250` | `4a41eb2b1cf0c9ae444185956d8f85c1e2ef9dbc` | yes |
| M12 | `74cbe57d80dae03d020a061aeba7e98758ce62aae52f53ba8f0deae7be619dc4` | `6afd94950933f5a0288f19bf4f4416ad01f3481d` | yes |

Each one-line edit was reversed. Actual restoration output:

```text
RESTORATION 12/12 exact bytes sha256=9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c
restored_driver_exit 0
shared-restored precision exit=0 172/175
shared-restored core exit=0 9/9
shared-restored compound exit=0 16/16
shared-restored hardening exit=0 33/33
shared-restored w2-regressions exit=0 30/30
shared-restored frozen exit=0 31/31
shared-restored r18-failsafe exit=0 1/1
shared-restored r19-bashcvar exit=0 45/45
shared-restored r19-frozen-f1f2 exit=0 13/13
shared-restored r19-helperfn exit=0 34/34
shared-restored r19-installers exit=0 18/18
shared-restored r19-vcs exit=0 17/17
COUNT_RESTORED [('M10', 1, 1, True), ('M11', 1, 1, True)]
clone_tool_sha256 9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c
```

The clone's checkout tool was never itself mutated; it also retains the same hash. No tracked lane file was edited, no sibling source was touched, and the only lane write by this seat is this report.

### Raw scratch receipts

All complete stdout/stderr, commands, per-case comparisons, phase outcomes, hashes, and restoration records remain under `/tmp/mado-r20w2-MutEvidence/mutation-lab/`. These are convenience copies, not the sole durable evidence: this report embeds the mutation definitions, immutable source/suite revisions, actual discriminating outputs, and reproduction command shapes.

| Absolute artifact | SHA-256 |
|---|---|
| `/tmp/mado-r20w2-MutEvidence/mutation-lab/run-probe.py` | `fe9a952bb2fbdb1ef2151085eaa5202f1982f361a31e7ef086759837426f1416` |
| `/tmp/mado-r20w2-MutEvidence/mutation-lab/metadata.json` | `ba92d0a5b5c3a4b1b5896ce83727f6a2e6aecf430c9b5a4af4d995f21f6a154c` |
| `/tmp/mado-r20w2-MutEvidence/mutation-lab/baseline-results.json` | `573004274d179a157be34741aed186fd112f9a2049868f69aa003a7ccd3a3b5a` |
| `/tmp/mado-r20w2-MutEvidence/mutation-lab/mutated-results.json` | `b059df5954fc1a19ebddebf9a39438657c3978ee939751590abaa2f625736734` |
| `/tmp/mado-r20w2-MutEvidence/mutation-lab/restored-results.json` | `188a96337282c8a6f303acdf75f8ddaf1373102df366b38ccff8b4644a71cf59` |
| `/tmp/mado-r20w2-MutEvidence/mutation-lab/restoration.json` | `5ac5e3c0aaad4cc47ba221d0ed56402bb932779a9b970efa7bbbda4b7e5fae60` |
| `/tmp/mado-r20w2-MutEvidence/mutation-lab/count-probes.json` | `31266ca502e8c1d15a188a170994501668173f884988d448c250471d46c4cc71` |
| `/tmp/mado-r20w2-MutEvidence/mutation-lab/outcome-summary.json` | `1852f0ccc8da6e0ba3065355e5f1f6608a31cfaadfdf3811a6b093d0d52a5f6b` |

Individual raw outputs follow `/tmp/mado-r20w2-MutEvidence/mutation-lab/runs/PHASE/SUBJECT/DETECTOR.stdout` and `.stderr`; `PHASE` is `baseline`, `mutated`, or `restored`, and subjects are `shared-pristine`, M01–M12, or `shared-restored` respectively.

## Limits

- This is a bounded twelve-mutant probe, not proof of complete detector coverage or overall recall/precision. It does not independently run recall, heldout cases, whole-corpus no-harm diff, isolation canaries, or a live host gate; those are not this assignment's detectors.
- The precision aggregate is not fully green: three baseline expectations fail unchanged. They were explicitly excluded from kill decisions. “Survived” means no additional per-case mismatch and all eleven existing suites passing, not a fictitious 175/175.
- The pristine/restored composite controls were shared across byte-identical specimens, not rerun twelve times. All twelve mutated composites were run independently, and restoration bytes were checked individually.
- M10/M11 survive the **requested** detectors despite the supplementary count-consistency observation failing on them. No suite expectation or contract was changed to make a mutant survive or die.
- Scratch commits and raw receipts are local to the named clone and may be removed with `/tmp`; the committed source pin, exact one-line mutation descriptions, hashes, commands, and actual relevant outputs are included here for reconstruction.
- No tracked tool, test, documentation, scorecard, lesson, or fleet state was changed. No runtime integration, round judgment, host operation, network fetch, or installation was performed.

## Installs

none
