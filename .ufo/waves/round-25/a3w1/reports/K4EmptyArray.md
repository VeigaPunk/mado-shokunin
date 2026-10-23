# K4EmptyArray — ALL-FALSE control, counter v4

## Verdict
CONTROL K4EmptyArray v4 best: cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED — not met

Both variants tied on the frozen predicate: empty-array 0/41 on two scored fresh seeds; one-constant-entry 0/41 on two scored fresh seeds. Retained the simpler empty-array control, which also avoids the constant variant's extra bind in every case. The restored empty-array bytes scored 0/41 once more. No result met C1.

## Scope and axes

Axes: exact-bind-table cases passed, embed hits, adherence to the ALL-FALSE shape, and exact restoration. Read `skill://godspeed` and the registration's Attempt 3/PRED-C1 (v4) section before implementation. Only the assigned program and this report were written in the lane; no resolver, counter, generator, corpus file, sibling source, package, service, user config, or live-compositor setting was changed. No subagents or other orchestration runtime were invoked.

Program: `.ufo/waves/round-25/controls/v4/K4EmptyArray.py`. A single stdlib Python file accepts required `--home DIR` but never opens DIR, follows sources, parses binds, or contacts the compositor. The baseline prints exactly `[]` and a newline. The variant changes only line 8 to print one fixed 18-field bind entry (SUPER/RETURN, dispatcher exec, arg true); its bind booleans are false and `submap_universal` is the Hyprland JSON string `"false"`. It does not execute the printed bind.

The retained source is:

```python
#!/usr/bin/env python3
"""ALL-FALSE control: accept --home without inspecting the config tree."""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--home", required=True)
parser.parse_args()
print("[]")
```

For the tested constant variant, replace only the final line with:

```python
print('[{"locked":false,"mouse":false,"release":false,"repeat":false,"longPress":false,"non_consuming":false,"auto_consuming":false,"has_description":false,"modmask":64,"submap":"","submap_universal":"false","key":"RETURN","keycode":0,"catch_all":false,"description":"","allow_input_capture":false,"dispatcher":"exec","arg":"true"}]')
```

Across the five fully scored runs (205 case evaluations), the oracle returned 10–194 entries per case. Thus no choice of a single constant entry could exactly match any of these observed tables; choosing a different constant cannot improve the measured case-pass score. This is a cardinality observation about these receipts, not a new contract or a claim about unrun seeds.

## Commands and setup

Working directory for every counter command: `/home/vgpnk/Projects/shokunin/mado-shokunin`. Every counter process had a 1200-second timeout, a 10-second timeout kill grace, and a 4,000,000,000-byte address-space limit. No `--seed` was supplied; every run drew a fresh seed. The two runs of each version were launched concurrently against unchanged program bytes; all completed before changing those bytes. The frozen counter controls its own host-wide six-instance oracle lock limit.

The first two attempts exited 2 before scoring because the Eval subprocess environment lacked `HYPRLAND_INSTANCE_SIGNATURE` and `WAYLAND_DISPLAY` (its HOME and XDG_RUNTIME_DIR were correct). The diagnostic `timeout 20 prlimit --as=4000000000 hyprctl binds -j` returned `HYPRLAND_INSTANCE_SIGNATURE not set! (is hyprland running?)`, exit 1. Read-only Bash commands `timeout 10 printenv HYPRLAND_INSTANCE_SIGNATURE XDG_RUNTIME_DIR WAYLAND_DISPLAY HOME` and `timeout 20 prlimit --as=4000000000 hyprctl instances -j` identified the existing operator instance and wayland-1. Each exit-2 attempt was then re-run exactly once with those existing session variables explicitly supplied to the counter child process. No host/session configuration was changed. Both initial exit-2 receipts are preserved below; neither is treated as a scored failure or a kill.

## Results and mutation probe

| Version/run | Fresh seed | cases_pass | embed_hits | Exit |
|---|---|---:|---:|---:|
| empty-array run 1 | 543117314893c994 | not measured | not measured | 2 |
| empty-array run 2 | 86ada8629515bd1a | not measured | not measured | 2 |
| empty-array run 1 exit-2 rerun | 96393ceb87c48b9f | 0/41 | 0 | 1 |
| empty-array run 2 exit-2 rerun | 2aaf5be0d75036e7 | 0/41 | 0 | 1 |
| one-constant-entry run 1 | e1f75dec66ebcb9c | 0/41 | 0 | 1 |
| one-constant-entry run 2 | 5ab71524d3ac00c5 | 0/41 | 0 | 1 |
| empty-array restored-byte detector | 8256fe04021db750 | 0/41 | 0 | 1 |

