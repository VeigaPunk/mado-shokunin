# RmNoReader — independent v4 re-measure and shape attack

## Verdict

REMEASURE K4NoReader: 0/41 (receipt said 0/41); strengthened: 0/41 — not met

The committed control's SHA-256 matches its receipt exactly. Each variant was scored once on a fresh seed at revision `459dd17f8fd60df85b25f15e69376a9765e267d3`. Both runs completed all 41 comparisons, reported `embed_hits=0`, and exited 1 (`TARGET_MISSED`). Neither was a setup failure or an inconclusive oracle run.

## Axes and expected detector

Axes: exact-case discrimination; no-reader shape compliance; absence of embedded long payloads; fidelity of vocabulary co-occurrences. The detector remains frozen v4: exact bind-multiset equality over all 18 fields against Hyprland v0.56.2's own tables, for BASE plus 40 generated cases, with `cases_pass=41/41` and `embed_hits=0` required together. No partial-row credit or changed predicate was used.

This is a re-measure of a negative control and one conditional-vocabulary strengthening attempt, not a feature-ablation mutation of a successful resolver. A failed negative-control baseline is not a killed implementation mutant.

## Identity and input hashes

The named receipt `.ufo/waves/round-25/controls/v4/K4NoReader.md:9` names SHA-256 `81cea9de1c64350771b3db47b2a08f7f85bec68aaaeafcfe8e2f9d5105979a1b`. Actual command, from the lane:

```sh
timeout 20 prlimit --as=4000000000 sha256sum .ufo/waves/round-25/controls/v4/K4NoReader.py .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py
```

Actual pre-score output (exit 0):

```text
81cea9de1c64350771b3db47b2a08f7f85bec68aaaeafcfe8e2f9d5105979a1b  .ufo/waves/round-25/controls/v4/K4NoReader.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
```

