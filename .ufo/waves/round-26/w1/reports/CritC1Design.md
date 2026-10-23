# CritC1Design — pre-data C1 falsification

## Verdict

C1 design: flawed (oracle version identity is not enforced, the append-only population leaves a cache-plus-delta shortcut untested, and the claimed table-changing guarantee is false).

The coverage axis is defensible, the named-field comparison matches the registered predicate apart from oracle identity enforcement, and the scored population really is 41. No cheap control meeting 41/41 is demonstrated here. The kill rule has not been shown to fire. This is a scoped design critique, not an admission judgment or a counter receipt.

## Review boundary and input identity

Read `registration.md` first, then all of `c1/count.py`, the relevant harness, the held animation claims, the fleet axis rule, and located source fragments already opened by source seats. All round paths below are relative to `.ufo/waves/round-26/` unless prefixed with `tools/` or `corpus/`.

Only this report was written. No product, counter, harness, control, registration, ledger, or source artifact was changed. No compositor, oracle, counter, test suite, alternative judging runtime, or subagent was started. Existing control receipts below were read, not re-executed. No tools were installed or updated; no process tree was left running.

Exact shell command executed, with cwd `/home/vgpnk/Projects/shokunin`:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 20 prlimit --as=4000000000 -- sha256sum mado-shokunin/.ufo/waves/round-26/registration.md mado-shokunin/.ufo/waves/round-26/c1/count.py mado-shokunin/.ufo/waves/round-26/harness/oracle.py
```

Output:

```text
56608ea38ecf4195217431c9eb481b39cfcf9c413255552e00e68206d93f873a  mado-shokunin/.ufo/waves/round-26/registration.md
f98e264b272f47bb93a72538294ea8a0805d724847baf0879f741e2f43d352cd  mado-shokunin/.ufo/waves/round-26/c1/count.py
680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441  mado-shokunin/.ufo/waves/round-26/harness/oracle.py
```

## A. Axis fit — the strongest held-rule objection does not establish a defect

**Counterexample attempted:** animations have already been covered, so testing 40 new trees merely re-scores an existing rule.

**Evidence:**

- `corpus/knowledge/hyprctl-verification-layer.md:158` holds counts, including 35 nodes and 6 beziers, but explicitly leaves directive-to-entry expansion `[INF]`.
- `corpus/knowledge/hyprland-config-plane.md:118-126` inventories the effective declarations; it does not give a config-to-JSON resolver.
- A case-insensitive `animation|bezier` search over current `tools/` found only `tools/mado-verify.sh`'s animation-enable check. Its actual operation at `tools/mado-verify.sh:3488-3494` is `getoption animations:enabled`, not reconstruction of the animation table.
- `registration.md:33-39` names a new operation, `python3 -I tools/mado-anims.py --home DIR`, and a base-counter result that would show it unmoved. The base command follows from `registration.md:81-84`: `python3 -I .ufo/waves/round-26/c1/count.py 96101be5`.
- The fleet rule permits a new tool, operation or edge class as a coverage move: `/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-26.md:361-365`; `AXES.md:12-13` distinguishes coverage from merely having runnable artifacts.

**Assessment:** the newly governed operation is static reconstruction of Hyprland's reported node/bezier sets, not the already held count agreement. Calling the implementation a script does not by itself force an operability label. Coverage remains defensible if that operation actually lands and is routed as the surface named here. A new pathname alone would not establish it.

**Impacted axes:** coverage; calibration if the finite result is advertised as broader animation understanding.

**Smallest safe correction:** keep the coverage claim about this operation. Do not promote the old count observation into proof of a general resolver or claim that all animation/config edge classes are covered.

## B. Cheap shapes — a stronger skipped-work control remains open

### Observed negative evidence, not a 41/41 defeat

`controls/K1SnapshotCache.txt:51-100` records a snapshot-only control against the frozen counter and revision `05319e0fed2ce25cf0a883380af2763a85fd4936`, seed `1b418d312d807328`. Its producer header names the same frozen counter and oracle hashes. Relevant verbatim lines:

```text
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (unperturbed)
CASE C35   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 (SOURCED+UNSOURCED)
PRED-C1-r26 cases_pass=2/41 verdict=TARGET_MISSED
exit=1
```

Locations are `:57`, `:93`, `:99-100`. Its first recorded seed scores 1/41 (`:2-4,49-50`). The static-default receipts likewise score 0/41 twice (`controls/K1StaticDefault.txt:48-49,97-98`). These reject those particular shapes; they do not reject compositions of caching and partial reading.

### Strongest additional shape: cached original events plus suffix-only parsing

**Counterexample:** embed the original configuration's animation/bezier events and source schedule, then parse only the appended suffixes and newly created files. Replay cached original events at their original include positions, so a later original declaration can still overwrite an early appended declaration. Handle only the generator's small new-line vocabulary; never interpret arbitrary original configuration bytes.

**Evidence:**

- Every case starts with the same snapshot (`c1/count.py:233-245`).
- Every mutation uses append mode (`c1/count.py:113-116,123-180`). No operation deletes or edits an original directive, removes a source edge, or replaces the root with an independent synthetic tree.
- New sourced paths have one fixed form, `~/.config/hypr/<six letters>.conf` (`c1/count.py:130-137`). New variable assignments use two fresh-looking name patterns and literal values (`:146-150`).
- The C1 verdict checks the output sets, not absence of embedded baseline events (`c1/count.py:218-278`). This is not an accusation of an omitted C2 embed requirement: C1 has no such registered requirement.
- There is a local precedent for this threat. The earlier `round-25/controls/CtlCacheDelta.md:7-11,78-103` describes a cached table plus uncached-line parser scoring 25/33. That old result is not an r26 result. Its documented killers included synthetic replacement trees, absent from this C1 population, and unsourced files, which a stronger suffix reader can distinguish.

**[INFERENCE]** This composition is a plausible 41/41 candidate because it need only implement the finite append-mutation algebra, not reconstruct the original tree from its current bytes. It was not built or scored by this critic, so claiming that it meets 41/41 would be unsupported. The listed snapshot-only and no-validation shapes do not settle it.

**Important non-defect:** a reader that skips runtime inheritance is not automatically cheating this predicate. The pinned writer emits `internalBezier`, `internalEnabled`, `internalSpeed`, and `internalStyle`, not an independently requested rendering-effective table (`fetch/SrcHyprctlAnims.bin:948-959`). Matching those reported fields is precisely what was registered. Require a true skipped-work witness, such as never interpreting the original directives, rather than rejecting an implementation merely for omitting unnecessary inheritance machinery.

**Impacted axes:** coverage evidence and calibration. A finite cached mutation recognizer must not stand in for the broader from-config-bytes capability.

**Smallest safe correction:** score the cache-plus-suffix/event control before data. If it meets the target, apply `registration.md:75-83`: preserve receipts, append the disposition, and redesign/re-register or declare exploratory. A replacement population should include baseline-changing/deletion and independent-tree cases. Do not silently edit this frozen counter, drop cases, or lower 41/41. Until tested, this is an unresolved falsification candidate, not a kill receipt.

## C. Predicate sentence, condition, receipt label

**What matches:**

- `registration.md:41-47` and `c1/count.py:5-11` state the same predicate after normalizing line wrapping/whitespace, including the command, named fields, 40 generated cases and target 41/41.
- The field tuples are exactly the registered six node fields and five bezier fields (`c1/count.py:35-36,185-195`). Successful cases require equality of both sets (`:266-278`). Ordering and duplicate multiplicity are deliberately ignored; the docstring declares that at `:13-15`. Extra object keys are outside the named-field predicate.
- The emitted label is exactly `PRED-C1-r26` (`c1/count.py:287`), and exit status follows the target (`:286-295`). The receipt does not repeat the whole sentence. The fleet asks for the same condition and receipt label, not for literal sentence repetition (`mado-round-26.md:357-360`), so this formatting is not a substantive mismatch.
- Generator helpers constrain mutations, but expected animation data comes from `O.oracle` (`c1/count.py:247-256`), not from a second lane animation model. Do not misclassify `sourced_files()` as an expected-value authority.

### Fixable defect: the promised oracle version is not guarded

**Counterexample:** keep the pinned harness bytes and tinywl/libwlroots binaries, but change the installed Hyprland version. The build guard still passes; a tool matching that other version can receive a receipt labelled with the predicate that promises v0.56.2.

**Evidence:** `O.check_build()` is the only pre-measure build check (`c1/count.py:205-208`). `harness/oracle.py:48-57` checks only tinywl, libwlroots and existence of the render node. The compositor is the ambient `Hyprland` executable under `/usr/bin` (`harness/oracle.py:148-160`), and IPC uses ambient `hyprctl` (`:128-131`). Neither a Hyprland commit/version check nor its executable/library identity is bound by that guard or the receipt. Hashing `oracle.py` does not hash its ambient dependencies.

This is an enforcement/reproducibility defect, not evidence that the currently installed version is wrong. No host package was changed or compositor started to demonstrate it.

**Impacted axes:** calibration/provenance and freshness; it weakens coverage evidence by leaving the promised oracle identity unverified.

**Smallest safe correction:** guard the actual compositor identity against the promised version/commit and bind the parser dependency identities relevant to the result; print them in receipts. A mismatch must exit 2, not produce a measured target result. Because harness bytes are frozen and pinned, publish this as an explicit successor/re-registration with retained old receipts, not an unnoticed in-place fix.

## D. Population — correct, and not 42

`NCASES = 40` (`c1/count.py:34`). `built` contains one BASE plus one entry per iteration (`:236-245`), exactly 41. `BASE#2` is an additional oracle guard only (`:248-256`), not a second scored BASE. The tool loop and printed CASE loop both range over `built` (`:258-283`), and the target denominator is `len(built)` (`:286-287`). The four roots are one snapshot input, not four separately scored cases (`harness/oracle.py:34-35,65-88`).

