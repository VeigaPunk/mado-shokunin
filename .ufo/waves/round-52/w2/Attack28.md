# Attack28 — round 52 w2 attack on C2 held overlap and source novelty

Seat: `Attack28` (attack, leaf; no subagent dispatch). Wave `w2`, round 52.
Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`. Frozen base
`85d57a818c3707397e21c840b6498b105ba798aa`. Target of this seat: **C2 held overlap and source
novelty** — attack each frozen claim/counter/source premise by concrete test or source evidence.
No claim or predicate edits; no tracked lane writes; no git/jj mutation in the lane (one fixture
clone committed only under my own scratch); no package queries, live reads, probes, screenshots,
producer execution, or host mutation. Not a vote; no non-author judgment is claimed — items
needing the frozen predicate's "independent non-author source-truth review" are named as pending.

## State attacked

The lane working tree has moved since w1 (git status at observation time): staged/uncommitted —
`corpus/SOURCES.md` (+S370-S373), `corpus/README.md` (+index row),
`corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (new, untracked, 32 lines, 18 propositions
P01-P18), `quality/counters/c2-r52-proposition-entry.py` (new, untracked, 66 lines),
`quality/counters/c1-r52-ledger.py`, `quality/tool-ledger.md`, `corpus/lessons/round-52.md`.
The landed entry slug is `hyprland-synthetic-dispatch-r52` — **not** the w1 draft slug
`hyprland-synthetic-key-dispatch-r52`. All findings below bind to those bytes as observed
(2026-10-27 ~11:16-0300). Pins for both the landed entry and the w1 draft live at
`.ufo/waves/round-52/fetch/` and `.ufo/waves/round-52/w1/C2EntryDraft/fetch/` respectively.

Method: every contested proposition quote was re-checked mechanically against the round-52 fetch
pins (whitespace-collapsed and raw substring at the cited line span); held-overlap claims were
re-derived from the held corpus at base; counter behavior was tested in a scratch clone
(`/fast/scratch/hyaku/mado-r52/Attack28/clone`, fixture rev `30d1d03…` = base + landed files
copied and committed there; clone top-level asserted before commit).

## Attack items

### H1 — Landed P06 is a held-fact re-anchor of round-51 step 7 (reproduced)

- **Attacked:** landed entry P06 ("`sendshortcut` requires exactly three fields", S370,
  `Hyprland-legacy-DispatcherTranslator.cpp:531-535`, quote `CVarList2 ARGS(args, 3); if
  (ARGS.size() != 3)`) as "new ground" toward the frozen predicate's ≥4 substantive propositions.
- **Reproduction:** `sed -n '203,204p' corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` at base
  — step 7 already states "`sendshortcut` demands exactly three comma-separated fields and rejects
  anything else `CVarList2 ARGS(args, 3);` / `if (ARGS.size() != 3)`
  (Hyprland-legacy-DispatcherTranslator.cpp:532-535)". Quote fragments identical; anchor :531-535
  vs :532-535 (draft widened by one line for the function signature). My pin check: quote
  whitespace-collapsed-OK at :531-535.
- **Outcome:** same fact, same code fragments, same file, held at base via S365. Only the row id
  (S370) and anchor width are new. TRUE and well-anchored, but not new coverage.
- **Verdict: reproduced** (C2Novelty N3 confirmed independently against the landed artifact).

### H2 — Landed P07 restates held `stringToModMask` mechanism; the draft's new-scope sharpening was lost (reproduced)

