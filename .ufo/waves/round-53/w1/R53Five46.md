# R53Five46 — executable counter/fixture evidence for C1 and C2 (executor, leaf)

Lane `mado-shokunin`, round 53, wave w1, seat `R53Five46` (executor, leaf). Base tip
`ad4bf2059bcfafe63671d262222908ee1fe8001c`; lane worktree clean except the untracked round-53
directory (`git status --porcelain` → `?? .ufo/waves/round-53/`). Axes named: **operability**
(C1) and **coverage** (C2). This report is evidence for the parent, not a vote and not a
non-author review; I did not commit, judge, widen scope or touch tracked lane bytes.

Evidence tags: `[OBS]` measured in this seat, `[INF]` composite inference, `[UNK]` unresolved.

## 1. Attacked predicates (frozen text, quoted)

- **C1** — `.ufo/waves/round-53/claims-frozen.md:5-7` [OBS]: “operability: instrument-ledger
  accountability counter … Before: r51 counter accepts repeated generic descriptions and ledger
  self-pointers; r52 verifier reproduced bypasses. Target: a newly committed, scratch-aware
  counter with explicit selftest returns TARGET_MET on the production ledger, TARGET_MISSED on a
  no-work control and each frozen forgery fixture, with exact population coverage and non-self
  pointers. This is a bounded structural accountability check, not semantic proof.”
- **C2** — `.ufo/waves/round-53/claims-frozen.md:9-11` [OBS]: “coverage: repair
  proposition-grounding defects in the indexed r52 dispatcher entry … Before: r52 verifier found
  P16 quote spliced, P17 misattributed, P18 mislocalized; no valid r52 admission counter. Target:
  append-only correction clearly repairs those three propositions against opened pinned source
  bytes; a frozen counter rejects the old bytes and accepts corrected entry with
  quote/pin/proposition bindings; independent reviewer checks source truth.”
- Causal separation: `.ufo/waves/round-53/claims-frozen.md:13`; controls frozen before data,
  no axis harm admissible.

At report time `.ufo/waves/round-53/` holds only `claims-frozen.md`, `w1-spec.json`,
`w1-dispatch.json`, `w1.ready*` and the `w1/` reports — **no round-53 registration document and
no frozen forgery-fixture registry** [OBS: `ls -la .ufo/waves/round-53/`]. The forgeries measured
here are therefore the ones the frozen before-state names (repeated generic descriptions,
ledger self-pointers) plus isolating arms I built in scratch.

## 2. What was built (scratch only, deleted before yield)

| Artifact | Purpose |
|---|---|
| `R53Five46/r53-c1-ledger.py` | scratch candidate C1 counter; reads only `--repo`/`--rev` through a `--shared` clone in `--work`; explicit `--selftest` |
| `R53Five46/build-fixtures-c1.py` + `fx-c1/` | one git fixture repo whose base commit is the lane base tree (`git archive`), then eleven commits, each changing only `quality/tool-ledger.md`; every commit asserts `git rev-parse --show-toplevel` = the fixture dir |
| `R53Five46/r53-c2-bindings.py` | scratch C2 binding checker: entry table × `corpus/SOURCES.md` × `.ufo/waves/round-52/fetch/` bytes |
| `R53Five46/build-fixtures-c2.py` + `c2-fx/` | corrected-entry fixture and six single-clause mutants; fetch root and `SOURCES.md` stay the read-only lane inputs |

No committed counter, fixture or tracked file was produced by this seat. The scratch candidates
are demonstrations that the frozen criteria are mechanically satisfiable with clause-attributed
controls, and they name the exact clause set a committed r53 counter must reproduce.

## 3. C1 before-state — the r51 counter on the same fixtures [OBS]

Command form:

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo /fast/scratch/hyaku/mado-r53/R53Five46/fx-c1 \
    --rev <fixture-rev> --work /fast/scratch/hyaku/mado-r53/R53Five46/r51/<fixture>
