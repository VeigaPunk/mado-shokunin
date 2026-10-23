# CritC1Counter — pre-data C1 review

## Finding

**A source-blind shortcut reached `41/41` on two fresh seeds.** Both unchanged-counter runs printed `PRED-C1-r27 cases_pass=41/41 verdict=TARGET_MET` and `exit=0`. The shortcut never follows a `source` directive, reads unsourced files, and resolves variables in a global prepass rather than at their point of use. Three small, valid configurations distinguish it from the pinned Hyprland oracle.

Axes: semantic/discriminative coverage; oracle/input validity; provenance and label isolation; ordered equality; host safety. This is review evidence, not a canonical judgment, admission, integration, or shipping decision. The registration's pre-data rule is at `.ufo/waves/round-27/registration.md:53-66`; its handling belongs to the owner/canonical judge.

## 1. High: file-role structure substitutes for source semantics

### Counterexample and receipts

Throwaway tool: `/fast/scratch/hyaku/mado-r27/crit/CritC1Counter-flat.py`, 3132 bytes, SHA-256 `68339595f2a1ae6c0d41276c78852f81af7fb5ebc7b423f320a4d0f0c7abf1ea`.

The tool was written before choosing either fresh seed; identical tool bytes were used in both runs. It has no seed, case-label, cached-oracle-table, environment, mountinfo, or network lookup. It does implement straightforward per-line fields, boolean words, gap expansion, repeated-selector merging, and the observed on-created-empty prefix. It is **not** a semantics-free `[]` or selector-only control. The skipped semantics are source reachability, source execution order, and temporal variable substitution:

- Tool lines 14-25 enumerate every file in the four roots, including files not sourced. They assign fixed buckets: other files, `hyprland.conf`, then six-lowercase-letter files directly under `.config/hypr`.
- Tool lines 26-31 collect all `$wsxxx` assignments globally; line 43 substitutes the final values everywhere.
- Tool lines 35-64 process only workspace lines; source directives never affect execution.

