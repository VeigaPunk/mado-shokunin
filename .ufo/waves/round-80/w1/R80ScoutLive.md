# Seat R80ScoutLive — live surface recon for the C1 join (round 80, one v1 wave)

Scope: read-only probes of the host's layer-surface state on 2026-11-04, joined with the frozen
`tools/mado-barfoot.py` (`r80-v1`, sha256 `c3eb5fbe…`). No config write, no compositor mutation, no
service action, no git mutation. Every command below was run from the lane root
`/home/vgpnk/Projects/shokunin/mado-shokunin` with artifacts written only into this seat's
directory `.ufo/waves/round-80/w1/R80ScoutLive/`.

## 1. Captured bytes (paths, hashes, commands)

All four captures live in `.ufo/waves/round-80/w1/R80ScoutLive/`:

| file | sha256 | command | rc |
|---|---|---|---|
| `monitors.json` | `e732af3461737da6f7ac920bdd716a6c7b7f2b37770bf58a2f3c9aa469103f66` | `hyprctl monitors -j` | 0 |
| `layers.json` | `46eb2481ed664862c53c93f76e52cee31753519c4e0587af5d5928c73fd6f53c` | `hyprctl layers -j` | 0 |
| `waybar-config.jsonc` | `a408a33df48a39dc16214124dd0b86d6ab03e13802bac173146ae8a858aae829` | `cp ~/.config/waybar/config.jsonc` (read-only source) | 0 |
| `surfaces-real.json` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | bytes `[]` (the honest real declaration, see §3) | — |
| `surfaces-wallpaper.json` | `50f248e82646134dbd650c195fa1d27467eea769895367760c7f7a935881f0a9` | wallpaper as `exclusive:-1` (see §4) | — |
| `surfaces-wallpaper-excl0.json` | `a8530388980049f4c5b431d31c7a6e16279832d72ae31fdaaf88456a779cd207` | wallpaper as `exclusive:0` (discrimination probe, §5) | — |

The two `hyprctl` captures are **byte-identical** to the hashes the lane already carries:
`monitors.json` = `e732af34…` and `layers.json` = `46eb2481…`, the same values cited in
`corpus/knowledge/bar-footprint-r77.md` row 7 (`fetch/live-monitors-r77.json`,
`fetch/live-layers-r77.json`). The host surface state has not drifted between that capture and this
one (both 2026-11-04).

Version pin re-confirmed against the model's target:

```
$ hyprctl version | head -n 1
Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).
rc=0
```

## 2. Registration expectation of the verdict

The instrument's registration names its exit map in the module docstring (`tools/mado-barfoot.py:75`):

```
Exit map: 0 CLEAN · 1 DIFFER · 2 SETUP/ERROR · 3 NOT_FORMED (NO_LAYER/UNMODELLED/NO_BAR).
```

`quality/tool-ledger.md:175` registers the module (row text still scoped "rounds 77-79 C1"; the r80
counting command is the separate row at `:182`), and `quality/tool-ledger.md:182` registers
`quality/counters/c1-r80-multisurface.py` as the r80 scorer of exactly this composition model.

The **expected verdict for this host** is stated twice:

- `corpus/knowledge/bar-footprint-r77.md` row 8: the live join "prints `box=MATCH reserved=EQ
  band=26 expected=26 verdict=CLEAN`".
- `corpus/knowledge/bar-footprint-composition-r80.md` §7 limit 1: today's host "has one exclusive
  surface (`waybar`) plus `wallpaper` at level 0; the live join with both declared
  (`.ufo/waves/round-80/receipts/live-join-r80.txt`) reads `boxes=MATCH,MATCH … attributed=26
  gt=0,26,0,0 CLEAN`".

So the registered expectation is **`CLEAN` on both the single-surface and the composition run**, with
`DIFFER` (rc 1) reserved for a real disagreement and `GT` explicitly *admissible* when an undeclared
consumer reserves more than the model accounts for (`corpus/knowledge/bar-footprint-composition-r80.md`
§6).

## 3. Run 1 and Run 2 — the live join, and the empty `--surfaces` refusal

Run 1, exactly as the seat specifies:

```
$ python3 -I tools/mado-barfoot.py --config .ufo/waves/round-80/w1/R80ScoutLive/waybar-config.jsonc \
    --layers .ufo/waves/round-80/w1/R80ScoutLive/layers.json \
    --monitors .ufo/waves/round-80/w1/R80ScoutLive/monitors.json --monitor DP-1
MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=26 width=0 margins=0,0,0,0 exclusive=true
MADO_BARFOOT_STATIC: monitor=DP-1 top=0 right=0 bottom=0 left=0 source=none
MADO_BARFOOT_DECL: monitor=DP-1 box=0,0,3440,26 edge=top
MADO_BARFOOT_LIVE: monitor=DP-1 level=2 ns=waybar box=0,0,3440,26 entries=1
MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
rc=0
```

This reproduces the registered expectation and the first block of
`.ufo/waves/round-80/receipts/live-join-r80.txt` line for line.

Run 2, with the `--surfaces` declaration that describes **the real extras**:

```
$ printf '[]' > …/surfaces-real.json
$ python3 -I tools/mado-barfoot.py --config …/waybar-config.jsonc --layers …/layers.json \
    --monitors …/monitors.json --monitor DP-1 --surfaces …/surfaces-real.json
MADO_BARFOOT: ERROR (stage=setup the surfaces declaration is empty)
rc=2
```

**This is the honest result, and it is a real limit in the declaration grammar**: the real extra set
is empty (§6), and `--surfaces` refuses an empty list (`tools/mado-barfoot.py:1385-1386`: `if not
surfaces: raise Setup("the surfaces declaration is empty")`). The flag therefore has no way to say
"the bar is the only surface"; that statement is expressed by *omitting* the flag, which selects the
single-surface branch. Run 1 is the correct live join for today's host.

## 4. Run 3 — composition run with the real wallpaper surface declared

`wallpaper` is a real observed surface (level 0, box `0,0,3440,1440`, pid 1722). The seat excludes
`waybar`/`wallpaper` from the *unknown-namespace* census, but the registration's §7.1 expectation is
precisely a composition run with `wallpaper` declared, so it is checked here against live bytes.
Declaration used: `{"namespace":"wallpaper","level":0,"position":"top",
"anchor":["top","bottom","left","right"],"exclusive":-1,"margins":{…0},"height":0,"width":0,"order":0}`.

```
$ python3 -I tools/mado-barfoot.py --config …/waybar-config.jsonc --layers …/layers.json \
    --monitors …/monitors.json --monitor DP-1 --surfaces …/surfaces-wallpaper.json
MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=26 width=0 margins=0,0,0,0 exclusive=true surfaces=2
MADO_BARFOOT_STATIC: monitor=DP-1 top=0 right=0 bottom=0 left=0 source=none
MADO_BARFOOT_DECL: monitor=DP-1 level=2 ns=waybar box=0,0,3440,26 anchor=top+left+right zone=26
MADO_BARFOOT_LIVE: monitor=DP-1 level=2 ns=waybar box=0,0,3440,26 entries=1
MADO_BARFOOT_ATTR: monitor=DP-1 level=2 ns=waybar edge=top contribution=26 box=0,0,3440,26
MADO_BARFOOT_DECL: monitor=DP-1 level=0 ns=wallpaper box=0,0,3440,1440 anchor=top+bottom+left+right zone=-1
MADO_BARFOOT_LIVE: monitor=DP-1 level=0 ns=wallpaper box=0,0,3440,1440 entries=1
MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH boxes=MATCH,MATCH reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
rc=0
```

Byte-identical to the second block of `.ufo/waves/round-80/receipts/live-join-r80.txt`. The
registered `boxes=MATCH,MATCH … attributed=26 gt=0,26,0,0 CLEAN` holds on today's host.

### What in that declaration is observed and what is inferred

- **`exclusive: -1` is pinned by the observed box** (INF, arithmetic on OBS bytes). Under the
  composition model every surface with `exclusive >= 0` arranges against the *running* usable box,
  which the bar has already shrunk to y=26; with `exclusive: -1` it arranges against the full monitor
  box (`tools/mado-barfoot.py:684`). Run 4 (§5) shows the alternative: `exclusive: 0` yields
  `0,26,3440,1414` and `verdict=DIFFER`. Only `-1` reproduces the observed `0,0,3440,1440`.
- **The anchor set is NOT recoverable** and must not be read as observed. The `hyprctl layers -j`
  entry carries no anchor field (`corpus/knowledge/bar-footprint-r77.md` row 7), and under a zero
  declared width and height this model spans the bounds on both axes regardless of the anchor set,
  so every anchor choice produces the same box. The declaration uses all four because that is the
  conventional full-output set, not because the reply proves it.

## 5. Run 4 — discrimination probe (same real bytes, `exclusive: 0`)

```
$ … --surfaces …/surfaces-wallpaper-excl0.json
MADO_BARFOOT_DECL: monitor=DP-1 level=0 ns=wallpaper box=0,26,3440,1414 anchor=top+bottom+left+right zone=0
MADO_BARFOOT_LIVE: monitor=DP-1 level=0 ns=wallpaper box=0,0,3440,1440 entries=1
MADO_BARFOOT_RESULT: monitor=DP-1 box=DIFFER boxes=MATCH,DIFFER reserved=EQ band=26 expected=26 attributed=26 gt=0,26,0,0 attr=0,26,0,0 ls=VALID verdict=DIFFER
MADO_BARFOOT: verdict=DIFFER
rc=1
```

The join moves from `CLEAN` to `DIFFER` on a one-field change against the same captures, which is the
`DIFFER` half of the exit map exercised on live bytes. This is a parameter probe of the join, not a
claim about host state.

## 6. What the host actually has on each level today

From `layers.json` and `monitors.json` (single monitor, `nmon=1`):

| level | name | entries | namespace | box (x,y,w,h) | pid |
|---|---|---|---|---|---|
| 0 | background | 1 | `wallpaper` | `0,0,3440,1440` | 1722 |
| 1 | bottom | 0 | — | — | — |
| 2 | top | 1 | `waybar` | `0,0,3440,26` | 1720 |
| 3 | overlay | 0 | — | — | — |

Both surfaces are children of the compositor itself:

```
$ ps -p 1665 -o pid,ppid,comm,args --no-headers
1665 1658 Hyprland Hyprland --watchdog-fd 4
$ ps -p 1720,1722 -o pid,ppid,comm,args --no-headers
1720 1665 waybar  /usr/bin/waybar
1722 1665 swaybg  /usr/bin/swaybg -i /home/vgpnk/.config/omarchy/current/background -m fill
$ pgrep -a waybar
1720 /usr/bin/waybar        # exactly one bar process
```

Monitor: `DP-1 3440x1440`, `scale 1`, `transform 0`, `reserved [0, 26, 0, 0]`, i.e. left 0, top 26,
right 0, bottom 0 (the reply's left, top, right, bottom order).

**The overlay level (3) is empty, and so is the bottom level (1).** There are exactly two layer
surfaces on this host: `waybar` and `wallpaper`. The unknown-namespace set — every namespace that is
neither `waybar` nor `wallpaper` — is **empty**, so there is no surface entry to write for it. I
cannot justify any anchor or exclusive value for a surface that does not exist, and I have not
invented one.

### Is there a second exclusive consumer? No.

Stated exactly: **the host has no second exclusive layer surface.** Evidence, in three independent
readings of the same capture:

1. Levels 1 and 3 carry zero entries; level 0 carries only `wallpaper`, level 2 only `waybar`.
2. `reserved` is `[0,26,0,0]`: the left, right and bottom bands are exactly 0. A positive exclusive
   zone on any surface anchored to those edges would have raised them.
3. The top band is 26, exactly the bar's height (26) and exactly the model's `expected=26` with zero
   margins; there is no residual to attribute to anyone else.

This is the honest state the C1 limit statement is written against, and it matches
`corpus/knowledge/bar-footprint-composition-r80.md` §7 limit 1. The r80 composition path is
exercised on this host (two surfaces, `boxes=MATCH,MATCH`) but **no second exclusive band exists to
exercise**, so the `attr=` vector can never be checked against a per-surface figure the compositor
does not print.

## 7. What the join prints for the unattributed part of `reserved`

Two branches, both observed above:

- **Single-surface branch (run 1)** prints no attribution fields at all: `RESULT: … reserved=EQ
  band=26 expected=26 verdict=CLEAN`. The unattributed remainder is `band - expected = 26 - 26 = 0`.
- **Composition branch (runs 3-4)** prints the compositor's total and the model's attribution as two
  four-value vectors in the reply's left, top, right, bottom order:
  `gt=0,26,0,0 attr=0,26,0,0`. The unattributed part is the componentwise difference
  `gt - attr = 0,0,0,0` — **nothing on this host is unattributed**; the entire `[0,26,0,0]` band is
  accounted for by the one `waybar` surface (`ATTR: ns=waybar edge=top contribution=26`).
- `expected=`/`attributed=` are scalars for the bar's own edge only (`26`/`26`), which is why both
  are printed beside the vectors.

Source for the field set: `tools/mado-barfoot.py:795-800` (`attributed=%d gt=%s attr=%s ls=%s
verdict=%s`), matching `corpus/knowledge/bar-footprint-composition-r80.md` §6.

## 8. C2 runbook row `hypridle-is-active` — the real answer here

```
$ systemctl --user is-active hypridle
inactive
rc=3
$ pgrep -a hypridle
(none)  rc=1
$ systemctl --user show hypridle -p LoadState -p ActiveState -p UnitFileState --no-pager
LoadState=loaded
ActiveState=inactive
UnitFileState=disabled
```

The real answer is `inactive` with exit status **3** — inside the frozen case's enum
(`active, activating, deactivating, failed, inactive, reloading, unknown`) and exactly one of its
frozen negatives is the mismatched-pair `out=inactive rc=0`, which this measurement is not. hypridle
is installed (`/usr/bin/hypridle`) but not running and not enabled.

A second unit that **is** `active`, with exit status 0:

```
$ systemctl --user is-active wayland-wm@hyprland.desktop.service
active
rc=0
$ systemctl --user is-active pipewire.service
active
rc=0
$ systemctl --user is-active swayosd-server.service
active
rc=0
```

`wayland-wm@hyprland.desktop.service` is the graphical session's own unit (`active running`), so the
pair (`active`, 0) versus (`inactive`, 3) is available on this host as a discriminating row.

## 9. Instrument integrity (read-only check, nothing rewritten)

```
$ sha256sum tools/mado-barfoot.py quality/counters/c1-r80-multisurface.py \
    quality/counters/c2-r80-runbook.py \
    .ufo/waves/round-80/controls/c1-cases-r80.json \
    .ufo/waves/round-80/controls/c2-runbook-cases-r80.json
