# CriticHonestyR20 — round-20 phrasing attack: guards are narrower than victory prose; verdict must say "typed row, not restored precision"

Scope: which phrasings in the round-20 closeout (SCORECARD committed-results, L1 report,
lesson, capability addendum) would overclaim the registered C1/C2 guards or re-open the
round-19 closure defects. Grounded on SCORECARD.md:1228-1283 (prereg at `e629f73`),
corpus/lessons/round-19-verifier-spotcheck.md (closure, `1f7f995`), the committed harmed
tool `367be947…` (identical at `1f7f995` and `e629f73`; verified via `git show`), the
pre-harm tool `c1ae45a7…` at `9c54c56`, and the in-flight counters
`.ufo/waves/round-20/tw-precision.py` + `tw-recall-split.py` (untracked; not yet committed).

Impacted axes: operability (C1 claim wording), calibration (tally + criterion wording),
freshness/provenance (source + receipt wording), discernment (stale-tally carry-over).

## A. C1 precision wording — where "fixed" overclaims

| # | Risky phrasing | Why it overclaims (evidence) | Required phrasing |
|---|---|---|---|
| A1 | "precision restored" / "rule B fixed" | The guard is narrower: "the pre-harm reading is restored" only on P cases at `9c54c56` (SCORECARD.md:1254-1258), and invisible-callee argv rows must now exist *classified as lead* — rows the old tool never emitted. The harmed tool already calls these rows "leads" in prose (tool:41-48) but emits no `evidence` key (verdict emit at tool:1640-1641). | "The pre-harm clean reading is restored on every pure-container/formatter case (each also green at `9c54c56`), and invisible-callee literal-argv rows now carry `evidence:"lead"` — the tool reports a typed row, not a confirmed command." |
| A2 | "findings are now marked as leads" / "lead tagging implemented" | A row *without* an `evidence` key normalizes to `"observed"`, never `"lead"` (tw-precision.py:81 `row.get("evidence", "observed")`). Unmarked output silently passes observed expectations. | "Every expected lead row carries an explicit `evidence:"lead"` key; the counter treats a missing key as `observed`, so absence of the key is a fail against any lead expectation." |
| A3 | "exit 1 means a real command ran" | Lead rows stay in `findings`: label `findings`, exit 1 (contract E1). Exit/label no longer separates stated-execution rows from invisible-body rows. | "exit 1 covers `observed` rows (command and its execution path stated) and `lead` rows (literal argv to an invisible callee); the verdict adds integer `observed_findings`/`lead_findings`." |
| A4 | "recall unchanged: 6/6" | Guard: "`tw-recall.py` 6/6 unchanged **and** reported split observed/lead" (SCORECARD.md:1256). tw-recall-split.py:18 counts `observed/lead/unmarked`; an incident line reclassified observed→lead is a changed claim behind an unchanged number. | "`tw-recall.py <REV>` 6/6 **with the `tw-recall-split.py` split reported verbatim, including any `unmarked` count**." |
| A5 | "no new findings in the corpus" / "diff clean" | The guard is asymmetric by design: "loses zero findings **and classes every added row**" (SCORECARD.md:1258-1259). E1 leads are added rows on purpose; claiming zero additions would mean the lead classifier never fires. | "Whole-corpus diff `9c54c56`→FINAL: 0 `(class,rule,line,evidence)` tuples lost; K tuples added, each `evidence=lead` (baseline unmarked rows join as `observed`)." |
| A6 | "0 findings on the control lines" | "the 20 control lines" is a specific set: the 26 pinned round-18 frozen input lines minus the 6 incident lines (closure reproduced this count). | "0 findings on the 20 pinned non-incident lines of the round-18 frozen corpus." |
| A7 | "precision: N/N" | The counter compares only the multiset of `(class, rule, line, evidence)` (tw-precision.py:92-94); command text is not joined. The suite dir `.ufo/waves/round-20/precision` does not exist yet, and `SUITE_PIN=None` → `could_not_evaluate` (tw-precision.py:19,66-67). | "`tw-precision.py <tool-commit> --suite-rev <suite-pin>`: passed/N (score = 10·passed/N) over families P/S/W/H/L; the comparison is class/rule/line/evidence, not command text." |
| A8 | "the tool proves the command ran" | Tool's own contract (tool:43-48): "whether that helper executes it is not visible"; written-then-run scripts are not analysed (tool docstring ~lines 33-35) — the round-19 `hyprctl` miss rode exactly that blind spot. | "`observed` = the transcript states the command and a visible path that runs it; the tool parses transcript text, it never proves execution." |
| A9 | "counter committed before any tool edit" | Ordering claim requires git-log evidence. Today both counters are untracked (`git status`: `?? .ufo/waves/round-20/tw-precision.py`, `?? tw-recall-split.py`) and the tool is unchanged since `01b8094`. | Name both commits: "counter landed at `<hash>`; first tool edit at `<hash>`; log shown" — and do not state it until landed. |
| A10 | "red before" | `before` cells are author-computed per the case contract (`git show REV:tools/mado-tripwire.py > /tmp/...; --scan`); a suite without measured `before` is not "red-before". | "X/Y cases measured red at `1f7f995` via temp-copy `--scan`; per-case `before` recorded in each seat's `cases.json`." |
| A11 | "the suite is pinned" | `SUITE_PIN=None` until L1 fills it; the precision dir is absent. | "Suite pinned at `<commit>`, the commit that first lands the suite and carries no tool change." |
| A12 | "fixtures prove the commands work" | `--scan` parses text only; the contract forbids executing fixture code, and the counter never does (tw-precision.py:161-163). | "All case results are parser-output comparisons on text; no fixture line was executed." |

