# Attack26 — C2 new source row URL collision distinct-scope review

Wave: round-52 W2 (attack, not a vote). Seat: Attack26 (critic; sibling Attack10/scout holds the
same target — this is the critic report). Lane root for all trailers:
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Base `85d57a818c3707397e21c840b6498b105ba798aa`
(lane tip unchanged; all corpus changes below are uncommitted working-tree state, confirmed by
`git status --short corpus/`).

Target control (W2 signal): repeated URL rows S370/S371/S373 require explicit QUALITY17
distinct-scope review. Attacked frozen clauses: C2 predicate "each maps to an opened-this-round
`S###` row" (registration.md) and the premise that the new entry is "grounded in sources opened
this round" (claims-frozen.md), plus the rule-17 process requirement (QUALITY.md:34) attached to
those rows. Method: local reads, grep, sha256sum, python3 range/URL comparisons in scratch only;
no network, no live reads, no installs, no tracked writes outside this report, no git/jj mutation.

## A1 — The collisions are real: byte-identical URLs+commit

Attacked clause: premise that S370–S373 are distinct new source rows.
Reproduction: python3 extraction of URL cells from `corpus/SOURCES.md` (landed rows, :320–323)
vs prior rows S364 (:313), S365 (:314), S367 (:316).

Outcome:
- S370 URL == S365 URL — `…/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp` — identical string.
- S371 URL == S367 URL — `…/src/config/shared/actions/ConfigActions.cpp` — identical.
- S373 URL == S364 URL — `…/src/managers/KeybindManager.cpp` — identical.
- S372 (`ConfigActions.hpp`) is the only new URL.

Verdict: REPRODUCED. W1 reports (C2PinAudit, RegistryContract, C2CoverageCritic) claimed the same
collisions; independently re-derived from the landed registry bytes.

## A2 — The bytes are not new either

Attacked clause: "sources opened this round" as a novelty premise.
Reproduction: `diff .ufo/waves/round-52/fetch/SHA256SUMS .ufo/waves/round-51/fetch/SHA256SUMS`
for the four files.

Outcome: 4/4 sha256-identical (DispatcherTranslator.cpp `7248cbb8…`, ConfigActions.cpp
`a83abeb5…`, ConfigActions.hpp `746c6f51…`, KeybindManager.cpp `8d8f35fc…`). The round-52
"opening" is a re-fetch of byte-identical content at the same immutable commit.

Verdict: REPRODUCED. Limitation: the frozen predicate speaks of *rows* opened this round, and the
rows are new with this-round access dates and fetch receipts; byte-identity alone does not
falsify C2 — it means all novelty rests on scope, which is exactly what rule 17 reviews.

## A3 — Ordering violation: rows landed before the mandated distinct-scope review

Attacked clause: QUALITY.md:34 criterion 17 — "send distinct-scope reuse to human review";
`corpus/lessons/round-52.md` Gate — "Review source URL collisions against prior rows before
appending".
Reproduction: `stat` timeline — lesson written 11:12:19, entry created 11:13:49,
`corpus/SOURCES.md` appended 11:15:54, W2 (review wave) dispatched 11:16:21; read of the
registry search log `corpus/SOURCES.md:374`.

Outcome: rows S370–S373 are in the registry while the registry's own search log states
"S370, S371 and S373 reuse canonical URLs with new scopes; distinct-scope review remains
outstanding." The review wave began ~30 seconds after the append; no review preceded admission.

Verdict: REPRODUCED (fixable process defect; see correction).

## A4 — The only screen run is a warning-only census, which rule 17 excludes

