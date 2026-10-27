# Attack15 — C2 duplicate claims / row completeness

Seat: `Attack15` (mutation-tester, leaf). Wave: round-52 w2 (attack, not a vote). Date: 2026-10-27.
Base: `85d57a818c3707397e21c840b6498b105ba798aa` (lane tip == base; landing is uncommitted worktree
state). Target: C2's duplicate-claim defenses and row/mapping-completeness checks — in the landed
artifact, in the W1 draft counter, and in the committed counter `quality/counters/c2-r52-proposition-entry.py`.

Attacked frozen clauses (claims-frozen.md C2; registration.md "Frozen predicates" C2):

- "each material factual proposition maps to a pinned source quote <=25 words and explicit support
  rationale" / "every material factual proposition is mapped";
- "A new committed counter checks proposition count, row/pin/quote bindings and complete mapping";
- "at least four substantive propositions" (count must mean distinct substantive propositions).

Method: all behavior on a scratch clone `/fast/scratch/hyaku/mado-r52/Attack15/repo` (toplevel
asserted before every commit). Staged landing bytes (`.ufo/waves/round-52/validate/corpus/`) were
committed on top of the frozen base to model the intended landing; no lane/tracked file was written,
no git state of the lane was touched (clone only), no installs, no live/probe reads. Counters were
run with `python3 -I`. Every mutant was `git reset --hard` back to its control rev with sha256
verification (restoration table at the end). Source truth / entailment was NOT judged (outside
non-author review boundary respected).

Fixture revs: `L0` = staged landing bytes on base `4e24291c26a0`; `L1` = L0 + minimal repairs
`6461a4a439c3`.

## Findings

### A1 — The landed map contains a duplicate proposition that every dup gate misses (REPRODUCED)

Clause: "every material factual proposition is mapped"; counter dup gates (clause_b
`duplicate_claim`, clause_e `duplicate_quote`/`duplicate_claim`).

Locator: `.ufo/waves/round-52/validate/corpus/knowledge/hyprland-synthetic-dispatch-r52.md`, map rows:

- `| P04 | repeat calls its delegate again only after a successful first call. | S370 |
  Hyprland-legacy-DispatcherTranslator.cpp:619-622 | auto result = sendshortcut(modifiedArgs); if
  (keyState == 2 && result.success) result = sendshortcut(modifiedArgs); | ...`
- `| P17 | sendshortcut's repeat branch can invoke its delegate twice for a successful repeat
  state. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:619-622 | if (keyState == 2 &&
  result.success) result = sendshortcut(modifiedArgs); | ...`

Same anchor span (619-622); P17's quote is a strict suffix slice of P04's quote; the claims restate
one fact. Both `key()`-normalized texts differ, so no dup gate fires. Observed on the landing runs
below: L0 clause_b `ok=1 propositions=18 ids=18` with no dup notes; L1 clause_e `ok=1` with no dup
notes. Net: 18 mapped rows carry at most 17 distinct facts, and the audited draft's two distinct
focus propositions (draft P16 `xtract` fill, draft P17 nothing-focused → events still sent) were
silently dropped between draft and landing with no re-audit receipt.

Verdict: reproduced — count padding by a near-duplicate exists in the artifact of record, invisible
to the counter that claims to check "proposition count".
Limitation: "distinct fact" is a semantic call; mine rests on the identical anchor span + suffix
quote + paraphrase pair, stated so a reviewer can re-derive it. Entailment not judged.

### A2 — The draft counter cannot certify the staged landing (REPRODUCED)

Command: `python3 -I .ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py --repo
<scratch clone> --rev 4e24291c... --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md`.

Observed (L0): `clauses_met=2 admitted=0/1 verdict=TARGET_MISSED` —
- clause_c `ok=0 ... miss=P01:anchor_no_fetch_root,...` (all 18 propositions): the landed
  `corpus/SOURCES.md` rows S370–S373 (validate copy lines 572-575) use anchor
  `DispatcherTranslator.cpp:531-627 @ efb509...; r52 fetch SHA256 7248cbb8...`, which contains
  neither the fetch-root path nor the pin basename that clause_c requires; round-51 rows show the
  house schema the counter expects (`... ; pin .ufo/waves/round-51/fetch/<file>`, e.g. S369).
