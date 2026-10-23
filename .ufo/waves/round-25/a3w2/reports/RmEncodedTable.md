# RmEncodedTable — independent remeasurement and cache-granularity attack

REMEASURE K4EncodedTable: 31/41 (receipt said 31/41); strengthened: 37/41 — not met

## Scope and integrity

Axes: shortcut strength, easy-grammar boundary, byte preservation, host isolation.

Read the godspeed skill, operator rules, registration Attempt 3/PRED-C1 (v4), the committed control/receipt, and its original shape in `a3w1-spec.json`. The receipt reports two measurements, 30/41 and 31/41; its headline is the best, 31/41. This independent fresh-seed measurement also returned 31/41, with `embed_hits=0`.

Before scoring, from the lane root:

```sh
timeout 20 prlimit --as=4000000000 sha256sum .ufo/waves/round-25/controls/v4/K4EncodedTable.py .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py
```

Actual output:

```text
4b4736a81453c37a29f6c4f0f4d20097b148484bab7386215688a03479858138  .ufo/waves/round-25/controls/v4/K4EncodedTable.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
```

The control hash equals the receipt's named hash exactly. Both scorer pins also equal the registration. No original control, receipt, counter, generator, implementation, or sibling file was edited.

## Measurement 1: committed control

Working directory: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Exact executed command:

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 timeout 1200 prlimit --as=4000000000 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EncodedTable.py
```

`-B` prevents bytecode writes when the counter imports its lane generator; `prlimit` supplies the required memory cap. No seed was supplied. One earlier asynchronous launch request was rejected by the tool with `Background job limit reached (100). Wait for running jobs to finish or cancel one.` It did not launch a measurement; the command above was then executed synchronously. There was one completed original-control score, no exit-2 receipt, and no score-until-pass retry.

Verbatim counter stdout, followed by the observed exit status:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EncodedTable.py sha256:4b4736a81453c37a29f6c4f0f4d20097b148484bab7386215688a03479858138
seed=3cea7f8dcd2c02d8
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        FAIL missing=41 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=0 key='XF86KbdBrightnessUp' keycode=0) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=68 key='W' keycode=0) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='' keycode=14) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='PRINT' keycode=0) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vrjeaedi) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vfdhipyo) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vzuiyqib) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vmotancz) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 11) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 20) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 13) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    FAIL missing=41 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE COMMENT-1    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=2) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    FAIL missing=41 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='' code=14; unbind mask=65 key='' code=13; add fullscreen) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE REWRITE-1    FAIL missing=42 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='M' code=0; unbind mask=65 key='E' code=0; add exec) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE REWRITE-2    FAIL missing=41 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='COMMA' code=0; unbind mask=72 key='' code=12; add workspace) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE REWRITE-3    FAIL missing=42 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='XF86AudioMute' code=0; unbind mask=68 key='A' code=0; add exec) v3_model=agree
    missing mask=64 key="" code=10 disp="workspace" arg="1"
    missing mask=64 key="" code=11 disp="workspace" arg="2"
CASE HARD-0       FAIL missing=20 extra=0 oracle_binds=24 (HARD tree lines=34 binds=24 unbinds=2 vars=4) v3_model=agree
    missing mask=72 key="J" code=0 disp="killactive" arg="n0pz"
    missing mask=72 key="" code=151 disp="togglegroup" arg="5z89"
CASE HARD-1       FAIL missing=14 extra=0 oracle_binds=17 (HARD tree lines=27 binds=17 unbinds=3 vars=4) v3_model=agree
    missing mask=73 key="mouse:274" code=0 disp="changegroupactive" arg=""
    missing mask=64 key="mouse:274" code=0 disp="mouse" arg="resizewindow"
CASE HARD-2       FAIL missing=15 extra=0 oracle_binds=21 (HARD tree lines=28 binds=21 unbinds=2 vars=4) v3_model=agree
    missing mask=68 key="" code=147 disp="layoutmsg" arg="tutq"
    missing mask=4 key="F5" code=0 disp="changegroupactive" arg="qx08"
CASE HARD-3       FAIL missing=16 extra=0 oracle_binds=21 (HARD tree lines=27 binds=21 unbinds=1 vars=4) v3_model=agree
    missing mask=72 key="" code=43 disp="exec" arg="uwsm-app -- 2zk94p \"$(i508f lmg)\""
    missing mask=1 key="" code=142 disp="exec" arg="notify-send 3xon4r notify-send vhyh2,u8e"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=31/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Receipt attack and shape-preserving strengthening

The original receipt accurately describes its bytes: whole-file SHA-256 hits replay saved operations; any changed file falls back to its easy parser. That is an encoded-cache-plus-delta control, but it is not as strong as the general shape permits. An added harmless line or whitespace-only re-spelling discards every observed row owned by that file. The fresh run exposes this directly: ADD-0 and COMMENT-0 each lose 41 unchanged rows in `tiling-v2.conf`; every REWRITE case also loses the cached keycode rows. These failures do not establish that a normalized encoded cache needs to interpret those real keycodes.

Retained stronger output:

```text
/fast/scratch/hyaku/mado-r25a3/rm/K4EncodedTable-strong.py
bytes=23889
sha256=710879a679e98a7ed134953ae71f879ecf2fc3354f6866f3d66783053ab2ac7d
```

Build was performed in the Python eval kernel, not by editing the lane. It decoded the existing control's payload; checked each of its five bind-bearing host files against that payload's original SHA-256; zipped each file's easy-operation sequence with its saved operation sequence; and encoded 192 observed-row templates into the same zlib/base64 payload. All five digests matched, all operation counts/kinds aligned, and duplicate template identities were checked to have identical cached fields except `arg`. The five files were `.config/hypr/bindings.conf` and the cached clipboard/media/tiling-v2/utilities files. The encoded payload grew from 12112 to 15860 base64 bytes.

The single behavior-bearing change is cache granularity on the changed-file fallback. Exact whole-file hits still replay the original manifest. For changed files, the original easy tokenizer supplies ordered operations. A normalized identity uses flags, canonical modifier tokens, literal key text, description, and dispatcher; an observed identity reuses its cached 18-field row, updating the non-mouse final argument from the changed line. Unknown identities still use the original easy parser. Comments, spacing, modifier/dispatcher case, and argument changes therefore need not destroy known row fields.

This remains ENCODED CACHE + DELTA: a literal cached `code:11` is an opaque identity, not an implemented keycode parser. No new keycode-bind interpreter, modifier alias/separator parser, submap/chord interpreter, full rejection grammar, label detection, oracle access, counter mutation, or generator-function transcription was added. The original easy parser's limitations on fresh HARD trees remain. This is a stronger witness within the shape, not a claim to have found its universal maximum.

## Measurement 2: strengthened control

Same working directory. Exact command, once, with a new default seed:

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 timeout 1200 prlimit --as=4000000000 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /fast/scratch/hyaku/mado-r25a3/rm/K4EncodedTable-strong.py
```

