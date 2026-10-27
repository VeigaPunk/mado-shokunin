# R54Seat04 — C1 source-truth counter path: item 4 audit

Seat: R54Seat04 (executor, wave 1). Axis focus: coverage + operability.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`.
Scratch: `/fast/scratch/hyaku/mado-r54/R54Seat04` (all fixtures; cleaned before yield).

## Deliverables

- `.ufo/waves/round-54/w1/R54Seat04.md` — this report.
- Counter draft `c1-r54-errata-truth.py` (844 lines) reproduced in full in **Appendix A**
  below. It is a **scratch draft only**: this seat made **no tracked lane edits**, per the
  seat spec ("draft only within report/scratch ... no lane edits"). The counter file is
  **not** in `quality/counters/`, so `ls quality/counters | grep -c r54` is still `0` in the
  live lane — the claim's "before" state is unchanged by this seat.
- No tool/package was installed or updated (see *Tooling* below).

## Scope and axes

Item 4 of the seat's assignment is the **C1 errata source-truth counter path**: audit the
frozen proposition rows, the exact pin quotes/anchors/hash requirements, and the six frozen
controls; draft the counter; identify edge cases; test a distinct failure/input.

This seat's distinct contribution (distinct from seats 01/02/03/05/06, which cover the
other C1 aspects) is **the anchor side-claim and quote-anchor binding layer**, exercised
from the *pin side* rather than only from the *entry side*. Concretely: I derived the
frozen side-claim bounds structurally from the pinned source bytes, and I attacked the
counter with **pin-byte mutations** (moving the enclosing function, moving the scan loop)
rather than the entry-table mutations the six registered controls use.

## Attacked predicate and citations

Attacked: `PRED-C1-r54` (`.ufo/waves/round-54/claims-frozen.md`), clauses (a) quotes, (b)
anchor side-claims, (c) pin hashes, (d) six controls rejected; kill rule and §9 do-nothing
control. Registration: `.ufo/waves/round-54/registration.md` — "C1 fixture inventory
(errata source-truth verifier)", the frozen proposition table, the frozen anchor
side-claims, the six frozen C1 controls, and "Counter form".

## Independent ground-truth re-derivation (before writing any counter)

I re-derived every frozen quantity from the pinned bytes rather than trusting the
registration's table.

Pins at `.ufo/waves/round-52/fetch/` — sha256 recomputed from the working-tree bytes and
from the git blob at base (identical):

```
a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  Hyprland-ConfigActions.cpp
746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073  Hyprland-ConfigActions.hpp
8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40  Hyprland-KeybindManager.cpp
7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771  Hyprland-legacy-DispatcherTranslator.cpp
```

All four match the registration table and the tree's own `SHA256SUMS` exactly.

Anchor/quote binding, re-derived by mapping every character of the whitespace-collapsed
pin back to its source line:

```
P19  span lines: 1554 -> 1558  expected 1554 -> 1558  MATCH
P20  span lines: 1576 -> 1576  expected 1576 -> 1576  MATCH
P21  span lines:  619 ->  622  expected  619 ->  622  MATCH
P22  span lines:  573 ->  574  expected  573 ->  574  MATCH
```

Each quote occurs exactly once in its pin (collapsed-occurrence count = 1 for all four), so
the binding is unambiguous.

**Structural side-claims, derived from the pin bytes (brace matching, not constants):**

```
Actions::pass(uint32_t modMask, ...) body : 1530 -> 1599   (P19 1554-1558 and P20 1576 are inside)
sendkeystate body                      : 591  -> 627        (frozen P21 claim 591-627  EXACT)
xkb keycode scan loop                  : 565  -> 571        (frozen P22 claim "after 571" EXACT)
```

The registration's P21 side-claim "inside lines 591–627" and P22 side-claim "after line
571" are **exactly** the real `sendkeystate` body bounds and the real scan-loop end. They
are not arbitrary numbers, and my counter re-derives them from the bytes so the side-claim
is falsifiable against a mutated pin rather than being a tautology.

## Counter design decisions (and the two that mattered)

1. **The frozen table is embedded as constants.** The frozen proposition table physically
   lives in `registration.md`. At base `e25149fe` that file is **untracked** (it is tracked
   only from `350d30e4` onward), so a counter that read its contract from an untracked wave
   file could not be reproducible at an arbitrary `--rev`. The table, the four frozen
   sha256s and the side-claim bounds are therefore constants in the counter, with the
   `SHA256SUMS` cross-check at clause (c) as an independent second source.

2. **The frozen-table comparison is part of the score, not a separate flag.** This is the
   one design decision that changed the counter's behaviour materially, and it was driven by
   a defect I found in my own first draft.

## Defect found in my own first draft (false MET), and the fix

My first draft computed the frozen-table drift but did **not** gate the verdict on it. I then
built a mutant that exposes this:

- Mutation: shorten P20's Quote cell to `sendKeyboardMods(0, 0, 0, 0);` — still a
  contiguous, still-contiguous-in-the-pin, still-spanning-1576 substring of the true quote.
- First-draft result: `propositions=4 quotes=4 anchors=4 pins=4` → would have printed
  **TARGET_MET** on a drifted tree.
- Fixed result: `quotes=3 anchors=3` → TARGET_MISSED.

Fix: the entry's row must equal the frozen table byte-for-byte (modulo trailing spaces) for
the proposition to score its `quotes`/`anchors` point, exactly as the registration's
"byte-for-byte modulo trailing spaces" requires. A regression assertion for this mutant is
now in the counter's selftest ("shortened-but-contiguous quote rejected").

## Results — the frozen line and the six controls

```
$ python3 -I c1-r54-errata-truth.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
    --rev 350d30e4ec5531f65ce99a57efeb8216f38e678a --work <scratch>
