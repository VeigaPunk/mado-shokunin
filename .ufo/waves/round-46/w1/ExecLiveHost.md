# ExecLiveHost — round 46 w1 — live read-only runs of the C1 reference on this host

Reference run: `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/l1-draft/mado-devices.py`
sha256 `b229efd08d2d329dd60ced114598943d0419dac2f3cf05b1f6c1eb506c49a33b` (recorded at `w1/ExecLiveHost/runs.txt:4`).
Host: Hyprland 0.56.2 `efb50993780079460b0cbed1363e2166a2de1d9f`, `Hyprlang: built against 0.6.8, system has 0.6.8` (`hyprctl version`;
pins match the fetch set). All commands read-only: `hyprctl version`, `hyprctl devices -j`, `hyprctl getoption <name> -j`.
No dispatch/keyword/reload/setprop, no socket of my own, no package transaction.

Receipt: `w1/ExecLiveHost/runs.txt` (304 lines; every case = command line, per-run dump size, stdout, exit code; the source graph
and the per-file greps are embedded at its end), plus `w1/ExecLiveHost/dup-main.txt` (duplicate/main analysis) and
`w1/ExecLiveHost/qcheck.py` with its output `w1/ExecLiveHost/quotes.txt` (28 fragment checks: every quoted line in this report
matched verbatim in `runs.txt` or the pinned fetch file — 28/28 PASS, 0 FAIL, `python3 -I qcheck.py` exit 0). Device names are kept as printed (product names); no serials, no
window titles, no home listings. Scratch `/fast/scratch/hyaku/mado-r46/ExecLiveHost` deleted at exit.

## 1. The config graph Hyprland actually reads (source order, globs expanded)

`~/.config/hypr/hyprland.conf:4-32` sources 19 files in this order (the expanded list is at the end of `runs.txt`):

```
omarchy/default/hypr/{autostart,bindings/media,bindings/clipboard,bindings/tiling-v2,bindings/utilities,envs,looknfeel,input,windows}.conf
~/.config/omarchy/current/theme/hyprland.conf
~/.config/hypr/{monitors,input,bindings,looknfeel,autostart}.conf
~/.local/state/omarchy/toggles/hypr/{flags,window-no-gaps}.conf      (the `*` glob, 2 files)
~/.config/hypr/{ai-usage,gkeep}.conf
```

Grep for `kb_`, `device`, `scroll_factor` over all 19: only two files carry input lines —
`~/.local/share/omarchy/default/hypr/input.conf:3-7` (`kb_layout = us`, `kb_variant =`, `kb_model =`, `kb_options = compose:caps`,
`kb_rules =`) and `~/.config/hypr/input.conf:10-11,34` (`kb_layout = br`, `kb_options = compose:caps`, and
`input:touchpad:scroll_factor = 0.4`). **No `device { }` block exists anywhere in the 19 files** (`grep -HnE '^[[:space:]]*device[[:space:]]*\{'`
over each → no match). That is why every block count below is `blocks=0 stale=0`.

## 2. Case table (full transcripts in runs.txt)

| case | what | exit | MADO_DEVICES line |
|---|---|---|---|
| 1 | `hyprctl devices -j \| … --devices - --config ~/.config/hypr/input.conf` | 0 | `keyboards=9 agree=9 differ=0 fallback=0 virtual=0 mice=4 mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK` |
| 2 | all 19 files, source order | **5** | `… unsupported=2 verdict=NOT_COMPARED` |
| 2b | the same 19 minus `envs.conf` | 0 | `… unsupported=0 … verdict=OK` |
| 2c/2d | 2b and 2 run on one identical dump (`devs.c6.json`) | 5 / 0 | `unsupported=2 NOT_COMPARED` / `unsupported=0 OK` |
| 3 | omarchy default `input.conf` **then** user `input.conf` | 0 | `keyboards=9 agree=9 … verdict=OK` |
| 1R | case 1 while the IME virtual keyboard exists | 0 | `keyboards=10 agree=9 … virtual=1 … verdict=OK` |
| 4 | scratch copy with `kb_layout = zz` | 1 | `agree=0 differ=9 … differ=layout … verdict=DIFFER` |
| 5 | `hyprland.conf` alone (source= not followed) | 1 | `agree=0 differ=9 … verdict=DIFFER` |
| S1 | synthetic dump: every keyboard `us`+4 empties, config `zz` | 1 | `agree=0 differ=0 fallback=9 … verdict=DIFFER` |
| S2 | synthetic: two `device` blocks (one real mouse, one fictional) | 1 | `mice_differ=0 blocks=2 stale=1 … verdict=DIFFER` |

