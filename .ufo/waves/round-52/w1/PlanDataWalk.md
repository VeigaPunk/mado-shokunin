# PlanDataWalk — round-52 planner data-walk

Seat: PlanDataWalk (w1, scout/planner). Date: 2026-10-27.
Base: `85d57a818c3707397e21c840b6498b105ba798aa` (repo HEAD at walk time; verified `git rev-parse HEAD`).
Method: committed-bytes only — `git ls-tree`/`git show`/`read` plus one read-only Python scan of the
ledger. No tracked bytes edited (`git status --porcelain` → only untracked `.ufo/waves/round-52/`),
no live reads, no package queries, no installs. Scratch `/fast/scratch/hyaku/mado-r52/PlanDataWalk/`
created; disk guard `/fast` 599G free, no ENOSPC risk.

## 1. Base-state observations (independently re-derived)

| Observation | Command / source | Result |
|---|---|---|
| Base commit is the round-51 verifier spot-check commit | `git log --oneline -5`; `git rev-parse HEAD` | `85d57a81 round-51 verifier spot-check (integrator, hyaku): non-author admit/reject`; HEAD matches frozen base |
| No round-52 counter committed | `git ls-tree -r --name-only 85d57a81 quality/counters/ \| grep -i r52` | empty — new-counter-absent precondition holds for both claims |
| No round-52 knowledge entry committed | `git ls-tree -r --name-only 85d57a81 corpus/knowledge/ \| grep -iE "dispatcher\|dispatch"` | only `dispatcher-semantics-r25.md`, `dispatcher-surface-and-request-grammar-r26.md`, `hyprland-dispatcher-dispatch-r51.md` — target entry absent |
| Registry at base = 306 rows, last S369 | `grep -cE '^\|\s*S[0-9]{3,}\s*\|' corpus/SOURCES.md`; `grep -oE '^\|\s*S[0-9]{3,}' corpus/SOURCES.md \| tail -3` | 306; S367–S369 last; next free id S370 |
| Knowledge index at base = 67 rows | `grep -c '^| \`knowledge/' corpus/README.md` | 67; README:78 indexes the r51 dispatcher entry |
| Base census receipt | `.ufo/waves/round-52/census-before.txt` + `.exit` | exit 0; `mado ok …/corpus/SOURCES.md`; W04 duplicate-URL warnings incl. S364/S366/S368 (warnings only) |
| Old C1 counter at base passes production | `.ufo/waves/round-52/receipts/c1-base.txt` | `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=85d57a81…`, exit 0 |
| Old C2 counter at base reports MET **against the r51 entry** — the receipt is contaminated for r52 target purposes | `.ufo/waves/round-52/receipts/c2-base.txt` | `a ok=1 index_row=knowledge/hyprland-dispatcher-dispatch-r51.md … clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=85d57a81…`, exit 0 — because the r51 entry exists at base; registration already rules this receipt untrusted for C2 |
| Production ledger at base has no self-pointer or generic-description rows | read-only Python scan of `quality/tool-ledger.md` at base (parse = c1-r51 `parse_rows` equivalent) | 82 rows parsed; **0 duplicate descriptions; 0 rows whose own path appears in their pointer cell; 0 rows pointing at `quality/tool-ledger.md` itself**; shared pointer *targets* (e.g. `PROVINCE.md:20`) are expected and fine |
| C1 do-nothing control shape | `.ufo/waves/round-52/controls/c1-do-nothing.md` | 3 identical rows, all `tools/mado-verify.sh`, description and pointer both `generic accountability pointer to this ledger itself` → pointer cell names the ledger itself; under old counter it would MISS only for `uncovered`/`dup`, never for the actual defect class |
| C2 no-work control | `.ufo/waves/round-52/controls/c2-do-nothing.md` | base revision, entry absent → new counter must report TARGET_MISSED at base |
| Old counter's pointer check is basename-containment only | `quality/counters/c1-r51-ledger.py:193-203` (`pointer_resolves`: any pointer token that exists whose bytes contain the row basename) and `quality/check-tool-ledger.py:259-265` (`names_basename`) | nothing rejects self-pointers, ledger-wide pointers, or generic descriptions; `empty_desc` is blank/placeholder-only (`check-tool-ledger.py:204-212`) |

## 2. C1 — operability: falsifiability, controls, measurement

