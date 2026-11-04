# mado round 81 — the overflow rounding, the auto-zone gate, and two matcher classes (2026-11-04, hyaku run 15)

Claims: **C1 coverage** — the composition's overflow rounding and its auto-zone gate: thirty-nine
frozen cases 39/39 (the thirty-three round-80 cases carried parsed-equal, plus six on the four
classes round 80 recorded as `NOT_MODELLED`), twenty-eight named mutations killed 28/28, the held
round-80 tool `base_correct=33/39`, tool selftest 121/121; **C2 operability** — the read-only
runbook gains an action-column matcher (`cut -c36-`: fixed separator, non-empty trimmed action, no
second arrow) and a `pgrep -x waybar` PID-list/exit-status matcher (26 cases / 26 rows / 26 distinct
anchors, `control_new=0/2`, twenty-three matcher mutants killed). Freeze
`0e2ccd2a8692825cac534f57246053b276be9f13`; base `c702094ace5dd9b2b5e152951b4b2f4dd578f8b6`;
declaration `.ufo/waves/round-81/claims-declaration-r81.md`.

Measured lines (verbatim, `receipts/measurement-c1-r81.txt:70` and
`receipts/measurement-c2-r81.txt:52`):

```
MADO_R81_BARFOOT: cases=39 correct=39 mutants=28 killed=28 base_correct=33/39 carried=33/33 tool_selftest=121/121 verdict=TARGET_MET rev=0e2ccd2a… tool_sha256=a129a435…
MADO_R81_RUNBOOK: cases=26 executed=26 matched=26 shapes=21/21 anchors=26/26 rows=26/26 control_new=0/2 mutants=23 killed=23 verdict=TARGET_MET rev=0e2ccd2a… tree=bound
```