## B. Host-pause wording — R19-V4 is a landmine

| # | Risky phrasing | Why it overclaims | Required phrasing |
|---|---|---|---|
| B1 | "no host probe this round" | Closure:124-125 — the r19 scan of the committed receipt (154 session files, `live_probe=3`, `host_mutation=0`) did **not** detect `hyprctl probe` inside a written-then-executed script. A zero probe count on this round's transcripts alone reproduces the same blind spot. | "no probe row on N scanned round-20 seat transcripts (receipt + per-file digests) **and** no written-script wrapper found by `<named complementary check>`; written-script scan blindness remains a stated limit" — or do not make the claim. |
| B2 | "the host was untouched" / "no host state change" | Closure:124 — "absence of any host state change was not independently measured" in round 19; a tripwire row count is not an actuator. | "no host mutation was measured/observed" only with a named measurement; otherwise "no host mutation was detected by the bounded scan" or explicitly "self-report". |
| B3 | "isolation proven" / "the harness is safe" | Criterion 29 is a harness property: setup failure aborts before any payload, and the payload is a canary file write (SCORECARD.md:1266-1269); `isolation-check.sh` forces `mount` to fail via a PATH stub and checks canary absence. | "`isolation-check.sh` green on the r19 `inns.sh` shape and on `isolate.sh`: a forced setup failure aborts before the /tmp canary payload — a harness-shape result, not proof that no host binary can ever run." |
| B4 | "the incident is fixed" / "won't happen again" | The r19 incident is a recorded self-report plus a post-hoc scan; the parser's written-script blindness is unchanged by an isolation harness. | "R19-V4 routed: the fail-open mount shape is red-tested by criterion 29; transcript-parser blindness to written scripts stays on the limit list." |
| B5 | "155 transcripts" | The committed receipt `evidence/final/tripwire-seat-scan.txt` contains 154 `"path"` entries (`grep -o '"path"' | wc -l` → 154; verified this review). | "154 files." |

## C. Tally and calibration wording — carry-over corrections are mandatory strings

| # | Risky phrasing | Evidence | Required phrasing |
|---|---|---|---|
| C1 | "5/13 name S096" (any reuse) | Closure:59 — any-line S096 credit is **8/13**, first-line **6/13**; `w2/reports/RerunC2.md:50-73` measured the stale `01b8094` snapshot. Five named tip files have no S096 on any qualifying line. | "S096 credit at `b435568`: 8/13 on any qualifying line, 6/13 on the first qualifying line; five named files carry only the pre-existing S090 row." |
| C2 | "ten OM10 assertions" (any reuse) | Closure:88 — **nine** labeled occurrences, **eight** distinct. | "nine labeled OM10 occurrences (eight distinct), replaced by OM10A six + OM10B eight." |
| C3 | "the all-file source condition is met" under C2 | C2's counter is permissive; closure:61 held the every-file promise unmet even while the counter read 13/13. | "13/13 on the registered counter; the all-file S096-credit condition remains open" — the R19-V2 correction must be a named correction, not silently restated as satisfied. |
| C4 | "all scorecard counts verified" | Criterion 30 is *a* stated count re-derived by *a* cited command at the measured revision — per-claim, not blanket. | "Criterion 30: each stated count names the command that re-derives it at `measured_commit`; N counts re-derived, K corrected (named)." |
| C5 | "round-19 C1 repaired" / "miss closed" | R19-V1: the ≥21/29 miss stays a miss; the round-20 target is a fresh registration, not a makeup. | "Round-19's ≥21/29 miss remains recorded as a miss; round-20 C2 is a fresh claim (20/28 → 22/30 under criteria 29-30)." |
| C6 | "receipts prove it" (undifferentiated) | The closure re-ran three registered probes and *evidence-verified* the rest; lane-cut receipts are self-produced evidence. | Per receipt, state which counters a non-author re-ran and which are evidence-verified. |

