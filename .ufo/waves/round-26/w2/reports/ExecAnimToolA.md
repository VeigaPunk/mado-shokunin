# ExecAnimToolA — C1 data seat A: mado-anims.py

Date: 2026-10-23. Wave: round-26 w2, data seat A. Verdict: **TARGET_MET on two consecutive fresh-seed counter runs
(41/41 each)**. The tool was not copied into the lane: the L1 lands the first unmodified file a data seat returns.

## Deliverable

| Field | Value |
|---|---|
| Path | `/fast/scratch/hyaku/mado-r26/data/ExecAnimToolA/mado-anims.py` |
| SHA-256 | `2beda3f7b1a5a7901f6a2cfc7e5b314b68ea9be8d0da27d3a92879946d9cab7d` |
| Size | 15,540 bytes |
| Runtime | python3 stdlib only (`glob`, `json`, `os`, `stat`, `struct`, `sys`) |
| CLI | `python3 -I mado-anims.py --home DIR` → one JSON array of two arrays on stdout, exit 0 |
| Reads | only paths under `--home`; no `os.environ`, no `/proc`, no network, no compositor |

The value the counter reports for the same bytes:
`tool=override:/fast/scratch/hyaku/mado-r26/data/ExecAnimToolA/mado-anims.py sha256:2beda3f7b1a5a7901f6a2cfc7e5b314b68ea9be8d0da27d3a92879946d9cab7d`.

## Receipts — last two counter runs (fresh seeds, unmodified tool)

Command, both runs (from `/home/vgpnk/Projects/shokunin/mado-shokunin`):

```sh
timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c1/count-v2.py 1b0b91e9 \
  --tool-file /fast/scratch/hyaku/mado-r26/data/ExecAnimToolA/mado-anims.py
```

Logs kept at `/fast/scratch/hyaku/mado-r26/data/ExecAnimToolA/run1.log` and `run2.log`.

### Run 1 — seed `6d96d225d31525cc`

```
counter c1-r26-v2 sha256:4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428 rev=1b0b91e9889cbf984b052f5de564db78330a72aa oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/fast/scratch/hyaku/mado-r26/data/ExecAnimToolA/mado-anims.py sha256:2beda3f7b1a5a7901f6a2cfc7e5b314b68ea9be8d0da27d3a92879946d9cab7d
seed=6d96d225d31525cc
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=base (unperturbed)
CASE C00   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:CATEGORY+BEZIER)
CASE C01   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:VARIABLE+ORDER+NEWSRC+BEZIER)
CASE C02   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:NEWSRC+UNSOURCED+BEZIER)
CASE C03   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:INVALID+CATEGORY+DISABLE+ORDER)
CASE C04   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:DISABLE+REBEZ+ROOT)
CASE C05   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:NEWSRC+SOURCED)
CASE C06   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ORDER+UNSOURCED)
CASE C07   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:NEWSRC+SPACING)
CASE C08   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:CATEGORY+ORDER+ROOT+BEZIER)
CASE C09   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:CATEGORY+NEWSRC+SPACING+VARIABLE)
CASE C10   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:DISABLE+VARIABLE)
CASE C11   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ORDER+SOURCED+BEZIER)
CASE C12   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:DISABLE+CATEGORY+VARIABLE)
CASE C13   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:SPACING+CATEGORY+ROOT)
CASE C14   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:SOURCED+BEZIER+VARIABLE)
CASE C15   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ROOT+VARIABLE+NEWSRC)
CASE C16   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:REBEZ+ROOT+COMMENT)
CASE C17   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ORDER+ROOT)
CASE C18   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:UNSOURCED+NEWSRC)
CASE C19   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:REBEZ+SOURCED)
CASE C20   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-bezier+rewrite-animation+rewrite-animation+UNSOURCED+INVALID)
CASE C21   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+rewrite-animation+INVALID)
CASE C22   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+NEWSRC+VARIABLE)
CASE C23   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+SPACING)
CASE C24   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-bezier+rewrite-animation+BEZIER)
CASE C25   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+rewrite-bezier+rewrite-animation+SPACING)
CASE C26   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:delete-animation+rewrite-animation+rewrite-animation+CATEGORY+SPACING)
CASE C27   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-bezier+delete-bezier+SPACING)
CASE C28   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+delete-bezier+rewrite-animation+SPACING)
CASE C29   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+DISABLE)
CASE C30   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:BEZIER+UNSOURCED+ROOT+CATEGORY+REBEZ)
CASE C31   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:COMMENT+VARIABLE+ROOT)
CASE C32   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:INVALID+SPACING+ORDER+NEWSRC+ROOT)
CASE C33   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:INVALID+BEZIER+SOURCED+NEWSRC+CATEGORY+UNSOURCED)
CASE C34   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:BEZIER+ORDER+NEWSRC+COMMENT+SPACING)
CASE C35   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:INVALID+REBEZ+SOURCED+CATEGORY+BEZIER+ROOT)
CASE C36   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:REBEZ+COMMENT+SOURCED+BEZIER+NEWSRC+ORDER)
CASE C37   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:ORDER+SOURCED+REBEZ+CATEGORY)
CASE C38   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:COMMENT+NEWSRC+DISABLE+ORDER)
CASE C39   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:ROOT+REBEZ+VARIABLE+NEWSRC+DISABLE)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C1-r26-v2 cases_pass=41/41 verdict=TARGET_MET
exit=0
```

