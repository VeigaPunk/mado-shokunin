# RmGrepAll — independent committed-control re-measure

REMEASURE K4GrepAll: 0/41 (receipt said 0/41); strengthened: 0/41 — not met

## Scope, axes and provenance

- C1 axes: operability, capability acquisition, sourced correctness. Review axes: control-shape fidelity, evidence provenance, host safety.
- Read `skill://godspeed` and registration's Attempt 3 / PRED-C1 (v4), lines 169–235, before scoring. The frozen rule is exact 18-field multiset equality for 41 cases and zero embed hits; v3 model agreement is diagnostic only.
- The original receipt names tool SHA-256 `ab04ebe701a4275329c84acb4d18599c608e80e25c7ca7b9b5aa3e66b920bd48` and reports 0/41. The current control file's independently measured SHA-256 is exactly that value. Its old completed receipts scored those override bytes at `1ed41fa8301a4562d125503e5b881ec8eb5a1908`; the receipt subsequently landed at `459dd17f`. This re-measure resolves REV to `459dd17f8fd60df85b25f15e69376a9765e267d3` and still explicitly uses `--tool-file`, not the lane's resolver.
- Counter SHA-256 matches the frozen `323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2`; generator SHA-256 matches `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`.
- Exactly one fresh-seed scored invocation per version, without `--seed`, setup errors, or retries. Original seed: `8ebcccd85ee74715`; strengthened seed: `81e5ea958f7861a3`. The seeds differ: this is not a paired same-seed error-count comparison.
- Both runs independently reported `ORACLE_CHECK base_vs_live missing=0 extra=0`, 79 snapshot files, the same snapshot digest, and 192 live binds. Both ended with `cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED`, exit 1, empty stderr. These are completed measurements, not environment failures.

## Shape attack: faithful grep, but not the strongest canonical-modifier mapping

The original implements its claimed source-blind shape: `K4GrepAll.py:14–24,78–91` walks all four roots without selecting extensions or reading `source`, skips whole-line `#`, matches bind suffixes, splits comma fields, and appends every parsed entry. There is no source graph, variable expansion, unbind application, inline-comment stripping, oracle access, subprocess, embedded table or fixture-label selection. Its 18-field mapping is materially stronger than a raw text grep.

There is nevertheless a fixable in-shape weakness at `K4GrepAll.py:35–36`: canonical modifiers must be separated by whitespace, underscore, plus or pipe. `SUPERCTRL` contains only the canonical names SUPER and CTRL but produces mask 0. Hyprland's pinned `stringToModMask` uppercases the field and performs substring tests, so it produces 68. This does not require aliases, variables or source resolution.

