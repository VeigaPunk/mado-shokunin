# K4EncodedTable — encoded cache plus file-level easy delta

## Verdict

CONTROL K4EncodedTable v4 best: cases_pass=31/41 embed_hits=0 verdict=TARGET_MISSED — not met

## Shape and build

This is the requested standalone shortcut, not `tools/mado-binds.py` and not a full resolver. It challenges the predicate with an encoded live-table cache; it does not mutate the frozen counter or any sibling source. There was no pre-existing pristine implementation assigned to this item, so a pristine/mutated/restored implementation triplet is not applicable. The two required counter runs measure the same immutable control bytes.

Axes: shortcut strength, grammar boundary, reproducible receipts, host isolation.

- Output program: `.ufo/waves/round-25/controls/v4/K4EncodedTable.py` (single Python stdlib file; `--home DIR`; JSON array only).
- Program bytes: 18816; SHA-256 before writing: `4b4736a81453c37a29f6c4f0f4d20097b148484bab7386215688a03479858138`. Both receipts below independently name the measured file hash.
- Build input: `timeout 20 prlimit --as=4000000000 hyprctl binds -j`, captured before and after reading the four snapshot roots; the two raw captures were byte-identical. SHA-256: `9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`; 192 live entries.
- Snapshot: 79 files, 2082602 bytes; counter-compatible aggregate digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`. All 79 individual file SHA-256 digests are inside the encoded payload.
- Source graph: 40 reachable files. Build-time association of each bind's description/dispatcher/argument with the live capture assigned every live row exactly once: 192 assigned, 0 unassigned. This associates observations with files; it does not reconstruct their 18 fields from bind grammar.
- Cache ownership: media 23, clipboard 4, tiling-v2 90, utilities 50, local bindings 25. The program embeds the complete live table and the per-file digest/ordered-operation manifest in zlib plus base64 (12112 base64 bytes). It embeds no decoded live argument/description literals in parser code.
- For an unchanged, originally reachable file, runtime hashes its bytes and replays cached entry references and its source/variable/unbind operations in order. It never parses that file's bind lines. Unsourced old files have no observed table cache and are easy-parsed if they become newly reachable.
- Changed/new/newly reachable files use only the easy comma grammar, optional descriptions, boolean flag projection, canonical whitespace-separated modifier names (case-insensitive), literal symbolic/single-digit keys, cached dispatcher vocabulary, variable expansion, comments, ordered unbinds, relative/tilde source paths and sorted globs. The final argument may contain commas, and shell substitutions remain literal text. Code-form unbind references can remove cached code entries.
- Deliberately absent: keycode-bind interpretation, modifier aliases or alternative separators, submaps, key chords, and Hyprland's complete reject/validation grammar. Cached rows are not semantically invalidated when a variable in another file changes. These boundaries retain the assigned shortcut shape rather than turning it into the claimed full resolver.

## Detector and commands

Expected detector: frozen counter v4, PRED-C1 (v4), requiring exact multiset equality over 18 fields for all 41 cases and `embed_hits=0`. Encoding may defeat the plain-substring embed check; changed-file or fresh-tree syntax outside the easy grammar must still be detected by the real Hyprland oracle. A run exiting 2 is inconclusive and is retried once, never counted as a killed shortcut.

Both runs used this exact command, each with its own fresh default seed, from the lane root (the `prlimit` wrapper supplies the required memory cap):

```sh
timeout 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EncodedTable.py
```

The frozen counter provides host-wide six-slot locking, removes exec keyword lines in each private oracle tree, queries its own nested instances and kills their process groups in `finally`. The control itself creates no child processes and uses no compositor API at runtime.

## Receipts (verbatim stdout and exit)

| Run | Seed | cases_pass | embed_hits | Verdict | exit |
|---|---|---|---|---|---|
| 1 | `6a651fe4047c01dd` | 30/41 | 0 | TARGET_MISSED | 1 |
| 2 | `7765512ff93f3fd7` | 31/41 | 0 | TARGET_MISSED | 1 |

### Run 1

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EncodedTable.py sha256:4b4736a81453c37a29f6c4f0f4d20097b148484bab7386215688a03479858138
seed=6a651fe4047c01dd
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-3        FAIL missing=1 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=65 key="" code=201 disp="exec" arg="omarchy-menu"
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=69 key='R' keycode=0) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='C' keycode=0) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=65 key='Y' keycode=0) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=73 key='' keycode=10) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vbqjibgt) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vcmuewwn) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vrtuezaf) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vlysohvm) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 20) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 4) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 20) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    FAIL missing=1 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=65 key="" code=201 disp="exec" arg="omarchy-menu"
CASE COMMENT-1    FAIL missing=1 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=65 key="" code=201 disp="exec" arg="omarchy-menu"
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=2) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    FAIL missing=42 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='O' code=0; unbind mask=72 key='UP' code=0; add exec) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE REWRITE-1    FAIL missing=42 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='RIGHT' code=0; unbind mask=72 key='DOWN' code=0; add exec) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE REWRITE-2    FAIL missing=42 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioNext' code=0; unbind mask=65 key='UP' code=0; add exec) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE REWRITE-3    FAIL missing=42 extra=0 oracle_binds=192 (REWRITE argswap mask=12 key='DELETE' code=0; unbind mask=68 key='F' code=0; add fullscreen) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE HARD-0       FAIL missing=17 extra=1 oracle_binds=20 (HARD tree lines=28 binds=20 unbinds=1 vars=4) v3_model=agree
    missing mask=72 key="" code=38 disp="moveintogroup" arg="u"
    missing mask=68 key="" code=58 disp="workspace" arg="e+1"
    extra   mask=64 key="W" code=0 disp="exec" arg="1nf4wh"
CASE HARD-1       FAIL missing=17 extra=1 oracle_binds=19 (HARD tree lines=30 binds=19 unbinds=3 vars=4) v3_model=agree
    missing mask=68 key="" code=30 disp="moveintogroup" arg="d"
    missing mask=64 key="N" code=0 disp="fullscreen" arg="w16l"
    extra   mask=64 key="KP_9" code=0 disp="exec" arg="xe0p9b"
CASE HARD-2       FAIL missing=13 extra=0 oracle_binds=17 (HARD tree lines=27 binds=17 unbinds=2 vars=4) v3_model=agree
    missing mask=64 key="8" code=0 disp="workspace" arg="special:z8sh"
    missing mask=64 key="F" code=0 disp="moveintogroup" arg="r"
CASE HARD-3       FAIL missing=14 extra=0 oracle_binds=18 (HARD tree lines=28 binds=18 unbinds=3 vars=4) v3_model=agree
    missing mask=4 key="mouse:273" code=0 disp="mouse" arg="resizewindow"
    missing mask=76 key="mouse:274" code=0 disp="sendshortcut" arg="CTRL, F11, activewindow"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=30/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### Run 2

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EncodedTable.py sha256:4b4736a81453c37a29f6c4f0f4d20097b148484bab7386215688a03479858138
seed=7765512ff93f3fd7
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=65 key='' keycode=201) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='P' keycode=0) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=65 key='X' keycode=0) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='' keycode=19) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vidtjkfn) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vgbtldtx) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vrbrmzoh) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vpvidagl) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 16) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 18) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    FAIL missing=1 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=65 key="" code=201 disp="exec" arg="omarchy-menu"
CASE COMMENT-1    FAIL missing=41 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=10 (SYNTH tree binds=10 unbound=1 vars=3) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    FAIL missing=42 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='L' code=0; unbind mask=0 key='XF86AudioRaiseVolume' code=0; add exec) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE REWRITE-1    FAIL missing=41 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='' code=16; unbind mask=65 key='' code=18; add changegroupactive) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE REWRITE-2    FAIL missing=42 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='' code=20; unbind mask=73 key='LEFT' code=0; add exec) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE REWRITE-3    FAIL missing=42 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='G' code=0; unbind mask=0 key='XF86AudioNext' code=0; add exec) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE HARD-0       FAIL missing=17 extra=0 oracle_binds=21 (HARD tree lines=29 binds=21 unbinds=1 vars=4) v3_model=agree
    missing mask=64 key="mouse_up" code=0 disp="changegroupactive" arg="id28"
    missing mask=69 key="" code=50 disp="moveintogroup" arg="d"
CASE HARD-1       FAIL missing=17 extra=1 oracle_binds=22 (HARD tree lines=32 binds=22 unbinds=3 vars=4) v3_model=agree
    missing mask=4 key="mouse:274" code=0 disp="mouse" arg="MoveWindow"
    missing mask=76 key="" code=202 disp="pseudo" arg=""
    extra   mask=64 key="mouse:274" code=0 disp="mouse" arg="movewindow"
CASE HARD-2       FAIL missing=15 extra=1 oracle_binds=20 (HARD tree lines=31 binds=20 unbinds=3 vars=4) v3_model=agree
    missing mask=72 key="" code=31 disp="swapwindow" arg="d"
    missing mask=73 key="O" code=0 disp="fullscreenstate" arg="5k0u"
    extra   mask=64 key="J" code=0 disp="exec" arg="cjpuyx"
CASE HARD-3       FAIL missing=13 extra=2 oracle_binds=17 (HARD tree lines=28 binds=17 unbinds=3 vars=4) v3_model=agree
    missing mask=64 key="" code=117 disp="movetoworkspacesilent" arg="e-1"
    missing mask=76 key="KP_5" code=0 disp="fullscreen" arg=""
    extra   mask=64 key="mouse:273" code=0 disp="mouse" arg="resizewindow"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=31/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Result and byte preservation

Both measurements exited 1, not 2; no inconclusive receipt or retry occurred. BASE passed both times, and each oracle agreed exactly with the live table before scoring. All VARIABLE, SOURCE, GLOB, UNSOURCED, UNBIND and SYNTH cases passed; all REWRITE and HARD cases failed. Seed-dependent edits of keycode-containing files also failed (ADD-3 and two COMMENT cases in run 1; two COMMENT cases in run 2).

Concrete detector output: REWRITE-0 in both runs reports `missing=42 extra=0`, including the missing workspace code:10 and code:11 entries. Changing a file invalidates its whole-file cache, and the easy parser cannot reconstruct those code binds. HARD additionally exposes alias/grammar/projection limitations; for example run 2 HARD-1 expects mouse argument `MoveWindow` but this parser lowercases it to `movewindow`.

The compressed payload contains all 192 live entries, yet both receipts report `embed_hits=0`: the plain-string embed guard does not detect this encoding. The composite predicate nevertheless rejects this standalone shortcut on behavioral cases. This is a rejected control shape, not a claimed killed implementation mutant (there was no pristine implementation baseline). No contract change is proposed. The observation establishes neither that every possible encoded-cache shape fails nor that the frozen counter covers all resolver defects.

Both measured control hashes equal the pre-write hash `4b4736a81453c37a29f6c4f0f4d20097b148484bab7386215688a03479858138`. Both measured frozen-counter hashes equal `323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2`, and both measured generator hashes equal `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`. Counter completion used its inspected process-group cleanup path; this item started no separate oracle or long-lived process.

Only this item's new control and this report were written in the lane. No counter, generator, claimed tool, corpus file, live compositor setting, package or service was edited. No git/jj write command was run. No scratch mutation of existing bytes was performed, so restoration means no pre-existing file was replaced. The retained control is the requested deliverable; its build hash and measured hashes are reported above. The counter receipts supply the actual counter/generator pins, rather than treating a stated pin as measured evidence.

Tool installs/updates: none. No extra builds, linters, formatters or smoke tests were run; only build-input acquisition/association and the requested bounded counter scoring.
