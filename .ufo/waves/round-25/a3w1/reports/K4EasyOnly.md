# K4EasyOnly — partial grammar, no cache

## Verdict

CONTROL K4EasyOnly v4 best: cases_pass=4/41 embed_hits=0 verdict=TARGET_MISSED — not met

Both fresh-seed runs returned exit 1 with 4/41 cases passing and no embedded-string hits. Only SYNTH-0 through SYNTH-3 passed in each run. BASE and all ADD, UNBIND, VARIABLE, SOURCE, GLOB, UNSOURCED, COMMENT, REWRITE and HARD cases failed. Neither run exited 2; no rerun or tuning followed the receipts.

## Scoped control

Axes: correctness inside the allowed easy grammar; fidelity to the forbidden-feature boundary; independent frozen-counter evidence; host safety.

Created only `.ufo/waves/round-25/controls/v4/K4EasyOnly.py` and this report. The control is a single Python standard-library file using the required `--home DIR` interface and printing an array with the 18 bind fields.

Implemented:

- Ordered, depth-first `source =` traversal with home-relative `~`, sorted globs, relative include paths and repeated includes; an active-stack guard prevents recursive source cycles, not a cache of parsed files.
- In-order variable definitions and expansion, including longest-known variable names and available environment-variable expansion.
- `#` comments and doubled `##` literal hashes.
- `unbind` applied in sequence, removing matches by canonical modifier mask and literal key string.
- `bind[dler]*`, optional descriptions, all combinations of those four letters, literal dispatchers and arguments, and comma-bearing final arguments.
- Exact canonical SUPER/SHIFT/CTRL/ALT tokens separated by whitespace. Named key strings are preserved exactly.

Deliberately absent: modifier aliases or alternate separators; keycode interpretation of `code:NN` or bare numbers; mouse-bind semantics; other flags; rejected-line rules; dispatcher validation; case lowering. Unsupported key spellings remain literal strings with keycode 0 rather than gaining prohibited semantics. Invalid short easy-bind lines are not filtered by Hyprland rejection rules. No submap grammar was added.

There is no embedded table, fixture recognition, cached source/result, counter import, compositor call or subprocess in the control. The frozen counter's easy entry defaults were read to establish the JSON field types; its complete hard-grammar model was not reused. No file at `tools/mado-binds.py` was built or edited.

## Expected detector and observed distinction

The detector is the unchanged v4 counter: exact multiset equality over all 18 fields against a nested Hyprland v0.56.2 table for every tree, plus `embed_hits=0`. The intentional defect is omitted hard grammar, not source/variable/comment/unbind omission.

Both oracle guards passed with `ORACLE_CHECK base_vs_live missing=0 extra=0`. Both BASE cases had 44 missing and 42 extra bindings; the first differences show true keycode 10/11 bindings versus this control's literal `code:10`/`code:11` keys with keycode 0. Every HARD case failed. REWRITE also failed: its lower-case modifier spellings remain outside this shape. All eight SYNTH measurements passed exactly, exercising permitted source traversal, variables, comments and unbind rather than a fixed empty response. `V3_MODEL_AGREE 41/41` appeared in both receipts as a diagnostic, not the predicate.

This is a newly constructed shortcut control, not a mutation of an existing resolver. No pristine/mutated/restored differential probe was assigned or run, so the result is a failed control, not a claimed killed mutant.

## Exact commands and receipts

Working directory for both runs: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

The runs used identical immutable control bytes, fresh random seeds and no `--seed` override. They were launched concurrently; the counter's shared six-slot oracle limit remained in effect. The explicit address-space cap applies to the counter and descendants. Each command had the specified 1200-second timeout and a 1250-second outer tool deadline.

### Run 1 — seed 54622b2331cd1a7d

```sh
prlimit --as=4000000000 -- timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EasyOnly.py
```