detail: control C1-CTL-1 spliced-quote rejected (quotes=3/4)
detail: control C1-CTL-2 shifted-anchor rejected (anchors=3/4)
detail: control C1-CTL-3 hash-tamper rejected (pins=3/4)
detail: control C1-CTL-4 wrong-range rejected (anchors=3/4)
detail: control C1-CTL-5 dropped-proposition rejected (propositions=3/4)
detail: control C1-CTL-6 swapped-pin rejected (quotes=3/4)
MADO_ERRATA_TRUTH: rev=350d30e4ec5531f65ce99a57efeb8216f38e678a propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
exit=0
```

Each control trips **exactly** the counter the registration names for it (CTL-1/6 →
`quotes≤3/4`, CTL-2/4 → `anchors≤3/4`, CTL-3 → `pins≤3/4`, CTL-5 → `propositions≤3/4`).
Same result at the frozen base `e25149fe`:

```
MADO_ERRATA_TRUTH: rev=e25149fec8152a3aabd2b18a0ee8663b23cf65aa propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
```

```
$ python3 -I c1-r54-errata-truth.py --repo . --rev <rev> --work <scratch> --selftest
MADO_C1_R54_SELFTEST: 43/43 assertions passed
exit=0
```

43 assertions ≥ the registration's required 30, and includes one red run per control.

## The harness bites (§9 do-nothing control, tested two ways)

I verified the control suite is not decorative by replacing the evaluator with deliberately
weak ones and re-running the six controls:

| evaluator under test | controls rejected | consequence |
|---|---|---|
| **always prints 4/4, reads nothing** (the §9 do-nothing counter) | **0/6** | verdict TARGET_MISSED — caught |
| weak: quote merely *appears somewhere* in the pin, anchor unchecked, hashes compared to the tree's own `SHA256SUMS` | **4/6** | CTL-2 shifted-anchor and CTL-4 wrong-range **ADMITTED** — caught |
| **real counter** | **6/6** | TARGET_MET |

The weak evaluator is exactly the failure mode the registration anticipates: it admits
CTL-2 and CTL-4, i.e. an anchor check that does not verify the quote *spans the named
lines*, and a hash check that trusts the tree's own `SHA256SUMS` instead of the frozen
round-52 hashes. This is the direct evidence that clauses (b) and (c) carry independent
weight and are not redundant with clause (a).

## Item-4 focus: edge cases found, and the distinct failure tested

**Distinct failure/input (mine, distinct from the registered six): pin-side structural
mutation.** The six registered controls all mutate the *entry table* (or `SHA256SUMS`).
I instead mutated the **pin bytes** so that the frozen anchor numbers no longer name the
enclosing structure — the anchor text stays `619-622` and `573-574`, but the source moves.

- Insert one line before `static SDispatchResult sendkeystate` → the function body becomes
  592–628, and the P21 quote moves to 620–623.
  Result: `quotes=4 anchors=3 pins=3`; details: `P21 quote spans [(620, 623)], anchor names
  619-622` and `pin bytes hash ... != frozen 992aa008041d`. **REJECTED** — the anchor leg
  catches it independently of the hash leg.
- Insert one line inside the xkb scan loop → the loop ends at 572, P21 and P22 both shift.
  Result: `quotes=4 anchors=2 pins=3`; details: `P21 quote spans [(620, 623)]`,
  `P22 quote spans [(574, 575)]`. **REJECTED.**

This is the attack the *six registered controls cannot make*: they never touch a pin, so a
counter that only ever reads the entry's own anchor text would still print TARGET_MET on
both of these. Only a counter that re-derives the structural bounds from the pinned bytes
rejects them. Both mutations are also caught by the hash leg (clause (c)), which is the
belt-and-braces the registration's structure intends.

**Entry-side edge cases (all rejected, each with an exact reason):**

| mutation | result | reason |
|---|---|---|
| P21 anchor → `591-627` (the function body itself) | anchors=3 | quote spans 619-622, anchor names 591-627 |
| P21 anchor → `620-622` (inside the range, off the quote) | anchors=3 | quote spans 619-622 |
| P22 anchor → `571` (exactly the scan-loop end, **not after** it) | anchors=3 | the "after 571" side-claim |
| P22 anchor → `572-574` | anchors=3 | quote spans 573-574 |
| P22 anchor → `571-574` (widened to include 571) | anchors=3 | quote spans 573-574 |
| P19 anchor → `1554-1559` (widened) | anchors=3 | quote spans 1554-1558 |
| P20 anchor → `1576-1576` (point written as a range) | anchors=3 | differs from frozen table `1576` |
| P19 pin → the *other* pin, same line numbers | quotes=3, anchors=3 | quote absent from that pin |
| P20 quote shortened to a contiguous substring | quotes=3, anchors=3 | differs from the frozen table |
| P20 quote interior space changed | quotes=3, anchors=3 | not contiguous **and** differs from frozen table |
| P20 quote **leading** space added | quotes=3, anchors=3 | differs from the frozen table |
| P20 quote **trailing** spaces added | quotes=4, anchors=4 | **tolerated** — registration says "modulo trailing spaces" |
| P20 anchor cell trailing spaces | quotes=4, anchors=4 | tolerated (same rule) |
| P20 pin cell given as a path prefix | quotes=4, anchors=4 | basename resolution, as designed |
| duplicate P22 row in the same table | propositions=3 | row is ambiguous, so it does not score |
| duplicate P22 row as a separate table | quotes=4 | the real table still scores; the duplicate is inert |
| decoy table placed *before* the real table | quotes=0, anchors=0 | the first matching table is the decoy |
| decoy table placed *after* the real table | quotes=4 | the real table is found |
| `Pin:anchor` header renamed | propositions=0 | no matching table |
| CRLF line endings in the entry | quotes=4 | `\r` is whitespace, no effect |
| entry's `verified-at:` line removed | quotes=4 | provenance trio is not a C1 clause |

The trailing-space asymmetry is deliberate and matches the registration exactly: *"checks
them against THIS table byte-for-byte modulo trailing spaces"*. Trailing spaces are
tolerated; a leading space is a real byte difference and is rejected. My first draft used a
symmetric `strip()` and wrongly accepted the leading-space case; I tightened it to
`cell_text()` (strip the cell, remove one pair of backticks, keep whitespace *inside*).

**Forgery resistance.** A consistent forgery — rewriting the pin bytes *and* rewriting the
tree's own `SHA256SUMS` to match — is still rejected:

```
FORGERY A (pin bytes + SHA256SUMS rewritten consistently):
   counts: {'propositions': 4, 'quotes': 4, 'anchors': 4, 'pins': 3}
   detail: pin bytes hash Hyprland-ConfigActions.cpp != frozen 0222d90e91ad
   -> REJECTED