Exact scored commands (cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`):

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count.py 5ddc5885 --tool-file /fast/scratch/hyaku/mado-r27/crit/CritC1Counter-flat.py --jobs 3 --seed 441b4edd8b45b26d
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -I .ufo/waves/round-27/c1/count.py 5ddc5885 --tool-file /fast/scratch/hyaku/mado-r27/crit/CritC1Counter-flat.py --jobs 3 --seed 37705180291e18c5
```

Verbatim stdout, including every CASE and `exit=`, is preserved at:

| Seed | Receipt under `/fast/scratch/hyaku/mado-r27/crit/` | Result | Receipt SHA-256 |
| --- | --- | --- | --- |
| `441b4edd8b45b26d` | `CritC1Counter-flat-seed1.txt` | 41/41, TARGET_MET, exit=0 | `5b984a21ecdab75716642014b22a6694ba3ef86433a3775e3c4eb0520142352d` |
| `37705180291e18c5` | `CritC1Counter-flat-seed2.txt` | 41/41, TARGET_MET, exit=0 | `25c48d3d0d8b0e36f538050c5b53fd24661edd18fa663f14310b0564bd4168a3` |

Corresponding `.stderr.txt` files are empty. Both receipts identify counter SHA-256 `3d7d301fb9315f9a6cea2427db7c39e556482b30d3f4283373579ae665afd136`, oracle SHA-256 `0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601`, revision `5ddc5885188a1de8606464526d636c9e2fc433e6`, and snapshot digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727` (79 files).

### Why this passes

All code anchors below are in `.ufo/waves/round-27/c1/count.py` unless otherwise stated.

- Lines 66-67 make every generated filename exactly six lowercase letters by default. Lines 205-209 put all new-source rules in one such file and append its source directive **after** root workspace lines. The filename reveals its execution bucket without reading the directive.
- Lines 190-198 choose existing-source rules only from directly sourced files, and exclude direct `$ws` uses. Lines 210-212 append every existing-source rule to **one** selected file. On the observed zero-workspace BASE, all these rules can be placed before root rules without following any source graph.
- Lines 199-204 put every generated definition ahead of generated root workspace lines. Lines 138-155 generate literal assignments and return all definitions before all workspace lines. This does not require a streaming variable evaluator.
- Lines 183-213 do not generate unsourced workspace-rule decoys, nested generated source chains, or a new source interleaved before conflicting root rules.
- Lines 214-219 enforce only the presence of a feature label from `TRAPS`, not a witness that a source-blind/global-variable reader disagrees with the oracle.

Thus `NEWSRC`, `SOURCED`, and `VARIABLE` labels overstate what is distinguished: the tables really match, but this generator lets filesystem membership and filename shape stand in for source semantics. Shuffling tool invocations at lines 287-288 does not randomize execution structure within a configuration.

### Valid distinguishing configurations, exercised

All three were run through the pinned `oracle()` and the unchanged `run_tool()` sandbox. Each returned `configerrors: [""]`; the shortcut failed all three. Reproducer fixtures are at `/fast/scratch/hyaku/mado-r27/crit/CritC1Counter-witness.py:14-25`; complete answers are in `CritC1Counter-witness.json` and verbatim stdout in `CritC1Counter-witness.txt` in that directory.

1. **Unreachable file:** root contains `workspace = 1, bordersize:2`; unsourced `.config/hypr/unread.conf` contains `workspace = 9, bordersize:5`. Oracle returns only selector `1`; shortcut also returns `9`.
2. **Actual source order:** root contains `source = ~/.config/hypr/aaaaaa.conf` followed by `workspace = 1, bordersize:2`; `aaaaaa.conf` contains `workspace = 1, bordersize:4`. Oracle's final border size is `2`; shortcut's is `4`.
3. **Temporal variable binding:** root is:

   ```text
   $wsabc = 1
   workspace = $wsabc, shadow:true
   $wsabc = 2
   workspace = $wsabc, bordersize:3
   ```

   Oracle returns selectors `1` (shadow true), then `2` (border size 3). Shortcut returns only selector `2`, with both fields.

Witness command, same cwd:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 180 prlimit --as=4000000000:8000000000 --core=0 -- python3 -I /fast/scratch/hyaku/mado-r27/crit/CritC1Counter-witness.py
```

Process exit was 0; `flat_passes` was false for every witness. The parent has a 4 GB soft limit with an 8 GB hard ceiling so the existing oracle can apply its own 8 GB limit.

### Smallest safe correction

Change the **counter's discriminating inputs**, not the intended workspace-table operation. Within the existing 15 SYNTH seats, reserve paired cases with the same files but different source reachability, and paired cases with a conflicting source before versus after the root rule. Randomize filenames independently of their execution roles; include workspace-bearing unsourced files. Include an interleaved variable redefinition witness. These remove the observed substitute authority (file membership/name buckets and final global assignment values) while retaining 41 cases and the existing oracle. Merely changing the six-letter filename length is not a semantic repair.

This is a fixable coverage defect. Exact correctness on the frozen finite generator is genuinely observed; it must not be represented as evidence that this shortcut implements source or temporal-variable semantics. No counter, harness, registration, or production tool was edited.

## 2. Medium: JSON boolean/number mismatches pass equality

`count.py:299-302` checks only the outer list type and then uses native Python `got == exp`. `harness/oracle.py:243-244` parses tool JSON with ordinary `json.loads`. Python therefore equates `true` with `1` and `false` with `0` recursively inside these objects.

Concrete oracle-backed example from witness 1:

```json
{"oracle":[{"workspaceString":"1","enabled":true,"borderSize":2}],"accepted_by_native_comparator":[{"workspaceString":"1","enabled":1,"borderSize":2}]}
```

The witness output records native equality true and serialized-JSON identity false. On all 41 real tables collected with seed `0123456789abcdef`, replacing every boolean with its integer value preserves native comparison equality in **41/41**, while changing serialized JSON in all **40 nonempty** tables. This is a direct comparator probe, **not another scored counter run or a claimed independent semantics-free implementation**. Summary: `/fast/scratch/hyaku/mado-r27/crit/CritC1Counter-summary.json`.

Impacted axis: fidelity of the advertised exact JSON values (`count.py:13-14`). Smallest correction: type-aware recursive JSON equality, at least distinguishing booleans from numbers, preserving array order and exact object membership. This is independent of the source-generation correction.

## 3. Negative findings and limits

- **BASE really is trivial:** all exercised runs returned `BASE=[]`. For the full oracle-inspection seed `0123456789abcdef`, it was the **only** empty table; generated tables had 1-5 entries. Both attack receipts also show nonempty tables for all 40 generated cases. An always-empty or static-empty answer is therefore not near saturation on these samples.
- **No rejection-collapse evidence:** querying `configerrors` alongside `workspacerules` for BASE plus all 40 cases of seed `0123456789abcdef` returned `[""]` throughout. The small distinguishing witnesses were also error-free. I did not find a generator bug making those tables empty through rejected workspace lines.
- **No direct case-label leak found in inspected paths:** `count.py:259-267` uses independent temporary home names; `287-288` shuffles tool runs; `harness/oracle.py:234-239` binds a case to fixed `/snap/home`, clears environment, and unshares namespaces. The demonstrated leak is generated file-role structure, not access to CASE labels or oracle answers.
- Generated `layoutopt` values (`count.py:117-118`) do not appear in the inspected oracle JSON. Ignoring them is not itself a false pass for the claimed table operation; the claim is not a complete layout-behavior evaluator.
- Results establish this shortcut on the two reported fresh seeds and the recorded snapshot, not every possible seed or future host configuration. No Rust judgment or other orchestration runtime was invoked.

## Inspection command and safety

Additional oracle-inspection command, same cwd:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 600 prlimit --as=4000000000:8000000000 --core=0 -- python3 -I /fast/scratch/hyaku/mado-r27/crit/CritC1Counter-probe.py --seed 0123456789abcdef --jobs 3
```

It imports the frozen generator without editing it, builds its exact 41 trees, and requests `workspacerules` plus `configerrors` only through the pinned oracle. Output data: `/fast/scratch/hyaku/mado-r27/crit/CritC1Counter-oracle-0123456789abcdef.json`, 7,840,245 bytes, SHA-256 `cf57309af15205544e3ffbfbe8cedf9d91547c10ae43344522f1442ca81d2659`. It includes copied BASE-file text as well as generated deltas and oracle tables; no such text is imported or executed by the shortcut.

Before writes, `env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- df -h /fast` reported 115 GB available. No tools were installed or updated. Each manually launched process used a cleared environment, timeout, and core limit. The oracle-inspection run used 3 concurrent instances; the two simultaneous scored runs used 3 each; the shared oracle slot limit remained in force. Counter runs use the harness's own limits. Every nested Hyprland was started by the pinned oracle, which cleans its process group in `finally` (`harness/oracle.py:214-228`); all launched commands returned, and temporary case/work trees were removed by the runners/counters. No live compositor queries or write operations were used.

Own direct `coredumpctl list --no-pager --no-legend` captures, launched under `timeout 20 prlimit --as=4000000000 --core=0` with a cleared environment, counted **1338 before, 1338 after, delta 0** (both exit 0). Both scored receipts, the full oracle probe, and the three-witness runner independently printed the same zero-delta host-safety result. The import inspection briefly created `.ufo/waves/round-27/c1/__pycache__/count.cpython-314.pyc`; I removed that generated file and its empty directory with `rm -- <file>` and `rmdir -- <directory>`, each under `env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 --`. The report is the only remaining lane write; experimental tools and evidence are under the authorized scratch directory. For future probe/witness reproduction, add Python's `-B` flag to avoid recreating import bytecode. No tracked lane source was edited.
