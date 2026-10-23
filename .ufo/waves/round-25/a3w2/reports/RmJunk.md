# RmJunk — independent re-measure and receipt attack

REMEASURE K4Junk: 0/41 (receipt said 0/41); strengthened: 0/41 — not met

## Scope, axes and provenance

Read registration.md, Attempt 3 / PRED-C1 (v4), the committed control and its receipt. Axes: exact sourced 18-field bind-table operability, fidelity to the JUNK shape, byte/measurement provenance, and host non-interference. No canonical judgment, admission or integration was invoked.

The working file, the blob at `459dd17f`, the receipt's named hash, and the re-measurement's tool hash all agree:

`0dd447855262b6ad6652a18e86928614994c8f296b064a865acd8890068175b6`

The frozen counter hash also agrees with the registration: `323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2`. The counter receipts identify the pinned generator hash and resolve the requested revision to `459dd17f8fd60df85b25f15e69376a9765e267d3`. Neither override is represented as a measurement of the claimed `tools/mado-binds.py`.

Exactly one completed fresh-seed measurement was made of each program, with no `--seed`. The original used seed `5b2234cf981aff60`, distinct from both old receipt seeds; the variant used `360233ce39a626c0`. Both exited 1 with an actual predicate line, not an environment failure or an unmeasured crash. Both had `ORACLE_CHECK base_vs_live missing=0 extra=0` and `V3_MODEL_AGREE 41/41`; the latter remains diagnostic only.

## Counterexample, shape fidelity and smallest safe correction

**The original implements the assigned shape.** Its only config read is the binary root file; it counts literal `line.startswith(b"bind")`, emits exactly that many objects with all 18 field names, and does not parse any fields. It neither trims indentation nor follows sources, expands variables, processes comments/unbinds, reads case identities, embeds a captured table, or invokes another process. Its content-free keys, args and flags use `SystemRandom`. The original shape is also recorded in `a3w1-spec.json:17-19`.

**Strongest counterexample: output cardinality already prevents success on BASE.** The new measurement gives `missing=192 extra=0` on BASE and `missing=194 extra=0` on every SOURCE case. The root-only count is zero, so any program obeying this exact count rule must print `[]` on those trees regardless of how well it invents individual rows. This is a shape-bound information deficit on this snapshot, not a claim that other shortcut shapes are saturated. Following sources to repair it would cross the assigned shape boundary.

Nonempty output was also measured: original SYNTH-0 has `missing=14 extra=8`, and HARD-0 has `missing=16 extra=16`. HARD-0 is especially useful: equal row counts did not rescue the invented table. The control was rejected for content as well as cardinality, not merely for returning empty JSON everywhere.

**A fixable weakness in the original sampler is not a counter defect.** Independently random flags can combine repeat with release/longPress or mouse with locked/release/repeat, while descriptions are nonempty even when `has_description` is false and mouse rows still say dispatcher `exec`. The diagnostic model explicitly rejects these flag combinations and distinguishes mouse dispatch/description defaults (`count-v3.py:468-505`). This is evidence for improving the invented-row sampler, not authority replacing the Hyprland oracle.

I wrote the permitted scratch variant `/fast/scratch/hyaku/mado-r25a3/rm/K4Junk-strong.py` (2,407 bytes; measured sha256 `7d80b88ee137c26617e6f892878e7d86ab5a2919551abb296d2781c17831f515`). It preserves the identical root-only count and no-field-parsing rule. It samples compatible release/repeat/longPress states, coherent mouse dispatch rows, empty descriptions when undescribed, and either key names or numeric-keycode representation; exec args remain randomly empty or invented hex. No tree resolution, live-table capture, case detection or subprocess was added.

**The attempted strengthening is not a no-harm improvement.** It still passes 0/41 and additionally records `EMBED_HIT 'resizewindow'`, hence `embed_hits=1` versus the original's zero. The literal was a generic sampled mouse argument, not a copied table; nevertheless it is exactly a live arg string of length 12, so it violates the frozen textual predicate (`count.py:233-240,295-298`). That provenance distinction does not waive the failure. The measured variant is preserved unchanged as evidence, not integrated or described as Pareto-superior.

Impacted axes: source-graph coverage and exact field semantics remain absent; original provenance is verified; the variant improves internal row coherence but regresses the embed axis. Smallest safe correction: retain the original 0/41 receipt, qualify the variant as an attempted sampler strengthening with its observed regression, and retain the frozen exact predicate. Omitting the literal `resizewindow` would address that particular embed hit, but was not applied or scored and would not repair the unavoidable BASE cardinality failure. Replacing the root-only count with real source/field resolution would be a different shape, not a correction to this control. Neither result supports accepting C1 or claiming global saturation.

