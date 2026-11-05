# R86ScribeLesson — round 86 lesson draft (scribe seat)

Freeze `237ecf4e69a4986108f719f3beeafe111adaa033`. Lesson landed by L1 at `corpus/lessons/round-86.md`.
Every number below was produced by a command in this seat or read from a named committed/untracked
receipt. Scratch was removed at yield; each command is pasted so it can be re-run.

Verification run by this seat (scratch clone `git clone --no-hardlinks` of the lane, checked out
`--detach 237ecf4e…`; `git -C "$clone" rev-parse --show-toplevel` asserted equal to the clone before use):

| check | command (clone = `<scratch>/lane`) | result |
|---|---|---|
| C1 at freeze | `python3 -I quality/counters/c1-r86-refusal-records.py --repo . --rev 237ecf4e69a4986108f719f3beeafe111adaa033 --base-rev 2b6dd76b65de4dfe701db87db13b7e448b3538ee --controls .ufo/waves/round-86/controls/c1-cases-r86.json --carried .ufo/waves/round-85/controls/c1-cases-r85.json --scratch-root <scratch>/c1` | `MADO_R86_REFUSALS: cases=75 correct=75 mutants=51 killed=51 base_correct=75/75 carried=72/72 tool_selftest=152/152 flooding=48/75 held_flooding=75/75 verdict=TARGET_MET rev=237ecf4e…`; rc 0 |
| C2 at freeze | `python3 -I quality/counters/c2-r86-clause-observations.py --repo . --rev 237ecf4e69a4986108f719f3beeafe111adaa033 --controls .ufo/waves/round-86/controls/c2-cases-r86.json --carried .ufo/waves/round-85/controls/c2-cases-r85.json --scratch-root <scratch>/c2b` | `MADO_R86_RUNBOOK: cases=37 executed=37 matched=37 shapes=27/27 anchors=37/37 rows=37/37 clauses_observed=37/37 … mutants=37 killed=37 verdict=TARGET_MET rev=237ecf4e… tree=bound`; rc 0 |
| held r85 C2 instrument at freeze (declared control 2) | `python3 -I quality/counters/c2-r85-status-classes.py --repo . --rev 237ecf4e… --controls .ufo/waves/round-85/controls/c2-cases-r85.json --carried .ufo/waves/round-84/controls/c2-runbook-cases-r84.json --scratch-root <scratch>/c2r85` | `mutants=37 killed=33 verdict=TARGET_MISSED rev=237ecf4e… tree=bound`; the four survivors `regex-anchor-dropped`, `line-anchor-prefix`, `negatives-skipped`, `samples-skipped` each `matched=36/36 killed=no`; rc 1 (as declared) |
| C2 selftest at the pre-repair revision | `python3 -I <scratch>/old/c2-r86-at-f72bba01.py --selftest` (file = `git show f72bba01:quality/counters/c2-r86-clause-observations.py`) | `MADO_R86_RUNBOOK_SELFTEST: 114/114`, rc 0 |
| C2 selftest at freeze | `python3 -I quality/counters/c2-r86-clause-observations.py --selftest` | `MADO_R86_RUNBOOK_SELFTEST: 114/114`, rc 0 |

Tools installed or upgraded by this seat: none. Nothing written outside this seat's scratch and this report.

## Mistakes

Each entry: class · evidence · captured by · fix · the check that catches it (and whether that check
was shown able to fail).

**M86-1 — a mutation anchor drifted when the function under it was refactored (instrument authoring).**
- Evidence: `.ufo/waves/round-86/receipts/instrument-repair-r86.md`, run-1 transcript:
  `MADO_R86_RUNBOOK: ERROR (stage=setup mutant regex-anchor-dropped anchor occurs 0 times, not once)`, rc 2.
- Captured by: the counter's own Setup guard (exit 2, no verdict emitted). Confirmed as a setup error, not a score.
- Fix: repair 1 at `237ecf4e` anchors the mutation on the branch body that now exists and uses `re.search`.
- Check that catches it: a pre-freeze dry run of the counter, requiring rc 0 and each mutant anchor
  occurring exactly once. The Setup guard is that check and it fired on run 1 (shown able to fail).
  At freeze the dry run passes (C2 rc 0 above).

