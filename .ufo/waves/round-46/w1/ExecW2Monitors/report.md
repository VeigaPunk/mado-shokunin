# ExecW2Monitors — round-46 w1, closure D1: falsify the round-45 v2 monitor data

Seat: `ExecW2Monitors` (leaf executor; no dispatch). Date 2026-10-26.
Lane: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Target rev under attack:
`4d22eeb66c2835af8aaa3fac6ad838fa616aa663` (round-45 tip; data commit `ee6659b9`, landed tool/entry/rows S302-S315/gate).
Scratch: `/fast/scratch/hyaku/mado-r46/ExecW2Monitors/` (removed before yielding; every number below is copied into this
seat directory first).

Round-45 closure D1 read: *"run the w2 falsification of the round-45 data inside this round's wave"*. The w2 never ran,
so this seat is that wave: five fresh nonces on the frozen C1 counter, the C2 counter at the data commit and at the tip, a
live run on the host, and 23 hand-written adversarial configs checked against my own reading of the round-45 pins.

## 1. Result

| probe | command | result |
|---|---|---|
| C1 / PRED-C1-r45-v2, nonce 46001 | `c1-r45-monitors-v2.py --repo <lane> --rev 4d22eeb6 --work <scratch> --nonce 46001` | `fixtures=81/81 generated=150/150 selftest=ok readonly=ok tool=present verdict=TARGET_MET` exit 0 |
| nonce 46002 | same, `--nonce 46002` | `TARGET_MET` exit 0 |
| nonce 46003 | same, `--nonce 46003` | `TARGET_MET` exit 0 |
| nonce 46004 | same, `--nonce 46004` | `TARGET_MET` exit 0 |
| nonce 46005 | same, `--nonce 46005` | `TARGET_MET` exit 0 |
| C2 / PRED-C2-r45-v2 at data commit | `c2-r45-monitor-entry-v2.py --repo <lane> --rev ee6659b9` | `admitted=1/1 verdict=TARGET_MET` exit 0, clauses a-j all 1 |
| C2 at tip | same, `--rev 4d22eeb6` | `admitted=1/1 verdict=TARGET_MET` exit 0, clauses a-j all 1 |
| live, sourced config with a monitor line | `hyprctl monitors all -j \| mado-monitors.py --monitors - --config ~/.config/hypr/monitors.conf` | `lines=1 rules=1 ... agree=1 differ=0 disabled=0 verdict=OK` exit 0 |
| adversarial (23 configs) | `python3 adversarial.py` | 22/22 match my reading of the pins; 1 measured conservative gap (F18), 0 unsound verdicts |

**D1 outcome: the round-45 v2 monitor data is not falsified.** The landed tool passes the frozen counter under five fresh
nonces (the nonce axis is what w2 was supposed to add), the entry passes its counter at both the data commit and the tip,
and the live host joins cleanly. No miss, no narrowing was needed, no re-measurement contradicts the published axis.

Evidence files in this directory:

- `c1-nonces.txt` — five nonce runs, per-nonce exit code, clause `s`/`g`/`r` lines and the final line.
- `c2-entry.txt` — C2 at `ee6659b9` and at `4d22eeb6`, clause summary.
- `live-runs.txt` — host dump projected to the nine documented fields, the 19 sourced config entries expanded,
  which of them hold a `monitor` line, and the live run output.
- `adversarial.txt` — every adversarial config, its dump, the tool's full stdout and my expectation.
- `adversarial.py` — the driver (fixtures are synthetic; no live data is embedded).
- `isnumber-probe.txt` / `isnumber-probe.cpp` — oracle probe against the installed `libhyprutils`, with its caveat.
- `quotes.txt` / `verify-quotes.py` — every quote this report uses, at its computed `grep -n` locator, checked by a
  script (`QUOTES: 24/24 verified`, exit 0).

## 2. Live run (host, 2026-10-26)

The host dump has one output. Projected to the documented fields only (`name, width, height, refreshRate, x, y, scale,
transform, disabled, mirrorOf`): `DP-1 3440x1440 99.997 0x0 scale 1 transform 0 enabled mirrorOf none`. No serial, no
description, no make/model is written anywhere in this seat.

