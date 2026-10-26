# SKILL.md section and PROVINCE.md refinement for `tools/mado-devices.py` — append-ready text

Seat `ScrSkill`, round 46 w1 (hyaku run 9), 2026-10-26. Freeze `8c5434c60e03f147ee1f75ab195e8bc3f0db4dec`, base
`b22ea56bff2faec39ce9ff75d2107eaf4612ecbe`. **`SKILL.md` and `PROVINCE.md` are not edited by this seat** — the L1 is
the integrator. Read at this seat's start: `SKILL.md` 2102 lines (tail section `:2100-2102`, round 45), `PROVINCE.md`
100 lines (tail refinement `:100`, round 45; tool table rows `:24-32`).

Insertion points: **SKILL.md → append after `:2102`** (end of file, in the append-only round order the file keeps);
**PROVINCE.md → append after `:100`**, plus one table row after `:32`.

Every locator below is computed (`grep -n`) and re-checked by `w1/ScrSkill/verify.py`; the last run is
`w1/ScrSkill/receipts/verify.txt`. Receipts this draft leans on: `receipts/locators.txt` (pin and docstring
locators, reference selftest), `receipts/host-runs.txt` (the host chain, `getoption`, `xkbcli`),
`receipts/synthetic-verdicts.txt` (ten fixture runs of the reference), and the L1's own
`.ufo/waves/round-46/receipts/live-devices-host-l1.txt` (cited as received, not re-run).

**Conditional on landing.** `tools/mado-devices.py` is absent at base, at the freeze and in this seat's working tree
(`git ls-tree` empty at both commits; `ls` fails — `receipts/locators.txt` §E). Both blocks become true only when C1
lands the tool at `tools/mado-devices.py` at the round-46 data commit. If C1 misses, omit Block 1's command and
table and Block 2's first paragraph, and record the miss: the counter's kill rule decides, not this draft. If the
landed docstring differs from the reference `.ufo/waves/round-46/l1-draft/mado-devices.py`, re-read the verdict
order, the exit map and the read caps against the landed bytes before keeping them.

---

## Block 1 — the SKILL.md section

**Goes after `SKILL.md:2102`** (append at end of file; the round-45 section `:2100-2102` is the current tail, and
this file appends round sections in order).

### Input-device rules versus running devices (round 46)

`hyprctl devices -j | python3 tools/mado-devices.py --devices - --config <file>…` joins two caller-supplied read-only
inputs: the `input`/`device` lines of one or more Hyprland config files, and one `hyprctl devices -j` dump. Output: one
`MADO_DEV_KEYBOARD:` line per keyboard, one `MADO_DEV_MOUSE:` line per pointer, one `MADO_DEV_BLOCK:` line per
`device` block, then one `MADO_DEVICES:` summary; `--selftest` runs its cases as inline strings and reads nothing from
the lane (its setup cases only fail to open `/nonexistent/*`)
(`mado-devices.py:446-447`, observed 48/48). The tool starts no process, opens no socket and reads no config tree of its
own — the caller captures the dump with the whitelisted read verb.

**Pass every file yourself.** No `source =` line is followed, so the tool reads exactly the files named on the command
line and the last file wins (a later `input:kb_layout =` overwrites an earlier one, `mado-devices.py:36`; selftest case
`later-wins`, `:466`). This host's chain is `~/.config/hypr/hyprland.conf:11` → `~/.local/share/omarchy/default/hypr/input.conf` (`kb_layout = us`
at `:3`) and `:17` → `~/.config/hypr/input.conf` (`kb_layout = br` at `:10`); the theme file at `:13` and the toggles
glob at `:23` carry no `input`/`device`/`kb_`/`scroll_factor` line (0 matches each). The correct host command therefore
names both files, in that order:

    $ hyprctl devices -j | python3 tools/mado-devices.py --devices - \
        --config ~/.local/share/omarchy/default/hypr/input.conf \
        --config ~/.config/hypr/input.conf

