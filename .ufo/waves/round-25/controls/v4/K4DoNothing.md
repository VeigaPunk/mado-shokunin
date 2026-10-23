# K4DoNothing — frozen C1 v4 control

## Verdict
CONTROL K4DoNothing v4 best: cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED — not met

Both fresh-seed control runs scored 0/41, embed_hits=0, exit=1. The absent-tool baseline at 41cc04c8 also scored 0/41, embed_hits=0, exit=1. No exit-2 result occurred, so no retry was needed. These are the counter's observed results, not a canonical Rust judgment or an admission of the claimed tool.

## Shape and scope

- Read the registration's current Attempt 3 section first, then the required godspeed skill and the relevant frozen counter sections.
- Created only `.ufo/waves/round-25/controls/v4/K4DoNothing.py` and this report in the lane. The control is **0 bytes**, sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855. It contains no parser, source traversal, embedded table, compositor access, or other claimed work. `tools/mado-binds.py` was not created or edited.
- The alternative allowed shape, explicitly exiting 0 without output, cannot score higher under the frozen executor: `c1/count-v3.py:729–743` checks a nonzero exit first, then parses stdout as JSON. Both allowed shapes return exit 0 and empty stdout, so both reach the same rejection. The explicit-exit variant was not separately built or run; the empty-file choice is the strongest tied shape by this executor logic.
- Verified the frozen counter hash before scoring: `323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2`; generator hash: `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`.
- Ran the two controls and the absent-tool baseline concurrently, each with a 1,200-second timeout and 4,000,000,000-byte address-space cap. No seed override was supplied; all three receipts have distinct fresh seeds. Existing frozen host-wide oracle locks enforce the six-instance limit.

## Counterexample, evidence, impacted axes, smallest safe correction

**Counterexample tested:** a valid Python program that succeeds silently, without reading the configuration. It is rejected on every case in both control runs, including BASE: `FAIL stdout is not a JSON array of objects`. Successful process termination alone therefore does not count as bind-table resolution. The missing-file baseline independently takes the `tool absent` failure path on every case.

**Evidence:** the full receipts below show matching live and BASE-oracle tables (`ORACLE_CHECK base_vs_live missing=0 extra=0`), 192 live binds, identical 79-file snapshot digests, and 41 case failures per run. `count-v3.py:735–743` rejects empty stdout before multiset comparison; `count.py:278–284` never increments the pass count for an absent tool or failed tool-output parse. All three diagnostic `V3_MODEL_AGREE 41/41` lines are explicitly not the predicate. `embed_hits=0` does not rescue failure to emit a table.

**Impacted axes:** C1 operability fails (no JSON bind table); C1 capability acquisition is not demonstrated (the control acquires no configuration semantics). No conclusion about other shortcut shapes, the resolver's grammar coverage, C2, or overall oracle soundness follows from this narrow control.

**Smallest safe correction:** none to the frozen counter is supported by this evidence. Within the assigned DO-NOTHING shape there is no correction that produces a valid table. Keep the observed rejection; implement and measure the actual resolver separately rather than converting silence or process exit 0 into success. This is a rejected shortcut, not a demonstrated counter defect or an axis tradeoff requiring a judgment here.

## Commands and safety

Working directory for all commands: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Preflight commands:

```sh
sha256sum .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py
df -h /fast
```

Observed preflight output:

```text
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  583G  221G  73% /fast
```

All three scoring commands finished with counter exit 1, not timeout or setup failure. Oracle exec-line stripping and nested-process termination were left to the frozen counter's existing `strip_exec` and `oracle` finally block (`count.py:77–97,124–189`); no independent nested compositor or live-compositor write verb was invoked. No packages, services, home configuration, git/jj state, counter bytes, or corpus files were modified; no tools were installed or upgraded. No builds, tests, linters, or formatters were run.

## Receipts

Each block preserves the counter stdout, followed by `exit=` from the command's recorded exit code. Tool-harness `Error:`, timing, and command-status wrappers are not counter stdout and are omitted.

### Control run 1 — seed 166466dfabe7fd52

