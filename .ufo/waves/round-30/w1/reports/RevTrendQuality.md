# RevTrendQuality — attack on the round-30 quality-trend verdict

Item: review only (no lane writes beyond this report). Revisions read: base
`8f51071b`, freeze `451e8b3c`, data `446dc39`, tip `92d3c86`. Every measurement
below reads committed bytes (`git show REV:path`) or a scratch copy under
`/tmp`; nothing in the lane was edited, committed or reverted.

## Axes named

1. **calibration / grounding (the scored axis)** — every active criterion
   resolves a `lessons/` citation.
2. **supersession fidelity** — is the active rule text of rows 41–51 equal to
   the rule it supersedes.
3. **evidence reproducibility** — does each receipt reproduce from the
   revision it names.
4. **re-verification** — was any stale entry or instrument re-measured.

## Verdict

| Axis | Verdict | Basis |
|---|---|---|
| 1 calibration / grounding | **improved** | counter reproduced at both revisions (below) |
| 2 supersession fidelity | **harmed** | 4 of 12 rows are not verbatim; one normative clause dropped (`H2`) |
| 3 evidence reproducibility | **harmed** | freeze-smoke C2 leg is not reproducible and not raw output (`H1`) |
| 4 re-verification | **unchanged** | no stale instrument re-run; the r29 composite still passes at tip |

Net: the **scored** quality axis improved; the **quality record** was harmed in
two places. The spot-check verdict "quality — improved" is supportable only for
axis 1 and repeats two sub-claims that the committed bytes do not support
(`H1`, `H2`).

## H1 (HIGH) — the freeze-smoke C2 leg is not reproducible from its labeled revision and is not the counter's output

`git show 451e8b3c:.ufo/waves/round-30/evidence/freeze-smoke-451e8b3c.txt`
C2 block is four lines:

```
--- C2 at freeze ---
UNRESOLVED criterion 39: no citation
UNRESOLVED criterion 40: no citation
LINE 20 superseded excluded
PRED-C2-r30 verdict=TARGET_MISSED
```

- It omits the `counter=c2-grounding-r30 rev=…` header and all three `METRIC`
  lines. The frozen counter prints those on every non-error path
  (`.ufo/waves/round-30/c2/count.py`, `main()`): `c2-before-8f51071b.txt`,
  `controls/C2K1-donothing.txt` and `c2-after-446dc396.txt` all carry them.
- The frozen counter (extracted from `451e8b3c`) at **`451e8b3c`** prints
  `literal 28/40`, `superseded=[20]`, `active=39 resolved_active=31`,
  `UNRESOLVED {1,2,3,4,5,38,39,40}`, `TARGET_MISSED` — identical to its
  output at `8f51071b` except the `rev=` line, because `corpus/QUALITY.md` at
  the freeze commit is the base bytes (40 numbered lines; the freeze commit
  adds no `corpus/` path).
- No commit in play yields the receipt's two-unresolved state: base and freeze
  → 8 unresolved; data and tip → 0. The two-unresolved state is exactly a
  mid-authoring worktree (rows 41–48 present, 49–51 absent), matching the
  registration's note that the worktree already carried the claimed edits.

Consequences, all cited to committed logic/text:

- Registration *Data rule*: "all measurements read committed bytes at named
  revisions (`git show REV:path`), never the worktree" — violated for this leg.
- QUALITY 9 (bind a verdict to a commit or frozen-copy sha; label mid-edit
  failures in-flight, never settled) — the receipt labels worktree output with
  the freeze sha.
