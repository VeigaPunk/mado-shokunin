# Round 25 pre-data control — CtlEmbedded

## Shape and scope

**FIXTURE-KEYED EMBED**, with two representations of one live capture. The plain stub stores the complete table as ordinary JSON text in a Python string. The encoded stub stores the same capture compressed with zlib and encoded with base64. Both ignore every input, including `--home`, and print the embedded table. Neither reads config files nor resolves sources, globs, variables, comments, bind flags, or unbind operations. Neither contacts the compositor when run.

Axes: cheap shortcut, truthful frozen-counter scoring, host safety, and exact-byte preservation.

Expected detector: the unchanged registered C1 counter requires `cases_pass=33/33` and `embed_hits=0`. A fixed table should pass BASE and four UNSOURCED cases but miss the changed tables; plain embedding should additionally trigger the substring screen. No counter or registration changes were made.

Scored revision: `04051723562b8a6ac1f3a9ae05e861aa6f544aff`. There were exactly two counter runs, one per variant, with fresh counter-generated seeds. No replay capture or seed override was passed.

## Capture and source bytes

The first read-only `timeout 20 hyprctl binds -j` attempt exited 1 with stdout `HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)\n\n` and empty stderr. The missing signature was obtained by reading `/run/user/1000`, whose `hypr/` entry exposed the single instance name. Only the control process environment was set; compositor and host configuration were not changed.

Successful capture command:

```sh
HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 timeout 20 hyprctl binds -j
```

Exit 0; stderr empty; 192 binds. Capture saved byte-exact at `/fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/live.json`; SHA-256 `9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`. Both counter runs independently captured that same live hash and the same 79-file snapshot digest.

Scratch sources:

- `/fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/plain.py`: plain JSON variant, SHA-256 `f439366fa9a8ee3ff08934a519999df7d0044e9e9ed6b09922d32cfddce93506`.
- `/fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/encoded.py`: base64/zlib variant, SHA-256 `342e79304f0a59440d488e642bc935f32f3ca6099fab947bbc395d0d90b08acf`.
- `/fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/stub.py` was plain for run 1, encoded for run 2, then restored byte-exact to plain.

The companion lane file `.ufo/waves/round-25/controls/CtlEmbedded.py` is a byte-exact copy of the **tested encoded variant** (SHA-256 `342e79304f0a59440d488e642bc935f32f3ca6099fab947bbc395d0d90b08acf`). It is not a resolver. The plain source remains in the private scratch directory.

## Run 1 — plain JSON

Exact command (after unsetting inherited `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` in this control process):

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 timeout 900 python3 -I .ufo/waves/round-25/c1/count.py 04051723562b8a6ac1f3a9ae05e861aa6f544aff --tool-file /fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/stub.py
```

Complete counter stdout, verbatim:

```text
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/stub.py sha256:f439366fa9a8ee3ff08934a519999df7d0044e9e9ed6b09922d32cfddce93506
seed=12d4142cda447b2e
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
EMBED_HIT 'Audio controls'
EMBED_HIT 'Bluetooth controls'
EMBED_HIT 'Brightness down'
EMBED_HIT 'Brightness down precise'
EMBED_HIT 'Brightness maximum'
CASE BASE         PASS missing=0 extra=0 (unperturbed)
CASE ADD-0        FAIL missing=1 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=72 key="X" code=0 disp="exec" arg="notify-send xgztgzyb5b"
CASE ADD-1        FAIL missing=1 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=9 key="DELETE" code=0 disp="exec" arg="true o7gdg4ymkx"
CASE ADD-2        FAIL missing=1 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=64 key="M" code=0 disp="exec" arg="notify-send a975kth1sx"
CASE ADD-3        FAIL missing=1 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=8 key="R" code=0 disp="exec" arg="printf xaog1eechq"
CASE UNBIND-0     FAIL missing=0 extra=1 (UNBIND mask=68 key='Delete' keycode=0)
    extra   mask=68 key="Delete" code=0 disp="exec" arg="omarchy-hyprland-monitor-internal toggle"