Verbatim counter stdout, followed by the observed exit status:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/rm/K4EncodedTable-strong.py sha256:710879a679e98a7ed134953ae71f879ecf2fc3354f6866f3d66783053ab2ac7d
seed=2ca800a182c60abe
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=190 (UNBIND mask=9 key='TAB' keycode=0) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=72 key='COMMA' keycode=0) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=0 key='XF86AudioPlay' keycode=0) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=68 key='F' keycode=0) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vrnpfpcc) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vvdjcayx) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vfzibbxt) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vizholte) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 20) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 5) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 17) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-1    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=76 key='R' code=0; unbind mask=65 key='C' code=0; add workspace) v3_model=agree
CASE REWRITE-1    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='BACKSPACE' code=0; unbind mask=64 key='COMMA' code=0; add movetoworkspacesilent) v3_model=agree
CASE REWRITE-2    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='' code=11; unbind mask=65 key='UP' code=0; add exec) v3_model=agree
CASE REWRITE-3    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioPlay' code=0; unbind mask=76 key='Z' code=0; add movetoworkspacesilent) v3_model=agree
CASE HARD-0       FAIL missing=15 extra=0 oracle_binds=21 (HARD tree lines=29 binds=21 unbinds=2 vars=4) v3_model=agree
    missing mask=72 key="" code=54 disp="moveintogroup" arg="u"
    missing mask=65 key="" code=161 disp="togglefloating" arg="su2g"
CASE HARD-1       FAIL missing=14 extra=2 oracle_binds=21 (HARD tree lines=28 binds=21 unbinds=1 vars=4) v3_model=agree
    missing mask=0 key="" code=103 disp="fullscreenstate" arg=""
    missing mask=8 key="mouse_down" code=0 disp="killactive" arg=""
    extra   mask=69 key="mouse:274" code=0 disp="fullscreen" arg="6o04"
    extra   mask=64 key="mouse:273" code=0 disp="mouse" arg="resizewindow"
CASE HARD-2       FAIL missing=17 extra=0 oracle_binds=23 (HARD tree lines=28 binds=23 unbinds=0 vars=4) v3_model=agree
    missing mask=65 key="mouse:272" code=0 disp="mouse" arg="MoveWindow"
    missing mask=64 key="mouse:273" code=0 disp="mouse" arg="resizewindow"
CASE HARD-3       FAIL missing=20 extra=0 oracle_binds=23 (HARD tree lines=29 binds=23 unbinds=2 vars=4) v3_model=agree
    missing mask=73 key="8" code=0 disp="killactive" arg="xvhu"
    missing mask=76 key="" code=72 disp="fullscreenstate" arg=""
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=37/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

