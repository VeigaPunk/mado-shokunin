# CritC2V2Forgery (round 44, w2) - forgeries against PRED-C2-r44-v2

Seat: `w2/CritC2V2Forgery`. Target: `quality/counters/c2-r44-gkeep-size-request-v2.py` (frozen in
`.ufo/waves/round-44/registration-v2.md`, commit `03fa5c61`), data commit `e46789213830597348fe96a351ae004d10587385`, base
`6a1a90528fe533cadee506a9fa3e9d13d15cc41f`. Nothing in the lane was written outside this seat's directory; the
forgeries live in a scratch clone `/fast/scratch/hyaku/mado-r44/CritC2V2Forgery/clone` (cloned `--shared`, every
git call `-C <clone>`, toplevel checked) and the seat holds their bytes plus a deterministic builder.

## Result in one line

**Seven forged entries, all admitted** by the frozen counter (`admitted=1/1`, exit 0, 12/12 clause-j surfaces
"cited" in every one), against three findings: **two mechanical holes** (clause j has no range-width bound; clause
h tests the census numbers only in four call-site spellings, not in the census's own `default_size=` /
`size_request_calls=` form) and **one predicate-text mismatch**; the other three forgeries confirm the declared
residuals are real and load-bearing.

Baseline first: the genuine data entry scores `a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1 j:1 admitted=1` exit 0
(`receipts-score-baseline-data.txt`), so every forgery below is a delta from a passing entry, not from a
broken counter.

## The seven forgeries (all reproduced by `repro.sh`; hashes deterministic across two clean runs)

| # | fixture (seat dir) | commit in clone | attacked clause | frozen verdict |
|---|---|---|---|---|
| F1 | `fixtures/f1-surface-false.md` | `dd4ac1cc` | clause j | admitted 1/1, j:1, 12/12 cited |
| F2 | `fixtures/f2-decision-table-noid.md` | `f5be7018` | clause j + g (`all_body_lines_bound`) | admitted 1/1, j:1, 12/12 cited |
| F3 | `fixtures/f3-census-words.md` | `38b15227` | clause h | admitted 1/1, h:1 |
| F4 | `fixtures/f4-wide-range.md` | `46ca8538` | clause j (range width) | admitted 1/1, j:1, 12/12 cited |
| F4b | `fixtures/f4b-eof-range.md` | `43333883` | clause j (range width, EOF-exact) | admitted 1/1, j:1, 12/12 cited |
| F5 | `fixtures/f5-one-line-all-surfaces.md` | `3c98a6cc` | clause j (one line, twelve locators) | admitted 1/1, j:1, 12/12 cited |
| F6 | `fixtures/f6-census-numbers-false.md` | `52b1e1b8` | clause h (census value forms) | admitted 1/1, h:1 |

Per-commit logs: `receipts-score-<8>.txt`; `fixtures/commits.txt` is the hash-to-fixture map.

## Finding 1 (F4, F4b) - clause j accepts a locator that spans the whole file. OPEN predicate defect, HIGH

**Attacks** `quality/counters/c2-r44-gkeep-size-request-v2.py:398` (`if int(a) <= L <= int(b or a):`) and the
predicate text at `:58-59` ("carries a locator `<receipt>:<a>[-<b>]` with a <= L <= b").

**Forgery.** F4 is a skeleton: header, five quoted id lines, two census lines, and five sentences of the form
`realToReportSize, sendWindowSize, the X11 branch and the ack list are all read here (Hyprland-Window.cpp:1-9999).`
(`fixtures/f4-wide-range.md:29,31,33,35,37`). Every sentence is true and says nothing; each range covers every line
of its file. The counter prints `clause=j surface=... cited=1` twelve times
(`receipts-score-46ca8538.txt`). F4b repeats it with ranges exactly at each file's length
(`Hyprland-Window.cpp:1-2966`, `Hyprland-XDGShell.cpp:1-980`, `xdg-shell.xml:1-1420`,
`gdktoplevel-wayland.c:1-2964`, `gkeep-ui.py:1-488`), so no upper-bound test can distinguish it from a real
citation either.

