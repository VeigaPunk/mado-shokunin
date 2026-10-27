# R53Three26 — revenger: prior-round failure reconstruction and minimal corrected contract

- Seat: `R53Three26`, role `revenger` (leaf; no dispatch). Lane root
  `/home/vgpnk/Projects/shokunin/mado-shokunin`; base/HEAD
  `ad4bf2059bcfafe63671d262222908ee1fe8001c` (`git rev-parse HEAD`; working tree clean
  except `?? .ufo/waves/round-53/`).
- Axes named: **operability** (C1 accountable instrument-ledger counter) and **coverage**
  (C2 proposition-grounded entry repair). This report attacks neither claim as a vote; it
  reconstructs what failed, measures the divergences on pinned bytes, and states the
  smallest contract that closes the measured defects without claiming semantics.
- Frozen text attacked: `.ufo/waves/round-53/claims-frozen.md:7` (C1) and `:11` (C2);
  freeze-before-data at `:13`. Routed r52 evidence: `.ufo/waves/round-52/w2/Attack01.md`,
  `Attack02.md`, `Attack07.md`; closure spot-check
  `corpus/lessons/round-52-verifier-spotcheck.md` §§2, 3, 5.
- No live read, package query, input capture, screenshot, producer run, compositor/service
  mutation, network fetch or tracked write was performed. No tool install/upgrade.
- Scratch: `/fast/scratch/hyaku/mado-r53/R53Three26`; disk checked first
  (`df -h /fast`: 594G avail); no ENOSPC. No git object writes or commits: the two
  fixture-level reproductions below call the shipped predicate functions directly instead
  of committing fixture repos (the seat forbids commits), and that substitution is named
  wherever it applies.

## 1. Reconstructed contract (what the lane's own frozen text actually asks)

C1 (`claims-frozen.md:7`), parsed as named properties:

1. a **newly committed** counter (not the r51 counter, not an uncommitted rewrite);
2. **scratch-aware**: pinned bytes from `--rev`, writes only under `--work`;
3. **explicit selftest**;
4. `TARGET_MET` on the production ledger;
5. `TARGET_MISSED` on a no-work control **and each frozen forgery fixture**;
6. **exact population coverage**;
7. **non-self pointers**;
8. bounded structural check, **not semantic proof**; no capability without the final
   committed demonstration.

C2 (`claims-frozen.md:11`):

1. append-only correction that **clearly repairs P16, P17, P18** against opened pinned
   bytes;
2. a frozen counter that **rejects the old bytes** and **accepts the corrected entry**
   with quote/pin/proposition bindings;
3. an **independent** non-author checks source truth (no seat, including this one, counts);
4. **no expansion credit** unless an admitted entry rests on a source row opened this
   round and uncovered ground per the coverage map.

The round-52 spot-check supplies the exact routed defects: P16 spliced, P17 misattributed,
P18 mislocalized (`round-52-verifier-spotcheck.md:38-40`), plus Gate records absent
(`:71`), stale `## Changes` (`:72`), QUALITY 17 review owed (`:73`), and the repair
instruction (`:74`).

## 2. C1 evidence chain

### 2.1 The base counter is green and blind to both named holes

[OBS] Command (read-only clone into scratch):

```
python3 /home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r51-ledger.py \
  --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
  --rev ad4bf2059bcfafe63671d262222908ee1fe8001c \
  --work /fast/scratch/hyaku/mado-r53/R53Three26/c1base
```

Output (tail):

```
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=ad4bf2059bcfafe63671d262222908ee1fe8001c)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
```

Population split at base: `tools/` 17 + `quality/*.py` 19 + `quality/counters/*.py` 46 =
**82**.

The predicate's only evidence rule is
`pointer_resolves` (`quality/counters/c1-r51-ledger.py:196-207`): for each token in the
pointer cell, if the token is a tracked file whose bytes **contain the row's basename**, the
row is accountable. The only description rule is non-empty/non-placeholder
(`:229-232`, `PLACEHOLDER` at `:76`). There is no self-reference or uniqueness rule. The
shipped checker has the same shape: `quality/check-tool-ledger.py:262-265`
(`names_basename`) and `:268-328` (`evaluate`) — "the ledger itself is not an instrument"
(`:15`) is a population statement, not a pointer exclusion.

### 2.2 Both named holes reproduce on base bytes