c3eb5fbef794c92ba45adc85ed1dcd18c505a2776a3fb1db34742a6eed27fa99  tools/mado-barfoot.py
6268667c1c78ffac3d87c573e3bb9bb29e8a2c4d5b43ad88e91548c145c5f2fe  quality/counters/c1-r80-multisurface.py
462287fbf3b637e5d35eea5bbfe810bea638fa8e02045ee9c6a66f36ce47bba3  quality/counters/c2-r80-runbook.py
17c27157a9b0c293dbd07d56d67673cb061e808b6abcd1bb31f16ff6c15fd6ed  .ufo/waves/round-80/controls/c1-cases-r80.json
f1dfb5f4c66a46e456f7da2d56709385cf6de2d3801463702fbb0a41911cc8cf  .ufo/waves/round-80/controls/c2-runbook-cases-r80.json
```

All five match the frozen prefixes in the seat brief. Nothing was rewritten; the seat never ran the
counting commands (that is the executors' job) and never touched a frozen instrument.

## 10. Findings, ranked

1. **The live join is `CLEAN` on both registered runs** (single-surface and composition), rc 0,
   byte-identical to `.ufo/waves/round-80/receipts/live-join-r80.txt`. The registration's §7.1
   expectation is satisfied by today's host.
2. **No second exclusive consumer exists on this host**, stated directly: two layer surfaces total
   (`waybar` level 2 at `0,0,3440,26` pid 1720; `wallpaper` level 0 at `0,0,3440,1440` pid 1722),
   levels 1 and 3 empty, and `reserved [0,26,0,0]` fully consumed by the bar's 26 px. The C1 limit
   statement's premise has no live instance today.
3. **`--surfaces` cannot express "no extras"**: an empty declaration is refused
   (`stage=setup the surfaces declaration is empty`, rc 2, `tools/mado-barfoot.py:1385-1386`). The
   honest live second run is therefore the *omitted-flag* run, not an empty declaration.
4. **Nothing in the `reserved` array is unattributed**: composition run prints
   `gt=0,26,0,0 attr=0,26,0,0`, difference `0,0,0,0`.
5. **`hypridle` is `inactive`, rc 3** (loaded, disabled, no process), and a contrasting active unit
   exists (`wayland-wm@hyprland.desktop.service`, rc 0) — the C2 `is-active` row's real answer here.
6. **Capability limit on the capture**: `hyprctl layers -j` carries no anchor and no exclusive-zone
   field, so a surface's declaration can be *pinned* only where its box changes with the field
   (wallpaper pins `exclusive: -1`), never for its anchor set.

## 11. Cleanup

Scratch root `/fast/scratch/hyaku/mado-r80/R80ScoutLive/` was created empty and never used (all
artifacts live in the seat directory); it was removed with `rm -rf` — nothing of this seat remains
under `/fast/scratch`. No file outside this seat's directory was created or modified.

STATUS: ok — nothing missing; the only unobservable item (a second exclusive consumer's per-surface
band) is absent from the host by measurement, not by omission.
