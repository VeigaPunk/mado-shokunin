# CritClaimsPreData — round 27 w2

REVIEW: Literal do-nothing misses both v2 targets; a stronger shortcut actually meets C1 v2. Coverage/operability are defensible surface names, but neither predicate supports an unbounded correctness claim. This is advisory criticism, not a judgment or admission decision.

## Scope and references

Read-only review, except this assigned report. `R27/` below means `.ufo/waves/round-27/` in the lane; `R26/` means `.ufo/waves/round-26/`. `Fleet prompt` means `/home/vgpnk/Projects/shokunin/.ufo/prompts/mado-round-27.md`; `Fleet AXES` means `/home/vgpnk/Projects/shokunin/AXES.md`.

The requested v2 predicates are `R27/registration.md:93-113` and `:127-140`. C1 v2 is **not the current data rule**: registration records its retirement at `:142-150`, then v3's retirement and v4 at `:156-172`. I reviewed v2 as requested and checked the corresponding current-v4 boundaries. No claim that a v2 bypass also passes v4 is made.

No held-out files, held-out receipts, w1 Held* reports, candidate implementations, or private critic scratch were opened. The public sealed-control aggregate was read; its underlying runs were not repeated.

## Direct answers

| Question | Finding |
|---|---|
| Is C1 coverage? | Yes, for the **new lane operation of deriving the workspace-rule table offline from config bytes**, not for discovering the already-known `hyprctl` verb. Registration names that distinction and the unmoved command at `:10-17`. Existing notes already mention the verb (`corpus/knowledge/rule-attribution-r24.md:21,58`; `window-rule-effects-getprop.md:12,31`) but do not supply this derivation. A targeted search of current `tools/` and `corpus/knowledge/` found workspace-rule references in those notes, not a tool implementation. This supports the stated surface; it is not an exhaustive historical absence proof. |
| Is C2 operability, or quality/calibration? | **Operability on the quality trend**, not calibration. Fleet AXES `:13` explicitly includes runnable scripts producing their stated outcome; `:20-22` places operability inside quality. Those are not mutually exclusive labels. The proposed surface is two runnable gates, with behavior beyond their prior versions (`registration.md:30-34,127-135`). Calibration instead concerns self-assessment versus observed state (Fleet AXES `:15`; Fleet prompt `:348-349`); this counter measures green acceptance and mutation rejection, not SCORECARD/SHONEN mismatch. |
| Could literal do-nothing meet either v2 counter? | No in the existing two-seed receipts. C1's `print("[]")` gets **1/41**, not 41/41; C2's missing suites get **green=0/8, W=0/15**, not the target. Details below. This does not establish resistance to every cheap shortcut: C1 v2 has an actual stronger bypass. |
| Are the claims causally separable? | Yes at the registered dependency boundary. C1 extracts only `tools/mado-wsrules.py` and runs it against config in its tool sandbox (`c1/count-v2.py:310-318,356-368`; current v4 `:346-354,392-404`; `harness/oracle.py:231-239`). C2's subjects are the **round-26** animation counter, bind counter, and population checker (`c2/count-v2.py:46-49,94-105`), whose tool paths are `tools/mado-anims.py` and `tools/mado-binds.py` (`R26/c1/count-v2.py:48`; `R26/c2/count.py:31`). C2 does not name the round-27 workspace tool. This is static separability, not an executed ablation or a review of the eventual suites' dependencies. |
| Any unenumerated universal? | The formal finite universals are enumerated. The C2 heading “fail when their subject is broken” is broader than the measured set if read literally. Neither predicate enumerates all legal configs, all future faults, all behavior-preserving edits, or every seed. The qualifiers “sourced,” “broken,” and “behaviour-preserving” also need evidence beyond an exit-code tally. |

## 1. Strongest observed counterexample: C1 v2 saturates on fixture-keyed variable semantics

**Counterexample.** `R27/controls/K1PrefixKeyed.py` follows sources but handles position-sensitive assignment only for names matching `$wsr[a-z]{4}` (`:43-52`); every other variable is a final-value global binding (`:53-60`). This skips ordinary position-sensitive variable semantics. The v2 generator exposes exactly that fixed prefix for redefinition probes (`c1/count-v2.py:265-276`), while ordinary definitions precede rule uses (`:201-203,280`).

**Evidence.** Both committed receipts identify counter SHA `258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87` and tool SHA `6fb88339190ad63e3549231281d6068ff4f09d31542e8568e62dccd3fe9b05fa`:

- `controls/v2/K1PrefixKeyed-seed1.txt:1-4,49-50`: seed `173629d63edd35b6`, **41/41 TARGET_MET, exit=0**.
- `controls/v2/K1PrefixKeyed-seed2.txt:1-4,49-50`: seed `41ac03e7529ad943`, **41/41 TARGET_MET, exit=0**.
- This review's `sha256sum` confirms that the inspected committed shortcut has the same tool SHA as those receipts.