[OBS] Logic-level reproduction (`repro_c1.py` in scratch) imports the shipped
`parse_rows`/`pointer_resolves`/`describe` and the checker's `evaluate`, and binds
`show()` to read-only `git show` on the lane (the counter's clone would otherwise need a
fixture commit). Variants keep production paths and pointer cells verbatim, changing one
field class at a time:

```
== production
   counter: bad_pointer=0 dangling=0 dup=0 empty_desc=0 ledger_rows=82 population=82 uncovered=0
   checker: bad_pointer=0 dangling=0 empty_desc=0 rows=82 uncovered=0
   counter-verdict: TARGET_MET (structural)
== F1 repeated-identical-generic-desc
   counter: bad_pointer=0 dangling=0 dup=0 empty_desc=0 ledger_rows=82 population=82 uncovered=0
   checker: bad_pointer=0 dangling=0 empty_desc=0 rows=82 uncovered=0
   counter-verdict: TARGET_MET (structural)
== F2 ledger-self-pointer
   counter: bad_pointer=0 dangling=0 dup=0 empty_desc=0 ledger_rows=82 population=82 uncovered=0
   checker: bad_pointer=0 dangling=0 empty_desc=0 rows=82 uncovered=0
   counter-verdict: TARGET_MET (structural)
== F3 self-pointer+own-path
   counter: bad_pointer=0 dangling=0 dup=0 empty_desc=0 ledger_rows=82 population=82 uncovered=0
   checker: bad_pointer=0 dangling=0 empty_desc=0 rows=82 uncovered=0
   counter-verdict: TARGET_MET (structural)
sample row: {'path': 'tools/mado-action-plan.py', ... 'pointer': '`quality/tool-ledger.md`'}
pointer_tokens: ['quality/tool-ledger.md']
resolves: True
```

F1 is the "repeated generic description" hole; F2/F3 are the "ledger self-pointer" hole
(the ledger names every instrument basename, so it satisfies its own rule). Both the
counter and the checker accept them. This confirms the claim's "Before" sentence on base
bytes rather than by citation.

### 2.3 The r52 draft closed neither class, and added interface traps

[OBS] from committed r52 reports (not re-executed by this seat):

- `Attack01.md:39-55` — the draft's four lexical description filters lose to 82/82 rows
  whose boilerplate carries a two-word phrase lifted from the instrument's own bytes
  (mostly the `env python3` shebang): `generic_desc=0 TARGET_MET`.
- `Attack02.md:68-80` — the draft's self-pointer test is exact string equality requiring a
  `/`; nine spellings pass: bare basename, own basename, `./`, trailing `)`, non-numeric
  suffix, `//`, leading `/`, case variant, and a mode-120000 symlink alias.
- `corpus/lessons/round-52-verifier-spotcheck.md:29-31` records no committed r52 counter
  and calls both classes reproduced.

[OBS] two interface defects in the draft, read at
`.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py`:

- `--ledger` reads an arbitrary working-tree file (`:821-825`) but then sets
  `ledger_rel = LEDGER_REL` (`:826`), so a fixture is judged against self-identity of the
  **production** ledger;
- the summary line (`:455-462`) prints counts, `verdict` and `rev` but **not** the ledger
  path or a mode, so a fixture pass is textually indistinguishable from a production pass.
- Its parser tolerates four-cell rows while the shipped checker calls them malformed
  (`check-tool-ledger.py:247-256`), so the r52 four-cell control cannot also be green under
  the checker; the r52 goal of failing it "specifically for self-pointer/context" is what
  forced the wider grammar.

## 3. C2 evidence chain

### 3.1 Pinned bytes and entry state

[OBS] `cd .ufo/waves/round-52/fetch && sha256sum -c SHA256SUMS` → five `OK` lines
(ConfigActions.cpp `a83abeb5…`, hpp `746c6f51…`, KeybindManager.cpp `8d8f35fc…`,
legacy-DispatcherTranslator.cpp `7248cbb8…`, README `c53296ae…`).

[OBS] Base entry `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`:
`git show ad4bf20:… | sha256sum` → `bee0d14379eb560595c5d2237ffc9fd0f6d61c3b6b728fbb0dab851687ecb078`,
6535 bytes, 32 lines; defects at `:28-30`.