## Committed-control re-measure

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`. The extra `prlimit` enforces the memory bound; `-B` prevents the frozen counter's generator import from writing lane bytecode. The supplied live-instance signature was set explicitly. No seed override was supplied.

```sh
HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 timeout 1200 prlimit --as=4000000000 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4NoReader.py
```

An initial asynchronous tool submission was refused with `Background job limit reached (100). Wait for running jobs to finish or cancel one.` It started no scoring command. The same command was then submitted synchronously and completed in 48.74 seconds. The receipt below is the actual shell result, recovered directly from this seat's recorded tool result rather than reconstructed from the generator or from an old receipt.

Stdout, verbatim, followed by the actual exit status:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4NoReader.py sha256:81cea9de1c64350771b3db47b2a08f7f85bec68aaaeafcfe8e2f9d5105979a1b
seed=f8298760f15b7b06
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
CASE ADD-3        FAIL missing=190 extra=189 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNBIND-0     FAIL missing=188 extra=189 oracle_binds=191 (UNBIND mask=64 key='K' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNBIND-1     FAIL missing=188 extra=189 oracle_binds=191 (UNBIND mask=64 key='RETURN' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNBIND-2     FAIL missing=188 extra=189 oracle_binds=191 (UNBIND mask=68 key='BACKSPACE' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE UNBIND-3     FAIL missing=188 extra=189 oracle_binds=191 (UNBIND mask=65 key='C' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE VARIABLE-0   FAIL missing=190 extra=189 oracle_binds=193 (VARIABLE $vwnzwcci) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE VARIABLE-1   FAIL missing=190 extra=189 oracle_binds=193 (VARIABLE $vdsmkcny) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE VARIABLE-2   FAIL missing=190 extra=189 oracle_binds=193 (VARIABLE $vyceganl) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE VARIABLE-3   FAIL missing=190 extra=189 oracle_binds=193 (VARIABLE $vrkdiaat) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SOURCE-0     FAIL missing=191 extra=189 oracle_binds=194 (SOURCE new file at root line 12) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SOURCE-1     FAIL missing=191 extra=189 oracle_binds=194 (SOURCE new file at root line 11) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SOURCE-2     FAIL missing=191 extra=189 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SOURCE-3     FAIL missing=191 extra=189 oracle_binds=194 (SOURCE new file at root line 19) v3_model=agree
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
CASE COMMENT-0    FAIL missing=190 extra=189 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE COMMENT-1    FAIL missing=190 extra=189 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE COMMENT-2    FAIL missing=190 extra=189 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE COMMENT-3    FAIL missing=190 extra=189 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SYNTH-0      FAIL missing=14 extra=192 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
    missing mask=5 key="UP" code=0 disp="exec" arg="ygua2ex7p 30id"
    missing mask=9 key="F23" code=0 disp="exec" arg="ygua2ex7p xoh9"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SYNTH-1      FAIL missing=13 extra=192 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=12 key="MINUS" code=0 disp="exec" arg="mbrf4jciw l3gg"
    missing mask=69 key="F21" code=0 disp="exec" arg="logger ugvfn2ssdg"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SYNTH-2      FAIL missing=12 extra=192 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
    missing mask=68 key="4" code=0 disp="exec" arg="95qht234z jiar"
    missing mask=69 key="F" code=0 disp="exec" arg="notify-send w1b1gj0q4y"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE SYNTH-3      FAIL missing=16 extra=192 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=3) v3_model=agree
    missing mask=76 key="INSERT" code=0 disp="exec" arg="true efjspj9nor"
    missing mask=12 key="F16" code=0 disp="exec" arg="logger mxd8lysumy"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE REWRITE-0    FAIL missing=189 extra=189 oracle_binds=192 (REWRITE argswap mask=73 key='B' code=0; unbind mask=73 key='F' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE REWRITE-1    FAIL missing=189 extra=189 oracle_binds=192 (REWRITE argswap mask=65 key='' code=16; unbind mask=72 key='' code=12; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE REWRITE-2    FAIL missing=188 extra=189 oracle_binds=191 (REWRITE argswap mask=65 key='' code=201; unbind mask=8 key='TAB' code=0; add movefocus) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE REWRITE-3    FAIL missing=189 extra=189 oracle_binds=192 (REWRITE argswap mask=68 key='BACKSPACE' code=0; unbind mask=65 key='LEFT' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE HARD-0       FAIL missing=19 extra=192 oracle_binds=19 (HARD tree lines=32 binds=19 unbinds=2 vars=4) v3_model=agree
    missing mask=72 key="mouse:273" code=0 disp="mouse" arg="resizewindow"
    missing mask=65 key="KP_5" code=0 disp="swapwindow" arg="d"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE HARD-1       FAIL missing=20 extra=192 oracle_binds=20 (HARD tree lines=28 binds=20 unbinds=2 vars=4) v3_model=agree
    missing mask=0 key="" code=240 disp="cyclenext" arg="8bx6"
    missing mask=4 key="" code=152 disp="resizeactive" arg="0 -24"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE HARD-2       FAIL missing=23 extra=192 oracle_binds=23 (HARD tree lines=33 binds=23 unbinds=3 vars=4) v3_model=agree
    missing mask=8 key="RETURN" code=0 disp="movetoworkspace" arg="18"
    missing mask=65 key="F17" code=0 disp="resizeactive" arg="-8 53"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
CASE HARD-3       FAIL missing=21 extra=192 oracle_binds=21 (HARD tree lines=32 binds=21 unbinds=3 vars=4) v3_model=agree
    missing mask=0 key="" code=200 disp="moveoutofgroup" arg=""
    missing mask=64 key="" code=56 disp="focusmonitor" arg="r"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="true"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="true"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Attack on the shape claim

The original program does implement the assigned no-reader shortcut at application level. Its entire code was inspected, including the complete histogram literal on line 9. It imports only `json` and `sys`; `--home DIR` is checked syntactically but DIR is never inspected; there are no application-level file, filesystem-metadata, environment, socket, subprocess, or compositor accesses. It expands stored histograms and serializes a fixed table (`K4NoReader.py:12-39`). This is a source-inspection finding, not a syscall-trace claim: Python's own module loading must not be confused with a promise of zero interpreter file opens.

The receipt accurately describes its construction: 27 strata, independent expansion of masks, keys, flags, short arguments and short descriptions, and short generic replacements for long payloads. The re-measure reproduces its claimed 0/41, with only three exact BASE rows matching (`missing=189 extra=189`).

It is not established as the strongest plausible synthetic table. Independent marginal expansion discards legal vocabulary correlations. For a concrete example, the original `workspace` histogram places keycode 10 at index 3 and argument `e-1` at that index; the fresh live capture has `(modmask=64, key="", keycode=10, arg="1")`. Thus even an allowed short argument need not remain associated with its key. The code also aligns modifier and flag frequencies independently of keys. Preserving those conditional frequencies is permitted without reading any supplied tree or parsing any bind grammar.

Build-time vocabulary observation, using the same explicit live-instance environment:

```sh
HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 timeout 20 prlimit --as=4000000000 hyprctl binds -j
```

It exited 0 with empty stderr. Stdout SHA-256 was `9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`, identical to both scoring captures. Parsed construction observations:

```text
rows=192
fields=[18]
short_arg_rows=83
short_description_rows=45
both_short_rows=3
live workspace code:10 rows=[(64, '', 10, '1')]
```

Only three live rows have both payload fields shorter than 12 characters. Consequently, any variant retaining this original control's stricter discipline of emitting only short payloads can match at most three BASE rows. That restriction is a property of these variants, not a proof about every program satisfying the literal no-reader shape. Independently, the fixed 192-row output cannot equal both the 192-row BASE and the differently sized generated tables. The fresh case data are not supplied to either program through its ignored home argument.

## Same-shape strengthening attempt

The retained candidate is `/fast/scratch/hyaku/mado-r25a3/rm/K4NoReader-strong.py`. The changed behavior-bearing point is the vocabulary conditioning: replace independent modifier/flag assignment within dispatcher strata with 50 strata fixed by `(dispatcher, modmask, locked, mouse, release, repeat, has_description)`. Within each stratum, keys/keycodes, short arguments and short labels remain independently expanded frequency histograms, sorted independently rather than preserving original row order. This preserves the observed joint non-payload vocabulary instead of merely its independent marginals. No config, generator-grammar, case-label, source-graph or delta parser was added.

Long payloads are discarded, not encoded or reconstructed. Generic replacement arguments are `true`, `CTRL, C`, `movewindow`, or a short workspace/default value; long descriptions receive short generic action labels. The candidate imports only `json` and `sys`, ignores DIR, and prints the same 18-field schema. Construction output:

```text
strata=50
rows=192
max_arg_length=11
max_description_length=11
source_embed_hits=0
bytes=10737
sha256=72166513084a5a7819c71b2cb34a4b23e5a99d890b37ed536151c42ecbbbd5a5
```

This strengthens co-occurrence fidelity, not the measured exact-case score. The actual fresh-seed run still passes zero cases; BASE exact-row matches decrease from three to two (`missing=190 extra=190`). It is therefore not a demonstrated stronger scorer or a claim of exhaustive optimization. The unsuccessful candidate is retained at the expressly requested scratch output path, without modifying the committed control or selecting another variant after seeing this result.

Exact scoring command, from the same lane directory and with the same bounded detector:

```sh
HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 timeout 1200 prlimit --as=4000000000 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /fast/scratch/hyaku/mado-r25a3/rm/K4NoReader-strong.py
```

The subprocess returned with empty stderr. Stdout is inserted directly from its captured result, verbatim, followed by its actual exit status:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/rm/K4NoReader-strong.py sha256:72166513084a5a7819c71b2cb34a4b23e5a99d890b37ed536151c42ecbbbd5a5
seed=561eef196e7743bc
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=190 extra=190 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE ADD-0        FAIL missing=191 extra=190 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE ADD-1        FAIL missing=191 extra=190 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE ADD-2        FAIL missing=191 extra=190 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE ADD-3        FAIL missing=191 extra=190 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE UNBIND-0     FAIL missing=189 extra=190 oracle_binds=191 (UNBIND mask=68 key='RIGHT' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE UNBIND-1     FAIL missing=189 extra=190 oracle_binds=191 (UNBIND mask=64 key='TAB' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE UNBIND-2     FAIL missing=189 extra=190 oracle_binds=191 (UNBIND mask=1 key='XF86MonBrightnessUp' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE UNBIND-3     FAIL missing=189 extra=190 oracle_binds=191 (UNBIND mask=68 key='R' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE VARIABLE-0   FAIL missing=191 extra=190 oracle_binds=193 (VARIABLE $vaiyiesq) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE VARIABLE-1   FAIL missing=191 extra=190 oracle_binds=193 (VARIABLE $vjiwsfkz) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE VARIABLE-2   FAIL missing=191 extra=190 oracle_binds=193 (VARIABLE $vgesdcyn) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE VARIABLE-3   FAIL missing=191 extra=190 oracle_binds=193 (VARIABLE $vgfimsrh) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE SOURCE-0     FAIL missing=192 extra=190 oracle_binds=194 (SOURCE new file at root line 13) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE SOURCE-1     FAIL missing=192 extra=190 oracle_binds=194 (SOURCE new file at root line 23) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE SOURCE-2     FAIL missing=192 extra=190 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE SOURCE-3     FAIL missing=192 extra=190 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE GLOB-0       FAIL missing=191 extra=190 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE GLOB-1       FAIL missing=191 extra=190 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE GLOB-2       FAIL missing=191 extra=190 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE GLOB-3       FAIL missing=191 extra=190 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE UNSOURCED-0  FAIL missing=190 extra=190 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE UNSOURCED-1  FAIL missing=190 extra=190 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE UNSOURCED-2  FAIL missing=190 extra=190 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE UNSOURCED-3  FAIL missing=190 extra=190 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE COMMENT-0    FAIL missing=191 extra=190 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE COMMENT-1    FAIL missing=191 extra=190 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE COMMENT-2    FAIL missing=191 extra=190 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE COMMENT-3    FAIL missing=191 extra=190 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE SYNTH-0      FAIL missing=14 extra=192 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
    missing mask=13 key="COMMA" code=0 disp="exec" arg="29wglfraf wcsj"
    missing mask=4 key="DELETE" code=0 disp="exec" arg="29wglfraf v3oq"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE SYNTH-1      FAIL missing=15 extra=192 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=3) v3_model=agree
    missing mask=5 key="F24" code=0 disp="exec" arg="phh9awbd3 b640"
    missing mask=13 key="F11" code=0 disp="exec" arg="notify-send teiu7u59e8"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE SYNTH-2      FAIL missing=12 extra=192 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
    missing mask=5 key="KP_1" code=0 disp="exec" arg="logger pl9piyan82"
    missing mask=65 key="H" code=0 disp="exec" arg="yn4x4h9g7 bt62"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE SYNTH-3      FAIL missing=13 extra=192 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
    missing mask=12 key="UP" code=0 disp="exec" arg="notify-send 0er75ukb72"
    missing mask=64 key="8" code=0 disp="exec" arg="logger epvfx8wtmw"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE REWRITE-0    FAIL missing=190 extra=190 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioMute' code=0; unbind mask=73 key='TAB' code=0; add movetoworkspace) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE REWRITE-1    FAIL missing=190 extra=190 oracle_binds=192 (REWRITE argswap mask=65 key='Y' code=0; unbind mask=68 key='SPACE' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE REWRITE-2    FAIL missing=191 extra=191 oracle_binds=192 (REWRITE argswap mask=64 key='F' code=0; unbind mask=64 key='XF86AudioMute' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE REWRITE-3    FAIL missing=190 extra=190 oracle_binds=192 (REWRITE argswap mask=64 key='ESCAPE' code=0; unbind mask=68 key='V' code=0; add changegroupactive) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE HARD-0       FAIL missing=21 extra=192 oracle_binds=21 (HARD tree lines=30 binds=21 unbinds=1 vars=4) v3_model=agree
    missing mask=72 key="mouse:274" code=0 disp="mouse" arg="MoveWindow"
    missing mask=72 key="" code=11 disp="togglegroup" arg="0b62"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE HARD-1       FAIL missing=23 extra=192 oracle_binds=23 (HARD tree lines=32 binds=23 unbinds=2 vars=4) v3_model=agree
    missing mask=0 key="7" code=0 disp="movetoworkspacesilent" arg="special:ma9g"
    missing mask=65 key="KP_1" code=0 disp="exec" arg="uwsm-app -- u76jg6"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE HARD-2       FAIL missing=19 extra=192 oracle_binds=19 (HARD tree lines=27 binds=19 unbinds=2 vars=4) v3_model=agree
    missing mask=72 key="0" code=0 disp="movetoworkspacesilent" arg="e-1"
    missing mask=72 key="" code=169 disp="swapwindow" arg="l"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
CASE HARD-3       FAIL missing=22 extra=192 oracle_binds=22 (HARD tree lines=29 binds=22 unbinds=2 vars=4) v3_model=agree
    missing mask=1 key="8" code=0 disp="movecurrentworkspacetomonitor" arg="l"
    missing mask=72 key="B" code=0 disp="layoutmsg" arg="v5v1"
    extra   mask=8 key="TAB" code=0 disp="bringactivetotop" arg=""
    extra   mask=9 key="TAB" code=0 disp="bringactivetotop" arg=""
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Probe verdict and restoration evidence

Control verdict: both variants are rejected by the frozen predicate (`TARGET_MISSED`, 0/41, no embedding hits). There is no evidence here of a surviving shortcut that meets v4. Mutation-kill verdict: inconclusive/not applicable as an implementation mutant, because no passing pristine implementation was assigned or measured. Neither the existing negative-control miss nor the conditional-vocabulary miss is relabeled a killed mutant. This probe does not judge or integrate the concurrently built resolver.

There was no in-place mutation of the committed control or frozen detector. Exact original bytes were preserved throughout, so no restoration or additional restored-byte scoring run was necessary. The explicit assignment's one fresh-seed score per variant was respected. The candidate is the intentionally retained named scratch deliverable, not a mutation left in a sibling's source.

Actual post-score hash command:

```sh
timeout 20 prlimit --as=4000000000 sha256sum .ufo/waves/round-25/controls/v4/K4NoReader.py .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py /fast/scratch/hyaku/mado-r25a3/rm/K4NoReader-strong.py
```

Actual output (exit 0):

```text
81cea9de1c64350771b3db47b2a08f7f85bec68aaaeafcfe8e2f9d5105979a1b  .ufo/waves/round-25/controls/v4/K4NoReader.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
72166513084a5a7819c71b2cb34a4b23e5a99d890b37ed536151c42ecbbbd5a5  /fast/scratch/hyaku/mado-r25a3/rm/K4NoReader-strong.py
```

The committed-control and detector/generator before/after hashes are identical; the candidate's post-score hash equals its construction hash. Both counter processes returned normally through their exit-1 predicate path. Nested Hyprland instances were started only by the frozen counter, whose inspected `oracle()` finally block terminates and waits for its process groups (`count.py:174-189`); no independent nested instance, live-compositor write verb, package/service/config edit, git/jj write command, extra behavioral detector, or other runtime was invoked. Only the assigned report and candidate output path were written by this seat. Tool installations or updates: none.
