# R53Seven64 — independent bounded item 64: executable C1/C2 counter behavior

Seat: `R53Seven64` (leaf, executor). Base `ad4bf2059bcfafe63671d262222908ee1fe8001c` (HEAD, measured).
Axes attacked: **operability (C1)** and **coverage (C2)**, frozen at `.ufo/waves/round-53/claims-frozen.md:5-13`.
Scope: build and exercise scratch-only counters/fixtures for the declared claims; inspect routed r52
defects as evidence only; no tracked lane writes, no commits, no live reads, no fetches, no producer
execution. Scratch root `/fast/scratch/hyaku/mado-r53/R53Seven64` (removed before yield).

## 1. Attacked predicates (verbatim anchors)

- **C1** — `claims-frozen.md:7`: “a newly committed, scratch-aware counter with explicit selftest returns
  TARGET_MET on the production ledger, TARGET_MISSED on a no-work control and each frozen forgery
  fixture, with exact population coverage and non-self pointers. This is a bounded structural
  accountability check, not semantic proof.”
- **C2** — `claims-frozen.md:11`: “append-only correction clearly repairs those three propositions
  against opened pinned source bytes; a frozen counter rejects the old bytes and accepts corrected entry
  with quote/pin/proposition bindings; independent reviewer checks source truth.”

Both were attacked as *executable discrimination*, not as prose: on identical bytes, does the instrument
separate a conforming input from the named forgery classes, and does it name the defect?

## 2. What was built (scratch, not lane artifacts)

No round-53 C1/C2 counter, control set, or fixture exists in the lane at inspection: `.ufo/waves/round-53/`
holds only `claims-frozen.md`, `w1/`, `w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1.ready.dispatched`.
The committed ledger-accountability counter is `quality/counters/c1-r51-ledger.py` (with
`quality/check-tool-ledger.py` as its checker); the committed r52 entry is
`corpus/knowledge/hyprland-synthetic-dispatch-r52.md`. I therefore built two scratch instruments:

| scratch instrument | sha256 | role |
|---|---|---|
| `c1-ledger-accountability.py` | `11d5a6c924399b6ce92888eb6bf9c4293468a4cbbc8f235a8ec54853034d602f` | C1 candidate: population/row/description/pointer accountability with 20-case frozen selftest |
| `c2-proposition-bind.py` | `9a8d138c4db94e8ac7e34f46ff315f20ca0b8d091a3cfdf7bd3f32cb5869593a` | C2 candidate: proposition/row/pin/quote/subject/locator binding with 8-case frozen selftest |
| `corrected-entry.md` (fixture) | `81eddb28eb4289a41dc1f82b238fd74aa349b761d841643322d798267599773d` | r52 entry with only P16→P16a/P16b, P17, P18 repaired |

C1 discriminating rules (exact): population = every `tools/` file + direct `quality/*.py` +
`quality/counters/*.py` at the revision (`__pycache__`/`.pyc`/`.pyo` excluded); fenced blocks are
documentation; header/separator skipped; every other `|` line is a row, and a malformed first cell is
counted `dangling` rather than silently skipped (the r51 parser drops such lines: `c1-r51-ledger.py:155-176`).
Pointer tokens must normalize to an exact repo-relative path present at the revision, be a regular blob
(`120000` symlink rejected), not equal `quality/tool-ledger.md` and not equal the row's own instrument,
and the pointer bytes must name the row basename at a token boundary. **Any** self/symlink token in a
cell fails the row even beside a valid token. Descriptions must be ≥4 words, non-placeholder, not a
name/stem echo, not a frozen generic phrase, and unique after normalization across rows. Exact coverage
requires `ledger_rows == population` and `uncovered=dangling=dup=0`. `TARGET_MET` is impossible unless
the built-in selftest passes; `--work` inside the measured tree is refused before any directory is created.

