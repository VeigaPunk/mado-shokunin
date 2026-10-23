# ExecBindToolB — C1 data seat (attempt 3, wave a3w2)

Independent implementation of the static bind-table resolver. I read only the pinned Hyprland /
hyprutils / hyprlang sources and the a3w1 recon reports; I did not read the counter's model
functions (`varlist`, `parse_key`, `line_entry`, `unbind_apply`, `mod_mask`, `model_check`). From
`count-v3.py` I read only the constant block and the case generators (`perturb`, `rewrite`, `synth`,
`hard`, `insert_before_bind`, `append`, `Gen`, `spell_mods`) to learn the case types.

## Deliverable (frozen)

```
/fast/scratch/hyaku/mado-r25a3/ExecBindToolB/mado-binds.py
sha256 778499d29ede8424ab79076641ac9a63a38132076ef43f8640e3f59a0160c304
size   16714 bytes, one Python 3 stdlib file, executable, CLI --home DIR, JSON array on stdout, exit 0
```

Integration owner: copy exactly these bytes to `tools/mado-binds.py` in the lane. The tool is not
in the lane; only this report is.

## Sources fetched (pinned, into /fast/scratch/hyaku/mado-r25a3/ExecBindToolB/src/)

| file | sha256 |
|---|---|
| Hyprland `efb50993780079460b0cbed1363e2166a2de1d9f` src/config/legacy/ConfigManager.cpp | `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b` |
| Hyprland same rev src/managers/KeybindManager.cpp | `8d8f35fc84c4a2f8de63ac2bf6f6531c651c6fa6d37b1aac7c8fc5d9342d4e40` |
| Hyprland same rev src/debug/HyprCtl.cpp | `798b7c6c4c1684557842463d46ac99c96629be4179e0e461dca77670247b91fa` |
| Hyprland same rev src/helpers/MiscFunctions.cpp | `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9` |
| hyprutils v0.14.2 src/string/VarList.cpp | `b02df8d688519366e7f20de5c3c44d21c3832316e8262ced0d295e129b166a36` |
| hyprutils v0.14.2 include/hyprutils/string/VarList.hpp | `9ad2fcbd5de691166b7db95de09b6bd054c9b4313deb3187e84c914dab74fc43` |
| hyprutils v0.14.2 src/string/String.cpp (trim, isNumber) | `a92c131a45f41918388eece78f225dbeab7791bb3cd2d3761d840aefa1527bac` |
| hyprlang v0.6.8 src/config.cpp (parseLine, parseComment, parseFile, getNextLine) | `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e` |

Two extra facts read from those files and used: `MULTILINE_SPACE_CHARSET = " \t"` (config.cpp:32),
and the CVarList split algorithm (delimiter replaced by NUL, `lastArgNo` stops splitting and keeps
the rest of the *original* string trimmed). I verified the split edge cases with a throwaway C++
program in scratch (empty input → one empty field; trailing comma → trailing empty field;
`lastArgNo` → last field keeps its commas and inner spaces); it was deleted after use.

## Semantics implemented (Hyprland v0.56.2 legacy hyprlang path)

- Line reading: `\n` split, `\`-continuation with trailing space/tab before the backslash removed
  (a continuation at EOF drops the line, as the parser errors), per-line trim on
  `space \t \n \v \f \r`.
- `#` handling: a line whose first non-space char is `#` is a comment (hyprlang directives
  `noerror` / `if` / `endif` tracked); otherwise the first unescaped `#` starts a trailing comment,
  `##` collapses to one `#` and scanning continues after it; a lone trailing `#` is a comment.
- Keywords: `bind`-prefixed keywords (handler `starts_with("bind")`, no `:` in the left side),
  exact `unbind`, exact `source`, exact `submap`; categories (`x {`, `}`) do not scope these.
