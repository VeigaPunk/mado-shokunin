# R53Three27 — simplifier: C1 accountability counter and C2 proposition repair

Seat `R53Three27`, role **simplifier** (leaf; no subagent dispatch, no commits, no background
jobs). Lane `/home/vgpnk/Projects/shokunin/mado-shokunin` at base tip
`ad4bf2059bcfafe63671d262222908ee1fe8001c` (asserted: `git rev-parse HEAD`). Wave
`.ufo/waves/round-53/w1`, frozen claims `.ufo/waves/round-53/claims-frozen.md`. Axes:
**coverage** (C2) and **operability** (C1); no score claimed, no axis widened.

Scope of this report: **suggest the simplest maintainable implementation and its test cases**,
and name deletion candidates with evidence. No tracked lane file was edited; the tracked tree is
byte-identical before and after (`git status --porcelain` → only the pre-existing untracked
`?? .ufo/waves/round-53/`, whose only new file is this report). No package query, no install, no live read, no host probe, no fetch.
Reads were the lane's own tracked bytes and the round-52 pinned fetch bytes, whose sha256 I
verified against `.ufo/waves/round-52/fetch/SHA256SUMS` (see §8). Every write stayed under
`/fast/scratch/hyaku/mado-r53/R53Three27` (removed before yield; disk guard `df -h /fast` →
590G available, 27% used).

---

## 0. Verdict

**C1 — the existing counter is redundant weight and the measured before-state reproduces.**
`quality/counters/c1-r51-ledger.py` (445 lines, **2011 ms** at the tip) accepts a
population-shaped *no-work* ledger and both isolating single-defect controls at the tip
(measured, §2). A **217-line, 58–65 ms** counter that reads only `git ls-tree` + `git show`
(the r52 `C1Simplify` reference shape, minus the defeatable two-word lexical clause) is
`TARGET_MET` on production and `TARGET_MISSED` on every isolating control (§3). Recommended
implementation is that shape, with a **built-in `--selftest` over eight in-memory fixtures**;
no clone, no child process, no scratch lifecycle.

**C2 — the three routed defects are repairable with five contiguous-quote rows.**
At the tip, 17/18 quotes bind whitespace-collapsed inside their cited span; **P16 does not**
(`not_in_span`, measured by two independent readings including the round-52 draft counter's own
clause d), while P17 and P18 bind mechanically and are false only in attribution/localization.
The **minimum** repair is an appended corrections table whose heading carries the superseded ID
list; five new rows (`P19`–`P23`) each quote one contiguous span (≤25 words) and repair one
defect (§5). A counter needs only: entry present + indexed, supersession resolved, quote
contiguous inside its cited span, pin file present at `--rev`, S-row present. That is ~200
lines, not the 965-line round-52 draft (§6).

**Deletions found, not made:** `quality/check-tool-ledger.py` is a *second implementation* of
the same ledger predicate and the only reason the r51 counter carries clone/sandbox/child-run
machinery (~250 lines); the r53 C1 predicate does not name it. It is a candidate for retirement
**after** the r53 counter lands, and the r51 counter and its checker must then be marked
historical rather than silently left as a competing authority (§7).

---

## 1. Attacked predication

C1 (`.ufo/waves/round-53/claims-frozen.md:5`), verbatim:

> Target: a newly committed, scratch-aware counter with explicit selftest returns TARGET_MET on
> the production ledger, TARGET_MISSED on a no-work control and each frozen forgery fixture,
> with exact population coverage and non-self pointers. This is a bounded structural
> accountability check, not semantic proof.

C2 (`.ufo/waves/round-53/claims-frozen.md:9`), verbatim:

> Before: r52 verifier found P16 quote spliced, P17 misattributed, P18 mislocalized; no valid
> r52 admission counter. Target: append-only correction clearly repairs those three
> propositions against opened pinned source bytes; a frozen counter rejects the old bytes and
> accepts corrected entry with quote/pin/proposition bindings; independent reviewer checks
> source truth.