### Run 2 — seed `a912923ee3a32be7`

```
counter c1-r26-v2 sha256:4ed70b5427f2e223a8d816679e6d1fad7d2e76d2ed57aa0fe7f135496e836428 rev=1b0b91e9889cbf984b052f5de564db78330a72aa oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441
tool=override:/fast/scratch/hyaku/mado-r26/data/ExecAnimToolA/mado-anims.py sha256:2beda3f7b1a5a7901f6a2cfc7e5b314b68ea9be8d0da27d3a92879946d9cab7d
seed=a912923ee3a32be7
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal nodes=35 beziers=6
ORACLE_VERSION commit=efb50993780079460b0cbed1363e2166a2de1d9f tag=v0.56.2
CASE BASE  PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=base (unperturbed)
CASE C00   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:SOURCED+SPACING)
CASE C01   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:COMMENT+ROOT+NEWSRC)
CASE C02   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:VARIABLE+CATEGORY+COMMENT+SOURCED)
CASE C03   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:NEWSRC+DISABLE+SOURCED)
CASE C04   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:UNSOURCED+INVALID+NEWSRC)
CASE C05   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:VARIABLE+UNSOURCED)
CASE C06   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ROOT+CATEGORY)
CASE C07   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:UNSOURCED+VARIABLE+SOURCED)
CASE C08   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:SPACING+INVALID+DISABLE)
CASE C09   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:DISABLE+UNSOURCED+REBEZ+BEZIER)
CASE C10   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:VARIABLE+BEZIER+CATEGORY+ROOT)
CASE C11   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:COMMENT+ORDER)
CASE C12   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:CATEGORY+UNSOURCED+ORDER)
CASE C13   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:BEZIER+NEWSRC+CATEGORY)
CASE C14   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:REBEZ+SPACING+CATEGORY)
CASE C15   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:NEWSRC+SPACING)
CASE C16   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:INVALID+ROOT+UNSOURCED)
CASE C17   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:INVALID+ORDER+SOURCED+UNSOURCED)
CASE C18   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:ROOT+ORDER+COMMENT)
CASE C19   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (APPEND:UNSOURCED+ORDER)
CASE C20   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+rewrite-animation+INVALID)
CASE C21   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+COMMENT+UNSOURCED)
CASE C22   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:delete-animation+REBEZ+INVALID)
CASE C23   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:delete-animation+ORDER+VARIABLE)
CASE C24   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-bezier+rewrite-animation+INVALID)
CASE C25   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-bezier+NEWSRC+UNSOURCED)
CASE C26   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:delete-animation+rewrite-animation+delete-animation+BEZIER)
CASE C27   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-bezier+delete-animation+ORDER)
CASE C28   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+SOURCED)
CASE C29   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (EDIT:rewrite-animation+rewrite-animation+rewrite-bezier+CATEGORY+ORDER)
CASE C30   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:NEWSRC+COMMENT+VARIABLE+ORDER+ROOT+BEZIER)
CASE C31   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:UNSOURCED+SOURCED+BEZIER+SPACING+NEWSRC+REBEZ)
CASE C32   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:INVALID+ORDER+VARIABLE)
CASE C33   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:COMMENT+DISABLE+ROOT+CATEGORY+SPACING+NEWSRC)
CASE C34   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:ORDER+BEZIER+CATEGORY+VARIABLE)
CASE C35   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:SPACING+REBEZ+ROOT)
CASE C36   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:SOURCED+CATEGORY+DISABLE+ROOT+SPACING)
CASE C37   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:SPACING+COMMENT+ROOT)
CASE C38   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:ROOT+CATEGORY+DISABLE+COMMENT+ORDER+INVALID)
CASE C39   PASS nodes missing=0 extra=0 beziers missing=0 extra=0 changed=yes (SYNTH:VARIABLE+BEZIER+ORDER+DISABLE+NEWSRC+ROOT)
HOST_SAFETY hyprland_coredumps_before=1337 after=1337 delta=0
PRED-C1-r26-v2 cases_pass=41/41 verdict=TARGET_MET
exit=0
```

