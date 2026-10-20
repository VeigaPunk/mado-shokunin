# ConnLessonChain — R17-V1..V5 → round-18 M1–M4 → QUALITY 24–26 → checks

Seat: `MadoR18.ConnLessonChain` (connector, read-only). Lane `mado-shokunin`,
baseline `d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`, pre-registration
`d3a000003e6ef0b1e3c7b4faf52d592eb293857ba` (current lane HEAD and
`refs/heads/master`). No lane VCS write, no lane gate, no host surface
operation, no tool install. Every hash below is a `git show` read; the only
executable runs were `receipt-check.py` and `pipe-rc-census.py` (both print
only) and an adapted copy of `receipt-check.py` against a disposable
`/tmp` clone.

## 1. The chain, with exact anchors

| outside finding | defect (anchor) | round-18 lesson row | criterion | dispatched check | fix artifact | disposition |
|---|---|---|---|---|---|---|
| R17-V1 | real-transcript tripwire receipts carry no tool sha256/`measured_commit`; `lessons/round-17.md:175-176` claims a re-cut under `962919ce…` that git never recorded (`corpus/lessons/round-17-verifier-spotcheck.md:183-190`) | M1 (`LessonDraft.md:9`) | 24, clause 1 | `receipt-check.py` + `receipt-claims.json` | `recut-receipts.sh` → `evidence/tripwire-*.txt`; `ErratumR17.md` (a) | fix **and** criterion |
| R17-V2 | round-17 before→after C3 row cites `7a98720e…` (the `f71ccbe` tool); landed tip tool is `962919ce…` (`spotcheck:193-196`) | M1 (same row) | 24, clause 3 | none dedicated (see F7) | `ErratumR17.md` (b) report carry-over | fix **and** criterion |
| R17-V5 | rubric-V tightenings shown to bite only in a seat `/tmp` lab; no committed mutant receipt (`spotcheck:206-208`; source `lessons/round-17.md:156-158`) | M2 (`LessonDraft.md:10`) | 25 | `measure-mutants.py` → `evidence/measure-mutants.json` | same | fix **and** criterion |
| JjAuditMado F10 | `tools/mado-verify.sh:3406` pipes `git show` into `sha256sum` without the producer rc, so a failed read becomes `e3b0c442…` and a false "local edit" FAIL; the UNKNOWN arm at `:3408` is dead (`JjAuditMado.md:235-250`, `:350`) | M3 (`LessonDraft.md:11`) | 26 | `pipe-rc-census.py` + gate OM scenario (`GateRcFix`) | `tools/mado-verify.sh` rc capture | fix **and** criterion |
| R17-V3 | rubric-V counter cannot tell a fetched row from an invented row (`spotcheck:197-200`) | M4 (`LessonDraft.md:12`) | **none** | `fetch-verify.py` (M4 fix) | C2 fetch receipts + `FetchBackfillR17` | **fix only** (C2) |
| R17-V4 | tripwire is a probe with no frozen input snapshot (`spotcheck:201-204`) | none | **none** | `--frozen` selftest + provenance check | C3 frozen replay | **fix only** (C3) |

This partition matches the pre-registered C1 text (`SCORECARD.md` tail,
round-18): V1/V2, V5 and F10 go to lessons **and** criteria; V3 is C2; V4 is
C3. M4 is an extra lesson row beyond C1's named set but no criterion cites
it, so it does not touch the c1 count. V4 has no lesson row for the same
reason: the round-17 lesson already names the frozen snapshot as round-18
plan item 1, and C3 is the fix.

## 2. Citation audit — right lesson, right outside finding?

| criterion | lesson citation | verdict | outside citation | verdict |
|---|---|---|---|---|
| 24 | `lessons/round-18.md#mistakes M1` | **correct**: M1 is drafted to cover V1 **and** V2 (V1 class `attribution`, V2 class `reference-drift`) | `lessons/round-17-verifier-spotcheck.md R17-V1/V2` | **correct and complete**: the criterion's third clause is R17-V2, so `V1` alone would drop it; the landed draft already writes `V1/V2` |
| 25 | `lessons/round-18.md#mistakes M2` | **correct**: M2 is the V5 lab-only-bite row | `…spotcheck.md R17-V5` | **correct** |
| 26 | `lessons/round-18.md#mistakes M3` | **correct**: M3 is the F10 row | `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMado.md F10` | **correct file and id**; it is outside the lane, so the absolute path is unambiguous but not portable. Nothing in the spotcheck contains F10 — using the spotcheck here would be a mis-citation, and the draft does not. |