Primary source: [Hyprland efb50993780079460b0cbed1363e2166a2de1d9f, KeybindManager.cpp:229–246](https://github.com/hyprwm/Hyprland/blob/efb50993780079460b0cbed1363e2166a2de1d9f/src/managers/KeybindManager.cpp#L229-L246), fetched ordinarily from the corresponding raw GitHub URL. The local older `controls/CtlGrepAll.py:27–42` also uses substring matching; its alias table and old score were not reused as evidence for v4. The frozen generator was read for the UNSOURCED witness below, not imported or copied into the control.

### Smallest safe in-shape correction

Wrote only `/fast/scratch/hyaku/mado-r25a3/rm/K4GrepAll-strong.py`, SHA-256 `71918efc4ad39c6fd406f641b918cceadbef920a0ae988c6737a26ad73261c40`. It retains the original reader and output mapping, changing canonical-modifier token lookup to uppercase substring membership over the same eight names. No aliases or forbidden semantics were added, and the committed control was not edited. The direct `entry('', 'SUPERCTRL, F1, exec, true')` probe below exercised both versions: masks 0 and 68, with the other 17 output fields identical. That probe is a source-grounded parser witness, not a separate nested-Hyprland oracle measurement.

### Strongest measured counterexample: an unsourced file changes the answer

In each fresh scored run, BASE has `missing=3 extra=70 oracle_binds=192`; every UNSOURCED case has `missing=3 extra=72 oracle_binds=192`. The generator's frozen `count-v3.py:258–265` writes exactly two ordinary bind lines to a fresh file beneath a scanned root, without adding a `source` directive. The unchanged Hyprland oracle count and exact two-extra increase isolate the source-blind false positive from inherited BASE mismatches. This witness survives the strengthened mapping.

[INFERENCE] A reader that ignores source directives is invariant when only those directives change and bind lines do not, while the Hyprland table can change. No additional comma-field or canonical-modifier accuracy can repair that information loss while preserving the every-file union shape.

Impact: sourced correctness and C1's exact bind-table capability. The modifier defect is safely fixable inside the shape; source-blind union is the shape's deliberate limitation, not a defect to hide with filename exclusions, deduplication, cached answers or relaxed comparison. Resolving that witness requires following ordered `source` expansion, which crosses the shape boundary. Variables, inline comments and unbind remain independent skipped semantics. For example, original SYNTH-3 retains `notify-send reekra448f # 6dc1l` where the oracle has `notify-send reekra448f`.

The strengthened version remains 0/41. It demonstrates a concrete local mapping improvement, not score improvement or saturation of all possible shortcut designs. Neither receipt provides a basis to claim C1 met or to substitute v3 model output for the Hyprland oracle. No admission or canonical judge was run.

## Exact hash commands and outputs

Working directory: `/home/vgpnk/Projects/shokunin` for the first command; the lane root for the second.

```sh
ulimit -v 4194304 && timeout 20s sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count.py
```

```text
ab04ebe701a4275329c84acb4d18599c608e80e25c7ca7b9b5aa3e66b920bd48  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count.py
exit=0
```

```sh
ulimit -v 4194304 && timeout 20s sha256sum /fast/scratch/hyaku/mado-r25a3/rm/K4GrepAll-strong.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count-v3.py
```

```text
71918efc4ad39c6fd406f641b918cceadbef920a0ae988c6737a26ad73261c40  /fast/scratch/hyaku/mado-r25a3/rm/K4GrepAll-strong.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count-v3.py
exit=0
```

## Exact scoring commands and verbatim receipts

Working directory for both: `/home/vgpnk/Projects/shokunin/mado-shokunin`. The supplied live signature and `WAYLAND_DISPLAY=wayland-1` were set only in the child environment. Added `-B` to the requested isolated Python invocation to prevent lane bytecode caches, `prlimit` for a 4,000,000,000-byte address-space limit and 16-MiB per-file limit, and timeout escalation. The async capture wrapper used a new process session, a 1230-second outer deadline, and would kill its process group if still running. No such timeout fired. The counter's host-wide six-slot lock was unchanged.

### Original control — one fresh seed

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 prlimit --as=4000000000 --fsize=16777216 -- timeout --kill-after=15 1200 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py sha256:ab04ebe701a4275329c84acb4d18599c608e80e25c7ca7b9b5aa3e66b920bd48
seed=8ebcccd85ee74715
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
CASE ADD-1        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-2        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-3        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-0     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=0 key='XF86AudioPause' keycode=0) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-1     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=64 key='' keycode=14) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-2     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=72 key='COMMA' keycode=0) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-3     FAIL missing=2 extra=70 oracle_binds=191 (UNBIND mask=64 key='P' keycode=0) v3_model=agree
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    missing mask=64 key="" code=21 disp="resizeactive" arg="100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-0   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vwuymhmz) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-1   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vivnvrds) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-2   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vgstuhox) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-3   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vzndgngu) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-0     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 9) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-1     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 9) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-2     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-3     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 7) v3_model=agree
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
CASE COMMENT-1    FAIL missing=4 extra=71 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=77 key="K" code=0 disp="exec" arg="true 0ldulo51as"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-2    FAIL missing=4 extra=71 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE COMMENT-3    FAIL missing=4 extra=71 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SYNTH-0      FAIL missing=7 extra=10 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=68 key="DOWN" code=0 disp="exec" arg="p1m3oyjys ragr"
    missing mask=8 key="X" code=0 disp="exec" arg="yl53ktina 379c"
    extra   mask=69 key="F8" code=0 disp="exec" arg="$snvvasaf tit9"
    extra   mask=69 key="Y" code=0 disp="exec" arg="$snvvasaf i342"