CASE UNBIND-1     FAIL missing=0 extra=1 (UNBIND mask=8 key='XF86AudioLowerVolume' keycode=0)
    extra   mask=8 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume -1"
CASE UNBIND-2     FAIL missing=0 extra=1 (UNBIND mask=64 key='SPACE' keycode=0)
    extra   mask=64 key="SPACE" code=0 disp="exec" arg="omarchy-launch-walker"
CASE UNBIND-3     FAIL missing=0 extra=1 (UNBIND mask=73 key='' keycode=15)
    extra   mask=73 key="" code=15 disp="movetoworkspacesilent" arg="6"
CASE VARIABLE-0   FAIL missing=1 extra=0 (VARIABLE $vnwuducf)
    missing mask=4 key="L" code=0 disp="exec" arg="lzdm5uy46 cw4h"
CASE VARIABLE-1   FAIL missing=1 extra=0 (VARIABLE $vbnsrsmw)
    missing mask=76 key="F8" code=0 disp="exec" arg="jida9t8wa nifv"
CASE VARIABLE-2   FAIL missing=1 extra=0 (VARIABLE $voruukuj)
    missing mask=73 key="Y" code=0 disp="exec" arg="7unbo3zzk xbv0"
CASE VARIABLE-3   FAIL missing=1 extra=0 (VARIABLE $vxkcdvlo)
    missing mask=77 key="D" code=0 disp="exec" arg="iauvoab41 pnfl"
CASE SOURCE-0     FAIL missing=2 extra=0 (SOURCE new file at root line 23)
    missing mask=5 key="F2" code=0 disp="exec" arg="logger e94xxxx1mr"
    missing mask=9 key="G" code=0 disp="exec" arg="true wuk2wezjf4"
CASE SOURCE-1     FAIL missing=2 extra=0 (SOURCE new file at root line 6)
    missing mask=1 key="COMMA" code=0 disp="exec" arg="printf vyvvmtxcg9"
    missing mask=73 key="J" code=0 disp="exec" arg="logger l2m38qrqof"
CASE SOURCE-2     FAIL missing=2 extra=0 (SOURCE new file at root line 4)
    missing mask=13 key="F20" code=0 disp="exec" arg="logger fayvs47usv"
    missing mask=5 key="DOWN" code=0 disp="exec" arg="notify-send n498ayhipr"
CASE SOURCE-3     FAIL missing=2 extra=0 (SOURCE new file at root line 8)
    missing mask=73 key="F2" code=0 disp="exec" arg="printf gt0k5rbzjp"
    missing mask=77 key="PERIOD" code=0 disp="exec" arg="logger 2y377przsi"
CASE GLOB-0       FAIL missing=1 extra=0 (GLOB new toggles file)
    missing mask=68 key="F18" code=0 disp="exec" arg="true y9t8jhxz70"
CASE GLOB-1       FAIL missing=1 extra=0 (GLOB new toggles file)
    missing mask=73 key="EQUAL" code=0 disp="exec" arg="printf noalr76xcx"
CASE GLOB-2       FAIL missing=1 extra=0 (GLOB new toggles file)
    missing mask=65 key="F15" code=0 disp="exec" arg="true sbw58gdlve"
CASE GLOB-3       FAIL missing=1 extra=0 (GLOB new toggles file)
    missing mask=8 key="0" code=0 disp="exec" arg="true z0460sxpdn"