```

r51 measures `population / ledger_rows / uncovered / dangling / bad_pointer / empty_desc / dup`
(`quality/counters/c1-r51-ledger.py:133` population, `:155` row parser, `:196` pointer resolver,
`:211` measurement). At the base tree it reports `population=82 ledger_rows=82` (82 = the
population formula, measured independently). Results on the forgeries:

```
### base              rc=0  C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET
### all-self          rc=0  C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET
### laundered-self    rc=0  C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET
### generic-repeat    rc=0  C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET
### generic-unique    rc=0  C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET
### anchor-mismatch   rc=0  C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET
### ledger-copy-alias rc=0  C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET
### dup-row           rc=1  C1_R51: population=82 ledger_rows=83 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok dup=1 checker=failed verdict=TARGET_MISSED
### dangling-row      rc=1  C1_R51: population=82 ledger_rows=83 uncovered=0 dangling=1 bad_pointer=0 empty_desc=0 selftest=ok checker=failed verdict=TARGET_MISSED
### bad-pointer       rc=1  C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=1 empty_desc=0 selftest=ok checker=failed verdict=TARGET_MISSED
### ledger-symlink    rc=1  C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=82 empty_desc=0 selftest=ok checker=failed verdict=TARGET_MISSED
### no-work-control   rc=1  C1_R51: population=82 ledger_rows=2 uncovered=81 dangling=0 bad_pointer=1 empty_desc=0 selftest=ok dup=1 checker=failed verdict=TARGET_MISSED
```

[OBS] The frozen before-state is reproduced: the r51 predicate is `TARGET_MET` on all 82 rows
pointing at the ledger itself, on the `./`-laundered spelling, on one repeated generic sentence,
on 82 unique generic sentences, on a pointer whose `:line` anchor does not contain the basename,
and on a byte-identical copy of the ledger. The committed no-work control
(`.ufo/waves/round-52/controls/c1-do-nothing.md`, sha256
`ad72f72f64708d1b877d0f2233f32a065bd11689d644af669176d1844ba2eba6`) already MISSes the r51
clauses (`uncovered=81 dup=1 bad_pointer=1`), so it cannot be the load-bearing arm for the
non-self / description clauses — the same attribution gap the r52 MistakeMiner measured
(`.ufo/waves/round-52/w1/MistakeMiner.md` §2.1) [OBS here on the same bytes].

## 4. C1 candidate — clause set, selftest, and clause-isolated matrix [OBS]

Candidate clauses (each its own counter field; verdict `TARGET_MET` only if every field is zero
and `ledger_rows == population == 82`):

- `uncovered / dangling / dup` — exact population coverage at `--rev` (same population formula
  as `c1-r51-ledger.py:133`).
- `empty_desc` — description not empty / punctuation-only.
- `desc_repeat` — no two rows share one normalised description (the repeated-sentence forgeries).
- `desc_unsupported` — ≥2 distinctive tokens of the description occur in the instrument's own
  bytes **and** they are ≥30% of the description's distinctive tokens (shared ≥2 ∧ ratio ≥0.30;
  tokens = lowercased `[a-z0-9_]+`, length ≥5, minus a stopword list).
- `self_pointer` — no pointer token resolves to the row, to the ledger path, or to bytes equal to
  the ledger (after `./` stripping, `:line` stripping, `normpath`, and `mode 120000` symlink
  resolution).
- `bad_pointer` — at least one pointer token names a tracked file whose bytes contain the row
  basename (the r51 clause).
- `pointer_anchor` — a `:line` anchor exists and that line contains the basename.

Thresholds were measured against the production ledger before being fixed: 79/79 line anchors
resolve and name the basename at the anchor line; description→own-bytes shared distinctive tokens
min = 3, min ratio = 0.40 (production ledger, 82 rows) [OBS]. So the 2/0.30 floor does not
reject production and sits one token below its worst row.

Explicit selftest (tiny in-selftest git repos, no lane read):

```
$ python3 -I r53-c1-ledger.py --selftest --work /fast/scratch/hyaku/mado-r53/R53Five46/st-work
SELFTEST_CASE: accept expect=TARGET_MET got=TARGET_MET ok
SELFTEST_CASE: self-pointer expect=TARGET_MISSED got=TARGET_MISSED ok
SELFTEST_CASE: self-pointer-laundered expect=TARGET_MISSED got=TARGET_MISSED ok
SELFTEST_CASE: self-pointer-content-alias expect=TARGET_MISSED got=TARGET_MISSED ok
SELFTEST_CASE: generic-repeat expect=TARGET_MISSED got=TARGET_MISSED ok
SELFTEST_CASE: generic-unique expect=TARGET_MISSED got=TARGET_MISSED ok
SELFTEST_CASE: empty-desc expect=TARGET_MISSED got=TARGET_MISSED ok
SELFTEST_CASE: bad-pointer expect=TARGET_MISSED got=TARGET_MISSED ok
SELFTEST_CASE: dangling expect=TARGET_MISSED got=TARGET_MISSED ok
SELFTEST_CASE: dup expect=TARGET_MISSED got=TARGET_MISSED ok
SELFTEST: 10/10 passed verdict=ok          (exit 0)
```

Production ledger at the lane base:

```
$ python3 -I r53-c1-ledger.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --rev ad4bf2059bcfafe63671d262222908ee1fe8001c --work .../w/lane-base
C1_R53: population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0 empty_desc=0 desc_repeat=0 \
desc_unsupported=0 self_pointer=0 bad_pointer=0 pointer_anchor=0 selftest=ok verdict=TARGET_MET \
rev=ad4bf2059bcfafe63671d262222908ee1fe8001c                        (exit 0)
```

Fixture matrix (one ledger mutation per commit; the deciding field is bolded in prose):

| Fixture | mutation | r51 | candidate | deciding field |
|---|---|---|---|---|
| base | none | MET | MET | — |
| all-self | cell 3 → `quality/tool-ledger.md` (82/82) | MET | MISS | `self_pointer=82` |
| laundered-self | cell 3 → `./quality/tool-ledger.md` | MET | MISS | `self_pointer=82` |
| generic-repeat | one identical sentence in all 82 rows | MET | MISS | `desc_repeat=82` (+`desc_unsupported=81`) |
| generic-unique | 82 distinct lorem-ipsum sentences | MET | MISS | `desc_unsupported=82` |
| dup-row | one duplicated instrument row | MISS | MISS | `ledger_rows=83 dup=1` |
| dangling-row | one row naming `tools/ghost-instrument.py` | MISS | MISS | `ledger_rows=83 dangling=1` |
| bad-pointer | first row → an existing file that never names it | MISS | MISS | `bad_pointer=1` |
| anchor-mismatch | first row → `PROVINCE.md:1` (line 1 lacks the basename) | MET | MISS | `pointer_anchor=1` |
| ledger-copy-alias | ledger bytes copied to `quality/ledger-copy.md`, all 82 rows point at the copy | MET | MISS | `self_pointer=82 (content_alias)` |
| ledger-symlink | `quality/ledger-symlink.md -> tool-ledger.md`, all rows point at the link | MISS | MISS | `self_pointer=82` (+`bad_pointer=82`) |
| no-work-control | committed `c1-do-nothing.md` as the ledger | MISS | MISS | `uncovered=81 dup=1 bad_pointer=1` |

Exact candidate summary lines (all `rc` captured; MISS lines omitted here only for width — they
are byte-identical except the named field):

```
all-self           rc=1  C1_R53: population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0 empty_desc=0 desc_repeat=0 desc_unsupported=0 self_pointer=82 bad_pointer=0 pointer_anchor=0 selftest=ok verdict=TARGET_MISSED
laundered-self     rc=1  C1_R53: population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0 empty_desc=0 desc_repeat=0 desc_unsupported=0 self_pointer=82 bad_pointer=0 pointer_anchor=0 selftest=ok verdict=TARGET_MISSED
generic-repeat     rc=1  C1_R53: population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0 empty_desc=0 desc_repeat=82 desc_unsupported=81 self_pointer=0 bad_pointer=0 pointer_anchor=0 selftest=ok verdict=TARGET_MISSED
generic-unique     rc=1  C1_R53: population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0 empty_desc=0 desc_repeat=0 desc_unsupported=82 self_pointer=0 bad_pointer=0 pointer_anchor=0 selftest=ok verdict=TARGET_MISSED
ledger-copy-alias  rc=1  C1_R53: population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0 empty_desc=0 desc_repeat=0 desc_unsupported=0 self_pointer=82 bad_pointer=0 pointer_anchor=0 selftest=ok verdict=TARGET_MISSED
ledger-symlink     rc=1  C1_R53: population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0 empty_desc=0 desc_repeat=0 desc_unsupported=0 self_pointer=82 bad_pointer=82 pointer_anchor=0 selftest=ok verdict=TARGET_MISSED
anchor-mismatch    rc=1  C1_R53: population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0 empty_desc=0 desc_repeat=0 desc_unsupported=0 self_pointer=0 bad_pointer=0 pointer_anchor=1 selftest=ok verdict=TARGET_MISSED
dup-row            rc=1  C1_R53: population=82 ledger_rows=83 uncovered=0 dangling=0 dup=1 empty_desc=0 desc_repeat=0 desc_unsupported=0 self_pointer=0 bad_pointer=0 pointer_anchor=0 selftest=ok verdict=TARGET_MISSED
dangling-row       rc=1  C1_R53: population=82 ledger_rows=83 uncovered=0 dangling=1 dup=0 empty_desc=0 desc_repeat=0 desc_unsupported=0 self_pointer=0 bad_pointer=0 pointer_anchor=0 selftest=ok verdict=TARGET_MISSED
bad-pointer        rc=1  C1_R53: population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0 empty_desc=0 desc_repeat=0 desc_unsupported=0 self_pointer=0 bad_pointer=1 pointer_anchor=0 selftest=ok verdict=TARGET_MISSED
no-work-control    rc=1  C1_R53: population=82 ledger_rows=2 uncovered=81 dangling=0 dup=1 empty_desc=0 desc_repeat=0 desc_unsupported=1 self_pointer=0 bad_pointer=1 pointer_anchor=0 selftest=ok verdict=TARGET_MISSED
```

### 4.1 What this licenses, and what it does not

- `[OBS]` The frozen C1 discrimination is mechanically achievable with named, isolated clauses on
  this ledger: production MET, no-work control MISS, and every forgery MISS for its own clause.
- `[OBS]` Two bypasses beyond the r52 report are measurable at the base: an `:line` anchor that
  does not name the instrument (`anchor-mismatch`), and a byte-identical ledger copy at another
  path (`ledger-copy-alias`); both pass r51 and fail only the new clauses.
- `[INF]` The committed r53 counter is absent at base (`git ls-tree -r --name-only
  ad4bf205… quality/counters | grep -ci r53` → 0), so the claim's target sentence is still an
  acceptance test, not an observed result of the committed instrument. This seat's candidate is
  not that instrument.
- **Residuals** (unchanged by the candidate): (a) `desc_unsupported` is a token-overlap heuristic;
  a description that paraphrases in vocabulary absent from the file is rejected although a human
  would accept it, and a description that copies the file's header prose passes although it may be
  generic — the clause measures “read from the instrument”, not “accountable”; (b) “non-self” is
  not “instrument-relevant”: 82 rows pointing at one legitimate document that contains all
  basenames would pass every pointer clause; (c) the population is derived from the tree, so a
  newly added instrument passes only after a ledger row exists — coverage is exact but does not
  prove the row was written by a human; (d) the `ledger-symlink` arm co-fires `self_pointer` and
  `bad_pointer`, so it is not an isolating control; the `generic-repeat` arm co-fires
  `desc_repeat` and `desc_unsupported`. Isolating arms exist for both (`ledger-copy-alias`,
  `generic-unique`).

## 5. C2 before-state — the committed r52 entry against its own pinned bytes [OBS]

Instrument: `r53-c2-bindings.py --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md
--fetch .ufo/waves/round-52/fetch --sources corpus/SOURCES.md`. It parses the entry's proposition
table (`.ufo`-free path), resolves each `S###` in `corpus/SOURCES.md:320-323`, verifies
`SHA256SUMS` (`sha256sum -c` on the same root: 5/5 OK), and opens the pinned fetch bytes.

