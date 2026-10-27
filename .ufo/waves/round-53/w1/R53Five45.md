# R53Five45 — simplifier: C1 ledger counter and C2 proposition repair

role: simplifier (leaf; no subagent dispatch, no votes)
axes named: **coverage** (C2) and **operability** (C1)
lane base: `ad4bf2059bcfafe63671d262222908ee1fe8001c`
frozen claims read: `.ufo/waves/round-53/claims-frozen.md:5-13` (C1 at :7, C2 at :11)
routed r52 defects read as evidence: `corpus/lessons/round-52-verifier-spotcheck.md:38` and
`.ufo/waves/round-52/w2/Attack01.md:50-51`, `Attack02.md:68-76`, `.ufo/waves/round-52/w1/C1Simplify.md:175-178`
source-only: no URL opened, no fetch, no live read, no producer run; all source truth below is
the committed pinned bytes under `.ufo/waves/round-52/fetch/` at
`efb50993780079460b0cbed1363e2166a2de1d9f` (`SHA256SUMS` re-verified: 5/5 OK by `sha256sum -c`, exit 0).

## Attacked predicates (verbatim scope of this review)

- **C1** (`.ufo/waves/round-53/claims-frozen.md:7`): the new counter "returns TARGET_MET on the
  production ledger, TARGET_MISSED on a no-work control and each frozen forgery fixture, with
  exact population coverage and non-self pointers. This is a bounded structural accountability
  check, not semantic proof."
- **C2** (`:11`): "append-only correction clearly repairs those three propositions against
  opened pinned source bytes; a frozen counter rejects the old bytes and accepts corrected entry
  with quote/pin/proposition bindings; independent reviewer checks source truth."

I propose implementations and test cases; I do not amend either predicate.

## 0. Verdict in one paragraph

Both claims are reachable with **less** code than the r52 attempts. C1: keep the ledger's
three-cell shape, but make the description cell an **identity copy of the instrument's own
declared header line** and make the pointer cell **exactly one backticked repo path**. That
rejects every r52 forgery class measured here (F-all 82/82, repeated generic descriptions 82/82,
self-pointer 1/1; the nine laundering spellings die on the same rules) with 353 lines and a
25 ms in-memory selftest, where the r51 counter ran 1.97 s and accepted the three classes I
measured at base (the nine spellings are reproduced in `Attack02.md:68-76`). C2: keep the entry append-only and
add one errata table with a `Supersedes` column plus a frozen supersession set `{P16,P17,P18}`;
split P16 into two contiguous rows (the ≤25-word contiguous-quote rule makes one row
impossible), re-attribute P17 to `sendkeystate`, and re-scope P18 to after the scan. A 374-line
counter with a 57 ms run rejects the old bytes (`required_missing=3`, `quotes_unbound=1`) and
accepts the corrected bytes, and also rejects partial, spliced, fabricated, over-long and no-op
repairs.

The one real cost is a mechanical 82-cell rewrite of `quality/tool-ledger.md` descriptions
(measured total and deterministic below). If integration refuses that rewrite, the only honest
alternative is to delete the description column; keeping authored prose as evidence cannot
satisfy C1's forgery clause (measured: no lexical rule separates F-all from production).

## 1. Method and safety

- Lane tree read-only: all bytes came from `git show <rev>:<path>` / `git ls-tree`; every
  measurement ran against `--rev ad4bf205…` (or a scratch clone/fixture).
- Scratch only `/fast/scratch/hyaku/mado-r53/R53Five45` (401 MB peak, `df -h /fast` → 594 G
  available, 27% used; no ENOSPC). Removed before yielding; nothing written to the lane,
  fleet, siblings, scripts/templates/state/watchdog or shokuknow.
- No commits, jj, task, background jobs, package queries, installs, live reads, screenshots.
  The scratch clone used for the before/after fixtures asserted
  `git rev-parse --show-toplevel` = the scratch dir before every fixture commit.
- Reference counters (`sha256`, 353 and 374 lines) were scratch-only; they are **not** proposed
  as literal drop-in files (headers and constants must change), but the rules and the selftest
  matrices below are the proposed contract.

## 2. C1 before-state, measured at the frozen base