CASE UNSOURCED-0  PASS missing=0 extra=0 (UNSOURCED new bindings file)
CASE UNSOURCED-1  PASS missing=0 extra=0 (UNSOURCED new bindings file)
CASE UNSOURCED-2  PASS missing=0 extra=0 (UNSOURCED new bindings file)
CASE UNSOURCED-3  PASS missing=0 extra=0 (UNSOURCED new bindings file)
CASE COMMENT-0    FAIL missing=1 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=77 key="F24" code=0 disp="exec" arg="logger 551pl55qve"
CASE COMMENT-1    FAIL missing=1 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=1 key="R" code=0 disp="exec" arg="logger bszzojn481"
CASE COMMENT-2    FAIL missing=1 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=8 key="1" code=0 disp="exec" arg="notify-send bsgwqibync"
CASE COMMENT-3    FAIL missing=1 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=72 key="8" code=0 disp="exec" arg="notify-send j6t1pmdqwj"
CASE SYNTH-0      FAIL missing=11 extra=192 (SYNTH tree binds=11 unbound=1 vars=3)
    missing mask=69 key="U" code=0 disp="exec" arg="logger kpe5qg3kq1"
    missing mask=1 key="U" code=0 disp="exec" arg="notify-send t6zidxr0dg"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-1      FAIL missing=14 extra=192 (SYNTH tree binds=14 unbound=1 vars=3)
    missing mask=64 key="Z" code=0 disp="exec" arg="notify-send goiy8p39zn"
    missing mask=72 key="P" code=0 disp="exec" arg="6ivabeact waqv"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-2      FAIL missing=11 extra=192 (SYNTH tree binds=11 unbound=1 vars=3)
    missing mask=5 key="8" code=0 disp="exec" arg="true vdf09evtqn"
    missing mask=1 key="1" code=0 disp="exec" arg="true 9btyk47ycf"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-3      FAIL missing=13 extra=192 (SYNTH tree binds=13 unbound=1 vars=3)
    missing mask=73 key="R" code=0 disp="exec" arg="25kgkhh5a uta6"
    missing mask=72 key="KP_9" code=0 disp="exec" arg="25kgkhh5a mmn3"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
PRED-C1 cases_pass=5/33 embed_hits=229 verdict=TARGET_MISSED
```

Counter stderr: empty. Exit code: **1**.

Final predicate line:

```text
PRED-C1 cases_pass=5/33 embed_hits=229 verdict=TARGET_MISSED
```

## Run 2 — base64/zlib

The encoded bytes replaced only the private scratch `stub.py`. Exact command:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 timeout 900 python3 -I .ufo/waves/round-25/c1/count.py 04051723562b8a6ac1f3a9ae05e861aa6f544aff --tool-file /fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/stub.py
```

Complete counter stdout, verbatim:

```text
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/stub.py sha256:342e79304f0a59440d488e642bc935f32f3ca6099fab947bbc395d0d90b08acf
seed=25ffa71b6a8b020c
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
CASE BASE         PASS missing=0 extra=0 (unperturbed)
CASE ADD-0        FAIL missing=1 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=13 key="X" code=0 disp="exec" arg="printf a5my5p2277"
CASE ADD-1        FAIL missing=1 extra=0 (ADD into .config/hypr/bindings.conf)
    missing mask=12 key="L" code=0 disp="exec" arg="logger r67cft0dwc"
CASE ADD-2        FAIL missing=1 extra=0 (ADD into .config/hypr/bindings.conf)
    missing mask=73 key="Q" code=0 disp="exec" arg="logger wcupwm2stu"
CASE ADD-3        FAIL missing=1 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=64 key="7" code=0 disp="exec" arg="true jckbe8rm71"
CASE UNBIND-0     FAIL missing=0 extra=1 (UNBIND mask=64 key='W' keycode=0)
    extra   mask=64 key="W" code=0 disp="killactive" arg=""
CASE UNBIND-1     FAIL missing=0 extra=1 (UNBIND mask=73 key='COMMA' keycode=0)
    extra   mask=73 key="COMMA" code=0 disp="exec" arg="makoctl restore"
CASE UNBIND-2     FAIL missing=0 extra=1 (UNBIND mask=64 key='XF86AudioMute' keycode=0)
    extra   mask=64 key="XF86AudioMute" code=0 disp="exec" arg="omarchy-audio-output-switch"
CASE UNBIND-3     FAIL missing=0 extra=1 (UNBIND mask=65 key='RETURN' keycode=0)
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-0   FAIL missing=1 extra=0 (VARIABLE $vkzolqil)
    missing mask=12 key="PERIOD" code=0 disp="exec" arg="4xy3lftin gqsw"
CASE VARIABLE-1   FAIL missing=1 extra=0 (VARIABLE $vbkjvhik)
    missing mask=72 key="I" code=0 disp="exec" arg="hzofqenis mw4h"
CASE VARIABLE-2   FAIL missing=1 extra=0 (VARIABLE $vtlilggq)
    missing mask=1 key="F15" code=0 disp="exec" arg="ukpy0ihq8 1f75"
CASE VARIABLE-3   FAIL missing=1 extra=0 (VARIABLE $vhsqcimk)
    missing mask=1 key="F" code=0 disp="exec" arg="w40ysht31 l1l0"
CASE SOURCE-0     FAIL missing=2 extra=0 (SOURCE new file at root line 17)
    missing mask=69 key="INSERT" code=0 disp="exec" arg="printf 7100vdz7pu"
    missing mask=68 key="9" code=0 disp="exec" arg="notify-send c2fd5dv0tz"
CASE SOURCE-1     FAIL missing=2 extra=0 (SOURCE new file at root line 20)
    missing mask=64 key="F9" code=0 disp="exec" arg="logger tjig7gx09t"
    missing mask=1 key="2" code=0 disp="exec" arg="true fxqkcnkudm"
CASE SOURCE-2     FAIL missing=2 extra=0 (SOURCE new file at root line 12)
    missing mask=64 key="KP_5" code=0 disp="exec" arg="logger k01zla5zn1"
    missing mask=9 key="H" code=0 disp="exec" arg="printf kgpjt7tu3t"
CASE SOURCE-3     FAIL missing=2 extra=0 (SOURCE new file at root line 7)
    missing mask=65 key="F5" code=0 disp="exec" arg="logger eoos1ym85r"
    missing mask=8 key="F15" code=0 disp="exec" arg="logger wqbj863mey"
CASE GLOB-0       FAIL missing=1 extra=0 (GLOB new toggles file)
    missing mask=1 key="SPACE" code=0 disp="exec" arg="notify-send lxccs40atb"
CASE GLOB-1       FAIL missing=1 extra=0 (GLOB new toggles file)
    missing mask=69 key="7" code=0 disp="exec" arg="true v2fay1bpwo"
CASE GLOB-2       FAIL missing=1 extra=0 (GLOB new toggles file)
    missing mask=8 key="INSERT" code=0 disp="exec" arg="printf 3qzdaf0ymk"
CASE GLOB-3       FAIL missing=1 extra=0 (GLOB new toggles file)
    missing mask=77 key="D" code=0 disp="exec" arg="printf uew31mzfw7"
CASE UNSOURCED-0  PASS missing=0 extra=0 (UNSOURCED new bindings file)
CASE UNSOURCED-1  PASS missing=0 extra=0 (UNSOURCED new bindings file)
CASE UNSOURCED-2  PASS missing=0 extra=0 (UNSOURCED new bindings file)
CASE UNSOURCED-3  PASS missing=0 extra=0 (UNSOURCED new bindings file)
CASE COMMENT-0    FAIL missing=1 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=8 key="UP" code=0 disp="exec" arg="logger 0mspm72fk8"
CASE COMMENT-1    FAIL missing=1 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=13 key="P" code=0 disp="exec" arg="true qq3b4yu533"
CASE COMMENT-2    FAIL missing=1 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=72 key="HOME" code=0 disp="exec" arg="logger yum2txnbaa"
CASE COMMENT-3    FAIL missing=1 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=76 key="X" code=0 disp="exec" arg="logger xc6d6y2dtx"
CASE SYNTH-0      FAIL missing=14 extra=192 (SYNTH tree binds=14 unbound=1 vars=3)
    missing mask=77 key="HOME" code=0 disp="exec" arg="lds2kvqpg gd10"
    missing mask=12 key="3" code=0 disp="exec" arg="true n3219pyo0d"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-1      FAIL missing=16 extra=192 (SYNTH tree binds=16 unbound=1 vars=2)
    missing mask=9 key="HOME" code=0 disp="exec" arg="notify-send jhsox8qo4p"
    missing mask=5 key="LEFT" code=0 disp="exec" arg="notify-send l88ibb3vub"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-2      FAIL missing=10 extra=192 (SYNTH tree binds=10 unbound=1 vars=2)
    missing mask=72 key="Q" code=0 disp="exec" arg="xu9uyftil 8xz6"
    missing mask=72 key="F20" code=0 disp="exec" arg="notify-send ztmvylojl2"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-3      FAIL missing=12 extra=192 (SYNTH tree binds=12 unbound=1 vars=2)
    missing mask=65 key="1" code=0 disp="exec" arg="true rt3t07u261"
    missing mask=69 key="KP_9" code=0 disp="exec" arg="notify-send 2iex5zy7zx"
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
PRED-C1 cases_pass=5/33 embed_hits=0 verdict=TARGET_MISSED
```

