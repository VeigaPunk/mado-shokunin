# ReviewQualityNote — holds

Target: the QUALITY round-19 block at the integrated tip `01b80946d92b26370d3012a7da655d00dd135154` (`git show 01b8094:corpus/QUALITY.md:163-204`). Three attacks: (Q1) are criteria 27/28 distinct discriminators from 6, 7, 9, 13, 16, 24; (Q2) is recording R18-V2 as an application of 24 instead of a new criterion 29 honest; (Q3) does the note's receipt claim (gate-swap-receipt, 383/6, R10) reproduce. All line numbers below are into `git show 01b80946d92b26370d3012a7da655d00dd135154:<path>` unless prefixed otherwise. Lane untouched except this report; scratch under /tmp/rqn19.

## Q1 — 27/28 vs 6, 7, 9, 13, 16, 24 (quotes and verdict: distinct)

Quotes (corpus/QUALITY.md at 01b8094):

- **6** (:12): "Publish each pinned value with a re-derivation command and named revision; any shortened hash must be a true suffix, with corrections preserving old and new values."
- **7** (:13): "Hash committed artifacts from `git show <commit>:<path>`; label work-window hashes provisional and bind them again at the commit."
- **9** (:15): "Bind each audit verdict to a commit or frozen-copy sha; label mid-edit failures in-flight, never as settled defects."
- **13** (:19): "Evidence meant to outlive a round is a committed path or quoted lines plus sha; `/tmp` records provenance only."
- **16** (:22): "Upstream documentation and releases support only dated `[INF-docs]`; never promote them to installed-host or end-to-end facts without independent host measurement."
- **24** (:131): "A sentence that relies on a scan, selftest, measure or replay receipt cites one whose own bytes name its producer (`tool_sha256=` equal to `git show <measured_commit>:<tool> | sha256sum`, read with the producer status checked) and its `measured_commit`; a claimed re-cut is a committed receipt with those fields, never a narrated rerun; a report labels every tool sha with the revision it belongs to"
- **27** (:174): "A credited source row's anchor is reproducible — tag- or commit-pinned bytes with their sha256, a content-addressed object id, or a registry checksum; a digest that committed receipts show rotating between fetches never anchors a row, and an unversioned alias (`latest`, `main`, `master`, `HEAD`) never serves as version-specific support without a pin in the anchor; the superseding row names the replaced id"
- **28** (:183): "When a present-tense value is superseded, every owned file that still states the old value carries, in the same round, an in-file pointer naming the new value and the SOURCES row that superseded it; a SKILL erratum or one note does not discharge the sweep for the other files"

Pairwise verdicts:

- **27 vs 7/13** — the note's own argument (QUALITY:165-167: "criteria 7 and 13 bind a digest to committed bytes, and a committed digest of a rotating GitHub tree page satisfies both; 27 asks whether the upstream an anchor names can be re-obtained to the same bytes") checks out against the mined row: S094 held committed per-fetch HTML digests of the walker GitHub tree page — satisfying 7 (hash committed bytes) and 13 (committed path + sha) — while committed receipts show the URL returning multiple distinct 200 digests (lesson round-19.md M1 row: 5 receipts / 5 distinct digests; w1 sweep 7 and 6 across seats). Committed-bytes binding and re-obtainability are genuinely different discriminators; 27's rotation and alias clauses exist in neither 7 nor 13.
- **27 vs 6** — 6 regulates how the lane publishes its own pinned values (re-derivation command, named revision, true-suffix hashes); 27 regulates the form of the upstream anchor a credited SOURCES row rests on. Different objects; distinct.
- **27 vs 9** — 9 binds audit verdicts to a commit/sha; 27 binds source-row anchors. Distinct objects. The note never argues this pair (caveat below).
- **27 vs 16** — 16 is a claim-tier rule (upstream docs stay dated `[INF-docs]`, never promoted to installed-host facts); 27 is an anchor-form rule. S084 shows the separation: per lesson M2, "The page bytes did reproduce … so the content was right; the alias moves on the next xdg release" — no false promotion (16 clean), pure anchor defect (27). Distinct.
- **27 vs 24** — 24 is receipt producer identity; 27 is source-anchor reproducibility. Distinct.
- **28 vs 6/9** — note :168-169 ("Criterion 6 asks for a named revision; 28 is a property of the owned file set after a supersession, which passes 6 and 9 untouched"). Verified shape: round-18's state had the 2.17.2 value published with named revision (6 ok) and a SKILL erratum (9-adjacent record) while 11 of 13 owned files were stale (fresh-pins-before.txt 2/13) — 28 fails where 6 and 9 pass. Distinct.
- **28 vs 7/13/16/24** — none of these requires a pointer sweep; committed stale bytes satisfy 13, correctly-tiered stale claims satisfy 16, receiptless prose satisfies 24's scope only when verdict-bearing. Distinct.

Caveats (not falsehoods):

