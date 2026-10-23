# K4LabelKeyed — independent re-measure and receipt attack

REMEASURE K4LabelKeyed: 37/41 (receipt said 37/41); strengthened: 37/41 — not met

## Scope and identity

Axes: operability / capability acquisition, sourced provenance, calibration, and host safety. This is a scoped critic report, not a canonical Rust judgment or admission.

Read registration Attempt 3, including PRED-C1 (v4) and its control/implementation boundary, the committed control and receipt, and the relevant counter/generator sections. The original receipt names sha256 `b43c4d700972ea00c8baa9b7e09496bb44f031db9e27edf41d223bb7a09dd6b9` for `controls/v4/K4LabelKeyed.py`. The on-disk file **matches exactly**. Counter and generator hashes also match their frozen pins.

Exact hash command:

```sh
timeout 15 prlimit --as=4000000000 sha256sum /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4LabelKeyed.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count.py /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count-v3.py
```

Verbatim output, with observed exit:

```text
b43c4d700972ea00c8baa9b7e09496bb44f031db9e27edf41d223bb7a09dd6b9  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4LabelKeyed.py
323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count.py
8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375  /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/c1/count-v3.py
exit=0
```

## Receipt attack and same-shape strengthening

**The program does implement the disclosed shortcut shape.** Inspection of the original control shows literal category extraction from `/proc/self/mountinfo` at lines 60–68, structural fallback at 71–89, an encoded table loaded at 22–23, unconditional cached BASE/UNSOURCED answers at 194–198, and only two fixed synthetic source-marker expansions at 182–188. It is not a general source-tree resolver. The mount-label recovery probe in the earlier receipt was not independently repeated here; the fresh measurements below exercise the complete control, not an isolated label-channel probe.

**The earlier zero-row HARD branch is not evidence of maximal strength.** `answer()` routes HARD through `synthetic()`, whose `easy_row()` call leaves `copied_vocab=False`. That requires the easy generator's exact exec-argument template (or its v/s-variable template); HARD uses a different argument vocabulary and h-variable names (`count-v3.py:566–569,598–647`). The original therefore leaves a narrow, same-shape extension unused. Its receipt discloses that limitation; the problem would be treating the result as proof that every fixture-keyed shortcut has been exhausted.

I created `/fast/scratch/hyaku/mado-r25a3/rm/K4LabelKeyed-strong.py` from the original bytes and changed only its description, the synthetic fixture routine, and the HARD call. The strengthened file:

- Keeps all original non-HARD branches and the encoded cache.
- Lets HARD use the existing easy-row decoder with cached dispatcher vocabulary instead of the easy exec-argument restriction.
- Rejects every HARD line containing `$`, rather than adding h-variable expansion.
- Conservatively vetoes every literal key mentioned by an unbind in the four fixed fixture files, without resolving aliases, modifier identity, or unbind order. This can omit valid rows; it is intentionally not a correct general unbind implementation.
- Still uses only the original two literal source markers and fixed `a.conf`, `d/x.conf`, `d/y.conf` filenames. It adds no general source/glob walk, hard modifier aliases, keycodes, mouse semantics, or hard flag model. No v3 per-line function was imported or copied.

This broadens the attempted literal subset without crossing the registered boundary, but **did not improve the observed result**: 37/41 again, and zero recovered HARD rows on its fresh seed. In the strengthened receipt the missing counts equal the full oracle bind counts (18, 22, 16, 20), with no extras. It is a strengthening attempt, not a demonstrated capability gain or a maximality proof. The file was not amended or re-scored after that result. Its measured sha256 is `773185e49f0e67d239809c8f62ea6d692f3f4b552fa966d89ae4ba6aefecc030`.

**Strongest local counterexample:** all four fresh HARD trees defeated both measurements. The strengthened HARD-3 tree alone needs 20 rows; it returned none, including no row for keycode 126 / `resizeactive` / `-26 -32`. Category identity cannot supply that fresh table. BASE through REWRITE all pass in both runs, so those 37 passes remain compatible with cached answers and fixture-specific decoding rather than general config interpretation.

