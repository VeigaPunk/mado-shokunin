# RevPreReg18 — round-18 pre-registration review

Reviewer: MadoR18.RevPreReg18 (leaf reviewer, no subagents).
Date: 2026-10-20.
Target: `SCORECARD.md:931-984`, "Round 18 — declared claims", at
`d3a00003e6ef0b1e3c7b4faf52d592eb293857ba` (baseline
`d9a5a18e17cd3a68b52148fcc01c4a30e340ba98`). Outside input:
`corpus/lessons/round-17-verifier-spotcheck.md` §6,
`.ufo/waves/hyaku/jj-w1/reports/JjAuditMado.md`.
Method: read-only. I ran the existing revision-bound counters and hermetic
suites, plus two isolated `/tmp` git repos for the vacuity tests. No lane
file was written except this report; no host/package/compositor/service
operation; no tool install. The `/tmp` repos were built from
`git -C <lane> archive d9a5a18` and are disposable.

## 1. Verdict

**The three axes are distinct, the numeric/categorical shells are
falsifiable, and the claims are separable at the score level. The
substantive parts of C1 and C2 are not falsifiable by the declared
counting command: both can pass vacuously, and I reproduced both. C3's
core frozen replay is the right shape, but its gate-registration and
selftest acceptance are under-specified, and its specified receipt does
not name the measured revision.**

**Calibration is the lowest active score under the lane's recorded
literal rule (15/23 = 6.5217 vs rubric V 4/6 = 6.6667). It is not the
lowest under the semantic block counter that QUALITY 22 also requires to
be reported (18/23 = 7.8261 > V 6.6667). The pre-registration reports
only the literal counter and does not re-derive the freshness,
operability, navigation or exact-set rows, so its QUALITY 22 citation is
only partly satisfied. The selection is nonetheless correct under the
recorded literal rule, and the round works both C1 and C2, so the
lowest-axis obligation is met under either reading.**

The C1 facts are accurate: the six real-transcript receipts carry no
tool sha or `measured_commit`; the six were last changed at `f71ccbe`
(not `0ab1ccc`), and `git diff f71ccbe 0ab1ccc -- .ufo/waves/round-17/evidence/`
does not touch them; `lessons/round-17.md:175-176` claims a re-cut under
`962919ce…` that git never recorded; the round-17 report line 76 cites
`7a98720e…` (the `f71ccbe` tool) while line 3 cites `962919ce…`;
`lessons/round-17.md:156-158` records the `/tmp`-only instrument
tightenings; `tools/mado-verify.sh:3406-3408` is the unreachable-guard
pipe digest described by JjAuditMado F10. The defect description is
sound.

## 2. Axis re-derivation (QUALITY 22)

Run at `d9a5a18`. All rows are active/non-retired as of the pre-reg.

| Row (recorded rule) | Counting command run | Observed | 0–10 |
|---|---|---|---|
| calibration / literal lesson citation (`^[0-9]+\. .*lessons/` over `^[0-9]+\. `) | `python3 .ufo/waves/round-17/measure.py d9a5a18` (`c1`) | 15/23 | **6.5217** |
| calibration / semantic block citation (QUALITY 22 report-both rule) | own block parse of `git show d9a5a18:corpus/QUALITY.md`; blocks 18–20 cite `lessons/` on continuation lines | 18/23 | **7.8261** |
| coverage / rubric V P1–P6 | same `measure.py` (`c2`) | 4/6: P1, P2, P4, P6; P3/P5 open; `rejected: []` | **6.6667** |
| coverage / U1–U7 sourced routes | `python3 .ufo/waves/round-16/measure.py d9a5a18` | 7/7, U6 facets true | 10.0000 |
| coverage / admitted-note navigation | SCORECARD fleet-r1 Counting block with `REV=d9a5a18` | 32/32, missing/extra/dup empty, exit 0 | 10.0000 |
| freshness / file-plane agreement | `bash tools/mado-verify.sh --no-live` | 29 PASS, 0 FAIL, 0 UNKNOWN, 8 SKIP, 4 NOTE, exit 0 | 10.0000 |
| operability / hermetic suite | `bash tools/mado-verify.sh --selftest` | 372/372, exit 0 | 10.0000 |
| operability / exact-set four cases (r13) | `python3 .ufo/waves/round-13/measure.py d9a5a18` | 4/4 cases `named_set_detection: true` | 10.0000 |
| operability / classifier | `python3 -I tools/mado-action-plan.py --selftest` | 52/52, exit 0 | pass |
| operability / tripwire scan suites | four `--selftest` dirs | 9/9, 16/16, 33/33, 30/30 | pass |
| depth / adjacency | unscored; no bounded rubric | — | — |

