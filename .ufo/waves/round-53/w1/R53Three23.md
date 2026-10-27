# R53Three23 — scribe, round 53 w1: C1/C2 evidence and lesson prose

- seat: `R53Three23`, role scribe (leaf; no dispatch, no vote, no gate authority)
- lane: mado — `/home/vgpnk/Projects/shokunin/mado-shokunin`
- round 53 w1, frozen base/tip `ad4bf2059bcfafe63671d262222908ee1fe8001c`
- claims under test: C1 operability (instrument-ledger accountability counter), C2 coverage
  (proposition-bound r52 dispatcher entry repair) — `.ufo/waves/round-53/claims-frozen.md`
- product: prose only. This seat writes no tracked file, admits nothing, and is not a
  non-author reviewer for either claim.

## 0. Boundary compliance (what this seat did and did not do)

Read-only on the lane: every command below reads committed bytes at the frozen revision or
committed wave artifacts; two isolated reads outside the lane (`/home/vgpnk/Projects/shokunin/CORPUS.md`)
supply the corpus contract text. No git/jj mutation, no packet/page fetch, no live probe, no
package query, no producer execution, no input capture, no screenshot, no service or
compositor call, no `task`/background job, no install.

- scratch: `/fast/scratch/hyaku/mado-r53/R53Three23` (scripts named in §2/§3, removed before
  yield; nothing written outside it and this report file)
- `git status --porcelain` at start: `?? .ufo/waves/round-53/` only — base tip clean, no
  round-53 tracked change exists yet
- disk guard: `/fast` 596G avail, `/tmp` 125G avail at seat start; no ENOSPC encountered
- tooling: preinstalled `git 2.x`, `python3`, `sha256sum` — nothing installed, nothing to record

Evidence labels: `[OBS]` measured by this seat; `[VERIFIED-ARTIFACT]` committed receipt whose
digest I recomputed but whose test run belongs to another seat; `[INF]` inference; `[UNK]` unknown.

## 1. Measured state at tip (all `[OBS]`)

| Item | Value | Command |
|---|---|---|
| lane HEAD == frozen base | `ad4bf2059bcfafe63671d262222908ee1fe8001c` | `git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD` |
| round-53 tracked change | none (`?? .ufo/waves/round-53/` only) | `git status --porcelain` |
| r52/r53 C1 counter committed | none (`ls quality/counters/ \| grep -Ei 'r5[23]'` → empty, exit 1) | same |
| ledger rows / population | `population=82 ledger_rows=82 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 dup=0` | `python3 ledger-census.py --repo … --rev ad4bf205…` (§2.1) |
| ledger self-pointer rows today | `0` (12 distinct pointer tokens; `SCORECARD.md` ×42, `PROVINCE.md` ×20) | §2.4 command |
| r52 entry digest | `bee0d14379eb560595c5d2237ffc9fd0f6d61c3b6b728fbb0dab851687ecb078` | `sha256sum corpus/knowledge/hyprland-synthetic-dispatch-r52.md` |
| r51 counter digest | `d5c2447d098681251fd41c04414d4e8823b41b78f150a5fc6bedd526a4a35b56` | `sha256sum quality/counters/c1-r51-ledger.py` |
| ledger digest | `df5b3705d0291f967c35f0d69d6a908fe37a30d35e84599c4c0f897ca6469e0b` | `sha256sum quality/tool-ledger.md` |
| r52 entry propositions | `18` (`P01`…`P18`), **no** `Errata` section (`grep -c Errata` → 0) | `grep -cE '^\| P[0-9]{2} \|' …` / `grep -c Errata …` |
| r52 fetch bytes | 5/5 `sha256sum -c SHA256SUMS` → `OK` | `sha256sum -c .ufo/waves/round-52/fetch/SHA256SUMS` |

Consequence for both claims: **neither r53 target artifact exists at tip** — no committed
r53 counter, no corrected entry bytes. Any C1/C2 success statement today is a plan, not a
measurement. This matches the round-52 closure state (`.ufo/waves/round-52/…` honest stop)
and fixes the red-before baseline the round-53 counters must beat.

