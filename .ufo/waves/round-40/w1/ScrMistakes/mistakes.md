# Round-40 `## Mistakes` — draft (seat ScrMistakes)

Scope: a draft of the `## Mistakes` section for `corpus/lessons/round-40.md` plus a candidate
QUALITY.md criterion 65. Rows are class / evidence pointer / captured-by / fix, in the shape of
`corpus/lessons/round-39.md#mistakes`. Everything below was measured by this seat over committed
bytes, the committed native capture, or a scratch copy in `/tmp` (paths and commands in §Evidence).
Nothing outside `.ufo/waves/round-40/w1/ScrMistakes/` was written; no compositor verb was run.

Inputs read: `.ufo/waves/round-40/registration.md` (freeze `5e7e885`),
`corpus/lessons/round-39.md`, `corpus/lessons/round-39-verifier-spotcheck.md`,
`quality/counters/c1-r40-live.py`, `.ufo/waves/round-40/ctl/run-c1-controls.py`,
`.ufo/waves/round-40/c1/ctl-ref-tool.py.txt`, `.ufo/waves/round-40/receipts/ctl-c1.txt`,
`.ufo/waves/round-40/c1/native-capture.jsonl`, `.ufo/waves/round-40/w1/ExecLiveCensus.md`,
`corpus/QUALITY.md` (criteria 61–64).

---

## Mistakes

**M40-1 — the C1 generator drew each value type from a broad table, so two conversion mutants survived the controls.**
Class: under-sampled fixture — a mutation survives because the generator never guarantees the
spelling the mutant gets wrong.
Evidence: the spelling tables and the quirk-first plan are `quality/counters/c1-r40-live.py:224-235`
(`COLOUR_SPELL`, `RGB_SPELL`, `BOOL_SPELL` — `"yes, please :)"` is one of ten entries — `WSPELL`),
`:260-301` (`make(..., quirk)`: `:265` `d = "yes, please :)" if quirk else rng.choice(BOOL_SPELL)`,
`:297` `n = 3 if quirk else rng.randint(1, 4)`, `:301` `d = "ultraheavy" if quirk else
rng.choice(WSPELL)`) and `:342` `plan = [(k, True, "agree") for k in kinds]`. Two re-derivations run
by this seat (§Evidence E1), each a copy of the frozen counter with the per-tree guarantee removed:
- V1, only the plan line changed to `quirk=False` (tables intact): the eight trees cover
  `garbage-bool=0/8`, `3-value-gap=4/8`, `ultraheavy=1/8`; `M03-bool-exact` scores
  `fixtures=13/13` — it **survives the whole suite** — and `M05-gap-three-values-wrong` scores
  `fixtures=6/13`, i.e. it is caught only by the four trees that happened to draw a 3-value gap.
- V2, the plan plus the bool table and the gap arity: coverage `0/8`, `0/8`, `2/8`; both `M03` and
  `M05` score `fixtures=13/13` — both survive.
Under the frozen generator the same two mutant files score `fixtures=0/13` each
(`receipts/ctl-c1.txt:5,:7`), and the kill is total rather than partial because every tree carries
the class (§Evidence E2: `garbage-bool=8/8`, `3-value-gap=8/8`, `ultraheavy=8/8`).
The *before* state is not committed: `receipts/ctl-c1.txt` holds 18 `control=` lines in their final
state only, and the L1 states (this task) that the first generator draft left M03 and M05
surviving. E1 is therefore the only re-derivable witness of that survival; V1/V2 are
reconstructions of "the guarantee absent", not the first draft's bytes.
Captured-by: none at the first draft — no control was authored against the spelling class itself,
and no receipt records which spelling each tree carries.
Fix: one quirk spelling of every type in every generated tree (the frozen `:342` plan), and one
control mutant per spelling class. **Shown able to fail:** `M03` and `M05` each `fixtures=0/13`
under the frozen generator, `fixtures=13/13` under V1 (M03) and V2 (both) with the guarantee
removed; the per-tree census reads `8/8` on the frozen generator and `0/8`, `0/8`, `2/8` on the
guarantee-free copy (E2).