Verbatim stdout, with the observed exit status appended:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EasyOnly.py sha256:fe5b5cc00af51d81cb6385e762b0488a5fb8eac4d7652cf7a65090e7a4c96648
seed=54622b2331cd1a7d
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=44 extra=42 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE ADD-0        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE ADD-1        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
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
CASE UNBIND-0     FAIL missing=44 extra=42 oracle_binds=191 (UNBIND mask=65 key='UP' keycode=0) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-1     FAIL missing=43 extra=41 oracle_binds=191 (UNBIND mask=65 key='' keycode=14) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-2     FAIL missing=44 extra=42 oracle_binds=191 (UNBIND mask=68 key='H' keycode=0) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-3     FAIL missing=44 extra=42 oracle_binds=191 (UNBIND mask=68 key='S' keycode=0) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-0   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vukgtkva) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-1   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vflkyaoq) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-2   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vkzxyute) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-3   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vjdhycla) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-0     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-1     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 13) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-2     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 9) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-3     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 23) v3_model=agree
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
CASE COMMENT-0    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE COMMENT-1    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE COMMENT-2    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE COMMENT-3    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=3) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=3) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    FAIL missing=169 extra=167 oracle_binds=192 (REWRITE argswap mask=64 key='' code=18; unbind mask=12 key='DELETE' code=0; add exec) v3_model=agree
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    missing mask=1 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
CASE REWRITE-1    FAIL missing=169 extra=165 oracle_binds=192 (REWRITE argswap mask=65 key='' code=10; unbind mask=64 key='T' code=0; add movetoworkspace) v3_model=agree
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    missing mask=1 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
CASE REWRITE-2    FAIL missing=169 extra=163 oracle_binds=192 (REWRITE argswap mask=68 key='I' code=0; unbind mask=65 key='F' code=0; add exec) v3_model=agree
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    missing mask=1 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
CASE REWRITE-3    FAIL missing=169 extra=163 oracle_binds=192 (REWRITE argswap mask=65 key='' code=12; unbind mask=64 key='COMMA' code=0; add focusmonitor) v3_model=agree
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    missing mask=1 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
CASE HARD-0       FAIL missing=17 extra=9 oracle_binds=17 (HARD tree lines=27 binds=17 unbinds=3 vars=4) v3_model=agree
    missing mask=13 key="" code=19 disp="togglegroup" arg="uapm"
    missing mask=13 key="mouse:274" code=0 disp="changegroupactive" arg="311k"
    extra   mask=4 key="19" code=0 disp="Togglegroup" arg="uapm"
    extra   mask=0 key="mouse:274" code=0 disp="changegroupactive" arg="311k"
CASE HARD-1       FAIL missing=19 extra=7 oracle_binds=20 (HARD tree lines=29 binds=20 unbinds=3 vars=4) v3_model=agree
    missing mask=68 key="" code=165 disp="workspace" arg="special:kxwe"
    missing mask=68 key="mouse_up" code=0 disp="moveintogroup" arg="r"
    extra   mask=0 key="165" code=0 disp="Workspace" arg="special:kxwe"
    extra   mask=0 key="mouse_up" code=0 disp="moveintogroup" arg="r"
CASE HARD-2       FAIL missing=21 extra=8 oracle_binds=21 (HARD tree lines=30 binds=21 unbinds=3 vars=4) v3_model=agree
    missing mask=72 key="F13" code=0 disp="workspace" arg="e-1"
    missing mask=64 key="mouse:273" code=0 disp="mouse" arg="MoveWindow"
    extra   mask=0 key="H" code=0 disp="togglespecialworkspace" arg="nrni"
    extra   mask=5 key="code:190" code=0 disp="focusmonitor" arg="l"
CASE HARD-3       FAIL missing=23 extra=10 oracle_binds=23 (HARD tree lines=32 binds=23 unbinds=2 vars=4) v3_model=agree
    missing mask=1 key="" code=210 disp="movetoworkspace" arg="15"
    missing mask=1 key="8" code=0 disp="fullscreen" arg="1bge"
    extra   mask=0 key="233" code=0 disp="layoutmsg" arg="zpfu"
    extra   mask=4 key="code:99" code=0 disp="togglespecialworkspace" arg="ajul"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=4/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### Run 2 — seed 47ea6a3943768c9a

```sh
prlimit --as=4000000000 -- timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EasyOnly.py
```

Verbatim stdout, with the observed exit status appended:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EasyOnly.py sha256:fe5b5cc00af51d81cb6385e762b0488a5fb8eac4d7652cf7a65090e7a4c96648
seed=47ea6a3943768c9a
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
CASE ADD-1        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE ADD-2        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE ADD-3        FAIL missing=44 extra=42 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-0     FAIL missing=44 extra=42 oracle_binds=191 (UNBIND mask=73 key='B' keycode=0) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-1     FAIL missing=44 extra=42 oracle_binds=191 (UNBIND mask=64 key='P' keycode=0) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-2     FAIL missing=44 extra=42 oracle_binds=191 (UNBIND mask=72 key='RIGHT' keycode=0) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE UNBIND-3     FAIL missing=44 extra=42 oracle_binds=191 (UNBIND mask=72 key='DOWN' keycode=0) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-0   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vgdbvvvq) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-1   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vdabznlx) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-2   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vhjtukfq) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE VARIABLE-3   FAIL missing=44 extra=42 oracle_binds=193 (VARIABLE $vpeqsneq) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-0     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 13) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-1     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-2     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE SOURCE-3     FAIL missing=44 extra=42 oracle_binds=194 (SOURCE new file at root line 5) v3_model=agree
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
CASE COMMENT-0    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
    extra   mask=64 key="code:10" code=0 disp="workspace" arg="1"
    extra   mask=64 key="code:11" code=0 disp="workspace" arg="2"
