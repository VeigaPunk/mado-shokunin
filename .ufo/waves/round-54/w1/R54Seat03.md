# R54Seat03 — executor: C1 errata source-truth counter path (item 3: the hash/manifest leg)

## Scope and registration

- Round 54, wave w1, item 3. Seat `R54Seat03` in `.ufo/waves/round-54/w1/swarm-registry.json`
  (`kind:spawn`, `role:executor`, `item:null`); dispatch prompt in
  `.ufo/waves/round-54/w1-dispatch.json:272-274`. Leaf seat: no dispatch, no background job,
  no git/jj mutation, no commit, no lane file edited.
- Governing prose: `.ufo/waves/round-54/claims-frozen.md` (C1 = **operability**, the
  record-instrument capability) and `.ufo/waves/round-54/registration.md` (C1 fixture
  inventory, frozen proposition table, six frozen controls).
- **Axes named: operability (C1) only.** No coverage claim is made or moved by this seat.
- Base: `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`. The lane `HEAD` moved during the wave
  (measured `350d30e4ec5531f65ce99a57efeb8216f38e678a` mid-seat); every number below is
  re-derived from an explicit `--rev`, never from the working tree.
- Source-only round honoured: no network fetch, no live host read, no producer execution, no
  package query, no host/config/compositor mutation, no `~/.local/bin` or PATH write, no
  campaign tool. The source repo `/home/vgpnk/Projects/shokuknow` was not read.
- Scratch: `/fast/scratch/hyaku/mado-r54/R54Seat03` only; removed at the end of this seat.
  No file of mine remains under `/tmp` (one empty, ambiguously-attributed directory is
  discussed in §9).
- **No tool was installed or updated.** `python3` 3.14.8 and `git` 2.56.0 were already
  present and sufficient; `RULES.md` was read first (`/home/vgpnk/.omp/agent/RULES.md`) and
  its directive did not trigger because no new tool was needed. `pacman` was not touched.

## 1. What already holds at base (the C1 target is a counter, not a content change)

The claim's "before" state is that no `c1-r54-*` counter exists. **The C1 entry and its pins
are already committed at base and already satisfy every substantive clause.** Measured at
`e25149fec8152a3aabd2b18a0ee8663b23cf65aa`:

- `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` exists (committed
  `8d5c36adda17d27a866fd04484375015116297f2`) with rows P19–P22.
- The four pins exist under `.ufo/waves/round-52/fetch/` and their bytes hash to the
  round-52 recorded digests (all four verified, `sha256sum` output reproduced in §6).
- `ls quality/counters | grep -c r54` → `0`.

So the C1 deliverable is **exactly one artifact**: the counter. The content side of the
predicate is satisfied already and must not be re-touched.

## 2. The counter draft (scratch only — not committed, not in the lane)

Draft: `/fast/scratch/hyaku/mado-r54/R54Seat03/c1-r54-errata-truth.py`.
At the revision whose behaviour is measured below it was 652 lines, sha256
`70720bc17741d9ab3eff48a8cac8c2abd0a99145b1b1b17cc682b21df527e439`; the **final** revision
additionally rewrote `resolve_work()` to resolve the scratch root from `$TMPDIR` (see point 5
below) and re-verified at `MADO_SELFTEST: 50/50 assertions passed` and
`MADO_ERRATA_TRUTH: … verdict=TARGET_MET`. **The exact final bytes are gone**: the seat's
scratch was removed at the end of the seat (seat rule: scratch is cleaned before yield), so
the hash above identifies the measured-but-not-final revision and the final revision differs
only in `resolve_work()` plus its docstring. The design below is what a landing seat needs;
it is not a byte-exact patch.
It is **not** written to `quality/counters/` — the seat spec forbids lane edits.

Design decisions, each one a finding:

1. **All inputs come from git objects at `--rev`** (`git show <rev>:<path>`), never from the
   working tree. This is what makes "a control = a mutated copy of the scored tree" true.
