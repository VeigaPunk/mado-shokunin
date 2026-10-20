# SimplifyScope — round 15 U6 and R14-V1 correction proposal (mado-r15-w1)

Seat: `SimplifyScope` (simplifier, leaf). Target: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Paths below are relative to that root. No files edited, no gate/harness/tests/mutation runs, no live probes, no input reads, no installs. Read-only `git show`/`ls-tree`/`cat-file`/`log`/`diff --stat`, `sha256sum`, `grep`, `jq` on the spec, and one static `sed`-excision pipeline over a committed blob.

## Verdict

The proposal is roughly 4–8x larger than the single claim (C1: sourced U1–U5 5/7 → U1–U6 6/7, plus unscored R14-V1 precision correction) needs. Four of its artifacts duplicate existing conventions or existing rows, and one (receipt-correction JSON / new static receipt check) contradicts a declared contract. Retain the bounded U6 note, one reconciled source join set, one static mapping, one C1-only measurement, and one appended erratum block. Everything else is a merge or drop candidate.

## Axes

- **coverage (claim axis):** sourced U1–U6 6/7 by one bounded input-debugging note. Moves only if the note stays bounded and joins reciprocally.
- **harm axes (must not move):** exact gate digest `fba82a66…`; navigation complete; source census clean; no-live/selftest receipts unchanged; no new gate behavior; historical receipt bytes unchanged.

## Findings (needless scope or repeated convention)

### F1 — S051 duplicates an existing row (drop; reconcile to S007)
- `corpus/SOURCES.md:19`: `S007 | libinput helper tools — https://wayland.freedesktop.org/libinput/doc/latest/tools.html | docs | A | … | queued`.
- InputDraft/SourceCollision propose a new **S051** for the same URL (`tools.html`, libinput 1.32).
- SCORECARD round-15 claim explicitly allows reconciliation: "Source identifiers may be reconciled before measurement if the source audit finds existing rows."
- SOURCES contract: "Only `status`, `recheck` and `used-by` change in place." So the right move is S007 queued→mined in place with a `used-by` entry. A new S051 would trip QUALITY criterion 17 (duplicate canonical URL screen).
- **Keep:** S007 in place. **Drop:** S051 reservation.

### F2 — three Wayland scouts read one installed XML (merge to one scout, one new row)
- Installed `/usr/share/wayland/wayland.xml` (sha256 `cc860987…e07`) contains `wl_seat` (line 2004), `wl_pointer` (2138), `wl_keyboard` (2573), all `version="11"`.
- Seats `WaylandKeyboard`, `WaylandPointer`, `WaylandSeat` all target this one file.
- Existing `S043` is the same local file but scoped to `wl_registry` (`corpus/SOURCES.md:55`). Scope cannot change in place, so a new row is genuinely required — but only one.
- Caveat: the installed file is not a pinned upstream revision. QUALITY criterion 6 requires a named revision, so the one new row must cite the upstream `wayland.xml` at a pinned tag, not the local path. Not fetched in this seat.
- **Keep:** one new S052 (upstream `wayland.xml` pinned revision, scope wl_keyboard/wl_pointer/wl_seat). **Drop:** two of the three Wayland scouts.

### F3 — five libinput scouts read one page (merge to one)
- `LibinputTools`, `LibinputList`, `LibinputEvents`, `LibinputRecord`, `LibinputReplay` each open a different section of the same `tools.html` (S007). The Change lines overlap (safety classes, rejection boundary, recording privacy, replay vs read-only).
- The rejection boundary (no record/replay/debug-events execution) fits in the note's `## Safe boundary` section and needs one anchored quote set, not five seats.
- **Keep:** one libinput scout. **Drop/merge:** four.

### F4 — receipt-correction.json is a second errata convention (drop; use appended erratum)
- Spec ReceiptCorrection: "Create ONLY … `.ufo/waves/round-15/receipt-correction.json`."
- Declared contract (SCORECARD round-15): "preserve historical records and append an accurate mapping to the committed derived target. No wrapper or new gate behavior."
- QUALITY.md criterion 4: "Errata are append-only blocks." Criteria 7 and 13 cover re-derivation and committed evidence paths.
- Existing precedent in the same convention: `corpus/knowledge/gate-standing-use.md:404` `## Erratum — round 14, R13-V2/V3 evidence precision`, appended to the gate note that records the derived PIN (`:440–446`).
- **Keep:** one appended `## Erratum — round 15, R14-V1 …` block in `corpus/knowledge/gate-standing-use.md`. **Drop:** the JSON file.