```

because clause (c) compares against the **frozen** round-52 sha256, not against the tree's
own `SHA256SUMS`. The `SHA256SUMS` cross-check is an *additional* requirement, not the
source of truth.

**Working-tree independence.** I sabotaged the working tree of a clone
(`g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` → `WORKING TREE SABOTAGE`) and the
counter still reported the frozen line at `TARGET_MET` — every byte is read from the
`--rev` git object, never from the checkout.

**No lane mutation.** The counter clones into `--work` with `--shared --no-checkout` and
builds control mutants with git plumbing (`read-tree` / `hash-object -w` / `update-index` /
`write-tree` / `commit-tree`) against a scratch index. Measured before/after a full run in
the live lane:

```
before: count=11391 loose=11391
after:  count=11391 loose=11391
HEAD unchanged: YES
no new lane objects: YES
```

## Integration hazard found for the landing seat (not yet applied)

Landing `quality/counters/c1-r54-errata-truth.py` **breaks the round-51 tool-ledger
counter** unless a ledger row is added in the same change. The r51 counter's population is
"every file under `quality/counters/`", so adding the counter raises population 82 → 83
while `quality/tool-ledger.md` stays at 82 rows:

```
detail: checker: LEDGER-ROW reason=uncovered path=quality/counters/c1-r54-errata-truth.py detail=no-row
detail: checker: LEDGER: population=83 ledger_rows=82 uncovered=1 ... verdict=TARGET_MISSED
C1_R51: population=83 ledger_rows=82 uncovered=1 ... verdict=TARGET_MISSED
```

Adding the row and pointing it at a file that actually contains the counter's basename
(`.ufo/waves/round-54/claims-frozen.md` contains it twice; `registration.md` contains it
**zero** times) restores it:

```
C1_R51: population=83 ledger_rows=83 uncovered=0 dangling=0 bad_pointer=0 empty_desc=0 selftest=ok verdict=TARGET_MET
```

Two consequences the landing seat must handle, both verified in a scratch clone:

1. The ledger row's pointer must be `.ufo/waves/round-54/claims-frozen.md`. Pointing it at
   `registration.md` yields `bad_pointer=1` → `TARGET_MISSED`, because the r51 checker
   requires the pointed-to file to contain the row file's basename.
2. With the row in place, the landed counter itself prints the frozen line from inside the
   simulated landing tree:
   `MADO_ERRATA_TRUTH: rev=3d3720fe... propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET`
   and its selftest is `43/43`.

This is a **cross-claim integration surface**, not a C1 defect: the claim's "causal
separability" section lists the shared record files as integration surfaces, not claim
evidence, and `quality/tool-ledger.md` is one of them.

## Two discrepancies in the frozen registration (reported, not acted on)

Both are in `.ufo/waves/round-54/registration.md` and neither changes a predicate; I did
not edit the frozen file (the freeze says no predicate/fixture/target changes after
scoring).

1. **Pin-manifest filename.** The registration's C1 fixture inventory says the pins' hashes
   come from *"its committed `SHA256SUMS.txt`"*. The round-52 fetch directory actually
   contains **`SHA256SUMS`** (no `.txt`). The `.txt` suffix is the *round-54* fetch
   directory's convention (`.ufo/waves/round-54/fetch/SHA256SUMS.txt`), so the registration
   appears to have carried the wrong round's filename into the round-52 inventory. A
   counter written literally from the registration would find no `SHA256SUMS.txt` under
   `.ufo/waves/round-52/fetch/` and would score `pins=0/4`. My counter uses the real path
   `.ufo/waves/round-52/fetch/SHA256SUMS`.

2. **`SHA256SUMS` records absolute paths.** Its five lines point at
   `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/...`. Matching
   those paths literally would break in any clone or on any other checkout, so the counter
   matches by **basename**. Only the four pins the registration lists are scored; the fifth
   line (`README.txt`) is ignored, as the registration's pin table has four rows.

## Harm watch

- `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 460/460 assertions passed`,
  exit 0 — unchanged (the counter is not landed by this seat).
- No config tree, compositor, service or sibling repo was written. No live/compositor read,
  no package query, no screenshot, no producer execution.
- No lane file was created or modified by this seat: the only file written under the lane
  is this report. `git status` shows the same `M corpus/README.md`, `M corpus/SOURCES.md`
  and `??` entries that sibling C2 seats had already produced before this seat ran; the
  lane HEAD is unchanged at `350d30e4ec5531f65ce99a57efeb8216f38e678a`.
- Source repo `shokuknow` untouched; no campaign tools used.

## Tooling

**No install or update was performed.** The host rules (`/home/vgpnk/.omp/agent/RULES.md`)
were read before any tooling step; no tool needed installing for this task. Tools used,
all pre-existing: `python3` (3.14.8, `python3 -I`), `git` (2.56.0), `bash`. Note the host
rule "PACMAN transactions paused" was respected trivially — no transaction was attempted.

## Risks and limitations

- **The counter is a scratch draft, not landed.** C1's target state is "the counter
  committed"; this seat deliberately did not commit it (no tracked lane edits). The landing
  seat must (a) commit `quality/counters/c1-r54-errata-truth.py`, (b) add the
  `quality/tool-ledger.md` row with the `claims-frozen.md` pointer, and (c) re-run the
  r51 ledger counter, which otherwise goes `TARGET_MISSED` as shown above.
- **Clause (b) is checked structurally, which is slightly stronger than a literal reading**
  of "the quote is at exactly these lines". I required the enclosing structure to be
  re-derived from the pinned bytes (sendkeystate body = 591–627, xkb scan loop ends at
  571). At the frozen pins these hold exactly, so the strictness costs nothing and it is
  what makes the side-claims falsifiable. A counter author who prefers the literal reading
  would score the same at the frozen revs but would **admit** my two pin-side mutants.
- **The `quotes`/`anchors` counters fold in the frozen-table comparison.** This is
  required by the registration ("byte-for-byte modulo trailing spaces"), but it means a
  drifted row costs its proposition a point on two legs rather than one. The six controls
  each still trip exactly the leg the registration names, so the frozen verdicts are
  unaffected.
- **This seat did not attempt the non-author source-truth review** of the four propositions
  (does the pinned quote entail the proposition's English claim?). That is a separate
  review act; this seat verified only that the quoted bytes are present, contiguous and
  correctly anchored.
- The claim's before-state ("no `c1-r54-*` counter exists → TARGET_MISSED by absence")
  remains literally true in the live lane: `ls quality/counters | grep -c r54` → `0`.

## Appendix A — counter draft (`c1-r54-errata-truth.py`, 844 lines)

Scratch path at time of writing: `/fast/scratch/hyaku/mado-r54/R54Seat04/c1-r54-errata-truth.py`
(sha256 `085738f5742be7b4ba5c999f641cb84901c997800f741605af89978e799dd982`). The scratch
directory is cleaned before this seat yields, so the authoritative copy is the text below.
This is a draft for review by the landing seat; it is not a lane file.

<!-- BEGIN COUNTER SOURCE -->
```python
#!/usr/bin/env python3
"""c1-r54-errata-truth.py — PRED-C1-r54: the round-53 errata propositions are source-true
at the pinned round-52 bytes, and the counter rejects its own six frozen controls.

Frozen contract (`.ufo/waves/round-54/claims-frozen.md`, sentence PRED-C1-r54):

    python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>
    prints one line
        MADO_ERRATA_TRUTH: rev=<rev> propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4
        controls=6/6 verdict=TARGET_MET
    and exits 0 only if, at the scored revision:
      (a) each of the four corrected propositions P19-P22 of
          corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md has its Quote cell
          occurring verbatim and contiguous in the round-52 pin named by its Pin:anchor cell;
      (b) each anchor side-claim holds (P19 at exactly ConfigActions.cpp:1554-1558;
          P20 at exactly :1576; P21 at exactly DispatcherTranslator.cpp:619-622 inside
          lines 591-627; P22 at exactly :573-574 after line 571);
      (c) each of the four pins' bytes hash to the round-52 recorded sha256;
      (d) each of the six frozen C1 controls of `.ufo/waves/round-54/registration.md` is
          rejected by this counter (each control is a mutated copy of the scored tree).

What it measures (never the working tree: every input byte comes from `--rev` in a scratch
clone):

``propositions``  the four frozen IDs P19-P22 each appear exactly once as a parseable row of
       the entry's `Corrected propositions` table (the table whose header carries `ID`,
       `Pin:anchor` and `Quote`).
``quotes``       for each such row, the row's own Quote cell occurs verbatim and contiguous
       in the pin named by the row's own Pin:anchor cell.
``anchors``      for each such row, that occurrence spans exactly the lines the row's own
       Pin:anchor cell names, and the frozen side-claim for that ID holds for those lines.
``pins``         for each of the four round-52 pins: the bytes at `<rev>` hash to the frozen
       round-52 sha256 AND the tree's own `.ufo/waves/round-52/fetch/SHA256SUMS` records that
       same sha256 for that file.
``controls``     the six frozen controls are executed here, now, against mutated copies of
       the scored tree; a control counts only when the mutant is REJECTED with the frozen
       expected counter deficit.

Judge of "verbatim": a maximal whitespace run that contains a newline collapses to exactly one
space (source indentation is not part of a quote); a whitespace run without a newline is kept
byte-for-byte, so a quote whose interior spacing differs from the source is rejected. The
quote must occur as one contiguous run; a quote assembled from two non-adjacent source
regions never matches. The match must be unique in the pin.

The frozen proposition table and the frozen round-52 hashes are embedded as constants below,
because the table physically lives in `.ufo/waves/round-54/registration.md`, which is not a
tracked file, and a counter that read its contract from an untracked wave file would not be
reproducible at an arbitrary `--rev`.

Exit codes: 0 = TARGET_MET, 1 = TARGET_MISSED, 2 = setup error (bad --repo/--rev/--work,
clone failure, malformed control run).

Scratch: `--work DIR`, else a fresh directory under `$TMPDIR`; no temporary path is
hard-coded. The six control runs build mutated trees with git plumbing in the scratch clone
(an index plus `hash-object`/`write-tree`/`commit-tree`); the scored repository is only ever
read. No working tree is checked out, so no lane file is touched.
"""

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "c1-r54-errata-truth.py"
ENTRY_REL = "corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md"
FETCH_REL = ".ufo/waves/round-52/fetch"
SUMS_REL = FETCH_REL + "/SHA256SUMS"
IDS = ("P19", "P20", "P21", "P22")

