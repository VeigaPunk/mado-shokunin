# R54Seat30 — registration freeze review, frozen-control attempts, do-nothing route

Seat: R54Seat30 (wave 1, item 30, executor). Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Base `e25149fec8152a3aabd2b18a0ee8663b23cf65aa`; freeze commit `350d30e4ec5531f65ce99a57efeb8216f38e678a`.
Scope read: `claims-frozen.md`, `registration.md`, the frozen r52/r54 pins, the r52 fetch manifest,
the landed (uncommitted) r54 entry + SOURCES rows + README index row.

This is an **attack item**, not a vote. No predicate, control, fixture or target was edited. No lane
file, tracked file, git/jj state, or sibling repo was written. Everything below was produced by
executing scripts in this seat's scratch; each script is named with the command that runs it, and
the decisive logic of the two counter mutants (`manifestblind.py`, `pinblind.py`) is quoted in the
findings, so the numbers are re-derivable from the frozen bytes alone.

**No tool was installed or updated this seat** (nothing in `/home/vgpnk/.omp/agent/RULES.md`'s
channel order was needed; the attacks are pure `python3` + `git show`/`git clone` against
already-present tools).

---

## Distinct attack item (the headline)

**The round-54 freeze is internally unsatisfiable as written, and its own do-nothing control
(claims-frozen §9) does not close the do-nothing route it claims to close.** Two independent
defects, each reproduced by execution against the frozen pins:

- **C1**: three of the four frozen proposition quotes (P19, P21, P22) are **not byte-contiguous**
  in the frozen r52 pins, and the registration's own judge rule *forbids* the normalization that
  would make them match. A counter that obeys the frozen judge rule scores `quotes=1/4` on the
  **honest** tree → `TARGET_MISSED`. A counter that scores `quotes=4/4` must be using a
  whitespace-collapse reading the registration explicitly does not authorize. The frozen C1 target
  is reachable only by violating the frozen judge rule.
- **C2**: the frozen located quote for **S376 is in no pin under any reading the registration
  authorizes** (the scdoc `*uwsm-app*` emphasis markers are stripped in the frozen quote), and
  **S375's frozen quote spans pin lines 117–119 while the frozen location column says `117-118`**.
  So C2's clause (b) is false on the frozen fixtures themselves, and the counter's own quote source
  has no lawful home (the frozen `SOURCES.md` row shape has **no quote cell**), which produces a
  hard dilemma: reading the quote from the row rejects the honest tree; hardcoding the frozen table
  makes control C2-CTL-1 vacuous.

Both are **fixture-level** defects (the freeze's own data vs the freeze's own pins), not
counter-design opinions, which is why they are distinct from the counter-design seats (items 1–6,
24–25) and from the predicate attackers (items 16–23).

---

## A. C1 — the frozen quote table is not byte-verifiable in the frozen pins

**Attacked predicate:** PRED-C1-r54 clause (a) — "each of the four corrected propositions P19–P22
… has its Quote cell occurring verbatim and contiguous in the round-52 pin named by its Pin:anchor
cell", plus registration.md's judge rule: *"Judge of 'verbatim': exact byte contiguity after
single-space normalization of interior newlines ONLY where the frozen quote itself carries a
newline (P19/P21/P22 are single logical lines)."*

### A1. Execution

```
$ python3 -I /fast/scratch/hyaku/mado-r54/R54Seat30/final_check.py     # section C1-FINDING-4
  P19 :1554-1558: byte-contiguous=False  whitespace-collapsed=True
  P20 :1576:      byte-contiguous=True   whitespace-collapsed=True
  P21 :619-622:  byte-contiguous=False  whitespace-collapsed=True
  P22 :573-574:  byte-contiguous=False  whitespace-collapsed=True
```

The frozen r52 pins at base `e25149fe` (`.ufo/waves/round-52/fetch/`), raw bytes:

```
  P19 pin lines 1554-1558:
    1554 '    g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);'
    1555 ''
    1556 '    if (S.m_passPressed == 1) {'
    1557 '        if (!isMouse)'
    1558 '            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);'
  P21 pin lines 619-622:
    619 '    auto result = sendshortcut(modifiedArgs);'
    620 ''
    621 '    if (keyState == 2 && result.success)'
    622 '        result = sendshortcut(modifiedArgs);'
  P22 pin lines 573-574:
    573 '            if (!keycode)'
    574 '                return {.success = false, .error = "sendshortcut: key not found"};'
```

