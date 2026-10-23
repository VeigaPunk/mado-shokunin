# K4LabelKeyed — frozen v4 fixture/label-keyed control

## Verdict

CONTROL K4LabelKeyed v4 best: cases_pass=37/41 embed_hits=0 verdict=TARGET_MISSED — not met

Both completed measurements: **37/41**, `embed_hits=0`, exit 1. Every BASE, ADD, UNBIND, VARIABLE, SOURCE, GLOB, UNSOURCED, COMMENT, SYNTH and REWRITE case passed. All four HARD cases failed on each seed. This does not meet PRED-C1 (v4); neither partial saturation nor an empty literal-string hit count establishes the claimed resolver capability.

## Scope and construction

- Control: `.ufo/waves/round-25/controls/v4/K4LabelKeyed.py`, 18,997 bytes, sha256:`b43c4d700972ea00c8baa9b7e09496bb44f031db9e27edf41d223bb7a09dd6b9`.
- Frozen counter: `.ufo/waves/round-25/c1/count.py`, sha256:`323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2`; generator sha256:`8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`.
- Revision scored: `1ed41fa8301a4562d125503e5b881ec8eb5a1908`.
- Read the registration through Attempt 3 before building. No changes to the counter, its rule, the claimed `tools/mado-binds.py`, corpus files, or other controls.
- The encoded payload holds all **192 live rows**, plus **190 normalized real-line heads mapped to the corresponding captured row indices**. Its zlib/base64 literal is 10,212 characters. The capture is the same sha256 printed by both completed receipts: `9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`.
- Fixed cached bind-file names are the snapshot's media, clipboard, tiling-v2, utilities and personal bindings files. The runtime does not discover their source graph.
- No `count-v3.py` functions are imported or copied. The control uses a small generator-template decoder, not a general Hyprland bind grammar.
- The same control bytes were used for every attempt; no edits followed either score.

### Shape-specific shortcuts

1. Read the `/snap/home` bind mount's root in `/proc/self/mountinfo` and extract the literal `cases/KIND-N/home` category when available. Otherwise use fixed filenames, generated filename lengths, synthetic layout and generator fingerprints.
2. BASE and UNSOURCED return the captured table without reading configuration bind contents. UNSOURCED is a category decision, not a reachability result.
3. SOURCE and GLOB select eight-character generated filenames in two fixed directories, without interpreting any `source` statement or expanding a source glob.
4. ADD and COMMENT search only the five known fixture bind files for the generator's random command shape. VARIABLE recognizes only its eight-character v/s variable names and nine-character values.
5. SYNTH expands exactly the known `a.conf` and `d/x.conf`, `d/y.conf` fixture edges at their two literal marker lines. It never resolves an arbitrary source path, filename, glob or layout.
6. REWRITE normalizes the cached real-line heads, updates the cached row's argument where that head matches, decodes the one unmatched easy-template addition, and applies the root's appended unbind. Unchanged real rows, including mouse rows, come from the captured table.
7. HARD selects the same cheap easy-template branch, without the harder grammar. It cannot recover fresh hard rows from the case category; it returned no rows on these eight HARD trees.

Skipped claimed work: general source/~ /glob resolution, variable scope and arbitrary variable expansion, real-file bind interpretation, modifier aliases, general keycode/mouse/flag/rejected-line grammar, and arbitrary ordered unbind/source interactions. Adding the counter's full hard-line model would cross the Attempt 3 implementation/control boundary, so it was not done.

## Counterexamples and evidence

### Literal identity is available inside the sandbox

The counter names each case home `.../cases/<label>/home` (`c1/count.py:247–249`), and the sandbox bind-mounts it at `/snap/home` while exposing `/proc` (`c1/count-v3.py:730–734`). A path-only probe, with the same mount/proc isolation flags, recovered the literal HARD category from an **empty** home. It needed no config bytes, network, environment or compositor socket.

Temporary input directory: `/fast/scratch/K4LabelKeyed-vl92f2cy/cases/HARD-2/home`. Created and removed with a Python `TemporaryDirectory`; no configuration file was written and no compositor was launched by this probe.

Exact probe subprocess command:

```sh
timeout 20 prlimit --as=4000000000 bwrap --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/bin /bin --proc /proc --dev /dev --tmpfs /tmp --ro-bind /fast/scratch/K4LabelKeyed-vl92f2cy/cases/HARD-2/home /snap/home --unshare-all --die-with-parent --clearenv --setenv PATH /usr/bin python3 -I -c 'from pathlib import Path; import re; lines=Path("/proc/self/mountinfo").read_text().splitlines(); roots=[l.split()[3] for l in lines if l.split()[4]=="/snap/home"]; print("mount_roots="+repr(roots)); print("fixture_kind="+next(re.search(r"/cases/(BASE|ADD|UNBIND|VARIABLE|SOURCE|GLOB|UNSOURCED|COMMENT|SYNTH|REWRITE|HARD)(?:-[0-3])?/home$",r)[1] for r in roots))'
```

