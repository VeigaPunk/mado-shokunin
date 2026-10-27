# QualitySweep — round 52

Seat: reviewer (lane-author review of frozen predicates). Base `85d57a818c3707397e21c840b6498b105ba798aa`.
Scope: review the frozen claims (`claims-frozen.md`, `registration.md`) and the round-51 spotcheck
(`corpus/lessons/round-51-verifier-spotcheck.md`) for frozen-predicate coherence, no-harm, and safety.
This seat does not render the outside/non-author source-truth verdict — that remains the independent
reviewer's job per the claims; everything below is predicate/controls/safety review from lane bytes.

## Deliverables

- `.ufo/waves/round-52/w1/QualitySweep.md` (this report)
- `.ufo/waves/round-52/w1/QualitySweep/c1-base-repro.txt` (base counter reproduction receipt)
- `.ufo/waves/round-52/w1/QualitySweep/c1-base.copy.txt` (copy of committed `receipts/c1-base.txt`)
- `.ufo/waves/round-52/w1/QualitySweep/c2-base.copy.txt` (copy of committed `receipts/c2-base.txt`)

## Verified before-state (measured at the frozen base)

| Frozen statement | Check | Result |
|---|---|---|
| "Existing counter at base reports 82/82 TARGET_MET" (claims-frozen C1) | Re-ran `quality/counters/c1-r51-ledger.py --repo <lane> --rev 85d57a8… --work <scratch>` (counter blob at base, sha256 `d5c2447d…`, identical to working tree) | `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET`, exit 0 — byte-identical to `receipts/c1-base.txt` (receipt copy in seat dir; repro receipt `QualitySweep/c1-base-repro.txt`) |
| "new counter absent" (claims-frozen C1) | `git ls-tree 85d57a8:quality/counters/` — 50 entries, newest `c1-r51-ledger.py`/`c2-r51-dispatch-entry.py`, no `*-r52*` | confirmed absent |
| C2 target entry absent at base | `git ls-tree 85d57a8:corpus/knowledge/` — 67 entries; dispatcher-family = `dispatcher-semantics-r25`, `dispatcher-surface-and-request-grammar-r26`, `hyprland-bind-key-match-r50`, `hyprland-dispatcher-dispatch-r51`; no r52 entry | confirmed absent; also matches `receipts/c2-base.txt` showing the old counter GREEN on the preceding r51 entry, which is exactly why registration marks that receipt untrusted for the r52 target |
| "No axis harm admissible" / claim separation | claims-frozen closing lines; control texts | C1 is measured on ledger/counter/control bytes, C2 on entry/source/counter; `controls/c2-do-nothing.md:3` appends no registry rows. PASS at the predicate level (one cross-claim harm vector found — F2 below) |
| Safety (source-only) | SKILL.md standing rules vs claims | Both claims are decidable from repo bytes at pinned revisions; no clause requires package queries, live reads, input capture, screenshots, producer execution or host mutation. The r51 counter itself refuses `/tmp` scratch roots and derives every byte from a scratch clone at `--rev` (`c1-r51-ledger.py:67-68, 382-388`). PASS |

Disk guard before work: `/fast` had 599G available. Scratch used: `/fast/scratch/hyaku/mado-r52/QualitySweep/`, removed on exit (receipts copied to the seat dir first). No installs; no package queries; no live reads; no web fetches (URLs quoted below are copied from committed lane text, not opened).

## Findings (severity-ordered; each names the attacked item/predicate)

### F1 — HIGH (coherence): the C1 do-nothing control cannot fail "specifically for self-pointer/context defects" under any invocation the frozen text implies