Counter stderr: empty. Exit code: **1**.

Final predicate line:

```text
PRED-C1 cases_pass=5/33 embed_hits=0 verdict=TARGET_MISSED
```

## Restoration and bounded output detector

The same additional bounded output detector was run before encoding, on the encoded bytes, and after restoring the plain bytes:

```sh
timeout 20 python3 -I /fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/stub.py --home /nonexistent-fixture-control-home
```

Its stdout was parsed as JSON and compared to the captured table; this is an output/restoration check, not an additional C1 score. Actual detector observations:

```json
{"binds": 192, "equals_captured_json": true, "exit": 0, "phase": "plain-before-encoding", "stderr": "", "stdout_sha256": "c7a279f94f1d8ed03b254c01ea3406662a82084072a22478bd7e2b709772fd12"}
{"binds": 192, "equals_captured_json": true, "exit": 0, "phase": "encoded", "stderr": "", "stdout_sha256": "9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779"}
{"binds": 192, "equals_captured_json": true, "exit": 0, "phase": "plain-restored", "stderr": "", "stdout_sha256": "c7a279f94f1d8ed03b254c01ea3406662a82084072a22478bd7e2b709772fd12"}
```

Before hashes, measured with `timeout 10 sha256sum` (abbreviated path labels below):

```text
a0afab65428112e7ef1b118bed3889491ed0de6729eeb2ae955c1f485f5695e5  registration.md
70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895  c1/count.py
f439366fa9a8ee3ff08934a519999df7d0044e9e9ed6b09922d32cfddce93506  scratch/stub.py (plain)
f439366fa9a8ee3ff08934a519999df7d0044e9e9ed6b09922d32cfddce93506  scratch/plain.py
342e79304f0a59440d488e642bc935f32f3ca6099fab947bbc395d0d90b08acf  scratch/encoded.py
9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779  scratch/live.json
```

After hashes, measured with `timeout 10 sha256sum` (exit 0, empty stderr):

```text
a0afab65428112e7ef1b118bed3889491ed0de6729eeb2ae955c1f485f5695e5  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/registration.md
70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count.py
f439366fa9a8ee3ff08934a519999df7d0044e9e9ed6b09922d32cfddce93506  /fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/stub.py
f439366fa9a8ee3ff08934a519999df7d0044e9e9ed6b09922d32cfddce93506  /fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/plain.py
342e79304f0a59440d488e642bc935f32f3ca6099fab947bbc395d0d90b08acf  /fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/encoded.py
9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779  /fast/scratch/hyaku/mado-r25/controls/CtlEmbedded/live.json
342e79304f0a59440d488e642bc935f32f3ca6099fab947bbc395d0d90b08acf  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/CtlEmbedded.py
```

The scratch tool returned to its exact original plain bytes. Counter and registration hashes are unchanged. Every subprocess was bounded by `timeout`, started in a separate process group, reaped, and its process group killed in a `finally` block. No packages or tools were installed or updated. No git/jj write commands, compositor mutations, services, or host config writes were used.

## Verdict

Both variants passed only BASE and the four UNSOURCED cases: **5/33**. Encoding reduced `embed_hits` from **229 to 0** without improving the behavioral score. Neither run met the target. Under mutation-test terminology a killed-mutant claim would be **inconclusive**, because the plain baseline already failed C1; this receipt reports the assigned pre-data control result, not a resolver regression test.

Final scored predicate (encoded variant):

```text
PRED-C1 cases_pass=5/33 embed_hits=0 verdict=TARGET_MISSED
```

CONTROL CtlEmbedded: not met
