# CritPremise — round-45 w1 findings: the premises, and the host claim

Seat: falsify C1/C2's premises (is the monitor plane genuinely uncovered; is the host claim honest;
what happens to the round-3 `99.997` sentence). All locators below are computed with `grep -n`/`sed -n`
against the files named, not typed; every pin citation is to
`.ufo/waves/round-45/fetch/` at the sha256 in `receipts/fetch-sha256.txt`. The commands and their
outputs behind every claim here are in `w1/CritPremise/receipts.txt` (same dir as this file).

## 0. What I ran (read-only; no compositor mutation, no host write)

```
git -C mado-shokunin ls-tree -r --name-only 0c89478a -- corpus/knowledge tools     # base inventory
git -C mado-shokunin grep -n -i -E 'monitor =|monitors -j|refreshRate|transform|desc:' 0c89478a -- corpus/knowledge tools SKILL.md PROVINCE.md
git -C mado-shokunin grep -n -E 'monitorv2|MonitorRule|WxH@|[0-9]+x[0-9]+@[0-9]+|mirrorOf|transform' 0c89478a -- corpus/knowledge
sed -n '183,185p' corpus/knowledge/hyprland-config-plane.md; sed -n '153p;280p' corpus/knowledge/hyprctl-verification-layer.md
sed -n '378,381p;928p' corpus/knowledge/config-health-report-r3.md; sed -n '218,219p' corpus/knowledge/remaining-planes-census.md
sha256sum .ufo/waves/round-45/fetch/*                       # vs receipts/fetch-sha256.txt
sha256sum ~/.config/hypr/monitors.conf
grep -rn -E '^\s*monitor\s*=|^\s*monitorv2' ~/.config/hypr ~/.local/share/omarchy/default/hypr \
     ~/.config/omarchy/current/theme/hyprland.conf ~/.local/state/omarchy/toggles/hypr
grep -n -E '^\s*source' ~/.config/hypr/hyprland.conf
hyprctl version | head -2
hyprctl monitors all -j | python3 -c '<projection>'
hyprctl getoption debug:disable_scale_checks -j
hyprctl monitors all -j | python3 -I .ufo/waves/round-45/l1-draft/mado-monitors.py \
     --monitors - --config ~/.config/hypr/monitors.conf
```

## 1. Premise "the monitor plane did not hold this surface" — SPLIT: chain uncovered, observation NOT

**Counterexample (strongest local evidence).** `corpus/knowledge/hyprctl-verification-layer.md:153`,
in its §4 "Non-getoption claim→live pairs" table:

> `| monitor mode (L-MON:10) | DP-1, 3440x1440@100, 0x0, 1 | hyprctl -j monitors → DP-1 3440x1440 @ 99.99700, at 0x0, scale 1 … | agreement …|`

That is the C1 join's observable half — one declared rule resolved to one output and compared to the
live dump — held since round 2 (probe window 2026-10-14, `hyprctl-verification-layer.md:3`), classed
`agreement`. Three more base notes hold the same observation:

- `corpus/knowledge/hyprland-config-plane.md:183-185`: "`hyprctl monitors`: DP-1 (ID 0),
  `3440x1440@99.99700 at 0x0` … Config declares `3440x1440@100` (`monitors.conf:10`).
  … all other monitor templates commented."
- `corpus/knowledge/config-health-report-r3.md:928`: F5 row, verdict `equal → REPRODUCED`.
- `corpus/knowledge/remaining-planes-census.md:218`: DP-1 scale 1, refresh 99.997 Hz.

**What the registration discloses.** `registration.md:18` names only `tools/mado-verify.sh:3518-3530`
("checks one hardcoded output … without reading any rule"); `registration.md:40-42` names two held
neighbours: the r3 F5 point sample and `workspace-rules-r27.md`. The receipt's wider sweep
(`receipts/c2-ground-base.txt`, part 2) *did* catch `hyprctl-verification-layer.md:280` and the r3
lines, but the prose list omits `hyprctl-verification-layer.md:153`, `hyprland-config-plane.md:183-185`
and `remaining-planes-census.md:218`.

**What is genuinely unmoved at base** (so the claim survives a restatement, and is not narrowed):

