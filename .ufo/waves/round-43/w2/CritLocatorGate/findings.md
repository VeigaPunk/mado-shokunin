# CritLocatorGate — findings: the new locator checker judges the wrong inputs (round 43, w2)

**Target.** `quality/check-locators.py` (sha256 `c1ea52ad5db21fdf81022d0425e7cad42fc3e34dd5083915b127a46ab948a27e`, byte-identical to
the w1 deliverable `.ufo/waves/round-43/w1/ExecLocatorGate/check-locators.py` — the data commit shipped the w1 file unchanged) and
**QUALITY criterion 77** (`corpus/QUALITY.md:401` at the data commit).

**Revision attacked.** `1959770657f1f8665097c1aed4be6c1cbb07139f` (data). Prose inputs are `git show <rev>:<path>` extracts of
`SKILL.md` (sha256 `1753e844…`, 2073 lines), `LOG.md` (`f6c27a36…`, 2483 lines) and the 60 files of `corpus/knowledge/`, plus an
auxiliary extract of `corpus/lessons/round-43.md` (`lesson43.md`) because criterion 77 names lessons and that file quotes the
round-42 defect the checker exists to catch.

**Reproduce (scratch is deleted, the revision is not):**

```
REV=1959770657f1f8665097c1aed4be6c1cbb07139f; W=$(mktemp -d)
git -C mado-shokunin show $REV:SKILL.md > $W/SKILL.md; git -C mado-shokunin show $REV:LOG.md > $W/LOG.md
mkdir -p $W/corpus/knowledge
for f in $(git -C mado-shokunin ls-tree -r --name-only $REV -- corpus/knowledge); do git -C mado-shokunin show $REV:$f > $W/$f; done
cd mado-shokunin && python3 -I quality/check-locators.py --fetch .ufo/waves/round-43/fetch $W/SKILL.md $W/LOG.md $W/corpus/knowledge/*.md
```

(expect `locators=16 miss=1`; the extracted `SKILL.md`/`LOG.md` sha256 are `1753e844…`/`f6c27a36…` as recorded above).

**Commands (all outputs are seat files).**

```
python3 -I quality/check-locators.py --selftest
python3 -I quality/check-locators.py --fetch .ufo/waves/round-43/fetch [--explain] <62 prose files>
python3 -I quality/check-locators.py --fetch .ufo/waves/round-42/fetch  <62 prose files>
python3 -I .ufo/waves/round-43/w2/CritLocatorGate/strictcheck.py  --fetch .ufo/waves/round-43/fetch <62 prose files>
python3 -I .ufo/waves/round-43/w2/CritLocatorGate/patchedcheck.py --fetch .ufo/waves/round-43/fetch <prose files / mutants>
```

## Headline

The shipped checker is **honest about its limits and has teeth on the defect it was built for** — and it is **blind to the
classes criterion 77 names**: a fact whose payload is numbers, a quote with its operands swapped, a locator whose line was
wrapped, a locator with no backticked fragment, a locator pointing past end-of-file. I built 13 inputs against the real pins
and 9 against a synthetic receipt; **20 of the 22 are judged wrongly** — 19 pass a wrong locator or a fabricated fragment
(11 real-pin, 8 synthetic), 1 refuses a correct one — and a **mutated copy of the landed entry passes with `miss=0`,
exit 0** (M1, M7). Only the two positive controls are judged right (A8 `OK`, S7 `MISS`). The landed data itself is clean
under a stricter test: all 14 `OK` verdicts carry the attributed quote verbatim in the cited range, and every digit run of
the fragment is present (`strict-r43.txt` → `ok_but_weak=0`). The one frozen `MISS` on the mandated set is a **real** error,
carried unchanged from round 42.

## 1. What the run finds (supports the data, not the gate)

| run | result | seat file |
|---|---|---|
| `--selftest` | `cases=18 passed=18 locators=19 miss=6`; `teeth flipped_table_broken=yes flips=11 ok_to_miss=4 miss_to_ok=5`; `SELFTEST: PASS`, exit=0 | `selftest.txt` |
| mandated 62 files, `--fetch r43` | `locators=16 miss=1`, rc 1 | `run-r43-fetch.txt` |
| mandated 62 files, `--fetch r42` | `locators=15 miss=1`, rc 1 | `run-r42-fetch.txt` |
| entry alone | `locators=10 miss=0`, rc 0 | `pristine-runs.txt` |
| `SKILL.md` alone | `locators=5 miss=0` (1 `NOFRAG`), rc 0 | `pristine-runs.txt` |
| `LOG.md` alone | `locators=1 miss=1`, rc 1 | `pristine-runs.txt` |
| test: quote present verbatim in the range | `ok=14 ok_with_absent_quote=0 ok_with_absent_number=0 ok_on_empty_range=0` | `strict-r43.txt` |

