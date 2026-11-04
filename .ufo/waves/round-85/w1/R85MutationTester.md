# R85MutationTester — independent semantic mutation probe

Axes: coverage (C1) and operability (C2). Frozen revision: `3905311c75a39c5710413105865c0a1a7dd0116a`.

## Method and boundaries

Read the frozen declaration first. No lane source changed; only this report and isolated scratch were written. No git mutation, installation, sibling runtime, or subagent dispatch.

A read-only `git archive` snapshot supplied the frozen counter, tool, cases and fixtures; archive symlinks were excluded. Fresh live observations were captured by the frozen C1 runner (72 cases) and frozen C2 runner (36 commands), both from that snapshot. C1 baseline was **72/72**, C2 baseline **36/36**. Counter mutations were scored by replaying those exact `(case, rc, stdout)` observations through their altered `expected_ok` / `case_correct` functions, including committed samples and negatives. This isolates scoring semantics from changing desktop output; it is not a claim that each mutant's complete CLI was executed. Each tool mutation was instead executed through the full frozen 72-case runner.

For every mutation the same detector ran on pristine, mutated, and exact-restored bytes. Copies were restored in place and rescored, including tool copies. Restoration hashes below equal pristine hashes. Scratch is removed at handoff; all citable findings, changes and measured outputs are retained here.

An initial C2 CLI attempt against the live lane returned `ERROR (stage=setup SKILL.md in the working tree is not the measured revision's bytes)`; this is **inconclusive**, not a mutant kill. The snapshot baseline eliminated that unrelated drift. A separate full frozen C1 CLI baseline returned `cases=72 correct=72 mutants=51 killed=51 base_correct=62/72 carried=61/61 tool_selftest=152/152 verdict=TARGET_MET`; those declared mutants are not included in the independent totals below.

## Results

**10 independent mutants: 8 survived, 2 died, 0 inconclusive after the clean snapshot baseline.** Counter-only subtotal: 7 survived, 1 died. Additional tool mutants: 1 survived, 1 died. None of the declared mutant list was selected as a mutation specification; the dict-collapse tool change has overlapping behavior with declared duplicate-collapse mutants.

| Independent mutation | Pristine → mutated → restored | Verdict / detecting case |
|---|---|---|
| C1-cause-substring | 72 → 72 → 72 / 72 | survived |
| C1-cause-casefold | 72 → 72 → 72 / 72 | survived |
| C1-stage-prefix | 72 → 72 → 72 / 72 | survived |
| C2-signal-ge128 | 36 → 35 → 36 / 36 | died — status-sigpipe-contained |
| C2-signal-gt128 | 36 → 36 → 36 / 36 | survived |
| C2-exact-low-window | 36 → 36 → 36 / 36 | survived |
| C2-long-line-search | 36 → 36 → 36 / 36 | survived |
| C2-negatives-need-samples | 36 → 36 → 36 / 36 | survived |
| C1-tool-dict-before-pairs | 72 → 69 → 72 / 72 | died — duplicate-allocation-keys, alloc-dup-key-equal, alloc-dup-key-interleaved |
| C1-tool-trailing-space-alias | 72 → 72 → 72 / 72 | survived |

## Exact semantic changes

### C1-cause-substring

Replace once:
```python
and (" cause=%s " % cause) not in stdout:
```
with:
```python
and cause not in stdout:
```

### C1-cause-casefold

Replace once:
```python
and (" cause=%s " % cause) not in stdout:
```
with:
```python
and (" cause=%s " % cause).casefold() not in stdout.casefold():
```

### C1-stage-prefix

Replace once:
```python
("ERROR (stage=%s " % stage) in stdout
```
with:
```python
("ERROR (stage=%s" % stage) in stdout
```

### C2-signal-ge128

Replace once:
```python
    if cls == "signal":
        return rc == 128 + status["signal"]
```
with:
```python
    if cls == "signal":
        return rc >= 128
```

### C2-signal-gt128

Replace once:
```python
    if cls == "signal":
        return rc == 128 + status["signal"]
```
with:
```python
    if cls == "signal":
        return rc > 128
```

### C2-exact-low-window

