# ExecAnimToolB — C1 data seat B (`tools/mado-anims.py`)

Date: 2026-10-23. Seat: `MadoR26.ExecAnimToolB` (leaf). Round-26 wave w2, C1 data seat B.
Work root: `/fast/scratch/hyaku/mado-r26/data/ExecAnimToolB/`. Lane writes: this report only.

**Verdict:** `DATA ExecAnimToolB met (41/41, both final fresh-seed runs TARGET_MET)`.

## Deliverable

- Scratch file: `/fast/scratch/hyaku/mado-r26/data/ExecAnimToolB/mado-anims.py`
- sha256 `fe3c5a191d03b9af10dfedb0d1f7a4ad65a604147bbe8502ff0f2026a8ac0ab6`
- 22,922 bytes, 699 lines, python3 stdlib only (`glob, json, math, os, re, stat, struct, sys`)
- CLI `python3 -I mado-anims.py --home DIR`, prints `[nodes, beziers]` JSON on stdout, exit 0.
  It does not import the oracle, embed or replay any captured table, read `os.environ`,
  `/proc`, `mountinfo`, mtimes or case identity, and makes no network access; behaviour is
  derived only from the files reachable through the config's `source =` graph under
  `--home` and the source rules below.
- The lane `tools/` directory was not written. The L1 lands the file under the registration rule.

Receipts for these exact bytes (both `tool=` lines name the same sha256); full logs:
`/fast/scratch/hyaku/mado-r26/data/ExecAnimToolB/receipts/runA.log` and `runB.log`.

## Receipt A (fresh seed)

Command:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/data/ExecAnimToolB/mado-anims.py
```

stdout (verbatim):

```text
counter c1-r26-v2 sha256:4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428 rev=1b0b91e9889cbf984b052f5de564db78330a72aa oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/fast/scratch/hyaku/mado-r26/data/ExecAnimToolB/mado-anims.py sha256:fe3c5a191d03b9af10dfedb0d1f7a4ad65a604147bbe8502ff0f2026a8ac0ab6
seed=c061ee0b4fd9a8a2
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=base (unperturbed)
CASE C00   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:DISABLE+ROOT+CATEGORY+SOURCED)
CASE C01   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:UNSOURCED+ROOT+CATEGORY)
CASE C02   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:BEZIER+VARIABLE)
CASE C03   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:CATEGORY+SOURCED)
CASE C04   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:VARIABLE+ROOT)
CASE C05   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:NEWSRC+COMMENT+UNSOURCED)
CASE C06   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ROOT+REBEZ+BEZIER+SPACING)
CASE C07   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:VARIABLE+BEZIER)
CASE C08   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:CATEGORY+NEWSRC+DISABLE+ORDER)
CASE C09   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:VARIABLE+DISABLE)
CASE C10   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ORDER+VARIABLE+INVALID+DISABLE)
CASE C11   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:DISABLE+NEWSRC+CATEGORY)
CASE C12   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:REBEZ+VARIABLE+DISABLE)
CASE C13   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:DISABLE+SOURCED)
CASE C14   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:CATEGORY+REBEZ+NEWSRC+DISABLE)
CASE C15   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:SOURCED+ORDER)
CASE C16   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:NEWSRC+VARIABLE+ROOT)
CASE C17   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ORDER+INVALID+BEZIER+SOURCED)
CASE C18   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:NEWSRC+ROOT)
CASE C19   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ROOT+NEWSRC+REBEZ+COMMENT)
CASE C20   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+rewrite-animation+SOURCED)
CASE C21   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:delete-animation+REBEZ+ORDER)
CASE C22   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+DISABLE+SPACING)
CASE C23   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:delete-animation+rewrite-animation+SPACING+SOURCED)
CASE C24   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+REBEZ+INVALID)
CASE C25   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:delete-animation+rewrite-bezier+rewrite-animation+CATEGORY+ROOT)
CASE C26   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:delete-animation+ROOT+BEZIER)
CASE C27   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:delete-animation+rewrite-bezier+SOURCED)
CASE C28   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:delete-animation+COMMENT+ROOT)
CASE C29   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+SOURCED)
CASE C30   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:SOURCED+COMMENT+ROOT+DISABLE)
CASE C31   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:SPACING+ORDER+SOURCED+REBEZ+BEZIER)
CASE C32   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:BEZIER+SOURCED+SPACING+NEWSRC+ORDER+VARIABLE)
CASE C33   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:INVALID+DISABLE+COMMENT+SPACING+ORDER+UNSOURCED)
CASE C34   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:CATEGORY+NEWSRC+SOURCED+VARIABLE+COMMENT)
CASE C35   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:NEWSRC+DISABLE+CATEGORY+BEZIER)
CASE C36   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:INVALID+SPACING+SOURCED+DISABLE)
CASE C37   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:UNSOURCED+ORDER+COMMENT+SPACING+NEWSRC)
CASE C38   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:ROOT+UNSOURCED+SPACING+SOURCED)
CASE C39   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:REBEZ+SOURCED+INVALID+NEWSRC+SPACING+DISABLE)
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C1-r26-v2 cases_pass=41/41 verdict=TARGET_MET
exit=0
```

`outer_exit=0`.

## Receipt B (fresh seed, same bytes)

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/data/ExecAnimToolB/mado-anims.py
```