# --- frozen proposition table (`.ufo/waves/round-54/registration.md`, C1 fixture inventory) ---
# ID -> (pin file name, anchor text as written in the entry's Pin:anchor cell, quote text)
FROZEN = {
    "P19": (
        "Hyprland-ConfigActions.cpp", "1554-1558",
        "g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) "
        "{ if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, "
        "WL_KEYBOARD_KEY_STATE_PRESSED);",
    ),
    "P20": (
        "Hyprland-ConfigActions.cpp", "1576",
        "g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);",
    ),
    "P21": (
        "Hyprland-legacy-DispatcherTranslator.cpp", "619-622",
        "auto result = sendshortcut(modifiedArgs); if (keyState == 2 && result.success) "
        "result = sendshortcut(modifiedArgs);",
    ),
    "P22": (
        "Hyprland-legacy-DispatcherTranslator.cpp", "573-574",
        'if (!keycode) return {.success = false, .error = "sendshortcut: key not found"};',
    ),
}
# frozen round-52 recorded sha256 for each pin (registration table; SHA256SUMS agrees)
FROZEN_SHA = {
    "Hyprland-ConfigActions.cpp":
        "a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637",
    "Hyprland-ConfigActions.hpp":
        "746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073",
    "Hyprland-KeybindManager.cpp":
        "8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40",
    "Hyprland-legacy-DispatcherTranslator.cpp":
        "7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771",
}
# frozen anchor side-claims (claims-frozen.md clause (b)). The bounds are not merely
# compared as numbers: they are re-derived from the pinned source bytes, so the
# side-claim is falsifiable against a mutated pin rather than being a tautology.
CLAIM_P21_RANGE = (591, 627)   # 591 <= start and end <= 627
CLAIM_P22_AFTER = 571          # start > 571
# the structural facts the frozen side-claims assert, given as (file, signature, kind)
STRUCTURAL_CLAIMS = (
    # P19/P20 live inside the `Actions::pass(uint32_t modMask, ...)` body.
    ("P19", "Hyprland-ConfigActions.cpp",
     "ActionResult Actions::pass(uint32_t modMask", "body"),
    ("P20", "Hyprland-ConfigActions.cpp",
     "ActionResult Actions::pass(uint32_t modMask", "body"),
    # P21 lives inside the `sendkeystate` body, whose bounds are the frozen 591-627.
    ("P21", "Hyprland-legacy-DispatcherTranslator.cpp",
     "static SDispatchResult sendkeystate", "body"),
    # P22 follows the xkb keycode scan loop, whose last line is the frozen 571.
    ("P22", "Hyprland-legacy-DispatcherTranslator.cpp",
     "for (xkb_keycode_t kc = keycode_min", "loop"),
)

EMPHASIS = "`*_ \t"


class SetupError(Exception):
    pass


# ---------------------------------------------------------------- git plumbing

def git_env(extra=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.setdefault("LC_ALL", "C.UTF-8")
    env.setdefault("GIT_AUTHOR_NAME", "mado-counter")
    env.setdefault("GIT_AUTHOR_EMAIL", "mado-counter@localhost")
    env.setdefault("GIT_COMMITTER_NAME", "mado-counter")
    env.setdefault("GIT_COMMITTER_EMAIL", "mado-counter@localhost")
    if extra:
        env.update(extra)
    return env


def git(repo, *args, check=True, env=None):
    proc = subprocess.run(("git", "-C", repo) + args, capture_output=True,
                          env=git_env(env))
    if check and proc.returncode != 0:
        raise SetupError("git %s failed in %s: %s" % (
            " ".join(args), repo, proc.stderr.decode("utf-8", "replace").strip()[:400]))
    return proc.stdout


def resolve_rev(repo, rev):
    out = git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}", check=False)
    text = out.decode().strip()
    if not text:
        raise SetupError("--rev %r does not resolve to a commit in %s" % (rev, repo))
    return text