```sh
prlimit --as=4000000000 timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4DoNothing.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4DoNothing.py sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
seed=166466dfabe7fd52
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL stdout is not a JSON array of objects (unperturbed) v3_model=agree
CASE ADD-0        FAIL stdout is not a JSON array of objects (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-1        FAIL stdout is not a JSON array of objects (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-2        FAIL stdout is not a JSON array of objects (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-3        FAIL stdout is not a JSON array of objects (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE UNBIND-0     FAIL stdout is not a JSON array of objects (UNBIND mask=76 key='B' keycode=0) v3_model=agree
CASE UNBIND-1     FAIL stdout is not a JSON array of objects (UNBIND mask=72 key='' keycode=11) v3_model=agree
CASE UNBIND-2     FAIL stdout is not a JSON array of objects (UNBIND mask=12 key='DELETE' keycode=0) v3_model=agree
CASE UNBIND-3     FAIL stdout is not a JSON array of objects (UNBIND mask=72 key='LEFT' keycode=0) v3_model=agree
CASE VARIABLE-0   FAIL stdout is not a JSON array of objects (VARIABLE $vwiczlic) v3_model=agree
CASE VARIABLE-1   FAIL stdout is not a JSON array of objects (VARIABLE $vzwgkfwb) v3_model=agree
CASE VARIABLE-2   FAIL stdout is not a JSON array of objects (VARIABLE $vkhnsqlu) v3_model=agree
CASE VARIABLE-3   FAIL stdout is not a JSON array of objects (VARIABLE $vwdtwvzh) v3_model=agree
CASE SOURCE-0     FAIL stdout is not a JSON array of objects (SOURCE new file at root line 11) v3_model=agree
CASE SOURCE-1     FAIL stdout is not a JSON array of objects (SOURCE new file at root line 6) v3_model=agree
CASE SOURCE-2     FAIL stdout is not a JSON array of objects (SOURCE new file at root line 13) v3_model=agree
CASE SOURCE-3     FAIL stdout is not a JSON array of objects (SOURCE new file at root line 7) v3_model=agree
CASE GLOB-0       FAIL stdout is not a JSON array of objects (GLOB new toggles file) v3_model=agree
CASE GLOB-1       FAIL stdout is not a JSON array of objects (GLOB new toggles file) v3_model=agree
CASE GLOB-2       FAIL stdout is not a JSON array of objects (GLOB new toggles file) v3_model=agree
CASE GLOB-3       FAIL stdout is not a JSON array of objects (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  FAIL stdout is not a JSON array of objects (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  FAIL stdout is not a JSON array of objects (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  FAIL stdout is not a JSON array of objects (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  FAIL stdout is not a JSON array of objects (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    FAIL stdout is not a JSON array of objects (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE COMMENT-1    FAIL stdout is not a JSON array of objects (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-2    FAIL stdout is not a JSON array of objects (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE COMMENT-3    FAIL stdout is not a JSON array of objects (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE SYNTH-0      FAIL stdout is not a JSON array of objects (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      FAIL stdout is not a JSON array of objects (SYNTH tree binds=11 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      FAIL stdout is not a JSON array of objects (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      FAIL stdout is not a JSON array of objects (SYNTH tree binds=11 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    FAIL stdout is not a JSON array of objects (REWRITE argswap mask=64 key='' code=16; unbind mask=68 key='Delete' code=0; add workspace) v3_model=agree
CASE REWRITE-1    FAIL stdout is not a JSON array of objects (REWRITE argswap mask=0 key='XF86AudioLowerVolume' code=0; unbind mask=65 key='RIGHT' code=0; add exec) v3_model=agree
CASE REWRITE-2    FAIL stdout is not a JSON array of objects (REWRITE argswap mask=65 key='' code=11; unbind mask=64 key='XF86AudioMute' code=0; add exec) v3_model=agree
CASE REWRITE-3    FAIL stdout is not a JSON array of objects (REWRITE argswap mask=68 key='BACKSPACE' code=0; unbind mask=64 key='ESCAPE' code=0; add changegroupactive) v3_model=agree
CASE HARD-0       FAIL stdout is not a JSON array of objects (HARD tree lines=30 binds=22 unbinds=3 vars=4) v3_model=agree
CASE HARD-1       FAIL stdout is not a JSON array of objects (HARD tree lines=32 binds=25 unbinds=1 vars=4) v3_model=agree
CASE HARD-2       FAIL stdout is not a JSON array of objects (HARD tree lines=35 binds=27 unbinds=3 vars=4) v3_model=agree
CASE HARD-3       FAIL stdout is not a JSON array of objects (HARD tree lines=28 binds=15 unbinds=3 vars=4) v3_model=agree
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### Control run 2 — seed ecc0ec494af77e9f

```sh
prlimit --as=4000000000 timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4DoNothing.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4DoNothing.py sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
seed=ecc0ec494af77e9f
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL stdout is not a JSON array of objects (unperturbed) v3_model=agree
CASE ADD-0        FAIL stdout is not a JSON array of objects (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-1        FAIL stdout is not a JSON array of objects (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE ADD-2        FAIL stdout is not a JSON array of objects (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE ADD-3        FAIL stdout is not a JSON array of objects (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE UNBIND-0     FAIL stdout is not a JSON array of objects (UNBIND mask=64 key='' keycode=11) v3_model=agree
CASE UNBIND-1     FAIL stdout is not a JSON array of objects (UNBIND mask=65 key='D' keycode=0) v3_model=agree
CASE UNBIND-2     FAIL stdout is not a JSON array of objects (UNBIND mask=64 key='mouse_up' keycode=0) v3_model=agree
CASE UNBIND-3     FAIL stdout is not a JSON array of objects (UNBIND mask=65 key='P' keycode=0) v3_model=agree
CASE VARIABLE-0   FAIL stdout is not a JSON array of objects (VARIABLE $vkaeudgo) v3_model=agree
CASE VARIABLE-1   FAIL stdout is not a JSON array of objects (VARIABLE $vpliuxoo) v3_model=agree
CASE VARIABLE-2   FAIL stdout is not a JSON array of objects (VARIABLE $vijsppua) v3_model=agree
CASE VARIABLE-3   FAIL stdout is not a JSON array of objects (VARIABLE $vvzscjqm) v3_model=agree
CASE SOURCE-0     FAIL stdout is not a JSON array of objects (SOURCE new file at root line 9) v3_model=agree
CASE SOURCE-1     FAIL stdout is not a JSON array of objects (SOURCE new file at root line 5) v3_model=agree
CASE SOURCE-2     FAIL stdout is not a JSON array of objects (SOURCE new file at root line 12) v3_model=agree
CASE SOURCE-3     FAIL stdout is not a JSON array of objects (SOURCE new file at root line 5) v3_model=agree
CASE GLOB-0       FAIL stdout is not a JSON array of objects (GLOB new toggles file) v3_model=agree
CASE GLOB-1       FAIL stdout is not a JSON array of objects (GLOB new toggles file) v3_model=agree
CASE GLOB-2       FAIL stdout is not a JSON array of objects (GLOB new toggles file) v3_model=agree
CASE GLOB-3       FAIL stdout is not a JSON array of objects (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  FAIL stdout is not a JSON array of objects (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  FAIL stdout is not a JSON array of objects (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  FAIL stdout is not a JSON array of objects (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  FAIL stdout is not a JSON array of objects (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    FAIL stdout is not a JSON array of objects (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-1    FAIL stdout is not a JSON array of objects (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE COMMENT-2    FAIL stdout is not a JSON array of objects (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE COMMENT-3    FAIL stdout is not a JSON array of objects (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE SYNTH-0      FAIL stdout is not a JSON array of objects (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE SYNTH-1      FAIL stdout is not a JSON array of objects (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      FAIL stdout is not a JSON array of objects (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      FAIL stdout is not a JSON array of objects (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    FAIL stdout is not a JSON array of objects (REWRITE argswap mask=76 key='Delete' code=0; unbind mask=0 key='XF86AudioPlay' code=0; add exec) v3_model=agree
CASE REWRITE-1    FAIL stdout is not a JSON array of objects (REWRITE argswap mask=65 key='' code=20; unbind mask=73 key='RIGHT' code=0; add exec) v3_model=agree
CASE REWRITE-2    FAIL stdout is not a JSON array of objects (REWRITE argswap mask=69 key='R' code=0; unbind mask=64 key='' code=20; add fullscreen) v3_model=agree
CASE REWRITE-3    FAIL stdout is not a JSON array of objects (REWRITE argswap mask=69 key='G' code=0; unbind mask=73 key='F' code=0; add exec) v3_model=agree
CASE HARD-0       FAIL stdout is not a JSON array of objects (HARD tree lines=29 binds=20 unbinds=2 vars=4) v3_model=agree
CASE HARD-1       FAIL stdout is not a JSON array of objects (HARD tree lines=29 binds=20 unbinds=2 vars=4) v3_model=agree
CASE HARD-2       FAIL stdout is not a JSON array of objects (HARD tree lines=28 binds=23 unbinds=1 vars=4) v3_model=agree
CASE HARD-3       FAIL stdout is not a JSON array of objects (HARD tree lines=32 binds=25 unbinds=2 vars=4) v3_model=agree
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### Absent-tool baseline — seed fc549bad5a101d40

```sh
prlimit --as=4000000000 timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 41cc04c8
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=41cc04c8d593837a0d5078bffaacdaa163d12897 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=MISSING_TOOL at 41cc04c8d593837a0d5078bffaacdaa163d12897
seed=fc549bad5a101d40
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL tool absent (unperturbed) v3_model=agree
CASE ADD-0        FAIL tool absent (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-1        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-2        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-3        FAIL tool absent (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE UNBIND-0     FAIL tool absent (UNBIND mask=65 key='B' keycode=0) v3_model=agree
CASE UNBIND-1     FAIL tool absent (UNBIND mask=8 key='TAB' keycode=0) v3_model=agree
CASE UNBIND-2     FAIL tool absent (UNBIND mask=8 key='XF86MonBrightnessUp' keycode=0) v3_model=agree
CASE UNBIND-3     FAIL tool absent (UNBIND mask=68 key='BACKSPACE' keycode=0) v3_model=agree
CASE VARIABLE-0   FAIL tool absent (VARIABLE $veysdqew) v3_model=agree
CASE VARIABLE-1   FAIL tool absent (VARIABLE $vptdadpm) v3_model=agree
CASE VARIABLE-2   FAIL tool absent (VARIABLE $vsvdfzph) v3_model=agree
CASE VARIABLE-3   FAIL tool absent (VARIABLE $vyhdkjkw) v3_model=agree
CASE SOURCE-0     FAIL tool absent (SOURCE new file at root line 9) v3_model=agree
CASE SOURCE-1     FAIL tool absent (SOURCE new file at root line 12) v3_model=agree
CASE SOURCE-2     FAIL tool absent (SOURCE new file at root line 13) v3_model=agree
CASE SOURCE-3     FAIL tool absent (SOURCE new file at root line 13) v3_model=agree
CASE GLOB-0       FAIL tool absent (GLOB new toggles file) v3_model=agree
CASE GLOB-1       FAIL tool absent (GLOB new toggles file) v3_model=agree
CASE GLOB-2       FAIL tool absent (GLOB new toggles file) v3_model=agree
CASE GLOB-3       FAIL tool absent (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  FAIL tool absent (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  FAIL tool absent (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  FAIL tool absent (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  FAIL tool absent (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    FAIL tool absent (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE COMMENT-1    FAIL tool absent (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-2    FAIL tool absent (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE COMMENT-3    FAIL tool absent (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE SYNTH-0      FAIL tool absent (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      FAIL tool absent (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE SYNTH-2      FAIL tool absent (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      FAIL tool absent (SYNTH tree binds=10 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    FAIL tool absent (REWRITE argswap mask=8 key='XF86AudioLowerVolume' code=0; unbind mask=64 key='' code=10; add workspace) v3_model=agree
CASE REWRITE-1    FAIL tool absent (REWRITE argswap mask=76 key='R' code=0; unbind mask=0 key='F9' code=0; add exec) v3_model=agree
CASE REWRITE-2    FAIL tool absent (REWRITE argswap mask=64 key='' code=18; unbind mask=68 key='X' code=0; add bringactivetotop) v3_model=agree
CASE REWRITE-3    FAIL tool absent (REWRITE argswap mask=65 key='' code=13; unbind mask=68 key='V' code=0; add moveintogroup) v3_model=agree
CASE HARD-0       FAIL tool absent (HARD tree lines=29 binds=18 unbinds=3 vars=4) v3_model=agree
CASE HARD-1       FAIL tool absent (HARD tree lines=33 binds=22 unbinds=3 vars=4) v3_model=agree
CASE HARD-2       FAIL tool absent (HARD tree lines=31 binds=21 unbinds=3 vars=4) v3_model=agree
CASE HARD-3       FAIL tool absent (HARD tree lines=29 binds=22 unbinds=1 vars=4) v3_model=agree
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