stdout (verbatim):

```text
counter c1-r26-v2 sha256:4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428 rev=1b0b91e9889cbf984b052f5de564db78330a72aa oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/fast/scratch/hyaku/mado-r26/data/ExecAnimToolB/mado-anims.py sha256:fe3c5a191d03b9af10dfedb0d1f7a4ad65a604147bbe8502ff0f2026a8ac0ab6
seed=7e6e8a10a315b6b5
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=base (unperturbed)
CASE C00   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ORDER+DISABLE+UNSOURCED+ROOT)
CASE C01   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:INVALID+UNSOURCED+COMMENT+CATEGORY)
CASE C02   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:REBEZ+ROOT+ORDER+NEWSRC)
CASE C03   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:SOURCED+NEWSRC+ROOT)
CASE C04   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ROOT+INVALID)
CASE C05   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=no (APPEND:INVALID+NEWSRC)
CASE C06   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:INVALID+ORDER+VARIABLE)
CASE C07   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:INVALID+BEZIER+NEWSRC+CATEGORY)
CASE C08   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:UNSOURCED+CATEGORY+REBEZ)
CASE C09   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:VARIABLE+ORDER)
CASE C10   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:SPACING+INVALID+CATEGORY+DISABLE)
CASE C11   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:DISABLE+REBEZ+CATEGORY)
CASE C12   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:CATEGORY+SOURCED)
CASE C13   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:REBEZ+UNSOURCED+SPACING+DISABLE)
CASE C14   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ROOT+REBEZ)
CASE C15   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ORDER+SOURCED+CATEGORY+NEWSRC)
CASE C16   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:VARIABLE+UNSOURCED)
CASE C17   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:SPACING+REBEZ+CATEGORY+DISABLE)
CASE C18   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:SPACING+SOURCED+DISABLE+COMMENT)
CASE C19   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:COMMENT+UNSOURCED+REBEZ+NEWSRC)
CASE C20   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:delete-animation+delete-animation+rewrite-animation+BEZIER+SOURCED)
CASE C21   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+rewrite-animation+UNSOURCED)
CASE C22   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+DISABLE+VARIABLE)
CASE C23   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+INVALID+COMMENT)
CASE C24   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+VARIABLE)
CASE C25   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:delete-animation+delete-animation+delete-bezier+ORDER)
CASE C26   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+delete-animation+delete-animation+REBEZ)
CASE C27   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-bezier+delete-animation+INVALID)
CASE C28   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+DISABLE)
CASE C29   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+delete-animation+delete-animation+SPACING)
CASE C30   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:DISABLE+BEZIER+ORDER+REBEZ+SOURCED)
CASE C31   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:SPACING+ORDER+REBEZ+UNSOURCED+VARIABLE)
CASE C32   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:SOURCED+INVALID+SPACING)
CASE C33   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:CATEGORY+VARIABLE+COMMENT)
CASE C34   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:INVALID+CATEGORY+COMMENT)
CASE C35   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:REBEZ+CATEGORY+NEWSRC+DISABLE+ORDER)
CASE C36   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:NEWSRC+BEZIER+SOURCED+INVALID)
CASE C37   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:VARIABLE+SOURCED+UNSOURCED)
CASE C38   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:COMMENT+ROOT+BEZIER+SOURCED+REBEZ)
CASE C39   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:ROOT+SPACING+CATEGORY+COMMENT+INVALID+ORDER)
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C1-r26-v2 cases_pass=41/41 verdict=TARGET_MET
exit=0
```

`outer_exit=0`.

## Rules implemented (source path:line)

Line anchors are from the pinned trees named in the seat contract plus three ordinary
pinned raw fetches into scratch (no bot challenge bypassed):