- **Attacked:** landed P07 ("`stringToModMask` uppercases input and checks known modifier names
  using substring membership", S373, `Hyprland-KeybindManager.cpp:221-225`) as new coverage; also
  attacked the staged S373 row scope ("`stringToModMask` source behavior") as a fresh row.
- **Reproduction:** `sed -n '44p' corpus/knowledge/bind-table-r25.md` — held line (S162): "describes
  `stringToModMask` as uppercasing then substring-matching tokens, making token order immaterial".
  `grep -n stringToModMask corpus/knowledge/hyprland-bind-key-match-r50.md` — held line 66 cites
  the `mods.contains("MOD4")` … family at KeybindManager.cpp:236 (same function, held by the r50
  key-match entry). The w1 draft's P07 had been sharpened to the sendshortcut-path consequence
  (silent mask 0, no rejection branch on this path); the landed P07 reverted to the bare mechanism
  statement with no sendshortcut-specific consequence.
- **Outcome:** the mechanism proposition is held ground from round 25 (S162) and round 50; S373's
  scope ("stringToModMask source behavior") overlaps held S162/r50 ground. The distinct-scope
  question this raises is exactly criterion 17's review case (see N3 below).
- **Verdict: reproduced.**

### H3 — Landed P15 is a held partial restatement; quote covers only the save, not the restore (reproduced)

- **Attacked:** landed P15 ("`sendkeystate` saves the prior `m_passPressed` value before changing
  it", S370, quote = the save line `const int oldPassPressed = …` at :612) as new coverage.
- **Reproduction:** r51 step 6 at base (`sed -n '197,198p' corpus/knowledge/hyprland-dispatcher-dispatch-r51.md`)
  already holds "`sendkeystate` is the one dispatcher that writes the field itself, **saving and
  restoring** it around its work". Round-51 w2 review `.ufo/waves/round-51/w2/RevC2EntryTruth/entry-truth.md:55`
  already recorded "sendkeystate save/restore is translator `:612-24`". Pin read
  (`sed -n '610,626p'` of the round-52 fetch): save :612, restore :624. The landed proposition
  narrowed to the save only; the quote contains no restore.
- **Outcome:** fact family held since round 51 (admitted text + w2 review note); the landed binding
  quotes half of the held fact. New as an admitted-entry binding; not new ground.
- **Verdict: reproduced.**

### H4 — Landed P17 misattributes the repeat double-call to `sendshortcut`; P04 and P17 double-count one fact (reproduced)

- **Attacked:** landed P17 ("`sendshortcut`'s repeat branch can invoke its delegate twice for a
  successful repeat state", S370, `Hyprland-legacy-DispatcherTranslator.cpp:619-622`).
- **Reproduction:** `sed -n '610,626p' .ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp`
  — :619-622 sits inside `sendkeystate` ("But sendkeystate overrides m_passPressed. Let's just call
  through sendshortcut with the proper state set." :610-611). The repeat-guarded second
  `sendshortcut(modifiedArgs)` call is `sendkeystate`'s delegation; `sendshortcut` itself has no
  repeat branch and no delegate. Landed P04 states the same fact, correctly attributed
  ("`repeat` calls its delegate again only after a successful first call", same anchor :619-622).
- **Outcome:** as worded, P17 asserts a `sendshortcut` repeat branch that does not exist in the pin
  (the quote shows `sendkeystate` calling `sendshortcut` twice). One new fact is counted twice, and
  one of the two statements is misattributed. This is a source-truth defect inside a material
  proposition — a live sample of the M51-2 class for the pending outside reviewer.
- **Verdict: reproduced.**

### H5 — Landed P16's quote is not verbatim at its locator under either comparison policy (reproduced)

- **Attacked:** landed P16 ("The action sends modifier state before the key event, then clears the
  modifier state", S371, locator `Hyprland-ConfigActions.cpp:1554-1558,1576`, quote =
  `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager->sendKeyboardKey(S.m_timeLastMs,
  key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);`).
- **Reproduction:** mechanical check of all 18 landed quotes against
  `.ufo/waves/round-52/fetch/` (script in scratch, since removed): 17/18 whitespace-collapsed OK;
  P16 FAILS even collapsed — the two quoted calls are separated in the pin by
  `if (S.m_passPressed == 1) { if (!isMouse)` (:1555-1557), and the PRESSED send at :1558 fires
  only in that branch. Independent confirmation: the w1 full-strength counter reports
  `P16:quote_not_at_pin` against the landed fixture (see C2 below). `quotes_raw=6/18` on the
  landed set; P14 fails a raw line-contains check (internal spacing of `uint32_t    m_timeLastMs
  = 0;` at hpp:117).
- **Outcome:** a material proposition in the landed entry fails the frozen predicate's "exact
  located quote" requirement as staged; the proposition also omits the `m_passPressed == 1` branch
  condition the quote depends on.
- **Verdict: reproduced.**

### H6 — Subject distinctness of the landed entry (not reproduced as a defect; held overlap bounded)

- **Attacked:** the frozen phrase "a distinct Hyprland dispatcher-execution mechanism" against the
  held map (r25 wiki/describe, r26 vocabulary/request grammar, r50 key match, r51 map/parse/press/
  submap/socket).
- **Reproduction:** compared landed subject (manufacture/delivery of a synthetic seat event by
  `sendshortcut`/`sendkeystate`) against the four held entries' subjects; re-ran the held-token
  comparison for P06/P07/P15 above.
- **Outcome:** subject distinctness holds; the held overlap is proposition-level, not
  subject-level. Net new-ground propositions in the landed entry: P01,P02,P03,P05,P08,P09,P10,P11,
  P12,P13,P14,P16,P18 = 13 of 18. The frozen ≥4 predicate is met on new ground alone even after
  H1-H3 removals — the claim is not falsified, but the coverage delta is inflated by 3 held items
  plus the P04/P17 double-count.
- **Verdict: not reproduced as a defect** (distinctness defensible; inflation real but not
  claim-fatal). Consistent with C2Novelty and C2SourceRecon w1 verdicts.

### N1 — The frozen predicate still has no novelty/distinctness clause (reproduced)

- **Attacked:** the frozen C2 predicate's silence on overlap; the w1 claim that round-51's shingle
  clause was dropped.
- **Reproduction:** `.ufo/waves/round-52/receipts/c2-base.txt` (old r51 counter at base) prints
  `body_shingles=3364 files=66+cand3 max=0.1%` — the r51 instrument carried a lexical-overlap
  clause; `grep -c shingle quality/counters/c2-r52-proposition-entry.py` → 0 (landed counter has no
  overlap/freshness-vs-base logic at all; see C3). The r52 frozen text names only proposition
  count, row/pin/quote bindings and index.
- **Outcome:** distinctness rests entirely on seat judgment; a subject-overlapping entry passes the
  frozen counter mechanically. Structural, not draft-specific.
- **Verdict: reproduced.**

### N2 — "Sources opened this round" is a re-fetch ceremony: all four pins byte-identical to round-51 (reproduced)

- **Attacked:** the frozen predicate phrase "grounded in sources opened this round" as satisfied by
  the landed pins.
- **Reproduction:** `sha256sum .ufo/waves/round-52/fetch/Hyprland-*` vs
  `.ufo/waves/round-51/fetch/SHA256SUMS`: ConfigActions.cpp `a83abeb5…` EQUAL, ConfigActions.hpp
  `746c6f51…` EQUAL, KeybindManager.cpp `8d8f35fc…` EQUAL, legacy-DispatcherTranslator.cpp
  `7248cbb8…` EQUAL (4/4). The staged S372 hpp URL has no registry row at base
  (`git show 85d57a8:corpus/SOURCES.md | grep -c ConfigActions.hpp` → 0) but the hpp bytes were
  already pinned in round 51's manifest (r51 entry pin table, row cell S367). Both round-52 fetch
  dirs (draft 10:03, lane root 10:47) match the round-51 manifest.
- **Outcome:** every byte the entry stands on was first opened in round 51 (or round 50 for
  KeybindManager.cpp, S352/S353); this round's opens are re-reads of immutable-commit URLs. A
  genuine URL read did occur in-round (fetch/README.txt, verify receipts), so a literal reading of
  "opened" is met; the *evidence* is not new. The predicate gives the counter no way to surface
  this beyond what the receipt already prints.
- **Verdict: reproduced.**

### N3 — QUALITY17 distinct-scope review for S370/S371/S373 is outstanding by the lane's own record (reproduced)

- **Attacked:** the staged rows' admissibility under `corpus/QUALITY.md:34` (criterion 17:
  repeated canonical URLs across active rows require explicit overlapping-scope review;
  "send distinct-scope reuse to human review").
- **Reproduction:** staged `corpus/SOURCES.md` search log states verbatim: "S370, S371 and S373
  reuse canonical URLs with new scopes; **distinct-scope review remains outstanding**."
  `.ufo/waves/round-52/census-after.txt` records `W04 S370/S371/S373 duplicate url … across
  scopes` for all three. Scope comparison at base: S365 = "how CDispatcherTranslator::run resolves
  a dispatcher name … and how implementations parse arguments" vs S370 = "sendshortcut and
  sendkeystate source-level argument parsing/key resolution" (S365's scope text generically covers
  per-dispatcher parsing; line ranges disjoint :30-35,797-867 vs :531-627). S367 = "what the
  submap dispatcher does to current submap state" vs S371 = "synthetic key and modifier delivery
  call order" (disjoint :1664-1682 vs :1530-1616). S364 = map population/press-time call vs S373 =
  "`stringToModMask` source behavior" (overlaps held S162/r50 ground per H2).
- **Outcome:** the lane's own paperwork admits the review criterion 17 mandates has not happened;
  until it does, the row admission is incomplete and H2's S373 scope question is undecided.
- **Verdict: reproduced.**

### N4 — Date-based freshness is indistinguishable: S364-S369 are also dated 2026-10-27 at base (reproduced)

- **Attacked:** any "opened this round" check keyed on the registry date column.
- **Reproduction:** `git show 85d57a818c3707397e21c840b6498b105ba798aa:corpus/SOURCES.md | grep
  "^| S36[4-9]"` — all six round-51 rows carry `mined | 2026-10-27`. The staged S370-S373 carry
  the same date.
- **Outcome:** a date-keyed freshness check accepts reused round-51 rows and cannot discriminate
  the round-52 rows; only row-id-vs-base absence is discriminative (implemented in the w1 draft
  counter's clause (c); absent from the landed counter, see C3).
- **Verdict: reproduced.**

### C1 — The w1 counter's r-green proves a separate synthetic fixture only, not landing (reproduced)

- **Attacked:** any reading of `w1/C2CounterDraft/receipts/r-green.txt` as evidence the C2 target
  is reachable on real lane bytes.
- **Reproduction:** receipt meta line: `rev=ae2efe0962dd69825dce67b4b8634f9c67f883a8`,
  `entry=corpus/knowledge/hyprland-dispatcher-action-effects-r52.md` — a scratch fixture revision
  and a third slug, five propositions over one pinned file in the counter's own grammar.
- **Outcome:** r-green demonstrates the counter's satisfiability on its own fixture; it says
  nothing about the w1 draft or the landed entry. The separate receipt `r-draft-as-is.txt`
  (TARGET_MET on the draft) does not transfer to the landed slug/shape either (C2, C4).
- **Verdict: reproduced.**

### C2 — The full-strength w1 counter rejects the landed state 3/5 clauses (reproduced)

- **Attacked:** the premise that the landed rows+entry would pass the counter the w1 evidence
  chain converged on.
- **Reproduction:** in the scratch clone (fixture rev `30d1d03…` = base + landed entry, staged
  SOURCES/README, round-52 fetch dir): `python3 -I .ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py
  --repo clone --rev 30d1d03… --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md --work w5`
  → `clauses_met=2 verdict=TARGET_MISSED exit=1` with:
  - clause (c) `rows_bound=0/18`: `anchor_no_fetch_root` on every proposition — the staged rows'
    anchor cell reads "… @ efb50993…; r52 fetch SHA256 7248…" and never names the round's fetch
    path, which the w1 counter requires;
  - clause (d) `quotes_bound=17/18`: `P16:quote_not_at_pin` (independent of my H5);
  - clause (e): `id_not_referenced` — proposition ids appear only inside the map, not in body
    prose (the w1 draft had a "What the evidence licenses" table referencing P01-P18; the landed
    32-line entry does not).
- **Outcome:** the strongest available counter does not credit the landed state as staged; either
  the rows' anchor format must gain the fetch path (and P16/id-references must be repaired), or
  the integration must record why the weaker committed counter supersedes.
- **Verdict: reproduced.**

### C3 — The committed (landed) counter does not isolate the "opened this round" control: fabricated-row bypass (reproduced — critical)

- **Attacked:** registration's frozen control story for C2 — "A no-work control at base must miss
  because target entry is absent" — and the implied corollary that a *work* entry crediting stale
  evidence must also miss. Premise: the new counter "checks proposition count, row/pin/quote
  bindings and index".
- **Reproduction:** in the scratch clone, starting from fixture `30d1d03…`: (i) reverted the entry
  to a 4-proposition table in the counter's own parse shape (`| P | S | claim | pin | anchor |
  quote | rationale |`) binding to base row S364 → counter reports `rowmeta:S364` ×4, TARGET_MISSED
  (the used-by string check bites); (ii) then appended a **fabricated** row S399 over the old
  KeybindManager.cpp URL with `mined | 2026-10-27 | used-by=<the r52 entry>` and re-pointed the
  four propositions at it → committed counter prints
  `C2_R52: props=4 rows=1 indexed=1 failures=0 verdict=TARGET_MET exit=0`.
  The four "quotes" (`exec` at :42) are not at their pins; the counter has no quote-at-anchor,
  no pin resolution, no base-absence/freshness comparison, no fetch-path requirement, no
  mapping-completeness or duplicate checks. Exact mutants and revisions:
  `ee45d86b…` (reused-row control, correctly rejected) and `15ea1773…` (fabricated-row bypass,
  wrongly accepted).
- **Outcome:** the committed PRED-C2-r52 instrument credits an entry whose "opened this round"
  evidence is a fabricated row id over a stale URL with today's date. The freshness half of the
  C2 control pair is unenforced; only entry-absence at base is enforced. This is the C2 analogue
  of the C1 lesson (a counter that does not isolate the required defect).
- **Verdict: reproduced.**

### C4 — The committed counter cannot credit the landed entry as landed (reproduced)

- **Attacked:** the operational premise that the committed counter scores the lane's own artifact.
- **Reproduction:** (a) default invocation:
  `python3 -I quality/counters/c2-r52-proposition-entry.py --repo clone --rev 30d1d03… --work w3`
  → `entry=absent verdict=TARGET_MISSED` — the `--entry` default is the **w1 draft slug**
  `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md`, not the landed slug. (b) with
  `--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md` on the fixture:
  `props=0 rows=0 indexed=1 failures=1 miss=props verdict=TARGET_MISSED exit=1` — the counter's
  proposition regex requires `| P<id> | S<row> |` in adjacent columns, but the landed table is
  `| ID | Proposition | Source row | Pin:anchor | Quote | Support | Why |` (S-row in column 3), so
  zero propositions parse. Base runs (both slugs, rev `85d57a81…`) correctly print
  `entry=absent verdict=TARGET_MISSED exit=1` — the no-work control does miss.
- **Outcome:** as committed, the counter neither targets the landed slug by default nor parses the
  landed table shape; someone must pass `--entry` correctly and the entry table must be re-shaped
  (or the counter re-written) before a TARGET_MET on real bytes is even expressible. Meanwhile C3
  shows the same instrument passes fabricated evidence.
- **Verdict: reproduced.**

## Consolidated verdict

- **Held overlap: reproduced, bounded.** Three landed propositions (P06, P07, P15) are held-fact
  re-anchors/restatements; P04/P17 double-count one fact and P17 misattributes it; P16's quote is
  not at its pin. Net new ground remains ≥13 propositions, so the frozen ≥4 predicate survives —
  but the as-staged coverage delta is inflated and two material propositions carry source-truth
  defects for the pending outside reviewer (P16 branch omission, P17 misattribution).
- **Source novelty: reproduced as a process gap, not a byte violation.** The in-round re-fetch is
  real and disclosed, but all four pins are byte-equal to round-51/50 pins, the date column cannot
  discriminate, S370/S371/S373 are duplicate-URL rows whose criterion-17 review the lane's own
  search log records as outstanding, and the committed counter cannot distinguish a fabricated
  fresh-dated row from a genuine open (C3).
- **Counter operability (in-scope as the C2 claim table's enforcement premise): both counters
  currently reject the landed state** (C2: 3/5 clauses on the full-strength instrument; C4:
  props=0 / wrong default slug on the committed one), **and the committed counter's freshness
  control is demonstrably bypassable** (C3). The w1 r-green fixture result does not bridge to
  landing (C1).
- Nothing here amends the frozen predicate; corrections are seat-side (reclassify P06/P07/P15,
  fix or split P16/P17, complete the criterion-17 review, repair row anchor format and counter
  regex/slug, add a base-absence freshness check) and process-side (commit the independent
  non-author per-proposition source-truth sample the predicate requires — as of observation,
  `corpus/lessons/round-52.md` itself records it as pending and warns against labeling any seat
  independent non-author).

## Limitations

- I did not run the counters against the real lane working tree: the counter reads only git
  objects at `--rev`, and the landed files are uncommitted; per the host guard I committed them
  only inside my scratch clone (clone top-level asserted). If integration revises the entry or
  rows after my observation time, C2-C4 and H1-H5 bind to the recorded bytes, not later ones.
- My source-truth sampling is mechanical (quote-at-anchor under two comparison policies) plus
  targeted region reads (P15/P16/P17); it is an attack seat's evidence, not the predicate's
  required independent non-author review, which remains pending by the lane's own record.
- The freshness bypass (C3) constructs a minimal entry in the counter's own grammar; it does not
  claim the landed entry is fabricated — it claims the instrument cannot tell.
- Line numbers are for the pinned bytes at `efb50993`; no network fetch was performed by this
  seat (all pins already local; identity verified by sha256 equality with the round-51 manifest).
- Scratch `/fast/scratch/hyaku/mado-r52/Attack28/` (clone fixture, work dirs, checker script) was
  used for all counter runs and removed on exit; no `/tmp` evidence, no installs, no package
  transaction, no lane write outside this report, no git/jj mutation in the lane.

## Evidence index (paths relative to lane root)

| item | evidence |
|---|---|
| landed entry | `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (untracked at observation) |
| staged rows/search log | `git diff corpus/SOURCES.md` (S370-S373 + "distinct-scope review remains outstanding") |
| index row | `git diff corpus/README.md` |
| committed counter | `quality/counters/c2-r52-proposition-entry.py` (66 lines) |
| pins | `.ufo/waves/round-52/fetch/SHA256SUMS` vs `.ufo/waves/round-51/fetch/SHA256SUMS` (4/4 equal digests) |
| held P06 source | `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:203-204` |
| held P07 source | `corpus/knowledge/bind-table-r25.md:44`, `corpus/knowledge/hyprland-bind-key-match-r50.md:66` |
| held P15 source | `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:197-198`; `.ufo/waves/round-51/w2/RevC2EntryTruth/entry-truth.md:55` |
| P16/P17 region | `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp:1550-1578`; `…/Hyprland-legacy-DispatcherTranslator.cpp:610-626` |
| base registry | `git show 85d57a818c3707397e21c840b6498b105ba798aa:corpus/SOURCES.md` (S364-S369 dated 2026-10-27; no S370+; 306 rows) |
| duplicate-URL screen | `.ufo/waves/round-52/census-after.txt` (W04 S370/S371/S373) |
| r51 overlap clause | `.ufo/waves/round-52/receipts/c2-base.txt` (`body_shingles=3364 … max=0.1%`) |
| r-green fixture | `.ufo/waves/round-52/w1/C2CounterDraft/receipts/r-green.txt` (`rev=ae2efe09…`, slug `…-action-effects-r52.md`) |
| pending review record | `corpus/lessons/round-52.md` ("outside non-author admit+reject sample remain pending") |
| fixture runs (scratch, removed) | clone rev `30d1d03…` = landed state; mutants `ee45d86b…` (reused row, rejected), `15ea1773…` (fabricated row, accepted) |

## Report

- `.ufo/waves/round-52/w2/Attack28.md`

```
seat=Attack28 wave=w2 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
claim=C2 coverage proposition-bound dispatcher source entry (held overlap + source novelty)
attacked=landed entry P06,P07,P15,P16,P17,P04; frozen phrases "distinct mechanism","opened this round"; QUALITY17 S370/S371/S373; committed counter freshness/binding premise; r-green landing premise
verdict=held overlap reproduced (P06/P07/P15 held re-anchors; P17 misattributed; P04/P17 duplicate; P16 quote not at pin); subject distinctness not reproduced as defect (13/18 new ground); source novelty reproduced as process gap (4/4 pins byte-equal to r51, date collision, criterion-17 review outstanding per lane's own search log); committed counter does not isolate freshness (fabricated-row bypass TARGET_MET 15ea1773) and rejects landed bytes (props=0, draft-slug default); full counter rejects landed state 3/5 clauses; r-green synthetic-only
receipts=none committed by this seat (scratch clone runs 30d1d03/ee45d86b/15ea1773, removed); lane receipts dir holds only c1-base.txt,c2-base.txt
report=.ufo/waves/round-52/w2/Attack28.md
```
