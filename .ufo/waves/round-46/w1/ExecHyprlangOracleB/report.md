# ExecHyprlangOracleB — a true hyprlang 0.6.8 oracle against the C1 contract (round 46, w1)

Seat: `w1/ExecHyprlangOracleB`. Claim touched: **C1 only, read-only** (the contract of
`.ufo/waves/round-46/l1-draft/mado-devices.py`). No file outside this seat was written; no counter was run;
`tools/mado-devices.py` does not exist yet, so nothing was scored.

## Verdict in one paragraph

A C++ oracle that registers exactly what Hyprland 0.56.2 registers and parses with the host's own
`libhyprlang.so.0.6.8` was run over **53 targeted configs**. **37 cases show no divergent line** (34 compared outright plus 3 the
reference declines to compare with identical state), **15 are declared unmodelled** by the contract
(`unsupported > 0` → `NOT_COMPARED`) yet still print a divergent line, and **1 is a genuine contract defect**: a config whose **last line ends in a backslash followed by a newline** — Hyprland drops the
whole line (`hyprlang-config.cpp:53-58`), the reference keeps it, so the tool prints **`verdict=AGREE` on a line
Hyprland discarded** (receipt `receipt-c14.txt`). Of those 15, 7 print a false keyboard/mouse line (e.g. `scroll_factor=-1.00` when hyprlang stores `16.0`) and 8 a
false `MADO_DEV_BLOCK` list (phantom `"0"` blocks, split blocks, creation order). The umbrella is honest; the lines
are not. Each verdict line below is backed by `results.json` (both programs' full output for
every case) and `cases.md` (config + oracle state + reference output per case).

## What the oracle is

`oracle.cpp` (sha256 `b89304eda9bd2d7ec8da1be028fd07bf1527c820cb7b1cc638deae0eea99d4b7`), built
`g++ -std=c++23 -O0 -o oracle oracle.cpp -lhyprlang` with g++ 16.2.1, linked against
`/usr/lib/libhyprlang.so.0.6.8` (owned by `hyprlang 0.6.8-5`). It

- registers the regular values `input:kb_model ... input:kb_file` with Hyprland's defaults
  (`Hyprland-ConfigValues.cpp:271-276`), `input:scroll_factor` (`:296`), `input:touchpad:scroll_factor` (`:324`)
  and a few neighbours a config line may touch (`input:repeat_rate`, `input:follow_mouse`, ...);
- registers the special category verbatim: `addSpecialCategory("device", {"name"})` and the **47** `addSpecialConfigValue`
  lines of `Hyprland-ConfigManager.cpp:518-565` (counted 47, matching the frozen census `device_keys=47`);
- constructs `CConfig(path, {.throwAllErrors = true, .allowMissingConfig = true})`, calls `commence()` then
  `parse()` — the same order as `Hyprland-ConfigManager.cpp:628` then `:743`;
- prints, per queried name, what Hyprland would *see*: `getConfigValueSafeDevice` (`:1115-1123`),
  `getDeviceString` with the `STRVAL_EMPTY` projection (`:1156-1167`, sentinel confirmed as `"[[EMPTY]]"` at
  `/usr/include/hyprland/src/macros.hpp:24`), `deviceConfigExplicitlySet` (`:1125-1129`), `getDeviceFloat`
  (`:1139-1145`), plus every device category hyprlang holds (`listKeysForSpecialCategory`, `specialCategoryExistsForKey`)
  and each category's set-by-user key set.

The oracle never models the parser: it *is* the parser. Only the query projection is re-implemented, and every
line of it is a copy of the pinned function it names.

## Method

Synthetic dump (`devices.json`, built by `cases.py`): keyboards `kbdX` (`de`), `kbdY` (`fr`),
`hl-virtual-keyboard-1`; mice `mouseA` (`scrollFactor 1.00`), `touchpadB` (`-1.00`). No host data, no serials.
Per case: `./oracle case.conf kbdX kbdY kbdY2 'kbd$X' 0 '' mouseA hl-virtual-keyboard-1` and
`python3 -I …/l1-draft/mado-devices.py --devices devices.json --config case.conf` (that file's sha256
`b229efd0…49a33b` equals `MODEL_SHA256` at `quality/counters/c1-r46-devices.py:68`; its own selftest prints
`48/48 passed`). Comparison: the five XKB names per keyboard, `kb_file`, the mouse `scroll_factor` (clamp when
`explicit=1`, else `-1`), and the created-block name list. `cases.md` holds every config (`cat -A`), the oracle's
state and the reference's output; `cases.py` regenerates both.

## The one defect: a final continuation line (C14)