Verbatim output:

```text
mount_roots=['/scratch/K4LabelKeyed-vl92f2cy/cases/HARD-2/home']
fixture_kind=HARD
stderr=''
exit=0
```

This demonstrates category leakage, not prediction of the random HARD table. The program also has structural routing so simply hiding this one label would not establish source-resolution capability.

### Encoded provenance and normalized fixture cache

The program contains the complete captured table, yet both completed receipts report `embed_hits=0`. The counter scans only literal arg/description substrings in the source (`c1/count.py:233–240`); encoding evades that audit. Both runs pass BASE and all UNSOURCED cases with cached rows alone, and all eight REWRITE cases pass through normalized fixture identities plus their small deltas. Therefore these individual passes do not demonstrate interpreting real config lines.

This is consistent with the already disclosed normalized-cache/easy-grammar gap in registration Attempt 2 (`registration.md:134–145`). It is not evidence that the entire v4 predicate is wrong. HARD supplies the decisive counterexample to extending that shortcut to all 41 cases: the first completed seed has 22, 22, 16 and 21 missing HARD rows; the second has 22, 28, 20 and 20. Neither has extra HARD rows.

The oracle checks succeeded in both completed runs (`base_vs_live missing=0 extra=0`); `V3_MODEL_AGREE 41/41` is diagnostic only. No oracle/model disagreement was demonstrated by this assignment.

## Impacted axes and smallest safe correction

- **Operability / capability acquisition:** category identification plus cached real rows covers 37 cases without the full resolver. HARD still prevents this control from meeting the frozen 41-case target. Report the miss; do not promote the partial result to acquired capability.
- **Sourced provenance:** `embed_hits=0` is a literal-substring result, not evidence that the output was derived from source semantics or lacks an embedded answer table. The captured table is explicitly the control's answer authority.
- **Calibration:** preserve all four receipts below, including the initial setup failures. Do not report those failures as scored 0/41 or omit them.
- **Host safety:** the live compositor was queried only with read verbs. Only the frozen counter started nested instances, under its six-slot host-wide lock and cleanup path. No packages, services, live compositor settings or host config files were changed.

Smallest safe correction now: leave v4 frozen, retain its HARD kill arm, record this failed control and describe the embedding check precisely as a plaintext audit. A future counter revision could give bind-mount source directories opaque unrelated names to close the demonstrated label channel; structural fixture leakage would still require independent layout/reachability variation. Those are prospective changes, not amendments to these receipts. Full admission or scored-axis judgment remains with the canonical judge.

## Commands and execution conditions

Working directory for every counter subprocess: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Initial command, launched twice with fresh seeds:

```sh
timeout 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4LabelKeyed.py
```

Those two attempts exited 2 before live capture. The Python tool kernel lacked `HYPRLAND_INSTANCE_SIGNATURE` and `WAYLAND_DISPLAY`; the session shell had both. Diagnosis used `timeout 10 printenv HYPRLAND_INSTANCE_SIGNATURE WAYLAND_DISPLAY XDG_RUNTIME_DIR HOME` and `timeout 20 hyprctl instances -j`. No compositor state was changed.

Each exit-2 attempt was re-run exactly once, with only the subprocess routing environment supplied from the session shell, again with fresh seeds:

```sh
HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 timeout 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4LabelKeyed.py
```

Both pairs were concurrent; the counter's own lock files bounded nested instances host-wide. The 1,200-second timeout and 4,000,000,000-byte per-process address-space cap applied to every attempt. Counter stdout and exit codes follow verbatim; stderr was empty for all four attempts.

Other bounded commands: `timeout 10 df -h /fast` (221 GB available before scratch use), `timeout 20 hyprctl binds -j` (read-only capture), and the two bubblewrap metadata probes. The first probe mounted the existing read-only host hypr directory and exposed its original mount root; the second, reproduced above, demonstrated literal case-label extraction. Both probes exited 0, and their subprocesses terminated. All counter subprocesses also exited; nested cleanup is the counter's `finally` path (`c1/count.py:174–189`). Temporary probe directories were removed. No tools were installed or updated. A raw-read footer inconsistency encountered while retaining the live capture was reported through `xd://report_issue`; it did not alter the control or scoring rule.

## Complete receipts

