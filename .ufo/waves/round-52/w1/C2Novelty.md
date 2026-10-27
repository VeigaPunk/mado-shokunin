# C2Novelty — round 52

Seat: C2Novelty (critic, leaf). Assignment: adversarial overlap check on the proposed dispatcher
surface using the corpus; identify novelty and source-truth deficiencies. No claim or predicate
edits; no tracked lane writes; source-only round (reads against locally pinned bytes only).
Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`, base `85d57a818c3707397e21c840b6498b105ba798aa`.

## Attacked items

1. **Frozen C2 predicate** (claims-frozen.md C2; registration.md C2 frozen condition) — specifically
   the phrases "a distinct Hyprland dispatcher-execution mechanism" and "grounded in sources opened
   this round", and the counter scope "checks proposition count, row/pin/quote bindings and index".
2. **The proposed surface as actually drafted**: `w1/C2EntryDraft/entry-draft.md`
   (slug `hyprland-synthetic-key-dispatch-r52`, 17 propositions P01-P17, proposed rows S370-S373),
   attacked proposition-by-proposition where deficient (P06, P14, P15, P16 named).

This is not a vote and not a falsification claim against the draft author; it is the assigned
adversarial review. Where the draft survives, I say so with evidence.

## Verdict in one paragraph

The drafted surface is **novel enough to stand** — ~13 of 17 propositions rest on ground no admitted
entry holds, and its "manufacture/delivery of a synthetic input event" subject is genuinely distinct
from round-51's routing subject — **but four deficiencies must be corrected or disclosed before the
frozen predicate is run**: (N1) the frozen predicate contains **no novelty/distinctness check**
(verified; round-51's shingle clause was dropped), so distinctness rests entirely on seat judgment;
(N2) "sources opened this round" is satisfied by a **re-fetch ceremony** — all four pins are
byte-identical to round-51 pins (the draft's own `fetch/verify.txt` says 4/4 EQUAL), three of four
URLs already carry registry rows at base, and a date-based freshness check cannot discriminate
because S364-S369 are also dated 2026-10-27; (N3) two propositions (P06, P15) are **held-fact
re-anchors**, not new ground, and would be counted as fresh coverage; (N4) P16 is labeled support
class `direct` but its entailment chain **requires an unquoted, unpinned line** (`xtract`,
ConfigActions.cpp:47-49) — a live instance of the exact M51-2 class inside a binding-perfect draft,
and a ready-made first sample for the outside source-truth reviewer.

## N1 — The frozen predicate has no distinctness/novelty clause (predicate attacked)

Claims-frozen.md C2 and registration.md C2 together freeze: ≥4 substantive propositions; each
mapped to an opened-this-round S### row, pin path/revision, exact located quote ≤25 words, support
rationale; every material factual proposition mapped; counter checks proposition count,
row/pin/quote bindings and index; outside reviewer judges source truth; base entry absent →
TARGET_MISSED. **Nothing in that list measures overlap against held corpus.** PRED-C2-r51 carried
clause (c), a ≤30% word-8-gram shingle check against every `corpus/knowledge/*.md` at base plus all
`.ufo/waves/round-*/candidate/` files; the round-52 predicate drops it entirely. Consequence: any
subject, including a restatement of round-51 ground, passes mechanically. My sibling
`C2CoverageCritic.md` demonstrates this with a socket-verb-restatement counterexample; I confirm
their structural claim independently and add that `receipts/c2-base.txt` shows the *old* counter
already printing `admitted=1/1 verdict=TARGET_MET` at the round-52 base for the existing r51 entry —
so a freshness check keyed on anything but a **new target slug** (which registration does require)
is meaningless, and a freshness check keyed on the slug alone still says nothing about subject
novelty. Impacted axis: coverage (premature saturation risk). Smallest safe correction (review-side,
no predicate edit): the integration review must treat subject distinctness as a gate question
answered against the held map below, and C2PinAudit/C2EntryQuality verdicts must name it.

Held dispatcher-execution map used for the distinctness judgment (all verified read this round):
`dispatcher-semantics-r25.md` (wiki-level: dispatchers describe, `hl.dispatch` executes, S188);
`dispatcher-surface-and-request-grammar-r26.md` (0.56.0 published vocabulary S196; request-side
resolution incl. Lua eval wrapper S018/S366); `hyprland-bind-key-match-r50.md` (match chain, mask
comparison, dispatch order, S352-S363); `hyprland-dispatcher-dispatch-r51.md` (map population,
parse-time validation, press path, submap/pass state, socket verb, five argument grammars
S364-S369, plus w2 errata). The draft's subject — how `sendshortcut`/`sendkeystate` build and hand
over a synthetic seat event — is **not** any of these four. Distinctness: DEFENSIBLE.

## N2 — "Opened this round" is a re-fetch ceremony, not new evidence (predicate + draft attacked)

Evidence (transcript: `w1/C2Novelty/anchor-spotcheck.txt` §1, §3):

- The draft's four pins re-fetched 2026-10-27 into `w1/C2EntryDraft/fetch/` are **byte-identical to
  the round-51 pins**: its own `fetch/verify.txt` records `4/4 EQUAL` (`quotes-check.txt` green run
  was against these same-bytes copies, per its report's receipt line).
- Three of the four URLs already carry registry rows **at the round-52 base**: S364
  (KeybindManager.cpp), S365 (DispatcherTranslator.cpp), S367 (ConfigActions.cpp) — verified
  `git show 85d57a8:corpus/SOURCES.md` (rows at lines 313-318). The draft calls S372
  (ConfigActions.hpp) a "new URL"; it has no registry row but **was pinned in round-51's manifest**
  (round-51 entry pin table: `Hyprland-ConfigActions.hpp | src/config/shared/actions/ConfigActions.hpp | S367`),
  so it too is a same-bytes re-open.
- The registry's only freshness signal is the opened **date**, and S364-S369 are dated **2026-10-27 —
  today**. A counter that verifies "opened this round" by date alone accepts round-51 rows
  (stale-row bypass; also a fabricated new row over an old URL passes, since the row id is new).

Consequence: if re-fetch-and-re-date counts as "opened this round", every future round can re-mine
the same four files under new scopes and claim fresh coverage indefinitely — the coverage axis
degrades into re-scoping churn, and this round's entry sets that precedent. The draft deserves
credit for **disclosing** the byte-equality in its Limits; the defect is that the frozen predicate
gives the counter no way to enforce or even surface the disclosure. Impacted axes: coverage,
operability. Smallest safe corrections (counter-side and process-side, no predicate edit):
(a) counter requires each cited S### row id to be **absent from the base revision's
corpus/SOURCES.md** (new row ids, not just new dates); (b) counter records in its verdict line the
count of pins byte-equal to any prior-round pin (`pins_prior_equal=4` here) so the overlap is on
the receipt, not only in prose; (c) if the lane wants "opened this round" to mean *new evidence*,
the draft itself names two genuinely unpinned alternates (exec→`supplementary/executor/Executor.{hpp,cpp}`;
`src/protocols/ShortcutsInhibit.{hpp,cpp}`) — switching surfaces is the honest fix; proceeding with
the draft is acceptable **only with (a)+(b) disclosure**.

## N3 — Provenance inflation: P06 and P15 are held facts with new anchors (draft items attacked)

- **P06** ("`sendshortcut` takes exactly three fields", S370, `:531-535`) is the **same quote**
  round-51 step 7 already bound for the same fact (`CVarList2 ARGS(args, 3); if (ARGS.size() != 3)`
  at DispatcherTranslator.cpp:532-535, held via S365). The fact was admitted last round; only the
  row id and anchor width are new.
- **P15** ("the press field is restored after delegation", S370, `:612`/`:624`) restates round-51
  step 6's parenthetical ("the one dispatcher that writes the field itself, saving and restoring it
  around its work") — and the round-51 **w2 truth review already cited exactly these translator
  lines** (`w2/RevC2EntryTruth/entry-truth.md` step-6 note: "sendkeystate save/restore is translator
  `:612-24`"). The draft's own report claims P15 "round 51 did not cite"; round 51's *entry* cited
  the ConfigActions twin (corrected by w2), but the lane's records carried the translator anchor
  before this round. New to the corpus as a binding; **not new ground**.

Both propositions are TRUE and well-anchored (verified at the pin). The deficiency is
classification: as frozen, the predicate counts them toward "≥4 substantive propositions" grounded
in newly opened sources, inflating the coverage delta. Smallest safe correction (entry-side):
reclassify P06/P15 as `held-fact/new-anchor`, keep them in the map with held cites
(`hyprland-dispatcher-dispatch-r51.md` step 7 for P06; step 6 + w2 note for P15), and let the
"new ground" count be 13/17. The distinctness verdict above already accounts for this.

## N4 — P16's support class is overstated, and the quote-comparison policy is unfrozen

**P16** ("an empty selector delivers to the current focus with no focus switch", S371,
quote `if (!window) return {};` at ConfigActions.cpp:1578-1579, support class `direct`). Verified at
the pin: anchors exact; the proposition is **true** — but the quoted line alone does not entail it.
`if (!window) return {};` is equally consistent with "an empty selector swallows the event". The
entailment chain needs: (i) delivery lines :1554-1576 sit **outside** `if (window)` (draft cites
:1537-1552,1578-1579 — the delivery block is in the gap), and (ii) `xtract`'s
`return window.value_or(Desktop::focusState()->window());` (ConfigActions.cpp:47-49), which decides
what "empty" resolves to — a line in the same pinned file that is **neither quoted nor anchored** in
any proposed row (I read it at the pin; the draft never cites it). That is precisely the M51-2
pattern (claim slightly broader than its cited lines, rescued by an uncited line) appearing inside a
draft whose own checker passed 17/17 — the strongest available local proof that the binding check
cannot catch entailment gaps and that the outside reviewer's sample choice matters. Two smaller
points ride along: the map's phrasing "empty passes nullptr" blurs null-handle vs disengaged
`std::optional` (`value_or` fires only on disengaged; for sendshortcut's call the optional is engaged
with a null handle, so xtract's focused-window branch never runs — the outcome coincides, the
mechanism differs), and **P14's quote is not raw-verbatim** at ConfigActions.hpp:117
(`uint32_t m_timeLastMs = 0; // ...` vs the pin's `uint32_t    m_timeLastMs    = 0;  // ...`):
it passes the draft's whitespace-normalizing checker and **fails a raw line-contains check of the
round-51 counter style**. Whether "exact located quote" means raw or whitespace-collapsed is
currently checker-dependent — the same proposition flips PASS/DEFECT on policy alone.
Impacted axes: coverage honesty, operability (receipt reproducibility). Smallest safe corrections:
(i) entry adds anchor ConfigActions.cpp:47-49 to P16's support set (same pin, same row S371 — the
row scope text already covers "seat delivery") or downgrades P16 to support class `chain`;
(ii) counter freezes and prints one quote-comparison policy; under a raw policy P14 must be re-quoted
with exact spacing (its anchor and word count are otherwise correct).

