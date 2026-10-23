# K4NoReader — scoped control findings

## Verdict

CONTROL K4NoReader v4 best: cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED — not met

## Assignment and method

This is the assigned pre-data **NO READER negative control**, not an implementation or a feature-ablation mutation of `tools/mado-binds.py`. That claimed tool was neither built nor edited. The retained control is `.ufo/waves/round-25/controls/v4/K4NoReader.py` (8,881 bytes, sha256:81cea9de1c64350771b3db47b2a08f7f85bec68aaaeafcfe8e2f9d5105979a1b).

- Plausibility: preserve all 192 rows, 24 dispatcher counts, modifier-mask counts, key/keycode frequencies, and observed flag frequencies.
- Shape compliance: ignore the supplied home; no filesystem, environment, socket, compositor, subprocess, or source-graph access at runtime.
- Payload discipline: retain only arg/description values shorter than 12 characters; replace longer values with independent short generic labels, not encodings.
- Discrimination: frozen v4 must require exact 18-field multiset equality for all 41 oracle cases; aggregate resemblance does not change the contract.

The program stores **marginal frequency histograms**, not a bind resolver, full row cache, encoded payload, or generator-grammar parser. There are 27 strata: one per dispatcher, with `exec` separated into hardware, switch, push-to-talk, and ordinary keys. Each stratum independently expands its modifier, key/keycode, flag, short-argument and short-description histograms. Rows are synthesized by aligning those expanded lists. Constant fields reproduce the observed empty submap, string `"false"` for `submap_universal`, false long-press/consumption/catch-all/input-capture flags, and all 18 JSON fields. The `--home DIR` syntax is accepted but DIR is not inspected. The only runtime imports are `json` and `sys`; no explicit file-open, path/stat, environment, subprocess or socket operation is present. Normal Python interpreter/module loading is not config-tree reading.

Long arguments and descriptions were discarded rather than split, compressed, encoded, or reconstructed. In particular, long `exec` arguments become the short conventional shell argument `true`; long shortcut arguments become `CTRL, C`; other long payloads receive short action labels or suitable short argument defaults. Every emitted argument/description is shorter than 12 characters. This is intentionally an approximate synthetic table, not a claim that these bindings describe any supplied tree.

## Gathered live vocabulary

The successful read-only observation was:

```sh
timeout 20 prlimit --as=4000000000 hyprctl binds -j
```

It returned a 192-row array with 18 fields (exit 0), retained as tool receipt `artifact://5358`. The SHA-256 of those captured stdout bytes is `9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`. This live table was used only to compute build-time vocabulary marginals; its long payloads are absent from the control.

A redundant attempted observation from the evaluation kernel, using the same `timeout`/`prlimit` executable sequence through `subprocess.run`, exited 1 and printed `HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)`. It provided no vocabulary and was not a scoring run; the successful shell receipt above was parsed instead. No compositor state was changed to resolve that environment difference. The safety capacity observation `timeout 20 prlimit --as=4000000000 df -h /fast` exited 0 and showed 221G available (73% used); this assignment wrote only the bounded control and report.

Dispatcher frequencies:

```text
exec: 104
workspace: 15
movetoworkspacesilent: 11
changegroupactive: 11
movetoworkspace: 10
movefocus: 4
movecurrentworkspacetomonitor: 4
swapwindow: 4
resizeactive: 4
moveintogroup: 4
sendshortcut: 3
fullscreen: 2
cyclenext: 2
bringactivetotop: 2
focusmonitor: 2
mouse: 2
killactive: 1
layoutmsg: 1
pseudo: 1
togglefloating: 1
fullscreenstate: 1
togglespecialworkspace: 1
togglegroup: 1
moveoutofgroup: 1
```

Modifier-mask frequencies:

```text
64: 42, 65: 37, 68: 26, 0: 23, 73: 22, 72: 19, 8: 7, 76: 6, 69: 3, 1: 2, 12: 2, 9: 2, 13: 1
```

Examples of key vocabulary include `TAB`, directional keys, `RETURN`, `SPACE`, `COMMA`, `PRINT`, letter keys, `XF86Audio*`, `XF86MonBrightness*`, `F9`, mouse keys, lid-switch keys, and keycodes 10–21, 61 and 201. There are 42 keycode-based rows. Observed flag totals: locked 26, mouse 2, release 1, repeat 14, has-description 190. All 192 observed rows have the same empty submap and false long-press/consumption/catch-all/input-capture fields.

## Exact scoring commands

Both commands ran from `/home/vgpnk/Projects/shokunin/mado-shokunin`, concurrently, using the frozen counter's host-wide six-oracle slot locks. Each used a fresh counter-generated seed; no `--seed`, altered case rule, alternate expected table, or new runtime was introduced. The extra `prlimit` imposes the required memory bound without changing counter arguments.