CASE COMMENT-1    FAIL missing=44 extra=42 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
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
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    FAIL missing=169 extra=163 oracle_binds=192 (REWRITE argswap mask=68 key='BACKSPACE' code=0; unbind mask=68 key='RIGHT' code=0; add exec) v3_model=agree
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    missing mask=1 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
CASE REWRITE-1    FAIL missing=169 extra=165 oracle_binds=192 (REWRITE argswap mask=65 key='SLASH' code=0; unbind mask=65 key='BACKSPACE' code=0; add exec) v3_model=agree
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    missing mask=1 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
CASE REWRITE-2    FAIL missing=169 extra=164 oracle_binds=192 (REWRITE argswap mask=64 key='G' code=0; unbind mask=73 key='X' code=0; add exec) v3_model=agree
    missing mask=64 key="F21" code=0 disp="exec" arg="omarchy-hyprland-monitor-internal toggle"
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="F21" code=0 disp="exec" arg="omarchy-hyprland-monitor-internal toggle"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
CASE REWRITE-3    FAIL missing=169 extra=157 oracle_binds=192 (REWRITE argswap mask=73 key='' code=14; unbind mask=65 key='TAB' code=0; add exec) v3_model=agree
    missing mask=1 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    missing mask=1 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
    extra   mask=0 key="XF86MonBrightnessUp" code=0 disp="exec" arg="omarchy-brightness-display 100%"
    extra   mask=0 key="XF86MonBrightnessDown" code=0 disp="exec" arg="omarchy-brightness-display 1%"
CASE HARD-0       FAIL missing=22 extra=13 oracle_binds=23 (HARD tree lines=31 binds=23 unbinds=3 vars=4) v3_model=agree
    missing mask=13 key="F" code=0 disp="workspace" arg="e-1"
    missing mask=69 key="8" code=0 disp="fullscreenstate" arg=""
    extra   mask=0 key="D" code=0 disp="" arg=""
    extra   mask=0 key="code:65" code=0 disp="CYCLENEXT" arg="xumw"
CASE HARD-1       FAIL missing=13 extra=11 oracle_binds=13 (HARD tree lines=27 binds=13 unbinds=3 vars=4) v3_model=agree
    missing mask=0 key="mouse_up" code=0 disp="fullscreen" arg=""
    missing mask=1 key="G" code=0 disp="exec" arg="uwsm-app -- 6edmck printf nzbo7,kyc"
    extra   mask=0 key="code:145" code=0 disp="togglespecialworkspace" arg=""
    extra   mask=64 key="code:134" code=0 disp="MOVEFOCUS" arg="l"
CASE HARD-2       FAIL missing=24 extra=11 oracle_binds=24 (HARD tree lines=31 binds=24 unbinds=3 vars=4) v3_model=agree
    missing mask=64 key="LEFT" code=0 disp="resizeactive" arg="-37 -10"
    missing mask=4 key="" code=191 disp="bringactivetotop" arg=""
    extra   mask=0 key="LEFT" code=0 disp="Resizeactive" arg="-37 -10"
    extra   mask=0 key="code:191" code=0 disp="BRINGACTIVETOTOP" arg=""
CASE HARD-3       FAIL missing=19 extra=12 oracle_binds=20 (HARD tree lines=29 binds=20 unbinds=2 vars=4) v3_model=agree
    missing mask=64 key="" code=139 disp="bringactivetotop" arg="l7cs"
    missing mask=4 key="" code=197 disp="movecurrentworkspacetomonitor" arg="d"
    extra   mask=0 key="code:139" code=0 disp="bringactivetotop" arg="l7cs"
    extra   mask=0 key="code:197" code=0 disp="movecurrentworkspacetomonitor" arg="d"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=4/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Before/after and restoration evidence

The same command was run immediately before and after the scoring pair:

```sh
sha256sum .ufo/waves/round-25/controls/v4/K4EasyOnly.py .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py
```

Both invocations produced identical hashes:

```text
fe5b5cc00af51d81cb6385e762b0488a5fb8eac4d7652cf7a65090e7a4c96648  .ufo/waves/round-25/controls/v4/K4EasyOnly.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
```

No original bytes were overwritten or required restoration. The new control remains at its mandated output path. No counter edit, sibling-source edit, corpus edit, git/jj write, package transaction, service change or live-compositor write verb was invoked. The only nested instances were those managed by the frozen counter's process-group cleanup; both bounded counter commands completed normally with exit 1. No independent nested compositor was started.

`df -h /fast` reported 221G available before the runs. No tooling installation or update was needed. Apart from the two explicitly assigned behavioral measurements and before/after hashes, no build, test suite, linter or formatter was run.