These are observed prior scores, not a new run by this seat. The registration itself records this bypass and retirement at `:144-150`.

**Impacted axes.** C1 coverage evidence, specifically premature saturation of its accuracy instrument. Correct surface naming does not make 41/41 evidence of general variable/source semantics.

**Smallest safe correction.** Do not present C1 v2 as the current rule or its score as current capability evidence. Keep its receipts and retirement explicit. The recorded successor removes the prefix convention; v4 adds additional semantic shapes (`registration.md:148-166`). Whether that documented pre-data retirement satisfies the canonical timing/kill-rule contract is for the canonical judge, not this reviewer. Fleet prompt `:357-360` prevents silently treating different counter versions as one unchanged rule.

This is **not** a literal do-nothing success. Literal C1 do-nothing is exactly `print("[]")` (`controls/K1DoNothing.py:1`). Its v2 receipts both show BASE empty and passing but generated cases failing: `controls/v2/K1DoNothing-seed1.txt:5-8,49-50` and `...seed2.txt:5-8,49-50`, **1/41 TARGET_MISSED, exit=1**. Current v4 receipts also give **1/41**, on seeds `8b1b1caa8415be87` and `bf84153533e19bc2` (`controls/v4/K1DoNothing-seed{1,2}.txt:1-7,49-50`). The generated population, not the host's empty baseline, distinguishes this control.

## 2. C2's simple controls miss for substantive reasons; do not confuse a W-only score with its full target

**Counterexamples tested by existing controls.** Missing suites, accept everything, reject everything, and source-identity shortcuts.

**Evidence.**

- Missing suites: `controls/v2/K2DoNothing-seed{1,2}.txt:5-9,31-32` show **green=0/8, W=0/15, exit=1**. Missing-suite `rc=None` is deliberately not a kill (`c2/count-v2.py:88-89,247-252`). Thus absence cannot satisfy the target by accidentally “failing” every mutant.
- AcceptAll: `controls/v2/K2AcceptAll-seed1.txt:31-32` gives **green=8/8, W=0/15**.
- RejectAll: `controls/v2/K2RejectAll-seed1.txt:31-32` gives **green=0/8, W=15/15**.
- The public sealed re-score aggregate, `controls/v2/L1-sealed-rescore-summary.txt:1-11`, supplies the stronger full-population checks: AcceptAll **17/17 green, 0/15 W, 0/18 H**; RejectAll **0/17 green**; base **0/17 green, 0/15 W**. Normalized pinning gets **8/17 green**, and an exact W blocklist gets **17/17 green, 15/15 W, 0/18 H**. Every listed control is `TARGET_MISSED`.
- Merely repackaging the old suites does not suffice: the same aggregate `:3` records R26Suites **6/17 green, 12/15 W, 14/18 H**, still missing the conjunction.

The W-only receipts have `h_valid=0` and no sealed greens. Their full-target miss alone would be weak evidence against a bypass, because **any** suite misses the minimum H/B requirements without sealed input. Here, missing-suite, AcceptAll, and RejectAll also fail non-held-out conjuncts; the published sealed aggregate separately addresses the stronger controls.

**Impacted axes.** Operability evidence on the quality trend. No full-target C2 cheap-control success is established by the evidence reviewed here. The aggregate is not an independent rerun or proof that no other shortcut exists.

**Smallest safe correction.** Retain the operability label, identify the change as offline gate operability, and report the complete green/W/H conjunction. Do not rebrand this as calibration or workspace-domain coverage. Do not claim that mutation rejection proves the new suites actually exercise subject behavior without reviewing those suites; the data-seat contract separately requires behavioral gates.

## 3. The formal universals are finite; the headings and semantic labels must stay bounded

**Counterexample to an overbroad reading.** A gate can satisfy this finite mutation set while accepting some other broken program. Similarly, 41 correct config trees do not enumerate all Hyprlang programs. These are scope counterexamples, not demonstrated new target-met implementations.

**Evidence and enumeration.**

