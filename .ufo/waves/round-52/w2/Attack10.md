# Attack10 — C2 new source row URL collision: QUALITY-17 distinct-scope review

Seat: `Attack10` (scout, leaf). Wave: round-52 w2. Date: 2026-10-27.
Target: the C2 source premise that new registry rows S370/S371/S373 — which reuse
canonical URLs already held by active rows S365/S367/S364 — were admitted with the
explicit QUALITY criterion-17 distinct-scope review the rule requires.

Attacked claim clauses:

- C2 (claims-frozen.md): "a distinct new indexed knowledge entry is grounded in
  sources opened this round" — for S370/S371/S373 this grounding depends on the
  rows being admissible reopened-this-round rows.
- registration.md C2 frozen predicate: rows must be "opened this round";
  QUALITY.md governs admission; criterion 17 (`corpus/QUALITY.md:34`) requires
  explicit repeated-URL/overlap review with human review for genuinely distinct
  scope, and states "A warning-only shared census is not this review."
- W1 requirements recorded as conditions on the data seat:
  `w1/C2PinAudit.md:23` ("the distinct-scope case QUALITY.md:34 (rule 17) sends
  to explicit review; data seat must record it"), `w1/RegistryContract.md:11`
  ("QUALITY.md:34-39 requires explicit repeated-URL/overlap review … Establish
  what is genuinely new, review the URL collisions"), `w1/C2CoverageCritic.md:93-96,118-122`
  (same-URL reopen admissible "only as an explicit distinct-scope reopen per
  criterion 17 (precedent S018 r39)").

## Reproduction

All commands run read-only against the lane worktree at base
`85d57a818c3707397e21c840b6498b105ba798aa` plus its uncommitted round-52
artifacts; counter runs executed in a scratch clone of the lane
(`/fast/scratch/hyaku/mado-r52/Attack10/repo`, toplevel asserted before the
fixture commit; scratch removed after).

1. Read the landed registry rows and search log:
   - `grep -n '^| S37[0123] ' corpus/SOURCES.md` → rows at worktree lines 320-323.
   - `grep -n 'distinct-scope review remains outstanding' corpus/SOURCES.md`
     → the round-52 search-log entry itself states (line 374):
     "S370, S371 and S373 reuse canonical URLs with new scopes;
     **distinct-scope review remains outstanding**."
2. Census disposition check:
   - `grep -c 'S370\|S371\|S373' .ufo/waves/round-52/census-before.txt` → 0.
   - `.ufo/waves/round-52/census-after.txt:24-26` → new W04 duplicate-URL
     warnings for S370/S371/S373 ("duplicate url … across scopes"), with no
     disposition record anywhere in round-52 bytes
     (`grep -rn 'W04' .ufo/waves/round-52/ corpus/lessons/round-52.md` finds
     only the two census files). Contrast the round-46 precedent
     (`corpus/lessons/round-46.md:59,70,106`) where the same W04 class was
     recorded with an explicit held-row rationale.
3. Lesson admission record check: `corpus/lessons/round-52.md` `## Gate` /
   `### C2` says "Review source URL collisions against prior rows before
   appending" (instruction) and "Admitted/rejected rows and outside non-author
   admit+reject sample remain pending final source audit" — no Gate admission
   block of the round-51 form (`corpus/lessons/round-51.md:9-19`, per-row URL /
   pin / quote record) exists for S370-S373.
4. Byte-level "opened this round" verification (the part that does hold):
   - `.ufo/waves/round-52/fetch/` holds the four files plus `SHA256SUMS`;
     `sha256sum` of each round-52 fetch file equals the round-51 pin and the
     registry-row hash (e.g. DispatcherTranslator.cpp 7248cbb8…,
     ConfigActions.cpp a83abeb5…, ConfigActions.hpp 746c6f51…,
     KeybindManager.cpp 8d8f35fc… — all EQUAL).
   - Cited-region disjointness from prior rows verified on the pinned bytes:
     S365 anchors DT:30-35,797-867 vs S370 DT:531-627 (sendshortcut/
     sendkeystate bodies) — disjoint; S367 CA:1664-1682 (submap) vs S371
     CA:1530-1616 — disjoint; S364 KM:41-113,602,782,785,798-823 and S352
     KM:289-334 (updateXKBTranslationState) vs S373 KM:221-242 (stringToModMask)
     — disjoint.
5. Instrument coverage check: `grep -n 'S365\|S367\|S364\|collision\|distinct' 
   quality/counters/c2-r52-proposition-entry.py` → no URL-collision or
   distinct-scope clause; the counter is structural only (consistent with the
   frozen "not automated semantic-entailment" boundary, so the review gap is
   caught by nothing).
6. Scope-wording overlap check (what the outstanding review must answer):
   S365 teaches "how CDispatcherTranslator::run resolves a dispatcher name to
   its implementation and **how implementations parse arguments**"
   (`corpus/SOURCES.md:314`) — S370 teaches "`sendshortcut` and `sendkeystate`
   source-level **argument parsing**/key resolution" (`:320`). Criterion 17
   explicitly refuses to let differing scope wording settle the question.
   Concrete held-ground overlap already on record: the r51 entry cites
   sendshortcut's three-field gate at DT:532-535 (`corpus/knowledge/
   hyprland-dispatcher-dispatch-r51.md:206-208`) — the same gate S370's P06
   re-anchors at :531-535 — and describes sendkeystate's save/restore at
   CA:1603-1615 (`:197-199`), adjacent to S370's P15 (DT:612/:624) and P16
   (the demoted held twin). W1 recorded these (C2Novelty N2/N3, C2PinAudit
   findings 1-2) but no landed artifact dispositions them as part of a
   criterion-17 review.

## Errors reported (all)

- E1 — The committed new counter's default entry slug is
  `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md` while the landed
  entry is `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`. Reproduction:
  stage the landed worktree state in a scratch clone (toplevel asserted;
  fixture commit only), run
  `python3 -I quality/counters/c2-r52-proposition-entry.py --repo . --rev HEAD
  --work <scratch>` → prints `C2_R52: entry=absent verdict=TARGET_MISSED rc=1`.
  The counter misses on the landed tree under its own defaults.
- E2 — Even with the correct slug
  (`--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md`), the same run
  prints `props=0 rows=0 indexed=1 failures=1 miss=props verdict=TARGET_MISSED
  rc=1`: the counter's proposition regex expects table cells
  `(P, S, claim, pin, anchor, quote, rationale)`, but the landed proposition
  table is 8 columns `(P, proposition, S-row, pin, anchor, quote, support,
  why)` — `S\d+` never appears in column 2, so zero propositions parse. The W1
  r-green receipt (`w1/C2CounterDraft.md`, MUTANTS 18/18 on the seat fixture)
  therefore demonstrates the counter against a synthetic fixture in the
  counter's own grammar, not against the landed entry. The orchestrator hint
  "counter draft r-green proves a separate synthetic fixture only, not landing"
  is reproduced with the exact failing runs above.
- E3 — `.ufo/waves/round-52/fetch/README.txt` promises "Source paths are listed
  in round52 source-reopen manifest once copied"; no such manifest exists under
  `.ufo/waves/round-52/` (only the four files and `SHA256SUMS`). The sha256
  receipts are present, so this is a documentation defect, not an evidence gap.

## Outcome

- Distinct-scope review requirement: REAL and UNMET as landed. The falsifier
  is the lane's own bytes: the registry search log admits the review "remains
  outstanding" at the moment the rows stand appended with status `mined`; the
  census W04 warnings for S370/S371/S373 are undispositioned; the round-52
  lesson carries no Gate admission record for these rows; no instrument checks
  the review. Under criterion 17's own text ("A warning-only shared census is
  not this review"), the append of S370/S371/S373 proceeded with the mandated
  review open — the C2 source premise "grounded in sources opened this round"
  is only partially established: the round-52 fetch (byte-equal, sha256
  receipts) satisfies the mechanical reopen, but the admission review that
  qualifies the reuse is admittedly incomplete.
- Verdict: **reproduced** (the specified control — explicit QUALITY-17
  distinct-scope review recorded before append — is not in place; falsifier
  found in the landed registry text itself).
- Mitigating verified facts (limits of the attack): the cited regions of the
  three reused URLs are disjoint from every prior row's anchors on the pinned
  bytes, so the "genuinely distinct scope" branch criterion 17 offers is
  available; nothing I checked proves the rows are semantic duplicates. The
  attack removes the review record, not the rows' distinctness.

## Limitations

- I did not perform the criterion-17 review myself and claim no non-author
  judgment: semantic non-overlap of S370 vs S365's broader "implementations
  parse arguments" scope, and the P06/P15/P16 held-ground dispositions, remain
  questions only the human review can settle. My disjointness check is at the
  line-anchor level only.
- Scope-wording comparison rests on registry `teaches` text, not on a full
  semantic diff of the entries.
- Line numbers for corpus files are worktree-relative at observation time;
  round-52 corpus artifacts are uncommitted at base `85d57a81`.
- Counter runs (E1/E2) executed in a scratch clone of the lane, not against a
  committed round tip; the findings describe the committed counter bytes run
  against the landed entry bytes, which is the pairing the claim must survive.
- No network fetch, live read, probe, or host mutation was performed; the
  source-only boundary was kept. Scratch `/fast/scratch/hyaku/mado-r52/Attack10`
  was removed after the runs.

Report: `.ufo/waves/round-52/w2/Attack10.md`
