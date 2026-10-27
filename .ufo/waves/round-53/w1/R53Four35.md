# R53Four35 — revenger: C1/C2 prior-round failure and the minimal corrected contract

Seat `R53Four35` (revenger, leaf). Round 53, wave 1, lane `mado-shokunin`.
Base tip `ad4bf2059bcfafe63671d262222908ee1fe8001c` (verified `git rev-parse HEAD`).
Frozen claims: `.ufo/waves/round-53/claims-frozen.md:5-13`.
Axes named: **operability** (C1 instrument/ledger accountability) and **coverage** (C2
proposition grounding). This is a reverse-engineering report: it reconstructs what the prior
round actually measured, and states the smallest contract that is simultaneously
(a) source-true, (b) mechanically falsifiable, and (c) not already falsified by the r52
evidence. It is not a vote, does not edit any tracked file, and does not claim admission.

Attached predicate (named): the **C1 frozen structural predicate** — "a newly committed,
scratch-aware counter with explicit selftest returns TARGET_MET on the production ledger,
TARGET_MISSED on a no-work control and each frozen forgery fixture, with exact population
coverage and non-self pointers" — and the **C2 frozen repair predicate** — "append-only
correction clearly repairs P16/P17/P18 against opened pinned source bytes; a frozen counter
rejects the old bytes and accepts the corrected entry with quote/pin/proposition bindings;
independent reviewer checks source truth; no expansion credit without a row opened this round
and uncovered ground" (`.ufo/waves/round-53/claims-frozen.md:5-13`).

No seat counts as a non-author reviewer; nothing below is that review. No live read, no
package query, no producer, no screenshot, no host/compositor mutation, no lane or fleet
edit, no git/jj mutation. Counter runs are read-only over `git show`/`ls-tree` and write only
in `/fast/scratch/hyaku/mado-r53/R53Four35` (removed before yield; disk guard 622,121,068 KiB
free, 27% used, no ENOSPC). One accidental scratch directory created inside the lane by the
r51 counter's own `--work` handling was removed in the same step (`git status --porcelain`
then showed only the pre-existing untracked `.ufo/waves/round-53/`); see D2.

## 1. Base state, measured

| Fact | Command | Output |
|---|---|---|
| Base tip | `git -C <lane> rev-parse HEAD` | `ad4bf2059bcfafe63671d262222908ee1fe8001c` |
| Worktree clean | `git -C <lane> status --porcelain` | `?? .ufo/waves/round-53/` only |
| Counters at base | `git ls-tree -r --name-only HEAD quality/counters/ \| grep -E 'r5[0-3]'` | `c1-r50-bind-entry.py`, `c1-r51-ledger.py`, `c2-r50-session-gate.py`, `c2-r51-dispatch-entry.py` — **no r52 or r53 counter is committed** |
| Entry at base | `git ls-tree -r --name-only HEAD corpus/knowledge/ \| grep r52` | `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` |
| Index row | `corpus/README.md:80` | `knowledge/hyprland-synthetic-dispatch-r52.md` (round 52; source-pinned synthetic shortcut path) |
| Registry rows | `corpus/SOURCES.md:320-323` | S370–S373, status `mined`, opened `2026-10-27`, `used-by` the r52 entry |
| Knowledge count | `ls corpus/knowledge/*.md \| wc -l` | `68` (the r52 entry is already indexed at base) |
| R51 C1 production | `python3 -I quality/counters/c1-r51-ledger.py --repo <lane> --rev ad4bf205… --work <scratch>` | `C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c`, rc 0 |
| R52 frozen-control | `.ufo/waves/round-52/controls/c1-do-nothing.md` (2 rows, 4-cell) | — |
| Round-53 controls | `ls .ufo/waves/round-53/` | `claims-frozen.md`, `w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1.ready.partial`, `w1/` — **no `registration.md`, no `controls/`** (D5, D11) |

The population rule is the one the r51 counter already implements
(`quality/counters/c1-r51-ledger.py:118-134`): every `tools/**`, every depth-1
`quality/*.py`, every depth-1 `quality/counters/*.py`, excluding `__pycache__`/`.pyc`/`.pyo`.
At r53 base that is `P=82`; committing one new counter raises it to 83, two to 84.

