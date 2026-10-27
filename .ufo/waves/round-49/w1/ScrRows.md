# ScrRows — SOURCES rows S352-S363 for round 49 (C2 bind key-match, C1 keysym tool)

Status: **complete**. Twelve rows drafted, opened, pinned and gate-lined; census run on a scratch copy of the registry.
No lane file edited outside this seat dir and this report.

## What was produced

| artifact | path | size / digest |
|---|---|---|
| registry rows (ready to append after S351) | `.ufo/waves/round-49/w1/ScrRows/rows.md` | 15152 B, sha256 `66174756…` |
| gate lines, rejects, census, flags | `.ufo/waves/round-49/w1/ScrRows/gate.md` | 17534 B, sha256 `bd46d4ab…` |
| pins (12 files) + manifest | `.ufo/waves/round-49/w1/ScrRows/pins/` | `pins/SHA256SUMS`, 13 lines |
| quote verification script + output | `verify-quotes.sh`, `quotes-verified.txt` | 19 PASS, rc 0 |
| host receipt (shape only) | `receipt-hyprctl-binds-r49.txt` | 1005 B, sha256 `3dc5de54…d1d8` |
| census baseline / with rows | `census-base.txt`, `census-with-rows.txt` | 2335 B / 3420 B |
| how-to-type samples (C1 support) | `how-to-type-slash-r49.txt`, `how-to-type-nosuchsym-r49.err` | 505 B / 2123 B |
| getoption reply | `hyprctl-getoption-rbs-r49.json` | 66 B |

Rows: S352 Hyprland KeybindManager.cpp · S353 Hyprland legacy/ConfigManager.cpp (bind parser) · S354 Hyprland
InputManager.cpp (mask feed) · S355 libxkbcommon src/keysym.c · S356 src/ks_tables.h · S357 tools/how-to-type.c ·
S358 include/xkbcommon/xkbcommon-keysyms.h · S359 wiki Binds.md @ `d5f07c60` · S360 wiki Variables.md @ `d5f07c60` ·
S361 this host's read-only `hyprctl` bind surface · S362 libxkbcommon src/state.c · S363 Hyprland src/devices/IKeyboard.hpp.
S355-S358 carry `used-by: tools/mado-keysym.py`; the rest carry the C2 entry path. All tier A, status `mined`, opened
2026-10-27, recheck `on-release` (S361 `90d`). S362/S363 were added mid-run at the C2 entry seat's request; both are new URLs.

## Gates

- Every row was opened this run at a tag or commit URL, never a branch: libxkbcommon tag `xkbcommon-1.13.2` (commit
  `d1442aaa…`), Hyprland commit `efb50993…` (the `v0.56.2` tag resolves to that commit, checked with the GitHub refs API),
  wiki commit `d5f07c60…` (2026-08-05T13:16:48Z, last content commit before the 0.56.2 release at 14:14:01Z).
