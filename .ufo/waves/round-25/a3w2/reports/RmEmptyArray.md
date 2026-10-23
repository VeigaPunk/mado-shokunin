# K4EmptyArray — independent re-measure and shape attack

REMEASURE K4EmptyArray: 0/41 (receipt said 0/41); strengthened: not attempted — not met

## Scope and axes

Axes: exact-table cases passed, embed hits, fidelity to the assigned ALL-FALSE shape, and preservation of committed bytes. Read `skill://godspeed`, registration Attempt 3/PRED-C1 (v4), the committed control and receipt, the original shape specification, and the detector's output/comparison paths. This is one independent fresh-seed measurement at `459dd17f8fd60df85b25f15e69376a9765e267d3`, not a resolver implementation or a new counter rule.

## Hash confirmation and unchanged-byte evidence

The control's measured SHA-256 equals the receipt's pristine/restored hash (`controls/v4/K4EmptyArray.md:61,63`). The same bounded hash command was run before and after the measurement, with identical output both times:

```sh
timeout --kill-after=5 20 prlimit --as=4000000000 sha256sum .ufo/waves/round-25/controls/v4/K4EmptyArray.py .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py
```

```text
db6ede4c405224fabda07312413f87b94f7ca684559966b5f9d28858da0e5962  .ufo/waves/round-25/controls/v4/K4EmptyArray.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
```

The counter receipt below independently records the same tool, counter and generator hashes. No source bytes were changed, so no restoration edit was needed. No scratch variant was created.

## Attack on the receipt

The original assignment (`a3w1-spec.json:12–14`) says: “Shape: ALL-FALSE. The tool prints `[]` for every tree. Also try a variant that prints one constant bind entry; report the better.” This excludes a multi-entry embedded table, bind-line counting, label-dependent selection, and config parsing from this particular shape.

The retained eight-line source really implements it: argparse accepts required `--home`; its parsed value is discarded; the only output on the required invocation is literal `[]` plus newline. It never opens the home/config tree or queries a compositor. The counter successfully evaluated that output in all 41 cases; the failures were missing binds, not malformed JSON, tool crashes, or setup failures.

The strongest permitted alternative is one fixed bind entry. On this independent seed, all 41 Hyprland tables contained **11–194 entries**. The detector compares `collections.Counter` multisets of all 18 fields (`count-v3.py:746–751`), preserving multiplicity. Therefore neither zero entries nor any single entry, regardless of its field values, can equal even one of these measured tables. A better-chosen constant might remove one missing bind, but cannot improve the registered exact-case score. This independently supports the receipt's decision to retain `[]`; it is not a claim about every unrun seed.

**Strengthening: not attempted.** There is no score-improving version within the prescribed zero/one-constant-entry shape on the measured tables. Adding a larger table or input-dependent behavior would change the shape, not strengthen it within its bounds.

Mutant: none applied. Expected detector: the same frozen v4 command below, requiring `cases_pass=41/41` and `embed_hits=0`. Actual output: `cases_pass=0/41`, `embed_hits=0`, `TARGET_MISSED`, exit 1. Mutation-kill classification is **inconclusive**, not killed or survived: the pristine baseline already fails, and no mutant was run. Restoration evidence is the identical before/after control hash above.

