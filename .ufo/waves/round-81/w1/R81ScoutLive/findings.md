# R81ScoutLive — command log and findings

Seat: `R81ScoutLive`, round 81, lane `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Read-only live recon. No mutating git/jj command, no pacman transaction, no compositor verb that
changes state, no install.

## Files read (via read, not shell)

- `/home/vgpnk/.omp/agent/RULES.md` (full)
- `.ufo/waves/round-81/fetch/S478.bin:1-90`
- `.ufo/waves/round-80/fetch/S470.bin:2587-2671`
- `tools/mado-barfoot.py:380-470`, `:560-700`, `:900-1010`, `:1400-1483`

## Commands, exact argv, and the lines that matter

### 0. Lane state before the seat started

```
$ ls -la /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/w1/ 2>&1
ls: cannot access '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/w1/': No such file or directory
```
The seat directory did not exist; it was created by this seat (next command).

### 1. Seat + scratch dirs, compositor probe

```
$ mkdir -p /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/w1/R81ScoutLive && \
  mkdir -p /fast/scratch/hyaku/mado-r81/R81ScoutLive && echo OK
OK
$ which hyprctl
/usr/bin/hyprctl
$ hyprctl version 2>&1 | head -5
Hyprland 0.56.2 built from branch v0.56.2 at commit efb50993780079460b0cbed1363e2166a2de1d9f clean ([gha] Nix: update inputs).
Date: Wed Aug 5 14:13:21 2026
Tag: v0.56.2, commits: 7661
$ echo "WAYLAND_DISPLAY=$WAYLAND_DISPLAY HYPRLAND_INSTANCE_SIGNATURE=$HYPRLAND_INSTANCE_SIGNATURE XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR"
WAYLAND_DISPLAY=wayland-1 HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1793632040_1005787507 XDG_RUNTIME_DIR=/run/user/1000
```

### 2. Capture

```
$ cd /fast/scratch/hyaku/mado-r81/R81ScoutLive && hyprctl monitors -j > monitors.raw.json 2>monitors.err
$ echo "rc=$?"
rc=0
$ hyprctl layers -j > layers.raw.json 2>layers.err
$ echo "rc=$?"
rc=0
$ wc -c monitors.raw.json layers.raw.json
1339 monitors.raw.json
 748 layers.raw.json
$ cat monitors.err layers.err
(no output)
```

### 3. Instrument usage and identity

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py --help 2>&1 | head -60
usage: mado-barfoot.py [-h] [--config CONFIG] [--layers LAYERS]
                       [--monitors MONITORS] [--monitor MONITOR]
                       [--rules RULES] [--surfaces SURFACES] [--selftest]
$ sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py
a129a435572805c3ae7730714f0dafdea2b9a7e420f53f0d109dc2d5f57d1230  /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py
```

`a129a435…` equals the frozen `r81-v1` digest from the dispatch.

### 4. Raw capture inspection

```
$ python3 -c "import json; m=json.load(open('monitors.raw.json')); print(json.dumps(m,indent=1)[:4000]); print('=== LAYERS ==='); l=json.load(open('layers.raw.json')); print(json.dumps(l,indent=1)[:4000])"
```
Matter lines from that dump:

```
  "id": 1, "name": "DP-1", "width": 3440, "height": 1440, "x": 0, "y": 0,
  "scale": 1, "transform": 0, "reserved": [0, 26, 0, 0], "disabled": false,
  "layers": {"0": [{"x": 0, "y": 0, "w": 3440, "h": 1440, "alpha": 1, "namespace": "wallpaper", "pid": 1722}],
             "1": [], "2": [{"x": 0, "y": 0, "w": 3440, "h": 26, "alpha": 1, "namespace": "waybar", "pid": 1720}],
             "3": []}
```

### 5. Redaction (before anything was saved to the seat dir)

```
$ cd /fast/scratch/hyaku/mado-r81/R81ScoutLive && python3 - <<'PY'
import json, collections
raw = json.load(open('monitors.raw.json'), object_pairs_hook=collections.OrderedDict)
REDACT = ("description", "serial", "make", "model")
...
PY
wrote monitors.redacted.json
$ grep -n -E 'redacted|description|serial|"make"|"model"' monitors.redacted.json
5:  "description": "<redacted: description>",
6:  "make": "<redacted: make>",
7:  "model": "<redacted: model>",
8:  "serial": "<redacted: serial>",
$ wc -c monitors.raw.json monitors.redacted.json
1339 monitors.raw.json
1343 monitors.redacted.json
```