- Attacked: `registration.md` C1 sentence "It must pass on the existing production ledger at the base revision and fail on `controls/c1-do-nothing.md` specifically for self-pointer/context defects"; `claims-frozen.md` C1 "Demonstrate production pass and control fail at the frozen revision."
- Evidence 1 — the control trips a third defect family: `controls/c1-do-nothing.md` contains **two byte-identical rows** for `tools/mado-verify.sh`. Any uniqueness check flags a duplicate; a complete-population check against the 82-file repo population fails with `uncovered≈81` (coverage failure, not self-pointer/context). Neither is "specifically self-pointer/context".
- Evidence 2 — no existing interface can even feed the control: `quality/counters/c1-r51-ledger.py` CLI is only `--repo/--rev/--work/--checker` (`:357-361`); `LEDGER_REL` is hard-coded (`:64`) and ledger bytes are read from the counter's own scratch clone at `--rev` (`:382-388`). The new counter therefore MUST define the control invocation (e.g., a documented control mode that takes the control ledger path and derives population from the control's own rows, or a fixture clone with the control overlaid at the pinned rev), or the "specifically" clause is unverifiable.
- Bounded resolution (no predicate edit needed): the C1 red receipt must echo the exact control command and the counter's per-defect output for that run, and the control-mode semantics must be stated — either deduplicate the control's rows before evaluation, or have the counter report `dup=` alongside and show the self-pointer and context defects are present in the same run. Fixtures that silently rewrite the control before running it would defeat the control; the receipt must show the control bytes used (sha256) equal the committed `controls/c1-do-nothing.md`.

### F2 — MEDIUM (no-harm, cross-claim): new r52 counters are themselves instrument-population files; until the ledger gains rows for them, the round-51 C1 counter regresses to TARGET_MISSED at any tip that commits them

- Attacked: no-harm clause ("No axis harm admissible", claims-frozen) as interaction between C1-r52 deliverables and the inherited r51 predicate.
- Evidence: population = every file under `tools/`, `quality/*.py`, `quality/counters/*.py` (`c1-r51-ledger.py` docstring; claims-frozen C1 "unique complete population"); base run is green at 82/82 with `uncovered=0` (my repro). Committing `quality/counters/c1-r52-*.py` / `c2-r52-*.py` raises P; the old counter then reports `uncovered>0` → exit 1 at the r52 final tip.
- Resolution: integration must add an accountable ledger row for every new counter before scoring (non-self pointer + context-bearing description under the NEW counter, so both counters are green at the same revision), and re-run both counters at the final tip. Otherwise the operability axis shows measurable harm between base and tip.

### F3 — MEDIUM (coherence): "instrument-specific functional context" has no operational definition, and the production ledger's pointer mass is concentrated — the green/control calibration is C1's pinch point