```
### old rc=1
C2_R53_FAIL: P16 quote_verbatim not_contiguous_in_file
C2_R53_FAIL: P16 quote_at_pin ranges=[(1554, 1558), (1576, 1576)]
C2_R53_FAIL: P17 symbol_scope token=sendshortcut spans=[(531, 589)] pin=[(619, 622)]
C2_R53_FAIL: P18 containment claim='inside the scan' loops=[(565, 571)] pin=[(574, 574)]
C2_R53: props=18 row_bound=18 pin_bound=18 row_scope=18 quote_words=18 quote_verbatim=17 \
quote_at_pin=17 symbol_scope=17 containment=17 support=18 checksums=ok \
failed=quote_verbatim,quote_at_pin,symbol_scope,containment verdict=TARGET_MISSED
```

[OBS] The committed entry (sha256 `bee0d14379eb560595c5d2237ffc9fd0f6d61c3b6b728fbb0dab851687ecb078`)
has 18 propositions; 17 bind row/pin/quote/scope/word-count/support, and exactly the three routed
defects fail, each under a distinct clause:

- **P16** (`corpus/knowledge/hyprland-synthetic-dispatch-r52.md:28`) joins `ConfigActions.cpp:1554`
  and `:1558` with an elision, so its quote is not a contiguous substring anywhere in the pinned
  file and not inside the pin span.
