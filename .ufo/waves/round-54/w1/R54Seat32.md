# R54Seat32 — round-54 registration freeze / predicate / fixture-inventory review

Seat: R54Seat32 (executor, wave-1 item 32). Base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`.
Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Scope of this seat: review the frozen registration / claim predicates / fixture
inventory; **attempt the frozen controls and the §9 do-nothing route**; find
omissions; report a distinct attack item tested against a failure/input
different from the other seats'.

This seat is a leaf: no subagent dispatch, no delegation, no background job, no
git/jj mutation in the lane, no commit/push. All fixture work was done in
scratch (`/fast/scratch/hyaku/mado-r54/R54Seat32`), built with `mktemp`-style
`git init` copies under scratch and `git -C <fixture>` explicit; the lane repo
was read only. Scratch fixture dirs were removed after the runs; the probe
scripts remain under scratch (scratch-only, not lane artifacts).

**No tool was installed or updated in this seat.** Nothing in the tooling
directive applied: no package, CLI, or service was needed to read the frozen
documents, hash the pins, or run the reference probes.

---

## Attack item (distinct): the C1 counter has no frozen anchor for the four
## expected pin hashes, and both admissible anchors are defective

**Attacked predicate:** `PRED-C1-r54` clause (c) — *"each of the four pins'
bytes hash to the round-52 recorded sha256"* — as frozen in
`.ufo/waves/round-54/claims-frozen.md` (C1 section) and
`.ufo/waves/round-54/registration.md` (C1 fixture inventory, lines 9–13 and
control `C1-CTL-3 hash-tamper`).

**The omission.** The C1 counter is told to verify the four pins against "the
round-52 recorded sha256". The frozen registration does not say *where* the
counter reads those expected hashes from, and the two candidate sources each
break the frozen control set in a different way:

| candidate anchor for the four expected sha256 | `C1-CTL-3 hash-tamper` (one nibble of `SHA256SUMS` changed) | coordinated tamper (pin bytes changed **and** `SHA256SUMS` updated to match) |
|---|---|---|
| **A.** the tree's own `.ufo/waves/round-52/fetch/SHA256SUMS` at `--rev` | rejected (`pins=3/4`) — control works | **admitted** (`pins=4/4`) — the tree certifies itself |
| **B.** the four values frozen in `registration.md`'s C1 table | **admitted** (`pins=4/4`) — control is a no-op | rejected (`pins=3/4`) — control works |

Neither anchor satisfies both. Anchor A is the only one that makes
`C1-CTL-3` reject, and it is exactly the anchor under which a rewritten pin
plus a rewritten sums file passes the pin-hash leg. Anchor B rejects a
coordinated tamper but then never notices `C1-CTL-3` at all, because the
counter never reads the file the control mutates.

This is reachable in the frozen form, not just in principle: `claims-frozen.md`
line 81 fixes the C1 read-set as *"`.ufo/waves/round-52/fetch/` (+SHA256SUMS)
and the frozen table of this file"* — but the frozen table it points at **is in
`registration.md`, not in `claims-frozen.md`**, and `claims-frozen.md` carries
no table at all (`grep -c "^|" claims-frozen.md` → `0`; `grep -c "g_pSeatManager"
claims-frozen.md` → `0`; `grep -c "a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637"
claims-frozen.md` → `0`). So the counter cannot satisfy the frozen read-set
and anchor the hashes externally at the same time.

**Measured.** Reference probe `ref_c1_sha.py --sha-source {registration,tree-sums,both}`:

```
$ python3 ref_c1_sha.py --repo controls/c1-ctl3-hash-tamper --rev <ctl3 rev> --sha-source registration
  Hyprland-ConfigActions.cpp   actual=a83abeb57175 reg=a83abeb57175 sums=a83abeb57175 -> PASS
  ...
pins=4/4  (sha-source=registration)      # C1-CTL-3 NOT rejected

$ python3 ref_c1_sha.py --repo controls/c1-ctl3-hash-tamper --rev <ctl3 rev> --sha-source tree-sums
  Hyprland-ConfigActions.cpp   actual=a83abeb57175 reg=a83abeb57175 sums=a83abeb57175 -> FAIL
  ...