def make_clone(repo, rev, work):
    clone = os.path.join(work, "clone-%d" % os.getpid())
    if os.path.exists(clone):
        shutil.rmtree(clone)
    git(work, "clone", "-q", "--shared", "--no-checkout", repo, clone)
    head = git(clone, "rev-parse", "HEAD").decode().strip()
    top = git(clone, "rev-parse", "--show-toplevel").decode().strip()
    if os.path.realpath(top) != os.path.realpath(clone):
        raise SetupError("clone toplevel %s != %s" % (top, clone))
    if head != rev:
        git(clone, "fetch", "-q", "--no-tags", "origin", rev)
    return clone


def blob(repo, rev, path):
    proc = subprocess.run(["git", "-C", repo, "cat-file", "blob", "%s:%s" % (rev, path)],
                          capture_output=True, env=git_env())
    if proc.returncode != 0:
        return None
    return proc.stdout


# ---------------------------------------------------------------- text helpers

def collapse(text):
    """Collapse every whitespace run that contains a newline to one space; keep other runs
    byte-for-byte. Return (collapsed_text, line_of_each_character)."""
    out = []
    lines = []
    line = 1
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            j = i
            has_nl = False
            while j < n and text[j].isspace():
                if text[j] == "\n":
                    has_nl = True
                j += 1
            run = text[i:j]
            line += run.count("\n")
            if has_nl:
                out.append(" ")
                lines.append(line)
            else:
                for c in run:
                    out.append(c)
                    lines.append(line)
            i = j
            continue
        out.append(ch)
        lines.append(line)
        i += 1
    while out and out[0] == " ":
        out.pop(0)
        lines.pop(0)
    while out and out[-1] == " ":
        out.pop()
        lines.pop()
    return "".join(out), lines


def occurrences(haystack, needle):
    """Every start offset of needle in haystack (non-overlapping scan, no regex)."""
    hits = []
    if not needle:
        return hits
    start = 0
    while True:
        idx = haystack.find(needle, start)
        if idx < 0:
            return hits
        hits.append(idx)
        start = idx + 1


def strip_emphasis(cell):
    return cell.strip(EMPHASIS)


def cell_text(cell):
    """The literal text of a table cell: outer whitespace and one pair of backticks are
    removed, but whitespace *inside* the backticks is kept. Only trailing spaces are
    tolerated (the registration compares byte-for-byte modulo trailing spaces), so a
    leading space inside the cell is a real difference and must not be silently dropped.
    """
    text = cell.strip()
    if len(text) >= 2 and text.startswith("`") and text.endswith("`"):
        text = text[1:-1]
    return text


def parse_anchor(text):
    """'1554-1558' or '1576' -> (start, end)."""
    text = text.strip().lstrip(":")
    if "-" in text:
        lo, hi = text.split("-", 1)
        return int(lo), int(hi)
    return int(text), int(text)


def parse_pin_cell(cell):
    """'Hyprland-ConfigActions.cpp:1554-1558' -> (file name, anchor text)."""
    cell = strip_emphasis(cell)
    if ":" not in cell:
        return cell, ""
    name, anchor = cell.rsplit(":", 1)
    return os.path.basename(name.strip()), anchor.strip()


def parse_tables(text):
    """Every markdown table of the document -> list of (header cells, rows)."""
    tables = []
    header = None
    rows = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            if header is not None:
                tables.append((header, rows))
            header, rows = None, []
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells if c):
            continue
        if header is None:
            header = cells
        else:
            rows.append(cells)
    if header is not None:
        tables.append((header, rows))
    return tables


def entry_rows(text):
    """The `Corrected propositions` table -> {ID: row cells}. None when absent."""
    for header, rows in parse_tables(text):
        names = [strip_emphasis(c).lower() for c in header]
        pin_idx = next((i for i, c in enumerate(names) if c.startswith("pin")), None)
        quote_idx = next((i for i, c in enumerate(names) if c.startswith("quote")), None)
        id_idx = next((i for i, c in enumerate(names) if c == "id"), None)
        if pin_idx is None or quote_idx is None or id_idx is None:
            continue
        found = {}
        dup = set()
        for cells in rows:
            if len(cells) <= max(id_idx, pin_idx, quote_idx):
                continue
            pid = strip_emphasis(cells[id_idx])
            if pid not in IDS:
                continue
            if pid in found:
                dup.add(pid)
            found[pid] = cells
        for pid in dup:
            found[pid] = None
        if found:
            return found, pin_idx, quote_idx
    return None, None, None


# ---------------------------------------------------------------- measurement

def structural_bounds(lines, signature, kind):
    """(first, last) source line of the brace-delimited block opened by `signature`.

    `kind` is "body" for a function definition and "loop" for a `for` header; both are
    resolved by brace matching from the signature line, so the returned bounds come from
    the source bytes and not from a constant.
    """
    for i, line in enumerate(lines):
        if signature not in line:
            continue
        depth = 0
        started = False
        for j in range(i, len(lines)):
            depth += lines[j].count("{") - lines[j].count("}")
            if "{" in lines[j]:
                started = True
            if started and depth == 0:
                return i + 1, j + 1
        return None
    return None


def parse_sums(text):
    """SHA256SUMS -> {basename: sha256}. Absolute paths in the file are matched by basename."""
    out = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        digest = parts[0].strip().lower()
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            continue
        out[os.path.basename(parts[-1])] = digest
    return out