### A2. Why this is a defect and not a counter choice

The registration's judge sentence is a **conditional permission**: normalization of interior
newlines is allowed *"ONLY where the frozen quote itself carries a newline"*, and it then states in
parentheses that **P19/P21/P22 are single logical lines** — i.e. they carry **no** newline. So for
three of the four frozen quotes the permission does not apply, and the required test collapses to
exact byte contiguity, which the measurements above show is **false** in the frozen pins.

Executed consequence on the honest tree (`verify.py --mode strict`, backticks stripped — the most
generous strict reading):

```
  strict judge (backticks stripped, NO whitespace normalization) on the HONEST tree:
     quotes = 1 /4
```

Only P20 survives. A counter that reaches `quotes=4/4` on the honest tree must therefore be using
whitespace-collapse, i.e. **violating the frozen judge rule**. Both branches are bad for the round:

| counter implementation | honest-tree `quotes` | verdict on honest tree | frozen-rule status |
|---|---|---|---|
| obeys the frozen judge rule | `1/4` | `TARGET_MISSED` | compliant, but the C1 target is unreachable |
| whitespace-collapses | `4/4` | `TARGET_MET` | reaches the target, but violates the frozen judge rule |

**The frozen C1 target is reachable only by violating the frozen judge rule.** Under the round's
own honesty rule ("No predicate, control, fixture or target in this file changes after any seat has
scored"), the correct disposition is a **pre-data re-registration under a NEW versioned file**
(`claims-frozen-v2.md`) that states an unambiguous normalization rule — **not** an executor quietly
picking the reading that scores.

Supporting corroboration from the lane's own precedent: the round-52 verifier spotcheck
(`corpus/lessons/round-52-verifier-spotcheck.md:40`) already scored the r52 entry under
**"whitespace-collapsed"** ("17/18 verbatim whitespace-collapsed in their pinned file"), i.e. the
lane's working definition of "verbatim" is whitespace-collapsed. That is a *different* rule from
the one frozen for round 54. The round-54 freeze silently tightened it while claiming to inherit
it. The fix is one sentence in a v2 file, not a predicate edit after scoring.

### A3. The frozen byte-for-byte table rule also fails on the honest entry

registration.md: *"the counter extracts the committed entry's P19–P22 rows and checks them against
THIS table byte-for-byte modulo trailing spaces; any drift is a TARGET_MISSED"*.

```
  P19: cell == frozen_table (byte-for-byte, modulo trailing spaces) = False
        cell with markdown backticks stripped                        = True
  P20: cell == frozen_table (byte-for-byte, modulo trailing spaces) = False
        cell with markdown backticks stripped                        = True
  P21: cell == frozen_table (byte-for-byte, modulo trailing spaces) = False
        cell with markdown backticks stripped                        = True
  P22: cell == frozen_table (byte-for-byte, modulo trailing spaces) = False
        cell with markdown backticks stripped                        = True
```

The committed entry (`corpus/knowledge/hyprland-synthetic-dispatch-r52-errata-r53.md`, base rev)
carries markdown backticks in all four Quote cells; the frozen registration table carries them
bare. A literal byte-for-byte comparison reports **drift on 4/4 rows → TARGET_MISSED**. The
registration must state that backticks are stripped. (The frozen table's `Anchor` column is also
`":1554-1558"` while the entry's cell is `"Hyprland-ConfigActions.cpp:1554-1558"` — the entry
merges pin+anchor into one cell, the table splits them into two columns, so the two are not
directly comparable cell-for-cell at all.)

---

## B. The frozen do-nothing control (§9) does not close the do-nothing route

**Attacked predicate:** claims-frozen.md §9 — *"a counter that prints the frozen line without
reading git objects fails the six control runs (each control is a mutated tree the counter must
reject; an always-print counter accepts them → `controls<6/6`)"* — and the frozen line format
`MADO_ERRATA_TRUTH: rev=<rev> propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6
verdict=TARGET_MET`.

### B1. The always-print counter is indistinguishable in the printed contract

```
$ python3 donothing.py --repo <tree> --rev <rev>       # prints the frozen line, reads nothing
  tree         MADO_ERRATA_TRUTH: rev=tree         propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
  C1-CTL-1     MADO_ERRATA_TRUTH: rev=C1-CTL-1     propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
  C1-CTL-2     MADO_ERRATA_TRUTH: rev=C1-CTL-2     propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
  C1-CTL-3     MADO_ERRATA_TRUTH: rev=C1-CTL-3     propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
  C1-CTL-4     MADO_ERRATA_TRUTH: rev=C1-CTL-4     propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
  C1-CTL-5     MADO_ERRATA_TRUTH: rev=C1-CTL-5     propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
  C1-CTL-6     MADO_ERRATA_TRUTH: rev=C1-CTL-6     propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
  C2-CTL-1 … C2-CTL-6  (identical line, TARGET_MET)
```

The `controls=6/6` field is **self-reported by the counter**. The §9 argument assumes the always-
print counter will print `controls<6/6` when run against a mutated tree — but an always-print
counter prints `6/6` unconditionally, so the *scored* line is identical on the honest tree and on
every control tree. §9 is closed only if the control runs are **externally** executed and their
per-control verdicts are recorded outside the counter's own stdout. The frozen contract does not
require that: `registration.md` says only *"Receipt: the counter's own control run is committed per
control"* — the counter's own run, i.e. self-reported. This is the same shape as round-52's
recorded lesson that a counter must be exercised **against mutated trees** by the judge, not
self-certified.

### B2. A counter that never opens a pinned byte passes all six frozen C1 controls

This is a sharper form. `manifestblind.py` reads only the entry's P19–P22 table cells and the
tree's `SHA256SUMS` manifest, and compares both against the frozen registration table. **It never
opens a `.cpp`.** Its decisive logic, in full:

```python
# manifestblind.py — the pins leg
sums = V.read(tree, ".ufo/waves/round-52/fetch/SHA256SUMS") or ""
recorded = {}
for ln in sums.split("\n"):
    if ln.strip():
        h, p = ln.split(None, 1)
        recorded[os.path.basename(p.strip())] = h
pins = sum(1 for f, h in V.FROZEN_SHA.items() if recorded.get(f) == h)   # manifest text only
# the quotes leg
q = row[5].strip("`")
if re.sub(r"\s+", " ", q) == re.sub(r"\s+", " ", quote): quotes += 1      # frozen table, no pin bytes
```

No pin file is opened anywhere in that script. The quote leg compares the **entry cell** to the
**frozen table**, and the pins leg compares the **manifest text** to the **frozen table**.

```
  honest tree, MANIFEST-BLIND counter (never opens a .cpp):
    MADO_ERRATA_TRUTH: rev=HONEST propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
  the six frozen C1 controls (each required verdict = MISSED):
   C1-CTL-1: verdict=TARGET_MISSED   REJECTED (ok)
   C1-CTL-2: verdict=TARGET_MISSED   REJECTED (ok)
   C1-CTL-3: verdict=TARGET_MISSED   REJECTED (ok)
   C1-CTL-4: verdict=TARGET_MISSED   REJECTED (ok)
   C1-CTL-5: verdict=TARGET_MISSED   REJECTED (ok)
   C1-CTL-6: verdict=TARGET_MISSED   REJECTED (ok)
```

All six frozen controls reject it. But the frozen controls are **all table-cell mutations**
(spliced quote / shifted anchor / wrong range / dropped row / swapped pin) plus one manifest-nibble
tamper. **Not one of them mutates a pinned source byte.** So a counter that never opens the pins
is indistinguishable from a real one under the frozen control set, and it then accepts a tree whose
pin bytes were altered:

```
  pin bytes altered, manifest left intact (no frozen control covers this):
   manifest-blind: MADO_ERRATA_TRUTH: rev=PIN_TAMPER propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
   pin-reading   : MADO_ERRATA_TRUTH: rev=PIN_TAMPER propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
   real verifier  : {'propositions': 4, 'quotes': 3, 'anchors': 3, 'pins': 3, 'table_bytes': 4}
```

(the `real verifier` line is the reference verifier reading pin bytes and hashing them; it drops to
`quotes=3/4 anchors=3/4 pins=3/4` → `TARGET_MISSED`.)

**C1-CTL-6 is the sharpest instance**: the required verdict is *"quote absent from that pin →
MISSED"*, i.e. the control is explicitly a **pin-reading** control. Yet the mutation is applied to
the **entry's pin cell**, and a counter that resolves the pin from the entry cell but never opens
the bytes still rejects it (it sees the quote is not in the *frozen table's* pin). The frozen
control set therefore cannot distinguish "reads the pin" from "reads the table".

**Concrete control the freeze is missing** (this is the omission to add in a v2 file): a seventh
C1 control that mutates **one byte of a pinned source file** (leaving the manifest alone), e.g.
`Hyprland-ConfigActions.cpp` `sendKeyboardMods(0, 0, 0, 0);` → `sendKeyboardMods(1, 1, 1, 1);`,
required verdict `pins≤3/4` MISSED. That single control forces the pin bytes to be opened, and it
is exactly what the current six cannot force.

### B3. "the round-52 recorded sha256" has two readings; one makes C1-CTL-3 vacuous

Clause (c): *"each of the four pins' bytes hash to the round-52 recorded sha256"*. Two authorities:
**A_tree** = the tree's `.ufo/waves/round-52/fetch/SHA256SUMS` at the scored rev; **B_frozen** = the
frozen registration table's recorded values.

```
  C1-CTL-3 (hash-tamper, required verdict = MISSED):
   authority=A_tree    MADO_ERRATA_TRUTH: rev=C1-CTL-3 propositions=4/4 quotes=4/4 anchors=4/4 pins=3/4 controls=6/6 verdict=TARGET_MISSED
   authority=B_frozen  MADO_ERRATA_TRUTH: rev=C1-CTL-3 propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
```

Under B_frozen the tree manifest is ignored entirely, so **C1-CTL-3 is vacuous** — the tamper is
invisible. The freeze does not say which authority governs, and C1-CTL-3 only bites under A_tree.
A v2 file must name the authority.

Related manifest facts (frozen r52 `SHA256SUMS`):
- it has **5** hash lines (the four pins **plus `README.txt`**), while the predicate prints
  `pins=4/4` — the denominator is stated nowhere;
- the paths are **absolute host paths** (`/home/vgpnk/Projects/shokunin/mado-shokunin/…`). Since a
  control is *"a mutated copy of the scored tree"* checked out elsewhere, a counter that resolves
  pin paths from the manifest reads the **original lane pins**, not the mutated copy — so CTL-3's
  tamper would be measured against pristine bytes. The counter must join on basename and read
  bytes from the tree under test.

### B4. The C1 read-list points at a table that is not in the named file

claims-frozen.md §Causal separability: *"C1 reads only … and **the frozen table of this file**"* —
i.e. the frozen table is supposed to be **in `claims-frozen.md`**. Measured at the freeze commit:

```
  .ufo/waves/round-54/claims-frozen.md: contains 'g_pSeatManager' = 0, contains 'uwsm-app client sends arguments' = 0
  .ufo/waves/round-54/registration.md:   contains 'g_pSeatManager' = 3, contains 'uwsm-app client sends arguments' = 1
```

The frozen table lives in **`registration.md`**, not `claims-frozen.md`. `claims-frozen.md` contains
no quote strings at all. The read-list is therefore wrong as written: a C1 counter that obeys it
literally reads a table that does not exist in the file it names, and a counter that reads
`registration.md` violates the frozen separability list. Same defect for C2, whose read-list names
no file containing its three located quotes.

---

## C. C2 — the located quote has no lawful home, and the frozen quote is in no pin

**Attacked predicate:** PRED-C2-r54 clause (b) — *"each of those rows is `mined`, `opened`
2026-10-27, carries a URL pinned at commit `0727985c9bae655bda488f87f99ea69a6ac1c003`, and its
`teaches`/quote cell's located quote (≤25 words) occurs verbatim in the round-54 pin named by its
source file"*.

### C1. The frozen quotes vs the frozen pins (frozen commit `350d30e4`)

```
  S375  pin=uwsm-0.27.1-README.md  frozen_location=117-118
     verbatim in pin                     : False
     whitespace-normalized in pin        : True
     whitespace-normalized + '*' stripped: True
     frozen quote inside location window  : False
  S376  pin=uwsm-0.27.1-uwsm-app.1.scd  frozen_location=60
     verbatim in pin                     : False
     whitespace-normalized in pin        : False
     whitespace-normalized + '*' stripped: True
     frozen quote inside location window  : False
  S377  pin=uwsm-0.27.1-main.py  frozen_location=3714
     verbatim in pin                     : True
     whitespace-normalized in pin        : True
     frozen quote inside location window  : True
```

Raw bytes:

```
  S376 pin line 60 : "*uwsm-app* client sends arguments to uwsm's app daemon via a pipe. Upon"
  S375 pin lines 117-119:
    117 '- Difference between environment state before and after preparation is exported'
    118 '  into systemd user manager (and D-Bus activation environment if reference D-Bus'
    119 '  implementation is used)'
```

Two distinct fixture defects:

1. **S376's frozen quote is in no pin under any authorized reading.** The pin renders the command
   as scdoc emphasis `*uwsm-app*`; the frozen quote drops the asterisks. Whitespace-normalized it
   still does not match (the `*` is not whitespace). It matches only after stripping `*`, which no
   clause of the freeze authorizes. **Clause (b) is false on the frozen fixture.**
2. **S375's frozen location is wrong.** The frozen quote spans pin lines **117–119** (its tail
   `implementation is used)` is on 119) but the frozen location column says `117-118`, and the quote
   is **not contained in its own declared window** (`False` above). The registration also froze the
   wrong *host* claim for the same row range (see D).

### C2. The quote has no cell to live in, and the three designs are a dilemma

The frozen `SOURCES.md` row shape (`corpus/SOURCES.md:11`) is:

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
```

