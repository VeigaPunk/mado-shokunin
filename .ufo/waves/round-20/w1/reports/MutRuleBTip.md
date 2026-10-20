# MutRuleBTip — 7 legacy-suite kills, 8 survivors; all 15 specimens restored

## Scope and axes

Assigned probe only: 15 independent, single-line mutations of HelperFn rule B and its helper-resolution dependencies at **`e629f731172b8238caffe50f152217ce56535fb4`**. No implementation was integrated and no lane verdict is issued here.

Axes named: **detector sensitivity**, **E1–E3 precision/evidence fidelity**, **exact restoration**, and **host safety**. Work was parallelized locally with a six-worker pool; no subagent was dispatched.

- Immutable source acquisition actually run: `git -C /home/vgpnk/Projects/shokunin/mado-shokunin show e629f731172b8238caffe50f152217ce56535fb4:tools/mado-tripwire.py`; captured as file bytes in the isolated scratch directory `/tmp/mado-r20-MutRuleBTip-3-qh_ljxaj`. This was a scratch directory, not a clone, so it has no checkout HEAD.
- Pristine SHA-256: **`367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d`**. Every specimen began with those exact bytes; mutations were separate files `M01/tool.py` through `M15/tool.py` under that scratch directory.
- Interpreter observed: **Python 3.14.8**. Every classifier invocation used `-I` and a scratch cwd.
- The eleven named existing suites were copied once, preserving symlinks, into the scratch tree before any detector run. The same copies were used for every pristine, mutated, and restored specimen. Fixture Python and shell text was **only parsed by the tripwire, never executed**.
- Context read: `/home/vgpnk/Projects/shokunin/mado-shokunin/SCORECARD.md:1228-1283`; `/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/lessons/round-19-verifier-spotcheck.md:63-91,145-156`.

## Expected detector

For **each** of the 15 specimen paths and **each** of the three phases, the bounded detector was the target tool's unchanged CLI:

```text
python3 -I <absolute scratch specimen>/tool.py --selftest <absolute copied suite directory>
```

`--selftest` runs the tool's parser over committed-format transcript fixtures and checks expected exits/findings; it does not run fixture commands. All eleven suites were run per mutant, including after the first failing suite. Outer timeout: 180 seconds per suite; no timeout occurred. The driver checks all tool bytes and all expectation-file digests before launching any parser subprocess. Its source SHA-256 was `428ddd4d355ae374dc5b6b40e601ce37f5a76e2c69029395307a4f5f0748a9b1`.

The source directories and exact copied `expected.json` digests were:

| Suite | Unique existing cases | Copied expected.json SHA-256 |
|---|---:|---|
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core` | 9 | `e8aff6efb9ce06eefac457d8dc8afa79405f2167c426f2c23900bc314b06b920` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound` | 16 | `eef778eac31181f9c76519ff7a0b01c368e2f5255c12791e13c0f0fc7ce065e2` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening` | 33 | `2d63cd7dfb6c4fdf2ee5f548547b6a8397f603db070abd22dd26c0dc83c30b80` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/w2-regressions` | 30 | `8a98c12b706203b710e9075117e0883987a453da4fa59ba156894de86b9ebd2e` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen` | 31 | `61741eae60cc8eb5f657c6feb9d447d8363715ecad618a2524e98aeb08fdba66` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/r18-failsafe` | 1 | `2bdacc98d259ced11017a6e49280423c694f2c314b236d92201a36a9ab729fee` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-bashcvar` | 45 | `6303675695ffa90059e6e014d03a87795f5a08ae96bd911f39d01b1d1672e602` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-frozen-f1f2` | 13 | `c1f1fcf397e2093bd92cb24a05ff7a001a1a704949f5dd512e4ce566999d5534` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-helperfn` | 34 | `717782d80f373bea30615d29d634b19061b5f38d4a0903648736cbcf9fcccda7` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-installers` | 18 | `7bdb0a0c2eb40296fa9acb7b6d02d131c5d0d6a17782bc23fb8491a59de69b2b` |
| `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-vcs` | 17 | `8a5e3ffd5b46a2bc62b6e65abdf3b744443cd11f32d18dcf429d1b9c044b0e31` |

Counts are derived from the actual suite receipts, not estimated from filenames. There are **247 unique existing cases**, not 11,115 independent cases. The latter is the repeated execution count, 247 × 15 specimens × 3 phases.