- `Hyprland efb50993780079460b0cbed1363e2166a2de1d9f`:
  `src/config/legacy/ConfigManager.cpp` (`fetch/SrcAnimConfig.bin`, sha256
  `9db68cf44048d86557d8a53068dcc40b9bd7347c7d95f38edc501565f65be62b`),
  `src/config/shared/animation/AnimationTree.cpp` (`fetch/SrcAnimTree.bin`),
  `src/debug/HyprCtl.cpp` (`fetch/SrcHyprctlAnims.bin`).
- `hyprutils v0.14.2` extracted at `/fast/scratch/hyaku/mado-r26/hyprutils-0.14.2/`
  (`src/animation/AnimationConfig.cpp`, `AnimationManager.cpp`, `BezierCurve.cpp`,
  `src/string/String.cpp`, `VarList.cpp`).
- `hyprlang v0.6.8` extracted at `/fast/scratch/hyaku/mado-r26/hyprlang-0.6.8/`
  (`src/config.cpp`).
- Three extra pinned fetches into `/fast/scratch/hyaku/mado-r26/data/ExecAnimToolB/src/`:
  `AnimationManager.cpp` sha256 `8c37cd0d1e972e8789468fdf063456a6a40ed17d482b898b0639a6d2a1fa7985`
  (16,288 B), `ParserUtils.cpp` sha256 `86f21b761695571fc17f5a2ad68ddd30bf06d06d4d6a47ab443dc89ca511c2c0`
  (5,902 B), `MiscFunctions.cpp` sha256 `065418241a3b40e21273bca1fd29036221942554cddb61e08422d86f0a13c1d9`.

Implemented:

1. **The 35-node tree and its initial values.** `AnimationTree.cpp:14-67` creates
   `__internal_fadeCTM` and `global` as roots and the other 33 nodes with their parents;
   then writes `global` (enabled 1, speed 8, `default`), `__internal_fadeCTM`
   (1, 5, `linear`), and `borderangle`/`shadowangle`/`glowangle` (0, 1, `default`).
   The dump reads only per-node `overridden`, `internalBezier`, `internalEnabled`,
   `internalSpeed`, `internalStyle` (`HyprCtl.cpp:947-959`), so `pValues` /
   `pParentAnimation` (`hyprutils AnimationConfig.cpp:9-70`) cannot be observed and are
   not tracked. Unset nodes keep enabled `-1`, which the JSON writer renders `true`.
2. **Node overwrite semantics.** `hyprutils AnimationConfig.cpp:35-51`: each successful
   write sets `overridden` true and replaces all five dumped fields; the last write wins.
3. **`animation =`** (`legacy/ConfigManager.cpp:1426-1479`):
   fields via `CVarList` (comma split, empty kept, trimmed; `hyprutils VarList.cpp:8-26`);
   unknown/empty node name returns without a write; enabled from
   `ParserUtils::parseInt(...).value_or(0) == 1` (`ParserUtils.cpp:134-149`: `0x` hex via
   `parseHex`, case-sensitive `true`/`on`/`yes` prefix 1, `false`/`off`/`no` prefix 0,
   otherwise `from_chars<int64_t>` over the whole token, including `0X` hex reached through
   `strToNumber`); any non-1 value is the off path, which writes enabled 0, speed 1,
   bezier `default`, empty style and ignores later fields; on the on path speed must pass
   `isNumber(..., true)` (`hyprutils String.cpp:50-84`) and `std::stof > 0`
   (float32, no exponent, `-.5` accepted, `5.`/`.5`/`+1`/`1e2` rejected); the bezier name
   must be a key in the curve map at that moment; the write happens before the nonempty
   style is validated (`src/animation/AnimationManager.cpp:388-457`), so an invalid style
   is stored as written and the returned error changes no table field.
4. **`bezier =`** (`legacy/ConfigManager.cpp:1389-1424`): four point tokens, each required
   and `isNumber(..., true)`, then `stof`; a nonempty sixth field is `too many arguments`;
   a trailing comma (empty sixth field) is allowed; checks all return before the write.
   Name may be empty. `hyprutils AnimationManager.cpp:54-58` replaces the key.
5. **Built-in curves** (`hyprutils AnimationManager.cpp:13,16-20,40-46`;
   `legacy/ConfigManager.cpp:766-767`): `default` = `(0.0,0.75),(0.15,1.0)` as doubles,
   `linear` = `(0,0),(1,1)`; user points are float32 promoted to double
   (`BezierCurve.cpp:11-20`); dump prints control points `[1]` and `[2]`.