## Rules implemented, with source anchors

`†` = anchor reached through the w1 source report (`w1/reports/SrcHyprctlAnims.md`, quotes re-checked there) or
`recon/anim-grammar.md` rather than opened by me in this seat. Everything else was opened in this seat: the fetched
`SrcAnimTree.bin`, `SrcAnimConfig-legacy-impl.bin`, `ParserUtils.cpp` (sha256
`86f21b761695571fc17f5a2ad68ddd30bf06d06d4d6a47ab443dc89ca511c2c0`, fetched for this seat), and the extracted
`hyprlang-0.6.8` / `hyprutils-0.14.2` trees under `/fast/scratch/hyaku/mado-r26/`.

| Rule | Anchor |
|---|---|
| 35 nodes, create order and parents (`__internal_fadeCTM`, `global`, … `specialWorkspaceOut`) | `src/config/shared/animation/AnimationTree.cpp:14-60` |
| Five seeded nodes: `global` 1/8/`default`, `__internal_fadeCTM` 1/5/`linear`, `borderangle`/`shadowangle`/`glowangle` 0/1/`default` | `AnimationTree.cpp:62-66` |
| Untouched node dumps as overridden=false, bezier="", speed 0, style "", enabled from the integer `-1` | hyprutils `src/animation/AnimationConfig.cpp:9-29` (createNode), `:35-51` (setConfigForNode) |
| Off-path write sets enabled 0, speed 1, bezier `default`, empty style and returns; later fields unread | `src/config/legacy/ConfigManager.cpp:1444-1447` |
| Node name is exact and case-sensitive; unknown/empty → no write | `ConfigManager.cpp:1432-1436`, hyprutils `AnimationConfig.cpp:31-33` |
| Enabled = `parseInt(field 1).value_or(0) == 1`; only exactly 1 continues | `ConfigManager.cpp:1438-1442` |
| `parseInt`: `0x` hex first, then `true`/`on`/`yes` and `false`/`off`/`no` prefixes, else whole-token base-10 `from_chars` | `src/config/shared/parserUtils/ParserUtils.cpp:133-149`; hyprutils `include/hyprutils/string/Numeric.hpp:25-55` |
| Speed: `isNumber(…, true)` then `stof`, `<= 0` or non-number → error before any write (locals 1.f/10.f never stored) | `ConfigManager.cpp:1452-1461`; hyprutils `src/string/String.cpp:49-84` |
| Bezier name must be an existing key, else "no such bezier" and no write | `ConfigManager.cpp:1463-1467`; hyprutils `src/animation/AnimationManager.cpp:88-95` |
| The write happens before style validation, so an invalid style is stored verbatim; field 5+ ignored, style is field 4 only | `ConfigManager.cpp:1469-1478` |
| `bezier =`: four required numeric points (`isNumber(…, true)`), non-empty sixth field → "too many arguments", empty name is a legal key, replace-or-insert | `ConfigManager.cpp:1389-1422` |
| Bezier map starts as `default` (0.0,0.75)/(0.15,1.0) plus `linear` (0,0)/(1,1) | hyprutils `AnimationManager.cpp:13, 40-46`; `ConfigManager.cpp:766-767` |
| Dump: node fields name/overridden/bezier/enabled/speed/style, bezier fields name/X0/Y0/X1/Y1, enabled as JSON truthiness of the stored int, speeds and points `{:.2f}` of the float value | `src/debug/HyprCtl.cpp:944-981`† |
| `speed` is a 32-bit float and the bezier points are float coordinates widened to double, so the printed digits are the rounded binary value | `ParserUtils`/`ConfigManager.cpp:1454, 1395-1417`; `hyprutils include/hyprutils/math/Vector2D.hpp:12-22`† |
| `animation`/`bezier` are unscoped handlers with `allowFlags=false`: exact left-hand side, fires at any category depth (including inside `animations { }`, which is an ordinary category) | `ConfigManager.cpp:612-613`; hyprlang `src/config.cpp:838-874` |
| Categories: `{` pushes the trimmed prefix, `}` pops, a stray close is an error, the stack is cleared at the end of every parsed file | hyprlang `src/config.cpp:892-920, 1044-1052` |
| Logical lines: join a line ending in `\` with the next after dropping spaces/tabs before the slash; a file ending on `\` is an error and stops the file | hyprlang `src/config.cpp:44-64, 1014-1031` |
| Comments: trim, truncate at the first `#` that is not doubled, `##` becomes one `#` and scanning continues after it; a line whose first non-space char is `#` is a directive | hyprlang `src/config.cpp:669-706` |
| Split on the first `=` and trim both sides; empty left side is an error | hyprlang `src/config.cpp:718-733` |
| `$variables`: expand up to 100 rounds on the right side and on the left side unless the line defines a variable; definitions are sorted by descending name length; recursion through values is re-expanded | hyprlang `src/config.cpp:736-812, 518-541` |
| After expansion, drop `\` before `{`, `}` and before another `\` | hyprlang `src/config.cpp:810-829` |
| `source =`: needs ≥2 characters, `~` becomes HOME, relative paths join the sourcing file's directory, glob matches are parsed inline in sorted order, directories are skipped, an inaccessible match stops the remaining matches, each sourced file starts with the parent's category stack and clears its own at EOF | `ConfigManager.cpp:1802-1854`; helpers `absolutePath` transcribed as in round-25 `tools/mado-binds.py` |
| Argument list: split on every comma with empty tokens kept and each token trimmed; past-the-end reads as "" | hyprutils `src/string/VarList.cpp:8-26`, `include/hyprutils/string/VarList.hpp:33-36` |
| `# hyprlang if/!if/endif/noerror` directives: if/endif nest and gate the following lines by variable truthiness; `noerror` has no tree effect | hyprlang `src/config.cpp:567-600, 674-679` |
| Errors never roll back earlier writes and never stop the file | hyprlang `src/config.cpp:1016-1039`; `recon/anim-grammar.md` §6 |