**Why it matters.** The freeze controls rejected `SHELL` on clause j alone (`.ufo/waves/round-44/receipts/ctl-c2-v2.txt:7`,
`... a:1 b:1 c:1 d:1 e:1 f:1 g:0 h:1 i:1 j:0 admitted=0`). The control was header plus census lines only; adding the five quoted id lines
clauses d/g/h require and five whole-file sentences flips it to admitted. Clause j was registered to answer `w1/CritClaimSizing` F1 (an entry "admitted while holding none of the
claimed surfaces", `registration-v2.md:52-55`); with whole-file ranges it certifies coverage it does not measure.
This is not the declared residual: `registration-v2.md:64-65` admits the *truth of the sentence* is unbound, but
F4's sentences are true and empty - the locator itself no longer denotes a place.

**Smallest safe correction (tested).** One condition at `:398`:

```python
if int(a) <= L <= int(b or a) and int(b or a) - int(a) <= 40:
```

The widest locator in the genuine data entry is 14 lines (`Hyprland-Window.cpp:1685-1699`;
`receipts-locator-widths.txt`), so any cap from 20 upward leaves the entry admitted. Tested at 40:
`receipts-widthcap-scores.txt` - data commit MET, F4 and F4b `admitted=0/1` with every surface
`cited=0`; F1, F2, F3, F5 unaffected.

## Finding 2 (F6) - clause h checks four spellings of the census, not the census's own form. OPEN predicate defect, HIGH

**Attacks** `quality/counters/c2-r44-gkeep-size-request-v2.py:586-604` (the T3 block) against
`registration-v2.md:50-51` ("census numbers not contradicted by prose") and the docstring at `:50` ("and no other
entry line contradicts them").

**Forgery.** F6 is the genuine entry plus one line in the census's own format with false values:
`gkeep client default_size=640x480 size_request_calls=7 application_id=org.omarchy.gkeep`
(`fixtures/f6-census-numbers-false.md:92`). The pins say `set_default_size(420, 500)` (`gkeep-ui.py:476`) and zero
`set_size_request(` calls (`.ufo/waves/round-44/fetch/gkeep-ui.py`, count 0; `receipts-verify-false-lines.txt`). The entry is
admitted with h:1 and no `clause=h prose` line: h only matches `set_size_request(`, `set_default_size(w, h)`,
`xdg_setSize=` and `x11_configure=`, so `default_size=WxH` and `size_request_calls=N` on any other line are
unbound. The exact census string is required exactly once (`host_census`, `:348`) and the second, false one is
never compared.

**Why it matters.** The census is the entry's central fact for S301/gkeep and the value T3 exists to protect; a
forger reproduces its format with wrong numbers and the counter prefers the true line. Numeric contradiction is
the one thing the registration promises is caught.

**Smallest safe correction (tested).** Two checks inside the T3 loop, after `:604`:

```python
                for w, h in re.findall(r"(?<!set_)default_size=(\d+)x(\d+)", l):
                    if (w, h) != (W0, H0):
                        h_ok = False
                for v in re.findall(r"size_request_calls=(\d+)", l):
                    if int(v) != N0:
                        h_ok = False
```

Tested (`receipts-censusforms-scores.txt`): data commit MET; F6 `admitted=0/1` with
`clause=h prose default_size=640x480 != 420x500` and `clause=h prose size_request_calls=7 != 0`; F1, F2, F3, F4,
F4b, F5 unaffected. Both corrections together: `receipts-widthcap-censusforms-scores.txt` (data MET;
F4, F4b, F6 MISSED; F1, F2, F3, F5 still MET - as classified below).

## Finding 3 (F3) - a wrong predicate sentence in the frozen docstring. Text defect, LOW; not a code hole under the registration's own wording

**Attacks** `quality/counters/c2-r44-gkeep-size-request-v2.py:50`. The sentence reads: "and no other entry line
contradicts them:" followed by the three numeric forms. The code implements exactly the three forms; the first
clause of the sentence is universal, the code is not.

**Forgery.** F3 is the genuine entry, byte for byte, plus four sentences that deny the census in words and carry
no number, no id and no call spelling (`fixtures/f3-census-words.md`, tail):

- `gkeep also asks the toolkit for a minimum window size, and the compositor honors that minimum over its own goal.`
  (contradicts `size_request_calls=0`)
- `On X11 the compositor never configures a surface directly; X11 windows keep whatever size the client picks.`
  (contradicts `x11_configure=1`)
- `The toplevel's setSize never puts a size on the wire, so no configure is ever delivered.` (contradicts
  `xdg_setSize=1`)
- `A gkeep window opens at whatever size the widget tree wants; gkeep declares no size of its own.` (contradicts
  `default_size=420x500`, `gkeep-ui.py:476`)

Admitted, h:1 (`receipts-score-38b15227.txt`).

**Classification.** The registration's predicate summary already narrows the promise to numbers
(`registration-v2.md:50-51`, "census numbers not contradicted by prose"), so the *behaviour* matches the
registration and F3 is a declared-residual-class admission. What is wrong is the docstring's broader sentence,
which is authoritative (the registration names the docstring as the predicate, `registration-v2.md:49`).

**Exact corrected sentence (docstring, line 50-51; for the next registration only - the predicate is frozen):**

> and no other entry line contradicts the censused numbers in one of these forms: a `set_size_request(` call when
> N = 0, a `set_default_size(w, h)` other than W, H, an `xdg_setSize=` or `x11_configure=` value other than X, Y, a
> `default_size=WxH` or `size_request_calls=N` value other than W, H, N (T3);

Do not attempt a lexical negation detector ("never", "no"): the genuine entry contains
"no gkeep window was open" (`corpus/knowledge/hyprland-gkeep-size-request-r44.md:78`) and would be flagged. The
honest resolution is the narrower sentence plus a declared residual for word-form prose.

## Findings 4-6 (F1, F2, F5) - the declared residuals, confirmed at full strength. No correction proposed

**F1 (declared, `registration-v2.md:64-65`).** Twelve body sentences, one per surface, each carrying the
surface's keyword and a locator that covers the counter-computed anchor, each false against its pin:
`realToReportSize returns the monitor's width for every client and never clamps it (Hyprland-Window.cpp:1685-1699)`
(`fixtures/f1-surface-false.md:29`) against `Hyprland-Window.cpp:1687`; `sendWindowSize transmits on every call`
against the early `return` at `:1743`; `The X11 branch is dead code` against the `configure` call at `:1751`;
`No ack is ever processed` against `onAck` at `:1514`; `setSize ... keeps no pending state` against
`Hyprland-XDGShell.cpp:355`; `The sendConfigure call is never reached` against `:455`; `A zero width or height is
an error` against `xdg-shell.xml:1154`; `The client never sends ack_configure` against `:560`; `GTK discards the
configured size` against `gdktoplevel-wayland.c:681`; `GTK never constrains` against `:525`; `A 0x0 configure is
treated as an ordinary size` against `:647`; `gkeep sets no application id` against `gkeep-ui.py:449`. Every line
verified by grep in `receipts-verify-false-lines.txt` (`VERIFY: PASS`, 22 checks). Admitted with 12/12
surfaces cited. This is exactly what "clause j binds a locator and a keyword per surface, not the truth of the
sentence" (`registration-v2.md:64-65`, 16 words) declares, so it is a declared residual, severity MEDIUM: a reader
who reads the counter's twelve `cited=1` lines as coverage would accept an entry whose every mechanism sentence is
false.

**F2 (declared, `quality/counters/c2-r44-gkeep-size-request-v2.py:66`).** A twelve-row decision table whose answers are all invented
("exactly the size the client asked for", "an error the client must report", "none; the window is anonymous") with
the keyword and a covering locator in the third column and **no id on any row**
(`fixtures/f2-decision-table-noid.md:29-42`). `all_body_lines_bound` never fires because no line names a cited id;
clause j is satisfied by the table itself. Admitted. Declared: "a decision table naming no id is not bound"
(`:66`).

**F5 (declared, same residual as F1).** One sentence carrying all twelve keywords and twelve point locators
(`fixtures/f5-one-line-all-surfaces.md:27`): "The report size, sendWindowSize, the X11 configure branch, the ack
list, setSize, ... are all covered by these twelve locators: Hyprland-Window.cpp:1685, ...". Admitted, 12/12
cited, **and it survives the Finding-1 width cap** (`receipts-widthcap-scores.txt`, rev `3c98a6cc`
MET). It is reported because it bounds the correction: a width cap stops whole-file saturation, not multi-surface
one-liners; separating those lexically is not possible without rejecting the genuine entry's own paragraph
(`corpus/knowledge/hyprland-gkeep-size-request-r44.md:30` carries three surfaces with three locators on one line).

## What the landed claim does and does not lose

Nothing moves in the published axis: the data commit still scores `admitted=1/1 TARGET_MET` under the frozen
counter and under all three patched copies (`e4678921` MET in `receipts-widthcap-scores.txt`,
`receipts-censusforms-scores.txt`, `receipts-widthcap-censusforms-scores.txt`), so C2's after-state
(SCORECARD round-44 note, "C2 **coverage**", `SCORECARD.md:2571`) stands, and C1 is untouched (C2's counter reads
no tool). What the findings bound is the *reach* of PRED-C2-r44-v2 as a coverage instrument: the twelve
`cited=1` lines do not establish that the entry holds the surfaces, and one false census line in the census's own
format is admitted. SCORECARD's planned item 3 for round 45 already books "The w2 open predicate defects of round
44, under a new registration" (`SCORECARD.md:2591`); Findings 1-2 belong there, with the tested corrections above.

## Impacted axes

- C2 **coverage** (sourced; assimilation): predicate reach, not the counter line. Genuine data entry unaffected.
- C1 **operability**: not touched (no tool or fixture read by the C2 counter writes `tools/mado-geometry.py`).
- Registry/lesson/README clauses (c-i): untouched; all seven forgeries reuse the genuine rows, Gate and README row,
  so each admission isolates the entry text.

## Reproduction

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin
bash .ufo/waves/round-44/w2/CritC2V2Forgery/repro.sh    # ~12 s; writes the receipts into this seat, exit 0
```

It clones the lane `--shared` into `/fast/scratch/hyaku/mado-r44/CritC2V2Forgery/clone`, checks the clone toplevel,
regenerates the three patched counter copies from the frozen counter (`patch.py`), commits the seven fixtures with
fixed author/committer dates (`build.py`, hashes stable across two clean runs), scores the data commit and all
seven with the frozen counter, runs `verify.py` against the pins, and scores everything under the three patched
copies. `receipts-repro-log.txt` is one full transcript.

## Limits of this review

- Only entry text was forged; registry cells, the lesson Gate, the README row and the pins were the genuine ones, so
  these findings say nothing about clauses c-i beyond what the freeze controls already established.
- The falsehood of F1/F2/F3/F6 sentences is established against the five pinned receipts only; no live host read and
  no `hyprctl` call was made (none was needed).
- The width cap at 40 is a guess bounded below by the genuine entry's 14-line maximum; any threshold in 20..40 was
  not individually swept.
- The three patched copies are proposals: the predicate is frozen before data, and no re-registration after data is
  admissible (registration kill rule). Nothing here edits the counter, the controls, the registration or the entry.
- Out of scope (other w2 seats): C1's predicate, the SKILL/PROVINCE/QUALITY text, and the ratio-domain-meta tool.

## Tooling

None installed. `python3` (3.14, stdlib only) and `git`; no package transaction, no compositor call, no network
fetch. Scratch directory `/fast/scratch/hyaku/mado-r44/CritC2V2Forgery/` is deleted at the end of this seat; every
path cited above is inside this seat directory.
