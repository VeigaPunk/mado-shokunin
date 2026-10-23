# K4DoNothing — independent re-measure and receipt attack

## Scope and axes

Reviewed only the committed DO-NOTHING control and its receipt under Attempt 3's frozen PRED-C1 (v4). Axes: C1 operability, capability acquisition, and sourced evidence. This is a counter measurement and scoped criticism, not a canonical Rust judgment, admission, or review of the real resolver.

## Identity and provenance

The receipt at `.ufo/waves/round-25/controls/v4/K4DoNothing.md:11` names sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The working file is exactly 0 bytes and its observed hash matches. The blob at `459dd17f:.ufo/waves/round-25/controls/v4/K4DoNothing.py` also has that hash. The frozen counter and generator match the registration's pins.

Working directory for all shell commands below: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Exact identity commands and outputs:

```sh
timeout 10 sha256sum .ufo/waves/round-25/controls/v4/K4DoNothing.py .ufo/waves/round-25/c1/count.py .ufo/waves/round-25/c1/count-v3.py
```

```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  .ufo/waves/round-25/controls/v4/K4DoNothing.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  .ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  .ufo/waves/round-25/c1/count-v3.py
```

```sh
timeout 10 git show 459dd17f:.ufo/waves/round-25/controls/v4/K4DoNothing.py | timeout 10 sha256sum
```

```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  -
```

```sh
timeout 5 stat --format='%s bytes %n' .ufo/waves/round-25/controls/v4/K4DoNothing.py
```

```text
0 bytes .ufo/waves/round-25/controls/v4/K4DoNothing.py
```

```sh
timeout 5 printenv HYPRLAND_INSTANCE_SIGNATURE
```

```text
efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120
```

The compositor signature was already present; no environment repair was necessary. The old receipt measured this control through `--tool-file` at `1ed41fa8`; the new run below measures the same verified bytes through `--tool-file` at the requested landing revision `459dd17f`. Neither receipt is evidence that the real `tools/mado-binds.py` was measured.

## Independent run — full receipt

Exact command:

```sh
prlimit --as=4000000000 --fsize=67108864 timeout --kill-after=15 1200 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4DoNothing.py
```

The first tool submission, with asynchronous launch requested, was refused before execution: `Background job limit reached (100). Wait for running jobs to finish or cancel one.` The same command was then submitted synchronously and executed once (tool job `bg_1122`). There was one actual counter run, no setup failure, and no scored retry. No seed override was supplied. The fresh seed `a90f13251a8c8930` differs from both old control seeds (`166466dfabe7fd52`, `ecc0ec494af77e9f`).

