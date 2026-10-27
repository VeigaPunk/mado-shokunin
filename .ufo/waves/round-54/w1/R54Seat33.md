# R54Seat33 — registration freeze / claim predicates / fixture inventory review

Seat: `R54Seat33` (wave-1 executor). Lane: `mado-shokunin`.
Base under review: `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`.
Governing frozen artefacts: `.ufo/waves/round-54/claims-frozen.md`, `.ufo/waves/round-54/registration.md`.
Scope of this seat: review the freeze, attempt the frozen controls and the do-nothing route, and report a distinct
attack item. No lane file outside this report was written; no git/jj mutation of the lane; no host, compositor,
service or source-repo read.

---

## 0. Distinct attack item (headline)

**A-33: the C2 predicate's quote leg is unsatisfiable as frozen, and the two natural candidate quotes disagree
about which S376 string is "the located quote".**

`registration.md`'s C2 fixture table freezes S376's located quote as

> `uwsm-app client sends arguments to uwsm's app daemon via a pipe.`

but the pinned byte at `uwsm-0.27.1-uwsm-app.1.scd:60` is

> `*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon`

The frozen quote is the **de-marked-up rendering** of the roff source: it carries no `*` emphasis markers and adds
a terminal `.` that the pin does not have at that position. Measured (receipt R3):

```
S375: registered=117-118 byte-literal=0 collapsed=1 span=(117, 119) roff-stripped=0
S376: registered=60    byte-literal=0 collapsed=0 span=None       roff-stripped=1
S377: registered=3714  byte-literal=1 collapsed=1 span=(3714, 3714) roff-stripped=1
```

Consequences, all reproduced end-to-end:

1. **Under a byte-literal judge, S376's frozen quote is not present in its pin at all** (`byte-literal=0`,
   `collapsed=0`, no span). No counter that checks the frozen table's own S376 string against the frozen pin can
   print `quotes=3/3`.
2. **Under a whitespace-collapse judge, S375's frozen quote matches but S376's does not** (`collapsed=1` vs
   `collapsed=0`), so `rows` still cannot reach 3/3. Only a *third* rule — strip roff `*` markers — admits S376,
   and that rule appears nowhere in the freeze.
3. The registration also freezes the **quote location** `uwsm-0.27.1-uwsm-app.1.scd:60` — the line number is
   right, but the *text* the location points at is not the text the table quotes.

