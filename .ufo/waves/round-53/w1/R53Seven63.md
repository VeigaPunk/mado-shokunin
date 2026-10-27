# R53Seven63 — simplifier: smallest maintainable C1 counter and C2 repair

Axes: **operability** (C1) and **coverage** (C2). Seat role `simplifier` (leaf). Base tip
`ad4bf2059bcfafe63671d262222908ee1fe8001c`. No tracked edit, no commit/jj, no host or live
read, no package query, no campaign-tool run. This is a design-and-weight review with
executed prototypes; it is not a claim verdict, an admission, or the non-author review.
Scratch `/fast/scratch/hyaku/mado-r53/R53Seven63` (452 KB, removed before yield).

## 0. Attacked predicates (frozen, quoted)

- **C1** (`.ufo/waves/round-53/claims-frozen.md`): "a newly committed, scratch-aware counter
  with explicit selftest returns TARGET_MET on the production ledger, TARGET_MISSED on a
  no-work control and each frozen forgery fixture, with exact population coverage and
  non-self pointers."
- **C2** (same file): "append-only correction clearly repairs those three propositions
  against opened pinned source bytes; a frozen counter rejects the old bytes and accepts
  corrected entry with quote/pin/proposition bindings."

Two things I can settle by measurement rather than opinion, and do below:

1. **"each frozen forgery fixture" names no fixture.** `ls .ufo/waves/round-53` →
   `claims-frozen.md  w1  w1-dispatch.json  w1-spec.json  w1.ready  w1.ready.dispatched`.
   There is no `controls/` and no fixture file, so the clause is unbounded as frozen. Under
   its strongest reading (the r52 `F-all` class, `Attack01.md` §T2) **no lexical clause can
   satisfy it**, measured in §1.4. The registration must name fixture paths and sha256s, or
   the clause is dead on arrival.
2. **The three C2 defects are exactly as routed, and each has a one-record, byte-backed
   repair** (§2.1). Two of the three are *not* quote failures: P17 and P18 have contiguous
   quotes and fail only on subject and localization.

## 1. C1 — smallest counter that keeps the r52 green fields and kills the measured forgeries

### 1.1 Measured state at base

- Population at `ad4bf20` under the ledger's own rule (files under `tools/`, `quality/*.py`,
  `quality/counters/*.py`; `__pycache__`/`.pyc` excluded): **82**.
- `git show ad4bf20:quality/tool-ledger.md` → 119 lines, **82 data rows**; a naive pipe scan
  returns 83 because the grammar example sits in a fenced block, and 79 if you stop at the
  prose paragraph that splits the table. Both parser traps are real and load-bearing.
- Pointer targets: 14 distinct; **0 are symlinks** (`git ls-tree -r` mode `120000` check), so
  rejecting symlink pointers costs nothing on production (38 symlinks exist elsewhere in the
  tree, so the case is not hypothetical).
- No C1 counter is committed: `git ls-tree -r ad4bf20 quality/counters/ | grep -E 'r5[23]'`
  → empty.

### 1.2 Simplest implementation (prototype, 277 lines incl. docstring + selftest)

Two reads only: `git ls-tree -r <rev>` (paths + modes) and `git show <rev>:<path>`. No
clone, no work tree, no child process, no writes; `--work` is accepted and ignored.

```
LEDGER53: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0
          self_pointer=0 generic_desc=0 verdict=TARGET_MET
```

Clauses, each one attached to a measured falsifier it closes:

| # | Clause | Kills (measured) |
|---|---|---|
| R1 | population = `tools/**` + `quality/counters/*.py` + `quality/*.py`, `.pyc/.pyo` excluded | exact-coverage clause |
| R2 | data rows = 3-cell pipe rows outside fences, header/separator skipped | 83-vs-82 fence trap; prose-split table |
| R3 | pointer cell must be **exactly one backticked token** | P03–P08, P15, P19–P21 (`… and docs/…` two-token laundering) |
| R4 | identity normalization: strip `:N`/`:N-M`, `./`, leading `/`, collapse `//`, strip trailing `.,;:)]}`, casefold; basename fallback for slash-free tokens | P03/P04/P05/P06/P07/P19/P20/P21 |
| R5 | `self` = identity equals ledger path **or** row path, full path **or** basename; plus ledger path always excluded even when `--ledger` names a control | r52 C1Simplify §5 false-green on control C |
| R6 | pointer must be a regular blob at rev (mode ≠ `120000`) whose bytes name the row's basename | P09 (symlink alias), P10, and the `names-nothing` class |
| R7 | description: non-placeholder, not shared verbatim, and not one **row-identity template** shared by ≥3 rows (digits and the row's own path words masked) | F3 (45/82), Attack01 `F-all` (81/82), all-index-substituted ledgers |

### 1.3 Measured matrix (all runs at `ad4bf20`, read-only, `--ledger` for fixtures)

Command shape:
`python3 -I c1-r53-proto.py --repo <lane> --rev ad4bf20 [--ledger <fixture>]`

| fixture (built from the production bytes, 82 rows) | result | rc |
|---|---|---|
| production ledger (rev bytes) | `TARGET_MET`, all fields 0, **65 ms** | 0 |
| r52 `controls/c1-do-nothing.md` (`ad72f72f…`) | `uncovered=82 dangling=2` MISSED | 1 |
| r52 `controls/c1-row-context-control.md` | `uncovered=81 dup=1 generic_desc=1` MISSED | 1 |
| all pointers → bare `tool-ledger.md` | `self_pointer=82` MISSED | 1 |
| one pointer → `quality//tool-ledger.md` | `self_pointer=1` MISSED | 1 |
| one pointer → `Quality/tool-ledger.md` | `self_pointer=1` MISSED | 1 |
| one pointer → `` `quality/tool-ledger.md)` `` | `self_pointer=1` MISSED | 1 |
| one pointer → `./tool-ledger.md` | `self_pointer=1` MISSED | 1 |
| one pointer → own basename (`mado-assessment.py`) | `self_pointer=1` MISSED | 1 |
| one pointer → a real mode-120000 symlink | `bad_pointer=1` MISSED | 1 |
| one duplicated row | `dup=1` (+`generic_desc=1`) MISSED | 1 |
| F3-forged (`15fe970d…`) | `generic_desc=45` MISSED (r52 draft: 10) | 1 |
| Attack01 `F-all-forged` (`d793c9ef…`) | `generic_desc=81` MISSED (r52 draft: 0) | 1 |
| H-minimal-forgery (`f4e5bba1…`) | `TARGET_MET` | 0 |
| per-row **distinct**-phrase forgery (this seat) | `TARGET_MET` | 0 |
| legit ledger-reader description | `TARGET_MET` | 0 |
| selftest (`--selftest`, literal ledgers + stub reader, no git) | `C1_R53_SELFTEST: 3/3 passed` | 0 |

### 1.4 The honest ceiling (do not claim past it)

R7 is **template detection, not context detection**. `F-all` dies only because the forger
reused one phrase ("env python3") for most rows; my per-row distinct-phrase ledger
(`sha256 d7c24dce…`, 82 distinct pairs lifted from each instrument's own bytes) passes
`TARGET_MET` at 82/82. A single-row forgery (H) passes too. So:

- Do not put a "distinguishes generic from functional descriptions" claim in the C1 receipt.
  Write: *the description clause rejects placeholders, verbatim reuse and row-identity
  templates; it does not entail that a description is true or functional.*
- If the freeze intends to score F-all/H-class forgeries, the claim cannot be met by any
  structural counter (r52 `Attack01` §T2 measured the same on both r52 candidates). Bound the
  fixture class in the registration instead — e.g. freeze exactly `c1-do-nothing`,
  `c1-row-context-control`, `F3-forged` (+ optionally `F-all-forged`) by path and sha256, and
  state that per-row-distinct-phrase forgery is out of class because it is unmeasurable
  lexically.

### 1.5 Bootstrap traps the integrator must handle (measured)

- Committing the counter changes the population 82 → 83 **and** needs its own ledger row:
  production bytes + the new row, scored at base, gives
  `dangling=1 bad_pointer=1` (`…:target-names-nothing=PROVINCE.md:20`). Score the production
  run **at the commit that adds counter + row + `PROVINCE.md` name**, or the receipt is red
  by construction.
- "Scratch-aware" should be defined as *no scratch is created*: the counter writes nothing,
  so the honest test is `--work <scratch>` → identical output and zero files created. Do not
  reintroduce the r52 harness's clone/`git add`/commit path (it was the only mutating code in
  the round, and it timed out at 110 s / 300 s under load while the counter itself takes 65 ms).
- Weight that should not come back: r51 wrapper 445 lines (2154 ms, r52-measured) and its
  sandboxed re-run of `quality/check-tool-ledger.py` with regex cross-comparison of six
  numbers; r52 draft 847 lines with the `Suite`/`fixture_repo`/`commit` selftest block
  (~230 lines). Neither clause is in the frozen predicate.

## 2. C2 — the three defects, the smallest append-only repair, and its counter

### 2.1 Source truth (pinned bytes reopened this round)

Pins: `.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp` (`sha256 a83abeb57175…`, upstream
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp`)
and `…/Hyprland-legacy-DispatcherTranslator.cpp` (`sha256 7248cbb89f89…`, upstream
`…/src/config/legacy/DispatcherTranslator.cpp`), revision `efb5099…`, opened 2026-10-27,
`sha256sum -c SHA256SUMS` → 5/5 `OK`.

- **P16 — spliced quote.** :1554 is `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);`; the
  key send is :1558, behind `if (S.m_passPressed == 1) { if (!isMouse)` at :1556-1557; the
  clear is :1576. The committed quote joins :1554 and :1558 with `; ` and is **not present
  anywhere contiguously** (measured `False`). The contiguous :1554-1558 excerpt is 16 words.
- **P17 — misattributed.** `sendshortcut` spans :531-589; `sendkeystate` spans :591-627;
  :619-622 (`auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) …`)
  is inside `sendkeystate`. P17's quote is a **substring of P04's quote at the same pin** —
  measured duplicate pin `{Hyprland-legacy-DispatcherTranslator.cpp:619-622: [P04, P17]}`.
- **P18 — mislocalized.** the scan loop is :565-571; :573-574 is `if (!keycode)` /
  `return {.success = false, .error = "sendshortcut: key not found"};` — after the loop, not
  "inside the scan".

### 2.2 Simplest repair (append-only, 4 records, one row withdrawn)

Append one `## Errata (round 53, append-only)` section; leave the table untouched:

- `E01 — supersedes P16 (spliced quote)`: pin `ConfigActions.cpp:1554-1558`, the **contiguous**
  16-word excerpt above, proposition restated to ordering only.
- `E02 — supersedes the P16 clear clause`: pin `ConfigActions.cpp:1576`, quote
  `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` (4 words).
- `E03 — supersedes P17 (misattributed subject)`: **`action: withdraw`**, justified
  mechanically — names `P04`, same pin, withdrawn quote is a substring of P04's. This deletes
  a duplicate authority instead of restating the same fact twice.
- `E04 — supersedes P18 (mislocalized return)`: pin `…DispatcherTranslator.cpp:565-574`, quote
  `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` (12 words).

### 2.3 Counter (prototype, 260 lines, 35 ms) and matrix

Grammar: `### E## — supersedes P##` + `- defect|action|proposition|row|pin|quote:` lines.
Checks: quote ≥1 and ≤25 words; quote verbatim (whitespace-collapsed) inside **one** of the
row's own pin ranges; `S###` row exists in `corpus/SOURCES.md`; every frozen defect row is
covered by an errata record; a `withdraw` record must name a duplicate row with the same pin
and a containing quote; superseded rows are exempt from their own quote check (a repair
record must carry a verified quote, so the exemption is not free).

| input | output | rc |
|---|---|---|
| committed entry at `ad4bf20` (old bytes) | `propositions=18 errata=0 covered=0/3 TARGET_MISSED`; `bad: P16:quote-not-contiguous-in-pin`, `P16/P17/P18:no-errata-record` | 1 |
| corrected fixture `entry-corrected.md` (`3ca8438b…`) | `propositions=18 errata=4 superseded=3 covered=3/3 quote_words_max=19 TARGET_MET` | 0 |
| m1 E01 re-spliced | `E01:quote-not-contiguous-in-pin` MISSED | 1 |
| m2 E03 removed | `P17:no-errata-record` MISSED | 1 |
| m3 E04 pin narrowed to :565-566 | `E04:quote-not-contiguous-in-pin` MISSED | 1 |
| m4 E03 withdraw names P01 | `E03:withdraw-pin-mismatch` MISSED | 1 |
| m5 E04 defect line removed | `E04:defect-unstated` MISSED | 1 |
| m6 E01 quote >25 words | `E01:quote-not-contiguous-in-pin` + word cap MISSED | 1 |
| selftest (literal entry + stub pin reader, no git) | `C2_R53_SELFTEST: 2/2 passed` | 0 |

Residual bound: the counter checks bindings, not entailment. A correct quote under a false
proposition passes; that is what the independent reviewer is for. State it in the receipt.

## 3. Duplicate authorities and dead paths (deletion candidates, not deletions)

**Deletions made: none** — the seat holds no tracked edit scope. **`lsp` unavailable:**
`write xd://lsp` → `No such tool: xd://lsp` (no LSP device mounted, no server answering
Python in this lane). Every caller claim below is therefore a **literal grep fallback**, not
semantic reference proof.

| candidate | literal callers (grep, `--exclude-dir=.git --exclude-dir=__pycache__`) | recommendation |
|---|---|---|
| `.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py` (847 L) | wave reports/receipts only (`C1Mutation.md`, `Falsify25.md`, `C1Fixture/receipts/*`) | keep as provenance of the rejection; never integrate. No code caller exists, so nothing breaks |
| `.ufo/waves/round-52/w1/C1Simplify/c1-r52-ledger.py` (194 L) + the 78-line landed rewrite (absent at base) | same wave dirs | same; mark superseded in round-52's lesson rather than delete |
| `.ufo/waves/round-52/w1/C2EntryDraft/{entry-draft.md,proposition-map.tsv}` (251 L + 19 L) | wave reports only | **competing proposition authority** with a different P16–P18. Mark superseded by the committed entry; do not let a third map into the round |
| `quality/counters/c1-r51-ledger.py` (445 L) | `PROVINCE.md`, `corpus/lessons/round-51*`, `round-52-verifier-spotcheck.md`, `.ufo/waves/round-51/**`, `quality/tool-ledger.md:118` | keep (cited by SCORECARD:2787 and the r51 freeze); the r53 counter must not call it, and must not re-run `check-tool-ledger.py` |
| `quality/check-tool-ledger.py` (832 L) | `PROVINCE.md`, `quality/tool-ledger.md:9,113`, `SCORECARD.md:2787`, wave dirs | keep as the lane gate; **one** gate owns each field, and the C1 receipt says which |

Stop point: the next deletion (either ledger gate) would remove a cited contract, and the
next merge (folding the r53 clauses into `check-tool-ledger.py`) would give one file two
predicates — that harms operability, so it is not proposed.

Weight deltas the integrator can bank: r51 wrapper 445 L (2154 ms, r52-measured) → 277 L /
65 ms; r52's harness/fixture-commit path (the round's only mutating code; 110 s and 300 s
timeouts measured on it in r52) → not needed at all, controls are read through `--ledger`;
C2 r51 counter 666 L → 260 L prototype, 35 ms.

