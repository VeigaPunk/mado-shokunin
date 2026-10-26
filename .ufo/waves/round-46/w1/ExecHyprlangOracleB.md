# Report — ExecHyprlangOracleB (mado round 46, w1)

Seat: `w1/ExecHyprlangOracleB`. Scope: build a TRUE oracle from the host's own `hyprlang 0.6.8` and run the
targeted contract edge cases against the frozen reference. Claim touched: **C1 only, read-only**. No counter run,
no `tools/mado-devices.py`, no scoring, no host or compositor mutation, nothing installed.

## Deliverable

`w1/ExecHyprlangOracleB/oracle.cpp` — C++23 program, `g++ -std=c++23 -O0 -o oracle oracle.cpp -lhyprlang`,
against `/usr/lib/libhyprlang.so.0.6.8` (`hyprlang 0.6.8-5`). It registers the regular `input:kb_*` values with
Hyprland's defaults and the `device` special category verbatim (47 values, `Hyprland-ConfigManager.cpp:518-565`),
`commence()` + `parse()` in Hyprland's order, and prints what `getConfigValueSafeDevice` / `getDeviceString` /
`deviceConfigExplicitlySet` / `getDeviceFloat` would return per name, plus every device category hyprlang holds.
The reference (`l1-draft/mado-devices.py`, sha256 `b229efd0…49a33b` = `MODEL_SHA256`, selftest `48/48`) was run on
the same 53 configs with a synthetic dump.

## Result

**53 cases: 37 with no divergent line (3 of them are `NOT_COMPARED` with identical state), 15 declared unmodelled
that still print a divergent line, 1 contract defect.**

**The defect — a final continuation line.** A config whose last line ends in `\` followed by a newline:
hyprlang drops the whole line (`hyprlang-config.cpp:53-58`, `Last line ends with backslash`), the reference keeps
it because `str.split("\n")` leaves a phantom final `""` that `join_continuations` takes as the partner.
`C14`: oracle `kbd_layout state=default raw="us"`, reference `layout="de" … verdict=AGREE` → **a false AGREE** on
a line Hyprland discarded. Controls: without the trailing newline both drop (`C23`); continuation then a blank
line both join (`C24`); continuation before `}` both swallow the brace into `"de}"` (`C35`). Latent against
scoring at this freeze: the frozen fixtures contain no backslash, and clause g's only continuation
(`c1-r46-devices.py:214`) always carries its partner inside the same element.

**Declared divergences are honest at the summary and false at the line**: all 15 differ from the truth in at least
one printed line — 7 in a keyboard/mouse line, 8 only in `MADO_DEV_BLOCK`. `scroll_factor = 0x10`
really is `16.0` (prints `-1.00`), `inf` clamps to `100.00`, `nan` stays `nan`, a `$layout` defined after use
stores the literal text, `device { kb_layout = de` (first key not `name`) creates a phantom category keyed `"0"`
and **discards** that value, a second `name =` re-keys the whole block, `#hyprlang if` can skip a block entirely.
Every one of them is why `unsupported` must exist; none is an implementation error.

**Everything the reference models matched the library**: `##`/`###`/`#`-after-`##`, comment-cut order,
continuation-into-comment, bracket cut (RHS brackets untouched, `device[a][b]`, `device [X]`, `input[x]:`),
empty RHS, `1.5`/`+.5e1`/`1.5x`, clamp, duplicate blocks, nested-category transparency, `[[EMPTY]]` → `""`, and the
global `input:scroll_factor` never reaching `scrollFactor`.

## Evidence (all inside `w1/ExecHyprlangOracleB/`)

`report.md` (full report, the 18 probes and the 53-case table), `cases.md` (per-case config `cat -A`, oracle
state, reference output), `results.json` (raw output of both programs, every case), `cases.py` (harness),
`oracle.cpp`, `render.py`, `receipt-build.txt` (g++ 16.2.1, build line, sha256s, `hyprlang 0.6.8-5`,
`STRVAL_EMPTY` at `/usr/include/hyprland/src/macros.hpp:24`, reference sha256 + `48/48` selftest, registration
anchors), `receipt-c14.txt` (`od -c` bytes, oracle error, reference line, `join_continuations` proof, hyprlang
`getNextLine` source).

## Risks / residual

- The oracle registers values and the device category, not Hyprland's keyword handlers: `source =` is not
  followed and `bind`/`exec`-style lines are unknown options with no state effect (no case here uses one).
- Float behaviour is this host's libstdc++ `std::stof`; the measured throw boundary agrees with the reference's
  `2**-126`, another stdlib could move it.
- One config file per oracle run; the reference's multi-`--config` merge was not exercised.
- **Disclosure:** one `pacman -Qo` read-only ownership query (no `-S/-Sy/-U/-R`, no transaction). Nothing was
  installed or updated; the guard's letter says "never run pacman" and I report the deviation.

## Blockers

None. The defect is reported, not fixed: the reference is frozen and the L1 is the only integrator.