`~/.config/hypr/hyprland.conf` sources 19 files today (list in `live-runs.txt`); exactly one of them holds a
`monitor` line — `~/.config/hypr/monitors.conf` line 10, `monitor = DP-1, 3440x1440@100, 0x0, 1`. The tool reads that
line as rule 1 (`mode=3440x1440@100.00 pos=0x0 scale=1.0000 transform=0`) and the output as `AGREE`, `verdict=OK`,
exit 0. `|refreshRate - 100| = 0.003 < 1` (`.ufo/waves/round-45/fetch/Hyprland-macros.hpp:40`), scale 1 divides
3440x1440 exactly, transform 0 equals the rule default
(`.ufo/waves/round-45/fetch/Hyprland-MonitorRule.hpp:46` region), `mirrorOf: "none"` matches a rule without `mirror`.

Two adjacent files were run as robustness probes, clearly labelled as *not* Hyprland sources:
`~/.local/share/omarchy/config/hypr/monitors.conf` (`monitor=,preferred,auto,auto` → 1 rule, empty selector, `AGREE`,
`OK`) and `~/.config/hypr/hyprlock.conf` (hyprlock's own `monitor =` keys → the tool reads them as two Hyprland monitor
lines with an empty selector, `lines=2 rules=1`, `AGREE`, `OK`). The second is a deploy hazard, not a false verdict: the
tool cannot tell another program's file from a Hyprland config, and a lock-screen file passed by mistake yields a
confident `OK`. Nothing in the round-45 contract promises otherwise, but the entry's deploy line should keep saying
"the Hyprland-sourced files, in source order".

## 3. Adversarial configs (23) against my reading of the pins

Each case is a config + a synthetic dump; my expectation is written from the pins first, then compared with the tool.
All 23 are in `adversarial.txt` with their configs. The three forms the assignment names are F01, F02 and F04.

| case | form under test | my reading (pin) | tool |
|---|---|---|---|
| F01 | `desc:` prefix that only the **long** description satisfies | matches: `.ufo/waves/round-45/fetch/Hyprland-Monitor.cpp:1206` checks `m_description` too; aquamarine builds it `make model serial (name)` and Monitor.cpp erases commas (`aquamarine-DRM.cpp:2101`, `Monitor.cpp:252`) | `AGREE` `OK` ✓ |
| F02 | **transform modifier before the rule** | nothing is added — the copy loop at `Hyprland-legacy-ConfigManager.cpp:1309` finds no rule and returns; the later mode line keeps transform 0 | `rules=1`, `differ=transform`, `DIFFER` ✓ (a tool that applied the modifier first would print `OK`) |
| F03 | `transform, 07` after the rule | `isNumber("07")` holds, `std::stoi` gives 7, `std::clamp(TSF,0,7)` passes (`Parser.cpp:219-220`) → transform 7 | `transform=7`, `AGREE` ✓ |
| F04 | **scale needing the 1/120 search**: 3440x1440 at 1.5 | 3440/1.5 is fractional → `searchScale = round(1.5*120) = 180` (`Monitor.cpp:1001`), 180/120 fails, then i=12 up `(180+12)/120 = 1.6` divides both (`Monitor.cpp:1011`) → expected 1.6 | `AGREE` with live 1.6 ✓ |
| F04b | same rule, live still 1.5 | the corrected scale is 1.6, a live 1.5 is not | `differ=scale` ✓ |
| F05 | 1920x1080 at 1.3 | i=4 up → 160/120 = 1.3333333 (1440x810) | `AGREE` with live `1.33333` (6 significant digits from `HyprCtl.cpp:242`-region float printing) ✓ |
| F06 | same, live written 1.3 | corrected ≠ written | `differ=scale` ✓ |
| F07 | 1920x1200 at 14.166667 | no candidate in ±89 divides both → `failed to find a clean divisor` → `getDefaultScale()` (`Monitor.cpp:1033-1035`), which the dump cannot predict | `notcompared=1`, `NOT_COMPARED` exit 5 ✓ |
| F08 | second rule for the same selector | `std::erase_if(... m_name == ...)` then `emplace_back` (`MonitorRuleManager.cpp:38`) → the 3440 rule is gone, the 2560 rule survives and now precedes HDMI-A-1 | `rules=2`, order `[DP-1 2560, HDMI-A-1]`, both `AGREE` ✓ |
| F08b | empty selector fallback | after the reverse name loop, the **first** rule with an empty name (`MonitorRuleManager.cpp:96`-region) | 1 rule, `AGREE` ✓ |
| F09 | `addreserved` on an unknown selector | falls through to `add(parser.rule())` — preferred/auto/auto, transform 0; only transform and `mirrorOf` are compared | `mode=preferred pos=auto scale=auto`, `AGREE` ✓ |
| F10 | `sdr_eotf` as a legacy key | `invalid syntax` returned **before** `add` (`ConfigManager.cpp:1378`) → no rule → Hyprland's hardcoded default | `rules=0 badrules=1`, `NO_MATCHING_MONITOR` exit 3 ✓ |
| F11 / F11b | `mirror, DP-1` with live `mirrorOf` the right/other id | `mirrorOf` is the mirrored output's decimal `id` or `none` (`HyprCtl.cpp:267`) | `AGREE` / `differ=mirror` ✓ |
| F12 / F12b | rate-less rule = 60 Hz, strict test | `|61-60| < 1` is false at exactly 1; 60.999 agrees (`macros.hpp:40`, `MonitorRule.hpp:46`) | `differ=mode` / `AGREE` ✓ |
| F13 | transform modifier on the **first** of two rules | the copy is re-added, so the rule moves to the end: final order `[HDMI-A-1, DP-1]` | `n=1 HDMI-A-1`, `n=2 DP-1 transform=3`, both `AGREE` ✓ |
| F14 | scale 0.1 | `stof` 0.1 < 0.25F → error, `m_scale = 1`, rule still added (`Parser.cpp:203`) | `scale=1.0000`, `AGREE` ✓ |
| F15 | scale 0.25 | not below the floor; 3440/0.25 = 13760 and 1440/0.25 = 5760 are whole | `scale=0.2500`, `AGREE` ✓ |
| F16 | `0x0` mode | Hyprland's preferred sentinel — `m_resolution` stays (0,0), mode not compared, position is | `mode=preferred`, `AGREE` ✓ |
| F17 | `disable` against a live disabled output | `DISABLED`, not a difference | `disabled=1`, `verdict=OK` ✓ |
| F18 | `transform, 1234567890` | **measured gap, see §4a**: Hyprland keeps transform 0 and adds the rule (`OK`); the tool says `unsupported` → `NOT_COMPARED` | conservative divergence, reported not counted |