Production ledger at base: 82 population files, 82 data rows, 3 cells each; 85 pipe lines total
(header + rule + 82 rows + one fenced grammar example, `quality/tool-ledger.md:11-13`).

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev ad4bf205… --work <scratch>
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=ad4bf205…)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf205…
exit=0
```

Three forgery fixtures, committed in a scratch clone of the same tree, each scored by the r51
counter (read-only `git show` semantics, same population 82):

| fixture | change vs production ledger | r51 verdict |
|---|---|---|
| `fx-self-migrated` (`4ec072e…`) | one row pointer → `quality/tool-ledger.md` | `TARGET_MET`, exit 0 |
| `fx-generic` (`3042eee…`) | every description → `Generic accountability note.` | `TARGET_MET`, exit 0 |
| `fx-fall` (`5090025…`) | `Attack01/controls/F-all-forged.md` copied over the ledger (all 82 descriptions generic, real paths/pointers, `env python3` bigram) | `TARGET_MET`, exit 0 |

Exact commands:

```
python3 -I quality/counters/c1-r51-ledger.py --repo before --rev 4ec072ede7747f0bd20c4e78c1428e5098760ee0 --work w0
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=4ec072e…
python3 -I quality/counters/c1-r51-ledger.py --repo before --rev 3042eee43a34f83a1c1698f4795e66121cfd2698 --work w0
C1_R51: population=82 … empty_desc=0 … verdict=TARGET_MET rev=3042eee…
python3 -I quality/counters/c1-r51-ledger.py --repo before --rev 50900252530387df36bec855924634c8e49c405a --work w0
C1_R51: population=82 … empty_desc=0 … verdict=TARGET_MET rev=5090025…
```

This is the frozen before-state ("accepts repeated generic descriptions and ledger
self-pointers") reproduced at the round base, not taken on trust. The r52 attacks' other six
laundering spellings (bare basename, `./`, trailing `)`, `:x`, `//`, leading `/`, case, symlink
mode 120000) are reproduced in `Attack02.md:68-76` and all die on the rule set in §3: the
single-token variants (`//`, leading `/`, case, `:N`) are measured green→MISS below, the
composite forms fail rule 3 by construction and are covered by the selftest `second-token` case,
and the symlink is measured end-to-end.

## 3. C1 — proposed simplest counter

### 3.1 Schema (three cells, unchanged shape)

```
| `<repo-relative instrument path>` | <description> | `<accountability pointer>` |
```

Hard rules, all structural:

| # | rule | field on violation |
|---|---|---|
| 1 | population = `git ls-tree -r --name-only <rev>` filtered to `tools/**` + `quality/*.py` + `quality/counters/*.py`, `__pycache__`/`*.pyc`/`*.pyo` excluded | `population` |
| 2 | rows = pipe lines **outside fenced blocks**, header and rule skipped, exactly 3 cells | `dangling` |
| 3 | both path cells are **exactly one backticked token** (pointer may carry `:N`/`:N-M`); no prose fallback, no second token | `dangling` |
| 4 | each population path appears exactly once; `population == ledger_rows` | `dup`, `uncovered` |
| 5 | description **equals** `derive_desc(instrument bytes at rev)` — first line after the shebang carrying ≥6 alphanumerics, leading `#`/quote/emphasis punctuation stripped, cut at the first sentence end | `desc_unbound` |
| 6 | pointer target exists at rev as a **regular blob** (git mode `120000` refused) | `bad_pointer` |
| 7 | pointer target is not the ledger, not the row's own path (after `/`, `//`, case and `:N` normalization; a `./`-prefixed token instead
fails resolution), and not a peer instrument | `self_pointer` (ledger/own), `bad_pointer` (peer) |
| 8 | pointer target's bytes name the row's basename as a **name-bounded** token (`(?<![\w.-])base(?![\w.-])`), not a substring | `bad_pointer` |

Summary line (always last; exit 0 MET, 1 MISSED, 2 setup error):

```
C1_R53_SELFTEST: <n>/<n> passed            (always first)
C1_R53: population=<P> ledger_rows=<R> uncovered=<n> dup=<n> dangling=<n> bad_pointer=<n> self_pointer=<n> desc_unbound=<n> selftest=ok verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>
```