Expected detector: the same frozen `c1/count.py` v4 command below, requiring 41/41 exact 18-field bind multisets and zero embed hits. For both constant-output shapes, nonempty/multi-bind oracle tables should produce missing-bind failures; the one-entry variant can also produce an extra bind. Observed: every scored case failed, ORACLE_CHECK reported missing=0 extra=0, and V3_MODEL_AGREE was 41/41 in every fully scored run. Empty output had extra=0 throughout; the fixed entry had extra=1 throughout.

Mutant: one behavior-bearing change at K4EmptyArray.py:8, `print("[]")` to the fixed one-entry JSON output. Mutation-testing verdict: **INCONCLUSIVE**, not killed or survived, because the pristine baseline already misses the target. The control verdict is independently **not met** for both shapes. No conclusion about feature coverage of a real resolver follows from this mutation.

## Hashes and restoration evidence

| Bytes | SHA-256 |
|---|---|
| Pristine empty-array program, 227 bytes | `db6ede4c405224fabda07312413f87b94f7ca684559966b5f9d28858da0e5962` |
| Mutated one-entry program, 550 bytes | `f1f1928ced8ef49072bfc6be5d302392e6d8855b6faa78490369fc178af3b46a` |
| Restored empty-array program, 227 bytes | `db6ede4c405224fabda07312413f87b94f7ca684559966b5f9d28858da0e5962` |
| Frozen counter v4 before and after | `323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2` |
| Pinned generator before and after | `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375` |

The counter's override hash receipts record pristine, mutant, and restored program bytes. After restoring only line 8, `timeout 20 prlimit --as=4000000000 sha256sum .ufo/waves/round-25/controls/v4/K4EmptyArray.py .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py` returned:

```text
db6ede4c405224fabda07312413f87b94f7ca684559966b5f9d28858da0e5962  .ufo/waves/round-25/controls/v4/K4EmptyArray.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
```

Restoration was followed by the same bounded behavioral detector on a fresh seed; its complete output is included below. All counter child processes exited without outer timeout. The frozen oracle terminates and waits for each nested Hyprland process group in its finally block (`count.py:174–189`); no separate service/process was left running by this control. No tools were installed or updated.

## Verbatim receipts

The following blocks preserve each counter's complete stdout and append its actual `exit=`. Every counter stderr was empty. Their order groups the two initial setup failures, their one-time reruns, the two constant-entry measurements, and the restored-byte detector; parallel completion order does not alter the individual receipts.

### empty-array run 1

Exact command:

```sh
timeout --kill-after=10 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py sha256:db6ede4c405224fabda07312413f87b94f7ca684559966b5f9d28858da0e5962
seed=543117314893c994
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
exit=2
```

### empty-array run 2

Exact command:

```sh
timeout --kill-after=10 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py sha256:db6ede4c405224fabda07312413f87b94f7ca684559966b5f9d28858da0e5962
seed=86ada8629515bd1a
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
exit=2
```

### empty-array run 1 exit-2 rerun

Exact command:

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 timeout --kill-after=10 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py sha256:db6ede4c405224fabda07312413f87b94f7ca684559966b5f9d28858da0e5962
seed=96393ceb87c48b9f
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=68 key='N' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=190 extra=0 oracle_binds=190 (UNBIND mask=9 key='TAB' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=64 key='J' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=68 key='I' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vmjnwozi) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vcwrxmee) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vmthgqxp) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vorvidix) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 4) v3_model=agree
    missing mask=12 key="Q" code=0 disp="exec" arg="true gy1ungropa"
    missing mask=76 key="6" code=0 disp="exec" arg="notify-send uhre6tjmw4"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
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
CASE COMMENT-0    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=15 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
    missing mask=4 key="F3" code=0 disp="exec" arg="notify-send u7rwufufmf"
    missing mask=12 key="BACKSPACE" code=0 disp="exec" arg="raw42827n 4xqu"