## 4. Preserved contract

- C1 green fields at base are byte-identical to r52's accepted numbers: `population=82`,
  `ledger_rows=82`, `uncovered=dup=dangling=bad_pointer=0`; the ledger markdown, its row
  grammar, `quality/check-tool-ledger.py` and `PROVINCE.md` are untouched by the proposal.
- C2: all 15 unaffected propositions still verify under the new counter (only P16 fails at
  base); no table row is rewritten, `corpus/SOURCES.md` and `corpus/README.md:80` are
  untouched, and the source rows S370–S373 keep their pins.
- No axis harmed: no tracked write, no host/live read, no source mutation, no install.

## 5. Tradeoffs recorded, not hidden

1. The supersede exemption lets a row avoid its own quote check — bounded by requiring every
   repair record to carry a verifying quote and every withdraw to name a matching duplicate.
2. R7's template clause is fixture-shaped: it rejects the class that repeats a skeleton, not
   semantics (§1.4 measured both sides).
3. Two C1 gates remain (`check-tool-ledger.py` lane gate, new counter claim receipt). Merging
   them is the tempting simplification and the wrong one: it couples a capability row to a
   claim receipt. Keep two, name the owner of each field.
4. C2 withdraws one proposition (P17) instead of restating it: net −1 row, no loss of ground,
   because P04 already carries the same fact.

