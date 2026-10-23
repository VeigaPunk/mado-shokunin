# RmEasyOnly — independent control re-measure and scoped attack

REMEASURE K4EasyOnly: 4/41 (receipt said 4/41); strengthened: 4/41 — not met

## Scope and hash check

Axes: receipt fidelity; correctness within the permitted easy grammar; fidelity to the forbidden-feature boundary; host safety and exact restoration.

Read the Attempt 3 registration and the original K4EasyOnly specification in `a3w1-spec.json:42-44`. The control genuinely reads the ordered source graph, expands RHS variables, handles comments, applies unbind, and emits easy `bind[dler]*` entries. It has no cache or embedded table, and does not implement the forbidden aliases/separators, keycodes, mouse semantics, rejected-bind rules, dispatcher validation or case lowering.

The assigned file SHA-256 is `fe5b5cc00af51d81cb6385e762b0488a5fb8eac4d7652cf7a65090e7a4c96648`, exactly the hash in `controls/v4/K4EasyOnly.md:52,471`. Its re-measurement also names that hash. The v4 counter and generator hashes match their frozen pins. The original receipt says 4/41 in both runs, not 41/41.

Initial command, from `/home/vgpnk/Projects/shokunin`:

```sh
timeout 20 sha256sum mado-shokunin/.ufo/waves/round-25/controls/v4/K4EasyOnly.py mado-shokunin/.ufo/waves/round-25/c1/count.py mado-shokunin/.ufo/waves/round-25/c1/count-v3.py
```

Observed output:

```text
fe5b5cc00af51d81cb6385e762b0488a5fb8eac4d7652cf7a65090e7a4c96648  mado-shokunin/.ufo/waves/round-25/controls/v4/K4EasyOnly.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  mado-shokunin/.ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  mado-shokunin/.ufo/waves/round-25/c1/count-v3.py
```

## Attack and same-shape strengthening