Counter stdout is preserved verbatim below; `exit=1` records the observed command exit status. Tool timing/status wrappers are not part of counter stdout.

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4DoNothing.py sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
seed=a90f13251a8c8930
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         FAIL stdout is not a JSON array of objects (unperturbed) v3_model=agree
CASE ADD-0        FAIL stdout is not a JSON array of objects (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-1        FAIL stdout is not a JSON array of objects (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE ADD-2        FAIL stdout is not a JSON array of objects (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-3        FAIL stdout is not a JSON array of objects (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE UNBIND-0     FAIL stdout is not a JSON array of objects (UNBIND mask=68 key='S' keycode=0) v3_model=agree
CASE UNBIND-1     FAIL stdout is not a JSON array of objects (UNBIND mask=0 key='XF86KbdBrightnessDown' keycode=0) v3_model=agree
CASE UNBIND-2     FAIL stdout is not a JSON array of objects (UNBIND mask=12 key='TAB' keycode=0) v3_model=agree
CASE UNBIND-3     FAIL stdout is not a JSON array of objects (UNBIND mask=72 key='S' keycode=0) v3_model=agree
CASE VARIABLE-0   FAIL stdout is not a JSON array of objects (VARIABLE $vgifepsr) v3_model=agree
CASE VARIABLE-1   FAIL stdout is not a JSON array of objects (VARIABLE $vecuflyt) v3_model=agree
CASE VARIABLE-2   FAIL stdout is not a JSON array of objects (VARIABLE $vdkbkjnx) v3_model=agree
CASE VARIABLE-3   FAIL stdout is not a JSON array of objects (VARIABLE $vzwaxcul) v3_model=agree
CASE SOURCE-0     FAIL stdout is not a JSON array of objects (SOURCE new file at root line 17) v3_model=agree
CASE SOURCE-1     FAIL stdout is not a JSON array of objects (SOURCE new file at root line 10) v3_model=agree
CASE SOURCE-2     FAIL stdout is not a JSON array of objects (SOURCE new file at root line 19) v3_model=agree
CASE SOURCE-3     FAIL stdout is not a JSON array of objects (SOURCE new file at root line 13) v3_model=agree
CASE GLOB-0       FAIL stdout is not a JSON array of objects (GLOB new toggles file) v3_model=agree
CASE GLOB-1       FAIL stdout is not a JSON array of objects (GLOB new toggles file) v3_model=agree
CASE GLOB-2       FAIL stdout is not a JSON array of objects (GLOB new toggles file) v3_model=agree
CASE GLOB-3       FAIL stdout is not a JSON array of objects (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  FAIL stdout is not a JSON array of objects (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  FAIL stdout is not a JSON array of objects (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  FAIL stdout is not a JSON array of objects (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  FAIL stdout is not a JSON array of objects (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    FAIL stdout is not a JSON array of objects (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-1    FAIL stdout is not a JSON array of objects (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE COMMENT-2    FAIL stdout is not a JSON array of objects (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE COMMENT-3    FAIL stdout is not a JSON array of objects (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE SYNTH-0      FAIL stdout is not a JSON array of objects (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
CASE SYNTH-1      FAIL stdout is not a JSON array of objects (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      FAIL stdout is not a JSON array of objects (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      FAIL stdout is not a JSON array of objects (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
CASE REWRITE-0    FAIL stdout is not a JSON array of objects (REWRITE argswap mask=0 key='XF86Calculator' code=0; unbind mask=0 key='XF86KbdLightOnOff' code=0; add resizeactive) v3_model=agree
CASE REWRITE-1    FAIL stdout is not a JSON array of objects (REWRITE argswap mask=68 key='W' code=0; unbind mask=64 key='G' code=0; add movecurrentworkspacetomonitor) v3_model=agree
CASE REWRITE-2    FAIL stdout is not a JSON array of objects (REWRITE argswap mask=0 key='XF86PowerOff' code=0; unbind mask=64 key='mouse_up' code=0; add exec) v3_model=agree
CASE REWRITE-3    FAIL stdout is not a JSON array of objects (REWRITE argswap mask=65 key='' code=17; unbind mask=73 key='F' code=0; add movetoworkspacesilent) v3_model=agree
CASE HARD-0       FAIL stdout is not a JSON array of objects (HARD tree lines=33 binds=20 unbinds=3 vars=4) v3_model=agree
CASE HARD-1       FAIL stdout is not a JSON array of objects (HARD tree lines=29 binds=23 unbinds=1 vars=4) v3_model=agree
CASE HARD-2       FAIL stdout is not a JSON array of objects (HARD tree lines=26 binds=15 unbinds=3 vars=4) v3_model=agree
CASE HARD-3       FAIL stdout is not a JSON array of objects (HARD tree lines=27 binds=15 unbinds=1 vars=4) v3_model=agree
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=0/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Attack: strongest allowed shape and counterexample

**Counterexample tested:** a real, valid Python file that successfully does nothing. All 41 cases reject its empty stdout before bind-table comparison. Even BASE is rejected although the oracle matches the 192-bind live capture. Thus successful termination is not mistaken for C1 operability.

**Does it implement its claimed shape?** Yes. Its zero-byte content is the literal empty-file alternative, not a missing-tool substitute or a partial parser. The historical shape description in `a3w1-spec.json:9` and the receipt's description agree: empty file, or exit 0 without output. That artifact is evidence of what the receipt claims, not authority to change this assignment or the predicate.

**Strongest same-shape challenge:** replace the empty file with explicit successful termination and still emit nothing. [INFERENCE] This cannot improve the score: `count-v3.py:735–742` rejects a nonzero process exit, then calls `json.loads(p.stdout)`; both permitted alternatives have exit 0 and empty stdout. Empty stdout always takes the same parse-error return. `count.py:281–284` then continues without incrementing the pass count, before consulting the expected table. This conclusion is independent of the case tree and seed. The fresh run's identical parse rejection on all 41 cases exercises that path for the committed empty-file alternative.

No stronger version was written or scored: the alternative is an observational tie, not a strengthening. Emitting `[]`, a constant object, or a table would violate the no-output shape and cross into separately assigned controls. The explicit-exit alternative was not run, and no empirical result is claimed for it.

**Evidence and limits:** the re-measure agrees with the receipt's 0/41, embed_hits=0, exit=1. The live hash and 79-file snapshot digest also match the old receipt. The new `ORACLE_CHECK` reports no BASE/live difference. `V3_MODEL_AGREE 41/41` is diagnostic only; it neither rescues the control nor replaces the Hyprland oracle. The empty file's embed_hits=0 is vacuous evidence about embedding, not evidence of acquired capability. This negative control says nothing about nonempty shortcut parsers, real-tool correctness, C2, or overall oracle completeness; treating it as saturation of those questions would be unsupported.

**Impacted axes:** C1 operability fails because no JSON table is produced. Capability acquisition is absent by construction. Sourced evidence supports this narrow negative-control result through pinned hashes, explicit override identity, a fresh seed, and the Hyprland-backed receipt; it does not transfer that result to the claimed resolver.

**Smallest safe correction:** none to this control, receipt, or frozen counter is supported by this review. Preserve the silent shape and rejection; do not turn silent success into a valid bind table or inflate the narrow rejection into a broader coverage claim. No fixable implementation defect or useful same-shape tradeoff was demonstrated. Canonical judgment remains outside this review.

## Safety and changes

Only this assigned report was written in the lane. The control, resolver, counter, generator, configs, and git/jj state were not edited. No stronger scratch file was created. The actual counter command had a 1,200-second timeout, 15-second kill-after, 4,000,000,000-byte address-space cap, and 67,108,864-byte per-file cap; it completed normally with counter exit 1 in 77.00 seconds. `-B` prevented imported lane bytecode caches. The frozen counter's host-wide six-slot lock and per-oracle process-group termination (`count.py:100–116,174–189`) were left intact. No independent nested compositor, live-compositor write command, service/package change, tool install/upgrade, build, linter, formatter, or additional test was invoked.

REMEASURE K4DoNothing: 0/41 (receipt said 0/41); strengthened: not attempted — not met
