# R54Seat05 — C1 errata source-truth counter: audit of the frozen contract

Round 54, wave 1, seat R54Seat05 (executor, C1 / PRED-C1-r54).
Axis focus: coverage + operability. Assigned item: 5 of the C1 item set
(the proposition-population leg: the counter must score `propositions=4/4`
from the *committed entry's* four rows, not from its own hardcoded table).

**No lane edit was made.** This seat produced (a) an isolated prototype counter
in its own scratch, (b) an audit of the frozen C1 contract against the real
round-52 pins and the committed entry, and (c) this report. The lane working
tree is unchanged by this seat (verified: `git status --porcelain` shows only
sibling C2 artifacts — `corpus/README.md`, `corpus/SOURCES.md`,
`corpus/knowledge/uwsm-app-environment-r54.md`, `corpus/lessons/round-54.md`,
`.ufo/waves/round-54/`).

## 0. Ground truth established (static, committed pins only)

All inputs below are read from the frozen base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`.

```
$ cd /home/vgpnk/Projects/shokunin/mado-shokunin && git rev-parse HEAD
e25149fec8152a3aabd2b18a0ee8663b23cf65aa
$ git ls-tree -r --name-only e25149fe -- .ufo/waves/round-52/fetch/
.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
.ufo/waves/round-52/fetch/Hyprland-ConfigActions.hpp
.ufo/waves/round-52/fetch/Hyprland-KeybindManager.cpp
.ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp
.ufo/waves/round-52/fetch/README.txt
.ufo/waves/round-52/fetch/SHA256SUMS

$ sha256sum .ufo/waves/round-52/fetch/*.cpp .ufo/waves/round-52/fetch/*.hpp
a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  Hyprland-ConfigActions.cpp
8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40  Hyprland-KeybindManager.cpp
7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771  Hyprland-legacy-DispatcherTranslator.cpp
746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073  Hyprland-ConfigActions.hpp
```

All four sha256 values match `registration.md`'s C1 fixture inventory table
exactly, and match the tree's `.ufo/waves/round-52/fetch/SHA256SUMS` lines.
The committed entry
`corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`
(blob sha256 `764f48679447fd62858e9773607a3c0bee5395b6182bdf9f30f5d7c95f4d0b65`)
carries exactly four proposition rows, P19–P22, whose **Pin:anchor** and
**Quote** cells are byte-identical to the frozen table in `registration.md`
(quote cells after stripping the surrounding backticks; the frozen table's own
backticks around the pin filename are markdown quoting, not part of the value).
So the entry as committed already satisfies the frozen table modulo trailing
spaces — the counter's job is to *prove* that against the pin bytes, not to
repair a drift.

## 1. The predicate is satisfiable — and only under a specific judge

`registration.md` fixes the judge as: *"Judge of 'verbatim': exact byte
contiguity after single-space normalization of interior newlines ONLY where the
frozen quote itself carries a newline (P19/P21/P22 are single logical lines)."*

That sentence, read as "literal bytes", **cannot verify the honest tree**:

```
P19 literal-occurrences=0   whitespace-collapsed-occurrences=1   frozen-anchor=1554-1558
P20 literal-occurrences=1   whitespace-collapsed-occurrences=1   frozen-anchor=1576-1576
P21 literal-occurrences=0   whitespace-collapsed-occurrences=1   frozen-anchor=619-622
P22 literal-occurrences=0   whitespace-collapsed-occurrences=1   frozen-anchor=573-574
```

The reason is structural: the pins are C++ with indentation and blank lines,
while the frozen quotes are single logical lines. E.g. the P19 quote
`g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(...)`
is spread over pin lines 1554–1558 with a blank line 1555 and three levels of
indentation; the P21 quote spans 619–622 across a blank line 620.

**Finding C1-A (blocking for a literal-judge implementation, resolved by the
anchor side-claims):** the correct judge is *whitespace-collapse the pin side,
then require byte-exact contiguity of the collapsed quote*, and separately
require that the matched occurrence spans **exactly** the frozen window. The
registration's anchor side-claims ("P19 at exactly lines 1554–1558", "P21 at
exactly :619–622", "P22 at exactly :573–574") are only satisfiable under this
collapsed judge — under it each of the four quotes occurs **exactly once** in
its pin and lands on exactly its frozen window. A counter that implements
"exact byte contiguity" literally will report `quotes=0/4` on the *honest*
tree and kill the claim falsely. Any implementing seat must collapse the pin
side, not the quote side.

Note the frozen predicate's own wording ("Quote cell occurring verbatim and
contiguous in the round-52 pin") is compatible with this: the *quote* is
contiguous in the collapsed pin stream, and the *anchor* pins it to the exact
window.

## 2. Counter design that survives all six frozen controls

Prototype: `quality/counters/c1-r54-errata-truth.py` (scratch draft at
`/fast/scratch/hyaku/mado-r54/R54Seat05/proto/c1-r54-errata-truth.py`).
Frozen constants are **embedded in the counter**, not read from the wave dir:
`git ls-files .ufo/waves/round-54` is empty at base, so a counter that read
`registration.md` from the working tree could not reproduce at an arbitrary
`--rev`. This matches the lane's existing pattern (`c1-r51-ledger.py`,
`c2-r51-dispatch-entry.py` embed their frozen contract; they only *read* lane
data through `show(clone, rev, path)`).

Four counters, matching the frozen line exactly:

- `propositions` — the frozen IDs **P19, P20, P21, P22** are present as table
  rows in the committed entry. Bound to the frozen ID set, *not* to "any P-row
  found" (see §4).
- `quotes` — the row's Quote cell equals the frozen quote (modulo trailing
  spaces) and that quote occurs contiguously in the pin named by **the row's own
  Pin:anchor cell**.
- `anchors` — the entry's **claimed** window must carry the quote: the
  collapsed content of the claimed window equals the quote, and the single
  occurrence is at that window, and the frozen side-claim holds
  (`591 ≤ 619 ∧ 622 ≤ 627` for P21; `573 > 571` for P22).
- `pins` — each of the four pin files' bytes hash to the round-52 recorded
  sha256. The check is two-sided: the tree's `SHA256SUMS` line **and** the
  frozen constant must both equal the hash of the bytes. A one-sided check
  (bytes vs. tree sums only) is defeated by re-hashing a tampered pin into the
  sums file; a check against the frozen constant only is defeated by editing
  both.

Verdict rule: `TARGET_MET` iff no drift, and all four counters are 4/4.

**Binding the anchor counter to the entry's claimed window** (rather than to
the frozen window alone) is what makes `anchors` degrade under C1-CTL-2 and
C1-CTL-4 as the registration requires. If the anchor counter only checked the
frozen window, a drifted anchor cell would leave `anchors=4/4` and the control
would pass silently.

### Measured control signatures (isolated clone, mutated tree per control)

```
$ python3 -I proto/c1-r54-errata-truth.py --repo <lane> --rev e25149fe --work <scratch>
MADO_ERRATA_TRUTH: rev=e25149fec8152a3aabd2b18a0ee8663b23cf65aa propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
EXIT=0

control|verdict|props|quotes|anchors|pins|drift
C1-CTL-1|MISSED|4|3|3|4|True
C1-CTL-2|MISSED|4|4|3|4|True
C1-CTL-3|MISSED|4|4|4|3|False
C1-CTL-4|MISSED|4|4|3|4|True
C1-CTL-5|MISSED|3|3|3|4|False
C1-CTL-6|MISSED|4|3|3|4|True
```

Every frozen control is rejected and each degrades a counter the registration
names for it (CTL-1 → quotes, CTL-2 → anchors, CTL-3 → pins, CTL-4 → anchors,
CTL-5 → propositions, CTL-6 → quotes). Selftest: **63 assertions, 0 failures**
(≥ 30 required, with one red run per control).

## 3. `--work` is not in the frozen command — a default is required

The frozen predicate command is

```
python3 -I quality/counters/c1-r54-errata-truth.py --repo . --rev <rev>
```

with **no `--work`**, yet the registration also requires that the counter run
its own six control runs (each control is a mutated tree, so the counter needs
a writable scratch to build them). A counter that *requires* `--work` fails the
frozen command outright. My first draft had exactly this bug and was caught by
running the frozen command verbatim.

**Finding C1-B:** the counter must supply a default scratch when `--work` is
omitted, honouring `TMPDIR` and never hardcoding `/tmp` (the registration's
"no `/tmp` hardcode"). Verified: both `TMPDIR=<scratch> python3 -I … --repo . --rev <rev>`
and `env -u TMPDIR python3 -I … --repo . --rev <rev>` print the frozen line and
exit 0, and both leave no scratch behind. An *explicitly* supplied `--work`
under `/tmp` is refused (scratch rule), matching `c1-r51-ledger.py`'s
`REFUSED_ROOTS` posture.

## 4. Item 5 — distinct failure found: the naive row-iterating counter admits a
## dropped-proposition control

This is the seat's assigned item, and it is where the C1 predicate is weakest.
A counter that scores `propositions` by iterating the **entry's** rows and
checking each row's quote against the pin it names — instead of requiring the
frozen ID set **P19–P22** — passes C1-CTL-5 while accepting a *renamed*
dropped proposition. Measured:

```
NAIVE counter (iterates entry rows, no frozen-ID binding, no anchor check):
   base                         naive ok=4/4  -> prints propositions=4/4
   X-CTL-5 drop P22 row         naive ok=3/4  (frozen line would say propositions=3/4)
   X-CTL-G P22->P23 w/ content  naive ok=4/4  (frozen line would say propositions=4/4)
```

**X-CTL-G (distinct from the frozen six, and distinct from other seats' item-5
probes): the P22 row is dropped and replaced by a row labelled `P23` that
carries P22's exact quote and anchor.** The table still has four data rows, so
any counter that counts *rows* or that iterates *whatever P-rows exist* scores
4/4 and prints `verdict=TARGET_MET` on a tree that no longer states P22. The
frozen predicate requires each of "the four corrected propositions **P19–P22**"
to verify, so a P23 row cannot discharge P22.

The frozen six controls do not cover this: C1-CTL-5 deletes the P22 row
outright (a naive counter *does* catch that, 3/4), which is exactly why the
family needs the ID binding rather than a row count. **Finding C1-C: the
counter must require the frozen ID set {P19,P20,P21,P22} to be present
(it must not infer the population from the entry), and must treat a renamed
row as a missing proposition.** My prototype binds to the frozen ID set and
rejects X-CTL-G (`props=3/4`).

Related distinct probes, all rejected by the prototype:

```
X-CTL-A|MISSED|4|4|4|4|True    P22 row replaced by a DUPLICATE P21 row (row count still 4)
X-CTL-B|MISSED|4|4|4|3|False   pin BYTES tampered, tree SHA256SUMS untouched
X-CTL-C|MISSED|4|4|3|4|True    P22 anchor window shifted to :574-575
X-CTL-D|MET  |4|4|4|4|False    P20 quote cell with trailing spaces -> ACCEPT (modulo trailing spaces)
X-CTL-E|MISSED|3|3|3|4|True    P22 row dropped, P19-P22 re-added in a SECOND table
X-CTL-F|MISSED|3|3|3|4|False   P22 row RENAMED to P23
```

X-CTL-B is the two-sided-hash requirement of §2 made concrete: flipping bytes
in `Hyprland-ConfigActions.cpp` while leaving `SHA256SUMS` alone must be
caught (it is), and it is *not* caught by a counter that only compares the
tree's sums against the bytes.

X-CTL-E guards a second file-shape hole: the entry gains a second
`Pin:anchor`/`Quote` table. A counter that scans the whole file for P-rows
would find P19–P22 in the decoy table; a counter that binds to the entry's
canonical table rejects it (`props=3/4`, plus an explicit
"additional Pin:anchor table(s) (ambiguous)" detail).

## 5. Frozen-artifact gaps the L1 should know about (no predicate edit made)

**Finding C1-D — `claims-frozen.md` does not contain the frozen quote strings
or the sha256 values.** The C1 predicate sentence in `claims-frozen.md` says the
counter reads "the frozen table of this file", but that file carries the
proposition IDs and anchors in prose only:

```
$ grep -c 'sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed' .ufo/waves/round-54/claims-frozen.md
0
$ grep -c 'auto result = sendshortcut(modifiedArgs)' .ufo/waves/round-54/claims-frozen.md
0
$ grep -c 'sendshortcut: key not found' .ufo/waves/round-54/claims-frozen.md
0
$ grep -c 'a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637' .ufo/waves/round-54/claims-frozen.md
0
$ grep -c 'a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637' .ufo/waves/round-54/registration.md
1
```

The verbatim quotes and the hashes live in **`registration.md`**, not in
`claims-frozen.md`. This does not break the claim (the counter may embed
either), but the causal-separability sentence in `claims-frozen.md` says C1
reads "the frozen table of **this file**", which is not where the table is.
Implementing seats should embed from `registration.md`'s C1 table (or copy it
into the counter); nobody should try to read a table out of `claims-frozen.md`
and find it missing.

**Finding C1-E — the two waves' SHA256SUMS files have different names.**
`registration.md` cites the round-52 sums as `SHA256SUMS.txt`, but the
committed round-52 file is `SHA256SUMS` (no suffix); `SHA256SUMS.txt` is the
**round-54** file (C2's, in `.ufo/waves/round-54/fetch/`). A counter that
hardcodes `SHA256SUMS.txt` under `.ufo/waves/round-52/fetch/` finds nothing and
reports `pins=0/4` on the honest tree. The prototype probes both names and
resolves the round-52 one. This is the same class of trap as C1-A and is worth
an L1 note in any re-registration.

## 6. Do-nothing control (§9) — reachable only if the counter reads git objects

The registration's do-nothing control: "a counter that prints the frozen line
without reading git objects fails the six control runs". A 4-line do-nothing
counter does exactly that:

```
$ python3 -I do_nothing.py --repo <lane> --rev e25149fe --work <scratch>
MADO_ERRATA_TRUTH: rev=e25149fec8152a3aabd2b18a0ee8663b23cf65aa propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
EXIT=0
```

It prints the frozen line and exits 0 on the honest tree — but it has no way
to reject any mutated tree, so under the six control runs it must report
`controls<6/6`. The prototype's own `controls=6/6` figure is *earned*: it is
produced by actually mutating six trees and observing six rejections, not by
printing a constant. **The counter must compute `controls=k/6` from real
control runs, never emit it as a literal.**

## 7. Harm watch — no lane mutation, no external substrate

- No lane file was created, modified or deleted by this seat; the only lane
  write is this report, at the path the seat spec names.
- All git fixtures are made in this seat's scratch with `git -C <explicit>`
  and `git clone --shared` from the lane; the clone's `--show-toplevel` is
  verified before any control commit, and control commits are made in the
  clone, never in the lane.
- The lane HEAD moved from `e25149fe` to `350d30e4` during this seat — that is
  sibling C2 work landing, not this seat. The prototype was re-run against the
  new HEAD and still prints `verdict=TARGET_MET` (the C1 inputs are untouched
  by C2).
- No host, domain, package, compositor, service or config read/write; no
  producer execution; no network fetch. Pins are static committed bytes only.
- No tool was installed or updated (Python 3.14.8 and git were already
  present); no package query was run. Nothing to report under the RULES.md
  tooling directive.

## 8. Recommendations to the implementing seats (advisory, no lane edit)

1. Collapse whitespace on the **pin** side; require the collapsed quote to
   occur contiguously and to span **exactly** the claimed window. Never compare
   the quote's literal bytes against the raw pin (C1-A).
2. Bind `propositions` to the frozen ID set {P19,P20,P21,P22}; never to a row
   count or to whatever P-rows the file happens to contain (C1-C).
3. Bind the `anchors` counter to the **entry's claimed** window so a drifted
   anchor cell degrades a counter (C1-CTL-2/4).
4. Verify pin hashes two-sided: bytes vs. tree `SHA256SUMS` **and** bytes vs.
   the frozen constant (§4, X-CTL-B).
5. Supply a default scratch when `--work` is absent; honour `TMPDIR`, never
   hardcode `/tmp` (C1-B).
6. Resolve the sums file as `SHA256SUMS` **or** `SHA256SUMS.txt` under
   `.ufo/waves/round-52/fetch/` (C1-E).
7. Compute `controls=k/6` from real mutated-tree runs; never print it as a
   constant (§6).
8. Add at least the distinct probes of §4 to the counter's own selftest, so
   the ID-binding property is regression-guarded rather than incidental.

## Trailer

- Files changed (lane): `.ufo/waves/round-54/w1/R54Seat05.md` (this report
  only).
- Files changed (scratch, `/fast/scratch/hyaku/mado-r54/R54Seat05/`):
  `proto/c1-r54-errata-truth.py` (prototype counter, 63-assertion selftest),
  `do_nothing.py` (§6 control). Scratch cleaned of work dirs before yield.
- Predicate attacked: **PRED-C1-r54** (`claims-frozen.md`), specifically the
  `propositions=4/4` leg (clause (a)) and the six frozen C1 controls.
- Commands: `python3 -I proto/c1-r54-errata-truth.py --repo <lane> --rev
  e25149fec8152a3aabd2b18a0ee8663b23cf65aa [--work <scratch>] [--selftest]`;
  `git rev-parse/ls-tree/show/sha256sum` against the frozen base only.
- Verification performed: frozen line reproduced verbatim with exit 0; six
  frozen controls all rejected with the registered counter degradation; six
  distinct extra probes (A–F) plus X-CTL-G; do-nothing control prints the
  frozen line but cannot reject a mutated tree; lane immutability confirmed.
- Not performed (out of seat scope, parent owns the gate): `bash
  tools/mado-verify.sh --selftest` (460/460), the navigation counter
  (69/69 → 70/70), the sources census, and the C2 counter. No counter was
  committed; no receipt was written under `.ufo/waves/round-54/receipts/`
  (that is an integrator surface).
- Risks / blockers: none blocking. The C1 claim as frozen is **satisfiable**
  at the base, subject to the judge reading in C1-A. The one open item is
  C1-C: an implementing seat that binds `propositions` to the entry's row set
  rather than the frozen ID set will pass the frozen six controls while
  admitting a renamed dropped proposition (X-CTL-G) — the strongest
  false-accept found this wave for C1.