## Exact measurement command and execution

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 timeout --kill-after=10 1200 prlimit --as=4000000000 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py
```

No `--seed` was supplied. The explicit session variables are the provided existing compositor signature and display; `-B` prevents import bytecode in the lane. Timeout and address-space bounds do not change the scored tool bytes or predicate.

An initial Bash async-launch request was rejected before execution: `Background job limit reached (100). Wait for running jobs to finish or cancel one.` The command was then executed once through Eval's `subprocess.run`, with the environment above, captured stdout/stderr and an outer 1220-second subprocess bound. Thus there was exactly one counter measurement, not a failed scored attempt followed by a retry. It returned exit 1 without an outer timeout; stderr was empty. `ORACLE_CHECK` was missing=0/extra=0 and `V3_MODEL_AGREE` was 41/41.

The counter owns the nested instances; its `finally` block terminates and waits for their process groups (`count.py:174–189`). No separate service, nested compositor, shell-out probe or orchestration runtime was started. No subagents, git/jj writes, packages, services, user configs, live-compositor write verbs, or sibling sources were used or changed. No tools were installed or updated. The only lane output is this report.

## Verbatim counter receipt

The following is complete stdout, followed by the actual `exit=`. Stderr was empty.

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py sha256:db6ede4c405224fabda07312413f87b94f7ca684559966b5f9d28858da0e5962
seed=c82d504f505efe51
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=0 key='XF86KbdBrightnessUp' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=68 key='I' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=13 key='TAB' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=72 key='mouse_up' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vcrcknnc) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vnlyncas) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vtfbkdwt) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vivyjeeg) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 17) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 17) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 7) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-0       FAIL missing=193 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-1       FAIL missing=193 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-2       FAIL missing=193 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-3       FAIL missing=193 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-0  FAIL missing=192 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-1  FAIL missing=192 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-2  FAIL missing=192 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-3  FAIL missing=192 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-0    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=12 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=65 key="F19" code=0 disp="exec" arg="bjr2g5w4x peeq"
    missing mask=8 key="F18" code=0 disp="exec" arg="true zcz5gmfc2z"
CASE SYNTH-1      FAIL missing=14 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
    missing mask=77 key="5" code=0 disp="exec" arg="eq0j7nb3t mvvt"
    missing mask=9 key="3" code=0 disp="exec" arg="notify-send f0w5cvvfom"
CASE SYNTH-2      FAIL missing=11 extra=0 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=2) v3_model=agree
    missing mask=72 key="HOME" code=0 disp="exec" arg="7kk3h1u9e yyk6"
    missing mask=13 key="R" code=0 disp="exec" arg="logger 9q9oalte1y"
CASE SYNTH-3      FAIL missing=17 extra=0 oracle_binds=17 (SYNTH tree binds=17 unbound=1 vars=3) v3_model=agree
    missing mask=69 key="SLASH" code=0 disp="exec" arg="okzxjb3ky 924m"
    missing mask=4 key="MINUS" code=0 disp="exec" arg="printf kjgiygr3zj"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='SPACE' code=0; unbind mask=73 key='X' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='C' code=0; unbind mask=72 key='' code=61; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=68 key='LEFT' code=0; unbind mask=68 key='X' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='COMMA' code=0; unbind mask=64 key='PRINT' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=20 extra=0 oracle_binds=20 (HARD tree lines=26 binds=20 unbinds=2 vars=4) v3_model=agree
    missing mask=64 key="" code=45 disp="pseudo" arg=""
    missing mask=73 key="F17" code=0 disp="fullscreen" arg="oe1e"
CASE HARD-1       FAIL missing=19 extra=0 oracle_binds=19 (HARD tree lines=28 binds=19 unbinds=3 vars=4) v3_model=agree
    missing mask=0 key="G" code=0 disp="togglegroup" arg="sat1"
    missing mask=8 key="" code=178 disp="sendshortcut" arg="Shift, D, activewindow"
CASE HARD-2       FAIL missing=21 extra=0 oracle_binds=21 (HARD tree lines=28 binds=21 unbinds=1 vars=4) v3_model=agree
    missing mask=68 key="PRINT" code=0 disp="movetoworkspace" arg="special:hlce"
    missing mask=69 key="mouse_down" code=0 disp="togglegroup" arg=""
CASE HARD-3       FAIL missing=17 extra=0 oracle_binds=17 (HARD tree lines=25 binds=17 unbinds=2 vars=4) v3_model=agree
    missing mask=76 key="" code=82 disp="togglefloating" arg=""
    missing mask=68 key="" code=43 disp="resizeactive" arg="-12 36"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```
