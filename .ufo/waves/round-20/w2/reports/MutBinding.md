# MutBinding — holds: the combined counter and suites kill all six assigned mutants; neither detector group suffices alone

## Scope and axes

Attacked only the binding guard of `28c68378eccbd5f227cdc28a62406ff390e3540a`. This is a mutation-sensitivity result, **not an admission judgment on C1 or round 20**.

Axes: (1) precision and observed/lead fidelity, (2) sensitivity to the six specified regressions without taking credit for baseline failures, (3) host isolation and exact-byte restoration. No production improvement or contract change was attempted.

All execution and mutation happened under `/tmp/mado-r20w2-MutBinding`, cloned from the lane with its origin removed. Clone HEAD was `a4046a8216080d4004de3f268c62cf142095ac07`. The tool blob at that tip was byte-identical to the assigned `28c6837` blob. Only this report was written in the lane; no sibling source, tracked lane source, fleet state, routing, or host configuration was changed.

## Method and commands actually run

Setup:

```sh
git clone -q /home/vgpnk/Projects/shokunin/mado-shokunin /tmp/mado-r20w2-MutBinding && git -C /tmp/mado-r20w2-MutBinding remote remove origin
```

Six separate source copies were made from the committed tool blob, one per mutant under `/tmp/mado-r20w2-MutBinding/mutation-lab/<mutant>/mado-tripwire.py`. Each received exactly one behavior-bearing defect. The unchanged counter reads committed bytes, so each mutant was also placed in an isolated scratch commit containing the changed tool and the `a4046a8` suite tree. These Git objects exist only in the clone. Git HOME and global/system configuration were redirected to scratch or `/dev/null`; there was no push.

The same bounded detector batch was run **six times on pristine bytes, six times on mutated bytes, and six times after restoration**, with independent source files and at most six concurrent detector batches:

```sh
python3 -I /tmp/mado-r20w2-MutBinding/mutation-lab/run-detectors.py pristine
python3 -I /tmp/mado-r20w2-MutBinding/mutation-lab/run-detectors.py mutated
python3 -I /tmp/mado-r20w2-MutBinding/mutation-lab/run-detectors.py restored
```

Runner SHA-256: `9080eb7d0644369d7933bd622c47ef611572871adf16b7da7efcabf282a6d113`.

For every source/phase, the runner executed these real commands (the recorded subprocess executable was `/usr/bin/python3`):

```text
/usr/bin/python3 -I /tmp/mado-r20w2-MutBinding/.ufo/waves/round-20/tw-precision.py REV
/usr/bin/python3 -I /tmp/mado-r20w2-MutBinding/mutation-lab/MUTANT/mado-tripwire.py --selftest SUITE_ABSOLUTE_PATH
/usr/bin/python3 -I /tmp/mado-r20w2-MutBinding/.ufo/waves/round-20/tw-recall-split.py REV
/usr/bin/python3 -I /tmp/mado-r20w2-MutBinding/mutation-lab/MUTANT/mado-tripwire.py --frozen /tmp/mado-r20w2-MutBinding/.ufo/waves/round-19/frozen
```

`REV` was `28c68378eccbd5f227cdc28a62406ff390e3540a` for pristine/restored runs and the individual scratch commit below for mutated runs. `MUTANT` denotes the exact directory names in the results table. `SUITE_ABSOLUTE_PATH` was each of the eleven paths in the suite table. The precision counter's default suite pin remained `f3da50488661509ce5d144c90f7780f8088e0903`; neither it nor the expectations were edited.

Counter SHA-256: `bd3bdc23747a6d8f195e69528f532988202db4ab3476d141a8ff46871e42a8e7`. Recall-split script SHA-256: `5c8f1424833de506f8f839164ff284614ed5080b6015cf615b61b31e30bc7956`. Interpreter: `Python 3.14.8`.

**Baseline handling:** every pristine and restored counter run produced 172/175, not 175/175. The three pre-existing failures were:

- `W-CaseWrapperForms-class-method-instance`
- `L-AdoptW2-AdvHelperFn-b14`
- `H-AdoptW2-RerunPrecision-corpus-jj-var-verb-help`