The 16→15 difference between the two fetch dirs is exactly the entry's `host-clients-r43.json:50-51`: **under `--fetch
.ufo/waves/round-42/fetch` the round's own census locator silently disappears** and the miss count is unchanged, so a reviewer
who passes the wrong (or only one) fetch dir cannot tell he stopped checking a locator.

## 2. FALSE OK — a locator the checker passes whose range does not hold the fact

Each row was run; the verdict in the row is the checker's output.

| # | input (seat file `adv-real.md`, `adv-synth.md`) | verdict | why it is wrong |
|---|---|---|---|
| A1 | `the goal box comes from `size` at `Hyprland-HyprCtl.cpp:394-395,412-413`` | `OK` (`supported=1`) | the range is JSON template text (`"size": [{}, {}]`, `"at": [{}, {}]`); the shared word `size` supports it. This is exactly criterion 77's "a word it shares with an unrelated line", and the checker returns `OK` for it |
| A5 | `the client asks for `window.set_default_size(640, 720)` at `gkeep-ui-excerpt.py:33-34`` | `OK` | `:33` reads `set_default_size(420, 500)`. `ID_RE` has no digit class, so **numbers are never compared** — and the number *is* the fact |
| A6 | `the rule is `windowrule = size 900 1000, match:class ^(org.omarchy.gkeep)$` at `host-gkeep.conf:4`` | `OK` | `:4` reads `size 420 500` |
| A9 | `the accessors are `m_realSize->value(); case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal()` at `Hyprland-GeometricMovableAnimated.cpp:19-20`` | `OK` | the fragment as written is in neither line; the token **set** is. Order and operators are not tested |
| A2 | `the window handle is `w->x` at `Hyprland-Target.cpp:10`` | `NOFRAG` | tokens of `w->x` are 1 char, dropped by `len(t) >= 3`; `fragments=0`, nothing checked, exit 0 |
| A3/A4 | `` the goal is `m_realSize->goal()` `` / newline / ``(`Hyprland-GeometricMovableAnimated.cpp:999`)`` and `the goal accessor is at Hyprland-GeometricMovableAnimated.cpp:999.` (no backticks) | `NOFRAG` | `Hyprland-GeometricMovableAnimated.cpp` has **24 lines**; **a line number past EOF passes** as long as the locator's own line carries no qualifying fragment |
| A10 | `` `m_realSize->goal()` `` at `Hyprland-GeometricMovableAnimated.cpp:0,9999,19` | `OK` | two bogus range members ride along; `:0` is not even refused |
| A11 | `` `m_realSize->goal()` `` at `Hyprland-GeometricMovableAnimated.cpp:19-1` | `OK` | a reversed range is silently widened to `1-19` |
| A12 | `` `fixtures=37/37 tool=present` `` at `receipts/c1-after-data.txt:1` | `SKIP`, no `LOC` line, rc 0 | every `receipts/…:N` locator in the lane's prose is invisible to the gate |
| A13 | `… at `.ufo/waves/round-43/receipts/live-geometry-host.txt:1`` | **no line at all** | `LOCATOR_RE`'s lookbehind `(?<![A-Za-z0-9_./-])` cannot start a match at a leading dot, so the lane's own `.ufo/…:N` citation form (32 occurrences in this prose set) is not a locator |
| S1/S3 | `size` at `rec.cpp:3` (a `//` comment line); `size` after a dropped 1-char fragment | `OK` | comment text supports a code fact; dropping short fragments moves the locator onto a different fragment |
| S4/S5/S9 | multi-line quote + wrong line (900 of 6) | `NOFRAG` | the task's "multi-line quote" class: the fragment and its locator on different physical lines are never compared |

Confirmed on the landed bytes (mutants are copies of the entry in `mut/`, tracked file untouched):