## Actual suite output and bounded verdict

| Phase | Suite executions passing / run | Case executions passing / run | Timeouts |
|---|---:|---:|---:|
| baseline | 165/165 | 3705/3705 | 0 |
| mutated | 158/165 | 3684/3705 | 0 |
| restored | 165/165 | 3705/3705 | 0 |

**Legacy-suite verdict: killed 7/15; survived 8/15; inconclusive 0/15.** Every pristine and restored specimen passed 247/247. All mutant failures were ordinary expected-finding mismatches, in `r19-helperfn`; every other suite passed for every mutant. No syntax-error or timeout was counted as a kill.

The exact behavior-bearing changes below refer to the immutable `e629f73:tools/mado-tripwire.py`, not a moving working-tree tool. Each mutation changed exactly the one listed source line; the detector's preflight byte comparison enforced that restriction.

| Mutant | Source line | Single-point behavior change | Mutated cases passed | Legacy-suite verdict |
|---|---:|---|---:|---|
| M01 | 1389 | Discard all rows produced by `helper_argv_leads`. | 245/247 | **killed** |
| M02 | 1386 | Read only the first positional argument in `helper_argv_leads`. | 245/247 | **killed** |
| M03 | 1386 | Read only the last positional argument in `helper_argv_leads`. | 246/247 | **killed** |
| M04 | 1387 | Fold lead arguments against `{}` instead of the bound helper environment. | 247/247 | **survived** |
| M05 | 1253 | Remove builtin `list` from `PURE_ARG_CALLS` (rename its entry to `__list`). | 247/247 | **survived** |
| M06 | 1256 | Add unconditional `frozenset` purity, including when that name is rebound. | 247/247 | **survived** |
| M07 | 1370 | Disable insertion into the same-cell `funcs` index. | 241/247 | **killed** |
| M08 | 1371 | Replace duplicate-definition rejection with one global last-definition entry, without per-call binding history. | 246/247 | **killed** |
| M09 | 1370 | Exclude builtin/pure spellings from the `funcs` index, even when defined in the text. | 247/247 | **survived** |
| M10 | 1412 | Reduce the helper recursion bound from depth < 4 to depth < 3. | 247/247 | **survived** |
| M11 | 1412 | Skip helper expansion when its signature has positional-only parameters. | 247/247 | **survived** |
| M12 | 1415 | Inspect only the first call found in an expanded helper body. | 247/247 | **survived** |
| M13 | 1417 | Discard recursively resolved helper findings. | 240/247 | **killed** |
| M14 | 1432 | Ignore the `PURE_ARG_CALLS` exemption in the lead branch. | 245/247 | **killed** |
| M15 | 1431 | Treat attribute/method calls like bare-name lead candidates. | 247/247 | **survived** |

### Actual failing-case output

These are the literal `CASE ... FAIL` lines captured from the mutated detector runs. A tuple is the legacy selftest's `(class, rule, JSONL line, optional filename)` key; it has **no evidence component**. Baseline/restored summaries for the same suite were `SELFTEST_SUMMARY: 34/34 passed failed=[]`, exit 0, for every specimen.

**M01**, mutated suite exit 1:

```text
SELFTEST_SUMMARY: 32/34 passed failed=['py-lead-cross-cell-literal', 'py-lead-two-calls']
CASE py-lead-cross-cell-literal FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
CASE py-lead-two-calls FAIL want=(1, [('package_query', 'pacman:-Qi', 1, '')]) got=(0, [])
```

**M02**, mutated suite exit 1:

```text
SELFTEST_SUMMARY: 32/34 passed failed=['py-lead-cross-cell-literal', 'py-lead-two-calls']
CASE py-lead-cross-cell-literal FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
CASE py-lead-two-calls FAIL want=(1, [('package_query', 'pacman:-Qi', 1, '')]) got=(0, [])
```

**M03**, mutated suite exit 1:

```text
SELFTEST_SUMMARY: 33/34 passed failed=['py-lead-cross-cell-literal']
CASE py-lead-cross-cell-literal FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
```

**M07**, mutated suite exit 1:

```text
SELFTEST_SUMMARY: 28/34 passed failed=['py-helper-shell-string', 'py-helper-shell-kw', 'py-helper-defined-after-call', 'py-helper-nonspawn-body', 'py-helper-binop-body', 'py-helper-default-nonliteral']
CASE py-helper-shell-string FAIL want=(1, [('package_query', 'pacman:-Qi', 1, '')]) got=(0, [])
CASE py-helper-shell-kw FAIL want=(1, [('host_mutation', 'pacman:-S', 1, '')]) got=(0, [])
CASE py-helper-defined-after-call FAIL want=(0, []) got=(1, [('package_query', 'pacman:-Q', 1, '')])
CASE py-helper-nonspawn-body FAIL want=(0, []) got=(1, [('package_query', 'pacman:-Q', 1, '')])
CASE py-helper-binop-body FAIL want=(0, []) got=(1, [('package_query', 'pacman:-Q', 1, '')])
CASE py-helper-default-nonliteral FAIL want=(0, []) got=(1, [('package_query', 'pacman:-Q', 1, '')])
```

**M08**, mutated suite exit 1:

```text
SELFTEST_SUMMARY: 33/34 passed failed=['py-helper-redefined']
CASE py-helper-redefined FAIL want=(0, []) got=(1, [('host_mutation', 'pacman:-S', 1, '')])
```

**M13**, mutated suite exit 1:

```text
SELFTEST_SUMMARY: 27/34 passed failed=['py-helper-literal-list', 'py-helper-shell-string', 'py-helper-shell-kw', 'py-helper-two-hop', 'py-helper-keyword', 'py-helper-literal-twice', 'py-lead-nested-literal']
CASE py-helper-literal-list FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
CASE py-helper-shell-string FAIL want=(1, [('package_query', 'pacman:-Qi', 1, '')]) got=(0, [])
CASE py-helper-shell-kw FAIL want=(1, [('host_mutation', 'pacman:-S', 1, '')]) got=(0, [])
CASE py-helper-two-hop FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
CASE py-helper-keyword FAIL want=(1, [('package_query', 'pacman:-Sl', 1, '')]) got=(0, [])
CASE py-helper-literal-twice FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
CASE py-lead-nested-literal FAIL want=(1, [('package_query', 'pacman:-Q', 1, '')]) got=(0, [])
```

**M14**, mutated suite exit 1:

```text
SELFTEST_SUMMARY: 32/34 passed failed=['py-helper-nonspawn-body', 'py-lead-pure-print']
CASE py-helper-nonspawn-body FAIL want=(0, []) got=(1, [('package_query', 'pacman:-Q', 1, '')])
CASE py-lead-pure-print FAIL want=(0, []) got=(1, [('package_query', 'pacman:-Q', 1, '')])
```

### Legacy assertions are not E1–E3 conformance

- The old `--selftest` key at `e629f731172b8238caffe50f152217ce56535fb4:tools/mado-tripwire.py:2055-2060` compares class, rule, line, and sometimes filename. It never compares `evidence`. All actual finding rows in the survivor probes below omitted the `evidence` key; **O*** below means only the round-20 comparison rule's default of **unmarked → observed**, not that the old tool emitted an explicit marker.
- **M08 is killed by a legacy expectation that conflicts with the supplied round-20 contract.** `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-helperfn/expected.json:118-123` expects `py-helper-redefined` to be clean. Its fixture line 1 contains two identical visible spawning definitions, then a call with literal `"pacman -S wayland"`. M08 produces `host_mutation/pacman:-S` and the suite fails. [INFERENCE] Under E3's latest-preceding-binding rule, the call reaches the second visible spawn and should instead be observed. The 7/15 number is therefore a **legacy-suite kill count**, not seven proofs of round-20 semantics. A global-last-definition implementation would still be wrong for a call before a later redefinition.
- Another legacy discrepancy is visible in `py-helper-defined-after-call`: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-19/tripwire/r19-helperfn/expected.json:111-115` wants clean, while its fixture line 1 calls `run_record(['pacman', '-Q', 'wayland'])` before defining `run_record`. [INFERENCE] E3's preceding-binding rule makes the call an unbound-name lead, not clean. No expectation was edited in this probe.

## Surviving shapes → eight case proposals

Each proposal below was **actually scanned** against pristine bytes, its associated mutant, and restored bytes. Each is one assistant `eval` toolCall on **JSONL line 1**, with `arguments.language = "py"` and `arguments.code` equal to the displayed snippet. The fixture code was never run. All finding rows shown below normalize the missing evidence key as O*, exactly as the declared precision counter does.

For a wanted row, the full expected tuple is `(package_query, pacman:-Q, 1, <evidence>)`; wanted clean means exit 0 and an empty findings multiset. These are proposals in this report only, not additions to the precision suite.

### M04: `L-MutRuleBTip-bound-argv-to-invisible-callee`

```python
def visible(argv):
    return hidden(argv)