The original is not the strongest easy-only parser: `line()` expands only the RHS, although ordinary keyword text can itself contain a variable. The [hyprlang v0.6.8 `CConfig::parseLine` source](https://raw.githubusercontent.com/hyprwm/hyprlang/v0.6.8/src/config.cpp) was opened directly; the `ISVARIABLE`/`LHSIT` code substitutes known variables in the LHS unless that LHS is itself a variable definition. This is variable expansion, not an additional bind-grammar feature.

The minimal counterexample is:

```ini
$suffix = nd
bi$suffix = SUPER SHIFT, F13, exec, printf edge
```

After expansion this is an ordinary canonical-modifier named-key bind. The original bytes emit `[]`; the stronger bytes emit the expected one-entry, 18-field table. The change is exactly one behavior-bearing line, after the variable-definition early return:

```python
keyword = self.expand(keyword)
```

The stronger file is `/fast/scratch/hyaku/mado-r25a3/rm/K4EasyOnly-strong.py`, SHA-256 `c911b86630a4b74fd72967a6440cb72b5b51db9cf565e62e1053cc4bcb7a5814`. No other source changes were made. It remains easy-only and cache-free; none of the forbidden work was added. This establishes a concrete allowed strengthening, not an exhaustive optimality claim for all possible easy-only implementations.

Both fresh-seed v4 runs passed the oracle guard and only SYNTH-0 through SYNTH-3 passed. BASE retained the same 44 missing / 42 extra entries, including literal `code:10`/`code:11` where the oracle has actual keycodes. Every HARD case failed. The allowed strengthening did not meet the frozen predicate and did not improve its observed 4/41 score. These two fresh-seed misses are not a claim that v4 killed or that a mutant survived: its whole-counter baseline already fails.

## Exact v4 commands and receipts

Working directory for both successful launches: `/home/vgpnk/Projects/shokunin/mado-shokunin`. One fresh seed each; no seed override or tuning/rerun after a scored miss. The specified counter invocation is wrapped in a 4,000,000,000-byte address-space cap, uses the supplied compositor signature, and adds `-B` to avoid writing lane bytecode. Outer execution deadlines were 1250 seconds; the counter timeout was 1200 seconds. An initial asynchronous tool launch was refused with `Background job limit reached (100). Wait for running jobs to finish or cancel one.` It launched no counter; the subsequent synchronous original run below is the sole original measurement.

### Committed control re-measure — seed 470e2219c04589de

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 prlimit --as=4000000000 -- timeout 1200 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EasyOnly.py
```

Verbatim counter stdout, with the observed exit status appended:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EasyOnly.py sha256:fe5b5cc00af51d81cb6385e762b0488a5fb8eac4d7652cf7a65090e7a4c96648
seed=470e2219c04589de
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=44 extra=42 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE ADD-0        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE ADD-1        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE ADD-2        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE ADD-3        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-0     FAIL missing=44 extra=42 oracle_binds=191 (UNBIND mask=72 key='LEFT' keycode=0) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-1     FAIL missing=43 extra=41 oracle_binds=191 (UNBIND mask=65 key='' keycode=13) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-2     FAIL missing=44 extra=42 oracle_binds=190 (UNBIND mask=9 key='TAB' keycode=0) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-3     FAIL missing=43 extra=41 oracle_binds=191 (UNBIND mask=73 key='' keycode=19) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-0   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vcujyygs) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-1   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vohabkuq) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-2   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vkaabdsd) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-3   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vvuattwk) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-0     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 17) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-1     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 19) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-2     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 11) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-3     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 32) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE GLOB-0       FAIL missing=44 extra=42 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE GLOB-1       FAIL missing=44 extra=42 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE GLOB-2       FAIL missing=44 extra=42 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE GLOB-3       FAIL missing=44 extra=42 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNSOURCED-0  FAIL missing=44 extra=42 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNSOURCED-1  FAIL missing=44 extra=42 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNSOURCED-2  FAIL missing=44 extra=42 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNSOURCED-3  FAIL missing=44 extra=42 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE COMMENT-0    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE COMMENT-1    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE COMMENT-2    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE COMMENT-3    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    FAIL missing=169 extra=165 oracle_binds=192 (REWRITE argswap mask=8 key='XF86AudioLowerVolume' code=0; unbind mask=73 key='' code=15; add exec) v3_model=agree
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    missing mask=1 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
CASE REWRITE-1    FAIL missing=169 extra=157 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioPrev' code=0; unbind mask=64 key='TAB' code=0; add movetoworkspacesilent) v3_model=agree
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    missing mask=1 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
CASE REWRITE-2    FAIL missing=169 extra=166 oracle_binds=192 (REWRITE argswap mask=64 key='X' code=0; unbind mask=65 key='M' code=0; add moveintogroup) v3_model=agree
    missing mask=13 key="8" code=0 disp="moveintogroup" arg="u"
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="8" code=0 disp="moveintogroup" arg="u"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
CASE REWRITE-3    FAIL missing=169 extra=164 oracle_binds=192 (REWRITE argswap mask=68 key='H' code=0; unbind mask=73 key='' code=10; add resizeactive) v3_model=agree
    missing mask=4 key="M" code=0 disp="resizeactive" arg="-100 0"
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="M" code=0 disp="resizeactive" arg="-100 0"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
CASE HARD-0       FAIL missing=20 extra=9 oracle_binds=21 (HARD tree lines=28 binds=21 unbinds=2 vars=4) v3_model=agree
    missing mask=65 key="mouse:273" code=0 disp="mouse" arg="resizewindow"
    missing mask=0 key="" code=215 disp="exec" arg="notify-send bb0thj"
    extra   mask=0 key="mouse:274" code=0 disp="movetoworkspacesilent" arg="e-1"
    extra   mask=4 key="F17" code=0 disp="MOVEOUTOFGROUP" arg=""
CASE HARD-1       FAIL missing=25 extra=8 oracle_binds=25 (HARD tree lines=33 binds=25 unbinds=2 vars=4) v3_model=agree
    missing mask=64 key="0" code=0 disp="sendshortcut" arg="CONTROL, 6, activewindow"
    missing mask=64 key="mouse:274" code=0 disp="mouse" arg="resizewindow"
    extra   mask=0 key="SPACE" code=0 disp="exec" arg="ox9vc9"
    extra   mask=0 key="code:142" code=0 disp="Togglefloating" arg="6ps4"
CASE HARD-2       FAIL missing=17 extra=10 oracle_binds=17 (HARD tree lines=27 binds=17 unbinds=3 vars=4) v3_model=agree
    missing mask=73 key="" code=60 disp="swapwindow" arg="r"
    missing mask=72 key="mouse:273" code=0 disp="mouse" arg="resizewindow"
    extra   mask=72 key="code:60" code=0 disp="swapwindow" arg="r"
    extra   mask=0 key="112" code=0 disp="movefocus" arg="d"
CASE HARD-3       FAIL missing=22 extra=8 oracle_binds=23 (HARD tree lines=31 binds=23 unbinds=2 vars=4) v3_model=agree
    missing mask=65 key="8" code=0 disp="changegroupactive" arg="0d30"
    missing mask=69 key="SLASH" code=0 disp="fullscreen" arg=""
    extra   mask=0 key="SLASH" code=0 disp="FULLSCREEN" arg=""
    extra   mask=8 key="F21" code=0 disp="LAYOUTMSG" arg="eavm"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=4/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### Stronger control — seed d8855f5c656eb184

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 prlimit --as=4000000000 -- timeout 1200 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /fast/scratch/hyaku/mado-r25a3/rm/K4EasyOnly-strong.py
```

Verbatim counter stdout, with the observed exit status appended:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/rm/K4EasyOnly-strong.py sha256:c911b86630a4b74fd72967a6440cb72b5b51db9cf565e62e1053cc4bcb7a5814
seed=d8855f5c656eb184
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=44 extra=42 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE ADD-0        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE ADD-1        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE ADD-2        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE ADD-3        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-0     FAIL missing=44 extra=42 oracle_binds=191 (UNBIND mask=72 key='RIGHT' keycode=0) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-1     FAIL missing=43 extra=41 oracle_binds=191 (UNBIND mask=65 key='' keycode=21) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-2     FAIL missing=44 extra=42 oracle_binds=191 (UNBIND mask=68 key='T' keycode=0) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-3     FAIL missing=44 extra=42 oracle_binds=191 (UNBIND mask=64 key='V' keycode=0) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-0   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vxzmouxy) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-1   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $veexufbk) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-2   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vahdysze) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-3   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vnabtsdd) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-0     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-1     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 13) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-2     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-3     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 17) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE GLOB-0       FAIL missing=44 extra=42 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE GLOB-1       FAIL missing=44 extra=42 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE GLOB-2       FAIL missing=44 extra=42 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE GLOB-3       FAIL missing=44 extra=42 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNSOURCED-0  FAIL missing=44 extra=42 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNSOURCED-1  FAIL missing=44 extra=42 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNSOURCED-2  FAIL missing=44 extra=42 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNSOURCED-3  FAIL missing=44 extra=42 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE COMMENT-0    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE COMMENT-1    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE COMMENT-2    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE COMMENT-3    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=2) v3_model=agree
CASE REWRITE-0    FAIL missing=170 extra=167 oracle_binds=192 (REWRITE argswap mask=76 key='Z' code=0; unbind mask=0 key='XF86AudioLowerVolume' code=0; add workspace) v3_model=agree
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    missing mask=1 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
CASE REWRITE-1    FAIL missing=169 extra=165 oracle_binds=192 (REWRITE argswap mask=65 key='C' code=0; unbind mask=73 key='' code=19; add workspace) v3_model=agree
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    missing mask=1 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
CASE REWRITE-2    FAIL missing=169 extra=166 oracle_binds=192 (REWRITE argswap mask=65 key='TAB' code=0; unbind mask=68 key='E' code=0; add swapwindow) v3_model=agree
    missing mask=8 key="PERIOD" code=0 disp="swapwindow" arg="d"
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="PERIOD" code=0 disp="swapwindow" arg="d"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
CASE REWRITE-3    FAIL missing=169 extra=165 oracle_binds=192 (REWRITE argswap mask=72 key='G' code=0; unbind mask=65 key='' code=15; add movetoworkspacesilent) v3_model=agree
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    missing mask=1 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
CASE HARD-0       FAIL missing=22 extra=10 oracle_binds=22 (HARD tree lines=35 binds=22 unbinds=2 vars=4) v3_model=agree
    missing mask=13 key="F10" code=0 disp="sendshortcut" arg="Shift, 2, activewindow"
    missing mask=76 key="" code=207 disp="movetoworkspace" arg="e-1"
    extra   mask=0 key="catchall" code=0 disp="exec" arg="oqitaj"
    extra   mask=0 key="F10" code=0 disp="sendshortcut" arg="Shift, 2, activewindow"