C2 discriminating rules (exact): unique `P##[a-z]?` ids; cited `S###` must exist in `corpus/SOURCES.md` at
the revision and its used-by cell must name the entry; `file:anchor[,anchor]` must resolve in the pinned
byte file; the quote (4–25 whitespace words) must occur **contiguously inside a single cited span** after
whitespace collapse (concatenating spans or eliding lines inside a span is rejected); when the proposition
names a function defined in the pinned file, the anchor start must fall inside at least one such
brace-span; an “inside/in/within the scan|loop” assertion requires the anchor start inside a for/while/do
block; support class and a ≥3-word rationale are required.

## 3. C1 — measured behavior

### 3.1 Green control: production ledger at base tip

```
$ python3 -I c1-ledger-accountability.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --rev ad4bf2059bcfafe63671d262222908ee1fe8001c --work ./work-c1-green
C1_LEDGER: population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0 bad_pointer=0 empty_desc=0 \
generic_desc=0 self_pointer=0 symlink_pointer=0 selftest=20/20 verdict=TARGET_MET ledger=present \
rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
rc=0
```

The committed r51 instrument agrees on the same revision (so the green state is not a property of my
stricter rules): `C1_R51: population=82 ledger_rows=82 … verdict=TARGET_MET rev=ad4bf2059…`, rc 0.

### 3.2 No-work control: revision where the tracked ledger does not exist

```
$ python3 -I c1-ledger-accountability.py --repo …/mado-shokunin \
    --rev 6ca8c559a4a3d6d361101592116eea2bc7452437 --work ./work-c1-base
C1_LEDGER: population=79 ledger_rows=0 uncovered=79 dangling=0 dup=0 bad_pointer=0 empty_desc=0 \
generic_desc=0 self_pointer=0 symlink_pointer=0 selftest=20/20 verdict=TARGET_MISSED ledger=absent \
rev=6ca8c559a4a3d6d361101592116eea2bc7452437
C1_DETAIL: ledger=absent uncovered=79
rc=1
```

### 3.3 The committed r51 counter still accepts two named forgery classes (reproduced)

Fixture A (`/fast/scratch/hyaku/mado-r53/R53Seven64/fixture-bypass`, rev `ba96c5dc…`, scratch git identity,
`git rev-parse --show-toplevel` printed the fixture dir): row `tools/mado-action-plan.py` pointer replaced
with `` `quality/tool-ledger.md` ``; row `tools/mado-anims.py` description replaced with `Shared utility.`

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo ./fixture-bypass --rev ba96c5dcdd63bee6489e3e5acaca050c426b2225 --work ./work-r51
detail: checker selftest ok (ratio=50/50 form=with-work)
detail: checker ledger ok (rev=ba96c5dcdd63bee6489e3e5acaca050c426b2225)
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok \
verdict=TARGET_MET rev=ba96c5dcdd63bee6489e3e5acaca050c426b2225
rc=0
```

The same bytes under my counter:

```
C1_LEDGER: population=82 ledger_rows=82 uncovered=0 dangling=0 dup=0 bad_pointer=1 empty_desc=0 \
generic_desc=1 self_pointer=1 symlink_pointer=0 selftest=20/20 verdict=TARGET_MISSED ledger=present \
rev=ba96c5dcdd63bee6489e3e5acaca050c426b2225
C1_DETAIL: bad_pointer L32 path='tools/mado-action-plan.py' kinds=['self_ledger']
C1_DETAIL: generic_desc L33 path='tools/mado-anims.py'
rc=1
```

Fixture B (`fixture-symlink`, rev `8dacf016…`): `docs/alias` is a `120000` symlink to `../tools/mado-eventq.py`
used as that row's sole pointer, and row `tools/mado-monitors.py` points at `` `./PROVINCE.md:100` ``.

```
$ python3 -I quality/counters/c1-r51-ledger.py --repo ./fixture-symlink --rev 8dacf01649f286de3debf16f188ecc5cc7d89b25 --work ./work-r51b
C1_R51: population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok \
verdict=TARGET_MET rev=8dacf01649f286de3debf16f188ecc5cc7d89b25          rc=0