**Lowest-axis answer.** Under the literal rule the ordering is
calibration 6.5217 < rubric V 6.6667 < everything else at 10.0 or pass.
The margin is 0.1449 (2.2% relative). Under the semantic block rule the
ordering flips: V 6.6667 < calibration 7.8261. The pre-registration's
"calibration lowest" is therefore **rubric-dependent and not stated as
such**. Because C1 and C2 are both worked, the practical lowest-axis
obligation holds either way; the record is still incomplete.

The pre-reg's own text says "QUALITY 22" and then, at `:945-947`,
"freshness … not re-measured"; it also carries operability, navigation
and exact-set from earlier rounds without re-running their rules. That
is not the literal "every active, non-retired axis under its recorded
counting rule" of QUALITY 22. I re-ran them; every carried value holds.
The defect is the missing re-derivation, not a wrong score.

## 3. Claim-by-claim: falsifiability, vacuity, separability

### C1 — calibration (`SCORECARD.md:951-960`)

Declared shell: append-only lesson-cited criteria; before 15/23 =
6.5217; target ≥ 18/26. The `measure.py` `c1` counts only
`^[0-9]+\. ` lines and the subset containing `lessons/` on the same
line. It does not check append-only, does not resolve the cited lesson
file or `#mistakes M<n>` row, and does not check the "runnable check
shown able to fail" rider.

Measured vacuity (isolated `/tmp` repo from `d9a5a18`, same
`measure.py`):

| edit | c1 | meets ≥18/26? |
|---|---|---|
| baseline | 15/23 = 6.5217 | no |
| append 3 criteria citing `lessons/round-18.md#mistakes M9-M11`, with no lesson file/rows | 18/26 = 6.9231 | **yes** |
| append 3 criteria citing `lessons/nonexistent.md` | 18/26 = 6.9231 | **yes** |
| rewrap existing criteria 18, 19, 20 to put a `lessons/` phrase on each first line (no new criterion) | 18/23 = 7.8261 | **yes** |
| delete uncited criteria 1 and 2 (no new criterion) | 15/21 = 7.1429 | **yes** |

The prose says "append-only", so a faithful closure would not rewrap or
delete; but the declared measurement would not catch it, and a report
that relied on that number would be false without the counter going red.
The `QualityDraft` task (`gen_w1.py:79`) asks for criteria 24–26 in the
right style, and `ReceiptCheck`/`MeasureMutants`/`PipeRcCensus` provide
the checks, but none of that is in C1's declared acceptance. The
runnable checks exist in the wave plan, not in the claim.

C1's facts are true (see §1). The remaining C1 risks are the overlap
with criteria 7/9/13/23 (criterion 24 re-states receipt provenance and
adds the tool sha; the `RevQualityOverlap` seat is assigned but the
pre-reg does not pre-empt a duplicate) and the possibility that an
extra, C3-motivated criterion is added to QUALITY: the pre-reg does not
say "only criteria 24–26", unlike round 17's explicit "only criterion
23" guard. If a fourth criterion is added, the denominator moves and
the 18/26 target no longer has the declared meaning.

### C2 — coverage rubric V (`SCORECARD.md:961-968`)

Declared shell: two documentary notes, P3 and P5, four sections,
`surface: P<n>`, mined tier-A used-by joins, upstream https
docs/spec/code row with surface keyword, `[UNK]` in the last section;
before 4/6 = 6.6667; target 6/6. The text adds the R17-V3 guard: "each
new credited row backed by a committed raw fetch receipt … so a closure
can tell a fetched row from an invented one."