## 2. C1 — operability: what the ledger predicate can and cannot see

### 2.1 Attacked predicate, as it stands

`[OBS]` `quality/counters/c1-r51-ledger.py` (digest above), verdict block at `:413-428`:

```
clean = (mine["population"] > 0 and mine["ledger_rows"] == mine["population"]
         and not any(mine[k] for k in ("uncovered", "dangling", "bad_pointer",
                                       "empty_desc", "dup")))
met = clean and selftest_rc and ledger_rc
```

with the two defect clauses it feeds:

```
:229-232   desc = row["desc"].strip(EMPHASIS)
           if not desc or PLACEHOLDER.match(desc):
               counts["empty_desc"] += 1
:76        PLACEHOLDER = re.compile(r"^[\s\-–—_*`.]+$")
:196-209   def pointer_resolves(clone, rev, files, row_path, pointer, cache):
               base = os.path.basename(row_path)
               for token in pointer_tokens(pointer):
                   if token not in files: continue
                   ...
                   if base.encode() in cache[token]: return True
```

and `[OBS]` its registration sentence, `.ufo/waves/round-51/registration.md` (C1 paragraph):
"each such file appears exactly once in `quality/tool-ledger.md` with a non-empty description
and an accountability pointer naming an existing repo file that contains the file's basename".

### 2.2 The structural gap (measured by reading the predicate, `[OBS]`)

1. **Description clause is a printer's test, not a context test.** The only rejection is
   empty-or-punctuation (`PLACEHOLDER`). "Does the thing." and a sentence copied verbatim
   from another row both pass. My independent census adds a lower bound the predicate does
   not impose: `short_desc_rows=0` at ≤3 words — the current 82 descriptions are all longer
   than three words, but nothing in the predicate enforces that.
2. **Pointer clause is a mention test, and the ledger mentions everything.** `pointer_resolves`
   accepts any tracked file containing the row's basename. `quality/tool-ledger.md` is tracked
   and contains all 82 basenames, so a row pointing at the ledger passes; so does the row's
   own file (self-mention). Today `self_pointer_rows=0` `[OBS]` — the weakness is latent in
   the predicate, not yet present in the data.
3. **`dup` is tracked but never named as a defect in the registration sentence.** The counter
   appends `dup=N` to the line only when non-zero (`:424-425`); the registration sentence does
   not require uniqueness of description text.

This is why the r53 claim's own bound is right: "bounded structural accountability check, not
semantic proof." The measured envelope in §2.4 says how far structure can be pushed.

### 2.3 Demonstrated bypasses — committed receipts, digest-checked, not re-executed

`[VERIFIED-ARTIFACT]` `.ufo/waves/round-52/w2/Attack01.md`
(`sha256 042ab7c80347174b607374777f7653d984206965dc650c8f366b52106d874c7b`): the forged
description family is accepted by the r51 predicate — its table prints
`production at base | generic_desc=0 verdict=TARGET_MET exit 0`, `control-F3-forged.md |
generic_desc=0 verdict=TARGET_MET — all 82 forged rows accepted`, and
`H4n-nameonly-forged.md (mado-anims.py desc = "mado anims py does things here.") |
generic_desc=0 TARGET_MET`.

`[VERIFIED-ARTIFACT]` `.ufo/waves/round-52/w2/Attack02.md`: nine self-pointer spellings pass a
counter that carries a `self_pointer` field (`P03`…`P07`, `P19`…`P21` quoted in that file);
note that file attacks the *uncommitted* r52 rewrite, not the committed r51 counter, so on the
tip counter the self-pointer family is established by §2.2 reading, not by that receipt.

`[INF]` Both receipts are lane-committed and were digest-verified here; I did not rerun them
(scribe scope, and re-running another seat's attack would not be evidence of anything new).

### 2.4 Candidate discriminators, measured on the unchanged production ledger `[OBS]`

Rule under test: a description must share ≥N content tokens (len ≥4, lowercased, stopwords
removed) with the instrument's **own header** (first 40 lines of the file at the same revision).
Script `/fast/scratch/hyaku/mado-r53/R53Three23/variants.py`, command
`python3 variants.py`, output:

```
A header>=2                  production_fail=0 forged_accepted=0
B header>=3                  production_fail=1 forged_accepted=0
    prod-fail quality/counters/c1-r48-terminal-cache.py
