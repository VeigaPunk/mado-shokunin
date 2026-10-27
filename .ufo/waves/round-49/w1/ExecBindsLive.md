# ExecBindsLive — C2 live receipts + C1 host join demo (round 49, w1)

Seat: `ExecBindsLive`. Round 49 (hyaku run 9), wave `w1` = BUILD. Lane base `03e4ae76aff7a4be59cb69970dd553baa319695a`.
Writes: this report + `.ufo/waves/round-49/w1/ExecBindsLive/**` only (no tracked file touched, no git/jj mutation).
Scratch `/fast/scratch/hyaku/mado-r49/ExecBindsLive/` deleted at the end; no scratch path is cited as evidence.
No tool installs this wave (nothing needed).

## What ran (read-only)

| read | result | receipt |
|---|---|---|
| `hyprctl version` | `Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean` | `receipts/live-version.txt` |
| `hyprctl getoption input:resolve_binds_by_sym -j` | `{"option": "input:resolve_binds_by_sym", "int": 0, "set": false }` | `receipts/live-version.txt` |
| `hyprctl binds -j` | 192 binds, 90401 bytes, sha256 `9a47199e…c779`; second capture 3 min later identical | `receipts/binds-shape.txt` |
| pinned `xkbcli compile-keymap` | host keymap from `--layout br --options compose:caps`, deterministic (two runs, one sha256 `efd487a3…ce81`) | `receipts/judge-behaviour.txt` |
| pinned `xkbcli how-to-type` | 58 distinct keysym names, both resolved values each | `receipts/bind-keys.txt` |
| upstream pins at `efb50993` / `xkbcommon-1.13.2` | 5 files, sha256 + grep-computed locators | `receipts/upstream-pins.txt` |

Counter-shaped receipt for the C2 entry's clause f: `receipts/binds-receipt.txt`, generated from the raw bytes, with the
form rule the C2 counter settled on: `key starting code:/mouse/switch: -> that form; key == "" AND keycode != 0 -> code;
otherwise named`, giving `binds=192 named=142 code=42 mouse=6 switch=2 catch_all=0`. (`hyprctl` never prints `code:` in the
key field — the 42 code binds carry `key` empty over 14 distinct keycodes, 10-21 / 61 / 201 = AE01-AE12 / AB10 / FK23.)

Host key input config, read-only: `~/.config/hypr/input.conf:10 kb_layout = br`, `:11 kb_options = compose:caps`,
`:18 numlock_by_default = true`; `kb_variant`/`kb_model` unset, so the keymap is the pc105 default.

## Live binds shape (192, shape-only fields)

- forms: keysym name 142, `code:N` 42, `mouse:<button>` 2, `mouse:down` 2, `mouse:up` 2, `switch:on/off:<name>` 2.
- `keycode` non-zero on exactly the 42 `code:N` binds: `AE01..AE12` (10..21), `AB10` (61), `FK23` (201) — key names computed
  from the compiled keymap's keycodes section, not typed.
- `catch_all` 0, `submap` empty on all 192, `mouse` true on 2 only.
- modmask histogram: `0`×23, `1`×2, `8`×7, `9`×2, `12`×2, `13`×1, `64`×42, `65`×37, `68`×26, `69`×3, `72`×19, `73`×22, `76`×6.
  No mask carries `2` (Lock) or `16` (Mod2/NumLock) even though `numlock_by_default = true`.
- `mouse` in the JSON is the `bindm` **flag**, not "the key is a mouse button": `mouse:272`/`mouse:273` come from `bindm`
  (`mouse=true`) while `mouse_up`/`mouse_down` come from plain `bind` (`mouse=false`). Grounded: `src/config/legacy/ConfigManager.cpp:1521`
  `case 'm': mouse = true; break;` and `:1589` `HANDLER = "mouse";`.

## Join: every bind keysym on the host keymap

`receipts/bind-keys.txt` (58 names, both name resolutions, judge output verbatim) and `receipts/host-join-summary.txt`.