Attacked clause: QUALITY.md:34 — "A warning-only shared census is not this review."
Reproduction: `.ufo/waves/round-52/census-after.txt` (W04 lines for S370/S371/S373, "duplicate
url … across scopes"); grep for "distinct-scope" across `.ufo/waves/round-52` — every hit is a
statement that the review "remains outstanding" or "must be recorded", none is a review.

Outcome: no explicit overlap review exists anywhere in the round tree; the census is the only
collision screen, and rule 17 names it as insufficient by text.

Verdict: REPRODUCED.

## A5 — Row cells lack the resolvable prior-id linkage rule 17 expects

Attacked clause: QUALITY.md:34 — "append a genuine superseding row with a resolvable prior id";
the r39 precedent handling (`.ufo/waves/round-39/registration-a2.md:71`: proposed S220 rejected
as a within-scope duplicate of byte-identical S196 — the amendment cites S196 re-opened and S018
gets `used-by` extended, not duplicated).
Reproduction: read of the landed row cells `corpus/SOURCES.md:320-323`.

Outcome: no row cell names its prior row (no S365/S367/S364 mention); scope/teaches cells carry
no criterion-17 marker; the reuse note lives only in the search log (:374), which is not a
row-resolvable prior id. A registry reader cannot mechanically resolve S370→S365, S371→S367,
S373→S364 from the rows.

Verdict: REPRODUCED (wording/record defect, not grounds for rejection by itself).

## A6 — Merits, hard case: S370 vs S365 overlap is arguable; P06/P15 are held-adjacent

Attacked premise: that region-newness settles distinctness without review.
Reproduction: scope-wording comparison and a line-range intersection test (python3, ranges taken
from the anchor cells): S365 anchors `:30-35,:797-867` vs S370 `:531-627` → `region_overlap=False`.
Cross-checks: W1 `C2Novelty.md:97-104` — landed P06's quote is the same quote round-51 bound for
the same fact (`CVarList2 ARGS(args, 3)` at :532-535, held via S365); W1 `RegistryContract.md:11`
— the r51 entry already describes `sendkeystate` saving/restoring `m_passPressed`
(`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:197-199`), overlapping landed P15
(save at DT:612 — new pin, but the save/restore fact was held).

Outcome: cited regions are disjoint, but S365's scope wording ("how implementations parse
arguments") generically covers per-dispatcher parsing, and two landed propositions restate
held r51 facts with new pins. This is precisely the case rule 17 sends to human review; neither
"URL equal → duplicate" nor "regions new → distinct" is licensed without it.

Verdict: REPRODUCED — the merits require the review; they do not pre-decide it. On merits,
admission is defensible if the review records prior-id linkage and the P06/P15 held-adjacency.

## A7 — S373 vs S364 AND vs S162: an overlap the URL census cannot see

Attacked premise: that the W04 URL census screens all duplicates.
Reproduction: S373 anchor `:221-242` vs S364 `:41-113,602,782,785,798-823` → disjoint; but the
held `corpus/knowledge/bind-table-r25.md:42` (S162 account) already teaches "`stringToModMask`
uppercases then substring-matches tokens", and landed P07 asserts the same uppercase+`contains`
facts (KeybindManager.cpp:221-225). S162 pins `ConfigManager.cpp` — a different URL — so no W04
flag fires.

Outcome: landed entry contains a scope-level duplication invisible to the census; the S373 row
names no S162 linkage.

Verdict: REPRODUCED — the distinct-scope review must also cover the S162 prior account, not only
the same-URL prior rows.

## A8 — Merits, easy case: S371 vs S367 is clean

Reproduction: S367 scope "what the submap dispatcher does to current submap state"
(`:1664-1682`) vs S371 "synthetic key and modifier delivery call order" (`:1530-1616`); ranges
disjoint, scopes disjoint.

Outcome: no wording overlap beyond sharing the file.
Verdict: NOT REPRODUCED — apart from the missing review record (A3–A5), no defect in this pair.

## A9 — S372 has no collision

Reproduction: census-after.txt W04 lines list only S370/S371/S373; S372's URL
(`ConfigActions.hpp`) appears in no active row (C2PinAudit info: it was denied a row in r51).

Verdict: outside attack scope; no collision to review.

## A10 — The counter cannot certify rule-17 compliance; green proves the fixture only

Attacked premise: that a passing counter closes the collision question.
Reproduction: read of `w1/C2CounterDraft.md` — clauses (a)–(e) check existence, declaration,
row bindings, quote-at-pin, mapping completeness; the doc states it "does not score novelty,
wording reuse, or held-fact omission"; clause (d) reports `pins_prior_equal=N/M` as information
only. Integration note: counter default `ENTRY=corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`
vs landed slug `hyprland-synthetic-dispatch-r52.md` — the constant must be changed at integration
(the draft itself flags this).

Outcome: a TARGET_MET run is compatible with the review still being outstanding; the r-green
receipt exercises a synthetic staged fixture, not the landed corpus state (matches the W2
signal "counter draft r-green proves a separate synthetic fixture only, not landing").

Verdict: REPRODUCED.

## Summary

| # | Attack | Verdict |
|---|--------|---------|
| A1 | S370/S371/S373 byte-identical URLs+commit to S365/S367/S364 | REPRODUCED |
| A2 | r52 fetch bytes sha256-identical to r51 pins (4/4) | REPRODUCED |
| A3 | Rows landed before the rule-17 review (registry concedes "outstanding") | REPRODUCED |
| A4 | Only screen is the warning-only W04 census; rule 17 excludes it | REPRODUCED |
| A5 | Rows lack resolvable prior-id linkage | REPRODUCED |
| A6 | S370/S365 merits arguable; P06/P15 held-adjacent | REPRODUCED |
| A7 | S373 duplicates S162's account in census-invisible form | REPRODUCED |
| A8 | S371/S367 clean on merits | NOT REPRODUCED |
| A9 | S372 no collision | n/a |
| A10 | Counter green cannot certify this; slug mismatch at integration | REPRODUCED |

Falsifier found: not for the C2 predicate itself — the rows are new rows with this-round
receipts, and rule 17 forbids inferring duplication from URL equality alone ("URL equality
alone neither admits nor rejects a row", RegistryContract). Control verified: the QUALITY17
distinct-scope review is REQUIRED and demonstrably NOT performed before admission. That is a
fixable defect against the round's Gate contract (lesson Gate: "Review source URL collisions
against prior rows before appending"), not an automatic kill of C2.

## Smallest safe correction

1. Perform the review now, before any commit of the working-tree landing: per pair, record
   prior-id linkage (S370→S365, S371→S367, S373→S364), region disjointness (measured above),
   scope-wording overlap (A6), and the S162 held-account adjacency of P07 (A7).
2. Record the outcome in the lesson Gate (`corpus/lessons/round-52.md`) and add resolvable
   prior-id markers to the row teaches cells (or a Gate-line old→new log per the SOURCES
   contract `corpus/SOURCES.md:3-7` and the r51 Gate precedent) — recording, not row removal.
3. Keep the counter's informational `pins_prior_equal`; do not extend the counter to judge
   scope — rule 17 assigns that to human review. Fix the ENTRY slug constant at integration.

## Limitations

- Source-only seat: no network, so the r52 fetch receipt (`fetch/README.txt`, SHA256SUMS) is
  taken as the lane's record; I verified byte-identity to r51 pins, not the network act.
- Proposition quotes were not re-audited here (W1 C2PinAudit did); this seat attacks the row
  collision/scope control only.
- No source-truth judgment (non-author boundary); A6/A7 state overlap facts, not falsity.
- r39 precedent read from lane registration files; I did not trace how the earlier same-URL
  pairs (S307/S320, S303/S317/S368) were reviewed in their own rounds.
- Scratch `/fast/scratch/hyaku/mado-r52/Attack26` used for comparison scripts; removed on exit.
- No installs; no tracked, fleet, or sibling writes; no git/jj mutation.