The selftest runs **inside every measurement** (25 ms) and prints its own `C1_R53_SELFTEST:
n/n passed` line before the summary; `--selftest` alone gives that receipt without a lane read. Measurement writes nothing, so `--work` is validated
(absolute, outside `--repo`) and otherwise unused — no clone, no sandbox, no refused-root list.

### 3.2 Why each rule is the minimum

- **Rules 1/4** are exactly the claim's "exact population coverage".
- **Rule 3** removes r51's whitespace-prose fallback. Production conforms 82/82 (measured:
  every pointer cell is one backticked path, 12 distinct targets), so the strict grammar costs
  nothing. It also kills eight of the nine Attack02 laundering spellings **by schema** — the
  cell is no longer `quality/tool-ledger.md` *and* an accountable doc, it is one token that must
  resolve. (`Attack02.md:68-75`; P08/P10/P11/P12 misclassification disappears with it.)
- **Rule 5** replaces r52's four-filter bigram clause, which is measured dead:
  `Attack01.md:50-51` reproduces `generic_desc=0 TARGET_MET` on F-all under both r52 byte sets.
  Identity cannot be forged without stating the instrument's own declared purpose; a forger who
  copies the header sentence has produced a *true* description, and the residual is then a
  property of the instrument's header, not of the ledger — which is exactly the bounded claim.
- **Rule 6** is the only thing that catches Attack02 P09 (symlink mode 120000); measured
  end-to-end in a 3-instrument fixture repo: `bad_pointer=1 TARGET_MISSED`.
- **Rule 7** gives "non-self pointers" a definition that does not depend on spelling:
  measured single-token variants `quality//tool-ledger.md`, `/quality/tool-ledger.md`,
  `Quality/tool-ledger.md`, `quality/tool-ledger.md:1` → all `self_pointer=1`; `./quality/…`
  → `bad_pointer=1`; the ledger in a second token → `dangling` (rule 3).
- **Rule 8** keeps the r51 licence (a comment naming the basename still counts) and adds the
  name-boundary so `mado-anims.py.bak` or `xmado-anims.py` do not satisfy it.

### 3.3 Reference measurement matrix (real lane, base, population 82)

| fixture | expected | observed (reference counter) |
|---|---|---|
| `ledger-migrated.md` (production paths/pointers, descriptions = `derive_desc`) | MET | `population=82 ledger_rows=82 … desc_unbound=0 verdict=TARGET_MET`, exit 0, 264 ms |
| production as-is (curated descriptions) | MISS (migration not applied) | `desc_unbound=82 TARGET_MISSED`, exit 1 |
| `fx-no-work.md` (header only) | MISS | `ledger_rows=0 uncovered=82 TARGET_MISSED`, exit 1 |
| one row missing | MISS | `uncovered=1` |
| duplicate row | MISS | `ledger_rows=83 dup=1` |
| row for a non-population path | MISS | `dangling=1` |
| 4-cell row (r52 control shape) | MISS | `dangling=2` (`c1-do-nothing.md`) |
| pointer → ledger (all rows) | MISS | `self_pointer=82` |
| pointer → own path (all rows) | MISS | `self_pointer=82` |
| pointer → ledger (one row) | MISS | `self_pointer=1` |
| pointer → peer instrument | MISS | `bad_pointer=1` |
| pointer → nonexistent doc | MISS | `bad_pointer=1` |
| pointer → real doc not naming the basename | MISS | `bad_pointer=1` |
| pointer cell with a second token | MISS | `dangling=1` (+`uncovered=1`) |
| `Attack01/controls/F-all-forged.md` | MISS | `desc_unbound=82 TARGET_MISSED` |
| `Attack01/controls/H4n-nameonly-forged.md` | MISS | `desc_unbound=82 TARGET_MISSED` |
| repeated generic descriptions | MISS | `desc_unbound=82` |
| empty description (`—`) | MISS | `desc_unbound=1` |
| production line-anchored pointers (79/82 carry `:N`) | MET | green row above (`desc_unbound=0`) |
| fenced grammar row present | MET | not parsed |

Post-commit simulation (counter itself in the population, real commit `09c53e0…`):

```
C1_R53_SELFTEST: 18/18 passed
C1_R53: population=83 ledger_rows=83 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 desc_unbound=0 selftest=ok verdict=TARGET_MET rev=09c53e0a3262c336022114069404f741b2f0d669
exit=0
```