| row | anchor | measured | defect class |
|---|---|---|---|
| P16 | `ConfigActions.cpp:1554-1558,1576` | joined quote raw count 0 and whitespace-collapsed count 0; `:1555-1557` elide `if (S.m_passPressed == 1) { if (!isMouse)` | **spliced**; second clause ("then clears") sits at `:1576`, outside the quote |
| P17 | `DispatcherTranslator.cpp:619-622` | quote at `:621-622`, collapsed count 1; enclosing function derived at `:619` is `sendkeystate` (`:591`), not `sendshortcut` (`:531`) | **misattributed subject** |
| P18 | `DispatcherTranslator.cpp:574` | quote raw count 1; the `for` at `:565` closes at `:571`; the return is inside the cache-miss `if` at `:559` | **mislocalized** ("inside the scan") |

This matches `Attack07.md:55-57,74-77` and the closure spot-check `:38-40` independently.

### 3.2 The three defects are mechanically separable

[OBS] `c2_proto.py` derives, from the pinned file bytes, the enclosing function and
innermost control statement with a brace stack, then applies: single-range anchor,
collapsed-contiguous quote, ≤25 words, `actor` match, `locus` match. Old rows encoded in
the proposed schema:

```
old-P16 (spliced)                 FAIL words=9  func=Actions::pass     ctrl=-     quote_not_contiguous
old-P17 (subject)                 FAIL words=9  func=sendkeystate      ctrl=-     actor:sendshortcut!=sendkeystate
old-P18 (localization)            FAIL words=12 func=sendshortcut      ctrl=if    locus:for!=if
new-P16a (mods before branch)     PASS words=16 func=Actions::pass     ctrl=-     ok
new-P16b (mods cleared after)     PASS words=4  func=Actions::pass     ctrl=-     ok
new-P17 (action twin repeat)      PASS words=11 func=Actions::sendKeyState ctrl=-  ok
new-P18 (cache-miss, after scan)  PASS words=12 func=sendshortcut      ctrl=if    ok
```

Each old row fails a **different** clause, so a counter need not parse English to
discriminate the three routed defects.

### 3.3 Append-only correction passes, old bytes fail

[OBS] `c2_contract.py` builds the corrected entry as `base bytes + corrections table` and
checks: prefix sha256 equals the frozen base digest, every superseded id is accounted,
replacement rows bind quote/actor/locus, and `after=<id>` orders anchors in one file:

```
base-entry                       TARGET_MISSED no_corrections_section
corrected-proposal               TARGET_MET
corrected-with-old-P16-quote     TARGET_MISSED C01:quote_not_contiguous
corrected-with-old-P17-subject   TARGET_MISSED C05:actor:sendshortcut!=sendkeystate
corrected-with-old-P18-locus     TARGET_MISSED C04:locus:for!=if
```

This is a prototype of the contract, not a frozen counter; it exists to show the clauses
are decidable and discriminating on the actual pinned bytes.

## 4. Divergences (measured), with confidence

| # | Divergence | Evidence | Confidence |
|---|---|---|---|
| D1 | r51 counter's pointer rule accepts the ledger itself and any file naming the basename; no self/uniqueness rule | §2.1-2.2; `c1-r51-ledger.py:196-207` | high |
| D2 | shipped checker shares D1 (self-pointer not excluded) | `check-tool-ledger.py:262-328` | high |
| D3 | r52 draft's self-pointer rule is exact-equality with `/`, defeated by nine spellings and symlink mode | `Attack02.md:68-80` | high (committed reproduction) |
| D4 | r52 draft's description "context" clause is lexically unfalsifiable; 82/82 forged pass | `Attack01.md:39-55` | high |
| D5 | `--ledger` fixture runs are mislabeled as production self-identity, and the summary omits ledger path/mode | draft `:455-462,821-826` | high (code read) |
| D6 | r52 draft's wider row grammar conflicts with the shipped checker's 3-cell rule | draft `:303-330`; checker `:247-256` | high |
| D7 | Entry P16/P17/P18 fail contiguity/subject/locus; each separable | §3.1-3.2 | high |
| D8 | Base entry is 6535 bytes/32 lines; an append-only clause can bind it by sha256 | §3.1 | high |
| D9 | Pin manifest uses absolute `/home/...` paths, so a counter in a clone must not rely on it verbatim | `fetch/SHA256SUMS` | high |
| D10 | S370/S371/S373 share canonical URLs with S365/S367/S364; QUALITY 17 review still owed; lesson Gate records absent; `## Changes` stale | spot-check `:71-73`; `SOURCES.md:320-323`; `README.md:374` | high (recorded, not re-derived) |

