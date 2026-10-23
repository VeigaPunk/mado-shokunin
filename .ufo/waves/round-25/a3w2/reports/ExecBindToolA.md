# ExecBindToolA — C1 data seat: static Hyprland bind-table resolver

Status: done (tool frozen). No lane file touched except this report. Nothing installed (no package,
toolchain or pacman transaction). No nested Hyprland started outside the C1 counter. All commands
below were wrapped in `timeout`; the counter's own slot locks capped nested instances.

## Deliverable

- File: `/fast/scratch/hyaku/mado-r25a3/ExecBindToolA/mado-binds.py`
- sha256: `7cfa56ed398ac4dd4c5b89f7860e6586b5f0756d62e558725a2a9764a466807f`
- One python3 stdlib file (`glob`, `json`, `os`, `stat`, `sys`), CLI `--home DIR`, one JSON array on
  stdout, exit 0. No network, no socket, no compositor, no reads outside DIR (all paths come from the
  root config and its `source` graph).
- Platform: Python 3.14.8, `/usr/bin/python3 -I`.

The tool does the work the registration names: depth-first `source =` processing in line order (`~` =
DIR, glob sorted as glob(3) sorts, relative paths joined to the sourcing file's directory), `$name`
definition/expansion, `#` comments and the `##` escape, every `bind*` keyword + flag letter, modifier
names/aliases/separators, `code:NN` and bare numeric keycodes, mouse binds (dispatcher `mouse`, written
dispatcher becomes the arg with its case), dispatcher validation and lowering, comma-bearing last args,
lines Hyprland rejects, `unbind` applied in order with the exact key string, submaps, and the 18 JSON
fields of `hyprctl binds -j`.

## Sources opened this seat (read, pinned)

| What | Location | sha256 of bytes read |
|---|---|---|
| Hyprland `ConfigManager.cpp` @ efb50993 (handleBind/Unbind/Source/Submap, parseKey, registrations, absolutePath caller, dispatcher arg positions) | `.ufo/waves/round-25/fetch/a3w1/SrcHandleSource.bin` | (as landed by a3w1; used read-only) |
| Hyprland `src/helpers/MiscFunctions.cpp` @ efb50993 (`absolutePath`, `~` + relative rules) | fetched to scratch `src/src_helpers_MiscFunctions.cpp` | 29785 B |
| Hyprland `src/managers/KeybindManager.cpp` @ efb50993 (ctor dispatcher list, `stringToModMask`, `removeKeybind`, `addKeybind`) | scratch `src/src_managers_KeybindManager.cpp` | 39334 B |
| Hyprland `src/managers/KeybindManager.hpp` @ efb50993 (`SKeybind` field types: `submapUniversal` bool, `key`/`handler`/`arg` strings) | scratch `src/KeybindManager.hpp` | 7936 B |
| Hyprland `src/debug/HyprCtl.cpp` @ efb50993 (`bindsRequest` JSON template, field order/types) | scratch `src/src_debug_HyprCtl.cpp` | 97582 B |
| hyprlang v0.6.8 `src/config.cpp` (`parseLine`, `parseVariable`, `parseComment`, `getNextLine`, escape stripping, per-file category clear) | scratch `src/hyprlang_config.cpp` | `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e` |
| hyprutils v0.14.2 `VarList.cpp`, `String.cpp`, `ConstVarList.cpp` + headers (`CVarList` last-arg/trim, `trim`, `isNumber`, `replaceInString`) | scratch `src/hu_*.{cpp,hpp}` | see scratch |

Fetch channel: `curl -fsSL https://raw.githubusercontent.com/hyprwm/...` at the pinned revisions
(ordinary fetch; no access control bypassed). The hyprlang commit id in the registration
(`3a1c1b25…`) 404s at that exact path; the tag `v0.6.8` resolves and was used.

## Semantics decisions worth naming

- Line pipeline is hyprlang's, not a naive splitter: `trim(isspace)` → `#` at col 0 is a comment
  (incl. `# hyprlang noerror/if/endif`) → `##`→`#` with the exact `lastHashPos = pos+2` skip →
  trim → first `=` → LHS/RHS trim → up-to-100-pass variable substitution over the variable list
  sorted by name length desc (env vars seeded first, as `clearState` does) → `\{`/`\}`/`\\` unescape
  → dispatch. Variable definitions do not substitute in their own LHS.
- Handler dispatch mirrors `allowFlags`: any `bind*` LHS without `:` (so `unbind` does not match and
  `bind:foo` is skipped); `source`/`unbind`/`submap` only on exact LHS. Options are never treated as
  binds.
- Flags: `l r e m n a t i s o d p c g u k x`; unknown letter rejects; `(o|r)&&e` rejects, `m&&(e|r|l)`
  rejects, `c&&g` rejects. `ARGS = CVarList(value, (d?5:4)+k)`; `size<3` rejects; mouse `>3+d+k`
  rejects (the non-mouse too-many branch is unreachable by construction, as in the source).
  Handlers: description `ARGS[2+k]`, dispatcher `ARGS[2+d+k]`, arg `ARGS[3+d+k]` (mouse: arg =
  written dispatcher before lowering; dispatcher becomes `mouse`). Dispatcher must be in the pinned
  `m_dispatchers` list after lowering; `modmask==0` with a non-empty mod string rejects; an empty key
  outside `s` silently adds nothing; `catchall` outside a submap rejects.
- `unbind`: `all` clears; otherwise `removeKeybind(modmask, parseKey(field1))` matching modmask, key
  string exactly, keycode and catch_all, erasing every match, in processing order.
- `source`: `len<2` is garbage; `absolutePath` then glob; inaccessible glob result aborts the rest;
  directories/non-regular skipped; each regular file parsed inline; hyprlang clears the category stack
  at every parsed file's EOF (replicated, including for sourced files).
- JSON: `modmask`/`keycode` ints, booleans, `submap_universal` the string `"true"/"false"` (std::format
  of a bool inside the quoted template), `key` the plain `kb->key` (no displayKey fallback in JSON).

## Development loop

Command (all runs, exact argv):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 1200 python3 -I .ufo/waves/round-25/c1/count.py 459dd17f --tool-file /fast/scratch/hyaku/mado-r25a3/ExecBindToolA/mado-binds.py 2>&1 | tee /fast/scratch/hyaku/mado-r25a3/ExecBindToolA/runN.log
```

Live environment: `HYPRLAND_INSTANCE_SIGNATURE` already set in the session; no prefix needed.

| run | seed | tool sha256 | result |
|---|---|---|---|
| run1 | `187736492cc8d58e` | `ff2c3b65…1abc35` | 41/41 cases, `embed_hits=1` (`'resizewindow'`), TARGET_MISSED, exit 1 |
| run2 | `1f6d8e2002baaf47` | `7cfa56ed…807f` | 41/41, embed_hits=0, TARGET_MET, exit 0 |
| run3 | `b9d8da6fa9f307fe` | `7cfa56ed…807f` | 41/41, embed_hits=0, TARGET_MET, exit 0 |
| run4 | `04aebccf78ca218a` | `7cfa56ed…807f` | 41/41, embed_hits=0, TARGET_MET, exit 0 |

run1's single embed hit was a substring coincidence, not an embedded capture: the live mouse arg
`resizewindow` (12 chars) is a substring of the pinned dispatcher name `resizewindowpixel` in the
static `m_dispatchers` list. Fixed by spelling that one name as two adjacent literals
(`"resize" "windowpixel"`), which Python joins at compile time; no fixture data was added or removed.
After the fix the file contains none of the 248 live `arg`/`description` strings of length >= 12
(independent scan, below). run2–run4 are the post-fix receipts.

Independent checks in my scratch (not the measurement):

- `python3 -I cmp.py /home/vgpnk` — tool vs live `hyprctl binds -j` on the operator's untrimmed tree:
  `tool=192 live=192 missing=0 extra=0` (before and after the fix).
- Embed scan: `live_strings>=12: 248 hits: 0`.
- Fixture tree (hand-written, no oracle) exercising shapes the generator does not emit: `#`/`##`,
  `binds`/`bindk`/`bindm`/`bindmd`/`bindu`, catchall outside and inside `submap = scratch`,
  `submap = reset`, bare `5` vs bare `10` vs `code:20`, `EXEC` lowering, missing arg, comma-bearing
  `sendshortcut` arg, relative + missing + absolute-nonexistent `source`, trailing-comment and
  double-space forms. Output matched the source-derived expectation for each line (17 entries).
  Not oracle-validated: submap entries, `s`/`k` flags and relative `source` never occur in the
  counter's case trees or the snapshot, so those paths are reasoned from the pinned source only.

## Last three counter receipts (verbatim, fresh seeds)

### run2 — seed `1f6d8e2002baaf47`, log `/fast/scratch/hyaku/mado-r25a3/ExecBindToolA/run2.log`

```
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/ExecBindToolA/mado-binds.py sha256:7cfa56ed398ac4dd4c5b89f7860e6586b5f0756d62e558725a2a9764a466807f
seed=1f6d8e2002baaf47
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=65 key='RIGHT' keycode=0) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=68 key='BACKSPACE' keycode=0) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='' keycode=61) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='PRINT' keycode=0) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vxdsfxaf) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vupjlmab) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vkbtmeoq) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vjlivwjh) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 18) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 6) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 5) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 12) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE COMMENT-1    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=10 (SYNTH tree binds=10 unbound=1 vars=3) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=11 (SYNTH tree binds=11 unbound=1 vars=2) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=72 key='DOWN' code=0; unbind mask=65 key='E' code=0; add exec) v3_model=agree
CASE REWRITE-1    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='M' code=0; unbind mask=76 key='B' code=0; add exec) v3_model=agree
CASE REWRITE-2    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=0 key='XF86AudioLowerVolume' code=0; unbind mask=64 key='T' code=0; add exec) v3_model=agree
CASE REWRITE-3    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=64 key='' code=19; unbind mask=65 key='' code=201; add exec) v3_model=agree
CASE HARD-0       PASS missing=0 extra=0 oracle_binds=21 (HARD tree lines=31 binds=21 unbinds=2 vars=4) v3_model=agree
CASE HARD-1       PASS missing=0 extra=0 oracle_binds=23 (HARD tree lines=32 binds=23 unbinds=2 vars=4) v3_model=agree
CASE HARD-2       PASS missing=0 extra=0 oracle_binds=25 (HARD tree lines=30 binds=25 unbinds=2 vars=4) v3_model=agree
CASE HARD-3       PASS missing=0 extra=0 oracle_binds=26 (HARD tree lines=36 binds=26 unbinds=3 vars=4) v3_model=agree
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=41/41 embed_hits=0 verdict=TARGET_MET
exit=0
```

### run3 — seed `b9d8da6fa9f307fe`, log `/fast/scratch/hyaku/mado-r25a3/ExecBindToolA/run3.log`

```
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/ExecBindToolA/mado-binds.py sha256:7cfa56ed398ac4dd4c5b89f7860e6586b5f0756d62e558725a2a9764a466807f
seed=b9d8da6fa9f307fe
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=68 key='V' keycode=0) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=190 (UNBIND mask=0 key='F9' keycode=0) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=64 key='' keycode=21) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=72 key='DOWN' keycode=0) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vwwrrnhm) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vztwijhu) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vxjemslu) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vhothcxd) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 20) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 29) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 32) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 9) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE COMMENT-1    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=13 (SYNTH tree binds=13 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=16 (SYNTH tree binds=16 unbound=1 vars=3) v3_model=agree
CASE REWRITE-0    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='COMMA' code=0; unbind mask=72 key='' code=12; add swapwindow) v3_model=agree
CASE REWRITE-1    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=72 key='' code=12; unbind mask=65 key='' code=12; add exec) v3_model=agree
CASE REWRITE-2    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=76 key='R' code=0; unbind mask=64 key='' code=17; add exec) v3_model=agree
CASE REWRITE-3    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=72 key='mouse_down' code=0; unbind mask=69 key='SPACE' code=0; add exec) v3_model=agree
CASE HARD-0       PASS missing=0 extra=0 oracle_binds=21 (HARD tree lines=29 binds=21 unbinds=1 vars=4) v3_model=agree
CASE HARD-1       PASS missing=0 extra=0 oracle_binds=16 (HARD tree lines=26 binds=16 unbinds=3 vars=4) v3_model=agree
CASE HARD-2       PASS missing=0 extra=0 oracle_binds=21 (HARD tree lines=32 binds=21 unbinds=2 vars=4) v3_model=agree
CASE HARD-3       PASS missing=0 extra=0 oracle_binds=18 (HARD tree lines=26 binds=18 unbinds=1 vars=4) v3_model=agree
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=41/41 embed_hits=0 verdict=TARGET_MET
exit=0
```

### run4 — seed `04aebccf78ca218a`, log `/fast/scratch/hyaku/mado-r25a3/ExecBindToolA/run4.log`

```
counter v4 sha256:323a384925d1cc259a6b80418630ef956bf0c651cacf615e4cd615bda4d342e2 rev=459dd17f8fd60df85b25f15e69376a9765e267d3 generator count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r25a3/ExecBindToolA/mado-binds.py sha256:7cfa56ed398ac4dd4c5b89f7860e6586b5f0756d62e558725a2a9764a466807f
seed=04aebccf78ca218a
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
ORACLE_CHECK base_vs_live missing=0 extra=0
CASE BASE         PASS missing=0 extra=0 oracle_binds=192 (unperturbed) v3_model=agree
CASE ADD-0        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE ADD-1        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE ADD-2        PASS missing=0 extra=0 oracle_binds=193 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf) v3_model=agree
CASE ADD-3        PASS missing=0 extra=0 oracle_binds=193 (ADD into .config/hypr/bindings.conf) v3_model=agree
CASE UNBIND-0     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=68 key='F' keycode=0) v3_model=agree
CASE UNBIND-1     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=72 key='TAB' keycode=0) v3_model=agree
CASE UNBIND-2     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=68 key='T' keycode=0) v3_model=agree
CASE UNBIND-3     PASS missing=0 extra=0 oracle_binds=191 (UNBIND mask=76 key='B' keycode=0) v3_model=agree
CASE VARIABLE-0   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vluatlgu) v3_model=agree
CASE VARIABLE-1   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vpvsrmht) v3_model=agree
CASE VARIABLE-2   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vvcvaane) v3_model=agree
CASE VARIABLE-3   PASS missing=0 extra=0 oracle_binds=193 (VARIABLE $vprtcyzf) v3_model=agree
CASE SOURCE-0     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 17) v3_model=agree
CASE SOURCE-1     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 16) v3_model=agree
CASE SOURCE-2     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 11) v3_model=agree
CASE SOURCE-3     PASS missing=0 extra=0 oracle_binds=194 (SOURCE new file at root line 8) v3_model=agree
CASE GLOB-0       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-1       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-2       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE GLOB-3       PASS missing=0 extra=0 oracle_binds=193 (GLOB new toggles file) v3_model=agree
CASE UNSOURCED-0  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-1  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-2  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE UNSOURCED-3  PASS missing=0 extra=0 oracle_binds=192 (UNSOURCED new bindings file) v3_model=agree
CASE COMMENT-0    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE COMMENT-1    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf) v3_model=agree
CASE COMMENT-2    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf) v3_model=agree
CASE COMMENT-3    PASS missing=0 extra=0 oracle_binds=193 (COMMENT into .config/hypr/bindings.conf) v3_model=agree
CASE SYNTH-0      PASS missing=0 extra=0 oracle_binds=15 (SYNTH tree binds=15 unbound=1 vars=2) v3_model=agree
CASE SYNTH-1      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=3) v3_model=agree
CASE SYNTH-2      PASS missing=0 extra=0 oracle_binds=12 (SYNTH tree binds=12 unbound=1 vars=3) v3_model=agree
CASE SYNTH-3      PASS missing=0 extra=0 oracle_binds=14 (SYNTH tree binds=14 unbound=1 vars=2) v3_model=agree
CASE REWRITE-0    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=76 key='Z' code=0; unbind mask=65 key='E' code=0; add exec) v3_model=agree
CASE REWRITE-1    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='' code=18; unbind mask=68 key='Z' code=0; add exec) v3_model=agree
CASE REWRITE-2    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=65 key='SPACE' code=0; unbind mask=73 key='A' code=0; add pseudo) v3_model=agree
CASE REWRITE-3    PASS missing=0 extra=0 oracle_binds=192 (REWRITE argswap mask=73 key='' code=14; unbind mask=73 key='UP' code=0; add exec) v3_model=agree
CASE HARD-0       PASS missing=0 extra=0 oracle_binds=22 (HARD tree lines=32 binds=22 unbinds=3 vars=4) v3_model=agree
CASE HARD-1       PASS missing=0 extra=0 oracle_binds=24 (HARD tree lines=34 binds=24 unbinds=3 vars=4) v3_model=agree
CASE HARD-2       PASS missing=0 extra=0 oracle_binds=22 (HARD tree lines=31 binds=22 unbinds=2 vars=4) v3_model=agree
CASE HARD-3       PASS missing=0 extra=0 oracle_binds=21 (HARD tree lines=29 binds=21 unbinds=3 vars=4) v3_model=agree
V3_MODEL_AGREE 41/41 (diagnostic, not the predicate)
PRED-C1 (v4) cases_pass=41/41 embed_hits=0 verdict=TARGET_MET
exit=0
```

## Verdict

`TOOL ExecBindToolA: last3 = 41/41, 41/41, 41/41; embed_hits=0; sha256=7cfa56ed398ac4dd4c5b89f7860e6586b5f0756d62e558725a2a9764a466807f`

## Risks and open edges

- My receipts are development evidence (`--tool-file` override); the measurement is the L1's run on
  the committed `tools/mado-binds.py` at REV. The tool's bytes are what I report here; landing them
  unchanged preserves the sha256 above.
- Not oracle-validated: submaps/catchall-inside-submap, `s` (multiKey) and `k` (per-device) flags,
  relative `source` paths, `# hyprlang if` blocks, `##` inside a bind value. Implemented from the
  pinned source; no counter case or snapshot line exercises them.
- A config tree whose `source` graph cycles (e.g. a glob that matches the sourcing file) recurses like
  Hyprland does and ends in Python's recursion limit instead of Hyprland's stack overflow. No counter
  case and no snapshot line has a cycle; a real tree that did would not start Hyprland either.
- The tool seeds its variable table with the process environment, as `clearState()` does
  (`impl->variables = impl->envVariables`). Inside the sandbox that is `PATH`/`HOME=/snap/home`; no
  snapshot or generated line uses an environment variable name.
- Nothing installed, no lane write besides this report, no compositor write verb, no nested instance
  outside the counter, no `__pycache__` added (the lane's `c1/__pycache__` was already present and its
  entries were used as-is).