**M40-2 — the first reference model mis-expanded a 3-value CSS gap, and only some trees could notice.**
Class: wrong reference model masked by fixture sampling — the model is wrong, the suite's coverage
of the input class is partial, so the failure count under-reports the defect.
Evidence: the correct expansion is CSS shorthand `1: all; 2: v h; 3: t h b; 4: t r b l`
(`quality/counters/c1-r40-live.py:188-196`, `:195` `n = [n[0], n[1], n[2], n[1]]`; reference tool
`.ufo/waves/round-40/c1/ctl-ref-tool.py.txt:588-617`, `:615-616`). The L1's first model
mis-expanded it and **2 of 8** generated fixtures failed. Reconstruction (E1-V1): with the per-tree
guarantee removed and gap arity drawn uniformly 1–4, only **4 of 8** trees at rev `e2b51d3b` carry a
3-value gap at all (per-tree `[False, True, False, False, True, False, True, True]`), and the wrong
3-value expansion then fails 7 of the counter's 13 fixtures instead of the suite — a partial kill
that depends on which trees drew the class. The `2 of 8` figure itself is not reproducible: the
first draft is uncommitted, so the count cannot be re-derived; what is re-derivable is the
mechanism (partial class coverage) and the current kill.
Captured-by: none — the wrong model was found by scoring the model against the generator's own
fixtures, after the generator existed; no source-grounded expansion was written first.
Fix: the expansion is grounded in the source (the CSS 1/2/3/4 rule, cited at the counter's
`:188-196`) and every tree carries a 3-value gap. **Shown able to fail:** `M05` (3-value swap)
`fixtures=0/13` under the frozen generator. At rev `e2b51d3b` the eight quirk gaps are
`9 19 18`, `39 36 4`, `1 26 3`, `28 36 30`, `2 26 7`, `6 36 19`, `20 17 5`, `16 14 5` — none has
`n[0] == n[1]`, so the swap is not masked by a value collision at this rev; a tree whose first two
values collided would let the swap pass, which is why the kill is asserted per revision, not
absolutely.

**M40-3 — a naive compare read the compositor's own conversion as 14 host divergences.**
Class: instrument defect reported as data — identity compare over a surface that converts.
Evidence: normalise the 70 committed native replies
(`.ufo/waves/round-40/c1/native-capture.jsonl`) into the base tool's `--getoption` shape
(`{value, custom_type, set}`) and run the base tool
(`git show 9fc511d:tools/mado-options.py`) against the host tree: `labels {mismatch: 14,
agreement: 50, agreement*: 6}` (E4). The 14 are 11 colour keys, 2 font-weight keys and the one bool
declared `yes, please :)`. The native-form model on the same bytes reads `agreement=62
agreement*=8 mismatch=0` (`.ufo/waves/round-40/w1/ExecLiveCensus.md`, `census-receipt.txt`). So the
14 is the base tool's naive rule, not host drift: the base tool's own documented comparison
(`tools/mado-options.py:53-60`, "Value comparison for `agreement`") handles int/float and the
scalar-versus-uniform-tuple case but has no colour, gradient, gap or weight conversion — which is
also why `general:gaps_in`/`gaps_out` do not appear among the 14.
A blunter rule — exact trimmed text equality — gives 39 mismatches (int 24, float 2, custom 13),
measured by this seat over the same bytes; the 14 is specifically the base tool's rule, which is
why that number reproduces exactly and the blunter one does not.
Captured-by: none — the base tool's rule is documented and its 14 labels read as a finding; no
control asked "what would this instrument say on a tree where nothing drifted?".
Fix: compare in the native forms, converting per the host's own handlers, including the
angle-inheritance rule (`gradient_text(declared, inherited)`, counter `:169-185`; call site
`.ufo/waves/round-40/c1/ctl-ref-tool.py.txt:644-656`, `:656`
`options[row["key"]].get("_angle", 0)`). **Shown able to fail:** `M15-angle-inheritance-absent`
`fixtures=0/13` (`receipts/ctl-c1.txt`); and the no-inheritance variant of the reference flips
exactly the two dependent keys (`general:col.active_border`, `group:col.border_active`) —
`62/8/0 → 62/6/2` in `w1/ExecLiveCensus.md` — so the rule is isolated from the colour conversion
rather than confounded with it.