- clause_d `ok=0 ... miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)`: landed P16's
  two-call quote (mods call + key call) is non-contiguous inside the 1554-1558 span (corroborates
  Attack24's item).
- clause_e `ok=0 ... miss=P01:id_not_referenced,...` (all 18): the landed entry never draws on any
  P-id outside its own map table (no licensing/steps section).

Verdict: reproduced — the W1 signal "r-green proves a separate synthetic fixture only, not landing"
is confirmed quantitatively; no W1 receipt ever ran either counter against the landed slug
(`hyprland-synthetic-dispatch-r52.md`); W1 receipts cover three other slugs (draft default
`...synthetic-key-dispatch-r52.md`, fixture `...dispatcher-action-effects-r52.md`, base probe).
Limitation: my L0 models the intended landing from worktree bytes; the lane has not committed it.

### A3 — The landing gap is exactly three items; repaired fixture goes green (control, NOT reproduced)

L1 = L0 + (i) the four anchors rewritten to the round-51 house schema, (ii) P16 re-anchored to the
contiguous single call at :1554, (iii) one prose line "Draws on: P01...P18.". Draft counter:
`clauses_met=5 admitted=1/1 verdict=TARGET_MET rev=6461a4a439c3`, `quotes_bound=18/18
quotes_raw=7/18 pins=4 pins_prior_equal=4/18`.

Verdict: the landing/counter mismatch is fully characterized (not a deeper counter defect);
`pins_prior_equal=4/18` also shows all four pins are byte-equal to prior-round copies — reported as
a diagnostic only, by design (ties to the QUALITY17 review, Attack10/26/24 territory).
Limitation: L1 is my repair fixture for gate attribution; its P16 re-quote is not a proposed
landing edit, and `quotes_raw=7/18` shows the green verdict depends on the frozen
whitespace-collapsed policy for 11 of 18 quotes (both numbers printed by the counter, as designed).

### A4 — Paraphrase-duplicate propositions survive the draft counter (REPRODUCED)

Mutant M1 on L1: added map row P19 = P04's fact reworded ("A repeat dispatch runs its delegate a
second time only if the first invocation succeeded."), different quote slice (`:619-620`),
prose-mentioned twice. Observed: `clauses_met=5 admitted=1/1 verdict=TARGET_MET rev=517b781116a7`
— proposition count inflated 18→19 with a duplicate fact; `duplicate_claim`/`duplicate_quote`
(keys are casefolded, punctuation-free exact-text) both silent.

Verdict: reproduced — "at least four substantive propositions" and the proposition count are
inflatable by paraphrase duplicates; the counter's dup defense is exact-text only.
Limitation: semantic duplication is outside any mechanical counter; the finding is that nothing
else (outside review checklist, QUALITY) is recorded as catching it either.

### A5 — Exact-duplicate claims are caught (control direction verified, NOT reproduced)

Mutant M2 on L1: added P20 with claim text byte-identical to P04 (different quote slice).
Observed: clause_b `ok=0 ... miss=duplicate_claim:repeat calls its delegate again only after a
successful first call`; clause_e fired the same note; rc=1 TARGET_MISSED at `ae6e68f3fbc4`. (M2's
clause_d `quote_not_at_pin` on P20 was fixture-side anchor imprecision, not the gate under test.)

Verdict: the exact-text dup gate works as W1's `duplicate_quote` mutant suggested; asymmetry
A4/A5 documented.

### A6 — A prose-claimed proposition id with no map row passes (REPRODUCED)

Clause: "every material factual proposition is mapped" (prose→row direction).

Mutant M3 on L1: two prose mentions of "P21", no P21 map row, no registry change. Observed:
`clauses_met=5 admitted=1/1 verdict=TARGET_MET rev=508da2f19200`. clause_e checks recs→referenced
(orphan map rows) but has no reverse check referenced→recs: an entry can name a proposition id as
drawn-on with no mapping at all, and "complete mapping" still passes.

Verdict: reproduced — the completeness clause is one-directional; the frozen sentence is not
enforced in the prose→row direction.
Limitation: M3's P21 carries no factual content; it demonstrates the missing check, not a live
unmapped claim (A1's P17 shows the landed text needs no such trick to carry a duplicate).

### A7 — Duplicate registry rows are silently tolerated (REPRODUCED); forward direction works (control)

Mutant M5 on L1: appended an exact duplicate of row S370 to `corpus/SOURCES.md`. Observed:
`clauses_met=5 admitted=1/1 verdict=TARGET_MET rev=da03a9f162b0` — `registry()` builds an
S-id→row dict and a later duplicate silently overwrites; no uniqueness check on registry rows.
Control mutant M4 (fresh row S374 cited in prose, unmapped): CAUGHT, clause_e
`row_unmapped:S374`, rc=1 at `cb5cdfafd546` — the row-level direction W1 tested still works.

Verdict: reproduced for duplicates (row uniqueness is a C1-predicate concept absent from the C2
counter and from the landed registry's own defenses); not a falsifier of any C2 sentence that does
not promise row uniqueness.
Limitation: duplicate-row padding changes no binding here because ids collide; a re-id'd copy
(S375 = S370's content) would additionally need only a distinct anchor string to pass — not
tested (out of my assigned scope).

### A8 — The committed counter is not the counter W1 validated, and does not implement the frozen check (REPRODUCED)

Locators: `quality/counters/c2-r52-proposition-entry.py` (lane worktree, untracked) vs
`.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py`. The W1 draft's own docstring
says it "is not committed and has not been copied to quality/counters/" — yet a same-named,
structurally different file sits in `quality/counters/`. The 18-mutant receipt `r-mutants.txt`
(escaped=0) attaches to the draft, not to this artifact. Verified properties of the committed file:

1. Proposition regex `^\|\s*(P\d+)\s*\|\s*(S\d+)\s*\|([^|]+)\|... ` expects exactly 7 columns; the
   landed 8-column map (ID | Proposition | Source row | Pin:anchor | Quote | Support class | Why)
   parses to **0 propositions** (run on L0: `props=0 ... verdict=TARGET_MISSED`, `miss=props`).
2. `grep -c 'fetch|duplicate|unmapped|prior_equal'` = **0**: it never opens the pinned bytes (no
   quote-at-pin check possible; the pin/anchor capture groups are bound and never used), has no
   duplicate detection, no unmapped/uncited/orphan logic, no fetch-root concept.
3. `grep -n 'a.base'` = empty: `--base` is parsed and never referenced — "opened this round"
   (absence at base) is never checked by the committed artifact.
4. `--entry` default remains `corpus/knowledge/hyprland-synthetic-key-dispatch-r52.md` — a slug the
   landing does not use (run on L0 with defaults: `entry=absent`).
5. Behavioral probe (fixture C1 `dc6e340a60cd`, 4 propositions in its own 7-column grammar):
   P02 an exact duplicate of P01's claim AND quote, P03 a quote appearing in no pinned bytes
   (`SENTINEL...`), S370 appended twice to the registry → `props=4 rows=1 indexed=1 failures=0
   verdict=TARGET_MET`, exit 0.

Verdict: reproduced — the frozen sentence "A new committed counter checks proposition count,
row/pin/quote bindings and complete mapping" is not implemented by the committed counter: count
(superficially), row existence/meta (partially) only; pin/quote bindings and complete mapping not
at all, duplicates and fabricated quotes admitted.
Limitation: C1 is a scratch fixture built to the committed counter's own grammar to isolate its
gates; it does not show the landed entry contains fabricated quotes (the draft counter bound 18/18
on L1). Corroborates Attack12 F4/F5 from the duplicate/completeness angle.

### A9 — Corroborations and non-reproductions at the registry (recorded, not my primary target)

- S373's URL (KeybindManager.cpp @ efb50993) is shared by **two** prior rows (S364, S352 —
  `corpus/SOURCES.md:301,313` working tree), not just S364 as W1 `C2PinAudit` §2 listed (matches
  Attack24's census note). S370≡S365, S371≡S367 likewise (worktree rows S313-316).
- The duplicated round-52 search-log line shown in `w2/Attack12/source-novelty.txt` (two identical
  `+Round 52 — synthetic shortcut path ...` lines) is **not reproduced** against current bytes:
  `grep -n 'Round 52 — synthetic shortcut path' corpus/SOURCES.md` → one hit, line 374. Either
  repaired since 11:2x or a diff-rendering artifact in that receipt.
- QUALITY17 distinct-scope review: lane's own log still says "distinct-scope review remains
  outstanding" (line 374); my A3 `pins_prior_equal=4/18` adds that the counter's only treatment of
  the reuse is a diagnostic. Attack10/Attack26 own this finding; cited for completeness.

## Verdict summary

| item | target | verdict |
|---|---|---|
| A1 | landed P04≡P17 duplicate vs counter dup gates | REPRODUCED (defect instance, gates blind) |
| A2 | counter certifies staged landing | REPRODUCED (2/5 TARGET_MISSED; r-green fixture-only) |
| A3 | landing gap fully characterized by 3 repairs | green at L1 (control; `quotes_raw=7/18` noted) |
| A4 | paraphrase-duplicate padding | REPRODUCED (survivor) |
| A5 | exact-duplicate claim gate | NOT REPRODUCED (caught; control works) |
| A6 | prose-claimed id without map row | REPRODUCED (survivor) |
| A7 | duplicate registry row | REPRODUCED (survivor); unmapped-fresh-row control caught |
| A8 | committed counter implements frozen check | REPRODUCED (does not; TARGET_MET on dup+fabricated fixture) |
| A9 | search-log duplicate line / S352 census | line-dup NOT REPRODUCED now; S352 sharing CONFIRMED |

Net for the claim: C2's counter evidence does not survive contact with the committed artifact
(A8) nor with the staged landing (A2), and the mapping-completeness/duplicate-claim guarantees the
frozen sentence names are unenforced in three concrete directions (A1, A4, A6, A7). This is a
coverage finding against the counter/landing pair, not a judgment that the entry's 17 distinct
propositions are semantically false — quotes bound 18/18 at L1 and entailment stays with the
outside non-author reviewer.

## Restoration evidence

All runs in `/fast/scratch/hyaku/mado-r52/Attack15` (repo + run transcripts). Per-mutant:
`git reset --hard` to L1 `6461a4a439c3` then sha256 compare — restored=True for M1..M5, C1, and
final reset. L1 file digests (sha256, first 16 hex): entry `e3b478cf8b93b152`,
`corpus/SOURCES.md` `9f864184a2a328dc`, `corpus/README.md` `5307102fa1f3c044`. Mutant revs:
M1 `517b781116a7`, M2 `ae6e68f3fbc4`, M3 `508da2f19200`, M4 `cb5cdfafd546`, M5 `da03a9f162b0`,
C1 `dc6e340a60cd`, L0 `4e24291c26a0`. Scratch dir removed after this report; no lane file outside
this report was created or modified; no git/jj state of any lane or sibling repo was mutated
(clone-only reads).

Checks main agent may re-run: the two counter commands in A2/A8 against any scratch clone
staging `validate/corpus/*` over base `85d57a81`; the A1 row comparison; the A8 greps.

```
claim=C2 coverage: proposition-bound dispatcher entry (duplicate claims / row completeness)
attacked=frozen "every material factual proposition is mapped"; "committed counter checks proposition count, row/pin/quote bindings and complete mapping"; ">=4 substantive propositions"; registration C2 counter scope
verdicts=A1 REPRODUCED; A2 REPRODUCED; A3 control-green; A4 REPRODUCED; A5 NOT REPRODUCED (gate works); A6 REPRODUCED; A7 REPRODUCED; A8 REPRODUCED; A9 line-dup NOT REPRODUCED now, S352 sharing CONFIRMED
survives=18 landed quotes bind bytes at L1 (18/18 collapsed); forward row-unmapped and exact-dup gates of the draft counter work; pins immutable and digest-stable; entailment unjudged (outside review)
receipts=scratch transcript embedded above; revs L0 4e24291c26a0 L1 6461a4a439c3 M1 517b781116a7 M2 ae6e68f3fbc4 M3 508da2f19200 M4 cb5cdfafd546 M5 da03a9f162b0 C1 dc6e340a60cd
report=.ufo/waves/round-52/w2/Attack15.md
scratch=/fast/scratch/hyaku/mado-r52/Attack15 (removed)
```
