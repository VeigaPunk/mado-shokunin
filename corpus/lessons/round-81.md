# mado round 81 — the overflow rounding, the auto-zone gate, and two matcher classes (2026-11-04, hyaku run 15)

Claims: **C1 coverage** — the composition's overflow rounding and its auto-zone gate: thirty-nine
frozen cases 39/39 (the thirty-three round-80 cases carried parsed-equal) on the four reachable
classes round 80 recorded as `NOT_MODELLED`, twenty-eight named mutations killed 28/28, the held
round-80 tool `base_correct=33/39`, tool selftest 121/121; **C2 operability** — the read-only runbook
gains an action-column matcher (`cut -c36-`: fixed separator, non-empty trimmed action, no second
arrow) and a `pgrep -x waybar` PID-list/exit-status matcher (26 cases / 26 rows / 26 distinct
anchors, `control_new=0/2`, twenty-three matcher mutants killed). Freeze
`0e2ccd2a8692825cac534f57246053b276be9f13`; base `c702094ace5dd9b2b5e152951b4b2f4dd578f8b6`.
Declaration: `.ufo/waves/round-81/claims-declaration-r81.md`.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M81-1 | rule-from-code: the first C2 action-column grammar bound the payload's XML-entity escaping (`&` → `&amp;`, `'` → `&apos;`) as a property of the output, and the live output contradicts it | `{LANE}/.ufo/waves/round-80/fetch/S473.txt` escapes at `:156-160` but **only inside** the `if (action == "")` reconstruction branch (`:143`), while the description path takes `action = $3` (`:141`) unescaped; `omarchy menu keybindings --print \| cut -c36- \| grep -c '&'` → `2` and one of the two lines is `→ Pop window out (float & pin)` — a **bare** ampersand; `grep -c '<'` on the same column → `0` (branch reading: wave seat `R81ExecC2Run` §4) | nothing did: the case was authored from the payload's escaping code instead of from its printed output | the grammar now binds the separator's fixed column, a non-empty trimmed action and the absence of a second `→`, never the entity text; the falsification is committed as a **positive sample** in `.ufo/waves/round-81/controls/c2-runbook-cases-r81.json` (`keybindings-actions` `.samples[1]`), so a revert to the entity rule fails the case. Shown able to fail: the earlier sandbox run printed `name=keybindings-actions ... match=no` before the narrowing (`/fast/scratch/hyaku/mado-r81/sandbox` commit `457a9b9a`, scratch) |
| M81-2 | normalisation-blind matcher: the first `pid_state` matcher read `stdout.strip()`, so a padded PID line (`" 1720\n"`) matched the shape it was meant to refuse | `.ufo/waves/round-81/controls/c2-runbook-cases-r81.json` `waybar-pgrep.negatives[3]` is `{"rc": 0, "out": " 1720\n"}`; the pre-fix code was `text = stdout.strip()` and the sandbox run scored the negative as matching | nothing did: the negative set was authored after the matcher, and the counter only reports `matched`, not *which* negative leaked | the matcher now rstrips newlines only (`text = stdout.rstrip("\n")`) and splits lines, so the leading space survives to the `re.fullmatch`; shown able to fail: the mutant `pid-zero-accepted` (`0 < int(line)` dropped) and `pid-numeric-blind` are each killed by this negative set, and a copy of the counter with the pre-fix `.strip()` restored prints `name=waybar-pgrep row=25 kind=pid_state match=no` and `matched=25 verdict=TARGET_MISSED` (receipt `receipts/control-c2-strip-regression-r81.txt`) |
| M81-3 | anchor drift: moving the zone computation after the box renamed the bounds-selection line (`if zone == -1:` → `if spec["exclusive"] == -1:`), and two carried C1 mutants anchored on the old text would have died `reason=anchor-absent` — silently lowering `killed` from 28 to 26 without any rule being exercised | `grep -c 'if zone == -1' {LANE}/tools/mado-barfoot.py` → `0` at the freeze; the counter's anchor-absent branch prints `MADO_R81_MUTANT: name=… correct=0/39 killed=no reason=anchor-absent` (`quality/counters/c1-r81-overflow-auto.py`, the `except Setup` arm) — reproducible by restoring either old anchor | the counter's anchor-absent branch is honest but no gate required every mutant anchor to still exist before the freeze | both carried mutants (`running-bounds-ignored`, `full-box-uses-usable`) were re-pointed at the renamed line with their semantics unchanged, and the declaration names the re-point; shown able to fail: every anchor is checked to occur exactly once before the freeze (`src.count(anchor) == 1` over all 28), and the pre-re-point run scored `killed=20/28` in `receipts/control-c1-r81-at-base.txt` |
| M81-4 | planned-ground drift: the round-80 `Planned` row named "`preview_scale`/fractional scaling" as this round's C1 ground, but no such symbol exists in any pinned compositor file, and the actual finite ground was the r80 entry's §11 item list | `grep -rc 'preview_scale' .ufo/waves/round-80/fetch/S470.bin .ufo/waves/round-79/fetch/S464.bin .ufo/waves/round-77/fetch/S46*.bin` → `0` in every file; the r80 lesson already said the only scale inputs are `monitor.scale`/`transform`, which the join refuses | nothing did: a `Planned` row is intent only and no gate reads it against the sources | the round declares the §11 classes instead and the report's `Landed changes` names the substitution; the fractional-scale ground stays a documented refusal (`ERROR (stage=model monitor … has scale/transform …)`), not a claim |
| M81-5 | misroot: wave seat `R81ScribeSources` created four self-referential symlinks inside the lane (`corpus/lessons/lessons`, `corpus/knowledge/knowledge`, `tools/tools`, `.ufo/.ufo`) while probing path resolution | `.ufo/waves/round-81/w1/R81ScribeSources.md` §9 lists the four paths and the `rm` that removed them; `ls -la corpus/lessons/lessons` → `No such file or directory` (re-checked 2026-11-04 after the seat settled) | the seat caught them with its own `ls`/`gone:` sweep; no gate reads the lane tree for symlink loops between commits | the seat removed all four and the lane `git status --porcelain` shows none of them; shown able to fail: the four `ls` calls exit 2 today, and the sweep is recorded in the wave findings so a later census does not read them as sources |

Sweep for a fifth: `grep -n 'TODO\|FIXME\|XXX' tools/mado-barfoot.py quality/counters/c1-r81-overflow-auto.py quality/counters/c2-r81-runbook.py` → no output (2026-11-04, at the freeze).
Second sweep (dead keys in the two new control sets): the C1 case keys are read by `case_files`/`expected_ok` and the six new cases carry only `name/config/layers/monitors/surfaces/monitor/expect`; the C2 new cases carry `argv/kind/name/negatives/samples/skill_anchor/value`; `python3 -c "…set(case)-KNOWN"` prints nothing for both new cases. Third sweep (unused mutants): every one of the 28 + 23 mutants is scored by the counter it lives in; no mutant is carried without an anchor check.

## Gate (sources opened this round)

Census at round start `c702094a` → 412 registry rows,
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin mado` exit 0 (standing W04 duplicate-URL warnings, W01 S277); at the
landing tip → 415 rows, exit 0 (`receipts/census-start-r81.txt` for the start; the end run is quoted
in the round report). Three rows added, all `mined`, all tier A, all pinned under `fetch/` and
verifying 3/3 with `sha256sum -c fetch/sha256-r81.txt`; no older row's `status`/`recheck`/`used-by`
cell moved.