Field order preserved; only the four identity values replaced (`"<redacted: <field>>"`), so the
file grew by exactly the 4-byte-per-field difference. Leak check:

```
$ grep -n -E '508AZFMF7323|LG Electronics|ULTRAWIDE' monitors.redacted.json
leak_grep_rc=1
```

### 6. Save captures to the seat dir and run the join

```
$ cp monitors.redacted.json layers.raw.json /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/w1/R81ScoutLive/
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py \
    --monitors /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/w1/R81ScoutLive/monitors.redacted.json \
    --layers   /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-81/w1/R81ScoutLive/layers.raw.json \
    --config   /home/vgpnk/.config/waybar/config.jsonc
MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=26 width=0 margins=0,0,0,0 exclusive=true
MADO_BARFOOT_STATIC: monitor=DP-1 top=0 right=0 bottom=0 left=0 source=none
MADO_BARFOOT_DECL: monitor=DP-1 box=0,0,3440,26 edge=top
MADO_BARFOOT_LIVE: monitor=DP-1 level=2 ns=waybar box=0,0,3440,26 entries=1
MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
rc=0
```

Flag set: `--config --layers --monitors` only. **No `--surfaces`** (the layers reply has no
declared `anchor`/`exclusive`/`margins`, so an extras declaration cannot be derived without
inventing it; levels 1 and 3 are empty anyway). **No `--rules`** in this run (cross-check in §8).
`--monitor` omitted: one monitor in the reply, auto-selected (`tools/mado-barfoot.py:1454-1459`).

The result was also saved verbatim to
`.ufo/waves/round-81/w1/R81ScoutLive/join-live-receipt.txt`.

### 7. Census, key set, pids

```
$ python3 -c "import json; d=json.load(open('layers.raw.json')); keys=sorted({k for m in d.values() for lv in m['levels'].values() for s in lv for k in s}); print('union of keys:', keys); ..."
union of keys: ['address', 'alpha', 'h', 'namespace', 'pid', 'w', 'x', 'y']
monitor DP-1 level 0 entries 1
   ns=wallpaper box=0,0,3440,1440 alpha=1 pid=1722
monitor DP-1 level 1 entries 0
monitor DP-1 level 2 entries 1
   ns=waybar box=0,0,3440,26 alpha=1 pid=1720
monitor DP-1 level 3 entries 0
fractional coords: []
$ for p in 1720 1722; do echo -n "pid $p: "; cat /proc/$p/comm 2>&1; done
pid 1720: waybar
pid 1722: swaybg
$ pgrep -x waybar | tr '\n' ' '; echo; echo "count=$(pgrep -x waybar | wc -l)"
1720 
count=1
```

### 8. Host rules — does a static reserve exist?

```
$ grep -rn 'addreserved' /home/vgpnk/.config/hypr/
grep_rc=1
$ cat /home/vgpnk/.config/hypr/monitors.conf
env = GDK_SCALE,1
monitor = DP-1, 3440x1440@100, 0x0, 1
(remaining lines are comments)
$ hyprctl getoption monitor 2>&1 | head -3
no such option
$ python3 -I …/mado-barfoot.py --monitors …/monitors.redacted.json --layers …/layers.raw.json \
    --config /home/vgpnk/.config/waybar/config.jsonc --rules /home/vgpnk/.config/hypr/monitors.conf
MADO_BARFOOT_CONFIG: pos=top layer=top level=2 ns=waybar height=26 width=0 margins=0,0,0,0 exclusive=true
MADO_BARFOOT_STATIC: monitor=DP-1 top=0 right=0 bottom=0 left=0 source=rules
MADO_BARFOOT_DECL: monitor=DP-1 box=0,0,3440,26 edge=top
MADO_BARFOOT_LIVE: monitor=DP-1 level=2 ns=waybar box=0,0,3440,26 entries=1
MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN
MADO_BARFOOT: verdict=CLEAN
rc=0
```

