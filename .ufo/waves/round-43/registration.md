# mado round 43 — registration (frozen before any round-43 data)

Lane `mado-shokunin`, base `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f` (the round-42 tip; `jj-lane.sh state` at round start:
`local=remote=a35cfdf… ahead=0 tracked=0 untracked=0`). Host 2026-10-26, Hyprland 0.56.2 (`efb50993780079460b0cbed1363e2166a2de1d9f`).
Shape: **two v1 waves** — `w1` (build + first falsifiers, 37 seats) and `w2` (falsify, dispatched after the data commit, 32 seats); planned
round total 69, no residual call planned. The §3 planner seat is held by the L1 (`MadoR43`); a planning data-walk rides `ScoutStagedGkeep`.
No earlier attempt of round 43 exists (`.ufo/watchdog.log` has no `lane-dead-no-report mado round=43` line).

**Why these claims.** Round 42 froze two claims with controls and stopped before its wave ran (closure `corpus/lessons/round-42-verifier-spotcheck.md`:
`rejected-honest-stop`, no axis harmed). Its instruments were never scored by any seat, so round 43 re-registers them instead of inventing new
ones: C1 **unchanged**, C2 with **round constants only**. Neither predicate has met data.

**Lowest-axis rule.** Every published axis ties at its maximum at base (`receipts/axis-base.txt`: navigation 59/59, calibration 63/63,
operability 12/12, `MADO_AXIS checked=3 mismatched=0 rev=a35cfdf…`), so each is a lowest axis. Lane axes: **operability** and **coverage**.

## Claims

- **C1 — operability (capability acquisition): `tools/mado-geometry.py`** — the round-42 claim, unchanged: a read-only join of the window-rule
  sizes in Hyprland config files and the sizes the compositor reports in one `hyprctl clients -j` dump (`hyprctl clients -j | mado-geometry.py
  --clients - --rules ~/.config/hypr/gkeep.conf`), per client matched by a `windowrule = size W H, match:class RX` line AGREE, DIFFER, TILED or
  BADSIZE, with `--selftest`. Before: no tool of the lane reads a window's reported size (`git ls-tree a35cfdf tools/` has no geometry tool).
  - **Predicate `PRED-C1-r42`** (unchanged, frozen at `809dc2caef09d9cbf15a496e55a1b208803a3561`): the docstring of
    `quality/counters/c1-r42-geometry.py` — 37 fixtures scored byte-exactly against the judge's model inside a bubblewrap sandbox under
    `RLIMIT_NPROC = 1`, plus clauses a, b, b2, b3, g. Its contract reference stays `.ufo/waves/round-42/c1/ctl-ref-tool.py.txt`.
  - **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c1-r42-geometry.py --repo . --rev <rev>`
    (fresh nonce per run, replayable with `--nonce`; clause a reads BASE `62dd798`, where the tool is also absent).
  - **Before** (round-43 base): `fixtures=0/37 tool=absent verdict=TARGET_MISSED`, exit 1 (`receipts/c1-before-base.txt`).
  - **Target:** `fixtures=37/37 tool=present verdict=TARGET_MET`, exit 0, at the data commit and at the tip. **Kill rule:** anything else at the
    data tip is a miss, reported as an honest stop; no narrowing.
- **C2 — coverage (sourced; assimilation of the gkeep-geometry theme of `merge/mado/`): `corpus/knowledge/hyprland-gkeep-geometry-r43.md`** — what
  determines the size of the host's gkeep window, end to end (host rule text, `RE2::FullMatch`, the `size`/`float` effects, the floating algorithm,
  the target and window that store the box, the animated variable behind `hyprctl clients -j` `size`, the client's own `set_default_size(420, 500)`,
  and today's host census). Base holds no rendered-geometry knowledge (`git grep -ciE 'set_default_size|GEOMETRIC_GOAL|RE2::FullMatch|rendered
  geometry' a35cfdf -- corpus/knowledge PROVINCE.md SKILL.md tools` finds none). The §2b sourced claim; rows S290-S299 are opened this round.
  - **Predicate `PRED-C2-r43`:** the docstring of `quality/counters/c2-r43-gkeep-entry.py` = `PRED-C2-r42` with only the round constants changed
    (BASE `a35cfdf`, entry `…-r43.md`, lesson `corpus/lessons/round-43.md`, fetch dir `.ufo/waves/round-43/fetch/`, opened/verified-at 2026-10-26,
    receipt `host-clients-r43.json`, the pins of the two re-captured own-work receipts). `diff quality/counters/c2-r42-gkeep-entry.py
    quality/counters/c2-r43-gkeep-entry.py` shows exactly those lines plus a 6-line docstring note.
  - **Counting command:** `cd /home/vgpnk/Projects/shokunin/mado-shokunin && python3 -I quality/counters/c2-r43-gkeep-entry.py --repo . --rev <rev>`
  - **Before:** `admitted=0/1 verdict=TARGET_MISSED`, exit 1 (`receipts/c2-before-base.txt`). **Target:** `admitted=1/1 verdict=TARGET_MET`, exit 0.
    **Kill rule:** as C1.