The `measure.py` `c2` does not read the fetch receipts, does not check
the row's `opened` date, and does not check that the note is documentary
rather than an observed-behaviour claim. I built an isolated `/tmp` repo
from `d9a5a18`, added two notes with `surface: P3`/`surface: P5`, four
three-line sections each, `[UNK]` in `## Unexercised behavior`, and two
fabricated SOURCES rows (`S099`/`S100`, `docs`, tier A, `mined`,
`used-by` naming the notes, `https://example.invalid/...`, no fetch
receipts). The unchanged `measure.py` returned **6/6 = 10.0**, with
`rejected: []`. This is exactly the R17-V3 failure mode the claim says
it closes.

The wave plan has `FetchVerify` (`gen_w1.py:64`) and `FetchBackfillR17`
(`:65`), and the notes' `source:`/`used-by` joins are real. But C2's
declared command is `measure.py` only; the receipt guard is prose. The
pre-reg should bind `fetch-verify.py` (body sha/bytes + `ROW …
receipted`) and an `opened: 2026-10-20` check into C2's acceptance. The
"documentary routes, not observed behaviour" rider likewise needs a
`## Host declaration` file-bytes/`[UNK]` check or a named L1 semantic
receipt; the structural counter checks only the last section's `[UNK]`.

The 4/6 baseline is correct: P1/P2 legacy, P4/P6 r17, P3/P5 open; no
existing walker/elephant/theme/wallpaper row is mined in the current
registry. The 6/6 target is a finite-denominator completion; after it
the same round-16 rule applies ("a subsequent coverage claim needs a new
declared rubric/baseline"), which the pre-reg does not restate.

### C3 — operability frozen replay (`SCORECARD.md:969-977`)

Declared shell: `--frozen DIR` digest-checks snapshot inputs, compares a
committed expected verdict, `frozen_match` 0 / `frozen_verdict_mismatch`
1 / `snapshot_tampered` or `frozen_error` 2; committed snapshot of real
incident lines; registry row `probe` → `gate`; before `--frozen` is a
usage error exit 2; after frozen exit 0 `frozen_match`, tampered copy
exit 2 `snapshot_tampered`, frozen selftest suite N/N.

I confirmed the baseline: `python3 -I tools/mado-tripwire.py --frozen
/tmp/no-such-frozen-dir` at `962919ce…` exits 2 with the usage line.
The four existing suites are 9/9, 16/16, 33/33, 30/30. The frozen
interface in the context is the right PROTOCOL §Gate-standard shape
(committed snapshot, `expected.json` pins input digests, `[UNK]`/tamper
order, selftest mode). The gaps are in acceptance, not in the concept:

1. **`N/N` is unpinned.** A zero-case "frozen selftest suite" passes
   `0/0`. The wave plan's `TwFrozenSelftest` has thirteen cases; C3
   should state the count and the suite path
   (`.ufo/waves/round-18/tripwire/frozen`).
2. **The frozen verdict does not name the measured revision.** The
   context's verdict JSON has `tool_sha256`, `expected_sha256`, `inputs`,
   `outcome`, but no `measured_commit`. PROTOCOL §Gate standard
   (`PROTOCOL.md:388-396`) says "A verdict names the revision it was
   measured against"; R17-V1's own fix is to put `tool_sha256` and
   `measured_commit` on the receipt. The planned criterion 24
   (`gen_w1.py:79`) says the same. As specified, a C3 frozen receipt
   would be `MISSING_PROVENANCE` under C1's `receipt-check.py` — a
   direct C1/C3 contradiction, even though the C1 score is text-only.
   Add `measured_commit` to the verdict (or a mandatory `RECEIPT` header
   line) and require `receipt-check.py` to pass it.
3. **The registry move is a label-only acceptance.** "The registry row
   moves `probe` → `gate`" can be satisfied by changing the cell at
   `SKILL.md:562`, while the row's entry command is still `--scan`, the
   pinned-value path is still the scan receipts, and the selftest still
   names only the four scan suites. The gate standard requires the entry
   command, verdict map, selftest spelling, pinned-value path, write
   scope and owner. The wave plan's `SkillRegistryDraft` (`gen_w1.py:80`)
   contains the right replacement; C3 should state the required fields.
   The prose at `SKILL.md:538-539` ("It is labelled a probe: it reads
   mutable transcripts with no frozen replay") must also be updated in
   the same change, or the SKILL contradicts its own registry row. The
   pre-reg's C3 does not mention that prose.
4. **One tamper class is under-specified.** The context enumerates
   absolute/`..`/symlink/missing/non-regular/unlisted/unpinned/digest
   mismatch; the claim says "a tampered copy". The thirteen-case suite
   covers several; C3 should name the suite/case table, not one copy.
5. **Expected-verdict independence is not stated.** The `TwFrozenSnapshot`
   task derives `expected_findings` from the round-17 receipts
   cross-checked against the independent oracles, explicitly *not* by
   running the tool on the snapshot. That satisfies the gate standard's
   "independent of the recomputation" only if the cross-check is
   committed and cited. C3's text does not say it.
6. **Exit vocabulary omits `unpinned_legacy`.** The context has three
   exit-2 outcomes (`snapshot_tampered`, `unpinned_legacy`,
   `frozen_error`); C3 lists two. The registry replacement task includes
   all three. Add it.
7. **`known_misses` are part of the frozen baseline** (the three real
   misses) and force a re-pin if the tool starts finding them; C3 does
   not mention them. This is a limit, not a defect, but it should be in
   the claim's stated vocabulary so a `frozen_match` is not read as "no
   misses".
8. **Snapshot provenance is not in C3's acceptance.** The context's
   `provenance.json` maps each snapshot line to its source path/sha and
   `[snapshot_line, source_line]`; `FrozenProvenanceCheck` re-extracts
   the source lines and verifies the source sha against
   `session-index.json`. Without that check, a fabricated snapshot with
   a self-consistent `expected.json` can still `frozen_match`. Bind
   `frozen-provenance-check.py` (or an equivalent committed provenance
   receipt) to C3's acceptance.

The frozen-replay core is falsifiable: a real snapshot plus expected
file can produce `frozen_match` or a mismatch, and a digest edit can
produce `snapshot_tampered`. The gate-standard/registry/selftest riders
are not bound by the declared acceptance and can pass vacuously.

## 4. Distinctness and causal separability

Axes: C1 calibration, C2 coverage, C3 operability. Distinct.

Score-level removal tests:

| Removed | C1 literal | C2 V | C3 frozen |
|---|---|---|---|
| revert `corpus/QUALITY.md` to d9a5a18 | 15/23 fails | 6/6 unaffected | pass unaffected |
| revert the two notes + their SOURCES rows | 18/26 unaffected | 4/6 fails | pass unaffected |
| revert `tools/mado-tripwire.py` `--frozen` | 18/26 unaffected | 6/6 unaffected | fails |

So the score claims are causally separable. Two qualifications:

- **Extra-criterion coupling.** The pre-reg does not limit C1 to
  criteria 24–26. A criterion motivated by C3 (e.g. "a frozen baseline
  names its measured revision") would count toward C1's numerator.
  Round 17 explicitly refused exactly this ("only criterion 23 is
  credited to C1; a tripwire criterion was proposed and not added").
  Add "only criteria 24–26" and state that no C3-derived criterion is
  added.
- **Criterion 24 / C3 receipt conflict.** C1 criterion 24's rule (tool
  sha + `measured_commit`) and C3's frozen verdict (no
  `measured_commit`) are in direct conflict if the C1 sentence relies
  on the frozen receipt. The score still separates; the evidence check
  does not. Resolve by adding `measured_commit` before measurement.

The C1 criteria do overlap semantically with the tripwire/operability
domain (R17-V1/V2 are scan-receipt defects), which is intended by the
routing, but it means "C1 counts QUALITY text only" is true of the
number, not of the check's subject.

## 5. Findings by severity

### Major

1. **C2 passes vacuously on invented rows.** `measure.py` `c2` cannot
   see a fetch receipt; two fabricated notes + two fabricated rows give
   6/6, `rejected: []` (repro §3). This is the exact R17-V3 failure the
   claim says it closes. Fix: co-require `python3
   .ufo/waves/round-18/fetch-verify.py` with `FETCH … ok` and `ROW …
   receipted`, plus an `opened: 2026-10-20` row check.
2. **C1 passes vacuously without append-only or lesson resolution.**
   Repro: 18/26 citing a nonexistent lesson file/rows; 18/23 by
   rewrapping existing criteria; 15/21 by deleting two uncited criteria.
   The prose requires append-only and lesson-grounded criteria; the
   counter checks neither. Fix: add a `git diff d9a5a18 REV --
   corpus/QUALITY.md` check (zero `^-` lines, exactly three added
   `^[0-9]+\. ` lines) and a resolver for `lessons/round-18.md#mistakes
   M<n>`; name the three runnable checks and their expected summaries.
3. **C3's frozen verdict does not name the measured revision.**
   `tool_sha256` is not `measured_commit`. This violates PROTOCOL
   §Gate standard (`PROTOCOL.md:388-396`), R17-V1's own fix, and the
   planned criterion 24. A frozen receipt would be
   `MISSING_PROVENANCE` under `receipt-check.py`. Fix: add
   `measured_commit` to the verdict or the committed receipt header, and
   require `receipt-check.py` to pass it. The same acceptance gap covers
   snapshot provenance: C3 does not require the
   `provenance.json`/`session-index.json` source-sha check, so a
   fabricated snapshot with a self-consistent `expected.json` can
   `frozen_match`; bind `frozen-provenance-check.py` too.
4. **C3's `N/N` frozen selftest is unpinned.** `0/0` is a vacuous pass.
   State the suite path and the case count (the wave plan has 13).
5. **C3's registry acceptance is label-only.** "Row moves probe → gate"
   can be satisfied without the `--frozen` entry, exit map, frozen
   selftest, pinned `expected.json`, or the `SKILL.md:538-539` prose
   update. State the required row fields and the prose edit.
6. **The "calibration lowest" statement is rubric-dependent.** Literal
   15/23 = 6.5217 is lowest; semantic 18/23 = 7.8261 puts V (6.6667)
   lower. QUALITY 22 requires both counters. Report both and name the
   scored rule; the lane works C2 anyway, so the lowest-axis obligation
   survives, but the record as written omits the reading under which
   calibration is not lowest.
7. **The baseline receipt is not committed at d3a0000.**
   `git ls-tree -r --name-only d3a0000 -- .ufo/waves/round-18` contains
   only `evidence/census-start.txt`; `evidence/measure-before.json` is
   untracked. The round-17 file of that name has `rev: 27cd06f` and
   `c1: 14/22`, not the pre-reg's 15/23/4-6. Commit the round-18
   `measure-before.json` and cite the full
   `.ufo/waves/round-18/evidence/measure-before.json` path (QUALITY 13).

### Moderate

8. **QUALITY 22 re-derivation is partial.** `:945-947` says freshness is
   "not re-measured"; operability/navigation/exact-set are carried. I
   re-ran them: 29/29, 372/372, 32/32, 4/4 — all hold. Cite the fresh
   commands, not the prior-round numbers.
9. **Harm watch omits `--regression` and the PIN_MADO re-cut** required
   by the F10 gate change. `GateRcFix` (`gen_w1.py:63`) performs the
   re-cut; the pre-reg's harm watch (`:982-983`) does not list
   `MADO_REGRESSION: PASS` or the re-cut. Add both (round 12 did).
10. **C3 names one tamper class.** Name the context's tamper table or
    the thirteen-case suite; one class can pass while traversal,
    symlink, unlisted, unpinned or digest handling is broken.
11. **C1's runnable checks are not in the declared acceptance.** The
    wave plan has `receipt-check.py`, `measure-mutants.py`,
    `pipe-rc-census.py` + the gate OM scenario; the pre-reg says "each
    with a runnable check shown able to fail" but does not name the
    commands or the expected `EXPECT_SUMMARY`.
12. **C2's documentary-only rider is not measurable.** `measure.py`
    checks only `[UNK]` in the last section; a note can claim observed
    behaviour in `## Host declaration` and still pass. Add a file-bytes/
    `[UNK]` check or a named L1 semantic receipt.
13. **C1 criteria 24–26 may duplicate 7/9/13/23.** Criterion 24 adds the
    tool sha and re-cut receipt, but it overlaps receipt provenance;
    25/26 are distinct. The pre-reg should record the
    `RevQualityOverlap` result and cap the addition at 24–26. Without
    the cap, an extra criterion moves the denominator and the 18/26
    meaning.
14. **C1/C3 coupling via criterion 24.** See Major 3; the separation
    sentence at `:979` is true of the score, not of the check.
15. **C3's expected-verdict independence is not stated.** Require the
    `TwFrozenSnapshot` rule: `expected_findings` from the committed
    round-17 receipts cross-checked against the independent oracles,
    not from running the frozen tool on the snapshot.
16. **C3 omits `unpinned_legacy`** from the exit vocabulary; the context
    and the registry replacement have it. Add it.
17. **The round-18 section omits the saturation/planned/retired
    declaration.** The top SCORECARD contract asks for the 9.0 / N=3
    line at each round start; round 17's result carried "Saturation
    9.0 / N=3 unchanged". Add the line and `retired: none`. Also state
    that 6/6 saturates rubric V and a later coverage claim needs a new
    rubric (round-16 rule).
18. **The census receipt is committed but not cited.** `census-start.txt`
    at d3a0000 shows exit 0 with the three historical W04 lines; the
    pre-reg's "census exit 0" has no path. Cite it.

### Minor

19. C2's `source:` placeholders (`S0xx-pending`) must be replaced with
    real S072+ ids before measurement; the `measure.py` regex only sees
    `S\d{3}`. The pre-reg does not say who does this (L1 integrates).
20. C2's row `opened` date is not checked; the claim says "opened this
    round". Add the check with the receipt join.
21. The `source:` join in `measure.py` accepts any one qualifying row;
    it does not require every cited S token to be mined/tier-A/used-by.
    The pre-reg's wording could be read as every row. Tighten or state
    "at least one".
22. The round-17 C1 report's line-76 citation of `7a98720e…` is correct
    for the `f71ccbe` measurement, but the pre-reg's C1 phrase "the
    round-17 report cites tool sha `7a98720e…`" omits that line 3 also
    cites `962919ce…`; the erratum task carries both with labels. Fine
    if the lesson row does the same.

## 6. Residual risk and verification gaps

- I did not execute `--frozen`: the tool at `d9a5a18` has no
  implementation; I only confirmed the baseline usage exit 2 and the
  four scan suites. The after-state (frozen match, tamper, selftest)
  remains to be demonstrated by `TwFrozenMode`/`TwFrozenSnapshot`/
  `TwFrozenSelftest`.
- I did not run `--regression` (it executes the sibling harness; the
  pre-reg reserves it for the gate-change harm watch). `GateRcFix`
  owns the PIN_MADO re-cut and the red-before/green receipt.
- I did not re-fetch the round-17 rows (R17-V3 backfill) or the
  round-18 P3/P5 sources; those receipts are being produced by the
  fetch seats. The C2 vacuity result is therefore about the declared
  instrument, not about the seats' eventual receipts.
- I did not open the OMP transcripts' content; the R17-V1/V2 facts were
  verified from git, the committed receipts, the report, and
  `lessons/round-17.md`, not from transcript bodies.
- The `/tmp` vacuity repos are mine and are not committed evidence; the
  edit recipes in §3 are reproducible from `d9a5a18` with the same
  `measure.py`.
- The semantic block counter (18/23) is my own parse; it matches the
  round-17 result's `18/23 = 7.8261`. It is a reporting counter, not the
  scored rule.
- No tool install or upgrade was performed.

**Bottom line:** C1/C2 need their declared acceptance widened to the
receipt/append-only/resolver checks they already describe; C3 needs
`measured_commit`, a pinned frozen-suite count, and the full registry
row/prose update. The axes and the score-level separation are sound;
the pre-registration is not yet a gate that can fail on the things it
says it measures.