- Variables: `$name = value` definitions are global and become visible to every later line (across
  `source` files); `$name` replacement runs on the left side (not on variable-definition lines) and
  the right side, up to 100 passes, longest names first; environment variables enter the table at
  parse start, as the parser does.
- `source`: resolved with the legacy `absolutePath` (leading `~` → HOME, `../x`, `./x`, relative →
  directory of the current file; other absolute paths untouched), then globbed (unsorted matches are
  sorted bytewise, which is the C locale's `strcoll`), regular files parsed depth-first in line
  order, directories and other file types skipped, unreadable matches abort that `source`, and a
  file sourced twice is parsed twice.
- Bind flags: all of `l r e m n a t i s o d p c g u k x` (`c` and `g` also set release); rejections
  in the source's order: unknown flag, `(release||longPress) && repeat`, `mouse && (repeat||release||locked)`,
  `click && drag`.
- Argument split: `(hasDescription?5:4) + perDevice` comma fields, last field keeps its commas;
  `< 3` fields rejected; mouse lines reject `> 3 + desc + device` fields; dispatcher looked up after
  lowercasing; `modmask == 0 && mod string != ""` rejected; a non-empty keysym is required unless
  the multi-key flag is set; `catchall` rejected outside a submap.
- Bind record: mouse lines rewrite the dispatcher to `mouse` and keep the written action as the
  argument (case preserved); `parseKey` handles `code:N`, all-digit keys greater than 9, `catchall`,
  and keeps every other key verbatim (case preserved); `stringToModMask` is the case-insensitive
  substring test over SHIFT/CAPS/CTRL|CONTROL/ALT|MOD1/MOD2/MOD3/SUPER|WIN|LOGO|MOD4|META/MOD5,
  with bits 1,2,4,8,16,32,64,128.
- `unbind`: split the value; `all` alone clears the table; otherwise remove every record matching
  modmask + key + keycode + catch_all (release/description ignored, order preserved otherwise).
- `submap`: first comma field becomes the current submap name, `reset` maps to the empty name.
- Output: the 18 fields of `hyprctl binds -j` with the same JSON types — `submap_universal` is the
  string `"true"`/`"false"`, the other flag fields are JSON booleans, `modmask`/`keycode` numbers,
  the rest strings. Records are appended and never deduplicated.

## Commands used

```
# dev loop, exactly as briefed (fresh seed each run):
cd /home/vgpnk/Projects/shokunin/mado-shokunin
HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120 \
  timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 459dd17f \
  --tool-file /fast/scratch/hyaku/mado-r25a3/ExecBindToolB/mado-binds.py
```

Local pre-check (no compositor): copied the four roots the counter copies into scratch
(`/fast/scratch/hyaku/mado-r25a3/ExecBindToolB/snap`, 79 files), ran the tool with
`env -i PATH=/usr/bin HOME=<snap>` and compared the multiset of the 18 fields against a read-only
`hyprctl binds -j` capture: `got 192 exp 192 missing 0 extra 0`.

## Verdict line

TOOL ExecBindToolB: last3 = 41/41, 41/41, 41/41; embed_hits=0; sha256=778499d29ede8424ab79076641ac9a63a38132076ef43f8640e3f59a0160c304

## Development evidence (12 fresh-seed counter runs, all exit 0 TARGET_MET)

Seeds in order: 065224a74ec99dd4, c9ba660bc87fdf49, 97536ce6e2a90801, a210706c6aaf6cce,
427829a9b3a076a5, 3ddf011c98d2db10, ecbdee97aebed70f, 976d6d0cd20e85bf, 56f6493445b7f84b,
24c9ec4eec2c4417, f9e11a0ea9ed578a (the first run of the day had no receipt file; it printed
`PRED-C1 (v4) cases_pass=41/41 embed_hits=0 verdict=TARGET_MET`). Every run printed
`ORACLE_CHECK base_vs_live missing=0 extra=0` and `V3_MODEL_AGREE 41/41`. No case line ever printed
FAIL. Counter and generator hashes in every receipt equal the pins.

## Capture-safety

The tool bytes contain no capture of the live table and no operator file: no path outside the
case home, no `live.json`/`out.json`/`snap` string, no `hyprctl` output. Checked mechanically
against the 248 live `arg`/`description` strings of length ≥ 12: `embed_hits 0`. The only strings
shared with the live capture are single-letter key names, which occur inside ordinary words. The
development inputs (`live.json`, `out.json`, `snap/`, receipts) live only under scratch and are not
part of the deliverable.

## Last three counter receipts (verbatim; latest three runs)

### receipt: seed=56f6493445b7f84b

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/ExecBindToolB/mado-binds.py sha256:778499d29ede8424ab79076641ac9a63a38132076ef43f8640e3f59a0160c304
seed=56f6493445b7f84b
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=65 key='' keycode=19) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=73 key='' keycode=13) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=69 key='R' keycode=0) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='PRINT' keycode=0) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vekwjprj) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vrhdvstz) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vadnmhhq) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vprifocp) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 9) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE COMMENT-1    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=17 (SYNTH tree binds=17 unbound=1 vars=3) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86MonBrightnessUp' code=0; unbind mask=0 key='XF86AudioMicMute' code=0; add fullscreen) v3_model=agree
CASE REWRITE-1    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='X' code=0; unbind mask=0 key='XF86TouchpadOn' code=0; add exec) v3_model=agree
CASE REWRITE-2    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=68 key='H' code=0; unbind mask=0 key='switch:on:Lid Switch' code=0; add changegroupactive) v3_model=agree
CASE REWRITE-3    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=68 key='I' code=0; unbind mask=65 key='O' code=0; add exec) v3_model=agree
CASE HARD-0       PASS missing=0 extra=0 oracle_binds=23 (HARD tree lines=29 binds=23 unbinds=2 vars=4) v3_model=agree
CASE HARD-1       PASS missing=0 extra=0 oracle_binds=22 (HARD tree lines=29 binds=22 unbinds=1 vars=4) v3_model=agree
CASE HARD-2       PASS missing=0 extra=0 oracle_binds=21 (HARD tree lines=28 binds=21 unbinds=3 vars=4) v3_model=agree
CASE HARD-3       PASS missing=0 extra=0 oracle_binds=19 (HARD tree lines=29 binds=19 unbinds=2 vars=4) v3_model=agree
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=41/41 embed_hits=0 verdict=TARGET_MET
exit=0
```

### receipt: seed=24c9ec4eec2c4417

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/ExecBindToolB/mado-binds.py sha256:778499d29ede8424ab79076641ac9a63a38132076ef43f8640e3f59a0160c304
seed=24c9ec4eec2c4417
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=68 key='TAB' keycode=0) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='' keycode=15) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=65 key='' keycode=201) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=73 key='COMMA' keycode=0) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vdhoihcy) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vnbcanqk) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vsxbljpf) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vdzqmfpw) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
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
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=2) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='G' code=0; unbind mask=64 key='mouse_down' code=0; add changegroupactive) v3_model=agree
CASE REWRITE-1    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=8 key='XF86MonBrightnessUp' code=0; unbind mask=76 key='Z' code=0; add exec) v3_model=agree
CASE REWRITE-2    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioRaiseVolume' code=0; unbind mask=65 key='' code=14; add movecurrentworkspacetomonitor) v3_model=agree
CASE REWRITE-3    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='LEFT' code=0; unbind mask=73 key='' code=17; add movetoworkspace) v3_model=agree
CASE HARD-0       PASS missing=0 extra=0 oracle_binds=17 (HARD tree lines=25 binds=17 unbinds=2 vars=4) v3_model=agree
CASE HARD-1       PASS missing=0 extra=0 oracle_binds=24 (HARD tree lines=29 binds=24 unbinds=3 vars=4) v3_model=agree
CASE HARD-2       PASS missing=0 extra=0 oracle_binds=19 (HARD tree lines=33 binds=19 unbinds=2 vars=4) v3_model=agree
CASE HARD-3       PASS missing=0 extra=0 oracle_binds=20 (HARD tree lines=31 binds=20 unbinds=2 vars=4) v3_model=agree
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=41/41 embed_hits=0 verdict=TARGET_MET
exit=0
```