visible(['pacman','-Q','wayland'])
```

**Expected under E1–E3:** exit 1; `want_findings = [{"class":"package_query","rule":"pacman:-Q","line":1,"evidence":"lead"}]`. A literal argument forwarded by a visible helper reaches an invisible callee; only a lead is established.

| Actual bytes | Exit | Finding-key excerpt |
|---|---:|---|
| baseline | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |
| mutated | 0 | `[]` |
| restored | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |

Fixture SHA-256: `4a9bbe19ce24062750f8e8372f8fee1886b2d6f886ecb7ef215dc0072f49e689`.
**Candidate-detector result: inconclusive as a mutant kill.** Pristine/restored already fail the required lead marker; the mutant additionally loses the row. This is a baseline E1 gap plus an untested argv-forwarding shape, not permission to claim a kill or weaken the required lead evidence. Its legacy-suite result remains survived.

### M05: `P-MutRuleBTip-list-is-data`

```python
BLOCK = list(['pacman','-Q','wayland'])
```

**Expected under E1–E3:** exit 0; `want_findings = []`. An unrebound builtin list only constructs data.

| Actual bytes | Exit | Finding-key excerpt |
|---|---:|---|
| baseline | 0 | `[]` |
| mutated | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |
| restored | 0 | `[]` |

Fixture SHA-256: `e7d39515d7960b402263eec6d7e162df71995b9a873889e0e2bbc89d83aec9df`.
**Candidate-detector result:** pristine/restored pass the declared row-key comparator and the mutant fails it. This provides a discriminating case proposal for the legacy-suite survivor. Explicit evidence-field/count assertions must still be included when this is adopted.

### M06: `S-MutRuleBTip-frozenset-shadowed-lambda-spawn`

```python
import subprocess
frozenset = lambda argv: subprocess.run(argv)
frozenset(['pacman','-Q','wayland'])
```

**Expected under E1–E3:** exit 1; `want_findings = [{"class":"package_query","rule":"pacman:-Q","line":1,"evidence":"observed"}]`. The latest preceding binding is a visible spawning lambda, not the builtin.

| Actual bytes | Exit | Finding-key excerpt |
|---|---:|---|
| baseline | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |
| mutated | 0 | `[]` |
| restored | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |

Fixture SHA-256: `94967fa7588bc6751627d1244dc8dfe6c627b5106e1dccef46724d3ba7a45a28`.
**Candidate-detector result:** pristine/restored pass the declared row-key comparator and the mutant fails it. This provides a discriminating case proposal for the legacy-suite survivor. Explicit evidence-field/count assertions must still be included when this is adopted.

### M09: `S-MutRuleBTip-list-shadowed-def-spawn`

```python
import subprocess
def list(argv):
    return subprocess.run(argv)
list(['pacman','-Q','wayland'])
```

**Expected under E1–E3:** exit 1; `want_findings = [{"class":"package_query","rule":"pacman:-Q","line":1,"evidence":"observed"}]`. A builtin spelling must not defeat its visible spawning def binding.

| Actual bytes | Exit | Finding-key excerpt |
|---|---:|---|
| baseline | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |
| mutated | 0 | `[]` |
| restored | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |

Fixture SHA-256: `55b1a85c502144270a19f3f392a880f1ec4096419fdede7dccd0140aa329796b`.
**Candidate-detector result:** pristine/restored pass the declared row-key comparator and the mutant fails it. This provides a discriminating case proposal for the legacy-suite survivor. Explicit evidence-field/count assertions must still be included when this is adopted.

### M10: `W-MutRuleBTip-four-visible-helpers`

```python
import subprocess
def hop4(argv):
    return subprocess.run(argv)
def hop3(argv):
    return hop4(argv)
def hop2(argv):
    return hop3(argv)
def hop1(argv):
    return hop2(argv)