**What the join models.** For each keyboard the expected names are, per `kb_layout`, `kb_variant`, `kb_options`,
`kb_model`, `kb_rules`, the `device` block's value when that block set it, else the global `input:kb_*`, else the
default (`us` for the layout, empty for the other four) (`Hyprland-InputManager.cpp:1226-1231`,
`Hyprland-ConfigManager.cpp:1115-1122`, `Hyprland-ConfigValues.cpp:272`); a `kb_file` is printed only as `kb_file=<set|->`.
When the names do not compile, the compositor resets the stored rules to `us` with four empty names
(`Hyprland-IKeyboard.cpp:101-116`). A virtual keyboard takes its keymap from its client and ignores later rule changes
(`Hyprland-VirtualKeyboard.cpp:41`, `Hyprland-IKeyboard.cpp:60-64`). For a pointer the expected factor is the block's
`scroll_factor` clamped to 0..100 when the block sets it, else `-1`; the global `input:scroll_factor` never reaches the
printed `scrollFactor` (`Hyprland-InputManager.cpp:1379-1382`, `Hyprland-ConfigValues.cpp:296`,
`Hyprland-HyprCtl.cpp:770`). A `device` block matches when its name equals a printed device name; names are lower-cased
with space, newline and comma turned into `-` and a `-N` suffix for duplicates
(`Hyprland-MiscFunctions.cpp:777-789`, `Hyprland-InputManager.cpp:2119-2130`).

**Decision table — a verdict, what it means, and the next read-only step it licenses.**