Saved verbatim to `.ufo/waves/round-81/w1/R81ScoutLive/join-live-rules-receipt.txt`.

### 9. Declared bar fields

```
$ grep -n -E '^  "(layer|position|height)"' /home/vgpnk/.config/waybar/config.jsonc
3:  "layer": "top",
4:  "position": "top",
6:  "height": 26,
$ grep -n '"width"' /home/vgpnk/.config/waybar/config.jsonc
rc=1
```

No bar-level `width` → `width=0` in the `CONFIG` row → `box.width == 0` branch in
`arrangeLayerArray` (S470:2610-2611).

### 10. Frozen source and host package versions

```
$ S=.ufo/waves/round-81/fetch/S478.bin; grep -n 'CBox&' "$S" | head -20
51:CBox& Hyprutils::Math::CBox::round() {
…
$ awk 'NR>=48 && NR<=66 {printf "%d| %s\n", NR, $0}' .ufo/waves/round-81/fetch/S478.bin
51| CBox& Hyprutils::Math::CBox::round() {
52|     double roundedX = std::round(x);
53|     double roundedY = std::round(y);
54|     double newW     = x + w - roundedX;
55|     double newH     = y + h - roundedY;
56| 
57|     x = roundedX;
58|     y = roundedY;
59|     w = std::round(newW);
60|     h = std::round(newH);
61| 
62|     return *this;
63| }
$ sha256sum .ufo/waves/round-81/fetch/S478.bin
2d04de99ba977e5c3d99546606aede0d3eacc819049e16da5e0fd0d2004d083c
$ pacman -Q hyprutils hyprland
hyprutils 0.14.2-1
hyprland 0.56.2-4
$ grep -n 'HYPRUTILS_MINIMUM_VERSION' .ufo/waves/round-81/fetch/S479.bin
150:set(HYPRUTILS_MINIMUM_VERSION 0.14.0)
156:pkg_check_modules(hyprutils_dep REQUIRED IMPORTED_TARGET hyprutils>=${HYPRUTILS_MINIMUM_VERSION})
```

`pacman -Q` is a query; the orchestrator's pause covers transactions only. No transaction was
issued by this seat.

### 11. arrangeLayerArray with line numbers

```
$ awk 'NR>=2600 && NR<=2672 {printf "%d| %s\n", NR, $0}' .ufo/waves/round-80/fetch/S470.bin
2610|         if (box.width == 0)
2611|             box.x = bounds.x;
2612|         else if ((PSTATE->anchor & both_horiz) == both_horiz)
2613|             box.x = bounds.x + ((bounds.width / 2) - (box.width / 2));
2635|         if (box.width == 0) {
2636|             box.x += PSTATE->margin.left;
2637|             box.width = bounds.width - (PSTATE->margin.left + PSTATE->margin.right);
2660|         box.round(); // fix rounding errors
2669|         ls->setBox(box);
2670|     }
2671| }
$ sha256sum .ufo/waves/round-80/fetch/S470.bin
9af8a74e7dc42ba3c5532303b9bb4ee7c350d4cef2f2c8984e41f2a01b3bdd22
```

### 12. Reachability arithmetic through the tool's own `cbox_round`

```
$ python3 - <<'PY'
import importlib.util
p="/home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py"
spec=importlib.util.spec_from_file_location("barfoot",p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for w in (0,3439,3440,3441,3443,3445): …
PY
  decl_w=   0 width==0 branch    pre=(x=0.0 w=3440.0) -> post=(x=0 w=3440) right_edge=3440  
  decl_w=3439 both_horiz centre  pre=(x=0.5 w=3439.0) -> post=(x=1 w=3439) right_edge=3440  
  decl_w=3440 both_horiz centre  pre=(x=0.0 w=3440.0) -> post=(x=0 w=3440) right_edge=3440  
  decl_w=3441 both_horiz centre  pre=(x=-0.5 w=3441.0) -> post=(x=-1 w=3442) right_edge=3441  OVERFLOW
  decl_w=3443 both_horiz centre  pre=(x=-1.5 w=3443.0) -> post=(x=-2 w=3444) right_edge=3442  OVERFLOW
  decl_w=3445 both_horiz centre  pre=(x=-2.5 w=3445.0) -> post=(x=-3 w=3446) right_edge=3443  OVERFLOW

frozen class replay: {'x': -1, 'y': 363, 'w': 1002, 'h': 100}
```