### receipt: seed=f9e11a0ea9ed578a

```text
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/ExecBindToolB/mado-binds.py sha256:778499d29ede8424ab79076641ac9a63a38132076ef43f8640e3f59a0160c304
seed=f9e11a0ea9ed578a
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=65 key='' keycode=18) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=72 key='' keycode=14) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=0 key='XF86KbdBrightnessDown' keycode=0) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=65 key='A' keycode=0) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vnjorinz) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vxzmiklw) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vspmmrer) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vkuthtyi) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 10) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 7) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 12) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 9) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE COMMENT-1    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=2) v3_model=agree
CASE REWRITE-0    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86KbdLightOnOff' code=0; unbind mask=72 key='G' code=0; add moveintogroup) v3_model=agree
CASE REWRITE-1    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='O' code=0; unbind mask=64 key='mouse_up' code=0; add exec) v3_model=agree
CASE REWRITE-2    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='LEFT' code=0; unbind mask=64 key='LEFT' code=0; add movefocus) v3_model=agree
CASE REWRITE-3    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='' code=61; unbind mask=0 key='XF86KbdBrightnessUp' code=0; add movetoworkspacesilent) v3_model=agree
CASE HARD-0       PASS missing=0 extra=0 oracle_binds=22 (HARD tree lines=30 binds=22 unbinds=1 vars=4) v3_model=agree
CASE HARD-1       PASS missing=0 extra=0 oracle_binds=20 (HARD tree lines=31 binds=20 unbinds=3 vars=4) v3_model=agree
CASE HARD-2       PASS missing=0 extra=0 oracle_binds=25 (HARD tree lines=30 binds=25 unbinds=2 vars=4) v3_model=agree
CASE HARD-3       PASS missing=0 extra=0 oracle_binds=22 (HARD tree lines=33 binds=22 unbinds=3 vars=4) v3_model=agree
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=41/41 embed_hits=0 verdict=TARGET_MET
exit=0
```

