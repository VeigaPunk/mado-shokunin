# MutVcs — partly falsified: H kills all five mutations; r19-vcs alone misses all five

## Scope and axes

Assigned leaf mutation probe only, against `28c68378eccbd5f227cdc28a62406ff390e3540a`. Axes: **write recall**, **help/dry-run precision**, **invocation-local filtering before deduplication**, and **isolation / exact restoration**. This is advisory detector-sensitivity evidence, not a round-admission judgment or integration decision.

**Result:** each of the five assigned defects causes at least one previously passing H case to fail, then pass again after exact restoration. The unchanged `r19-vcs` guard passes **17/17 under every mutant**: five survivors on that guard alone. These guard-only survivors are coverage findings, not permission to change the contract.

**Important baseline qualification:** H is already **51/52**, not green. Its pre-existing failure is `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`; it stays identically red in every phase. A raw H-process exit of 1 is therefore **inconclusive as an aggregate kill detector**. The five behavioral kills below rely only on individually green pristine/restored H witnesses that newly fail under mutation. The baseline-red case is neither credited as a kill nor removed from any run.

## Isolation and pinned inputs

The clone was created with the assigned command, and its origin was removed:

```text
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r20w2-MutVcs
git -C /tmp/mado-r20w2-MutVcs remote remove origin
```

Both commands completed successfully with no output. All runnable code, copied fixtures, mutant snapshots, and receipts are under `/tmp/mado-r20w2-MutVcs/mutation-probe/`. The **only lane write is this report**. No tracked lane source, suite, expectation, sibling file, fleet file, or runtime state was modified. No subagent or other agent runtime was invoked.

Read-only `git show` supplied the tool at `28c6837`, the counter and r19 guard at `a4046a8216080d4004de3f268c62cf142095ac07`, and the precision inputs at their registered suite pin `f3da50488661509ce5d144c90f7780f8088e0903`. The tool bytes at `a4046a8` and `28c6837` compared equal.

| Pinned input | SHA-256 |
|---|---|
| Tool, 113,654 bytes | `9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c` |
| Committed `tw-precision.py` | `bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7` |
| Precision `expected.json` at f3da504 | `1039c4fa6ede43b1f08cca231e6c713aa032722e4955f89dbd8b8f3de092254f` |
| Copied r19-vcs `expected.json` at a4046a8 | `8a5e3ffd5b46a2bc62b6e65abdf3b744443cd11f32d18dcf429d1b9c044b0e31` |

The r19-vcs copy contains its manifest plus 15 fixture files. None changed during the experiment.

## Same bounded detectors in all three phases

For **each** of the five isolated tool paths, I ran the H counter slice and r19-vcs selftest first pristine, then mutated, then restored: **30 detector processes total**. Independent copies/detectors ran concurrently. Each top-level process had a 180-second timeout; the unchanged counter/selftest child scans have 120-second timeouts. Every process completed; every captured stderr was empty.

The H adapter `/tmp/mado-r20w2-MutVcs/mutation-probe/detect-h.py:18-35` imports the **unchanged committed counter**, calls `load_suite(f3da504...)` (including its fixture digest/schema checks), selects **all 52 H cases**, and invokes the counter's unchanged `scan_case` comparator on the supplied scratch tool. That comparator requires both the expected scanner exit and the exact multiset of `(class, rule, line, evidence)` (`/tmp/mado-r20w2-MutVcs/.ufo/waves/round-20/tw-precision.py:166-201`). The adapter does not change expectations or drop the baseline-red case. It is a path-based H slice, **not a claim to have run the full 175-case `tw-precision.py REV` CLI**.

Adapter SHA-256: `6c0b205bb62dff1d5881f3f21bd4fbdea3ae79f781bfd008ae957d4cc517e64f`.

Example exact commands, repeated unchanged in all three phases for M2:

```text
/usr/bin/python -I /tmp/mado-r20w2-MutVcs/mutation-probe/detect-h.py /tmp/mado-r20w2-MutVcs/mutation-probe/M2-after-dedup/mado-tripwire.py
/usr/bin/python -I /tmp/mado-r20w2-MutVcs/mutation-probe/M2-after-dedup/mado-tripwire.py --selftest /tmp/mado-r20w2-MutVcs/mutation-probe/r19-vcs
cwd=/tmp/mado-r20w2-MutVcs/mutation-probe/M2-after-dedup
```

