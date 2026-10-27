# Attack31 — C2 duplicate claims / row completeness (w2, reviewer, leaf)

Attacked claim clause: frozen C2 (`.ufo/waves/round-52/claims-frozen.md`) — "each material
factual proposition maps to a pinned source quote <=25 words … with a written support
rationale; a new committed counter checks proposition count, row/pin/quote bindings and
complete mapping" — read as: **no duplicate propositions, no unmapped/stale rows, quotes
actually located at pins.** Attacked artifacts: the landed (uncommitted) counter
`quality/counters/c2-r52-proposition-entry.py`, the landed entry
`corpus/knowledge/hyprland-synthetic-dispatch-r52.md`, landed registry rows S370–S373, and
the W1 draft counter `.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py`.

Method: scratch clone of the lane at base `85d57a81`, overlaid with the exact uncommitted
worktree bytes (modified `corpus/README.md`, `corpus/SOURCES.md`, `quality/tool-ledger.md`,
new `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`, `corpus/lessons/round-52.md`,
both counters, `.ufo/waves/round-52/fetch/`), committed as fixture rev `2c68a4b8`. A
"green-variant" (same content, table reordered to satisfy BOTH counter grammars, contiguous
P16 quote, pin-path anchors, one `sourced: P01-P18` line) is the MET baseline; 15 one-change
mutants probe each counter. Driver + full receipts: `.ufo/waves/round-52/w2/Attack31/`.
No tracked edits, no fleet/lane writes, no network, no installs; git mutation confined to
`/fast/scratch/hyaku/mado-r52/Attack31/repo` (toplevel asserted).

## Findings by severity

**F1 [HIGH] The landed counter is unsound in both directions and checks almost nothing of
the predicate.** `quality/counters/c2-r52-proposition-entry.py` (47 lines) is a rewrite of
the W1 draft, not a copy. Reproduction: `python3 -I quality/counters/c2-r52-proposition-entry.py
--repo <clone> --rev HEAD --work <work>` on the committed landed state:

- Default args → `entry=absent TARGET_MISSED` (receipt `r1-landed-default.txt`): its
  `--entry` default is the **stale draft slug** `hyprland-synthetic-key-dispatch-r52.md`;
  the landed entry is `hyprland-synthetic-dispatch-r52.md`.
- `--entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md` → `props=0 … TARGET_MISSED`
  (`r2`): its proposition regex requires the S-id in cell 2; the landed table has it in
  cell 3. It cannot parse the entry it was committed to check.
- Depth: it never opens a pin (pin/anchor cells are regex-captured then discarded), never
  checks quote-at-pin, duplicates, unmapped rows, id-citation, or ≥2 distinct rows, and
  parses `--base` but never uses it (`grep 'a\.base'` → no hits), so the
  opened-this-round/absent-at-base gate is gone entirely; `mined`/`2026-10-27`/`used-by`
  are bare substring tests over the whole row line. Escape matrix (all `TARGET_MET`,
  receipts `m-*.txt`): dup-claim, dup-quote, fab-quote, phantom-pin, unmapped-cited,
  unmapped-uncited, orphan-prop, single-row, row-reuse, rowmeta-spoof, empty-claim — 12/16
  mutants escape; it catches only missing-row, index-removed, quote-26w. Verdict:
  **falsified** — the landed counter cannot demonstrate the C2 predicate in either
  direction as committed.

**F2 [HIGH] Landed P16's quote is a fabricated splice — violates "exact located quote".**
`corpus/knowledge/hyprland-synthetic-dispatch-r52.md` P16 quotes
`sendKeyboardMods(modMask, 0, 0, 0); … sendKeyboardKey(S.m_timeLastMs, key - 8, …)` at
anchor `ConfigActions.cpp:1554-1558,1576`. Pin bytes
(`.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp`) put the first call at :1554 and
the second at :1558 with `if (S.m_passPressed == 1) {` / `if (!isMouse)` between; the
concatenated text occurs nowhere contiguously. The W1 draft counter catches it:
`P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)` (`r4-draft-landed.txt`, clause d
FAIL). The landed counter passes it silently because it never opens the pin (F1).
Verdict: **reproduced defect** on landed bytes.

**F3 [MED] Landed P17 is a duplicate claim of P04 — and factually wrong.** P04:
"`repeat` calls its delegate again only after a successful first call" quoting
`sendshortcut`'s second delegate guard at DT.cpp:619-622. P17: "`sendshortcut`'s repeat
branch can invoke its delegate twice for a successful repeat state" quoting a substring of
the same lines — the same fact, claimed twice (proposition-count padding). It is also
wrong: :619-622 sits inside `sendkeystate` (def :591); `sendshortcut` (def :531-590) has
no repeat branch and no `sendshortcut(modifiedArgs)` call site. Mutation `dup-claim`
(exact-copy) is caught only by the draft (`miss=duplicate_claim:repeat calls its delegate
again only after a successful first call`); `dup-quote` likewise
(`duplicate_quote:auto result sendshortcut modifiedargs …`); the semantic paraphrase
(`near-dup-claim`) escapes **both** counters — duplicate detection is exact-normalized-key
only, an honest syntactic boundary. Verdict: **reproduced** as landed duplicate +
misattribution; only exact duplicates are mechanically gated even by the draft.