## Risks and limits (all outside the measured case generator)

- `{{ expression }}` evaluation is not implemented. The parser would evaluate a brace expression
  before the keyword handler; no base line and no generated line contains one.
- A lone `-` key would throw `std::stoi` in the compositor (crash, not a bind); the tool treats it
  as a literal key. No case emits it.
- `# hyprlang if` truthiness is approximated (variable exists and is not one of the empty/false
  spellings); no base or generated line uses `if`.
- `submap` uses the same comma split and ignores the second (reset) field, which is not one of the
  18 output fields; no case emits `submap`.
- The sub-key (`s`, `&`-separated) and per-device (`k`, `!device`) paths are implemented from the
  source but not exercised by any case or by the base tree; their only visible effect would be
  `key: ""` for the multi-key flag and shifted argument indices for the per-device flag.
- Glob matching is Python's `glob` on an already absolute, tilde-expanded pattern. Generated and
  base patterns are `dir/*.conf` with ASCII names, where Python and glibc agree; backslash-escaped
  or `~user` patterns are not generated.
- The tool assumes the case-home layout `$HOME/.config/hypr/hyprland.conf`, as the counter passes
  it (`--home /snap/home`), and reads `$HOME` from the environment only for config-variable
  substitution, matching the parser's environment-variable table.

No tool was installed or upgraded in this seat. No lane file was written except this report; no
nested compositor was started outside the counter; all scratch artifacts, processes and temporary
files stay under `/fast/scratch/hyaku/mado-r25a3/ExecBindToolB/`.
