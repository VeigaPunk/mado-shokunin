# R54Seat01 — C1 source-truth counter path: build, audit, and edge-case report

Seat: `R54Seat01` · role: executor · wave `w1` · round 54 (mado) · base
`e25149fec8152a3aabd2b18a0ee8663b23cf65aa`.
Axis focus: coverage + operability. Assigned item 1: *build/inspect the isolated C1
source-truth counter path; audit the frozen proposition rows, the exact pin
quotes/anchors/hash requirements and the six controls; draft only within
report/scratch; identify edge cases; no lane edits.*

**No lane edit was made.** `quality/counters/` still holds no `r54` counter
(`ls quality/counters | grep -c r54` → `0`), so the frozen predicate's *before*
state (TARGET_MISSED by absence) is unchanged by this seat. Everything below is a
scratch artifact plus this report.

Scratch (cleaned before yield): `/fast/scratch/hyaku/mado-r54/R54Seat01/`
— `c1-r54-errata-truth.py` (draft counter), `harness.py` (git-fixture driver),
`stub-always-print.py` (§9 do-nothing control), `naive-abs-sums-counter.py`
(negative control), `receipts-main.txt`, `receipts-naive.txt`.

No tool was installed or updated in this wave; the host RULES.md tooling directive
had nothing to act on (python 3.14.8 and git 2.56.0 were already present).

---

## 1. The frozen table is self-consistent, and the pins verify — under one reading

The first thing to settle is whether PRED-C1-r54 is *reachable at all*. It is, but
only under one of two readings of the registration's judge clause, and the other
reading makes the frozen target unreachable. That divergence is the single most
important finding of this seat.

`registration.md` says:

> Judge of "verbatim": exact byte contiguity after single-space normalization of
> interior newlines ONLY where the frozen quote itself carries a newline (P19/P21/P22
> are single logical lines).

That sentence is self-referential in a way that changes the verdict. The three
multi-line quotes (P19, P21, P22) are stored in the entry as **single logical
lines** — they carry no newline — so under the literal rule no newline
normalization applies to them, and they must occur **byte-exact** in the pin. They
do not. Measured against the committed pin bytes:

```
$ python3 -I - <<'PY'   # in /fast/scratch/hyaku/mado-r54/R54Seat01
... (reads .ufo/waves/round-52/fetch/* and the entry's P19-P22 rows)
PY
P19  pin=Hyprland-ConfigActions.cpp  anchor=:1554-1558
   literal_byte_contiguous_in_pin = False
     1554: '    g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0);'
     1555: ''
     1556: '    if (S.m_passPressed == 1) {'
     1557: '        if (!isMouse)'
     1558: '            g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);'
   quote bytes: 'g_pSeatManager->sendKeyboardMods(modMask, 0, 0, 0); if (S.m_passPressed == 1) { if (!isMouse) g_pSeatManager->sendKeyboardKey(S.m_timeLastMs, key - 8, WL_KEYBOARD_KEY_STATE_PRESSED);'

P20  pin=Hyprland-ConfigActions.cpp  anchor=:1576
   literal_byte_contiguous_in_pin = True
P21  pin=Hyprland-legacy-DispatcherTranslator.cpp  anchor=:619-622
   literal_byte_contiguous_in_pin = False
     619: '    auto result = sendshortcut(modifiedArgs);'
     620: ''
     621: '    if (keyState == 2 && result.success)'
     622: '        result = sendshortcut(modifiedArgs);'
P22  pin=Hyprland-legacy-DispatcherTranslator.cpp  anchor=:573-574
   literal_byte_contiguous_in_pin = False
     573: '            if (!keycode)'
     574: '                return {.success = false, .error = "sendshortcut: key not found"};'
```

Three decisive facts:

1. **The quote text is not byte-contiguous in the pin** for P19/P21/P22, because the
   pins carry newlines and indentation inside the quoted regions (line 1555 and 620
   are blank; 1557 and 621 are separate statements).