## D. Sourcing, capability, scope and seat wording

| # | Risky phrasing | Why it overclaims | Required phrasing |
|---|---|---|---|
| D1 | "sourced" / "upstream-verified" without receipts | Prereg: C1 is "sourced on SOURCES rows opened this round" — that means fetch receipts (curl, sha256, tag→commit) under `.ufo/waves/round-20/fetch/<Seat>/receipts.jsonl`. Reserved ids S099-S110 are L1-assigned; drafts write `S1xx-pending`. | "sourced on S1xx… rows opened this round, receipts at fetch/<Seat>/receipts.jsonl, tag→commit recorded"; a claim without a receipt path is unsourced. |
| D2 | silently re-listing `tool_install`/`vcs_write` as capabilities | SCORECARD.md:1198-1202 explicitly omits both because their w2 precision findings are open. | Capability re-entry only with the named w2 precision findings shown closed (help/dry-run H-family, eval-surface W-family, rule-B P-family); otherwise the omission stays. |
| D3 | "all suites pass" while a case was edited | Guard: "every existing tripwire suite all-pass **(a case edit only with its reason)**". | "11/11 suites all-pass at tool_sha256 `<X>`; case edits: `<names>` + reasons, or `none`." |
| D4 | "frozen replay passes" | Guard: "round-19 frozen replay recorded (re-pinned for round 20 if the schema moves)". | "frozen_match at `<commit>` under expectation digest `<D>`; if the verdict schema moved: recorded as a documented re-pin, not claimed as a match on the old pin." |
| D5 | "no misroot" / "every write stayed in lane" | R19-V6 — the QualityDraft misroot was a real write-scope violation; the claim needs a fleet-root check, not intent. | Only with a named check: "`git -C <fleet> status --porcelain -- .ufo/waves/round-20` empty" + absolute paths at every seat item. |
| D6 | "all seats reported" | Closure:127 — 25 of 86 members lacked reports; file count ≠ joined roster. | "N reports joined to the roster; dead seats named, uncredited; no claim credited to a missing seat." |
| D7 | "recovered seat output counts" | Closure:154 — "provider recovery must not be reported as claim evidence." | Dead/retry-exhausted seats are dead; their provider-side output is not claim evidence. |
| D8 | "harm watch PASS" unqualified | R19-V5 — green bounded checks do not close the open limits (worktree-ledger/harm-watch execution-provenance, anchor-alias checker). | "Harm watch: gate selftest N/N, regression PASS, classifier 52/52, suites N/N, U 7/7, V 6/6, navigation complete, census exit 0 — while limits `<list>` remain open." |
| D9 | counting planned extras as C1 | Prereg tail: "No exploratory claim"; C1 families are P/S/W/H/L — `curl|sh`, pip pre-verb options, `jj --help` carve-outs count only insofar as suite cases land. | "Registered claims: C1 (families P/S/W/H/L over the pinned suite) and C2 (criteria 29-30); all other tool deltas reported under harm watch as non-claim repairs." |
| D10 | "the counter ran clean" from exit 0 | tw-precision.py returns 0 even with failing cases (score in JSON); rc=2 is `could_not_evaluate` — which is *not* a red and not a pass. | Report `passed/N` and per-family counts from the JSON; rc=2 must be reported as "not measured", never folded into either red or green. |

## Strongest counterexample available locally

The single sentence most likely to be written — "the frozenset harm is fixed and
precision is restored" — is false under the registered guard in two independent ways:
(1) restoration is defined only over the pure-data reading at `9c54c56`, while the
final tool deliberately *adds* `lead` rows the pre-harm tool never had, so the final
tool is not the `9c54c56` tool plus a fix; (2) a lead row emitted *without* an
`evidence` key (the harmed tool's current output shape, tool:1640-1641) is counted as
`observed` by the counter, so "marked as lead" requires the literal key, not prose or
docstring (the harmed docstring already says "lead", tool:43-48, while producing an
unmarked ordinary finding — the exact harm). Required: the two-part phrasing in A1.

## Limits

- Did not run `tw-precision.py` (suite unlanded, `SUITE_PIN=None` → could_not_evaluate
  by design) and did not scan this round's live transcripts; B1/B2 phrase requirements
  stand regardless of what that scan later shows.
- Did not diff every executor's `cases.json` `before` cells; the requirement (A10) is
  structural. Suite contents still arriving; case quality is CriticC1Overfit's lane.
- Did not re-derive the 8/13 vs 6/13 S096 tallies myself; they are cited from the
  closure's independent count (closure:59-61), which is the authority R19-V2 names.
- `tw-recall-split.py`, `isolate.sh`, `isolation-check.sh`, `corpus-diff.py` were read
  as untracked working-copy bytes; L1 may still change them.

## Installs

none.