C header>=2 & one non-name   production_fail=0 forged_accepted=0
D header>=2 & >=1 non-name   production_fail=0 forged_accepted=0
```

- `A` is production-compatible (82/82 pass; overlap histogram mode 12 with 9 rows, minimum 2 —
  one row at overlap=2, one at 3, one at 4, two at 5) **and** rejects both forged descriptions I tested
  (`"does the thing"`, own-name restatement) against `tools/mado-anims.py` and
  `quality/check-tool-ledger.py`.
- `B` (≥3) costs one ledger rewrite today → **not** TARGET_MET-compatible without a tracked edit.

Weaker than it looks. Two further probes, `[OBS]`:

- generic sentence `"This instrument does the thing."` → accepted for `0/82` targets; the
  own-name restatement `"<basename tokens> does things here."` → **accepted for 20/82**
  (headers that name their own module, e.g. `tools/mado-action-plan.py` sharing
  `action`, `plan`, `mado`).
- cross-row description swap (row *a* carrying row *b*'s description) → accepted for
  **3733/6642 = 56.2 %** of ordered pairs.
- nearest-header binding (description's best-matching header, argmax Jaccard, must be its own
  instrument) → `own_is_argmax=57/82` on the production ledger, i.e. **25 rows fail today**,
  clustered in the v1/v2 counter families (`c1-r40-live{,-v2}.py`, `c1-r46-devices{,-v2,-v3}.py`,
  `c2-r43-gkeep-entry{,-v2}.py`, `c1-r44-geometry-states{,-v2}.py` …). Those instruments are
  near-duplicates by construction, so an argmax rule cannot be made green without rewriting
  the ledger it is meant to audit.

Reading: the honest discriminating power of a lexical context signal is a **≥2-token overlap
with the instrument's own header plus a description-distinctness clause**. It kills the
repeated-generic family (the r52 Attack01 class) and the empty/punctuation class; it does not
kill own-name restatement or cross-row borrowing, and no cheap rule does, because 25/82
instruments are family-duplicates.

### 2.5 Operability trap the r53 landing will hit `[OBS]`

Population rule (`quality/counters/c1-r51-ledger.py:133-148`) counts every direct
`quality/counters/*.py` and every direct `quality/*.py`. A new `quality/counters/c1-r53-*.py`
therefore enters the population **of its own commit**:

```
population_now=82 population_with_new_counter=83
new_in_population=['quality/counters/c1-r53-ledger.py']
```

So a counter that demands `ledger_rows == population` cannot print `TARGET_MET` on the
production ledger unless the same commit adds the ledger row for the counter itself (row 83),
with a pointer that is not the ledger and not the counter file. A sentence claiming
"TARGET_MET on production" without that row is arithmetically unreachable. Precedent for an
acceptable pointer target: `.ufo/waves/round-51/registration.md` already names three
instruments (`.ufo/waves/round-51/registration.md` ×3 in the pointer tally).

Scratch-awareness precedent to extend, not invent `[OBS]`
(`quality/counters/c1-r51-ledger.py:68,278-286,404-407`): `REFUSED_ROOTS = ("/tmp", "/var/tmp",
"/dev/shm")`, `--selftest --work <sandbox>` with an explicit `n/n passed` ratio, and a hint
when selftest work sits under a refused root. The r53 counter should keep all of that and add
a `--selftest` that runs the *fixture matrix* it claims to discriminate.

### 2.6 Append-ready prose — the contract the r53 counter must satisfy

Draft for the round-53 lesson / registration (not written to any tracked file by this seat):

> **C1-R53 contract (draft).** `quality/counters/c1-r53-ledger.py` measures
> `quality/tool-ledger.md` at an explicit `--rev`, writes only under `--work`, and prints one
> final line `C1_R53: population=<P> ledger_rows=<P> uncovered=0 dangling=0 bad_pointer=0
> empty_desc=0 dup=0 distinct_desc=<P> context=<P> selftest=ok verdict=TARGET_MET rev=<rev>`
> where `<P>` is the exact r51 population rule (unchanged) and:
> 1. **unique population** — each file appears exactly once (existing rule);
> 2. **description distinctness** — no two rows carry the same normalized description text
>    (new; kills the r52 Attack01 repeated-generic family);
> 3. **instrument-context signal** — each description shares ≥2 content tokens (len ≥4,
>    lowercased, stopwords removed) with the instrument's own header (first 40 lines at
>    `--rev`); measured 82/82 pass on the unchanged ledger, 0 false accepts on the two forged
>    families tested (§2.4);
> 4. **non-self pointer** — at least one pointer token resolves to a tracked file that is
>    neither `quality/tool-ledger.md` nor the row's own path, after normalizing `./`,
>    repeated `/`, and a trailing non-numeric suffix, and the basename occurrence must sit on
>    a prose line outside a fenced code block (new; kills the r52 Attack02 spellings and the
>    r51 comment-only residual);
> 5. **fixtures** — `--selftest` must return `TARGET_MISSED` for: no-work ledger; all-rows
>    generic description; ledger self-pointer; row self-pointer; comment-only pointer;
>    duplicate description; and `TARGET_MET` for the production ledger **including the row
>    this counter adds** (§2.5).
>
> **Stated bound.** Rules 2–3 are lexical. They bound the generic-description family; they do
> not prove that a description is true, and they do not reject own-name restatement (20/82
> headers admit it) or cross-row borrowing (56.2 % of pairs admit it). The claim's admission
> language must therefore say *structural accountability*, exactly as
> `.ufo/waves/round-53/claims-frozen.md` C1 already does.

## 3. C2 — coverage: the three falsified propositions, re-measured, and their repair

### 3.1 Attacked artifact, byte-identical to the round-52 attack target

`[OBS]` `corpus/knowledge/hyprland-synthetic-dispatch-r52.md`, digest
`bee0d143…ecb078` — the same digest `w2/Attack07.md` records (`bee0d143…ecb078`), so the
defects are not stale: the file has not been touched since the attack. Indexed at
`corpus/README.md:80`; rows `S370`–`S373` at `corpus/SOURCES.md:320-323`; fetch bytes verify
(§1). Defective rows verbatim:

```
| P16 | The action sends modifier state before the key event, then clears the modifier state. | S371 | Hyprland-ConfigActions.cpp:1554-1558,1576 | `<mods call>; <key call>` | direct | … |
| P17 | `sendshortcut`'s repeat branch can invoke its delegate twice for a successful repeat state. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:619-622 | `if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` | direct | … |
| P18 | An unresolved keysym returns the `key not found` error inside the scan. | S370 | Hyprland-legacy-DispatcherTranslator.cpp:574 | `return {.success = false, .error = "sendshortcut: key not found"};` | direct | … |
```

### 3.2 Three mechanical signals — one per defect class `[OBS]`

Seat scripts: `quotes.py` (verbatim/contiguity/≤25 words), `scope.py` (brace-scope extraction
of top-level function and `for`-loop ranges from the pinned bytes). Commands and output:

```
$ python3 quotes.py cases-orig.json
P16-orig   pin=1554-1554;1558-1558;1576-1576 words=9   strict=True  contig=False file=False FAIL
P17-orig   pin=619-622            words=9   strict=True  contig=True  file=True  OK
P18-orig   pin=574-574            words=10  strict=True  contig=True  file=True  OK
cases=3 fails=1
```

```
$ python3 -c '…scope.json…'
fn {'name': 'sendshortcut', 'start': 531, 'end': 589}
fn {'name': 'sendkeystate', 'start': 591, 'end': 627}
loop {'name': 'for', 'start': 565, 'end': 571}
P17 pin line 619 owner: ['sendkeystate']
P18 quoted line 574 inside loop 565-571? False
```

Reading, defect by defect:

- **P16 = splice.** The quote is not the file's text anywhere (`file=False`); it exists only
  when lines 1554 and 1558 are glued, eliding `if (S.m_passPressed == 1) { if (!isMouse)`.
  The "then clears" clause rests on `:1576`, which the rationale itself calls part of the
  *locator*, not the quote. Mechanism: quote contiguity.
- **P17 = wrong subject, and the quote is innocent.** The quote is verbatim and contiguous;
  the defect is that `keyState`/the repeat branch live in `sendkeystate` (`:591-627`), and
  `sendshortcut` (`:531-589`) has no state field. Mechanism: named-owner vs pin-enclosing-function.
- **P18 = wrong localization, quote innocent again.** The return at `:573-574` executes after
  the loop closes at `:571`; "inside the scan" is false. Mechanism: localization word vs
  bracket range.

This is the load-bearing finding for the counter design: **only one of the three defects is
visible to a quote-only counter.** A counter that checks quote-at-pin accepts P17 and P18 as
written, so "rejects the old bytes" is unreachable for those two rows unless the counter also
binds *proposition text* — subject symbol and localization — to pin structure.

### 3.3 Verified repaired rows (append-ready; every quote re-checked this seat)

`$ python3 quotes.py cases-fixed.json` →

```
P16a       pin=1554-1554          words=4   strict=True  contig=True  file=True  OK
P16b       pin=1556-1558          words=12  strict=True  contig=True  file=True  OK
P16c       pin=1576-1576          words=4   strict=True  contig=True  file=True  OK
P17fix     pin=619-619;621-622    words=13  strict=True  contig=True  file=True  OK
P17subject pin=591-591            words=6   strict=True  contig=True  file=True  OK
P18fix     pin=571-571;573-574    words=12  strict=True  contig=True  file=True  OK
cases=6 fails=0
```

Draft errata text (for an append-only `## Errata (round 53)` section on the entry — the
precedent is `corpus/knowledge/hyprland-dispatcher-dispatch-r51.md:318`, "Errata (round 51 w2;
append-only source-truth correction)"):

| ID | Corrected proposition | Pin | Quote (verbatim, ≤25 words) |
|---|---|---|---|
| P16a | The action sends a modifier update carrying the requested mask before it branches on `m_passPressed`. | S371 `ConfigActions.cpp:1554` | `g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);` |
| P16b | The pressed keyboard event is sent only when `m_passPressed == 1` and the input is not a mouse. | S371 `ConfigActions.cpp:1556-1558` | `if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` |
| P16c | After the press/release branch the action sends a modifier update with a zero mask. | S371 `ConfigActions.cpp:1576` | `g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` |
| P17 | Inside `sendkeystate` (function opens `:591`), a `repeat` state whose first `sendshortcut` call succeeded invokes `sendshortcut` a second time. | S370 `DispatcherTranslator.cpp:619-622` (owner line `:591`) | `auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) result = sendshortcut(modifiedArgs);` |
| P18 | When the key-name scan finds no matching keysym (`keycode` still 0 after the loop closes at `:571`), the cache-miss branch returns the `key not found` error. | S370 `DispatcherTranslator.cpp:565-574` | `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` |

Attribution notes the errata text must carry, because they are the difference between repair
and papering over:

- **P16** is split rather than reworded: the original asserted call *ordering* across a
  22-line span. Ordering is supported by line order in the pin locator (`:1554` < `:1576`),
  not by one contiguous quote; three clause rows keep each quote verbatim. Count 18 → 20.
- **P17's** repaired content is the same ground as **P04** (`:619-622`, "repeat calls its
  delegate again only after a successful first call"), differing only by naming the delegate
  and its owner. Repaired as a subject-bound restatement it duplicates P04; withdrawn it
  leaves 17 propositions. The errata must choose one and say so — a silent 18→20 inflation
  would be a coverage overclaim.
- **P15** (`:612`, "saves the prior `m_passPressed` value **before changing it**") has the
  same binding-gap shape as P17/P18 (the writes at `:614-617` and the restore at `:624` lie
  outside pin and quote). It is *not* in the routed set; flagged here only so the repaired
  counter is not written to accept a row whose claim exceeds its pin by construction.

### 3.4 What a proposition-binding counter must do (design consequence, `[OBS]`-derived)

1. parse the main Proposition-map table by position (`| P## | Proposition | S### | pin | quote | …`),
   not by the r52 landed regex that expected `| P## | S### |` (that is why the landed r52
   counter read `props=0`, `w2/Attack07.md` T1);
2. quote binding: whitespace-collapsed quote ⊆ pin window, and the pin window must be
   *contiguous* unless the row is explicitly declared multi-range (my P16-orig test shows the
   discriminator: `contig=False, file=False`);
3. subject binding: every backticked function name in a proposition must be the enclosing
   function of the pin's quoted line (brace-scope extraction reproduced `sendkeystate` for
   `:619` without a compiler, §3.2);
4. localization binding: a proposition saying "inside the loop/scan" must pin a line inside a
   loop range (reproduced: `:574` outside `565-571`);
5. scope: errata rows are parsed as *superseding* the original IDs, so the count is stated
   explicitly and old bytes are rejected rather than double-counted.

Bound: rules 3–4 are structural. A proposition can name the right function and still assert a
false relation inside it; the counter cannot close that, and the claim must not say it does.

### 3.5 Coverage-bookkeeping facts that limit what r53 may claim `[OBS]` / `[OBS-doc]`

- **No expansion credit is available this round.** `CORPUS.md:123` (fleet root, rule 4):
  "Expansion is knowledge, not rows. The expansion trend counts admitted `knowledge/` entries
  whose `source:` cites a `mined` row on uncovered coverage-map ground." `S370`–`S373` were
  opened 2026-10-27 in round **52** (`corpus/SOURCES.md:320-323`), and round 53 has no
  `fetch/` directory (`.ufo/waves/round-53/` holds only spec, claims, dispatch, ready,
  registry — `[OBS]`). A repaired, admitted r52 entry therefore cannot move *expansion* in
  round 53; the most it can do is remove a quality defect on already-landed ground. The
  frozen C2 sentence is stricter than the contract and should be read as: repair now,
  expansion credit only in the round that opened the row.
- **The entry's URL duplicates are exact, not "scope-overlap".** `[OBS]` extracted URL cells:
  `S370` ≡ `S365` (`…/src/config/legacy/DispatcherTranslator.cpp`), `S371` ≡ `S367`
  (`…/src/config/shared/actions/ConfigActions.cpp`), `S373` ≡ `S364`
  (`…/src/managers/KeybindManager.cpp`), all at revision
  `efb50993780079460b0cbed1363e2166a2de1d9f`; `S372` (`ConfigActions.hpp`) is new ground.
  `corpus/QUALITY.md:34` (rule 17) requires an explicit review or a superseding row for such
  reuse, and says a warning-only census is not that review — routed defect 3 remains open.

## 4. Routed round-52 defects, re-measured as evidence only

| # | Routed defect | Measured at tip | Class |
|---|---|---|---|
| 1 | `corpus/lessons/round-52.md` `## Gate` lacks per-row S370–S373 records | `grep -c "S37[0-3]" corpus/lessons/round-52.md` → `0`; the Gate section (`:5-13`) carries only the instruction | `[OBS]` open |
| 2 | Same lesson `## Changes` stale | `:23-25` still reads "Pending final integration revisions and receipts." while round-52 changes landed at `56d6e705` | `[OBS]` open |
| 3 | QUALITY 17 distinct-scope review owed | URL cells identical for 3 of 4 rows (§3.5); no review record found in the lesson | `[OBS]` open |
| 4 | Entry P16–P18 falsified | digest unchanged since the r52 attack; §3.2 reproduces all three | `[OBS]` open |
| 5 | SHONEN boxes `[~]`, operator-owned | outside this seat's authority; no promotion claimed | `[INF]` per r52 closure §5 |

These are the *inputs* to C2, not findings this seat may close: a scribe reporting them is not
a verifier and supplies no admission.

## 5. Gates any r53 landing must clear (prose, not a vote)

C1: a committed `quality/counters/c1-r53-*.py` at the measured revision; production
`TARGET_MET` with the counter's own ledger row present (population 83, not 82); `TARGET_MISSED`
on the no-work control and on every declared forgery fixture; a selftest that runs the fixture
matrix; all writes under `--work`, refused under `/tmp`,`/var/tmp`,`/dev/shm`.

C2: an append-only errata section that states the chosen P17 disposition (restate as
subject-bound duplicate of P04 → 20 propositions, or withdraw → 17) and does not silently
inflate the count; three repaired propositions whose quotes I have verified verbatim and
contiguous; a frozen counter that rejects the current bytes (splice, owner mismatch,
localization mismatch) and accepts the errata; one independent non-author reviewer on source
truth; **no expansion-credit sentence** (§3.5, `CORPUS.md:123`); Gate records for S370–S373
appended in the round-53 lesson (new entry, never a rewrite, per `CORPUS.md:112-118` rules 1–2).

## 6. Axis statement (coverage, operability) — as far as a scribe may state it

| Axis | Status this seat can defend | Basis |
|---|---|---|
| operability | **unchanged, at risk of a null round.** No counter at tip; the r53 target is reachable only if the counter's own ledger row lands in the same commit (§2.5). The r51 predicate cannot see the two demonstrated bypass families (§2.2/2.3), and the strongest production-compatible discriminator I could measure is a weak lexical one (§2.4). | `[OBS]` |
| coverage | **no move available this round.** Entry bytes unchanged; repair is planned, not landed; expansion credit barred by the round the rows were opened in; a repaired admission would be a quality repair on already-indexed ground. | `[OBS]` + `CORPUS.md:123` |
| harm | **none observed.** No tracked byte changed by this seat; no axis row, capability, or score touched; no entry marked admitted or superseded. | `[OBS]` |

## 7. Limits and unknowns

- I did not re-execute `c1-r51-ledger.py`, the r52 landed counter, or any seat's fixture: the
  bypasses in §2.3 are digest-verified committed receipts (`[VERIFIED-ARTIFACT]`), not my runs.
- My census reimplements the r51 population/pointer contract from its source; it is not the
  counter. Where it differs (it adds the short-description and self-pointer tallies), the
  difference is labelled.
- `[UNK]` Whether the r53 executors intend a `dup`-based distinctness clause or a
  header-overlap clause; both are measured above, and both are production-compatible.
- `[UNK]` Whether the r53 C2 repair intends to restate or withdraw P17 — the choice changes
  the proposition count and therefore the frozen counter's expected-count field.
- Brace-scope extraction is textual (comment/string aware only for `"`), sufficient for the
  two functions and one loop exercised here; it is not a parser and is not offered as one.
- No newly opened source: every quote came from committed `.ufo/waves/round-52/fetch/` bytes
  (`sha256sum -c` OK), whose registered origin is the pinned Hyprland revision
  `efb50993780079460b0cbed1363e2166a2de1d9f` recorded in `corpus/SOURCES.md:320-323`
  (opened 2026-10-27).

## Trailer

- Report: `.ufo/waves/round-53/w1/R53Three23.md` (this file; all paths relative to lane root
  `/home/vgpnk/Projects/shokunin/mado-shokunin`)
- Attacked predicates: PRED-C1-r51 (`quality/counters/c1-r51-ledger.py`, digest
  `d5c2447d…a35b56`) as the before-state of frozen C1; the r52 proposition map
  (`corpus/knowledge/hyprland-synthetic-dispatch-r52.md`, digest `bee0d143…ecb078`) as the
  before-state of frozen C2
- Scratch `/fast/scratch/hyaku/mado-r53/R53Three23/` — `ledger-census.py`, `quotes.py`,
  `cases-orig.json`, `cases-fixed.json`, `scope.py`, `scope.json`, `context-signal.py`,
  `variants.py`, `nearest.py` — removed before yield
- Writes: this report only. No tracked lane file, fleet file, sibling report, script,
  template, state, watchdog, or shokuknow write; no `~/.local/bin` or PATH write
- No git/jj mutation, commit, push, task, delegation, or background job; no fetch, live read,
  package query, input capture, screenshot, producer execution, service/compositor mutation;
  no install (so no tool/version/channel record)
- Tooling: preinstalled `git`, `python3`, `sha256sum`