**Falsifiable core.** The claim is one executable sentence: a *new* counter, at the pinned base revision,
passes the production ledger (exit 0, TARGET_MET) and fails `controls/c1-do-nothing.md` with defects
*classified as* self-pointer/context (registration: "specifically for self-pointer/context defects").
Both arms are mechanically decidable; the claim is bounded ("bounded accountability checks, not prose
entailment"), so residual forgery space is admitted, not hidden.

**The defect the counter must close (observed, not inferred):**
- `pointer_resolves` accepts any existing file containing the row basename (`c1-r51-ledger.py:193-203`).
  Round-51 seat evidence `w1/ScrLedgerRows/ledger-rows.md:212` measured **26 of 79 population files
  contain their own basename**, so a row pointing at itself passes `bad_pointer=0` today.
- The do-nothing control's pointer (the ledger itself) resolves under the old rule whenever the measured
  ledger bytes contain the row basename — which the control's own rows supply.

**Minimum check set the new counter needs (derived from the frozen predicate words):**
1. population row uniqueness — no duplicate row paths (control: 3 identical rows);
2. resolvable evidence pointer — pointer names a file present at the revision (control pointer resolves
   under the old rule, so resolution alone cannot be the discriminator);
3. non-self pointer — two readings: (a) pointer path ≠ row path; (b) pointer ≠ the measured ledger
   (`quality/tool-ledger.md`). The frozen control is built on reading (b) ("generic accountability
   pointer to this ledger itself"); production rows satisfy both readings (scan in §1). A counter
   implementing only (a) leaves the control's actual defect unmeasured → attack surface for
   C1ControlAttack/Falsify seats.
4. instrument-specific functional context in the description — production descriptions are per-instrument
   (read from each file's header per the ledger contract); control descriptions are identical generic
   text ×3.

**Measurement plan (for builder/verifier seats).** Green: run new counter `--rev 85d57a818c3707397e21c840b6498b105ba798aa` on the real repo → TARGET_MET, plus derive the population from the tree (82 at base) rather than any hardcoded count. Red: selftest must embed the frozen control verbatim (or a fixture byte-matching it) and emit a receipt naming `self_pointer`/`context` defects, distinct from `uncovered`/`dup`. Registration requires "explicit red/green receipts" — the old counter has no embedded red arm, so this is genuinely new behavior, not a rename.

## 3. C2 — coverage: falsifiability, controls, measurement

**Falsifiable core.** A new indexed entry at a new slug, grounded in rows **opened this round** (S370+,
opened 2026-10-27), ≥4 substantive propositions, each bound to a pin path/revision + located quote ≤25
words + written support rationale; complete mapping of material factual propositions; a new counter
checks count/bindings/index; an outside (non-lane) reviewer judges source truth; base must MISS.

**The trap already observed at base.** `receipts/c2-base.txt` shows the old counter admitting at base —
because its frozen `ENTRY = corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` exists at base. Any
r52 counter that (i) reuses the r51 slug, (ii) globs `corpus/knowledge/*dispatcher*`, or (iii) fails to
pin its exact target path will report MET at base and the no-work control collapses. The registration's
"separate target slug and prove absent at base" is the load-bearing control.

**Distinct-surface evidence (source bytes, locally pinned, opened in round 51 and re-readable).**
The r51 entry (`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:12-18`, errata at :318-357) claims
the parse/lookup/call/socket/submap/result-struct path and states it read **five** dispatcher
implementations' argument handling; its errata withdrew the broader claims (comma preservation,
mouse serialization, special-path count = 5, universal submap-scope, host-branch). The pinned
`.ufo/waves/round-51/fetch/Hyprland-legacy-DispatcherTranslator.cpp` (868 lines, sha256
`7248cbb8…`) holds ~65 implementation functions (`workspace` :137, `movetoworkspace` :209,
`sendshortcut` :531, `sendkeystate` :591, `passDispatcher` :524, `mouseDispatcher` :675,
`resolveWorkspace` helper :52-…) of which r51 read five. That is a concrete, source-verifiable
distinct-mechanism surface (per-dispatcher argument semantics) that does not re-claim r51's
ingress/lookup account. Other never-rowed local pins: `Hyprland-KeybindManager.hpp`,
`Hyprland-ConfigActions.hpp`, `Hyprutils-VarList*.cpp`, `Hyprland-docs-hyprctl.1.rst`.
Census precedent: round 51 added same-URL rows S364-S366/S368 at new line regions (W04 warnings, exit 0),
so round-52 rows on the same pinned commit at unexplored regions are registry-legal. New rows must be
*registered as opened this round* with pins under `.ufo/waves/round-52/fetch/`.

**Measurement plan.** Green: counter names the exact new entry path; entry exists at final rev; README
index row present; every proposition row binds S-row (opened 2026-10-27) → pin file+revision → quote
≤25 words present verbatim at the pinned line range → rationale non-empty. Red: same counter at base
`85d57a81` → entry absent → TARGET_MISSED (receipt). Structural counter cannot judge "substantive" or
source truth — per claim, that arm belongs to the outside reviewer (round-51 precedent:
`w2/RevC2EntryTruth/entry-truth.md` forced append-only errata; closure integrator spot-check §3
re-opened S364 live and agreed).

## 4. One-case-overfit risks (named, per claim)

**C1**
- *Control-string overfit*: a context check keyed to the literal control wording ("generic accountability
  pointer to this ledger itself") or its hash is one-case fitting; trivially mutated generics
  ("accountability pointer A/B/C") would sail through. The check must be a property (per-row
  specificity / non-identity / function words), and C1ControlAttack should try per-row generic variants.
- *Non-self reading (a) vs (b)*: §2 item 3 — the frozen control only fails under reading (b); a
  counter built on (a) passes the control and the claim is false.
- *Golden-ledger overfit*: hardcoding `population=82`, row count, or ledger content hash passes base and
  breaks on every future legitimate edit; population must be derived from the tree at `--rev` like
  `c1-r51-ledger.py:144-158`.
- *Wrong-defect pass*: the control fails the old counter already (uncovered/dup); the new counter's red
  receipt must name self_pointer/context classes, or the "distinguishes" claim is vacuous.

**C2**
- *Slug/target overfit*: hardcoding S370-S373 or a prose section name as the only legal binding; the
  counter should bind whatever rows the entry cites and verify registry opened-this-round metadata.
- *Count=4 satisfiability*: exactly 4 thin propositions ("the file compiles", "the map is a map") satisfy
  a count check; "substantive" is outside the counter by design — outside reviewer is the only guard,
  and the claim concedes it.
- *Quote-cherry-picking*: ≤25-word quotes can be true-but-non-supporting (round-51 M51-2 pattern);
  only the non-author source-truth sample closes this.
- *Distinctness drift*: re-claiming r51's five implementations or its ingress path under a new slug
  would be overlap, not coverage — C2CoverageCritic/C2Novelty seats exist for this; my §3 surface note
  marks what r51 actually read so the check is evidence-based.

## 5. SCORECARD / PROVINCE / round-51 spotcheck inspection

- **SCORECARD.md:2791-2795** (round-52 planned intent): (1) replace C1's lexical self-pointer predicate
  with a non-self, context-bearing check — matches C1 frozen; (2) bind C2 held tokens to propositions +
  outside source-truth review — matches C2 frozen; (3) the 13-row mado quarantine slice and
  `considerthese/2026-10-26.md` proposal 2 (a running ledger of live-state tools with last-live-run
  verdicts) are explicitly **distinct from C1's inventory** — no axis harm, but also no credit: C1 must
  not be scoped to cover proposal 2.
- **SCORECARD round-51 record** (`### Round 51`, lines ~2766-2808): C1 +10 operability, C2 +10 coverage,
  both TARGET_MET "under frozen literal predicate"; disclosed residuals: self-pointer/generic-description
  bypass (C1), generic held-token + lexical-only overlap (C2) — both residuals are exactly what the
  round-52 frozen predicates target. Coverage remains lowest axis (3.6364), consistent with C2 targeting
  coverage.
- **Round-51 verifier spotcheck** (`corpus/lessons/round-51-verifier-spotcheck.md`, committed at base):
  non-author integrator re-measured both predicates at final tip, re-opened S364 live against the pinned
  upstream (line 785 verbatim, sha256 match), ruled both "improved (bounded)", and routed to round 52:
  non-self context-bearing pointers (C1), proposition-bound citations with outside review (C2). Its
  discernment spot-check (§3) is one admit + one reject — the minimum sample; do not read it as a trend.
  It also rules W2's `tokens=[the]` attack non-reproducing (parser-incompatible) — do not perpetuate it.
- **PROVINCE.md**: config plane read-only; round-36 localization refusal boundary; corpus/knowledge is
  in-lane; upstream English Hyprland source channels are the lane's established source ground
  (rounds 50-51 precedent). C2's candidate surface (§3) stays inside it.
- **Mistakes**: M51-2 (source-truth overreach, captured-by none → fix added QUALITY 104) and M51-3
  (falsification fixture mismatch → QUALITY 105 requiring exact parser-compatible replay) both feed
  directly into the round-52 controls: outside source-truth review (C2) and exact red/green receipts
  with frozen-shape controls (C1). `mistake-candidate.md` M52-1 (claim-to-source binding) is consistent
  with this walk's findings.

## 6. Limitations

- I verified base absence/presence and counter behavior from committed bytes and receipts; I did not run
  either old counter myself (receipts at base are committed and consistent with the counter source I read).
- The "26 of 79 files contain their own basename" figure is round-51 seat evidence (`ScrLedgerRows`),
  not re-derived here; my own scan covered the ledger rows, not the population files.
- C2 distinct-surface note identifies candidate mechanism families from pinned bytes; it is not a
  proposition map and quotes nothing — builder seats must open/register rows and bind quotes.
- This report is lane-author planning evidence, not an outside verdict (per QualitySweep's own scope).

## Deliverables

- `.ufo/waves/round-52/w1/PlanDataWalk.md`

Report: `.ufo/waves/round-52/w1/PlanDataWalk.md`