**There is no quote column.** The landed rows carry the located quote nowhere:

```
  ncols = 11
    col5 = 'README.md:117-118 @ 0727985…; pin .ufo/waves/round-54/fetch/uwsm-0.27.1-README.md SHA256 1874fb83…'
    col6 = 'Difference before and after preparation is exported into systemd user manager'
  frozen quote present in ANY cell? False
  frozen quote (full, with D-Bus clause) present in ANY cell? False
```

The `teaches` cell is a **paraphrase**, not a quote; it is not in the pin under any reading:

```
  S375 teaches='Difference before and after preparation is exported into systemd user manager'
      collapsed in pin: False   +'*' stripped: False
  S376 teaches="uwsm-app client sends arguments to uwsm's app daemon via a pipe"
      collapsed in pin: False   +'*' stripped: True
  S377 teaches='unit name includes desktop and command substrings and random hexadecimal text'
      collapsed in pin: False   +'*' stripped: False
```

Hence the clause-(b) quote has exactly three possible sources, and each fails differently
(`c2_dilemma.py`, executed):

```
C2 DILEMMA — honest-tree reachability vs C2-CTL-1 rejection
C2-CTL-1 required verdict = MISSED (a row quote absent from the pin).

design                                           honest rows leg    C2-CTL-1 rows leg  verdict
A  quote = row's teaches cell                           0/3                  0/3  TARGET UNREACHABLE (honest tree fails the same clause)
B  quote = frozen registration table                    2/3                  2/3  TARGET UNREACHABLE (honest tree fails the same clause)
B' quote = frozen table + scdoc '*' stripped            3/3                  3/3  CONTROL VACUOUS (C2-CTL-1 admitted)
```