Anchor forms are consistent with the existing bar: criteria 6–23 use
`lessons/<file>.md#mistakes M<n>`, and round-17's lesson has a `## Mistakes`
heading, so `#mistakes` resolves. `lessons/round-18.md` does not exist yet;
L1's integration supplies it. M1–M4 ids are marked provisional in the draft;
the criteria must be landed only after the lesson row ids are fixed.

**Mechanical count (simulated append, no lane write).** Appending the
draft's body to `corpus/QUALITY.md` as it stands gives:

```
criteria 26 cited 18 score 6.9231
```

i.e. 18/26, every new criterion carrying `lessons/` on its own numbered line,
no extra `^[0-9]+\. ` line introduced. That is the pre-registered target, and
it is reachable exactly as drafted. Two style conditions matter and hold:
the criterion's numbered line must be the **same physical line** as the
citation (measure.py's literal rule), and no numbered list may be added in
the round-18 section. Criteria 24–26 are single physical lines like 23.

**One wording risk inside criterion 24.** "a scan, **selftest or measure**
receipt" overreaches the artifacts: `measure.py` output (`measure-before.json`
/ a future `measure-final.json`) carries `rev`/`commit`, not `tool_sha256`,
so a measure receipt cannot satisfy the criterion as written, and
`receipt-check.py` accepts only `tool_sha256` (not `SCRIPT_SHA256`, and the
real key is `SELFTEST_SCRIPT_SHA256`). Either scope the criterion to
scan/selftest receipts (measure receipts are already bound by criteria 6/7/22)
or make the instrument emit its own sha. As written, a closure can show a
measure receipt that the criterion demands be rejected but that no round-18
artifact satisfies.

## 3. Which R17-V* need a fix rather than a criterion

- **R17-V3 → fix only (C2).** The instrument cannot see an invented row;
  the remedy is procedural (raw fetch receipt per credited row) plus
  `fetch-verify.py`. A criterion saying "credited rows have committed fetch
  receipts" would be a fourth new criterion, changing the pre-registered
  denominator (19/27) and numbering; C2's counting rule already carries it.
  M4 records the limit without a criterion. This is the correct partition.
- **R17-V4 → fix only (C3).** A probe with no pinned snapshot is a capability
  gap, not a recurring textual rule. C3 supplies `--frozen` plus the snapshot
  and provenance check. No criterion, no lesson row; the round-17 lesson's C3
  section already names the plan.
- **R17-V1/V2/V5/F10 → fix + criterion.** Each has a real committed-receipt
  artifact (recut, mutant JSON, gate scenario) *and* a reusable rule. That is
  the only set C1 names for criteria, and the criteria numbers line up
  one-to-one with M1/M2/M3.

## 4. What I verified as fact

1. **R17-V1 is real at baseline.** All six receipts named by the finding
   (`tripwire-r13..r16.txt`, `tripwire-anchor-r15.txt`,
   `tripwire-pacmanlog-join.txt`) last changed at `f71ccbe` (12:09:20) and at
   `988b858` (11:50:30); `git diff f71ccbe 0ab1ccc -- .ufo/waves/round-17/evidence/`
   touches none of them. None contains `tool_sha256`, `measured_commit`, or a
   `RECEIPT` header (grep over the six = 0). Tool shas by revision:
   `988b858 4ced68d3…`, `f71ccbe 7a98720e…`, `0ab1ccc` and `d9a5a18
   962919ce…`.