Both are attacked as *construction* predicates. The C1 sentence is read as: population exact,
one row per population path, **non-self** resolvable pointers, and rejection of the r52-routed
defects (repeated generic descriptions, ledger self-pointers) — not as the withdrawn
"instrument-specific context" wording, which round-52 measured as defeatable
(`.ufo/waves/round-52/w1/C1Simplify.md` §6: a forged ledger with 82 unique boilerplate
descriptions passes every lexical context check).

---

## 2. C1 before-state, measured at the tip

Controls were generated in scratch from the tip population (82 paths) by rewriting the
production ledger's own rows, so population/row-count cannot be the cause of any verdict.
Generation rule: 3 cells per row, descriptions and pointers copied from production except the
one column each fixture mutates.

Scoring the four fixtures with the **r51 counter's own `parse_rows` + `describe`** (imported
read-only; `clone=LANE`, `rev=ad4bf205…`, `files=ls-tree`):

| fixture (82 rows, 3 cells) | r51 counters | r51 verdict |
|---|---|---|
| `control-P-padded` — population-shaped, one repeated generic description, every pointer `` `quality/tool-ledger.md` `` | `uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 dup=0 ledger_rows=82` | **TARGET_MET** |
| `control-C-ledger-self` — production descriptions, every pointer = the ledger | same, all zero | **TARGET_MET** |
| `control-D-generic-desc` — production pointers, one repeated generic description | same, all zero | **TARGET_MET** |
| `control-B-self-and-generic` — every pointer = the row's own path | `bad_pointer=53` | TARGET_MISSED |

`control-B` misses only incidentally: an instrument's own file contains its own basename for
**29/82** population files, so **29 self-pointers pass** the r51 pointer clause today
(`82 − 53 = 29`). The clause that fails is therefore neither "non-self" nor "specific"; it is
"the pointed-at file mentions the basename", satisfied by the ledger's own row list.