- **Design A** (the clause's literal pointer — read the quote from the row): rejects the honest tree
  (0/3) → **the C2 target is unreachable**.
- **Design B** (hardcode the frozen table): still 2/3 on the honest tree, because S376's frozen
  quote is not in its pin → **the C2 target is unreachable**.
- **Design B′** (frozen table + strip scdoc `*`): reaches 3/3 on the honest tree, but then it never
  reads the row's quote, so **C2-CTL-1 is admitted** → the frozen control is **vacuous**.

**No design satisfies both the C2 target and the C2 control set.** The v2 file must (i) add a
quote cell to the row shape (or name `registration.md` as the counter's authorized quote source),
(ii) freeze S376's quote with its scdoc markers, (iii) correct S375's location to `117-119`, and
(iv) add a control that mutates the **row's quote cell** so a table-hardcoding counter is rejected.

### C3. The landed entry's `source:` line does not literally cite S376

```
  entry source: line ids via \bS\d{3}\b: ['S375', 'S377']
  -> 'S376' is absent from the source: line (range form S375-S377).
```

Clause (a) requires the trio to cite "rows S375, S376 and S377"; C2-CTL-2 replaces the citation
with `S999` and expects the **registry leg** to fail — which presumes the counter parses ids off
the `source:` line. The landed line uses an en-dash range `S375–S377`, so a literal id scan finds
S375 and S377 but **not S376**. The lane has range-form precedent (the kitty entry's
`source: S123, S124, …` list, and `S123-S131` inside it), so the range is not anomalous — but the
freeze must say whether a range expands. Note the sibling entry (already rewritten in the working
tree, observed mid-flight) also reports a **host** discrepancy against the frozen set — see D.

### C4. The frozen host set does not match the entry's citation style

Clause (c) requires ≥2 citations *from the frozen host set*, cited "as `file:line`". The frozen
strings are full paths (`~/.local/share/omarchy/default/hypr/autostart.conf:1` … `:6`,
`~/.config/hypr/bindings.conf:2`, `~/.local/share/omarchy/bin/omarchy-toggle-idle:9`). Against the
entry as written:

```
  frozen host-set strings matched verbatim : 0/8
  matched by basename:line only            : 3/8
```

The freeze does not say which form counts, and the two readings differ by 8 vs 3 — a counter that
requires the full path scores the honest entry `0/8` → clause (c) fails → `TARGET_MISSED`. A v2
file must state the required citation form (or the frozen set should be given as the basename
form the lane actually uses).

### C5. The frozen host set itself overstates the autostart range

The freeze's own `fetch/README.txt` (committed at the freeze) asserts six `exec-once = uwsm-app --`
lines at `autostart.conf:1-6` including `omarchy-hyprland-monitor-watch`. The entry now in the
working tree reports, from direct host inspection, that `autostart.conf:1-5` hold **five**
`uwsm-app` declarations, that `:6` launches the **polkit agent**, and that the monitor watcher is
at **`:9`**. If that reading is right, then frozen host-set members `autostart.conf:6` and the
`:1-6` range are **false joins**, and a counter that only counts citation strings would admit an
entry built on them. The freeze is source-only this round, so this is reported as a **conflict
between two lane artifacts**, not adjudicated here: the freeze's `fetch/README.txt` and the
sibling entry disagree about the same host bytes. This seat performed **no host reads** (out of
scope by the wave rules); the conflict is visible from the committed text alone.

---

## D. Reproducibility — what I ran

Scratch (this seat's own; nothing outside it, and it was removed before yielding):

```
/fast/scratch/hyaku/mado-r54/R54Seat30/
  final_check.py     frozen-table-vs-frozen-pins checks (A, C)
  evidence.py        consolidated re-run of A, A2, B, B2, C, D, E, F
  verify.py          reference verifier implementing the frozen C1/C2 clauses
  controls.py        builds the 12 frozen control trees and runs the verifier on each
  verdict.py         emits the frozen output lines under each competing reading
  manifestblind.py   mutant counter: reads entry + manifest, NEVER opens a .cpp
  pinblind.py        mutant counter: entry only, never opens a .cpp
  donothing.py       always-print counter (frozen line, reads nothing)
  c2_dilemma.py      the C2 design dilemma
  tree/              honest tree snapshot (entry + SOURCES + README + both fetch dirs)
  work/              the 12 mutated control trees + the pin-tamper fixtures
```

Commands (abridged):

```
git -C <lane> show e25149fe:.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
git -C <lane> show e25149fe:.ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp
git -C <lane> show 350d30e4:.ufo/waves/round-54/claims-frozen.md
git -C <lane> show 350d30e4:.ufo/waves/round-54/registration.md
python3 final_check.py
python3 evidence.py
python3 controls.py --root tree --work work/final --mode collapsed
python3 c2_dilemma.py
python3 manifestblind.py --repo tree --rev HONEST
python3 donothing.py --repo tree --rev HONEST
```

Reference-verifier result on all 12 frozen controls, collapsed mode (the only mode under which the
honest tree passes at all):

```
  control                       | expected | C1 legs      | C2 legs
  C1-CTL-1 spliced-quote       | MISSED   | props=4 quotes=3 anchors=3 pins=4 | REJECTED (ok)
  C1-CTL-2 shifted-anchor      | MISSED   | props=4 quotes=4 anchors=3 pins=4 | REJECTED (ok)
  C1-CTL-3 hash-tamper         | MISSED   | props=4 quotes=4 anchors=4 pins=3 | REJECTED (ok)
  C1-CTL-4 wrong-range         | MISSED   | props=4 quotes=4 anchors=3 pins=4 | REJECTED (ok)
  C1-CTL-5 dropped-proposition | MISSED   | props=3 quotes=3 anchors=3 pins=4 | REJECTED (ok)
  C1-CTL-6 swapped-pin         | MISSED   | props=4 quotes=3 anchors=3 pins=4 | REJECTED (ok)
  C2-CTL-1 forged-quote        | MISSED   | quote=2/0 ids=0 idx=1 host=0/3 | REJECTED (ok)
  C2-CTL-2 unregistered-id     | MISSED   | quote=2/0 ids=0 idx=1 host=0/3 | REJECTED (ok)
  C2-CTL-3 missing-trio        | MISSED   | quote=2/0 ids=0 idx=1 host=0/3 | REJECTED (ok)
  C2-CTL-4 not-indexed         | MISSED   | quote=2/0 ids=0 idx=0 host=0/3 | REJECTED (ok)
  C2-CTL-5 wrong-commit        | MISSED   | quote=2/0 ids=0 idx=1 host=0/3 | REJECTED (ok)
  C2-CTL-6 no-host-joins       | MISSED   | quote=2/0 ids=0 idx=1 host=0/0 | REJECTED (ok)
```

Note the honest-tree C2 line in that run: `cited_ids=0` (the `source:` range hides S376) and
`frozen_quote=2/3` (S376's frozen quote is in no pin). Those are the two clause-(a)/(b) failures
described in C1–C2 above, visible on the same run.

---

## E. Recommended disposition (advisory only — the L1 holds the planner seat)

Per claims-frozen.md, the frozen file cannot be edited after any seat has scored. The honest paths:

1. **Re-register pre-data under `claims-frozen-v2.md`** with the corrections enumerated above:
   - **C1**: state one normalization rule (whitespace-collapse, matching the round-52 lane
     precedent) and say it applies to all four quotes; state that markdown backticks are stripped
     and that the Pin:anchor cell is split into pin + anchor before comparison; name the sha256
     authority (tree manifest vs frozen table); state the `pins` denominator (4 of 5 manifest
     lines).
   - **C1 controls**: add a seventh control that mutates a **pinned source byte** with the manifest
     untouched (required verdict `pins≤3/4` MISSED), so "reads the pin" becomes forced.
   - **C2**: give the row a quote cell (or authorize `registration.md` as the counter's quote
     source); freeze S376's quote **with** the scdoc `*uwsm-app*` markers; correct S375's
     location to `117-119`; state the host-citation form; add a control that mutates the **row's
     quote cell**.
   - **Both**: fix the causal-separability read-list — the frozen table is in `registration.md`,
     not `claims-frozen.md`; and require control runs to be **externally** executed with per-control
     verdicts recorded outside the counter's stdout, so `controls=6/6` is not self-reported.
2. If the L1 prefers not to re-register, then the honest reading of the frozen text is that **C1's
   clause (a) and C2's clause (b) are unsatisfiable on the frozen fixtures**, both claims die by
   the frozen kill rule, and the round is an honest stop. That is a legitimate outcome — but it
   should be recorded as a *frozen-fixture* falsification, not as a counter failure.

**No claim is asserted met or missed by this seat.** This report attacks the freeze; it does not
score either claim.