| row | source and locator (opened 2026-11-04) | status | located quote (≤25 words) | what it licenses / does not |
|---|---|---|---|---|
| S478 | https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.0/src/math/Box.cpp — `CBox::round` `:51-63`; sha256 `2d04de99…`, 5901 B (`.ufo/waves/round-81/fetch/S478.bin`) | mined (new) | `    double newW     = x + w - roundedX;` (at `:54`) | the coupled origin-then-far-edge rounding that puts a one-pixel overflow at `x=-1, w=1002`; it does not say which version the host's package actually installed |
| S479 | https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/CMakeLists.txt — `:150`; sha256 `97b8028a…`, 25010 B (`.ufo/waves/round-81/fetch/S479.bin`) | mined (new) | `set(HYPRUTILS_MINIMUM_VERSION 0.14.0)` (at `:150`) | the pin that licenses reading S478 at tag `v0.14.0`; a minimum version is not an installed-version read |
| S480 | https://raw.githubusercontent.com/hyprwm/hyprutils/v0.14.2/src/math/Box.cpp — `CBox::round` `:51-63`; sha256 `2d04de99…`, 5901 B (byte-identical to S478) (`.ufo/waves/round-81/fetch/S480.bin`) | mined (new) | `    double newH     = y + h - roundedY;` (at `:55`) | the installed version's bytes are the model's bytes (`pacman -Q hyprutils` → `0.14.2-1`, `cmp` empty); it does not make S479's minimum-version pin an installed-version read |