CASE HARD-1       FAIL missing=18 extra=11 oracle_binds=18 (HARD tree lines=30 binds=18 unbinds=3 vars=4) v3_model=agree
    missing mask=72 key="" code=229 disp="swapwindow" arg="u"
    missing mask=0 key="" code=118 disp="togglespecialworkspace" arg=""
    extra   mask=0 key="code:229" code=0 disp="swapwindow" arg="u"
    extra   mask=0 key="code:218" code=0 disp="Movecurrentworkspacetomonitor" arg="u"
CASE HARD-2       FAIL missing=22 extra=6 oracle_binds=22 (HARD tree lines=26 binds=22 unbinds=2 vars=4) v3_model=agree
    missing mask=64 key="EQUAL" code=0 disp="killactive" arg="6zs0"
    missing mask=64 key="" code=180 disp="togglefloating" arg=""
    extra   mask=0 key="EQUAL" code=0 disp="killactive" arg="6zs0"
    extra   mask=0 key="4" code=0 disp="layoutmsg" arg="msf5"
CASE HARD-3       FAIL missing=22 extra=8 oracle_binds=23 (HARD tree lines=33 binds=23 unbinds=3 vars=4) v3_model=agree
    missing mask=65 key="" code=123 disp="togglespecialworkspace" arg=""
    missing mask=65 key="" code=20 disp="workspace" arg="special:4k48"
    extra   mask=8 key="Y" code=0 disp="movetoworkspace" arg="special:w7ak"
    extra   mask=0 key="" code=0 disp="exec" arg="3plnan"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=4/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## One bounded mutation probe