**M86-2 — the counter contradicted the population it prints (frozen-predicate implementation).**
- Evidence: `.ufo/waves/round-86/receipts/c2-anchor-only-r86.txt`:
  `MADO_R86_RUNBOOK: … matched=34/37 … clauses_observed=34/37 … declared` with `anchors:1`, while
  `case_correct` required `OBS["anchors"] == 1 + len(samples) + len(negatives)`. The three anchored
  cases (`version`, `omarchy-version`, `border-size-int`) could not pass. Verdict `TARGET_MISSED`.
- Captured by: **the scored run** (`TARGET_MISSED`, `matched=34/37`, `clauses_observed=34/37`).
  The draft's M86-2 says "captured by: none"; that is wrong and is corrected here. What was missed is
  the selftest: the same revision's `--selftest` printed `114/114` (reproduced in this seat, row above),
  because its anchor assertion checks the raw counter `OBS == {anchors:3, samples:1, negatives:1}`,
  not the verdict `case_correct` returns on the declared case.
- Fix: repair 2 at `237ecf4e` snapshots the live call (`LIVE["anchors"]`) and requires `== 1`, the
  declared reading. The full `OBS` counters are unchanged.
- Check that catches it: `case_correct` on each declared anchored control case must equal the declared
  verdict. The scored run performs that check across 37 cases and it returned 34/37 at `f72bba01`
  (shown able to fail). The selftest does **not** perform it; at freeze it still passes 114/114 with
  the same blind spot. **Open:** a selftest that drives a negative refused by the producer-status gate
  through `case_correct` is the missing unit check. Not added here (instruments are frozen).

**M86-3 — two mutations targeted a function on no scoring path (mutation population integrity).**
- Evidence: `.ufo/waves/round-86/receipts/c2-live-observation-r86.txt`: `negatives-skipped matched=37/37
  killed=no`, `samples-skipped matched=37/37 killed=no`, `mutants=37 killed=35`.
- Cause, measured in this seat by AST scan of the `MUTATIONS` anchors (`anchor_two.py`, scratch):
  at `f72bba01` the anchors `for sample in case.get("samples", []):` and
  `for sample in case.get("negatives", []):` occur only in `held_case_correct`
  (output: `samples-skipped anchor found in: ['held_case_correct']`, same for `negatives-skipped`).
  At `237ecf4e` they occur in `case_correct` (output: `['case_correct']`, both).
- Captured by: the kill table of that run (`killed=35`). The Setup guard did not fire, because the
  string occurs once in the file; the defect is which function it is in.
- Fix: `237ecf4e` anchors on `for sample in samples:` / `for sample in negatives:` inside `case_correct`.
- Check that catches it: the anchor-scope check above (every mutant anchor must lie in the function that
  scores, `case_correct`). It returned the held function at `f72bba01` (fails) and the scoring function
  at `237ecf4e` (passes). Shown able to fail. Not wired into the counter; it is a seat-side check.

**M86-4 — the draft's S492 quote is not in the pinned bytes (lesson gate; draft defect, found by this seat).**
- Evidence: `corpus/lessons/round-86.md` Gate row S492 quotes "If the whole *string* matches the regular
  expression *pattern*, return a corresponding Match." It occurs **0** times in
  `.ufo/waves/round-86/fetch/S492.bin`. The bytes read `return a` / `corresponding :class:\`~re.Match\`.`
  across a line break. The draft's word count (14) is also wrong: the verbatim sentence is 13 words.
- Captured by: nothing (no located-quote check ran on the draft).
- Fix for L1: quote the verbatim text (see Gate).
- Check that catches it: a whitespace-normalised substring search of the quote in the pinned file, which
  prints offsets. Shown able to fail: the draft string gives count 0; the corrected string gives count 1.

**M86-5 — the gate omits the byte offsets it was asked for, and miscounts S491 (lesson gate; draft defect).**
- Evidence: the draft gives line numbers only (`line 159`, `line 957`). S491's draft quote is 12 words;
  the verbatim sentence is 11.