| mutant | change | checker |
|---|---|---|
| `M1-numbers.md` | `size 420 500`→`size 640 720`, `set_default_size(420, 500)`→`(640, 720)` | `locators=10 miss=0`, **rc 0** |
| `M7-arg-swap.md` | `FullMatch(other, *m_regex)`→`FullMatch(*m_regex, other)` (argument order is semantic in RE2) | `locators=10 miss=0`, **rc 0** |
| `M6-wide-range.md` | `WindowRuleApplicator.cpp:426`→`:400-500` | `miss=0` (criterion-legal, but no tightness is required) |
| `M5-no-fragment.md` | the backticks stripped from the `:42` quote | `miss=0` |
| `M4-wrapped-locator-9999.md` | entry line 66's quote kept, its locator moved to a new line as `:9999` | `MISS`, but only because a *later* fragment (`org.omarchy.gkeep`) sits on that line — **the boundary of the escape**: a wrapped locator passes when its line carries no qualifying fragment at all (A3/A4, `SKILL.md:257`) |
| `M2`/`M3`/`M8` (negative controls) | `:70-71`→`:70`, `:428-429`→`:429`, GOAL→CURRENT accessor | `MISS` — the checker catches these |

## 3. FALSE MISS — a correct locator the checker refuses

| # | input | verdict | why it is wrong |
|---|---|---|---|
| A7 | `` w->size(Desktop::View::IGeometric::GEOMETRIC_GOAL) `` at `Hyprland-GeometricMovableAnimated.cpp:19` | `MISS` | `:19` is `case IGeometric::GEOMETRIC_GOAL: return m_realSize->goal();` — the fact is right; the tokens `Desktop`/`View` are not in the source. **The asymmetry is backwards**: precise qualification is punished, abbreviation is not (A8, next row) |
| A8 (measured negative) | `` w->size(GEOMETRIC_GOAL) `` at `Hyprland-HyprCtl.cpp:427-428` | `OK` | the task's hypothesised abbreviation-MISS does **not** exist: `GEOMETRIC_GOAL` matches after `::`. The abbreviation direction is a false **OK** risk, not a false MISS |
| lesson:216 ×2 (landed) | "this seat re-derived all three from `host-gkeep.conf:2-4`, `host-clients-r43.json` and `gkeep-ui-excerpt.py:6,33`" | `MISS`, `MISS` | `host-clients-r43.json` is a **bare file name**, not a locator, so it becomes a "fragment"; both locators are attributed to it and scored against tokens `host,clients,r43,json`. The sentence is a correct pointer list (census verified: `host-gkeep.conf:2-4` = float/center/size, `gkeep-ui-excerpt.py:6,33` = application_id/default_size) |
| lesson:118 | `Hyprland-RegexMatchEngine.cpp:10-16` | `MISS`, `ATTR 'round-42-verifier-spotcheck.md:84'` | the attributed fragment is a **skipped locator span** (name not in `--fetch`), not a quote: `_candidates` drops a locator-shaped span only when its name resolves. Right verdict, wrong reason — and the mechanism turns `NOFRAG` lines into `MISS` |
| lesson:124 | `Hyprland-HyprCtl.cpp:394-395,412-413` | `MISS`, `ATTR 'receipt.txt:60'` | same mechanism on a **quoted checker output** |

## 4. Every MISS, triaged

**Mandated set (16 locators, 1 MISS).**

- `LOG.md:2483 Hyprland-HyprCtl.cpp:394-395,412-413 … verdict=MISS` — **real error**, and not round-43 data: the line is
  byte-identical at the base (`git show a35cfdf:LOG.md | sed -n 2483p | sha256sum` = `418a2949…` = the same line at 1959770).
  It is the round-42 text the lane keeps append-only. Consequence: **criterion 77's named command exits 1 over `LOG.md` at the
  data commit**, so the criterion cannot be satisfied by the whole-file check it names; the close-out must scope the run to the
  round-43 appended lines (the correction at `LOG.md:2487` at HEAD, absent at 1959770).

**Auxiliary `corpus/lessons/round-43.md` (22 locators, 5 MISS, 15 NOFRAG).**

| line | verdict | triage |
|---|---|---|
| 115 | `MISS` | real, by design: it quotes the round-42 wrong locator to identify it (quotation ≠ assertion — a declared w1 limit, re-shown here) |
| 118 | `MISS` (attr = skipped locator span) | the quoted locator is the round-42 defect, so the verdict is right **by coincidence**; the fragment that decided it is not the fact's quote |
| 124 | `MISS` (attr = `receipt.txt:60`) | quotation of a checker output — by design |
| 216 (two locators) | `MISS`, `MISS` | **checker limit → false MISS on correct prose** (§3). `w2/ExecHarmTip.md` F4 groups all five lesson misses as quotations or a previous-line fragment and calls the gate "red on the lesson by its own declared limit"; the mechanism here is narrower and *not* declared: the bare backticked file name `host-clients-r43.json` becomes a "fragment", so both locators of a correct pointer list are scored against tokens `host,clients,r43,json`. A correct author is refused, and criterion 77 counts a `MISS` as a violation |