### F5 — the derived-target re-derivation is already one static pipeline (collapse the seven parallel derivations)
Re-derived in this seat (static, read-only, no excision written to disk):

```sh
git show 32118fc1014837b3a385c7a66abbdc59b1560835:tools/mado-verify.sh \
 | sed -e '/^[[:space:]]*# >>> MADO-R7-REGRESSION-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-REGRESSION-BLOCK <<<$/d' \
       -e '/^[[:space:]]*# >>> MADO-R7-SELFTEST-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R7-SELFTEST-BLOCK <<<$/d' \
       -e '/^[[:space:]]*# >>> MADO-R8-BLOCK >>>$/,/^[[:space:]]*# <<< MADO-R8-BLOCK <<<$/d' \
 | sha256sum        # cd1d73d75fcc8e5b96d5b83c0d16660897e58cf32edf77416d389fa16b9f3f96
```

Observed: `cd1d73d7…`, **117602 bytes**. Matches `MUTATE_TARGET … bytes=117602` in all three receipts (`.ufo/waves/round-14/evidence/regression-recut.txt:8`, `regular-target-mutants.txt:8`, `retained-census-mutants.txt:8`). The committed `PIN_MADO` at `tools/mado-verify.sh:1639` is the same value. Marker counts at `32118fc`: 8 begin, 8 end (three families).

Consequence: DerivedIntent, ReceiptCorrection, AttackMistake, ReceiptSafety, ReceiptMutation, ReceiptChain and ReviewRouted each re-prove this one line. One derivation command in the erratum block is sufficient.

### F6 — new static receipt check contradicts "no new gate behavior" (drop)
- MistakeRecord and FrontierRecord ask for "a minimal demonstrably-failing static receipt header check." ReceiptMutation asks for "a red/green check that rejects original provisional mutation receipts."
- SCORECARD: "No wrapper or new gate behavior." `gate-standing-use.md:425–428`: "No generic receipt wrapper or second runtime format is required or shipped."
- The R14-V1 requirement is a *precision* mapping (provisional header → committed derived target). Its verification is the F5 pipeline plus the existing `git show | sha256sum` gate-digest command. A new check is a tool, not a correction.
- **Keep:** one lesson row (MistakeRecord) with class/evidence/fix. **Drop:** new header check and ReceiptMutation seat.

### F7 — two measurement files = two conventions (keep one C1-only probe)
- `.ufo/waves/round-14/measure.py` (582 lines, 24,952 B) already implements C1: `covers:` U1–U7 extraction (`:160`), `mined_ab` reciprocity (`:106`), U4 facets (`:151–178`), U5 decision-section facets (`body_facets` `:112`, candidate loop `:181–197`); C2 gate execution (`build`, `gate_run` `:231–273`).
- Round-15 MeasureBuild asks for a *new* `.ufo/waves/round-15/measure.py` that "reuses" C1 and runs no gate. A second file that copies C1 is a second convention.
- SCORECARD fixes the counting command: `python3 .ufo/waves/round-15/measure.py REV`. The path is declared, so the planner must choose one implementation at that path: a C1-only probe (C2 dropped, since no gate execution is in scope) with U6 facets (`## Layer ladder`, `## Safe boundary`, `## Unexercised delivery` with `[UNK]` last) added to the existing generic body-facet logic.
- **Keep:** one C1-only probe. **Drop:** the parallel copy and the C2 gate path for this round.

### F8 — seat count versus scope (merge candidates; dispatch is config-fixed)
- `dispatch.json` policy: `minLanes 16`, `waveMinLanes 64`, `maxLanes 64`, spawn 64. The 64-seat count is config-driven, so trimming it is a planner/config decision, not a seat-level one. Reported here, not applied.
- Merge candidates by overlapping Change text:

| Cluster | Seats today | Retain (proposal) |
|---|---|---|
| libinput docs | LibinputTools/List/Events/Record/Replay (5) | 1 scout |
| Wayland XML | WaylandKeyboard/Pointer/Seat (3) + TextInputBoundary (1) | 1 scout; TextInputBoundary is a one-sentence boundary, not a registry row (its own text: "no extra registry row or broad IME claim required") |
| version anchors | InputVersions, DocsVersion, ReviewDocsEra (3) | 1 |
| Hyprland docs | HyprInputDocs (1) | 1 |
| privacy/safety | InputSafety, ReceiptSafety, PrivacyThreat, SourceTrust (sentinels 4) + ReviewPrivacy, ReviewSafety, ReviewRecheck, PrivacyJoin, AttackSynthetic | 1 sentinel + 1 reviewer |
| source/registry | SourceChain, SourceCollision, ReviewSourceTier, ReviewRegistry, ReviewQuotes, AttackSource (6) | 2 |
| R14-V1 receipt | ReceiptCorrection, DerivedIntent, AttackMistake, MistakeRecord, ReceiptMutation, ReceiptChain, ReceiptSafety, ReviewRouted (8) | 2 (executor + one attack) |
| measurement/score | MeasureBuild, ReviewCensus, ReviewScore, AttackMetric, AttackCoverage, GapCensus, ReviewNavigation (7) | 2 |
| U6 inference attacks | AttackDefault, AttackDelivery, AttackText, AttackNoHarm, ReviewKeyboard, ReviewPointer, ReviewSeat, ReviewLibinput, ReviewNoHarm (9) | 1 per inference class, mapped by EvidenceClassJoin |
| scribes | GateDecisions, FrontierRecord, ReportAudit, MistakeRecord (4) | 2 (lesson row; decision matrix) |

- Per-seat prompt boilerplate (the godspeed header and the identical Acceptance block) repeats 64 times. Not a scope change, but it inflates every dispatch.

## Retained set (what survives simplification)

1. One bounded U6 note: `covers: U6`, provenance trio, `## Layer ladder` / `## Safe boundary` / `## Unexercised delivery` with `[UNK]` last. Sources: S007 (in place) and the new S052.
2. Source join: S007 queued→mined with `used-by` in place; S052 new mined row; reciprocal `used-by`. No S051.
3. One static mapping (EvidenceClassJoin-level: OBS-static / INF-docs / UNK per statement).
4. One C1-only measurement at the declared path; U4/U5 facets preserved; no gate execution.
5. One appended erratum in `corpus/knowledge/gate-standing-use.md`: derived target `cd1d73d7…` (117602 B) with F5 command; three provisional headers mapped (`ef50e262…`, `d6d5eb27…`, no measured_commit header); historical bytes untouched; not a final full-gate receipt.
6. One lesson row for R14-V1 (MistakeRecord).

## Measured facts (this seat)

- `git show 32118fc…:tools/mado-verify.sh | sha256sum` → `fba82a662795813ac65e4af293bd4ca3d135148a277ccf1d5e90777ac3f5c207`, 177,849 B. Identical at HEAD `ea0446f` (`git show HEAD:tools/mado-verify.sh | sha256sum`). The receipts' provisional gate digests (`ef50e262…`, `d6d5eb27…`) match neither.
- F5 excision → `cd1d73d7…`, 117,602 B.
- Installed `wayland.xml` sha256 `cc860987…e07`; wl_seat 2004, wl_pointer 2138, wl_keyboard 2573.
- SOURCES S007 (line 19) URL equals the proposed S051 URL.

## Tradeoffs and caveats

- **S052 still needs a new row and a pinned upstream revision** (not fetched here). Dropping S051 does not remove all source work.
- **Erratum location** is my choice from precedent (`gate-standing-use.md:404`); the alternative is `corpus/lessons/round-14.md`. Pick one and state it.
- **Seat-count reduction** requires a dispatch-config change (waveMinLanes 64). Not applied.
- **Derivation proof is static equality of bytes** (sha + byte count match the receipts). It does not re-execute the mutation suite and does not make the provisional receipts full-gate receipts.
- I did not re-open S007 or the libinput page; F1 relies on the registry row text and URL identity.

## Install and tool record

None. No tool installed or upgraded by this seat.