The reader half (source following, `$var` expansion, `##` escapes, multi-line joins, category stack, file-to-file
category reset) is the round-25 `tools/mado-binds.py` transcription, reused with the env seeding removed as the
data-seat contract requires.

## Falsification beyond the frozen counter (same tool bytes, same tree)

Two dev drivers in the same scratch dir, both run through the harness oracle by path:

```sh
cd /fast/scratch/hyaku/mado-r26/data/ExecAnimToolA
timeout 300 prlimit --as=4000000000:8000000000 -- python3 -I dev_base.py     # operator snapshot
timeout 600 prlimit --as=4000000000:8000000000 -- python3 -I dev_extra.py    # 11 hand-built trees
```

- `dev_base.py`: the 79-file operator snapshot (`digest sha256:fe1b2d8b…`) — `BASE MATCH`, 35 nodes, 6 beziers
  (the five omarchy curves plus the redefined `linear`).
- `dev_extra.py`: `DEV cases_pass=11/11`. Each case builds a fresh home, runs `oracle(home, …, ["animations"])` and
  the tool, and compares the parsed field sets:
  `anim_edges` (unknown/empty node, `1.0`, `0x1`, `true`, `online`, `none`, `2`, missing bezier, missing speed,
  `-4`, `+4`, `.5`, `5.`, `1e2`, styles with and without `%`, a comma inside the style, angle `once`/`loop`,
  `global … loop`, off-path with garbage trailing fields), `bezier_edges` (trailing comma, six fields, empty name,
  short, `.5`, negatives, `1e2`, redefined key, redefined `default`), `categories` (`animations { }` with
  `enabled = yes, please :)`, a nested `bezier`/`animation`, a `windowrule` line, a `decoration { }` block that still
  fires the handler, `animations:animation` which must not fire, `animations:enabled`, a nested `fade { }`),
  `continuation` (joins with and without trailing spaces, an unjoinable last line), `directives` (`# hyprlang
  if $flag`, `!$missing`, `noerror true/false`, an unclosed if), `escapes` (`##` in a style, `#` inside and after
  a style, `##` at the start of style), `formatting` (`0.005`, `0.015`, `1.005`, `2.675`, `-0`, `0.125`, `9.995`,
  `0.994`, `0.004`, `3.14159`), `noroot`, `offpath` (`0`, `0x2`, `0x0`, `false`, `yes`, `yesterday`), `sources`
  (glob with two files, relative source, `./` source, a missing source that must not stop later lines),
  `variables` (`$a = $b`, `$name` in the node slot, `$s` reused and redefined, `${s}` which is not a variable).