| verdict | where it prints | what it means | next read-only step |
|---|---|---|---|
| `AGREE` | keyboard line | the five printed names equal the ones the tool computed from the `device` block, the global option or the default | none for that keyboard — but it is agreement with the files you passed: pass the rest of the chain before reading it as agreement about the host |
| `DIFFER` + `differ=<names>` | keyboard line | those printed names are unequal to the computed ones: a join, not a blame — a runtime `hyprctl keyword`, a file not passed or a block under another name produces it too | `hyprctl getoption input:kb_<name> -j` for the global the compositor holds: a value the file does not set means a runtime `keyword` wrote it; else re-run with one `--config` file at a time to find the writer |
| `FALLBACK` | keyboard line | the printed rules are exactly `us` and four empty names while the config expected something else — the shape left after a keymap that does not compile (`Hyprland-IKeyboard.cpp:101-116`) | `xkbcli compile-keymap --layout <L> --variant <V> --options <O> --rules <R> --model <M>` on the expected names: rc 1 with `Failed to compile xkb_symbols` reproduces the failure off-compositor, and `hyprctl getoption input:kb_layout -j` says whether `us` came from the global instead |
| `VIRTUAL` | keyboard line | the name starts `hl-virtual-keyboard`: the client's keymap is not in the dump, so the printed names witness the config at creation only (`Hyprland-VirtualKeyboard.cpp:41`, `Hyprland-IKeyboard.cpp:60-64`); it exists only while its IME holds one, so `virtual=0` in a run is not a fault | none in the dump; and a virtual keyboard never moves the top verdict — a contradicting block still prints `differ=` and exits 0 (`receipts/synthetic-verdicts.txt`) |
| `AGREE` | mouse line | the block's factor (clamped 0..100), or `-1` when the block does not set it, equals `scrollFactor` at two decimals | none; `input:scroll_factor` is a separate global option and is never the printed field (`Hyprland-ConfigValues.cpp:296`) |
| `DIFFER` | mouse line | the factor the block sets, or the `-1` of "not set", differs from `scrollFactor` | `hyprctl getoption input:scroll_factor -j` for the global (it reaches no pointer's printed field), then re-read the block's value, then re-run per file |
| `MATCHED` | block line | the block's name equals the `name` of a printed device (or of one its `belongsTo` object names) | none |
| `NO_SUCH_DEVICE` | block line | no printed device carries that name; names are normalised (`Hyprland-MiscFunctions.cpp:777-789`), so a product name as the kernel reports it cannot match | compare verbatim with the names from the same dump (`hyprctl devices -j`); an unplugged device explains it |
| `NOT_COMPARED` | summary, rc 5 | an unmodelled line is present — `$`, `{{` or a backslash in a relevant line, a `name =` rename, or a `device { }` whose first assignment is not `name` — and "an unmodelled line can change any expectation" (`mado-devices.py:87`); it outranks `DIFFER` | the count is not line-attributed: grep the files for those three tokens and for a `device {` block whose first key is not `name` (`receipts/synthetic-verdicts.txt`) |
| `DIFFER` | summary, rc 1 | at least one keyboard differs or falls back, or one mouse differs | read the per-device lines, not the top verdict; a `stale=` block also surfaces here when something else differs |
| `NO_KEYBOARDS` | summary, rc 3 | the dump held no `keyboards` element | re-capture with `hyprctl devices -j`: an empty list means the dump did not come from a live session (this host's lists ten, one of them the fcitx5 virtual keyboard) |
| `STALE_BLOCK` | summary, rc 4 | a `device` block matched no device **and nothing else differed** — rc 4 is reachable only in that clean case, because `DIFFER` is tested before it (`receipts/synthetic-verdicts.txt`) | the `MADO_DEV_BLOCK:` line names the block; same verbatim comparison as `NO_SUCH_DEVICE` |
| `SETUP` | single line, rc 2 | `usage`, `unreadable` (missing, unreadable, a directory, a FIFO or any non-regular path), `too_large` (> 1048576 B; stdin at most 1048577) or `bad_json` (not UTF-8 JSON with `keyboards` and `mice` lists of objects that each carry a string `name`) | fix the argument: a setup failure reads no further and is never a verdict (`mado-devices.py:29-34`) |

Exit map: 0 `OK` · 1 `DIFFER` (`differ + fallback + mice_differ > 0`) · 2 `SETUP` (usage | unreadable | too_large |
bad_json) · 3 `NO_KEYBOARDS` (`keyboards = 0`) · 4 `STALE_BLOCK` (`stale > 0`) · 5 `NOT_COMPARED`
(`unsupported > 0`), tested in that order — NOT_COMPARED, DIFFER, NO_KEYBOARDS, STALE_BLOCK, OK. stderr is empty on
0/1/3/4/5, and a setup failure prints exactly one line, `MADO_DEVICES: SETUP <reason>` (`mado-devices.py:80-89`).

**Read-only boundary.**

- **Reads** — the files named with `--config` (one or more, read in argument order, each opened
  `O_RDONLY|O_NONBLOCK` and required to be a regular file, `mado-devices.py:126-130`; 1048576 B cap; UTF-8 with
  errors replaced) and one dump with `--devices` (a regular file, or `-` for standard input at most 1048577 bytes).
  Nothing else: no `source =` line is followed, no `$NAME` is expanded, no environment variable is read, no config
  tree is discovered — the caller names every file the lane means to read.
- **Writes** — nothing. stdout only; `--selftest` builds its cases as inline strings and probes only the fixed paths
  `/nonexistent/x` and `/nonexistent/y` for the unreadable case, creating no file.
- **Process and socket** — starts no process, opens no socket, connects no compositor and no Wayland client: "It reads
  files and standard input only; it starts no process and opens no socket." (`mado-devices.py:26`). The dump is
  captured by the caller with the whitelisted read verb `hyprctl devices -j`; `keyword`, `setprop`,
  `switchxkblayout` and `reload` are never the lane's, and no config byte is written.
- **Session material** — the dump is projected to what the tool prints: device names, the five rule names, the factor,
  and per block a name and a key count. A raw dump also carries device paths and vendor/product ids, so it stays in
  scratch and only the projected lines are committed (`receipts/host-runs.txt`).

**Licence notes.**

- **`DIFFER` is a join, not a blame.** It reads the bytes of the files you name and one dump; it never asks the
  compositor which names it stored or which writer set them ("It is a join, not a blame", `mado-devices.py:19`). The
  expected side is the tool's own model of the lookup, so a `differ=` label is `[INF]` even when the printed side is
  `[OBS]`.
- **`FALLBACK` has one shape and two writers.** A keymap that does not compile and a runtime `hyprctl keyword
  input:kb_layout us` both leave `us` with four empty names; `hyprctl getoption input:kb_layout -j` separates them,
  because only the second also changes the option the compositor holds.
- **`VIRTUAL` never moves the top verdict.** A `device` block naming a virtual keyboard can print
  `differ=layout` on its line while the run exits 0 (`receipts/synthetic-verdicts.txt`), so a virtual keyboard cannot
  turn a host run red and its printed names are not evidence about the keymap in use.
- **`unsupported` is counted, not located.** `NOT_COMPARED` says a line could change any expectation but never prints
  which line, so the follow-up is a grep of the same files for `$`, `{{`, a backslash, a `name =` rename and a
  `device {` block without `name` as its first key.
- **A sparse dump reads `DIFFER`, not `AGREE`.** A keyboard object that omits the five names never equals an expected
  name (`mado-devices.py:71`), so a hand-trimmed dump reports all five as differing; capture the whole dump.

Host run 2026-10-26, Hyprland 0.56.2 at `efb50993`, the two-file chain above (`receipts/host-runs.txt`; the L1's
single-file run is `receipts/live-devices-host-l1.txt`):

    $ hyprctl devices -j | python3 tools/mado-devices.py --devices - \
        --config ~/.local/share/omarchy/default/hypr/input.conf \
        --config ~/.config/hypr/input.conf
    MADO_DEV_KEYBOARD: name="hl-virtual-keyboard-fcitx5" block=no layout="br" variant="" options="compose:caps" model="" rules="" kb_file=- differ=- verdict=VIRTUAL
    MADO_DEVICES: keyboards=10 agree=9 differ=0 fallback=0 virtual=1 mice=4 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK

Nine keyboards and all four pointers AGREE, the fcitx5 virtual keyboard is `VIRTUAL`, no `device` block
exists on this host (`blocks=0`), and the run exits 0.

**The keyboard count is not a constant.** A capture of the same command by this seat, moments after the L1's, printed
`MADO_DEVICES: keyboards=9 agree=9 differ=0 fallback=0 virtual=0 mice=4 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK`
— the fcitx5 virtual keyboard was absent from that dump and came back in the next capture
(`receipts/host-runs.txt`, the "flaps across captures" section). So `virtual=0` is not a defect, `VIRTUAL` is only
observable while an IME holds a virtual keyboard, and a `keyboards=` count is only comparable within one capture.

**Known limits.** This host has no `device` block, so `MATCHED`, `NO_SUCH_DEVICE`, `STALE_BLOCK`, every `block=yes`
line and every mouse `DIFFER` are exercised only by the tool's fixtures and by the seat's synthetic runs, not by a
live host run here. No keyboard differs, so `DIFFER` and `FALLBACK` are fixture-only on this host as well. `AGREE`
says the stored rules equal the config's names, not that the layout types correctly, and a `kb_file` keymap is never
read — the tool prints only whether one is set. No verdict survives a config change: `hyprctl keyword input:kb_*`, a
reload or a replug can change the stored names after the dump was taken, and a virtual keyboard appears and disappears
with its IME client between two captures. A pointer printing the config's global
`input:scroll_factor` is `DIFFER` by design, because the printed field only ever carries the block's own value. The
model is hyprlang 0.6.8 as Hyprland reads it; a line form it does not model is counted, never guessed.

---

## Block 2 — the PROVINCE.md refinement

**Goes after `PROVINCE.md:100`** (append at end of file), with one conditional table row inserted after
`PROVINCE.md:32` (last row, `tools/mado-geometry.py`; the table is `:24-32`, header `:22`).

### 2a. The table row (conditional on C1 landing the tool)

| Tool | Reads | Writes | Owner and adjacent lanes |
|---|---|---|---|
| `tools/mado-devices.py` | the bytes of every file the caller names with `--config` (one or more, read in argument order; each opened `O_RDONLY\|O_NONBLOCK` and required to be a regular file, so a missing, unreadable, directory, FIFO or device path is `SETUP unreadable`; 1048576 B cap; UTF-8 with errors replaced) and one caller-supplied `hyprctl devices -j` dump (`--devices`, the same regular-file rules, or `-` for standard input at most 1048577 bytes, UTF-8 JSON holding `keyboards` and `mice` lists of objects); it follows no `source =` line, expands no `$NAME`, reads no environment variable and discovers no config tree, so the caller names every file the lane means to read; no compositor socket, no Wayland client, no network, no process started — the dump is captured by the operator with `hyprctl devices -j` | nothing — stdout only (`MADO_DEV_KEYBOARD:`, `MADO_DEV_MOUSE:`, `MADO_DEV_BLOCK:`, `MADO_DEVICES:` lines); `--selftest` builds its cases as inline strings and probes only `/nonexistent/*`, creating no file | mado, round 46 (a read-only join of the owned input-device plane with one captured device dump; it reads what the compositor stored, never what it renders or what a keymap types; the operator applies any change) |

### 2b. The refinement paragraph (paste unquoted at the end of `PROVINCE.md`)

**Round-46 refinement (append-only; one tool, two counters, one entry; no new write surface):** the input-device
plane of the owned config tree — the `input` block's `kb_layout`, `kb_variant`, `kb_options`, `kb_model`, `kb_rules`,
`kb_file` and `scroll_factor` keys, the `device` / `device[NAME]` blocks, and the `kb_*` and `scroll_factor` values
those blocks set — is owned here, at the resolution Hyprland 0.56.2 gives it. `tools/mado-devices.py` models the six
`kb_*` keys of that block and the block's own `scroll_factor`; the global `input:scroll_factor` reaches no pointer's
printed field and is read only through `hyprctl getoption`. The tool reads only the
files the caller names (`--config`) and one `hyprctl devices -j` dump (`--devices`, or `-`), so it follows no `source
=`, connects no socket and starts no process, the operator captures the dump with a whitelisted read verb and applies
any change. It is "a join, not a blame": a runtime `hyprctl keyword`, a config file not passed or a `device` block
whose name never matches a device can move the printed side with no config byte changing, and a virtual keyboard's
printed names do not witness its keymap.

The two round-46 counters are record instruments, named here for the same reason the round-23 refinement names the
`tools/` instruments — the province accounts for every tracked instrument it runs, and neither touches a config plane,
the compositor or a host service. `quality/counters/c1-r46-devices.py` (`PRED-C1-r46`) reads git objects at
`--repo`/`--rev` with ambient `GIT_*` removed and extracts the tool blob, then runs it as a child process under
bubblewrap (`--ro-bind / /`, a tmpfs over the repository, the counter's lane and that lane's parent, a writable bind
of the marker directory only): its `--selftest` (60 s cap, run with `PATH=/usr/bin:/bin`, so the decoys below do not
guard that run — `c1-r46-devices.py:374-375`), 90 frozen fixtures in three runs (`seed 46` environment A,
`seed 46` environment B, a nonce in environment A) and 150 nonce-drawn cases judged by the pinned reference. For the
fixture and generated runs the PATH starts with a directory of four marker-writing decoys — `hyprctl`, `libinput`,
`journalctl`, `udevadm` — that must never run (clause r); that clause is a PATH-lookup check by construction: it does
not see an absolute path, and the tmpfs set covers only the repository and the lane (`hidden_paths`,
`c1-r46-devices.py:241-243`), so it is not a sandbox against a tool that opens the compositor socket under
`/run/user/<uid>`. The counter writes only beneath the `--work` directory, which must lie outside the repository and the
lane. `quality/counters/c2-r46-input-device-entry.py` (`PRED-C2-r46`) reads git objects at the entry's revision,
`corpus/SOURCES.md`, `corpus/lessons/round-46.md`, `corpus/README.md` and the ten pinned files under
`.ufo/waves/round-46/fetch/`, recomputes sha256 and locator lines, and writes nothing; it demands the census line
`hyprland input-device default_layout=us fallback_layout=us device_keys=47 scroll_factor_max=100 json_scroll_decimals=2 virtual_prefix=hl-virtual-keyboard` and binds twenty-eight surfaces to locators no wider than
30 lines.

The round-46 entry `corpus/knowledge/hyprland-input-devices-r46.md` lands with the data commit as source-read
knowledge of the owned plane, on the round-38 addendum's pattern: ten pinned upstream files — eight Hyprland files at
`efb50993`, hyprlang v0.6.8 `src/config.cpp` and the hyprland-wiki Keywords page — are read as bytes, and nothing is
connected, dispatched or re-read from the host, so the entry adds no write surface and no runtime capability.

**Declared limits.** A tool holding a model of the contract is an implementation of it (`c1-r46-devices.py:42`): the
fixtures are the contract's cases, not Hyprland's runtime. The C1 read-only clause is a PATH-lookup check, and three
shapes escape it: an absolute path to a real binary (the decoy lives on PATH only), the `--selftest` run, whose PATH
is `/usr/bin:/bin` (`:374-375`), and an AF_UNIX connect to the live compositor socket, which `--ro-bind / /` leaves
reachable because the tmpfs set hides only the repository and the lane (`:241-243`). So clause r is not evidence that a
scored tool ran nothing, and this refinement does not claim it is. No round-46 counter reads the host: every dump in a
fixture is synthesised, and C2's trust root is the ten pins.

### 2c. Insertion note (not part of the pasted text)

One thing the L1 should decide before keeping 2a and 2b as written: `PROVINCE.md:34` claims that "the inventory
above covers every tracked file under `tools/`…", and at this seat's tip the table (`:24-32`) holds nine rows while
`tools/` holds thirteen files — `mado-eventq.py`, `mado-options.py`, `mado-wsrules.py` and the round-45
`mado-monitors.py` have no row (`receipts/locators.txt` §E, `ls tools/`). Adding the round-46 row makes ten of
thirteen; the coverage sentence stays false either way. That is a pre-existing gap this seat does not repair — the L1
decides between adding the four rows and rewording the sentence.

**If a v2 counter set lands instead of the frozen v1.** Block 2's counter paragraph was written against the frozen
`c1-r46-devices.py` / `c2-r46-input-device-entry.py` / `c1-r46-fixtures.json`. An untracked v2 set
(`c1-r46-devices-v2.py`, `c1-r46-fixtures-v2.json`, `c2-r46-input-device-entry-v2.py`) appeared in the lane during this
seat and is still moving; this draft makes no claim about it. If the L1 freezes and lands a v2, swap both counter paths
and re-read four cells against the landed bytes before keeping the paragraph: the sandbox's tmpfs set
(`hidden_paths`), the `--selftest` environment's PATH, the fixture/generated counts, and the C2 census line and
surface count. The clause-r scope sentence in particular must describe the landing harness, not the v1's.

---

## Block 3 — optional routing and probe rows (only if the L1 keeps them in step with round 45)

Round 45 gave `mado-monitors.py` a Claim-first routing row (`SKILL.md:142-158`) and a Read-only-probes row
(`:204-225`) beside its prose section; without them the new section is unreachable from the two tables a fresh agent
starts at. Both rows below are in those tables' exact column shapes.

**Routing row — goes after `SKILL.md:158`** (last row, the `mado-geometry.py` row):

| Does each keyboard run the XKB names its config declares, and each mouse the scroll factor its `device` block sets? | two read-only inputs, no new verb: file bytes (the `input` and `device` lines) + hyprctl live (`devices -j`, which prints each keyboard's stored rules and each pointer's factor) | `hyprctl devices -j \| python3 tools/mado-devices.py --devices - --config <each file in the source chain>`; per-verdict licence and exit map in § "Input-device rules versus running devices" | `[OBS]` for both printed sides (the config values and the stored rules); the expected side is `[INF]` — a source re-implementation of the per-device lookup; which keymap a virtual keyboard really uses, and whether a layout types correctly, stay `[UNK]` |

**Probe row — goes after `SKILL.md:225`** (last row, the `mado-geometry.py` probe row):

| `hyprctl devices -j \| python3 tools/mado-devices.py --devices - --config ~/.local/share/omarchy/default/hypr/input.conf --config ~/.config/hypr/input.conf` | whether each keyboard's stored XKB names and each pointer's scroll factor are the ones the `input`/`device` config asks for: a read-only join of config bytes and one `devices` dump, per keyboard AGREE / DIFFER / FALLBACK / VIRTUAL, per mouse AGREE / DIFFER, per block MATCHED / NO_SUCH_DEVICE; `--selftest` | host run 2026-10-26 (`receipts/host-runs.txt`; the L1 single-file run is `receipts/live-devices-host-l1.txt`): nine keyboards `verdict=AGREE`, `name="hl-virtual-keyboard-fcitx5" … verdict=VIRTUAL`, four mice `scroll_factor=-1.00 reported=-1.00 verdict=AGREE`; `MADO_DEVICES: keyboards=10 agree=9 differ=0 fallback=0 virtual=1 mice=4 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK`, rc 0; per-verdict licence in § "Input-device rules versus running devices" |

---

## Block 4 — locator receipt (not SKILL text)

| locator | token found there (`grep -n`) |
|---|---|
| `Hyprland-InputManager.cpp:1226-1231` | the six `getDeviceString(devname, "kb_*", "input:kb_*")` reads |
| `Hyprland-InputManager.cpp:1213` | `void CInputManager::applyConfigToKeyboard` |
| `Hyprland-InputManager.cpp:1274` | `did not change` (the skip) |
| `Hyprland-InputManager.cpp:1286` | `setKeymap(IKeyboard::SStringRuleNames{…})` |
| `Hyprland-InputManager.cpp:1379-1382` | `deviceConfigExplicitlySet(devname, "scroll_factor")`, the 0..100 clamp, `std::nullopt` |
| `Hyprland-InputManager.cpp:2119-2130` | `getNameForNewDevice` and its `-N` duplicate suffix |
| `Hyprland-ConfigManager.cpp:1115` | `getConfigValueSafeDevice` |
| `Hyprland-ConfigManager.cpp:518` | `addSpecialCategory("device", {"name"})` |
| `Hyprland-ConfigManager.cpp:1196` | `deviceConfigExists` |
| `Hyprland-ConfigValues.cpp:272` | `input:kb_layout` default `us` |
| `Hyprland-ConfigValues.cpp:296` | `input:scroll_factor` (a separate global option) |
| `Hyprland-IKeyboard.cpp:60-64` | `setKeymap` and its `m_keymapOverridden` early return |
| `Hyprland-IKeyboard.cpp:101-116` | the compile failure, the rule reset and `m_currentRules.layout  = "us"` (`:113`) |
| `Hyprland-HyprCtl.cpp:770` | `"scrollFactor": {:.2f}` |
| `Hyprland-HyprCtl.cpp:788-792` | `rules`, `model`, `layout`, `variant`, `options` |
| `Hyprland-MiscFunctions.cpp:777-789` | `deviceNameToInternalString` (lower-case; space, newline, comma → `-`) |
| `Hyprland-protocols-VirtualKeyboard.cpp:12` | `name = "hl-virtual-keyboard"` |
| `Hyprland-VirtualKeyboard.cpp:41` | `m_keymapOverridden = true` |
| `mado-devices.py:19` | `It is a join, not a blame` |
| `mado-devices.py:26` | `starts no process and opens no socket` |
| `mado-devices.py:29-34` | the setup contract (`SETUP <reason>`, the four reasons) |
| `mado-devices.py:36-37` | files read in argument order |
| `mado-devices.py:71` | `a missing or non-string value never equals an expected name` |
| `mado-devices.py:80-89` | the output lines and the `V =` verdict chain |
| `mado-devices.py:87` | `an unmodelled line can change any expectation` |
| `mado-devices.py:99` | `MAX_BYTES = 1048576` |
| `mado-devices.py:126-130` | `os.open(path, os.O_RDONLY \| os.O_NONBLOCK)`, `S_ISREG`, `too_large` |
| `mado-devices.py:446` | `def selftest()` |
| `c1-r46-devices.py:9` | `revision-addressed git reads with ambient GIT_* removed` |
| `c1-r46-devices.py:29` | the marker-writing `hyprctl`/`libinput`/`journalctl`/`udevadm` decoys |
| `c1-r46-devices.py:42` | `a tool holding a model of the contract is an implementation of it` |
| `c2-r46-input-device-entry.py:8` | `nothing in the lane is` written |
| `c2-r46-input-device-entry.py:58` | `The twenty-eight surfaces` |

Quotes used above, all ≤ 25 words: "It is a join, not a blame" (`mado-devices.py:19`); "It reads files and standard
input only; it starts no process and opens no socket." (`:26`); "an unmodelled line can change any expectation"
(`:87`); "a missing or non-string value never equals an expected name" (`:71`); "a tool holding a model of the
contract is an implementation of it" (`c1-r46-devices.py:42`); "the inventory above covers every tracked file under
`tools/`" (`PROVINCE.md:34`); the census line (`entry.md:53`).