- Captured by: nothing.
- Fix: byte offsets in the Gate (see Gate). Check that catches it: the located-quote script of M86-4
  prints start/end offsets and the word count; run before landing.

**M86-6 — receipts cited as committed or as landed are untracked, and one cited receipt does not exist (evidence custody; draft and declaration defect).**
- Evidence: `git ls-files .ufo/waves/round-86/` lists only `claims-declaration-r86.md`,
  `c1-cases-r86.json`, `c2-cases-r86.json`, `S491.bin`, `S492.bin`, `c1-r86.txt`,
  `c2-anchor-only-r86.txt`, `c2-live-observation-r86.txt`, `c2-repaired-r86.txt`,
  `instrument-repair-r86.md`. `git status` shows as untracked (`??`): `control-c1-r86.txt`,
  `control-c2-r86.txt`, `control-held-rule-r86.txt`, `selftest-c1-r86.txt`, `selftest-c2-r86.txt`,
  `census-start-r86.txt`, `census-end-r86.txt`. The declaration says "Do-nothing controls are built and
  committed **before** the candidate measurements"; those control receipts are not committed.
  `receipts/cleanup-r86.json`, cited by the draft's R7 row, **does not exist**
  (`find .ufo/waves/round-86 -name 'cleanup*'` returns nothing).
- Captured by: nothing.
- Fix for L1 at landing: either track the cited receipts or stop citing them as committed; drop the
  `cleanup-r86.json` citation or land the receipt.
- Check that catches it: for every receipt path a lesson cites, `git ls-files --error-unmatch <path>`
  must succeed, and the path must exist.

**M86-7 — the receipts name revisions other than the freeze (round-level; the declared target is `rev=<freeze>`).**
- Evidence: `c1-r86.txt` and the three `c2-*-r86.txt` print `rev=f72bba01…`; `control-held-rule-r86.txt`
  prints `rev=b33afc08…` (post-freeze). `control-held-rule-r86.txt` does not record its argv, so the
  carried-set argument is not reproducible from the receipt.
- Fix: this seat re-ran all three at `237ecf4e` (table above). All three reproduce the declared outcome.
  The C1 counter bytes are identical between `f72bba01` and `237ecf4e` (`git diff --stat` on that path
  is empty); only the C2 counter changed. The `rev` label, not the verdict, was the defect.
- Check that catches it: the counter's printed `rev=` must equal the freeze named in the declaration, and
  each control receipt must record its argv. Not yet mechanical.

**M86-8 — "shipped" overstates the attempt-1 state (draft wording; M86-5).**
- Evidence: `f72bba01` is "preserve in-flight work … (L1 died on provider failure; not a landed round)".
  Its counters were never scored to a verdict and never shipped. Captured by: nothing.
- Fix: say "preserved uncommitted-to-verdict" in M86-5.

### Round-85 routed defects R1–R7: disposition after this seat's checks

| defect | draft disposition | this seat | status |
|---|---|---|---|
| R1 four clause-skipping survivors live on a perfect score | closed for declared population | C2 at freeze 37/37 killed; held r85 at freeze reproduces the four survivors (33/37) | **closed** for the declared population; the selftest blind spot (M86-2) remains |
| R2 cause test is substring membership; all-cause flooding scores full | closed | C1 at freeze: flooding 48/75, held 75/75 | **closed** |
| R3 numeric status cannot authenticate termination cause | open | unchanged; QUALITY 142 | **open** |
| R4 wave telemetry: null seat outputs beside a green wave check | open | QUALITY 145 present at `corpus/QUALITY.md` (`**145.**`); no instrument | **open** |
| R5 append-only LOG correction | retained | not re-checked by this seat | not verified |
| R6 declaration locators off by one | applied | the S491 line 159 and S492 line 957 locators are correct; the S492 quote text is not (M86-4) | **partly applied** |
| R7 L1 probe dirs under shared scratch root | fixed for r86 (cites `cleanup-r86.json`) | the cited receipt is absent (M86-6); `/fast/scratch/hyaku/mado-r86/l1` still exists at this seat's check | **open** until the receipt exists |