CASE SYNTH-1      FAIL missing=16 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=2) v3_model=agree
    missing mask=65 key="F13" code=0 disp="exec" arg="h5newe54h hb52"
    missing mask=64 key="KP_9" code=0 disp="exec" arg="k1aa5hszo 15gv"
CASE SYNTH-2      FAIL missing=15 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
    missing mask=64 key="6" code=0 disp="exec" arg="dt81t87om y0u6"
    missing mask=12 key="C" code=0 disp="exec" arg="bv13hbye6 mbum"
CASE SYNTH-3      FAIL missing=15 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=3) v3_model=agree
    missing mask=13 key="F2" code=0 disp="exec" arg="printf zi7xmh61mp"
    missing mask=69 key="I" code=0 disp="exec" arg="notify-send nm8bx0drc8"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=68 key='T' code=0; unbind mask=72 key='RIGHT' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='' code=13; unbind mask=0 key='XF86MonBrightnessDown' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='' code=13; unbind mask=65 key='O' code=0; add togglefloating) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=68 key='E' code=0; unbind mask=0 key='XF86AudioRaiseVolume' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    missing mask=0 key="XF86AudioMute" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume mute-toggl
CASE HARD-0       FAIL missing=20 extra=0 oracle_binds=20 (HARD tree lines=34 binds=20 unbinds=3 vars=4) v3_model=agree
    missing mask=73 key="F10" code=0 disp="fullscreen" arg=""
    missing mask=13 key="F4" code=0 disp="togglespecialworkspace" arg="no83"
CASE HARD-1       FAIL missing=19 extra=0 oracle_binds=19 (HARD tree lines=28 binds=19 unbinds=2 vars=4) v3_model=agree
    missing mask=13 key="KP_9" code=0 disp="moveoutofgroup" arg="uolp"
    missing mask=64 key="PERIOD" code=0 disp="swapwindow" arg="u"
CASE HARD-2       FAIL missing=23 extra=0 oracle_binds=23 (HARD tree lines=28 binds=23 unbinds=1 vars=4) v3_model=agree
    missing mask=69 key="F13" code=0 disp="togglespecialworkspace" arg="owhq"
    missing mask=72 key="mouse:274" code=0 disp="mouse" arg="MoveWindow"
CASE HARD-3       FAIL missing=22 extra=0 oracle_binds=22 (HARD tree lines=30 binds=22 unbinds=2 vars=4) v3_model=agree
    missing mask=0 key="mouse_down" code=0 disp="movetoworkspacesilent" arg="special:ctdo"
    missing mask=73 key="7" code=0 disp="movetoworkspacesilent" arg="e-1"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### empty-array run 2 exit-2 rerun

Exact command:

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 timeout --kill-after=10 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py sha256:db6ede4c405224fabda07312413f87b94f7ca684559966b5f9d28858da0e5962
seed=2aaf5be0d75036e7
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
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=64 key='' keycode=10) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=65 key='B' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=0 key='XF86Calculator' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=190 extra=0 oracle_binds=190 (UNBIND mask=9 key='TAB' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vsjwbqqv) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vcoahzwi) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vtqfswai) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vmdomzpf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 20) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 17) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 5) v3_model=agree
    missing mask=8 key="F4" code=0 disp="exec" arg="logger ryy0cb4bjv"
    missing mask=65 key="F7" code=0 disp="exec" arg="logger 0l7jpsy8bz"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 13) v3_model=agree
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
CASE COMMENT-0    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=11 extra=0 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=2) v3_model=agree
    missing mask=64 key="U" code=0 disp="exec" arg="notify-send kgwxglfiyx"
    missing mask=73 key="F12" code=0 disp="exec" arg="3wkpyd0b4 2xio"
CASE SYNTH-1      FAIL missing=12 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=4 key="P" code=0 disp="exec" arg="b1vjgdd1t ji4a"
    missing mask=9 key="END" code=0 disp="exec" arg="printf nge87jnyur"
CASE SYNTH-2      FAIL missing=12 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=64 key="5" code=0 disp="exec" arg="logger u370a931rk"
    missing mask=77 key="N" code=0 disp="exec" arg="j0ybtio90 ztet"