6. **hyprlang v0.6.8 line handling** (`src/config.cpp`): `getNextLine` continuations
   (`:44-64`, trailing spaces/tabs before `\` dropped, EOF-after-`\` ends the file);
   comment/`##` scanning and `# hyprlang if/!if/endif/noerror` (`parseLine :669-814`,
   `parseComment :567-606`, `SVariable::truthy` = nonempty in `config.hpp:27-29`);
   `=` split with trimmed sides; `$name` expansion ordered longest-name-first, up to 100
   rounds, with LHS substitution only for non-variable lines (`:732-806`,
   `parseVariable :518-541`); `{{expr}}` evaluation (`parseExpression :619-667`: three
   whitespace tokens, one of `+ - * /`, float32 result, shortest-decimal splice) with the
   odd/even backslash escape rule and literal-keep on an unclosed `}}`; escape stripping
   of `\\`, `\{`, `\}` after expansion; category push/pop and the stack being cleared at
   the end of every parsed file; handler match by exact bare LHS (unscoped
   `allowFlags=false` handlers), so `animation`/`bezier` fire at any category depth.
7. **`source =`** (`legacy/ConfigManager.cpp:1805-1859`, `MiscFunctions.cpp:61-83`):
   `len < 2` rejected; `~` replaced by `--home`; relative, `./`, `../` resolved against
   the sourcing file's directory; matches parsed immediately in sorted glob order;
   directories and non-regular files skipped; an inaccessible match stops later matches;
   each sourced file restores the parent's current path on return.
8. **Output** (`HyprCtl.cpp:927-985`): JSON `[[node,...],[bezier,...]]` with node fields
   name/overridden/bezier/enabled/speed/style and bezier fields name/X0/Y0/X1/Y1.
   `{:.2f}` values are emitted as the number the printed decimal parses to, so
   `json.loads` of Hyprland's text and of this tool's output compare equal.

## Development evidence (scratch, not receipts)

All comparisons ran the pinned `harness/oracle.py` under
`timeout 900 prlimit --as=4000000000:8000000000 --`; the tool was invoked through
`oracle.run_tool` (bwrap, cleared env, `--home /snap/home`). Scratch scripts:
`dev_check.py`, `dev_edges.py`, `dev_edges2.py`, `dev_edges3.py`, and the formatting
probe in `probe/`.

- Snapshot of the operator's four config roots (79 files, digest
  `fe1b2d8b…`) — tool vs oracle: nodes 35/35, beziers 6/6, **MATCH** (first comparison).
- Five crafted trees (`vars`, `sources`, `cheese`, `enabled`, `cat`) covering `$var` in
  node/speed/bezier fields, `##`, `#`, line continuations, escaped `{{`, expressions with
  bare-name operands, off-path writes, invalid speed/bezier/style, `0x`/`0X`/`on`/`no`
  enabled spellings, empty/late/extra bezier argument cases, a non-`animations` category:
  **5/5 MATCH** after one fix (see below).