(Instrument imported read-only; no byte of it changed — see the sha256 in §3.)

### 13. Instrument selftest

```
$ python3 -I /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-barfoot.py --selftest
MADO_BARFOOT_SELFTEST: 121/121
selftest_rc=0
```

### 14. Citation pins and saved-capture hashes

```
$ grep -n -E '^def (main|parse_surfaces|surface_zone|cbox_round|find_layer|declared_bar|evaluate_composition)|…' tools/mado-barfoot.py
324:def declared_bar(config):
498:def cbox_round(box):
559:def surface_zone(spec):
604:def parse_surfaces(raw):
706:def evaluate_composition(config, layers, monitors, monitor, static, static_source, extras):
890:def find_layer(layers, monitor, level, namespace):
1454:        monitor = args.monitor
1460:        static = dict(ZERO_STATIC)
1461:        static_source = "none"
1462:        if args.rules:
$ sha256sum …/R81ScoutLive/monitors.redacted.json …/R81ScoutLive/layers.raw.json
82c01435afb9ab98e77d37f19ef3698f0cb671aea571cfde5c3871bb4026d013  …/monitors.redacted.json
46eb2481ed664862c53c93f76e52cee31753519c4e0587af5d5928c73fd6f53c  …/layers.raw.json
```

## Findings (condensed)

1. **Join: `verdict=CLEAN`.** `MADO_BARFOOT_DECL: monitor=DP-1 box=0,0,3440,26 edge=top` vs
   `MADO_BARFOOT_LIVE: monitor=DP-1 level=2 ns=waybar box=0,0,3440,26 entries=1`;
   `MADO_BARFOOT_RESULT: monitor=DP-1 box=MATCH reserved=EQ band=26 expected=26 verdict=CLEAN`.
   Bar box matches declared `height=26` / `position=top` exactly, and the reserved band (26) equals
   the declared height.
2. **Census:** level 0 `wallpaper` 0,0,3440,1440 pid 1722 (swaybg); level 1 empty; level 2 `waybar`
   0,0,3440,26 pid 1720; level 3 empty. One pid per entry; one waybar process (`pgrep -x waybar`
   → `1720`, count 1).
3. **Negative-tie unreachable live.** The bar declares no `width`, so `arrangeLayerArray`
   S470:2610-2611 takes `box.x = bounds.x` (integer `0`) and S470:2637 sets
   `box.width = 3440`; `box.round()` (S470:2660) is the identity on `0,0,3440,26`. The negative
   half-integer that the frozen class needs (`x = (3440 − w)/2 = -0.5`) requires a declared bar
   width of 3441 or more, oddly exceeding the 3440-px monitor — never declared on this host. The
   live reply also carries only post-round integers (`fractional coords: []`).
4. **Limit 1 of the live join:** `--surfaces` is underivable — `hyprctl layers -j` exposes only
   `address, alpha, h, namespace, pid, w, x, y` (+ `level` as the enclosing key), while
   `parse_surfaces` (`:604`) needs declared `anchor`/`exclusive`/`margins`/`order`. The
   composition half (auto-zone gate, extras overflow) stays synthetic on this host.
5. **Limit 2:** the `reserved` check is an aggregate and the static term is assumed zero by default
   (`MADO_BARFOOT_STATIC: … source=none`, `:1460-1462`); the `--rules` cross-check reads the same
   zero from `~/.config/hypr/monitors.conf` (`source=rules`, identical rows), and
   `grep -rn addreserved ~/.config/hypr/` → rc=1, so today the assumption holds but was not a
   measurement in the primary run. The band also cannot attribute the 26 px to one surface.
6. **GAP:** hyprutils on the host is 0.14.2 while S478 is the v0.14.0 `Box.cpp`; `0.14.2 ≥ 0.14.0`
   (S479:150) but the 0.14.2 bytes were not compared.
7. **[INFERENCE]** `swaybg` reserves no zone: it is absent from the 26 px band, which matches the
   bar's height exactly.

STATUS: ok