### Run 1 — initial setup error

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4LabelKeyed.py sha256:b43c4d700972ea00c8baa9b7e09496bb44f031db9e27edf41d223bb7a09dd6b9
seed=ed1eef295b22c9ab
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
exit=2
```

Stderr: empty.

### Run 1 — one permitted re-run

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4LabelKeyed.py sha256:b43c4d700972ea00c8baa9b7e09496bb44f031db9e27edf41d223bb7a09dd6b9
seed=fa959a1880dab12a
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=8 key='XF86AudioLowerVolume' keycode=0) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=65 key='' keycode=14) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='RIGHT' keycode=0) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='SPACE' keycode=0) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vzbkmmby) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vcdlaepu) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vleqwygn) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vvldzqxq) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 23) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 16) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 16) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE COMMENT-1    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='V' code=0; unbind mask=72 key='' code=13; add movetoworkspace) v3_model=agree
CASE REWRITE-1    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='' code=19; unbind mask=68 key='S' code=0; add swapwindow) v3_model=agree
CASE REWRITE-2    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='LEFT' code=0; unbind mask=76 key='B' code=0; add exec) v3_model=agree
CASE REWRITE-3    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=68 key='S' code=0; unbind mask=65 key='' code=18; add exec) v3_model=agree
CASE HARD-0       FAIL missing=22 extra=0 oracle_binds=22 (HARD tree lines=29 binds=22 unbinds=2 vars=4) v3_model=agree
    missing mask=73 key="D" code=0 disp="togglefloating" arg="irfa"
    missing mask=4 key="" code=142 disp="bringactivetotop" arg=""
CASE HARD-1       FAIL missing=22 extra=0 oracle_binds=22 (HARD tree lines=31 binds=22 unbinds=3 vars=4) v3_model=agree
    missing mask=64 key="mouse:272" code=0 disp="mouse" arg="resizewindow"
    missing mask=64 key="" code=19 disp="fullscreen" arg="bvim"
CASE HARD-2       FAIL missing=16 extra=0 oracle_binds=16 (HARD tree lines=29 binds=16 unbinds=1 vars=4) v3_model=agree
    missing mask=68 key="6" code=0 disp="cyclenext" arg=""
    missing mask=0 key="EQUAL" code=0 disp="exec" arg="notify-send a1yi0y uqqe, 272x"
CASE HARD-3       FAIL missing=21 extra=0 oracle_binds=21 (HARD tree lines=27 binds=21 unbinds=1 vars=4) v3_model=agree
    missing mask=72 key="" code=69 disp="swapwindow" arg="r"
    missing mask=8 key="F6" code=0 disp="togglespecialworkspace" arg="z9ml"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=37/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Stderr: empty.

### Run 2 — initial setup error

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4LabelKeyed.py sha256:b43c4d700972ea00c8baa9b7e09496bb44f031db9e27edf41d223bb7a09dd6b9
seed=a8985539613db62b
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
exit=2
```

Stderr: empty.

### Run 2 — one permitted re-run

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4LabelKeyed.py sha256:b43c4d700972ea00c8baa9b7e09496bb44f031db9e27edf41d223bb7a09dd6b9
seed=4f30e17b6a80a8af
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=72 key='TAB' keycode=0) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='mouse_up' keycode=0) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=65 key='RIGHT' keycode=0) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=73 key='' keycode=15) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vnbsvmdv) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vqfzfrqb) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vjtkogtx) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vaapzkiz) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 19) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 19) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 5) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-1    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=1 key='XF86MonBrightnessDown' code=0; unbind mask=64 key='O' code=0; add workspace) v3_model=agree
CASE REWRITE-1    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='SPACE' code=0; unbind mask=73 key='UP' code=0; add layoutmsg) v3_model=agree
CASE REWRITE-2    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86KbdBrightnessDown' code=0; unbind mask=64 key='X' code=0; add exec) v3_model=agree
CASE REWRITE-3    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioPause' code=0; unbind mask=64 key='P' code=0; add movetoworkspace) v3_model=agree
CASE HARD-0       FAIL missing=22 extra=0 oracle_binds=22 (HARD tree lines=30 binds=22 unbinds=3 vars=4) v3_model=agree
    missing mask=65 key="" code=36 disp="bringactivetotop" arg=""
    missing mask=73 key="" code=148 disp="togglespecialworkspace" arg=""
CASE HARD-1       FAIL missing=28 extra=0 oracle_binds=28 (HARD tree lines=33 binds=28 unbinds=3 vars=4) v3_model=agree
    missing mask=72 key="mouse:274" code=0 disp="mouse" arg="MoveWindow"
    missing mask=65 key="W" code=0 disp="fullscreenstate" arg="snro"
CASE HARD-2       FAIL missing=20 extra=0 oracle_binds=20 (HARD tree lines=30 binds=20 unbinds=3 vars=4) v3_model=agree
    missing mask=1 key="" code=204 disp="moveoutofgroup" arg="as06"
    missing mask=65 key="R" code=0 disp="swapwindow" arg="u"
CASE HARD-3       FAIL missing=20 extra=0 oracle_binds=20 (HARD tree lines=28 binds=20 unbinds=2 vars=4) v3_model=agree
    missing mask=72 key="" code=143 disp="focusmonitor" arg="r"
    missing mask=13 key="J" code=0 disp="movetoworkspace" arg="e-1"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=37/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Stderr: empty.