The other exact invocations substitute `M1-any-n`, `M3-jj-push-dry`, `M4-ignore-values`, or `M5-drop-help-argv1` for `M2-after-dedup`. All argv/cwd/exit/output digests are recorded in `/tmp/mado-r20w2-MutVcs/mutation-probe/phase-results.json`, SHA-256 `b3e59ec588e22e9e415f255ffed822578b10054414f2449ebba311294e26bd17`.

### Actual aggregate outputs

The H summaries are line 2 of each `{pristine,mutated,restored}-H.stdout`; the selftest summaries are line 19 of each corresponding `*-r19-vcs.stdout` in each mutant directory.

| Independent mutant directory | H pristine | H mutated | H restored | New baseline-green H failures | r19-vcs pristine / mutated / restored | Casewise H / r19 verdict |
|---|---:|---:|---:|---:|---|---|
| `M1-any-n` | 51/52 | 49/52 | 51/52 | 2 | 17/17 · 17/17 · 17/17 | **killed / survived** |
| `M2-after-dedup` | 51/52 | 47/52 | 51/52 | 4 | 17/17 · 17/17 · 17/17 | **killed / survived** |
| `M3-jj-push-dry` | 51/52 | 49/52 | 51/52 | 2 | 17/17 · 17/17 · 17/17 | **killed / survived** |
| `M4-ignore-values` | 51/52 | 46/52 | 51/52 | 5 | 17/17 · 17/17 · 17/17 | **killed / survived** |
| `M5-drop-help-argv1` | 51/52 | 50/52 | 51/52 | 1 | 17/17 · 17/17 · 17/17 | **killed / survived** |

All H adapter process exits were 1, including pristine/restored. All r19-vcs process exits were 0. **Exit alone does not distinguish any H mutant here**; exact case results do.

For example, actual M2 mutated output at `/tmp/mado-r20w2-MutVcs/mutation-probe/M2-after-dedup/mutated-H.stdout:2`:

```text
H_COUNTER_SUMMARY: 47/52 passed failed=['H-HelpBash-jj-help-then-describe', 'H-CaseDryRunBash-add-n-then-add', 'H-CaseDryRunBash-push-dry-run-then-push', 'H-CaseHelpDryRunEval-ctl-dry-then-push-same-cell', 'H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help']
```

And `/tmp/mado-r20w2-MutVcs/mutation-probe/M2-after-dedup/mutated-r19-vcs.stdout:18-19`:

```text
SELFTEST_SCRIPT_SHA256: 67c908c71bec4e819197dd6fcec5496035b39a34a09b53bfe96b2a067f54aaa9
SELFTEST_SUMMARY: 17/17 passed failed=[]
```

## Mutants, expected detectors, and actual behavioral witnesses

Source locations below refer to the original tool at 28c6837, available in `/tmp/mado-r20w2-MutVcs/tools/mado-tripwire.py`. Each mutant starts independently from those bytes; defects are never combined. Exact mutated bytes are preserved as `mutated.snapshot.py` in its own directory even though the exercised `mado-tripwire.py` was restored.

All five witness fixtures are one-line transcript data under `/tmp/mado-r20w2-MutVcs/.ufo/waves/round-20/precision/`. Their embedded commands were **parsed, never executed**.

For brevity, `git:commit`, `jj:describe`, and `jj:git` in the output table mean the complete normalized row `{"class":"vcs_write","rule":RULE,"line":1,"evidence":"observed"}`.

