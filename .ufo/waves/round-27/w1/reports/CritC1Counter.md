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

## Follow-up on the L1's request: counters v2 and v3

### v2 (`c1/count-v2.py`, sha256 `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87`, REV `a4dc0da0`): a prefix-keyed reader scored 41/41

Tool: `/fast/scratch/hyaku/mado-r27/crit/CritC1Counter-v2-prefix.py`, SHA-256 `6fb88339190ad63e3549231281d6068ff4f09d31542e8568e62dccd3fe9b05fa`. The tool follows `source =` lines in order, including nested sources and sorted globs. Every variable is bound globally (its last value applies everywhere), except names matching `$wsr[a-z]{4}`, which are bound by position. That exception targets a v2 naming leak. v2 named every redefined (VARREDEF) variable `$wsr` plus 4 letters (`count-v2.py:268`), and every ordinary variable `$ws` plus 3 letters (`count-v2.py:141`).

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -B -I .ufo/waves/round-27/c1/count-v2.py a4dc0da0 --tool-file /fast/scratch/hyaku/mado-r27/crit/CritC1Counter-v2-prefix.py --jobs 3 --seed 173629d63edd35b6
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -B -I .ufo/waves/round-27/c1/count-v2.py a4dc0da0 --tool-file /fast/scratch/hyaku/mado-r27/crit/CritC1Counter-v2-prefix.py --jobs 3 --seed 41ac03e7529ad943
```

Both runs printed `PRED-C1-r27-v2 cases_pass=41/41 verdict=TARGET_MET` and `exit=0` (revision `a4dc0da0394a71badf506e9c72144cd1b8ca7281`). Receipts: `crit/CritC1Counter-v2-prefix-seed1.txt` (sha256 `b967ebd6f70136328a14787cce0f74b7d4f2142f36c13380d1f9f89b31af08d4`) and `-seed2.txt` (`ea27399740087b5f9216b4e27235a7017cba54ec7d033d98c30537c6e3b1e14b`). Both stderr files are empty. The L1 has already retired v2 on this evidence (registration §"C1 redesign before data: counter v3").

### v3 (`c1/count-v3.py`, sha256 `ee4cea19c11a1a8160115f4754e88c11c58aac9a3bff40ccfd16920cd1d691bd`, REV `71d4ea79`): two readers that do not key on names scored 41/41

Neither reader uses variable names, file names, labels or cached answers. Each departs from Hyprland's variable handling in a way v3 never tests.

1. **GlobalOnce, an adapted global-prepass reader:** `crit/CritC1Counter-v3-globalonce.py`, SHA-256 `5fe54d4992578bb69f7ceabe4af166c894e5a80a16bda43e7e811d9ba8c4ca39`. A name defined once is bound everywhere, regardless of position. Only a name defined more than once is bound by position. It substitutes a variable only when a whole comma-separated field equals `$name`, and it reads each file at most once.
2. **FileScope:** `crit/CritC1Counter-v2-filescope.py`, SHA-256 `f56e20a77dc511b10963cf70a69c2971499244ee035d309f224525c1cd553bcb`. It binds variables by position, but a definition made inside a sourced file never reaches the file that sourced it.

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -B -I .ufo/waves/round-27/c1/count-v3.py 71d4ea79 --tool-file /fast/scratch/hyaku/mado-r27/crit/CritC1Counter-v3-globalonce.py --jobs 2 --seed de8aea81933f318e
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -B -I .ufo/waves/round-27/c1/count-v3.py 71d4ea79 --tool-file /fast/scratch/hyaku/mado-r27/crit/CritC1Counter-v3-globalonce.py --jobs 2 --seed 82b835f60a9347f7
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -B -I .ufo/waves/round-27/c1/count-v3.py 71d4ea79 --tool-file /fast/scratch/hyaku/mado-r27/crit/CritC1Counter-v2-filescope.py --jobs 2 --seed 58e7d7aefc10988d
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 900 prlimit --core=0 -- python3 -B -I .ufo/waves/round-27/c1/count-v3.py 71d4ea79 --tool-file /fast/scratch/hyaku/mado-r27/crit/CritC1Counter-v2-filescope.py --jobs 2 --seed 31dd8f7d7f7c0de8
```

All four runs printed `PRED-C1-r27-v3 cases_pass=41/41 verdict=TARGET_MET`, `exit=0` and `HOST_SAFETY ... delta=0`, with no FAIL lines (revision `71d4ea79f5330a63ca3867661211c0bb55daed28`). Snapshot digest: `fe1b2d8b…3727`, 79 files. All stderr files are empty. Receipts (sha256):

| Receipt in `/fast/scratch/hyaku/mado-r27/crit/` | Seed | sha256 |
| --- | --- | --- |
| `CritC1Counter-v3-globalonce-seed1.txt` | `de8aea81933f318e` | `ed8c31296ce7437753bbe402e7c4fdcaec3efbccd880dcee236afa4a6bfa20d2` |
| `CritC1Counter-v3-globalonce-seed2.txt` | `82b835f60a9347f7` | `fd7770d6b1be8329c24d894c7bf60115fb942ec174296161185e5b6e45fdc5e1` |
| `CritC1Counter-v3-filescope-seed1.txt` | `58e7d7aefc10988d` | `295a934ee6ee2136348c3486685d66416a3680d5d5bd4825460cfce6a7b97da7` |
| `CritC1Counter-v3-filescope-seed2.txt` | `31dd8f7d7f7c0de8` | `b54c14a1c649e8d3a07b8946b3eea1357004acf6620bb4252ee3032a6ade1623` |