## 5. Minimal corrected contract

### 5.1 C1 — clauses that are decidable (and the limit that must be stated)

**P — population.** `git ls-tree -r --name-only <rev>`; blobs under `tools/` (excluding
`__pycache__`, `.pyc`, `.pyo`) plus `quality/*.py` and `quality/counters/*.py`. The ledger
never defines the population. At base P=82; after this round's counter is committed P=83,
so the production ledger must gain exactly that row.

**C — coverage.** Every population path once; `uncovered=dangling=dup=0`;
`ledger_rows=P`; production grammar is exactly three cells (the shipped checker rejects
anything else). Controls must use the same grammar so a control cannot fail for a
malformed-row reason.

**S — pointer (non-self, in the pointer cell only).** Canonicalize each backticked token:
strip emphasis, `#fragment`, `:<suffix>`, trailing punctuation, leading `./`; collapse
`//`; strip a leading `/`. Then require all of:
1. resolves at `--rev` to a blob with mode `100644`/`100755` — reject `120000` (symlink)
   and gitlinks;
2. is not `quality/tool-ledger.md` (or the fixture path in fixture mode);
3. is not the row's own instrument path;
4. is not any other population path (a peer instrument is not accountable for a sibling);
5. its bytes name the row's basename as a name (`check-tool-ledger.py:262-265` rule);
6. belongs to an accountable document class: `PROVINCE.md`, `SCORECARD.md`,
   `corpus/lessons/*.md`, `corpus/QUALITY.md`, `corpus/knowledge/*.md`,
   `.ufo/waves/round-*/registration.md`.

A self token **anywhere in the pointer cell** is fatal even when a second accountable token
is present (no laundering). A self token in a non-pointer cell is recorded, not scored,
when an accountable target exists.

Production compatibility check: all 82 pointer tokens in the base ledger fall in exactly
these classes (SCORECARD 42, PROVINCE 20, `corpus/lessons/*` 9, `corpus/QUALITY.md` 3,
`.ufo/waves/round-*/registration.md` 8), so clause 6 does not rewrite production.

**D — description.** Non-empty/non-placeholder; normalized (casefold, punctuation,
whitespace) **unique across rows**; not a name restatement (after removing path/basename
words and closed-class function words, at least two content words remain). No claim that a
description is true, functional or derived from the instrument. This closes the r51
"repeated generic" class only for repeated/name-only text; it does **not** close
`Attack01`'s F-all (82 unique template sentences with a lifted word pair) and no lexical
clause can. The limit must be printed by the counter, not merely listed in a report.

**F — fixture mode.** A distinct flag (`--fixture <repo-relative path>` or equivalent)
scores that file's bytes against the population at `--rev`; the row self-identity is the
fixture path, not the production ledger; the summary prints `mode=fixture ledger=<path>`.
Production prints `mode=production ledger=quality/tool-ledger.md`. This closes D5 and makes
a fixture pass unable to masquerade as the production run.

**V — verdict.** `TARGET_MET` only when every count is zero **and** the production path is
the one scored at `--rev`. Each fixture must return `TARGET_MISSED` **with its named
defect field non-zero** (not merely dangling/malformed). Print per-class counts; exit 0/1/2
as today.

**T — selftest.** Builds its fixtures under `--work` and asserts, at minimum: green
production copy; identical repeated descriptions; self-pointer spellings (full path, `./`,
`//`, leading `/`, trailing `)`, `:x` suffix, basename only, case variant); symlink alias;
peer instrument; two-token laundering; name restatement; placeholder; duplicate row;
missing row; and one production-mode run. Assert exit codes and the exact defect fields.

**Freeze order.** Commit the fixture files and the expected defect field per fixture in the
freeze; run at the freeze rev and again at the data tip. Do not hard-code 82/83 in the
counter; derive P.

**Fixture-set warning.** If the round freezes `Attack01`'s F-all (unique generic sentences)
as a required `TARGET_MISSED`, C1 fails again by construction. Freeze fixtures the named
target properties can decide (population, self/alias pointers, duplicate/name-only
descriptions), and record F-all as an out-of-scope residual in the claim's limit sentence.

### 5.2 C2 — clauses, and the corrected rows

