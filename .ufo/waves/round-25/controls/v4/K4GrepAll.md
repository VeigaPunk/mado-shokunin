# K4GrepAll — grep every bind line

## Verdict
CONTROL K4GrepAll v4 best: cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED — not met

Both completed runs missed all 41 cases, with no embedded-string hits. This is a scoped control receipt, not a claimed resolver or an admission decision. No conclusion about other shortcut shapes or counter saturation follows.

## Scope and axes

- C1 axes: operability, capability acquisition, sourced correctness.
- Review axes: control-shape fidelity, evidence provenance, host safety.
- Authored only `.ufo/waves/round-25/controls/v4/K4GrepAll.py` and this report. Did not create or edit `tools/mado-binds.py`, change any counter, change corpus content, or invoke another runtime.
- Read registration's current Attempt 3 rule first and the godspeed skill before implementation. Used the older `controls/CtlGrepAll.py` only as the local field-mapping pattern; its old receipt is not evidence for v4.

## Implemented shape

Single stdlib Python file; CLI `python3 -I K4GrepAll.py --home DIR`; JSON array of 18-field objects on stdout. Its scored sha256 is `ab04ebe701a4275329c84acb4d18599c608e80e25c7ca7b9b5aa3e66b920bd48`.

It walks every file beneath `.config/hypr`, `.config/omarchy/current/theme`, `.local/share/omarchy/default/hypr`, and `.local/state/omarchy/toggles/hypr`, without selecting file extensions or consulting `source`. It skips whole-line `#` comments, matches `bind<suffix> = ...`, and maps comma fields, flag booleans, canonical modifier names, numeric/code keys, and mouse dispatchers. Canonical names are SHIFT, CAPS, CTRL, ALT, MOD2, MOD3, SUPER and MOD5, matched case-insensitively with ordinary separator handling. The final argument retains its internal commas and whitespace. Lines lacking a handler field cannot form an entry and are skipped.

No source graph/glob evaluation, variable expansion, unbind processing, inline-comment removal, submap state, modifier aliases, dispatcher validation, or rejected-flag validation. No fixture labels, embedded bind table, oracle access, shell-outs, counter imports or real-tree special cases. This deliberately skips the claimed resolver work rather than reproducing v3's full per-line model.

## Counterexample, evidence and smallest safe correction

**Source-blind union is the strongest isolated witness.** In both fresh runs BASE has `missing=3 extra=70 oracle_binds=192`; every UNSOURCED case has `missing=3 extra=72 oracle_binds=192`. The two added extras are a direct response to a new file that Hyprland does not source. This is not just inherited base drift: the counter's frozen UNSOURCED generator writes exactly two ordinary bind lines to a fresh file without changing the root's source directives (`c1/count-v3.py:258-265`), and the actual Hyprland oracle table remains at 192. Both runs show `ORACLE_CHECK base_vs_live missing=0 extra=0`.

A flat reader is invariant to changes solely in source directives when bind lines remain unchanged, whereas Hyprland need not be. The measured UNSOURCED delta exposes the corresponding false positive without depending on variables, aliases, or hard flag grammar. Impact: sourced correctness and hence C1's exact bind-table capability, not merely JSON formatting.

Other independent skipped semantics are visible: UNBIND cases increase extras from 70 to 71 while the oracle count falls to 191; VARIABLE and COMMENT cases increase both missing and extra entries; all SYNTH and HARD cases also fail. The second receipt's SYNTH-2 provides a concrete comment witness: the oracle has arg `notify-send iseuf1f747`, while this control retains `notify-send iseuf1f747 # wv3l4`.

Smallest safe semantic correction for the source witness would be to start at `.config/hypr/hyprland.conf` and consume bind lines only through ordered source expansion. That crosses this control's expressly forbidden source-graph boundary and still would not supply its missing variables, unbind and comment semantics. Therefore the shape limitation is not a defect to conceal with filtering, fixture exclusions or relaxed equality. Keep this control unchanged; an actual resolver is separate claimed work. No counter defect is demonstrated by these receipts.

## Exact commands and setup provenance

Working directory for every command: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Counter revision resolved to `1ed41fa8301a4562d125503e5b881ec8eb5a1908`.

The inherited process environment initially had `XDG_RUNTIME_DIR=/run/user/1000`, but neither `HYPRLAND_INSTANCE_SIGNATURE` nor `WAYLAND_DISPLAY`. Two initial invocations, each followed by its required one exit-2 rerun, stopped before scoring. All four receipts are preserved below; they are setup errors, not 0/41 measurements.

Initial command (four fresh-seed invocations):

```sh
prlimit --as=4000000000 -- timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py
```

Read-only discovery command:

```sh
prlimit --as=4000000000 -- timeout 10 hyprctl instances -j
```