| Mutant | Smallest behavior-bearing change | Expected H detector / embedded command | Actual pristine → mutated → restored output | Verdict |
|---|---|---|---|---|
| M1 | At 640-655, return true for **any parsed `-n` flag**, before command-specific dry-run rules. Value-option parsing remains intact. | `H-CaseDryRunBash-commit-n-no-verify`: `git commit -n -m x` | `(exit 1, [git:commit])` → `(exit 0, [])` → `(exit 1, [git:commit])` | **killed** by a baseline-green witness |
| M2 | Move git/jj help/dry-run filtering from individual classification calls to **after** `(class, rule, evidence)` deduplication at 2060-2075. Optional `exemptions` parameters bypass only these carve-outs during initial collection; the retained representative is then filtered. Original locations: 588-608, 675-685, 1126-1135. | `H-HelpBash-jj-help-then-describe`: `jj describe --help; jj describe -m x` | `(exit 1, [jj:describe])` → `(exit 0, [])` → `(exit 1, [jj:describe])` | **killed**: help representative hides the real write |
| M3 | At 604-611, immediately return no finding for `jj git push --dry-run`, **without requiring `--ignore-working-copy`**. | `H-CaseDryRunBash-jj-push-dry-run-snapshots`: `jj git push --dry-run` | `(exit 1, [jj:git])` → `(exit 0, [])` → `(exit 1, [jj:git])` | **killed**: snapshot finding disappears |
| M4 | At 621, replace `GIT_VALUE_OPTS.get(verb, frozenset())` with `frozenset()`, so separate option values are not consumed. Separator handling remains unchanged. | `H-HelpBash-git-commit-m-h`: `git commit -m -h` | `(exit 1, [git:commit])` → `(exit 0, [])` → `(exit 1, [git:commit])` | **killed**: message value becomes false help |
| M5 | At 650, omit a leading post-subcommand `--help` from flag recognition: `git_option_flags(verb, rest[1:] if rest and rest[0] == "--help" else rest)`. Global and later help recognition are unchanged. This specifically drops the subcommand **argv[1]** rewrite rule. | `H-HelpBash-git-commit-help`: `git commit --help` | `(exit 0, [])` → `(exit 1, [git:commit])` → `(exit 0, [])` | **killed**: help is falsely reported as a write |

Each witness's exact normalized actual/expected rows appear on line 1 of that mutant's phase H stdout and in `/tmp/mado-r20w2-MutVcs/mutation-probe/results-summary.json`, SHA-256 `f7fbb849d7703b939c4ea3a2c10478ec541ea77f6670a2e0202fb49d4b4f76ef`.

### Witness fixture hashes

Every path below is under `/tmp/mado-r20w2-MutVcs/.ufo/waves/round-20/precision/`, line 1:

| File | SHA-256 |
|---|---|
| `CaseDryRunBash--commit-n-no-verify.jsonl` | `db5ad59952d4ee0bf6fa2f9fa374f0b4eff473a793d8b75431e6eed9a9b0e2e5` |
| `CaseHelpBash--HelpBash-jj-help-then-describe.jsonl` | `8a33360947451d414e564db0411bebedbd6df38e716aac8d602847639bf4d319` |
| `CaseDryRunBash--jj-push-dry-run-snapshots.jsonl` | `41410412c1e07d6dd46ee31c52a46aa321aece78d6ec754367a4c3b003942057` |
| `CaseHelpBash--HelpBash-git-commit-m-h.jsonl` | `6906fb33bdc82d5e7cc729f034361560870c35605f04c7c6f3fa26051088559f` |
| `CaseHelpBash--HelpBash-git-commit-help.jsonl` | `a32c63250ea92ad38927ddd926ffeb938d0568003481d14ba6060a95a2111b2c` |

### All newly failing H cases

The existing variable-verb baseline failure is additional to every list below and is not a new failure.

- **M1 (2):** `H-CaseDryRunBash-commit-n-no-verify`; `H-CaseHelpDryRunEval-n-two-meanings`.
- **M2 (4):** `H-HelpBash-jj-help-then-describe`; `H-CaseDryRunBash-add-n-then-add`; `H-CaseDryRunBash-push-dry-run-then-push`; `H-CaseHelpDryRunEval-ctl-dry-then-push-same-cell`.
- **M3 (2):** `H-CaseDryRunBash-jj-push-dry-run-snapshots`; `H-CaseHelpDryRunEval-jj-push-dry-run-snapshot`.
- **M4 (5):** `H-HelpBash-git-commit-m-h`; `H-HelpBash-git-commit-m-help`; `H-CaseDryRunBash-commit-msg-value-dry-run`; `H-CaseHelpDryRunEval-help-flag-vs-value`; `H-CaseHelpDryRunEval-ctl-commit-m-dry-run-value`.
- **M5 (1):** `H-HelpBash-git-commit-help`.

