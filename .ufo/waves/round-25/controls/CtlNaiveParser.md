# CtlNaiveParser — cheap partial resolver control

## Shape and scope

Axes: meet the frozen PRED-C1 target, minimize resolver work, preserve the host and frozen scoring inputs.

The control is a 55-line, 2,339-byte Python program. It starts at
`--home/.config/hypr/hyprland.conf`, follows `source =` recursively in file order,
expands a leading `~` against `--home`, expands sorted globs, and resolves relative
source paths against their including file. It reads only sourced files. It
recognizes `bind*` flag letters, builds a modifier bitmask, recognizes numeric
`code:` keys, and emits a JSON array with the 18 expected field names. It ignores
full-line comments because they do not match either statement pattern.

It deliberately skips variable expansion, inline-comment stripping, and `unbind`.
Its behavior-bearing shortcut is a fixed four-field comma split: it records the
`d` flag but does not shift the dispatcher and argument past a description, and
always emits an empty description. It also does not evaluate submap statements,
per-device offsets, multi-key semantics, or the full Hyprlang language. No live
bind table, command arguments, or descriptions are embedded. No socket or
compositor call exists in the stub.

Scratch stub: `/fast/scratch/hyaku/mado-r25/controls/CtlNaiveParser/stub.py`.
Byte-exact lane copy: `.ufo/waves/round-25/controls/CtlNaiveParser.py`.

## Expected detector and measurement

The detector is the frozen counter, unchanged: compare complete bind multisets
across all 18 JSON fields for BASE and the 32 generated cases, and require
`cases_pass=33/33` and `embed_hits=0`. Expected failure mechanisms are literal
variables, retained inline comments, retained unbound entries, and description
text misread as a dispatcher.