- (a) The block's "Not restatements" paragraph (:165-171) argues only 7/13→27, 6→28, 9→28. It never mentions **16 or 24** for either new criterion. The distinctness holds on inspection (above), but the recorded argument is incomplete relative to the full neighbor set.
- (b) Nearest unexamined neighbor is criterion **17** (:34): "… append a genuine superseding row with a resolvable prior id" vs 27's final clause "the superseding row names the replaced id". Same requirement, different trigger (17: URL-collision merge review; 27: anchor supersession). A partial overlap worth an erratum sentence; not a restatement of 27's core.

## Q2 — R18-V2 as an application of 24, not criterion 29 (verdict: honest)

- **24's letter covers both facets of R18-V2.** Facet 1: criterion 26's red-before `.ufo/waves/round-18/evidence/gate-rc-redbefore.txt` carries no producer header — verified: `grep -c 'tool_sha256|measured_commit'` on the committed bytes = **0**; digests exist only as prose (:8 committed d9a5a18 gate `fba82a66…`, :10 an uncommitted edited gate `2bdf5e8a…`). That is exactly 24's "a sentence that relies on a … receipt cites one whose own bytes name its producer". Facet 2: the re-cut existed only as narrated prose (w3 report "383/389") — exactly 24's "a claimed re-cut is a committed receipt with those fields, never a narrated rerun".
- **The framing pre-dates the target it misses.** The baseline lesson (lessons/round-18-verifier-spotcheck.md:118, committed at `9c54c56`, before the round-19 pre-registration at `17661e0` set "target ≥ 21/29") itself directs: "Commit a header-bound receipt (`tool_sha256`, `measured_commit`) of the swapped-block run, **so QUALITY 24 holds** for criterion 26's own evidence." "Application of 24" is the lesson's own framing, not a post-hoc dodge; the decision is also attributed (QUALITY:169-171 "outside critic CriticC1, round-19 w1") and recorded in lesson M4: "Applied, not re-numbered (CriticC1: a criterion 29 would restate 24)".
- **Anti-duplication is standing lane discipline**, not an invention of this round: the round-14/15 rulings in QUALITY ("No duplicate provenance criterion or generic wrapper is introduced"; "no generic execution wrapper or duplicate provenance criterion is introduced") and 24's own preamble (:127-129: round-14/15 rulings "stand for input binding and commit binding … Criterion 24 adds only what those leave open").
- **The miss is recorded, not hidden.** Independent rerun of the C1 counter (instrument identity checked first: `sha256sum .ufo/waves/round-17/measure.py` = `de4c422b55c67f822cb9f0be21fe5e879e3d15c46830565c1c661381817cfcdc`, equal to the pre-registered/measure-before receipt value):
  - `python3 .ufo/waves/round-17/measure.py 01b80946d92b26370d3012a7da655d00dd135154` → `c1 = {criteria: 28, lesson_cited: 20, score: 7.1429}`
  - `python3 .ufo/waves/round-17/measure.py 9c54c56a6a7528675027b7f628f97a1b8d1b8e8d` → `c1 = {criteria: 26, lesson_cited: 18, score: 6.9231}`
  20/28 < the declared ≥21/29 (SCORECARD:1098). No criterion 29 exists at the tip (28 is the last numbered criterion; the R18-V2 note at :192-204 is unnumbered, as declared).
- **No buried new discriminator.** R18-V2's own fix item is literally "make 24 hold"; the only new fact round 19 adds (the R10 omission) is a count-labeling matter in 10/23 territory, disclosed rather than criterion-ized.

Caveat (wording precision): "round 18's '383/389, five OM9' omitted R10" (QUALITY:200-201) is true of the quoted phrase — SCORECARD.md:1043-1044 at `9c54c56` (unchanged at tip): "Criterion 26's reproducible red is the d9a5a18 block swapped into the landed gate (383/389, five OM9 failures; w3 report `W3CriticC1Final.md`)" — and of the spotcheck lesson :49 ("the w3 swap result 383/389"). But the w3 report the phrase cites **did print R10**: W3CriticC1Final.md:187-195 lists "- R10 (pin drift, expected)" plus the five OM9 lines (and its own arithmetic `383 + 5 ≠ 389` was internally inconsistent). The omission is at summary level; a reader could over-generalize the note's sentence to "round 18 never observed R10", which is false. Precision erratum candidate, not dishonesty.

## Q3 — Receipt claim reproduction (verdict: reproduces fully)

Claimed: `.ufo/waves/round-19/evidence/gate-swap-receipt.txt` with `tool_sha256=6e6782c3…` = committed fixture `gate-swap-d9a5a18.sh`, `measured_commit=df84807`, `383 passed, 6 failed` = five OM9 + R10, and that round 18's phrase omitted R10.