CASE SYNTH-1      FAIL missing=7 extra=10 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
    missing mask=69 key="C" code=0 disp="exec" arg="true 7gsxfwr5g8"
    missing mask=72 key="N" code=0 disp="exec" arg="83f54rwbt rcwx"
    extra   mask=65 key="7" code=0 disp="exec" arg="true w3og3q9ppx # 1gn0y"
    extra   mask=8 key="HOME" code=0 disp="exec" arg="$srmfgloe zb2d"
CASE SYNTH-2      FAIL missing=8 extra=11 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
    missing mask=65 key="J" code=0 disp="exec" arg="notify-send 2s37bxvdun"
    missing mask=1 key="KP_5" code=0 disp="exec" arg="8d8pp3xnj nawv"
    extra   mask=1 key="KP_5" code=0 disp="exec" arg="$sanehysc nawv"
    extra   mask=12 key="A" code=0 disp="exec" arg="$sanehysc rvgg"
CASE SYNTH-3      FAIL missing=5 extra=8 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
    missing mask=69 key="W" code=0 disp="exec" arg="wjdqazqp5 enn7"
    missing mask=69 key="DOWN" code=0 disp="exec" arg="notify-send reekra448f"
    extra   mask=69 key="DOWN" code=0 disp="exec" arg="notify-send reekra448f # 6dc1l"
    extra   mask=4 key="Q" code=0 disp="exec" arg="$svdcvtjx sqht"
CASE REWRITE-0    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=64 key='XF86AudioMute' code=0; unbind mask=0 key='XF86AudioMicMute' code=0; add exec) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE REWRITE-1    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=8 key='XF86AudioLowerVolume' code=0; unbind mask=64 key='mouse_up' code=0; add exec) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE REWRITE-2    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=1 key='XF86MonBrightnessUp' code=0; unbind mask=73 key='UP' code=0; add exec) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE REWRITE-3    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=12 key='DELETE' code=0; unbind mask=72 key='COMMA' code=0; add movetoworkspacesilent) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE HARD-0       FAIL missing=14 extra=23 oracle_binds=19 (HARD tree lines=28 binds=19 unbinds=3 vars=4) v3_model=agree
    missing mask=4 key="mouse:273" code=0 disp="mouse" arg="resizewindow"
    missing mask=72 key="mouse:274" code=0 disp="mouse" arg="MoveWindow"
    extra   mask=0 key="" code=168 disp="sendshortcut" arg="ctrl, M, activewindow"
    extra   mask=1 key="6" code=0 disp="moveoutofgroup" arg=""
CASE HARD-1       FAIL missing=18 extra=27 oracle_binds=24 (HARD tree lines=33 binds=24 unbinds=2 vars=4) v3_model=agree
    missing mask=64 key="mouse:272" code=0 disp="mouse" arg="MoveWindow"
    missing mask=13 key="" code=71 disp="moveintogroup" arg="r"
    extra   mask=1 key="0" code=0 disp="layoutmsg" arg="azi4  # paoqt"
    extra   mask=0 key="" code=71 disp="focusmonitor" arg="d"
CASE HARD-2       FAIL missing=14 extra=22 oracle_binds=17 (HARD tree lines=25 binds=17 unbinds=1 vars=4) v3_model=agree
    missing mask=4 key="mouse:274" code=0 disp="mouse" arg="MoveWindow"
    missing mask=68 key="COMMA" code=0 disp="sendshortcut" arg="CONTROL_SHIFT, TAB, activewindow"
    extra   mask=13 key="H" code=0 disp="changegroupactive" arg=""
    extra   mask=4 key="mouse:274" code=0 disp="bringactivetotop" arg="fo1x"
CASE HARD-3       FAIL missing=12 extra=23 oracle_binds=19 (HARD tree lines=31 binds=19 unbinds=3 vars=4) v3_model=agree
    missing mask=76 key="mouse:274" code=0 disp="togglegroup" arg=""
    missing mask=64 key="S" code=0 disp="sendshortcut" arg="ctrl  SHIFT, F20, activewindow"
    extra   mask=0 key="F21" code=0 disp="moveoutofgroup" arg="gepa"
    extra   mask=0 key="mouse_down" code=0 disp="focusmonitor" arg="u"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Stderr: empty.