Those three are inconclusive as mutation detectors and receive **no kill credit**. Every kill below uses a named case that passed on pristine bytes, failed on mutated bytes, and passed again on restored bytes. The counter returns exit 0 for an evaluated suite even when cases fail; I inspected its per-case `pass`, `got`, and `want`, rather than treating counter exit 0 as success.

## Mutants, expected detectors, and observed results

All pristine/restored runs: precision **172/175**; eleven existing suites **247/247**, each suite exit 0. Each mutant retains the same three original precision failures; none converts one into a pass.

| ID / directory | Smallest mutation; original source location | Expected detector | Mutated precision | Newly failing previously passing cases | Mutated existing suites | Combined verdict |
|---|---|---|---:|---:|---:|---|
| B1 `builtin-rebinding` | At `/tmp/mado-r20w2-MutBinding/tools/mado-tripwire.py:1453-1462`, return `pure` for a name in `PURE_ARG_CALLS` **before** consulting its binding; two-line insertion | Shadowed builtin controls, especially `S-CaseShadowing-print-lambda-spawn` and `S-CaseShadowing-run-as-frozenset-control` | 166/175 | 6 | 247/247 | **killed by precision** |
| B2 `delete-unbinding` | At `/tmp/mado-r20w2-MutBinding/tools/mado-tripwire.py:1588-1595`, delete the binding-update loop and leave `if isinstance(stmt, ast.Delete): return` | `S-CaseShadowing-del-run`, `-del-run-cross-cell`, `-del-print-restores-builtin` | 169/175 | 3 | 247/247 | **killed by precision** |
| B3 `cross-cell-carry` | At `/tmp/mado-r20w2-MutBinding/tools/mado-tripwire.py:2052`, replace `binding_envs.setdefault("py", {})` with `{}`; literal carry remains intact | Earlier-cell pure/helper and spawning-wrapper cases | 153/175 | 19 | 247/247 | **killed by precision** |
| B4 `parameter-lead` | At `/tmp/mado-r20w2-MutBinding/tools/mado-tripwire.py:1874-1877`, remove `"parameter"` from the lead-eligible kind tuple | `S-CaseShadowing-param-shadows-helper` and `-param-shadows-spawn-alias` | 170/175 | 2 | 247/247 | **killed by precision** |
| B5 `attribute-leads` | At `/tmp/mado-r20w2-MutBinding/tools/mado-tripwire.py:1876`, change the bare-name guard to `isinstance(node.func, (ast.Name, ast.Attribute))` | Pure-data cases and `L-AdoptW2-CriticC3W2-dc-pytest-param` | 151/175 | 21 | 247/247 | **killed by precision** |
| B6 `class-body-deferral` | In `eager_calls` at `/tmp/mado-r20w2-MutBinding/tools/mado-tripwire.py:1643-1671`, add `visit_ClassDef` that visits bases/decorators/keyword values but not `node.body` | Existing `r19-class-body-deferred-clean`, now correctly expecting an observed finding | 172/175 | 0 | 246/247 | **killed by existing suite** |

### Actual killing output excerpts

The following are projections of the real counter JSON; `O` means `evidence: observed`, `L` means `evidence: lead`. The listed pristine and restored findings equal the unmodified expected findings.

| Mutant / case | Pristine and restored `got` | Mutated `got` |
|---|---|---|
| B1 / `S-CaseShadowing-print-lambda-spawn` | exit 1; `package_query / pacman:-Q / line 1 / O`; `pass:true` | exit 0; `findings:[]`; `pass:false` |
| B2 / `S-CaseShadowing-del-run` | exit 1; `package_query / pacman:-Q / line 1 / L`; `pass:true` | exit 1; same class/rule/line but **O**; `pass:false` |
| B3 / `P-CasePureFormatters-quote-cross-cell` | exit 0; `findings:[]`; `pass:true` | exit 1; `host_mutation / pacman:-S / line 2 / L` plus `host_mutation / sudo / line 2 / L`; `pass:false` |
| B4 / `S-CaseShadowing-param-shadows-helper` | exit 1; `package_query / pacman:-Q / line 1 / L`; `pass:true` | exit 0; `findings:[]`; `pass:false` |
| B5 / `L-AdoptW2-CriticC3W2-dc-pytest-param` | exit 1; only `package_query / pacman:-Qi / line 1 / L`; `pass:true` | exit 1; the wanted lead plus unwanted `host_mutation / pacman:-S / line 1 / L` and `host_mutation / sudo / line 1 / L`; `pass:false` |