## Exact commands and isolation

All commands ran with cwd `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Prerequisite/provenance commands:

```sh
timeout 10 sha256sum .ufo/waves/round-25/controls/v4/K4Junk.py .ufo/waves/round-25/c1/count.py
timeout 10 prlimit --as=4000000000 printenv HYPRLAND_INSTANCE_SIGNATURE WAYLAND_DISPLAY XDG_RUNTIME_DIR HOME
timeout 10 prlimit --as=4000000000 --core=0 git show 459dd17f:.ufo/waves/round-25/controls/v4/K4Junk.py | timeout 10 sha256sum
```

Their outputs, respectively:

```text
0dd447855262b6ad6652a18e86928614994c8f296b064a865acd8890068175b6  .ufo/waves/round-25/controls/v4/K4Junk.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
```

```text
efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120
wayland-1
/run/user/1000
/home/vgpnk
```

```text
0dd447855262b6ad6652a18e86928614994c8f296b064a865acd8890068175b6  -
```

Measurement commands:

```sh
timeout 1200 prlimit --as=4000000000 --core=0 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Junk.py
timeout 1200 prlimit --as=4000000000 --core=0 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /fast/scratch/hyaku/mado-r25a3/rm/K4Junk-strong.py
```

`prlimit` caps inherited address space at 4,000,000,000 bytes and disables core dumps; `-B` avoids lane bytecode writes. The required capture environment was already present and was not changed. An initial asynchronous submission of the first argv was refused by the tool with `Background job limit reached (100). Wait for running jobs to finish or cancel one.` It produced no counter receipt or seed; the actual first measurement was then submitted synchronously. There was no score-seeking rerun. Measured wall times were 46.22 s and 19.84 s, both exit 1.

Only the prescribed counter started nested Hyprland instances, using its host-wide six-slot locks. Both commands returned normally, exercising the counter's oracle process-group cleanup and temporary-tree finally blocks (`count.py:174-189,299-300`). No independent nested instance, service or long-lived process was started. No live compositor write verb, git/jj write command, config change, package/tool installation or update occurred. The only direct writes were this report and the named scratch variant. No builds, linters, formatters or other verification runs were performed.

## Original control re-measurement — counter stdout verbatim, then exit

The timing/status footer from the command tool is not counter stdout. Its observed status is rendered below as `exit=1`.

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4Junk.py sha256:0dd447855262b6ad6652a18e86928614994c8f296b064a865acd8890068175b6
seed=5b2234cf981aff60
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=65 key='N' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=64 key='' keycode=20) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=65 key='' keycode=10) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=72 key='TAB' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $votcvbqt) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=226 key="R" code=0 disp="exec" arg="987092b176c26a072ed935c7ce526fa7"
CASE VARIABLE-1   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vjkuqcmi) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=214 key="N" code=0 disp="exec" arg="f46c8e3998aaa2483f16dfc5a86d7074"
CASE VARIABLE-2   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vjuvtwqy) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=47 key="7" code=0 disp="exec" arg="f67a86a19f66d7388532ff069868b656"
CASE VARIABLE-3   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vumcvaad) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=154 key="T" code=0 disp="exec" arg="69b1e03dd151055002873f214dc48ff4"
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 16) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 7) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 16) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
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
CASE COMMENT-0    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=14 extra=8 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
    missing mask=72 key="BACKSPACE" code=0 disp="exec" arg="925649x2b ry4j"
    missing mask=77 key="L" code=0 disp="exec" arg="c00gjxggj 6pvj"
    extra   mask=235 key="T" code=0 disp="exec" arg="15c15c8090dda697e6a5ebcb6a7761a2"
    extra   mask=73 key="E" code=0 disp="exec" arg="a58fbef0661eba566d27eb88703150c8"
CASE SYNTH-1      FAIL missing=12 extra=5 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
    missing mask=12 key="F10" code=0 disp="exec" arg="logger uqwy16jrg4"
    missing mask=76 key="F24" code=0 disp="exec" arg="notify-send pxwreypay0"
    extra   mask=38 key="3" code=0 disp="exec" arg="801ffd4470be1459a2d1bd44039c8b5f"
    extra   mask=14 key="H" code=0 disp="exec" arg="96942c98bb296361fa53187a42146abb"
CASE SYNTH-2      FAIL missing=12 extra=6 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
    missing mask=5 key="I" code=0 disp="exec" arg="uza0vu6lv q0pc"
    missing mask=72 key="F20" code=0 disp="exec" arg="true doxjekz81q"
    extra   mask=242 key="N" code=0 disp="exec" arg="9978ca802e23ab239461eae4d9f08da4"
    extra   mask=166 key="S" code=0 disp="exec" arg="d9567fb59ca33b889c8ca540ad1e8639"
CASE SYNTH-3      FAIL missing=13 extra=6 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=72 key="U" code=0 disp="exec" arg="tckoz6z5y nui5"
    missing mask=4 key="F1" code=0 disp="exec" arg="notify-send y6ffx5qvck"
    extra   mask=250 key="O" code=0 disp="exec" arg="99f83c4280288532df81f22860763e3c"
    extra   mask=173 key="N" code=0 disp="exec" arg="d9f06bb1af4d08ed233c70de7d043625"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='TAB' code=0; unbind mask=64 key='G' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='' code=17; unbind mask=65 key='' code=12; add movecurrentworkspacetomonitor) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='X' code=0; unbind mask=72 key='mouse_down' code=0; add changegroupactive) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='switch:on:Lid Switch' code=0; unbind mask=69 key='R' code=0; add togglefloating) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE HARD-0       FAIL missing=16 extra=16 oracle_binds=16 (HARD tree lines=29 binds=16 unbinds=2 vars=4) v3_model=agree
    missing mask=73 key="" code=135 disp="changegroupactive" arg="ohk7"
    missing mask=73 key="" code=219 disp="fullscreen" arg="mf3z"
    extra   mask=47 key="T" code=0 disp="exec" arg="6cbffde138a4540485abdbb85ba3bfb1"
    extra   mask=164 key="I" code=0 disp="exec" arg="d14c7ba65c06f36aca96c4e32b2bc76b"
CASE HARD-1       FAIL missing=23 extra=19 oracle_binds=23 (HARD tree lines=32 binds=23 unbinds=1 vars=4) v3_model=agree
    missing mask=1 key="Y" code=0 disp="togglespecialworkspace" arg=""
    missing mask=72 key="" code=224 disp="movetoworkspace" arg="7"
    extra   mask=22 key="5" code=0 disp="exec" arg="8b4debccaf18f3ad6e18775809f85cee"
    extra   mask=211 key="Q" code=0 disp="exec" arg="d6ee8e50fbc7272949274b0732b97487"
CASE HARD-2       FAIL missing=16 extra=14 oracle_binds=16 (HARD tree lines=28 binds=16 unbinds=1 vars=4) v3_model=agree
    missing mask=4 key="" code=33 disp="togglespecialworkspace" arg=""
    missing mask=72 key="" code=179 disp="movetoworkspacesilent" arg="17"
    extra   mask=78 key="Z" code=0 disp="exec" arg="fbccf2d25fff88cbd8129df4fef61435"
    extra   mask=203 key="Q" code=0 disp="exec" arg="e333bbc3c3d313243e048f7d2e320786"
CASE HARD-3       FAIL missing=21 extra=15 oracle_binds=21 (HARD tree lines=28 binds=21 unbinds=2 vars=4) v3_model=agree
    missing mask=73 key="mouse_up" code=0 disp="cyclenext" arg=""
    missing mask=4 key="N" code=0 disp="togglefloating" arg="tb2i"
    extra   mask=138 key="B" code=0 disp="exec" arg="84024c580eb031c3d8f80e2c0dce5a64"
    extra   mask=7 key="5" code=0 disp="exec" arg="6f435f7ab04b1c98ec6bca81966cb0b9"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Attempted strengthened sampler — counter stdout verbatim, then exit

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/rm/K4Junk-strong.py sha256:7d80b88ee137c26617e6f892878e7d86ab5a2919551abb296d2781c17831f515
seed=360233ce39a626c0
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
EMBED_HIT 'resizewindow'
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL missing=192 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=64 key='P' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=73 key='DOWN' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=0 key='XF86AudioMute' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 oracle_binds=191 (UNBIND mask=68 key='PRINT' keycode=0) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vvdedfre) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=172 key="mouse:272" code=0 disp="mouse" arg="movewindow"
CASE VARIABLE-1   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vqnuwcin) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=29 key="mouse:274" code=0 disp="mouse" arg="movewindow"
CASE VARIABLE-2   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vcuutgho) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=190 key="mouse:274" code=0 disp="mouse" arg="resizewindow"
CASE VARIABLE-3   FAIL missing=193 extra=1 oracle_binds=193 (VARIABLE $vidgjgev) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=69 key="G" code=0 disp="exec" arg=""
CASE SOURCE-0     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 5) v3_model=agree
    missing mask=1 key="SLASH" code=0 disp="exec" arg="printf wxiu0ja416"
    missing mask=5 key="RIGHT" code=0 disp="exec" arg="logger q9iuc0gehi"
CASE SOURCE-1     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 18) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 oracle_binds=194 (SOURCE new file at root line 11) v3_model=agree
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
CASE COMMENT-0    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=13 extra=7 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
    missing mask=72 key="5" code=0 disp="exec" arg="printf s1xyowbdln"
    missing mask=68 key="F7" code=0 disp="exec" arg="logger mgsl8g3v9m"
    extra   mask=6 key="" code=22 disp="exec" arg=""
    extra   mask=42 key="mouse:273" code=0 disp="mouse" arg="movewindow"
CASE SYNTH-1      FAIL missing=12 extra=6 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=2) v3_model=agree
    missing mask=4 key="PERIOD" code=0 disp="exec" arg="true wwcpn0owri"
    missing mask=4 key="LEFT" code=0 disp="exec" arg="true lb96kxogsz"
    extra   mask=0 key="mouse:272" code=0 disp="mouse" arg="resizewindow"
    extra   mask=123 key="mouse:273" code=0 disp="mouse" arg="movewindow"
CASE SYNTH-2      FAIL missing=11 extra=7 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=2) v3_model=agree
    missing mask=8 key="F8" code=0 disp="exec" arg="notify-send tqiw0xt231"
    missing mask=77 key="2" code=0 disp="exec" arg="0z0nils4q hpxh"
    extra   mask=92 key="P" code=0 disp="exec" arg=""
    extra   mask=11 key="" code=224 disp="exec" arg="79569ae23d292636f2050cb45bc70e29"
CASE SYNTH-3      FAIL missing=13 extra=8 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
    missing mask=9 key="F14" code=0 disp="exec" arg="k68lv1aie yxj7"
    missing mask=9 key="SPACE" code=0 disp="exec" arg="x7anjyo6j n42q"
    extra   mask=64 key="mouse:273" code=0 disp="mouse" arg="movewindow"
    extra   mask=109 key="mouse:272" code=0 disp="mouse" arg="resizewindow"
CASE REWRITE-0    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioPrev' code=0; unbind mask=1 key='XF86MonBrightnessUp' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-1    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='' code=11; unbind mask=64 key='S' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-2    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='P' code=0; unbind mask=68 key='H' code=0; add movetoworkspace) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE REWRITE-3    FAIL missing=192 extra=0 oracle_binds=192 (REWRITE argswap mask=69 key='SPACE' code=0; unbind mask=0 key='XF86AudioLowerVolume' code=0; add exec) v3_model=agree
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioMute" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume mute-toggl
CASE HARD-0       FAIL missing=21 extra=17 oracle_binds=21 (HARD tree lines=34 binds=21 unbinds=3 vars=4) v3_model=agree
    missing mask=72 key="mouse:272" code=0 disp="mouse" arg="resizewindow"
    missing mask=64 key="" code=159 disp="togglegroup" arg="0g7j"
    extra   mask=170 key="" code=131 disp="exec" arg="efe0f30e3014144cb1ecdfe5c7945d60"
    extra   mask=239 key="" code=102 disp="exec" arg="9c2bb025bbda89898706f00bac890fa7"
CASE HARD-1       FAIL missing=21 extra=15 oracle_binds=21 (HARD tree lines=32 binds=21 unbinds=2 vars=4) v3_model=agree
    missing mask=69 key="" code=215 disp="focusmonitor" arg="l"
    missing mask=8 key="A" code=0 disp="swapwindow" arg="r"
    extra   mask=71 key="mouse:272" code=0 disp="mouse" arg="movewindow"
    extra   mask=160 key="mouse:272" code=0 disp="mouse" arg="movewindow"
CASE HARD-2       FAIL missing=21 extra=13 oracle_binds=21 (HARD tree lines=27 binds=21 unbinds=2 vars=4) v3_model=agree
    missing mask=1 key="" code=133 disp="movetoworkspace" arg="e-1"
    missing mask=73 key="MINUS" code=0 disp="resizeactive" arg="9 2"
    extra   mask=218 key="mouse:274" code=0 disp="mouse" arg="movewindow"
    extra   mask=211 key="" code=162 disp="exec" arg=""
CASE HARD-3       FAIL missing=21 extra=16 oracle_binds=21 (HARD tree lines=28 binds=21 unbinds=3 vars=4) v3_model=agree
    missing mask=64 key="2" code=0 disp="changegroupactive" arg="uuqq"
    missing mask=72 key="F1" code=0 disp="fullscreenstate" arg=""
    extra   mask=72 key="G" code=0 disp="exec" arg=""
    extra   mask=89 key="" code=65 disp="exec" arg="041eb4ebd71ba78c4455eae7062adfd6"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=1 verdict=TARGET_MISSED
exit=1
```