One measurement was run, with a fresh counter-generated seed. The tool runner's
working directory was `/home/vgpnk/Projects/shokunin/mado-shokunin`; the exact
shell-equivalent command was:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 python3 -I .ufo/waves/round-25/c1/count.py 04051723562b8a6ac1f3a9ae05e861aa6f544aff --tool-file /fast/scratch/hyaku/mado-r25/controls/CtlNaiveParser/stub.py
```

Exit code: **1**. Observed wall time: **1.33 seconds**. No replay, rerun,
`--seed`, or `--live-json` was used.

## Complete counter stdout (verbatim)

```text
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/CtlNaiveParser/stub.py sha256:a82d4d3a748480a7f273182ddd1a984605a8b43169288d959f4c6f7ec1f7fe66
seed=c7a02d21511df377
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
CASE BASE         FAIL missing=190 extra=190 (unperturbed)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE ADD-0        FAIL missing=191 extra=191 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE ADD-1        FAIL missing=190 extra=190 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE ADD-2        FAIL missing=191 extra=191 (ADD into .config/hypr/bindings.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE ADD-3        FAIL missing=191 extra=191 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE UNBIND-0     FAIL missing=189 extra=190 (UNBIND mask=68 key='A' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE UNBIND-1     FAIL missing=189 extra=190 (UNBIND mask=73 key='' keycode=17)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE UNBIND-2     FAIL missing=189 extra=190 (UNBIND mask=0 key='XF86AudioNext' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE UNBIND-3     FAIL missing=189 extra=190 (UNBIND mask=65 key='' keycode=13)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE VARIABLE-0   FAIL missing=191 extra=191 (VARIABLE $vrmlnqit)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE VARIABLE-1   FAIL missing=191 extra=191 (VARIABLE $vtgtnbvt)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE VARIABLE-2   FAIL missing=191 extra=191 (VARIABLE $vysodkfx)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE VARIABLE-3   FAIL missing=191 extra=191 (VARIABLE $vpnqpxfy)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE SOURCE-0     FAIL missing=191 extra=191 (SOURCE new file at root line 11)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE SOURCE-1     FAIL missing=192 extra=192 (SOURCE new file at root line 6)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE SOURCE-2     FAIL missing=191 extra=191 (SOURCE new file at root line 7)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE SOURCE-3     FAIL missing=191 extra=191 (SOURCE new file at root line 18)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE GLOB-0       FAIL missing=191 extra=191 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE GLOB-1       FAIL missing=191 extra=191 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE GLOB-2       FAIL missing=190 extra=190 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE GLOB-3       FAIL missing=191 extra=191 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE UNSOURCED-0  FAIL missing=190 extra=190 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE UNSOURCED-1  FAIL missing=190 extra=190 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE UNSOURCED-2  FAIL missing=190 extra=190 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE UNSOURCED-3  FAIL missing=190 extra=190 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE COMMENT-0    FAIL missing=191 extra=191 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE COMMENT-1    FAIL missing=191 extra=191 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE COMMENT-2    FAIL missing=191 extra=191 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE COMMENT-3    FAIL missing=191 extra=191 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="Volume up" arg="exec, omarchy-swayosd-client --output-volume rais
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="Volume down" arg="exec, omarchy-swayosd-client --output-volume lowe
CASE SYNTH-0      FAIL missing=11 extra=12 (SYNTH tree binds=13 unbound=1 vars=3)
    missing mask=76 key="F7" code=0 disp="exec" arg="logger yv1grkz6k9"
    missing mask=64 key="F1" code=0 disp="exec" arg="9bii6elt5 6csh"
    extra   mask=68 key="HOME" code=0 disp="8ip9j 5dvu4f" arg="exec, notify-send rnr17lqyjc # 14vfr"
    extra   mask=76 key="F7" code=0 disp="exec" arg="logger yv1grkz6k9 # yedjy"
CASE SYNTH-1      FAIL missing=12 extra=13 (SYNTH tree binds=15 unbound=1 vars=3)
    missing mask=1 key="L" code=0 disp="exec" arg="logger oyicw5wu8f"
    missing mask=9 key="5" code=0 disp="exec" arg="notify-send zq0l9cddwf"
    extra   mask=9 key="F6" code=0 disp="exec" arg="notify-send an0391l0pp"
    extra   mask=1 key="L" code=0 disp="D0ftn 8w00e7" arg="exec, logger oyicw5wu8f # 0g7q1"
CASE SYNTH-2      FAIL missing=14 extra=15 (SYNTH tree binds=17 unbound=1 vars=2)
    missing mask=8 key="DOWN" code=0 disp="exec" arg="true 4elvwaw0t8"
    missing mask=64 key="F15" code=0 disp="exec" arg="notify-send 0o3n9hzdor"
    extra   mask=65 key="F3" code=0 disp="Mu18f 9egipi" arg="exec, $smeghjvj mmcd"
    extra   mask=8 key="DOWN" code=0 disp="E1wdj ude5dr" arg="exec, true 4elvwaw0t8"
CASE SYNTH-3      FAIL missing=13 extra=14 (SYNTH tree binds=13 unbound=1 vars=3)
    missing mask=12 key="Z" code=0 disp="exec" arg="notify-send r7aow2o2p6"
    missing mask=8 key="MINUS" code=0 disp="exec" arg="notify-send dhvwfffj0l"
    extra   mask=12 key="F18" code=0 disp="I690e 7ivwfm" arg="exec, true 9bxmzxjhth # sf0k3"
    extra   mask=12 key="Z" code=0 disp="Yviz7 91g3v4" arg="exec, notify-send r7aow2o2p6 # wenpd"
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

Counter stdout SHA-256: `ec5c0b753ea59a06f1e2fa7fac8e94f930e04cf0458a764066693298a1d91e08`
(18,650 bytes, 171 lines, including its final newline).

## Failed case types

| Type | Passed | Missing / extra entries observed |
|---|---:|---|
| BASE | 0/1 | 190 / 190 |
| ADD | 0/4 | 190–191 / 190–191 |
| UNBIND | 0/4 | 189 / 190 |
| VARIABLE | 0/4 | 191 / 191 |
| SOURCE | 0/4 | 191–192 / 191–192 |
| GLOB | 0/4 | 190–191 / 190–191 |
| UNSOURCED | 0/4 | 190 / 190 |
| COMMENT | 0/4 | 191 / 191 |
| SYNTH | 0/4 | 11/12, 12/13, 14/15, 13/14 respectively |

Every case failed. The BASE diagnostics directly show description strings
misread as dispatchers. Every snapshot-derived case inherits that BASE mismatch;
the family labels alone therefore do not establish independent detection of each
omission. The four whole synthetic trees also failed without the host snapshot.

This is a new pre-data shortcut control, not a mutation of an existing passing
resolver. A failing BASE is not claimed as a killed mutant. The measured result
is that this partial resolver did not meet the frozen target.

Final counter line:

```text
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

CONTROL CtlNaiveParser: not met

## Byte preservation and restoration evidence

SHA-256 values were recorded before and after the scoring run:

| File | Before | After |
|---|---|---|
| `.ufo/waves/round-25/registration.md` | `a0afab65428112e7ef1b118bed3889491ed0de6729eeb2ae955c1f485f5695e5` | `a0afab65428112e7ef1b118bed3889491ed0de6729eeb2ae955c1f485f5695e5` |
| `.ufo/waves/round-25/c1/count.py` | `70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895` | `70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895` |
| Scratch `stub.py` | `a82d4d3a748480a7f273182ddd1a984605a8b43169288d959f4c6f7ec1f7fe66` | `a82d4d3a748480a7f273182ddd1a984605a8b43169288d959f4c6f7ec1f7fe66` |

The required lane stub copy was also hashed after writing and has the identical
SHA-256 `a82d4d3a748480a7f273182ddd1a984605a8b43169288d959f4c6f7ec1f7fe66`.
No pre-existing lane source bytes were mutated, so no byte restoration was
necessary. Only the isolated scratch stub and this control's two authorized lane
receipt files were created. The counter's code removes its private temporary
directory in `finally`. All shell commands were timeout-bounded; the scoring
command completed and no service or background job was started.

No tools were installed or updated. No git/jj write command, host configuration
write, compositor mutation, or write to the read-only source clones was performed.
