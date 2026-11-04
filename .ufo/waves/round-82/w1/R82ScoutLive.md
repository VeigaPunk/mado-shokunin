# R82ScoutLive — live surface recon (round 82, w1)

Read-only live recon on the seat box: `hyprctl` captures, one bar-footprint join for DP-1, the
three round-82 tray runbook rows, and waybar's process state. No compositor verb that changes
state was issued; no mutating git command was run; nothing was written outside this seat
directory and `/fast/scratch/hyaku/mado-r82/R82ScoutLive/` (the scratch tree is deleted at the
end of the seat).

## Provenance

| item | value |
| --- | --- |
| lane working tree HEAD | `b6146ee69689bb4e19826bc18429b6ff77473341` ("round-82: the wave evidence ...") |
| freeze commit | `780c30fcae12d74ce8ab3b871a0888696c2415d9` — ancestor of HEAD: **yes** |
| diff freeze..HEAD | only `.ufo/waves/round-82/` evidence (`make-spec-r82.py`, receipts, `w1-spec.json`, `w1-dispatch.json`, `w1.ready`) — no instrument, no SKILL.md, no case file |
| `tools/mado-barfoot.py` | `380075284d7d5c6f56a82600935d512def617223be27f33241ff5dbcb0bcab59` = frozen `38007528…` **match** |
| `quality/counters/c1-r82-allocation-band.py` | `1e9f394df80284e78f1fdf3f24cb5e14d1e4091f4880ccc60a2a45060b54612d` = frozen `1e9f394d…` **match** |
| `quality/counters/c2-r82-runbook.py` | `1e8eb49928bfc9b8e5e1e72da74c0496cbe6d095fe3fdc72c479fffd80b3fb0f` = frozen `1e8eb499…` **match** |
| `.ufo/waves/round-82/controls/c1-cases-r82.json` | `e404bb3fa93d5f12338129adc8733574084e6fab2ee12fbb471dd45df94a315f` = frozen `e404bb3f…` **match** |
| `.ufo/waves/round-82/controls/c2-runbook-cases-r82.json` | `f64d7d5db40fc1da3d75c15315274264dfb53c38396135b978dff7b0b04b36d5` = frozen `f64d7d5d…` **match** |
| instrument version | `tools/mado-barfoot.py` reports `VERSION = "r82-v1"` |
| compositor | Hyprland 0.56.2, commit `efb50993780079460b0cbed1363e2166a2de1d9f` (matches the frozen `version` case) |

The working-tree instruments are byte-identical to the frozen hashes, so the rows executed below
are the committed rows even though HEAD has advanced past the freeze with evidence only.

## 1. Captures (redacted, saved in this seat dir)

| capture | file | bytes | sha256 |
| --- | --- | --- | --- |
| `hyprctl monitors -j` | `hyprctl-monitors-redacted.json` | 1514 | `fd21eb325f487d05608d154d2d18f848e3788a808039afe39f87a03f8c55a803` |
| `hyprctl layers -j` | `hyprctl-layers-redacted.json` | 544 | `15fb3e5fd9e2a775ebc96b84d0d54e2220d12c93698ef1437c5ba1a40d8803b3` |

Redaction applied before the bytes were written: every monitor `description`, `serial`, `make`
and `model` value is replaced by `<redacted: <field>>`. Verified mechanically against the raw
capture: `secret_value_leaks=0`, all four placeholders present, no `token`/`session_id`/`/home/…`
string in the saved bytes. The raw captures existed only in scratch and are deleted with it.

Monitor facts recorded (nothing else):

| name | reserved `[left, top, right, bottom]` | scale | transform | geometry |
| --- | --- | --- | --- | --- |
| `DP-1` | `[0, 26, 0, 0]` | `1` | `0` | 3440x1440 at `0,0` (focused) |

Layer census for `DP-1` (`layers` reply carries only `levels`):

| level | namespace | box `x,y,w,h` | pid |
| --- | --- | --- | --- |
| 0 (background) | `wallpaper` | `0,0,3440,1440` | `<pid>` |
| 1 (bottom) | — empty — | — | — |
| 2 (top) | `waybar` | `0,0,3440,26` | 1720 |
| 3 (overlay) | — empty — | — | — |

Namespace set is exactly `{wallpaper, waybar}` — no second top-level consumer is visible in the
capture, which is what makes the `EQ` below attributable. Only the `waybar` row's pid is quoted
(it is the §4 pid, the item that asks for it); the `wallpaper` row's pid is masked.

## 2. Bar-footprint join for DP-1

Declared config (written by this seat, saved as `waybar-config-26-top.json`; 202 bytes):
`name=waybar`, `layer=top`, `position=top`, `height=26`, `exclusive=true`, no margins, no
`output` key.

Invocation (frozen instrument, redacted captures, my config):

```
python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py \
  --config  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-82/w1/R82ScoutLive/waybar-config-26-top.json \
  --layers  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-82/w1/R82ScoutLive/hyprctl-layers-redacted.json \
  --monitors /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-82/w1/R82ScoutLive/hyprctl-monitors-redacted.json \
  --monitor DP-1
```

Output, verbatim:

```
MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=26 width=0 margins=0,0,0,0 exclusive=true
MADO_BARFOOT_STATIC: monitor=DP-1 top=0 right=0 bottom=0 left=0 source=none
MADO_BARFOOT_DECL: monitor=DP-1 box=0,0,3440,26 edge=top
MADO_BARFOOT_LIVE: monitor=DP-1 level=2 ns=waybar box=0,0,3440,26 entries=1
MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
EXIT=0
```

**RESULT line:** `MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN`
**Verdict: `CLEAN`** (exit 0).

No DIFFER: the modelled box `0,0,3440,26` is the live waybar box `0,0,3440,26`, and the modelled
band 26 (`height` + opposite margins, static reserve none) equals the live `reserved` top of 26,
so the whole reserved band is attributable to the declared bar. Note the config's `height=26` is
the seat's declared input (the seat writes the config); the live side is independently captured,
and this is one snapshot — any runtime change after the capture is outside the model.

## 3. Round-82 tray runbook rows (C2, three commands only)

All three commands were run live, read-only, at the same snapshot as §1/§2. Counts only; the
owner row's PID, user and connection are masked, so no PID is quoted next to a process name.

| row | command | exit | lines | matching row (masked) | shape verdict |
| --- | --- | --- | --- | --- | --- |
| `tray-owner` | `busctl --user list` | 0 | 119 (1 header + 118 data) | `org.kde.StatusNotifierWatcher <pid> waybar <user> <connection> user@<uid>.service - -` | **PASS** — one row, `tray-owner` regex `(?m)^org\.kde\.StatusNotifierWatcher\s+[1-9][0-9]*\s` matches; PID is a non-zero integer, process cell is `waybar`, 8 cells |
| `tray-interface` | `busctl --user introspect org.kde.StatusNotifierWatcher /StatusNotifierWatcher --no-pager` | 0 | 21 (1 header + 4 interface + 8 method + 3 property + 5 signal) | `org.kde.StatusNotifierWatcher interface - - -` | **PASS** — `tray-interface` regex `(?m)^org\.kde\.StatusNotifierWatcher\s+interface\s` matches |
| `tray-methods` | same introspect piped through `awk '$2=="method"'` | 0 | 8 | every row `.<Name> method <sig> <res> <flags>` | **PASS** — `tray-methods` `lines_shape` (`min_lines=2`, regex `^\.[A-Za-z]+\s+method\s+`): 8 ≥ 2 and 8/8 rows match |

Method table contents (names only, no PIDs): `.Introspect`, `.GetMachineId`, `.Ping`, `.Get`,
`.GetAll`, `.Set`, `.RegisterStatusNotifierHost`, `.RegisterStatusNotifierItem` — 2 of the 8 are
the watcher's own (`RegisterStatusNotifierHost`, `RegisterStatusNotifierItem`), the other 6 come
from the `org.freedesktop.DBus.{Introspectable,Peer,Properties}` interfaces the census lists.

Shape semantics were taken from the frozen instrument itself (`quality/counters/c2-r82-runbook.py`,
`matches()`: `re.search(value, stdout.rstrip("\n"))` for `regex`, and `all(pattern.match(line))`
plus `len(lines) >= min_lines` for `lines_shape`), not re-invented.

The ring is live-consistent: the watcher's bus-name owner is waybar, and waybar's layer surface
(§1) is the process that owns that bus name.

## 4. waybar process state (state pair)

| probe | result |
| --- | --- |
| `pgrep -x waybar` exit status | **0** |
| `pgrep -x waybar` PID | **1720** (exactly one match, no duplicate instance) |

Consistency: the `waybar` layer surface in the DP-1 capture carries pid 1720, i.e. the same
process holds the bus name, the layer surface and the reserved band measured above. (PID+name is
quoted only here, for waybar, because this item asks for that pair.)

## Axes and what was kept

- **Axes:** (a) does the live box equal the modelled box; (b) does the live `reserved` band equal
  the modelled band and is it attributable; (c) are the tray rows executable and shape-true on
  this box; (d) is waybar a single live owner.
- **Cheap cells run:** redaction self-check (0 leaks), instrument-hash check (5/5 frozen), freeze
  ancestry check, per-type census counts, masked owner-row field check, `pgrep` match count.
- **Kept because they improve an axis and harm none:** the `CLEAN` join (a, b), the three PASS
  shape verdicts under the instrument's own matchers (c), the single-owner state pair (d).
- **Not claimed:** this seat reproduces 3 of the 29 C2 rows live, not the 29-case measurement
  (that is the frozen receipt at `780c30fc…`), and it does not exercise C1's `--allocation`
  path (no dynamic-band case was run here; §2 uses a declared static height 26).

## Limits / unresolved

- One snapshot: any compositor or waybar change after the captures is outside the model; the
  `layers` reply carries no `exclusive` flag, so exclusivity is inferred from the bar's declared
  `exclusive=true` plus the observed `reserved` band, never read directly.
- The `layers` reply exposes only `levels` per monitor; the seat reports the namespace/box/pid
  cells it carries and nothing inferred beyond them.
- The declared side of §2 is the config this seat wrote (`height=26`, `top`), per the seat
  assignment; the user's own waybar config was not read.
- `availableModes`, `currentFormat` and similar cells were not needed for the join and are kept
  only as captured structure. The workspace cells are shape-only (`activeWorkspace.name` is a
  single digit, `specialWorkspace.name` is empty), so the saved capture carries no workspace
  content.

STATUS: ok
