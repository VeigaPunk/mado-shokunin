# Round 54 — frozen claims (mado, hyaku run 10, attempt 1)

Frozen 2026-10-27 before any wave dispatch; base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`.
This freeze answers routed defect 1 of the round-53 closure (M53-4: pre-data
control freeze omitted). No predicate, control, fixture or target in this file
changes after any seat has scored; a falsified predicate is an honest stop or a
pre-data re-registration under a NEW versioned file, never an edit of this one.

Axis scores at base: every published axis ties at its maximum under the bounded
rubrics (`receipts/before.txt`), so each owned axis is a lowest axis
(`AXES.md` stagnation nudge does not apply; a capability entered round 51).

## C1 — operability (record-instrument capability): errata source-truth verifier

**Surface the claim moves:** the lane's record instruments over its own
sourced entries (no desktop surface; PROVINCE.md round-36 boundary: record
instruments score the lane's paperwork, never a compositor).

Predicate (PRED-C1-r54, frozen sentence; the same sentence is the counter's
contract and the report label): `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>`
prints one line `MADO_ERRATA_TRUTH: rev=<rev> propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET`
and exits 0 only if, at the scored revision, (a) each of the four corrected
propositions P19–P22 of `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`
has its Quote cell occurring verbatim and contiguous in the round-52 pin named
by its Pin:anchor cell, (b) each anchor side-claim holds (P19 at exactly
ConfigActions.cpp:1554-1558; P20 at exactly :1576; P21 at exactly
DispatcherTranslator.cpp:619-622 inside lines 591–627; P22 at exactly
:573-574 after line 571), (c) each of the four pins' bytes hash to the
round-52 recorded sha256, and (d) each of the six frozen C1 controls of
`registration.md` is rejected by the counter.

Before (base `e25149fe`): no `c1-r54-*` counter exists — `ls quality/counters | grep -c r54` → 0;
the predicate is TARGET_MISSED by absence (`receipts/before.txt`).
Target: the counter committed and the frozen line with `verdict=TARGET_MET` at
the round's final content revision.

Kill rule: if any frozen C1 control is admitted by the counter, or any real pin,
quote, or anchor mis-verifies, the counter prints `verdict=TARGET_MISSED` and a
non-zero exit — the claim is dead for the round and reported honestly.

Do-nothing control (§9): a counter that prints the frozen line without reading
git objects fails the six control runs (each control is a mutated tree the
counter must reject; an always-print counter accepts them → `controls<6/6`).
Receipt: the counter's own control run is committed per control.

## C2 — coverage (sourced entry): `uwsm-app`'s environment on the owned chain

**Surface the claim moves:** the P1/P6 owned chain's launcher half — the
omarchy/Hyprland `exec-once`/`bindd` lines launch every autostart app, the
terminal binding and the idle re-arm through `uwsm-app`; the coverage map's
frontier names "`uwsm-app`'s environment" open since round 47. This is NOT
r52-correction ground (round-53 planned row 2: no coverage claim from the
correction plane).

Predicate (PRED-C2-r54, frozen sentence): `python3 -I quality/counters/c2-r54-uwsm-entry.py --repo . --rev <rev>`
prints one line `MADO_UWSM_ENTRY: rev=<rev> admitted=1/1 rows=3/3 controls=6/6 verdict=TARGET_MET`
and exits 0 only if, at the scored revision, (a) `corpus/knowledge/uwsm-app-environment-r54.md`
exists, is indexed by `corpus/README.md`, and opens with the provenance trio
(`source:`, `verified-at:`, `recheck:`) citing rows S375, S376 and S377 of
`corpus/SOURCES.md`; (b) each of those rows is `mined`, `opened` 2026-10-27,
carries a URL pinned at commit `0727985c9bae655bda488f87f99ea69a6ac1c003`, and
its `teaches`/quote cell's located quote (≤25 words) occurs verbatim in the
round-54 pin named by its source file; (c) the entry carries at least two host
join citations among the frozen host set of `registration.md`; and (d) each of
the six frozen C2 controls of `registration.md` is rejected.

Before (base `e25149fe`): entry absent (`ls corpus/knowledge | grep -c r54` → 0), rows S375–S377 absent (last registry row S374), predicate TARGET_MISSED by absence (`receipts/before.txt`).
Target: entry and rows committed, indexed, frozen line `verdict=TARGET_MET` at the round's final content revision.

Kill rule: any forged control admitted, any real row/quote/host-join
mis-verified → `verdict=TARGET_MISSED`, non-zero exit, honest stop.

Do-nothing control (§9): a recycled round-47 entry text with a new title fails
clause (b) (its rows' quotes are not uwsm quotes) and clause (c); a stub entry
fails (a); an entry citing S999 fails the registry leg of (b). Receipt per control.

## Causal separability

C1 reads only `quality/counters/c1-r54-errata-truth.py`,
`corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`,
`.ufo/waves/round-52/fetch/` (+SHA256SUMS) and the frozen table of this file.
C2 reads only `quality/counters/c2-r54-uwsm-entry.py`,
`corpus/knowledge/uwsm-app-environment-r54.md`, `corpus/README.md` (its row),
rows S375–S377 of `corpus/SOURCES.md` and `.ufo/waves/round-54/fetch/`.
Shared record files (README registry table, SOURCES.md, lesson, LOG, SCORECARD)
are integration surfaces, not claim evidence.

## Harm watch (frozen)

`bash tools/mado-verify.sh --selftest` stays 460/460; the navigation counter
stays complete (69/69 → 70/70 after the C2 index row, never fewer); the sources
census stays exit 0; no config tree, compositor, service or sibling repo is
written; `.ufo/waves/round-54/` seats write wave-dir reports only.

## Exploratory claims

None. Both claims are counting-claim claims.