Thus the registered 1 + 40 population equals the counter's scored population. No population repair is warranted for C1. This establishes cardinality, not 40 distinct semantic changes or exhaustive edge coverage.

## E. Generator blind spots and one already witnessed false guarantee

### E1. An EFFECTIVE label does not guarantee a table change

`registration.md:117-119` says every C1 case carries at least one table-changing operation. In code the guarantee is only membership in the hand-written `EFFECTIVE` set (`c1/count.py:45,240-244`). There is no check that a generated oracle table differs from BASE (`:254-278`).

The unchanged C35 in the existing snapshot-only receipt above is a concrete witness: `SOURCED+UNSOURCED` includes an EFFECTIVE operation, yet replaying the base table passes. Source-level examples also permit no effect: `DISABLE` can select an already disabled node (`c1/count.py:159-160`); generated speeds can round to zero (`:88-91,104-109`), while the opened handler rejects nonpositive enabled-animation speed before applying the node (`fetch/SrcAnimConfig-legacy-impl.bin:1451-1469`). These explain possible causes; the C35 receipt does not preserve its generated line, so its exact cause is unknown.

**Impacted axes:** calibration; strength of coverage evidence. This does not change the denominator or demonstrate that a static table can meet all 41.

**Smallest safe correction:** append an honest correction to the all-changing assertion now. If a successor counter needs that guarantee, establish semantic inequality from oracle output or use a guaranteed novel valid table entry; do not equate an operation name with an observed change.

