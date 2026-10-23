RESC1: remeasure 41/41; beyond-generator trees agree 9/10

# ResC1Remeasure — independent measurement attack

The single fresh-seed v4 remeasurement did not falsify PRED-C1 (v4): 41/41, embed_hits=0, exit=0. A separate hand-made tree falsifies unrestricted tree-equivalence: ordinary hyprlang arithmetic produces different bind arguments. That is a scope finding, not a failure of the frozen finite predicate. No admission or canonical judgment is made here.

Impacted axes: operability/capability accuracy outside the generator; calibration if the finite receipt is presented as general equivalence. Receipt provenance/reproducibility survived this attack. Host-safety bounds were retained.

## 1. Frozen bytes and committed-receipt consistency

- Measured commit: `ef94763c6a75d1b0860091b19bb61c9bd7cda9e3`.
- `git show ef94763c:tools/mado-binds.py` hashes to **`9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950`**, exactly the requested tool hash. The working-tree tool had this same hash before each hand-made-tree invocation.
- Counter: `323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2`; generator: `8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375`. Both matched the Attempt 3 pins before execution.
- The original receipt was read from commit `90224671e8e0a265ecc96b54100f981e31afe2c9` and was byte-identical to the lane receipt. Receipt sha256: `6daa8d03fb10c86e55f9868a256709bd8781285d20f098d5002c49dba8db1d1c`.
- Its seed `ed0d8a943980d2f2` is distinct from the fresh seed `5aec873104392f2d`. Re-generating only the original seed's case descriptions and v3-model counts reproduced all **40/40** generated receipt lines; BASE is separately consistent at 192 binds. This was not another counter run or an old-seed oracle replay.
- Original receipt, fresh receipt, and a separate current read-only capture have the same live sha256: `9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`.
- Original and fresh snapshots agree: 79 files, digest `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`, 192 live binds. The independent snapshot used for the seed check matched too.
- Both receipts say `ORACLE_CHECK base_vs_live missing=0 extra=0`; each BASE line says PASS, missing=0, extra=0, oracle_binds=192. The original contains exactly 41 distinct passing case lines, its diagnostic says 41/41, its predicate says 41/41 with zero embed hits, and its recorded exit is 0. No internal inconsistency found.

Machine-readable checks: `/fast/scratch/hyaku/mado-r25a3/res/ResC1Remeasure/committed-receipt-consistency.json`.

## 2. One fresh counter run — verbatim receipt and exit

