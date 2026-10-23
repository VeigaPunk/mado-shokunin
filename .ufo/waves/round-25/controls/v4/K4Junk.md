# K4Junk — frozen v4 JUNK control

## Verdict
CONTROL K4Junk v4 best: cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED — not met

Both requested fresh-seed runs measured 0/41 with embed_hits=0 and exit=1. Neither exited 2, so no retry was made. This is a mechanical counter result, not a canonical judgment or a saturation claim about other controls.

## Scope, axes and implementation

Read registration.md first, including its current Attempt 3 / PRED-C1 (v4) section. Axes examined: C1 exact bind-table operability, resistance to schema-only shortcut output, evidence provenance, and host non-interference.

The only program written is `.ufo/waves/round-25/controls/v4/K4Junk.py` (1,543 bytes; sha256:0dd447855262b6ad6652a18e86928614994c8f296b064a865acd8890068175b6). Its interface is `python3 -I K4Junk.py --home DIR`. It opens only `DIR/.config/hypr/hyprland.conf`, counts binary lines beginning literally with `bind`, and emits exactly that many objects. Leading whitespace is not stripped. No bind fields are parsed.

Every object has all 18 counter field names, with the expected scalar types, including the string-valued `submap_universal`. Keys, args, descriptions, modifier masks and boolean flags are freshly random; the dispatcher is `exec`, submap is empty, keycode is zero, and catch_all is false. Flags are content-free independent booleans, not a claim that each invented combination could be produced by a valid bind declaration. Type-correct output makes this stronger than the older all-integer junk shape without doing the forbidden resolver work.

The control follows no sources or globs, expands no variables, interprets no comments or unbinds, embeds no live table, detects no case labels, and invokes no compositor or subprocess. All randomness comes from Python's SystemRandom; a counter seed replays case generation, not the control's random output. No claimed `tools/mado-binds.py` was built or edited.

## Counterexample, evidence and smallest safe correction

The strongest observed counterexample is already BASE: in both runs the root-only count produces `[]`, while the independent oracle contains 192 binds (`missing=192 extra=0`). SOURCE-0 then contains 194 oracle binds but still receives `[]` (`missing=194 extra=0`). SOURCE changes the source graph without introducing a root bind declaration; a root-count-only output cannot represent either table. This is an information-loss barrier of the shape, not a random-seed near miss.

The control also exercised its nonempty object generation. Run 1 SYNTH-0 yielded eight invented entries against thirteen oracle entries (`missing=13 extra=8`); run 2 SYNTH-0 yielded seven against eleven (`missing=11 extra=7`). Thus rejection was not only rejection of empty output: all-field JSON objects passed output decoding and still failed exact multiset comparison. VARIABLE and HARD likewise show invented extra entries with random args.

Both receipts show `ORACLE_CHECK base_vs_live missing=0 extra=0`, unchanged pinned counter/generator hashes, and `V3_MODEL_AGREE 41/41`. The last line is diagnostic only and is not substituted for Hyprland's oracle. These runs demonstrate no counter defect and do not establish that every possible shortcut fails.

Impacted axes: C1 source-graph coverage and exact field semantics are absent in this shape; provenance remains explicit because the receipt names the override and its hash. The smallest safe correction is to retain the frozen exact 18-field multiset predicate and report this control's miss. Changing this control into a real parser would leave its assigned shape; changing the counter to accept counts or JSON shape would weaken the claim. There is no tradeoff here that satisfies PRED-C1 (v4), and no canonical judgment was invoked.

## Exact commands and isolation

Execution directory for the following commands: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Prerequisite observations:

```sh
timeout 10 sha256sum .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py && timeout 10 df -h /fast
timeout 10 prlimit --as=4000000000 printenv HYPRLAND_INSTANCE_SIGNATURE WAYLAND_DISPLAY XDG_RUNTIME_DIR HOME
```

Observed counter sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 and generator sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375. `/fast` had 221G available. The inherited environment already supplied the live session signature, WAYLAND_DISPLAY=wayland-1, XDG_RUNTIME_DIR=/run/user/1000 and HOME=/home/vgpnk; it was not modified.

Run 1 and run 2 used this identical argv, concurrently, without --seed or counter changes:

```sh
timeout 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Junk.py
```

