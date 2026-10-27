# R54W2Seat03 — w2 falsification: item 3, C1 P22 quote judge

Seat: `R54W2Seat03`, role reviewer (w2-dispatch.json:38-42), leaf member — no subagents, no
background jobs, no lane/source/git mutation. Attacked item: **C1 P22 quote judge** — raw
bytes vs the registered normalization, literal vs whitespace-normalized matching, and the
exact anchor.

- Base: `e25149fec8152a3aabd2b18a0ee8663b23cf65aa` (frozen, claims-frozen.md:3). Lane HEAD
  during this seat: `350d30e4ec5531f65ce99a57efeb8216f38e678a` (unchanged by this seat).
- Counter state at scoring time: `ls quality/counters | grep -c r54` → `0` (exit 1). **No
  c1-r54 counter is landed in the lane, so no landed judge could be re-run; this seat
  falsifies the frozen judge itself against the pin bytes** (the item as dispatched:
  "Re-run only existing pinned commands where available; if a counter is absent, report
  NOT RUN/absent"). The pinned commands that do exist — digest recomputation, span
  extraction — were re-run; everything below is freshly measured, not inherited.
- My prior w1 report: `.ufo/waves/round-54/w1/R54Seat03.md` (executor, item 3 hash/manifest
  leg; its Finding 1 measured the quote-judge matrix for all four propositions). This w2
  seat re-derives the P22 row of that matrix from scratch and adds three numbers w1 did not
  publish: the B-mode space count, the two-window side-claim ambiguity, and the component
  uniqueness counts.
- Scratch: `/fast/scratch/hyaku/mado-r54/R54W2Seat03` (created, used, removed before yield —
  see §6). No `/tmp` files. No tool installed or updated (none needed; `RULES.md` directive
  not triggered). No live-host read, no producer execution, no campaign tool, no config or
  compositor mutation; `/home/vgpnk/Projects/shokuknow` not read.

## 1. Frozen contract lines under attack

| citation | text |
|---|---|
| claims-frozen.md:24 | "(a) each of the four corrected propositions P19–P22 … **has its Quote cell occurring verbatim and contiguous in the round-52 pin** named by its Pin:anchor cell" |
| claims-frozen.md:27-28 | "… P22 at **exactly** :573-574 **after line 571**), (c) …" |
| claims-frozen.md:37-39 | Kill rule: any real pin, quote, or anchor mis-verifies → `verdict=TARGET_MISSED`, non-zero exit, honest report |
| registration.md:30 | P22 row: pin `Hyprland-legacy-DispatcherTranslator.cpp`, anchor `:573-574`, quote `` `if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};` `` |
| registration.md:34 | side-claim: "P22 at exactly lines 573–574 with `573 > 571`" |
| registration.md:21-23 | propositions leg: entry rows checked against the frozen table "byte-for-byte modulo trailing spaces" |
| registration.md:19 | recorded pin digest `7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771` |
| registration.md:51-53 | **the judge**: "Judge of \"verbatim\": exact byte contiguity after single-space normalization of interior newlines ONLY where the frozen quote itself carries a newline (P19/P21/P22 are single logical lines)." |
| claims-frozen.md:5-7 | freeze rule: a falsified predicate is an honest stop or a pre-data re-registration in a NEW versioned file, never an edit |

## 2. Ground truth: the pin bytes (measured this seat)

`git -C /home/vgpnk/Projects/shokunin/mado-shokunin show e25149fec8152a3aabd2b18a0ee8663b23cf65aa:.ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp`
→ `sha256sum` = `7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771` — equal
at base, at HEAD `350d30e4`, and in the working tree (three digests printed identical), and
equal to the registered digest (registration.md:19). Pin leg (c) holds for P22's pin.

Raw bytes around the anchor (`sed -n '569,576p' … | cat -A`), 1-based line numbers:

```
571:            }$                      <- scan-loop close ("after line 571" refers to this)
572:$                            <- BLANK line
573:            if (!keycode)$          <- 12 leading spaces
574:                return {.success = false, .error = "sendshortcut: key not found"};$   <- 16 leading spaces
575:        } else$
576:            keycode = g_pKeybindManager->m_keyToCodeCache[KEYPAIRSTRING];$
```

The frozen P22 quote cell contains **no newline** (measured: `'\n' in quote` → `False`),
which under registration.md:53 means the registered judge permits **zero** normalization
for P22 and demands raw byte contiguity.

## 3. FINDING W2-03-A (blocking, judge-level): the P22 quote judge is unsatisfiable as frozen; matching requires a normalization registration.md:51-53 does not authorize

Match matrix, freshly measured this seat (script in scratch, `python3 -I`, exit 0):

| mode | operation | P22 result |
|---|---|---|
| A | raw byte substring of the anchor span 573–574 joined by `\n` (what "verbatim and contiguous", claims-frozen.md:24, means literally) | **False** |
| B | the registered judge applied to the span: interior `\n` → single space, indentation kept | **False** |
| C | per-line `strip()` + single-space join (minimum normalization that can match) | True |
| D | full whitespace-collapse of both sides | True |
| E | raw byte substring anywhere in the whole 868-line pin | **False** |
| E2 | return-statement bytes alone, anywhere in the pin | True (line 574) |

Why B fails — the decisive number w1 did not publish: the raw gap between `if (!keycode)`
and `return` in the pin is `)` + `\n` + **16 spaces** (`')\n                '`, measured
repr). The registered normalization turns the newline into exactly one space and keeps the
16-space indentation, leaving **17 spaces where the frozen quote has 1**. The quote also
omits the 12- and 16-space leading indents of lines 573/574. So the failure is not "the
registered normalization was not applied" — **no operation the registered judge names can
ever make P22 match**; the minimum matching normalization is per-line strip + join
(C), which registration.md:51-53 authorizes for no quote (P22's cell carries no newline).

E + E2 localize the mismatch precisely: the return statement's bytes occur exactly once
(line 574); the quote's bytes occur **nowhere** in the pin (0 byte-exact occurrences —
consistent with w1 R54Seat02:93). The mismatch is confined to the two-line join.

Consequences (falsification, per claims-frozen.md:37-39 and :5-7):

- A counter faithful to the registered judge scores `quotes=3/4` **on the perfect base
  tree** → prints `verdict=TARGET_MISSED`, non-zero exit. The predicate is **unsatisfiable
  as frozen**: clause (a) cannot hold for P22 under registration.md:51-53.
- A counter that prints the frozen `TARGET_MET` line necessarily judges P22 by an
  **unfrozen** normalization (C or D). No frozen control (C1-CTL-1…6, registration.md:42-47)
  exercises the judge's normalization, so the deviation is invisible to `controls=6/6` —
  `controls=6/6` therefore cannot evidence judge fidelity (same conclusion as my w1
  Finding 3, variant V8, now P22-specific).
- Either way the frozen contract line registration.md:51-53 (and with it clause (a) of
  claims-frozen.md:24) is falsified for P22. Frozen claims/registration remain unchanged per
  my dispatch; the honest outcomes are an honest stop or a pre-data re-registration in a NEW
  versioned file (claims-frozen.md:6-7) that declares the actual judge (per-line strip +
  single-space join, or full whitespace collapse) for newline-free multi-line quotes.

## 4. FINDING W2-03-B (anchor): the side-claim cannot pick the span — only exact equality to the frozen anchor cell can

Collapse-match window enumeration over the whole pin (all `(start,end)` whose collapsed
text equals the collapsed quote): exactly **two** windows — `(572,574)` and `(573,574)`.
The frozen anchor is exactly `(573,574)`. The registered side-claim `573 > 571`
(registration.md:34; "after line 571", claims-frozen.md:28) is satisfied by **both** window
starts, because line 572 is blank and `572 > 571` is also true (measured:
`{572: True, 573: True}`). So the side-claim is a consistency check, **not** a span
discriminator; an anchors leg implemented as "the collapse window whose start clears the
side-claim" would certify span 572–574 — a span the frozen table does not name. The anchors
leg must require exact equality with the frozen anchor cell `:573-574`. (Redundant in a
full counter because the propositions leg already pins the entry's cell byte-for-byte
(registration.md:21-23); it becomes load-bearing only for table-only counter variants —
my w1 variant V8 — whose quotes/anchors legs trust the entry's cells.)

Span content re-verified: 573 = 12-space-indented `if (!keycode)`, 574 = 16-space-indented
`return {…"sendshortcut: key not found"…};`, 571 = scan-loop closing `}`, so the real span
does satisfy "after line 571". The side-claim itself is TRUE of the real span — it is only
non-discriminating.

Component uniqueness inside the pin (measured): `if (!keycode)` occurs **twice** (lines 573
and 579); `"sendshortcut: key not found"` occurs **once** (line 574). Quote occurrence
alone therefore entails neither the anchor (two windows) nor even the first component
(two sites); only the return line is unique. Pinning P22 requires the exact-span + exact-
anchor-cell check, not quote presence.

## 5. Consistency legs re-run this seat (all pass at base)

- **Pin digest (clause c, P22's pin):** sha256 at base = at HEAD = at worktree =
  `7248cbb8…fbe771` = registration.md:19. ✓
- **Propositions leg (table drift) for P22:** entry P22 row at base
  (`git show e25149fe…:corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`,
  row committed per my w1 §1 at `8d5c36adda17d27a866fd04484375015116297f2`) — its Quote
  cell is **byte-equal modulo trailing spaces** to registration.md:30's cell (both
  `sha256 b9b4aeebb508ceeb…`), its Pin:anchor cell is
  `Hyprland-legacy-DispatcherTranslator.cpp:573-574`, and the cell carries no trailing
  spaces (`cat -A` on both rows: `` `;` |$ ``). ✓ No drift.
- **Counter:** NOT RUN — absent (`ls quality/counters | grep -c r54` → `0`). No landed
  P22 judge exists to execute; per dispatch this is reported, not invented.

## 6. Relation to wave-1 evidence (cross-reference, not substitution)

- w1 `R54Seat03` (mine) Finding 1: same matrix for all four quotes (P22: A/B/E False,
  C/D True); w1 did not publish the B-mode space count, the window/side-claim ambiguity, or
  the uniqueness counts — all three are new here.
- w1 `R54Seat01:73-83` and `R54Seat02:84-123` (0 byte-exact occurrences; the "single
  logical lines" parenthetical is true of the entry cell, not of the pin bytes) —
  independent concurrence.
- w1 `R54Seat04:62-76`: span 573→574 MATCH, "after 571" EXACT — concurrence on the anchor.
- w1-results.json: R54Seat14 F1 (blocking): "Frozen quote judge is unsatisfiable by a
  faithful counter on real pins. Exact match (J0) admits C1 1/4"; R54Seat15 F1_C1_judge:
  "literal quotes 1/4 at base pins" — claim-wide statements; this seat supplies the P22-
  specific numbers behind them.

## 7. Verification log (exact commands → outputs → exits)

All commands run from a scratch cwd; git reads against the lane by `-C`; no lane file
written. Key measurements:

1. `git -C <lane> show e25149fe…:…/Hyprland-legacy-DispatcherTranslator.cpp | sha256sum` →
   `7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771  -`; same digest for
   `350d30e4…` blob and worktree file. exit 0.
2. `sed -n '569,576p' pin | cat -A` → bytes quoted in §2. exit 0.
3. `python3 -I p22_quant.py` → matrix §3 (A/B/E False, C/D True), windows
   `[(572,574),(573,574)]`, side-claim map `{572: True, 573: True}`, uniqueness 2/1,
   entry-cell byte-equality True. exit 0. (Script's printed "18" for the B-mode gap carries
   an off-by-one in its reporting line only; the correct separator after B is 17 spaces =
   1 substituted newline + 16 indent spaces, verifiable from the quoted raw-gap repr. The
   B=False verdict itself is a direct string comparison, unaffected.)
4. `ls quality/counters | grep -c r54` → `0`, exit 1 (counter absent).
5. `git -C <lane> rev-parse HEAD` → `350d30e4ec5531f65ce99a57efeb8216f38e678a`;
   `git status --porcelain` shows no file of this seat outside `.ufo/waves/round-54/w2/`.

Scratch `/fast/scratch/hyaku/mado-r54/R54W2Seat03` (script + pin extract only) was removed
before this yield; no ENOSPC encountered (scratch fs had 580G free at seat start); nothing
of mine remains under `/tmp`.

## 8. Verdict

**FALSIFIED for P22, judge-level (W2-03-A, blocking):** under the registered judge
(registration.md:51-53) the P22 quote cannot verify at a perfect tree — raw contiguity
fails in the anchor span and anywhere in the pin, and the registered normalization leaves
17 spaces where the quote has 1. The C1 target line (`quotes=4/4 … TARGET_MET`) is
reachable only by a counter that deviates from the frozen judge via an unregistered
normalization that no frozen control detects. **Anchor (W2-03-B, high):** the `573 > 571`
side-claim admits both collapse windows (572,574) and (573,574); only exact equality with
the frozen anchor cell pins the span. Pin digest, table-drift, and span-content legs all
hold at base; the defect is in the frozen judge wording alone. Per claims-frozen.md:5-7 the
remedy is an honest stop or a pre-data v2 re-registration declaring the real judge — not an
edit, and nothing was edited.

Report: .ufo/waves/round-54/w2/R54W2Seat03.md
