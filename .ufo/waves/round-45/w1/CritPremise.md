# w1 / CritPremise — premises falsification (final)

Seat scope: is the monitor plane genuinely uncovered, is the host claim honest, and what becomes of
the round-3 `99.997` sentence. Evidence: `w1/CritPremise/findings.md`; commands and outputs:
`w1/CritPremise/receipts.txt`. All locators computed; all reads read-only; no tool installed, no
pacman, no compositor mutation; scratch `/fast/scratch/hyaku/mado-r45/CritPremise` removed.

## 1. "A surface the lane did not hold" (`registration.md:11`) — SPLIT: chain new, observation NOT

Counterexample (strongest local evidence): `corpus/knowledge/hyprctl-verification-layer.md:153` is
already the C1 join's observable half — declared `DP-1, 3440x1440@100, 0x0, 1` vs
`hyprctl -j monitors` → `3440x1440 @ 99.99700, at 0x0, scale 1`, classed `agreement`, dated
2026-10-14 (`:3`), i.e. before r14. Three more base rows hold the same observation:
`hyprland-config-plane.md:183-185`, `config-health-report-r3.md:928`, `remaining-planes-census.md:218`.
The registration discloses `mado-verify.sh:3518-3530` (`registration.md:18`) and one r3 neighbour
(`:40-42`), not these four. The frozen claim grep still exits 1 (reproduced), so the *chain* is
genuinely unmoved: rule storage/lookup (`Hyprland-MonitorRuleManager.cpp:37-42,96-107`), 60 Hz default
(`Hyprland-MonitorRule.hpp:46`), 1 px/1 Hz bound (`Hyprland-Monitor.cpp:819-840`), 1/120 snap with an
89-step search (`:997-1049`), eight line keys (`Hyprland-legacy-ConfigManager.cpp:1345-1379`), `desc:`
selector (`Hyprland-Monitor.cpp:1201-1211`), `sdr_eotf` docs/code divergence
(`wiki-Monitors.md:253` vs `Hyprland-legacy-ConfigManager.cpp:576,819`), and a general tool (none:
`tools/mado-options.py:179` excludes `monitor`). C1's tool is new in fact; C2's novelty is the chain.

**Smallest safe correction:** extend `entry.md:14`'s `ground:` line and §6 to cite the four held rows
and state the delta in one sentence; the L1 reports the incomplete disclosure list. No re-freeze, no
narrowing.

## 2. Round-3 `99.997` sentence — neither superseded, corrected nor contradicted

`config-health-report-r3.md:380`: "`monitors.conf:10` declares `3440x1440@100`; live `refreshRate`
`99.997`. Class carried: EDID nominal quantization `[INF]`." The entry's nearest sentence
(`entry.md:82`) is about **tolerance**. Pins: selection at `Hyprland-Monitor.cpp:819-840`, running
value = the chosen mode's own rate (`:903`), synthesizing would have printed `100.00000`; the mode
list's provenance (EDID → kernel → Aquamarine) is in none of the nine pins, so `[INF]` neither
confirmed nor refuted. Two classes already stand for one fact — `:257` uses r3's wording while `:153`
says `EDID-actual`.

**Smallest safe correction:** word §6 as tolerance, not cause ("tolerated by the 1 Hz bound; the rate
is the chosen mode's own rate; the mode list's provenance is outside these pins"), keep `[INF]`, and
pick one of the two standing wordings.

## 3. Host claim — HONEST, independently reproduced

`sha256sum ~/.config/hypr/monitors.conf` = `69c9d899…95ee`, identical to
`receipts/live-monitors-host-l1.txt:3`; the whole `source =` chain (`hyprland.conf:4-13,16-23,29,32`)
holds exactly one `monitor =` line (`monitors.conf:10`; `hyprlock.conf:8,19` are hyprlock's own), so
"one rule" is true of the effective plane; a fresh read-only run of the reference reproduced the
receipt's three lines and `exit=0`; the dump projects to one output, DP-1 3440×1440 99.997 0x0 scale 1
transform 0 not-disabled mirror none under `Hyprland 0.56.2 … efb50993`. The receipt commits no
description, serial, make, model, title or PID (the raw dump does carry them, `Hyprland-HyprCtl.cpp:277-278`).

## 4. Three model gaps to name before the data commit

1. Scale correction is gated on `debug:disable_scale_checks` (`Hyprland-Monitor.cpp:721,997`);
   `entry.md:62` states it unconditionally and the reference tool never mentions it. Host is
   `int 0, set false`, so the host claim stands.
2. The `m_isUnsafeFallback` branch (`Hyprland-MonitorRuleManager.cpp:86-94`, 1920×1080/auto-right/1)
   precedes the rule list and is absent from the monitors JSON, so a DIFFER there is not
   config-attributable and no single-dump tool can see it; `entry.md:54` omits the branch.
3. Two tolerances for one fact, undeclared: `tools/mado-verify.sh:3526` passes at <0.5 Hz, the new
   tool's AGREE uses the 1 Hz bound — say which is the operator's expectation and which is Hyprland's.

## 5. What supports the claims

Nine pin sha256 all verify, including the repeated URLs (S158 `798b7c6c…`, S162 `9db68cf4…`); registry
tops at S301 (`corpus/SOURCES.md:250`) so S302-S310 do not collide; the census arithmetic holds
(`line_keys=8`, `default_refresh=60`, `refresh_tolerance=1`, `scale_step=1/120 scale_search=89`
from `:1001,1010`, `json_refresh_decimals=5` from `Hyprland-HyprCtl.cpp:242`); the "(preferred, auto,
auto)" default is right (`Hyprland-MonitorRuleManager.cpp:113` + `Hyprland-Monitor.cpp:773,750`); and
`receipts/axis-base.txt` is published=derived at 61/61, 71/71, 12/12, so the axis move is a
re-derivation, as declared — no axis count is over-claimed.

Not mine (other seats): scoring either counter, the control suites, the sourced-config live run
(`w1/ExecLiveHost`), the privacy gate (`w1/ExecPrivacyGate`).