Mutant: remove only the new keyword-expansion line from the isolated stronger scratch file, thereby restoring the original RHS-only expansion defect. The mutant hash is exactly the original control's hash. The lane control was never mutated.

Expected detector: the same source-grounded public-CLI detector below must return the exact 18-field single entry for the two-line config above. Each detector run has a 15-second outer timeout and a 256 MiB address-space cap, with a 5-second inner tool timeout; temporary home trees are removed by `TemporaryDirectory`. This detector does not start Hyprland or change the v4 predicate. The full v4 counter is not claimed as the mutation detector, because its baseline misses are inconclusive for that purpose.

Exact same command on pristine stronger, mutated and restored bytes:

```sh
timeout 15 prlimit --as=268435456 -- python3 -I -B -c 'import json, pathlib, subprocess, sys, tempfile
expected = [{"locked": False, "mouse": False, "release": False, "repeat": False, "longPress": False, "non_consuming": False, "auto_consuming": False, "has_description": False, "modmask": 65, "submap": "", "submap_universal": "false", "key": "F13", "keycode": 0, "catch_all": False, "description": "", "allow_input_capture": False, "dispatcher": "exec", "arg": "printf edge"}]
with tempfile.TemporaryDirectory(prefix="K4EasyOnly-lhs-", dir="/fast/scratch/hyaku/mado-r25a3/rm") as home:
    root = pathlib.Path(home, ".config/hypr")
    root.mkdir(parents=True)
    (root / "hyprland.conf").write_text("$suffix = nd\nbi$suffix = SUPER SHIFT, F13, exec, printf edge\n")
    result = subprocess.run([sys.executable, "-I", "-B", sys.argv[1], "--home", home], capture_output=True, text=True, timeout=5)
    print("tool_stdout=" + result.stdout.strip())
    print("tool_stderr=" + result.stderr.strip())
    print("tool_exit=" + str(result.returncode))
    passed = result.returncode == 0 and json.loads(result.stdout) == expected
    print("LHS_VARIABLE_DETECTOR " + ("PASS" if passed else "FAIL"))
    sys.exit(0 if passed else 1)
' /fast/scratch/hyaku/mado-r25a3/rm/K4EasyOnly-strong.py
```