- QUALITY 49 (a composite counter "is smoke-run once at freeze … and its full
  output is committed") — the committed output is not the counter's full
  output for C2, so the composite smoke rule is not satisfied.
- `SCORECARD.md` round-30 section ("freeze smoke … ran all three counters at
  the freeze") and `LOG.md` round-30 ("all three counters run at the freeze
  commit `451e8b3c` and print real tallies") are falsified for C2.
- The non-author spot-check re-ran C2 at base and tip but never checked this
  receipt, so it did not catch it.

C1 and C3 legs **do** reproduce: the gate at `451e8b3c` prints
`MADO_INDEX: … indexed=41/43 missing=2` exit 1, matching the receipt.

Repair: re-run the C2 leg at `451e8b3c`, commit its full output, and restate
the SCORECARD/LOG sentence; or strike the C2 line and downgrade the "composite
at freeze" claim to the two legs that reproduce.

## H2 (MEDIUM-HIGH) — 4 of 12 supersessions are not verbatim, one drops a normative clause, and the committed preamble says otherwise

Per-row comparison of the rule body (base criterion vs superseding row, tail
after `Supersedes` excluded):

| row ← criterion | rule body |
|---|---|
| 41←1, 42←2, 43←3, 44←4, 45←5 | identical prefix ✔ |
| 46←18, 47←19 | identical prefix; only the trailing citation moved (by design) ✔ |
| 48←32 | prefix identical, **body deletions** ✘ |
| 49←38, 50←39, 51←40 | **body deletions** ✘ |

Deleted spans (exact strings):

- **48←32**: `Ground: lesson round21 M13, `residual/FinalBindingReview.md` F1–F5 and its six inert fixtures. This criterion is added after final falsification, supplies no retroactive pass and no numeric C2/criterion-count credit; delivered C1 fails it and remains harmed.`
  The replacement tail restores `residual/FinalBindingReview.md F1–F5 and its
  six inert fixtures` but **not** "supplies no retroactive pass and no numeric
  C2/criterion-count credit". Row 48 is counted inside `active=40` **and**
  `resolved_active=40` (`c2-after-446dc396.txt`) — the round takes
  criterion-count credit from the criterion whose text disclaimed it.
- **49←38**: `(M28-1, `count.py:100` pinned count-v4.py at `3d7d301f…` vs committed `635ae788…`)`
- **50←39**: `(M28-2: H1's directory was cleaned before closure; leg 1 verified from the committed `ReviewerSuiteMonotone.md` receipt)`
- **51←40**: `(M28-3: `ref-chk-no-anchor` survived; `ref-chk-unreadable-exit-one` in the same round was killed)`

The committed claim at `corpus/QUALITY.md:344` — "Each superseding row below
restates its rule verbatim" — is false against its own referents; the same
false claim is repeated in `corpus/lessons/round-30.md` (M30-1, fix column) and
in the spot-check's C2 row. No information is destroyed (the data commit is
pure addition, 22 insertions / 0 deletions; the deleted spans survive at
`QUALITY.md:306,334-336`), but the **active** set loses the three worked
instances that gave 49–51 their force, while the record says it did not.

**The fidelity loss was gratuitous** — proved constructively: I rebuilt a
scratch repo from `446dc39` with rows 48–51 restored to their base rule bodies
plus `Supersedes criterion N` and the same canonical citations; the frozen
counter prints `literal 40/52`, `active=40 resolved_active=40`,
`PRED-C2-r30 verdict=TARGET_MET` exit 0. Verbatim preservation costs nothing
under the frozen predicate.

Note also: rows 46, 47 **and 48** were unnecessary for the metric — criteria
18, 19 and 32 already resolved at base under the frozen counter
(`lesson round21 M13` matches `SPELL_RE`; 18/19 resolved from continuation
lines). Only 1–5 and 38–40 moved the number. The one row that changed
substantive text is one of the three that bought nothing.

## M3 (MEDIUM) — 5/40 of the improved numerator rests on a lesson minted in the same data commit

Rows 41–45 cite only `lessons/round-30.md#mistakes M30-1`, and M30-1 is added
by the same commit (`+56` lines). Measured sensitivity: deleting the `| M30-1 |`
table row in a scratch copy of `round-30.md` makes the frozen counter print
`active=40 resolved_active=35 fraction=0.8750`, `UNRESOLVED 41–45`,
`TARGET_MISSED`. The dependency is declared in the registration and the lesson
(`captured-by: none`), so it is honest rather than hidden — but "40/40" is not
robust to removing one self-authored row, and a stricter rubric would require
the ground to predate the repair (or report 35/40 self-ground-excluded).

## L4 (LOW) — new active row 48 carries a path that does not resolve from the corpus root

`residual/FinalBindingReview.md` does not exist in the lane worktree, at
`446dc39`, or in any commit (`git log --all -- residual/FinalBindingReview.md`
empty); the real file is
`.ufo/waves/round-21/residual/FinalBindingReview.md` (19,378 B, present at
`446dc39`). Inherited from base criterion 32, re-propagated into the new active
row instead of repaired, and invisible to the counter (`PATH_RE` only matches
`lessons/round-*.md`). QUALITY 8 (path landed only after confirming it exists
at the named commit) and QUALITY 13 (evidence is a committed path or quoted
lines plus sha) apply.

## L5 (LOW) — registration arithmetic and wording

- "12 lines superseded by rows 41–51": rows 41–51 make **11** new
  supersessions; 12 is the counter's set including criterion 20, which was
  already superseded at base by 21.
- Rows 42–45 carry the typo `uncitation` and are not self-contained ("Same
  seed-uncitation ground").

## L6 (LOW) — counter robustness (latent on committed bytes, but the rubric's own limits)

- `PATH_RE = lessons/(round-[\w.-]+\.md)` matches only `round-*` lesson names;
  a future citation to a differently named lesson scores "no citation". All 37
  lesson files are `round-*.md` today, so this is latent.
- `ANCH_RE` validates the anchor as a whole-file substring
  (`want.lower() in body.lower()`): `#mistakes` resolves for any lesson with
  that heading; anchor locality is never checked.
- Supersession is self-declared text: any later line writing "Supersedes
  criterion 52" retires 52 with no check that the retired rule lost anything.
- Non-`lessons/` citation paths are not checked at all (L4 is the live case).

## Re-verification question

- **The round re-verified nothing stale beyond citation resolution.** No
  round-30 artifact invokes `.ufo/waves/round-29/c1/count.py` (grep over
  `.ufo/waves/round-30`, `LOG.md`, `SCORECARD.md`). Rows 38–40's *citations*
  were re-resolved mechanically; their *rule content* was re-typed, not
  re-measured.
- I ran the r29 six-leg composite at `446dc39` myself:
  `h1-receipt PASS`, `boolword-v5 PASS` (normal 41/41, boolword 2/2, mutant
  0/2), `h2-rotate PASS`, `refpub-kills PASS` (12/12), `q36-witness PASS`,
  `q37-open-ended PASS` (`r26sha=803e0096c994`), `PRED-C1-r29 verdict=TARGET_MET`
  exit 0, 121 s. Its guard pin still matches committed bytes:
  `sha256(.ufo/waves/round-27/c1/count-v4.py) =
  635ae788fd897c8f1fba88e4ab2ffcb95e7f79a88703b82e49a8729ce7d271a1`.
- So no stale-instrument harm accrued: axis 4 is **unchanged**, not improved.

## Residual risk and verification gaps

- I did not run `tools/mado-verify.sh --selftest` or the sources census
  (harm-watch owners), nor re-derive C1/C3 (other reviewers' items).
- Live worktree mutation reported by peer `RevC1Fence` and confirmed read-only
  by me: `M quality/q36-successor-receipts.txt` (4 lines, `git diff` shows only
  ephemeral `/tmp/mado-r28-q36-*` and `/fast/scratch/…/run.*` run-dir paths;
  every `rc=`/`expected=`/`PASS` line unchanged). Uncommitted, outside the
  registered write scope, no verdict moved — but a committed receipt is being
  rewritten in place during the wave.
- Untracked `.ufo/waves/round-30/w1/` is this wave's reports (expected).

## Recommended verdict restatement

Quality = **improved on the scored citation axis** (reproduced: literal
28/40 → 40/52; resolved-active 31/39 → 40/40; base control TARGET_MISSED),
**harmed on record fidelity** (4/12 non-verbatim; the no-credit clause dropped),
**harmed on evidence reproducibility** (C2 freeze-smoke leg), **unchanged on
re-verification**. Withdraw "restates its rule verbatim" and "all three
counters run at the freeze commit" until repaired; re-issue the C2 freeze
receipt from `451e8b3c` or strike the leg.

## Tooling

No tools installed or updated by this seat.