pins=3/4  (sha-source=tree-sums)         # C1-CTL-3 rejected
```

and on the coordinated-tamper mutant (pin bytes changed *and* the tree's
`SHA256SUMS` line updated to the new hash — a mutation **no** frozen C1 control
performs):

```
$ python3 ref_c2_clause_b.py sha-tree controls/c1-extra-coordinated-pin-tamper <rev>
clause_c_tree_anchored: pins=4/4          # tamper invisible under anchor A
$ python3 ref_c1_sha.py --repo controls/c1-extra-coordinated-pin-tamper --rev <rev> --sha-source registration
pins=3/4  (sha-source=registration)       # tamper caught under anchor B
```

**Why this is distinct from the other seats.** The C1 reviewer seats (16–20)
and the mutation-testers (24–25) work the C1 *counter* against the frozen
controls. This item is one level up: it is a defect in the **frozen
registration's fixture inventory** — the frozen C1 control `C1-CTL-3` cannot be
satisfied simultaneously with the frozen C1 clause (c) by any single counter,
so a counter built to the frozen text either admits `C1-CTL-3` or admits a
coordinated tamper. No counter-side fix resolves it; the freeze must supply
the anchor.

---

## Attack item 2 (distinct): C1's frozen judge of "verbatim" is satisfied by
## the honest tree only under a reading that also admits the spliced-quote
## control — and under the literal reading the honest tree scores 1/4

**Attacked predicate:** `PRED-C1-r54` clause (a) and the `registration.md`
judge sentence (lines 51–53): *"Judge of 'verbatim': exact byte contiguity after
single-space normalization of interior newlines ONLY where the frozen quote
itself carries a newline (P19/P21/P22 are single logical lines)."*

The frozen quotes for P19, P21 and P22 are **single logical lines in the entry
table**, but they are **not single logical lines in the pin**: the pin wraps
them across several physical lines with differing indentation and, for P19 and
P21, a blank line inside the quoted span. Measured against the real pin bytes:

```
P19: strict_bytes=False  single_space_join_exact=False  ws_collapsed_eq=True
P20: strict_bytes=True   single_space_join_exact=True   ws_collapsed_eq=True
P21: strict_bytes=False  single_space_join_exact=False  ws_collapsed_eq=True
P22: strict_bytes=False  single_space_join_exact=True   ws_collapsed_eq=True
TOTALS: {'strict': 1, 'join_sp': 2, 'collapse': 4} of 4
```

So the frozen judge sentence admits three readings and they give three
different honest-tree scores:

* **literal reading** — "exact byte contiguity", no normalization (the rule
  says normalization applies *ONLY* where the quote carries a newline, and
  P19/P21/P22 do not): honest tree scores `quotes=1/4` → **the claim is dead
  on arrival**;
* **region-join reading** — join the quoted anchor span with single spaces:
  P19 and P21 still fail (the blank separator lines inside the span leave a
  double space) → `quotes=2/4`;
* **whitespace-collapse reading** — collapse whitespace runs everywhere:
  `quotes=4/4` → TARGET_MET.

Only the third reaches the target. And that third reading is **not what the
lane's own house convention uses for this exact entry**: the round-52
source-truth review (`corpus/lessons/round-52-verifier-spotcheck.md` line 38)
judged the r52 entry's quotes by *"17/18 verbatim whitespace-collapsed in their
pinned file"* and failed P16 because the *spliced* quote *"occurs nowhere
contiguously"*. Under the collapse reading the C1 splice control is still
caught (the spliced P19 string is absent even collapsed) — measured
`quotes=3/4 verdict=TARGET_MISSED` — so the control set works; but the frozen
sentence does not name the reading that the house convention and the frozen
quotes jointly require. The registration states a judge rule that its own
frozen quote table contradicts.

**Measured.**

```
$ python3 ref_c1.py --repo fixture --rev <rev> --judge collapse
MADO_ERRATA_TRUTH: rev=... propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
$ python3 ref_c1.py --repo fixture --rev <rev> --judge strict
MADO_ERRATA_TRUTH: rev=... propositions=4/4 quotes=1/4 anchors=1/4 pins=4/4 controls=6/6 verdict=TARGET_MISSED
note: P19:quote=absent
note: P21:quote=absent
note: P22:quote=absent
```

**Distinctness.** Seats 34/35 are auditing "C1 source pins with exact-byte
checks … hashes/anchor coordinates"; seats 16–20 are attacking the C1
predicate with the registration controls. This item is specifically that the
**frozen judge sentence's own literal reading contradicts its own frozen
quote table**, which is a freeze-completeness defect, and it has a
counterfactual that the other seats' tests do not produce: the honest tree
itself, at `quotes=1/4`.

---

## Attack item 3 (distinct): the C2 fixture inventory pins a quote and a
## quote-location that do not exist in the C2 pins, so C2's clause (b) is
## unsatisfiable as frozen

**Attacked predicate:** `PRED-C2-r54` clause (b) — *"its `teaches`/quote cell's
located quote (≤25 words) occurs verbatim in the round-54 pin named by its
source file"* — and the C2 frozen quote table (`registration.md` lines 59–64).

The registration's C2 table freezes, for S376, the located quote

```
uwsm-app client sends arguments to uwsm's app daemon via a pipe.
```

against quote-location `uwsm-0.27.1-uwsm-app.1.scd:60`. The pinned bytes at
line 60 are:

```
*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon
```

The frozen quote **does not occur in the pin** — the pin carries markdown
emphasis (`*uwsm-app*`), and the registration's quote drops the asterisks and
drops the trailing `Upon`. Measured:

```
frozen quote strict  : False
frozen quote collapsed: False
landed teaches strict : False
landed teaches collapsed: False
with markdown emphasis: True
```

So under **both** candidate judges (strict byte contiguity and whitespace
collapse) the frozen S376 quote is absent from its pin. And because the
registration's C2 section carries **no judge sentence at all** (the judge
sentence lives at lines 51–53, inside the C1 section — `grep -n "verbatim"
registration.md` → only lines 25, 42, 51, 52, all C1-side), C2 has no frozen
rule that licenses stripping markdown emphasis. Under a faithful C2 counter the
S376 leg can never be met, so `rows=3/3` is unreachable.

The same table has a second, independent defect: for S375 the frozen quote
location is `uwsm-0.27.1-README.md:117-118`, but the quote's bytes actually
span **lines 117–119** (line 119 carries `  implementation is used)`), so the
quote is not contained in the frozen location at all:

```
quote contained in lines 117-118 (collapsed): False
quote contained in lines 117-119 (collapsed): True
```

**Measured.** Clause (b) isolated (`ref_c2_clause_b.py clause-b`), frozen-table
anchor, collapse judge, on the honest tree:

```
$ python3 ref_c2_clause_b.py clause-b fixture <rev> collapse
clause_b: rows=2/3  judge=collapse
  note: S376=quote-absent-from-pin
