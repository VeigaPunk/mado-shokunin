# CritC2Counter — pre-data read-only review

REVIEW CritC2Counter: confirmed non-behavioral classifier and H-population counterexamples; no canonical C2 score or sealed-H result claimed.

## Scope and axes

Reviewed registration first, then the frozen C2 counter, W catalogue and all three subject interfaces. Axes: **real behavioral-gate validity, green-run robustness, held-out population/provenance, isolation, and honest attribution**. No lane implementation, counter, W file, suite or sealed held-out file was changed or executed. The only lane write is this report. The diagnostic executes only the frozen counter's `benign` and `load_mutants` data helpers, not its main, any suite, subject main or oracle. No other runtime or judge was invoked.

Citation key, relative to the lane:

- **R**: `.ufo/waves/round-27/registration.md`
- **C**: `.ufo/waves/round-27/c2/count.py`
- **W**: `.ufo/waves/round-27/c2/mutants-w.json`
- **S1**: `.ufo/waves/round-26/c1/count-v2.py`
- **S2**: `.ufo/waves/round-26/c2/count.py`
- **Q**: `.ufo/waves/round-26/quality/check-population.py`

Frozen C SHA256: `2e180ed29c31abcb3421d7e57a147d05ac9d2982ebe4dbc555747b287e754dc7`.
W SHA256: `0ad0e46c1a6e61f369c30ab08d6a998f6dce7d16436087b5df57fb8f22323608`.
Subject bytes read from `5ddc5885` matched the inspected working files; their hashes are in the diagnostic receipt.

## 1. Strongest counterexample: normalize the green generator, then SHA-pin

**Evidence:** C:118–124 creates only two green transformations: the exact trailing `# benign edit <8hex>` comment and the exact `_benign_<8hex> = <tag modulo 997>` assignment immediately after the first import. C:177–182 supplies pristine A/B plus those six edits, then W and H. C:193–204 observes only exit status, not whether a subject was exercised.

A classifier removes only those two exact generated shapes and compares each applicable subject's hash with its pristine pin. It accepts the same source identity, not correct behavior. It needs no W strings, hidden data, timing, source execution, network, Git lookup inside the suite, or host side channel: three embedded hashes suffice. It is independent of worker scheduling and seed.

**Concrete diagnostic:** for fresh seeds `ea2ee13a11112617` and `7d9753ff553277c8`, respectively:

| Pure classifier | Greens accepted | W rejected | Subjects executed |
| --- | --- | --- | --- |
| Raw SHA pin | 2/8 | 15/15 | 0 |
| Raw AST pin | 5/8 | 15/15 | 0 |
| Generated-edit-normalized SHA pin | **8/8** | **15/15** | **0** |

The same classifier rejects six synthetic, applicable code-change rows, with `need=5`. Those rows deliberately reuse public W mutations; they are not the actual H population. All 15 W edits were applicable, syntactically valid and distinct as edited subject bytes.

**Bounded conclusion:** [INFERENCE] for any actual H row whose edited bytes differ from pristine after that normalization, rejection is certain. Any six or more such H rows would let this non-gate meet the numeric predicate, even if every genuine H change were novel. Actual sealed H was not read, so this is not an observed `TARGET_MET` receipt.

**Impacted axes:** behavioral validity and premature saturation. Failure of the registered raw SHA/AST controls would not establish that the pinning family was ruled out (R:62–66). This is a construct weakness, not a mismatch between C and its registered exit-status definition.

**Smallest safe correction:** before data, register and officially score this stronger control against sealed H. If it meets, follow R:55–56 rather than interpreting the score as operability. Any redesigned positive population needs independently justified, concealed semantic alternatives that change executable structure, not just recognizable nuisance edits. A fresh seed and additional negative mutants alone do not fix this counterexample. Merely requiring the suite to execute something would also be insufficient if its decision can still be pin-based.

## 2. The W-blocklist control is weakened by its own catalogue

**Evidence:** W:5–6 uses `ok = gn == en` as `new`, but that text already prefixes pristine S1:359. W:82–83 has `new` equal to the empty string, which occurs in every source. The diagnostic found exactly these two `new`-in-pristine collisions.

A literal implementation of R:64–65, “contains any W mutant's new text,” therefore rejects pristine inputs. Its failure is expected independently of gate quality. This is not evidence that contextual source blocklists have been defeated. Recognizing exact changed statements or deletion effects is stronger than raw substring matching; it would still be a non-behavioral W recognizer, with no demonstrated protection against novel H.