All 37 non-HARD cases passed the stronger control, including REWRITE-2's argument swap of the cached `code:11` binding. Every HARD case still failed. Both programs contain the complete encoded live table and both score `embed_hits=0`: encoding still evades that plain-substring guard. Fresh seeds differ, so the six-point aggregate difference is not a paired same-seed estimate; the individual oracle receipts and the targeted probe below are the evidence. Neither control meets PRED-C1 (v4).

## One isolated mutation probe: stale cached argument

To challenge the stronger cache's argument-update invariant, copied its exact measured bytes into an isolated scratch directory; did not mutate the retained stronger output or the lane.

Mutant: replace this single assignment in the scratch copy's cached-entry path:

```python
entry["arg"] = expand(operation[2], variables)
```

with:

```python
entry["arg"] = CACHE["live"][operation[1]]["arg"]
```

This is a plausible stale-cache defect: known key identity is retained but an edited argument is silently ignored.

Expected detector: a fixed scratch home sources only the snapshot `tiling-v2.conf`, with exactly the SUPER/code:11/workspace argument changed from `2` to `8`. Expected rows are the 90 cached live observations for that file, with only the corresponding row's argument changed to `8`. The detector runs the actual tool CLI and compares all row fields as a duplicate-preserving multiset using `collections.Counter(json.dumps(row, sort_keys=True, separators=(",", ":")) for row in rows)`. It reports nonzero if tool exit, missing count, or extra count is nonzero. This is a bounded targeted detector, not another full v4 score and not a new oracle claim.

The identical CLI command was run on pristine, mutated, and restored bytes:

```sh
timeout 10 prlimit --as=4000000000 python3 -I -B /fast/scratch/hyaku/mado-r25a3/rm/K4EncodedTable-argdelta-si2z8qlx/probe.py --home /fast/scratch/hyaku/mado-r25a3/rm/K4EncodedTable-argdelta-si2z8qlx/home
```

Actual detector outputs:

```text
pristine tool_exit=0 rows=90 expected=90 missing=0 extra=0 detector_exit=0 sha256=710879a679e98a7ed134953ae71f879ecf2fc3354f6866f3d66783053ab2ac7d
mutated tool_exit=0 rows=90 expected=90 missing=1 extra=1 detector_exit=1 sha256=c9affb1cb73b7d2f7b05c1a05b606a23325a6c323039e31c72affbee4083391c
restored_bytes_equal_pristine=True
restored tool_exit=0 rows=90 expected=90 missing=0 extra=0 detector_exit=0 sha256=710879a679e98a7ed134953ae71f879ecf2fc3354f6866f3d66783053ab2ac7d
mutation_verdict=killed
```

Restoration used the saved exact original scratch bytes in `finally`, before the restored detector run. The targeted detector's pristine baseline passed, so this isolated mutant is killed. The full-v4 baseline control already failed, so its remeasurement is a rejected control, not a killed implementation mutant. No detector result changes the contract.

## Preservation and cleanup

After both scores and after restoring the probe, ran:

```sh
timeout 20 prlimit --as=4000000000 sha256sum .ufo/waves/round-25/controls/v4/K4EncodedTable.py .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py /fast/scratch/hyaku/mado-r25a3/rm/K4EncodedTable-strong.py /fast/scratch/hyaku/mado-r25a3/rm/K4EncodedTable-argdelta-si2z8qlx/probe.py
```

Actual output:

```text
4b4736a81453c37a29f6c4f0f4d20097b148484bab7386215688a03479858138  .ufo/waves/round-25/controls/v4/K4EncodedTable.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
710879a679e98a7ed134953ae71f879ecf2fc3354f6866f3d66783053ab2ac7d  /fast/scratch/hyaku/mado-r25a3/rm/K4EncodedTable-strong.py
710879a679e98a7ed134953ae71f879ecf2fc3354f6866f3d66783053ab2ac7d  /fast/scratch/hyaku/mado-r25a3/rm/K4EncodedTable-argdelta-si2z8qlx/probe.py
```

The original control/counter/generator hashes are unchanged. The retained stronger output equals the hash scored by v4. The probe's restored hash equals its pristine hash and the retained stronger file's hash.

Removed only this item's restored throwaway probe/fixture tree after recording its restoration evidence:

```sh
timeout 20 prlimit --as=4000000000 rm -r -- /fast/scratch/hyaku/mado-r25a3/rm/K4EncodedTable-argdelta-si2z8qlx
```

Cleanup exited 0 with no output. The requested stronger output remains at its named path. Only this report was written in the lane. No git/jj write commands, subagent dispatch, package/service/config changes, live-compositor write verbs, or independently started nested compositor were used. The two counters completed and followed their inspected nested-process-group cleanup paths; the three direct tool subprocesses also completed. No background process was intentionally retained. No lane bytecode was generated by these `-B` runs.

Tool installs/updates: none. No build, lint, formatter, or other verification was run beyond the two requested v4 scores, the one bounded three-state mutation detector, and the recorded integrity hashes.

REMEASURE K4EncodedTable: 31/41 (receipt said 31/41); strengthened: 37/41 — not met
