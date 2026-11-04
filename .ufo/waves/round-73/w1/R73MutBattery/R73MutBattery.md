# R73MutBattery — independent instrument battery

## Scope and method

Axes: frozen-command sensitivity, isolated mutation fidelity, exact-byte restoration. Four C1 and four C2 mutants were run independently; no sibling or committed file was edited. Frozen revision: `1459cca11fb5d3956a6e9a128217852dd0c28cb9`; base: `d3f6c9f5d8b3401c01f189e8cd4b8dbc917a2bce`.

The hard no-git-write rule conflicts with the seat request for plumbing commits. L1 explicitly accepted isolated in-place copies instead. No clone, commits, or git mutations were performed. Each counter was loaded from `git show <frozen>:<instrument>` into its own scratch directory, executed against the read-only original repo, replaced with one mutant, executed again, restored exactly, and executed a third time. All eight triples ran concurrently, with a separate pre-created scratch root per mutant. Explicit absolute `--controls` paths preserve the frozen controls while cwd remains scratch.

**Result: 4 killed, 4 survived, 0 inconclusive in the completed battery.** All 16 pristine/restored detector runs returned rc 0 with their exact frozen contract line. A survivor is a coverage gap, not a change to either contract.

An initial setup attempt omitted creating the scratch-root directories. All its legs returned rc 2 with `--scratch-root is not a directory`, so none counted as a kill. Full initial receipts are retained in [initial-setup-attempt.json](initial-setup-attempt.json). The sole setup repair was creating those directories before repeating the same detector commands.

## Results

| Mutant / named repro | Mutant rc | Verdict | Receipt |
|---|---:|---|---|
| C1-drop-base-killed | 1 | killed | [C1-drop-base-killed.json](C1-drop-base-killed.json) |
| C1-skip-N4 | 1 | killed | [C1-skip-N4.json](C1-skip-N4.json) |
| C1-accept-None / GAP-BAT-1 | 0 | survived | [C1-accept-None.json](C1-accept-None.json) |
| C1-skip-held-hash / GAP-BAT-2 | 0 | survived | [C1-skip-held-hash.json](C1-skip-held-hash.json) |
| C2-drop-global-guard | 1 | killed | [C2-drop-global-guard.json](C2-drop-global-guard.json) |
| C2-drop-environ-guard | 1 | killed | [C2-drop-environ-guard.json](C2-drop-environ-guard.json) |
| C2-relax-copy-keywords / GAP-BAT-3 | 0 | survived | [C2-relax-copy-keywords.json](C2-relax-copy-keywords.json) |
| C2-ignore-base-controls / GAP-BAT-4 | 0 | survived | [C2-ignore-base-controls.json](C2-ignore-base-controls.json) |

## Actual mutant contract lines

### C1-drop-base-killed

```text
MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=4 base_killed=0 verdict=TARGET_MISSED rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9
```

### C1-skip-N4

```text
MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=3 base_killed=1 verdict=TARGET_MISSED rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9
```

### C1-accept-None

```text
MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=4 base_killed=2 verdict=TARGET_MET rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9
```

### C1-skip-held-hash

```text
MADO_R73_MUTANT_KILL: cases=10 mutants=4 killed=4 base_killed=2 verdict=TARGET_MET rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9
```

### C2-drop-global-guard

```text
MADO_R73_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=27/28 base_controls=25/28 verdict=TARGET_MISSED rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9
```

### C2-drop-environ-guard

```text
MADO_R73_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=26/28 base_controls=25/28 verdict=TARGET_MISSED rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9
```

### C2-relax-copy-keywords

```text
MADO_R73_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=28/28 base_controls=25/28 verdict=TARGET_MET rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9
```

### C2-ignore-base-controls

```text
MADO_R73_GUARD_SHAPES: population=20 readers=13 guarded=13 unguarded=0 controls=28/28 base_controls=25/28 verdict=TARGET_MET rev=1459cca11fb5d3956a6e9a128217852dd0c28cb9
```

## Restoration evidence

Each receipt records command argv, full stdout/stderr, rc, expected last line, literal before/after substitution, pristine hash, mutated hash, restored hash, and all three detector outputs. Hashes below are SHA-256; every restored hash equals its pristine hash.