Ancestor cost at the tip, read-only with a scratch `--work`:

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev ad4bf2059bcfafe63671d262222908ee1fe8001c --work <scratch>
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=ad4bf2059bcfafe63671d262222908ee1fe8001c)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
rc=0 elapsed_ms=2011
```

Production is conformant to a *strict* pointer grammar today: **82/82 pointer cells are exactly
one backticked repo path** (with `:<line>` suffix), 12 distinct pointer targets, **0 duplicate
descriptions**, minimum description length 9 words (measured over the tip ledger). Every rule
below therefore costs nothing on production bytes.

---

## 3. C1 — recommended counter (simplest maintainable)

**Shape:** one pure scoring function + one git reader. No clone, no child process, no
`--checker` delegation, no scratch tree. Inputs: `--repo`, `--rev`, optional `--ledger PATH`
(the frozen control), optional `--work` accepted and unused. Writes: **none** (documented on the
`--work` help string so a harness passing it is not a surprise).

**Measured size and cost of the reference I ran:** 217 lines including docstring, exit map and
`--selftest`; **58–65 ms** on production (three runs), **44 ms** on a control. The r52 reference
(194 lines, 171 ms) is the same shape *plus* a two-word lexical clause that reads all 82
instrument blobs and is defeatable by construction; dropping it returns ~110 ms and 82 blob
reads.

### Rules (each a measurement, none semantic)

| # | Rule | Counter |
|---|---|---|
| 1 | population = files at `--rev` under `tools/` (any extension) + `quality/*.py` + `quality/counters/*.py`, excluding `__pycache__`, `*.pyc`, `*.pyo`; from a single `git ls-tree -r --name-only` | `population=P` |
| 2 | every population path appears exactly once in a **3-cell** pipe row outside fenced blocks; a 4-cell row is `dangling` (so the r52 4-cell control cannot be scored as a row) | `ledger_rows`, `dup`, `dangling`, `uncovered` |
| 3 | pointer cell is **exactly one backticked repo path**; `:<line>` / `:<n>-<m>` stripped; prose fallback removed (it is what accepted the generic self-pointer) | `bad_pointer` |
| 4 | pointer target exists at `--rev` and its bytes contain the row file's basename | `bad_pointer` |
| 5 | pointer target is **not** the row's own path and **not** the canonical ledger (`quality/tool-ledger.md`), excluded unconditionally — also when `--ledger` names an external control (the round-52 false-green trap, `C1Simplify.md` §5.1) | `self_pointer` |
| 6 | description, after stripping emphasis: non-empty, not placeholder-only, **not verbatim-identical to an earlier row's description**, and ≥3 whitespace words (production floor 9; the floor only stops a single-row "A tool." retrofit, which repetition cannot see) | `generic_desc` |
| 7 | `TARGET_MET` iff `population > 0`, `ledger_rows == population`, and every counter is 0 | `verdict` |

Line: `C1_R53: population=<P> ledger_rows=<R> uncovered=<n> dup=<n> dangling=<n> bad_pointer=<n> self_pointer=<n> generic_desc=<n> verdict=<MET|MISSED> rev=<sha>`; exit 0 / 1 / 2 (setup).

### Measured discrimination (the eight selftest cases)

`--selftest` regenerates each fixture **in memory from the population at `--rev`** — no
committed fixture bytes, no writes — and asserts the exact counter set, so a parroting counter
cannot pass. Measured at `ad4bf205…`:

| case | mutation of the production rows | expected | verdict measured |
|---|---|---|---|
| production-shape | none | all 0 | MET |
| B-self-and-repeat | every pointer → own path; every description → one generic sentence | `self_pointer=82 generic_desc=81` | MISSED |
| C-ledger-self | every pointer → `` `quality/tool-ledger.md` `` | `self_pointer=82` | MISSED |
| D-repeat-desc | one repeated description, pointers untouched | `generic_desc=81` | MISSED |
| E-one-self | one row's pointer → own path | `self_pointer=1` | MISSED |
| F-bad-pointer | one row's pointer → `corpus/nonexistent.md` | `bad_pointer=1` | MISSED |
| G-dropped-row | last row removed | `uncovered=1` | MISSED |
| H-empty | empty ledger | `uncovered=82` | MISSED |

`SELFTEST: 8/8 passed` (measured). Note `generic_desc=81`, not 82: the first occurrence of a
repeated string is by definition not a repeat — which is exactly why rule 6 also carries the
3-word floor. A padded ledger of 82 *distinct* boilerplate descriptions still passes; that is
the claim's own stated bound ("bounded structural accountability check, not semantic proof") and
the receipt must print that sentence.

### Frozen control set to commit before data

Four files under `.ufo/waves/round-53/controls/`, derived deterministically by mutating the
**demonstration rev's** production rows (rule table above): `c1-no-work-padded.md` (the
population-shaped no-work control), `c1-ledger-self.md`, `c1-repeat-desc.md`,
`c1-one-self.md`. The scored demonstration is then one command per file:

```
python3 -I quality/counters/c1-r53-ledger.py --repo <lane> --rev <demo> --ledger .ufo/waves/round-53/controls/<f>
```

### Population coupling the integrator must not miss

Committing `quality/counters/c1-r53-ledger.py` changes `P` from 82 to 83, and committing
`quality/counters/c2-r53-proposition-entry.py` changes it to **84**. Consequences:

1. The C1 demonstration rev must contain **both** new counters **and** their two ledger rows;
   otherwise the counter misses on its own population.
2. Every frozen control file must be generated at that rev (84 rows), not today's 82.
3. Each new ledger row's pointer must name an existing file containing its basename and must not
   be the ledger — `PROVINCE.md` or `.ufo/waves/round-53/registration.md` are the honest targets.

---

## 4. C2 before-state, measured against the pinned bytes

Pins (identical to the frozen digests, `sha256sum -c`-equivalent):

```
a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771  .ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp
```

Entry `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (32 lines) at the tip, proposition
rows scored by one rule — *quote is a whitespace-collapsed contiguous substring of the cited
span* — read from `corpus/knowledge` + `fetch/`:

| row | anchor | words | binding |
|---|---|---|---|
| P01–P15 | as committed | 5–19 | all bind (5 raw-verbatim: P02, P05, P11, P13, P15; 10 collapsed) |
| **P16** | `ConfigActions.cpp:1554-1558,1576` | 9 | **`not_in_span(1554-1558)`** |
| P17 | `legacy-DispatcherTranslator.cpp:619-622` | 9 | binds (mechanically) |
| P18 | `legacy-DispatcherTranslator.cpp:574` | 10 | binds raw |

Independent confirmation with the round-52 draft counter at the tip
(`.ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py`, `--entry` the landed slug,
`--fetch-root .ufo/waves/round-52/fetch`):

```
C2_R52: d ok=0 quotes_bound=17/18 quotes_raw=6/17 pins=4 policy=whitespace-collapsed
        miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)
```

So the counter's mechanical reach covers **one** of the three routed defects; the other two are
truth defects the claim already assigns to the independent reviewer. Cheap defense in depth for
P17 only (§5.3).

The source facts behind the three defects, read from the pinned bytes (not re-fetched):

- `ConfigActions.cpp:1554` `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` then `:1555-1557`
  `if (S.m_passPressed == 1) { if (!isMouse)` then `:1558` the PRESSED key send, then `:1561`,
  `:1566` alternative branches, then `:1576` `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);`.
  The two quoted statements are not adjacent; the elided guard conditions the shown send.
- `legacy-DispatcherTranslator.cpp`: `sendshortcut` starts `:531` and ends `:589`;
  `sendkeystate` starts `:591`, and `:619` / `:621-622` are inside it. The repeat branch is
  `sendkeystate`'s; `sendshortcut` has none.
- `:565-571` is the `for` scan loop; `:573-574` `if (!keycode) return {… "key not found"};` is
  **after** the loop, inside the cache-miss block; `:579-580` is the separate `invalid key`
  guard.

---

## 5. C2 — the repair, as bytes

Append to `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (nothing above line 32 changes;
the old wording stays visible, which is what "append-only" protects):

```markdown
## Proposition corrections (round 53; append-only; supersedes P16, P17, P18)

The r52 non-author spot-check (`corpus/lessons/round-52-verifier-spotcheck.md:38,:74`) found
P16's quote spliced across :1554 and :1558 (eliding `if (S.m_passPressed == 1) { if (!isMouse)`),
P17's repeat branch attributed to `sendshortcut` although the pin sits inside `sendkeystate`,
and P18's `key not found` return described as inside the scan although it follows the loop. The
rows below replace them one clause per contiguous span; P17's old wording is withdrawn in
favour of P23. Pins and checksums are unchanged.

| ID | Proposition | Source row | Pin:anchor | Quote (<=25 words) | Support class | Why it supports |
|---|---|---|---|---|---|---|
| P19 | The action sends the current modifier mask to the seat before it delivers a key event. | S371 | Hyprland-ConfigActions.cpp:1554 | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` | direct | This is the first seat delivery in the body; the key/button sends begin at :1556-:1569. |
| P20 | After the key/button branch the action sends a zeroed modifier mask. | S371 | Hyprland-ConfigActions.cpp:1576 | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` | direct | Anchor order :1554 < :1558/:1563/:1568 < :1576; the second call clears all four fields. |
| P21 | The pressed key event is sent only when `m_passPressed == 1` and the key is not a mouse button. | S371 | Hyprland-ConfigActions.cpp:1556-1558 | `if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` | direct | The two guards enclose the pressed send; :1561 and :1566 select the other branches. |
| P22 | After the keycode scan fails to assign a keycode, `sendshortcut` returns `key not found`, distinct from the later `invalid key` guard. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:573-574 | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` | direct | The guard follows the for-loop (:565-:571) inside the cache-miss block; :579-:580 returns `invalid key`. |
| P23 | `sendkeystate`'s repeat branch replaces the first `sendshortcut` result with the second call's result when the first succeeded. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:619-622 | `auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` | direct | The branch is inside `sendkeystate` (:591-:627); the assignment overwrites the first result. P04 records the call count, this row the replacement. |
```

Measured binding of each new row (same rule as §4): `P19` raw, 4 words · `P20` raw, 4 ·
`P21` collapsed, 12 · `P22` collapsed, 12 · `P23` collapsed, 13. All `in_span`, all ≤25.

Why this shape rather than the three alternatives:

1. **Not in-place rewriting of rows 28–30.** The lane's own corrections record is prose that
   *supersedes* earlier wording while the table stays untouched
   (`corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:318-322`). Rewriting the rows would
   create a second convention for the same act.
2. **Not a full re-statement of all 20 rows.** The heading carries the superseded IDs, so only
   the repaired rows are appended; 16 unaffected rows are not duplicated and cannot drift.
3. **Not a new `Supersedes` column.** One heading regex (`supersedes P16, P17, P18`) is the whole
   machinery; new rows get fresh monotone IDs, so the ID grammar stays `P\d+` and the
   uniqueness check stays strict.
4. **P17 is replaced, not edited**: the corrected claim lives in `P23`, whose proposition names
   `sendkeystate` (the actual owner). If the non-author reviewer judges `P23` too close to `P04`
   (the r52 near-duplicate finding, `Attack08.md:20`), the honest alternative is to withdraw it
   as well and keep only the heading's supersession — the counter accepts both, because a
   superseded ID is not evaluated.

Entry-level marking of the defect where a reader consumes it is the index row
`corpus/README.md:80`; the integrator should point it at the corrections section. The counter
does not check prose markers.

### 5.3 Optional, cheap: the possessive-subject rule

A row that writes `` `X`'s `` asserts X is the owner. Rule: the backticked token before `'s` in
the Proposition cell must equal the **column-0 function definition** enclosing the anchor line.
Measured: landed P17 → enclosing `sendkeystate`, subject `sendshortcut` → **mismatch (reject)**;
`P23` → subject `sendkeystate` → pass; all other landed rows have no possessive, so unaffected
(and P13/P16's enclosing detection via a column-0-only scan is `pass`, not the naive
nearest-match which returns `moveWindowOutOfGroupHelper` for a line inside `Actions::pass`).
This is ~10 lines and mechanically rejects the second of the three defects; it stays lexical and
must be reported as such.

---

## 6. C2 — recommended counter (simplest maintainable)

**Do not commit the 965-line round-52 draft.** Its clause set contains four things the r53
predicate does not name and the landed entry cannot satisfy:

| draft component | status under the landed entry shape | move |
|---|---|---|
| mandatory `\| pin \| … \|` manifest table (clause c) | the landed entry has **no** manifest, only a prose sentence naming `fetch/`; clause c measured `rows_bound=0/18` with `anchor_no_fetch_root` tokens | drop; use one frozen constant `FETCH_ROOT = ".ufo/waves/round-52/fetch"` |
| novelty shingle clause vs base corpus + candidate dirs | not in the r53 predicate; reads the whole corpus | drop |
| `held:` citation clause | not in the r53 predicate; the entry carries none | drop |
| column auto-assignment / block-form / registry-state probes | not needed for one known 7-column table | drop |
| clause d (pin + span + quote binding) | **the load-bearing part**; measured correct on the landed rows | keep, verbatim in behaviour |

Minimal clause set and line (~200 lines, stdlib only, no writes, `--work` accepted-unused):

| clause | check | failure token |
|---|---|---|
| a | entry exists at `--rev` **and** has a `corpus/README.md` index row naming it | `entry_absent`, `not_indexed` |
| b | proposition tables parsed; each ID unique in the **effective** map; `props >= 4` | `dup_id`, `too_few` |
| c | a heading matching `supersedes\s+(P\d+(\s*[,–-]\s*P\d+)*)` removes those IDs from the effective map (this is the whole append-only join) | — |
| d | per effective row: pin basename resolves under `FETCH_ROOT` at `--rev`; anchor in range; quote non-empty, ≤25 whitespace words, whitespace-collapsed **contiguous inside the cited span** | `pin_absent`, `anchor_oob`, `quote_too_long`, `quote_not_at_pin` |
| e | the row's `S###` exists in `corpus/SOURCES.md` at `--rev` with status `mined` | `row_absent`, `row_unmined` |
| f | (optional) possessive-subject rule §5.3 | `subject_mismatch` |

Line: `C2_R53: entry=<rel> indexed=1 props=<n> effective=<n> superseded=<n> quotes_bound=<n>/<n> words_max=<n> pins=<n> verdict=<MET|MISSED> rev=<sha>`; exit 0 / 1 / 2.

**Test cases** (each is a one-line fixture against a scratch clone-free input; `--entry-file`
may stage the corrected/spliced text from the filesystem exactly like C1's `--ledger`):

| case | input | expected |
|---|---|---|
| base rev `85d57a8…` | entry absent (`git cat-file -e` → 128, measured) | MISSED, `entry_absent` |
| tip rev `ad4bf205…` (old bytes) | committed entry | **MISSED**, `P16:quote_not_at_pin` (measured by the draft counter) |
| repaired entry | corrections section appended | **MET**, `quotes_bound=20/20`, `superseded=3` |
| splice mutant | `P19` quote ← the old space-joined text | MISSED |
| missing heading | drop `supersedes P16, P17, P18` | MISSED (old P16 becomes effective) — proves clause c is load-bearing |
| subject mutant | `P23` ← `sendshortcut`'s repeat branch… | MISSED via §5.3 (only with clause f) |
| index mutant | remove `corpus/README.md:80` | MISSED |
| row mutant | `P22` row cell ← `S999` | MISSED |

The counter cannot claim entailment; the receipt must print
`entailment=not-checked (outside non-author review)`.

---

## 7. Deletion candidates (found, not performed) and the preserved contract

| candidate | evidence it is redundant | evidence it has live callers | disposition |
|---|---|---|---|
| `quality/check-tool-ledger.py` (832 lines) | second implementation of the same ledger predicate; the r53 C1 predicate does not name it, and rule table §3 needs none of it | `PROVINCE.md:118` (doc), `quality/counters/c1-r51-ledger.py:65` (`DEFAULT_CHECKER`), `quality/tool-ledger.md:9,:113,:117`, `SCORECARD.md:2787` (capability row) | retire **after** the r53 counter lands, in the same change that marks `c1-r51-ledger.py` historical; until then it is a competing authority |
| r51 counter machinery: `make_clone`, `resolve_work`, `sandbox_env`, `run_python`, `checker_selftest`, `checker_ledger`, 8 regex constants (~250 of 445 lines) | superseded by the no-clone shape; the r51 line stays valid for its own frozen predicate | `SCORECARD.md:2787` cites the r51 command | keep as provenance; **never copy it forward** into the r53 counter |
| round-52 draft counter's manifest/novelty/held/block-form clauses (~700 of 965 lines) | outside the r53 predicate; clause c measured failing on the landed shape | none committed | do not port |
| r52 entry row `P17` (near-duplicate of `P04`, wrong subject) | `Attack08.md:20`, `Falsify29.md:141` | none | superseded by `P23` (§5) |
| the five superseded v1 counters with registration-only pointers (`c1-r40-live.py`, `c1-r44-geometry-states.py`, `c1-r45-monitors.py`, `c2-r40-forms-entry.py`, `c2-r45-monitor-entry.py` — measured: apart from the three round-51 rows, the only rows with a registration-only pointer) | superseded by their `-v2` | registration is their only tracked citation (`quality/tool-ledger.md:24-25`) | **not** deletable: provenance; deleting them also silently changes `P` |

Preserved contract (unchanged by every recommendation above): population definition and the
`82`-path arithmetic; the ledger's 3-cell row grammar and `:<line>` pointer annotation;
`quality/tool-ledger.md` as the single ledger path; `PRED-C1-r51`/`PRED-C2-r51` as historical
predicates; the whitespace-collapsed quote policy and the 25-word cap; the r52 `fetch/` pins and
their checksums; the `S370`–`S373` registry rows; append-only corrections.

Tradeoff: the r53 C1 predicate as frozen is **strictly weaker** than the r52 wording (no
instrument-specific context), and the recommended counter therefore cannot reject a
population-shaped ledger whose 82 descriptions are *distinct* boilerplate. That is the honest
reading of "bounded structural accountability check"; claiming more would repeat the round-52
overstatement that its own simplifier measured false (`C1Simplify.md` §6, control F3).

---

## 8. Commands, environment, receipts

Lane: `git -C <lane> rev-parse HEAD` → `ad4bf2059bcfafe63671d262222908ee1fe8001c`.
Population at the tip: 82; ledger rows 82; 12 distinct pointer targets; 0 non-conforming pointer
cells; 0 duplicate descriptions; minimum description 9 words.

Executed (all read-only w.r.t. the lane; every write under
`/fast/scratch/hyaku/mado-r53/R53Three27`):

1. `python3 -I .ufo/waves/round-52/w1/C1Simplify/c1-r52-ledger.py --repo <lane> --rev ad4bf205…`
   → `verdict=TARGET_MET`, `real 0m0.171s`.
2. `python3 -I v53.py --repo <lane> --rev ad4bf205…` → `C1_R53: population=82 ledger_rows=82
   uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MET`,
   rc 0, 58–65 ms.
3. `python3 -I v53.py … --ledger controls/control-P-padded.md` → `self_pointer=82
   generic_desc=81 verdict=TARGET_MISSED`, rc 1; same for `-C` (`self_pointer=82`), `-D`
   (`generic_desc=81`), `-E` (`self_pointer=1`), `-F` (`bad_pointer=1`).
4. `python3 -I v53.py … --selftest` → `SELFTEST: 8/8 passed`.
5. r51 `parse_rows`+`describe` on the same four controls → `P`, `C`, `D` = `TARGET_MET`;
   `B` = `bad_pointer=53`.
6. `python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev ad4bf205… --work <scratch>`
   → `verdict=TARGET_MET`, 2011 ms.
7. `python3 -I .ufo/waves/round-52/w1/C2CounterDraft/c2-r52-proposition-entry.py --repo <lane>
   --rev ad4bf205… --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md --fetch-root
   .ufo/waves/round-52/fetch` → clause d `quotes_bound=17/18 … miss=P16:quote_not_at_pin`,
   overall `verdict=TARGET_MISSED`.
8. `sha256sum` of the two pins → `a83abeb5…`, `7248cbb8…`, equal to `fetch/SHA256SUMS`.
9. `git cat-file -e 85d57a8…:corpus/knowledge/hyprland-synthetic-dispatch-r52.md` → exit 128
   (base absence, the C2 no-work control).

**Newly opened external source: none.** No URL, access date or web quote applies to this report:
the pinned bytes were already on disk (round-52 `fetch/`, opened 2026-10-27, digests verified
above), and their registry rows are `corpus/SOURCES.md:320-323` (`S370`–`S373`, status `mined`,
`on-release`). Tool installs: **none** (no `/home/vgpnk/.omp/agent/RULES.md` action needed).

Scratch `/fast/scratch/hyaku/mado-r53/R53Three27` removed before yield; the four controls, the
217-line counter copy, and the two binding checkers were scratch-only. The lane is unchanged:
`git status --porcelain` → `?? .ufo/waves/round-53/` only (untracked wave dir, pre-existing).

---

## 9. Limits

- I did not build or commit the counters; sizes and timings are of scratch copies shaped for the
  frozen predicate. `quality/counters/c1-r53-ledger.py` and `c2-r53-proposition-entry.py` do not
  exist, and no r52 C1/C2 counter was ever committed (`git log -- quality/counters/` shows no
  round-52 counter commit).
- The C2 counter cannot check P17/P18 truth without the optional possessive rule; the
  independent reviewer remains the only check for localization and for near-duplication.
- Control files must be generated at the demonstration rev (population 84), not at the tip
  (§3); generating them today would freeze a population that the very commits under test change.
- No axis score is claimed and no vote is cast: this seat is not a non-author reviewer for
  either claim.

---

Report trailer

- report: `.ufo/waves/round-53/w1/R53Three27.md`
- seat: `R53Three27` (simplifier, leaf)
- attacked predicate: `PRED-C1-r53` (claims-frozen.md:5) and `PRED-C2-r53` (claims-frozen.md:9)
- base: `ad4bf2059bcfafe63671d262222908ee1fe8001c`
- axes: coverage (C2), operability (C1); no harm claimed to either
- armed evidence: measured counters/verdicts in §2, §3, §4, §5, §8
- new external source opened: none (pins reused, digests verified; registry rows SOURCES.md:320-323)
- tool installs: none; pacman touched: no
- tracked lane edits: none; wave writes: this report only
- scratch: `/fast/scratch/hyaku/mado-r53/R53Three27` (removed before yield)
- no commits, no jj, no task dispatch, no background jobs
