# R54Seat16 — adversarial attack on frozen PRED-C1-r54 (do-nothing reachability, control-set completeness, scored-invocation operability)

Seat: R54Seat16 (item 16, w1, reviewer/attack share). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base under attack: `e25149fec8152a3aabd2b18a0ee8663b23cf65aa` (`git rev-parse HEAD` → same; read-set clean: `git status --porcelain -- corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md .ufo/waves/round-52/fetch` → empty).
No installs or updates (python3 3.14.8, git 2.56.0 as found). No lane tracked edits; no fleet/sibling/source-repo writes; no git/jj mutation outside the scratch fixture; scratch `/fast/scratch/hyaku/mado-r54/R54Seat16` removed before yield (this report is self-contained).

## Axes

Coverage — does the frozen control set actually cover clause (c) of the predicate? Operability — can the frozen scored invocation be executed honestly under the declared scratch fences? Honesty — does the §9 do-nothing control hold at the level of the frozen predicate sentence, or only at the level of an extra-receipt process?

## Attacked predicate (unchanged, quoted)

`claims-frozen.md:19-30`: `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>` prints `MADO_ERRATA_TRUTH: rev=<rev> propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET` and exits 0 only if … (c) each of the four pins' bytes hash to the round-52 recorded sha256, and (d) each of the six frozen C1 controls of `registration.md` is rejected by the counter. Kill rule `claims-frozen.md:37-39`; do-nothing control §9 `claims-frozen.md:41-44`; control definitions and required verdicts `registration.md:36-47`; counter form `registration.md:49-53` (`--work <dir>` honours the scratch rule (no `/tmp` hardcode); control = a mutated copy of the scored tree, `registration.md:36-38`).