2. **R17-V2 wording is a staleness defect, not a fabricated tool claim.**
   The round-17 report's table column is labelled `After @ f71ccbe
   (= content of 6046ab7)` (`.ufo/reports/round-17/mado.md:73-78`), so
   `7a98720e…` is labelled with `f71ccbe`; the tip tool `962919ce…` appears
   at report line 3 and in the lesson, but the after row is not re-measured at
   `0ab1ccc`. `LessonDraft.md:9` says the report cites `7a98720e…` "as the
   landed tool" — an overstatement; the precise defect is "after-state
   measured at a superseded revision, tip sha not in the row". Fix the
   LessonDraft phrase before landing so the M1 evidence pointer does not
   itself drift from the source.
3. **Instrument shas in the check items are correct.** `f52f43f` measure.py =
   `a280b3ab…`, `ab0bc9b` = `4023124f…`, `d9a5a18` = `de4c422b…`; the
   `MeasureMutants` item's loose/tight pins match.
4. **`measure-mutants.json` schema** (`mado-measure-mutants-v1`) records
   `instruments.loose/tight.{rev,sha256}`, `baseline_rev`, and six mutants
   with `diff_sha256`, `mutant_commit`, `baseline`, `mutant`, `bites`;
   summary `{"mutants":6,"bites":6,"no_bite":[],"unexpected_tight_only":[],"baselines_agree":true}`.
5. **`pipe-rc-census.py d9a5a18`** exits 1 with
   `SUMMARY … files=1 sites=12 checked=3 unchecked=9` and `VERDICT RED`;
   the nine unchecked sites are `640, 942, 944, 962, 1377, 2788, 3406, 3444,
   3474`, and `:3406` is the F10 site. `:2780`, `:3336`, `:3407` are
   `checked` under the precondition-guard rule.
6. **`receipt-check.py` current run** (read-only, lane claims):
   six `MISSING_PROVENANCE` (the R17-V1 receipts at `d9a5a18`), fixture ok,
   fixture `SHA_MISMATCH`, stale-rev fixture `SHA_MISMATCH`, six
   `PENDING`, `EXPECT_SUMMARY: 9/15`, exit 2.

## 5. Defects in the landed chain artifacts (must be reconciled before 24–26 land)

These are grounded in the files as they stand; all are in round-18 seats'
artifacts, none is a lane-gate result.

**F1 — the criterion-24 checker cannot parse the receipt format the R17-V1
fix is required to write.** `recut-receipts.sh` writes line 1 as
`RECEIPT tool=… tool_sha256=<hex> measured_commit=<REV> utc=… cmd=…`
(script line 179). `receipt-check.py` matches
`^\s*tool_sha256\s*[=:]` and `^\s*measured_commit\s*[=:]` (line-anchored), so
the shared header line yields neither. Direct check of the regexes against
the mandated line: `sha match: False rev match: False`. Consequence: when L1
fills the `PENDING-L1` revs, the six re-cut receipts will report
`MISSING_PROVENANCE` and the check exits 1 — the criterion's own green
control fails on the fix. The checker's docstring already promises "on a
RECEIPT header line (regex over every line)"; the implementation contradicts
it.

**F2 — the checker does not bind `measured_commit` to the revision the claim
asserts, so the exact R17-V1/V2 defect passes.** `evaluate()` resolves
`tool_sha256` against `sha256(git show measured_commit:tool)` and never
compares `measured_commit` with `rev`. Reproduced in a disposable clone:

```
rev read at: 2a9d6fad…   (tool at that rev = 962919ce…)
receipt: measured_commit=f71ccbe…, tool_sha256=7a98720e…
RECEIPT stale-consistent-read-at-later-rev ok
EXPECT_SUMMARY: 1/2
```

A receipt that attests the **old** tool, left unchanged across a tool edit,
reads `ok` at the later revision. That is precisely "the re-cut git never
recorded": internally consistent, not re-cut. The current `stale-rev` fixture
does not catch it because the fixture's tool sha is the new one (cross-binding
error), not because the revision lagged.

**F3 — claim paths do not match the re-cut outputs.** Claims point at
`.ufo/waves/round-18/evidence/tripwire-r13-recut.txt` … `-r16-recut.txt`,
`tripwire-anchor-r15-recut.txt`, `tripwire-pacmanlog-join-recut.txt`;
`recut-receipts.sh` writes `tripwire-r13.txt` … `tripwire-r16.txt`,
`tripwire-anchor-r15.txt`, `tripwire-pacmanlog-join.txt`. After the revs are
filled the checker will return `ERROR` (unreadable receipt) and exit 2. The
join receipt also puts its provenance on a comment line
(`# receipt: tool_sha256=… measured_commit=…`), which F1's anchored regex
would not parse even at the right path.