The outer 4,000,000,000-byte address-space limit applies to the counter and is inherited by its children. Both commands finished normally with exit 1 (15.03 s and 22.40 s). Only the prescribed counter started nested compositors; its shared six-slot locks bound concurrency. Its oracle finally block terminates and waits for each own process group before scoring, and its outer finally removes the temporary trees. No independent nested compositor or other long-lived process was started by this seat.

No packages or tools were installed or updated. No live compositor write verb, git/jj write command, config change, counter edit, corpus edit or claimed-tool edit was made. Only the assigned control program and this report were written directly by this seat; the counter's prescribed temporary trees and slot locks are its own documented side effects. No checks beyond the two assigned counter measurements were run.

## Run 1 receipt — stdout verbatim, then exit

Original captured output: artifact://5727. Tool timing/status footer is not counter stdout; its observed status is rendered as `exit=1` below.

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Junk.py sha256:0dd447855262b6ad6652a18e86928614994c8f296b064a865acd8890068175b6
seed=ae346e2ab45d17e4
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=73 key='TAB' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=64 key='F' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=0 key='switch:off:Lid Switch' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=0 key='XF86KbdBrightnessDown' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vdokqdjf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=75 key="Z" code=0 disp="exec" arg="5e051357255124bff4cb20c3a0f5380a"
CASE VARIABLE-1   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vgmzthlq) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=196 key="Z" code=0 disp="exec" arg="3baaf0d12d6d896e90a6623ad8e14429"
CASE VARIABLE-2   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vsfjiqmg) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=138 key="K" code=0 disp="exec" arg="42b2187e967944fb678c0adfa91d9dcf"
CASE VARIABLE-3   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vypkxnvp) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=90 key="V" code=0 disp="exec" arg="ed5a31abc71070788a908c88ecb378db"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 5) v3_model=agree
    missing mask=1 key="F15" code=0 disp="exec" arg="logger qe2lqvjhhh"
    missing mask=76 key="RIGHT" code=0 disp="exec" arg="logger vk4r9ji1za"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 19) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 32) v3_model=agree
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
CASE COMMENT-0    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=77 key="DELETE" code=0 disp="exec" arg="notify-send d8uj9dw8hj"
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=13 extra=8 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=9 key="F23" code=0 disp="exec" arg="printf ym35kwv0xu"
    missing mask=68 key="F3" code=0 disp="exec" arg="j1521tu9v vrtg"
    extra   mask=146 key="A" code=0 disp="exec" arg="dfe9310c8edec0fb1ba1bf3220bb9e1e"
    extra   mask=184 key="K" code=0 disp="exec" arg="a7ba40c05c66a281002689aa494c50c1"
CASE SYNTH-1      FAIL missing=12 extra=8 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
    missing mask=76 key="F18" code=0 disp="exec" arg="notify-send gpuacbkpb8"
    missing mask=4 key="KP_1" code=0 disp="exec" arg="k6sulwtk7 4esc"
    extra   mask=197 key="K" code=0 disp="exec" arg="21257ce679a730db67c906830d0f801e"
    extra   mask=37 key="R" code=0 disp="exec" arg="70576609cf31646fd3cf336f1ecd6705"
CASE SYNTH-2      FAIL missing=14 extra=8 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
    missing mask=65 key="KP_9" code=0 disp="exec" arg="true gvpvszskgi"
    missing mask=12 key="S" code=0 disp="exec" arg="vk7mq9bjd 7b7u"
    extra   mask=101 key="E" code=0 disp="exec" arg="e3968a1bdfc751d0cef643212f70499d"
    extra   mask=67 key="J" code=0 disp="exec" arg="7a0bb2c26b1d6c9828a3c4f363a92a1b"