The B5 fixture at `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-20/precision/CaseAdoptW2--AdoptW2-CriticC3W2-dc-pytest-param.jsonl:1` supplies the negative attribute control and positive bare-name lead in the same cell. It contains `pytest.param(['sudo','pacman','-S','x'], ...)` followed by an unbound `expect(['pacman','-Qi','walker'], ...)`; the mutant adds the first call's two unwanted leads. Fixture SHA-256: `452e02a55447e44611e9f6c2c82a701ce2decdd57c8bf2d580b7ad246d8452ea`.

B6's actual command was:

```sh
/usr/bin/python3 -I /tmp/mado-r20w2-MutBinding/mutation-lab/class-body-deferral/mado-tripwire.py --selftest /tmp/mado-r20w2-MutBinding/.ufo/waves/round-19/tripwire/r19-bashcvar
```

It returned exit 1. `/tmp/mado-r20w2-MutBinding/mutation-lab/class-body-deferral/mutated/round-19--tripwire--r19-bashcvar.stdout:33,46-47`:

```text
CASE r19-class-body-deferred-clean FAIL want=(1, [('package_query', 'pacman:-Q', 1, '', 'observed')]) got=(0, [])
SELFTEST_SCRIPT_SHA256: 8df8ec008911a51ab1f3d9dde88580d74ab1c3b62edcc335ad0cec66770c9224
SELFTEST_SUMMARY: 44/45 passed failed=['r19-class-body-deferred-clean']
```

Pristine/restored output: `CASE r19-class-body-deferred-clean ok` and `SELFTEST_SUMMARY: 45/45 passed failed=[]`, exit 0. The expectation and its reasoned edit are at `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-19/tripwire/r19-bashcvar/expected.json:412-426`; the actual class-body fixture is `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-19/tripwire/r19-bashcvar/class-body-deferred.jsonl:1`. Thus this particular edit is load-bearing against the assigned class-deferral regression.

B6 mutated suite stdout SHA-256: `6a9fb7216ad9871bb4b805b0207e26bd84af766ee60f7b80c0100ed2ea3378cc`. Its pristine/restored stdout SHA-256: `07fe90a58c5385a56031ef9348407f4fb3c5e745c2d33a0a8c3d984ee13146ef`.

### Complete existing-suite sweep

Each row was run on all six pristine, mutated, and restored source copies. Baseline/restoration pass counts are shown; every mutant has that count except B6's one noted failure.

| Absolute suite path | Pristine/restored | Mutated deviation |
|---|---:|---|
| `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-17/tripwire/core` | 9/9 | none |
| `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-17/tripwire/compound` | 16/16 | none |
| `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-17/tripwire/hardening` | 33/33 | none |
| `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-17/tripwire/w2-regressions` | 30/30 | none |
| `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-18/tripwire/frozen` | 31/31 | none |
| `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-18/tripwire/r18-failsafe` | 1/1 | none |
| `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-19/tripwire/r19-bashcvar` | 45/45 | B6: 44/45, exit 1 |
| `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-19/tripwire/r19-frozen-f1f2` | 13/13 | none |
| `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-19/tripwire/r19-helperfn` | 34/34 | none |
| `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-19/tripwire/r19-installers` | 18/18 | none |
| `/tmp/mado-r20w2-MutBinding/.ufo/waves/round-19/tripwire/r19-vcs` | 17/17 | none |