## Held-ground defects found during verification (must not be inherited)

The draft is clean of these; they live in **admitted** ground and both stem from loose line ranges:

1. **r51 entry step 7 exec anchor is wrong** (present at base, survived the w2 errata): "exec does
   not split at all and hands the tail to the process executor
   (Hyprland-legacy-DispatcherTranslator.cpp:48-51)" — lines 48-51 are `windowFromArg`'s tail and
   `resolveWorkspace`'s head. The actual `static SDispatchResult exec(const std::string& args)` is
   at :65-70 with `Config::Supplementary::executor()->spawn(args)` at :66 (`spawnRaw` at :73 for
   `execr`). The claim is true; the anchor is not; the w2 audit repeated the wrong numbers.
2. **r26 entry's `S018:1131-1132` citation is out of range**: the Lua eval wrapper
   (`std::string evalStr = std::format("return hl.dispatch({})", in);`) is cited to S018, whose
   declared locator is `dispatchGetProp`, lines 1463-1645 of HyprCtl.cpp. Line 1131 is outside it;
   the wrapper region (HyprCtl.cpp:1130-1141) lies inside **S366's** locator (1126-1158). A
   round-52 entry needing the wrapper must hold-cite S366, not S018.

## What survives (fairness record)

- All 17 anchors I spot-checked are **line-exact** against the pins (transcript §3); P01-P05,
  P07-P13, P17 are true, well-quoted, and on ground no admitted entry holds (state alphabet and
  repeat-as-double-press P02-P04; delegation rebuild P05; substring modifiers and silent zero P07 —
  verified `stringToModMask` has no error path, :221-242; keycode branches P08-P10; cache key P11;
  selector semantics P12; seat timestamp/offset/mask P13-P14; failure taxonomy P17).
