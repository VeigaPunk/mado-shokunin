author: hyaku closure (non-author integrator, @m_zfl)

# mado round 83 — non-author verifier spot-check

Round 83, hyaku run 15, attempt 1. Lane base `67dd2b667b72f7f72309340d488b355d543841a5`; lane HEAD
`bc48e8035cf93019937d955031a6deeac4bb59ab` (= `origin/master`, `jj-lane.sh state`: ahead=0
behind=0 tracked=0 untracked=0; `git status --porcelain` empty); instrument freeze
`dbc09269fe547ab13541e722dd7d2ba33015f348`; content revision `5ceb187f9494e22a9cf23ccc34c3f5ef90d9eafa`.
Report `.ufo/reports/round-83/mado.md` @`1a519e8b4f495c423b82a876b15093ea4c784c6a`, authored
`mado-shokunin <mado@shokunin.local>` — lane identity, correct. The lane did not author this file;
this judge ran no lane gate and no mutating git/jj command in the lane.

Dispatch digest (copied from `.ufo/watchdog.log`, lines 2369/2381):
`2026-11-04T10:56:14-03:00 launch mado round=83 pgid=2782827 driver=hyaku-inline attempt=1` /
`2026-11-04T11:34:12-03:00 complete mado round=83; hyaku-inline attempt=1`.

## 1. Conformance

- Report path/heading/content: real report, not a marker — opens by naming C1 coverage and C2
  operability, all required sections present, `SHONEN` heading with one `[~]` line per box and
  SHONEN.md carries exactly those four boxes. Status `ok`.
- All six cited lane commits exist and are ancestors of `master`:
  `git merge-base --is-ancestor <h> master` → yes for 4e48d8e7, 4208c24a, aeeb5e54, dbc09269,
  5ceb187f, bc48e803.
- Dispatched prompt `.ufo/prompts/mado-round-83.md` is the canonical `templates/round-prompt.md`
  rendering (§1–§5 verbatim modulo substitutions) + hyaku addendum §6; round-level items (mission
  binding, L2 ≥8, commit-then-push, push scope, L0 channel) and the five child-lane items all
  present. Fidelity check passes.