- C1 v2 builds exactly BASE + 25 APPEND + 15 SYNTH (`c1/count-v2.py:328-333`), compares every case type-strictly (`:356-374`), and requires all constructed cases (`:375-385`). Current v4 preserves that boundary (`:364-369,392-421`). Thus “for each of 40 generated cases” is enumerated, not an all-configurations claim.
- Feature descriptions are population descriptions, not a guarantee that each tree contains every listed shape. For example, `controls/v2/K1DoNothing-seed1.txt:10` names an APPEND case without DECOY, NESTED, or GLOB; those features are conditional in `c1/count-v2.py:220-264`. Do not read `registration.md:96-97` as a universal per-case feature guarantee.
- C2 guards exactly 15 valid W records (`c2/count-v2.py:190-193`), seals the external file set and hashes (`:195-220`), creates every public/sealed green and W/H run (`:226-233`), and requires every green, all W, at least six H, at least two H per subject, at least three sealed benign edits covering all subjects, and `ceil(0.75*h_valid)` kills (`:255-265`). This matches the finite registered conjunction (`registration.md:127-135`).
- The loader's row validity checks are replacement applicability, AST parsing/difference, and byte uniqueness (`c2/count-v2.py:113-142`). They do **not** themselves demonstrate that a mutant is behaviorally broken or a green edit behavior-preserving. No actual mislabeled sealed row is alleged here; the separately assigned held-out review owns those contents.
- There is also a static validation caveat: the documented “must compile” requirement (`registration.md:121-122`; `c2/count-v2.py:16-18`) is implemented with `ast.parse`, not Python compilation (`:128-135`). **[INFERENCE, not exercised here]:** module-level `return` has a parseable AST but is rejected during compilation, so parsing alone is weaker than that literal requirement. This does not establish that the actual sealed set contains such a row.

**Impacted axes.** Evidence quality for C1 coverage and C2 operability; false provenance if the finite results are promoted to “all configs/all broken subjects.” C1's “sourced” qualifier is also not proved by JSON equality: source/provenance review remains separate from the numeric counter.

**Smallest safe correction.** Keep the exact finite predicates unchanged in reporting. Qualify C2's broad heading with the W/sealed-H population; report held-out semantic validity as a separate evidence obligation. Do not claim complete domain coverage, fault completeness, behavior-preserving equivalence detection, or no harm anywhere from these scores. An authorized correction to the compilation guard would need explicit counter-version treatment, not a silent post-score patch.

## 4. C1 still cannot be re-derived from REV and seed alone

**Counterexample.** Keep REV and seed fixed but change the invoking HOME's Hyprland config. The tool bytes remain the same while the input population changes.

**Evidence.** C1 v2 snapshots `os.path.expanduser("~")`, prints only file count/digest, and derives BASE/APPEND from it (`c1/count-v2.py:322-333`). Current v4 retains the same live-HOME dependency (`:358-369`). The harness reads the four live roots and copies eligible files (`harness/oracle.py:34-35,65-90`); temporary inputs are then deleted (`c1/count-v2.py:386-387`; current v4 `:422-423`). Existing control receipts identify a 79-file digest, but that digest is not the bytes needed to replay the input.

**Impacted axes.** Reproducibility/provenance of the coverage measurement, not causal overlap with C2. Fleet prompt `:343-345` asks for a closure command over committed bytes. REV pins the tool, not this external snapshot. This issue was already identified in the w1 registration review and remains in v2/v4.

**Smallest safe correction.** Preserve and identify the exact snapshot bytes plus seed as replay inputs, and make the closure command resolve those pinned inputs. If a counter/input interface change is required, handle it explicitly under the frozen-rule contract. Do not imply that the printed digest or REV alone makes the observed population recoverable. C2 likewise needs the sealed bytes available at closure, not only their pre-data hashes (`registration.md:48-50,137-140`); this review did not inspect those bytes or allege a seal mismatch.

## Review record, exact commands, safety

Used `read`, `grep`, and `glob` for static inspection. Read existing receipts; did not execute counters, controls, suites, tests, builds, formatters, a compositor, or a judgment runtime. No subagents dispatched; no git/jj commands run; no tool installs or upgrades; no process tree remains. Only this report was written.

From the lane directory, ran this bounded read-only safety command twice:

```sh
env -i PATH=/usr/bin timeout 30 prlimit --as=4000000000 --core=0 -- coredumpctl list --no-pager --no-legend /usr/bin/Hyprland | env -i PATH=/usr/bin timeout 30 prlimit --as=4000000000 --core=0 -- wc -l
```

Outputs: before `1338`; after `1338`; observed host Hyprland coredump delta `0`. This seat started no Hyprland instance and inherited no display/session variables into its shell commands.

Also ran:

```sh
env -i PATH=/usr/bin timeout 30 prlimit --as=4000000000 --core=0 -- sha256sum .ufo/waves/round-27/c1/count-v2.py .ufo/waves/round-27/c1/count-v4.py .ufo/waves/round-27/c2/count-v2.py .ufo/waves/round-27/harness/oracle.py .ufo/waves/round-27/controls/K1PrefixKeyed.py
```

Output, in that order:

```text
258118841448530d63cc07804115b3eca5780c23e62a8d6f238779a2a090bf87
635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1
4dfb34b5551a908aa7fd56e75526417b43659018c47fa5993ad39a72b6b109d3
0da5b85570e1325242ff33838d5520328b50cdc72894b3424e7d3d6504c87601
6fb88339190ad63e3549231281d6068ff4f09d31542e8568e62dccd3fe9b05fa
```

No after-state performance claim or acceptance decision is made. All runtime scores above are explicitly attributed to pre-existing receipts.