Name resolution is the first thing that bites: the live binds are upper-case (`SLASH`, `RETURN`, `SPACE`, `A`..`Z`), the
pinned judge is case-**sensitive**, so the judge alone rejects a bind name:

- `--keysym SLASH` → exit 2, `ERROR: Failed to convert argument to keysym` + usage (`receipts/judge-behaviour.txt`).
- `xkb_keysym_from_name("SLASH", 0)` = NoSymbol, `…(…, CASE_INSENSITIVE)` = `0x002f`; `"A"` = `0x0041` / `0x0061`.
- Hyprland therefore accepts **either** resolution per bind: `KeybindManager.cpp:710` `KBKEY` with `XKB_KEYSYM_NO_FLAGS`,
  `:711` `KBKEYLOWER` with `XKB_KEYSYM_CASE_INSENSITIVE`, `:724` `if (key.keysym != KBKEY && key.keysym != KBKEYLOWER)`.
  libxkbcommon's case-insensitive "best" match is the lower-case name (`src/keysym.c:268`), which is why `SLASH`→slash but
  also why `A`→`a` in that branch.

On the br keymap all 58 keysyms exist; **0** are reachable only at level ≥ 2 and **0** are absent. The L1 sample reproduces
exactly: `slash` → `AD01` levels 3/4 with `[ Mod5 LevelThree ]` (+ `Lock`, `Shift` variants) and `AB11` level 1 `[ ]`.

## Flagged: live binds that cannot fire (operability)

`receipts/bind-reachability.txt`. Model, all sourced: a press fires a bind iff its translated keysym equals either
resolution **and** depressed mods equal the bind modmask exactly (`KeybindManager.cpp:652`), where the modmask is
depressed-only (`InputManager.cpp:1711` `m_lastMods = MODS.depressed;`). Which keysym is compared on this host: the
`resolve_binds_by_sym = 0` branch, i.e. `m_xkbTranslationState` (`KeybindManager.cpp:369`), and the keycode used is
`e.keycode + 8` (`:367`), so `code:N` is an xkb keycode — exactly what the compiled keymap prints.

Of 184 key/code binds: **176 fire**, **8 cannot fire**; 3 binds are exact duplicates of an earlier bind
(same modmask + key), 2 of which fire *in addition* to their twin.