CASE SYNTH-3      FAIL missing=13 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=13 key="RETURN" code=0 disp="exec" arg="notify-send rtromteaem"
    missing mask=8 key="Y" code=0 disp="exec" arg="true xvjljempay"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=68 key='F' code=0; unbind mask=68 key='H' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='A' code=0; unbind mask=76 key='Z' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='' code=16; unbind mask=0 key='XF86MonBrightnessDown' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=68 key='PERIOD' code=0; unbind mask=8 key='XF86AudioRaiseVolume' code=0; add movetoworkspace) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=18 extra=0 oracle_binds=18 (HARD tree lines=26 binds=18 unbinds=3 vars=4) v3_model=agree
    missing mask=8 key="mouse:274" code=0 disp="fullscreenstate" arg="gyhh"
    missing mask=65 key="mouse:272" code=0 disp="mouse" arg="movewindow"
CASE HARD-1       FAIL missing=21 extra=0 oracle_binds=21 (HARD tree lines=33 binds=21 unbinds=3 vars=4) v3_model=agree
    missing mask=72 key="R" code=0 disp="swapwindow" arg="u"
    missing mask=13 key="" code=135 disp="movefocus" arg="u"
CASE HARD-2       FAIL missing=20 extra=0 oracle_binds=20 (HARD tree lines=27 binds=20 unbinds=1 vars=4) v3_model=agree
    missing mask=13 key="DOWN" code=0 disp="exec" arg="printf 7s3bj0 ead2, texl"
    missing mask=72 key="mouse:274" code=0 disp="mouse" arg="movewindow"
CASE HARD-3       FAIL missing=25 extra=0 oracle_binds=25 (HARD tree lines=33 binds=25 unbinds=3 vars=4) v3_model=agree
    missing mask=65 key="" code=144 disp="bringactivetotop" arg=""
    missing mask=64 key="mouse:274" code=0 disp="mouse" arg="movewindow"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### one-constant-entry run 1