For **all 18 source/phase runs**, recall-split remained `detected_observed:5`, `detected_lead:1`, `detected_unmarked:0`, `undetected:0`; finding totals were observed 10, lead 1. All 20 control lines remained finding-free. Round-19 frozen replay always returned exit 0 and `MADO_TRIPWIRE_FROZEN: frozen_match`. Those guards alone did not distinguish any of these mutants.

## Restoration and byte evidence

Define `B = 9613f510054043e71463a52b87178ee967dad8132a054159d43603876b85e27c`, the full SHA-256 of the committed `28c6837` tool. Every source was B before mutation and was restored to **exact B bytes** before the final detector batch. Each pristine/mutated/restored batch also checked that its source hash did not change while it ran.

| Mutant | Before | Mutated SHA-256 | Restored | Scratch commit carrying mutated tool |
|---|---|---|---|---|
| `builtin-rebinding` | B | `a4245e1bf9df1ad3bbf2c46a83ec32a7e27088d8f695f14792fa388f0c822fb3` | B | `245f7046bac8c8f577a93bd60c68147bc5e38467` |
| `delete-unbinding` | B | `8e8a9e19df134bd508211c430a4e751a02004aa9c54a2e923aa2a9de612735b0` | B | `b4c4d7bbdf66b0cb0cb58d42e923d63b89b559d3` |
| `cross-cell-carry` | B | `5c76781a4a646f66fcba2c1789b680f9e05586d706a9fffc8adf6d550e9aeaba` | B | `5dad41aee6f42a64709d47d5f1ae01e953ba285f` |
| `parameter-lead` | B | `4cf3acfe36e2bfd007020296e77b49684d7842b1b820a42cffc7b5d2ba08242d` | B | `c6386564459bf5610ae7a98eefecb6d61cd840c8` |
| `attribute-leads` | B | `e9f49f85e66a69910b4da4f264b1b9dfc03dee5f97d1a7fecbaca7b9e216c732` | B | `618ca46e5f089bedde2e431dfc89e1df8926bfdf` |
| `class-body-deferral` | B | `8df8ec008911a51ab1f3d9dde88580d74ab1c3b62edcc335ad0cec66770c9224` | B | `b44f74b303d819101d9161abc964c0187cdba3d7` |

For each mutant, all **14 detector commands' exit codes, stdout bytes, and stderr bytes matched exactly between pristine and restored runs**. This includes the precision counter's three unchanged original failures, not just its numerator.

Counter stdout SHA-256 was `dec728fe803ea32ecffee4bf86c223c79a90f4f85fd5279d036338ad2140ebbe` for every pristine/restored run. Mutated counter stdout hashes:

| Mutant | SHA-256 |
|---|---|
| B1 | `7c7000d4496b8014c7469e5052260f41635b91312025ef2ec0af6998cd4f584a` |
| B2 | `c89dd933c80252fd318d958aa3b486b9632c249031a7a1b4d4be1fa81b2f7910` |
| B3 | `29c2b3f583740d259443184b56786c729069765441882efe72d2b641f131cd10` |
| B4 | `9be4235ad098a3c090b3da1a2a9a5f0ba5e58f10d129762ce0341aca0c348c84` |
| B5 | `4ff257547a376a6fd8dcfd699300fd2b6407372422f6a06d1777b4f93704155f` |
| B6 | `d95725f50a975dba3bb82ce71ca05a6842ba8c7ba76d7be84d88ba4696b4ac49` |

Raw receipts are under `/tmp/mado-r20w2-MutBinding/mutation-lab/<mutant>/<pristine|mutated|restored>/`: `precision.stdout`, the eleven suite stdout/stderr files, `recall-split.stdout`, `frozen-r19.stdout`, and `summary.json` containing each actual argv, rc, and stream hashes. Aggregate receipts:

- `/tmp/mado-r20w2-MutBinding/mutation-lab/pristine-results.json` — `64938e792f8cd41c7c93f35f508d6292e381fd2a59249af93bd3e70e7ae6882b`
- `/tmp/mado-r20w2-MutBinding/mutation-lab/mutated-results.json` — `94457c0a69a33a92ab52510038ca728880e8796bd0d013214acc74a0489ded5e`
- `/tmp/mado-r20w2-MutBinding/mutation-lab/restored-results.json` — `8eb8db0455a7ab7929f6ef2c89f2eaad070591efc57f37c3bc35d72e6d7d6199`
- `/tmp/mado-r20w2-MutBinding/mutation-lab/comparisons.json` — `2e6715d20d5ed76e3d776835e127cfd4bc14fdecf7aa87da61b0ae7e93818219`

