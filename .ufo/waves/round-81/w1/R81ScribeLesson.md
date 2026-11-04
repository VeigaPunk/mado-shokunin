# R81ScribeLesson — report (round 81, seat scribe / lesson)

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, read-only. Base `c702094a`, freeze
`0e2ccd2a`; the lane advanced to `f3eb70c7` while this seat worked. Deliverables:
`w1/R81ScribeLesson/lesson-draft.md` (the lesson prose) and
`w1/R81ScribeLesson/findings.md` (every command with its literal output).

## Behavior

Drafted the round-81 lesson in the round-80 shape: a five-column `## Mistakes` table
(id · class · evidence pointer · captured-by · fix shown able to fail) plus a `## Gate` block.
Five rows, each confirmed or corrected against committed bytes:

- **M81-1 (a)** — the first C2 action-column grammar imported the payload's XML escaping. Confirmed:
  the escaping exists (`S473.txt:156-160`), but the printed column carries a **bare** `&` —
  `omarchy menu keybindings --print | cut -c36- | grep -c '&'` → `2`, with
  `17: → Pop window out (float & pin)` and `147: … &amp;&amp; …`. The frozen case now pins both
  spellings as positives (`controls/make-c2-cases-r81.py:56-57`); the matcher never binds entity
  text (`c2-r81-runbook.py:344-356`).
- **M81-2 (b)** — `pgrep -x waybar` was `.strip()`ed. Confirmed in its fix: the matcher now
  `rstrip("\n")`s (`c2-r81-runbook.py:411`), the frozen negative is `" 1720\n"`
  (`c2-runbook-cases-r81.json:942`), and a `.strip()` variant accepts exactly that negative.
- **M81-3 (new)** — the frozen C2 counter's docstring still says `PRED-C2-r79-v1` and the r80
  contract (`cases=24 … shapes=19/19 … mutants=16`, `:32`) while `:51-54` pin `26/21/23` and the
  receipt prints `cases=26 …`. The frozen blob `1bc9ca40…` carries the stale text.
- **M81-4 (c)** — the r80 §11 sentence is right about the formula (`(bounds.w - w + 1)//2`, `w`
  never recomputed, `dd4f844c:503/513`) and wrong about its boundary: a probe over bounds 1..60 ×
  width 1..70 finds 1,200 disagreements, all at negative **half-integer** ties, and 1,170 negative
  *integer* ties that **agree** (`bw=1000 w=1002` → both `(-1, 1002)`), so "only when the tie's
  absolute coordinate is non-negative" is falsified. The brief's 1000/1001 case reproduces
  (`(0,1001)` vs `(-1,1002)`).
- **M81-5 (caught in the landed lesson)** — `corpus/lessons/round-81.md:47` says the r28 entry's
  `S224/S228/S231` ids collide. `comm -12` of the lane's 414 ids and the package's 147 staged ids is
  94, but all three cited ids are **free** (`coll=0`); the collisions are the **parent** entry's
  `S214`/`S219` (`coll=1` each).

## Gates

- Census, round start: **412 rows / exit 0** (`grep -cE` → 412; declaration + `receipts/census-start-r81.txt`).
- Census, re-run by this seat at `f3eb70c7`: **414 rows / exit 0**, last lines
  `mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` and `census_rc=0`;
  S478/S479 are committed at `corpus/SOURCES.md:430-431`.
- Pins: `sha256sum -c .ufo/waves/round-81/fetch/sha256-r81.txt` → `S478.bin: OK`, `S479.bin: OK`.
- Gate rows: S478 `w = std::round(newW);` at `:59` (row's own quote: `double newW     = x + w - roundedX;` at `:54`); S479
  `set(HYPRUTILS_MINIMUM_VERSION 0.14.0)` at `:150`, and `:156` shows `hyprutils>=…` — a floor, not
  a runtime read (`pacman -Q hyprutils` → `hyprutils 0.14.2-1`).
- Assimilation (`/home/vgpnk/Projects/shokuknow/merge/mado/`, read-only):
  **admit on content** `host-bar-producers-r28.md` (6354 B host config re-measured today; idle.sh
  `159 B` + sha prefix `6d8d2c11d3c3b15f` = S228; `pgrep -x hypridle` at `:3`), landing gated by its
  dangling parent + the 94-id renumber; **reject** `host-bar-and-idle-binding-r26.md` §1
  ("eight of the eleven visible elements" vs its own 18-name enumeration and the host's 2+8+8).

## Touched surfaces

Wrote only inside `.ufo/waves/round-81/w1/R81ScribeLesson/`: `lesson-draft.md`, `findings.md`, and
receipts `amp-grep.txt`, `census.txt`, `counter-docstring.txt`, `source-pins.txt`, `tree-drift.txt`,
`assimilation.txt`, `host-check.txt`, `r80-boundary.txt`, `matcher-probe.py/.out`,
`tie-probe.py/.out`. Scratch `/fast/scratch/hyaku/mado-r81/R81ScribeLesson` removed after copying.
No instrument, control, declaration, SKILL.md, LOG.md or fleet-root file touched.

## Findings (routed)

- **F1 MEDIUM** — the landed lesson's Gate names the wrong colliding ids (M81-5); the draft carries
  the corrected sentence and the same 94 count.
- **F2 MEDIUM (live)** — the frozen C2 counter tree-binds `SKILL.md`/`tools/mado-barfoot.py`
  (`c2-r81-runbook.py:651-655`); at `f3eb70c7` the tree's SKILL.md is `25b87bf0…` but
  `0e2ccd2a:SKILL.md` is `08213132…`, so re-running the frozen command at the freeze rev now exits 2.
  Re-measure at a rev whose bytes are in the tree.
- **F3 LOW** — the C2 `--selftest` 88/88 has no unit check for `action_column`/`pid_state`; the
  frozen samples/negatives and seven mutants are their only exercise.
- **F4 INFO** — `receipts/measurement-c1-r81-at-tip.txt` was 0 bytes and untracked at my read.
- **F5 LOW** — the landed M81-2's "the sandbox run scored the negative as matching" has no artifact
  under the sandbox or `/fast/scratch/hyaku/mado-r81/l1`; cite a log or mark it reconstructed.
- **F6 INFO** — instrument docstrings disagree by generation (C1 `PRED-C1-r81-v1` vs C2 `PRED-C2-r79-v1`).

## Out of scope

No counting-command re-run (C2 blocked by F2; C1 is the executor's committed receipt), no edits to
frozen instruments/controls/declaration/SKILL.md/LOG.md, no mutations, no installs.

## Artifacts

- `.ufo/waves/round-81/w1/R81ScribeLesson/lesson-draft.md`
- `.ufo/waves/round-81/w1/R81ScribeLesson/findings.md` (STATUS: ok)
- `.ufo/waves/round-81/w1/R81ScribeLesson/` receipts listed above.