- **Separability.** C1 touches `tools/mado-geometry.py` only (plus receipts). C2 touches the entry, registry rows, the lesson `## Gate` and the
  README index; C2's census lines are recomputed by C2's own parsers from pinned receipts, so C2 never runs C1's tool and C1 reads no C2 file.

## Pre-wave fetches (PINS of C2; `fetch/`, `receipts/fetch-sha256.txt`, fetched 2026-10-26T04:11-03:00)

Hyprland raw files at `efb50993780079460b0cbed1363e2166a2de1d9f` (`https://raw.githubusercontent.com/hyprwm/Hyprland/<commit>/<path>`), all seven
**byte-identical** to the round-42 pins: `Hyprland-RegexMatchEngine.cpp` (src/desktop/rule/matchEngine), `Hyprland-WindowRuleApplicator.cpp`
(src/desktop/rule/windowRule), `Hyprland-DefaultFloatingAlgorithm.cpp` (src/layout/algorithm/floating/default), `Hyprland-Target.cpp`,
`Hyprland-WindowTarget.cpp` (src/layout/target), `Hyprland-GeometricMovableAnimated.cpp` (src/desktop/view/types), `Hyprland-HyprCtl.cpp` (src/debug).
Own-work: `host-gkeep.conf` (byte copy of `~/.config/hypr/gkeep.conf`, sha256 `3726e488…`, identical to round 42), `host-clients-r43.json`
(`hyprctl clients -j` reduced to address/mapped/class/floating/size/at/monitor; 4 clients Alacritty, zcode, grok-bot, chromium, none floating,
no gkeep window), `gkeep-ui-excerpt.py` (regenerated: `sed -n '446,$p'` of `~/Projects/gkeep/gkeep/ui.py` at gkeep `133b867`, full-file sha256
`07a3c4a5…`; the round-42 excerpt's header claimed lines 446-495 of a 488-line file and carried one extra blank line — a round-42 mistake, mined in
the lesson).

## Controls (committed receipts at this freeze)

- **C1:** `receipts/ctl-c1.txt` — the round-42 runner `.ufo/waves/round-42/ctl/run-c1-controls.py` re-run at the round-43 base: `CTL_C1: rev=a35cfdf… controls=46`, 48 `ok` lines (REF, BASE-absent and the 46 controls: 3 do-nothing, 5 cheats, 38 single-defect mutants), `CTL_C1 VERDICT: PASS (controls scoring TARGET_MET: 0 of 47; reference met: 1)`, exit 0; the equivalent mutants `M03`, `M20`, `M38` stay excluded by name.
  Count definition (round-42 closure routed item 3): `controls=` in the header counts the do-nothing controls, cheats and mutants and excludes
  the two anchors `REF` and `BASE-absent`; the verdict line's denominator counts every non-reference run, i.e. `controls` + `BASE-absent`.
- **C2:** `receipts/ctl-c2.txt` — the round-42 runner with the round constants (`ctl/run-c2-controls.py`): `CTL_C2: controls=74 correct=74/74`, exit 0 — control P admitted under the real and the pin-patched counter (with the round-43 pins), the 72 mutants and forgeries rejected.
- `receipts/freeze-counter-check.txt` — every counter, checker and control path this file names exists at the freeze.

## Residuals (declared, carried from round 42)

- C1: a tool that contains a model of the contract is an implementation; clause g is a heuristic over names; the sandbox is detectable; Python `re`
  is not RE2 (the regex alphabet is restricted to where they agree); whether Hyprland applies a rule's size to a live window is a compositor fact the
  counter does not score (an oracle observation, if the wave obtains one, is reported, not scored).
- C2: the pins are the trust root; a real receipt can be cited for a claim it does not support at a true locator with a word-bounded quote (the
  non-author closure's job); a held id's receipt is not pinned; locators of HTML receipts are not checked.
- `w2` attacks both predicates and the landed data; a hole it finds is reported as an open defect of the predicate (no re-registration after data).
  A hole `w1` finds **before any data commit** re-registers as v2 with a new freeze, and the report names both predicates.

## Frontier step, assimilation, considerthese (§2b / §10)

- Theme: the **gkeep geometry** theme of `/home/vgpnk/Projects/shokuknow/merge/mado/` (11 staged files). One successor entry admitted, at least one
  staged file refused with reason and flip condition; id guard and quarantine slice run in scratch (`assimilation/`) before any registry append.
- Mistake mining (`corpus/lessons/round-43.md` `## Mistakes`): the round-42 closure's routed defects (wrong prose locators, tally, SHONEN pointer,
  missing lesson) and the excerpt header; the locator fix is a checker shown able to fail on the round-42 LOG bytes (seat `ExecLocatorGate`).
- considerthese: `considerthese/2026-10-25.md` proposal 2 ("count dead attempts and dirty closures"), planned in round 42 and never landed.