Observed live truth behind the join: every keyboard prints `layout="br" options="compose:caps" variant="" model="" rules=""` and
`active_keymap="Portuguese (Brazil)"` (projection at `runs.txt:245-276`); every mouse prints `scrollFactor=-1.0`; the dump's
other lists are empty: `{'mice': 4, 'keyboards': 10, 'tablets': 0, 'touch': 0, 'switches': 0}` (`runs.txt:278`).
Corroboration from config side (read-only): `hyprctl getoption input:kb_layout -j` → `"str": "br", "set": true`;
`input:kb_options` → `"compose:caps"`; `input:scroll_factor` → `"float": 1.000000, "set": false`.

## 3. Answers to the questions asked

**(1) Single file → OK, 9/9 AGREE.** The reference's five-name comparison holds live: expected `br`/`compose:caps` from the
global `input:kb_*` options (no device block sets them) equals the printed rules on all nine keyboard nodes.
Pin chain: `Hyprland-InputManager.cpp:1229` (`getDeviceString(devname,"kb_layout","input:kb_layout")`),
`Hyprland-ConfigManager.cpp:1115-1121` (device block wins only when `m_bSetByUser`), `Hyprland-ConfigValues.cpp:272` (default `"us"`).

**(2) All sourced files, source order → NOT_COMPARED (exit 5).** `unsupported=2`, and the cause is exactly two lines:
`~/.local/share/omarchy/default/hypr/envs.conf:2` `# hyprlang noerror true` and `:4` `# hyprlang noerror false`
(`#[ \t]*hyprlang\b` → `unsupported`). **Causality is controlled**: cases 2c/2d run the 19 files and then the same 18 (envs.conf
omitted) against the **identical dump** `devs.c6.json` — `unsupported=2 verdict=NOT_COMPARED` exit 5 versus
`unsupported=0 verdict=OK` exit 0. Only that one file differs.
These directives gate `env =` lines, not input, but the tool's model is line-coarse — *any* directive anywhere poisons the whole join.
So on an omarchy host, the "join the real config graph" workflow cannot produce a verdict at all with the full source list.

Also worth stating plainly: **the tool does not follow `source =`.** Passing only `~/.config/hypr/hyprland.conf` (case 5) yields
`DIFFER` (9) with expected `us`/`""` — the tool's own docstring lists this under "a join, not a blame", and it is reproducible here.

**(3) omarchy default input.conf before the user's → the verdict does not change (OK, 9 AGREE).** The default at
`omarchy/default/hypr/input.conf:3-7` sets `us`/`compose:caps`; the user file at `~/.config/hypr/input.conf:10-11` later
overwrites `kb_layout` to `br`, so the effective global (confirmed by `getoption`: `br`, `set: true`) is unchanged and every
keyboard still AGREEs. Converse bisect: the omarchy default **alone** predicts `us` against the printed `br` → `DIFFER` 9
(per-file bisect at `runs.txt:283-304`; the omarchy default alone is `runs.txt:293`, exit 1, `differ=9`). The user file is what makes the host agree; the default contributes nothing to the verdict.