**F4 [MED] Landed P06 duplicates held round-51 ground.** P06: "`sendshortcut` requires
exactly three fields", S370, DT.cpp:531-535 — identical to held
`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md` step 7 ("demands exactly three
comma-separated fields and rejects anything else … :532-535", errata-narrowed to the
dispatcher-time read). Same claim, same cited lines, dressed under a new row id. No
counter can see it (cross-entry duplicate detection does not exist); it adds zero
coverage. Verdict: **reproduced** (duplicate-authority; bounded — P06 is load-bearing
neither for the ≥4 count nor the subject's distinctness).

**F5 [MED] Landed P07 restates held parser behaviour.** P07 claims `stringToModMask`
"uppercases input and checks known modifier names using substring membership" —
already held at `corpus/knowledge/bind-table-r25.md:44` (S162: "uppercasing then
substring-matching tokens, making token order immaterial"). The W1 draft deliberately
claimed only the `sendshortcut`-path consequence (silent mask-0) with the held cite; the
landed text claims the parser itself. Verdict: **reproduced** (duplicate-adjacent;
partially observation-tier, so bounded).

**F6 [MED] Row-completeness hole shared by both counters: a fresh `used-by`-only row is
invisible.** Mutant `unmapped-uncited` appends S375 (`mined`, `2026-10-27`, `used-by` the
entry, 40-hex + fetch pin in anchor) mapped by no proposition and cited nowhere:
**landed MET, draft MET** (`m-unmapped-uncited.txt`). The draft's own clause-(e) text
("every registry row this entry opened is mapped by a proposition") is falsified against
its implementation, which scopes "opened by this entry" to prose citations. Contrast:
`unmapped-cited` IS caught by the draft (`miss=row_unmapped:S374`) but escapes the landed
counter. Verdict: **reproduced** in both; bounded — the frozen predicate speaks of
proposition→row mapping, so this is a registry-hygiene invariant the counter advertises
but does not enforce.

**F7 [LOW] QUALITY17 review fired as W04 warnings but the explicit review is unrecorded.**
`.ufo/waves/round-52/census-after.txt:24-26` flags S370/S371/S373 as duplicate URLs; the
criterion (QUALITY.md ~line 34) says a warning-only census is *not* the review and
distinct-scope reuse goes to explicit/human review. `w1/RegistryContract.md` demanded it.
No record found in `corpus/lessons/round-52.md`. Anchor regions ARE disjoint
(S370 :531-627 vs S365 :30-35,797-867; S371 :1530-1616 vs S367 :1664-1682; S373 :221-242
vs S352 :369-899-spans / S364 :41-823), so the rows likely survive review — but S370's
scope wording "argument parsing" sits inside S365's declared scope "how implementations
parse arguments", which is precisely the wording-overlap case review exists for.
Verdict: **gap confirmed** (process, not byte defect).

**F8 [LOW] Landed counter parse-fragility: malformed table rows are silently dropped.**
An 8-cell P19 row (first battery run) was not counted or flagged: `props=18` with
`failures=0`. A row that fails the regex vanishes instead of erroring — an entry can shed
bad rows rather than answer for them. Also `empty-claim` (blank claim cell) escapes the
landed counter (regex `[^|]+` accepts whitespace) while the draft reports
`P02:empty(claim)`. Minor: `--work` is required but only gates a `/tmp` refusal (no
artifact written); `GIT_*` env scrubbing was dropped vs the draft. Verdict:
**reproduced**.

**F9 [INFO] Draft-counter receipts on landed bytes (for L1's integration decision).**
`r4-draft-landed.txt`: clause (a) PASS (index row present), (b) PASS (18 props), (c)
FAIL `anchor_no_fetch_root` on all 18 — landed anchors say `r52 fetch SHA256 …`, the
draft requires the literal `.ufo/waves/round-52` path; (d) FAIL `P16:quote_not_at_pin`;
(e) FAIL `id_not_referenced` on all 18 — the landed entry never cites a P-id outside the
map (its intro says "see the proposition map", never P01…). So under the W1 counter the
landed state is 2/5 TARGET_MISSED; under the landed counter it is vacuous MISS (F1) or,
in its own grammar, vacuous MET (12/16 escapes). Either way **no currently committed
artifact demonstrates the C2 predicate**.

## Residual risk / verification gaps

- Fixture is a faithful overlay of the *uncommitted* landed state; if integration is
  still in flight, F1/F2/F3 may be transient — but all defects are on real bytes, not
  hypotheticals, and receipts are reproducible via `Attack31/driver.py`.
- I did not fetch URLs (source-only bounds); pin identity rests on the lane's own
  `SHA256SUMS` and the committed fixture bytes.
- Semantic-duplicate judgment (P04/P17, P06, P07) is evidence-cited, not a verdict on
  admission — non-author judgment remains with the canonical reviewer per role bounds.
- The `near-dup-claim` escape marks the syntactic floor of *any* exact-key duplicate
  check; a paraphrase battery would need seat-level (non-mechanical) review.

Report trailer:

```
seat=Attack31 wave=w2 round=52 lane=mado-shokunin base=85d57a818c3707397e21c840b6498b105ba798aa
target=C2 duplicate claims / row completeness
fixture=/fast/scratch/hyaku/mado-r52/Attack31/repo rev=2c68a4b8 (landed-state commit) + GREEN tag
artifacts=.ufo/waves/round-52/w2/Attack31/{driver.py,receipts/}
landed_counter: vacuous-both-ways; 12/16 mutants escape (receipts m-*.txt)
draft_counter: catches landed P16 splice + 11/16; escapes unmapped-uncited row + semantic dup
landed_entry: P16 fabricated quote (not at pin); P17 dup-of-P04 + wrong function; P06/P07 duplicate held ground
verdict=findings reproduced; C2 not demonstrated by any committed artifact at fixture rev
```
