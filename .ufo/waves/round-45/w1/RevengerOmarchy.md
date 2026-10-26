# RevengerOmarchy — how omarchy writes and expects `monitors.conf` (round 45, w1)

Read-only reverse-engineering of the omarchy install on this host
(`/home/vgpnk/.local/share/omarchy`, git HEAD `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`,
branch `rc`, 2026-07-20, `version` = `3.8.3`), joined against the round-45 reference
`l1-draft/mado-monitors.py` (sha256 `c6ac5fc2d35e40b34dcf031940222fbe5ec5f0ce4b07d6a41866b196843726be`,
selftest `33/33 passed`, the same hash the round's live receipt `receipts/live-monitors-host-l1.txt`
recorded) and the round-45 pins in `.ufo/waves/round-45/fetch/`. No omarchy script was executed;
no compositor state was changed; the only compositor read was `hyprctl monitors -j` for a mode token.

Everything below is either a command + its output (receipts in
`.ufo/waves/round-45/w1/RevengerOmarchy/receipt-*.txt`) or marked `[INFERENCE]`.

---

## 1. The default file

There is **no** `default/hypr/monitors.conf`. The shipped default is
`config/hypr/monitors.conf` (sha256 `6259c0eda4b0501389503133a03df100fd5ce49d1af1616cb0d898a8dd338f55`,
26 lines), installed to `~/.config/hypr/monitors.conf` by `omarchy-refresh-hyprland:10` →
`omarchy-refresh-config hypr/monitors.conf` (that helper only `cp -f`s the default over the user
file after backing it up, and it never edits monitor lines).

Numbered shipped file (`receipt-files.txt`):

```
 1| # See https://wiki.hypr.land/Configuring/Basics/Monitors/
 2| # List current monitors and resolutions possible: hyprctl monitors
 3| # Format: monitor = [port], resolution, position, scale
 4|
 5| # Optimized for retina-class 2x displays, like 13" 2.8K, 27" 5K, 32" 6K.
 6| env = GDK_SCALE,2
 7| monitor=,preferred,auto,auto
 8|
 9| # Good compromise for 27" or 32" 4K monitors (but fractional!)
10| # env = GDK_SCALE,1.75
11| # monitor=,preferred,auto,1.6
12|
13| # Straight 1x setup for low-resolution displays like 1080p or 1440p
14| # Or for ultrawide monitors like 34" 3440x1440 or 49" 5120x1440
15| # env = GDK_SCALE,1
16| # monitor=,preferred,auto,1
17|
18| # Portrait/rotated secondary monitor (transform: 1 = 90°, 3 = 270°)
19| # monitor = DP-2, preferred, auto, 1, transform, 1
20|
21| # Example for Framework 13 w/ 6K XDR Apple display
22| # monitor = DP-5, 6016x3384@60, auto, 2
23| # monitor = eDP-1, 2880x1920@120, auto, 2
24|
25| # Disable the second ghost monitor on an Apple 6K XDR over Thunderbolt
26| # monitor=DP-2,disable
```

**Active lines: exactly two** — `6` (`env = GDK_SCALE,2`) and `7`
(`monitor=,preferred,auto,auto`). One monitor rule, empty selector, mode `preferred`, position
`auto`, scale `auto`. Every other line is a comment or prose. Git history of the file
(`git log -12 -- config/hypr/monitors.conf`) shows the line shapes that came and went:
`monitor=,preferred,auto,2` (commit `e446c4c71`), `monitor=,preferred,auto,1.666667`
(`033a2d9f0`), then `1.6` (`261a7dcc1`, "Don't suggest invalid scale"), then
`monitor=,preferred,auto,auto,vrr,1` (`6329062f2`) and back to `auto` (`58443c82c`) with the
migration `migrations/1776781957.sh:6` rewriting it in place.

