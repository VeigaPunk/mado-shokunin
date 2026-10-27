# R53One5 — C1 instrument-ledger accountability counter, C2 proposition-grounding repair (evidence prose)

Seat `R53One5` (scribe, leaf — no dispatch). Round 53, wave w1. Lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin`. Base tip `ad4bf2059bcfafe63671d262222908ee1fe8001c`
(`git rev-parse HEAD` → that sha; `git status --porcelain` → `?? .ufo/waves/round-53/` only).
Axes named: **operability** (C1) and **coverage** (C2). No score, admission or axis move is
claimed here; this seat drafts evidence and lesson prose only.

Tag legend for this report: `[OBS]` = a command I ran in this seat and whose output is quoted
below; `[OBS-r52]` = bytes of a committed round-52 receipt I read (not re-executed by me);
`[INF]` = composite inference over measured parts; `[UNK]` = not measured. Frozen claim text is
quoted from `.ufo/waves/round-53/claims-frozen.md`; only the blockquote markers and the bold
emphasis on the two headings are added, the words are verbatim.

Fence as executed: no lane tracked edit, no git/jj mutation or commit, no task/subagent/background
job, no live read, no package query, no process/compositor probe, no screenshot, no input capture,
no producer execution, no network fetch. Scratch was `/fast/scratch/hyaku/mado-r53/R53One5`
(explicit paths; cleaned before yield). No new source was opened; the only source bytes read are
the already-pinned r52 `fetch/` blobs, whose sha256 I re-verified. All writes in this seat: this
report, plus throwaway drivers under the scratch dir listed at the end.

## Attacked predicates (verbatim)

> **C1 — operability: instrument-ledger accountability counter**
>
> Before: r51 counter accepts repeated generic descriptions and ledger self-pointers; r52 verifier
> reproduced bypasses. Target: a newly committed, scratch-aware counter with explicit selftest
> returns TARGET_MET on the production ledger, TARGET_MISSED on a no-work control and each frozen
> forgery fixture, with exact population coverage and non-self pointers. This is a bounded
> structural accountability check, not semantic proof. No capability admitted unless the final
> committed demonstration and controls pass.

> **C2 — coverage: repair proposition-grounding defects in the indexed r52 dispatcher entry**
>
> Before: r52 verifier found P16 quote spliced, P17 misattributed, P18 mislocalized; no valid r52
> admission counter. Target: append-only correction clearly repairs those three propositions
> against opened pinned source bytes; a frozen counter rejects the old bytes and accepts corrected
> entry with quote/pin/proposition bindings; independent reviewer checks source truth. No claim of
> expansion credit unless an admitted entry rests on a source row opened this round and uncovered
> ground per coverage map.

> C1 and C2 are causally separate; no exploratory claim. Control design and measurement must be
> frozen before data. No axis harm admissible.

---

## 1. C1 — what the incumbent counter measures, and the two bypasses it admits

### 1.1 The instrument under test

`quality/counters/c1-r51-ledger.py` (19,094 B, 445 lines) is the only committed ledger counter at
the base tip: `git ls-tree -r --name-only ad4bf205… -- quality | grep -ci r52` → `0`. Its own
measurement is: population = every file under `tools/` + direct children `quality/*.py` +
`quality/counters/*.py` at `--rev`; each population file must have exactly one 3-cell row with a
non-placeholder description and a pointer token naming an existing repo file whose bytes contain
the row file's basename.

Production run at the frozen base tip `[OBS]`:

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --rev ad4bf2059bcfafe63671d262222908ee1fe8001c \
    --work /fast/scratch/hyaku/mado-r53/R53One5/c1/work
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=ad4bf2059bcfafe63671d262222908ee1fe8001c)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
EXIT=0
```

Exact population arithmetic at the same rev `[OBS]` (`git ls-tree -r --name-only <rev>` filtered
by the counter's own predicate):

```
tools 17
quality_root_py 19
quality_counters_py 46
total 82
```

So "exact population coverage" is already 82/82 and is not the open gap.

### 1.2 The CLI surface: no counter selftest, no ledger override

```
$ python3 -I quality/counters/c1-r51-ledger.py --help
usage: c1-r51-ledger.py [-h] [--repo REPO] --rev REV [--work WORK] [--checker CHECKER]
options: -h, --help  --repo REPO  --rev REV  --work WORK  --checker CHECKER
```

`argparse` declarations are exactly those four (`c1-r51-ledger.py:358-361`). There is **no**
`--selftest` of the counter itself: `selftest_rc`/`selftest_state` in `main` refer only to the
gateway checker's `--selftest` (`:278-300`, `:394-403`). The frozen C1 target's "explicit
selftest" is therefore absent, and so is any `--ledger` override that would let a caller point the
counter at a control or forgery fixture without constructing a git revision — the r52 attack seats
had to build throwaway git fixtures for exactly that reason (`Attack20.md` §A1–§A9).

Scratch handling is half-present `[OBS]`: default `--work` is `tempfile.mkdtemp(prefix="c1-r51-",
dir=TMPDIR)` (`:331-336`) — i.e. `/tmp` unless the caller overrides — and `REFUSED_ROOTS`
(`:68`) is consulted only to print a hint after a checker selftest failure (`:404-407`), never to
refuse a work root. Child processes are sandboxed (`HOME`/`TMPDIR`/`XDG_*` under `--work`,
`:251-270`) and the clone plus created work dir are removed on exit (`:434-441`), so containment
is real but opt-in.

### 1.3 Bypass 1 — a ledger self-pointer resolves for every row

`pointer_resolves()` (`:196-207`) accepts any token that is a file at `--rev` **whose bytes
contain the row file's basename**. `quality/tool-ledger.md` is itself a file in the tree and its
table contains every population basename, so `quality/tool-ledger.md` is a valid pointer for
every row. Independent exercise of the counter's own function, no git fixture, ledger bytes read
from the production file `[OBS]` (excerpt of one run; the complete six-line output is quoted in
§1.5):

```
$ python3 -I /fast/scratch/hyaku/mado-r53/R53One5/c1/drive_bypass.py
HOLE1_pointer_resolves path=tools/mado-binds.py pointer=quality/tool-ledger.md -> True
HOLE1_token_in_files=True basename_in_ledger_bytes=True
```

### 1.4 Bypass 2 — repeated generic descriptions pass the description gate

The description gate is emptiness only (`:230-232`): `PLACEHOLDER = re.compile(r"^[\s\-–—_*`.]+$")`
(`:76`). Any sentence passes; the same sentence may be used for every row — there is no
uniqueness, length or instrument-context check anywhere in the file. Sweep `[OBS]`:
`grep -c desc quality/counters/c1-r51-ledger.py` → `18`, and every occurrence is a docstring line,
the parse cell (`:171`), the emptiness test (`:229-232`), the tally key, or an output field — no
comparison between descriptions exists.

### 1.5 The two holes together, at full population

A full-population, grammar-valid, duplicate-free ledger whose every description is the same
generic sentence and whose every pointer is the ledger itself, scored by the counter's own
`parse_rows` + `describe` + the `clean` predicate from `main` (`:415-417`) `[OBS]` — complete
output of the run whose first two lines appear in §1.3:

```
$ python3 -I /fast/scratch/hyaku/mado-r53/R53One5/c1/drive_bypass.py
HOLE1_pointer_resolves path=tools/mado-binds.py pointer=quality/tool-ledger.md -> True
HOLE1_token_in_files=True basename_in_ledger_bytes=True
HOLE2_placeholder_match=None desc='Generic accountability pointer to this ledger itself.'
SYNTHETIC rows_same_desc=82 rows_same_pointer=82 unique_desc=1 unique_pointer=1
SYNTHETIC fields population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 dup=0 clean=True verdict=TARGET_MET
SYNTHETIC details=0
```

Limit of this measurement `[OBS]`: `describe`'s git reader was stubbed to return the real
production ledger bytes for the one token `quality/tool-ledger.md`; the counter's own parsing,
token filter and tally logic ran unmodified. The end-to-end form (real git fixture, all three
gates) is recorded in the committed r52 receipt `[OBS-r52]`
`.ufo/waves/round-52/w2/Attack20/receipts/isored-r51.out`:

```
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=9a6cefa4f6fef39d3cffa068137ab952bb276192)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET rev=9a6cefa4f6fef39d3cffa068137ab952bb276192
```

Attack20 §A9 describes that fixture (`9a6cefa4…`) as all 82 population rows, unique synthetic
descriptions, every pointer `quality/tool-ledger.md`, and records that the committed gate
`quality/check-tool-ledger.py` also exits 0 `TARGET_MET` on it (`receipts/isored-chk.out`). Both
incumbent instruments therefore pass a no-work ledger; the frozen `controls/c1-do-nothing.md`
fails them only through row shape, duplication and coverage (`Attack20.md` §A1–§A3), not through
either defect the r53 claim names.

### 1.6 Production-compatibility constraints a C1 replacement inherits

Measured on the production ledger at base tip `[OBS]` (counter's own `parse_rows`, production
bytes):

```
rows 82 unique_desc 82 dup_desc_groups 0
unique_pointer_cells 69 shared 10 max_share 4
x4 '`PROVINCE.md:20`'   x3 '`.ufo/waves/round-51/registration.md`'   x2 '`SCORECARD.md:2370`'
self_rows 0
```

Consequences, stated as compatible versus incompatible design moves (production measurements are
`[OBS]`; each clause's effect on them is `[INF]` from those measurements):

| Candidate clause | Production effect | Evidence |
|---|---|---|
| description must be unique per row | stays green (82/82 unique) | measurement above |
| pointer must not name the ledger or the row's own path | stays green (0 self rows) | measurement above; `grep -n tool-ledger.md quality/tool-ledger.md` → one prose mention at `:3`, no row |
| pointer cell must be unique per row | **breaks production** (10 shared pointer cells, max 4) | measurement above |
| description must share a phrase with the instrument's bytes (r52 draft's context test) | green on production, but 2 of 26 honest reader descriptions were falsely rejected in r52 (`Attack06.md` §A1/§A2: `generic_desc=1 verdict=TARGET_MISSED`, exit 1) | `[OBS-r52]` `w2/Attack06.md:75-143` |

The last row is the design warning I would put in front of the C1 author: a lexical
"instrument-context" signal is neither necessary nor sufficient (`Attack06.md` §A4 — forged
`PRED-C1-r47 does things.` accepted, honest ledger-gate description rejected, same counter, same
revision). The frozen C1 target asks for "non-self pointers" and "exact population coverage", not
for a prose-entailment test; a replacement that only adds non-self resolution, description
distinctness and a counter `--selftest` satisfies the frozen sentence without inheriting that
false-positive surface.

### 1.7 What C1 still needs (not measured here — no counter was built)

A discriminating pair is now specified by measurement, not assumption:

- green: production ledger at `ad4bf205…` — 82/82, the run in §1.1.
- red: full-population no-work ledger — §1.5's shape (grammar-valid, dup-free, all-generic,
  all-self). The r52 frozen control is **not** an isolating red: `controls/c1-do-nothing.md` is
  two rows with four cells each (`cat` shows `| tools/mado-verify.sh | quality/tool-ledger.md
  (commentary only) | nothing | generic accountability pointer to this ledger itself |` twice), so
  shape/coverage fire first (`Attack20.md` §A1–§A3).
- selftest: must exercise the counter on both sides without a caller-built git fixture, or the
  red arm stays expensive and outside the counter's own proof.

I did not build, run or score any round-53 counter. No operability capability is asserted.

---

## 2. C2 — the three proposition defects, re-measured against the pinned bytes

### 2.1 Provenance first

| Input | Anchor | Result |
|---|---|---|
| Entry bytes | `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` at `ad4bf205…` | `git show <rev>:<path> \| sha256sum` = `bee0d14379eb560595c5d2237ffc9fd0f6d61c3b6b728fbb0dab851687ecb078`; work-tree sha256 identical `[OBS]` |
| Pin integrity | `.ufo/waves/round-52/fetch/SHA256SUMS` | `sha256sum -c` → 5 × `OK`, exit 0 `[OBS]` |
| Registry rows | `corpus/SOURCES.md:320-323` (S370–S373) | each row's `fetch SHA256` equals the file it pins: S370 `7248cbb8…`, S371 `a83abeb5…`, S372 `746c6f51…`, S373 `8d8f35fc…` `[OBS]` |
| No r52 counter | `git ls-tree -r --name-only ad4bf205… -- quality` | zero `r52` matches; last counters are `c2-r51-dispatch-entry.py` and c3/c4 `[OBS]` |
| Pins opened | SOURCES rows say `opened 2026-10-27`, `recheck on-release`; entry line 32 names revision `efb50993780079460b0cbed1363e2166a2de1d9f` | `[OBS]` |

No source was fetched or newly opened by this seat. The witness files are the four r52 `fetch/`
blobs; their URLs are the S370/S371 rows (`raw.githubusercontent.com/hyprwm/Hyprland/
efb50993780079460b0cbed1363e2166a2de1d9f/src/config/legacy/DispatcherTranslator.cpp` and
`.../src/config/shared/actions/ConfigActions.cpp`), opened 2026-10-27.

### 2.2 Reproduction (my own run, entry table and pins read-only)

Driver: whitespace-collapse the entry's quote and the pin; test the quote against the whole file
and against the declared anchor ranges (multi-range locators split on `,`); find the enclosing
`static SDispatchResult <name>(` by brace matching `[OBS]`:

```
$ python3 -I /fast/scratch/hyaku/mado-r53/R53One5/c2/verify_p16_p18.py
ENTRY rows=18 ids=P01,P02,P03,P04,P05,P06,P07,P08,P09,P10,P11,P12,P13,P14,P15,P16,P17,P18
P04 pin=Hyprland-legacy-DispatcherTranslator.cpp span=619-622 words=13 quote_in_pin_file=True quote_in_anchor_range=True anchor_function=sendkeystate(591-627)
P16 pin=Hyprland-ConfigActions.cpp span=1554-1558,1576 words=9 quote_in_pin_file=False quote_in_anchor_range=False anchor_function=None(None-None)
   fragments: first=1554 last=1568
   intervening_bytes='g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED); else g_pSeatManag'
P17 pin=Hyprland-legacy-DispatcherTranslator.cpp span=619-622 words=9 quote_in_pin_file=True quote_in_anchor_range=True anchor_function=sendkeystate(591-627)
P18 pin=Hyprland-legacy-DispatcherTranslator.cpp span=574 words=10 quote_in_pin_file=True quote_in_anchor_range=True anchor_function=sendshortcut(531-589)
P04_RECHECK span=619-622 quote_in_anchor_range=True words=13
```

(The driver truncates its `intervening_bytes` field at 200 characters; the quoted prefix is
byte-exact, the elision is the driver's, not the pin's.)

**P16 — spliced quote, and the locator itself is non-contiguous.** The entry cites
`Hyprland-ConfigActions.cpp:1554-1558,1576` with the quote
`g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);`.
The two calls sit at `:1554` and `:1558`; between them the pin has
`:1556 if (S.m_passPressed == 1) { if (!isMouse)`. The space-joined quote occurs nowhere in the
pin (`quote_in_pin_file=False`) and nowhere in either declared range
(`quote_in_anchor_range=False`). The elided guard is material: the press at `:1558` runs only when
`m_passPressed == 1` and the key is not a mouse button; the `else` at `:1559-1560` sends a pointer
button instead. A multi-range locator (`1554-1558,1576`) cannot bind one contiguous "located
quote" by construction — both the quote text and the locator shape need repair.

**P17 — quote binds, subject is the wrong function.** The quote is contiguous at its declared
`619-622`, but the enclosing function there is `sendkeystate` (`:591-627`);
`sendshortcut` spans `:531-589` and contains no `keyState`/repeat logic (grep of the pin:
`sendshortcut` def at `:531`, `sendkeystate` def at `:591`, the double call at `:619` and `:622`).
The landed proposition says "`sendshortcut`'s repeat branch" — false about the owner. P04 states
the same fact correctly and its quote also binds at `619-622` (`P04_RECHECK` above), so P17 is a
duplicate as well as a misattribution.

**P18 — quote binds, localization is false.** The return at `:574` is
`return {.success = false, .error = "sendshortcut: key not found"};` — the quote is right and the
anchor is right, but "inside the scan" is wrong. Measured indentation and structure `[OBS]` (the
tail of the `verify_corrections.py` run; its first five lines are quoted in §2.3):

```
DT:565 indent=12 'for (xkb_keycode_t kc = keycode_min; kc <= keycode_max; ++kc) {'
DT:566 indent=16 'xkb_keysym_t sym = xkb_state_key_get_one_sym(ks, kc);'
DT:568 indent=20 'keycode                                            = kc;'
DT:571 indent=12 '}'
DT:573 indent=12 'if (!keycode)'
DT:574 indent=16 'return {.success = false, .error = "sendshortcut: key not found"};'
```

The loop closes at `:571`; `:573-574` sit at the same indent as the `for` statement, inside the
cache-miss branch, so the return executes **after** the scan leaves `keycode` zero, not inside the
scan body.

### 2.3 Draft append-only correction (proposed; NOT applied)

The lane's rule is append-only (`SKILL.md` "Errata append-only; rejections kept"), so the table
rows stay in place and a correction block is appended at the end of
`corpus/knowledge/hyprland-synthetic-dispatch-r52.md` (32 lines today). Proposed block, with every
quote re-verified in this seat (`verify_corrections.py` output below):

```markdown
## Erratum (round 53, 2026-10-27) — P16, P17, P18 withdrawn and replaced

withdrawn: P16, P17, P18 above. Replaced by P16a/P16b/P16c/P17R/P18R below; the earlier rows stay
as rejected history and are not part of the effective proposition set.

The landed P16 quote elided a guard and its locator was non-contiguous (`:1554-1558,1576`); P17
named `sendshortcut` for a branch inside `sendkeystate`; P18 read the `:574` return as inside the
scan loop. Each replacement quote below is a contiguous whitespace-collapsed span inside its own
single-range anchor in the pinned bytes, re-checked 2026-10-27.

| ID | Proposition | Source row | Pin:anchor | Quote (<=25 words) | Support class | Why it supports |
|---|---|---|---|---|---|---|
| P16a | `Actions::pass` emits modifier state before the guarded key/pointer delivery block. | S371 | Hyprland-ConfigActions.cpp:1554 | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` | direct | The call precedes the block opened at :1556 (positional). |
| P16b | The key-press call at :1558 runs only inside the `m_passPressed == 1` branch and only when `!isMouse`. | S371 | Hyprland-ConfigActions.cpp:1556-1558 | `if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` | direct | Guard and call are contiguous; the landed P16 quote elided exactly this guard. |
| P16c | `Actions::pass` clears modifier state after the delivery block (block closed at :1574). | S371 | Hyprland-ConfigActions.cpp:1576 | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` | direct | The clearing call follows the block; locator is the one line. |
| P17R | `sendkeystate`'s repeat branch calls its delegate twice only when the first call succeeded; `sendshortcut` (:531-589) has no repeat branch. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:621-622 | `if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` | direct (function-span ownership); same fact as P04 — count once | Anchor lies inside `sendkeystate` (:591-627); the landed row named the wrong function. |
| P18R | If the scan (loop :565-571) leaves `keycode` zero, the cache-miss branch returns the `key not found` error at :574. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:573-574 | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` | direct | Return is guarded by `!keycode` and sits outside the loop body; the landed row localized it inside the scan. |
```

Verification of those five quotes `[OBS]` (first five lines of the `verify_corrections.py` run;
the six `DT:` indentation lines are quoted in §2.2):

```
$ python3 -I /fast/scratch/hyaku/mado-r53/R53One5/c2/verify_corrections.py
P16a pin=Hyprland-ConfigActions.cpp spans=[(1554, 1554)] words=4 binds_in_anchor=True enclosing=None(None-None)
P16b pin=Hyprland-ConfigActions.cpp spans=[(1556, 1558)] words=12 binds_in_anchor=True enclosing=None(None-None)
P16c pin=Hyprland-ConfigActions.cpp spans=[(1576, 1576)] words=4 binds_in_anchor=True enclosing=None(None-None)
P17R pin=Hyprland-legacy-DispatcherTranslator.cpp spans=[(621, 622)] words=9 binds_in_anchor=True enclosing=sendkeystate(591-627)
P18R pin=Hyprland-legacy-DispatcherTranslator.cpp spans=[(573, 574)] words=12 binds_in_anchor=True enclosing=sendshortcut(531-589)
```

`enclosing=None` for the P16 rows is a property of the regex used for the span probe, not of the
pin: `:1554`/`:1556-1558`/`:1576` sit inside
`ActionResult Actions::pass(uint32_t modMask, uint32_t key, std::optional<PHLWINDOW> w)` opened at
`:1530` and closed at `:1599` (method definition, not a `static SDispatchResult` free function).
The same file's `Actions::sendKeyState` (`:1601-1618`, including its own repeat double-call at
`:1612-1613`) is a separate route and is not claimed here.

### 2.4 What a frozen C2 counter must be able to distinguish (measured discriminators)

| Discriminator | Old bytes | Corrected bytes |
|---|---|---|
| quote contiguous in its own anchor range | P16: `False` (whole file and anchor ranges) | all five rows: `True` |
| single-range locator | P16: `1554-1558,1576` (two ranges) | one range per row |
| anchor inside the function the proposition names | P17: anchor inside `sendkeystate`, proposition says `sendshortcut` | P17R names `sendkeystate`; anchor inside it |
| anchor inside the loop a containment claim names | P18: "inside the scan", anchor `:574` outside loop `:565-571` | P18R says "after the scan leaves `keycode` zero" and anchors `:573-574` |
| quote ≤25 words | the three rows I re-ran are 9, 9, 10 words; the r52 verifier measured max 19 across the table `[OBS-r52]` | 4, 12, 4, 9, 12 words (max 12) |
| pin integrity | `sha256sum -c` exit 0 | unchanged |

Integration constraint found while drafting, because the correction must be append-only: the old
rows remain in the file, so a counter that scans "the table" still sees the rejected bytes. The
`withdrawn:` line above is the machine-readable hook — the effective proposition set is the landed
rows minus the withdrawn IDs plus the replacement rows. A counter that does not key on such a line
cannot satisfy "rejects the old bytes and accepts corrected entry" in the same file. I did not
write such a counter; this is a draft constraint, not a claim.

### 2.5 Coverage / expansion credit

The correction rests on S370 (dispatcher) and S371 (ConfigActions) — rows opened 2026-10-27 in
round 52, already `mined` and already mapped in `corpus/README.md`. No source row was opened in
round 53, so under the frozen C2 sentence and CORPUS rule 4 ("expansion counts admitted
`knowledge/` entries whose `source:` cites a `mined` row on uncovered coverage-map ground") this
repair cannot carry round-53 expansion credit, even if a future counter admits it. The entry
remains unadmitted until a frozen counter passes **and** a non-author reviewer re-opens the quoted
bytes; I am neither.

---

## 3. Routed round-52 defects, inspected as evidence only

All four routed items in `corpus/lessons/round-52-verifier-spotcheck.md:69-74` were checked in the
bytes at base tip; nothing here upgrades them into findings of mine.

1. **Gate records absent for S370–S373.** `corpus/lessons/round-52.md` `## Gate` §C2 contains only
   the instruction "Record each source URL, access date and located quote <=25 words here once
   verified." and no records. CORPUS rule 1 (`CORPUS.md:113-116`) requires exactly those three
   fields per new row. Reproduced by reading both files `[OBS]`.
2. **Stale Changes note.** `corpus/lessons/round-52.md` `## Changes` reads, in full, "Pending final
   integration revisions and receipts." `[OBS]` — while the r52 verifier's own landing statement
   (read from that lesson, `[OBS-r52]`) records the entry, index row, S370–S373 and `fetch/` as
   committed at `56d6e70`. Both files are in the lane at base tip; the contradiction is between
   their words, and I did not re-run the landing check at `56d6e70`.
3. **QUALITY 17 distinct-scope review outstanding.** Criterion text at `corpus/QUALITY.md:34`
   requires an explicit overlapping-scope review for repeated canonical URLs; `corpus/SOURCES.md`
   round-52 search log (`:374`) states "S370, S371 and S373 reuse canonical URLs with new scopes;
   distinct-scope review remains outstanding." `[OBS]` — a warning-only census is explicitly not
   that review.
4. **The entry's own repair target** is §2 above; the verifier's wording at
   `corpus/lessons/round-52-verifier-spotcheck.md:74` matches my measurements.

Adjacent observation, out of C2 scope `[OBS]` for the bytes, `[INF]` for the rendering: the
entry's coverage-map row at `corpus/README.md:80` is preceded by a blank line at `:79` and
followed by a blank line at `:81`, while the table body ends at `:78` (the next content is `:82`
`## Quality bar`). Under CommonMark/GFM table rules the row therefore begins a new block with no
header, so it renders as text rather than a table member; the line is still present as an index
line, and I did not check whether the lane's own index scripts count it. I did not edit it.

## 4. Limits of this seat's evidence

- No git fixture was created (seat ban on commits); the full-population no-work ledger was scored
  through the counter's own functions with only the git reader stubbed, and the end-to-end form is
  cited from the committed r52 receipt, not re-executed.
- No round-53 counter exists to run; no admission, no axis score, no expansion credit is claimed.
- The r52 attack/verifier documents and receipts are read as bytes; their executions are
  `[OBS-r52]`, not this seat's runs.
- Only P16–P18 were re-derived. The other 15 landed propositions and the r52 critique's adjacent
  observations (P12 "null optional" wording, P04/P17 duplicate, quote-length ceiling) were read
  but not re-measured; they stay as routed evidence.
- The draft correction was not applied and is not in any tracked file.
- Scratch: `/fast/scratch/hyaku/mado-r53/R53One5/` held two drivers and one work dir; removed
  after this report. No `/tmp` path was used.

## 5. Evidence index (paths relative to the lane root; every lane path verified present at `ad4bf205…`; the fleet-root `CORPUS.md` row sits outside the lane revision)

| Path | Role |
|---|---|
| `quality/counters/c1-r51-ledger.py` | incumbent counter under test (`:76`, `:196-207`, `:230-232`, `:331-336`, `:358-361`, `:404-407`, `:415-417`) |
| `quality/tool-ledger.md` | production ledger (82 rows; 82 unique descriptions; 0 self rows; 10 shared pointer cells) |
| `quality/check-tool-ledger.py` | incumbent gate; passes the all-self ledger per r52 receipt |
| `.ufo/waves/round-52/controls/c1-do-nothing.md` | frozen r52 control (2 rows × 4 cells) |
| `.ufo/waves/round-52/w2/Attack20.md` + `receipts/isored-r51.out`, `isored-chk.out` | recorded r51/committed-gate bypass on a full-population no-work ledger |
| `.ufo/waves/round-52/w2/Attack06.md` | context-check false-positive ceiling (2/26 honest descriptions) |
| `.ufo/waves/round-52/fetch/{SHA256SUMS,Hyprland-ConfigActions.cpp,Hyprland-legacy-DispatcherTranslator.cpp}` | pins (`sha256sum -c` exit 0) |
| `corpus/knowledge/hyprland-synthetic-dispatch-r52.md` | landed entry, sha256 `bee0d143…` at rev |
| `corpus/SOURCES.md:320-323`, `:374` | S370–S373 rows and round-52 search log |
| `corpus/lessons/round-52.md` (`## Gate`, `## Changes`) | absent Gate records, stale Changes |
| `corpus/lessons/round-52-verifier-spotcheck.md:69-74` | routed defects |
| `corpus/QUALITY.md:34` | criterion 17 |
| `corpus/README.md:79-80` | blank line before the r52 coverage-map row |
| `CORPUS.md` (fleet root, read-only) `:113-116`, rule 4 | Gate-record contract and expansion rule |

Scratch drivers (ephemeral, deleted before yield): `/fast/scratch/hyaku/mado-r53/R53One5/c1/
drive_bypass.py`, `/fast/scratch/hyaku/mado-r53/R53One5/c2/{verify_p16_p18.py,verify_corrections.py}`.

## 6. Axis read (what this evidence moves, and what it does not)

- **operability (C1):** the before-state is now measured on the exact base tip and both bypasses
  are reproduced through the incumbent counter's own functions, with the production green run in
  the same report. This is groundwork for a r53 counter, not a move: no counter was committed or
  scored, so operability stays where the r52 verifier left it (unprovable until a committed
  counter passes production plus red fixtures).
- **coverage (C2):** the three defects are re-derived against pin bytes with contiguous-span
  checks, and a fully bound append-only replacement block is drafted and verified. Still no move:
  the entry is unedited, no counter scores it, and a non-author reviewer has not re-opened it.
  Repair credit requires those three, and expansion credit is barred in any case because no
  source row was opened this round.
- **no harm:** zero tracked files were written; every claim above is tagged to a command or to a
  committed receipt's bytes; the one adjacent defect surfaced (coverage-map row detached from its
  table by the blank line at `corpus/README.md:79`) is reported, not edited.

Report: `.ufo/waves/round-53/w1/R53One5.md`
