# RevQualityOverlap — do QUALITY 1–23 already contain criteria 24–26?

Seat `MadoR18.RevQualityOverlap`, reviewer. Date 2026-10-20. Round 18, wave 1.
Scope: `corpus/QUALITY.md` criteria 1–23 at the pre-registration commit
`d3a0000e6ef0b1e3c7b4faf52d592eb293857ba` (blob `c5fd80139d72…`; byte-identical
at `d9a5a18` and in the current worktree — no seat has appended 24–26 yet, so
this review is prospective). Question: do 24–26 (R17-V1 receipt provenance,
R17-V5 mutant receipts, JjAuditMado F10 pipe digest) add a distinct,
falsifiable rule, or do they restate an existing criterion and inflate the
lesson-cited fraction?

Method: read-only `git show`/`git log`/`git ls-tree`, plain file reads, and a
`/tmp` re-implementation of the published c1 regex
(`^[0-9]+\. ` / `^[0-9]+\. .*lessons/`). I did not run the lane gates
(`measure.py`, `label-check.py`, `mado-tripwire.py`, `mado-verify.sh`). I did
run the two new, still-untracked round-18 checks read-only:
`receipt-check.py` (rc=2, `EXPECT_SUMMARY: 9/15`) and `pipe-rc-census.py
d9a5a18` (rc=1, `VERDICT RED`). No git/jj write, no host action, no install.

## 0. Bottom line

| proposed | existing criteria that already bind the defect | distinct residue left | verdict |
|---|---|---|---|
| **24** R17-V1 | 7 no; 9 half (inputs pinned, producer not); 10 half (count shape, no tool); 13 yes (committed); 23 conditional, token-scoped | the digest of the **executable bytes that actually ran**, and a re-cut claim falsifiable from the receipt's own bytes | **distinct only if narrowed**; broad phrasing duplicates 6+9+10+13+23 and PROTOCOL §Gate standard |
| **25** R17-V5 | 13 yes on location (`/tmp`); 1 says falsifiable, not red-case; 21 is a single-instrument instance | the **delta**: a committed case the pre-change instrument credits and the post-change rejects, at both named digests | **distinct**; but "commit your evidence" is 13 and must not be re-legislated |
| **26** F10 | 3 yes in principle (unknown≠observation); 2 yes in principle (empty digest is not a measured anchor); 9 satisfied on its face (a sha is printed) | the **mechanism**: producer-status capture for pipeline-derived verdicts; empty input is never evidence; census over `tools/*.sh` | **distinct as a code-level extension of 3**; abstract phrasing is 3 restated |

No criterion here is *necessarily* an inflation; two of the three have a broad
phrasing that is. Section 6 gives the clauses that must be dropped to avoid it,
and the arithmetic that depends on single-line formatting.

## 1. The bar's own anti-duplication standard

`corpus/QUALITY.md` has twice declined a provenance criterion when 7/9/13
already sufficed, and recorded the rejected candidate instead:

> `QUALITY.md:57-61` — “R13-V2/V3 use existing criteria 7, 9 and 13: a within-run boundary
> receipt does not establish cross-revision output equality, and future
> standalone selftest receipts carry their resolved commit and raw gate
> digest locally. No duplicate provenance criterion or generic wrapper is
> introduced; the lesson records the rejected implementation candidate.”

> `QUALITY.md:65-70` — “R14-V1 applies existing criteria 7, 9 and 13: preserve provisional historical
> headers; append their exact derived-target relation to committed bytes.
> Never stamp a later full-gate measured commit onto a pre-commit mutation run.
> The lesson's M1 and standing-use erratum name the boundary and red/green
> static correction audit; no generic execution wrapper or duplicate
> provenance criterion is introduced.”

