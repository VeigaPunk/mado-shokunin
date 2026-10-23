# RmEcho — independent K4Echo re-measure

REMEASURE K4Echo: 0/41 (receipt said 0/41); strengthened: not attempted — not met

## Scope and expected detector

Axes: server-echo strength, measurement fidelity, and host/sibling safety. The assigned control replaces static config resolution with asking an already running compositor for its bind array. The detector is the unchanged frozen C1 v4 counter: target 41/41 and embed_hits=0. This report re-measures that existing control, not a newly introduced feature-ablation mutant. Its failure is a rejected shortcut, not evidence that a new mutation was killed against a passing pristine resolver.

Exactly one counter invocation executed, with a fresh seed. An attempted asynchronous bash launch was rejected before execution with `Background job limit reached (100). Wait for running jobs to finish or cancel one.` It produced no seed or counter receipt. The actual invocation below ran through Python subprocess orchestration, with the requested live-session environment, a 1200-second timeout, a 4,000,000,000-byte address-space limit, and `-B` to prevent lane bytecode writes. No rule or control bytes changed.

## Identity and preservation

The receipt names control sha256 `a0458dfeea7254092ccc9b26960b37242a6496ec56441c96f24ebcc8a1168ef0` at `controls/v4/K4Echo.md:153,464`. The working file, the committed blob at `459dd17f`, and the new counter receipt all name that exact hash.

Commands executed from the lane root:

```sh
timeout 10 prlimit --as=4000000000 sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Echo.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count-v3.py
```

This command ran before and after the measurement. Both outputs were identical (absolute paths shortened here only):

```text
a0458dfeea7254092ccc9b26960b37242a6496ec56441c96f24ebcc8a1168ef0  controls/v4/K4Echo.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  c1/count-v3.py
```

Committed-blob check:

```sh
timeout 10 prlimit --as=4000000000 git show 459dd17f:.ufo/waves/round-25/controls/v4/K4Echo.py | timeout 10 prlimit --as=4000000000 sha256sum
```

```text
a0458dfeea7254092ccc9b26960b37242a6496ec56441c96f24ebcc8a1168ef0  -
```

## Independent measurement