**Cross-reads.** `w2/ExecHarmTip.md` F4 (same five locators, read as "no harm") and the in-flight `w2/MutCheckLocators.md`
(selftest mutants) attack adjacent ground; my three selftest mutants (`N4`, `N10`, `N11`) are not a substitute for that
matrix, and the false-OK/false-MISS classes in §2-§3 are disjoint from it. Quotation-vs-assertion is a declared w1 limit
(`w1/ExecLocatorGate.md` §Limits) and I do not re-report it as a defect; the two lesson quotations are triaged as real.

The lesson's ten "computed locators" (lines 55-57) and two id rows (153, 175) are all `NOFRAG`: **10 of the round's own
"locators the entry carries" list is never checked**, which is where criterion 77's prose says `NOFRAG` is "not a pass" while
the command exits as if it were.

## 5. The selftest cannot see any of these classes (F11)

Mutants of the checker in the seat dir (`mut/n/N4-after-first.py`, `mut/n/N10-no-comments.py`, `mut/n/N11-short-tokens.py`; 2
lines each; each `SELFTEST: FAIL`, rc 1 — `mut/n/*.out`) show the table *does* kill an
attribution inversion, a short-token filter removal, and comment-stripping. But:

- `cases=18 cases_with_numeric_fragment=0` (measured by loading `CASES`): **no case has a digit inside a fragment**, so a
  checker with no digit rule is at its own maximum.
- No case has a locator alone on a line (the wrapped form), a locator with no fragment *and* an out-of-file line, a qualified
  name, a reversed multi-range, or a bare-file-name sibling. A1/A2/A3/A4/A9/A10/A11/A12/A13 are all outside the table.
- `N10-no-comments` (skip `//` lines of the receipt) **fails** the selftest at case 7 (`gamma` at `rec.cpp:4-3`, a comment
  line, is expected `OK`): the table **encodes comment support as correct**, so the obvious tightening (compare code, not
  comments) cannot pass the shipped selftest.

## 6. Coverage: the gate scores 2.05% of the locator-shaped tokens

`coverage-census.txt`, `coverage-skipped.txt` (62 files, 16 679 lines):

- `locator_tokens_all=779 resolved=16 skipped=763` → **16/779 = 2.1%**; 165 distinct skipped basenames.
- 32 `.ufo/…:<line>` citations in this prose set that `LOCATOR_RE` **cannot match at all** (leading-dot lookbehind).
- 919 bare `:N` / `:N-M` continuations (`SKILL.md:255` uses `:2007`, `:427-428`, `:448`, `:7-8`) — never scored, so the second
  half of a two-part locator is free.
- 111 lane-document locators (`LOG.md:…`, `SKILL.md:…`, `PROVINCE.md:…`, `registration.md:…`) — none resolvable, all `SKIP`.
- 474 of the 763 skipped tokens name a basename that exists somewhere in the rev tree: they are checkable in principle with
  `git show <rev>:<path>` and are not checked.
- 413 lines have an odd backtick count (multi-line quotes): every one of them is a `NOFRAG`-shaped blind spot when its locator
  is on one of the two lines.

## 7. Criterion 77's own bytes fail its own instrument

- `corpus/QUALITY.md:401` says "the appended correction `LOG.md:2487`". At the revision that lands the criterion, `LOG.md` has
  **2483 lines** (`git show 1959770:LOG.md | wc -l`) — **the criterion's worked example carries a locator past EOF at its own
  revision** (it resolves only later, at HEAD, where the correction is line 2487). Class M43-1, in the instrument that defines
  the class, uncatchable by the instrument (`q77-run.txt`: `SKIP … LOG.md:2487 reason=unresolved-name`).
- The same paragraph, run through its own checker, prints `locators=2 miss=2`, rc 1 (`q77-run.txt`): its two "shown able to
  fail" example locators are scored as assertions. A criterion whose quotation of a defect cannot pass its own command will
  fail any close-out that runs it over the file holding the quotation.
- Criterion 77 says "a locator with no backticked fragment is `NOFRAG`, not a pass"; the command exits 0 with any number of
  `NOFRAG` (the data commit lands one at `SKILL.md:257`, and the lesson lands 15). Text and check disagree.

## 8. Impacted axes

- **Coverage (evidence quality), the lane's own axis.** The criterion is the round's evidence gate; at 2.1% token coverage and
  with M1/M7 passing, a "criterion 77 met" line would be **premature saturation** of that axis. The gate cannot support the
  claim "every source locator in prose is checked"; it supports "16 locators naming a file in one fetch dir were checked, and
  14 of them hold their quote".
