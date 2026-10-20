# RevCriterion30 — Narrow criterion 30 before counting it as new

## Findings

### High — the proposed core requirement duplicates criterion 10

The draft’s first clause (“A count stated in a SCORECARD, lesson, or report claim is re-derived at the measured revision by a cited command”) is already the general rule of QUALITY 10: every count is reported with a command and date and re-derived from its named revision rather than copied from a prior summary (`corpus/QUALITY.md:16`; source rationale `corpus/lessons/round-12.md:19`). Adding this as a new numbered rule would award another calibration point for an existing requirement and conflicts with R19-V1’s no-duplicate disposition (`corpus/lessons/round-19-verifier-spotcheck.md:149`). The preregistration says 30 does not restate 24, 27, or 28, but does not resolve the direct overlap with 10 (`SCORECARD.md:1270-1273`).

The named nearby rules do not make the broad clause distinct: 22 covers re-deriving axes under their recorded counting rules; 24 binds receipts to their producer bytes and measured commit; 26 requires producer failure status to propagate as UNKNOWN (`corpus/QUALITY.md:107,131,144-154`). A narrower requirement about explicit count scope and matching historical claims to their own revision would be new; bare re-derivation is not.

**Recommended line, only if criterion 30 is narrowed to that distinct requirement:**

> 30. For a published count whose result depends on its measured revision, population, eligibility predicate, unit, or line-selection rule, state those terms with the value. A later re-measurement is a separate claim, not a red against a correctly revision-scoped historical value; append a correction that preserves the earlier value with its actual scope and states the new value with its own revision and rule. A mismatch is red only when claim and re-derivation use the same declared revision and rule. (lesson: lessons/round-20.md#mistakes M3; outside lessons/round-19-verifier-spotcheck.md R19-V2, R19-V4, R19-V5)

The registry/check should therefore include `claim_revision` (not only the revision passed to the checker), measured population/unit, predicate, and selection rule. The command and revision-binding rule from criterion 10 remain required; criterion 30 should not score them a second time.

### High — the planned S096 red compares unlike revisions and rules

The draft calls `SCORECARD.md:1167` red at `b435568`, comparing its “5/13 name S096 on the crediting line” with 8/13 any-line or 6/13 first-line (`.ufo/waves/round-20/w1/drafts/ScribeQuality.md:12-15`). But the SCORECARD paragraph explicitly scopes that report to wave 2 “over `01b8094`” (`SCORECARD.md:1162-1168`), and the underlying RerunC2 table is a measurement of committed bytes at `01b80946…`, with its tally defined as files where S096 was “cited as evidence” (`.ufo/waves/round-19/w2/reports/RerunC2.md:50-73`). The closure’s 8/13 and 6/13 figures are instead at reviewed tip `b435568`, under its any-matching-line and first-matching-line rules (`corpus/lessons/round-19-verifier-spotcheck.md:59-61`).

Thus the exact historical `5/13` at SCORECARD line 1167 is not an honest red merely because a later revision yields different values. The closure supports a real *later-tip correction*; register that as a separate claim at `b435568`, explicitly choosing any-line (8/13) or first-line (6/13), and preserve the `01b8094` result only as a historical claim under its original “cited as evidence” rule. [UNK] whether 5/13 independently re-derives under that original rule: I read the source report, but did not rerun its counter. The planned registry fields described in the draft do not name a claim revision, so as described they cannot distinguish these cases.

### Medium — two other planned reds are grounded, with their units stated

- **155 vs 154:** the R19 lesson says “155 round-19 transcripts” (`corpus/lessons/round-19.md:123-130`); the closure reports 154 entries in the scan receipt (`corpus/lessons/round-19-verifier-spotcheck.md:125`). I parsed the receipt JSON as data: `len(files)=154`; all 154 `files[].path` entries have `.jsonl` suffix and the `MadoR19` prefix; `exit=1`. The receipt is `.ufo/waves/round-19/evidence/final/tripwire-seat-scan.txt`, SHA-256 `9572d2a655d1e06aef73b4e87edb713e9486be1f0e9a8f92ed98bb42830e3139`. This is a well-grounded mismatch for that scan population; the checker should say it counts receipt `files` entries (transcript JSONL inputs), not make a generic file/transcript equivalence claim.
- **Ten vs nine/eight:** SCORECARD says ten old OM10 assertions were replaced (`SCORECARD.md:1225-1226`). The closure compared the baseline and final selftest labels and reports nine old labeled assertion occurrences, eight distinct, at baseline, replaced by OM10A six plus OM10B eight (`corpus/lessons/round-19-verifier-spotcheck.md:87-89`). This is a grounded red when the counted unit is labeled occurrences/distinct labels and revisions are bound to baseline `9c54c56` and final `7b4839d`; the check should not infer the broader “no other prior assertion lost” claim from a label count.

### Low — the draft’s lesson anchor points to the wrong mistake row

The ScribeQuality draft cites round-20 mistake M2 for count re-derivation (`.ufo/waves/round-20/w1/drafts/ScribeQuality.md:12`), while the round-20 ScribeMistakes draft labels stale tallies M3 and M2 as the fail-open harness (`.ufo/waves/round-20/w1/drafts/ScribeMistakes.md:8-9`). Use M3 for this criterion once the lesson lands; its anchor is not yet verifiable in the canonical lesson.

## Residual risk

A registry-driven checker can miss any unregistered claim; a text/grep counter can miss dynamically generated labels and cannot decide whether a number denotes assertions, labels, evidence-positive files, or all matching files. The draft acknowledges that counting cannot establish provenance or behavior; keep criteria 24 and 27’s producer/anchor boundaries, and criterion 26’s command-failure handling, explicit. A green count check is not a truth or behavior audit by itself.

## Verification gaps

- Reviewed the draft and source text at lane HEAD `e629f731172b8238caffe50f152217ce56535fb4`; `git diff -- corpus/QUALITY.md SCORECARD.md corpus/lessons/round-19-verifier-spotcheck.md` was empty. Criterion 30 is not in canonical QUALITY at this revision; this is a review of the draft, not a landed criterion.
- No `count-rederive.py` or claim-registry check was run; the draft labels both planned/not landed. No round-20 lesson citation can be validated until that canonical lesson exists.
- LSP is not mounted in this session: `read xd://lsp` returned “No such tool.” Literal search was used only to locate passages; conclusions above rely on direct reads of the cited text and receipt data, not grep as semantic proof.
- No build, suite, live gate, host probe, or fixture execution was performed.

## Limits

This was a read-only review of criterion wording, the round-19 closure and the identified receipts/reports. I did not independently rerun the RerunC2 counter at `01b8094`, re-derive the old OM10 labels from `git show`, or validate the proposed future checker against its three claim records. Those remain required before treating the checker’s reds/greens as verified.

## Installs

none