The reference selftest is also 48/48 at this rev (`mado-monitors.py --selftest` → `MADO_MONITORS_SELFTEST: 48/48 passed`).

## 4. Findings — residuals, each with what it attacks

None of these turns an `OK` into a wrong `OK`; all but (d) and (f) are cases where the tool refuses to compare
(`NOT_COMPARED`) or where the tool's model is narrower than Hyprland. They are reported because D1 asks for the
falsification attempt's residue, and because the entry's prose should not claim more than the pins support.

**(a) The INTEGER grammar is narrower than the installed `isNumber` at 10+ digits.** The tool's docstring defines an
INTEGER as `-?[0-9]{1,9}` "(hyprutils isNumber without a float part)". Measured against the installed library
(`isnumber-probe.txt`, `g++ -std=c++23 isnumber.cpp -lhyprutils`, hyprutils 0.14.2-1), `isNumber("1234567890") = 1`
and `isNumber("123456789") = 1`: there is no 9-digit cap. `isNumber("+3") = 0` and `isNumber("3.5") = 0`, so the sign and
float-part parts of the model are right. Consequence: a 10-digit `transform` VALUE is `Unsupported` in the tool
(`NOT_COMPARED`) while Hyprland's `std::stoi` + `std::clamp` path fails the parse and *still adds the rule* with
transform 0 (F18). Direction is safe (the tool under-claims), the docstring parenthetical is inaccurate.
Caveat, stated because it matters: this oracle is the **installed** hyprutils, not a pin — no Numeric/String.hpp pin of
that version exists under `.ufo/waves/*/fetch/`.

**(b) hyprlang `#@if` / `#@endif` conditionals are not modelled.** `hyprlang-config.cpp:683` skips every line while the
innermost `if` block has failed, so a gated `monitor = ...` never becomes a rule; the tool counts it. This can produce a
false `DIFFER` and, in a `disable`/rule pair, a false `DISABLED`. Not exercised on this host: no `#@` line exists in any
file the host sources (`grep -rn '#@' ... → no match`). Worth one sentence in the entry's "not modelled" list.