It exited 0, with empty stderr, identifying the oldest/live compositor as pid 1614, signature `efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120`, `wl_socket=wayland-1`. Only the child counter environment was amended from these discovered values; no compositor configuration or state was changed. The environment correction is operational setup, not an amendment to the counter or its predicate.

Completed-run command (twice, no `--seed`, no score-based rerun):

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 prlimit --as=4000000000 -- timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py
```

Each invocation was additionally bounded by a 1250-second Python subprocess timeout. Counter v4 itself performs the oracle runs and sandbox execution, including its host-wide six-slot lock. Both completed runs exited 1 normally and emitted empty stderr. Initial failures occurred before any nested oracle was started. The completed calls returned through v4's oracle process-group cleanup and temporary-directory cleanup (`c1/count.py:174-189,299-300`); no independent compositor was started by this control.

## Completed receipts (stdout and exit, verbatim)

### Run 1, attempt 1

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py sha256:ab04ebe701a4275329c84acb4d18599c608e80e25c7ca7b9b5aa3e66b920bd48
seed=b20f429c0ff84f05
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=3 extra=70 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-0        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-1        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-2        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-3        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-0     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=65 key='RIGHT' keycode=0) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-1     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=73 key='' keycode=14) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-2     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=72 key='RIGHT' keycode=0) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-3     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=65 key='SLASH' keycode=0) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-0   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vecprzvz) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-1   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vvrvuhok) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-2   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vxgwvzvf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-3   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vunyiwzl) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-0     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 23) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-1     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 16) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-2     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-3     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 16) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE GLOB-0       FAIL missing=3 extra=70 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE GLOB-1       FAIL missing=3 extra=70 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE GLOB-2       FAIL missing=3 extra=70 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE GLOB-3       FAIL missing=3 extra=70 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNSOURCED-0  FAIL missing=3 extra=72 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNSOURCED-1  FAIL missing=3 extra=72 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNSOURCED-2  FAIL missing=3 extra=72 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNSOURCED-3  FAIL missing=3 extra=72 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-0    FAIL missing=4 extra=71 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-1    FAIL missing=4 extra=71 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-2    FAIL missing=4 extra=71 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-3    FAIL missing=4 extra=71 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SYNTH-0      FAIL missing=8 extra=11 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=73 key="F9" code=0 disp="exec" arg="wejxgnx79 4tkf"
    missing mask=12 key="F4" code=0 disp="exec" arg="wejxgnx79 a4q6"
    extra   mask=13 key="F15" code=0 disp="exec" arg="logger 9r15tiaipc # k9ezm"
    extra   mask=8 key="F9" code=0 disp="exec" arg="true kh960810jt"
CASE SYNTH-1      FAIL missing=10 extra=13 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=3) v3_model=agree
    missing mask=12 key="F5" code=0 disp="exec" arg="notify-send nmh0feaysj"
    missing mask=64 key="F18" code=0 disp="exec" arg="ous6xaove 7irv"
    extra   mask=5 key="F24" code=0 disp="exec" arg="true 1h637dbavv # gg1py"
    extra   mask=65 key="S" code=0 disp="exec" arg="$szjsidjm 74p9"
CASE SYNTH-2      FAIL missing=10 extra=13 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
    missing mask=1 key="9" code=0 disp="exec" arg="true 7qf1shvamq"
    missing mask=1 key="F8" code=0 disp="exec" arg="d77ly2gf6 1jfi"
    extra   mask=1 key="F8" code=0 disp="exec" arg="$scflrrej 1jfi"
    extra   mask=69 key="F17" code=0 disp="exec" arg="$scflrrej natf"
CASE SYNTH-3      FAIL missing=6 extra=9 oracle_binds=17 (SYNTH tree binds=17 unbound=1 vars=3) v3_model=agree
    missing mask=64 key="F12" code=0 disp="exec" arg="7f7yvi5gj fdd2"
    missing mask=1 key="F17" code=0 disp="exec" arg="ecnl155t5 lw9q"
    extra   mask=4 key="H" code=0 disp="exec" arg="notify-send 27awgr7zhw # ibdcu"
    extra   mask=69 key="1" code=0 disp="exec" arg="$spovbclp 3qrn"
CASE REWRITE-0    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=73 key='' code=10; unbind mask=1 key='XF86MonBrightnessUp' code=0; add movetoworkspacesilent) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE REWRITE-1    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=65 key='P' code=0; unbind mask=68 key='BACKSPACE' code=0; add workspace) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE REWRITE-2    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=0 key='PRINT' code=0; unbind mask=72 key='SPACE' code=0; add exec) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE REWRITE-3    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=68 key='BACKSPACE' code=0; unbind mask=73 key='X' code=0; add movetoworkspace) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE HARD-0       FAIL missing=16 extra=21 oracle_binds=22 (HARD tree lines=27 binds=22 unbinds=3 vars=4) v3_model=agree
    missing mask=69 key="6" code=0 disp="movefocus" arg="l"
    missing mask=65 key="" code=102 disp="workspace" arg="e-1"
    extra   mask=8 key="3" code=0 disp="swapwindow" arg="r"
    extra   mask=8 key="mouse:274" code=0 disp="mouse" arg="resizewindow    # cieg0"
CASE HARD-1       FAIL missing=14 extra=24 oracle_binds=18 (HARD tree lines=28 binds=18 unbinds=2 vars=4) v3_model=agree
    missing mask=65 key="" code=123 disp="pseudo" arg=""
    missing mask=13 key="" code=106 disp="togglespecialworkspace" arg=""
    extra   mask=72 key="4" code=0 disp="movetoworkspacesilent" arg="20"
    extra   mask=65 key="mouse_down" code=0 disp="togglespecialworkspace" arg=""
CASE HARD-2       FAIL missing=11 extra=24 oracle_binds=17 (HARD tree lines=29 binds=17 unbinds=2 vars=4) v3_model=agree
    missing mask=72 key="mouse:272" code=0 disp="mouse" arg="resizewindow"
    missing mask=73 key="ESCAPE" code=0 disp="pseudo" arg=""
    extra   mask=1 key="ESCAPE" code=0 disp="pseudo" arg=""
    extra   mask=0 key="ESCAPE" code=0 disp="exec" arg="v78mwq"
CASE HARD-3       FAIL missing=17 extra=26 oracle_binds=21 (HARD tree lines=31 binds=21 unbinds=3 vars=4) v3_model=agree
    missing mask=68 key="" code=139 disp="fullscreen" arg="lw1o"
    missing mask=69 key="mouse_up" code=0 disp="layoutmsg" arg="hzk2"
    extra   mask=64 key="J" code=0 disp="exec" arg="y84xdl"
    extra   mask=0 key="SLASH" code=0 disp="zqjwuhydt" arg="yugq"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### Run 2, attempt 1

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py sha256:ab04ebe701a4275329c84acb4d18599c608e80e25c7ca7b9b5aa3e66b920bd48
seed=ea3c85f78454752e
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=3 extra=70 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-0        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-1        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-2        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-3        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-0     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=73 key='' keycode=16) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-1     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=76 key='T' keycode=0) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-2     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=65 key='SPACE' keycode=0) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-3     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=0 key='XF86AudioPlay' keycode=0) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-0   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vahtrdcr) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-1   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vlczbeqr) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-2   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vtozocas) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-3   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vahnjxsg) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-0     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-1     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 7) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-2     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 7) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-3     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE GLOB-0       FAIL missing=3 extra=70 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE GLOB-1       FAIL missing=3 extra=70 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE GLOB-2       FAIL missing=3 extra=70 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE GLOB-3       FAIL missing=3 extra=70 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNSOURCED-0  FAIL missing=3 extra=72 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNSOURCED-1  FAIL missing=3 extra=72 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNSOURCED-2  FAIL missing=3 extra=72 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNSOURCED-3  FAIL missing=3 extra=72 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-0    FAIL missing=4 extra=71 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=4 key="6" code=0 disp="exec" arg="logger kbqsubbwch"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-1    FAIL missing=4 extra=71 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=13 key="B" code=0 disp="exec" arg="true 4ki5oxxcsm"
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-2    FAIL missing=4 extra=71 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-3    FAIL missing=4 extra=71 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SYNTH-0      FAIL missing=7 extra=10 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
    missing mask=12 key="Z" code=0 disp="exec" arg="yylbzoo3u 0xom"
    missing mask=12 key="R" code=0 disp="exec" arg="i57n4plih 4x9y"
    extra   mask=64 key="F11" code=0 disp="exec" arg="$smqvxrfv ma73"
    extra   mask=77 key="G" code=0 disp="exec" arg="printf u51bafozjg"
CASE SYNTH-1      FAIL missing=7 extra=10 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
    missing mask=4 key="1" code=0 disp="exec" arg="cg1yauzkh oyl3"
    missing mask=77 key="4" code=0 disp="exec" arg="cg1yauzkh d129"
    extra   mask=76 key="7" code=0 disp="exec" arg="$spaghzqf wvwj"
    extra   mask=64 key="I" code=0 disp="exec" arg="$spaghzqf 698p"
CASE SYNTH-2      FAIL missing=7 extra=10 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
    missing mask=68 key="Y" code=0 disp="exec" arg="notify-send iseuf1f747"
    missing mask=76 key="DELETE" code=0 disp="exec" arg="1217hhf6e uypc"
    extra   mask=68 key="Y" code=0 disp="exec" arg="notify-send iseuf1f747 # wv3l4"
    extra   mask=76 key="DELETE" code=0 disp="exec" arg="$sbspfuhs uypc"
CASE SYNTH-3      FAIL missing=9 extra=12 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=76 key="COMMA" code=0 disp="exec" arg="2elaubm89 d057"
    missing mask=13 key="I" code=0 disp="exec" arg="m8p4eru5d dgui"
    extra   mask=69 key="F16" code=0 disp="exec" arg="$sbcvopcm e7ra"
    extra   mask=8 key="F8" code=0 disp="exec" arg="$spayvrsp wxyc"
CASE REWRITE-0    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioNext' code=0; unbind mask=68 key='A' code=0; add exec) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE REWRITE-1    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=73 key='LEFT' code=0; unbind mask=65 key='SLASH' code=0; add fullscreenstate) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE REWRITE-2    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=73 key='' code=15; unbind mask=0 key='XF86TouchpadToggle' code=0; add exec) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE REWRITE-3    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=68 key='PRINT' code=0; unbind mask=68 key='Delete' code=0; add exec) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE HARD-0       FAIL missing=15 extra=21 oracle_binds=22 (HARD tree lines=28 binds=22 unbinds=2 vars=4) v3_model=agree
    missing mask=68 key="F13" code=0 disp="fullscreen" arg=""
    missing mask=68 key="" code=103 disp="changegroupactive" arg="znrc"
    extra   mask=69 key="" code=85 disp="togglefloating" arg="p94o    # mps3h"
    extra   mask=0 key="mouse:274" code=0 disp="mouse" arg="movewindow"
CASE HARD-1       FAIL missing=16 extra=28 oracle_binds=22 (HARD tree lines=33 binds=22 unbinds=2 vars=4) v3_model=agree
    missing mask=8 key="F7" code=0 disp="fullscreenstate" arg=""
    missing mask=65 key="mouse:273" code=0 disp="mouse" arg="resizewindow"
    extra   mask=8 key="9" code=0 disp="pseudo" arg=""
    extra   mask=1 key="" code=14 disp="sendshortcut" arg="shift, F1, activewindow"
CASE HARD-2       FAIL missing=20 extra=28 oracle_binds=22 (HARD tree lines=30 binds=22 unbinds=2 vars=4) v3_model=agree
    missing mask=72 key="0" code=0 disp="layoutmsg" arg="pwhr"
    missing mask=4 key="A" code=0 disp="fullscreenstate" arg="zq6l"
    extra   mask=8 key="mouse_up" code=0 disp="cyclenext" arg=""
    extra   mask=64 key="BACKSPACE" code=0 disp="exec" arg="sh87zs"
CASE HARD-3       FAIL missing=13 extra=26 oracle_binds=16 (HARD tree lines=29 binds=16 unbinds=3 vars=4) v3_model=agree
    missing mask=4 key="" code=131 disp="layoutmsg" arg=""
    missing mask=4 key="mouse:272" code=0 disp="mouse" arg="movewindow"
    extra   mask=4 key="F7" code=0 disp="togglespecialworkspace" arg="795v # 22z9b"
    extra   mask=8 key="mouse_down" code=0 disp="layoutmsg" arg="nrt2"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Initial setup-error receipts (stdout and exit, verbatim)

### Initial run 1, attempt 1

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py sha256:ab04ebe701a4275329c84acb4d18599c608e80e25c7ca7b9b5aa3e66b920bd48
seed=3018b4756d91041f
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
exit=2
```