No predicate, control, fixture, or frozen file was changed. The counter `quality/counters/c1-r54-errata-truth.py` does not exist at base (`receipts/before.txt`: `r54 counters present: 0`), so all attacks are run against reference counters I wrote in scratch, driven by real git fixtures — the findings are contract-level and judge-independent (F1's do-nothing counter reads nothing; F2 depends only on the pin leg and table fidelity; F3 is about scratch location).

## F1 — HIGH: the do-nothing counter reaches the frozen target line in the single scored invocation; `controls=6/6` is self-attested

The predicate sentence constrains only what the scored invocation prints on the good tree. An always-print counter emits the byte-exact frozen line with exit 0 without reading one git object — and also emits it on every control tree. §9 (`claims-frozen.md:41-43`) says such a counter "accepts them → controls<6/6", but that is not what the counter prints: it prints `controls=6/6` unconditionally. The count only becomes falsifiable if the scoring process performs six additional receipt runs and reads their verdicts — a step that lives in the receipt protocol (`claims-frozen.md:44`, `registration.md` honesty rules), not in the predicate sentence. Seat18 asserted the opposite ("a counter that emits the target line without reading the selected revision cannot satisfy controls=6/6", `R54Seat18.md` §Do-nothing) at contract level without observing the self-attestation mechanism; executed here, the printed line says `6/6` on all seven mutated trees.

Answer to the assignment's reachability question: **do-nothing reaches target in the scored invocation.** It is dead only under the receipt protocol (six external runs, each printing `TARGET_MET` → kill rule fires). Whether the round is safe therefore depends on a process convention the freeze does not state: the scored line's `controls` leg is attested either by the counter running its own six controls in-process (which forces F3), or by external receipt runs (which makes the printed `6/6` a lie no invocation can detect). Executed evidence (R1a/R1b below): `dn.py` prints the frozen line, `exit=0`, on base and on ctl1–ctl6 and coll.

Closure (L1 decision, pre-data v2 or receipt contract — recommendation only): state explicitly that clause (d) must be evaluated in-process during the scored invocation and that the scored line's `controls` counts must equal the number of frozen controls the counter itself constructed and rejected; and/or fix the receipt format so each control receipt carries the required per-leg verdict shape (below) so a receipt checker can bind receipts to `registration.md:40-47`.

## F2 — HIGH: the six frozen controls cannot enforce clause (c); the two natural single-oracle pin legs fail the contract in opposite directions

Clause (c) says the pins must hash to the round-52 recorded sha256. The only in-tree record of those digests is `.ufo/waves/round-52/fetch/SHA256SUMS` — a mutable tree object the counter itself reads from `--rev`. Three reference pin legs, all executed (R4, R5, R6):

1. **Manifest-only (single-legged).** Passes all six frozen controls with the required leg shapes (R4: ctl1 `quotes=3/4`, ctl2 MISSED, ctl3 `pins=3/4`, ctl4 MISSED, ctl5 `propositions=3/4`, ctl6 `quotes=3/4`) — yet prints `TARGET_MET exit=0` on the collusive tree (ConfigActions.cpp tampered by one appended line outside every quote/anchor, manifest digest updated consistently): `propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET`. This executes, against a real counter, the input Seat18 specified but did not run (`R54Seat18.md`, "coordinated digest substitution"). No frozen control mutates pin bytes at all, so the minimal contract-compliant counter admits a clause-(c) violation.
2. **Frozen-digest-only.** On the CTL-3 tree it prints `pins=4/4 … verdict=TARGET_MET` (R5): CTL-3 changes only the manifest, so a counter bound to the frozen digests cannot produce CTL-3's required verdict `pins≤3/4` (`registration.md:44`) — the control is admitted by construction. This refines Seat26's guidance ("compare against the frozen digests as well as the revision's manifest", `R54Seat26.md:178`): "as well as" is mandatory; "instead of" is fatal. It also bounds Seat35's D5 note that CTL-3 is "caught either way" (`R54Seat35.md:117`): true only for manifest-reading oracles; the frozen-digest-only oracle is a third way that does not catch it.
3. **Frozen-digest-only with honest in-process controls.** Dies honestly on the good tree: its own CTL-3 self-control yields `pins=4/4` (accepted) → `controls=5/6 … TARGET_MISSED exit=1` (R6). The most literal implementation of clause (c) is itself killed by the control set that clause (d) tells it to satisfy.

Consequence: the only counter shape that satisfies the whole frozen contract must bind the manifest to the frozen digests AND the pin bytes to the manifest (two-legged). The freeze permits that shape but no frozen control requires it, and one of the two single-oracle variants passes all six controls while violating clause (c) in substance. The control set is one control short: a seventh control applying the consistent pin+manifest rewrite and requiring `MISSED` (any leg) would force the binding leg. Alternatively the counter form (`registration.md:49-53`) could state the two-legged requirement explicitly. Recommendation for L1 only; predicate untouched by this seat.

## F3 — MEDIUM: the frozen scored invocation carries no `--work`; an honest clause-(d) evaluation has no legal default scratch location

If clause (d) is evaluated in-process (the reading that makes F1's self-attestation honest), the scored invocation `python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>` must construct six mutated git trees at run time (each control is a mutated copy of the scored tree, `registration.md:36-38`). The frozen form passes no `--work`, and `registration.md:50-51` forbids a `/tmp` hardcode. Executed with the only repo-relative default (`<repo>/.c1-r54-work`), the scored invocation mutates the scored repository itself (R3a/R3b: `git status --porcelain` of the fixture goes from empty to `?? .c1-r54-work/`) — in the lane that writes outside the wave fence and pollutes the tree being scored; a `/tmp` default is a forbidden hardcode; a counter that refuses without `--work` cannot print the frozen line at all. With explicit `--work` outside the repo the same counter prints `TARGET_MET` and pollutes nothing (R2a-ctl) — the defect is in the frozen invocation form, not in the concept. Closure: add `--work <dir>` (or an explicit sanctioned default) to the scored form in a v2 freeze, or adopt the receipt-external reading — which then makes F1 the binding constraint.

## Executed matrix (verbatim; full log was `matrix.log` in scratch, now removed)

Fixture: read-set-only git repo built from committed base blobs (`git archive e25149fe -- corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md .ufo/waves/round-52/fetch`), `mktemp -d` under the designated scratch, toplevel asserted before commit; base + 8 child revs, each differing from base by exactly one mutation built via temp-index + `commit-tree` (ctl1–ctl6 exactly per `registration.md:40-47`; coll = Seat18's consistent pin+manifest rewrite, tamper appended at EOF so all quotes/anchors/line counts survive). Read-set simplification declared: the fixture carries exactly the C1 read-set, which is all the predicate, the six controls, and both reference counters read; committed-tree blob totals (25,318 blobs, ~349 MB) made full-tree duplication per control pointless.

```
=== R1a dn.py on BASE (do-nothing, scored invocation)
MADO_ERRATA_TRUTH: rev=7b8d5ed3de992470dc74ff69ffab42ffd9acc43f propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
--- exit=0
=== R1b dn.py on ctl1..ctl6,coll (7 runs, identical output shape per rev)
MADO_ERRATA_TRUTH: rev=<ctl-rev> propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
--- exit=0        (ctl1 fe88f2df, ctl2 a941be9a, ctl3 d84d59d6, ctl4 f33454de, ctl5 d49df87b, ctl6 f75ddd7b, coll 407a67ac)
=== R3a fixture status BEFORE mc1 default-work run
(empty)
=== R2a mc1.py on BASE (honest (a)-(c), in-process (d), default work dir <repo>/.c1-r54-work)
MADO_ERRATA_TRUTH: rev=7b8d5ed3de992470dc74ff69ffab42ffd9acc43f propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
--- exit=0
=== R3b fixture status AFTER mc1 default-work run
?? .c1-r54-work/
=== R2a-ctl mc1.py on BASE with explicit --work (outside repo)
MADO_ERRATA_TRUTH: rev=7b8d5ed3de992470dc74ff69ffab42ffd9acc43f propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
--- exit=0        (no repo pollution)
=== R4 base    mc1.py --no-self-controls (manifest-only pin leg)
… pins=4/4 … verdict=TARGET_MET   exit=0
=== R4 ctl1    … quotes=3/4 anchors=3/4 pins=4/4 … TARGET_MISSED  exit=1   (required: quotes≤3/4 ✓)
=== R4 ctl2    … quotes=3/4 anchors=3/4 … TARGET_MISSED          exit=1   (quote not at anchor ✓)
=== R4 ctl3    … pins=3/4 … TARGET_MISSED                        exit=1   (required: pins≤3/4 ✓)
=== R4 ctl4    … quotes=3/4 anchors=3/4 … TARGET_MISSED          exit=1   (side-claim fails ✓)
=== R4 ctl5    … propositions=3/4 quotes=3/4 anchors=3/4 … MISSED exit=1  (required: propositions≤3/4 ✓)
=== R4 ctl6    … quotes=3/4 pins=4/4 … TARGET_MISSED             exit=1   (quote absent from swapped pin ✓)
=== R4 coll    … propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 … TARGET_MET  exit=0   ← clause-(c) violation admitted
=== R5 base    mc1.py --pins-oracle frozen --no-self-controls … TARGET_MET exit=0
=== R5 ctl3    … pins=4/4 … verdict=TARGET_MET                   exit=0   ← CTL-3 admitted; required pins≤3/4 unproducible
=== R6 BASE    mc1.py --pins-oracle frozen WITH in-process controls
… pins=4/4 controls=5/6 verdict=TARGET_MISSED                    exit=1   ← literal clause-(c) oracle dies on the good tree
```

Reference-counter inputs and the frozen table were taken byte-for-byte from `registration.md:14-19,25-45` (pin digests independently re-hashed from the worktree and equal to the recorded values: `a83abeb5…`, `746c6f51…`, `8d8f35fc…`, `7248cbb8…`, matching `SHA256SUMS`). Note on the quote judge: mc1 uses whitespace-collapse + blank-drop + exact span equality (Seat34's "v4") to resolve quotes 4/4 on the good tree; under the literal frozen judge (`registration.md:51-53`) quotes resolve 1/4 (Seats 15/34/35) — that pre-existing defect is not mine and does not touch F1–F3 (dn.py is judge-independent; F2 is pin-leg/table-level; F3 is scratch-location-level).

## Distinctness from sibling seats

Primary item here — do-nothing self-attestation in the scored invocation, the `--work`-absent invocation form, and the executed three-oracle pin-leg contradiction — has no sibling coverage (grep over `.ufo/waves/round-54/w1` for `--work|self-attest|unconditional|always-print|controls=6/6` hits only Seat26's counter-authoring guidance and Seat28/35's "not exercised" notes). Secondary: I executed Seat18's unexecuted collusive recipe (attributed) and exhibit the frozen-digest-only oracle that Seat35's "caught either way" and Seat26's recommendation do not cover. Seat24/25's mutation runs were blocked by the absent counter; my reference counters unblock that class of test for w2.

## Residual risk and verification gaps

- All results are reference-counter behavior on a read-set fixture, not the (absent) production counter; w2 must re-run the matrix against the landed `c1-r54-errata-truth.py` with the same nine revs.
- Receipt faithfulness is unenforced by anything committed: a counter's self-built control trees could differ from `registration.md:40-47`'s mutations and reject for the wrong reason. My per-leg shapes make receipt checking possible; nothing currently does it.
- The fixture's exported blobs were verified clean against the lane (`git status --porcelain` empty over the exported paths; worktree==git-object equality previously established by Seat34 F1), but the fixture is not byte-complete for paths outside the C1 read-set.
- Seat15's untracked-freeze finding stands independently: `claims-frozen.md`/`registration.md` and the round-54 pins are untracked at base, so no `--rev`-reading counter can treat this freeze as history.
- Not exercised here: `--selftest`, C2 in any form, `mado-verify.sh --selftest` (main-agent surface), network or upstream re-fetch.

## Tool report

No tool installed or updated; no package query. Used preinstalled python3 3.14.8 (`-I`), git 2.56.0 (read-only against the lane; init/commit only inside the scratch fixture with toplevel asserted), tar, sha256sum, coreutils. Host guard respected: no writes outside this report and `/fast/scratch/hyaku/mado-r54/R54Seat16` (removed); nothing in `~/.local/bin` or any PATH dir touched.

## Report trailer

Lane-relative report: `.ufo/waves/round-54/w1/R54Seat16.md`. No predicate, control, fixture, or frozen file changed. Scratch cleaned before yield.