## 2. C1 — reconstructed contract

### 2.1 What the inherited predicate actually tests (source bytes)

`quality/counters/c1-r51-ledger.py` is a **structural** counter, and its four green fields
are population/rows, dangling, bad_pointer, empty_desc. It has no description-context field
and no self-reference field. Its `pointer_resolves` (`:180-194`) accepts any token that
exists at `--rev` and whose bytes contain the row's basename as a substring; its
`describe` (`:196-238`) charges `empty_desc` only for empty/placeholder text. That is the
code path behind the frozen "Before" sentence ("accepts repeated generic descriptions and
ledger self-pointers"). It also has no `--ledger` flag: it reads the ledger **from the
revision** under test.

### 2.2 Failure reproduction at the r53 base (not inferred from r52 reports)

Fixture: `--shared` clone of the lane in scratch, commit at base, then one mutated
`quality/tool-ledger.md` per fixture; before every fixture commit
`git rev-parse --show-toplevel` printed the fixture dir.

| Fixture | Mutation | r51 counter output | rc |
|---|---|---|---|
| `forged-generic.md` (rev `8d96a9d1…`) | every row's description → `Generic accountability note for this instrument.`; pointers untouched | `C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=8d96a9d1b640a69c1809d216837db505ac55456c` | 0 |
| `forged-selfpointer.md` (rev `0c16a604…`) | every row's pointer cell → `` `quality/tool-ledger.md` `` | `… verdict=TARGET_MET rev=0c16a604689aaeb13e1e428f196d14a989e8121d` | 0 |

Both frozen "Before" failures are reproduced **at the r53 base**, on the exact counter the
round would inherit. (The r51 counter cannot even score the no-work control: it has no
`--ledger` flag, so the control can only be exercised by a new counter.)

### 2.3 The r52 draft counter, and the ceiling that cannot be closed lexically

The reviewed r52 draft (`0fe862f1…`, 847 lines,
`.ufo/waves/round-52/w1/C1CounterDesign/c1-r52-ledger.py`, 53-check selftest) was re-run at
the r53 base:

| Input | Output | rc |
|---|---|---|
| production ledger | `C1_R52: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MET rev=ad4bf205…` | 0 |
| `forged-generic.md` | `… generic_desc=82 verdict=TARGET_MISSED …` | 1 |
| frozen control `c1-do-nothing.md` | `C1_R52: population=82 ledger_rows=2 uncovered=81 dup=1 dangling=0 bad_pointer=0 self_pointer=1 generic_desc=1 verdict=TARGET_MISSED` | 1 |
| `Attack01/controls/F-all-forged.md` (82 rows, production paths/pointers, filler + a two-word phrase lifted from each instrument's own bytes) | `C1_R52: population=82 ledger_rows=82 uncovered=0 dup=0 dangling=0 bad_pointer=0 self_pointer=0 generic_desc=0 verdict=TARGET_MET` | **0** |
| five self-pointer laundering spellings (pointer cell = self token **and** the production pointer), built at r53 base | each `… self_pointer=0 … verdict=TARGET_MET`, rc 0 — tokens `tool-ledger.md`, `/quality/tool-ledger.md`, `Quality/tool-ledger.md`, `quality/tool-ledger.md:x`, `quality/tool-ledger.md)` | 0 each |

So the strongest reviewed design:
1. **cannot** separate a motivated generic-description forgery from production prose —
   82/82 forged rows pass (`generic_desc=0 TARGET_MET`), which is the r52 lesson M52-1
   residual and the Attack01 F-all result reproduced on r53 base bytes;
2. still accepts five of the nine self-pointer spelling shapes (its self test is exact-string
   equality against `quality/tool-ledger.md` and the row path; basename, leading slash, case
   fold, non-numeric suffix and trailing punctuation are not normalized).

Consequence for the frozen r53 C1 text: **if the frozen forgery fixture set includes the
generic-prose class (F-all), the claim is unsatisfiable by construction** — no lexical rule
can reject it without rejecting production rows (C1CounterDesign ceiling 1, and the
measured 82/82). The minimal contract therefore must (i) freeze only *structural* fixtures,
and (ii) record the generic-prose class as a declared ceiling, not a fixture. That is the
single change that turns the r52 dead end into a passable claim.

### 2.4 Minimal corrected contract (C1)

Restated claim (bounded, structural): *at the final revision that contains the counter and
its ledger row, the counter mechanically establishes that every population instrument has
exactly one ledger row with a resolvable, non-self, non-symlink evidence pointer, and that
its own selftest discriminates green from red. It does not judge description meaning.*

| # | Clause | Mechanical check | Status at r53 base |
|---|---|---|---|
| C1.1 | One committed program, `quality/counters/c1-r53-ledger.py`; `python3 -I <c> --repo <lane> --rev <rev> --work <scratch>`; every byte from `--rev`; no working-tree read; no write outside scratch; exit 0/1/2 | source + receipt | absent (no r53 counter) |
| C1.2 | Population = `git ls-tree -r --name-only <rev>` filtered by the r51 rule; print `population=P ledger_rows=R`; require `R==P`, `uncovered==0`, `dup==0`, `dangling==0` | measured arithmetic (below) | P=82 |
| C1.3 | Fence-aware ledger parse: rows inside ```/~~~ fences are not data; rows wider than 3 cells are scored, not dropped | fixture F8 | r51 is fence-aware; the r52 landed rewrite was not (A5/O1) |
| C1.4 | **Non-self under normalized identity**: strip backticks/emphasis, `./`, collapse `//`, strip leading/trailing `/`, strip trailing `);,`, strip a `:<suffix>` with no `/`, casefold; self if equals ledger path or row path, **or** if it has no `/` and its basename equals either basename. Charge `self_pointer` on any self token in the pointer region, regardless of other tokens | fixture F5 | r51 has no field; draft fails 5 shapes |
| C1.5 | **Resolvable target** at `--rev`: regular blob (mode 100644/100755, **not** 120000), not a population instrument, bytes name the row's basename name-boundedly; else `bad_pointer` | fixtures F6/F7 | r51 uses substring, no mode check |
| C1.6 | **Context clause removed from the predicate.** No requirement that a generic-description forgery fail; record it as a ceiling with the measured 82/82 | — | r52 froze an unfalsifiable clause |
| C1.7 | `--selftest --work <scratch>` builds a throwaway fixture repo (asserted toplevel), runs a fixed count N of named green/red probes, prints `<PRED>_SELFTEST: i/N passed`, exit 0 only on full pass; measurement mode never takes the selftest path | fixture F10 | draft: `53/53 passed`; r52 landed rewrite: silent no-op (O3) |
| C1.8 | **Scratch-aware**: the counter itself refuses (exit 2, before any write) a work root whose realpath is inside `--repo`, under `/tmp`, `/var/tmp`, `/dev/shm`, or inside `$HOME`; creates the dir only after the check; removes what it created | fixture F11 | r51 accepts all of these (below) |
| C1.9 | Production receipt at the final committed revision, naming rev + counter sha256 + ledger sha256, archived under `.ufo/waves/round-53/receipts/` | receipt | absent |
| C1.10 | Control + fixture receipts at the **same** counter digest and revision; each names the defect field that fired | receipt | absent |

Measured population arming (the clause that makes C1.2 non-vacuous): a fixture commit that
adds `quality/counters/c1-r53-probe.py` **without** a ledger row produced
`C1_R51: population=83 ledger_rows=82 uncovered=1 … verdict=TARGET_MISSED`; adding a row
whose pointer resolves to a committed document that names the probe produced
`C1_R51: population=83 ledger_rows=83 uncovered=0 … verdict=TARGET_MET`. Two consequences:
the production run must be at the commit that contains the counter **and** the row, and every
other new counter committed in the same round changes `P` (D4).

Measured scratch behaviour of the inherited counter (C1.8 is not already met):
`--work <lane>/.ufo/scratch-probe` created the directory inside the lane and failed only
because the inner gate refuses it (`detail: checker selftest failed (exit=2 form=with-work)`),
and `--work /tmp/<dir>` ran with
`detail: hint: the gate refuses --selftest work under /tmp, /var/tmp, /dev/shm` plus
`selftest=failed`. The counter's own `REFUSED_ROOTS` is a post-failure hint, not a check.

Normalization rule is green-safe: applied to the 82 production pointer cells it yields
`false_positive_self_tokens=0`; applied to seven laundering shapes it yields `self=True` for
each, while a production pointer (`.ufo/waves/round-51/registration.md`) stays non-self.

### 2.5 Frozen fixture set — must-fail vs ceiling

Must fail (exit 1, with the named field non-zero; each is one mutation of production, so the
signal is attributable):

| ID | Fixture | Required signal |
|---|---|---|
| F1 | no-work: zero rows / the r52 4-cell control shape | `uncovered`/`self_pointer` (field, not just exit) |
| F2 | duplicate row | `dup=1` |
| F3 | one production row deleted | `uncovered=1` |
| F4 | row for a non-population path | `dangling=1` |
| F5 | seven self-pointer spellings (basename, `./`, leading `/`, case, `//`, `:x`, trailing `)`) and one symlink alias (mode 120000) | `self_pointer=1` (symlink may be `bad_pointer`) |
| F6 | pointer to a peer instrument | `bad_pointer=1` |
| F7 | pointer to a nonexistent path | `bad_pointer=1` |
| F8 | grammar example moved outside the fence | `dangling`/`bad_pointer` |
| F9 | new instrument committed without its row | `uncovered=1` (measured 82→83) |
| F10 | counter with a dropped selftest case | selftest fails (fixed-count guard) |
| F11 | work root inside repo, `/tmp`, `/var/tmp`, `/dev/shm`, `$HOME` | exit 2 before any write |

Declared ceilings, **not** fixtures: generic prose (F-all, measured 82/82 pass), evidence
cycles and a shared registry document across rows (Attack02 P13/P14), and a target whose
bytes merely mention the instrument name. Putting any of these in the frozen fixture set
makes C1 unsatisfiable.

## 3. C2 — reconstructed contract

### 3.1 What the committed entry declares vs the pinned bytes (all three defects measured)

Pins: `.ufo/waves/round-52/fetch/` — `Hyprland-ConfigActions.cpp` sha256 `a83abeb5…`,
`Hyprland-legacy-DispatcherTranslator.cpp` sha256 `7248cbb8…` (digests equal
`.ufo/waves/round-52/fetch/SHA256SUMS` and the S370/S371 row cells). These are local pinned
bytes opened read-only this round; I did **not** fetch the URLs. URL/date for these rows:
`https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp`
and `…/src/config/legacy/DispatcherTranslator.cpp`, opened `2026-10-27` per
`corpus/SOURCES.md:320-321`.

| Prop (entry `:28-30`) | Declared | Measured on the pin | Verdict |
|---|---|---|---|
| P16 | claim "sends modifier state before the key event, then clears the modifier state"; pin `Hyprland-ConfigActions.cpp:1554-1558,1576`; quote joins the `:1554` mods call to the `:1558` PRESSED call | the joined quote occurs **nowhere** in the file or the span (`collapsed_in_full_file=False`, `collapsed_in_anchor_span=False`, and still false over `1554-1576`); between them sit `:1556 if (S.m_passPressed == 1) {` and `:1557 if (!isMouse)`; the clear is a separate `:1576 g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);`; the anchor regex `(\d+)(?:-(\d+))?` parses `1554-1558` and silently drops `,1576` (`remaining=',1576'`) | **spliced quote + unsupported ordering claim + truncated multi-span anchor** |
| P17 | claim "`sendshortcut`'s repeat branch can invoke its delegate twice"; pin `…Translator.cpp:619-622`; quote `if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` | anchor 619–622 lies inside `sendkeystate` (function span `591-627`); `sendshortcut` spans `531-589` and contains no repeat branch; the quote is a strict substring of P04's quote on the same anchor (`P17_quote_substring_of_P04_quote=True`) | **wrong subject + duplicate fact** |
| P18 | claim "returns the `key not found` error **inside the scan**"; pin `…Translator.cpp:574` | the scan is `:565 for (xkb_keycode_t kc = …) {`, its body is depth 4, and it closes at `:571 }`; `:573 if (!keycode)` and `:574 return {… "key not found"};` sit at depth 3, i.e. **after** the loop, before the separate `:579-580` `invalid key` guard | **mislocalized ("inside" is false)** |

Exact corrected compression of the same facts (each quote verified as an **exact**
whitespace-collapsed span match, ≤25 words):

| New | Proposition | Pin | Quote (verified) | Words |
|---|---|---|---|---|
| P16a | The action asserts the modifier mask, then sends the keyboard PRESSED event only inside the press-field branch when the key is not a mouse button. | `Hyprland-ConfigActions.cpp:1554-1558` | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` | 16 |
| P16b | After the branch, the action clears the modifier mask before the window-null return. | `Hyprland-ConfigActions.cpp:1576-1579` | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0); if (!window) return {};` | 8 |
| P17′ | Before delegating, `sendkeystate` writes 1 to the shared press field for down/repeat and 0 for up. | `Hyprland-legacy-DispatcherTranslator.cpp:614-617` | `if (keyState == 1 || keyState == 2) Config::Actions::state()->m_passPressed = 1; else Config::Actions::state()->m_passPressed = 0;` | 15 |
| P18′ | After the keysym scan, a zero keycode returns `sendshortcut: key not found`. | `Hyprland-legacy-DispatcherTranslator.cpp:573-574` | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` | 12 |

The `invalid key` contrast at `:579-580` can live in the rationale as an unquoted locator, or
be a separate proposition with its own contiguous quote; it must not be asserted inside P18′.

### 3.2 The counter's discrimination boundary (measured on the committed entry)

The reviewed r52 draft counter was run at base with the committed entry:

```
$ python3 -I <round-52>/w1/C2CounterDraft/c2-r52-proposition-entry.py --repo <lane> \
    --rev ad4bf2059bcfafe63671d262222908ee1fe8001c \
    --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md \
    --fetch-root .ufo/waves/round-52/fetch --work <scratch>
C2_R52: a ok=1 index_row=`knowledge/hyprland-synthetic-dispatch-r52.md` (round 52;...
C2_R52: b ok=1 propositions=18 ids=18 forms=table
C2_R52: c ok=0 rows_bound=0/18 distinct_rows=0 miss=P01:anchor_no_fetch_root,...
C2_R52: d ok=0 quotes_bound=17/18 quotes_raw=6/17 pins=4 policy=whitespace-collapsed pins_prior_equal=4/17 miss=P16:quote_not_at_pin(Hyprland-ConfigActions.cpp:1554)
C2_R52: e ok=0 prose_rows=4 prop_rows=4 manifest_rows=0 miss=P01:id_not_referenced,...
C2_R52: clauses=abcde clauses_met=2 admitted=0/1 verdict=TARGET_MISSED rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
```

Four facts follow:
1. **P16 is caught structurally** by quote-at-span binding (17/18 bind).
2. **P17 and P18 pass clause (d)** — the best structural counter available cannot see a wrong
   subject or a wrong location. They need the new checks in C2.5–C2.7 (or a frozen
   defect-signature list), otherwise "the counter rejects the old bytes" is false.
3. **Clause (c) fails on the committed registry rows** (`anchor_no_fetch_root` 18/18): the
   S370–S373 anchor cells carry `<file>:<span> @ <40-hex>; r52 fetch SHA256 <digest>` and not
   the literal fetch path. The registry is append-only; the fix belongs in the counter
   (accept the digest form and verify it — all four digests match, measured). Rewriting the
   rows would break append-only history.
4. **Clause (e) fails on the committed entry** (`id_not_referenced` 18/18): the 32-line landed
   entry has no prose citing a `P##` id. Either restore a "What the evidence licenses" table
   or explicitly drop clause (e) — but the choice must be printed, not implicit.

Also: the draft's pin resolution is by basename under the fetch root; the wave tree holds nine
byte-identical pin copies (A8). The r53 counter must take an explicit fetch root (or a
digest-checked manifest) and must not index basenames across the whole wave.

### 3.3 Minimal corrected contract (C2)

| # | Clause | Mechanical check | Measured basis |
|---|---|---|---|
| C2.1 | Entry exists at rev and an unfenced `corpus/README.md` row indexes it | index parse | already true |
| C2.2 | **Append-only repair shape**: a correction block names P16/P17/P18, quotes each withdrawn text exactly once, supplies corrected propositions with `supersedes: P##`, and no withdrawn id remains live or duplicated; front matter records `verified-at` and the repair round | parser over the block | entry has no correction block today |
| C2.3 | One contiguous `file:start-end` anchor per proposition (no comma lists); the counter parses the full span | anchor grammar | P16's `,1576` tail is dropped by the current regex |
| C2.4 | Quote 3–25 whitespace words, collapsed-verbatim inside the anchor; policy frozen and printed; `quotes_raw` reported as diagnostic | span scan | P16 fails; 17/18 pass |
| C2.5 | **Subject binding**: if a proposition names a backticked identifier the pin defines as a function, the anchor must lie inside that function's brace span | brace-span parse | P17 fails (`619` in `sendkeystate`, not `sendshortcut`) |
| C2.6 | **Duplicate-fact rejection**: no proposition quote may be a ≥6-word contiguous substring of another quote on the same pin; no identical claims | substring test | P17 quote ⊂ P04 quote |
| C2.7 | **Containment binding**: a proposition asserting "inside the scan/loop" must have its anchor inside a preceding loop block (brace depth) | depth parse | P18 fails (`573-574` depth 3, loop body depth 4) |
| C2.8 | Row binding without rewriting the registry: row exists, `mined`, `used-by` names the entry, and the anchor cell's 64-hex digest (or fetch path) resolves to the pin file at rev | digest compare | digests all match at base |
| C2.9 | **Freshness re-scoped**: rows exist at base, so "absent at base" must not be a clause; the receipt classifies the move as **repair**, cites the r52 opening date, and claims 0 expansion | receipt fields | S370–S373 present at base |
| C2.10 | Frozen counter digest recorded before data; run at (a) base rev → `TARGET_MISSED` naming P16 (`quote_not_at_pin`), P17 (`subject_out_of_scope`, `duplicate_quote`), P18 (`containment_outside_anchor`); (b) corrected rev → `TARGET_MET`; both receipts name rev + counter sha256 | two runs | this report's run is (a) |
| C2.11 | **Reviewer boundary**: the source-truth review is out-of-swarm; no r53 seat may be recorded as the non-author reviewer; until it lands the entry is `provisional` and the counter pass is necessary-not-sufficient | report field | seat spec: "No seat counts as non-author reviewer" |
| C2.12 | Proposition ids cited outside the map, or clause (e) explicitly dropped and printed | parse | committed entry fails as written |

Acceptance for C2 on these clauses: counter `TARGET_MISSED` at base with the three named
defects, `TARGET_MET` on the corrected bytes; all four corrected quotes bind exactly (measured
above); the correction block is append-only; the reviewer step is handed off, not
self-certified.

## 4. Divergences (each with its evidence)

- **D1 — C1's generic-prose fixture is unsatisfiable.** Measured at r53 base: the reviewed r52
  draft accepts `F-all-forged.md` 82/82 (`generic_desc=0 TARGET_MET`). Any frozen fixture of
  that class makes C1 mathematically unreachable. Freeze structural fixtures only; declare the
  ceiling (C1.6).
- **D2 — "scratch-aware" is not met by the inherited counter.** `--work` inside the lane was
  created and only failed through the inner gate; `--work /tmp/...` was accepted with a hint.
  The counter itself must refuse (C1.8).
- **D3 — r52 shipped the wrong bytes, not just the wrong test.** The reviewed 847-line draft
  was displaced by an uncommitted 78-line rewrite at `quality/counters/c1-r52-ledger.py`
  (Attack01 T3/O1–O3: fence row parsed as data → red on production; no named red signals;
  `--selftest` a no-op). Nothing was committed; the round had no C1 measurement at tip. The
  minimal process fix inside the contract: one digest, one program, receipts that name it.
- **D4 — C1 and C2 are causally separate but mechanically coupled by `population`.** Each newly
  committed counter adds a ledger row (measured 82→83). A C1 receipt taken before the C2
  counter commits is invalidated by it. Both counters and both rows must land in one revision,
  and both production receipts must name that revision.
- **D5 — the r53 fixture set is not frozen yet.** `ls .ufo/waves/round-53/` shows no
  `controls/`; "control design and measurement must be frozen before data" is currently
  unmet, so any counter run today is pre-freeze and cannot be the claim's measurement.
- **D6 — C2 clause (c) is incompatible with the committed registry rows.** `anchor_no_fetch_root`
  18/18; the digest form must be accepted and verified (digests match) rather than rewriting
  append-only rows.
- **D7 — C2 "row opened this round" cannot be satisfied at r53 base.** S370–S373 exist and are
  `mined`; the r53 counter must re-scope freshness and the report must claim repair, not
  expansion (this is also the frozen claim's own "no expansion credit" clause).
- **D8 — C2 clause (e) fails on the landed entry.** No `P##` id appears outside the map. The
  choice between restoring the licensing table and dropping the clause must be frozen and
  printed.
- **D9 — structural binding cannot catch P17/P18 by design.** 17/18 quotes bind while both
  propositions are false. Function-scope, duplicate-substring and containment checks (or a
  frozen defect-signature list) are required for "rejects the old bytes" to be true of all
  three.
- **D10 — residual, not in the three-proposition scope:** P12 still says "null optional
  window"; the translator value is a null `PHLWINDOW` and the optional engaged-with-null
  exists only inside `Actions::pass` (r52 Attack32 A4). A strict type-level subject check would
  surface it; fixing it is a fourth repair, outside the frozen C2 target.
- **D11 — no round-53 registration artifact.** The frozen text says registration governs, but
  the directory has only `claims-frozen.md` plus the spec/dispatch. The C1 ledger pointer needs
  a committed document that names the counter, so the wave report/receipt must be committed
  before the production run.
- **D12 — routed r52 defects still open.** `corpus/lessons/round-52.md:5` `## Gate` has no
  per-row record for S370–S373 (the CORPUS contract wants URL, access date and a ≤25-word
  located quote for each); `:23-25` `## Changes` still reads "Pending final integration
  revisions and receipts." Both are append-only corrections, not rewrites.
- **D13 — QUALITY 17 review still outstanding.** `corpus/SOURCES.md:374` records that S370,
  S371 and S373 reuse the S365/S364/S367 canonical URLs at the same commit with "distinct-scope
  review remains outstanding". A warning census is not the review (QUALITY.md:34). Until the
  verdict is recorded per row, the entry's row set sits under an open criterion.
- **D14 — no in-round non-author reviewer.** The seat spec forbids any seat counting as the
  non-author reviewer, so C2 can end at most `provisional`; this report is not that review and
  must not be cited as one.

## 5. Confidence

| Claim | Confidence | Basis |
|---|---|---|
| The three P16–P18 defects and their exact corrected quotes | **high** | independent span/brace/function checks against digest-verified pins; corrected quotes are exact span matches |
| The r51 counter accepts generic descriptions and self-pointers at r53 base | **high** | two forged fixtures executed at base, rc 0 |
| The r52 draft accepts F-all 82/82 | **high** | executed at r53 base |
| Five laundering shapes survive the draft's self test | **high** | executed at r53 base |
| The normalization rule catches 7 shapes with 0 production false positives | **high** | executed over the 82 committed pointer cells |
| Population arming 82→83 | **high** | executed in a scratch fixture |
| The counter cannot catch P17/P18 structurally | **high** | executed: 17/18 bind, both false propositions pass |
| The corrected claim wording is the *only* minimal one | **medium** | source-true and mechanically falsifiable; alternate splits (drop P17, merge P16 into one multi-row map) are defensible |
| Reviewer/admission outcome | **unknown** | out-of-swarm judgment; not claimed |

Limits: no live read, no dispatcher run, no client receipt, no URL fetch; all source facts are
the r52 local pins, digest-verified at base. The scratch fixture commits are local-only and
unreachable from the lane; no lane ref was moved. The `--shared` clone and forged ledgers were
deleted with the scratch root.

## Report

```
attacked=C1 "a newly committed, scratch-aware counter with explicit selftest returns TARGET_MET on the production ledger, TARGET_MISSED on a no-work control and each frozen forgery fixture, with exact population coverage and non-self pointers"; C2 "append-only correction repairs P16/P17/P18 against opened pinned bytes; a frozen counter rejects the old bytes and accepts the corrected entry with quote/pin/proposition bindings; independent reviewer checks source truth; no expansion credit without an opened-this-round row and uncovered ground"
before=measured at ad4bf205: r51 counter 82/82 TARGET_MET on production; forged-generic and forged-selfpointer both TARGET_MET rc 0; r51 has no --ledger and no scratch refusal (in-lane work dir created; /tmp accepted with hint); no r52/r53 counter committed; r52 entry committed+indexed, P16 spliced (quote not in file/span; ',1576' anchor tail dropped), P17 subject wrong (619-622 in sendkeystate 591-627, not sendshortcut 531-589; quote ⊂ P04 quote), P18 "inside scan" false (loop 565-571 depth 4; 573-574 depth 3)
reproduced=r52 draft counter at r53 base: production TARGET_MET; F-all-forged 82/82 TARGET_MET (ceiling); frozen control self_pointer=1 generic_desc=1 TARGET_MISSED; five laundering spellings self_pointer=0 TARGET_MET; entry at base: clauses a,b ok; c 0/18 anchor_no_fetch_root; d 17/18 quotes_bound, P16 quote_not_at_pin; e 18/18 id_not_referenced; verdict TARGET_MISSED rc 1
contract=C1: fence-aware population exact (82 base, 83 per new counter), normalized non-self identity + symlink/mode rejection + name-bounded resolvable target, scratch refusal outside repo//tmp//var/tmp//dev/shm/$HOME, fixed-count selftest, receipts at final revision, generic-prose class declared ceiling not fixture. C2: append-only correction block (P16→P16a+P16b, P17→press-field write, P18→after-scan return), one contiguous anchor, quote<=25 collapsed-verbatim, subject/containment/duplicate checks, digest-based row binding without registry rewrite, freshness re-scoped to repair, out-of-swarm reviewer boundary
corrections=freeze structural fixtures only (F1-F11) and drop the generic-description requirement; add function-scope, duplicate-substring and containment checks; accept the committed digest-form row anchors; land both counters+rows in one revision and receipt at it; commit a naming document before the production run; keep the entry provisional pending out-of-swarm source-truth review
divergences=D1 unsatisfiable generic fixture; D2 not scratch-aware; D3 r52 landed rewrite replaced reviewed bytes; D4 population couples C1/C2; D5 no r53 controls/ yet; D6 clause c vs committed rows; D7 row-freshness vs r53 base; D8 clause e; D9 P17/P18 invisible; D10 P12 residual; D11 no r53 registration; D12 Gate/Changes open; D13 QUALITY 17 open; D14 no in-round non-author reviewer
sources=local pins .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp (sha256 a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637) and Hyprland-legacy-DispatcherTranslator.cpp (sha256 7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771), revision efb50993780079460b0cbed1363e2166a2de1d9f, URLs per corpus/SOURCES.md:320-321, opened 2026-10-27 by round 52, re-opened read-only this round (no fetch)
confidence=high on byte-level and executed-counter facts; medium on the exact minimal wording; unknown on reviewer/admission
report=.ufo/waves/round-53/w1/R53Four35.md
```

Path note: this report is at
`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-53/w1/R53Four35.md`; the trailer
`report=` path is relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`.