## Impacted axes and smallest safe correction

- **Operability / capability acquisition:** the original 37/41 reproduces independently. Neither the original nor the same-shape extension meets 41/41. Retain the HARD kill arm; do not turn partial coverage into a resolver claim.
- **Sourced provenance:** both programs explicitly retain the encoded live table, while both receipts say `embed_hits=0`. That number is only the counter's literal-substring audit (`count.py:233–240`), not proof of source-derived answers or absence of embedded data. Cached BASE/UNSOURCED answers have a different authority from the config tree.
- **Calibration:** the earlier numeric receipt is confirmed. The fixable interpretation defect is any claim of saturation/maximality from an intentionally narrow HARD branch; the fresh extension also failed, but does not establish universal impossibility. Report the observed miss and the scope of the plaintext audit precisely.
- **Boundary/tradeoff:** adding the full hard-line model to chase 41/41 is not an eligible control repair under registration lines 204–210. It would change the work being measured into an implementation path, even if presented as a stronger control. That classification and any scored-axis decision belong to the canonical judge.
- **Smallest safe correction:** retain the frozen counter, preserve these misses, and keep the capability/provenance claims bounded to what the receipts show. Opaque mount-source names would address the disclosed literal identity leak in a future counter, not in this frozen run; layout fingerprints would remain a separate concern.

## Execution conditions

Working directory for both scored commands: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Each command used a fresh default seed, the specified revision `459dd17f`, a 1,200-second timeout, and a 4,000,000,000-byte address-space cap. `-B` prevents importing the lane generator from writing `__pycache__`; the supplied compositor signature and `WAYLAND_DISPLAY` route the read-only capture. Both commands completed with exit 1 and a PRED-C1 line. No additional stderr appeared in either tool result.

An initial asynchronous launch request for the original command returned only `Background job limit reached (100). Wait for running jobs to finish or cancel one.` No receipt or job ID was returned. The synchronous original measurement below is the sole completed original measurement in this assignment; no scored result was retried. The stronger version was scored once.

No lane source, original control, counter, registration, receipt, live configuration, package, service, or compositor setting was changed. The only lane write is this report; the only implementation output is the authorized scratch file. No git/jj write command, subagent, or other judgment runtime was invoked. Hyprland instances were started only by the frozen counter, whose `finally` path terminates their process groups. Both counter command invocations returned. No tools were installed or updated.