- **P17** (`:29`) attributes the repeat branch to `sendshortcut` (span `:531-589`) while the pin
  `:619-622` lies inside `sendkeystate` (`:591-627`).
- **P18** (`:30`) says the `key not found` return is “inside the scan”; the scan loop is
  `:565-571`, the return is `:574`.

## 6. C2 repair fixture — old bytes rejected, corrected bytes accepted [OBS]

The corrected fixture changes exactly the three rows (derived from the pinned bytes; the quote is
the full contiguous passage, 16 words):

```
| P16 | The action sends the modifier state before delivering the key, and the delivery is selected by the borrowed pass field. | S371 | Hyprland-ConfigActions.cpp:1554-1558 | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` | direct | The modifier call precedes the pass-selected delivery call inside one contiguous passage. |
| P17 | `sendkeystate`'s repeat branch invokes its delegate twice when the repeat state is set and the first call succeeded. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:619-622 | `if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` | direct | The second delegate call is inside `sendkeystate`, guarded by repeat and success. |
| P18 | After the keymap scan closes, the cache-miss branch returns the `key not found` error. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:574 | `return {.success = false, .error = "sendshortcut: key not found"};` | direct | The return follows the scan loop's closing brace at 571, inside the cache-miss branch. |
```

```
### fixed rc=0
C2_R53: props=18 row_bound=18 pin_bound=18 row_scope=18 quote_words=18 quote_verbatim=18 \
quote_at_pin=18 symbol_scope=18 containment=18 support=18 checksums=ok failed=- verdict=TARGET_MET
```

Single-clause mutants, each derived from the corrected fixture:

```
### m1-fabricated-quote rc=1  failed=quote_verbatim,quote_at_pin     (P01 quote invented at a real pin)
### m2-long-quote       rc=1  failed=quote_words                      (P16 quote 65 words, contiguous at pin)
### m3-wrong-row        rc=1  failed=row_bound,row_scope              (P05 → S379, absent)
### m4-wrong-pin        rc=1  failed=quote_at_pin                     (P01 pin 620-626 inside S370, quote absent)
### m5-symbol-swap      rc=1  failed=symbol_scope                     (P04 subject → `sendshortcut`)
### m6-row-scope        rc=1  failed=row_scope                        (P01 row → S371, range 1530-1616)
```

Exact per-mutant summary lines:

```
m1  C2_R53_FAIL: P01 quote_verbatim not_contiguous_in_file / C2_R53_FAIL: P01 quote_at_pin ranges=[(591, 594)]
    C2_R53: props=18 row_bound=18 pin_bound=18 row_scope=18 quote_words=18 quote_verbatim=17 quote_at_pin=17 symbol_scope=18 containment=18 support=18 checksums=ok failed=quote_verbatim,quote_at_pin verdict=TARGET_MISSED