### Strengthened control — one fresh seed

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 prlimit --as=4000000000 --fsize=16777216 -- timeout --kill-after=15 1200 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /fast/scratch/hyaku/mado-r25a3/rm/K4GrepAll-strong.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/rm/K4GrepAll-strong.py sha256:71918efc4ad39c6fd406f641b918cceadbef920a0ae988c6737a26ad73261c40
seed=81e5ea958f7861a3
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=3 extra=70 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-0        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-1        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-2        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE ADD-3        FAIL missing=3 extra=70 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-0     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=1 key='XF86MonBrightnessDown' keycode=0) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-1     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=64 key='' keycode=10) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-2     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=65 key='' keycode=201) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE UNBIND-3     FAIL missing=3 extra=71 oracle_binds=191 (UNBIND mask=0 key='XF86PowerOff' keycode=0) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-0   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vfmdevtv) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-1   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vmcddiqv) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-2   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vensitnv) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE VARIABLE-3   FAIL missing=4 extra=71 oracle_binds=193 (VARIABLE $vkrfqgaz) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-0     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 4) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-1     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 4) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-2     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 4) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SOURCE-3     FAIL missing=3 extra=70 oracle_binds=194 (SOURCE new file at root line 9) v3_model=agree
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
CASE COMMENT-3    FAIL missing=4 extra=71 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE SYNTH-0      FAIL missing=9 extra=12 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=69 key="F10" code=0 disp="exec" arg="00uq1pp5a b6rw"
    missing mask=1 key="SPACE" code=0 disp="exec" arg="true 82wzr78ri2"
    extra   mask=77 key="KP_1" code=0 disp="exec" arg="$spwfnetb p0cg"
    extra   mask=72 key="H" code=0 disp="exec" arg="$spwfnetb ow2y"
CASE SYNTH-1      FAIL missing=4 extra=7 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=4 key="C" code=0 disp="exec" arg="true 8o18unpr7w"
    missing mask=76 key="F17" code=0 disp="exec" arg="true cxv98u17zt"
    extra   mask=68 key="F24" code=0 disp="exec" arg="true ikq2ju8od2"
    extra   mask=4 key="C" code=0 disp="exec" arg="true 8o18unpr7w # mbz7t"
CASE SYNTH-2      FAIL missing=8 extra=11 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
    missing mask=9 key="J" code=0 disp="exec" arg="usgckzucn y4bk"
    missing mask=64 key="HOME" code=0 disp="exec" arg="4zh1zowz3 ns1e"
    extra   mask=77 key="F1" code=0 disp="exec" arg="$sqedkghj dstm"
    extra   mask=72 key="MINUS" code=0 disp="exec" arg="printf xb4l4itsr9"
CASE SYNTH-3      FAIL missing=8 extra=11 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=3) v3_model=agree
    missing mask=5 key="7" code=0 disp="exec" arg="6vo1zxywu hxc5"
    missing mask=12 key="T" code=0 disp="exec" arg="dx3p7o1ow 47uw"
    extra   mask=9 key="0" code=0 disp="exec" arg="$safxnvaw izq2"
    extra   mask=76 key="UP" code=0 disp="exec" arg="$sqvfmbqt 72w0"
CASE REWRITE-0    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=0 key='XF86PowerOff' code=0; unbind mask=64 key='TAB' code=0; add workspace) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE REWRITE-1    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=65 key='' code=10; unbind mask=0 key='switch:off:Lid Switch' code=0; add moveintogroup) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE REWRITE-2    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioMicMute' code=0; unbind mask=68 key='PRINT' code=0; add exec) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE REWRITE-3    FAIL missing=3 extra=71 oracle_binds=192 (REWRITE argswap mask=65 key='' code=14; unbind mask=72 key='' code=10; add pseudo) v3_model=agree
    missing mask=64 key="P" code=0 disp="pseudo" arg=""
    missing mask=64 key="" code=20 disp="resizeactive" arg="-100 0"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="uwsm-app -- xdg-terminal-exec --dir=\"$(omarchy-c
    extra   mask=65 key="RETURN" code=0 disp="exec" arg="omarchy-launch-browser"