```sh
timeout 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4NoReader.py
```

Run 1 stdout, verbatim, followed by its actual exit status:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4NoReader.py sha256:81cea9de1c64350771b3db47b2a08f7f85bec68aaaeafcfe8e2f9d5105979a1b
seed=db390930029a569e
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=189 extra=189 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE ADD-0        FAIL missing=190 extra=189 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE ADD-1        FAIL missing=190 extra=189 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE ADD-2        FAIL missing=190 extra=189 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE ADD-3        FAIL missing=190 extra=189 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNBIND-0     FAIL missing=188 extra=189 oracle_binds=191 (UNBIND mask=69 key='SPACE' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNBIND-1     FAIL missing=188 extra=189 oracle_binds=191 (UNBIND mask=73 key='' keycode=19) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNBIND-2     FAIL missing=188 extra=189 oracle_binds=191 (UNBIND mask=64 key='X' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNBIND-3     FAIL missing=188 extra=189 oracle_binds=191 (UNBIND mask=65 key='RIGHT' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE VARIABLE-0   FAIL missing=190 extra=189 oracle_binds=193 (VARIABLE $vgilnwmo) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE VARIABLE-1   FAIL missing=190 extra=189 oracle_binds=193 (VARIABLE $vmosxntd) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE VARIABLE-2   FAIL missing=190 extra=189 oracle_binds=193 (VARIABLE $vqlahokd) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE VARIABLE-3   FAIL missing=190 extra=189 oracle_binds=193 (VARIABLE $vkiulvtk) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SOURCE-0     FAIL missing=191 extra=189 oracle_binds=194 (SOURCE new file at root line 20) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SOURCE-1     FAIL missing=191 extra=189 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SOURCE-2     FAIL missing=191 extra=189 oracle_binds=194 (SOURCE new file at root line 20) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SOURCE-3     FAIL missing=191 extra=189 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE GLOB-0       FAIL missing=190 extra=189 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE GLOB-1       FAIL missing=190 extra=189 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE GLOB-2       FAIL missing=190 extra=189 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE GLOB-3       FAIL missing=190 extra=189 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNSOURCED-0  FAIL missing=189 extra=189 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNSOURCED-1  FAIL missing=189 extra=189 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNSOURCED-2  FAIL missing=189 extra=189 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNSOURCED-3  FAIL missing=189 extra=189 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE COMMENT-0    FAIL missing=190 extra=189 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE COMMENT-1    FAIL missing=190 extra=189 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE COMMENT-2    FAIL missing=190 extra=189 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE COMMENT-3    FAIL missing=190 extra=189 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SYNTH-0      FAIL missing=13 extra=192 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=69 key="INSERT" code=0 disp="exec" arg="a8vcvgi48 2g93"
    missing mask=13 key="F15" code=0 disp="exec" arg="printf 167uf1hd0y"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SYNTH-1      FAIL missing=10 extra=192 oracle_binds=10 (SYNTH tree binds=10 unbound=1 vars=2) v3_model=agree
    missing mask=9 key="F7" code=0 disp="exec" arg="printf 5a1w0j7svs"
    missing mask=8 key="PERIOD" code=0 disp="exec" arg="logger v9vcypkxh5"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SYNTH-2      FAIL missing=13 extra=192 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
    missing mask=8 key="D" code=0 disp="exec" arg="4ebbambln 693h"
    missing mask=64 key="F14" code=0 disp="exec" arg="ljeysep0u ufti"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SYNTH-3      FAIL missing=16 extra=192 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=3) v3_model=agree
    missing mask=5 key="V" code=0 disp="exec" arg="true cajfw37upt"
    missing mask=65 key="F4" code=0 disp="exec" arg="notify-send m8t62z9e4t"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE REWRITE-0    FAIL missing=189 extra=189 oracle_binds=192 (REWRITE argswap mask=69 key='SPACE' code=0; unbind mask=68 key='H' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE REWRITE-1    FAIL missing=189 extra=189 oracle_binds=192 (REWRITE argswap mask=73 key='TAB' code=0; unbind mask=0 key='XF86Calculator' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE REWRITE-2    FAIL missing=189 extra=189 oracle_binds=192 (REWRITE argswap mask=64 key='L' code=0; unbind mask=64 key='mouse_up' code=0; add moveintogroup) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE REWRITE-3    FAIL missing=189 extra=189 oracle_binds=192 (REWRITE argswap mask=64 key='O' code=0; unbind mask=0 key='XF86AudioPause' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE HARD-0       FAIL missing=18 extra=192 oracle_binds=18 (HARD tree lines=29 binds=18 unbinds=1 vars=4) v3_model=agree
    missing mask=72 key="mouse:274" code=0 disp="mouse" arg="resizewindow"
    missing mask=4 key="F18" code=0 disp="focusmonitor" arg="d"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE HARD-1       FAIL missing=20 extra=192 oracle_binds=20 (HARD tree lines=30 binds=20 unbinds=1 vars=4) v3_model=agree
    missing mask=0 key="" code=154 disp="togglefloating" arg=""
    missing mask=65 key="mouse_down" code=0 disp="changegroupactive" arg="zbmq"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE HARD-2       FAIL missing=15 extra=192 oracle_binds=15 (HARD tree lines=26 binds=15 unbinds=3 vars=4) v3_model=agree
    missing mask=4 key="F14" code=0 disp="layoutmsg" arg="xnak"
    missing mask=0 key="" code=31 disp="moveintogroup" arg="l"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE HARD-3       FAIL missing=20 extra=192 oracle_binds=20 (HARD tree lines=28 binds=20 unbinds=1 vars=4) v3_model=agree
    missing mask=65 key="1" code=0 disp="killactive" arg="fusa"
    missing mask=64 key="mouse:272" code=0 disp="mouse" arg="movewindow"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED

exit=1
```

Run 2 stdout, verbatim, followed by its actual exit status:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4NoReader.py sha256:81cea9de1c64350771b3db47b2a08f7f85bec68aaaeafcfe8e2f9d5105979a1b
seed=fc4574b8efa1e6ab
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=189 extra=189 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE ADD-0        FAIL missing=190 extra=189 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE ADD-1        FAIL missing=190 extra=189 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE ADD-2        FAIL missing=190 extra=189 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE ADD-3        FAIL missing=190 extra=189 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNBIND-0     FAIL missing=188 extra=189 oracle_binds=191 (UNBIND mask=73 key='' keycode=15) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNBIND-1     FAIL missing=188 extra=189 oracle_binds=191 (UNBIND mask=73 key='F' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNBIND-2     FAIL missing=188 extra=189 oracle_binds=191 (UNBIND mask=68 key='C' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNBIND-3     FAIL missing=188 extra=189 oracle_binds=191 (UNBIND mask=12 key='DELETE' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE VARIABLE-0   FAIL missing=190 extra=189 oracle_binds=193 (VARIABLE $vffickbk) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE VARIABLE-1   FAIL missing=190 extra=189 oracle_binds=193 (VARIABLE $vkzpikca) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE VARIABLE-2   FAIL missing=190 extra=189 oracle_binds=193 (VARIABLE $vyqyhrgp) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE VARIABLE-3   FAIL missing=190 extra=189 oracle_binds=193 (VARIABLE $vvhxgasv) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SOURCE-0     FAIL missing=191 extra=189 oracle_binds=194 (SOURCE new file at root line 16) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SOURCE-1     FAIL missing=191 extra=189 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SOURCE-2     FAIL missing=191 extra=189 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SOURCE-3     FAIL missing=191 extra=189 oracle_binds=194 (SOURCE new file at root line 4) v3_model=agree
    missing mask=65 key="6" code=0 disp="exec" arg="notify-send 2xphculpzx"
    missing mask=12 key="C" code=0 disp="exec" arg="true mp6ck9tel3"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE GLOB-0       FAIL missing=190 extra=189 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE GLOB-1       FAIL missing=190 extra=189 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE GLOB-2       FAIL missing=190 extra=189 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE GLOB-3       FAIL missing=190 extra=189 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNSOURCED-0  FAIL missing=189 extra=189 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNSOURCED-1  FAIL missing=189 extra=189 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNSOURCED-2  FAIL missing=189 extra=189 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNSOURCED-3  FAIL missing=189 extra=189 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE COMMENT-0    FAIL missing=190 extra=189 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE COMMENT-1    FAIL missing=190 extra=189 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE COMMENT-2    FAIL missing=190 extra=189 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE COMMENT-3    FAIL missing=190 extra=189 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SYNTH-0      FAIL missing=13 extra=192 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
    missing mask=4 key="KP_9" code=0 disp="exec" arg="logger 2ich7mzrht"
    missing mask=1 key="9" code=0 disp="exec" arg="true dcnevvq4vz"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SYNTH-1      FAIL missing=14 extra=192 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
    missing mask=72 key="7" code=0 disp="exec" arg="printf c6822g1z3g"
    missing mask=4 key="B" code=0 disp="exec" arg="printf jsgor3nnm3"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SYNTH-2      FAIL missing=11 extra=192 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=2) v3_model=agree
    missing mask=77 key="F10" code=0 disp="exec" arg="printf 5vphvjwoa6"
    missing mask=68 key="Y" code=0 disp="exec" arg="n1qc3kla1 esf0"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SYNTH-3      FAIL missing=13 extra=192 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=4 key="F20" code=0 disp="exec" arg="notify-send rxko1t6wq9"
    missing mask=64 key="HOME" code=0 disp="exec" arg="printf 4dzna0013z"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE REWRITE-0    FAIL missing=189 extra=189 oracle_binds=192 (REWRITE argswap mask=72 key='' code=61; unbind mask=65 key='' code=15; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE REWRITE-1    FAIL missing=189 extra=189 oracle_binds=192 (REWRITE argswap mask=65 key='' code=14; unbind mask=72 key='RETURN' code=0; add movetoworkspace) v3_model=agree
    missing mask=4 key="Z" code=0 disp="movetoworkspace" arg="3"
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE REWRITE-2    FAIL missing=189 extra=189 oracle_binds=192 (REWRITE argswap mask=68 key='N' code=0; unbind mask=13 key='TAB' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE REWRITE-3    FAIL missing=189 extra=189 oracle_binds=192 (REWRITE argswap mask=72 key='TAB' code=0; unbind mask=73 key='F' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE HARD-0       FAIL missing=24 extra=192 oracle_binds=24 (HARD tree lines=34 binds=24 unbinds=3 vars=4) v3_model=agree
    missing mask=64 key="" code=72 disp="movetoworkspacesilent" arg="e-1"
    missing mask=13 key="F23" code=0 disp="killactive" arg=""
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE HARD-1       FAIL missing=21 extra=192 oracle_binds=21 (HARD tree lines=31 binds=21 unbinds=3 vars=4) v3_model=agree
    missing mask=0 key="SLASH" code=0 disp="togglespecialworkspace" arg="ha7k"
    missing mask=4 key="mouse:272" code=0 disp="mouse" arg="resizewindow"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE HARD-2       FAIL missing=19 extra=192 oracle_binds=19 (HARD tree lines=30 binds=19 unbinds=2 vars=4) v3_model=agree
    missing mask=64 key="" code=78 disp="moveoutofgroup" arg="h8og"
    missing mask=8 key="mouse_up" code=0 disp="cyclenext" arg=""
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE HARD-3       FAIL missing=21 extra=192 oracle_binds=21 (HARD tree lines=31 binds=21 unbinds=3 vars=4) v3_model=agree
    missing mask=72 key="" code=125 disp="movecurrentworkspacetomonitor" arg="u"
    missing mask=64 key="F18" code=0 disp="killactive" arg=""
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED

exit=1
```

## Detector interpretation and restoration evidence

Expected detector: exact equality of every generated output multiset to the nested-Hyprland oracle over all 18 fields, plus the frozen long-payload embedding scan. The control deliberately omits config reading, source ordering, variable expansion, comment handling, bind parsing, and unbind application; vocabulary resemblance cannot supply fresh case payloads or the supplied tree's semantics.

Both runs rejected the no-reader control: `cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED`, exit 1. Run 1 seed: `db390930029a569e` (26.82 s, receipt `artifact://5810`); run 2 seed: `fc4574b8efa1e6ab` (18.86 s, receipt `artifact://5785`). Both had `ORACLE_CHECK base_vs_live missing=0 extra=0` and `V3_MODEL_AGREE 41/41`. Neither was an exit-2 oracle/setup/unstable run, so no retry was triggered. Each BASE comparison reported 189 missing and 189 extra rows out of 192: three synthesized rows happened to match, but the exact-table case failed. Every generated case also failed. This is a definite rejection of this control, not a future resolver capability result or a proof about all possible no-reader programs.

This assignment constructs a retained negative-control program, not a scratch edit of a pre-existing implementation. No successful pristine implementation was supplied or run, so this report does **not** call the result a killed implementation mutant, and does not reinterpret the existing missing-tool baseline as a killed mutant. There are no mutated source bytes requiring restoration. The hash commands were `timeout 20 prlimit --as=4000000000 sha256sum .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py` before scoring and that same command with `.ufo/waves/round-25/controls/v4/K4NoReader.py` appended afterward. The before/after frozen-input hashes are:

```text
Before scoring:
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
Initial control bytes, immediately before both scoring runs:
81cea9de1c64350771b3db47b2a08f7f85bec68aaaeafcfe8e2f9d5105979a1b  .ufo/waves/round-25/controls/v4/K4NoReader.py
After both runs, actual sha256sum output:
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
81cea9de1c64350771b3db47b2a08f7f85bec68aaaeafcfe8e2f9d5105979a1b  .ufo/waves/round-25/controls/v4/K4NoReader.py
```

The control path did not exist before this assignment (`controls/v4` itself was absent at first inspection); its initial written hash and its final on-disk hash are recorded above. Only the assigned control path and this report were written. No counter, generator, claimed-tool, corpus, package, service, user config, live-compositor write verb, or git/jj write command was changed or invoked. The scoring subprocesses returned; the frozen oracle's `finally` terminates and waits for every nested compositor process group it starts. No additional runtime, independent baseline mutation, restoration detector, or unrelated verification was invoked. Tool installations/updates: none.