**M40-4 — round-39's fix for the same class put distractors in the trees and did not generalise to a per-type guarantee.**
Class: inherited fix that closes one instance of a class (a distractor present somewhere) without
closing the class (a spelling of every type in *every* tree); the receipt still cannot show its own
coverage.
Evidence: `corpus/lessons/round-39.md#mistakes M39-2` — the wave-built tool listed handler names as
options because "the selftest had no flag-variant or keyed-block case"; the fix recorded there is
"two selftest assertions … and the counter's generated trees carry the distractors
(`c2/ctl-wave-v1.txt` `fixtures=1/11`)". One round later the same shape re-appeared one level down:
a tree can carry every distractor and still never carry the *spelling* a conversion mutant gets
wrong (M40-1, E1-V1: `garbage-bool=0/8`). The receipt is the second half of the defect:
`receipts/ctl-c1.txt` is 20 lines — 18 `control=` lines, one per control, plus the summary and
exit lines — and records the final state only, so a reader cannot tell a
generator that guarantees the class from one that drew it by luck without rebuilding all eight
trees from the counter's seed rule (`quality/counters/c1-r40-live.py:522-523`,
`seed = int(hashlib.sha256(("%s:%d" % (rev, i))…`).
Captured-by: none — no seat and no receipt enumerated the per-tree spelling coverage.
Fix: the freeze receipt carries a per-tree spelling census (for each of the eight trees: the bool
spelling, the gap arity, the weight name, the gradient's angle state), so an under-sampled tree set
is visible without re-running a rejected draft. **Shown able to fail:** the census over the frozen
generator prints `trees=8 garbage-bool=8 3-value-gap=8 ultraheavy=8 inherited-angle=8`; over the
guarantee-free copy it prints `garbage-bool=0 3-value-gap=0 ultraheavy=2` (E2) and over E1-V1's
copy `garbage-bool=0 3-value-gap=4 ultraheavy=1` — the check reads the difference that M40-1's
survival turned on.

---

## Candidate QUALITY.md criterion 65

> 65. A generator that exists to kill a conversion or parsing mutant carries, in **every**
> generated tree, one quirk spelling of every value type its model converts — the spelling the
> host's parser accepts by prefix, the negative integer, the fractional-alpha colour, the 3-value
> CSS shorthand, the named weight — and the control set lists one mutant per spelling class, each
> scoring `0/N` on the frozen generator and `N/N` once the quirk guarantee is removed. A broad
> table sampled per tree under-samples: with the guarantee removed at rev `e2b51d3b`, the eight
> trees carry the prefix-garbage bool in `0/8` trees and a 3-value gap in `4/8`, and
> `M03-bool-exact` (prefix versus exact bool) scores `fixtures=13/13` — a full survivor — while
> `M05-gap-three-values-wrong` (3-value shorthand) is caught only by the trees that happened to
> draw the class (`fixtures=6/13`). Under the frozen generator both score `fixtures=0/13`. The
> freeze receipt carries the per-tree spelling census (one line per tree: the spelling of each
> type), so the guarantee is readable from committed bytes without rebuilding the trees from the
> seed rule. (lesson: lessons/round-40.md#mistakes M40-1)

Placement note for the L1: criterion 64 is the current last row (`corpus/QUALITY.md`), so 65 is
free. The row's citation points at the round-40 lesson's `## Mistakes` heading, the section that
carries M40-1; per criterion 54 the anchor resolves against `corpus/lessons/round-40.md` only.
This seat did not edit `corpus/QUALITY.md` — the row is a candidate for the L1 to land.

---

## Evidence (commands this seat ran, in `/tmp` scratch)

Scratch root: `D=$(mktemp -d /tmp/mado-scr-mistakes.XXXXXX)`; lane read-only at
`rev e2b51d3b3f79768282914d57c1fa32cc85dcb06a`. All scoring ran the frozen counter with `--tool`,
the same switch `ctl/run-c1-controls.py:63-69` uses; the counter writes only to its own temp dirs.

**E1 — the two mutants under a generator with the per-tree guarantee removed.**
Mutant bytes are the reference tool (`.ufo/waves/round-40/c1/ctl-ref-tool.py.txt`) with the
harness's own replacement strings (`ctl/run-c1-controls.py:29-30` M03, `:33-34` M05).
- **V1** = the frozen counter with one substitution, asserted to occur exactly once:
  `plan = [(k, True, "agree") for k in kinds]` → `plan = [(k, False, "agree") for k in kinds]`
  (the broad tables stay intact).
- **V2** = V1 plus two more: `"yes", "true", "on", "1", "yes, please :)", "no", "off",` →
  `"yes", "true", "on", "1", "no", "off",` and `n = 3 if quirk else rng.randint(1, 4)` →
  `n = rng.choice((1, 2, 4))`.

```
M03-bool-exact               frozen         fixtures=0/13
M03-bool-exact               V1             fixtures=13/13     <- survivor
M03-bool-exact               V2             fixtures=13/13     <- survivor
M05-gap-three-values-wrong   frozen         fixtures=0/13
M05-gap-three-values-wrong   V1             fixtures=6/13      <- caught by 4/8 trees only
M05-gap-three-values-wrong   V2             fixtures=13/13     <- survivor
```

All runs print `exit=1`; on the V1/V2 lines the exit is clause b (the reference tool's selftest is
71 < the required 79), not the fixture line — the fixture count is the observable, exactly as in
`ctl/run-c1-controls.py:82-89`.

**E2 — per-tree spelling census (the M40-4 receipt check).**
Rebuilds the eight trees from the counter's own seed rule (`:522-523`) and `Fixture` class, then
counts per class:

```
frozen   trees=8  garbage-bool=8  3-value-gap=8  ultraheavy=8  inherited-angle=8
V2       trees=8  garbage-bool=0  3-value-gap=0  ultraheavy=2  inherited-angle=8
V1       trees=8  garbage-bool=0  3-value-gap=4  ultraheavy=1  inherited-angle=8
```

**E3 — V1's per-tree 3-value gap coverage** (the M40-2 reconstruction):
`[False, True, False, False, True, False, True, True]` — 4 of 8 trees.

**E4 — the naive run reproduces 14/70 exactly.**
Normalised capture (`{key: {value, custom_type, set}}` from the committed jsonl, 70 keys) then
`python3 -I <base tool> --home /home/vgpnk --getoption /tmp/mado-naive-live.json` → exit 0,
`labels {'mismatch': 14, 'agreement': 50, 'agreement*': 6}`, total 70. The 14 rows:
`animations:enabled` (`yes, please :)`), `decoration:shadow:color`, `general:col.active_border`,
`general:col.inactive_border`, `group:col.border_active`, `group:col.border_inactive`,
`group:col.border_locked_active`, `group:col.border_locked_inactive`, `group:groupbar:col.active`,
`group:groupbar:col.inactive`, `group:groupbar:text_color`, `group:groupbar:text_color_inactive`
(11 colour), `group:groupbar:font_weight_active`, `group:groupbar:font_weight_inactive` (2 weight).
Exact trimmed text equality over the same bytes gives 39 mismatches (`int 24, float 2, custom 13`).

---

## Limits and conflicts (verbatim)

- **Before-state uncommitted.** The first generator draft's control run (M03/M05 surviving) and the
  first reference model's `2 of 8` failure are not in any commit. The L1 states both; this seat
  re-derived the first class of failure (E1: M03 survives outright under V1/V2; M05 survives under
  V2 and is caught only partially under V1) and the mechanism of the second (E3). The `2 of 8`
  number is reported as stated, not as measured.
- **`14 of 70` agrees with my re-derivation**, but only under the base tool's comparison rule (E4);
  it is not a count of host drift. `w1/ExecLiveCensus.md` gives `mismatch=0` under the native
  model, and no committed receipt carries a naive-run label census — E4 is the witness this draft
  offers, and it is scratch, not committed.
- **Seeds depend on the revision.** E1–E3 and the M40-2 collision statement are true at
  `e2b51d3b`; a later revision re-draws the trees, so the census must be re-run (and committed) at
  the data rev.
- **Not done here:** no edit to `corpus/QUALITY.md`, `corpus/lessons/round-40.md` or any tracked
  file; no commit; the full `ctl/run-c1-controls.py` harness was not re-run (the committed
  `receipts/ctl-c1.txt` is quoted, and E1 uses the counter's `--tool` switch on two mutants only);
  no compositor verb was run by this seat.