CASE SYNTH-3      FAIL missing=14 extra=9 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
    missing mask=77 key="F16" code=0 disp="exec" arg="logger xr2948vsdj"
    missing mask=5 key="2" code=0 disp="exec" arg="notify-send ln36bi6ntl"
    extra   mask=109 key="P" code=0 disp="exec" arg="8801c7ca240dea40bbcd5569dc224787"
    extra   mask=91 key="W" code=0 disp="exec" arg="2cd3748be33fb9613e48522f78bf6fd4"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='B' code=0; unbind mask=0 key='XF86KbdBrightnessUp' code=0; add moveintogroup) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='TAB' code=0; unbind mask=1 key='XF86MonBrightnessDown' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='' code=18; unbind mask=64 key='UP' code=0; add resizeactive) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=72 key='mouse_up' code=0; unbind mask=64 key='UP' code=0; add sendshortcut) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=21 extra=16 oracle_binds=21 (HARD tree lines=31 binds=21 unbinds=2 vars=4) v3_model=agree
    missing mask=0 key="" code=31 disp="moveoutofgroup" arg=""
    missing mask=1 key="" code=52 disp="workspace" arg="e-1"
    extra   mask=54 key="P" code=0 disp="exec" arg="0e6795f9ad4906ceceed4fcf8276a109"
    extra   mask=30 key="0" code=0 disp="exec" arg="071a910082e928bdc6e8421cacec7eec"
CASE HARD-1       FAIL missing=22 extra=12 oracle_binds=22 (HARD tree lines=29 binds=22 unbinds=3 vars=4) v3_model=agree
    missing mask=72 key="L" code=0 disp="resizeactive" arg="26 27"
    missing mask=64 key="mouse:273" code=0 disp="mouse" arg="movewindow"
    extra   mask=249 key="9" code=0 disp="exec" arg="2395403198c7330e914fce527d41dd93"
    extra   mask=200 key="T" code=0 disp="exec" arg="aaa237c12d435188bcf0a030825fdb1e"
CASE HARD-2       FAIL missing=26 extra=14 oracle_binds=26 (HARD tree lines=31 binds=26 unbinds=2 vars=4) v3_model=agree
    missing mask=1 key="" code=226 disp="movecurrentworkspacetomonitor" arg="l"
    missing mask=64 key="KP_1" code=0 disp="pseudo" arg=""
    extra   mask=121 key="I" code=0 disp="exec" arg="23f5939bcd0cad1d5574b9d753388a5c"
    extra   mask=131 key="K" code=0 disp="exec" arg="2575679d75da6d23ece58d748d0ea436"
CASE HARD-3       FAIL missing=24 extra=16 oracle_binds=24 (HARD tree lines=32 binds=24 unbinds=1 vars=4) v3_model=agree
    missing mask=72 key="" code=229 disp="resizeactive" arg="-4 36"
    missing mask=68 key="1" code=0 disp="moveoutofgroup" arg=""
    extra   mask=151 key="8" code=0 disp="exec" arg="51a03245900819504aa19a13a88ad72f"
    extra   mask=173 key="0" code=0 disp="exec" arg="53ae10f1858bd93960eafe08014ad6c1"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Run 2 receipt — stdout verbatim, then exit

Original captured output: artifact://5750. Tool timing/status footer is not counter stdout; its observed status is rendered as `exit=1` below.

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Junk.py sha256:0dd447855262b6ad6652a18e86928614994c8f296b064a865acd8890068175b6
seed=0c9f7d7d67b0125c
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=64 key='' keycode=12) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=190 extra=0 oracle_binds=190 (UNBIND mask=0 key='F9' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=8 key='XF86MonBrightnessUp' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=72 key='DOWN' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vuhblkno) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=121 key="M" code=0 disp="exec" arg="5db77a3edc49dcaa735de6887ec1f319"
CASE VARIABLE-1   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vyqunyst) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=149 key="Q" code=0 disp="exec" arg="4cd99104ee424937e033f7eb1c49d594"
CASE VARIABLE-2   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vatwnpnt) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=176 key="8" code=0 disp="exec" arg="f0810aca11e576d17dce8fede8af0bc8"
CASE VARIABLE-3   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vygghbnd) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=49 key="R" code=0 disp="exec" arg="c512f632213ded9220b667021abb393e"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 17) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 19) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 4) v3_model=agree
    missing mask=13 key="MINUS" code=0 disp="exec" arg="notify-send tpuj7rsnms"
    missing mask=73 key="U" code=0 disp="exec" arg="logger ilt7lza2qa"
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
CASE COMMENT-0    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=11 extra=7 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=3) v3_model=agree
    missing mask=9 key="1" code=0 disp="exec" arg="notify-send 307kijc9sq"
    missing mask=77 key="RIGHT" code=0 disp="exec" arg="true dvyimomxsz"
    extra   mask=157 key="3" code=0 disp="exec" arg="96fe663979491a3d509f78d33655ca85"
    extra   mask=21 key="W" code=0 disp="exec" arg="0a94eb216dee6dc94503ff1a8f90e077"