m2  C2_R53_FAIL: P16 quote_words words=65
    C2_R53: props=18 row_bound=18 pin_bound=18 row_scope=18 quote_words=17 quote_verbatim=18 quote_at_pin=18 symbol_scope=18 containment=18 support=18 checksums=ok failed=quote_words verdict=TARGET_MISSED
m3  C2_R53_FAIL: P05 row_bound row=S379 absent / C2_R53_FAIL: P05 row_scope no_declared_range
    C2_R53: props=18 row_bound=17 pin_bound=18 row_scope=17 quote_words=18 quote_verbatim=18 quote_at_pin=18 symbol_scope=18 containment=18 support=18 checksums=ok failed=row_bound,row_scope verdict=TARGET_MISSED
m4  C2_R53_FAIL: P01 quote_at_pin ranges=[(620, 626)]
    C2_R53: props=18 row_bound=18 pin_bound=18 row_scope=18 quote_words=18 quote_verbatim=18 quote_at_pin=17 symbol_scope=18 containment=18 support=18 checksums=ok failed=quote_at_pin verdict=TARGET_MISSED
m5  C2_R53_FAIL: P04 symbol_scope token=sendshortcut spans=[(531, 589)] pin=[(619, 622)]
    C2_R53: props=18 row_bound=18 pin_bound=18 row_scope=18 quote_words=18 quote_verbatim=18 quote_at_pin=18 symbol_scope=17 containment=18 support=18 checksums=ok failed=symbol_scope verdict=TARGET_MISSED