All these case results return to pass with the restored tool. No H passing case changes to a different passing/failing outcome after restoration; pristine/restored H output bytes match exactly for every mutant.

### Baseline-red case, retained and inconclusive

`H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help` expects `(exit 0, [])`, but every pristine, mutated, and restored run returns:

```json
{"exit":1,"findings":[{"class":"vcs_write","evidence":"observed","line":1,"rule":"jj:$c"}]}
```

Evidence: `/tmp/mado-r20w2-MutVcs/mutation-probe/phase-results.json`, each phase's H counter cases. Its registered fixture hash is `047d96a1e5d8578f9a66f784f89c7faf24dbadcb986fb7aae34c842cebb548f2`. This probe does not resolve or alter that expectation. It cannot supply a mutation kill.

## Restoration evidence

Restoration ran in a `finally` block after the mutated detector batch, before restored replay. Every exercised scratch tool compared byte-for-byte equal to the original both immediately after restoration and after restored detectors completed.

**Common before and after SHA-256:**

`9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`

| Mutant | Mutated SHA-256 | Exact bytes restored | Pristine/restored detector stdout identical |
|---|---|---|---|
| M1 | `9bdab6aac7a83c13eacc2764c1474f52e9f6b8f00f29483c14c9d0a30fe9db18` | true | H true; r19-vcs true |
| M2 | `67c908c71bec4e819197dd6fcec5496035b39a34a09b53bfe96b2a067f54aaa9` | true | H true; r19-vcs true |
| M3 | `f9212aae3a577e724c5deba39deefdbc0c35d0400663711d822efc08c4b99f88` | true | H true; r19-vcs true |
| M4 | `069a00d226c28e23f9896c1b9c474edb7d59952f303553dbf52047331302feae` | true | H true; r19-vcs true |
| M5 | `9fed21725a32046fc718bae0b67d2aecc6285f89e4dbb578cb62061fb9beca29` | true | H true; r19-vcs true |

Receipts:

- `/tmp/mado-r20w2-MutVcs/mutation-probe/restoration.json`, SHA-256 `23e3d218ecdafb1b25466a0d649fbe413c93365c1aebaaa013f42097967fb4b3`.
- `/tmp/mado-r20w2-MutVcs/mutation-probe/post-restored-detector.json`, SHA-256 `2745b0887ea89aa26720c46ecf5fec25900094f848e29182b1cd372862b8b1b3`; records five exact tool restorations and unchanged r19 fixture hashes.
- `/tmp/mado-r20w2-MutVcs/mutation-probe/mutations.json`, SHA-256 `0ab303caf9cb9f7f8921677cfbd4b58edb5fd0a1c6a3b117e745a96a512d8de4`.
- `/tmp/mado-r20w2-MutVcs/mutation-probe/inputs.json`, SHA-256 `8272b06e2903d9f8ebd9b8da7e5427807f56cc1e943d4a365469eab7dedf4984`.

## Limits

- Bounded to the five assigned semantic mutations, all 52 registered H cases, and the 17-case r19-vcs suite. No whole-corpus diff, full 175-case precision CLI, held-out suite, recall harness, frozen check, other existing suite, or measurement/tally/isolation harness was run by this seat.
- H's already-red aggregate is explicitly inconclusive as a process-exit-only detector. The positive kill evidence is the green → red → green case behavior, not an already-failing suite exit.
- All five mutants survive **r19-vcs alone**. No mutant survives the individually baseline-green H witnesses. This does not establish exhaustive coverage of all possible help/dry-run defects.
- The optional-parameter/late-filter M2 is one semantic relocation across its necessary callsites, not several combined defects. It moves both git and jj carve-outs; the H witnesses detect both jj help and git dry-run dedup traps.
- Fixture commands, Python cells, and session material were data only. No real jj command, live gate, prohibited package operation, compositor/service/input probe, screenshot, or payload command was executed. No upstream source was fetched, no other runtime was invoked, and no contract/source fix was made.
- Temporary receipts are not committed lane artifacts. This report embeds the mutation definitions, actual outcomes, case names, command forms, and full hashes so the finding is not only a temporary-path assertion.

## Installs

none