**A — append-only.** Entry bytes at `--rev` must start with the frozen r52 bytes
(6535 bytes, sha256 `bee0d14379eb560595c5d2237ffc9fd0f6d61c3b6b728fbb0dab851687ecb078`);
corrections follow a fixed marker. The counter hashes the prefix from `git show`, never the
working tree.

**B — supersession.** Every superseded id (`P16`, `P17`, `P18`) is accounted for; each has
exactly one correction row; a replacement binds fully, a withdrawal carries a reason; no id
superseded twice; authoritative set = original rows − superseded + replacements, computed
from the entry (no hard-coded count).

**R — row binding.** For each replacement: one contiguous anchor `file:start[-end]` (no
comma ranges); quote whitespace-collapsed and contiguous inside that anchor; ≤25 words;
`actor` equals the enclosing function derived from the pin; `locus` equals the innermost
control kind (`if`/`for`/`while`/`switch`/`else`) or `function`; optional `after=<id>`
requires the same pin file and a strictly later anchor; pin digest equals the frozen
digest for that file (path-relative, never the absolute paths in `SHA256SUMS`).

**I — independent review.** The counter's pass is structural only. An independent
non-author samples the corrected propositions against the pin; no seat in this wave,
including this one, counts as that reviewer.

**E — expansion.** Zero. S370-S373 are already indexed (`corpus/README.md:80`) and
registered (`corpus/SOURCES.md:320-323`, opened 2026-10-27); the repair opens no source row
and covers no new ground. Any expansion credit requires a row opened this round mapped to
uncovered ground, which this repair does not provide.

Corrected rows (all pins under `.ufo/waves/round-52/fetch`, S371/S370 already registered):

| id | action | supersedes | proposition | pin:anchor | quote (words) | actor | locus | after |
|---|---|---|---|---|---|---|---|---|
| C01 | replace | P16 | `Actions::pass` sends the modifier mask before its `m_passPressed == 1` key branch. | `ConfigActions.cpp:1554-1558` | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` (16) | `Actions::pass` | function | — |
| C02 | replace | P16 | After the key/pointer branch, `Actions::pass` sends a zeroed modifier mask. | `ConfigActions.cpp:1576` | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` (4) | `Actions::pass` | function | C01 |
| C03 | withdraw | P17 | Withdrawn: duplicates P04 and assigns `sendkeystate`'s repeat to `sendshortcut`; no replacement fact claimed. | `DispatcherTranslator.cpp:619-622` (historical) | — | — | — | — |
| C04 | replace | P18 | On a cache miss, after the scan finds no matching keycode, `sendshortcut` returns the `key not found` error. | `DispatcherTranslator.cpp:573-574` | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` (12) | `sendshortcut` | if | — |

Notes:
- C01/C02 split the original P16 into a contiguous quote plus an order binding; the
  "then clears" clause is no longer carried by a splice.
- C03 removes a duplicate, not a unique fact (`P04` already pins `:619-622`; `Attack07.md:82`
  records the double-count). Withdrawing it keeps the authoritative count at 18
  (18 − P17 + one extra P16 row).
- If the round wants the action-level twin instead, the only defensible row is
  `Actions::sendKeyState` at `ConfigActions.cpp:1612-1613` with quote
  `if (keyState == 2 && result.has_value()) result = Actions::pass(modMask, key, w);`
  (11 words, actor `Actions::sendKeyState`, locus function). It is optional; it reverses
  the r52 draft's deliberate demotion (`w1/C2SourceRecon.md:31,49`) and is not needed to
  repair the three routed defects.
- The corrections section must open with a "superseded, do not cite" sentence, because the
  original table stays in the file by append-only discipline. The index row
  (`corpus/README.md:80`) should then point at the correction anchor; that is a tracked
  edit for the integration seat, not this one.

## 6. Axis and harm accounting

- **operability (C1):** the corrected clauses close the measured self-pointer and
  identical-generic classes; they do not overclaim semantics. Cost: P goes 82→83 and the
  new counter's own row must be written, or the run is `uncovered=1`. No coverage surface
  changes.
- **coverage (C2):** the repair removes three false/defective propositions and adds no
  ground. Expansion credit is zero by rule; the quality harm recorded by the r52 spot-check
  is what the repair addresses, not the coverage count.
- No axis is harmed by either contract: C1 touches only instrument accounting; C2 edits one
  entry's propositions against already-pinned bytes.
- Routed r52 defects remain dependencies, not this seat's writes: Gate records for
  S370-S373, the stale `## Changes`, and the QUALITY 17 distinct-scope review
  (`round-52-verifier-spotcheck.md:71-73`). A C2 "admitted" sentence that cites S370/S371
  should not land before that review is recorded.