- Every gate quote was located by a computed line number and re-grepped at that line in the pinned bytes: 19/19 PASS.
- Rejects recorded with reason and flip: the rendered 0.56.0 archive and the latest-git wiki URL (no commit anchor; the wiki
  repo has no tags), ArchWiki Hyprland (0 hits for `0.56.2`, `resolve_binds_by_sym`, `xkb_keysym`), and two held-duplicate
  URLs (`IKeyboard.cpp` = S319, `ConfigValues.cpp` = S318) that are cited, not re-registered.

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$L/corpus/SOURCES.md"` where `$L` is a
scratch lane-shaped root (symlinks to the lane's top-level entries, `corpus/SOURCES.md` the modified copy), so `used-by`
resolves exactly as in lane mode.

- baseline (committed registry, 288 rows): `rc=0`, W04 ×17, W01 ×1, E ×0 — equal to the round-48 closure census.
- with S352-S363 (300 rows): `rc=1`, W04 ×19, W01 ×1, **E11 ×12** — the twelve `E11` are the two artifacts other seats are
  still writing (`corpus/knowledge/hyprland-bind-key-match-r49.md`, `tools/mado-keysym.py`), absent at 01:44. No other error
  class. The two extra `W04` are the documented duplicate-URL decisions (S353 vs S162/S303/S317 on the same file with a
  fourth scope; S354 vs S316, whose anchored range does not cover the mask feed).

## Findings for the L1

1. **Header count.** The claim says 2659 `#define XKB_KEY_` lines. `grep -c 'define XKB_KEY_'` = 2659, but 21 are inside the
   header's doc comment; anchored `grep -cP '^\s*#\s*define\s+XKB_KEY_'` = 2638. C1 fixtures and counters must say which
   count they assert.
2. **The header is sufficient — corrected during this run.** I first drafted S356/S358 saying the header cannot reproduce
   lookup order or the canonical name. `ExecKeysymNames` reported the opposite rule and I re-checked it with a script over the
   two pins: taking the **first** `#define` per value in file order reproduces `ks_tables.h`'s `keysym_to_name[]` exactly
   (2505 values, 0 mismatches); the last-define rule flips 120 names; `name_to_keysym[]` equals the header's 2638 names
   value-for-value. Both rows, the S356 gate line and the report were rewritten. Independently, that seat's 10,613-ARG parity
   sweep (first stdout line + exit status, 0 diffs) and 344 rows under a second keymap support it.
3. **`--keymap` is `optional_argument`** (`tools/how-to-type.c:171`): only `--keymap=FILE` binds the file; the spaced form
   would read FILE as the keysym argument. The contract already writes the `=` form.
4. **Held ground the C2 entry will want.** `ConfigValues.cpp:278` (resolve_binds_by_sym default false) is inside S318's
   `:271-279`; `IKeyboard.cpp:376-385` (sym state updated with zero depressed/latched/locked + current group) is S319's file.
   Both are cited with locators, not re-registered; if the entry needs S319 to back those lines, that is a scope widening only
   the L1 can make. `S359` carries the wiki's layout section (`:462-474`) including the `resolve_binds_by_sym` paragraph, so
   no separate keyboard-layouts row is needed.
5. **Wiki pin is content-stable.** `content/Configuring/Basics/Binds.md` is byte-identical at `d5f07c60` and at `5e26bcc1`
   (6 h later): sha256 `3d8a2a68…7d628`.
6. **Host shape.** `hyprctl binds -j` on this build carries no `ignore_mods` field at all (flag parsed, not serialized);
   zero binds use it, so flag `i` has code-only support here (S353 `:1525`).
7. Live parity check: `xkbcli compile-keymap --layout br --options compose:caps` reproduces the round-48 keymap digest
   `efd487a3…ce81` (73079 B); `how-to-type --keysym slash` gives the exact five-row AD01/AB11 table in the claims sample,
   `--keysym nosuchsym` gives rc 2 with the ERROR line.
8. **Naming is three-way, and ARG has two traps.** `xkb_keysym_get_name` prints the table name, else `U%04X` inside
   `0x01000100-0x0110ffff`, else `0x%08x` (`src/keysym.h:43-51`, pinned inside S355); the `0x01000000-0x010000ff` band
   therefore stays hex. In `--keysym` mode `0x0` is refused (no such name) while decimal `0` is the keysym named `0`
   (0x0030), and `-h`/`--help` exit 0 with usage on stdout. All three are in S355/S357 and in the gate lines, so C1 fixtures
   can assert them.

## Touched surfaces

- Written: `.ufo/waves/round-49/w1/ScrRows/` (rows.md, gate.md, pins/, receipt, census files, verify script, samples) and this
  report. Nothing else in the lane, the fleet, or the host. No tool installs. No git/jj mutation. No compositor mutation;
  only `hyprctl version -j`, `binds -j`, `getoption … -j` and the three allowed `xkbcli` verbs, in a clean environment with
  HOME/XDG_* under scratch.
- Scratch `/fast/scratch/hyaku/mado-r49/ScrRows` stayed under 2 MB and is removed at the end of this seat run.

## Out of scope (not done here)

- The C2 entry itself and the C1 tool: other seats own them; this seat supplies rows, gate lines and pinned sources.
- No edit of `corpus/SOURCES.md` (the L1 integrates), no counter, no judge, no freeze decision.
- The raw `hyprctl binds -j` payload is deliberately not published (dispatcher args and command text are the operator's);
  only the shape receipt is kept.

## Limits

- The census `E11 ×12` is expected-pending, not clean; it clears when the entry and the tool land.
- The scratch lane-shaped root is a symlink construction, so `E11` resolution is proven against the real lane paths but the
  run itself was not a lane check-out.
- `pins/` is ~1.1 MB (three large upstream files: `ks_tables.h`, `xkbcommon-keysyms.h`, `state.c`); the L1 may prefer to
  move them to `.ufo/waves/round-49/fetch/`.