| Mutant | Pristine and restored SHA-256 | Mutated SHA-256 |
|---|---|---|
| C1-drop-base-killed | `9730224579f73b2eab188b73ed78b15003d7499da845c7a8e14f581b42938f14` | `ddfd6ffe1fad8baa8fcc9a9c2b4b8c46364f5376187bd69e5587a0fe439f19ec` |
| C1-skip-N4 | `9730224579f73b2eab188b73ed78b15003d7499da845c7a8e14f581b42938f14` | `e7cbddaf79d1f56060dc77a7ed9c1a629c559feee6d8fa3c71f8f6da33662346` |
| C1-accept-None | `9730224579f73b2eab188b73ed78b15003d7499da845c7a8e14f581b42938f14` | `d9ee3e5f83e5951371c43b5c97caa4a9cd0e62bd611f77d353eb272c0f61a8c7` |
| C1-skip-held-hash | `9730224579f73b2eab188b73ed78b15003d7499da845c7a8e14f581b42938f14` | `227d800067bc035f1ac5e2f84912345ab6aa467b9d5b4478172b96256e769d9c` |
| C2-drop-global-guard | `6be2602839ae15995be14e6327cc9e2221e5af07ae67467cbd7878800555dba7` | `cfa47cf1d1d829af266fac2d51492ecc0c8f52e1ee7bd5e899e0307109419c41` |
| C2-drop-environ-guard | `6be2602839ae15995be14e6327cc9e2221e5af07ae67467cbd7878800555dba7` | `1647212eedee89eea98ecada1329f97653539f3dc5c7b83adf01e0c1837a2170` |
| C2-relax-copy-keywords | `6be2602839ae15995be14e6327cc9e2221e5af07ae67467cbd7878800555dba7` | `6061722e80839fdc99f4b71971221cf0ad746028516b32f37d46e21417f669d9` |
| C2-ignore-base-controls | `6be2602839ae15995be14e6327cc9e2221e5af07ae67467cbd7878800555dba7` | `670ba4199e5c7b3445d666ebadd2fb46820bb0192ff5da91de533d68972208f3` |

## Named survivor reproductions

For each named repro, read its linked JSON receipt. Fetch `git show 1459cca11fb5d3956a6e9a128217852dd0c28cb9:<instrument path>` (C1: `quality/counters/c1-r73-summary-mutants.py`; C2: `quality/counters/c2-r73-shapes.py`) into an isolated copy under the assigned scratch root. Assert the receipt's `old` string occurs once, replace it once with `new`, create the exact `--scratch-root` directory shown in `command`, then execute that receipt's argv with cwd set to the instrument parent. The observed surviving output and rc are above. Restore the original bytes in a finally block. Do not execute the command against production instrument bytes.

### GAP-BAT-1 — C1-accept-None

The frozen measurement never produces a None verdict from the tested rule functions. Broadening score acceptance to None leaves all observed answers unchanged. No claim is made that a None-returning rule was exercised.

Literal mutation (JSON strings):
```json
{
  "old": "        if got == case[\"expected\"]:\n",
  "new": "        if got is None or got == case[\"expected\"]:\n"
}
```

### GAP-BAT-2 — C1-skip-held-hash

The frozen held controls already have the correct digest, so removing their digest rejection is invisible on this positive-only path. No corrupted-control challenge was part of this battery.

Literal mutation (JSON strings):
```json
{
  "old": "    if digest != HELD_CONTROLS_SHA:\n        raise SetupError(\"held controls sha256 %s does not match the frozen digest\" % digest)\n",
  "new": ""
}
```

### GAP-BAT-3 — C2-relax-copy-keywords

The frozen classifier controls do not distinguish accepting dict(os.environ, **keywords) from rejecting it. The actual function is named copies_environ (the assignment called it copied_environ).

Literal mutation (JSON strings):
```json
{
  "old": "and node.func.id == \"dict\" and len(node.args) == 1 and not node.keywords:",
  "new": "and node.func.id == \"dict\" and len(node.args) == 1:"
}
```

### GAP-BAT-4 — C2-ignore-base-controls

The measured held score is already 25/28, so removing that conjunct cannot change the frozen measurement verdict. No wrong-base-score challenge was part of this battery.

Literal mutation (JSON strings):
```json
{
  "old": "and controls == FROZEN_CONTROLS and base_controls == FROZEN_BASE_CONTROLS)",
  "new": "and controls == FROZEN_CONTROLS)"
}
```

## Boundaries and handoff

No tool installations, no host/config/network probes, no fleet or production writes, and no extra runtimes. The requested eight probes are complete; no integration or claim judgment is performed. Scratch contents were deleted only after all receipts were saved in this seat directory. The report is intentionally inside the permitted seat directory, not the contradictory flat trailer path.

## Self-evaluation

Accuracy 4/5: exact recorded outputs and hashes; the four survivor explanations are bounded to this detector. Completeness 4/5: all eight requested mutants and restoration runs completed, with L1-approved copy-based substitution for forbidden commits. Clarity 4/5: full contract lines make this longer than a summary. Actionability 4/5: named repros include literal deltas and commands, but intentionally require reconstructing disposable copies. Conciseness 4/5: detailed receipts are separate; repeated long hashes remain necessary restoration evidence. Overall 4.0/5. Improvement priority: if extending coverage, independently challenge the four survivor branches rather than interpreting positive-path success as branch coverage. Would the user agree? The measured gaps and accepted protocol deviation are explicit.