- The draft's held-ground discipline is otherwise good: S364-S369 and S352/S353 cited as held, the
  `sendKeyState` twin correctly demoted to contrast after recon review, `[INF]` flags where the
  claims outrun the quotes, and honest Limits (byte-equality disclosed, doc-gap recorded, no
  host-runtime claims).
- The distinctness defense ("manufacture and delivery, not routing") holds against the held map;
  the novelty ceiling attack I prepared against a *wider-census* surface (re-reading the 66
  unread `DispatcherTranslator` implementations — same mechanism class as r51 step 7) does not
  apply to what was actually drafted.

## Dissent and limits

- I did not run the draft's `check-quotes.py` (execution of seat scripts is another seat's job); my
  verification is independent reads of the same pins. My P16 finding assumes the reviewer agrees
  that a proposition whose decisive line is unquoted is not `direct`-supported; the draft's own
  checker semantics concede the general point ("a quote that is verbatim at the anchor and says
  something else still passes").
- N2's process correction (c) — preferring the unpinned alternates — is a recommendation, not a
  blocking defect: with (a)+(b) disclosure, the drafted surface still adds ~13 grounded facts the
  corpus does not hold, which is real coverage.
- The outside-review component of the frozen predicate remains unfrozen as to verdict mechanics
  (sample size, verdict vocabulary, receipt shape). I hand the reviewer P16 as the first sample; I
  recommend the integration record a per-proposition verdict receipt under
  `.ufo/waves/round-52/receipts/` so the human judgment is at least committed and auditable. This is
  a process observation, not a claim edit.
- No package installs (none needed; tooling authorization read at `/home/vgpnk/.omp/agent/RULES.md`).
  No scratch writes beyond this seat dir; `/fast/scratch/hyaku/mado-r52/C2Novelty/` created empty,
  nothing to clean. No git/jj mutation, no network, no live reads.

## Deliverables

| artifact | path (relative to lane root) |
|---|---|
| this report | `.ufo/waves/round-52/w1/C2Novelty.md` |
| verification transcript | `.ufo/waves/round-52/w1/C2Novelty/anchor-spotcheck.txt` |

Every claim above is grounded in local reads at base `85d57a81` or at the round-51 pin bytes
(byte-identical to the round-52 draft pins per the draft's own `fetch/verify.txt`). Source URLs and
pins used: the four Hyprland 0.56.2 raw URLs already named in `w1/C2EntryDraft/pins.txt`
(commit `efb50993780079460b0cbed1363e2166a2de1d9f`, accessed 2026-10-27 via the draft's own fetches;
read by this seat from disk this round).

## Post-review addendum (counter resolution)

`C2CounterDraft` reports (IRC, this wave) that the counter now implements: clause (c)
row-vs-base freshness at the frozen base (a reused row fails as `row_not_new(S###)` —
base-absence, not dates); a frozen, printed quote policy (`quote_policy=whitespace-collapsed`,
with `quotes_raw` reported beside bindings — on the real draft `quotes_bound=17/17 quotes_raw=6/17`);
and `pins_prior_equal=4` printed as a diagnostic, deliberately not a gate (reopening a pinned file
under a new scope is legitimate; row freshness is clause (c)'s job). My N4 P16 sample was relayed
to the entry seat as a reviewer item. This resolves the counter-side portion of N2 and N4 as
recommended; the entry-side portions (P06/P15 reclassification, P16 xtract anchor) and the N1
review-gate question remain open at review/integration.

## Report

- `.ufo/waves/round-52/w1/C2Novelty.md`

```
seat=C2Novelty wave=w1 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
claim=C2 coverage proposition-bound dispatcher source entry
attacked=C2 frozen predicate phrases "distinct mechanism"+"opened this round"; draft items P06,P14,P15,P16
verdict=draft surface distinctness DEFENSIBLE (~13/17 new ground); defects N1(novelty clause absent),N2(re-fetch ceremony, 4/4 pins byte-equal to r51; date collision),N3(P06/P15 held-fact re-anchors),N4(P16 support-class overstatement, xtract:47-49 unquoted; P14 not raw-verbatim)
held_defects_found=r51 exec anchor :48-51 wrong (actual :65-70); r26 S018:1131-1132 out of S018 locator range (use S366)
corrections=counter: row-id-vs-base freshness + pins_prior_equal in verdict + frozen quote-comparison policy; entry: reclassify P06/P15 held-fact/new-anchor, add xtract anchor to P16; reviewer: sample P16 first, commit per-proposition verdict receipt
receipt=.ufo/waves/round-52/w1/C2Novelty/anchor-spotcheck.txt
report=.ufo/waves/round-52/w1/C2Novelty.md
```