## Gate

Two sources, both pinned under `.ufo/waves/round-86/fetch/`. Byte offsets are into the pinned file, from
`python3` `bytes.find` on the file as stored (quotes wrapped across a line break are matched after
whitespace normalisation; the offsets bracket the raw bytes).

**S491 — RFC 7493 (I-JSON) §2.3 Object Constraints** — `https://www.rfc-editor.org/rfc/rfc7493.txt`,
accessed 2026-11-04. Pin `.ufo/waves/round-86/fetch/S491.bin`, 12,849 B, sha256
`a44ccf1451a7bf4f4bbb78b39e10ed0e9a27ff2ee5b639c6458042b5a7197062`.
- Located quote (11 words, lines 159–160): "Objects in I-JSON messages MUST NOT have members with duplicate names."
- Byte offset 6364–6437 (raw bytes span the wrap `duplicate⏎   names.`).
- **ADMIT.** The sentence is a normative MUST NOT for I-JSON messages, which is the specification
  constraint the duplicate-name refusal needs. Scope kept as the row states it: it grounds *refusing* a
  duplicate-name object for an I-JSON-profile surface, not choosing one of the duplicates.

**S492 — CPython v3.14.8 `Doc/library/re.rst`, `fullmatch`** — `https://raw.githubusercontent.com/python/cpython/v3.14.8/Doc/library/re.rst`,
accessed 2026-11-04. Pin `.ufo/waves/round-86/fetch/S492.bin`, 78,262 B, sha256
`d252cc185dfc1014e1b4a8087b2515b71c76527f0f2f6dfddba9a880537e6a48`.
- Located quote (13 words, lines 957–958, under `.. function:: fullmatch` at line 955):
  "If the whole *string* matches the regular expression *pattern*, return a corresponding :class:`~re.Match`."
  (Corrects the draft's "… return a corresponding Match.", which is not in the bytes; see M86-4.)
- Byte offset 39792–39901.
- Judgement: **ADMIT** for the `anchor: line` whole-line rule as `fullmatch` semantics. A second, related
  sentence ("If the whole *string* matches this regular expression", `Pattern.fullmatch`, line 1299–1300,
  byte offset 53427) carries the same point and is not needed as a second citation.

**REJECT — "RFC 8259 alone grounds a duplicate-name refusal as a specification constraint."**
- Evidence: `.ufo/waves/round-84/fetch/rfc8259.txt:322` reads "The names within an object SHOULD be unique."
  (registry row S486). A SHOULD does not ground a refusal on its own.
- Flip: an I-JSON-profile surface, where the SHOULD becomes a MUST — that is what S491 supplies, which is
  why the pair is recorded together.

Registry: `corpus/SOURCES.md` S491 and S492 rows are present (lines 443–444). The draft's
"before 425 / after 427" count holds: `git show a722c604:corpus/SOURCES.md` has 425 `^| S` rows and the
working tree has 427.

## Census

Command (run by this seat, scratch copy of output at `<scratch>/census-run.txt`):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado
echo rc=$?   # → rc=0
```

Exit code **0**. Tail (last 4 lines, verbatim):

```
mado	W04	S490 duplicate url tiswww.case.edu/php/chet/bash/bashref.html across scopes
mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md
```

The output is identical to `.ufo/waves/round-86/receipts/census-end-r86.txt` except that the receipt
appends the line `rc=0`. The standing `W04` duplicate-URL warnings are unchanged: S454–S456, S458, S465,
S466, S470, S475, S477, S481, S490 appear in this run as warnings, not errors. Census status: green
(`ok` on the registry), with the standing warnings recorded.

## Not done by this seat

- No edit to any counter, control set, the declaration, or another seat's report. The selftest blind spot
  (M86-2) and the receipt-custody gaps (M86-6) are findings for L1 to land or route, not fixes here.
- R5 and the "5 of 22 desktop-facing entries" figure in the draft's Domain share section were not re-measured.
