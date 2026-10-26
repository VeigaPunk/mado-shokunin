# ExecW2Monitors — report trailer (round-46 w1, closure D1)

**Verdict: the round-45 v2 monitor data survives the w2 falsification that never ran.** Five fresh nonces on the frozen
C1 counter, the C2 counter at the data commit and at the tip, one live host run, and 23 hand-written adversarial configs
against my own reading of the round-45 pins: no miss, no narrowing, no unsound verdict. Detailed report and every
receipt: `.ufo/waves/round-46/w1/ExecW2Monitors/` (`report.md` is the argument; `c1-nonces.txt`, `c2-entry.txt`,
`live-runs.txt`, `adversarial.txt`, `isnumber-probe.txt`, `quotes.txt` + `verify-quotes.py` are the evidence).

## Files changed

**None tracked.** This seat created only its own directory
`.ufo/waves/round-46/w1/ExecW2Monitors/` (report + receipts + the two small drivers) and this report file. No edit to
`tools/`, `corpus/`, `quality/`, the counters, the fixtures, the controls, the registration or the pins. No git or jj
mutation; the lane was read with `git show` / `git rev-parse` only.

## Behaviour measured

- `c1-r45-monitors-v2.py --repo <lane> --rev 4d22eeb66c2835af8aaa3fac6ad838fa616aa663 --work <scratch> --nonce N` for
  N = 46001..46005: **five times** `fixtures=81/81 generated=150/150 selftest=ok readonly=ok tool=present
  verdict=TARGET_MET`, exit 0 each time (`c1-nonces.txt`). The nonce axis is exactly what the round-45 w2 owed.
- `c2-r45-monitor-entry-v2.py --repo <lane> --rev {ee6659b9, 4d22eeb6}`: `admitted=1/1 verdict=TARGET_MET`, clauses
  a-j all 1, exit 0 both (`c2-entry.txt`).
- Live: `hyprctl monitors all -j | mado-monitors.py --monitors - --config ~/.config/hypr/monitors.conf` →
  `lines=1 rules=1 ... agree=1 differ=0 disabled=0 verdict=OK`, exit 0 (`live-runs.txt`). The host sources 19 files;
  exactly one holds a `monitor` line (`~/.config/hypr/monitors.conf:10`), so "every sourced conf with a monitor line"
  is one run, and it agrees.
- Adversarial: 23 configs, 22/22 match my reading of the pins, including the three named forms — a `desc:` prefix only
  the long description satisfies, a `transform` modifier written before the rule that creates it, and 3440x1440 at scale
  1.5 needing the 1/120 search to reach 1.6 (`adversarial.txt`).

## Exact retained evidence

`report.md` §1 table, §3 case-by-case table, §4 residuals. Every quote is at a computed `grep -n` locator and checked by
`verify-quotes.py` (`QUOTES: 24/24 verified`, exit 0). The host dump is projected to `name/width/height/refreshRate/x/y/
scale/transform/disabled/mirrorOf` only — no serial, no description, no make/model of the host monitor anywhere.

## Risks

1. **Conservative gaps, reported not fixed** (a fix would be round data I am not authorised to write):
   (a) the tool's INTEGER grammar caps at 9 digits while the installed `isNumber` has no cap — measured
   `isNumber("1234567890")=1`; a 10-digit `transform` VALUE becomes `NOT_COMPARED` where Hyprland keeps transform 0 and
   adds the rule. (b) hyprlang `#@if`/`#@endif` gating (`hyprlang-config.cpp:683`) is unmodelled and can produce a false
   `DIFFER`/`DISABLED`; not exercised on this host (no `#@` line in any sourced file). (c) `##` is an escape, not a
   comment; the tool's blanket `unsupported` is the safe side. (d) `m_isUnsafeFallback` bypasses the config and is
   invisible in the dump — unmodellable with the two declared inputs. (e) mode/pos/scale parse by `stoi`/`stof` prefixes
   in Hyprland vs strict regex in the tool → `NOT_COMPARED`, never a false `OK`. (f) the per-field whitespace trim rests
   on `CVarList2::construct`, which is not in any pin.
2. **Deploy hazard, no verdict error:** a non-Hyprland file carrying `monitor =` keys (the host's `hyprlock.conf`) is read
   silently and can yield a confident `OK`; the caller must pass the sourced set in source order.
3. **Oracle caveat on (a):** the probe measures the *installed* hyprutils 0.14.2, not a pin; recorded as such in
   `isnumber-probe.txt` so it cannot be mistaken for pin-backed.

## Blockers

None.

## Tooling

No install, no upgrade, no package transaction: the `isNumber` oracle used the system `g++` and the already-installed
`libhyprutils`; `isnumber-probe.cpp` and its output are in the seat directory. Scratch
`/fast/scratch/hyaku/mado-r46/ExecW2Monitors/` removed before yield; nothing outside the seat directory was written.