hop1(['pacman','-Q','wayland'])
```

**Expected under E1–E3:** exit 1; `want_findings = [{"class":"package_query","rule":"pacman:-Q","line":1,"evidence":"observed"}]`. Four visible helper expansions remain inside the declared depth-four bound.

| Actual bytes | Exit | Finding-key excerpt |
|---|---:|---|
| baseline | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |
| mutated | 0 | `[]` |
| restored | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |

Fixture SHA-256: `be70fc33278aff5ccb2143087852707b9efa39683d9f950d25e3c89c0bf026ec`.
**Candidate-detector result:** pristine/restored pass the declared row-key comparator and the mutant fails it. This provides a discriminating case proposal for the legacy-suite survivor. Explicit evidence-field/count assertions must still be included when this is adopted.

### M11: `W-MutRuleBTip-positional-only-helper`

```python
import subprocess
def launch(argv, /):
    return subprocess.run(argv)
launch(['pacman','-Q','wayland'])
```

**Expected under E1–E3:** exit 1; `want_findings = [{"class":"package_query","rule":"pacman:-Q","line":1,"evidence":"observed"}]`. The visible positional-only parameter receives the literal argv and reaches a spawn.

| Actual bytes | Exit | Finding-key excerpt |
|---|---:|---|
| baseline | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |
| mutated | 0 | `[]` |
| restored | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |

Fixture SHA-256: `e8941970371efa6f7fd2f9c6bd8e2fc703570493c1059d7ad55a68c8c5332dfc`.
**Candidate-detector result:** pristine/restored pass the declared row-key comparator and the mutant fails it. This provides a discriminating case proposal for the legacy-suite survivor. Explicit evidence-field/count assertions must still be included when this is adopted.

### M12: `W-MutRuleBTip-spawn-after-data-call`

```python
import subprocess
def launch(argv):
    tuple(argv)
    return subprocess.run(argv)