Assimilation: **none** this round. The staged package `/home/vgpnk/Projects/shokuknow/merge/mado/`
was built against a 192-row registry and its id space now collides: `comm -12` of the lane's 414 ids
and the package's 147 staged ids → **94 collisions** (`.ufo/waves/round-81/assimilation/collisions`),
so nothing appends without the renumber-by-document protocol, and no staged entry touches this
round's claim ground (§11's overflow/auto-zone classes, the action column, the pgrep row). Reject
sample (read, not adopted): `knowledge/corpus/knowledge/host-bar-producers-r28.md` — it **amends**
`host-bar-and-idle-binding-r26.md` from the same package, so adopting it alone dangles the parent;
its source ids S224/S228/S231 are **free** in the lane registry (`reg=0 staged=1` each, so this refusal is not an id closure), and its 6354 B host-config claim is a 2026-10-23 read the r80
connector already flagged for re-measurement. Flip: adopt both entries together once the host config
is re-read and the ids are renumbered by document. No admit is claimed because nothing was adopted.

Precision notes for the closure: S478's anchor names the whole function and the quote is inside it;
S479's quote is the version pin, not a behaviour. Neither row duplicates a held URL (the census's
W04 list is unchanged for these two).

## Wave-routed defects (append-only)

- **F1 (medium), fixed.** The Gate's reject sample first said the staged entry's ids collide; they are
  free (`S224/S228/S231` → `reg=0 staged=1` each). The sentence is corrected above; the 94-collision
  count is unchanged and correct.
- **F2 (medium), answered by measurement.** The frozen C2 counter tree-binds `SKILL.md` and
  `tools/mado-barfoot.py` to `--rev`, so re-running the *declared* command at the freeze `0e2ccd2a`
  after the SKILL registry rows landed exits 2. The claim is therefore measured at the content tip
  `f3eb70c7` in `receipts/measurement-c2-r81-at-tip.txt` (`tree=bound`, `TARGET_MET`), and the freeze
  receipt stays as the freeze-time record. Any later SKILL.md edit needs a fresh measured rev; none is
  planned this round.
- **F3 (low), deferred.** The C2 counter's `--selftest` has no unit check for `action_column`/`pid_state`
  (they are exercised only by the frozen samples/negatives and the seven mutants). Editing the frozen
  instrument after the freeze would break its cited sha256, so the unit checks are a round-82 repair.
- **F6 (info), deferred.** The C2 counter's docstring still says `PRED-C2-r79-v1`. Same reason: the
  frozen bytes are cited by sha256; the label is corrected with F3 next round.
- **F4/F5 (info/low), resolved.** The at-tip receipt was mid-write when the seat read it and is now
  committed (`6006feb5`); M81-2's demonstration now cites the committed strip-regression receipt.
