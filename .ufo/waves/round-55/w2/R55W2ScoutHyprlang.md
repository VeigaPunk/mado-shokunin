# R55W2ScoutHyprlang — report (round 55, w2, falsify; read-only research; RE-ISSUE of the w1 item)

Deliverable: `.ufo/waves/round-55/w2/R55W2ScoutHyprlang/hyprlang-check.md` (full evidence, row-by-row table, receipts in `receipts/`).

## What I attacked

The C2 source claims of `tools/mado-kbdopts.py` and of `registration.md` §C2 (v1), plus the errata `registration-v2.md` E7:
`configStringToInt` prefix handling; `isNumber` on `+5`, `007`, `-3`, `3.5`, `0x10`; Hyprland enforcement of `.min`/`.max`
for INT options; the special-category merge of repeated device blocks; the "first value must be the key" rule; and every
place the docstring/registration contradicts or goes beyond the source.

## What ran (exact)

- `curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/<path>` — `README.md`, `CMakeLists.txt`, `src/config.cpp`, `src/common.cpp`, `include/hyprlang.hpp`, `src/config.hpp`, `src/public.hpp` (note: the tag's layout is lowercase `src/`, not `src/Config.cpp`).
- `curl -fsSL https://raw.githubusercontent.com/hyprwm/hyprutils/v0.7.1/<path>` — `src/string/String.cpp`, `include/hyprutils/string/String.hpp`, `src/string/VarList.cpp`, `CMakeLists.txt`.
- `curl -fsSL https://raw.githubusercontent.com/hyprwm/Hyprland/efb50993780079460b0cbed1363e2166a2de1d9f/<path>` — `src/config/values/ConfigValues.{cpp,hpp}`, `types/IValue.hpp`, `types/IntValue.{hpp,cpp}`, `ConfigValue.hpp`, `ConfigManager.cpp`, `src/config/values/types/*`.
- Full-tree search: `curl -fsSL https://codeload.github.com/hyprwm/Hyprland/tar.gz/efb50993…` (50.8 MB, read-only download of the same pinned commit; not a `raw.githubusercontent.com` URL, disclosed) and `grep -rn 'm_min\|m_max' src/…`.
- `g++ -std=c++23 -O0` — the exact fetched `configStringToInt` body with the HU0.7.1 `trim`/`isNumber` (token table, 37 tokens); the full fetched hyprlang v0.6.8 `config.cpp`/`common.cpp` compiled with `-lhyprutils` against the host `libhyprutils` 0.14.2 and run as drivers (`driver`: t1–t6; `driver2`: s1–s6).
- `g++` host check of `isNumber` against `libhyprutils.so.13` (= 0.14.2) on 10 tokens.
- `python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-kbdopts.py --config <scratch case> --keyboard k1 --keyboard k2 --keyboard kbd` on each probe case (read-only; the lane tool was not modified or written; `--selftest` → `MADO_KBDOPT_SELFTEST: 83/83 assertions passed`).
- `grep -rnE '\{ *#|\} *#|#hyprlang' fixtures/c2 fixtures/c2-holdout` → empty (no committed or hold-out fixture covers the two silent findings). The same grep on `~/.config/hypr/input.conf` → empty.
- Host reads only: `hyprctl version`; `hyprctl getoption input:repeat_rate -j`, `input:repeat_delay -j`, `input:numlock_by_default -j` (→ 40, 250, 1); `~/.config/hypr/input.conf` (read). No `hyprctl keyword/dispatch/reload`.
- Pacman: not used (paused host-wide). No installs or upgrades were performed.

## What did not run

- The Hyprland 0.56.2 binary was not built or run; the numlock consumer of `m_numlockOn` and the keyboard repeat effect are [INFERENCE] from the pinned lines.
- The installed `libhyprlang.so.0.6.8` was not executed; the v0.6.8 tag source was compiled against host hyprutils 0.14.2 (the same `isNumber` symbol the installed library imports, per `nm -D`).
- The Lua path (`LuaConfigInt.cpp`) was read, not run.
- `source` inclusion (sourced file) was not executed; it is read from the pin (`legacy/ConfigManager.cpp:614`, `:1802`).
- The frozen counters, the C2 harness, and the sentence-to-pin audit were not run (not my item).

## Verdicts (per target)

| target | verdict | evidence |
|---|---|---|
| `configStringToInt` boolean prefixes (true/on/yes→1; false/off/no→0), checked first, case-sensitive | **SURVIVES** | `hyprlang-check.md` §1.1; `src/config.cpp:259,261`; `receipts/token-table.txt`, `receipts/driver-out.txt` |
| `configStringToInt` hex: docstring says hex → `unsupported` | **BROKEN** (`0x10` → 16; `0X10` → error) | §1.1; `src/config.cpp:195-197`; `receipts/token-table.txt` |
| `isNumber` on `+5` / `007` / `-3` / `3.5` / `0x10` | `+5`, `3.5` rejected (SURVIVES); `007`→7 (SURVIVES); **`-3` accepted** (BROKEN vs "sign → unsupported"); `0x10` does not reach isNumber | §1.2; `hyprutils String.cpp:25,34,39,58`; `receipts/isnum-host.txt` |
| Hyprland enforcement of `.min`/`.max` for INT options | **NOT ENFORCED on the `.conf` path**; only `LuaConfigInt.cpp:52-56` compares. The docstring's "outside → unsupported" is a tool choice with a wrong basis. Enforcing site for `.conf`: none found | §1.3; `receipts/driver-out.txt` t3, `receipts/driver2-out.txt` s5 |
| special-category merge for repeated device blocks | **SURVIVES**: same-name blocks merge; a later write of the same key wins (observed) | §1.4; `src/config.cpp:368,376,438`; `receipts/driver-out.txt` t1, `receipts/driver2-out.txt` s1 |
| "first value must be the key" | **SURVIVES** as a config error (`src/config.cpp:434-435`, observed); not stated in the registration; the tool counts instead | §1.5; `receipts/driver-out.txt` t2 |
| Silent wrong value: inline comment on a block line (`input { # main`, `} # end`) | **BROKEN** (silent, `unsupported=0`): tool k1 `repeat_delay=400 from=D`, k2 `repeat_rate=25 from=-`; hyprlang 30 (G) and device delay unset | §3 A-t5; `receipts/cases/t5.conf`, `receipts/tool-probe-out.txt`, `receipts/driver-out.txt` |
| Silent wrong value: `#hyprlang if NOPE` conditional | **BROKEN** (silent, `unsupported=0`): tool `repeat_rate=60 from=G`; hyprlang 25 (line skipped) | §3 A-s3; `receipts/cases/s3.conf`, `receipts/driver2-out.txt` s3 |
| `source = …` ignored by the tool | **CONTRADICTS** the source (Hyprland registers and reads `source`, `legacy/ConfigManager.cpp:614,1802`); effect not run | `hyprlang-check.md` §2 row 6 |
| numlock 0..1 attributed to `ConfigValues.cpp:277` (v1) | **CONTRADICTS** (line 277 is `MS<Bool>` with no range); v2 E7 already retracts it | §2 row 4 |
| `$V` variable expansion, `##` escape, `rgba()` | **flagged** by the tool (`unsupported ≥1`) — not silent — but the docstring's cited rules are wrong: `on##`→1, `$V`→40, `rgba(…)`→4278850590 | §2 rows 9, 10, 16; `receipts/driver2-out.txt` s4, s6; `receipts/driver-out.txt` t6 |
| `name = kbd#1` → device `kbd` | **SURVIVES** | §2 row 13; `receipts/driver2-out.txt` s2 |
| `std::max(0, …)` clamp "a no-op on the modelled range" | **SURVIVES** in range; for `-3` the effective rate is 0, not "unsupported" [INFERENCE on the stored effective value] | §1.6; `Hyprland-InputManager.cpp:1282-1283` (pin) |
| `getDeviceInt` device-over-global rule | **SURVIVES** | `legacy/ConfigManager.cpp:1119` (pin); `(set)`/`(unset)` in receipts |

## Tool-vs-source contradictions the frozen text carries (summary)

The full table (17 rows) is in `hyprlang-check.md` §2. The ones that matter for the frozen claims:
1. hex and sign tokens: text says `unsupported`; hyprlang accepts `0x10` (16) and `-digits`.
2. ranges: text says `.min/.max` of ConfigValues.cpp:277-280 are the range source; the `.conf` path does not enforce them.
3. inline `{ #` / `} #` and `#hyprlang if` directives are outside the modelled grammar but are not counted as `unsupported` — **silent wrong values** (§3).
4. `source` is ignored silently; Hyprland reads it.
5. the device-key-before-name case is a hyprlang config error, not a count.

## Unverified / limits

- Effects in Hyprland (numlock consumer, keyboard repeat) are inferred from pinned lines, not executed.
- The installed binary was not run; the source was compiled against host hyprutils 0.14.2 (the isNumber symbol is the same one the installed library imports).
- Fixture coverage statements are from a `grep`, not a harness run.
- I did not alter any tracked file; no `git`/`jj` command was run; no commit, no push, no subagent, no background job. The only lane writes are the deliverable directory `w2/R55W2ScoutHyprlang/` and this report.
- Scratch was under `/fast/scratch/hyaku/mado-r55/R55W2ScoutHyprlang/` and is removed before yield. Receipts were copied first into `w2/R55W2ScoutHyprlang/receipts/`.