**(4) `kb_layout = zz` → DIFFER, not FALLBACK — and the tool cannot observe a FALLBACK.** With a scratch copy carrying
`kb_layout = zz` against the *current* dump the tool reports `differ=layout verdict=DIFFER` (exit 1): that is the
config-vs-**running**-compositor divergence, because nothing has reloaded — the live keyboards still print `br`. What a typo
looks like *after* a reload is the compositor's own reset: `Hyprland-IKeyboard.cpp:107-113` clears `rules/model/variant/options`
and sets `layout = "us"` when the keymap fails to compile, and `hyprctl devices -j` prints those stored rules
(`Hyprland-HyprCtl.cpp:786-797`). Synthetic S1 (all keyboards rewritten to `us` + four empties) classifies each as
`fallback=9` and the top verdict is `DIFFER` (fallback counts into the DIFFER rule), exit 1. **The tool predicts but never observes
this: it can only label FALLBACK when the dump it is handed already prints `us`+empty, and then it cannot tell a failed reload
from a config that genuinely says `us`.** No reload was attempted (host guard), so no live FALLBACK was produced.

## 4. Duplicates and the `main` keyboard

**Does `hyprctl devices -j` list any device twice? No.** 13 elements without the IME keyboard, 14 with it; all distinct, 0 exact
duplicates in both dumps (`dup-main.txt`). What repeats is the *base* product name, resolved by the compositor's suffix rule
(`Hyprland-MiscFunctions.cpp:777` `deviceNameToInternalString`, `Hyprland-InputManager.cpp:1141` `getNameForNewDevice`):

| shared base | the two (or four) printed names | lists |
|---|---|---|
| `razer-razer-deathadder-v2` | `razer-razer-deathadder-v2` / `…-1` / `…-keyboard` / `…-keyboard-1` | mouse, **keyboard**, keyboard, **mouse** |
| `hp--inc-hyperx-alloy-origins-core-consumer-control` | `…-consumer-control` / `…-consumer-control-1` | keyboard / mouse |
| `power-button` | `power-button` / `power-button-1` | keyboard / keyboard |

Note the cross-class collision: a keyboard node named `razer-razer-deathadder-v2-1` and a *mouse* node named
`razer-razer-deathadder-v2-keyboard-1` come from the same physical mouse (its HID keyboard interface), and the `-1` is assigned
per internal-name collision, not per class. A `device { name = … }` block written against one of them silently re-targets the other
if the suffix is dropped — the tool's `MATCHED/NO_SUCH_DEVICE` is name-exact, so it would say `MATCHED` for whichever node it names
and never warn about the twin.

**`main`:** there are two states, and it is not the physical keyboard.
- without the IME keyboard: `main: true` on **`power-button-1`** (a power-button node), while the actual typing keyboard
  `hp--inc-hyperx-alloy-origins-core` is `main: false`.
- with the IME keyboard (`hl-virtual-keyboard-fcitx5` present): `main: true` on **`hl-virtual-keyboard-fcitx5`**.

`main` is `k->m_active` (`Hyprland-HyprCtl.cpp:797`). The reference ignores the field — correct for its claims — but anyone reading
"the main keyboard" off this dump on this host gets the power button or the IME.

## 5. Live drift: the device set is not stable (affects any census that hard-codes counts)

`hl-virtual-keyboard-fcitx5` (`Hyprland-VirtualKeyboard.cpp`, prefix `hl-virtual-keyboard`) comes and goes with the IME's state:

- earlier dumps, `keyboards=9 virtual=0`: `devs.json` (my first `hyprctl devices -j`) and `devs.c1..c4`, `devs.s1`, `devs.s2`;
- a few minutes later, six consecutive ~0.4 s polls (all identical): `10 ['hl-virtual-keyboard-fcitx5']` every time, and the scripted cases that
  followed (`devs.c5..c7`) all carry it: `keyboards=10 virtual=1`;
- case 1R on such a dump: `keyboards=10 agree=9 differ=0 virtual=1 … verdict=OK` exit 0, and the VIRTUAL line is
  `name="hl-virtual-keyboard-fcitx5" block=no layout="br" variant="" options="compose:caps" model="" rules="" kb_file=- differ=- verdict=VIRTUAL`
  — the vk prints the configured rules, so its printed rules do not witness the client keymap it actually uses (the docstring says
  this; the live line shows a VIRTUAL that would otherwise have "AGREEd").