Replace once:
```python
    if cls == "exact":
        return rc == status["code"]
```
with:
```python
    if cls == "exact":
        return 0 < rc <= status["code"]
```

### C2-long-line-search

Replace once:
```python
        if found is not None and found.group(0) == line:
            return True
```
with:
```python
        if found is not None and (found.group(0) == line or len(line) > 256):
            return True
```

### C2-negatives-need-samples

Replace once:
```python
    for sample in case.get("negatives", []):
        if okay(sample["rc"], sample["out"]):
```
with:
```python
    for sample in (case.get("negatives", []) if case.get("samples") else []):
        if okay(sample["rc"], sample["out"]):
```

### C1-tool-dict-before-pairs

Replace once:
```python
    data = load_json(raw, "allocation", pairs_hook=allocation_pairs)
```
with:
```python
    data = load_json(raw, "allocation")
    if isinstance(data, dict):
        data = allocation_pairs(list(data.items()))
```

### C1-tool-trailing-space-alias

Replace once:
```python
        out[name] = value
    return out


def band_of
```
with:
```python
        out[name.rstrip()] = value
    return out


def band_of
```

## Smallest distinguishing additions for survivors

These are proposed additions only; the frozen population and contract were not modified. Matcher-negative tests must assert rejection, not turn a deliberately wrong output into a successful tool expectation.

- **C1-cause-substring:** one matcher-negative observation for an identity refusal: expected rc=2/stage=setup/cause=alloc-duplicate-key, observed `MADO_BARFOOT: ERROR (stage=setup cause=alloc-duplicate-key-extra message)`. Pristine returned False; mutant True.
- **C1-cause-casefold:** same matcher-negative observation with observed cause `ALLOC-DUPLICATE-KEY`. Pristine False; mutant True.
- **C1-stage-prefix:** same observation with stage `setupx` and correct cause. Pristine False; mutant True.
  These three are counter-level negative probes; adding only further correct positive tool observations cannot distinguish the weakened matchers.
- **C1-tool-trailing-space-alias:** clone `alloc-unknown-case-variant`, replace allocation with `{"waybar ":34}`, retain expected setup refusal/cause=alloc-unknown-namespace. Executed added witness: pristine **1/1**, mutant **0/1**, restored **1/1**. Mutant instead exits 0 and emits a composed result. This is a single-key exact-identity population hole.
- **C2-signal-gt128:** append one negative to `status-sigpipe-contained`: rc=142 with unchanged `MADO_STATUS: sigpipe line 0\n`. Pristine matcher False; mutant True. The frozen rc=128 negative kills `>=128`, but does not kill `>128`.
- **C2-exact-low-window:** append one negative to `status-exit7-contained`: rc=1 with unchanged `MADO_STATUS: exit7\n`. Pristine False; mutant True. The frozen negatives cover 0, 141, and wrong text at 7, not a different small nonzero status.
- **C2-long-line-search:** a new generic regex matcher case (`value: "x"`, `anchor: "line"`, status ok, live `x`, negative `x` followed by 256 `y` characters). Measured case_correct: pristine **True**, mutant **False** (negative wrongly accepted). The two frozen anchored patterns themselves contain `^...$`, masking this fallback. An attempted long suffix on the existing version pattern returned False under both; it is NOT a distinguishing case.
- **C2-negatives-need-samples:** **no additional well-formed passing ordinary case can kill this mutant.** Skipping negatives is monotone: removing rejection checks cannot lower a passing score. Smallest meaningful addition is a meta-test instrumenting matcher calls for `{kind: exact, value: x, negatives:[{rc:0,out:y}]}` with no samples and live x. Measured call trace: pristine `['x','y']`, mutant `['x']`; both return True. Assert y was evaluated. Alternatively independently mutate matching semantics and require this negative to kill that second mutant, but that is a different detector. A synthetic case with a contradictory negative would make pristine fail and is therefore not a valid kill.

The surviving counter weakenings expose limits of scoring a matcher solely on correct positive cases; they do not authorize changing the contract. The whitespace alias is directly an unrepresented tool-input defect.

## Hash and restoration evidence

