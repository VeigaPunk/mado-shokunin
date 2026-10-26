# w1/LabFloatFormat — `%.2f` vs `std::format("{:.2f}", float)` (seat report)

Full report + receipts: `.ufo/waves/round-46/w1/LabFloatFormat/report.md`, `.../LabFloatFormat/receipts/`
(`run.txt` sha256 `cdcccdd5b46f09374f389d5a9d5aa8461763b90ff39e5e954c93fa2846690d80`, re-read by `verify.sh`).

**Verdict: NOT FALSIFIED.** 0 mismatches in 2,640,408 compared rows (2,326,323 distinct f32 patterns) and 1,325,976
end-to-end joins through the frozen reference (`mice_differ=0`, `bad_run=0`).

Sets attacked, all clean: every 3-decimal config value 0.000–100.000 via `std::stof` (100,001); every exact 2-decimal
midpoint reachable in binary, `j/8` with j odd (400 — 0.125→`0.12`, 0.375→`0.38`, 0.625→`0.62`, 0.875→`0.88`); every
midpoint `k/200` in [0,100] ±3 f32 ulp on each side plus 0.0/−0.0/−1.0 (70,003); 10^5 random f32 bit patterns and 10^5
uniform-in-range values (seeds 46), plus 10^6+10^6 supplementary (seeds 7, 2026).

Not merely equal: an independent oracle computing `Decimal(float)` rounded `ROUND_HALF_EVEN` to 0.01 agrees with both
sides on 570,649 values (`python_vs_exact=0 float_vs_exact=0`). The C++ `float` and `double` columns never differ, so
the model survives a `double`-typed optional. gcc/clang and -O0..-Os outputs are byte-identical.

Implementation identity: Hyprland imports `std::to_chars(char*, char*, float, std::chars_format, int)@GLIBCXX_3.4.29`,
defined by `/usr/lib/libstdc++.so.6.0.36` — the file behind its `libstdc++.so.6`. The tested formatter is the one that
prints the host's `scrollFactor` (`HyprCtl.cpp:770`; the argument is a `float`, per `InputManager.cpp:1380` +
`ConfigManager.cpp:1139`, passed at `HyprCtl.cpp:773`).

Impact: supports C1's string comparison at `l1-draft/mado-devices.py:395` and C2's census `json_scroll_decimals=2`.
Coverage note only: `--selftest` prints 48/48 but contains no tie value (`grep -c 125` = 0 on the reference); the
half-even rule is pinned by the fixture `mouse-round-half-even` (`quality/counters/c1-r46-fixtures.json:1553`).
By-product: −0.0 prints `-0.00` on both sides, and the reference's strictness there matches the compositor
(`hyprlang-config.cpp:467` `std::stof`, `InputManager.cpp:1380` `std::clamp`), so `config=-0, dump=-0.00` is AGREE while
`config=-0, dump=0.00` is DIFFER (`receipts/negzero.txt`).

Residuals: not exhaustive over 2^32 (the decision set is: all midpoints ±3 ulp, all ties); libstdc++ only (matches the
host); FP rounding mode and locale held at default — no `fesetround`/`setlocale` in any pin under
`.ufo/waves/round-46/fetch/`.

Planned check for the integrator: none needed for C1/C2; nothing in the claims was edited by this seat.
No tools installed. Host untouched: no hyprctl invocation, no compositor call, no package transaction.