Exact command:

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 timeout --kill-after=10 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py sha256:f1f1928ced8ef49072bfc6be5d302392e6d8855b6faa78490369fc178af3b46a
seed=e1f75dec66ebcb9c
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=1 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE ADD-0        FAIL missing=193 extra=1 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE ADD-1        FAIL missing=193 extra=1 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE ADD-2        FAIL missing=193 extra=1 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE ADD-3        FAIL missing=193 extra=1 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNBIND-0     FAIL missing=191 extra=1 oracle_binds=191 (UNBIND mask=72 key='' keycode=13) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNBIND-1     FAIL missing=191 extra=1 oracle_binds=191 (UNBIND mask=73 key='M' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNBIND-2     FAIL missing=191 extra=1 oracle_binds=191 (UNBIND mask=65 key='W' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNBIND-3     FAIL missing=191 extra=1 oracle_binds=191 (UNBIND mask=64 key='K' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE VARIABLE-0   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vjxdrlfj) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE VARIABLE-1   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vmdjzjsz) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE VARIABLE-2   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vywuktxu) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE VARIABLE-3   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vhvrvwrw) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SOURCE-0     FAIL missing=194 extra=1 oracle_binds=194 (SOURCE new file at root line 5) v3_model=agree
    missing mask=12 key="KP_1" code=0 disp="exec" arg="printf jycoyhe472"
    missing mask=76 key="U" code=0 disp="exec" arg="logger oaueae1hgg"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SOURCE-1     FAIL missing=194 extra=1 oracle_binds=194 (SOURCE new file at root line 9) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SOURCE-2     FAIL missing=194 extra=1 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SOURCE-3     FAIL missing=194 extra=1 oracle_binds=194 (SOURCE new file at root line 18) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE GLOB-0       FAIL missing=193 extra=1 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE GLOB-1       FAIL missing=193 extra=1 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE GLOB-2       FAIL missing=193 extra=1 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE GLOB-3       FAIL missing=193 extra=1 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNSOURCED-0  FAIL missing=192 extra=1 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNSOURCED-1  FAIL missing=192 extra=1 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNSOURCED-2  FAIL missing=192 extra=1 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNSOURCED-3  FAIL missing=192 extra=1 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE COMMENT-0    FAIL missing=193 extra=1 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE COMMENT-1    FAIL missing=193 extra=1 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE COMMENT-2    FAIL missing=193 extra=1 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE COMMENT-3    FAIL missing=193 extra=1 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SYNTH-0      FAIL missing=14 extra=1 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
    missing mask=12 key="F5" code=0 disp="exec" arg="ekwgrfowo 3knc"
    missing mask=12 key="F2" code=0 disp="exec" arg="logger 19wrixjrqk"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SYNTH-1      FAIL missing=16 extra=1 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=3) v3_model=agree
    missing mask=4 key="G" code=0 disp="exec" arg="3ol2oabsm 09zr"
    missing mask=73 key="F18" code=0 disp="exec" arg="logger df2729usef"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SYNTH-2      FAIL missing=11 extra=1 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=2) v3_model=agree
    missing mask=73 key="S" code=0 disp="exec" arg="notify-send f5iflggufb"
    missing mask=8 key="F1" code=0 disp="exec" arg="printf q86luwal50"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SYNTH-3      FAIL missing=16 extra=1 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=2) v3_model=agree
    missing mask=4 key="TAB" code=0 disp="exec" arg="true gqx4h88n6o"
    missing mask=9 key="PRINT" code=0 disp="exec" arg="notify-send nylag32z02"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE REWRITE-0    FAIL missing=192 extra=1 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioMicMute' code=0; unbind mask=8 key='XF86MonBrightnessDown' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE REWRITE-1    FAIL missing=192 extra=1 oracle_binds=192 (REWRITE argswap mask=0 key='PRINT' code=0; unbind mask=65 key='' code=10; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE REWRITE-2    FAIL missing=192 extra=1 oracle_binds=192 (REWRITE argswap mask=73 key='RIGHT' code=0; unbind mask=1 key='XF86MonBrightnessUp' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE REWRITE-3    FAIL missing=192 extra=1 oracle_binds=192 (REWRITE argswap mask=64 key='BACKSPACE' code=0; unbind mask=72 key='RIGHT' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE HARD-0       FAIL missing=23 extra=1 oracle_binds=23 (HARD tree lines=31 binds=23 unbinds=1 vars=4) v3_model=agree
    missing mask=4 key="mouse:272" code=0 disp="mouse" arg="MoveWindow"
    missing mask=1 key="" code=76 disp="togglegroup" arg="m8tg"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE HARD-1       FAIL missing=25 extra=1 oracle_binds=25 (HARD tree lines=32 binds=25 unbinds=1 vars=4) v3_model=agree
    missing mask=64 key="" code=124 disp="movetoworkspacesilent" arg="20"
    missing mask=73 key="F24" code=0 disp="movetoworkspacesilent" arg="e+1"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE HARD-2       FAIL missing=20 extra=1 oracle_binds=20 (HARD tree lines=28 binds=20 unbinds=2 vars=4) v3_model=agree
    missing mask=73 key="M" code=0 disp="moveoutofgroup" arg=""
    missing mask=65 key="SPACE" code=0 disp="workspace" arg="special:ozt8"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE HARD-3       FAIL missing=20 extra=1 oracle_binds=20 (HARD tree lines=27 binds=20 unbinds=2 vars=4) v3_model=agree
    missing mask=72 key="" code=243 disp="movefocus" arg="d"
    missing mask=0 key="" code=117 disp="movecurrentworkspacetomonitor" arg="r"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### one-constant-entry run 2