### Pristine stronger output

```text
tool_stdout=[{"locked": false, "mouse": false, "release": false, "repeat": false, "longPress": false, "non_consuming": false, "auto_consuming": false, "has_description": false, "modmask": 65, "submap": "", "submap_universal": "false", "key": "F13", "keycode": 0, "catch_all": false, "description": "", "allow_input_capture": false, "dispatcher": "exec", "arg": "printf edge"}]
tool_stderr=
tool_exit=0
LHS_VARIABLE_DETECTOR PASS
exit=0
```

Before mutation, `timeout 20 sha256sum /fast/scratch/hyaku/mado-r25a3/rm/K4EasyOnly-strong.py .ufo/waves/round-25/controls/v4/K4EasyOnly.py .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py` returned:

```text
c911b86630a4b74fd72967a6440cb72b5b51db9cf565e62e1053cc4bcb7a5814  /fast/scratch/hyaku/mado-r25a3/rm/K4EasyOnly-strong.py
fe5b5cc00af51d81cb6385e762b0488a5fb8eac4d7652cf7a65090e7a4c96648  .ufo/waves/round-25/controls/v4/K4EasyOnly.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
```

### Mutated output

The surgical scratch edit deleted line 100 (`keyword = self.expand(keyword)`). `timeout 20 sha256sum /fast/scratch/hyaku/mado-r25a3/rm/K4EasyOnly-strong.py` returned:

```text
fe5b5cc00af51d81cb6385e762b0488a5fb8eac4d7652cf7a65090e7a4c96648  /fast/scratch/hyaku/mado-r25a3/rm/K4EasyOnly-strong.py
```

```text
tool_stdout=[]
tool_stderr=
tool_exit=0
LHS_VARIABLE_DETECTOR FAIL
exit=1
```

### Restored output and exact-byte evidence

The exact deleted line was inserted after line 99. The unchanged detector then returned:

```text
tool_stdout=[{"locked": false, "mouse": false, "release": false, "repeat": false, "longPress": false, "non_consuming": false, "auto_consuming": false, "has_description": false, "modmask": 65, "submap": "", "submap_universal": "false", "key": "F13", "keycode": 0, "catch_all": false, "description": "", "allow_input_capture": false, "dispatcher": "exec", "arg": "printf edge"}]
tool_stderr=
tool_exit=0
LHS_VARIABLE_DETECTOR PASS
exit=0
```

Final command, from the lane directory:

```sh
timeout 20 sha256sum /fast/scratch/hyaku/mado-r25a3/rm/K4EasyOnly-strong.py .ufo/waves/round-25/controls/v4/K4EasyOnly.py .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py
```

Observed output:

```text
c911b86630a4b74fd72967a6440cb72b5b51db9cf565e62e1053cc4bcb7a5814  /fast/scratch/hyaku/mado-r25a3/rm/K4EasyOnly-strong.py
fe5b5cc00af51d81cb6385e762b0488a5fb8eac4d7652cf7a65090e7a4c96648  .ufo/waves/round-25/controls/v4/K4EasyOnly.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
exit=0
```

Mutation verdict: KILLED by the targeted LHS-variable detector (pristine exit 0, mutant exit 1, restored exit 0); exact stronger bytes restored, with the original control and frozen counter/generator hashes unchanged. V4 kill/survival attribution is INCONCLUSIVE, not a killed mutant inferred from an already failing counter baseline.

## Safety and touched paths

Created only the assigned report in the lane and the named stronger file in isolated scratch. All mutations were confined to that scratch file. No sibling source, lane control, frozen counter, corpus, package, service, host configuration or live compositor write was touched. No git/jj write, subagent dispatch, other model runtime, build, linter or formatter was invoked. The only nested Hyprland instances were those started and cleaned up by the frozen counter; both counter processes completed normally with exit 1. Detector subprocesses completed, and their temporary fixture scopes closed. No tool installation or update was needed.

Report: `.ufo/waves/round-25/a3w2/reports/RmEasyOnly.md`