2. **Four separate legs**, matching the frozen line's four counters:
   `propositions` (entry row vs the frozen table, byte-for-byte modulo trailing spaces),
   `quotes` (quote cell vs the pin span at the anchor), `anchors` (frozen anchor + side-claim),
   `pins` (bytes vs recorded digest vs frozen digest + manifest self-consistency).
3. **Controls are run by the counter itself**, each as one mutated commit over `--rev`,
   scored by the same `evaluate()`; each must be rejected. A control that cannot be applied
   counts as **not** rejected (never silently skipped).
4. **Control trees are built with plumbing** (`read-tree` → `hash-object -w` →
   `update-index --cacheinfo` → `write-tree` → `commit-tree`) against a `--shared` clone, so a
   control costs kilobytes and never checks out 400 MB. **The scored repo's object store is
   never written to** (measured: `git count-objects -v` unchanged at `count: 11391` before and
   after every run in this seat).
5. **Scratch** is `--work DIR` or a `mkdtemp` under `$TMPDIR`; a `--work` inside the scored
   repository is refused (measured: `MADO_SETUP_ERROR --work inside the scored repository is
   refused`, exit 2). The scratch root is **not** hardcoded to `/tmp`: it is
   `os.environ.get("TMPDIR") or tempfile.gettempdir()`, i.e. the caller's `$TMPDIR` when set —
   the convention of `quality/counters/c2-r51-dispatch-entry.py:582-585`. (Note the
   consequence: with `$TMPDIR` unset the fallback *is* the system temp dir, which is how the
   sibling seat's counter produced the `/tmp` directory discussed in §10.)

   **Self-found defect IN THE FINAL DRAFT (reported because a landing seat would inherit
   it):** the refusal check runs *after* `os.makedirs(work)`, so a refused `--work` inside the
   lane still creates an empty directory there. Measured: my own probe
   `--work /home/vgpnk/Projects/shokunin/mado-shokunin/scratchprobe` left an empty
   `scratchprobe/` in the lane root (the counter exited 2 with
   `MADO_SETUP_ERROR --work inside the scored repository is refused`, but the directory
   remained). **I removed it** (`rmdir scratchprobe`; the lane root now has no stray
   directory — `git status --porcelain` shows only sibling seats' in-flight files and the
   wave reports). **Fix for the landing seat: test the refusal BEFORE creating the
   directory** — i.e. resolve `work`, compare it against the repo root, and only then
   `makedirs`. A landing seat must also not run a refusal probe with a lane path.

## 3. FINDING 1 (item 3, distinct): the frozen table's quotes are NOT byte-contiguous in the pins

This is the single most consequential fact for the C1 counter, and it is **not** stated in the
registration.

`registration.md` line 55 says: *"Judge of 'verbatim': exact byte contiguity after
single-space normalization of interior newlines ONLY where the frozen quote itself carries a
newline (P19/P21/P22 are single logical lines)."*

Measured against the real pins (method and full output in §6):

| ID | A: raw byte substring of the anchor span | B: newline→single space, indent kept | C: per-line strip + join | D: whitespace-collapse both sides | E: byte substring of the whole file |
|---|---|---|---|---|---|
| P19 | **False** | **False** | True | True | **False** |
| P20 | True | True | True | True | True |
| P21 | **False** | **False** | True | True | **False** |
| P22 | **False** | **False** | True | True | **False** |

**Reading the registration literally (normalization only where the quote itself carries a
newline; P19/P21/P22 are single logical lines ⇒ no normalization) makes the predicate
UNSATISFIABLE**: three of four frozen quotes are not byte substrings of their pins anywhere,
so `quotes` could never reach 4/4 and the counter would print `verdict=TARGET_MISSED` on a
perfect tree. The frozen table was authored as the **whitespace-collapsed form of the anchor
span** (e.g. P19 = lines 1554–1558 with the blank line 1555 and the indentation collapsed),
not as a byte excerpt.

**Resolution used by this draft, and the resolution L1 should ratify:** judge a quote by
whitespace-collapsing **both** sides (pin span and quote cell) and comparing those. The
draft documents this reading in its own docstring, because a counter written to the literal
wording is a dead counter.

**Also measured — the collapsed span is not unique.** Every window of the pin that collapses
to the frozen quote:

- P19 (frozen span 1554–1558): `(1553,1558)`, `(1554,1558)`
- P20 (1576–1576): `(1575,1576)`, `(1575,1577)`, `(1576,1576)`, `(1576,1577)`
- P21 (619–622): `(618,622)`, `(618,623)`, `(619,622)`, `(619,623)`
- P22 (573–574): `(572,574)`, `(573,574)`

So "the quote occurs in the file" is **not** sufficient to establish an anchor; only the
*exact* span plus the frozen side-claim does. The draft's `anchors` leg requires
`row.start == frozen.start and row.end == frozen.end` **and** the side-claim, and the `quotes`
leg requires the collapse-match at exactly the row's anchor span.

**Side-claims re-derived from the pins** (independent of the entry's own prose):

- P19: anchor `1554-1558`; line 1553 is blank, 1554 is `    g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);`, 1558 is `            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);` ✓
- P20: anchor `1576`; line 1576 is `    g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);` ✓ (the only occurrence of that string in the file — `grep -n` → one hit)
- P21: anchor `619-622`; line 591 is `static SDispatchResult sendkeystate(const std::string& args) {` and 627 is `}` ⇒ `591 ≤ 619` and `622 ≤ 627` hold ✓
- P22: anchor `573-574`; line 571 is `            }` (end of the scan loop) ⇒ `573 > 571` holds ✓; line 574 is `                return {.success = false, .error = "sendshortcut: key not found"};` ✓

## 4. FINDING 2 (item 3, distinct): the pins leg has three independent failure modes, and the six frozen controls only exercise one

The frozen control set's hash-tamper control is `C1-CTL-3`: *"one recorded sha256 in the
tree's SHA256SUMS changed by one hex nibble"*, required verdict `pins≤3/4 MISSED`. The
registration does **not** say which line may be changed. Three distinct inputs exist, and the
counter must reject all of them:

| input | what it breaks | reference counter | a counter that hardcodes the digests (V1) | a counter with no manifest self-check (V3) |
|---|---|---|---|---|
| tamper the `Hyprland-ConfigActions.cpp` line (= C1-CTL-3) | recorded ≠ bytes | **MISS** ✓ | **ADMIT** ✗ | MISS ✓ |
| tamper the `Hyprland-KeybindManager.cpp` line (a registry pin **no proposition cites**) | recorded ≠ bytes | **MISS** ✓ | **ADMIT** ✗ | MISS ✓ |
| tamper the `README.txt` line (a manifest line for a file that is **not one of the four registry pins**) | manifest no longer self-consistent | **MISS** ✓ | **ADMIT** ✗ | **ADMIT** ✗ |

**The reference counter therefore needs a leg the frozen table does not name:** every line of
`SHA256SUMS` must match the bytes of the file it names, not only the four registry pins. The
draft carries this as `manifest_ok`; dropping it (variant V3) admits the third input above.

**Second sub-finding: two of the four registry pins are cited by no proposition.** The frozen
table cites only `Hyprland-ConfigActions.cpp` (P19, P20) and
`Hyprland-legacy-DispatcherTranslator.cpp` (P21, P22). `Hyprland-ConfigActions.hpp` and
`Hyprland-KeybindManager.cpp` are in the registration's four-pin table and in `SHA256SUMS`, but
no proposition names them. A counter that hashes only the *cited* pins would report `pins=2/4`
and could never print the frozen line — so `pins=4/4` must mean **all four registry pins**,
not "the pins the propositions cite". The draft scores all four (`PIN_ORDER`).

**Third sub-finding (a real trap): the manifest records ABSOLUTE paths that name the original
lane root**, e.g.

```
a83abeb57175e659…  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
```

A counter that resolves a pin by the path **recorded in the manifest** never reads the scored
tree's blob. Measured on a tree whose pin bytes are forged (`key - 8` → `key - 9`, manifest
left stale, so the quote survives):

```
forged tree: b8c02abb555e3379b10aa14baa25eed65dfb1cd8
forged pin digest in tree : 0e10a3fb2669f88dd9e631f575f29d4cd2e3d9759b5f6081bfb62969bc43c94f
manifest recorded digest   : a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637
PRISTINE lane file digest  : a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637

P1 tree-based  : tree=0e10a3fb2669f  lane-file=a83abeb57175e  -> REJECT
P2 path-resolve: resolved-file=a83abeb57175e  manifest=a83abeb57175e  -> ADMIT (forged tree not noticed)
```

The path-resolving counter admits a **forged pin** because the path it opens still exists on
this host and is pristine. **Mitigation:** key the manifest by **basename** and always read the
pin bytes from the scored tree. The draft does this.

## 5. FINDING 3 (item 3, distinct): the six frozen controls do not discriminate a full counter from a table-only counter

I built eight plausible counter variants and ran every frozen control plus two extra inputs
through each (`ADMIT` = the variant still prints `TARGET_MET` on the mutated tree):

```
control                                reference V1       V2       V3       V4       V5       V6       V7       V8
------------------------------------------------------------------------------------------------------------------
GOOD TREE (must be MET)                MET      MET      MISS     MET      MET      MISS     MET      MET      MET
C1-CTL-1 spliced-quote                 reject   reject   reject   reject   reject   reject   reject   reject   reject
C1-CTL-2 shifted-anchor                reject   reject   reject   reject   reject   reject   reject   reject   reject
C1-CTL-3 hash-tamper                   reject   ADMIT    reject   reject   reject   reject   reject   reject   reject
C1-CTL-4 wrong-range                   reject   reject   reject   reject   reject   reject   reject   reject   reject
C1-CTL-5 dropped-proposition           reject   reject   reject   reject   reject   reject   reject   reject   reject
C1-CTL-6 swapped-pin                   reject   reject   reject   reject   reject   reject   reject   reject   reject
(extra) README.txt digest tamper       reject   ADMIT    reject   ADMIT    reject   reject   reject   reject   reject
(extra) KeybindManager digest tamper   reject   ADMIT    reject   reject   reject   reject   reject   reject   reject
```

Variant legend: **V1** pins leg compares bytes to digests hardcoded in the counter (never
reads the tree's `SHA256SUMS`) — admits C1-CTL-3 and both extra inputs. **V2** parses the
manifest by full path instead of basename — misses the *good* tree (the recorded absolute path
does not exist in a clone). **V3** drops the manifest self-consistency check — admits the
README-line tamper. **V4** quotes leg checks only that the quote occurs *somewhere* in the pin
file, not at the anchor. **V5** quotes leg demands a byte-contiguous match — misses the good
tree (this is Finding 1). **V6** quote-anywhere + entry-anchors-trusted. **V7** anchors leg
trusts the entry's own anchor cells and only checks the side-claim bounds — for P20 the
side-claim is `None`, so P20's anchor is never compared to the frozen table at all. **V8** =
**table-only counter**: the propositions leg is the frozen-table drift check and the pins leg
is the hash check, while the quotes and anchors legs are decorative.

**The load-bearing result: V8 rejects all six frozen controls.** The frozen control set does
not distinguish a counter that verifies quotes and anchors against the pin bytes from one that
only compares the entry's cells to the frozen table and hashes the pins. Two consequences:

- **The claim is satisfiable by a table-only counter** (V8). That is not a registration defect
  per se — the frozen sentence does not forbid it — but it means **`controls=6/6` alone does
  not evidence source-truth verification**. A counter that satisfies the frozen predicate can
  be built without ever comparing a quote to a pin.
- **Recommendation to L1 (advisory, registration is frozen and I did not edit it):** the C1
  receipt should record, per control, the leg that fired (e.g. `pins=3/4`, `quotes=3/4`), not
  only `TARGET_MISSED`. The draft prints `MADO_REASON <leg>:<detail>` on stderr for exactly
  this reason. Without that, a wave-2 falsify seat cannot tell a verifying counter from V8.

**Counter-variant hazard for the frozen control list itself:** C1-CTL-2 (`P20` anchor
`:1576`→`:1575`) is caught by the *table drift* check, not by the anchor leg — because
`:1575` is not the frozen `:1576`. A counter whose propositions leg only checked "a row
exists with a plausible anchor" and left the anchor comparison to the anchors leg would need
the anchors leg to compare against the frozen table (V7 shows what happens when it does not:
V7 still rejects C1-CTL-2 because the *quotes* leg fails, but V7 would not reject a mutation
that keeps the quote findable and only moves P20's anchor to a line that also contains a
findable quote).

## 6. Distinct failure inputs I ran (not among the six frozen controls)

All are scratch-tree mutations of the scored tree, each scored by the draft:

| id | input | expected | measured |
|---|---|---|---|
| D1 | rev **before** the entry existed (`ad4bf2059bcf…`, parent of `8d5c36ad…`) | TARGET_MISSED, exit≠0 | `propositions=0/4 quotes=0/4 anchors=0/4 pins=4/4 verdict=TARGET_MISSED`, rc=1 ✓ |
| D2 | entry deleted from the tree | TARGET_MISSED | `propositions=0/4 … verdict=TARGET_MISSED`, rc=1 ✓ |
| D3 | good tree | TARGET_MET, rc=0 | `…pins=4/4 controls=6/6 verdict=TARGET_MET`, rc=0 ✓ |
| D4 | registry pin renamed (`.hpp` → `.hpp.bak`), manifest updated to the new basename | TARGET_MISSED | `pins=3/4 verdict=TARGET_MISSED`, rc=1 ✓ |
| D5 | manifest **copied** to `SHA256SUMS.txt` (registration's name) beside the committed `SHA256SUMS` | TARGET_MET (both are the same bytes) | `verdict=TARGET_MET`, rc=0 — **and see Finding 4** |
| D6 | pin bytes forged (`key - 8`→`key - 9`), quote preserved, manifest stale | TARGET_MISSED | `quotes=3/4 anchors=3/4 pins=3/4 verdict=TARGET_MISSED`, rc=1 ✓ |
| D7 | P19's and P20's quote cells swapped | TARGET_MISSED | `propositions=2/4 quotes=2/4 anchors=2/4 verdict=TARGET_MISSED`, rc=1 ✓ |
| D8 | P22 anchor widened `:573-574` → `:570-574` | TARGET_MISSED | `propositions=3/4 quotes=3/4 anchors=3/4 verdict=TARGET_MISSED`, rc=1 ✓ |
| — | pin bytes forged, counter resolves the pin by the manifest's recorded path | MUST reject | **ADMIT** (Finding 2, third sub-finding) |
| — | do-nothing stub counter (`dn1`) on a mutated control tree | MUST be caught | stub prints `… verdict=TARGET_MET` with rc=0 on the mutated tree — only an external per-control run catches it |

## 7. FINDING 4: the registration names the wrong manifest file

`registration.md:12` says the round-52 pin hashes come from *"its committed `SHA256SUMS.txt`"*.
**The committed file is named `SHA256SUMS` (no `.txt`).** Measured:

```
$ git ls-tree --name-only e25149fe… .ufo/waves/round-52/fetch/
.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
.ufo/waves/round-52/fetch/Hyprland-ConfigActions.hpp
.ufo/waves/round-52/fetch/Hyprland-KeybindManager.cpp
.ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp
.ufo/waves/round-52/fetch/README.txt
.ufo/waves/round-52/fetch/SHA256SUMS

$ git cat-file -e e25149fe…:.ufo/waves/round-52/fetch/SHA256SUMS.txt
fatal: path '…/SHA256SUMS.txt' does not exist in 'e25149fe…'
```

The registration's **C2** section (line 57) uses `SHA256SUMS.txt` — which **is** the correct
name in `.ufo/waves/round-54/fetch/`. So the C1 section inherited the C2 spelling. A counter
written to the registration's literal path reads nothing and reports `pins=0/4` on a perfect
tree. The draft tries `SHA256SUMS` then `SHA256SUMS.txt` and asserts in its selftest which one
it used (`manifest name is the committed SHA256SUMS`). **Advisory for L1:** the C1 fixture
inventory should say `SHA256SUMS` (registration is frozen; I did not edit it).

## 8. FINDING 5 (integration, not a C1 defect): landing the counter breaks the C1-r51 tool ledger

This is the coupling the executor seat that lands the counter must handle. The r51 ledger
counter's population is **every file under `tools/`, every `quality/*.py` and every
`quality/counters/*.py`** at the scored revision (`quality/counters/c1-r51-ledger.py:133-146`,
`population()`), and the ledger must have exactly one row per population file. Landing a new
counter without a ledger row turns that claim red. Measured on a scratch fixture that lands
the draft counter at `350d30e4…` + the counter:

```
LEDGER-ROW reason=uncovered path=quality/counters/c1-r54-errata-truth.py detail=no-row
LEDGER: population=83 ledger_rows=82 uncovered=1 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED
```

(exit 1; the same command at the current lane `HEAD` prints
`population=82 ledger_rows=82 uncovered=0 … verdict=TARGET_MET`.) So the landing commit needs
a `quality/tool-ledger.md` row for `quality/counters/c1-r54-errata-truth.py` with a valid
accountability pointer, or the C1-r51 claim regresses at the round's final revision. The
registration's harm watch does not mention this.

## 9. Harm watch

- `bash tools/mado-verify.sh --selftest` → **`MADO_SELFTEST: 460/460 assertions passed`**,
  exit 0 — unchanged from the frozen before-receipt
  (`.ufo/waves/round-54/receipts/before.txt`: `MADO_SELFTEST: 460/460 assertions passed`).
- Lane git state untouched by this seat: `git rev-parse --show-toplevel` = the lane,
  `git count-objects -v` `count: 11391` identical before and after every run (the control
  harness writes only into its scratch clone's own object directory),
  `git status --porcelain` shows only sibling seats' in-flight files
  (`corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/uwsm-app-environment-r54.md`,
  `corpus/lessons/round-54.md`, `.ufo/waves/round-54/`), none of them mine.
- No lane file edited by this seat except this report. No commit, no push, no `jj` operation,
  no dispatch, no background job, no tool install.
- The draft counter was run only against scratch clones and against read-only `--rev`
  inspections of the lane.
- **One empty directory, `/tmp/c1-r54-calmcxj_`, existed under `/tmp` and I removed it**
  (`rmdir`; it was empty — 0 entries — and no process held it open, `fuser` returned
  nothing). **Attribution is genuinely ambiguous and I will not overstate it:** both my draft
  and the sibling seat `R54Seat04`'s counter use `mkdtemp(prefix="c1-r54-")` with a
  `TMPDIR`-or-system-temp fallback, so either could have produced the name. I removed it
  because it was empty and unheld — a live owner would simply recreate it — rather than
  leaving an artifact of unknown ownership in `/tmp`. `ls -d /tmp/c1-r54-*` now matches
  nothing. **My own scratch (`/fast/scratch/hyaku/mado-r54/R54Seat03`) was removed at the
  end of this seat** (`rm -rf`), and no `/tmp` path of mine remains.

## 10. Risk notes for the landing seat

1. **Ratify the judge reading** (Finding 1). Without it, three of four propositions can never
   verify and the claim is dead on a perfect tree. The draft's reading (collapse both sides)
   is the only one that makes the frozen table meaningful.
2. **Ship the manifest self-consistency leg** and key by basename (Finding 2) — otherwise
   C1-CTL-3 is admissible by variant V1 and a forged pin is admissible by a path-resolving
   counter.
3. **Ship the tool-ledger row** with the counter (Finding 8) or the C1-r51 claim regresses.
4. **Print the leg that fired** per control (Finding 5) so a falsify seat can tell the
   reference counter from V8.
5. The counter must read `SHA256SUMS`, not `SHA256SUMS.txt` (Finding 7).
6. **Order the scratch refusal before `makedirs`** (§2, self-found defect) so a refused
   `--work` cannot leave a directory in the lane.
7. `--selftest` must carry **≥30 assertions including one red run per control**; the draft
   carries **50 assertions** with a red run per control, and the `--selftest` path also
   asserts that P19/P21/P22 are *not* byte-contiguous (the Finding-1 guard, so a later edit
   that "fixes" the judge into byte mode fails loudly).

## Trailer — exact commands and outputs

All commands were run from `/fast/scratch/hyaku/mado-r54/R54Seat03` (scratch) or with
absolute paths; the lane root is `/home/vgpnk/Projects/shokunin/mado-shokunin`.

```bash
# 1. base state
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && git rev-parse HEAD
e25149fec8152a3aabd2b18a0ee8663b23cf65aa
$ ls quality/counters | grep -c r54
0
$ git ls-tree -r --name-only e25149fe… -- .ufo/waves/round-52/fetch/
.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
.ufo/waves/round-52/fetch/Hyprland-ConfigActions.hpp
.ufo/waves/round-52/fetch/Hyprland-KeybindManager.cpp
.ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp
.ufo/waves/round-52/fetch/README.txt
.ufo/waves/round-52/fetch/SHA256SUMS

# 2. pin digests (all four match the registration table)
$ sha256sum .ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp \
    .ufo/waves/round-52/fetch/Hyprland-ConfigActions.hpp \
    .ufo/waves/round-52/fetch/Hyprland-KeybindManager.cpp \
    .ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp
a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  …/Hyprland-ConfigActions.cpp
746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073  …/Hyprland-ConfigActions.hpp
8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40  …/Hyprland-KeybindManager.cpp
7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771  …/Hyprland-legacy-DispatcherTranslator.cpp

# 3. the anchor lines, byte-exact (Finding 1 / Finding 3 side-claims)
$ awk 'NR>=1553 && NR<=1558 {printf "%d|%s|\n", NR, $0}' …/Hyprland-ConfigActions.cpp
1553||
1554|    g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);|
1555||
1556|    if (S.m_passPressed == 1) {|
1557|        if (!isMouse)|
1558|            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);|
$ awk 'NR>=1575 && NR<=1577 {printf "%d|%s|\n", NR, $0}' …/Hyprland-ConfigActions.cpp
1575||
1576|    g_pSeatManager->sendKeyboardMods(0, 0, 0, 0);|
1577||
$ awk 'NR>=571 && NR<=574 {printf "%d|%s|\n", NR, $0}' …/Hyprland-legacy-DispatcherTranslator.cpp
571|            }|
572||
573|            if (!keycode)|
574|                return {.success = false, .error = "sendshortcut: key not found"};|
$ awk 'NR>=619 && NR<=622 {printf "%d|%s|\n", NR, $0}' …/Hyprland-legacy-DispatcherTranslator.cpp
619|    auto result = sendshortcut(modifiedArgs);|
620||
621|    if (keyState == 2 && result.success)|
622|        result = sendshortcut(modifiedArgs);|

# 4. the draft counter, selftest and main run
$ export TMPDIR=/fast/scratch/hyaku/mado-r54/R54Seat03
$ python3 -I c1-r54-errata-truth.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
      --rev e25149fec8152a3aabd2b18a0ee8663b23cf65aa --selftest
MADO_SELFTEST: 50/50 assertions passed
$ python3 -I c1-r54-errata-truth.py --repo /home/vgpnk/Projects/shokunin/mado-shokunin \
      --rev e25149fec8152a3aabd2b18a0ee8663b23cf65aa
MADO_ERRATA_TRUTH: rev=e25149fec8152a3aabd2b18a0ee8663b23cf65aa propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
$ echo $?
0

# 5. variant admission matrix (Finding 5) and distinct inputs (Finding table in §6)
$ python3 -I matrix.py
$ python3 -I distinct.py
$ python3 -I pathtrap.py
$ python3 -I donothing.py

# 6. harm watch
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && bash tools/mado-verify.sh --selftest
MADO_SELFTEST: 460/460 assertions passed

# 7. ledger coupling (Finding 8): a scratch fixture that lands the counter
$ cd /fast/scratch/hyaku/mado-r54/R54Seat03/ledgertest && python3 -I quality/check-tool-ledger.py --repo . --rev HEAD
LEDGER-ROW reason=uncovered path=quality/counters/c1-r54-errata-truth.py detail=no-row
LEDGER: population=83 ledger_rows=82 uncovered=1 dangling=0 bad_pointer=0 empty_desc=0 verdict=TARGET_MISSED rev=d2ae2b9337428438931eb089fc4bcdd849162eb2
$ echo $?
1
```

## Attacked predicate and citations

- **Predicate attacked:** `PRED-C1-r54` (`claims-frozen.md:19-43`), specifically clause (a)
  "each Quote cell occurring verbatim and contiguous in the round-52 pin named by its
  Pin:anchor cell", clause (c) "each of the four pins' bytes hash to the round-52 recorded
  sha256", and the §9 do-nothing control, plus the six frozen controls of
  `registration.md:43-50`.
- **Citations:** `registration.md:12` (the `SHA256SUMS.txt` name — Finding 7),
  `registration.md:25-40` (the frozen proposition table and anchor side-claims),
  `registration.md:43-50` (the six frozen controls), `registration.md:52-55` (the counter
  form and the judge of "verbatim" — Finding 1), `registration.md:57` (the C2 manifest name
  that the C1 section copied), `claims-frozen.md:19-43` (the frozen sentence),
  `claims-frozen.md:41-43` (the §9 do-nothing control),
  `corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md` (the entry under test;
  committed `8d5c36adda17d27a866fd04484375015116297f2`),
  `.ufo/waves/round-52/fetch/SHA256SUMS` (the committed manifest, 5 lines, absolute paths),
  `quality/counters/c1-r51-ledger.py:133-146` (the ledger population — Finding 8),
  `quality/tool-ledger.md:11-13` (the ledger row grammar),
  `.ufo/waves/round-54/receipts/before.txt` (the 460/460 before-receipt),
  `quality/counters/c2-r51-dispatch-entry.py:582-585` (the `$TMPDIR` scratch convention the
  draft follows).

## Honest limits of this seat

- The draft counter is **not committed and not in the lane**; the seat spec forbids lane
  edits. It is a working artifact in scratch, reported here in full by hash and by its
  measured behaviour, and it will be removed with the scratch at the end of the seat.
- I did **not** run the counter from `quality/counters/c1-r54-errata-truth.py` inside the
  lane, because the file does not exist there yet; all runs were from the scratch path with
  `--repo` pointing at the lane.
- The **frozen registration was not edited** and no frozen file was changed. Where the
  registration conflicts with the measured ground (Findings 1 and 7), I report the conflict
  and the resolution I used; ratifying them is L1's call under the round's honesty rule.
- I did not evaluate the C2 claim at all.
- The variant analysis (Finding 5) is about *counter implementations*, not about the C2
  counter; C1 alone was in scope for this seat.