**Why both pass (v3 code).** All generated definitions go at the top of the appended root block, before every use: `write(root, defs + body)` (`count-v3.py:281`). Each use is a whole field, either the selector or the first rule item (`count-v3.py:142-149`). The VARREDEF block puts its variable only in selector position (`count-v3.py:269-277`). Existing-file lines carry no `$` (`count-v3.py:209`), and decoys carry no variables (`count-v3.py:258`). v3 therefore never puts a definition in a sourced file, never uses a name before its definition, never embeds `$name` inside a value, and never sources a file twice.

Hyprland does each of those things differently (pinned sources fetched to `crit/`; sha256 and bytes listed below). hyprlang keeps one global variable list (`hyprlang v0.6.8 src/config.cpp:518-526`) and sorts it longest name first. While parsing each line, it substitutes variables as substrings, repeating the pass (`config.cpp:733-753`). Each `source =` parses its file again; there is no deduplication (`Hyprland efb50993 src/config/legacy/ConfigManager.cpp:1824-1839`). These are real-config patterns: the operator's own snapshot defines `$activeBorderColor` in a sourced file (`.local/share/omarchy/default/hypr/looknfeel.conf:4`) and redefines it in another (`.config/omarchy/current/theme/hyprland.conf:1`). Those uses are outside workspace rules.

**Witnesses on valid configs:** every case returned `configerrors: [""]`. Runner: `crit/CritC1Counter-v3-witness.py`. Results: `crit/CritC1Counter-v3-witness.json` (sha256 `76c0cb0945048d913b39a73b05791d95ca2610c76091e9557e43401e71ee60f4`) and stdout `crit/CritC1Counter-v3-witness.txt`. The runner exited 0 with host-safety delta 0.

| Witness | Pinned Hyprland | Fails |
| --- | --- | --- |
| `workspace = 3, $gapvar` then `$gapvar = bordersize:4` | `[{"workspaceString":"3","enabled":true}]`: the literal item is ignored | GlobalOnce adds `borderSize: 4` |
| `$monvar = DP-1`, `workspace = 3, monitor:$monvar` | `monitor: "DP-1"` | GlobalOnce prints `monitor: "$monvar"` |
| root sources `twice.conf` (`bordersize:1`), sets `bordersize:3`, sources `twice.conf` again | `borderSize: 1` | GlobalOnce prints `3` |
| `vars.conf` holds `$itemvar = monitor:DP-1`; root sources it, then `workspace = 2, $itemvar` | `monitor: "DP-1"` | FileScope omits the monitor |

An order-blind reader (`crit/CritC1Counter-v2-orderblind.py`, sha256 `b5741c5c…8aa9`) was exercised only on these witnesses, not scored by a counter. It also fails the last one: it runs sourced files after the sourcing file's own lines.

**Not near on v3, per the L1's pilots** (not my runs): binding every variable globally scored 23/41 (`controls/v3/K1PrefixKeyed-L1pilot.txt`; the L1 reports 23-30/41). The source-blind flat scanner scored 2/41. Under v2 and v3, about 75% of cases carry an unsourced decoy (`count-v2.py:253`), so a source-blind reader cannot get near.

**Negative checks from source.** Merging overrides every field that is set; the monitor is overridden only by a non-empty value (`src/config/shared/workspace/WorkspaceRule.cpp:5-48`). The generated 12-key menu covers every settable field that `workspacerules -j` prints (`src/debug/HyprCtl.cpp:522-548`). `layoutopt`, `layout` and `animation` are not printed. I found no hidden merge special case and no missing JSON-visible key.

**Smallest safe correction (v4 generator; same population, oracle and comparator):**

- Sometimes place a definition in a sourced file that runs before its use in the parent.
- Sometimes embed `$name` inside a rule value, such as `monitor:$v` or `gapsin:$v 4`.
- Sometimes use a once-defined name before its definition, in rule-item form. Hyprland keeps the literal and ignores the item; do not use selector form for this.
- Sometimes source one file twice, with a conflicting rule in between.

All four shapes were witnessed valid, with small numbers and no cycles. Every name and file name should stay random.

**Provenance risk:** `/fast/scratch/hyaku/mado-r27/crit/` now holds readers that meet v2 or v3 at 41/41: prefix, globalonce and filescope. Data seats that build `tools/mado-wsrules.py` independently must not read that directory. The L1 may want to copy these readers into `controls/` as K1 controls, as it did with K1FlatScan and K1PrefixKeyed.

**Sources opened for this check** (`curl -fsSL` raw URLs; file name, sha256, bytes): Hyprland `efb50993…` `src/debug/HyprCtl.cpp` `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` 97582 B; `src/config/legacy/ConfigManager.cpp` `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` 90963 B; `src/config/shared/workspace/WorkspaceRule.cpp` `96e1cc448847b03e7f48dc7e1c2bc4ed6c192fcf7c11c608b33f5760f7788f96` 1912 B; `WorkspaceRule.hpp` `924caa92a66b414ad852c793b61fe987c2f1a6286962e6622d495ff98a1227ab` 1944 B; `WorkspaceRuleManager.cpp` `06e8dcbaea83e51710bd372a8f264ad3d07bbe061b9720bbe456811451c02d10` 2672 B; `WorkspaceRuleManager.hpp` `d9ce8271e195d3e8a298fde9591ce449a4c8df0e1563acf775ac9a34c2b3d323` 1174 B; hyprlang `v0.6.8` `src/config.cpp` `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e` 43049 B. Copies are in `crit/` as `CritC1Counter-src-*`.

**Host safety (follow-up):** my own `coredumpctl` captures counted 1338 before and 1338 after, delta 0; every receipt and the witness runner also printed delta 0. Every nested Hyprland ran through the pinned `oracle()`, at most 8 slots at once. Imports ran with `python3 -B` and `sys.dont_write_bytecode`, and `c1/__pycache__` does not exist. No tools were installed and no lane files were edited apart from this report.