## 6. Environment, reproduction, limitations

- Base `git rev-parse HEAD` → `ad4bf2059bcfafe63671d262222908ee1fe8001c`;
  `git status --porcelain` → `?? .ufo/waves/round-53/` only (the wave's own untracked dir).
  `df -h /fast` → 592 G available, 27 % used.
- Prototypes and fixtures lived in `/fast/scratch/hyaku/mado-r53/R53Seven63` and are removed
  after measurement per seat bounds; identities: `c1-r53-proto.py 9b8eb834…` (277 L),
  `c2-r53-proto.py 4f9ad32d…` (260 L), `entry-corrected.md 3ca8438b…`. Reproduction is the
  clause tables in §1.2/§2.2 plus the matrix commands (`python3 -I <proto> --repo <lane>
  --rev ad4bf20 [--ledger <fixture>]`, `--selftest`); no campaign tool or host probe is used.
- No source URL was newly opened this round beyond the already-pinned r52 fetch; the upstream
  URLs and revision above come from `corpus/SOURCES.md:320-323` and were checked against the
  fetch bytes by `sha256sum -c` (`OK` ×5).
- Limitations: prototypes are prototypes — no committed counter and no revised entry exist,
  so neither claim is met by this report. Numbers are from this host on 2026-10-27 under
  concurrent sibling load; the two parser traps and the three C2 defects are the only
  measured deltas from the r52 record.

Report: `.ufo/waves/round-53/w1/R53Seven63.md`