$ python3 -I c1-ledger-accountability.py --repo ./fixture-symlink --rev 8dacf016… --work ./work-c1c
C1_LEDGER: … bad_pointer=2 … symlink_pointer=1 … verdict=TARGET_MISSED …
C1_DETAIL: bad_pointer L37 path='tools/mado-eventq.py' kinds=['symlink']
C1_DETAIL: bad_pointer L43 path='tools/mado-monitors.py' kinds=['malformed']
rc=1
```

Mechanism (read, not assumed): `c1-r51-ledger.py:196-208` accepts any token whose bytes contain the row
basename, without comparing the token to the ledger or the instrument and without checking blob mode;
`:155-176` drops a first cell lacking `/` instead of counting it; `:229-232` checks only empty/placeholder
descriptions and never description repetition or genericity. The ledger row the r51 instrument accepts is therefore self-referential, and
`docs/alias` (a symlink) passes because `git show` returns the link target string, not file content.

### 3.4 Frozen selftest matrix (20 cases, all pass; 19 negative + 1 positive)

`S00-valid-control` MET; `S01-absent-ledger` MISSED (`ledger=absent`); `S02` self-ledger sole pointer;
`S03` self-ledger beside a valid pointer; `S04` self-instrument pointer; `S05` bare basename of a nested
file; `S06` `./`-prefixed ledger; `S07` `:x` annotation; `S08` trailing `)`; `S09` duplicated description;
`S10` name-echo; `S11` two-word generic; `S12` `TODO`; `S13` empty; `S14` dangling extra row; `S15`
uncovered row; `S16` duplicate row; `S17` pointer to a file that does not name the instrument; `S18`
symlink alias; `S19` `./`-prefixed row path. Output ends `selftest=20/20`.

Scratch containment negative test: `--work ./fixture-bypass/work-inside` →
`C1_LEDGER: verdict=SETUP_ERROR error='--work must be outside the measured tree'`, rc 2, and
`ls fixture-bypass/work-inside` → `No such file or directory` (no directory was created).

## 4. C2 — measured behavior

### 4.1 Old committed bytes: rejected, with exactly the three routed defects

```
$ python3 -I c2-proposition-bind.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --rev ad4bf2059bcfafe63671d262222908ee1fe8001c \
    --entry corpus/knowledge/hyprland-synthetic-dispatch-r52.md \
    --pins …/mado-shokunin/.ufo/waves/round-52/fetch --work ./work-c2-old
C2_BIND: propositions=18 ids_unique=yes rows_bound=18 pins_resolved=18 quotes_contiguous=17 \
quotes_over_cap=0 quote_words_max=19 subjects=5/6 locators=0/1 rationale_bad=0 selftest=8/8 \
verdict=TARGET_MISSED entry=hyprland-synthetic-dispatch-r52.md rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
C2_DETAIL: P16 quote_not_contiguous_at_pin L28
C2_DETAIL: P17 subject_not_at_pin named=['sendshortcut'] L29
C2_DETAIL: P18 locator_outside_loop L30
rc=1
```

No other row fails: all 18 pins resolve, 17/18 quotes are contiguous at their span, max quote 19 words —
the three named defects are isolated, not inferred from a general failure.

### 4.2 Corrected fixture: accepted

`corrected-entry.md` replaces only the three rows (P16 → P16a contiguous excerpt + P16b clear call; P17
subject `sendkeystate`; P18 after-loop wording); the other 15 rows are byte-identical to the committed entry.

```
$ python3 -I c2-proposition-bind.py --repo …/mado-shokunin --rev ad4bf205… \
    --entry-file ./corrected-entry.md --entry-name hyprland-synthetic-dispatch-r52.md \
    --pins …/round-52/fetch --work ./work-c2-new