| chain element | base coverage | pin |
|---|---|---|
| same-selector erase + append; reverse lookup; empty-selector fallback | none (workspace-rule analogues only, `workspace-rules-r27.md:30,48`) | `Hyprland-MonitorRuleManager.cpp:37-42,96-107` |
| 60 Hz default without `@RATE` | none | `Hyprland-MonitorRule.hpp:46` |
| 1 px / 1 Hz closeness bound, synthesized-mode fallback | none | `Hyprland-Monitor.cpp:819-840` |
| 1/120 scale snap, 89-step search | none | `Hyprland-Monitor.cpp:997-1049` |
| eight line keys, unknown key rejects the line | none | `Hyprland-legacy-ConfigManager.cpp:1345-1379` |
| `desc:` short/long description selector | none (the dump's `description` is the short form) | `Hyprland-Monitor.cpp:1201-1211`, `Hyprland-HyprCtl.cpp:277` |
| documented `sdr_eotf` on a `monitor =` line vs `monitorv2` only | none | `wiki-Monitors.md:253`; `Hyprland-legacy-ConfigManager.cpp:576,819,1351-1379` |
| a tool joining arbitrary rules with a dump | none: `tools/mado-options.py:179` lists `monitor` as an excluded directive, so it never parses the line | — |

**Verdict.** The sentence "a surface the lane did not hold" (`registration.md:11`) is false as
written for the *observation* and true for the *chain and the tool*. `entry.md:14`'s ground line
("`output-colour-boundaries-r14.md` left 'runtime state agreement' UNK") is literally true — r14's own
negative at `output-colour-boundaries-r14.md:91` is scoped "to round-14 executed work" — but a reader
who takes it as "the lane had nothing" is being misled, because the round-2 note already carried a
monitor-mode agreement row.

**Impacted axes.** coverage (C2's novel content is the chain, not the host observation); provenance
(§6 of the entry duplicates a held row without citing it). Operability is unaffected: C1's tool is
new in fact.

**Smallest safe correction.** No re-freeze and no scope reduction: (i) in `entry.md`, extend the
`ground:` line and §6 to cite `hyprctl-verification-layer.md:153`, `hyprland-config-plane.md:183-185`
and the r3 F5 row, and state the delta in one sentence ("those rows compare the one host rule by hand;
this entry supplies rule resolution, the tolerance and the general tool"); (ii) the L1 reports the
incomplete disclosure list rather than silently relying on it.

## 2. The round-3 `99.997` sentence — the new entry neither supersedes, nor corrects, nor contradicts it

The sentence, `corpus/knowledge/config-health-report-r3.md:378-380` (heading at `:378`):

> "`monitors.conf:10` declares `3440x1440@100`; live `refreshRate` `99.997`. Class carried: EDID nominal quantization `[INF]`."

The entry's nearest sentence, `entry.md:82`:

> "The 0.003 Hz gap is inside the 1 Hz closeness bound."

and `entry.md:23`: "Hyprland's own closeness test: within 1 px and 1 Hz of the request".

**What the pins prove.** Mode choice sorts the output's own mode list, takes the closest, and only
synthesizes the requested rate when nothing is within 1 px and 1 Hz (`Hyprland-Monitor.cpp:819-840`);
the running value is then *the chosen mode's* rate, `m_refreshRate = mode->refreshRate / 1000.f`
(`Hyprland-Monitor.cpp:903`). The host's dump prints `99.997`, not `100.00000`, so on this host the
bound was satisfied by an advertised mode. The bound explains **why Hyprland accepts** the gap; it
does **not** explain **where 99.997 comes from**. That origin is the mode list's rate, whose
enumeration (EDID → kernel → Aquamarine) is in none of the nine pins: `fetch/` holds no Aquamarine
source. So the r3 class `[INF]` is neither confirmed nor refuted by round 45.

**The lane already carries two wordings for one fact.** `hyprctl-verification-layer.md:257` repeats
r3's class ("Monitor `99.99700` vs declared `100`: treated as EDID nominal quantization"), while the
same file's §4 row at `:153` says "agreement (fresh rate reported as EDID-actual; 99.997 vs nominal 100
`[INF]`)" — `EDID-actual` against r3's `EDID nominal quantization`. Round 45 should say which wording
it adopts, or a third phrasing joins two standing ones.

**Verdict.** Not a supersession, not a correction, not a contradiction: an orthogonal addition about
tolerance. The risk is a *reading* risk — if §6 is quoted as "the 0.003 gap is explained by the bound",
the origin question is smuggled closed. `[INF]` remains the standing class and must not be upgraded on
these pins.

**Smallest safe correction.** In §6, word it as tolerance, not cause ("the 0.003 Hz gap is tolerated
by the 1 Hz closeness bound; the rate itself is the chosen mode's own rate, and the mode list's
provenance is outside these pins"), keep the r3 `[INF]` untouched, and pick one of the two held
wordings.

## 3. Host claim honesty — HONEST, and independently reproduced

- **Config bytes match the receipt.** `sha256sum ~/.config/hypr/monitors.conf` →
  `69c9d8996dfdcd6747775e984a479c53a520bd2ef193d337e171927fdf6795ee`, identical to
  `receipts/live-monitors-host-l1.txt:3`.
- **The declared line is the effective plane.** `monitors.conf:10` is `monitor = DP-1, 3440x1440@100, 0x0, 1`.
  Recursing the whole `source =` chain (`hyprland.conf:4-13,16-23,29,32`) — omarchy defaults, the
  theme tree, the toggles glob and the local files — yields **no other** `monitor =` or `monitorv2`
  line; the only other hits are `hyprlock.conf:8,19`, which are hyprlock's own config, a different
  consumer. So "one rule, one output" (`entry.md:82`) is true of the effective plane, not just of the
  file the tool was pointed at.
- **The round's own verdict reproduces.** A fresh read-only run of the reference —
  `hyprctl monitors all -j | python3 -I l1-draft/mado-monitors.py --monitors - --config ~/.config/hypr/monitors.conf` —
  printed the receipt's three lines byte-for-byte (`MADO_MON_RULE: n=1 sel="DP-1" …`, `… verdict=AGREE`,
  `… verdict=OK`) and `exit=0`, matching `live-monitors-host-l1.txt:6-8`.
- **Live fields.** `hyprctl monitors all -j` projects to one object: DP-1, 3440×1440, `refreshRate`
  99.997, x/y 0/0, scale 1, transform 0, disabled false, mirrorOf none; `hyprctl version` is
  `Hyprland 0.56.2 … efb50993780079460b0cbed1363e2166a2de1d9f clean`, as the receipt's line 2 says.
- **Session material.** The dump *does* carry `description`, `make`, `model`, `serial`
  (`Hyprland-HyprCtl.cpp:277-278`); the committed receipt keeps only name/size/rate/pos/scale/
  transform/disabled/mirrorOf and states the projection, so no serial or description is committed.
  No window titles, no PIDs, no home-directory listing. Nothing to redact.

## 4. Counterexamples to the model the claim will publish (defects, all fixable inside the claim)

**(a) The scale correction is conditional, and `entry.md:62` presents it unconditionally.**
`Hyprland-Monitor.cpp:997` opens the block only when the debug switch is off:

> `if (!*PDISABLESCALECHECKS && (logicalSize.x != std::round(logicalSize.x) || …`

`Hyprland-Monitor.cpp:721` binds that to `debug:disable_scale_checks`. Host value:
`hyprctl getoption debug:disable_scale_checks -j` → `{"option": "debug:disable_scale_checks", "int": 0, "set": false}`,
so the host claim is unaffected. But the reference tool never mentions the switch
(`grep -n -i -E 'scale_checks|debug:' l1-draft/mado-monitors.py` → no match): on a config with the
switch on, the tool would still predict the 1/120 snap and could report a DIFFER that Hyprland does
not produce. Fix: one clause in §3 plus either a `NOT_COMPARED` reason or an explicit residual.

**(b) A branch precedes the rule list and is invisible in the dump.**
`Hyprland-MonitorRuleManager.cpp:86-94` returns a hardcoded rule for `m_isUnsafeFallback` outputs —
`1920x1080`, auto-right, scale 1 — before the reverse lookup at `:96-107` and the empty-selector
fallback at `:103-107`. `entry.md:54` states the lookup order without that branch. The flag is not in
the monitors JSON (`grep -n isUnsafeFallback Hyprland-HyprCtl.cpp` → no match; only
`Hyprland-Monitor.cpp:331` and `Hyprland-MonitorRuleManager.cpp:140`), so a DIFFER on such an output is not attributable to the
config and no single-dump tool can tell. Fix: name the branch and the resulting residual.

**(c) Two tolerances for one question, undeclared.** `tools/mado-verify.sh:3526` passes DP-1 only when
`abs(refreshRate - 100) < 0.5`, while the new tool calls AGREE on Hyprland's own 1 Hz bound
(`Hyprland-Monitor.cpp:836-837`). Both are read-only checks of the same host fact; a host at 99.4 Hz
would fail the gate and pass the new tool. Fix: state which threshold is the operator's expectation
and which is the compositor's own test (the tool's receipt could label the bound it applied).

## 5. What supports the claims (so the L1 knows what survived this sweep)

- **Pins verify.** All nine sha256 in `receipts/fetch-sha256.txt` match the files in `fetch/`,
  including the two URLs repeated from held rows: `Hyprland-HyprCtl.cpp` = S158's
  `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` (`corpus/SOURCES.md:170`) and
  `Hyprland-legacy-ConfigManager.cpp` = S162's `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`
  (`corpus/SOURCES.md:174`). No false provenance on the repeat.
- **Registry space is free.** `corpus/SOURCES.md:250` is the last row (S301); S302-S310 do not collide.
- **Census line arithmetic holds.** Eight keys exactly — mirror, bitdepth, cm, sdrsaturation,
  sdrbrightness, transform, vrr, icc (`Hyprland-legacy-ConfigManager.cpp:1351-1379`) → `line_keys=8`;
  `m_refreshRate = 60` (`Hyprland-MonitorRule.hpp:46`) → `default_refresh=60`; the rate bound is 1
  (`Hyprland-Monitor.cpp:836-837`) → `refresh_tolerance=1`; `std::round(m_scale * 120.0)`
  (`:1001`) and `for (size_t i = 1; i < 90; ++i)` (`:1010`) → `scale_step=1/120 scale_search=89`;
  `{:.5f}` (`Hyprland-HyprCtl.cpp:242`) → `json_refresh_decimals=5`. Fixture `scale-snap`
  (`l1-draft/mado-monitors.py:467`) with 2880×1920 at scale 1.6 is a clean divisor, so it does not
  exercise the snap — the 89-step search is covered only by the code statement.
- **Lookup-order statement.** Reverse iteration then first empty selector then a default of
  `Vector2D{}`/scale −1 (`Hyprland-MonitorRuleManager.cpp:96-118`), which is `preferred` +
  `auto` scale + `auto` position at `Hyprland-Monitor.cpp:769-780` and `:750` — so `entry.md:54`'s
  "(preferred, auto, auto)" is right even though the struct literals read `Vector2D()` / `-1`.
- **`sdr_eotf` divergence.** Registered only as a `monitorv2` special value
  (`Hyprland-legacy-ConfigManager.cpp:576`) and read only there (`:819`), absent from the legacy key
  loop (`:1351-1379`), while the wiki documents it on the monitor line (`wiki-Monitors.md:253`,
  table row `:319`) — the entry's `[INF]` label for the rejection is the correct strength.
- **Axis arithmetic is not being overstated.** `receipts/axis-base.txt` is published=derived at
  61/61, 71/71, 12/12: no axis count can rise, so the round's "after-state is the counter line" framing
  is the only honest one, as the registration says.

## 6. Refusals / out of scope here

- I did not score either counter or run the control suites (other seats own that); the C1 REF line in
  `receipts/ctl-c1.txt:1` is `fixtures=49/49 TARGET_MET`, consistent with the frozen target, but I did
  not reproduce it.
- I did not run the tool with `hyprctl monitors -j` (active-only) or against the sourced-file set —
  `w1/ExecLiveHost` owns that run; my effective-plane check is file-level and independent of it.
- No tool installed, no pacman, no scratch retained: `/fast/scratch/hyaku/mado-r45/CritPremise`
  removed (nothing was written there).