Dead (keysym changes at the level the bind's own mask selects):

| bind | mask | dispatcher | why |
|---|---|---|---|
| 74 `TAB` | 65 Shift Mod4 | workspace | Shift+Tab is ISO_Left_Tab; `TAB` exists only at level 1 keycode 23 |
| 85 `TAB` | 9 Shift Mod1 | cyclenext | same |
| 87 `TAB` | 9 Shift Mod1 | bringactivetotop | same (and an exact duplicate of bind 85) |
| 89 `TAB` | 13 Shift Control Mod1 | focusmonitor | same |
| 105 `TAB` | 73 Shift Mod1 Mod4 | changegroupactive | same |
| 135 `COMMA` | 65 Shift Mod4 | exec | `comma` is level 1 only (keycode 59 AB08) |
| 138 `COMMA` | 73 Shift Mod1 Mod4 | exec | same |
| 181 `SLASH` | 65 Shift Mod4 | exec | Shift makes AB11 `?` (0x3f); slash rows need no Shift |

So the sharp answer to the C1 question on this host: `bind = SUPER, SLASH` fires from **AB11 only**, and the AD01
AltGr+Q path cannot fire it because Mod5 in the press makes `modmask != 64`. `bind = SHIFT SUPER, SLASH` fires from
nothing at all.

Duplicates (`hyprctl` reports both, and `handleKeybinds` collects **all** matches into `bindsHit`, `:773`, then dispatches
each, `:781` ff. — no early exit, so a duplicate double-dispatches):

- `(8, TAB)`: binds 84 `cyclenext` **and** 86 `bringactivetotop` → Alt+Tab runs both.
- `(9, TAB)`: binds 85 `cyclenext` + 87 `bringactivetotop` → both cannot fire (Shift+Tab), see the table.
- `(0, F9)`: binds 162 and 163, both `exec` → the command runs twice per press.

## C1 input: pinned judge behaviour the tool must reproduce

`receipts/judge-behaviour.txt` (real runs, `env -i PATH=/usr/bin`, HOME/XDG in scratch):

| case | judge | note for the contract |
|---|---|---|
| `--keymap=FILE --disable-compose` (no ARG) | rc **2**, stderr `ERROR: missing positional parameter` + usage, **stdout empty** | usage goes to stderr, so stdout+rc is well defined |
| `--keysym nosuchsym` / `SLASH` / `2f` / `0x0` | rc **2**, same stderr shape, stdout empty | ARG parsing: names are case-sensitive, hex needs `0x`, `0x0` is rejected |
| `--keysym 0` | rc 0, `keysym: 0 (0x0030)` | `0`..`9` are names first (usage text says so) |
| `--keymap=missing` | rc **1**, `ERROR: Failed to open keymap file "…"`, `ERROR: Failed to create XKB keymap`, stdout empty | tool must exit 1, print nothing on stdout |
| `--keymap=FILE --layout us` | rc **2**, `ERROR: Cannot use RMLVO options with keymap input` | the tool has no RMLVO path anyway |
| no `--disable-compose` | rc 0 **but stdout gains** `=== Access via Compose sequences ===` | the flag is load-bearing: it changes stdout, not the exit code |
| `--keymap` (bare) or `-` | reads the keymap from stdin, rc 0 | FILE is required by contract, so the tool may refuse anything but a path |

The tool was **absent** at every check of this seat: `tools/mado-keysym.py` did not exist at five checks between
04:36Z and 04:47:08Z, so the demo above ran the judge itself; `bind-keys.txt` is the byte-exact target the tool must emit for these 58 names, and the
name-resolution step (CASE_INSENSITIVE → canonical/numeric) is the caller's, not the tool's, since the judge is
case-sensitive.

## Pins (sha256, commit/tag URLs, never a branch)

See `receipts/upstream-pins.txt`: `KeybindManager.cpp` `8d8f35fc…4e40`, `input/InputManager.cpp` `feedf32e…4765`,
`IKeyboard.cpp` `8a800efe…a3d`, `config/legacy/ConfigManager.cpp` `9db68cf4…62b`, libxkbcommon `src/keysym.c`
`123e3390…69c5`. All locators in that file are `grep -n` on those bytes and are re-grepped by the generator
(`22 patterns, missing after emit = 0`). Judge binary `f6c0b122…7e54`, compile-keymap `43b924f6…7250`, keysyms header
`13023369…63f3` — all match the round's pins.

Two source facts that close the round's open ground: `parseKey` makes a **bare number > 9** a keycode too
(`config/legacy/ConfigManager.cpp:1481-1487`), and `resolve_binds_by_sym` defaults to `0`
(`:533 addSpecialConfigValue("device", "resolve_binds_by_sym", Hyprlang::INT{0})`), is read per device
(`InputManager.cpp:1224`) and stored on the keyboard (`:1241`). The other state, `m_xkbSymState`, only ever receives the
group (`IKeyboard.cpp:382` / `:422` zero everything but the layout group) — that is the "layout 0 vs active layout" answer
for the C2 entry.

## Risks / blockers

- `tools/mado-keysym.py` does not exist yet, so the C1 side-by-side demo could not run; the judge-side target is complete.
- Safer contract edge for the C1 counter: compare **stdout + exit status only** — stderr carries a `Usage: <argv[0]>` line
  that can never match between the tool and the judge.
- The dead-bind table depends on the host keymap being `br` + `compose:caps` (it is, `input.conf:10-11`); a layout change
  moves every row.