Exact command:

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 timeout --kill-after=10 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py sha256:f1f1928ced8ef49072bfc6be5d302392e6d8855b6faa78490369fc178af3b46a
seed=5ab71524d3ac00c5
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=1 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE ADD-0        FAIL missing=193 extra=1 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE ADD-1        FAIL missing=193 extra=1 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE ADD-2        FAIL missing=193 extra=1 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE ADD-3        FAIL missing=193 extra=1 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNBIND-0     FAIL missing=191 extra=1 oracle_binds=191 (UNBIND mask=68 key='RIGHT' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNBIND-1     FAIL missing=191 extra=1 oracle_binds=191 (UNBIND mask=0 key='XF86AudioPlay' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNBIND-2     FAIL missing=191 extra=1 oracle_binds=191 (UNBIND mask=65 key='COMMA' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNBIND-3     FAIL missing=191 extra=1 oracle_binds=191 (UNBIND mask=8 key='XF86MonBrightnessUp' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE VARIABLE-0   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vajjazhk) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE VARIABLE-1   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vtuhsogr) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE VARIABLE-2   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vmvebafe) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE VARIABLE-3   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vsdxlbug) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SOURCE-0     FAIL missing=194 extra=1 oracle_binds=194 (SOURCE new file at root line 17) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SOURCE-1     FAIL missing=194 extra=1 oracle_binds=194 (SOURCE new file at root line 18) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SOURCE-2     FAIL missing=194 extra=1 oracle_binds=194 (SOURCE new file at root line 20) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SOURCE-3     FAIL missing=194 extra=1 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE GLOB-0       FAIL missing=193 extra=1 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE GLOB-1       FAIL missing=193 extra=1 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE GLOB-2       FAIL missing=193 extra=1 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE GLOB-3       FAIL missing=193 extra=1 oracle_binds=193 (GLOB new toggles file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNSOURCED-0  FAIL missing=192 extra=1 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNSOURCED-1  FAIL missing=192 extra=1 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNSOURCED-2  FAIL missing=192 extra=1 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE UNSOURCED-3  FAIL missing=192 extra=1 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE COMMENT-0    FAIL missing=193 extra=1 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE COMMENT-1    FAIL missing=193 extra=1 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE COMMENT-2    FAIL missing=193 extra=1 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE COMMENT-3    FAIL missing=193 extra=1 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SYNTH-0      FAIL missing=10 extra=1 oracle_binds=10 (SYNTH tree binds=10 unbound=1 vars=2) v3_model=agree
    missing mask=9 key="T" code=0 disp="exec" arg="wultjh6bs nw6a"
    missing mask=69 key="Q" code=0 disp="exec" arg="notify-send mp4orq7s86"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SYNTH-1      FAIL missing=13 extra=1 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=77 key="INSERT" code=0 disp="exec" arg="printf srcbdwmm4k"
    missing mask=69 key="9" code=0 disp="exec" arg="logger huutsnouei"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SYNTH-2      FAIL missing=12 extra=1 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=69 key="F17" code=0 disp="exec" arg="logger 8uu3xugbhd"
    missing mask=4 key="SPACE" code=0 disp="exec" arg="logger amoijg4e55"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE SYNTH-3      FAIL missing=13 extra=1 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
    missing mask=9 key="Y" code=0 disp="exec" arg="printf by88yafwoh"
    missing mask=5 key="ESCAPE" code=0 disp="exec" arg="notify-send hnpyo3u31o"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE REWRITE-0    FAIL missing=192 extra=1 oracle_binds=192 (REWRITE argswap mask=65 key='RETURN' code=0; unbind mask=0 key='switch:off:Lid Switch' code=0; add workspace) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE REWRITE-1    FAIL missing=192 extra=1 oracle_binds=192 (REWRITE argswap mask=73 key='' code=13; unbind mask=64 key='ESCAPE' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE REWRITE-2    FAIL missing=192 extra=1 oracle_binds=192 (REWRITE argswap mask=73 key='' code=10; unbind mask=65 key='' code=21; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE REWRITE-3    FAIL missing=192 extra=1 oracle_binds=192 (REWRITE argswap mask=72 key='' code=10; unbind mask=8 key='XF86AudioLowerVolume' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE HARD-0       FAIL missing=24 extra=1 oracle_binds=24 (HARD tree lines=34 binds=24 unbinds=3 vars=4) v3_model=agree
    missing mask=72 key="mouse:274" code=0 disp="mouse" arg="movewindow"
    missing mask=0 key="" code=82 disp="exec" arg="uwsm-app -- w6rwh8 q8vn, d4ud"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE HARD-1       FAIL missing=17 extra=1 oracle_binds=17 (HARD tree lines=27 binds=17 unbinds=1 vars=4) v3_model=agree
    missing mask=65 key="8" code=0 disp="sendshortcut" arg="CTRL, RIGHT, activewindow"
    missing mask=65 key="BACKSPACE" code=0 disp="pseudo" arg="rgcb"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE HARD-2       FAIL missing=22 extra=1 oracle_binds=22 (HARD tree lines=30 binds=22 unbinds=0 vars=4) v3_model=agree
    missing mask=13 key="" code=86 disp="fullscreen" arg="m2jx"
    missing mask=68 key="" code=115 disp="pseudo" arg="met8"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
CASE HARD-3       FAIL missing=18 extra=1 oracle_binds=18 (HARD tree lines=27 binds=18 unbinds=2 vars=4) v3_model=agree
    missing mask=65 key="" code=239 disp="fullscreen" arg="tblu"
    missing mask=0 key="mouse:274" code=0 disp="cyclenext" arg="t1vf"
    extra   mask=64 key="RETURN" code=0 disp="exec" arg="true"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### empty-array restored-byte detector

Exact command:

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 timeout --kill-after=10 1200 prlimit --as=4000000000 python3 -I .ufo/waves/round-25/c1/count.py 1ed41fa8 --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py
```

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=1ed41fa8301a4562d125503e5b881ec8eb5a1908 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4EmptyArray.py sha256:db6ede4c405224fabda07312413f87b94f7ca684559966b5f9d28858da0e5962
seed=8256fe04021db750
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=1 key="8" code=0 disp="exec" arg="true 07cij1v2yg"
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=64 key='' keycode=12) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=64 key='mouse_up' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=68 key='L' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=64 key='J' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vamhczgi) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vhspmsaw) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vxfvlevz) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 oracle_binds=193 (VARIABLE $vilqyydg) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 19) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 16) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 17) v3_model=agree
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
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=16 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=3) v3_model=agree
    missing mask=8 key="F21" code=0 disp="exec" arg="zu2xlyuq3 7p74"
    missing mask=8 key="COMMA" code=0 disp="exec" arg="notify-send s8d3g9avp3"
CASE SYNTH-1      FAIL missing=15 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
    missing mask=1 key="Z" code=0 disp="exec" arg="notify-send 14yabr6p66"
    missing mask=64 key="F3" code=0 disp="exec" arg="notify-send c2cid8lx9b"
CASE SYNTH-2      FAIL missing=15 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
    missing mask=76 key="SLASH" code=0 disp="exec" arg="logger 4jclljuj7r"
    missing mask=73 key="PERIOD" code=0 disp="exec" arg="true pccon08rur"
CASE SYNTH-3      FAIL missing=12 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=68 key="F6" code=0 disp="exec" arg="regaz6wml e1ke"
    missing mask=65 key="KP_9" code=0 disp="exec" arg="printf duobiiz4v2"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='' code=17; unbind mask=76 key='B' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='PRINT' code=0; unbind mask=0 key='XF86AudioLowerVolume' code=0; add movetoworkspacesilent) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioMute" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume mute-toggl
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='W' code=0; unbind mask=65 key='BACKSPACE' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=72 key='' code=61; unbind mask=65 key='SLASH' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=19 extra=0 oracle_binds=19 (HARD tree lines=28 binds=19 unbinds=2 vars=4) v3_model=agree
    missing mask=69 key="P" code=0 disp="togglefloating" arg=""
    missing mask=73 key="" code=101 disp="togglespecialworkspace" arg=""
CASE HARD-1       FAIL missing=24 extra=0 oracle_binds=24 (HARD tree lines=31 binds=24 unbinds=2 vars=4) v3_model=agree
    missing mask=68 key="F10" code=0 disp="bringactivetotop" arg="o308"
    missing mask=64 key="mouse:273" code=0 disp="mouse" arg="movewindow"
CASE HARD-2       FAIL missing=20 extra=0 oracle_binds=20 (HARD tree lines=32 binds=20 unbinds=3 vars=4) v3_model=agree
    missing mask=73 key="H" code=0 disp="sendshortcut" arg="CTRL_SHIFT, F21, activewindow"
    missing mask=72 key="mouse:272" code=0 disp="mouse" arg="MoveWindow"
CASE HARD-3       FAIL missing=21 extra=0 oracle_binds=21 (HARD tree lines=28 binds=21 unbinds=1 vars=4) v3_model=agree
    missing mask=73 key="" code=72 disp="movetoworkspace" arg="special:d4bi"
    missing mask=72 key="BACKSPACE" code=0 disp="fullscreen" arg="apzd"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```