1. **Header vs criterion 24's formula.** Receipt :1: `RECEIPT tool=.ufo/waves/round-19/evidence/gate-swap-d9a5a18.sh tool_sha256=6e6782c30de4b1a2a308e73ede3a1a36eb4b1a6ba6fdd81e69b5cbc84202ac6e measured_commit=df84807d8fc49f5d8fb4ec3060859e5b1992084c utc=2026-10-20T17:41:13Z cmd=bash .ufo/waves/round-19/gate-swap.sh df84807…`. Verified `git show df84807:<fixture> | sha256sum` = `6e6782c3…` and identical at the tip. `df84807` is an ancestor of the tip (`git merge-base --is-ancestor` ok); committed 2026-10-20 14:40:39 -0300 = 17:40:39Z, receipt utc 17:41:13Z — 34 s later, consistent.
2. **Independent byte rebuild.** Base block `17661e0:tools/mado-verify.sh` lines 3467-3489 → sha256 `c86f51b8…` (= receipt :2); old block `d9a5a18:` lines 3402-3415 → `414bf6ed…` (= receipt :2). Rebuilding the landed gate with that one block exchanged yields **182300 bytes** (= receipt :2 `fixture_bytes=182300`) with sha256 `6e6782c3…` — byte-exact equal to the committed fixture. The receipt's provenance chain is reproducible from named revisions alone.
3. **Execution rerun.** Committed fixture copied to /tmp/rqn19/fixture.sh; `bash fixture.sh --selftest` (the gate's hermetic mode; scratch under /tmp/w5-mado-m52-*, no substrate read) → exit 2, `MADO_SELFTEST: FAILED — 383 passed, 6 failed`, and `diff` of receipt lines 3-9 against my run lines 1-7 is **empty** — the FAILED line and all six failure rows are byte-identical, including R10's `got '88286b3dfa…' want '20714096e1…'` and the five OM9 rows.
4. **R10 identification.** The note's gloss "(the fixture's own `PIN_MADO` self-pin moves with any gate edit)" matches the fixture bytes: :583 `st_eq "R10: derived target equals the recorded gate revision" "$PIN_MADO" "$dsha"` and the comment at :1618-1619 ("selftest() asserts the derived target equals PIN_MADO on pristine runs, so a stale pin is visible"). R10 is a self-pin, not a second behavioural defect.
5. **Checker arm.** `python3 -I .ufo/waves/round-18/receipt-check.py .ufo/waves/round-19/receipt-claims.json` prints `RECEIPT r19-c26-redbefore-headerless MISSING_PROVENANCE` and `RECEIPT r19-c26-regression-recut-headerless MISSING_PROVENANCE` — exactly the note's claim (QUALITY:192-195).

## Residual findings (adjacent to the note; none falsifies its sentences)

- **R1.** The same checker run ends `EXPECT_SUMMARY: 3/5`, exit 2: `r19-tw-recall-before` and `r19-fresh-pins-before` read **ERROR** because the committed `receipt-check.py` does not understand the `tool_rev` key (unchanged since `be886a3`; `git diff 9c54c56..01b8094 -- .ufo/waves/round-18/receipt-check.py` is empty). receipt-claims.json:15 discloses this accurately ("The unmodified round-18 checker ignores this key and returns ERROR …"), and the "three-hunk change" it points to exists only as a proposal in w1 `ReceiptClaims19.md` — never landed.
- **R2.** Lesson M5 re-cut both before-receipts as `tw-recall-before-recut.txt` / `fresh-pins-before-recut.txt` with `measured_commit=df84807` (committed; headers verified — producer bound to the commit that carries it, data rev in argv). These shapes would credit under the *unmodified* checker, but the committed receipt-claims.json still points at the originals with the unlanded `tool_rev` key; the only committed reference to the recuts is the dispatch generator `gen_w2.py`. No committed claims file exercises the recut shape.
- **R3.** `gate-swap-receipt.txt` itself has no claim row in receipt-claims.json, so its `ok` status is never checker-verified anywhere committed. Criterion 24's letter does not require enrollment (I verified the formula manually, Q3.1), but the note's instrumentation demonstrates only the red arm.
- **R4.** The "omitted R10" wording nuance (Q2 caveat): the w3 report printed R10; only the SCORECARD/lesson summaries omitted it.
- **R5.** Distinctness-argument gaps: 16 and 24 never addressed for 27/28 (Q1 caveat (a)); 27's supersession clause near-overlaps 17's "resolvable prior id" (Q1 caveat (b)).

## Limits

- Read committed bytes at `01b8094`; the worktree equals it per assignment (cited files spot-checked sha-equal, e.g. measure.py `de4c422b…`, fixture `6e6782c3…` at both revisions).
- `measure.py REV` as literally written in SCORECARD fails (`fatal: Needed a single revision` — the script does `git rev-parse --verify REV^{commit}`); I substituted the explicit commit ids. [INFERENCE] `REV` is a runner-substituted placeholder; the committed before-receipts show resolved shas in their `cmd=` fields.
- Did not run `anchor-durability.py` / `supersede-sweep.py` red/green arms or the round-18 claims file (other seats' items); did not rerun `gate-swap.sh` itself (my reproduction rebuilt and ran the fixture directly, which is the stronger path).
- Fixture rerun was a /tmp copy in `--selftest` mode only, per the gate-run rule; no live gate, no lane writes, no fetches, no VCS writes.

## Installs

None.
