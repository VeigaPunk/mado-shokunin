# ExecSkillRows — round-50 w1: every command in the candidate SKILL section, run; every row checked

Seat: `ExecSkillRows` (round-49 w2 item, never dispatched; retargeted by the round-49 closure D1 to the candidate section
`.ufo/waves/round-49/w1/ScrSkill/skill-section.md`). Lane base `8ae47b957034ae21012bbf09173cca2c48be345e`.

Scope: run every command the section gives (read-only; `HOME`, `XDG_*` under `/fast/scratch/hyaku/mado-r50/ExecSkillRows`,
removed at exit) and check each decision-table row against its cited locator or receipt. No lane file edited; no compositor
write; no input injected; `pacman` untouched. libxkbcommon 1.13.2 (`xkbcli --version` → `1.13.2`), how-to-type
sha256 `f6c0b122…7e54`, compile-keymap `43b924f6…7250` — both equal to the round-49 receipt's binaries.

## Verdict

**15 of 17 rows verified; 2 rows carry a defective first read (one root cause), and the command block has one invocation-form
mismatch.** (9 rows in the decision table + 8 error-pattern rows; the two failures are decision-row 7 and error-row 1.) Every source locator (59 citations) and every host figure holds. The section's own diagnostic for “does this name
resolve” reports `NoSymbol` for **53 of the host's 142 keysym-named binds** — including the live `SLASH` bind — while the same
row's rule says those names work.

## What I ran (all as written in the section)

| section command | rc | result |
|---|---|---|
| `/usr/lib/xkbcommon/xkbcli-compile-keymap --layout br --options compose:caps > FILE` | 0 | 73079 B, sha256 `efd487a3…cf6fce81` = round-49 receipt copy **and** `.ufo/waves/round-48/receipts/xkbcli-compile-keymap-r48.txt:59` |
| `/usr/lib/xkbcommon/xkbcli-how-to-type --keymap=FILE --disable-compose --keysym ARG` | 0/2 | ARG matrix: `slash`/`0x2f`/`U002F`/`47` → `keysym: slash (0x002f)`; `XKB_KEY_a`/`U+002F`/`0X2F`/`nosuchsym` → rc 2 `ERROR: Failed to convert argument to keysym`; `Return` → `RTRN` level 1; `slash` rows = AD01 levels 3/4 under `Mod5 LevelThree` **and** AB11 level 1 `[ ]`; `Caps_Lock` rc 0 with an empty table; `Multi_key` keycode 66 |
| `python3 tools/mado-keysym.py how-to-type --keymap FILE …` | 0/2 | 38/38 selftest; **39/39 stdout+rc equal to the judge** on the `--keymap=FILE` form |
| `--keysym` without `--disable-compose`, and without `--keysym` | 2/2 | tool refuses both, message `ERROR: --disable-compose and --keysym are required` |
| degenerate: no `--keysym` `0x100`; compose on `dead_acute` | 0 | `Amacron (0x03c0)`; compose header appears (1 line) — both as the section states |
| row-4 fallback command: compile with no names, then how-to-type | 0 | `71249 B`; `slash` → `61 AB10 English (US) 1 [ ]` vs the configured keymap's `97 AB11 Portuguese (Brazil) 1 [ ]` — the command separates the two keymaps |
| row-4 first read: `--layout zz` | 1 | 0 B stdout, `[XKB-338] Couldn't find file "symbols/zz" in include paths` — as the matrix says |
| `hyprctl binds -j`, `hyprctl devices -j`, `hyprctl getoption input:{resolve_binds_by_sym,kb_layout,kb_options,kb_file} -j` | 0 | 192 binds; `{"int": 0, "set": false}`; `br`; `compose:caps`; `[[EMPTY]]`; 10 keyboards, all layout `br` |

Host figures recomputed and **equal to the section**: 192 binds = 142 keysym-named + 42 empty-`key`-with-keycode + 2 `mouse:N`
+ 4 `mouse_*` + 2 `switch:`; all 192 submaps `""`; modmask 64/65/68 top three (42/37/26); `SLASH` = 1 row, modmask 65;
42 keycode binds all non-zero, range 10..201 (`receipts/binds-tally-r50.md`).

## Findings

### F1 (row 7 “does the name resolve at all?” and error-row 1) — the first read contradicts the rule it states