CASE SYNTH-1      FAIL missing=12 extra=6 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=76 key="N" code=0 disp="exec" arg="true ftkk6v3vzt"
    missing mask=1 key="ESCAPE" code=0 disp="exec" arg="notify-send hyimvxjxkp"
    extra   mask=107 key="R" code=0 disp="exec" arg="949d744a548f7e830c2fbedb56e626f6"
    extra   mask=181 key="C" code=0 disp="exec" arg="426e0b942b79d2c4b397d710ae32985a"
CASE SYNTH-2      FAIL missing=16 extra=9 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=3) v3_model=agree
    missing mask=1 key="F24" code=0 disp="exec" arg="printf rxt596qc3k"
    missing mask=69 key="BACKSPACE" code=0 disp="exec" arg="true wz3jwhg1xl"
    extra   mask=64 key="Q" code=0 disp="exec" arg="eab4abaedc74f1b1099b47783851751d"
    extra   mask=247 key="N" code=0 disp="exec" arg="07a8259c37dc69bc7784c9eaef973f36"
CASE SYNTH-3      FAIL missing=12 extra=6 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=68 key="F18" code=0 disp="exec" arg="printf cf2ui0rpt2"
    missing mask=4 key="DELETE" code=0 disp="exec" arg="true lr57itkc9y"
    extra   mask=95 key="Z" code=0 disp="exec" arg="8074a852ac39e09866a310f37afecc57"
    extra   mask=71 key="B" code=0 disp="exec" arg="d84e1b23cda76b99f78f1c0e1c35aa23"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='' code=11; unbind mask=68 key='BACKSPACE' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=76 key='Z' code=0; unbind mask=64 key='G' code=0; add killactive) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='A' code=0; unbind mask=72 key='S' code=0; add workspace) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=12 key='TAB' code=0; unbind mask=64 key='L' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=23 extra=16 oracle_binds=23 (HARD tree lines=29 binds=23 unbinds=2 vars=4) v3_model=agree
    missing mask=69 key="F5" code=0 disp="moveintogroup" arg="l"
    missing mask=1 key="V" code=0 disp="swapwindow" arg="l"
    extra   mask=206 key="8" code=0 disp="exec" arg="988ddf52d07364688922fd7d2d26998c"
    extra   mask=176 key="H" code=0 disp="exec" arg="a64ea4f3691b51e440a698e91e30bc35"
CASE HARD-1       FAIL missing=23 extra=19 oracle_binds=23 (HARD tree lines=33 binds=23 unbinds=2 vars=4) v3_model=agree
    missing mask=72 key="F10" code=0 disp="togglegroup" arg=""
    missing mask=68 key="F" code=0 disp="movefocus" arg="d"
    extra   mask=216 key="Z" code=0 disp="exec" arg="abb5a1a6f26e812ee644f3e65c8ee1e4"
    extra   mask=84 key="J" code=0 disp="exec" arg="a4c0d54500ec0b56d50bff4ec16dbbab"
CASE HARD-2       FAIL missing=22 extra=18 oracle_binds=22 (HARD tree lines=36 binds=22 unbinds=3 vars=4) v3_model=agree
    missing mask=4 key="mouse:274" code=0 disp="mouse" arg="movewindow"
    missing mask=65 key="" code=145 disp="resizeactive" arg="-60 54"
    extra   mask=108 key="5" code=0 disp="exec" arg="ba1e4d19369dc10173eb7f980327fb19"
    extra   mask=223 key="J" code=0 disp="exec" arg="b2974b313f977845532827df23a09df2"
CASE HARD-3       FAIL missing=17 extra=15 oracle_binds=17 (HARD tree lines=29 binds=17 unbinds=3 vars=4) v3_model=agree
    missing mask=64 key="F7" code=0 disp="layoutmsg" arg="z1pd"
    missing mask=4 key="mouse:272" code=0 disp="mouse" arg="resizewindow"
    extra   mask=111 key="Y" code=0 disp="exec" arg="875f74b6988603c2c861e6b2902fb4f3"
    extra   mask=184 key="R" code=0 disp="exec" arg="14ec48e3d4734a53fe734231017fd372"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```
