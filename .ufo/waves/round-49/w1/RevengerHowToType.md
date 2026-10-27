# RevengerHowToType — scoped findings (mado round 49, w1, BUILD)

Target: intent and history of `how-to-type` and `xkb_keymap_key_get_mods_for_level`
upstream. Full report with every locator: `.ufo/waves/round-49/w1/RevengerHowToType/report.md`
(+ `verify-quotes.sh`, 29 checks / 0 failures, and the pinned sources + receipts in that dir).

Supports: **C1** (the `mado-keysym.py` contract and the judge's expectations). Nothing here
touches C2's Hyprland entry.

## Verdict

1. `how-to-type` is a *demo for an API*, not a UI: `188a1c7` (2020-03-20) says the program
   "was written to exercise the new `xkb_keymap_key_get_mods_for_level()` function"; the API
   itself (`d92a248`, 2020-02-05) exists to "invert the keycode->keysym transformation" for
   auto-type/desktop automation. Its output format is whatever was readable at the time.
2. The output is three independent decisions: **the mask set** (API), **the mask→name
   expansion** (tool), **the canonical keysym name** (library). Only the third moved inside
   1.11.0→1.13.2 for `--keymap FILE --disable-compose --keysym ARG`.
3. **The pin matters at three boundaries**
   - `< 1.11.0`: no `--keymap`, no `--disable-compose`, no `=== Direct access ===` (1.10.0 is
     316 lines and has neither option).
   - `1.11.0`: keymap **format v2 became the default *input* format** for all tools
     (`44c8deb`; `src/keymap-formats.h:13-14`) and the tool was rewritten (compose on by
     default, `--keymap`, `=== Direct access ===`, mask test via `mod_get_mask2`).
   - `1.13.1 → 1.13.2`: canonical name of keysym `0xff7e` changes
     `Mode_switch` → `ISO_Group_Shift` (`60d0e5f8`, 2026-05-30), new keysym names are added,
     and three xkbcomp parse fixes land. 1.13.2 is a real behavioural step, not a patch.

## Facts the frozen counter must encode (all observed on the pinned binary)

- Header line: `keysym: <name> (<value>)` with `%#06x` — four hex digits below `0x10000`
  (`0x002f`), wider above (`0x10001e9`). Blank line, `=== Direct access ===`, blank line.
- Column widths 8/9/8/20/7/rest; `LAYOUT` prints `layout+1`, `LEVEL#` prints `level+1`.
- One row per mask from `xkb_keymap_key_get_mods_for_level`, in keycode → layout → level →
  type-entry order. No sorting, no de-duplication, **no Lock filtering** (a `Lock` row appears
  whenever the key type maps a Lock-bearing mask; `preserve` does not remove it from the mask).
- Modifier names are printed for every modifier whose **encoding** is contained in the mask,
  in modifier-index order — so one bit can print two names (`[ Mod5 LevelThree ]`, and
  `[ Shift Lock Mod5 LevelThree ]` ordering).
- `get_name` has three tiers: explicit table → `U%04X` (Unicode keysyms ≥ `0x01000100`) →
  `0x%08x` (unnamed). `0x00E9` → `eacute`, `0x10001E9` → `U01E9`, `0x10000E9` → `0x010000e9`.
- ARG grammar under `--keysym`: explicit name (case-sensitive), `0x…` hex, or decimal.
  **`U+002F` is rejected, rc 2** — `U+` belongs to codepoint parsing, which `--keysym` skips.
- Refusal: rc **2** with usage on **stderr** (`EXIT_INVALID_USAGE` = 2, `meson.build:166`;
  `7141820`, 2020-07-09).

## Keysym header: sufficient or not?

- **Sufficient** for explicit names and for canonical choice: the header documents the rule
  ("the first one listed is considered the 'canonical' name", line 105) and upstream generates
  its table with exactly `if value not in canonical_names: canonical_names[value] = name`
  (`scripts/update-keysyms-derived-headers.py:47-48`). Deprecation is likewise header-encoded
  (lines 116-136).
- **Not sufficient** for the whole function: the `U%04X` and `0x%08x` tiers are computed, and
  the 2638 defines cover 2505 values with 120 multi-name values (9 names for `0xff7e`), so the
  tool must apply first-wins ordering, not "pick any define for the value".
- Practical consequence for C1: embed a table generated from the pinned header (2638 names) +
  the two computed tiers; a sandbox that exposes the header at run time is optional, not
  required.

## What changed 1.11.0 → 1.13.2 (contract-relevant)

| release | change | affects the contract? |
|---|---|---|
| 1.11.0 | `--keymap`, `--disable-compose`, `=== Direct access ===`, `--verbose`, keysym-parse fixes (`errno`), mask test via `mod_get_mask2`, format v2 default input | **establishes** the contract's shape |
| 1.12.0 | keysym data update (new names, `XF86BrightnessAuto` deprecated), keycodes parse up to `0xfffffffe`, serialization API break (tools keep `PRETTY│KEEP_UNUSED`) | names accepted by `--keysym`; fixtures still pretty |
| 1.13.0 | compose lookup fix `52fe698` | **no** (compose disabled) |
| 1.13.2 | canonical `0xff7e` flip, new keysyms, xkbcomp type/interpret parse fixes, hash perf | **yes** (header name; accepted names; malformed-type handling) |
| 1.14.x | usage prints `v1`/`v2` labels, `--version` | out of pin; a pin bump changes the usage text |

Tool source on the reachable path is **identical** from 1.11.0 to 1.13.2 except
`lookup_compose_sequences()` (10 insertions / 2 deletions, the `52fe698` UTF-8 fallback);
`src/keysym.c` has **no** commits in that range; `src/keymap.c` changes there are confined to
constructors, `get_as_string*`, `key_by_name` — not to `get_mods_for_level`, `key_get_name`,
`num_levels_for_key` or `key_get_syms_by_level`.

## Receipts worth reading first (in `.ufo/waves/round-49/w1/RevengerHowToType/`)

`receipt-0xff7e-name.txt` (pinned binary prints `ISO_Group_Shift` for `--keysym 0xff7e`),
`receipt-canonical-name-decode.txt` (per-tag `keysym_to_name` offsets: 19891 `Mode_switch`
through 1.13.1, 17760 `ISO_Group_Shift` at 1.13.2), `receipt-arg-forms.txt` (`U+` rejected),
`receipt-keysym-names.txt` (Lock rows + the three name tiers), `receipt-modmaps.txt`
(`LevelThree` = `0x80` = `Mod5`), `receipt-v1-v2-bytes.txt` (`--output-format v1` == `v2` ==
default, byte for byte), `receipt-keymap-sample.txt` (`FOUR_LEVEL_SEMIALPHABETIC` map/preserve),
`receipt-verify-quotes.txt`.

## Not established

- The 1.13.1 (and older) *binary* output was never run — building that release was out of
  scope. The old name is established from the decoded table plus the commit's own test/fixture
  diffs, and is marked `[INFERENCE]` in the report.
- Compose semantics (out of contract when `--disable-compose` is used).

## Host hygiene

All probes ran with `env -i`, `HOME`/`XDG_CONFIG_HOME` in seat scratch
(`/fast/scratch/hyaku/mado-r49/RevengerHowToType`), read-only xkbcli subcommands only
(`compile-keymap`, `how-to-type`), no compositor call at all, no package transaction, no
network write. Scratch dir removed at exit; nothing written outside this seat directory and
the sibling `.md` report.