One consequence worth recording: `std::stof` overflow. `dev_overflow.py` builds
`animation = windows, 1, 99…9, b1` and `bezier = big, 99…9, 0.2, 0.3, 0.4` (60 nines, both pass `isNumber`).
The harness oracle returned `no nested instance within 40 s` for both: the nested Hyprland aborts before answering,
which is exactly the uncaught `std::out_of_range` that `recon/anim-grammar.md` §5 predicts. The tool drops the line
and writes nothing; the real behaviour is unobservable because the compositor never produces a dump.

## Host safety accounting

- Both counter runs: `HOST_SAFETY … delta=0`. Absolute count went 1335 → 1337 between run 1 and run 2.
- That +2 is my own `dev_overflow.py` probe, at 06:32:14 and 06:32:54: PIDs 2245463 and 2367290, `/usr/bin/Hyprland`
  with `-c …/data/ExecAnimToolA/devO-pmv1gx6g/tmp*/home/.config/hypr/hyprland.conf`, SIGABRT, `Storage: none`
  (metadata only, no core file). Read-only `coredumpctl list`/`info` used to attribute them; a peer
  (`MadoR26.RescoreK2DoNothing`) also spotted them and was answered with the same attribution.
- Every Hyprland instance I started went through `harness/oracle.py` (`oracle()` / the counters). `hyprctl` was
  never run directly, the live compositor was never dispatched to or reloaded, no `WAYLAND_DISPLAY` or
  `HYPRLAND_INSTANCE_SIGNATURE` was set or inherited, no `/dev/dri` node was touched by me, and every sandbox was
  torn down by the harness. No lane or fleet git/jj write was executed.
- Tool installs/upgrades: none.

## Known gaps

1. `{{ … }}` hyprlang expressions are not evaluated (`hyprlang src/config.cpp:756-802`). No line in the counter's
   generator and no `.conf` under the four config roots contains `{{` (grep over the roots is empty), and this
   seat's assignment names variables, comments and `##` only. A tree that used them in an `animation`/`bezier`
   line would diverge.
2. Environment variables are deliberately not seeded (contract). hyprlang copies the process environment into its
   variable table (`src/config.cpp:543-551, 1073-1074`), so in principle `$HOME` would expand inside a value; the
   tool leaves it literal. No config under the roots uses `$HOME`/`$PATH`; the counter cannot emit it.
3. `stof` overflow on a speed or a bezier point: the tool treats the line as an error and writes nothing, while
   Hyprland throws out of `parseLine` and (measured) aborts. Unobservable state, unreachable from the counter.
4. Variable substitution recomputes each `$name` inside a round instead of testing once per round, so it is slightly
   more eager than hyprlang. Both reach the same fixpoint unless a chain needs more than 100 rounds.
5. A root `hyprland.conf` whose last line ends in `\` is unscorable through this harness: the oracle appends
   `ORACLE_EXTRA` to its copy, so the slash joins the appended empty line, while the tool reads the unmodified
   tree. Both follow their input; the counter's writers never end a file on a backslash.
6. String escaping in the JSON uses `json.dumps` rather than a transcription of `escapeJSONStrings`
   (`src/helpers/MiscFunctions.cpp:85-105`†). The two agree on every byte the counter and the operator tree
   produce (ASCII, no control characters); non-ASCII would differ only in `\u` versus raw form, which parses to
   the same value.
7. Output order is a fixed tree order, not `unordered_map` order; the counter compares field sets, and `hyprctl`'s
   own order is unspecified, so this is not observable through the frozen comparison.