**F4 — criterion 24's runnable-check paragraph cites artifacts and outputs
that do not exist.** The draft names
`.ufo/waves/round-18/checks/receipt-check.py` (real path:
`.ufo/waves/round-18/receipt-check.py`, no `checks/` dir), claims it prints
`RECEIPT_SUMMARY: 0/4` on the four files `tripwire-r13.txt`,
`tripwire-selftest-core.txt`, `label-check-final.txt`,
`frozen-tampered-recut.json`, and exits 1. The real check prints
`RECEIPT <id> <status>` + `EXPECT_SUMMARY: 9/15`,
runs over six round-17 receipts (including the join), and exits 2 because of
the `PENDING` placeholders. This is the same reference-drift/number-drift
class the round is closing; it must not land inside the closing criteria.

**F5 — criterion 25's check is described against a schema that does not
exist.** The draft names `checks/mutant-check.py RECEIPT.json`, "six keys",
`loose_output`/`tight_output`, "two 64-hex instrument shas", and a 40-hex
`measured_commit`. The landed `measure-mutants.py` takes
`--lane/--out/--keep/--workdir` (no receipt argument, no verify mode) and
writes the JSON described in §4.4 (`baseline_rev`, `instruments.*.sha256`,
per-mutant `baseline`/`mutant`/`bites`). The criterion text must be rewritten
to those names and fields, or a validator must be added; as drafted it cites
a script and keys that do not exist.

**F6 — criterion 26's check names, invocation and site list are wrong.** The
draft names `checks/pipe-rc-lint.py tools/*.sh` and `PIPE_RC_FLAGS: 9` with
lines `244, 942, 944, 1133, 1377, 1383, 2788, 3406, 3474`. The real
`pipe-rc-census.py` takes `[--repo DIR] REV`, prints `SITE …`,
`SUMMARY … sites=12 checked=3 unchecked=9`, `VERDICT RED`. The actual
unchecked lines are `640, 942, 944, 962, 1377, 2788, 3406, 3444, 3474`:
`244`, `1133` and `1383` are not sites at all (not assignments), and
`640`, `962`, `3444` are missing from the draft. The count 9 coincides by
accident. The draft's `pipe-rc-fixture.sh guarded/unguarded` control is also
not the dispatched control (the dispatched runtime control is the gate's OM
scenario). Replace with the committed census output and the OM scenario.

**F7 — criterion 24's third clause (report sha label, R17-V2) has no failing
control.** `receipt-check.py` validates receipts, not report sentences;
`recut-receipts.sh` validates the receipts' own headers; the erratum is prose.
C1 promises "each with a runnable check shown able to fail", so this clause
needs either a claim kind (`report`, `rev`, `cited_sha256`, `tool`) or a
narrowed criterion. The round-17 label-check precedent shows the shape
(label-check-final.txt's `superseded-commit-mutant` line already tests a
`measured_commit` label), but it is not wired to report text.

**F8 — erratum draft window ambiguity.** `ErratumR17.md` (a) says "Under
`962919ce…` exactly one real-transcript receipt changed: `tripwire-r17.txt`"
and then "Counts were not identical across that re-measure… r15 aggregate
`live_probe` moved 28 → 29". Those statements are about different windows:
`git diff f71ccbe 0ab1ccc` touches `tripwire-r17.txt` and the selftest/oracle
files, not `r13..r16`/anchor/join; the per-file moves belong to
`988b858 → f71ccbe`. Name the window per sentence or the erratum repeats the
class it corrects.

**F9 — criterion 25 demands `measured_commit`; the landed mutant receipt
records `baseline_rev`.** Either rename/add the key in the receipt or change the criterion to
"baseline revision".

## 6. Proposed move (one, bounded)

**Bind criterion 24's check to the revision the claim asserts, not only to
the revision the receipt names.**

Mechanically, in `receipt-check.py`:

1. Parse the shared header inline: `\btool_sha256\s*[=:]` and
   `\bmeasured_commit\s*[=:]` anywhere on a line beginning `RECEIPT `
   (keep the existing line-anchored and JSON forms for other receipts).