m6  C2_R53_FAIL: P01 row_scope ranges=[(591, 594)] declared=(1530, 1616)
    C2_R53: props=18 row_bound=18 pin_bound=18 row_scope=17 quote_words=18 quote_verbatim=18 quote_at_pin=18 symbol_scope=18 containment=18 support=18 checksums=ok failed=row_scope verdict=TARGET_MISSED
```

### 6.1 Why no committed instrument can produce this today [OBS]

- `git ls-tree -r --name-only ad4bf205… quality/counters/ | grep -ci r52` → `0`; the r52 “landed
  counter” named in `.ufo/waves/round-52/w2/Attack07.md` is a working-tree artifact, never
  committed.
- The only committed dispatcher-entry counter, `quality/counters/c2-r51-dispatch-entry.py`, is
  hard-wired to the r51 slug and r51 fetch root (its docstring, `:5-27`); at the base it prints
  `C2_R51: clauses=abcd clauses_met=4 admitted=1/1 verdict=TARGET_MET rev=ad4bf205…` [OBS] — it
  does not read the r52 entry at all.
- The tracked `.ufo/waves/round-52/validate/corpus/knowledge/hyprland-synthetic-dispatch-r52.md`
  is **byte-identical** to the committed entry (sha256 `bee0d143…ecb078`; `diff` of rows P11-P18:
  identical). It is not a corrected draft.

## 7. Sources opened this round (URL, date, located quote)

No network fetch was made; the bytes opened are the committed round-52 fetch copies under
`.ufo/waves/round-52/fetch/`, sha256-verified against `SHA256SUMS` (5/5 OK). Registry rows:
`corpus/SOURCES.md:320-323`, opened 2026-10-27, revision
`efb50993780079460b0cbed1363e2166a2de1d9f`.

- S371 — `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/shared/actions/ConfigActions.cpp`
  (code, tier A, access date 2026-10-27). Located: `:1554`
  `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);`; `:1556` `if (S.m_passPressed == 1) {`;
  `:1558` `g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);`;
  `:1576` `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);`.
- S370 — `https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp`
  (access date 2026-10-27). Located: `:531` `static SDispatchResult sendshortcut(const std::string& args) {`;
  `:589` its closing `}`; `:591` `static SDispatchResult sendkeystate(const std::string& args) {`;
  `:565-571` the `for (xkb_keycode_t kc = …) { … }` scan; `:574`
  `return {.success = false, .error = "sendshortcut: key not found"};`; `:619` `auto result = sendshortcut(modifiedArgs);`;
  `:621-622` `if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);`;
  `:627` closing `}`.
- S372 — `…/src/config/shared/actions/ConfigActions.hpp` (access date 2026-10-27), `:117`
  `uint32_t m_timeLastMs = 0;  // timestamp of last key/mouse event`.