`registration.md` supplies a verbatim judge rule for C1 only ("Judge of 'verbatim': exact byte contiguity after
single-space normalization of interior newlines ONLY where the frozen quote itself carries a newline"). **C2 has no
judge rule at all** — no normalisation, no marker-stripping, no length rule. C2's rows leg therefore has no defined
pass condition, and the freeze does not say which of the three candidate strings is the located quote.

Per the honesty rule (`claims-frozen.md` §"Honesty rules": a falsified predicate is an honest stop or a pre-data
re-registration under a NEW versioned file), this is a predicate-level defect in the freeze, not a counter defect:
the C2 quote leg cannot be met by any counter that implements a rule the freeze actually states.

---

## 1. C1 fixture inventory — every frozen anchor and hash re-derived from the pinned bytes

`registration.md` C1 table, all four rows re-checked against `.ufo/waves/round-52/fetch/` at base (receipt R2):

| ID | pin | frozen anchor | byte-literal hits | whitespace-collapsed hits | actual span | matches frozen span |
|---|---|---|---|---|---|---|
| P19 | `Hyprland-ConfigActions.cpp` | `:1554-1558` | **0** | 1 | (1554, 1558) | yes |
| P20 | `Hyprland-ConfigActions.cpp` | `:1576` | 1 | 1 | (1576, 1576) | yes |
| P21 | `Hyprland-legacy-DispatcherTranslator.cpp` | `:619-622` | **0** | 1 | (619, 622) | yes |
| P22 | `Hyprland-legacy-DispatcherTranslator.cpp` | `:573-574` | **0** | 1 | (573, 574) | yes |

**All four recorded sha256 values in `registration.md` match the pinned bytes exactly.** Recomputed:

```
a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  Hyprland-ConfigActions.cpp
746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073  Hyprland-ConfigActions.hpp
8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40  Hyprland-KeybindManager.cpp
7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771  Hyprland-legacy-DispatcherTranslator.cpp
```

The C1 anchor side-claims are all **true**, and the side-claim bounds hold in the pinned bytes:
P21 at 619–622 with `591 ≤ 619` and `622 ≤ 627` (yes); P22 at 573–574 with `573 > 571` (yes, line 571 is `}`).

**C1 defect D-33-a (judge-rule / data mismatch).** The frozen C1 quotes are *space-joined single logical lines* —
they do **not** occur byte-literally in the pins (P19/P21/P22 = 0 literal hits). `registration.md`'s own judge rule
resolves this: *"exact byte contiguity after single-space normalization of interior newlines ONLY where the frozen
quote itself carries a newline (P19/P21/P22 are single logical lines)."* Read strictly, "single-space normalization
of interior newlines" is permitted **only where the quote carries a newline**, and P19/P21/P22 are stated to be
single logical lines — so a literal reading of the frozen rule permits **no** normalisation for exactly the three
quotes that need it. Under that literal reading the honest tree is `quotes=1/4` and C1's target is unreachable; only
P20 (single-line in the source, no newline to normalise) survives. Under the permissive reading (collapse all
whitespace) the honest tree scores 4/4. **The freeze does not say which reading governs**, and the two readings
give opposite verdicts on the honest tree (receipt R4):

```
C1 strict  (byte-literal judge) : propositions=4/4 quotes=1/4 anchors=1/4 pins=4/4 verdict=TARGET_MISSED
C1 lenient (collapse judge)      : propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 verdict=TARGET_MET
```

Note the contrast with C2: C1 at least *has* a judge rule (an ambiguous one); C2 has none.

---

## 2. Frozen controls attempted — all twelve, each as a mutated committed tree

All twelve were built as real git trees in a scratch clone of the base (`/fast/scratch/hyaku/mado-r54/R54Seat33/fixture`),
with `git rev-parse --show-toplevel` asserted before every commit, then judged by a reference judge implementing
the frozen predicates (`judge.py`, scratch only). Every control was **rejected** by the reference judge, so the
control *set* is sound in the direction it was written for. The defects below are in the controls' *coverage*, not
in their reject behaviour.

### C1 controls (receipt R-battery)

| control | mutation (as frozen) | required | reference judge (lenient/collapse, honest anchor check) | result |
|---|---|---|---|---|
| C1-CTL-1 | spliced P19 quote | `quotes≤3/4` MISSED | `quotes=3/4` MISSED | rejected ✓ |
| C1-CTL-2 | P20 anchor `:1576`→`:1575` | MISSED | `quotes=4/4 anchors=3/4` MISSED | rejected ✓ |
| C1-CTL-3 | one sha256 nibble | `pins≤3/4` MISSED | `pins=2/4` MISSED | rejected ✓ **but see D-33-b** |
| C1-CTL-4 | P21 anchor → `:573` | MISSED | `anchors=3/4` MISSED | rejected ✓ |
| C1-CTL-5 | drop P22 row | `propositions≤3/4` MISSED | `propositions=3/4` MISSED | rejected ✓ |
| C1-CTL-6 | P19 pin → `KeybindManager.cpp` | MISSED | `quotes=3/4` MISSED | rejected ✓ |

**D-33-b (C1-CTL-3 is under-specified — the control depends on a hash-oracle choice the freeze never makes).**
`registration.md` says C1 reads `.ufo/waves/round-52/fetch/` **(+SHA256SUMS)**. The freeze does not say whether the
counter must check the pin bytes against (i) the tree's own `SHA256SUMS` at `--rev`, or (ii) the sha256 values
recorded in `registration.md`'s table. The two readings are **mutually exclusive on C1-CTL-3 and on a forged-pin
tree** (receipt R6):

```
oracle=tree       CTL-3 -> pins=2/4 verdict=TARGET_MISSED     FORGE -> pins=4/4 verdict=TARGET_MET
oracle=hardcoded  CTL-3 -> pins=4/4 verdict=TARGET_MET       FORGE -> pins=2/4 verdict=TARGET_MISSED
oracle=both       CTL-3 -> pins=2/4 verdict=TARGET_MISSED     FORGE -> pins=2/4 verdict=TARGET_MISSED
```

- With the **tree** oracle, C1-CTL-3 is rejected — but a **self-consistent forgery is admitted**: a pin whose bytes
  are altered (length-preserving, outside every quoted span) while the tree's `SHA256SUMS` is updated to match
  scores `pins=4/4 verdict=TARGET_MET`. The frozen control set has **no control for this** — C1-CTL-3 tampers only
  the sums file, never the pin bytes.
- With the **registration-table** oracle, C1-CTL-3 is **admitted** (`pins=4/4 verdict=TARGET_MET`) — the frozen
  control's own required verdict ("not a control that gets rejected") is not met, so the counter fails the frozen
  contract on the frozen control.
- Only the `both` oracle (cross-check tree sums *and* the frozen table) rejects both. The freeze does not require it.

A second, independent gap in the same control: `registration.md` says C1-CTL-3 changes "one recorded sha256 in the
tree's SHA256SUMS". The tree's `SHA256SUMS` has **five** lines — four pins plus `README.txt`. Tampering the
`README.txt` line instead of a pin line leaves `pins=4/4 verdict=TARGET_MET` (measured), i.e. the mutation as
written admits a counter that never notices. The frozen control must name **which** line.

### C2 controls

| control | mutation (as frozen) | required | reference judge | result |
|---|---|---|---|---|
| C2-CTL-1 | S376 row quote → `sends arguments via a socket` | MISSED | `rows=0/3` MISSED | rejected ✓ |
| C2-CTL-2 | entry `source:` cites S999 | MISSED | `admitted=0` MISSED | rejected ✓ |
| C2-CTL-3 | remove `source:` line | MISSED | `admitted=0` MISSED | rejected ✓ |
| C2-CTL-4 | remove README index row | MISSED | `admitted=0` MISSED | rejected ✓ |
| C2-CTL-5 | URL pinned at `469a39a5…` | MISSED | `commit=0` MISSED | rejected ✓ |
| C2-CTL-6 | no host joins | MISSED | `hosts=0` MISSED | rejected ✓ |

**D-33-c (C2-CTL-1 cannot discriminate the real S376 quote).** C2-CTL-1 mutates S376's row quote to a string that is
absent from the pin. But the **honest** S376 row quote is *also* absent from the pin under every judge the freeze
states (§0). C2-CTL-1 therefore cannot tell a counter that correctly checks S376 from one that ignores S376
entirely: both reject the forged quote for the same reason. A control that fires identically on the honest and the
forged tree measures nothing.

**D-33-d (C2-CTL-6's "host join" is not specified as a string form).** The frozen host set is given as **full
paths** (`~/.local/share/omarchy/default/hypr/autostart.conf:1` … `:6`, `~/.config/hypr/bindings.conf:2`,
`~/.local/share/omarchy/bin/omarchy-toggle-idle:9`), but the lane's citation convention is **basename** form
(`bindings.conf:2`, `omarchy-toggle-idle:9`, `autostart.conf:1-5`). Measured against the sibling-landed r54 entry
(receipt R5):

```
frozen FULL-PATH set hits in landed entry: 0 / 8
BASENAME set hits in landed entry         : 3 / 8
```

A counter matching the frozen set literally scores the honest tree `hosts=0`; a counter matching basenames scores
`hosts=3`. The freeze does not say which. Worse, the basename form is **substring-fragile**: the landed entry's
`autostart.conf:1-5` contains the literal substring `autostart.conf:1`, so a naive substring matcher counts a
**range** citation as the `:1` citation — one of the six `autostart.conf` members — while the entry's own prose
says `:6` is the polkit agent and the monitor watcher is at `:9`, not `:6`. The freeze cannot be satisfied by the
landed entry under its own full-path set, and is satisfied under a basename set that the freeze never wrote down.

---

## 3. Do-nothing route — attempted and **reachable** on C2

`claims-frozen.md` §9 promises: *"a recycled round-47 entry text with a new title fails clause (b) (its rows'
quotes are not uwsm quotes) and clause (c); a stub entry fails (a); an entry citing S999 fails the registry leg of
(b)."* Three do-nothing routes were built and run.

**Route N-1 — content-free stub (no body at all).** Trio + two frozen host-join strings + no proposition, with the
three rows carrying byte-exact quote cells:

```
MADO_UWSM_ENTRY: rev=8c83195… admitted=1 rows=3/3 controls=0/6 verdict=TARGET_MET
  detail: S375:frozen_q=1,cell_q=1,pin=1,commit=1,mined=1 S376:frozen_q=0,cell_q=1,pin=1,commit=1,mined=1
          S377:frozen_q=1,cell_q=1,pin=1,commit=1,mined=1 hosts=2
```

The entry asserts **nothing whatsoever** about `uwsm-app`, and the predicate still prints `verdict=TARGET_MET`.
Clause (a) is satisfied by the trio alone; clauses (b) and (c) are satisfied entirely by the **registry rows** and
two **strings**. Nothing in PRED-C2-r54 requires the entry to *contain* the three pinned facts.

**Route N-2 — recycled round-47 body.** The r47 entry body verbatim (27 KB about `xdg-terminal-exec`, not
`uwsm-app`) under the r54 filename, with the trio prepended and two frozen host-join strings appended, and rows
carrying byte-exact quote cells:

```
MADO_UWSM_ENTRY: rev=5564cac… admitted=1 rows=3/3 controls=0/6 verdict=TARGET_MET
```

The recycled body carries one frozen full-path host join of its own (`~/.config/hypr/bindings.conf:2` — the r47
entry's own terminal-route citation), so **one** appended string is enough to reach the `hosts≥2` threshold. The
r47 body asserts nothing about `uwsm-app`'s environment.

**Route N-3 — the honest tree as frozen is already TARGET_MISSED.** With the sibling-landed rows (whose quote cells
are 11-word paraphrases, e.g. `Difference before and after preparation is exported into systemd user manager`), a
counter that enforces clause (b) as written scores `rows=0/3` — the paraphrase occurs **0** times literally and
**0** times collapsed in its pin (measured: all three landed quote cells are `literal=0 collapsed=0`). The landed
rows are not frozen-registry-conformant either.

**Why N-1/N-2 are reachable.** Clause (a) is a *shape* test (file exists, indexed, trio present, cites S375–S377);
clause (b) is a test of the **registry rows**, not of the entry; clause (c) counts **strings**. The predicate never
binds the entry's prose to the pinned facts, so the entry is free to be empty or recycled. The frozen C2 do-nothing
control set has **no control that mutates the entry's body** — all six mutate the trio, the index, the rows, or the
host-join strings.

---

## 4. Additional freeze-level omissions found while reviewing the fixture inventory

**D-33-e (C2's frozen row shape has no place for a located quote).** `registration.md` gives the C2 row shape as
`kind / tier / scope / status / opened / recheck / used-by` and puts the located quote in a separate table column
(`located quote (≤25 words)`). But `corpus/SOURCES.md`'s actual header is
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` — there is **no
"located quote" column**. The row that carries the quote is `teaches`. The freeze's own §"Causal separability"
says C2 reads "rows S375–S377 of `corpus/SOURCES.md`" and clause (b) says *"its `teaches`/quote cell's located
quote … occurs verbatim in the round-54 pin"*, using a slash that papers over the schema mismatch. A counter must
guess whether to read `teaches` (the only quote-bearing cell) or a nonexistent column.

**D-33-f (the C1 frozen table lives in `registration.md`, but the predicate names a table in `claims-frozen.md`).**
`claims-frozen.md` §"Causal separability" states C1 reads *".ufo/waves/round-52/fetch/ (+SHA256SUMS) and the frozen
table of this file"*. `claims-frozen.md` contains **no** sha256 table (measured: 0 hits for the P19 pin's recorded
hash); the table with the hashes is in `registration.md` (1 hit). A counter that reads "the frozen table of this
file" as directed finds no hashes there.

**D-33-g (the freeze pins a file that is not tracked in the scored tree).** At base, `git ls-tree` over
`.ufo/waves/round-54/` returns **nothing** — the whole round-54 wave directory is untracked at `e25149fe`. The C2
predicate's clause (b) requires each row's quote to occur in "the round-54 pin", and the C1 causal list names
`.ufo/waves/round-54/fetch/`. A counter invoked as `--repo . --rev <rev>` reads git objects; if the round-54 pins are
not committed at the scored revision, the C2 counter cannot read them at all. (At wave-1 time the directory *is*
tracked on the lane's moving HEAD — `git ls-tree HEAD -- .ufo/waves/round-54/` lists `claims-frozen.md`,
`fetch/README.txt`, `fetch/SHA256SUMS.txt` and the three pins — so this is a base-vs-final-revision hazard rather
than a defect of the freeze text. Flagged because the freeze names a base revision and a scored revision that
differ in exactly this respect.)

**D-33-h (the r52 `SHA256SUMS` records absolute host paths).** The tree's sums file reads
`…  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp`, while the
round-54 `SHA256SUMS.txt` uses bare relative names (`uwsm-0.27.1-README.md`). A counter that joins the recorded
path against the repo would resolve outside the tree; one that matches basenames works. The freeze does not say
which, and C1-CTL-3's mutation target is exactly this file.

---

## 5. What I did **not** attack (declared scope boundary)

- No host read of `~/.config/hypr/*` or `~/.local/share/omarchy/*`; the host-set discrepancy in D-33-d is
  reported from the **lane's own** committed prose plus the registration's own text, not from a host read.
- No sibling seat's lane file was edited; the only lane write is this report.
- No sibling seat's work was re-judged on its merits — the reference judge is mine, in scratch, and is a
  *predicate-interpretation probe*, not a claim about any sibling's counter.
- The `w1` wave directories of other seats were not modified; `git` was used read-only against the lane and
  write-only inside scratch.

---

## 6. Reproduction

All numbers above are reproducible from scratch (nothing lane-side is required except read access to the base
revision):

```
S=/fast/scratch/hyaku/mado-r54/R54Seat33
bash $S/receipt.sh          # R1..R7, the consolidated receipt
bash $S/controls.sh         # all twelve frozen controls as mutated committed trees
```

Fixture construction used `git init` in a scratch directory, `git archive e25149fe | tar -x` for the base tree, and
`git rev-parse --show-toplevel` asserted against the fixture path before every commit. Scratch was removed after
the receipts were captured.

---

## 7. Recommendation (for the L1 / wave-2 falsify wave)

1. **Re-register C2 under a new versioned file** (`claims-frozen-v2.md`) that (a) gives S376's located quote in a
   form actually present in the pin (or states the roff-marker normalisation explicitly), (b) states the C2
   verbatim judge rule that C1 has, (c) names the `SOURCES.md` cell that carries the quote, and (d) names the
   hash/quote string form and the cell that carries it. As frozen, the C2 rows leg has no defined pass condition
   and the C2 target is unreachable by any counter implementing a stated rule.
2. **Add the missing C1 control**: a pin whose **bytes** are altered with the tree's `SHA256SUMS` made consistent
   (measured `pins=4/4 verdict=TARGET_MET` under the tree oracle — currently admitted). Require the counter to
   cross-check the tree's sums **and** the frozen table, and name which `SHA256SUMS` line C1-CTL-3 tampers.
3. **Add the missing C2 control**: mutate the entry's **body** while the trio, index, rows and host strings stay
   green (measured `verdict=TARGET_MET` on a content-free entry and on a recycled r47 body). If the intent is that
   the entry must assert the three pinned facts, the predicate must say so and a control must enforce it.
4. **Pin the C1 judge reading** explicitly ("collapse whitespace runs to a single space before comparing") and the
   C1 hash oracle explicitly; the two readings of the current text give opposite verdicts on the honest tree.

**Honesty note.** This seat is an attack seat, not an author seat. The findings above are reported against the
frozen registration as written; per `claims-frozen.md` §"Honesty rules" none of them has been used to edit
`registration.md` or `claims-frozen.md`, and no falsified predicate has been silently worked around.

**Tooling.** No tool was installed or updated in this seat (no `pacman`, `uv`, `cargo` or `npm` action); the work
used only the pre-existing `python3`, `git`, `awk`, `grep` and `sha256sum`. No host/config/service/compositor
state was mutated.