This host's installed copy (`~/.config/hypr/monitors.conf`, sha256
`69c9d8996dfdcd6747775e984a479c53a520bd2ef193d337e171927fdf6795ee`, 29 lines) is the same text
from an earlier refresh with two local edits: line 9 `env = GDK_SCALE,1` and line 10
`monitor = DP-1, 3440x1440@100, 0x0, 1` (the shipped presets are still commented). It is *not*
omarchy's default any more: the shipped default's rule cannot express a mode/position/scale
mismatch at all (see §4, D1).

Sourcing order (`config/hypr/hyprland.conf`): `:16 source = ~/.config/hypr/monitors.conf`, then
`:23 source = ~/.local/state/omarchy/toggles/hypr/*.conf`. **Monitor rules are not confined to
`monitors.conf` on omarchy** — see §2.3.

---

## 2. What reads and writes monitor lines

`grep -rn 'echo "monitor=|sed -i.*monitor' bin install migrations config` returns four writers and
nothing else (`receipt-files.txt`, tail):

| where | writes | target |
|---|---|---|
| `bin/omarchy-hyprland-monitor-internal:25` | `echo "monitor=$INTERNAL,disable"` | `~/.local/state/omarchy/toggles/hypr/internal-monitor-disable.conf`, then `hyprctl reload` (`:27`) |
| `bin/omarchy-hyprland-monitor-internal-mirror:31` | `echo "monitor=$EXTERNAL, preferred, auto, 1, mirror, $INTERNAL"` | `…/toggles/hypr/internal-monitor-mirror.conf`, then `hyprctl reload` (`:33`) |
| `bin/omarchy-hyprland-monitor-scaling-cycle:43` | `sed -i -E "s|^(monitor=,preferred,auto,).*|\1${NEW_SCALE}|"` | `~/.config/hypr/monitors.conf` (guarded by `:41`–`:42`) |
| `migrations/1776781957.sh:6` | `sed -i 's/^monitor=,preferred,auto,auto,vrr,1$/…auto/'` | `~/.config/hypr/monitors.conf` (one-shot) |

plus `bin/omarchy-hyprland-monitor-scaling-cycle:35`, which does **not** write a file but adds a
live rule: `hyprctl keyword monitor "$ACTIVE_MONITOR,${WIDTH}x${HEIGHT}@${REFRESH_RATE},auto,$NEW_SCALE"`.
`bin/omarchy-menu:326` opens `~/.config/hypr/monitors.conf` in `$EDITOR`.

Readers are all `hyprctl monitors -j` consumers: `monitor-focused:5`, `monitor-focused-apple:5`,
`monitor-internal:11`, `monitor-internal-mirror:11,13`, `monitor-scaling-cycle:5-10`,
`menu-keybindings:246`, `launch-screensaver:23`, `capture-screenshot:52-53`,
`capture-screenrecording:62,95,106,148`, `windows-vm:338`.

### 2.1 The scaling cycle (the only script that rewrites a rule in place)

```bash
13| SCALES=(1 1.25 1.6 2 3 4)
...
35| hyprctl keyword monitor "$ACTIVE_MONITOR,${WIDTH}x${HEIGHT}@${REFRESH_RATE},auto,$NEW_SCALE"
...
41|   mapfile -t ACTIVE_LINES < <(grep -E '^[[:space:]]*monitor=' "$MONITOR_CONF" | grep -vE 'disable[[:space:]]*$')
42|   if [[ ${#ACTIVE_LINES[@]} -eq 1 ]] && [[ "${ACTIVE_LINES[0]}" =~ ^monitor=,preferred,auto, ]]; then
43|     sed -i -E "s|^(monitor=,preferred,auto,).*|\1${NEW_SCALE}|" "$MONITOR_CONF"
```

Three hard assumptions, all checkable against the frozen contract:

* **the scale is the last field of the line** — `sed`'s `.*` swallows everything after the third
  comma. Simulated on scratch copies with the script's own expression (`receipt-sed-guard.txt`):
  `monitor=,preferred,auto,auto,vrr,1` → `monitor=,preferred,auto,1.25`: **`vrr,1` is deleted**.
  The contract models `vrr` as a KEY,VALUE pair after the scale, so a pre-migration line loses a
  real setting silently.
* **the catch-all line is the only active `monitor=` line and begins `monitor=`** — the guard's
  regex needs no space before `=`. Against the shipped file: 1 active line, regex MATCH. Against
  **this host's** file: 0 active lines (`monitor = DP-1, …` has a space), so persistence never
  happens here and the scale survives only until the next `hyprctl reload`.
* **`hyprctl keyword monitor` changes only the scale** — per the contract (and
  `Hyprland-MonitorRuleManager.cpp:38`, erase-by-selector on add) the keyword *replaces* the whole
  rule, and it passes `auto` as the position. A display that had an explicit position is re-placed
  by `auto`. Fixture `G04`: conf `monitor = DP-2, 2560x1440@144, 3440x0, 1`, live `x=0` →
  `differ=position`. So cycling scaling can also move monitors on a multi-head setup.

### 2.2 The mode token the cycle emits does not fit the entry's grammar

`REFRESH_RATE` comes from `.refreshRate` (`:10`); `hyprctl` prints that field with five decimals
(`Hyprland-HyprCtl.cpp:242` → `"refreshRate": {:.5f},`) and jq 1.7 preserves the literal. On this
host (`hyprctl monitors -j | jq -r '.[]|select(.focused)|"\(.width)x\(.height)@\(.refreshRate)"'`)
the token is **`3440x1440@99.99700`**, so the keyword string is
`DP-1,3440x1440@99.99700,auto,<scale>`. Fed to the reference as a config line:

```
MADO_MONITORS: lines=1 rules=0 v2=0 unsupported=1 badrules=0 … verdict=NOT_COMPARED   exit=5
```