Invoked the unchanged counter once, without `--seed` or `--tool-file`: `python3 -I -B .ufo/waves/round-25/c1/count.py ef94763c6a75d1b0860091b19bb61c9bd7cda9e3`. A supervisor put its temporary directory under this seat's scratch, applied memory/file/CPU limits and a 300-second deadline, and recorded the exit. No retry. The counter retained its default four oracle workers and its own host-wide six-slot locking.

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=ef94763c6a75d1b0860091b19bb61c9bd7cda9e3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=tools/mado-binds.py@ef94763c6a75 sha256:9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950
seed=5aec873104392f2d
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='K' keycode=0) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=68 key='BACKSPACE' keycode=0) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='BACKSPACE' keycode=0) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='COMMA' keycode=0) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vmazfopw) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vesfwugj) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vkjxxisa) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vtadujih) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 9) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 11) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 20) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 7) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE COMMENT-1    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
CASE REWRITE-0    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=68 key='H' code=0; unbind mask=72 key='COMMA' code=0; add exec) v3_model=agree
CASE REWRITE-1    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='LEFT' code=0; unbind mask=65 key='COMMA' code=0; add exec) v3_model=agree
CASE REWRITE-2    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86Calculator' code=0; unbind mask=72 key='mouse_up' code=0; add exec) v3_model=agree
CASE REWRITE-3    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='SPACE' code=0; unbind mask=64 key='' code=21; add fullscreen) v3_model=agree
CASE HARD-0       PASS missing=0 extra=0 oracle_binds=19 (HARD tree lines=30 binds=19 unbinds=3 vars=4) v3_model=agree
CASE HARD-1       PASS missing=0 extra=0 oracle_binds=19 (HARD tree lines=29 binds=19 unbinds=1 vars=4) v3_model=agree
CASE HARD-2       PASS missing=0 extra=0 oracle_binds=25 (HARD tree lines=30 binds=25 unbinds=1 vars=4) v3_model=agree
CASE HARD-3       PASS missing=0 extra=0 oracle_binds=20 (HARD tree lines=29 binds=20 unbinds=0 vars=4) v3_model=agree
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=41/41 embed_hits=0 verdict=TARGET_MET
exit=0
```

Exact receipt file: `/fast/scratch/hyaku/mado-r25a3/res/ResC1Remeasure/fresh-v4-receipt.txt`. Supervisor result: `timed_out=False residual_processes=[]`.

## 3. Ten hand-made exec-free trees

Base directory: `/fast/scratch/hyaku/mado-r25a3/res/ResC1Remeasure/trees/`. Each row's home is `<base>/<tree>/home`; root is `.config/hypr/hyprland.conf`. These were authored directly, not generated by count-v3.py.

For each tree, a `python3 -I -B` adapter imported the frozen count.py read-only and called its **own `oracle(home, work)`**. No other nested-Hyprland launch path was used. The matching tool command was `python3 -I -B tools/mado-binds.py --home <home>` from the lane, with a cleared relevant environment and the matching tool hash. An independent JSON multiset comparison checked the exact 18-field schema and every field, retaining multiplicities. Both oracle adapter and tool exited 0 for every row.

| Tree | Beyond-generator surface | Oracle/tool binds | Result and complete multiset diff |
|---|---|---:|---|
| `01-submaps` | Enter a named submap, `submap = reset`, catchall inside and outside the submap, submap reset argument | 5/5 | **Agree**; missing=0, extra=0. Catchall survives only inside the named submap. |
| `02-bindu` | Universal binds in default/named submaps, `ud` combination | 4/4 | **Agree**; missing=0, extra=0. |
| `03-bindk` | Per-device inclusion/exclusion fields; `kd`, `km`, `kx` combinations | 4/4 | **Agree**; missing=0, extra=0. This establishes the exported 18 fields, not device-filter execution behavior. |
| `04-binds` | Multi-key/modifier `&` lists, `sd`, combined `sk` | 4/4 | **Agree**; missing=0, extra=0. Not a runtime key-event test. |
| `05-relative-source` | `./nested/child.conf`, child `../shared.conf`, submap state carried back to parent | 5/5 | **Agree**; missing=0, extra=0. |
| `06-no-match` | `source = ./missing/*.conf` between two binds | 2/2 | **Agree**; missing=0, extra=0. Oracle log reports `source= globbing error: found no match`; both binds still appear. Agreement is table-only, not diagnostic parity. |
| `07-hashes` | `##` inside arg/description; `###`, `####`, trailing ordinary comment | 4/4 | **Agree**; missing=0, extra=0. Both give A arg `special:alpha#beta`, B `special:gamma##`, C arg `special:epsilon#zeta` and description `Label#hash`, D `special:eta##theta`. |
| `08-late-vars` | Variable defined after use, undefined modifier before definition, reassignment | 3/3 | **Agree**; missing=0, extra=0. A retains literal `$mado_late`; the early undefined-modifier bind is absent; later B arg is `81`, C is `83`. |
| `09-source-cycle-guard` | Finite source revisit A→B→A, terminated by B retargeting `$mado_next` to stop.conf | 5/5 | **Agree**; missing=0, extra=0. A/91 occurs twice, then S/93, B/92, Z/94. A global visited-file suppression would incorrectly lose the second A. |
| `10-arithmetic` | Unescaped arithmetic directly in bind args and in a variable; escaped arithmetic control | 3/3 | **Disagree**; missing=2, extra=2. Only args differ: A oracle `101`, tool `{{100 + 1}}`; B oracle `102`, tool `{{100 + 2}}`. C agrees at literal `{{100 + 3}}`. All other 17 fields agree. |

Per-tree input hashes, full missing/extra entries and exits: `<tree>/result.json`. Full oracle table/log and exact tool stdout: `<tree>/oracle.raw.json`, `<tree>/oracle-work/hyprland.log`, `<tree>/tool.raw.json`. Aggregate: `/fast/scratch/hyaku/mado-r25a3/res/ResC1Remeasure/handmade-results.json`.

Cycle scope: no implicit cycle/depth guard appears in the tool's `handle_source`/`parse_file` or Hyprland's pinned `handleSource` path. Tree 09 uses an explicit configuration-level variable guard; no unguarded stack-overflow tree was started, and no claim about a table for a crashing compositor is made.

## 4. Strongest counterexample and smallest safe correction

Relevant input from tree 10:

```ini
$mado_number = 100
bind = SUPER, A, workspace, {{$mado_number + 1}}
$mado_calculated = {{$mado_number + 2}}
bind = SUPER, B, workspace, $mado_calculated
bind = SUPER, C, workspace, \{{100 + 3}}
```

For `(modmask=64, key=A, dispatcher=workspace)`, Hyprland exports `arg="101"`, while the tool exports `arg="{{100 + 1}}"`. For B, it exports `102` versus `{{100 + 2}}`. Each discrepancy is one missing and one extra full 18-field row. The escaped C case agrees, ruling out a blanket recommendation to evaluate every brace pair.

Local source evidence:

- `.ufo/waves/round-25/fetch/S172.bin:109-146` documents arithmetic and escaping.
- Retained pinned hyprlang v0.6.8 source `/fast/scratch/hyaku/mado-r25a3/ExecBindToolA/src/hyprlang_config.cpp`, sha256 `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e`: `parseExpression` at 619-667; expression evaluation within the variable-expansion loop at 755-794, before variable assignment at 805-806 and escape removal at 808 onward.
- The measured tool's `parse_line` at 403-418 substitutes variables, then assigns variables or unescapes braces without that expression stage. The frozen generator's SYNTH/HARD paths do not emit arithmetic expressions.

This is a **fixable parser omission**, not evidence that the frozen 41-case receipt is false. The smallest semantics-preserving implementation correction is to add hyprlang's unescaped expression stage in the expansion loop, before variable assignment/brace unescaping, preserving its numeric formatting and error behavior; retain tree 10 as an independent oracle regression. Do not special-case the workspace dispatcher or these numbers. Until that repair exists, explicitly disclose unsupported arithmetic wherever prose implies unrestricted config-tree equivalence. Keep the frozen predicate and both measurement receipts unchanged; do not replace the finite claim with a broader or narrower one.

## 5. Safety and execution accounting

- Hyprland readback identified v0.56.2 at `efb50993780079460b0cbed1363e2166a2de1d9f`, system hyprlang 0.6.8.
- All hand-made trees were small regular-file trees, checked exec/plugin-free before oracle use; their bind dispatchers are non-exec. Only the counter's oracle started nested instances.
- Counter supervisor: 16 GiB per-process address-space cap, 16 MiB per-file cap, CPU cap, 300-second deadline. Hand-made oracle calls: 120-second individual deadlines; tool calls: 15 seconds; core dumps disabled for the hand-made probes. Every completed supervisor reported no residual processes; the oracle's own finally block killed its process groups.
- No git/jj writes, clone, live-compositor write verbs, package/service/config changes, or lane edits other than this report. Python counter imports used `-I -B`, avoiding lane bytecode writes. Scratch evidence is confined to `/fast/scratch/hyaku/mado-r25a3/res/ResC1Remeasure/` apart from the counter's documented slot/runtime bookkeeping.
- No tools installed or upgraded. No canonical judge/runtime invoked. No other verification claimed.