## 7. Residuals and confidence

- **C1 holes measured:** high confidence (base counter run plus logic-level reproduction on
  base bytes; committed r52 attacks agree).
- **C1 corrected contract:** medium-high. Pointer clauses are mechanical and
  production-compatible; the symlink/mode and canonical-spelling rules are prototyped.
  Confidence is bounded by two facts: the fixture set is not yet frozen, and the
  description clause is deliberately not semantic. `Attack01`'s F-all remains open and
  must be declared, not hidden.
- **C2 defects measured:** high confidence (independent derivation of function/locus plus
  closure and Attack07 agreement).
- **C2 corrected contract:** medium-high. The three old rows fail three different clauses
  and the corrected rows pass on the pinned bytes; the remaining risk is wording-level
  entailment, which only the required independent non-author review can settle. My
  prototypes are author-side and count for nothing under the frozen claim.

## 8. Verification inventory (all read-only on the lane; scratch only)

| # | Command (cwd) | Result |
|---|---|---|
| 1 | `git -C <lane> rev-parse HEAD; git -C <lane> status --porcelain` | `ad4bf205…`; only `?? .ufo/waves/round-53/` |
| 2 | `python3 <lane>/quality/counters/c1-r51-ledger.py --repo <lane> --rev ad4bf20… --work <scratch>/c1base` | §2.1 `TARGET_MET`, 82/82, exit 0 |
| 3 | `python3 -I repro_c1.py` (scratch) | §2.2: production/F1/F2/F3 all `TARGET_MET (structural)` |
| 4 | `python3 -I c1_proto.py` (scratch) | production 82 rows, 0 failures; 10 self-pointer spellings FAIL; repeated description FAIL; name restatement FAIL |
| 5 | `cd <lane>/.ufo/waves/round-52/fetch && sha256sum -c SHA256SUMS` | 5 × `OK` |
| 6 | `git -C <lane> show ad4bf20:corpus/knowledge/hyprland-synthetic-dispatch-r52.md \| sha256sum` | `bee0d143…ecb078`, 6535 B / 32 L |
| 7 | `python3 -I c2_proto.py` (scratch) | §3.2 table: 3 old FAIL on distinct clauses, 4 corrected PASS |
| 8 | `python3 -I c2_contract.py` (scratch) | §3.3: base MISS, corrected MET, three old-encoding MISS |
| 9 | population split script (`git ls-tree` + regex) | 17 tools + 19 quality/*.py + 46 counters = 82 |

No test, build, lint or counter in the lane was modified; no commit, jj operation,
subagent, background job, live probe, or network fetch occurred.

## Trailer

- **Attacked predicate:** C1 frozen operability predicate
  (`claims-frozen.md:7`: newly committed scratch-aware counter, production `TARGET_MET`,
  no-work + frozen-forgery `TARGET_MISSED`, exact population, non-self pointers) and C2
  frozen coverage predicate (`:11`: append-only P16-P18 repair, old-rejecting/new-accepting
  counter with quote/pin/proposition bindings, independent source-truth review, no
  expansion credit). This seat re-measured the before-state and specified the minimal
  contract; it claims no pass, no admission and no non-author review.
- **Exact command/output:** §2.1 counter run line; §2.2 F1/F2/F3 verdict lines; §3.1
  `sha256sum -c` five OKs; §3.2/§3.3 prototype tables. All commands are quoted with their
  working directory and the exact stdout lines that carry the finding.
- **Newly opened source:** none — no external URL was fetched and no source was newly
  opened by this seat. The cited bytes are lane-local pinned mirrors already registered at
  `corpus/SOURCES.md:320-323` (URLs at Hyprland commit
  `efb50993780079460b0cbed1363e2166a2de1d9f`, opened 2026-10-27). Located quote used for
  the P16 finding: `Hyprland-ConfigActions.cpp:1556-1558`
  `if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(...)`; for P17:
  `Hyprland-legacy-DispatcherTranslator.cpp:591` `static SDispatchResult sendkeystate(...)`;
  for P18: `:571-574` loop close then `if (!keycode)`.
- **Report path (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`):**
  `.ufo/waves/round-53/w1/R53Three26.md`