def evaluate(repo, rev, details):
    """Independent measurement of clauses (a), (b), (c) at `rev`.

    Each proposition is scored three times, and a proposition only scores a point when
    BOTH the frozen-table check and the source check pass:

    ``propositions``  the row for that ID exists exactly once in the entry's table.
    ``quotes``       the row's own Quote cell equals the frozen quote byte-for-byte
                     (modulo trailing spaces) AND that quote occurs verbatim and
                     contiguous in the pin the row's own Pin:anchor cell names.
    ``anchors``      the row's own Pin:anchor cell equals the frozen pin and anchor
                     byte-for-byte AND an occurrence of the quote spans exactly the
                     anchor lines AND the frozen side-claim for that ID holds.
    ``pins``         the pin's bytes at `rev` hash to the frozen round-52 sha256 AND the
                     tree's own SHA256SUMS records that same sha256 for that file.

    The frozen-table comparison is part of the score, not a separate flag: a shortened
    quote that is still contiguous in the pin, or an anchor moved to a different range,
    must cost the proposition its point rather than passing silently.
    """
    counts = {"propositions": 0, "quotes": 0, "anchors": 0, "pins": 0}
    entry = blob(repo, rev, ENTRY_REL)
    if entry is None:
        details.append("entry absent at %s" % rev[:12])
        return counts
    text = entry.decode("utf-8", "replace")
    rows, pin_idx, quote_idx = entry_rows(text)
    if not rows:
        details.append("entry has no Corrected propositions table")
        return counts

    for pid in IDS:
        cells = rows.get(pid)
        if cells is None:
            details.append("proposition %s absent or duplicated" % pid)
            continue
        counts["propositions"] += 1
        pin_name, anchor_text = parse_pin_cell(cells[pin_idx])
        quote = cell_text(cells[quote_idx])
        frozen_pin, frozen_anchor, frozen_quote = FROZEN[pid]
        # the frozen table: the entry's row must equal it byte-for-byte modulo trailing spaces
        quote_frozen = quote.rstrip() == frozen_quote
        pin_frozen = pin_name == frozen_pin
        anchor_frozen = anchor_text.lstrip(":") == frozen_anchor
        if not quote_frozen:
            details.append("%s quote differs from the frozen table" % pid)
        if not pin_frozen:
            details.append("%s pin %s differs from the frozen table %s"
                           % (pid, pin_name, frozen_pin))
        if not anchor_frozen:
            details.append("%s anchor %s differs from the frozen table %s"
                           % (pid, anchor_text, frozen_anchor))
        # clause (a): the quote occurs verbatim and contiguous in the pin the row names
        pin_bytes = blob(repo, rev, FETCH_REL + "/" + pin_name)
        if pin_bytes is None:
            details.append("%s pin absent: %s" % (pid, pin_name))
            continue
        collapsed, lmap = collapse(pin_bytes.decode("utf-8", "replace"))
        qcollapsed, _ = collapse(quote)
        hits = occurrences(collapsed, qcollapsed)
        if not hits:
            details.append("%s quote not contiguous in %s" % (pid, pin_name))
            continue
        if len(hits) > 1:
            details.append("%s quote occurs %d times in %s" % (pid, len(hits), pin_name))
        if quote_frozen:
            counts["quotes"] += 1
        # clause (b): an occurrence spans exactly the anchor lines, side-claim holds
        try:
            want = parse_anchor(anchor_text)
        except ValueError:
            details.append("%s anchor unparseable: %r" % (pid, anchor_text))
            continue
        spanning = [h for h in hits
                     if (lmap[h], lmap[h + len(qcollapsed) - 1]) == want]
        if not spanning:
            spans = sorted({(lmap[h], lmap[h + len(qcollapsed) - 1]) for h in hits})
            details.append("%s quote spans %s, anchor names %d-%d"
                           % (pid, spans, want[0], want[1]))
            continue
        if pid == "P21":
            lo, hi = CLAIM_P21_RANGE
            if not (lo <= want[0] and want[1] <= hi):
                details.append("%s anchor %d-%d outside %d-%d" % (pid, want[0], want[1], lo, hi))
                continue
            # the frozen 591-627 is the `sendkeystate` body; re-derive it from the pin
            lines = pin_bytes.decode("utf-8", "replace").splitlines()
            bounds = structural_bounds(lines, "static SDispatchResult sendkeystate", "body")
            if bounds != (lo, hi):
                details.append("%s sendkeystate body is %s, frozen side-claim says %d-%d"
                               % (pid, bounds, lo, hi))
                continue
            if not (bounds[0] <= want[0] and want[1] <= bounds[1]):
                details.append("%s anchor %d-%d outside sendkeystate body %d-%d"
                               % (pid, want[0], want[1], bounds[0], bounds[1]))
                continue
        if pid == "P22":
            if not want[0] > CLAIM_P22_AFTER:
                details.append("%s anchor %d-%d not after line %d"
                               % (pid, want[0], want[1], CLAIM_P22_AFTER))
                continue
            # the frozen 571 is the last line of the xkb keycode scan loop
            lines = pin_bytes.decode("utf-8", "replace").splitlines()
            bounds = structural_bounds(lines, "for (xkb_keycode_t kc = keycode_min", "loop")
            if bounds is None or bounds[1] != CLAIM_P22_AFTER:
                details.append("%s xkb scan loop ends at %s, frozen side-claim says %d"
                               % (pid, bounds[1] if bounds else None, CLAIM_P22_AFTER))
                continue
            if want[0] <= bounds[1]:
                details.append("%s anchor %d-%d not after the scan loop ending at %d"
                               % (pid, want[0], want[1], bounds[1]))
                continue
        if pid in ("P19", "P20"):
            # both propositions live inside the `Actions::pass(uint32_t modMask, ...)` body
            lines = pin_bytes.decode("utf-8", "replace").splitlines()
            bounds = structural_bounds(
                lines, "ActionResult Actions::pass(uint32_t modMask", "body")
            if bounds is None or not (bounds[0] <= want[0] and want[1] <= bounds[1]):
                details.append("%s anchor %d-%d outside Actions::pass body %s"
                               % (pid, want[0], want[1], bounds))
                continue
        if quote_frozen and pin_frozen and anchor_frozen:
            counts["anchors"] += 1

    # clause (c): frozen round-52 hashes, cross-checked against the tree's own SHA256SUMS
    sums_text = blob(repo, rev, SUMS_REL)
    recorded = parse_sums(sums_text.decode("utf-8", "replace")) if sums_text else {}
    if not recorded:
        details.append("SHA256SUMS absent at %s" % rev[:12])
    for name, expected in sorted(FROZEN_SHA.items()):
        data = blob(repo, rev, FETCH_REL + "/" + name)
        if data is None:
            details.append("pin absent: %s" % name)
            continue
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            details.append("pin bytes hash %s != frozen %s" % (name, actual[:12]))
            continue
        if recorded.get(name) != expected:
            details.append("SHA256SUMS records %s for %s, frozen is %s"
                           % (recorded.get(name), name, expected[:12]))
            continue
        counts["pins"] += 1
    return counts


# ---------------------------------------------------------------- control mutants

def entry_text_of(repo, rev):
    data = blob(repo, rev, ENTRY_REL)
    return data.decode("utf-8", "replace") if data else ""


def row_line(text, pid):
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.strip().startswith("|") else []
        if cells and strip_emphasis(cells[0]) == pid:
            return line
    raise SetupError("row %s not found in entry" % pid)


def replace_row_line(text, pid, new_line):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and strip_emphasis(cells[0]) == pid:
                lines[i] = new_line
                return "\n".join(lines) + "\n"
    raise SetupError("row %s not found in entry" % pid)


def cell_line(pid, line, want_index):
    cells = line.strip().strip("|").split("|")
    return cells[want_index].strip()