Mistakes below were mined by seat `R81ScribeLesson` against the committed bytes at the freeze and at
the landing tip `f3eb70c7` (2026-11-04). Each cell names the command that confirms it; a red state
that no committed artifact preserves is marked *reconstructed*, never reported as observed.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M81-1 | rule-from-code: the first C2 action-column grammar bound the payload's XML-entity escaping as a property of the printed output | `.ufo/waves/round-80/fetch/S473.txt:156-160` is the escaping block (`gsub(/&/, "\\&amp;", action);` …), but the live output escapes only some ampersands: `omarchy menu keybindings --print \| cut -c36- \| grep -c '&'` → `2`, and `… \| grep -n '&'` → `17: → Pop window out (float & pin)` and `147: → omarchy-hw-external-monitors &amp;&amp; omarchy-hyprland-monitor-internal off` (193 lines total) | nothing did: the case was authored from the `gsub` block, which runs per action, instead of from the bytes it prints; the pre-fix case is *reconstructed* — the sandbox commits `9dd96085`/`457a9b9a`/`1dd44e95` hold the lane's older counters but no `quality/counters/c2-r81-runbook.py` (`git ls-tree -r --name-only` → 0 matches) and its worktree is clean | the grammar binds the separator at the fixed column, a non-empty trimmed action and the absence of a second `→`, never entity text (`quality/counters/c2-r81-runbook.py:344-356`), and both spellings are positive samples (`controls/make-c2-cases-r81.py:56-57`). Shown able to fail: `special_matches("action_column", …, 0, " → Pop window out (float & pin)\n → Action 1\n")` → `True`, while an entity-keyed predicate (`'&amp;' if '&' in line`) returns `False` on that same sample |
| M81-2 | normalisation-blind matcher: the first `pid_state` matcher read `stdout.strip()`, so a padded PID line matched the shape it was built to refuse | the frozen case carries the pad as a negative, `controls/c2-runbook-cases-r81.json:942` (`{"rc": 0, "out": " 1720\n"}`), and the matcher now reads `text = stdout.rstrip("\n")` (`quality/counters/c2-r81-runbook.py:411`) with `re.fullmatch(r"[0-9]+", line)` per line; `special_matches("pid_state", {}, 0, " 1720\n")` → `False`, while a `.strip()` variant accepts it (`matcher-probe.out`: `STRIP variant on negative ' 1720\n': True`) | nothing did: the negative set was authored after the matcher; the counter reports only `matched`, never which negative leaked. The pre-fix code is *reconstructed* — the same sandbox holds no r81 counter and the later scratch (`/fast/scratch/hyaku/mado-r81/l1/`) holds only the seven C1 fixture dirs | rstrip newlines only, then split lines and `fullmatch` each; the pad survives to the numeric test and fails it, and `pid-numeric-blind` keeps its kill. Shown able to fail: the `.strip()` variant turns the frozen negative into a match, so `case_correct` returns `False` and the case's row reads `matched=25/26` — a red measurement, not a subtle one |
| M81-3 | number-drift in the frozen instrument's own docstring: `quality/counters/c2-r81-runbook.py` still describes round 79 and prints the r80 contract | `:2` = `"""mado — PRED-C2-r79-v1:…`; `:5` names `### Executable runbook rows (round 79)`; `:15` "The seventeen round-78 cases…"; `:22-24` "the held round-78 rule … over all twenty-two cases"; `:27-30` the round-79 counting command; `:32` `Contract: … cases=24 … shapes=19/19 … mutants=16`. The code pins `CASES = 26`, `CARRIED = 24`, `SHAPES = 21`, `MUTANTS = 23` (`:51-54`), and `receipts/measurement-c2-r81.txt:52` prints `cases=26 … shapes=21/21 … mutants=23`. The frozen blob is byte-identical (`git show 0e2ccd2a:quality/counters/c2-r81-runbook.py \| sha256sum` → `1bc9ca40…`) | nothing did: the instrument was derived from the r80 counter and its narrative/contract were not regenerated; the C1 counter's docstring *was* regenerated (`PRED-C1-r81-v1`, r81 narrative), which is what makes the omission visible. No check compares a docstring to its own constants | constants and the receipt are the primary numbers, and the docstring must be regenerated when they move. Shown able to fail: `grep -n 'cases=24' quality/counters/c2-r81-runbook.py` → `32:Contract: … cases=24 …` while `grep 'MADO_R81_RUNBOOK:' receipts/measurement-c2-r81.txt` → `cases=26` |
| M81-4 | claim-boundary: the r80 entry generalised its rounding counterexample into a biconditional that the bytes do not support | `corpus/knowledge/bar-footprint-composition-r80.md:192-196` says the tool's `(bounds.size - size + 1) // 2` "equals `CBox::round`'s result **only when** the tie's absolute coordinate is non-negative". The formula attribution is right for the tool it described (`git show dd4f844c:tools/mado-barfoot.py \| sed -n '503p'` → `x = bounds["x"] + (bounds["w"] - w + 1) // 2`, vertical twin at `:513p`; `w` is never recomputed on that branch), but the boundary is false: `tie-probe.out` over bounds 1..60 × width 1..70 finds 1,200 disagreements — **every one** at a negative half-integer tie — and 1,170 negative *integer* ties that **agree** (e.g. `bw=1000 w=1002` → tool `(-1, 1002)`, source `(-1, 1002)`, tie `-1.0`) | nothing did: the r80 wave probed one instance (1001/1000) and wrote the boundary from it; the frozen `overflow-tie-negative` case pins only that instance | state the divergence as a negative *half-integer* tie (`size > bounds` with an odd difference, e.g. `bw=1000, w=1001` → tool `(0, 1001)` vs source `(-1, 1002)`), not any negative tie. Shown able to fail: the probe's 1,170 agreeing negative ties contradict the r80 sentence by construction, and `bw=1000 w=1002` is a two-line check |
| M81-5 | attribution-drift, caught inside the round in this round's own Gate text: the landed Gate's reject sample says the r28 entry's source ids collide | `corpus/lessons/round-81.md:47` — "its S224/S228/S231 ids collide". `comm -12` of the lane's 414 ids and the package's 147 staged ids → **94** collisions, but the cited-id table is `S214 lane=1 pkg=1 coll=1`, `S219 lane=1 pkg=1 coll=1`, `S224 lane=0 pkg=1 coll=0`, `S228 lane=0 pkg=1 coll=0`, `S231 lane=0 pkg=1 coll=0`: the child's three ids sit in the lane's free gap S222-S252, and the collisions belong to the **parent** entry's S214/S219 | nothing did: the 94-collision count was right, so the sentence read as verified; nobody re-checked the three ids it names against the collision file | name the parent's `S214`/`S219` as the colliding ids and keep the count 94. Shown able to fail: `grep -c '^S224$' .ufo/waves/round-81/assimilation/collisions` → `0` while `grep -c '^S214$' .ufo/waves/round-81/assimilation/collisions` → `1` |

Sweep for a sixth: `grep -n 'TODO\|FIXME\|XXX' tools/mado-barfoot.py quality/counters/c1-r81-overflow-auto.py quality/counters/c2-r81-runbook.py` → no output (2026-11-04). Second sweep (dead keys in the two new control sets): the C2 new cases carry `argv/kind/name/negatives/samples/skill_anchor/value` and every key is read by `case_correct`/`special_matches`; the C1 new cases carry `name/config/layers/monitors/surfaces/monitor/expect` and every key is read by `case_files`/`expected_ok`. Third sweep (anchor liveness, the M81-3 class): `grep -c 'if zone == -1' tools/mado-barfoot.py` → `0` at the tip while the two re-pointed mutants anchor on the successor; every one of the 28 + 23 mutants is scored, and the eight `reason=anchor-absent` rows in `receipts/control-c1-r81-at-base.txt` belong to the *held* r80 tool at the base, where the new anchors do not exist — that is the control's shape, not a kill.

## Gate (sources opened this round)

Census, read-only, `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mado`:

- **round start** (`c702094a`): `412` rows, exit `0`. `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `412`; the census prints the standing `W04` duplicate-URL warnings and `W01 S277`, then `mado	ok	…/corpus/SOURCES.md`.
- **this seat's re-run** (2026-11-04, at `f3eb70c7`): `414` rows, `census_rc=0`; the last two lines are `mado	ok	/home/vgpnk/Projects/shokunin/mado-shokunin/corpus/SOURCES.md` and `census_rc=0`. The two new rows are `corpus/SOURCES.md:430` and `:431`; no older row's `status`/`recheck`/`used-by` cell moved.

Pins: `cd .ufo/waves/round-81/fetch && sha256sum -c sha256-r81.txt` → `S478.bin: OK`, `S479.bin: OK`, `verify_rc=0`.

| row | source and locator (opened 2026-11-04) | status | located quote (≤25 words) | what it licenses / does not |
|---|---|---|---|---|
| S478 | https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.0/src/math/Box.cpp — `CBox::round` `:51-63`; sha256 `2d04de99…`, 5901 B (`.ufo/waves/round-81/fetch/S478.bin`; row at `corpus/SOURCES.md:430`) | mined (new) | `    double newW     = x + w - roundedX;` (at `:54`) | the origin-then-far-edge coupling (`w = std::round(newW);` at `:59`), which is why a one-pixel overflow lands at `x=-1, w=1002`; it does **not** say which hyprutils version the host installed — `pacman -Q hyprutils` → `hyprutils 0.14.2-1`, and S478 is the `v0.14.0` tag |
| S479 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/CMakeLists.txt — `:150` and `:156`; sha256 `97b8028a…`, 25010 B (`.ufo/waves/round-81/fetch/S479.bin`; row at `corpus/SOURCES.md:431`) | mined (new) | `set(HYPRUTILS_MINIMUM_VERSION 0.14.0)` (at `:150`) | a **floor**, not a runtime read: `:156` is `pkg_check_modules(hyprutils_dep … hyprutils>=${HYPRUTILS_MINIMUM_VERSION})`, so `v0.14.0` is the tag licence for S478, and the host's 0.14.2-1 is a different build |

Assimilation (`/home/vgpnk/Projects/shokuknow/merge/mado/`, read-only; 72 files, 147 staged rows,
69 entries). Two entries sit on this round's bar plane — the same bar whose process state C2 binds
with `pgrep -x waybar` and whose config the C1 join reads — so the sample is drawn from them:

- **admit (content; landing gated)** — `knowledge/corpus/knowledge/host-bar-producers-r28.md`. Its
  three checkable claims were re-measured today and hold: `wc -c ~/.config/waybar/config.jsonc` →
  `6354` (the entry's byte count, `:34`); `sha256sum
  ~/.local/share/omarchy/default/waybar/indicators/idle.sh` → `6d8d2c11d3c3b15f…` with `wc -c` →
  `159`, the S228 row's pinned prefix and size; and `grep -n 'pgrep -x hypridle'` →
  `3:if pgrep -x hypridle >/dev/null; then`, the entry's quote at `:60` — a sibling of C2's
  process-probe class. Its module enumeration reconciles with the host bytes (`modules-left` 2,
  `modules-center` 8, `modules-right` 8 → 18; ten `custom/*` definitions, the tenth
  `custom/expand-icon` nested in `group/tray-expander` at `config.jsonc:189`, defined at `:193`).
  Landing is gated, not cleared: the entry **amends** `host-bar-and-idle-binding-r26.md` and that
  parent is rejected below, and the pair's ids must be renumbered by the document protocol (94 of
  147 staged ids collide).
- **reject** — `knowledge/corpus/knowledge/host-bar-and-idle-binding-r26.md` §1. The sentence at
  `:29-30` says "eight of the eleven visible elements" while its own enumeration at `:19-27` lists
  18 module names (2 + 8 + 8) and the host bytes carry 18. Both the numerator and the denominator
  are wrong — nine custom top-level elements of eighteen, or ten custom definitions counting the
  nested `custom/expand-icon` — and the r28 entry's ten-row table already supersedes the inventory.
  Reject until corrected; its `S214`/`S219` are also two of the 94 colliding ids, so it cannot land
  as-is on either ground.

Correction to the landed Gate's reject sample: `corpus/lessons/round-81.md:47` says the r28 entry's
"`S224/S228/S231` ids collide". None of the three does (`grep -c '^S224$'
.ufo/waves/round-81/assimilation/collisions` → `0`, likewise S228/S231); the collisions it means are
the **parent's** `S214`/`S219` (`→ 1` each), which is M81-5 above. The entry's 6354 B claim is no
longer an open re-measurement either: it was re-read today and holds at `6354`.

Precision notes for the closure: S478's anchor names the whole function `:51-63` and the quoted line
is inside it; S479's quote is the version floor and says nothing about behaviour; the two rows are
already committed at `f3eb70c7`, and their `used-by` cell names
`corpus/knowledge/bar-footprint-rounding-auto-r81.md`, whose `source:` line must then carry both
ids. Neither row duplicates a held URL — the census's W04 list is unchanged for these two.