- Attacked: `registration.md` C1 "a description containing instrument-specific functional context"; `claims-frozen.md` C1 "instrument-specific context checks".
- Evidence: at base the accountability-pointer column is heavily reused — my frequency pass over `quality/tool-ledger.md @ 85d57a8`: `` `PROVINCE.md:20` `` ×4, `.ufo/waves/round-51/registration.md` ×3, and multiple SCORECARD line anchors ×2. These are all legal **non-self** resolvable targets, so the new non-self check alone does not separate production from a synthetic ledger; the context check must do that work. Round-51's routed defect was that generic descriptions pass; if the context test is calibrated only against the control's two generic rows, it can either fail real production descriptions (green impossible) or be so loose the control passes (red impossible).
- Bounded resolution: define the context check mechanically inside the counter (e.g., description must share a non-stopword token with the instrument basename/function, or a fixed generic-phrase denylist that includes the control's own phrases: "generic accountability pointer", "commentary only", "nothing") and print per-row failure reasons so the red/green receipts are auditable. The claim's own limit sentence ("bounded accountability checks, not prose entailment") correctly caps what this proves; keep that limitation in the report.

### F4 — HIGH (coherence): "sources opened this round" is not decidable from the registry's `opened` column, because round 51 and round 52 share the same opening date (2026-10-27)

- Attacked: `registration.md` C2 "each maps to an opened-this-round `S###` row"; `claims-frozen.md` C2 "grounded in sources opened this round".
- Evidence: `corpus/SOURCES.md:11` header has `status` and `opened` columns; rows S364–S369 are all `mined | 2026-10-27` (`:313-318`) — opened during **round 51**, the same calendar date this round runs (`round-51-verifier-spotcheck.md:4` date 2026-10-27; spotcheck §4 confirms S364–S369 were the r51 additions). A date-equality check ("opened == today") cannot distinguish r51-opened rows from r52-opened rows; an entry citing S364–S369 would satisfy a naive check while violating the predicate's intent.
- Bounded resolution (implementable without predicate edits): operationalize "opened this round" as "S-row absent from `git show 85d57a8…:corpus/SOURCES.md`" (i.e., appended after the frozen base), or require the row's `used-by` cell to name the new entry's slug. The C2 counter/receipt must state which operationalization is enforced; otherwise the clause is receipt-prose only.

### F5 — MEDIUM (coherence): C2's "distinct dispatcher-execution mechanism" frozen condition is measured by nothing, and the r52 counter check list drops the lexical-novelty clause its r51 predecessor had

- Attacked: `registration.md` C2 "one new indexed entry on a distinct Hyprland dispatcher-execution mechanism".
- Evidence: at base, four dispatcher-family entries already exist (`dispatcher-semantics-r25`, `dispatcher-surface-and-request-grammar-r26`, `hyprland-bind-key-match-r50`, `hyprland-dispatcher-dispatch-r51` — base `git ls-tree`); the r51 entry already covers the dispatcher map lookup/press call, the legacy translator table, the `hyprctl dispatch` request path, submap handling, bind-field extraction and the result struct (entry head, my read at base). The r51 counter enforced novelty mechanically (clause (c) shingle-overlap ceiling; `receipts/c2-base.txt` shows `c ok=1 … max=0.1%` over 66 files + 3 candidates); the r52 registration's counter list — "proposition count, row/pin/quote bindings and index" — contains no distinctness/novelty clause, so a near-copy of the r51 entry on a marginal facet would pass the frozen tooling.
- Bounded resolution: carry distinctness in receipts and outside review, mechanically assisted — e.g., the C2 receipt records a `distinct-from:` line naming the four slugs above plus the specific new surface, and re-prints the r51-style shingle-overlap numbers against at least those four entries as disclosure (disclosure only; not proposed as a predicate amendment).

### F6 — LOW (coherence): C2's pin root is not pinned by the frozen text

- Attacked: `registration.md` C2 "a pin path/revision and exact located quote <=25 words".
- Evidence: the r51 predicate bound pins to a named directory (`.ufo/waves/round-51/fetch/`, per registration r51 and the entry's Pin manifest); the r52 registration says only "a pin path/revision". Without a named root, quote-in-pin verification can point at any in-repo path, weakening the binding check the counter is supposed to enforce.
- Bounded resolution: the C2 counter/receipt should define this round's pin root (by r51 precedent: `.ufo/waves/round-52/fetch/`) and verify each quote appears verbatim in the pinned bytes at the stated revision (the mechanism the r51 counter already used and the r51 spotcheck independently re-verified).

### F7 — LOW (claims hygiene): `claims.md` carries two `## C2` sections; `claims-frozen.md` is clean and must remain the sole authority

- Evidence: `.ufo/waves/round-52/claims.md` headers at `:5` (C1), `:13` (C2) and `:19` (C2 again) with different before-state narratives ("M51-2 …" vs "spot-check §5 …") and slightly different target wording ("material" vs "admitted" propositions; a "proposition→source table" named only in the second). `claims-frozen.md` contains exactly one C1 and one C2 (verified by full raw read). The two C2 variants are mutually satisfiable — no behavioral contradiction found — but a seat reading only `claims.md` could score against the wrong narrative. No predicate edit proposed; receipts should cite `claims-frozen.md` exclusively.

### F8 — LOW (evidence hygiene): committed `receipts/c1-base.txt` does not echo the verbatim command line

- Evidence: the receipt starts at `detail:` lines; the lane's standing rule is that measurement receipts echo verbatim commands (round-12 lesson R12-c, `corpus/lessons/round-12.md:106`). Impact is low — I reproduced the receipt byte-for-byte from the pinned base (seat-dir receipt `QualitySweep/c1-base-repro.txt` includes the full command) — but the new counters' red/green receipts should carry the exact argv per the frozen "Selftest includes explicit red/green receipts" clause.

## Coherence with the round-51 spotcheck routing

- Spotcheck §5 bullet 1 (`round-51-verifier-spotcheck.md:80`) routed C1's self-pointer/generic-description blind spot → claims-frozen C1 targets exactly non-self pointers + instrument-specific context. Aligned (F1/F3 name what remains to make it measurable).
- Spotcheck §5 bullet 2 (`:81`) routed proposition binding + outside source-truth review, and explicitly ordered the lane not to perpetuate the non-reproducing `tokens=` bypass → claims-frozen C2 states the token-predicate limitation without claiming the bypass reproduced, matching M51-3 (`corpus/lessons/round-51.md:38`) and the W2 correction. Aligned — no recycled false claim found.
- Spotcheck §5 bullet 3 (`:82`) (verdict-freshness / 13 unverifiable rows) is not covered by any r52 claim. Correct under the one-theme rule — but it stays an open residual; no r52 receipt may imply it was addressed.
- M51-2 (`corpus/lessons/round-51.md:36`) already recorded that the frozen C2 counter verifies bindings/lexical structure, not source truth; r52's addition of an independent non-author truth sample is the routed response. Aligned.

## Residual risk and verification gaps

- I reviewed frozen text and base bytes only; the wave's worker outputs (prototypes, fixtures, entries) were not reviewed and do not exist at base. F1/F4/F5/F6 must be re-checked against the actual committed counter/entry before scoring.
- I did not run the r51 C2 counter myself (read `receipts/c2-base.txt` only); its TARGET_MET-on-the-old-entry behavior is consistent with the registration's untrusted-for-C2 note but is not independently reproduced by this seat.
- "Substantive/material proposition" (C2) and "instrument-specific context" (C1) remain human-judged boundaries; the counters can only enforce the mechanical shadows. The claims' own non-entailment disclaimers are the correct cap — do not let report language upgrade them.
- The distinctness surface (F5) ultimately needs the outside reviewer; my finding only ensures the evidence exists to review.

## Limitations and scope statement

- No outside/non-author verdict is claimed or implied. No claim or predicate was edited; no tracked lane file was written; writes were limited to this report, the seat dir, and seat scratch. No git/jj mutation, no commits, no installs, no package queries, no live reads, no screenshots, no producer execution, no web fetches.
- Line anchors: `claims-frozen.md` (raw full read), `registration.md:7-15` (frozen predicates), `controls/c1-do-nothing.md` (whole file), `controls/c2-do-nothing.md:1-3`, `receipts/c1-base.txt`, `receipts/c2-base.txt`, `quality/counters/c1-r51-ledger.py:64,67-68,357-361,382-388`, `corpus/lessons/round-51-verifier-spotcheck.md:30-43,80-83`, `corpus/lessons/round-51.md:36-38`, `corpus/SOURCES.md:11,313-318 @ 85d57a8`, `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:1-34 @ 85d57a8`.
- Commands run (all read-only against the lane, writes only to seat scratch): `df -h /fast`; `git cat-file -e 85d57a8…^{commit}`; `git ls-tree 85d57a8:quality/counters/`; `git ls-tree 85d57a8:corpus/knowledge/`; sha256 compare of counter blob vs working tree; description-column frequency pass over `quality/tool-ledger.md @ 85d57a8`; the pinned-base counter reproduction recorded in the seat dir. Scratch removed after receipt copies were written.

## Report

- `.ufo/waves/round-52/w1/QualitySweep.md`