- **Operability: unaffected.** The checker is not a tool of the C1 claim and touches no C1/C2 path; C1/C2 receipts are
  independent (verified: I wrote no counted file).

## 9. Smallest safe corrections, each measured (`patchedcheck.py`, prototype only)

`patchedcheck.py` implements four tightenings and was run over every fixture; **it changes no landed verdict**:

- **C1 order** — the fragment's identifiers must occur in the cited text *in the fragment's order* (not as a set). Kills
  M7/A9/S6; keeps the abbreviation case A8 and lesson:98 `OK` (verbatim-only was tried first and false-MISSed lesson:98).
- **C2 range** — refuse a range member outside `1..len`, `:0`, and a reversed range instead of widening it. Kills A10/A11/S7.
- **C3 siblings** — drop *every* `LOCATOR_RE`-shaped backticked span from the candidate set, resolved or not, and treat a bare
  fetch-file name as a pointer. Removes the three false MISSes (lesson:216 ×2, lesson:118 → `NOFRAG`).
- **C4 digits** — every digit run of the fragment must occur in the cited text. Kills M1/A5/A6/S8.

Measured: mandated 62 files → `locators=16 ok=14 miss=1 nofrag=1` (only `LOG:2483` moves, and it stays `MISS`); pristine entry
→ `10 ok`; lesson → `ok=2 miss=2 nofrag=18` (from `ok=2 miss=5 nofrag=15`: the two false MISSes and the stray-attr MISS become
`NOFRAG`); adv-real → A5, A6, A9, A10, A11 now `MISS`; `M1-numbers` → 2 `MISS`; `M7-arg-swap` → `MISS`.

Two further corrections are policy, not code: (i) count `NOFRAG` (and single-identifier fragments, the A1/S1/S3 class) in a
named `weak=` bucket and make the criterion say what it does with them, since `NOFRAG` is where M5, A2, A3, A4, A12, A13 and
the 15 lesson locators live; (ii) have the close-out run the checker over the round-43 appended lines, not all of `LOG.md`,
because the carried round-42 line makes the whole-file exit 1 permanent.

## 10. What I do not claim

- I did not run the checker against a *forged* fetch directory; the receipt bytes are the declared trust root and I left it.
- A7 (qualified prose vs unqualified source) has no cheap fix and I do not pretend C1–C4 close it; the honest repair is a
  sentence in the criterion ("quote the receipt's own bytes"), which the lane already follows at 14/14 scored sites.
- A1/S1/S3 (a generic identifier, or comment text, supporting a fact) is a reading limit, not a code bug: no token test can
  decide what a line *says*. It is reported as `weak`, not as a defect to be closed by more regex.
- Criterion 77's `LOG.md:2487` pointer is true at HEAD; I report that it is false at the data commit, not that the tip is wrong.

## Files (seat dir `.ufo/waves/round-43/w2/CritLocatorGate/`)

Runs: `selftest.txt`, `run-r43-fetch.txt`, `run-r42-fetch.txt`, `run-r43-explain.txt`, `strict-r43.txt`, `pristine-runs.txt`,
`lesson43-run.txt`, `adv-real.out`, `adv-synth.out`, `patched-mandated.txt`, `patched-lesson.txt`, `patched-runs.txt`,
`q77-run.txt`, `mut-runs.txt`, `coverage-census.txt`, `coverage-skipped.txt`, `multiline-census.txt`.
Inputs: `adv-real.md` (`d7540528…`), `adv-synth.md` (`9cdf989f…`), `fx/fetch/rec.cpp` (`f8dfc509…`), `mut/M1-numbers.md`
(`fc3d8d8a…`), `mut/M2…` (`25f46adf…`), `mut/M3…` (`432d7976…`), `mut/M4…` (`018a4155…`), `mut/M5…` (`0712bf2c…`),
`mut/M6…` (`df0f7919…`), `mut/M7…` (`c4e03281…`), `mut/M8…` (`31d5f37b…`); checker mutants `mut/n/N4-after-first.py`
(`ed0bab2d…`), `mut/n/N10-no-comments.py` (`8984b71c…`), `mut/n/N11-short-tokens.py` (`f7f58843…`) with their `.out` runs.
Instruments (mine, read-only prototypes): `strictcheck.py` (verbatim quote + digit audit), `patchedcheck.py` (C1-C4).

Tools installed: none. Scratch `/fast/scratch/hyaku/mado-r43/CritLocatorGate/` deleted after the receipts were copied here.