Config (`od -c` in `receipt-c14.txt`), the last byte pair is `\` and `\n`:

```
device {
    name = kbdX
    kb_layout = de \
```

- **hyprlang 0.6.8**: `getNextLine` sees the trailing backslash, `std::getline` for the partner returns EOF →
  `GETNEXTLINEFAILURE_BACKSLASH`, the assembled line is **dropped**; `parse()` reports
  `Last line ends with backslash` and `Unclosed category at EOF`. `kb_layout` stays at its default:
  `ORACLE_FIELD: name="kbdX" field=kb_layout state=default raw="us"`.
- **Reference**: `join_continuations("…de \\\n".split("\n"))` → `["device {", "    name = kbdX", "    kb_layout = de"]`
  — the phantom final `""` element of `str.split` is taken as the partner line. State
  `{'kbdX': {'kb_layout': 'de'}}`, `unsupported=0`, and with `de` in the dump it prints
  `MADO_DEV_KEYBOARD: name="kbdX" … layout="de" … verdict=AGREE`.
- **Consequence**: a **false AGREE**. Hyprland runs `us` (the line never applied) while the tool says the keyboard
  agrees with `de`. This is the optimistic direction — the one that hides a fault.
- **Controls that separate it**: `C23` (same file, no trailing newline) → both drop, match. `C24` (continuation
  followed by a blank line) → both join with the blank line and keep `de`, match. `C35` (`kb_layout = de \` then
  `}`) → both swallow the brace into the value `"de}"` and never close the block, match. So the divergence is
  exactly "the backslash line is the last line and the file ends with a newline".
- **Blast radius at this freeze**: I read the frozen fixtures — `quality/counters/c1-r46-fixtures.json`
  (sha256 `027ed508…8e3fc1`) holds **no backslash at all**, and the clause-g generator's only continuation
  (`quality/counters/c1-r46-devices.py:214`, `"input:kb_layout = br,\\\nus"`) always carries its partner inside
  the same element, so **no pinned or generated case reaches this branch today**. The defect is latent against
  C1's scoring and live against the contract.
- Not mine to fix (L1 is the only integrator); the smallest description of a fix: drop a trailing phantom split
  element before `join_continuations`, i.e. treat "the backslash line is the final raw line" as dropped, exactly
  as the docstring's "a final such line is dropped" already says.

## The 18 assigned probes

| probe | oracle (hyprlang 0.6.8) | reference | support | case |
| --- | --- | --- | --- | --- |
| `device {` whose first key is not `name` | error `special category's first value must be the key` (`hyprlang-config.cpp:435`); a category keyed **`"0"`** is created, the first key's value is **not applied**; a later `name =` rewrites the name field, so later keys land under that name | unmodelled (2×) | declared | `C01`, `C29`, `C30` |
| second `name =` in a block | one category whose name field becomes the **last** value; earlier keys travel with it (`getSpecialConfigValuePtr` matches on `values[key]`, `:1083-1099`), so `kb_layout` set before the rename is now reached via the new name | unmodelled | declared | `C02`, `E01` |
| `device[X]:name = Y` | bracket path sets `currentSpecialKey=X` (`:296-297`) but the block's key becomes `Y`; a following `device[X]:…` creates a **second** block keyed `X` (`:291-331` matches an existing category by its stored key at `:310`) | unmodelled; block creation order differs too | declared | `C03` |
| `device:kb_layout` outside a block | error + a phantom category keyed `"0"`; value not applied | unmodelled | declared | `C04` |
| block closed, then flat `device:…` | the flat key does **not** reach the closed block (`currentSpecialKey` reset, `:896`); a second phantom `"0"` appears | unmodelled | declared | `C05` |
| `device [X]` with a space | the line has no `=`, so it is rejected as `Invalid config line` (`:713-715`) before any bracket logic — brackets are read only from a key line's LHS; with `=`, the cut leaves `"device :kb_layout"`, matches nothing, no effect | identical (ignored, not even counted) | **match** | `C06`, `C32`, `C33` |
| brackets in a value | RHS is never bracket-processed: `kb_layout = de[foo]` stores `de[foo]`; two LHS groups `device[a][b]` name the block `a][b` | identical | **match** | `C07`, `C31` |
| `input[x]:kb_layout = de` | the bracket name is cut and discarded, the **global** is set | identical | **match** | `C08` |
| `device` block nested in another category | `misc:device:name` is no device (error, no state) | identical | **match** | `C09` |
| `##` at line end | one literal `#`: `de #` | identical | **match** | `C10` |
| `###` | `de ##` (same pair/resume arithmetic as `:686-703`) | identical | **match** | `C11` |
| `#` in a value after `##` | `a##b#c` → `a#b`; `de##x#y` → `de#x` | identical | **match** | `C12`, `C25` |
| continuation into a comment | joined line, then cut at `#`: `de` | identical | **match** | `C13` |
| final continuation line | **line dropped** (`:53-58`) | line kept | **DEFECT** | `C14` |
| `kb_layout =` (empty) | sets `""`, `m_bSetByUser=1`; expected `""` | identical | **match** | `C15` |
| `scroll_factor = 1e-40` | `std::stof` **throws** (libstdc++ ERANGE on underflow) → key unset → `-1` | unmodelled, and prints `-1.00` (state correct) | declared, state right | `C16` |
| `scroll_factor = 0x10` | `std::stof` accepts hex → stored **16.0**, clamp 16, `hyprctl` would print `16.00` | unmodelled, prints `-1.00` | declared, **state wrong** | `C17` |
| `scroll_factor =  1.5` / `+.5e1` | `1.5` / `5` | identical | **match** | `C18`, `C19` |
| `scroll_factor = 1e39` | `std::stof` throws out_of_range → unset → `-1` | unmodelled, prints `-1.00` | declared, state right | `C20` |
| variable defined after use | the literal `$layout` **is stored** (no re-parse; `parseVariable` only replays in dynamic mode) | unmodelled, prints `us` | declared, **state wrong** | `C21` |
| `$` inside a device name | literal block `kbd$X` exists | unmodelled, block absent | declared, **state wrong** | `C22` |

Extras that also matter: `inf`/`nan` are accepted by `std::stof` and stored (clamp → `100`, `nan`) while the
reference prints `-1.00` (`C26`, `C27`); the `[[EMPTY]]` sentinel maps to `""` exactly as the contract says
(`E13`); the global `input:scroll_factor` **never** reaches `scrollFactor` (`E05`: `explicit=0`, resolved `2`,
printed `-1.00`); clamp to `0..100` (`E06`: `200` → `100.00`); duplicate blocks collapse to one category with
the last value (`E04`); `#hyprlang if $undef` **skips the whole block** so no device exists (`E03`), exactly why
`unsupported` must stay; a bare `#hyprlang` is *not* a directive yet is counted (`E02`: precision cost only, never
wrong); CRLF, stray `}`, unclosed block, empty `name`, one-line braces, close-with-comment, and a nested block
followed by a device key all match (`E11`, `E14`, `E15`, `E16`, `E10`, `E12`, `E09`). `E17` confirms the
documented counting difference only: hyprlang stores `sensitivity`, the reference's `keys=` counts the 7 modelled
keys — contract-conformant ("keys counts the DEVICE KEYS the block set"), no verdict effect.

## Declared divergences where the reference's printed line is false

`NOT_COMPARED` protects the summary, not the lines. These print a per-device value that the real parser
contradicts: `C17` (`-1.00` vs `16.00`), `C26` (`-1.00` vs `100.00`), `C27` (`-1.00` vs `nan`), `C21`
(`layout="us"` vs the literal `$layout`), `E03` (models a block hyprlang skipped), `C02`/`C29` (a block's expected
names after a re-name / a discarded first key), and the `MADO_DEV_BLOCK` lists of `C01`, `C03`, `C04`, `C05`,
`C06`, `C22`, `C30`, `E01` (phantom `"0"` blocks, split blocks, creation order). All are inside the declared
`unsupported` model, so this is a **contract precision** observation for the L1, not an implementation divergence.

## Answers to the contract's sharper questions

- `device[X]` bracket names, `device:name` flat keys, a second `name`, `$`, `{{`, `\`, hex/inf/nan floats and
  `#hyprlang` directives are the **only** constructs where hyprlang does something the reference refuses to model —
  and in every one of them the refusal is the right call: each of `C02/C03/C04/C05/C06/C29/C30/E03` changes a
  device's effective keys in a way no line-local model captures.
- No construct was found where the reference *models* a line and gets it wrong **except** the final continuation
  (`C14`). All the modelled comment, continuation, bracket, empty-RHS, float-prefix, clamp, global-fallback,
  duplicate-block and nesting behaviour matched the library bit for bit.

## Limits and what I did not verify

- The oracle registers Hyprland's config **values** and the `device` category, not its keyword handlers
  (`source`, `exec`, `bind`, ...): such a line becomes an unknown-option error with no state effect, and
  `source =` is **not** followed. No case here uses one; the reference declares the same limit for `source`.
  The generator does emit `bind = …` / `$mod = …` (`c1-r46-devices.py:216`) — those only exercise the reference's
  own ignoring, which I did not re-check because Hyprland would route them to handlers my oracle omits.
- One config file per oracle run; the reference's multi-`--config` merge was not exercised.
- Float behaviour is this host's libstdc++ `std::stof` (g++ 16.2.1). The reference's `2**-126` threshold matches
  the throw/no-throw boundary I measured (`1e-40` and `1e39` throw, `1.5`/`+.5e1` do not), but another stdlib
  could move it.
- The oracle prints the **config side**; the join/verdict remains the reference's, which I recomputed by hand from
  the oracle's field lines.
- No counter run, no `tools/mado-devices.py`, no C1/C2 score: the wave has no tool yet, and scoring is the L1's.
- Host safety: reads only (`/usr/include/hyprland` header grep, `readlink`, `sha256sum`). No compositor call, no
  input injection, no Wayland client, no config write, no git/jj mutation anywhere. **Disclosure:** I ran
  `pacman -Qo /usr/lib/libhyprlang.so.0.6.8` (a read-only ownership query — no `-S/-Sy/-U/-R`, no sync, no
  transaction, no install); the same fact was available from `readlink`. Nothing was installed or updated.

## Files

`report.md` (this), `cases.md` (all 53 configs + oracle state + reference output), `results.json` (raw output of
both programs per case), `cases.py` (harness), `oracle.cpp` (the oracle), `render.py` (cases.md renderer),
`receipt-build.txt` (compiler, build line, hashes, library, reference sha256 + selftest, registration anchors),
`receipt-c14.txt` (the defect, reproduced end to end).