Consequence for C1: the *keyboard count* in the summary line (`keyboards=9` vs `10`) and `virtual=0|1` depend on whether fcitx5 holds
its vk at dump time, while the top verdict stays `OK` (VIRTUAL never counts as differ). Any operability check or fixture that pins
`keyboards=9` is timing-fragile on this host; the verdict is not. This also reproduces the L1 live receipt
(`receipts/live-devices-host-l1.txt`: 9 AGREE, 1 VIRTUAL, OK): I observed exactly that shape (case 1R, 10 keyboards) *and* the
9-keyboard shape (cases 1-4) on the same host minutes apart.

## 6. Mouse half of C1 has no live signal on this host

All four mice print `scrollFactor = -1.0`, which is `m->m_scrollFactor.value_or(-1)` (`Hyprland-HyprCtl.cpp:770`) with the optional
unset: `m_scrollFactor` is assigned only when `deviceConfigExplicitlySet(devname,"scroll_factor")` holds, else `std::nullopt`
(`Hyprland-InputManager.cpp:1379-1382`; the clamp is `std::clamp(getDeviceFloat(devname,"scroll_factor","input:scroll_factor"),0.F,100.F)`).
The host has no `device` block and no touchpad device (`'touch': 0` in the dump, `runs.txt:278`), so `input:touchpad:scroll_factor = 0.4`
(`~/.config/hypr/input.conf:34`) reaches nothing, and `input:scroll_factor` is `set: false` (getoption). Therefore every mouse can only
trivially AGREE at `-1.00`, and the tool's clamp/DIFFER and `MATCHED/NO_SUCH_DEVICE` branches are **unexercised live**. They were
exercised only synthetically (S2: `blocks=2`, one `MATCHED keys=2`, one `NO_SUCH_DEVICE keys=1` → `stale=1`, top verdict `DIFFER`
because differ is tested before STALE_BLOCK). S2 is a fixture built in scratch from the real dump — it is not host state.

## 7. What this supports / what it does not establish

Supports: C1's join semantics on the keyboard-global path (9/9 AGREE, exit 0), its `VIRTUAL` classification on a real
`hl-virtual-keyboard-fcitx5`, its `NOT_COMPARED` exit 5 with the documented cause, its `stale`/block bookkeeping on real names, and
an empty stderr with the documented exit codes (0/5/1) — `runs.txt` records a `[stderr]` block only when stderr is non-empty, and it
contains none (0 occurrences over every case). It also confirms the docstring's two operational caveats live: no `source =`
following (case 5) and "a DIFFER may come from a config file not passed".

Does not establish: FALLBACK observed live (none produced — no reload), the mouse scroll-factor branch live (only `-1.00`), or
device-block precedence live (no block exists). Those rest on the pins
(`Hyprland-IKeyboard.cpp:107-113`, `Hyprland-InputManager.cpp:1379-1382`, `Hyprland-ConfigManager.cpp:1115-1121`) plus the
reference's fixtures, not on this seat.

Ranked observations, in case the claims' wording is revisited: (a) the full-source join is `NOT_COMPARED` on any omarchy host because
of two `# hyprlang noerror` lines in `envs.conf` — the tool's "any directive poisons the join" rule is coarse relative to hyprlang,
which scopes `noerror` to the lines between the pair; (b) device-set drift (`keyboards` 9↔10 via the IME vk) makes count-based
expectations fragile; (c) the internal-name twin collisions (`-1`/`-keyboard` across classes) make a name-exact `device` block a
silent mis-target risk that the tool cannot flag.

## 8. Nothing changed

No tracked file in the lane was created, edited or deleted; no git/jj mutation anywhere (all git calls were read-only `log`/`status`
reads from the lane before I switched to absolute paths); no package transaction; no host service touched. Only
`w1/ExecLiveHost/{runs.txt,dup-main.txt,quotes.txt,qcheck.py}` (plus this report) exist from this seat. Tooling installed: none (python3 -I and the host's
`hyprctl` sufficed; nothing added).