The same file records the accepted exception: criterion 23 extends 9 at
token level and says so in its own text (`QUALITY.md:118-119`:
“This specifies criterion 9's commit binding at token level”). A new criterion
is admissible in this bar when it names the criterion it extends and adds only
the mechanism that criterion lacks; it is inflation when it restates the
extension target. Criterion 22 (`QUALITY.md:107`) also requires literal and
semantic counters to be reported separately rather than silently switching
rubrics.

`QUALITY.md:24`: “this bar governs claim admission only.” That matters for
criterion 26, which is a code-invariant rule, not a claim rule.

## 2. R17-V1 vs 7, 9, 13, 23

Quoted verbatim:

> `QUALITY.md:13` — “7. Hash committed artifacts from `git show <commit>:<path>`; label work-window hashes provisional and bind them again at the commit. (lesson: lessons/round-12.md#mistakes M2; lessons/round-10.md:98-107)”

> `QUALITY.md:15` — “9. Bind each audit verdict to a commit or frozen-copy sha; label mid-edit failures in-flight, never as settled defects. (lesson: lessons/round-12.md#mistakes M6; lessons/round-10.md:98-107)”

> `QUALITY.md:19` — “13. Evidence meant to outlive a round is a committed path or quoted lines plus sha; `/tmp` records provenance only. (lesson: lessons/round-12.md#mistakes M11; lessons/round-10.md:74-78)”

> `QUALITY.md:111-119` — “23. A sentence that attributes a verdict token to a receipt must cite a receipt whose recorded outcome is that token at the revision the sentence describes … When the receipt records a `measured_commit`, the sentence's revision must match it. A superseded receipt is named as superseded and keeps its true token; corrections append and never relabel. This specifies criterion 9's commit binding at token level; it did not bite on round-16 line 131-132 because 9 binds the commit, not the token.”

Adjacent rules that already carry part of the load:

> `QUALITY.md:12` — “6. Publish each pinned value with a re-derivation command and named revision; any shortened hash must be a true suffix, with corrections preserving old and new values.”

> `QUALITY.md:16` — “10. Report each count as `<n> — <command> <date>` and rederive it from the named revision instead of transcribing a prior summary.”

> fleet `PROTOCOL.md:393-394` (S003) — “A verdict names the revision it was measured against: a gate grades the tree it runs on, so a run over a moving worktree is not comparable to one over the cited commit.”

### 2.1 Artifact test (what the receipts actually carry)

At `d9a5a18`, the six cited scan receipts are all committed (criterion 13
satisfied) and all last changed at `f71ccbe` — never re-cut at `0ab1ccc`, which
is exactly R17-V1:

| receipt | `tool_sha256` | `measured_commit` | input `"sha256"` fields | last change |
|---|---|---|---|---|
| `evidence/tripwire-r13.txt` | 0 | 0 | 33 | `f71ccbe` |
| `evidence/tripwire-r14.txt` | 0 | 0 | 33 | `f71ccbe` |
| `evidence/tripwire-r15.txt` | 0 | 0 | 65 | `f71ccbe` |
| `evidence/tripwire-r16.txt` | 0 | 0 | 97 | `f71ccbe` |
| `evidence/tripwire-anchor-r15.txt` | 0 | 0 | 1 | `f71ccbe` |
| `evidence/tripwire-pacmanlog-join.txt` | 0 | 0 | 0 | `f71ccbe` |

Tool digest by revision (`git show REV:tools/mado-tripwire.py | sha256sum`):
`988b858` = `4ced68d3…`, `f71ccbe` = `7a98720e…`, `0ab1ccc` = `962919ce…`.
The lesson sentence `corpus/lessons/round-17.md:175-176` (“… tool sha256
`962919ce…`; all real-transcript receipts re-cut with identical counts.”)
therefore claims a re-cut under a tool digest that no cited receipt records and
that git shows never occurred (`0ab1ccc` touches none of the six files). That
is R17-V1/V2, confirmed.

### 2.2 What each criterion does and does not reject

- **7 — no.** 7 governs how a committed artifact is hashed (`git show
  <commit>:<path>`). The receipts are the artifact; 7 has nothing to say about
  what a receipt must record. It did not bite.
- **9 — half, and it did not bite.** “Bind each audit verdict to a commit or
  frozen-copy sha”: each receipt carries per-input sha256 values, so the scan
  verdict *is* bound to the transcript bytes (a frozen-copy sha). 9 is
  satisfied and the receipts pass. 9 says nothing about the tool that produced
  the verdict, so the producer gap survives it.
- **10 — half.** The counts are pinned values and 10 demands
  `<n> — <command> <date>` rederived from the named revision. The receipts lack
  the revision *and* the tool, so 10 arguably rejects the summary sentence's
  revision half, but not the producer half. Do not restate 10 in 24.
- **13 — satisfied, and it did not bite.** The receipts are committed paths.
- **23 — conditional and token-scoped, and it did not bite.** 23 is about a
  sentence attributing a *verdict token*. Two escapes apply here: (a) the
  round-17 sentence attributes a *process* (“re-cut … with identical counts”),
  not an outcome token; (b) the commit clamp is conditional — “When the receipt
  records a `measured_commit`” — so a receipt that records none passes by
  construction. 23 is the closest criterion and its own text concedes the gap
  (“9 binds the commit, not the token”); 24 is the same move one level further
  (the *producer*, not the token).
- **PROTOCOL §Gate standard** already requires “a verdict names the revision it
  was measured against”. The revision half of R17-V1 is a **contract
  compliance** failure, not a QUALITY gap; repeating it in 24 would duplicate
  the contract as well.

### 2.3 The distinct residue for criterion 24

The only facts not derivable from 6/9/10/13/23 or PROTOCOL are:

1. **Which bytes ran.** Under jj colocation the working-copy tool can differ
   from the tool at the named commit. A receipt that names `measured_commit`
   lets a reader derive *the committed* tool digest (`git show REV:tool`), but
   not the digest of the file that actually executed. Recording the executing
   file's sha256 is new information and is the jj-relevant guard.
2. **A re-cut claim must be falsified or evidenced by the receipt bytes
   themselves.** Git's silence is not a receipt; if a re-cut under a new digest
   is claimed, the receipt at the named revision must record that digest (or
   the receipt's committed bytes must show the change).

Those two clauses are distinct and falsifiable: the six round-17 receipts fail
them (0/6 tool digest, 0/6 measured commit), while an authored fixture with
`measured_commit` + `tool_sha256` passes. If criterion 24 is written as
“receipts must be committed and name the revision”, drop it: that is 13 + 10 +
PROTOCOL, i.e. inflation.

## 3. R17-V5 vs 1, 13, 21 (and 18)

> `QUALITY.md:3` — “1. Every claim falsifiable or marked opinion.”

> `QUALITY.md:19` — criterion 13, quoted in §2.

> `QUALITY.md:87-91` — “A static action-plan classifier must return nonzero on the literal libinput
> incident argv, listed argv[0] basenames even when path-prefixed or
> mislabeled, unknown kind and malformed action, with a source-read control.”

> `QUALITY.md:94-95` — “a hard-coded new-only fixture never proves it ran.”

Criterion 18 embeds the same pattern for another instrument (“Exercise
mixed-glob rejection without misclassifying its regular member”,
`QUALITY.md:46`). So the bar has *instances* of a red-case requirement but no
general rule.

### 3.1 Artifact test

- The tightening is committed: `ab0bc9b` changes only
  `.ufo/waves/round-17/measure.py` (+36/−4, “tighten rubric-V instrument
  (exact surface line, pinned legacy, relevance, facet floor)”).
- No committed mutant for it exists at `d9a5a18`: `git ls-tree -r d9a5a18
  .ufo/waves/round-17` matches `mutant|variant|tamper` only on
  `evidence/frozen-tampered-recut.json` (tripwire) and
  `evidence/schema-variants.json` (SOURCES schema), plus seat reports.
- The round-17 report nevertheless claims the delta:
  fleet `.ufo/reports/round-17/mado.md:113-115` — “Mined mistakes:
  `lessons/round-17.md` § Mistakes M1-M5 (each fix shown able to fail:
  label-check red line; instrument tightenings; tripwire anchor exit 1)”.
- The lesson self-discloses the gap at `corpus/lessons/round-17.md:156-158`:
  “the instrument tightenings were shown to bite only in a wave-2 seat's
  `/tmp` lab … not by a committed mutant receipt; "shown to bite" is
  seat-attested, not lane-receipted.”

### 3.2 What each criterion does and does not reject

- **13 — location only.** It rejects the `/tmp` demonstration as round-outliving
  evidence (and the lane disclosed that, which is why R17-V5 is a routed
  upgrade rather than an admitted falsity). But a committed **green** suite
  satisfies 13 and still does not establish that the tightening bites.
- **1 — in principle only.** A rerun is a falsifier, so “bites” is falsifiable,
  but 1 does not require the falsifier to be a *rejecting* case committed next
  to an *accepting* one. A green receipt of the new instrument alone satisfies
  1 and 13.
- **21/18 — single-instrument instances.** 21's red-case clause is scoped to
  the action-plan classifier; 18's to mixed-glob source targets. Neither
  generalizes to every instrument change.

### 3.3 The distinct residue for criterion 25

The delta rule: for an instrument change, cite a committed case the **pre-change
instrument credits** and the **post-change instrument rejects**, with both
instruments identified by their committed digests. That is not implied by
1 + 13 (which admit a committed green run) and is broader than 21 (one
instrument). “`/tmp` does not count” must be cited to 13, not restated.

## 4. F10 vs 2, 3, 9

> `QUALITY.md:4-5` — “2. Every claim carries a source: a measured anchor (path:line, command,
>    evidence id) — never oral knowledge.”

> `QUALITY.md:6` — “3. Observation, inference, and unknown stay separate.”

> `QUALITY.md:15` — criterion 9, quoted in §2.

### 4.1 Source and reproduction

`tools/mado-verify.sh:3406-3408` at `d9a5a18`:

```
blob=$(tmo git -C "$tree" show "HEAD:$OMARCHY_SKILL_REL" 2>/dev/null | sha256sum | cut -d' ' -f1)
sw=$(sha256sum "$leaf" 2>/dev/null | cut -d' ' -f1)
if [ -z "$blob" ]; then
```

`blob` is always 64 hex characters, so the `-z` UNKNOWN arm is dead; a failed
`git show` becomes the empty-input digest `e3b0c442…` and the row prints
`FAIL … (local edit)`. The jj audit's F10 reproduces it; the worktree fix
(`OM9` scenario, `STUB_GIT_SHOW_RC=128`) now asserts UNKNOWN. The selftest stub
before round 18 exited 0 for every verb (JjAuditMado F14), so no scenario could
reach the arm.

### 4.2 What each criterion does and does not reject

- **3 — the classification, yes.** A failed read is unknown; printing FAIL
  collapses unknown into observation. A criterion written as “a failed read is
  unknown” is 3 restated. Crucially, 3 is *claim*-scoped; it did not stop a
  *tool* from printing the false FAIL, because no reviewer applied it to
  verdict-producing code.
- **2 — in principle.** The empty-input digest is not “a measured anchor” for
  the blob; the FAIL's anchor is fabricated, not missing.
- **9 — satisfied on its face, and it did not bite.** The FAIL prints a sha and
  a path; the binding exists, it is just wrong. 9 requires binding, not that
  the bound value be measured.
- **PROTOCOL §Gate standard** maps undeclared nonzero *exit codes* to
  could-not-evaluate; it does not govern internal pipelines.

### 4.3 The distinct residue for criterion 26

A verdict or digest derived by piping a producer into a consumer must capture
the producer's exit status; a failed read forces unknown; the digest of empty
output is never evidence about the intended input — enforced by a static census
over `tools/*.sh`. This is a mechanism 3 does not state and a code-level
extension of it. If criterion 26 is written as “observation, inference and
unknown stay separate”, it is 3 restated and should be dropped.

## 5. The runnable checks that already exist in the worktree (uncommitted)

These are wave-1 artifacts; I read them at 12:44–12:45Z and did not edit them.
They are evidence that 24–26 can be made falsifiable, not yet evidence under
criterion 13 (they are untracked).

- **24 — `.ufo/waves/round-18/receipt-check.py` + `receipt-claims.json`.**
  Requires `tool_sha256` and `measured_commit` and resolves the tool digest
  against `git show <measured_commit>:<tool>`. Run: rc=2,
  `EXPECT_SUMMARY: 9/15` — six round-17 receipts `MISSING_PROVENANCE` (red
  shown), three fixtures `ok`/`SHA_MISMATCH`/`SHA_MISMATCH` (the last one is
  the R17-V2 cross-binding shape: `962919ce…` attested at `f71ccbe`, whose tool
  is `7a98720e…`), six re-cut claims `PENDING`. The red side is demonstrated;
  the green side is **blocked on L1** committing the re-cut receipts.
- **25 — `.ufo/waves/round-18/measure-mutants.py` +
  `evidence/measure-mutants.json`.** Six mutants (M1 exact surface line,
  M2 legacy pin, M3 upstream keyword, M4 section floor, M5 registry-only,
  M6 duplicate id), loose `f52f43f` (`a280b3ab…`) vs tight `d9a5a18`
  (`de4c422b…`), run in a throwaway `/tmp` repo: `mutants 6, bites 6,
  no_bite []`, baselines agree. Good. Gap: no negative control, so `no_bite`
  is reachable in code but never demonstrated; one mutant both instruments
  reject would prove the check can report a non-bite.
- **26 — `.ufo/waves/round-18/pipe-rc-census.py`.** Run at `d9a5a18`: rc=1,
  `SUMMARY … files=1 sites=12 checked=3 unchecked=9`, `VERDICT RED`. The nine
  unchecked sites are `:640, :942, :944, :962, :1377, :2788, :3406, :3444,
  :3474`; `:3406` (F10) is among them, so the red case exists and the check
  exits nonzero. The green side needs the fixed revision. Note my own first
  invocation masked the census's rc with `| tail` — the same defect class; the
  check must never be consumed through a pipe without `${PIPESTATUS[0]}`.

## 6. Inflation test and the score arithmetic

### 6.1 The discriminating test

A new criterion is load-bearing only if its runnable check rejects at least one
artifact that every existing criterion admits. Applying that:

- 24: the six round-17 receipts pass 9 (input shas) and 13 (committed) and 23
  (no measured_commit recorded); they fail a receipt check that demands the
  producer digest and a mandatory measured_commit. **Passes — provided the
  criterion states only that.**
- 25: the round-17 report's “instrument tightenings … shown able to fail”
  passes 1 and 13 if a committed green suite existed; it fails a check that
  demands the pre/post delta. **Passes — provided the delta is stated.**
- 26: the false FAIL at `:3406` passes 9 on its face (a sha is printed) and
  would be *rejected* by 3 only if 3 were applied to code; the census flags it
  mechanically. **Passes as a code-level extension of 3; as an abstract
  restatement of 3 it is inflation.**

To keep the bar honest, the lesson should record the clauses deliberately *not*
made into criteria (R13-V2/V3 precedent): the commitment rule (13), the
revision/count rule (10, PROTOCOL §Gate), the token rule (23), and the
classification rule (3). Without that record the three additions look like
numerator engineering even if each residue is real.

### 6.2 Arithmetic under the published c1 rule

Measured on committed bytes with the exact published regexes
(`.ufo/waves/round-17/measure.py:82-96`):

| state | criteria | literal lesson-cited | score |
|---|---|---|---|
| baseline `d3a0000` | 23 | 15 | **6.5217** |
| 24/25/26 all on one physical line | 26 | 18 | **6.9231** (target) |
| two on one line, one wrapped | 26 | 17 | 6.5385 (misses ≥18/26) |
| all three wrapped | 26 | 15 | 5.7692 (**below baseline**) |

Criterion 22 also requires both counters, so note: the baseline **semantic**
count (citation anywhere in the criterion's block) is 18/23 = 7.8261, because
criteria 18, 19 and 20 wrap their `(lesson: …)` onto a continuation line and
are invisible to the literal rule. The literal 18/26 target therefore lands
*below* the bar's existing semantic lesson-cited count; the score movement
from 6.5217 to 6.9231 is a formatting-sensitive measure, not by itself proof of
a stricter bar. State both numbers in the round report.

Operational consequence for L1: each criterion must be **one physical line**
with the `(lesson: lessons/round-18.md#mistakes Mn)` citation on that same
line, and `corpus/lessons/round-18.md` must exist at the measured revision (it
does not yet; the round-17 closure verified exactly this for criterion 23).

## 7. Findings by severity

**P1 — inflation risk in the broad phrasings.** If 24 says “receipts must be
committed and name the revision”, it duplicates 6 + 9 + 10 + 13 + 23 and
PROTOCOL:393; if 25 says “commit your evidence”, it duplicates 13; if 26 says
“a failed read is unknown”, it duplicates 3. Each must state only the residue
in §2.3/§3.3/§4.3 and name the criterion it extends, as 23 names 9. Evidence:
quotes in §1–§4; the receipts’ input shas (§2.1) show 9 is already satisfied.

**P1 — the formatting trap is decisive.** 18/26 = 6.9231 only if all three are
single-line; one wrapped drops to 17/26 = 6.5385, all three to 15/26 = 5.7692.
This is not gaming — it is the published literal rule — but L1 must format
deliberately; criteria 18–20 already lost their citations to wrapping.

**P2 — criterion 24’s check cannot be green at integration without L1.**
`receipt-check.py` exits 2 (`9/15`) while the six re-cut claims are `PENDING`;
the red side is shown, the green side requires committed re-cut receipts with
`tool_sha256` and `measured_commit` at the landed revision.

**P2 — criterion 26’s census is broader than F10.** Nine unchecked sites at
`d9a5a18`, not just `:3406`: `:640`, `:942`, `:944`, `:962`, `:1377`, `:2788`,
`:3444`, `:3474` in addition. Three of them are `find … | wc -l` count sites
feeding NOTE rows (`:2788` backup-file count, `:3444` skill-group word count,
`:3474` hook-dir count), and `:640`/`:962` hash a fixture file created moments
earlier. The criterion must be scoped to *verdict-bearing digests/comparisons*
and the check must carry per-site judgement; otherwise it either over-flags
benign counts or, if narrowed to one line, under-tests. `wc` also cannot
distinguish producer failure from a legitimate empty input (`find` finds
nothing), so a blanket “every pipe must capture rc” rule would be wrong.

**P2 — criterion 25’s check has no non-bite control.** `no_bite` is computed
(`measure-mutants.py:564`) but never exercised; add one mutant both instruments
reject so the check is shown able to report “does not bite”, not only “bites”.

**P3 — 23’s conditional is the specific loophole.** “When the receipt records a
`measured_commit`” lets a receipt with no such field pass; 24 should make the
field mandatory for a tool-run receipt rather than restating 23’s clause.

**P3 — the tool-digest distinction must survive quoting.** The round-17 report
cites `7a98720e…` (the `f71ccbe` tool) while the landed tip is `962919ce…`;
24’s check resolves the digest against the named commit and its stale-rev
fixture is exactly that cross-binding, so a report sentence must not reuse the
wrong digest when citing a re-cut.

## 8. Residual risk and verification gaps

- I did not run `measure.py`, `label-check.py`, `mado-tripwire.py` or
  `mado-verify.sh`; the c1 figures come from the published regex re-implemented
  on `git show d3a0000:corpus/QUALITY.md` (23 criteria, 15 literal, 18
  semantic), and the target figures from the same expression on a `/tmp` copy.
- F10’s failure mode is source-verified (`:3406-3408`) and quoted from
  JjAuditMado’s reproduction; I did not re-execute a failing `git show`.
- The round-18 checks and their receipts are untracked and owned by other
  seats; they may change before integration. Per criterion 13 they are not
  evidence until committed.
- The census is static; it cannot prove a flagged site is a hazard (some may
  hash a file already proven present). Its own exit status must be consumed
  without a pipe that discards it.

No tool was installed or upgraded for this review.