**Impacted axes:** control strength and false reassurance.

**Smallest safe correction:** retain an honestly labeled literal control if required by its frozen shape, but add a separately registered contextual mutant-effect recognizer and the normalized pin above. Do not silently change the existing control's shape after scoring.

## 3. “Benign” preserves intended decisions, not all observable behavior

**Evidence:** both counters read their own complete bytes and print their SHA256: S1:284–285 and S2:132–133. Thus both generated edits necessarily alter a provenance field in their normal stdout. Assignment insertion also shifts later source locations and introduces a module binding. The diagnostic confirms byte changes for all six variants, unchanged ASTs for comments, changed ASTs for assignments, and exact recovery after generated-edit normalization.

For the functional decision surface, the insertions are well placed in these particular pristine subjects: S1:41, S2:23 and Q:38 are complete one-line imports. There is no `_benign_` collision or `globals`/`locals`/`vars`/`__dict__`/source-location inspection in the subjects. Q does not read its own source; its read inputs and decision logic are Q:48–50,83–171. I found no functional regression from either edit in Q, or a decision change in S1/S2, from static inspection. Full subject runs were not performed.

**Impacted axes:** equivalence definition and green false positives. A gate comparing entire receipts could fail a purported green because the provenance really changed. Conversely, hash changes are truthful and must not be suppressed to manufacture equivalence.

**Smallest safe correction:** define the observable equivalence projection explicitly: case decisions, error categories and exit status, excluding truthful self-hash fields, added unused bindings and incidental source locations. Under that projection the current edits are reasonable nuisance edits; they are not strong semantic positive controls. Do not claim byte-for-byte receipt preservation for all three subjects.

## 4. H “validity” does not mean a distinct behavioral defect

**Evidence:** C:103–115 checks subject membership, string shape, `old != new`, and one occurrence of `old`. It does not check Python syntax, semantic difference, duplicate IDs, duplicate effects, subject diversity or overlap with W. This conforms to the narrow validity definition in R:41–43 and C:22–25; the weakness is partly the definition itself.

Using the actual frozen loader on synthetic scratch-only rows produced:

```text
SYNTHETIC_H equivalent accepted=6 invalid=0 unchanged_AST=6
SYNTHETIC_H syntax accepted=6 invalid=0 syntax_errors=6
SYNTHETIC_H duplicate accepted=8 invalid=0 distinct_effects=1 need=6
SYNTHETIC_H known_code_changes accepted=6 invalid=0 normalized_rejected=6 need=5
```

The equivalent rows append different comments to Q's `import argparse`; their executable ASTs are identical. The syntax rows cannot parse. The duplicate population has eight IDs but just one edited program. Six applicable rows can also all concern one subject; there is no H quota for the other subjects. None of these observations alleges that the sealed seats actually supplied such rows.

**Impacted axes:** population validity, independence and novelty. A real behavioral gate can be penalized for accepting equivalent programs; a compile-only check can get easy kills on syntactically broken programs; one easy defect can dominate the H fraction and satisfy the six-row floor.

**Smallest safe correction:** before sealing/scoring, independently certify each intended semantic mutant with a behavioral witness, record syntax status, reject equivalences, and deduplicate `(subject, edited-program hash)` across H and against W. Fix the intended subject/defect-class distribution in the registration. If syntax-error mutants are intentionally in scope, label and count them separately rather than presenting them as six independent semantic challenges. Changing this validity meaning requires a pre-data contract revision, not a post-score reinterpretation.

## 5. `h_need` arithmetic is sound; its changing population is the weakness

**Evidence:** C:165–173 prints invalid H rows and drops them; C:202–204 computes `hv = len(H)`, then `ceil(0.75 * hv)`. Neither `hbad` nor the intended sealed cardinality constrains success once six valid rows remain. C:103 silently iterates zero items when a JSON root is not a list, without even adding an invalid record.

The frozen loader diagnostic submitted eight synthetic rows: six applicable and two missing anchors. It returned `accepted=6 invalid=2 need=5`; five kills then clear the H threshold, whereas the intended eight-row population would require six. This models applicability drift, not a claim that a suite is authorized to modify sealed H. With fewer than six valid rows the minimum does correctly prevent success. A malformed non-list JSON returned `accepted=0 invalid=0`, so an additional malformed file can disappear silently beside an otherwise sufficient population.