while Hyprland's own parser accepts it: `Hyprland-Parser.cpp:134`
`m_rule.m_refreshRate = stof(value.substr(value.find_first_of('@') + 1));` — no decimal cap, no
regex. The entry's `MODE` form (`@[0-9]{1,3}(\.[0-9]{1,3})?`) is **stricter than the pinned
parser**; the failure mode is an honest `NOT_COMPARED`, never a false AGREE/DIFFER, but it means a
rule copied from `hyprctl monitors` output (which the file's own line 2 invites: "List current
monitors and resolutions possible: hyprctl monitors") cannot be scored.

### 2.3 Monitor rules outside `monitors.conf`

`hyprland.conf:23` sources `~/.local/state/omarchy/toggles/hypr/*.conf` **after**
`monitors.conf:16`, and two of the four writers put `monitor=` lines there. A join fed only
`monitors.conf` therefore cannot see omarchy's own disable/mirror rules. With both files in
sourcing order the contract reproduces them exactly (`receipt-fixtures2.txt`):

* `D01` shipped conf + `monitor=eDP-1,disable`, eDP-1 off → `DISABLED`, exit 0.
* `D02` same, eDP-1 lit → `differ=disabled` → `DIFFER`, exit 1.
* `D03` user adds `monitor = eDP-1, 2880x1920@120, auto, 2` to the conf, toggle disables it:
  `lines=3 rules=2` — the toggle **erased** the user's same-selector rule (erase-on-add), exactly
  `Hyprland-MonitorRuleManager.cpp:38`.
* `D04` shipped conf + `monitor=DP-2, preferred, auto, 1, mirror, eDP-1`, live mirror `eDP-1` via
  `mirrorOf:"1"` → both AGREE, exit 0.
* `C13`/`C14` the same line with the mirror in place vs `mirrorOf:"none"` → AGREE vs `differ=mirror`.

---

## 3. Preset-by-preset: what the tool reports if uncommented

Synthetic dumps only (fake make/model/serial strings); confs derived byte-exactly from the shipped
file by uncommenting the numbered lines (`drive.py`, `drive2.py`, `drive3.py` in this seat dir;
outputs `receipt-fixtures*.txt`, `receipt-correction-probe.txt`, `receipt-nomatch.txt`).

| # | active lines | synthetic live state | tool output |
|---|---|---|---|
| shipped | 6,7 | DP-1 3440x1440@99.997 scale 1 | `1 rule, AGREE`, `verdict=OK` exit 0 (reproduces `receipts/live-monitors-host-l1.txt` offline) |
| shipped | 6,7 | same output, scale **2** | `AGREE`, exit 0 — the catch-all compares **nothing but transform** |
| shipped | 6,7 | same output, transform **1** | `differ=transform`, `DIFFER` exit 1 |
| 1x | 6,7,15,16 | live scale 1 | `AGREE`, exit 0 |
| 1x | 6,7,15,16 | live scale 2 | `differ=scale`, exit 1 |
| 1x | 6,7,15,16 | live scale 1.5 (what auto gives on a medium-PPI 4K, §4 D2) | `differ=scale`, exit 1 |
| fractional | 6,7,10,11 | live 1.6 on 3440x1440 | `AGREE`, exit 0 (`lines=2 rules=1`: the 1.6 line **erased** the `auto` line) |
| fractional | 6,7,10,11 | live 1.0 (this host is a 3440x1440 1x panel) | `differ=scale`, exit 1 |
| fractional | 10,11 only | live 1.6 on 1366x768 | `differ=scale` — Hyprland would never leave 1.6 there (`E=2.0`) |
| fractional | 10,11 only | live **2.0** on 1366x768 | `AGREE` — the tool applies the 1/120 correction |
| portrait | 7,19 | DP-2 live transform 0 | `differ=transform`, exit 1 |
| portrait | 7,19 | DP-2 live transform 1, scale 1 | `AGREE`, exit 0 |
| Apple pair | 7,22,23 | DP-5 6016x3384@59.997 + eDP-1 2880x1920@119.999, both scale 2 | 3 rules, 2 AGREE, `OK` |
| Apple pair | 7,22,23 | only DP-1 wired | DP-1 falls to the catch-all: `AGREE` (the Apple rules match nothing) |
| ghost | 7,26 | DP-2 present and disabled | `DISABLED`, `verdict=OK` exit 0 |
| ghost | 7,26 | DP-2 present and lit | `differ=disabled`, exit 1 |
| ghost | 26 only | only DP-1 wired | `matched=0` → `NO_MATCHING_MONITOR` exit 3 (`receipt-nomatch.txt`) |
| mirror (script) | mirror line only | DP-2 mirrors eDP-1 (`mirrorOf:"1"`) | DP-2 AGREE, eDP-1 UNRULED, exit 0 |
| mirror (script) | mirror line only | `mirrorOf:"none"` | DP-2 `differ=mirror`, exit 1 |
| pre-migration | `monitor=,preferred,auto,auto,vrr,1` | scale 1 | `AGREE` exit 0 — `vrr` is consumed as a modelled key and **never compared** to live `adaptiveSync` |
| hyprctl token pasted | `monitor = DP-1, 3440x1440@99.99700, 0x0, 1` | DP-1 | `unsupported=1` → `NOT_COMPARED` exit 5 |
| env only | `env = GDK_SCALE,2` | DP-1 | `lines=0` → `NO_RULES` exit 4 |
| all commented | — | DP-1 | `NO_RULES` exit 4 |

All five top verdicts (`OK`, `DIFFER`, `NO_MATCHING_MONITOR`, `NO_RULES`, `NOT_COMPARED`) were
reproduced from omarchy's own text.

The 1/120 correction direction is testable and **matches the pin**: 1366x768 has
`gcd(1366·120, 768·120) = 240`, so from `K=180` (1.5) the reachable neighbours are `K=240` (2.0,
sixty steps **up**) and `K=120` (1.0, sixty steps down). `Hyprland-Monitor.cpp:1010-1029` tries
`+i` before `-i`. The tool agrees: rule 1.5 + live 2.0 → `AGREE` (`G01`); rule 1.5 + live 1.0 →
`differ=scale` (`G02`). Requesting omarchy's `1.6` there yields `E=2.0` → `AGREE` against live 2.0
(`G03`), `DIFFER` against a live 1.6 (`C03`).

---

## 4. Where omarchy's assumptions and the entry's contract diverge

**D1 — the shipped default cannot be wrong about mode, position or scale.**
`monitor=,preferred,auto,auto` leaves all three implicit and the contract compares only an explicit
field; the sole comparable field is `transform` (default 0). Fixtures `C01` (live scale 2 → AGREE)
and `D06` (live transform 1 → DIFFER) show it. An `OK` from the shipped default therefore says
"not disabled and not rotated", not "the display runs what omarchy intends". The file's own claim
("Optimized for retina-class 2x displays") is carried entirely by the `env` line, which is outside
the monitor-rule chain.

**D2 — `env = GDK_SCALE,…` is not a monitor rule, and `scale auto` is not 2.**
The entry's chain begins at the `monitor =` line; the contract ignores `env` lines entirely
(`C19`: an env-only file is `NO_RULES`, exit 4). Meanwhile `scale auto` resolves through
`CMonitor::getDefaultScale` (`Hyprland-Monitor.cpp:1413-1417`): `PPI > 200 → 2`, `PPI > 140 → 1.5`,
else `1`. So on a medium-PPI 4K panel omarchy's shipped pairing is GTK 2x (`GDK_SCALE,2`) with a
compositor at 1.5x, and 1.5 is not even in the cycle list `SCALES=(1 1.25 1.6 2 3 4)`
(`:13`). The tool reports `AGREE` for that pairing because an auto scale is never compared.
Whether GTK honours the commented `GDK_SCALE,1.75` is **not established by any pinned source**
`[INFERENCE]` — it is simply outside the verified chain, so no claim in the entry can lean on it.

**D3 — the presets are alternatives, but leaving line 7 active makes the last one win.**
Uncommenting the fractional pair while keeping the default (`E01`, `E06`) gives `lines=2 rules=1`
with `scale=1.6000`: adding a rule erases the earlier rule with the same (empty) selector
(`Hyprland-MonitorRuleManager.cpp:38`). Nothing in the file says the presets replace line 7, and
the result is a `DIFFER` on any 1x panel. The same applies to `monitor=,preferred,auto,1`
(`E02` → `AGREE` only by luck of the live scale).

**D4 — the scaling cycle deletes KEY,VALUE pairs and can silently not persist.** §2.1. On this
host the guard matches 0 lines, so the notify "Display scaling set to Nx" (`:47`) is true only for
the session.

**D5 — cycling scaling also resets position**, because the keyword re-sends `auto` as the position
and replaces the whole rule (§2.1, fixture `G04`).

**D6 — the scale the user asks for is not the scale Hyprland applies, and omarchy silences the
notice.** `default/hypr/looknfeel.conf:128 disable_scale_notification = true` turns off the
"invalid scale … found suggestion" overlay (`Hyprland-Monitor.cpp:1042-1046`) that Hyprland raises
when its 1/120 correction replaced the requested scale. The correction itself is the entry's
subject (and the tool models it, §3); omarchy's UI layer deliberately hides the only signal that a
substitution happened.

**D7 — the documented format is the 4-field form only.** `default/omarchy-skill/SKILL.md:290-293`
tells the agent to write `monitor = eDP-1, 1920x1080@60, 0x0, 1` and `hyprctl monitors` to list
modes — i.e. it invites the `WxH@rate` token that `hyprctl` prints with five decimals, which §2.2
shows is `NOT_COMPARED` for the reference tool while Hyprland accepts it.

**Non-divergences confirmed** (they strengthen the contract rather than contest it): erase-on-add
and newest-match-wins (`D03`, `C06`), `disable`/`disabled` both accepted (the script writes
`disable`, `Hyprland-legacy-ConfigManager.cpp:1299` accepts both), `mirror` compared by output id,
`transform` applied to an *existing* rule only (`monitor=…,transform,1` after a named rule —
`Hyprland-legacy-ConfigManager.cpp:1302-1316`), and the `preferred`/`auto` prefixes
(`Hyprland-Parser.cpp:111`).

---

## 5. Residual divergences of the reference tool from Hyprland 0.56.2 (found here)

1. **Mode token grammar is narrower than the parser** (`@` decimals ≤ 3 vs `stof`,
   `Parser.cpp:134`). Direction of error is safe (`NOT_COMPARED`).
2. **`misc:disable_scale_checks` is unmodelled** (`Hyprland-Monitor.cpp:997`): with the checks off,
   a live fractional scale is legal and the tool's corrected `E` would report a false `DIFFER`.
   Nothing in omarchy sets it (`grep` over `default/hypr`, `config/hypr` finds only
   `disable_scale_notification`), so this is a latent hole, not a live one.
3. **`env` is a registered handler** (`Hyprland-legacy-ConfigManager.cpp:619`) and `setenv` happens
   on every parse (`:1870`), so a `GDK_SCALE` change takes effect on `hyprctl reload` for newly
   spawned children — the removed "You must relaunch" note (commit `278945418`) is consistent with
   the pin, and still nothing about it is a monitor rule.

---

## 6. Reproduction

Scratch root (deleted after the run): `/fast/scratch/hyaku/mado-r45/RevengerOmarchy/`. Copies of the
drivers, the reference tool and every fixture conf/dump are in this seat dir
(`drive*.py`, `verify_quotes.py`, `mado-monitors-reference.py`, `fixtures/`), so all outputs can be
regenerated without scratch:

```
python3 -I drive.py          # shipped file + presets, verdict matrix (receipt-fixtures.txt)
python3 -I drive2.py         # two-file sourcing order, toggles, host conf (receipt-fixtures2.txt)
python3 -I drive3.py         # "preset uncommented, default still active" (receipt-fixtures3.txt)
python3 -I verify_quotes.py  # locators + sha256 + quote verification (receipt-quotes.txt)
```

Tools installed for this seat: **none** (no package, uv, npm or binary install; nothing was added to
any PATH directory).

## 7. Provenance, confidence, residuals

* Inputs read-only, sha256 of every cited file in `receipt-quotes.txt`; 36 quotes located by
  `grep -nF` and re-verified as substrings of the cited line by `verify_quotes.py`
  (output: `ALL QUOTES LOCATED AND VERIFIED (n=36)`).
* omarchy: HEAD `8fcc9d6048af4cb0e3af8512c78049857a3b53dd`, `version` 3.8.3; default
  `config/hypr/monitors.conf` sha256 `6259c0e…`, host copy `69c9d89…` (identical to the value
  `receipts/live-monitors-host-l1.txt:3` recorded).
* Fixtures are synthetic dumps and derived confs; no live multi-output state, no `desc:` selector,
  no `monitorv2` block (omarchy has none) was exercised. The Apple/portrait/ghost presets were
  scored against invented outputs, not hardware.
* No omarchy script was run and no compositor call except the allowed
  `hyprctl monitors -j` (mode token only; no name/description/serial in any receipt).
* Confidence: **high** for §1, §2, §4 (file text, script text and pinned parser read directly, tool
  outputs reproduced); **medium** for §2.1's runtime consequences (position reset, non-persisting
  guard) — modelled from the pins and the scripts' own regexes, not observed on hardware; **low /
  inference** for anything about GTK's `GDK_SCALE` parsing.