# each control returns (path, new_bytes) describing the mutation of the scored tree
def ctl_spliced_quote(repo, rev):
    text = entry_text_of(repo, rev)
    line = row_line(text, "P19")
    cells = line.strip().strip("|").split("|")
    quote = strip_emphasis(cells[5])
    spliced = quote.replace("if (S.m_passPressed == 1) { if (!isMouse) ", "")
    if spliced == quote:
        raise SetupError("control C1-CTL-1 could not splice the P19 quote")
    cells[5] = "`%s`" % spliced
    new_line = "|" + "|".join(" %s " % c for c in cells) + "|"
    return ENTRY_REL, replace_row_line(text, "P19", new_line).encode("utf-8")


def ctl_shifted_anchor(repo, rev):
    text = entry_text_of(repo, rev)
    line = row_line(text, "P20")
    cells = line.strip().strip("|").split("|")
    pin, _ = parse_pin_cell(cells[4])
    cells[4] = " %s:1575 " % pin
    new_line = "|" + "|".join(" %s " % c for c in cells) + "|"
    return ENTRY_REL, replace_row_line(text, "P20", new_line).encode("utf-8")


def ctl_hash_tamper(repo, rev):
    data = blob(repo, rev, SUMS_REL)
    text = data.decode("utf-8", "replace")
    name = "Hyprland-ConfigActions.cpp"
    out = []
    hit = False
    for line in text.splitlines(True):
        if not hit and line.split() and line.split()[-1].endswith(name):
            parts = line.split()
            digest = parts[0]
            nibble = "0" if digest[0] != "0" else "1"
            parts[0] = nibble + digest[1:]
            line = "  ".join(parts) + ("\n" if line.endswith("\n") else "")
            hit = True
        out.append(line)
    if not hit:
        raise SetupError("control C1-CTL-3 could not tamper the recorded sha256")
    return SUMS_REL, "".join(out).encode("utf-8")


def ctl_wrong_range(repo, rev):
    text = entry_text_of(repo, rev)
    line = row_line(text, "P21")
    cells = line.strip().strip("|").split("|")
    pin, _ = parse_pin_cell(cells[4])
    cells[4] = " %s:573 " % pin
    new_line = "|" + "|".join(" %s " % c for c in cells) + "|"
    return ENTRY_REL, replace_row_line(text, "P21", new_line).encode("utf-8")


def ctl_dropped_proposition(repo, rev):
    text = entry_text_of(repo, rev)
    lines = text.splitlines()
    out = []
    dropped = False
    for line in lines:
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and strip_emphasis(cells[0]) == "P22":
                dropped = True
                continue
        out.append(line)
    if not dropped:
        raise SetupError("control C1-CTL-5 could not drop the P22 row")
    return ENTRY_REL, ("\n".join(out) + "\n").encode("utf-8")


def ctl_swapped_pin(repo, rev):
    text = entry_text_of(repo, rev)
    line = row_line(text, "P19")
    cells = line.strip().strip("|").split("|")
    pin, anchor = parse_pin_cell(cells[4])
    cells[4] = " Hyprland-KeybindManager.cpp:%s " % anchor
    new_line = "|" + "|".join(" %s " % c for c in cells) + "|"
    return ENTRY_REL, replace_row_line(text, "P19", new_line).encode("utf-8")


# control name -> (mutator, expected counter that must be below its maximum)
CONTROLS = (
    ("C1-CTL-1 spliced-quote", ctl_spliced_quote, "quotes"),
    ("C1-CTL-2 shifted-anchor", ctl_shifted_anchor, "anchors"),
    ("C1-CTL-3 hash-tamper", ctl_hash_tamper, "pins"),
    ("C1-CTL-4 wrong-range", ctl_wrong_range, "anchors"),
    ("C1-CTL-5 dropped-proposition", ctl_dropped_proposition, "propositions"),
    ("C1-CTL-6 swapped-pin", ctl_swapped_pin, "quotes"),
)
MAXIMA = {"propositions": 4, "quotes": 4, "anchors": 4, "pins": 4}


def commit_mutation(clone, rev, path, data, work, tag):
    """Build a mutated commit of the scored tree in the scratch clone (no checkout)."""
    index = os.path.join(work, "index-%s" % tag)
    if os.path.exists(index):
        os.remove(index)
    env = {"GIT_INDEX_FILE": index}
    git(clone, "read-tree", rev, env=env)
    sha = subprocess.run(["git", "-C", clone, "hash-object", "-w", "--stdin"],
                         input=data, capture_output=True, env=git_env()).stdout.decode().strip()
    if not sha:
        raise SetupError("hash-object failed for %s" % path)
    git(clone, "update-index", "--add", "--cacheinfo", "100644,%s,%s" % (sha, path), env=env)
    tree = git(clone, "write-tree", env=env).decode().strip()
    commit = subprocess.run(
        ["git", "-C", clone, "commit-tree", tree, "-p", rev, "-m", "control %s" % tag],
        capture_output=True, env=git_env()).stdout.decode().strip()
    if not commit:
        raise SetupError("commit-tree failed for %s" % path)
    os.remove(index)
    return commit


def run_controls(clone, rev, work, details):
    """Execute the six frozen controls; count the ones the counter rejects."""
    rejected = 0
    for tag, (name, mutator, expect) in enumerate(CONTROLS, start=1):
        try:
            path, data = mutator(clone, rev)
            mutant = commit_mutation(clone, rev, path, data, work, "ctl%d" % tag)
        except SetupError as exc:
            details.append("control %s could not be built: %s" % (name, exc))
            continue
        mcounts = evaluate(clone, mutant, [])
        ok = mcounts[expect] < MAXIMA[expect]
        if ok:
            rejected += 1
            details.append("control %s rejected (%s=%d/%d)"
                           % (name, expect, mcounts[expect], MAXIMA[expect]))
        else:
            details.append("control %s ADMITTED (%s=%d/%d)"
                           % (name, expect, mcounts[expect], MAXIMA[expect]))
    return rejected


# ---------------------------------------------------------------- self test