C2_BIND: propositions=19 ids_unique=yes rows_bound=19 pins_resolved=19 quotes_contiguous=19 \
quotes_over_cap=0 quote_words_max=19 subjects=7/7 locators=0/0 rationale_bad=0 selftest=8/8 \
verdict=TARGET_MET entry=hyprland-synthetic-dispatch-r52.md rev=ad4bf2059bcfafe63671d262222908ee1fe8001c
rc=0
```

Frozen selftest (8/8): `T00` valid MET; `T01` spliced quote; `T02` wrong subject; `T03` locator outside
loop; `T04` quote over 25 words; `T05` duplicate id; `T06` unbound S-row; `T07` used-by mismatch — each
MISSED with its named defect.

### 4.3 Source truth at the pinned bytes (read-only, lane-owned pins)

Pin provenance: `.ufo/waves/round-52/fetch/`, revision `efb50993780079460b0cbed1363e2166a2de1d9f`, opened
2026-10-27 (entry footer `corpus/knowledge/hyprland-synthetic-dispatch-r52.md:32`; rows
`corpus/SOURCES.md:320-323`). `sha256sum -c SHA256SUMS` in that directory: all 5 files `OK`
(`Hyprland-ConfigActions.cpp` = `a83abeb5…`, `DispatcherTranslator.cpp` = `7248cbb8…`). No fetch was
performed this round.

Located lines (verbatim, indentation stripped for display):

- `Hyprland-ConfigActions.cpp:1554` `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);`
- `Hyprland-ConfigActions.cpp:1556` `if (S.m_passPressed == 1) {`
- `Hyprland-ConfigActions.cpp:1558` `g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);`
- `Hyprland-ConfigActions.cpp:1576` `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);`
- `Hyprland-legacy-DispatcherTranslator.cpp:589` `}` (closes `sendshortcut`, opened `:531`)
- `Hyprland-legacy-DispatcherTranslator.cpp:591` `static SDispatchResult sendkeystate(const std::string& args) {`
- `Hyprland-legacy-DispatcherTranslator.cpp:565` `for (xkb_keycode_t kc = keycode_min; kc <= keycode_max; ++kc) {`
- `Hyprland-legacy-DispatcherTranslator.cpp:571` `}` (loop closes)
- `Hyprland-legacy-DispatcherTranslator.cpp:574` `return {.success = false, .error = "sendshortcut: key not found"};`
- `Hyprland-legacy-DispatcherTranslator.cpp:621-622` `if (keyState == 2 && result.success)` / `result = sendshortcut(modifiedArgs);`

Independent contiguity check on the collapsed span `:1554-1558`: old P16 quote (9 words) present = **False**;
corrected contiguous quote with the guard lines included (16 words) present = **True**.
`grep -Fc 'sendKeyboardMods(modMask, 0, 0, 0); g_pSeatManager->sendKeyboardKey' Hyprland-ConfigActions.cpp`
→ `0`. P17's anchor `:619-622` lies after `sendshortcut` ends at `:589` and inside `sendkeystate`
(`:591`…); P18's `:574` return is after the loop closes at `:571`.

## 5. Routed r52 defects — observed state at base tip (evidence only)

1. **Gate records absent** — `corpus/lessons/round-52.md:5` `## Gate` contains prose instructions but no
   per-row URL/access-date/≤25-word quote record for S370–S373 (section read in full).
2. **Stale Changes note** — `corpus/lessons/round-52.md:23` `## Changes` still reads
   `Pending final integration revisions and receipts.`
3. **QUALITY 17 review still outstanding** — the criterion is defined at `corpus/QUALITY.md:34`; the
   registry text still says so at `corpus/SOURCES.md:374` (“distinct-scope review remains outstanding”).
4. **P16–P18 still present in the indexed entry** — measured in §4.1 against committed bytes, not assumed
   from the r52 lesson. The entry remains at `corpus/README.md:80` route (index row unchanged).

These are reported as observed state, not as my claim to repair; C2’s repair is a lane move and my item is
counter/fixture behavior.

## 6. Limits, risks, blockers

- **Structural, not semantic** (frozen C1 wording agrees): C1's description rule still admits a long,
  non-duplicated, non-generic sentence that under-describes an instrument; pointer containment still
  admits a document that merely lists the instrument path. Both are named limitations, not proof of
  accountability.
- **Committed-counter requirement unmet by construction**: my instruments are scratch-only (this seat may
  not write tracked files). C1 cannot be called met until a lane-committed counter carries this behavior
  and its final-tip receipt; my measurement shows only that the predicate is decidable and that the
  current committed r51 instrument still fails it.
- **“Each frozen forgery fixture” is unanchored in round 53**: no r53 fixture/control file exists at
  inspection, so the claim’s quantifier cannot yet be checked against named immutable inputs. I froze 19
  negative cases inside the instrument; the lane must freeze its own list before data per
  `claims-frozen.md:13`.
- **C2 correction is a fixture, not a lane write**: `corrected-entry.md` demonstrates the binding rules
  (old bytes rejected, repaired bytes accepted) but is not an append-only lane correction and carries no
  admission or expansion credit.
- No blocker encountered; no ENOSPC (`/fast` 591 G avail, `/home` 589 G avail); disk guard checked before
  work; no tool installs.

## 7. Scratch and tooling

Scratch `/fast/scratch/hyaku/mado-r53/R53Seven64` held the two counters, two git fixtures (created with
`--shared` clones, scratch identity, toplevel asserted), receipts and the corrected fixture; it was
removed after this report was written. Lane `git status --porcelain` at first read showed only the
pre-existing untracked `.ufo/waves/round-53/`; the final read additionally showed
`?? corpus/lessons/round-53.md`, which appeared during the wave and was **not** written by this seat
(sibling activity, left untouched). HEAD unchanged `ad4bf205…`; this seat wrote only this report. No package transactions, no
live reads, no screenshots, no input capture, no producer execution, no lane/fleet/sibling writes.

---

## Trailer

**Attacked predicate.** C1 `.ufo/waves/round-53/claims-frozen.md:7` (scratch-aware accountability counter:
production pass, no-work and frozen-forgery misses, exact population, non-self pointers) and C2
`.ufo/waves/round-53/claims-frozen.md:11` (counter rejects the r52 P16/P17/P18 bytes and accepts a
corrected entry with quote/pin/proposition bindings).

**Exact commands/outputs.** §3.1–3.4 and §4.1–4.3 above; each block is copied from the executed command
(rc shown). Source-truth raw checks: `sha256sum -c SHA256SUMS` → 5× `OK`; the `awk`/`grep -Fc` line reads
in §4.3.

**Sources opened (local, read-only).** `SKILL.md`; `.ufo/waves/round-53/claims-frozen.md:1-13`,
`w1-dispatch.json`; `quality/counters/c1-r51-ledger.py:1-430`; `quality/tool-ledger.md`;
`corpus/knowledge/hyprland-synthetic-dispatch-r52.md:1-32`; `corpus/SOURCES.md:320-323,374`;
`.ufo/waves/round-52/fetch/{Hyprland-ConfigActions.cpp,Hyprland-legacy-DispatcherTranslator.cpp,SHA256SUMS}`
(revision `efb5099…`, opened 2026-10-27, pinned hashes above); `corpus/lessons/round-52-verifier-spotcheck.md`;
`corpus/lessons/round-52.md:5-25`; `corpus/QUALITY.md:34`; `corpus/README.md:80`. No new external URL was
fetched; the source URLs are the already-registered ones in `corpus/SOURCES.md:320-323`.

**Report path (relative to `/home/vgpnk/Projects/shokunin/mado-shokunin`):**
`.ufo/waves/round-53/w1/R53Seven64.md`