## Original control — exact command and complete receipt

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 timeout 1200 prlimit --as=4000000000 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4LabelKeyed.py
```

Verbatim counter output, with observed exit:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-25/controls/v4/K4LabelKeyed.py sha256:b43c4d700972ea00c8baa9b7e09496bb44f031db9e27edf41d223bb7a09dd6b9
seed=2d81af4a315fb44d
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='RIGHT' keycode=0) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=0 key='XF86TouchpadOn' keycode=0) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=0 key='switch:off:Lid Switch' keycode=0) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=69 key='R' keycode=0) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vyetfoeb) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vhswhsto) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vidgdgud) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vemmywje) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 12) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 23) v3_model=agree
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
CASE COMMENT-1    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=17 (SYNTH tree binds=17 unbound=1 vars=3) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
CASE REWRITE-0    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=72 key='S' code=0; unbind mask=68 key='W' code=0; add workspace) v3_model=agree
CASE REWRITE-1    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='P' code=0; unbind mask=65 key='' code=21; add exec) v3_model=agree
CASE REWRITE-2    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=68 key='LEFT' code=0; unbind mask=1 key='XF86MonBrightnessUp' code=0; add exec) v3_model=agree
CASE REWRITE-3    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=1 key='XF86MonBrightnessDown' code=0; unbind mask=68 key='E' code=0; add movetoworkspace) v3_model=agree
CASE HARD-0       FAIL missing=16 extra=0 oracle_binds=16 (HARD tree lines=30 binds=16 unbinds=3 vars=4) v3_model=agree
    missing mask=1 key="F3" code=0 disp="cyclenext" arg=""
    missing mask=0 key="DELETE" code=0 disp="movetoworkspacesilent" arg="e-1"
CASE HARD-1       FAIL missing=17 extra=0 oracle_binds=17 (HARD tree lines=32 binds=17 unbinds=1 vars=4) v3_model=agree
    missing mask=76 key="KP_5" code=0 disp="movefocus" arg="u"
    missing mask=72 key="mouse:274" code=0 disp="mouse" arg="movewindow"
CASE HARD-2       FAIL missing=18 extra=0 oracle_binds=18 (HARD tree lines=25 binds=18 unbinds=2 vars=4) v3_model=agree
    missing mask=13 key="5" code=0 disp="bringactivetotop" arg="xzbv"
    missing mask=1 key="" code=187 disp="togglegroup" arg=""
CASE HARD-3       FAIL missing=22 extra=0 oracle_binds=22 (HARD tree lines=31 binds=22 unbinds=3 vars=4) v3_model=agree
    missing mask=64 key="F13" code=0 disp="layoutmsg" arg="3k1s"
    missing mask=1 key="" code=92 disp="moveintogroup" arg="d"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=37/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Strengthened control — exact command and complete receipt

```sh
env HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 WAYLAND_DISPLAY=wayland-1 timeout 1200 prlimit --as=4000000000 python3 -I -B .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /fast/scratch/hyaku/mado-r25a3/rm/K4LabelKeyed-strong.py
```

Verbatim counter output, with observed exit:

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/rm/K4LabelKeyed-strong.py sha256:773185e49f0e67d239809c8f62ea6d692f3f4b552fa966d89ae4ba6aefecc030
seed=1014adc9d0c61ba0
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=8 key='XF86AudioLowerVolume' keycode=0) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='RETURN' keycode=0) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=68 key='V' keycode=0) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=72 key='RETURN' keycode=0) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vfowtcyt) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vfsxtfrk) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vnbdzvfe) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vwzdkjpr) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 11) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 9) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 13) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE COMMENT-1    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='L' code=0; unbind mask=65 key='SPACE' code=0; add exec) v3_model=agree
CASE REWRITE-1    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86TouchpadOn' code=0; unbind mask=64 key='' code=21; add exec) v3_model=agree
CASE REWRITE-2    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='X' code=0; unbind mask=0 key='XF86AudioLowerVolume' code=0; add exec) v3_model=agree
CASE REWRITE-3    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='A' code=0; unbind mask=0 key='XF86KbdBrightnessDown' code=0; add exec) v3_model=agree
CASE HARD-0       FAIL missing=18 extra=0 oracle_binds=18 (HARD tree lines=27 binds=18 unbinds=2 vars=4) v3_model=agree
    missing mask=13 key="2" code=0 disp="sendshortcut" arg="shift, F5, activewindow"
    missing mask=69 key="" code=166 disp="bringactivetotop" arg=""
CASE HARD-1       FAIL missing=22 extra=0 oracle_binds=22 (HARD tree lines=32 binds=22 unbinds=2 vars=4) v3_model=agree
    missing mask=4 key="" code=75 disp="layoutmsg" arg="px9q"
    missing mask=65 key="4" code=0 disp="pseudo" arg=""
CASE HARD-2       FAIL missing=16 extra=0 oracle_binds=16 (HARD tree lines=27 binds=16 unbinds=3 vars=4) v3_model=agree
    missing mask=72 key="7" code=0 disp="movetoworkspacesilent" arg="special:bhae"
    missing mask=72 key="UP" code=0 disp="killactive" arg=""
CASE HARD-3       FAIL missing=20 extra=0 oracle_binds=20 (HARD tree lines=31 binds=20 unbinds=2 vars=4) v3_model=agree
    missing mask=64 key="" code=126 disp="resizeactive" arg="-26 -32"
    missing mask=76 key="F7" code=0 disp="moveintogroup" arg="d"
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=37/41 embed_hits=0 verdict=TARGET_MISSED
exit=1
```