def selftest(repo, rev, work, details):
    checks = []

    def ok(name, cond, note=""):
        checks.append((name, bool(cond), note))

    # --- normalization rules -------------------------------------------------
    text = "a\n  b\n\nc"
    collapsed, lmap = collapse(text)
    ok("collapse: newline run -> one space", collapsed == "a b c", repr(collapsed))
    ok("collapse: line map", lmap == [1, 2, 2, 4, 4], repr(lmap))
    ok("collapse: intra-line spaces kept", collapse("a  b")[0] == "a  b")
    ok("collapse: leading space kept mid-text", collapse("x\n a")[0] == "x a")
    ok("occurrences: finds both", occurrences("abab", "ab") == [0, 2])
    ok("occurrences: none", occurrences("abc", "z") == [])
    ok("parse_anchor: range", parse_anchor(":1554-1558") == (1554, 1558))
    ok("parse_anchor: single", parse_anchor("1576") == (1576, 1576))
    ok("parse_pin_cell: file and anchor",
       parse_pin_cell("`Hyprland-ConfigActions.cpp:1554-1558`")
       == ("Hyprland-ConfigActions.cpp", "1554-1558"))
    ok("parse_pin_cell: basename only",
       parse_pin_cell("/tmp/x/Hyprland-ConfigActions.hpp:12") == ("Hyprland-ConfigActions.hpp", "12"))

    # --- table parsing ------------------------------------------------------
    doc = "| ID | Pin:anchor | Quote |\n|---|---|---|\n| P19 | a.cpp:1 | `q` |\n"
    rows, pin_idx, quote_idx = entry_rows(doc)
    ok("entry_rows: found", bool(rows) and "P19" in rows)
    ok("entry_rows: pin index", pin_idx == 1 and quote_idx == 2)
    ok("entry_rows: duplicate is rejected",
       entry_rows(doc + "| P19 | a.cpp:2 | `q` |\n")[0].get("P19") is None)
    ok("parse_sums: basename match",
       parse_sums("%s  /a/b/Hyprland-ConfigActions.cpp\n" % ("a" * 64))
       == {"Hyprland-ConfigActions.cpp": "a" * 64})

    # --- the frozen table against the frozen pins ---------------------------
    for pid in IDS:
        pin_name, anchor_text, quote = FROZEN[pid]
        data = blob(repo, rev, FETCH_REL + "/" + pin_name)
        ok("%s: pin present at rev" % pid, data is not None)
        if data is None:
            continue
        collapsed, lmap = collapse(data.decode("utf-8", "replace"))
        qcollapsed, _ = collapse(quote)
        hits = occurrences(collapsed, qcollapsed)
        ok("%s: quote occurs once" % pid, len(hits) == 1, str(len(hits)))
        if len(hits) != 1:
            continue
        start = hits[0]
        span = (lmap[start], lmap[start + len(qcollapsed) - 1])
        ok("%s: spans the frozen anchor" % pid, span == parse_anchor(anchor_text),
           "%s vs %s" % (span, parse_anchor(anchor_text)))
        ok("%s: pin bytes hash to the frozen sha256" % pid,
           hashlib.sha256(data).hexdigest() == FROZEN_SHA[pin_name])
    ok("P21 side-claim: inside 591-627",
       CLAIM_P21_RANGE[0] <= 619 and 622 <= CLAIM_P21_RANGE[1])
    ok("P22 side-claim: after 571", 573 > CLAIM_P22_AFTER)

    # --- red runs: the six controls must be rejected -------------------------
    clone = make_clone(repo, rev, work)
    for tag, (name, mutator, expect) in enumerate(CONTROLS, start=1):
        path, data = mutator(clone, rev)
        mutant = commit_mutation(clone, rev, path, data, work, "st%d" % tag)
        mcounts = evaluate(clone, mutant, [])
        ok("selftest red: %s rejected" % name,
           mcounts[expect] < MAXIMA[expect],
           "%s=%d" % (expect, mcounts[expect]))

    # --- red run: a SHORTENED quote that is still contiguous and still spans
    # the anchor must not score, because the frozen table is the contract ------
    text = entry_text_of(clone, rev)
    line = row_line(text, "P20")
    cells = line.strip().strip("|").split("|")
    cells[5] = " `sendKeyboardMods(0, 0, 0, 0);` "
    short_line = "|" + "|".join(" %s " % c for c in cells) + "|"
    short = replace_row_line(text, "P20", short_line).encode("utf-8")
    mutant = commit_mutation(clone, rev, ENTRY_REL, short, work, "stshort")
    mcounts = evaluate(clone, mutant, [])
    ok("selftest red: shortened-but-contiguous quote rejected",
       mcounts["quotes"] < 4 and mcounts["anchors"] < 4, str(mcounts))

    # --- green run: the unmutated tree is met -------------------------------
    gcounts = evaluate(clone, rev, [])
    ok("selftest green: propositions 4/4", gcounts["propositions"] == 4, str(gcounts))
    ok("selftest green: quotes 4/4", gcounts["quotes"] == 4, str(gcounts))
    ok("selftest green: anchors 4/4", gcounts["anchors"] == 4, str(gcounts))
    ok("selftest green: pins 4/4", gcounts["pins"] == 4, str(gcounts))

    passed = sum(1 for _, good, _ in checks if good)
    total = len(checks)
    for name, good, note in checks:
        if not good:
            print("fail: %s %s" % (name, note))
    print("MADO_C1_R54_SELFTEST: %d/%d assertions passed" % (passed, total))
    return passed == total, passed, total


# ---------------------------------------------------------------- main

def resolve_work(work):
    created = False
    if work is None:
        base = os.environ.get("TMPDIR") or None
        work = tempfile.mkdtemp(prefix="c1-r54-", dir=base)
        created = True
    work = os.path.abspath(work)
    if os.path.exists(work) and not os.path.isdir(work):
        raise SetupError("--work %s is not a directory" % work)
    os.makedirs(work, exist_ok=True)
    if not os.access(work, os.W_OK | os.X_OK):
        raise SetupError("--work %s is not writable" % work)
    return work, created


def main(argv=None):
    ap = argparse.ArgumentParser(description="PRED-C1-r54: errata source-truth verifier")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    work = None
    created = False
    try:
        repo = os.path.abspath(args.repo)
        if not os.path.isdir(repo):
            raise SetupError("--repo %s is not a directory" % repo)
        try:
            git(repo, "rev-parse", "--git-dir")
        except SetupError:
            raise SetupError("--repo %s is not a git repository" % repo)
        rev = resolve_rev(repo, args.rev)
        work, created = resolve_work(args.work)

        if args.selftest:
            good, passed, total = selftest(repo, rev, work, [])
            return 0 if good else 1

        details = []
        clone = make_clone(repo, rev, work)
        counts = evaluate(clone, rev, details)
        controls = run_controls(clone, rev, work, details)
        for line in details:
            sys.stderr.write("detail: %s\n" % line)
        met = (counts["propositions"] == 4 and counts["quotes"] == 4
               and counts["anchors"] == 4 and counts["pins"] == 4 and controls == 6)
        print("MADO_ERRATA_TRUTH: rev=%s propositions=%d/4 quotes=%d/4 anchors=%d/4 "
              "pins=%d/4 controls=%d/6 verdict=%s"
              % (rev, counts["propositions"], counts["quotes"], counts["anchors"],
                 counts["pins"], controls, "TARGET_MET" if met else "TARGET_MISSED"))
        return 0 if met else 1
    except SetupError as exc:
        sys.stderr.write("setup-error: %s\n" % exc)
        return 2
    finally:
        if created and work and os.path.isdir(work):
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
```
<!-- END COUNTER SOURCE -->

## Report

- `.ufo/waves/round-54/w1/R54Seat04.md`