Exact command, with working directory `/home/vgpnk/Projects/shokunin/mado-shokunin`:

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 timeout 1200 prlimit --as=4000000000 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Echo.py
```

Counter stdout, verbatim, followed by its observed exit status:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Echo.py sha256:a0458dfeea7254092ccc9b26960b37242a6496ec56441c96f24ebcc8a1168ef0
seed=afbf9f59093bae68
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=65 key='E' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=72 key='DOWN' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=76 key='T' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=65 key='B' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vbktbtmu) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vehouhpy) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vklmultp) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vnkazzzc) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 4) v3_model=agree
    missing mask=73 key="INSERT" code=0 disp="exec" arg="logger bj4hdzhpsv"
    missing mask=69 key="V" code=0 disp="exec" arg="printf 9zsnydf0sk"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 18) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 12) v3_model=agree
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
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=12 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=72 key="0" code=0 disp="exec" arg="logger h9ubybstui"
    missing mask=76 key="COMMA" code=0 disp="exec" arg="printf tuo2kh1j4k"
CASE SYNTH-1      FAIL missing=14 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
    missing mask=1 key="F" code=0 disp="exec" arg="logger i8s58lt3kx"
    missing mask=69 key="F4" code=0 disp="exec" arg="kjzhh56ro gso8"
CASE SYNTH-2      FAIL missing=14 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
    missing mask=64 key="F14" code=0 disp="exec" arg="printf xuse449p0t"
    missing mask=4 key="F20" code=0 disp="exec" arg="printf m9ql2jg0a8"
CASE SYNTH-3      FAIL missing=11 extra=0 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=3) v3_model=agree
    missing mask=13 key="LEFT" code=0 disp="exec" arg="true kklndsshns"
    missing mask=5 key="R" code=0 disp="exec" arg="logger 9bqh7lhlat"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=69 key='G' code=0; unbind mask=68 key='LEFT' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='S' code=0; unbind mask=68 key='H' code=0; add movetoworkspace) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='' code=15; unbind mask=68 key='Delete' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='' code=10; unbind mask=68 key='Delete' code=0; add movetoworkspacesilent) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=21 extra=0 oracle_binds=21 (HARD tree lines=31 binds=21 unbinds=2 vars=4) v3_model=agree
    missing mask=68 key="E" code=0 disp="pseudo" arg=""
    missing mask=4 key="F19" code=0 disp="togglefloating" arg=""
CASE HARD-1       FAIL missing=21 extra=0 oracle_binds=21 (HARD tree lines=26 binds=21 unbinds=2 vars=4) v3_model=agree
    missing mask=13 key="mouse_down" code=0 disp="fullscreen" arg="zfie"
    missing mask=0 key="5" code=0 disp="bringactivetotop" arg=""
CASE HARD-2       FAIL missing=26 extra=0 oracle_binds=26 (HARD tree lines=34 binds=26 unbinds=3 vars=4) v3_model=agree
    missing mask=0 key="F15" code=0 disp="sendshortcut" arg="shift, 5, activewindow"
    missing mask=72 key="3" code=0 disp="layoutmsg" arg=""
CASE HARD-3       FAIL missing=26 extra=0 oracle_binds=26 (HARD tree lines=34 binds=26 unbinds=2 vars=4) v3_model=agree
    missing mask=64 key="SLASH" code=0 disp="togglespecialworkspace" arg=""
    missing mask=0 key="" code=12 disp="movetoworkspacesilent" arg="special:u6gp"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Stderr was empty. Elapsed time: 76.656 seconds. This is a completed measurement, not an environment failure: ORACLE_CHECK matched, all 41 cases were scored, and PRED-C1 (v4) reported TARGET_MISSED. All cases had zero extra entries and every expected entry missing.

## Attack on the shape claim

The implementation really is a server echo. Inspection of the complete 256-line control found no config parser, embedded bind table, generator grammar, fixture/label selection, or compositor launcher. `--home` is accepted and deliberately unused (`K4Echo.py:203-206`). The program calls `hyprctl binds -j`, falls back to instance discovery, then probes discovered read-only command sockets (`:209-247`); the socket request is exactly `j/binds` (`:177-200`). It prints the first valid JSON array of objects, or `[]` when discovery fails (`:248-251`). It goes materially beyond a weak one-command echo: filesystem discovery, visible compositor process context, Unix socket tables, instance-specific queries, and conventional abstract addresses are all present.

The receipt's explanation is supported by the actual sandbox argv (`c1/count-v3.py:729-743`, reused at `c1/count.py:72-74`): no `/run` bind, private `/tmp`, cleared compositor-related environment, private PID/network namespaces, and only `/usr`, the case snapshot, the control file, fresh `/proc`, and `/dev` exposed. Its omitted scan of `/snap/home` does not identify a stronger existing-compositor route: `copy_roots` copies only regular-file bytes, not sockets (`count-v3.py:96-119`). The oracle instances are also completed and cleaned before tool scoring begins (`count.py:255-281`; oracle process-group cleanup `:174-189`). Merely guessing a signature cannot restore a missing filesystem endpoint or a compositor absent from the tool's namespaces.

[INFERENCE] No meaningful stronger server-echo implementation was identified within this sandbox and this shape. Extending the same endpoint guesses does not address the missing compositor; launching a compositor, parsing configs/deltas, embedding a table, or bypassing isolation would change the assigned shape or violate its bounds. Therefore no strengthened file was written and no second score was attempted. This is not a proof that the control covers every conceivable socket name or environment: the conclusion is scoped to the frozen counter and the inspected server-echo avenues. Successful tool stderr is suppressed by `run_tool`, so the old receipt's detailed diagnostic JSON was not independently reproduced and is not presented as fresh observation.

## Restoration and safety

No existing bytes were mutated, and no scratch implementation was created; restoration was therefore unnecessary. Before/after control and counter/generator hashes are identical, and the committed control hash also agrees. A pristine/mutated/restored detector triplet does not apply to this unchanged-control re-measure; no extra runs were made under that label. The counter subprocess returned normally (exit 1); its inspected finally paths own nested process-group teardown and temporary-directory removal. No independent orphan-process census was run. No manual compositor start or write verb, package/tool installation or update, runtime invocation, git/jj write, subagent dispatch, or peer-source edit occurred. Only this requested report was written in the lane.

REMEASURE K4Echo: 0/41 (receipt said 0/41); strengthened: not attempted — not met