The rows tell the reader to run `mado-keysym.py … --keysym NAME` and read **rc 2 as NoSymbol**, with the next step “fix the
spelling”. The rule in the same row says Hyprland resolves **exact, then case-insensitive** (`KeybindManager.cpp:710-711`)
and accepts either (`:724`), “which is why `SLASH` and `slash` both work”. The judge — and therefore the tool — resolves with
`XKB_KEYSYM_NO_FLAGS` only (`how-to-type.c:286`), so it is case-**sensitive**.

Measured (libxkbcommon 1.13.2, `xkb_keysym_from_name` with `0` vs `XKB_KEYSYM_CASE_INSENSITIVE` over the 58 distinct keysym
names in the live bind table, `receipts/case-sensitivity.md`):

- 14 of 58 distinct names resolve **only** through the case-insensitive path: `BACKSPACE COMMA DELETE DOWN ESCAPE LEFT
  PERIOD PRINT RETURN RIGHT SLASH SPACE TAB UP`; none of the 58 fails both.
- Those 14 names carry **53 of the 142** keysym-named bind rows (`TAB` 11, `LEFT`/`RIGHT`/`COMMA`/`SPACE` 5 each, `UP`/`DOWN`/
  `PRINT` 4 each, `RETURN`/`BACKSPACE` 3 each, `DELETE`/`ESCAPE`/`PERIOD`/`SLASH` 1 each).
- Run the section's command verbatim: `--keysym SLASH` → rc 2, no output; `--keysym slash` → rc 0 with the AB11 row. The host's
  live `SLASH` bind (modmask 65, `exec`) works in Hyprland. So the section's first read labels a working bind NoSymbol and its
  next step (“fix the spelling”) sends the reader to change a spelling that is fine.
- Lower-casing is not the fix either: it resolves only 4 of the 14 (`slash`, `comma`, `period`, `space`). The **canonical**
  spelling resolves 14/14 (`BackSpace`, `Delete`, `Down`, `Escape`, `Left`, `Print`, `Return`, `Right`, `Tab`, `Up`, …).

Suggested repair (one sentence in the two rows): *the tool resolves case-sensitively like the library (`how-to-type.c:286`
`XKB_KEYSYM_NO_FLAGS`), while Hyprland retries case-insensitively (`KeybindManager.cpp:710-711`), so rc 2 is NoSymbol only if
the **canonical** spelling of the sym also returns rc 2 — e.g. `--keysym SLASH` rc 2 but `--keysym slash` prints the table.*

### F2 (the command block) — the tool line and the judge line are not the same invocation

The block gives the judge as `--keymap=FILE` and the tool as `--keymap FILE`, under the sentence “stdout and exit status equal
the judge's, byte for byte”. The judge's `--keymap` is declared `optional_argument` (`how-to-type.c:171`), so the space form
leaves the file name as a stray positional and is rejected:

```
judge   --keymap host-br.xkb … --keysym slash  -> rc 2, 0 B, ERROR: missing positional parameter
judge   --keymap=host-br.xkb … --keysym slash  -> rc 0, 505 B
/usr/bin/xkbcli how-to-type --keymap host-br.xkb …  -> rc 2 (same)
tool    --keymap host-br.xkb … --keysym slash  -> rc 0, 505 B   (accepts both forms)
```

So parity holds on the `=` form (39/39, `receipts/tool-parity.md`) and fails on the form the tool line itself uses; a reader who
copies the tool's line onto the judge gets rc 2. Fix: write the tool line as `--keymap=FILE` too, or add “the judge takes only
`--keymap=<file>` (optional_argument, `how-to-type.c:171`); the tool accepts both”. Evidence: `receipts/arg-forms.txt`.

### Notes (verified, not defects)

- **N1** — `SKILL.md:2226` is the heading `## XKB keymap compile (round 48)`; the `--layout zz` rc-1 matrix row is
  `SKILL.md:2247`. The rule is right (my run: rc 1, same `[XKB-338]` text); only the pointer is a heading.
- **N2** — row 2's “default 0 (`legacy-ConfigManager.cpp:533`)” points at the **device**-level registration; the input-level
  default is `ConfigValues.cpp:278` (also cited). Both lines say what the row needs; the live `{"int": 0, "set": false}` matches.