- Structural trees (`empty` = comment-only root, unclosed category at EOF, CRLF, JSON
  escaping of `"` and `\` in names/styles): **MATCH**. `eofslash` mismatched for the
  counter-artifact reason recorded under gaps.
- Source resolution tree (directory source skipped, `inc/*.conf` sorted, `./inc/b.conf`,
  `inc/../inc/c.conf`, unmatched glob): **MATCH**.
- `{:.2f}` fidelity: 29 hand-picked boundaries plus 20,000 random float32 tokens
  (`probe/fmt2.cpp` compiled with host `g++ -std=c++23`, `std::stof` +
  `std::format("{:.2f}")`) compared against Python `format(f32(x), ".2f")`: **0
  mismatches**.
- One defect found and fixed during development: `0X1` (capital `X`) enabled `layers` in
  the oracle but not in the tool. `ParserUtils::parseInt` only tests lowercase `0x` for
  `parseHex`, but `strToNumber<int64_t>` itself accepts `0x`/`0X` in its integral branch;
  `parse_int` now models both (lowercase through the uint64→int64 wrap, uppercase through
  the int64 range check). Both final receipts are on the fixed bytes.

## Host safety

- Every nested Hyprland was started only by `harness/oracle.py`; I started nothing with
  `WAYLAND_DISPLAY`, `HYPRLAND_INSTANCE_SIGNATURE`, a DRM card node, or a live `hyprctl`
  verb. No write verb was ever sent to the live compositor.
- Both final receipts: `hyprland_coredumps_before=1338 after=1338 delta=0`.
- An earlier development counter run (pre-fix seed `fcd1ed671cad7fd8`, 41/41) printed
  `delta=1`. `coredumpctl info 2367290` identifies that record's command line as
  `.../data/ExecAnimToolA/devO-pmv1gx6g/tmp.../home/.config/hypr/hyprland.conf`, i.e. a
  sibling data seat's nested instance, not this seat's run.
- One record of mine is visible: during `dev_edges2.py` I built a root whose glob
  re-sourced the root itself; the nested Hyprland SIGSEGV'd (PID 2456401, command line
  `.../dev-edges2-sh_zhh4r/dirsource-oracle/home/...`), inside bwrap, adding one coredump
  record (1337 → 1338). The test was not repeated; no host session was involved. The
  snapshot and every generated case shape contain no source cycle.
- After the runs, `pgrep -af "Hyprland|tinywl"` showed only the live session's
  `/usr/bin/Hyprland --watchdog-fd 4` and `earlyoom`; no nested process or tinywl was
  left behind.

## Known gaps and limits

1. **Root EOF trailing backslash vs the counter's oracle copy.** Hyprland abandons a file
   whose last line ends on `\`; the counter's oracle appends `ORACLE_EXTRA` to the root
   copy, so a root-ending continuation there joins the appended empty line and is parsed.
   The tool models the tree itself (EOF error) and therefore differed on a crafted
   `eofslash` root. The snapshot has no trailing-backslash line (checked all four roots;
   none), and the generator's `append`/`edit_case`/`synth_tree` always end files with a
   newline and never create a trailing `\`. Not reachable by the frozen cases.
2. **Source cycles are not detected.** Hyprland recurses without a guard (the crafted
   self-source crashed the nested instance); the tool raises `RecursionError` and exits
   non-zero. Neither the snapshot nor any generated case contains a cycle.
3. **Process environment is not seeded.** hyprlang starts its variable table from the
   process environment; the seat contract forbids `os.environ`, so a `$NAME` that refers
   to a process variable is left literal, and the `env =` handler's `setenv` is not
   modeled (it cannot change the same parse's variable snapshot anyway). All snapshot and
   case variables are defined in-file.
4. **`{{…}}` expressions** are implemented per `config.cpp:619-667` but only smoke-tested
   (two crafted cases); operand overflow, exotic hex-float prefixes and the exact
   shortest-float text for non-counter values are approximations. Expression `std::stof`
   overflow is treated as a literal error rather than the uncaught exception it is in C++.
5. **Symlinked root.** The root is read via `realpath` (matching `std::filesystem::
   canonical`), but relative sources then resolve against the canonical directory whereas
   Hyprland's `m_configCurrentPath` stays the pre-canonical main path. Snapshot and SYNTH
   roots are regular files.
6. **Glob details.** Python `glob` + `sorted()` approximates glibc `glob(GLOB_TILDE)` with
   C-locale `strcoll`: equal for the ASCII names in the snapshot and cases; tilde after a
   slash, malformed bracket patterns and `~user` are not modeled beyond `absolutePath`'s
   leading-`~` replacement.
7. **Style validation is unobservable.** It is implemented and invoked after the write
   (as the source does), but its result cannot change the dump; only the write matters.
8. **`stof` double rounding.** Decimal → double → float32 can theoretically differ from
   decimal → float32 at a midpoint; the 20,000-token fuzz found none, and every frozen
   case passed.
9. **Invalid UTF-8** is decoded with `surrogateescape`; Hyprland would emit raw bytes that
   its own JSON consumer cannot decode either, so such a tree is outside the oracle.

## Files, tools, and lane writes

- Created (scratch): `mado-anims.py`, `dev_check.py`, `dev_edges.py`, `dev_edges2.py`,
  `dev_edges3.py`, `probe/` (formatting probes), `src/` (three pinned fetches),
  `receipts/runA.log`, `receipts/runB.log` under
  `/fast/scratch/hyaku/mado-r26/data/ExecAnimToolB/`.
- Lane writes: this report only. No `git`/`jj` write command was run in the lane or the
  fleet repo; no counter or harness file was edited; no other lane file was touched.
- Tool installs/upgrades: none.
- No subagent, task, workpool or background runtime was started (leaf seat).

Report: `.ufo/waves/round-26/w2/reports/ExecAnimToolB.md`