**Impacted axes:** denominator stability and honest missing-data attribution.

**Smallest safe correction:** prevalidate H against a frozen subject revision; treat later applicability drift or a malformed file as a setup guard, rather than dropping rows and lowering the threshold. Carry the sealed expected cardinality/effect manifest into measurement. Keep the existing ceiling formula for that fixed certified population.

## 6. Sealing and execution isolation are procedural, not enforced here

**Evidence:** C:59–67 makes shared Git clones; C:70–94 changes files and starts ordinary host subprocesses with a cleared environment, timeout and address-space limit. There is no mount/PID/network isolation or concealment of the host filesystem/process tree. `-I` is Python import isolation, not an OS security boundary. The clone retains `.git`, and A receives REV explicitly (C:84–89).

The random `cl-` path and fresh HOME do not directly encode a case label. Provided environment variables are uniform across classes, so I found no direct environment-only green/mutant discriminator. However, the fixed `/fast/.../mado-r27/c2/.../m27c2-.../cl-.../m` ancestry identifies the measurement context, host Git exposes pristine bytes, and the host process tree/held-out path are not hidden by this launcher. These are available channels, not demonstrated reads of peers or sealed files.

There is also a deterministic order channel in the permitted `--jobs 1` configuration: C:177–187 submits all eight greens before every negative row, and per-clone cleanup leaves their common parent until C:189–190. [INFERENCE] a shared ordinal marker could pass the first eight invocations and reject the rest. With the prescribed six workers, start/completion races mean that simple ordinal scheme is not a demonstrated exact classifier. I did not run one. Timing/path tricks are unnecessary for finding 1.

C:168–169 hashes an H file, then `load_mutants` reopens it at C:99. It neither checks a committed manifest nor guarantees the hashed buffer is the loaded buffer. R:48–50 can supply sealing through an external procedure; this code alone cannot establish that provenance. No tampering was attempted or observed.

Finally, C:197 counts every nonzero exit as a kill, including timeout or unrelated setup failure. That follows the predicate, but it is weaker evidence than a witnessed behavioral assertion failure.

**Impacted axes:** isolation, false provenance, result attribution and timing robustness.

**Smallest safe correction:** isolate suites with a private process view and minimal filesystem/network exposure, hide sealed material and unnecessary Git history, shuffle positive/negative scheduling, and eliminate cross-run writable state. Hash and parse one immutable H buffer and compare an independently frozen manifest. Distinguish harness/setup failure from evidence of a behavioral kill in any redesigned contract. These changes close side channels but do not by themselves cure source-identity pinning.

## Exercised evidence and commands

Diagnostic source and verbatim stdout:

- `/fast/scratch/hyaku/mado-r27/crit/CritC2Counter-probe.py`
- `/fast/scratch/hyaku/mado-r27/crit/CritC2Counter-probe.txt`

Executed from the lane:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 60 prlimit --as=4000000000 --core=0 -- python3 -I /fast/scratch/hyaku/mado-r27/crit/CritC2Counter-probe.py
```

Exit 0. The probe extracts only the two named data-helper ASTs, reads subjects using bounded, read-only `git show 5ddc5885:<path>`, evaluates classifiers, and removes its own temporary synthetic fixtures. It never dispatches another agent or invokes the C2 scoring runtime. Its final lines explicitly state `NOT_A_CANONICAL_SCORE` and `exit=0`.

Also exercised:

```sh
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- df -h /fast
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/c2/count.py .ufo/waves/round-27/c2/mutants-w.json .ufo/waves/round-26/c1/count-v2.py .ufo/waves/round-26/c2/count.py .ufo/waves/round-26/quality/check-population.py
env -i PATH=/usr/bin HOME=/home/vgpnk timeout 20 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend
```

`/fast` had 115G available. Coredump command ran before and after; Python counted lines containing `/usr/bin/Hyprland` from captured output. `HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0 own_Hyprland_starts=0`.

No installations, Git/JJ write commands, builds, linters, full-suite tests, host compositor commands or canonical measurements were run. Every subprocess started by the diagnostic completed; no service/process tree was left running. The canonical owner can decide whether to add and score the normalized-pin control before data; this critic has not changed the contract or issued an admission judgment.