2. **The quote text is exactly right.** Whitespace-collapsed, each quote occurs in
   its pin **exactly once** and spans **exactly** the frozen anchor range:
   P19 → (1554, 1558), P20 → (1576, 1576), P21 → (619, 622), P22 → (573, 574).
   The anchor side-claims therefore hold on the located spans:
   - P19 span == 1554–1558 ✔
   - P20 span == 1576 ✔
   - P21 span == 619–622, and 591 ≤ 619, 622 ≤ 627 ✔ (`sendkeystate` opens at 591: `'static SDispatchResult sendkeystate(const std::string& args) {'`, closes at 627: `'}'`)
   - P22 span == 573–574, and 573 > 571 ✔ (the keysym scan closes at 571: `'            }'`)

   The frozen table was therefore *derived* under the whitespace-collapsed reading.
   That is the house rule: `quality/counters/c2-r51-dispatch-entry.py` (docstring,
   "Citation grammar this counter checks") scores a quote that "appears verbatim,
   **whitespace collapsed**, in the pin's cited line span".
3. **The round-52 lesson already ruled on this shape.** `corpus/lessons/round-52-verifier-spotcheck.md:38`
   records the same judgement applied to the *predecessor* proposition P16: the
   space-joined quote "occurs nowhere contiguously in `Hyprland-ConfigActions.cpp`"
   — the same class of finding, and the reason the errata entry was written.