- S373 — `…/src/managers/KeybindManager.cpp` (access date 2026-10-27), `:221`
  `uint32_t CKeybindManager::stringToModMask(std::string mods) {`, `:223-224` the `::toupper`
  transform and `if (mods.contains("SHIFT"))`.

These quotes are the pinned bytes; utterance of them is a source-truth claim only insofar as the
fetch checksums hold. The independent reviewer arm required by C2 remains outside this seat.

## 8. Boundaries, safety, cleanup

- Writes: this report only. No tracked lane file, fleet file, state/watchdog, scripts/templates or
  shukuknow write; `git status --porcelain` at the lane is `?? .ufo/waves/round-53/` throughout.
- No git/jj mutation in the lane; the only repositories created are scratch fixtures, each commit
  guarded by `git rev-parse --show-toplevel` printing the fixture path.
- No live read, package query, producer execution, screenshot, input capture, compositor/host
  mutation or network fetch; the remote URLs above are registry text, not fetches this round.
- No LSP device was mounted in this environment; symbol reasoning used regex/brace-span analysis
  over the pinned bytes, which is recorded as a ceiling (§4.1, §6).
- Scratch `/fast/scratch/hyaku/mado-r53/R53Five46` (69 MB at peak; `/fast` 594 GB free) deleted
  before yield; no `/tmp` usage beyond the tool default, no background jobs, no task/agent calls,
  no tool installs.

## 9. What the parent can apply

1. C1: the clause set in §4 is a concrete, clause-attributed acceptance test; the committed
   counter must reproduce MET on `ad4bf205…:quality/tool-ledger.md` and MISS on
   `all-self`, `laundered-self`, `generic-repeat`, `generic-unique`, `anchor-mismatch`,
   `ledger-copy-alias`, `dup-row`, `dangling-row`, `bad-pointer`, `pointer_anchor`,
   `no-work-control` — with the deciding field named in the receipt (QUALITY 56/57).
2. C2: the corrected P16/P17/P18 rows in §6 are derived from pinned bytes and pass the binding
   checker; the committed counter must return MISS on the committed entry
   (`bee0d143…`) for the three named clauses and MET on the corrected fixture, while an
   independent reviewer still owns entailment. Note the repair drops P16’s “then clears the
   modifier state” clause rather than binding it: the clear at `ConfigActions.cpp:1576` is outside
   the contiguous 1554-1558 passage, so an entry that keeps that fact needs its own row.
3. Both items stay provisional absent the committed instruments; no axis score is claimed here.

Report: .ufo/waves/round-53/w1/R53Five46.md