Six additional seat-authored **data-only** witness fixtures were scanned, never executed, with pristine, mutated, and restored tools. They independently established that each change actually alters its assigned behavior. Actual argv shape:

```text
/usr/bin/python3 -I TOOL_ABSOLUTE_PATH --scan /tmp/mado-r20w2-MutBinding/mutation-lab/witnesses/MUTANT.jsonl
```

Pristine `TOOL_ABSOLUTE_PATH` was `/tmp/mado-r20w2-MutBinding/tools/mado-tripwire.py`; mutated/restored used the separate tool copies. The output progression was:

| Witness | Pristine → mutated → restored |
|---|---|
| B1 rebound `frozenset = subprocess.run` | observed `pacman:-Q`, exit 1 → clean, exit 0 → same observed row, exit 1 |
| B2 pure `run` followed by `del run` | lead `pacman:-Q`, exit 1 → clean, exit 0 → same lead, exit 1 |
| B3 earlier-cell pure `show` | clean, exit 0 → lead `pacman:-Q` on transcript line 2, exit 1 → clean, exit 0 |
| B4 opaque `run` parameter | lead `pacman:-Q`, exit 1 → clean, exit 0 → same lead, exit 1 |
| B5 only `pytest.param` with argv data | clean, exit 0 → lead `pacman:-Q`, exit 1 → clean, exit 0 |
| B6 `subprocess.run` in a class body | observed `pacman:-Q`, exit 1 → clean, exit 0 → same observed row, exit 1 |

All six witness pristine/restored stdout hashes matched byte-for-byte. Witness receipts are `/tmp/mado-r20w2-MutBinding/mutation-lab/witnesses/before.json` and `/tmp/mado-r20w2-MutBinding/mutation-lab/witnesses/restored.json`. These new probes were **not** substituted for the committed counter or existing suites when assigning the combined kill verdicts.

## Coverage findings

- **Combined detector: killed 6; survived 0; inconclusive 0 for the six assigned defects.** Each kill has a pristine-pass / mutant-fail / restored-pass case. The three unrelated pre-existing precision failures remain inconclusive and unchanged.
- **Precision counter alone: B6 survives.** It remains 172/175 with identical case verdicts even when an eager class-body spawn disappears. The existing class-body case in `r19-bashcvar` supplies the missing sensitivity.
- **Eleven existing suites alone: B1–B5 survive.** All remain 247/247 despite independently demonstrated binding/lead defects. The round-20 precision suite supplies their sensitivity.
- **Recall split and frozen replay alone: all six survive.** Their stable green output is not evidence of binding correctness.
- No contract was weakened, no expected case edited, and no surviving subgroup mutant was treated as permission to change behavior.

## Limits

- Bounded to the six requested one-point mutations and the enumerated detectors. This is not an exhaustive binding analysis, a whole-corpus no-harm diff, a held-out precision rerun, or a round-admission judgment. Those unperformed conclusions are [UNK].
- The aggregate precision baseline is not green at 175/175. Kill claims are deliberately case-level and exclude its three original failures.
- The round-19 `tw-recall.py`, live gate, verifier selftest/regression, and calibration measure were not run; recall-split and the eleven **tripwire** suites were run as stated.
- All fixture command strings were parsed as transcript data. No pacman, sudo, jj, service/compositor operation, host probe, or fixture payload was executed. No other runtime, delegation, web source, or fetch was used.
- The first asynchronous launch was refused by the tool's host-wide background-job cap before execution; it was replaced by a completed foreground launch. No detector run was skipped.
- Raw receipts and scratch Git objects are ephemeral under `/tmp`; this report retains the mutation locations, commit and content hashes, real commands, decisive output excerpts, and restoration result.

## Installs

none