launch(['pacman','-Q','wayland'])
```

**Expected under E1–E3:** exit 1; `want_findings = [{"class":"package_query","rule":"pacman:-Q","line":1,"evidence":"observed"}]`. An earlier pure call in the helper body must not hide its later spawn.

| Actual bytes | Exit | Finding-key excerpt |
|---|---:|---|
| baseline | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |
| mutated | 0 | `[]` |
| restored | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |

Fixture SHA-256: `06f8418a613ceb56b3d0070c06feb1bff71e690e1d123ba84c850e0b9c2fb1eb`.
**Candidate-detector result:** pristine/restored pass the declared row-key comparator and the mutant fails it. This provides a discriminating case proposal for the legacy-suite survivor. Explicit evidence-field/count assertions must still be included when this is adopted.

### M15: `P-MutRuleBTip-literal-join-is-data`

```python
DISPLAY = ' '.join(['pacman','-Q','wayland'])
```

**Expected under E1–E3:** exit 0; `want_findings = []`. An attribute formatter call stays pure under E2.

| Actual bytes | Exit | Finding-key excerpt |
|---|---:|---|
| baseline | 0 | `[]` |
| mutated | 1 | `[package_query / pacman:-Q / JSONL 1 / O* (evidence key absent)]` |
| restored | 0 | `[]` |

Fixture SHA-256: `d8dfbcd522ed6b001b9e9b9a3010da4046d669b7dfe6f9b701fac2f7190ec5ef`.
**Candidate-detector result:** pristine/restored pass the declared row-key comparator and the mutant fails it. This provides a discriminating case proposal for the legacy-suite survivor. Explicit evidence-field/count assertions must still be included when this is adopted.

## Before / mutant / restoration hashes

All 15 before hashes and all 15 restored hashes equal **B** below. Each mutant hash differs from B. Restoration was performed with the inverse single-line edit, then compared **byte-for-byte**, not merely by checksum; the complete eleven-suite detector was rerun for every restored specimen.

```text
B = 367be94773d8fec5e6df91f80ac777070c407c1128f7c75b3dcaa26cc83fdb4d
```

| Mutant | Before SHA-256 | Mutant SHA-256 | Restored SHA-256 / bytes |
|---|---|---|---|
| M01 | B | `5cbac5078d6c9443ed3aea91963cfc898b78deb80efad8952c63a52d5d1182fb` | B / exact |
| M02 | B | `76040723d6b785ff6433608473d1d1d7a5c2e5c7684de386b95a94e219eba8be` | B / exact |
| M03 | B | `971cbf880a1325de861f9d6a240a42e8a25f685c660bd7b28fea1ddd9eea3045` | B / exact |
| M04 | B | `b739a4443b2882ecd3a4a60a028a5d9ca656248f6b4e79ce30b6eea92dd2cbd1` | B / exact |
| M05 | B | `2c77f6089c928b70a615f4a83b0abfae6990527a8b8ba9bd006a90731b6fada6` | B / exact |
| M06 | B | `101a33d7e4b9bd22665268ce3cfb0a83cf9cf8454c6b66e6b1c96aee444553c6` | B / exact |
| M07 | B | `8c8165a6cd8aaab9d39ec8bb37a50a1e16006801a0f0bc4776533416ffe5ff61` | B / exact |
| M08 | B | `8743d85351090ee77d36143463a5f839234bd1433aca80c723c003fc412d8177` | B / exact |
| M09 | B | `6457b08a66ab65b892585863b1374c4c891fb0322d25d19c2b02c4a4f594a3ea` | B / exact |
| M10 | B | `34520dd25c62ee0ae94b6d7708582bff40028b475330908a0e50f09dbaf8771c` | B / exact |
| M11 | B | `a947fa4615468e1524fba1d26623f7c87cfcc396de5a101732b605d790201b40` | B / exact |
| M12 | B | `a6c7a3e46ae301045d5a2847b53061b51f799d850908dd0d473d229ec723b4b2` | B / exact |
| M13 | B | `84321e4a2642eced7f84872942ac39dacd496b4c5982cb321f536dbc71dadbfc` | B / exact |
| M14 | B | `9e6791baa5c69240d68d6946b0257d408ae4dd7149b01c77a94db84d3b02e092` | B / exact |
| M15 | B | `aaa94a2c44190d04a707e0dfa4200f49567ca7a63489f075e0c0f031d426494b` | B / exact |

The first inverse-edit batch was rejected atomically because its M11 replacement accidentally repeated the mutated line. Hash recording showed that **none** of the 15 files had been restored by that rejected batch. Anchors were reread, the replacement was corrected, and the successful inverse batch restored all 15 exact originals **before** any restored-phase detector invocation. No restored result is based on the rejected edit.

## Receipt pointers and reproducibility

The report contains the complete mutation definitions, source/expectation hashes, all failing-case output, all proposal payloads and their observed comparisons, and exact restoration evidence; its claims do not depend solely on a temporary pointer. Full per-suite stdout/stderr and commands remain locally at:

- `/tmp/mado-r20-MutRuleBTip-3-qh_ljxaj/receipts/<baseline|mutated|restored>/MNN-<suite>.json` (495 suite receipts).
- `/tmp/mado-r20-MutRuleBTip-3-qh_ljxaj/baseline.json`: SHA-256 `053271fa6a2be58f80a08443af8b9092c3bf813e234de4f17a182dfe39498e7f`.
- `/tmp/mado-r20-MutRuleBTip-3-qh_ljxaj/mutated.json`: SHA-256 `dc830a0d648776aa22874e0d33da910e3163a8f1b6a79590b8ef9003356b7c9b`.
- `/tmp/mado-r20-MutRuleBTip-3-qh_ljxaj/restored.json`: SHA-256 `95305f979ad828b7e5d6f75b4ca8252af30daa2441c9bd523a99fa1f584ad39a`.
- `/tmp/mado-r20-MutRuleBTip-3-qh_ljxaj/proposal-probes.json`: SHA-256 `d740e5fc13003004989508803034319d1d1d659f78b96c3d390de7d90f6c3b3f` (24 scans, including restored).
- `/tmp/mado-r20-MutRuleBTip-3-qh_ljxaj/restoration.json`: SHA-256 `1fe28053d6c218f3b6f28c0db93be700039d3dc0a60b0a838d71bd92c934150a`.

Actual driver invocations, from that absolute scratch cwd, were `python3 -I /tmp/mado-r20-MutRuleBTip-3-qh_ljxaj/run_suites.py baseline`, the same with `mutated`, and the same with `restored`. Exits were respectively **0, 1, 0**. The initial asynchronous Bash launch was refused at the host background-job cap before executing; the completed detector runs were launched via Python's subprocess API through Eval, using the same interpreter and commands, not another runtime.

A fresh reader can reconstruct each mutant from the pinned `git show` bytes using the following exact line table, copy the eleven suite directories listed above while preserving symlinks, and run `python3 -I <tool> --selftest <copied-suite>` for all three byte states. Baseline or restoration failure must be marked inconclusive. The table is executable **data**, not an invitation to execute any fixture code:

```python
# (id, original source line, exact before line, exact mutant line)
MUTATIONS = [
    ('M01', 1389, '            out.extend(classify_shell(shlex.join(vals)))', '            out.extend([])'),
    ('M02', 1386, '    for a in node.args:', '    for a in node.args[:1]:'),
    ('M03', 1386, '    for a in node.args:', '    for a in node.args[-1:]:'),
    ('M04', 1387, '        vals = argv_strings(literal_value(a, env))', '        vals = argv_strings(literal_value(a, {}))'),
    ('M05', 1253, '    "print", "list", "tuple", "set", "dict", "sorted", "reversed", "repr", "str",', '    "print", "__list", "tuple", "set", "dict", "sorted", "reversed", "repr", "str",'),
    ('M06', 1256, '    "setattr", "iter", "next", "input",', '    "setattr", "iter", "next", "input", "frozenset",'),
    ('M07', 1370, '        if isinstance(node, ast.FunctionDef) and not node.decorator_list:', '        if isinstance(node, ast.FunctionDef) and False and not node.decorator_list:'),
    ('M08', 1371, '            funcs[node.name] = None if node.name in funcs else (node.lineno, node)', '            funcs[node.name] = (node.lineno, node)'),
    ('M09', 1370, '        if isinstance(node, ast.FunctionDef) and not node.decorator_list:', '        if isinstance(node, ast.FunctionDef) and node.name not in PURE_ARG_CALLS and not node.decorator_list:'),
    ('M10', 1412, '        if helper is not None and node.lineno > helper[0] and depth < 4:', '        if helper is not None and node.lineno > helper[0] and depth < 3:'),
    ('M11', 1412, '        if helper is not None and node.lineno > helper[0] and depth < 4:', '        if helper is not None and node.lineno > helper[0] and depth < 4 and not helper[1].args.posonlyargs:'),
    ('M12', 1415, '                body = [n for n in ast.walk(helper[1]) if isinstance(n, ast.Call)]', '                body = [n for n in ast.walk(helper[1]) if isinstance(n, ast.Call)][:1]'),
    ('M13', 1417, '                hits.extend(inner)', '                hits.extend([])'),
    ('M14', 1432, '                    and name not in PURE_ARG_CALLS):', '                    and True):'),
    ('M15', 1431, '            if (isinstance(node.func, ast.Name) and helper is None', '            if (isinstance(node.func, (ast.Name, ast.Attribute)) and helper is None'),
]
```

Counting command actually used through Eval: load the three phase JSON arrays; for each array sum the two integers captured by `re.search(r'SELFTEST_SUMMARY: (\d+)/(\d+) passed', row['summary'])`; group `row['exit']` by mutant. A mutant is killed only when all 11 baseline/restored exits are zero and at least one mutated suite exit is nonzero. Results: baseline 3,705/3,705, mutated 3,684/3,705, restored 3,705/3,705; seven groups killed and eight survived. The source has 247 unique cases; these repeated run totals do not increase coverage breadth.

## Limits

- This is a bounded mutation/coverage probe of **e629f73**, not a review or verification of the pending round-20 implementation, claim admission, integration, or shipping.
- Only the eleven requested existing suites and the eight explicitly displayed proposal payloads were exercised. The round-20 precision counter, six-incident recall counter, real-transcript controls, whole-corpus no-harm diff, gate selftest/regression, calibration counters, and pre-harm `9c54c56` were **not run** by this seat.
- The suite copies came from the specified existing directories at snapshot time. Their expectation hashes are recorded above; this probe did not independently authenticate every fixture byte to a historical commit. Frozen-mode checks ran as cases inside the requested suites; no additional frozen-corpus replay is claimed.
- The legacy comparator does not assert `evidence`, `observed_findings`, or `lead_findings`. Seven candidate proposals distinguish mutants under the declared row-key normalization; that does not establish explicit-marker/schema compliance. M04's extra candidate detector is baseline-red and therefore inconclusive as a kill.
- M08's historical clean expectation conflicts with the supplied E3 semantics, as detailed above. No test expectation or contract was changed to improve a kill count.
- No paused host tool, service/compositor/input operation, live gate, package transaction/query, screenshot, external runtime, network source, lane VCS write, or fixture payload was executed. Only this report was written inside the lane; all mutation tools, fixture copies and raw receipts stayed in this seat's isolated `/tmp` tree. Exact original bytes were restored even for failing mutant detectors.

## Installs

none