CASE HARD-0       FAIL missing=15 extra=25 oracle_binds=17 (HARD tree lines=27 binds=17 unbinds=3 vars=4) v3_model=agree
    missing mask=69 key="F20" code=0 disp="togglespecialworkspace" arg=""
    missing mask=4 key="mouse:274" code=0 disp="mouse" arg="resizewindow"
    extra   mask=0 key="BACKSPACE" code=0 disp="cyclenext  # ni80c" arg=""
    extra   mask=0 key="" code=146 disp="movecurrentworkspacetomonitor" arg="d"
CASE HARD-1       FAIL missing=16 extra=24 oracle_binds=23 (HARD tree lines=30 binds=23 unbinds=1 vars=4) v3_model=agree
    missing mask=64 key="6" code=0 disp="fullscreenstate" arg=""
    missing mask=65 key="HOME" code=0 disp="changegroupactive" arg=""
    extra   mask=0 key="" code=101 disp="moveintogroup" arg="u"
    extra   mask=9 key="" code=101 disp="cyclenext" arg=""
CASE HARD-2       FAIL missing=18 extra=26 oracle_binds=24 (HARD tree lines=30 binds=24 unbinds=1 vars=4) v3_model=agree
    missing mask=65 key="4" code=0 disp="bringactivetotop" arg=""
    missing mask=65 key="" code=64 disp="resizeactive" arg="0 36"
    extra   mask=0 key="F7" code=0 disp="moveintogroup" arg="u"
    extra   mask=0 key="" code=0 disp="exec" arg="6t2mwe"
CASE HARD-3       FAIL missing=14 extra=22 oracle_binds=20 (HARD tree lines=27 binds=20 unbinds=2 vars=4) v3_model=agree
    missing mask=68 key="N" code=0 disp="fullscreen" arg=""
    missing mask=0 key="KP_9" code=0 disp="fullscreen" arg=""
    extra   mask=0 key="" code=19 disp="movetoworkspacesilent" arg="special:ggry"
    extra   mask=9 key="Z" code=0 disp="cyclenext  # vcxt8" arg=""
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Stderr: empty.

## Exact direct parser probe

```sh
prlimit --as=4000000000 --fsize=16777216 -- timeout 10 python3 -I -B -c 'import importlib.util, json
paths = [('"'"'original'"'"', '"'"'/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4GrepAll.py'"'"'), ('"'"'strong'"'"', '"'"'/fast/scratch/hyaku/mado-r25a3/rm/K4GrepAll-strong.py'"'"')]
for label, path in paths:
    spec = importlib.util.spec_from_file_location(label, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.entry('"'"''"'"', '"'"'SUPERCTRL, F1, exec, true'"'"')
    print(label + '"'"': '"'"' + json.dumps(result, sort_keys=True))
'
```

```text
original: {"allow_input_capture": false, "arg": "true", "auto_consuming": false, "catch_all": false, "description": "", "dispatcher": "exec", "has_description": false, "key": "F1", "keycode": 0, "locked": false, "longPress": false, "modmask": 0, "mouse": false, "non_consuming": false, "release": false, "repeat": false, "submap": "", "submap_universal": "false"}
strong: {"allow_input_capture": false, "arg": "true", "auto_consuming": false, "catch_all": false, "description": "", "dispatcher": "exec", "has_description": false, "key": "F1", "keycode": 0, "locked": false, "longPress": false, "modmask": 68, "mouse": false, "non_consuming": false, "release": false, "repeat": false, "submap": "", "submap_universal": "false"}
exit=0
```

Stderr: empty.

## Host safety and scope

Only this report and the named scratch stronger-control file were written. No subagents, git/jj write commands, live-compositor write verbs, package/service changes, user-config writes, counter edits or resolver edits. No additional runtime or judge was invoked. Both counter processes exited normally; their nested oracle instances were launched only by the frozen counter, whose `finally` blocks terminate and wait for their process groups and remove temporary trees (`count.py:174–189,299–300`). No independent nested compositor was launched. The direct parser probe exited 0; imports used `python3 -I -B`.

No tools were installed or updated. No build, lint, formatter or other verification run was performed. A broad cached-source filename search timed out; it was not treated as evidence of absence, and the pinned primary modifier source was read directly instead.

REMEASURE K4GrepAll: 0/41 (receipt said 0/41); strengthened: 0/41 — not met