- **N3** — row 5's next step “set it globally, or per device” has no per-device first read: `hyprctl getoption
  device:resolve_binds_by_sym -j` → `no such option` (reproduced live; the round-49 receipt already shows it). The per-device
  value is real in config (`InputManager.cpp:1224`), but the row's instrument cannot confirm it.
- **N4** — “the file's only reads of it are `:280` and `:369`”: `grep -n m_xkbTranslationState KeybindManager.cpp` gives 11
  sites (null checks, creation, the two sym reads) and `grep -c xkb_state_update_mask` gives 0, so “never given a modifier”
  holds; “reads” means sym reads.

## Row-by-row verdicts (`receipts/locators-check.md` holds all 59 citations with the line text)

| # | row | verdict | evidence |
|---|---|---|---|
| 1 | modifier-free level | ok | `:332` state; no `xkb_state_update_mask` in the file; slash rows match; `wiki:80,:91` |
| 2 | which layout | ok | `:296-314` input names; `legacy:533`+`ConfigValues:278`; live `int 0`; `wiki-Variables:181` |
| 3 | device layout vs `input:kb_layout` | ok | `:299` vs `InputManager:1229`, `:1224-1241`; 10 keyboards all `br` |
| 4 | bind-side compile fallback | ok (N1 pointer) | `:326-328`; `--layout zz` rc 1; default-vs-configured rows differ |
| 5 | keycode field | ok | `legacy:1482-1485`; `:696-698`; `:367` (+8); 42 rows, keycode 10..201 |
| 6 | mask equality | ok | `:652`; `:221-240` uppercased substring; `IKeyboard:360`+`InputManager:1915-1931`; bits 1/4/64 |
| 7 | **name resolves at all** | **FAIL (F1)** | `how-to-type.c:286` vs `:710-711`; 53/142 rows |
| 8 | options rewrite syms | ok | `host-br.xkb:1581-1584` = my compile; `Caps_Lock` rc 0 empty table; `Multi_key` 66; `input.conf:10-11` |
| 9 | submap / several matches | ok | `:700`; `legacy:1619-1621`; `:773`, `:781-812`; all 192 submaps empty |
| E1 | **listed, never fires** | **FAIL (F1)** | same mechanism; “rc 2 is the silent skip made visible” holds only for canonical spellings; `:713-722` is the real skip |
| E2 | shifted char never fires | ok | `:332`,`:369`; `wiki:80`; slash = AB11 level 1 |
| E3 | unexpected key / option edit | ok | receipt `host-br.xkb:1581-1584`; `Caps_Lock` has no row |
| E4 | numeric key field | ok | `legacy:1482-1483`; `keysym.c:325`; `--keysym 47`/`0x2f`/`U002F` all → slash |
| E5 | second-layout bind | ok (N3) | `wiki-Variables:181`; live `int 0`; `:369`, `IKeyboard:218`,`:382` |
| E6 | Caps/Num lock irrelevant | ok | `IKeyboard:360` depressed|latched; `Num_Lock` has one row, `Caps_Lock` none |
| E7 | unbind case-sensitivity | ok | `:197-198` exact compare; `wiki:111` |
| E8 | `mouse:272` vs `bindm` | ok | `legacy:1589`,`:1594`; `wiki:144`; `:461-468` |

## Deliverables (all exist, verified with `test -f`)

`Report: .ufo/waves/round-50/w1/ExecSkillRows.md` — this file.
Seat receipts: `.ufo/waves/round-50/w1/ExecSkillRows/receipts/` — `commands.txt`, `arg-forms.txt`, `tool-parity.md`,
`case-sensitivity.md`, `locators-check.md`, `binds-tally-r50.md`, `hyprctl-live-r50.md`, `pin-integrity.txt`.

## Risks / blockers

- F1 is a **diagnostic** defect, not a code defect: `tools/mado-keysym.py` reproduces the judge exactly (39/39), and the judge
  is right about libxkbcommon. The fix belongs in the two rows' wording; if the L1 wants the counter to catch it, the check is
  “the row's first read must not label a case-insensitively-resolvable bind as NoSymbol” (fixture: `--keysym SLASH` rc 2,
  `--keysym slash` rc 0 on this keymap).
- The section's multi-layout rows stay source-supported only: the host has one layout (10/10 keyboards `br`), so rows 2/E5 have
  no live observation, as the section itself says. I did not exercise `resolve_binds_by_sym = 1` (compositor mutation is out of
  lane scope).
- `input:kb_file` is empty on this host, so the `kb_file` branch of `KeybindManager.cpp:312-314` is unexercised; I cited it, I
  did not observe it.
- Session material: the live binds and devices JSON remained in scratch only; receipts carry counts and shapes, no device names,
  switch names, serials or home paths (`~` for the home directory).
- No tool installed or upgraded this seat; scratch removed on exit.