### 3.4 Selftest matrix (18 in-memory cases; fixed-count guard)

Stub reader: 3 instruments + 2 docs, no git, no writes, 25 ms. Each case asserts a **named
field is non-zero** (not only the exit code); four positive cases must stay green:

`green` · `no-work`→uncovered · `missing-row`→uncovered · `dup-row`→dup · `dangling`→dangling ·
`4-cell`→dangling · `self-ledger`→self_pointer · `self-row`→self_pointer · `one-self`→self_pointer ·
`peer-instrument`→bad_pointer · `missing-doc`→bad_pointer · `name-absent`→bad_pointer ·
`second-token`→dangling · `line-anchor`→MET · `forged-desc`→desc_unbound · `desc-copy`→MET ·
`fence-skipped`→MET · `empty-desc`→desc_unbound.

Discrimination is two-sided when scored against a deliberately always-accept counter (the r52
`hole-probes.py` precedent, `C1CounterDesign.md`, "Six hole probes"): with the same suite the
always-accept counter must fail `no-work`/`self-*`/`desc_*` cases. Recommend the receipt record
both directions.

### 3.5 Migration cost (the only open decision for L1)

- `derive_desc` was run over all 82 instruments at base: **82/82 non-empty**, 0 failures
  (`NO-DESCRIPTION: 0 []`). Sample: `tools/mado-action-plan.py` → `mado-action-plan.py —
  fail-closed static action-plan safety gate (mado r16 / C2).`
- Rewriting the description cell of every row is mechanical, deterministic and total; the
  generated ledger measured green (§3.3). No instrument edits are needed.
- Consequence: a header edit to any instrument requires the matching ledger description edit in
  the same commit; the failure is explicit (`desc_unbound`, detail line names the path). This is
  the single-authority cost, and it is the same shape as a generated index.
- **Fallback if the L1 refuses the rewrite:** delete the description column (two cells). Then
  authored prose cannot exist in a conforming ledger, F-all-class fixtures become `dangling`,
  and the extractor disappears — but the human one-liner index is lost and the r51 gate's row
  grammar (3 cells) becomes stale. I recommend the identity rewrite over this: it keeps the
  artifact's shape and its human index at the price of one deterministic comparison.

### 3.6 Residual limits (must appear in the C1 receipt)

1. A pointer to an omnibus document legitimately naming many basenames (12 shared targets at
   base) is accepted; `Attack02` P13 (evidence cycle) and P14 (shared registry) remain possible.
   Bounded by the claim's own "structural accountability, not semantic proof".
2. A description that copies the instrument's own header is accepted — that is the design (it is
   a true statement by the instrument), not a bypass; do not claim more than "identity to the
   declared header".
3. The counter proves coverage/binding, never that an instrument is *useful* or that the
   pointer document *discusses* it beyond naming it.
4. The counter's own row is part of the population: its ledger description must equal its own
   header line, so the header and ledger row must land in the same commit (measured 83/83
   green).

## 4. C2 — the three defects, re-verified against pinned bytes

All line numbers are in `.ufo/waves/round-52/fetch/` (revision `efb5099…`, checksums OK).