### Initial run 1, attempt 2

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py sha256:ab04ebe701a4275329c84acb4d18599c608e80e25c7ca7b9b5aa3e66b920bd48
seed=1597b44bb9bf3598
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
exit=2
```

### Initial run 2, attempt 1

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py sha256:ab04ebe701a4275329c84acb4d18599c608e80e25c7ca7b9b5aa3e66b920bd48
seed=f67a4b82c8c68e7a
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
exit=2
```

### Initial run 2, attempt 2

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py sha256:ab04ebe701a4275329c84acb4d18599c608e80e25c7ca7b9b5aa3e66b920bd48
seed=04d985f317192770
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
exit=2
```

## Other exercised commands and bounds

```sh
timeout 10 df -h /fast
```

Output:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  583G  221G  73% /fast
```

Runtime-availability discovery:

```sh
timeout 10 prlimit --as=4000000000 -- sh -c 'command -v python3; command -v bwrap; command -v Hyprland; command -v hyprctl; command -v timeout; command -v prlimit'
```

It exited 0 and returned `/usr/bin/python3`, `/usr/bin/bwrap`, `/usr/bin/Hyprland`, `/usr/bin/hyprctl`, `/usr/bin/timeout`, and `/usr/bin/prlimit` in that order. Existing tools sufficed: no packages or tools were installed or updated. No git/jj write commands, live-compositor write verbs, service changes or user-configuration writes were performed. No build, lint or separate smoke test was run; the only scored execution was the explicitly assigned v4 control protocol.