```

**Why this matters for the C2 control set.** `C2-CTL-1 forged-quote` mutates
the S376 row quote to `sends arguments via a socket` and requires "quote absent
from pin → MISSED". Measured on the CTL-1 mutant under the frozen-table
anchor:

```
clause_b: rows=2/3  judge=collapse
  note: S376=quote-absent-from-pin
```

— **byte-identical to the honest tree's output**. The control does not
discriminate: the honest S376 leg already fails for the same reason the forged
one does, so CTL-1 passes for the wrong reason and provides no evidence that
the counter binds quotes to pins. A counter that only ever checks the S375 and
S377 legs would report the same `rows=2/3` on the honest tree and on the
forged-quote mutant.

**Distinctness.** The C2 critic seats (21–23) attack PRED-C2-r54 for
quote/citation/host-join bypass on a *hypothetical* counter. This item shows
the **frozen fixture inventory itself is inconsistent with the frozen pins**,
so the inconsistency is inherited by every counter built to the freeze — and it
produces a specific artifact the other seats' attacks do not: CTL-1's verdict
is identical on the honest tree and on the mutant.

---

## Attack item 4 (distinct): the §9 do-nothing route — the frozen line
## `controls=6/6` is a self-report, and the always-print counter passes all
## six C1 controls

**Attacked predicate:** `claims-frozen.md` §9 do-nothing control for C1 — *"a
counter that prints the frozen line without reading git objects fails the six
control runs (each control is a mutated tree the counter must reject; an
always-print counter accepts them → `controls<6/6`)"* — and the frozen output
line `MADO_ERRATA_TRUTH: rev=<rev> propositions=4/4 quotes=4/4 anchors=4/4
pins=4/4 controls=6/6 verdict=TARGET_MET`.

The frozen line carries `controls=6/6` as a **field of the counter's own
output**, and the registration's kill rule turns on that field ("if any frozen
C1 control is admitted by the counter, the counter prints
`verdict=TARGET_MISSED` and a non-zero exit"). But nothing in the frozen
contract requires the counter to *derive* `controls=6/6` from actually running
the six controls — the field is a literal in a print statement.

**Measured.** `donothing.py` prints the frozen line verbatim for any `--rev`
and exits 0, without reading a single git object:

```
$ for D in controls/c1-ctl*; do python3 donothing.py --repo $D --rev $(git -C $D rev-parse HEAD); done
c1-ctl1-spliced-quote                      rc=0 verdict=TARGET_MET
c1-ctl2-shifted-anchor                     rc=0 verdict=TARGET_MET
c1-ctl3-hash-tamper                        rc=0 verdict=TARGET_MET
c1-ctl4-wrong-range                        rc=0 verdict=TARGET_MET
c1-ctl5-dropped-proposition                rc=0 verdict=TARGET_MET
c1-ctl6-swapped-pin                        rc=0 verdict=TARGET_MET
```

All six control mutants are **admitted** with `controls=6/6 verdict=TARGET_MET`
— the exact opposite of the §9 requirement that an always-print counter must
report `controls<6/6`. The §9 defense as written ("an always-print counter
accepts them → `controls<6/6`") presumes the counter's `controls=` field is a
*count of control runs it actually performed*; the frozen text never says so,
and the counter author is free to emit the literal. The registration's
"Receipt: the counter's own control run is committed per control" makes the
same point again from the receipt side: the receipt is produced by the
self-reporting artifact.

For contrast, my reference implementation (which does run the six control
mutants and counts real rejections) reports honestly:

```
--- C1-CTL-1 spliced-quote ---   quotes=3/4 ... verdict=TARGET_MISSED
--- C1-CTL-2 shifted-anchor ---  quotes=3/4 ... verdict=TARGET_MISSED
--- C1-CTL-4 wrong-range ---     quotes=3/4 ... verdict=TARGET_MISSED
--- C1-CTL-5 dropped-proposition --- propositions=3/4 ... verdict=TARGET_MISSED
--- C1-CTL-6 swapped-pin ---     quotes=3/4 ... verdict=TARGET_MISSED
--- C1-CTL-3 hash-tamper ---     pins=4/4 ... verdict=TARGET_MET   <-- admitted, see item 1
```

**Note on the honesty of this report.** `C1-CTL-3` is *not* rejected by my
reference implementation either — it is reported as `TARGET_MET` above, and
that is reported here rather than hidden. The cause is item 1: my probe
anchors the expected hashes on the frozen table (anchor B), under which the
`SHA256SUMS` mutation is invisible by construction. Under anchor A CTL-3 is
rejected and the coordinated tamper is admitted. This is the defect, not a
property of the control.

**Distinctness.** The C1 reviewer seats test the do-nothing route as a
*counter-design* risk for a counter that exists. This item is that the
**frozen output line's own `controls=6/6` field is a self-report**, so the
freeze as written does not close the route even for a counter that reads
nothing — and the specific artifact is that the always-print counter's output
on all six control mutants is *byte-identical* to the honest counter's output
on the honest tree.

---

## Supporting observations (recorded, not counted as the attack item)

**S1 — the r52 `SHA256SUMS` path column points outside any tree copy.**
`.ufo/waves/round-52/fetch/SHA256SUMS` records absolute host paths:

```
a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
```

The r54 file uses bare basenames (`uwsm-0.27.1-README.md`), so the two
inventories are not the same shape. A counter that resolves the pin *path*
from the r52 sums file reads the **live lane**, not the tree at `--rev`:

```
live  sha: a83abeb57175e6598
tree  sha: 4c0a60a712ee2438
```

The frozen contract says the counter "reads all inputs from `--repo`/`--rev`
git objects"; a path-column-driven resolution violates that silently. A
counter that resolves by basename inside `--repo` is safe. This is a
regression hazard for the C1-CTL-3 control specifically, and it is the same
defect family as item 1.

**S2 — `claims-frozen.md` names `SHA256SUMS.txt` for the r52 pins, but the
committed file is `SHA256SUMS`.** `claims-frozen.md` line 81 says
*"`.ufo/waves/round-52/fetch/` (+SHA256SUMS)"* (correct), while
`registration.md` line 12 says *"hashes from its committed `SHA256SUMS.txt`"*
and line 57 says the r54 pins' *"sha256 in its `SHA256SUMS.txt`"* (correct for
r54). The r52 file has no `.txt` suffix:
`git ls-tree -r --name-only e25149fe -- .ufo/waves/round-52/fetch` →
`.ufo/waves/round-52/fetch/SHA256SUMS`, and
`test -e .ufo/waves/round-52/fetch/SHA256SUMS.txt` → absent. A counter written
from `registration.md` alone looks for a file that does not exist.

**S3 — the r52 `SHA256SUMS` records five lines, but the C1 table names four
pins.** The extra line is the r52 `README.txt`
(`c53296aeafcdd746ececcb183bcffaf76467a9917db46ae5dc5591bcde674ad0`), which
is outside the C1 claim's scope. A counter that iterates the sums file rather
than the frozen four-pin table scores five pins, not four, and the frozen line
demands `pins=4/4`.

**S4 — the C2 host-join clause (c) is ambiguous and the landed entry cites
none of the frozen host set literally.** The frozen host set is written as
full paths (`~/.local/share/omarchy/default/hypr/autostart.conf:1`, …,
`~/.config/hypr/bindings.conf:2`, `~/.local/share/omarchy/bin/omarchy-toggle-idle:9`),
and the clause requires the entry to cite ≥2 *as `file:line`*. The landed
entry's host-join prose uses bare basenames and a **range**
(`autostart.conf:1-5`, `bindings.conf:2`, `omarchy-toggle-idle:9`) — measured
exact full-path hits against the landed entry: **0**; basename hits: 3 (and
`autostart.conf:1` matches only as a *substring* of `autostart.conf:1-5`, so
the six-element frozen set collapses to at most three usable strings, two of
which are the same file). Under the strict frozen reading the landed entry
satisfies clause (c) with **0** hits. The clause also does not say whether
the ≥2 hits must be **distinct files** or merely distinct strings — under
basename matching, `bindings.conf:2` and `omarchy-toggle-idle:9` are two
distinct files, so the landing is defensible under basename matching only.
`C2-CTL-6 no-host-joins` therefore does not discriminate between these two
readings: both reject the mutated entry.

**S5 — the entry's `source:` line uses an en-dash range, and the house row
extractor reads it as two rows.** `source: S375–S377` yields
`re.findall(r"\bS(\d{3,})\b", line)` → `['375', '377']` — **S376 is not
extracted**. The house convention in `quality/counters/c2-r51-dispatch-entry.py`
(line 386) uses exactly that regex, so a house-convention C2 counter sees two
cited rows, not three, and clause (a) ("citing rows S375, S376 and S377")
fails on the landed entry. Every other lane entry spells its rows out
(`source: S370, S371;`, `source: S326 - …`); the en-dash range form is unique
to this round's draft. This is a landing defect rather than a freeze defect,
but it is the kind of thing a sibling will miss, and it is cheap to fix by
spelling the three rows.

**S6 — `claims-frozen.md` "Before" receipt claims `ls corpus/knowledge | grep -c r54`
→ 0, but the file exists.** `ls corpus/knowledge | grep -c r54` → **1**
(`uwsm-app-environment-r54.md`). The count is 1 because the entry landed as an
untracked file in the working tree (`git status --porcelain` → `?? corpus/knowledge/uwsm-app-environment-r54.md`)
before the freeze was taken, so the "Before" baseline in the frozen file is
already stale at freeze time. The C2 "Before" line in `claims-frozen.md` reads
*"entry absent (`ls corpus/knowledge | grep -c r54` → 0), rows S375–S377 absent
(last registry row S374), predicate TARGET_MISSED by absence"*. At the scored
revision the entry and the three rows are present (as untracked/uncommitted
working-tree state at the time of this seat), so a `--rev` counter reading git
objects at `e25149fe` would still see the true absent baseline — the defect is
that the frozen receipt was **not** measured against the frozen base but
against the working tree, which already contained the round's output.

---

## Reproduction index

| # | Attack item | Frozen predicate / clause attacked | Probe (scratch) | Key output |
|---|---|---|---|---|
| 1 | No frozen anchor for the four expected pin hashes; anchor A admits a coordinated tamper, anchor B admits `C1-CTL-3` | `PRED-C1-r54` (c); `registration.md` C1 table + `C1-CTL-3` | `ref_c1_sha.py --sha-source {registration,tree-sums,both}` | `pins=4/4` (CTL-3 admitted) / `pins=3/4` (coordinated tamper admitted) |
| 2 | Frozen judge of "verbatim" contradicts the frozen quote table; literal reading scores the honest tree `quotes=1/4` | `PRED-C1-r54` (a); `registration.md` judge sentence (51–53) | `ref_c1.py --judge {strict,collapse}` | `quotes=1/4` (strict) vs `quotes=4/4` (collapse) |
| 3 | C2 frozen quote and quote-location do not exist in the C2 pins; clause (b) unsatisfiable; `C2-CTL-1` non-discriminating | `PRED-C2-r54` (b); `registration.md` C2 quote table (59–64) | `ref_c2_clause_b.py clause-b`; `ref_c2.py` | honest `rows=2/3 note S376=quote-absent-from-pin`; CTL-1 mutant **byte-identical** |
| 4 | §9 do-nothing route: `controls=6/6` is a self-report; always-print counter passes all six C1 controls | `claims-frozen.md` §9; frozen `MADO_ERRATA_TRUTH:` line | `donothing.py` over the six `controls/c1-ctl*` trees | `verdict=TARGET_MET rc=0` on all six mutants |

Scratch location: `/fast/scratch/hyaku/mado-r54/R54Seat32/`
(`ref_c1.py`, `ref_c1_sha.py`, `ref_c2.py`, `ref_c2_clause_b.py`, `donothing.py`,
`controls.py`). Fixture trees were built under
`/fast/scratch/hyaku/mado-r54/R54Seat32/controls/` and
`/fast/scratch/hyaku/mado-r54/R54Seat32/fixture/`, each an independent
`git init` copy with `git -C <fixture>` explicit and the toplevel asserted
before each commit; both fixture trees were deleted after the runs. **No file
in the lane was written except this report**; no git/jj mutation, commit, push
or delegation was performed; the source repo was not touched.

## Bottom line

Four distinct attack items, all measured against the frozen bytes rather than
asserted. Three of them (1, 2, 3) are **defects in the frozen registration
itself**, not in any counter: the C1 pin-hash anchor is unspecified and
unsatisfiable against its own control set; the C1 verbatim judge contradicts
the C1 quote table; and the C2 quote table contradicts the C2 pins, which
makes `C2-CTL-1` non-discriminating and `rows=3/3` unreachable. The fourth (4)
shows the §9 do-nothing route is open because the frozen line's `controls=6/6`
is a self-report. Under the honesty rules these are pre-data defects, so the
round's remedy is a re-registration under a NEW versioned file
(`claims-frozen-v2.md`) or an honest stop — **not** an edit to the frozen
`claims-frozen.md` / `registration.md`.