SHA-256 of frozen C1 counter: `ab2306ac59f8744a51ff0d4bc4d719fc669fce03c7fe4d877872efad90d9ae9c`.
SHA-256 of frozen C2 counter: `e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471`.
SHA-256 of frozen tool: `d2eb4547b2e285fb80415e81b70c05e47aa6184eadb863e3cd72dab43e6bfd12`.

- **C1-cause-substring**: before `ab2306ac59f8744a51ff0d4bc4d719fc669fce03c7fe4d877872efad90d9ae9c`; mutated `ab0380c7c7a4b552ee0545b8cb855420f632b714c336517bea0ae3654d64f471`; restored `ab2306ac59f8744a51ff0d4bc4d719fc669fce03c7fe4d877872efad90d9ae9c`.
- **C1-cause-casefold**: before `ab2306ac59f8744a51ff0d4bc4d719fc669fce03c7fe4d877872efad90d9ae9c`; mutated `95e69e8fe56e6b6c3003841fce19d767d1f2177f64aa784f6dbed729ca7800bb`; restored `ab2306ac59f8744a51ff0d4bc4d719fc669fce03c7fe4d877872efad90d9ae9c`.
- **C1-stage-prefix**: before `ab2306ac59f8744a51ff0d4bc4d719fc669fce03c7fe4d877872efad90d9ae9c`; mutated `888f43c44314a0a1149659ae253f7c84b222f71e4111a5d62b7570f9a1a8a63a`; restored `ab2306ac59f8744a51ff0d4bc4d719fc669fce03c7fe4d877872efad90d9ae9c`.
- **C2-signal-ge128**: before `e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471`; mutated `6b980fba031c2e38b04423851db60d3cb827fd608a826467d81df0882a240cba`; restored `e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471`.
- **C2-signal-gt128**: before `e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471`; mutated `9336cda071d3cb7b74c35d6674db51e845ba0797463b214bd9e68d0e5c4e42af`; restored `e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471`.
- **C2-exact-low-window**: before `e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471`; mutated `45b995a12bb4d1d172596fe54908de4131c014e89aa40a8d16e062ede14b9518`; restored `e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471`.
- **C2-long-line-search**: before `e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471`; mutated `ef87e4e46f90c5d691d9942a15a29528a35481160711c9e88e5d7c04c5a07b76`; restored `e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471`.
- **C2-negatives-need-samples**: before `e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471`; mutated `bcd2b50dd8ba425a020efe6338062a805f4dd41d40f121cb54800dc7feb9f4e0`; restored `e689438131a633317799377065b84dd54afcb5ba90de1a1dcd67fdf58043f471`.
- **C1-tool-dict-before-pairs**: before `d2eb4547b2e285fb80415e81b70c05e47aa6184eadb863e3cd72dab43e6bfd12`; mutated `048da233f34fbb6561377e26669c3282bddcf9721252613ee65fbc4f141163fe`; restored `d2eb4547b2e285fb80415e81b70c05e47aa6184eadb863e3cd72dab43e6bfd12`.
- **C1-tool-trailing-space-alias**: before `d2eb4547b2e285fb80415e81b70c05e47aa6184eadb863e3cd72dab43e6bfd12`; mutated `7fabc542cbad9c6633a17acb9c6372334e3f6eaf8fcd7a60daf6fb14b4903421`; restored `d2eb4547b2e285fb80415e81b70c05e47aa6184eadb863e3cd72dab43e6bfd12`.

## Scope and evidence quality

No integration or shipping judgment. Full C2 CLI mutation enumeration was not rerun; the bounded detector here is explicitly observation replay, not its CLI wrapper, binding gate or selftest. Unrun checks are not claimed. No installed/updated tools.

Self-evaluation: accuracy 4/5 (bounded semantic replay, not full C2 CLI); completeness 4/5 (all assigned surfaces probed, but a skip-negative mutant requires a meta-test rather than an ordinary added case); clarity 4/5 (counter and tool mutants separated); actionability 5/5 (exact changes, kill cases and hashes); conciseness 4/5 (hash detail retained for restoration audit). Overall 4.2/5. No scope was silently reduced; detection limits are explicit.