**Conclusion.** The predicate is reachable under the *pin-region* reading
(whitespace-collapse the pin region, then compare byte-for-byte against the
single-line frozen quote). It is **unreachable** under a literal byte-exact
reading of the quote. The clause as written ("ONLY where the frozen quote itself
carries a newline") selects the unreachable reading for exactly the three quotes
that need the other one. My draft implements pin-region as the default and
exposes `--judge byte-exact` so the divergence is measurable rather than asserted:

```
### B. lane @ base e25149fe, pin-region judge (stdout only)
MADO_ERRATA_TRUTH: rev=e25149fec8152a3aabd2b18a0ee8663b23cf65aa propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET
exit=0

### C. lane @ base, byte-exact judge (stdout only)
MADO_ERRATA_TRUTH: rev=e25149fec8152a3aabd2b18a0ee8663b23cf65aa propositions=4/4 quotes=1/4 anchors=1/4 pins=4/4 controls=6/6 verdict=TARGET_MISSED
exit=1
```

**Recommendation to L1 (registration text, not a claims-frozen edit).** The
`claims-frozen.md` predicate sentence says the Quote cell must occur "verbatim and
contiguous". A counter author who reads that as byte-exact will build a counter
that cannot pass at the frozen table, and the round would report an honest stop
that is really a specification artifact. The clause in `registration.md` should
say *whitespace-collapsed contiguity in the pin region, spanning exactly the cited
anchor*, naming the house rule explicitly. `claims-frozen.md` is frozen and must
not be edited; if L1 judges the predicate sentence itself to be the defect, the
route is a pre-data re-registration under a NEW versioned file
(`claims-frozen-v2.md`), which the round's own rules already provide.

**Consequence for the wave.** Seats that build the counter must pin the judge
choice in the counter's docstring and must report which reading they used. A
counter whose docstring says "byte-exact" will score `quotes=1/4` at base and
look like a failed claim; that is a defect of the counter, not of the entry.

## 2. What the counter must check, leg by leg

The frozen line is `MADO_ERRATA_TRUTH: rev=<rev> propositions=4/4 quotes=4/4
anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET`, so the four counters must
be independent legs, not one boolean restated four times. Concretely:

| leg | what it must bind | what it must NOT bind |
|---|---|---|
| `propositions` | the entry's P19–P22 rows exist **and** match the frozen table byte-for-byte modulo trailing spaces | the prose of the Proposition column (see §4.5) |
| `quotes` | each frozen quote occurs contiguously in the pin its **own row** names, and the occurrence spans exactly the row's cited anchor range | the pin's *file* identity alone (that is what C1-CTL-6 attacks) |
| `anchors` | the located span equals the frozen anchor and satisfies the frozen side-claim (the `within 591–627` / `after 571` halves) | the anchor string alone (a shift must not be absorbed by the quote leg) |
| `pins` | the four frozen pin **files** are present, their bytes hash to the frozen round-52 digests, **and** the tree's own `SHA256SUMS` records the same digest | the tree's `SHA256SUMS` alone (see §4.1) |
| `controls` | the six frozen controls, each rejected | — |

Two of these need care and are where the naive draft fails.

**The `pins` leg must be checked twice.** C1-CTL-3 attacks the tree's
`SHA256SUMS` (one recorded sha256 nibble changed → `pins≤3/4` MISSED). A counter
that reads only the tree's `SHA256SUMS` therefore *does* reject C1-CTL-3 — but it
admits a tree whose **pin bytes** were edited and whose `SHA256SUMS` was updated to
agree with the edit. The predicate leg (c) says "each of the four pins' bytes hash
to the **round-52 recorded sha256**", i.e. the digests frozen in `registration.md`,
not whatever the tree happens to say about itself. Requiring **both** (frozen digest
AND tree `SHA256SUMS` agree) rejects CTL-3 with `pins=3/4` as the frozen control
requires *and* closes the self-consistent re-pin. Measured (§4.1).

**The `propositions` leg must absorb the frozen-table drift.** The registration
requires the counter to check the entry's extracted rows "against THIS table
byte-for-byte modulo trailing spaces; any drift is a TARGET_MISSED". If drift is
only reported as a detail line and not counted, the counter can print
`propositions=4/4` while the tree has drifted. My draft decrements the
`propositions` counter on drift, so a drifted tree reads `propositions=3/4`.

## 3. The draft counter

`/fast/scratch/hyaku/mado-r54/R54Seat01/c1-r54-errata-truth.py` — modelled on
`quality/counters/c2-r51-dispatch-entry.py` (same `--repo/--rev/--work/--selftest`
shape, same `git -C` + `git show` object reads, same scratch discipline: `--work`
or a `mkdtemp` under `$TMPDIR`, nothing written outside it).

Behaviour verified:

- **Reads git objects, not the worktree.** A dirty worktree entry file does not
  change the verdict at a fixed `--rev` (checked by appending a marker to the
  worktree copy, re-running, then restoring — verdict unchanged, file restored).
- **stdout is exactly one line.** The predicate says "prints one line"; detail
  lines go to stderr. The harness asserts this on every case.
- **Scratch inside the scored repository is refused** (exit 2, setup error), so a
  counter run can never write into the tree it scores. Checked: `--work` pointing
  into `.ufo/waves/round-54/w1/` is refused and **no directory is created**.
- **Absent entry at an older rev is a clean miss, not a crash.** At
  `ad4bf2059bcfafe63671d262222908ee1fe8001c` (before the errata entry landed) it
  prints `propositions=0/4 quotes=0/4 anchors=0/4 pins=0/4 controls=0/6
  verdict=TARGET_MISSED`, exit 1. (My first draft raised `AttributeError` here —
  fixed; noted because a crashing counter is scored `ERROR`, never `ok`, by the
  lane's own discrimination gate.)
- **A bogus rev is a setup error**: exit 2, `detail=cannot resolve rev …`.
- **Selftest: 42/42 assertions**, including one red run per frozen control and
  the judge-divergence, duplicate-row, multi-occurrence and re-pin cases. This
  exceeds the registration's "≥ 30 assertions including one red run per control".

```
$ python3 -I c1-r54-errata-truth.py --selftest --repo . --rev HEAD
C1_R54_SELFTEST: 42/42 assertions passed
```

## 4. Distinct failure inputs (this seat's own; the frozen six do not cover these)

The harness builds **real git repositories** whose trees are mutated copies of the
scored tree, commits them, and runs the counter as a **subprocess** against
`--repo <fixture> --rev <commit>` — the shape the registration demands ("the
counter reads all inputs from `--repo`/`--rev` git objects, so a control = a
mutated copy of the scored tree"). Fixtures live under the designated scratch,
created with `mktemp -d`; every git call is `git -C <fixture> …` with an explicit
path; `git rev-parse --show-toplevel` is asserted to print the fixture dir before
every commit. The lane and the source repo are read-only throughout.

### 4.1 The pin-byte laundering hole (`pin-edit`) — **the frozen six miss it**

C1-CTL-3 edits the tree's `SHA256SUMS`. It does **not** edit the pin bytes. So a
counter that recomputes the digest over the *live lane file* — which is what a
literal resolver of the recorded `SHA256SUMS` paths does, because the round-52
`SHA256SUMS` records **absolute** paths under the lane's own checkout:

```
$ cat .ufo/waves/round-52/fetch/SHA256SUMS
a83abeb57175e65908d8d67ddc9802310134e5a4752fa3764f980401b48a7637  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/Hyprland-ConfigActions.cpp
746c6f517620eb039afbfbb9a4a0e2d5ba1c5eb117bcc8f396173f63091b7073  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/Hyprland-ConfigActions.hpp
8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/Hyprland-KeybindManager.cpp
7248cbb89f898c783c50c89d068df9821a6b38aeb6abeb6064e92c1610fbe771  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/Hyprland-legacy-DispatcherTranslator.cpp
c53296aeafcdd746ececcb183bcffaf76467a9917db46ae5dc5591bcde674ad0  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-52/fetch/README.txt
```

`pin-edit` appends a comment to the pin's bytes and leaves `SHA256SUMS` alone.
The quoted text is untouched, so the quote leg still passes; the bytes no longer
hash to the recorded digest, so leg (c) must reject.

```
# naive variant (resolves the recorded absolute paths literally):
case pin-edit      expect=TARGET_MISSED got=TARGET_MET   exit=0 **FAIL**

# my counter:
case pin-edit      expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
```

**Recommendation.** A counter must (i) key the `SHA256SUMS` map on the **basename**
— the recorded paths are absolute and meaningless in a clone — and (ii) compare
against the **frozen** digests, not only the tree's own file. Both together make
`pin-edit` and the self-consistent re-pin (`launder`) misses.

### 4.2 `launder` — pin bytes and `SHA256SUMS` edited together

The tightest variant of §4.1: the pin's bytes are edited *and* the tree's
`SHA256SUMS` is updated to agree. Any counter that trusts only the tree's
`SHA256SUMS` admits this outright. My counter rejects it (`pins=3/4`) because the
edited bytes no longer hash to the frozen digest.

### 4.3 `dup-row` — a duplicated proposition id

The frozen table names exactly four propositions. A verbatim-duplicated `P19` row
is table drift. A counter that keys a dict by proposition id and lets the last row
win is indifferent to the duplicate. **My own first draft had this bug** — the
harness caught it (`dup-row` → `TARGET_MET`) — and it is now fixed: a repeated id
lowers `propositions` to 3/4 → `TARGET_MISSED`. This is not in the frozen six.

### 4.4 `reanchor` — a cited range that still *contains* the quote

`P19`'s anchor moved from `:1554-1558` to `:1550-1560`. The quote is still
contiguous in the pin and still inside the cited range, so a counter that asks
only "is the quote somewhere in this range" admits it. Both the quote leg (the
occurrence's span must equal the cited range) and the anchor leg (the range must
equal the frozen anchor) reject it. **My own first draft had this bug too** — it
located the first occurrence in the file rather than the occurrence *at* the cited
anchor — and was fixed; the fix is generalised in §4.6.

### 4.5 Prose drift is out of scope, and that is a scope decision to state

Editing the entry's `Proposition` **prose** cell for P19 (e.g. "sends nothing at
all, ever.") leaves every leg green:

```
proposition-prose drift -> MADO_ERRATA_TRUTH: rev=df745580848cba7e9e62e45b807017b34b22ae97 propositions=4/4 quotes=4/4 anchors=4/4 pins=4/4 controls=6/6 verdict=TARGET_MET exit=0
```

This is **correct** under the frozen predicate: the frozen table carries only
ID / Pin file / Anchor / Quote, and the predicate binds the quote, the anchor and
the hash — not the prose. But it means the counter certifies *source truth of the
cited evidence*, not the truth of the English sentence. Worth stating in the
counter's docstring so the capability is not over-claimed.

### 4.6 Multi-occurrence quotes

If a pin carries the same quote twice, the counter must judge the occurrence **at
the cited anchor**, not the first occurrence in the file. Asserted in the selftest
by duplicating P20's quote in the fixture: the counter still resolves
`quotes=4/4 anchors=4/4` (the occurrence at 1576 is the one judged). Each of the
four frozen quotes occurs exactly once in its committed pin today, so this is a
robustness property, not a live discrepancy.

### 4.7 `sums-rename` — the `SHA256SUMS` filename

`registration.md`'s C1 inventory prose says "hashes from its committed
`SHA256SUMS.txt`", but the round-52 tree actually ships the file as
**`SHA256SUMS`** (no extension); `.ufo/waves/round-54/fetch/` (C2's directory)
does use `SHA256SUMS.txt`. A counter that hardcodes one spelling breaks on the
other. My counter accepts both (`sums-rename` → `TARGET_MET`); the naive variant,
which hardcodes `SHA256SUMS`, reads `TARGET_MISSED` on the renamed tree. A
counter should accept either spelling, or the registration prose should be
corrected.

### 4.8 The harness has teeth — the §9 do-nothing control

`stub-always-print.py` prints the frozen green line and reads nothing. Run
against a mutated tree it still prints `TARGET_MET`; the harness detects that and
reports it, so the harness cannot be satisfied by a counter that prints:

```
case stub-green   (stub green) exit=0 verdict=TARGET_MET
case stub-ctl5    (stub on a mutated tree) exit=0 verdict=TARGET_MET -> stub correctly detected as a do-nothing counter
```

Note for the wave: the counter's **own** control run (`controls=6/6`) is what makes
the frozen line honest. A counter that hardcodes `controls=6/6` prints the frozen
line on a mutated tree; only the counter's internal control run distinguishes it.

### 4.9 Full harness result

```
### D. harness, 15 cases
case green        expect=TARGET_MET   got=TARGET_MET   exit=0 OK
case ctl-1-splice expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
case ctl-2-shift  expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
case ctl-3-hash   expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
case ctl-4-range  expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
case ctl-5-drop   expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
case ctl-6-swap   expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
case launder      expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
case pin-edit     expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
case dup-row      expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
case reanchor     expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
case widen-quote  expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
case sums-rename  expect=TARGET_MET   got=TARGET_MET   exit=0 OK
case stub-green   (stub green) exit=0 verdict=TARGET_MET
case stub-ctl5    (stub on a mutated tree) exit=0 verdict=TARGET_MET -> stub correctly detected as a do-nothing counter
HARNESS: 15/15 cases as expected
```

The naive variant, same harness, same fixtures — two cases differ:

```
### E. naive variant (absolute-path SHA256SUMS resolver) — 2 cases differ
case green        expect=TARGET_MET   got=TARGET_MET   exit=0 OK
case launder      expect=TARGET_MISSED got=TARGET_MISSED exit=1 OK
case pin-edit     expect=TARGET_MISSED got=TARGET_MET   exit=0 **FAIL**
case sums-rename  expect=TARGET_MET   got=TARGET_MISSED exit=1 **FAIL**
HARNESS: 11/13 cases as expected
```

## 5. Edge-case checklist for whoever lands the counter

1. **Pin the judge in the docstring** — pin-region (default) or byte-exact; the
   frozen line differs (`quotes=4/4` vs `quotes=1/4`). See §1.
2. **Key `SHA256SUMS` on the basename**; the recorded paths are absolute. (§4.1)
3. **Compare against the frozen digests as well as the tree's own file.** (§4.1, §4.2)
4. **Accept both `SHA256SUMS` and `SHA256SUMS.txt`.** (§4.7)
5. **Count frozen-table drift in the `propositions` counter**, not only in a
   detail line. (§2)
6. **Reject a duplicated proposition id** rather than resolving it silently. (§4.3)
7. **Judge the quote occurrence at the cited anchor**, not the first occurrence;
   require the occurrence's span to equal the cited range. (§4.4, §4.6)
8. **One stdout line**; details to stderr. The predicate says "prints one line".
9. **Refuse a scratch root inside the scored repository** (exit 2), as the house
   counters do.
10. **Handle an absent entry without crashing** — a crash is scored `ERROR`,
    never `ok`, by `quality/check-counter-discrimination.py`.
11. **Do not resolve the pin's absolute path from `SHA256SUMS`; read the blob at
    `--rev`.** A counter that reads the live lane is not scoring the revision it
    was asked to score.
12. **A counter that reads the live lane** also breaks under the round's own
    fixture protocol (the fixtures live elsewhere), so this is not a hypothetical.

## 6. Harm watch and scope

- `bash tools/mado-verify.sh --selftest` → `MADO_SELFTEST: 460/460 assertions passed` (unchanged).
- Sources census → `TZ=UTC bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mado`
  → `mado ok /home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md`, **exit=0** (unchanged).
- Navigation index: the lane's `corpus/README.md` and `corpus/SOURCES.md` show as
  modified and `corpus/knowledge/uwsm-app-environment-r54.md` / `corpus/lessons/round-54.md`
  as untracked — these are **sibling seats'** C2 work, not this seat's. This seat
  wrote no tracked lane file.
- No config tree, compositor, service, sibling repo or host substrate was read or
  written. No package query, no input capture, no screenshot, no producer
  execution. The only host reads were `git show` on the lane's own objects and
  the two lane gates above; the source repo `/home/vgpnk/Projects/shokuknow` was
  never opened.
- No git/jj mutation in the lane, no commit, no push, no delegation, no
  background job. All fixtures were scratch-local `mktemp -d` repositories with
  `git -C <fixture>` and a toplevel assertion before each commit.
- One transient directory (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-54/w1/tmpprobe`)
  was created by a `--work` probe and removed with `rmdir` in the same session;
  it was empty and is gone. A second probe (`tmpprobe2`) was refused before
  creation by the counter's scratch rule.
- **Tooling: none installed or updated.** python 3.14.8 and git 2.56.0 were
  already present; the RULES.md tooling directive had nothing to act on.

## 7. Open items for L1 / wave 2

1. **The judge clause is ambiguous and the two readings disagree on the frozen
   table** (§1). This is the highest-value item in this report: it decides whether
   PRED-C1-r54 is satisfiable. Recommendation: correct `registration.md`'s judge
   clause to name the house rule (whitespace-collapsed contiguity in the pin
   region, spanning exactly the cited anchor). `claims-frozen.md` is frozen and
   was not touched; if L1 judges the predicate sentence itself to be at fault, the
   route is a pre-data re-registration under a NEW versioned file.
2. **The six frozen controls do not close the pin-byte laundering hole** (§4.1,
   §4.2). A counter that trusts only the tree's `SHA256SUMS` passes all six and
   admits an edited pin. Wave 2 should hold the landed counter to `pin-edit` and
   `launder` in addition.
3. **The frozen six do not cover a duplicated proposition id** (§4.3) or a
   **widened cited range** (§4.4). Both were live bugs in this seat's own first
   draft; a landed counter that has not been tested against them may carry them.
4. **`registration.md` names `SHA256SUMS.txt` where the round-52 tree ships
   `SHA256SUMS`** (§4.7). Either the prose or the counter's tolerance is wrong.
5. **The counter's own control run is what makes `controls=6/6` honest** (§4.8);
   a landed counter must run the six controls in-process, not print the number.