2. For a claim whose `rev` is a commit, require
   (a) `git merge-base --is-ancestor <measured_commit> <rev>`, and
   (b) `sha256(git show <rev>:<tool>) == sha256(git show
   <measured_commit>:<tool>) == tool_sha256`;
   for a claim that declares `supersedes`, also require the receipt bytes to
   differ from the superseded receipt (a copied file is not a re-cut).
3. *(companion, smaller)* add a `report` claim kind for R17-V2:
   `{report, rev, cited_sha256, tool}` asserts the cited sha equals
   `sha256(git show rev:tool)` or that the same sentence labels an earlier
   revision.

Why this and not the obvious fix: relaxing the regex alone makes the re-cut
receipts parse but still prints `ok` for a receipt that attests a superseded
tool at the current revision — the demonstrated F2 case, i.e. exactly the
unreceipted re-cut R17-V1 names. The ancestry + tool-equality clause is what
makes the check fail on the real defect while staying green on the honest
re-cut (whose receipt is committed *after* `measured_commit`, so
`rev == measured_commit` would be wrong).

**Axes.** Calibration improves (criterion 24 becomes a real check for V1/V2);
operability is harm-watched (no behaviour change to the gate or tripwire);
coverage and freshness are untouched. **Risks.** `WORKTREE` fixtures must be
exempt from the ancestry clause; a re-cut receipt is necessarily committed
after `measured_commit`, so equality must not be required; report-sha claims
need a stable substring, not a line number; a tool edit between measurement
and commit is already refused by `recut-receipts.sh`'s second `sha256sum`.
**Verification.** Red: the six round-17 receipts still print
`MISSING_PROVENANCE`; a `/tmp` clone receipt attesting `f71ccbe` read at a
later rev where the tool changed must print a lag/mismatch status, not `ok`;
green: the round-18 re-cut receipts at the commit that contains them, plus
the two authored fixtures; `EXPECT_SUMMARY` returns to `15/15` and exit 0
only after the six `PENDING` revs are filled.

## 7. Reconciliation checklist for L1 (before criteria 24–26 are committed)

1. Fix `receipt-check.py` per §6 (or rewrite criterion 24's check paragraph
   to a check that exists and bites).
2. Point the six recut claims at `recut-receipts.sh`'s actual paths, fill the
   revs, and re-run; expect 15/15 exit 0 only after the re-cut lands.
3. Replace criteria 24–26's "Runnable check" paragraphs with the committed
   artifacts' paths, invocation and exact output tokens (`EXPECT_SUMMARY`,
   `SITE`/`SUMMARY`/`VERDICT`, `measure-mutants.json` fields).
4. Fix M1's "as the landed tool" phrasing to the staleness wording; fix the
   erratum's re-cut-window ambiguity.
5. Keep the three numbered lines single-line with the citation on the same
   physical line; the measured append is 18/26 = 6.9231.
6. Decide the V2 clause: add the report-sha claim kind or drop the clause
   from criterion 24 (C1 would then have only two unchecked clauses, but the
   outside citation `R17-V1/V2` would become over-broad).

## 8. Limits

- I did not run `tools/mado-verify.sh`, `measure.py`, `mado-tripwire.py`,
  or any host surface command; no package query, no git/jj write in the lane.
- `receipt-check.py` and `pipe-rc-census.py` were read and executed only as
  new round-18 check scripts; the stale-consistent demonstration used a
  disposable `/tmp` clone (`git clone` → one commit) and an adapted copy of
  the checker with `LANE` pointed at that clone. No lane byte was written
  except this report.
- `measure-mutants.py` was not executed (it writes `evidence/measure-mutants.json`);
  its schema was read from the committed JSON as it stood at 12:45.
- The round-18 lesson file and the integrated `QUALITY.md` do not exist yet;
  counts above are simulated against the landed drafts, not measured at an
  integration commit. `[INFERENCE]` wherever a final criterion wording is
  predicted from the draft rather than read from a committed `QUALITY.md`.

## 9. Report

`Report: .ufo/waves/round-18/w1/reports/ConnLessonChain.md`