**P16 (entry :28) — spliced quote, branch-conditioned event, third clause outside the quote.**
`Hyprland-ConfigActions.cpp` :1554 is `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);`,
:1556-1557 is `if (S.m_passPressed == 1) { if (!isMouse)`, :1558 is the PRESSED key call, and
:1576 is `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);`. The entry's space-joined quote occurs
nowhere contiguously (the verifier's finding at `round-52-verifier-spotcheck.md:38`). The
proposition is also imprecise: the key event only fires in the `m_passPressed == 1` branch, and
the "then clears" clause rests on :1576, which is in the locator but not the quote.

**P17 (entry :29) — wrong subject.**
`sendkeystate` spans :591-627 and owns `keyState`; `sendshortcut` spans :531-589 and has no
state field. The repeat logic at :619-622 is inside `sendkeystate`. The entry attributes it to
"sendshortcut's repeat branch" — false. P04 (:16) already states the same fact correctly, so P17
is also a duplicate (Attack07 A17).

**P18 (entry :30) — wrong localization.**
The scan loop is :565-571; the `if (!keycode)` guard is :573 and the `key not found` return is
:574, i.e. after the loop, inside the cache-miss branch opened at :559. "inside the scan" is
false.

## 5. C2 — proposed append-only repair (exact text to append)

The ≤25-word **contiguous** quote rule forces P16 into at least two rows: no contiguous excerpt
of ≤25 words spans the delivery block (:1554-1574) and the clear at :1576 (that span is 69
words), while :1554-1558 is 16 words and already shows the ordering and the branch guard. Two
rows are therefore both necessary and sufficient for P16; P17 and P18 each become one row.
Four rows supersede three IDs; the original rows stay untouched.

```markdown
## Errata (round 53; append-only source-truth repair of P16–P18)

The round-52 verifier spot-check (`corpus/lessons/round-52-verifier-spotcheck.md` §2, C2)
found three proposition-grounding defects against the pinned bytes at
`efb50993780079460b0cbed1363e2166a2de1d9f`: P16 spliced a quote across an elided guard,
P17 named the wrong function as the owner of the repeat branch, and P18 placed the error
return inside a loop that closes before it. The original rows above stay unchanged
(append-only); each row below supersedes one of them and carries exactly one contiguous
pinned fact, so its quote is a verbatim excerpt of a single pin span.

| ID | Supersedes | Corrected proposition | Source row | Pin:anchor | Quote (<=25 words) | Support class | Why it supports |
|---|---|---|---|---|---|---|---|
| P19 | P16 | `Actions::pass` sends the `modMask` modifier state before its delivery block, and sends a PRESSED key event only when `m_passPressed == 1` and the key is not a mouse button. | S371 | Hyprland-ConfigActions.cpp:1554-1558 | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` | direct | The mods call, the branch guard and the PRESSED call are one contiguous excerpt. |
| P20 | P16 | After the key/button delivery block, `Actions::pass` clears the modifier state. | S371 | Hyprland-ConfigActions.cpp:1576 | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` | direct | The clear call follows the block that closes at :1574. |
| P21 | P17 | `sendkeystate` calls `sendshortcut` a second time when the state is `repeat` and the first call succeeded. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:619-622 | `auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` | direct | `keyState` is `sendkeystate`'s local (:591-627); `sendshortcut` spans :531-589 and has no state field. |
| P22 | P18 | After the keymap-range scan assigns no keycode, `sendshortcut` returns `sendshortcut: key not found` from the cache-miss branch. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:565-574 | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` | direct | The loop closes at :571; the return at :573-574 executes after it. |

The repaired facts are bounded to these source lines: P19/P20 are the ordering and branch
condition of `Actions::pass` and its modifier clear; P21 is the reuse inside `sendkeystate`;
P22 is the post-scan miss return. No key event, socket request, or host state is claimed.
```

Quote word counts: 16, 4, 13, 12 (all ≤25); each was measured verbatim whitespace-collapsed
inside its pin span. The section-only form is the lane's r51 convention
(`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:318-…`); the original P16–P18 rows keep
their wrong text, so the errata heading must keep naming them (as above).

## 6. C2 — proposed simplest counter

Clauses (binding only; entailment stays with the reviewer):

- **(a)** entry exists at rev and is indexed in `corpus/README.md` by **basename** (the README
  row is `knowledge/…`, not `corpus/knowledge/…` — the r51 counter's `index_row` already knew
  this; a naive `ENTRY in readme` check is the trap I measured, `index=absent` on green bytes).
- **(b)** every row is parsed **by header name, never by column position** (the r52 landed
  counter's A01: it expected `| P## | S### |` and got `props=0` on its own entry).
  For each row: unique ID; `Source row` in the entry's `source:` list; `Pin` resolves to one or
  more `file:start-end` spans in `FETCH`; each file's SHA256 matches `SHA256SUMS`; quote ≤25
  whitespace words and a **whitespace-collapsed contiguous substring of one span**; rationale
  non-empty. Multi-span cells are supported (`:1554-1558,1576`), so the splice check is real
  rather than a schema accident.
- **(c)** append-only repair: errata rows carry `Supersedes`; each names an existing main row;
  the corrected proposition text must **differ** from the superseded text (no-op repair is not a
  repair); the errata row passes (b). Superseded main rows are excluded from (b); every other
  main row must pass. `superseded ⊇ {P16,P17,P18}` (frozen constant) — otherwise the old bytes
  could go green by fixing only P16, the single defect a mechanical check can see.
- **(d)** `--entry <file>` substitutes fixture entry bytes while pins/index/SHA resolve at
  `--rev`; no clone, no fixture commit. Writes nothing; 57 ms.

Summary line:

```
C2_R53_SELFTEST: <n>/<n> passed            (always first)
C2_R53: rows=<all> props=<main> superseded=<n> required_missing=<n> quotes_unbound=<n> quote_too_long=<n> pins_bad=<n> rows_bad=<n> index=<ok|absent> rev_pin=<0|1> selftest=ok verdict=<…> rev=<sha>
```

### 6.1 Measured matrix (committed bytes; scratch clone `before`)

| bytes | command | observed |
|---|---|---|
| old entry at base `ad4bf205` | `python3 c2-r53-props.py --repo before --rev ad4bf205…` | `rows=18 … superseded=0 required_missing=3 quotes_unbound=1 rows_bad=1 … TARGET_MISSED`, exit 1 |
| corrected entry committed `20d39b2…` (base + 4-row errata) | `--rev 20d39b2…` | `rows=22 props=18 superseded=3 required_missing=0 quotes_unbound=0 rows_bad=0 … TARGET_MET`, exit 0 |
| errata missing P22 (`fx4-partial`) | `--entry fx4-partial.md` | `rows=21 … superseded=2 required_missing=1 TARGET_MISSED` |
| "repaired" P19 quote splices :1558 + :1576 (`fx4-spliced`) | `--entry fx4-spliced.md` | `quotes_unbound=1 rows_bad=1 TARGET_MISSED` |
| fabricated P20 clear quote (`fx4-fabricated`) | `--entry fx4-fabricated.md` | `quotes_unbound=1 rows_bad=1 TARGET_MISSED` |
| 26-word quote, two rows (`fx4-long`) | `--entry fx4-long.md` | `quote_too_long=2 quotes_unbound=2 rows_bad=2 TARGET_MISSED` |
| P21 corrected text equals P17's (`fx4-noop`) | `--entry fx4-noop.md` | `rows_bad=1 required_missing=1 TARGET_MISSED` |
| bad SHA / bad pin file | selftest | `quotes_unbound=1 … MISSED` |

### 6.2 Selftest matrix (17 in-memory cases)

`green`→MET · `no-errata`→MISS · `spliced-quote`→MISS · `too-long`→MISS · `fabricated`→MISS ·
`bad-pin-file`→MISS · `bad-sha`→MISS · `no-index`→MISS · `src-outside`→MISS ·
`supersedes-unknown`→MISS · `empty-why`→MISS · `partial-required`→MISS · `dup-id`→MISS ·
`identical-proposition`→MISS · `quote-single-line`→MET · `pin-range-wider`→MET ·
`errata-chain` (two rows supersede the same ID) →MISS.

### 6.3 Limits (state these in the C2 receipt)

1. The counter cannot decide that P21's *subject* or P22's *localization* is true; it forces one
   bound supersession per frozen defect and the reviewer checks source truth. Do not claim
   automated entailment of P17/P18. (A `Scope` cell derived from the enclosing function would
   catch P17 mechanically — `sendkeystate` at :591 — but it needs a C++ brace scanner and is
   brittle; not recommended this round.)
2. The frozen `{P16,P17,P18}` set is a constant in the counter: it must be registered **before**
   data, or the predicate is retrofitted.
3. Semantic novelty remains the reviewer's; this repair adds no new source row, so C2 earns
   **no expansion credit** under its own sentence ("no claim of expansion credit unless an
   admitted entry rests on a source row opened this round and uncovered ground per coverage map").
4. The main table still contains P16–P18 as written; the errata section is the only supersession
   record. If L1 wants row-level markers, that is a rewrite, not append-only — record the choice.

## 7. Simplification: deletions and candidates (with evidence)

I found no semantic callers for the r51 checker or the r51 counters outside historical records. Note: **no `lsp` device is mounted in this session**, so these are text-grep results, not
semantic reference proof; the literal command is recorded.

```
$ grep -rn "check-tool-ledger\|c1-r51-ledger\|c2-r51-dispatch-entry" --include=*.py \
    --include=*.sh --include=*.md --include=*.json . | grep -v '^\./\.ufo/'
PROVINCE.md:118,120
quality/tool-ledger.md:9,113-119
SCORECARD.md:2780,2787
corpus/lessons/round-51.md:24,30
corpus/lessons/round-51-verifier-spotcheck.md:32,40
corpus/lessons/round-52-verifier-spotcheck.md:29,36
quality/check-tool-ledger.py:2,49-50,797,813,827
quality/counters/c1-r51-ledger.py:2,4,7,34,52,63,65
quality/counters/c2-r51-dispatch-entry.py:6
```

- **Deletion candidate:** `quality/check-tool-ledger.py` (832 lines) + `quality/counters/c1-r51-ledger.py`
  (445 lines) + their two ledger rows. Their clauses (population, coverage, pointer resolution)
  are subsumed by the r53 counter; the r51 checker cannot agree on the new fields, and r51's
  cross-check is 932 ms of the 1.97 s runtime (checker selftest alone, measured).
  **Recommendation: do not delete this round.**
  The lane keeps superseded counters as provenance (`c1-r40-live.py` *and* `c1-r40-live-v2.py`
  both remain), SCORECARD rows 2780/2787 cite them, and PROVINCE.md records them as instruments.
  Instead: mark the r51 checker superseded in its docstring and ledger row, and let the r53
  counter be the only ledger gate. Deleting them here would strand the SCORECARD capability
  rows (2780/2787), the PROVINCE instrument record, and the two ledger rows.
- **Drop, not delete:** r51's clone/sandbox/checker cross-check machinery, the prose pointer
  fallback, and the bigram context clause — none is carried by the proposed counter. Measured
  effect: 1.97 s → 264 ms; 445 + 832 (r51 pair) and 847 (r52 draft) lines → 353 lines; 25 ms
  selftest vs the r52 draft's fixture-repo selftest block (~230 of its 847 lines, per
  `C1Simplify.md` §9).
- **Keep:** fence skipping (measured 83 vs 82 rows when omitted — the exact r52 landed-counter
  O1 regression), `:N`/`:N-M` strip (79/82 production pointers carry one, so the strip is
  load-bearing), name-bounded basename
  and the base-relative population filter.

## 8. Axis statement (coverage + operability, no harm)

- **operability (C1): improves.** One gate, one schema, a mechanical 82-row migration, 7.5×
  faster measurement, an in-memory selftest that runs with every measurement, and all measured
  r52 forgery classes rejected. Cost: header/ledger coupling (explicit failure).
- **coverage (C2): quality repaired, expansion unchanged.** Three false propositions get bound,
  contiguous, append-only corrections; no new S-row, so no expansion credit. The counter blocks
  partial repairs, which is the failure mode that harmed r52.
- **No axis harmed:** no tracked file was modified, no capability claimed, no score changed; the
  proposal cannot be satisfied by a no-work ledger (measured), which is the harm the claims
  guard against.

## 9. Report trailer

- Report: `.ufo/waves/round-53/w1/R53Five45.md`
- Lane tree: read-only for this seat. `git status --porcelain` at yield shows
  ` M corpus/SOURCES.md` (a sibling appended row S374 at 12:51), `?? corpus/lessons/round-53.md`
  (12:55) and `?? .ufo/waves/round-53/` (this report lives inside it). The first two are sibling
  work that appeared during this run; this seat wrote neither and did not touch them.
- Scratch `/fast/scratch/hyaku/mado-r53/R53Five45` (401 MB: reference counters, migrated ledger,
  fixtures, one scratch clone with its fixture branches) removed on completion; nothing written
  outside this report and that scratch.
- Reference artifacts (scratch, sha256): `c1-r53-ledger.py` `9a90565052d1…` (353 lines);
  `c2-r53-props.py` `617474ef65bb…` (374 lines, after the no-op-repair and manifest-coverage
  checks); migrated ledger
  `53719334cedd…`; corrected entry `entry-4row.md` `d174acb50dbe…`.
- Tooling: preinstalled `python3`, `git`, `sha256sum` only; no installs, no package queries, no
  network fetch, no live read, no screenshot, no producer execution, no git/jj mutation of the
  lane (fixture commits only inside the scratch clone).