### E2. Fixed substrate and source topology

All mutations are additive. No original animation/bezier removal, root replacement, source deletion/reordering, source replacement, or new empty/default substrate is generated (`c1/count.py:113-180,233-245`). `ORDER` appends two directives; it does not reorder source edges (`:172-176`). The helper deduplicates files and recognizes only a literal `source =` regex with tilde/glob handling (`:67-85`); new sources use a single literal path (`:130-134`).

**Concrete ungenerated contrast:** `source = a.conf`, a conflicting middle animation directive, then `source = a.conf` again requires occurrence-sensitive replay. The opened handler calls `parseFile()` for each source occurrence (`fetch/SrcAnimConfig-legacy-impl.bin:1824-1840`); the generator's global `seen` list cannot exercise creation of that topology (`c1/count.py:72-79`). This is a generator blind spot, not a claim that the generator supplies wrong expected values.

### E3. Variable/grammar depth is narrow

`VARIABLE` creates literal speed/bezier variables immediately followed by one use at root EOF (`c1/count.py:146-150`). It never deliberately generates reassignment, a pre-existing-name collision, variable source paths, expression-valued animation fields, or escaped/comment-sensitive names. `CATEGORY` produces one fixed balanced block (`:155-158`); `SPACING` produces two fixed layouts (`:177-180`). These cannot support a claim of general hyprlang grammar coverage.

### E4. Random mixtures are not stratified edge-class coverage

The 40 cases sample operation names rather than guaranteeing each operation or each INVALID alternative (`c1/count.py:161-170,237-244`). There is no per-node/per-style/per-error coverage condition. In particular, the line labelled invalid with on/off `2` is not necessarily rejected: the opened handler compares the parsed integer to 1 before its range check, then takes the disabled-node update path (`fetch/SrcAnimConfig-legacy-impl.bin:1437-1446`). Style error reporting likewise follows a node update (`:1469-1475`). The independent oracle handles these facts correctly; names like INVALID do not prove rejection semantics were exercised.

**Impacted axes for E2-E4:** coverage generality and calibration, not the arithmetic of the registered 41-case score.

**Smallest safe correction:** keep the present score explicitly scoped to its snapshot and generated distribution. For any stronger successor, freeze independent-tree/destructive and occurrence-sensitive cases, plus stratified grammar/error witnesses, before data. Do not retroactively count a finite random pass as saturation or silently change this predicate after its receipts exist.

## Disposition

The decisive concrete counterexample is the already recorded unchanged C35, which falsifies the all-changing explanation without falsifying the 41-case comparator. The most important untested cheap shape is cached original events plus suffix-only parsing. The oracle identity guard is a separate fixable defect. Coverage classification and population equality survive this review. None of these findings authorizes counter edits, admission, or a claim that an unrun shortcut met the target.