- Wave: ONE v1 wave `w1`, `w1-results.json` seats=10, 7 nonempty outputs, 3 empty (scout
  R83ScoutSource, connector R83ConnSiblings, scribe R83ScribeEntry) — exactly as the report
  discloses; no seat replaced, no empty output backfilled. Attack seats 4/10 ≥ 25%. L2 floor 10 ≥ 8.
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado` → exit 0,
  warning set = W04 scoped duplicate URLs + W01 S277 — matches the report's disclosure.

## 2. Claims — re-measured vs evidence-verified

Plain re-measurements this judge ran over committed bytes (lane gates NOT executed, per §Gate
standard Closure consequence):

- Controls: `c1-cases-r83.json` = 58 cases (47 carried from `c1-cases-r82.json` + 11 new);
  `c2-runbook-cases-r83.json` = 31 (29 + 2 new). Runbook section in SKILL.md
  ("### Executable runbook rows"): 29 command rows at base → 31 at tip.
- Registry: `corpus/SOURCES.md` rows 418 (base) → 420 (content 5ceb187f and tip) with the
  report's own counting command.
- Wave/SHONEN/LOG: `w1-results.json` 10/7/3; SHONEN 4 boxes; `LOG.md:4109` Round 83 entry;
  `corpus/knowledge/bar-footprint-surface-band-r83.md` opens with the provenance trio and cites
  S481/S464/S470 + S484/S485; `corpus/QUALITY.md` criterion 137 (mutant target equals the actual
  enumerated mutation list before scoring) cites the round-83 lesson number-drift row.
- SCORECARD diff base→tip is additions only; no existing row edited; no numeric delta awarded.

Evidence-verified (committed receipts, revision-pinned):

- C1 receipts: `control-c1-r83-at-base.txt` — held r82 tool (sha256 58ef4f6a…) `cases=58
  correct=52 … verdict=TARGET_MISSED rev=67dd2b66` (do-nothing control); freeze receipt
  `measurement-c1-r83-freeze.txt` — `mutants=38 killed=39 … verdict=TARGET_MISSED rev=dbc09269`
  exit 1, correctly printed; `measurement-c1-r83-repaired.txt` — `mutants=39 killed=39
  verdict=TARGET_MET rev=dbc09269`; `final-c1-r83.txt` — `cases=58 correct=58 mutants=39
  killed=39 base_correct=52/58 carried=47/47 tool_selftest=136/136 verdict=TARGET_MET
  rev=5ceb187f`. The declared claim's frozen predicate FAILED (38-declared vs 39-observed
  mutation population) and the lane did not retroactively admit — the honest stop is real, and
  R83ReviewerC1's three 58/58-surviving causal cheats (non-bar live-box substitution, extra
  positive-band override, explicit-zone override) are disclosed in the lesson and the bounded
  knowledge entry. **C1 does not verify as declared.**
- C2 receipts: `final-c2-r83.txt` — `cases=31 executed=31 matched=31 shapes=26/26 anchors=31/31
  rows=31/31 superseded=waybar-pgrep mutants=27 killed=27 verdict=TARGET_MET rev=5ceb187f
  tree=bound`; freeze receipt identical at dbc09269; `control-c2-r82-at-r83.txt` — held r82
  instrument refuses at stage=setup ("0 command rows, frozen target expects 29"). The declared
  finite predicate verifies; the lane claims only the finite predicate and rejects the
  producer-success reading per R83ExecC2Live. **C2 verifies as declared (finite).**
- Harm watch receipts, all at 5ceb187f: `final-index-r83.txt` 102/102 missing=0 dangling=0
  duplicates=0; `final-ledger-r83.txt` population=152 ledger_rows=152 uncovered=0;
  `final-axis-r83.txt` checked=3 mismatched=0 (navigation 102/102, calibration 86/86,
  operability 12/12); `final-gate-r83.txt` `MADO_SELFTEST: 460/460` exit 0. No owned axis harmed.

## 3. Per-axis verdicts (this judge)

| Axis | Verdict | Reason |
|---|---|---|
| coverage | unchanged | C1's finite before→after re-derives (52/58 held → 58/58 candidate, 47/47 carried, selftest 136/136), but the frozen claim missed its own mutation predicate and causal certification fails (3 surviving cheats); lane awards no delta, admits nothing. Real finite progress, no admitted axis move. |
| operability | improved | C2 verifies on its declared finite predicate: runbook 29→31 rows re-counted in SKILL.md, 31/31 executed/matched, 27/27 mutants, TARGET_MET at 5ceb187f, supersession disclosed; producer-success correctly refused. |
| depth | unchanged | Bounded documentary entry only; explicitly refuses causal admission. |
| freshness | unchanged | Dormant 9.6552 value stays operator-owned; no freshness claim. |
| calibration | unchanged | Honest stop self-reported with exact receipts; no numeric self-upgrade. |
| adjacency | unchanged | Connector seat empty (disclosed); scope held at existing layer/tray boundary; no sibling ground absorbed. |

## 4. Discernment spot-check (LEARNING.md)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S484 systemd v262 busctl(1) | admit | live URL + committed `fetch/busctl-man.txt` | agree | Quote "For arrays, a numeric argument for the number of entries followed by the entries shall be specified." resolves at :495–496 both live (27,072 B fetched) and in the committed fetch; 17 words ≤ 25; tier A docs; scope honestly limited to terse property formatting, not pipeline failure propagation. |
| S485 Waybar SNI host.cpp @90b209ad | admit | live URL + committed `fetch/waybar-sni-host.cpp` | agree | Quote `sn_watcher_call_register_host(host->watcher_, host->object_path_.c_str(), host->cancellable_,` resolves at :78 live (5,196 B) and committed; registered-list read `sn_watcher_dup_registered_items` at :101 grounds the anchor; the "not proof that every host state is healthy" caveat matches R83ExecC2Live's producer-masking finding. |
| Use a live box as the allocation's source | reject | `c1-cases-r83.json` (`alloc-live-band-differs`, `alloc-live-box-differs-composed`), carried r82 cases | agree | Independent inputs must be allowed to disagree; the mismatch cases exist and kill `box-verdict-blind`/`box-verdict-blind-single` (final-c1 receipt), and carried `auto-left-dock` is present in `c1-cases-r82.json`, contradicting the blanket rule the lane rejected. |
| Absent allocation always forbids a compositor-assigned spanning box | reject | carried `auto-left-dock` in `c1-cases-r82.json` | agree | The carried case is a compositor-assigned spanning box without an allocation entry; the blanket rule would break it (47/47 carried). |

New SOURCES.md row re-opened: both S484 and S485 (quotes, anchors, tiers, 2026-11-04 opened dates
all resolve; no existing row's status/recheck/used-by cell changed — verified by reading the base
registry diff). Gate quote discipline (D10 carry-in) is met: each admitted row's own sentence is
quoted with location.

## 5. Trend verdicts (this judge)

- **expansion: improved** — one new admitted knowledge entry on ground the coverage map did not
  hold (second-surface allocation + tray state pair), citing mined rows S484/S485 (re-opened by
  this judge) and indexed 102/102 (`final-index-r83.txt`). The entry is explicitly bounded, so
  this is corpus expansion, not a causal claim. The lane self-graded `unchanged "for admission"`;
  this judge grades by the LEARNING.md observable (net new admitted entries on uncovered ground
  citing mined rows), which the round meets.
- **quality: improved** — the number-drift defect is red-before/green-after with committed
  evidence: freeze receipt prints `mutants=38 killed=39 … TARGET_MISSED` exit 1, successor
  receipt prints 39/39 `TARGET_MET`, the original claim stays reported missed, and QUALITY.md
  criterion 137 is grounded in the lesson's number-drift row. Fixture-PID supersession and anchor
  repairs are disclosed with both hashes. No admitted entry failed its re-check.
- **discernment: improved** — the outside-lane spot-check the lane left pending is this file:
  it agrees with both sampled admits and both rejects (table above), and the lane's own rejections
  of the overstrong interpretations (live-box oracle, producer-success) were correct. No
  disagreement is left unlearned.

Lane self-grades were expansion unchanged / quality improved / discernment unchanged; the two
divergences are graded above with the observable each rests on. Neither gates admission.

## 6. Routed defects (lane must fix next round)

- **R1 (medium) — gate-registry drift at the registry home.** SKILL.md §Gate registry carries
  rows for the r80/r81 counters (SKILL.md:806–810) but none for `c1-r82-allocation-band.py`,
  `c2-r82-runbook.py`, `c1-r83-surface-band.py`, `c2-r83-runbook.py`; they are registered only in
  `quality/tool-ledger.md` (rows for all four present; ledger gate 152/152 uncovered=0). Per
  PROTOCOL §Gate standard/Registry the child lane's registry home is its own SKILL.md; add the
  four rows there next round.
- **R2 (info) — C1 predicate bookkeeping.** The frozen declaration's mutant constant (38) did not
  equal the enumerated list (39). Repaired forward and grounded as QUALITY 137; the declaration
  file itself stays frozen as filed. Next freeze: run the pre-scoring population assertion the
  report itself plans.
- **R3 (info) — empty seats** (scout, connector, scribe) are disclosed evidence gaps, never
  backfilled; no replacement was spawned. The sibling-overlap review the connector would carry is
  still owed; the lane correctly kept scope at the existing boundary rather than claiming it.

## 7. Notes for the operator

- Promotion is operator-owned. The four SHONEN boxes look fully checkable by a non-author
  (SKILL.md decision tables/error patterns/checklists with cited sources; LOG Round 83 end-to-end
  counter runs with committed receipts; executable declaration commands with resolvable pointers;
  PROVINCE unchanged and accurate) — all four are `[~]` lane assertions awaiting a non-author
  verifier; this spot-check re-opened samples of each but did not write `[x]`.
- Round verdict: honest stop, `ok`/not admitted — C1's frozen predicate missed, C2's strong
  interpretation refused; both refusals are the round's best work.
