# CtlAllFalse — round 25 pre-data control

Shape: **ALL-FALSE**.

The stub starts at `--home DIR` / `DIR/.config/hypr/hyprland.conf`, follows literal `source =` paths with leading-tilde expansion and sorted glob expansion, visits each pathname once, strips text after `#`, and counts lines matching `^\s*bind[a-z]*\s*=`. It emits that many JSON objects, each with all 18 required fields set to defaults: booleans `false`, integer fields `0`, strings empty except `submap_universal` equal to the string `"false"`.

It skips bind-field parsing, flags, modifier masks, keys/keycodes, descriptions, dispatchers, arguments, variable expansion, submaps, unbind processing, duplicate-source semantics, and faithful Hyprland/Hyprlang comment parsing. It neither calls a compositor nor embeds a live bind table. This is a line-counting shortcut, not a faithful resolver.

Expected detector: the unchanged frozen counter compares exact multisets across all 18 fields for BASE and 32 perturbations and checks embedded live strings. Passing requires `cases_pass=33/33` and `embed_hits=0`.

Scratch stub: `/fast/scratch/hyaku/mado-r25/controls/CtlAllFalse/stub.py`.
Byte-exact lane copy: `.ufo/waves/round-25/controls/CtlAllFalse.py`.

## Exact invocation

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

```sh
timeout 900 python3 -I .ufo/waves/round-25/c1/count.py 04051723562b8a6ac1f3a9ae05e861aa6f544aff --tool-file /fast/scratch/hyaku/mado-r25/controls/CtlAllFalse/stub.py
```

One fresh-seed scoring run; no replay, alternate live input, counter edit, or registration edit.

## Complete counter stdout (verbatim)

```text
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/CtlAllFalse/stub.py sha256:b91a458db2c76b72fab5058d70009589f78fe0b8ad4c8a969cb66bc2c771fead
seed=7c59bfa472ac63e6
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
CASE BASE         FAIL missing=192 extra=192 (unperturbed)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE ADD-0        FAIL missing=193 extra=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE ADD-1        FAIL missing=193 extra=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE ADD-2        FAIL missing=193 extra=193 (ADD into .config/hypr/bindings.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE ADD-3        FAIL missing=193 extra=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE UNBIND-0     FAIL missing=191 extra=192 (UNBIND mask=72 key='' keycode=13)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE UNBIND-1     FAIL missing=191 extra=192 (UNBIND mask=64 key='L' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE UNBIND-2     FAIL missing=191 extra=192 (UNBIND mask=65 key='' keycode=201)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE UNBIND-3     FAIL missing=191 extra=192 (UNBIND mask=65 key='' keycode=21)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE VARIABLE-0   FAIL missing=193 extra=193 (VARIABLE $vjmqxzar)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE VARIABLE-1   FAIL missing=193 extra=193 (VARIABLE $vajhxbyo)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE VARIABLE-2   FAIL missing=193 extra=193 (VARIABLE $vbupnsyi)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE VARIABLE-3   FAIL missing=193 extra=193 (VARIABLE $vbrgiszh)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE SOURCE-0     FAIL missing=194 extra=194 (SOURCE new file at root line 11)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE SOURCE-1     FAIL missing=194 extra=194 (SOURCE new file at root line 17)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE SOURCE-2     FAIL missing=194 extra=194 (SOURCE new file at root line 29)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE SOURCE-3     FAIL missing=194 extra=194 (SOURCE new file at root line 11)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE GLOB-0       FAIL missing=193 extra=193 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE GLOB-1       FAIL missing=193 extra=193 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE GLOB-2       FAIL missing=193 extra=193 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE GLOB-3       FAIL missing=193 extra=193 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE UNSOURCED-0  FAIL missing=192 extra=192 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE UNSOURCED-1  FAIL missing=192 extra=192 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE UNSOURCED-2  FAIL missing=192 extra=192 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE UNSOURCED-3  FAIL missing=192 extra=192 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE COMMENT-0    FAIL missing=193 extra=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE COMMENT-1    FAIL missing=193 extra=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE COMMENT-2    FAIL missing=193 extra=193 (COMMENT into .config/hypr/bindings.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE COMMENT-3    FAIL missing=193 extra=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE SYNTH-0      FAIL missing=15 extra=16 (SYNTH tree binds=15 unbound=1 vars=3)
    missing mask=8 key="F15" code=0 disp="exec" arg="2r16amxp9 2z8b"
    missing mask=5 key="F1" code=0 disp="exec" arg="true 23q7jor4ws"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE SYNTH-1      FAIL missing=12 extra=13 (SYNTH tree binds=12 unbound=1 vars=3)
    missing mask=76 key="E" code=0 disp="exec" arg="printf faas6m7mh6"
    missing mask=64 key="9" code=0 disp="exec" arg="true 0jz9k3kkds"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE SYNTH-2      FAIL missing=14 extra=15 (SYNTH tree binds=14 unbound=1 vars=2)
    missing mask=8 key="J" code=0 disp="exec" arg="logger sqcng0iyrp"
    missing mask=5 key="EQUAL" code=0 disp="exec" arg="printf t73sy2ksbf"
    extra   mask=0 key="" code=0 disp="" arg=""
CASE SYNTH-3      FAIL missing=15 extra=16 (SYNTH tree binds=15 unbound=1 vars=3)
    missing mask=72 key="T" code=0 disp="exec" arg="notify-send b72pktr65h"
    missing mask=4 key="F19" code=0 disp="exec" arg="printf 5jg43wachz"
    extra   mask=0 key="" code=0 disp="" arg=""
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

Exit code: **1**.

Final predicate line:

```text
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

CONTROL CtlAllFalse: not met

## Preservation evidence

No existing resolver was mutated: this was the assigned standalone pre-data shortcut control. The scored scratch bytes and the lane copy were unchanged across the run, and no pre-existing source bytes required restoration. SHA-256 values measured both before and after scoring:

| File | Before SHA-256 | After SHA-256 |
|---|---|---|
| Scratch `CtlAllFalse/stub.py` | `b91a458db2c76b72fab5058d70009589f78fe0b8ad4c8a969cb66bc2c771fead` | `b91a458db2c76b72fab5058d70009589f78fe0b8ad4c8a969cb66bc2c771fead` |
| Lane `controls/CtlAllFalse.py` | `b91a458db2c76b72fab5058d70009589f78fe0b8ad4c8a969cb66bc2c771fead` | `b91a458db2c76b72fab5058d70009589f78fe0b8ad4c8a969cb66bc2c771fead` |
| Frozen `c1/count.py` | `70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895` | `70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895` |
| Frozen `registration.md` | `a0afab65428112e7ef1b118bed3889491ed0de6729eeb2ae955c1f485f5695e5` | `a0afab65428112e7ef1b118bed3889491ed0de6729eeb2ae955c1f485f5695e5` |

No tools were installed or updated. The bounded foreground scoring command exited; no background job or service was started.