**(c) `##` is an escape, not a comment, and the tool's blanket `unsupported` is the safe side.** hyprlang collapses
`##` to a single literal `#` and keeps scanning (`hyprlang-config.cpp:693`, `:701`), so `monitor = ..., 1 ## note`
reaches the handler with `# note` appended and is rejected as invalid syntax — the rule is *not* added. The tool marks
any line containing `##` unsupported → `NOT_COMPARED`. The contract's counts (`unsupported`) are therefore not
Hyprland's outcome, but no verdict is wrong.

**(d) `m_isUnsafeFallback` bypasses the config entirely and is invisible in the dump.** `MonitorRuleManager.cpp`
returns a hardcoded 1920x1080 rule for an unsafe fallback output before consulting any rule. Nothing in
`hyprctl monitors all -j` exposes that flag, so a host in that state would be compared against a rule Hyprland ignores.
Unmodellable with the two declared inputs; belongs in the residuals list, not in a fix.

**(e) Mode/position/scale parse by `stoi`/`stof` prefixes in Hyprland, by strict regex in the tool.** `3440x1440@100abc`,
`0x0x5`, `1.5x` are all accepted (with prefixes truncated) or turned into an error-but-rule-added by Hyprland's parser;
the tool marks them `unsupported`. Subset grammar → conservative, no false agreement found.

**(f) The per-field whitespace trim rests on an unpinned function.** The tool strips each comma field of ASCII
whitespace. The round-45 pin set holds `hyprutils-String.cpp` with only `trim()` (isspace, both ends); `CVarList2`'s
`construct` is compiled into `libhyprutils.so` and is not in any pin, and `VarList2.hpp` only documents `allowEscape`
(default true, which is why the tool's `\` → unsupported rule is right). So "each field is stripped of ASCII whitespace"
is the round-45 author's reading, not a pin-backed fact. It matters only for values with interior padding.

**(g) Deploy hazard, no verdict error:** a non-Hyprland file with `monitor =` keys (the host's `hyprlock.conf`) is read
silently and can yield a confident `OK` (`live-runs.txt`, second probe). The tool has no way to know the file is not
sourced; the caller must pass the sourced set in source order.

**(h) Ordering is currently moot on this host.** `monitors.conf` is sourced at `hyprland.conf:16`, after the theme file at
line 13 and before `input.conf`; it is the only sourced file with a `monitor` line, so no shadowing question arises
today. `add()` erase-and-append (`MonitorRuleManager.cpp:38`) is what makes the *file order* the caller passes matter.

## 5. What the falsification did not break

- No fixture in the 81 fails under any of the five nonces; the generated 150 cases agree with the pinned reference in
  every run; the read-only marker stays absent; the selftest stays 48/48.
- The eight semantics round-45 v2 repaired are all still repaired under my own reading: `transform 07` (F03), the
  `addreserved` `stoi` fields (F09), the `0x0` preferred sentinel (F16), `modeline` (contract + selftest), CR-terminated
  lines (fixture `crlf-lines`), the `desc:` long description (F01), the clean-divisor scale search (F04/F05/F07) and a
  non-finite JSON number (fixture `nan-scale`).
- The live host is the case the entry claims: rule agreed, no difference, `OK`.

## 6. Limits of this seat

- I did not audit the entry's prose claims (that is C2's counter plus the non-author reading), nor the round-46 C1/C2
  plane, nor the session-material gate. Those belong to other seats of this wave.
- The 1/120 search was checked by brute force in double arithmetic (all 89 steps, up before down) rather than by
  running Hyprland: no compositor mutation was performed and no display state was changed.
- `hyprctl monitors all -j`, `hyprctl version` and config reads are the only compositor contacts. No `dispatch`,
  `keyword`, `reload`, `setprop`, `output`, `plugin`, `--batch`. No package transaction, no service restart, no install
  (the probe used the system `g++` and the installed `libhyprutils`; the only artefacts are under scratch, now removed).
- No git/jj mutation anywhere: the lane was read through `git show`/`git rev-parse` only; no fixture repository was
  created for this seat.
