# ExecArithToolB — hyprlang 0.6.8 `{{ ... }}` expressions in `tools/mado-binds.py`

**Status: TARGET_MET.** My last two frozen-counter runs, both on the final bytes and both on a
fresh seed, print `cases_pass=51/51 embed_hits=0 verdict=TARGET_MET` and `exit=0` (receipts
verbatim below). The file is the round-25 tool bytes (`9efa1136...`) plus hyprlang expression
evaluation; the 20 V3 cases and BASE still pass, so no round-25 behaviour was lost.

## Deliverable

| | |
|---|---|
| path | `/fast/scratch/hyaku/mado-r26/data/ExecArithToolB/mado-binds.py` |
| sha256 | `01751e133eddb927d60190e233d341c7bc1b774b5ca05a1ed5bab741e2b8179b` |
| size | 29524 bytes, 910 lines |
| CLI | `python3 -I mado-binds.py --home DIR` → one JSON array on stdout, exit 0 |
| imports | stdlib only: `glob json math os stat struct sys fractions.Fraction` |
| reads | `DIR/.config/hypr/hyprland.conf` and its `source =` closure, nothing else |
| round-25 original kept beside it | `mado-binds-r25.py`, sha256 `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950` |

The fifteen preserved functions (`trim`, `at`, `cvarlist`, `is_number`, `parse_key`,
`mod_mask`, `truthy`, `parse_comment`, `handle_bind`, `handle_unbind`, `handle_submap`,
`absolute_path`, `handle_source`, `parse_file`, `main`) are byte-identical to the round-25
bytes; `State`, `parse_line` and the escape helper are the only rewritten pieces, plus the new
binary32/expression block. `DISPATCHERS` is copied verbatim.

## Receipts (verbatim stdout, both on sha256 `01751e133eddb927d60190e233d341c7bc1b774b5ca05a1ed5bab741e2b8179b`)

Run A — seed `a44037d323676a9f`:

```text
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=1b0b91e9889cbf984b052f5de564db78330a72aa oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r26/data/ExecArithToolB/mado-binds.py sha256:01751e133eddb927d60190e233d341c7bc1b774b5ca05a1ed5bab741e2b8179b
seed=a44037d323676a9f
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal binds=192
CASE BASE           PASS oracle_binds=192 missing=0 extra=0 (unperturbed)
CASE A00            PASS oracle_binds=195 missing=0 extra=0 (ARITH[ws+unclosed+ws+resize]@sourced)
CASE A01            PASS oracle_binds=193 missing=0 extra=0 (ARITH[move+ws+desc]@sourced)
CASE A02            PASS oracle_binds=192 missing=0 extra=0 (ARITH[desc+move]@sourced)
CASE A03            PASS oracle_binds=194 missing=0 extra=0 (ARITH[resize+resize+unclosed]@sourced)
CASE A04            PASS oracle_binds=195 missing=0 extra=0 (ARITH[ws+var+var]@sourced)
CASE A05            PASS oracle_binds=196 missing=0 extra=0 (ARITH[ws+unclosed+resize+escaped]@root)
CASE A06            PASS oracle_binds=193 missing=0 extra=0 (ARITH[move+escaped]@sourced)
CASE A07            PASS oracle_binds=196 missing=0 extra=0 (ARITH[move+unclosed+ws+ws]@sourced)
CASE A08            PASS oracle_binds=194 missing=0 extra=0 (ARITH[escaped+resize+exec]@sourced)
CASE A09            PASS oracle_binds=193 missing=0 extra=0 (ARITH[desc+unclosed]@sourced)
CASE A10            PASS oracle_binds=195 missing=0 extra=0 (ARITH[ws+resize+ws+ws]@sourced)
CASE A11            PASS oracle_binds=196 missing=0 extra=0 (ARITH[ws+unclosed+unclosed+unclosed]@sourced)
CASE A12            PASS oracle_binds=194 missing=0 extra=0 (ARITH[resize+move+desc+move]@sourced)
CASE A13            PASS oracle_binds=193 missing=0 extra=0 (ARITH[move+escaped]@sourced)
CASE A14            PASS oracle_binds=193 missing=0 extra=0 (ARITH[exec+move+ws+escaped]@sourced)
CASE A15            PASS oracle_binds=194 missing=0 extra=0 (ARITH[desc+unclosed+unclosed+exec]@sourced)
CASE A16            PASS oracle_binds=196 missing=0 extra=0 (ARITH[unclosed+resize+exec+ws]@sourced)
CASE A17            PASS oracle_binds=194 missing=0 extra=0 (ARITH[move+unclosed+escaped+move]@sourced)
CASE A18            PASS oracle_binds=195 missing=0 extra=0 (ARITH[escaped+escaped+var]@sourced)
CASE A19            PASS oracle_binds=192 missing=0 extra=0 (ARITH[desc+move]@sourced)
CASE A20            PASS oracle_binds=194 missing=0 extra=0 (ARITH[desc+desc+unclosed]@sourced)
CASE A21            PASS oracle_binds=192 missing=0 extra=0 (ARITH[resize+move]@sourced)
CASE A22            PASS oracle_binds=194 missing=0 extra=0 (ARITH[move+escaped+exec]@sourced)
CASE A23            PASS oracle_binds=194 missing=0 extra=0 (ARITH[exec+var+move+resize]@sourced)
CASE A24            PASS oracle_binds=193 missing=0 extra=0 (ARITH[unclosed+move]@sourced)
CASE A25            PASS oracle_binds=194 missing=0 extra=0 (ARITH[ws+ws+desc]@sourced)
CASE A26            PASS oracle_binds=192 missing=0 extra=0 (ARITH[desc+move]@sourced)
CASE A27            PASS oracle_binds=193 missing=0 extra=0 (ARITH[escaped+resize]@sourced)
CASE A28            PASS oracle_binds=195 missing=0 extra=0 (ARITH[desc+ws+unclosed]@sourced)
CASE A29            PASS oracle_binds=192 missing=0 extra=0 (ARITH[move+exec+desc+desc]@sourced)
CASE VADD-0         PASS oracle_binds=193 missing=0 extra=0 (ADD into .config/hypr/bindings.conf)
CASE VADD-1         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
CASE VUNBIND-0      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=0 key='XF86AudioMute' keycode=0)
CASE VUNBIND-1      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=65 key='RIGHT' keycode=0)
CASE VVARIABLE-0    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vtolhwtb)
CASE VVARIABLE-1    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vrfwtevy)
CASE VSOURCE-0      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 12)
CASE VSOURCE-1      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 10)
CASE VGLOB-0        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VGLOB-1        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VUNSOURCED-0   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VUNSOURCED-1   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VCOMMENT-0     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .config/hypr/bindings.conf)
CASE VCOMMENT-1     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
CASE VSYNTH-0       PASS oracle_binds=14 missing=0 extra=0 (SYNTH tree binds=14 unbound=1 vars=2)
CASE VSYNTH-1       PASS oracle_binds=12 missing=0 extra=0 (SYNTH tree binds=12 unbound=1 vars=3)
CASE VREWRITE-0     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=73 key='' code=16; unbind mask=69 key='G' code=0; add exec)
CASE VREWRITE-1     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=64 key='mouse_up' code=0; unbind mask=8 key='XF86AudioRaiseVolume' code=0; add exec)
CASE VHARD-0        PASS oracle_binds=22 missing=0 extra=0 (HARD tree lines=31 binds=22 unbinds=1 vars=4)
CASE VHARD-1        PASS oracle_binds=24 missing=0 extra=0 (HARD tree lines=33 binds=24 unbinds=2 vars=4)
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
exit=0
```

Run B — seed `043289cfdbea7443`:

```text
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=1b0b91e9889cbf984b052f5de564db78330a72aa oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r26/data/ExecArithToolB/mado-binds.py sha256:01751e133eddb927d60190e233d341c7bc1b774b5ca05a1ed5bab741e2b8179b
seed=043289cfdbea7443
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal binds=192
CASE BASE           PASS oracle_binds=192 missing=0 extra=0 (unperturbed)
CASE A00            PASS oracle_binds=194 missing=0 extra=0 (ARITH[exec+ws+var+unclosed]@sourced)
CASE A01            PASS oracle_binds=194 missing=0 extra=0 (ARITH[unclosed+ws+unclosed]@sourced)
CASE A02            PASS oracle_binds=195 missing=0 extra=0 (ARITH[exec+var+move+resize]@sourced)
CASE A03            PASS oracle_binds=193 missing=0 extra=0 (ARITH[desc+move]@sourced)
CASE A04            PASS oracle_binds=193 missing=0 extra=0 (ARITH[exec+exec]@sourced)
CASE A05            PASS oracle_binds=192 missing=0 extra=0 (ARITH[desc+desc+desc+move]@sourced)
CASE A06            PASS oracle_binds=193 missing=0 extra=0 (ARITH[ws+move+unclosed+resize]@sourced)
CASE A07            PASS oracle_binds=195 missing=0 extra=0 (ARITH[escaped+var+var]@sourced)
CASE A08            PASS oracle_binds=194 missing=0 extra=0 (ARITH[exec+unclosed+exec]@sourced)
CASE A09            PASS oracle_binds=193 missing=0 extra=0 (ARITH[move+exec]@sourced)
CASE A10            PASS oracle_binds=194 missing=0 extra=0 (ARITH[resize+desc+resize+ws]@sourced)
CASE A11            PASS oracle_binds=192 missing=0 extra=0 (ARITH[resize+move]@sourced)
CASE A12            PASS oracle_binds=193 missing=0 extra=0 (ARITH[ws+move]@sourced)
CASE A13            PASS oracle_binds=193 missing=0 extra=0 (ARITH[desc+desc]@sourced)
CASE A14            PASS oracle_binds=195 missing=0 extra=0 (ARITH[var+unclosed+unclosed]@sourced)
CASE A15            PASS oracle_binds=196 missing=0 extra=0 (ARITH[exec+ws+var+desc]@sourced)
CASE A16            PASS oracle_binds=194 missing=0 extra=0 (ARITH[desc+unclosed+exec+ws]@sourced)
CASE A17            PASS oracle_binds=194 missing=0 extra=0 (ARITH[var+escaped+desc+resize]@sourced)
CASE A18            PASS oracle_binds=194 missing=0 extra=0 (ARITH[resize+var+resize+resize]@sourced)
CASE A19            PASS oracle_binds=195 missing=0 extra=0 (ARITH[resize+var+move+move]@sourced)
CASE A20            PASS oracle_binds=194 missing=0 extra=0 (ARITH[resize+var+desc+escaped]@sourced)
CASE A21            PASS oracle_binds=194 missing=0 extra=0 (ARITH[ws+ws]@sourced)
CASE A22            PASS oracle_binds=194 missing=0 extra=0 (ARITH[unclosed+resize]@sourced)
CASE A23            PASS oracle_binds=193 missing=0 extra=0 (ARITH[desc+var+resize]@sourced)
CASE A24            PASS oracle_binds=194 missing=0 extra=0 (ARITH[var+desc]@root)
CASE A25            PASS oracle_binds=194 missing=0 extra=0 (ARITH[ws+unclosed]@sourced)
CASE A26            PASS oracle_binds=193 missing=0 extra=0 (ARITH[resize+ws]@sourced)
CASE A27            PASS oracle_binds=192 missing=0 extra=0 (ARITH[resize+exec]@sourced)
CASE A28            PASS oracle_binds=194 missing=0 extra=0 (ARITH[exec+move+unclosed]@sourced)
CASE A29            PASS oracle_binds=195 missing=0 extra=0 (ARITH[var+escaped+escaped]@sourced)
CASE VADD-0         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
CASE VADD-1         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE VUNBIND-0      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=65 key='RETURN' keycode=0)
CASE VUNBIND-1      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=68 key='PERIOD' keycode=0)
CASE VVARIABLE-0    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vrwfwcbq)
CASE VVARIABLE-1    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vxgqxmrw)
CASE VSOURCE-0      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 9)
CASE VSOURCE-1      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 5)
CASE VGLOB-0        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VGLOB-1        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VUNSOURCED-0   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VUNSOURCED-1   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VCOMMENT-0     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
CASE VCOMMENT-1     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
CASE VSYNTH-0       PASS oracle_binds=13 missing=0 extra=0 (SYNTH tree binds=13 unbound=1 vars=3)
CASE VSYNTH-1       PASS oracle_binds=13 missing=0 extra=0 (SYNTH tree binds=13 unbound=1 vars=2)
CASE VREWRITE-0     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=64 key='V' code=0; unbind mask=8 key='XF86AudioLowerVolume' code=0; add movecurrentworkspacetomonit)
CASE VREWRITE-1     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=68 key='PERIOD' code=0; unbind mask=65 key='' code=12; add exec)
CASE VHARD-0        PASS oracle_binds=20 missing=0 extra=0 (HARD tree lines=29 binds=20 unbinds=2 vars=4)
CASE VHARD-1        PASS oracle_binds=25 missing=0 extra=0 (HARD tree lines=34 binds=25 unbinds=3 vars=4)
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
exit=0
```

Receipt files: `/fast/scratch/hyaku/mado-r26/data/ExecArithToolB/receipt-A.txt`,
`receipt-B.txt`. Both runs: 51 ` PASS ` lines, 0 ` FAIL ` lines,
`HOST_SAFETY ... delta=0`.

Baseline for comparison, same counter, round-25 bytes: `cases_pass=22/51` (BASE + all 20 V3 +
one ARITH), `exit=1` — every point gained here is expression handling.

## Rules implemented (source anchors)

hyprlang v0.6.8 = tag `v0.6.8`, commit `3a1c1b25b059dae2c6bbc46991562ba1158d125c`;
`src/config.cpp` sha256 `fa1b6898f2f1676de73220450f18f09603f0c3f8833e4c0a7c42c12aebe1de3e`
(fetched copy: `.ufo/waves/round-26/fetch/SrcHyprlangExpr.bin`). Hyprland v0.56.2 =
`efb50993780079460b0cbed1363e2166a2de1d9f`.

| Rule | Implementation | Source |
|---|---|---|
| `{{` is scanned only on an `=` line's right-hand side; the scan is `RHS.contains("{{")`, first `{{` guarded by an escape count, closed by the next `}}` | `expand_expressions()` | config.cpp:757-793 |
| a `{{` is active when the run of immediately preceding `\` is even; odd leaves it literal and the search continues | `expand_expressions()` inner loop | config.cpp:761-776 |
| a missing `}}` stops the scan and leaves the text literal (no error) | `if end == -1: break` | config.cpp:783, :793 |
| an expression is split by `CConstVarList(s, 0, 's', true)`: `std::isspace` delimiters, empty tokens dropped, tokens trimmed; index past the end reads `""` | `parse_expression()` uses `"".split()` + `at()` | config.cpp:627; hyprutils `ConstVarList.cpp:8-25`, `CVarList::operator[]` |
| token 1 must be exactly `+ - * /`, otherwise the line is an error; tokens 3+ are ignored (three-token grammar, no precedence, no parentheses, no juxtaposition) | `parse_expression()` | config.cpp:629-630 |
| an operand identical to a variable's name uses that variable's stored text; otherwise the token itself; both go through `std::stof` | `parse_expression()` | config.cpp:632-656 |
| `std::stof` is a glibc `strtof` prefix parse (trailing junk ignored, `inf`/`nan`/hex floats accepted); `invalid_argument` and ERANGE `out_of_range` both hit `catch (...)` and drop the line | `stof()`, `_scan_float()` | config.cpp:636-655, error return :786-788 |
| arithmetic is IEEE binary32 `+ - * /` with no divide-by-zero check; invalid operations give x86's default QNaN | `arith()`, `frac_to_f32()` | config.cpp:658-666 |
| the float is spliced back with `std::format("{}", value)` | `fmt_f32()`, `_render_magnitude()` | config.cpp:791 |
| `$name` substitution runs before the expression scan on the same RHS, longest name first, up to 100 iterations, and also rewrites text inside an escaped `{{` | `parse_line()` | config.cpp:732-752, :796-801 |
| a variable line stores the expanded RHS and returns before the escape pass | `parse_line()` → `set_var()` | config.cpp:805-806, :518-527 |
| non-variable lines then strip escapes: `\\` → `\`, `\{` → `{`, `\}` → `}`; other backslashes kept; the loop still advances after a `\\` pair and stops one character early | `strip_escapes()` | config.cpp:808-827 |
| the bind handler receives that post-strip text and only splits on commas | unchanged round-25 `handle_bind()` | ConfigManager.cpp:1492-1654 (split at :1554), HyprCtl.cpp:1078-1080 (`escapeJSONStrings`) |

Number formatting detail: libstdc++'s `std::format("{}", float)` renders the **shortest string**
(not the shortest digits) over both `f` and `e` styles, so a large exact integer prints its exact
digits (`1009043392`), `1e5` prints `1e+05`, `0.0001` prints `1e-04` while `0.0001234` prints
fixed, ties go to the closest decimal, then to an even last digit, then to fixed, and
`0.0f/0.0f` prints `-nan` (x86 default QNaN). `_render_magnitude()` implements exactly that.

## Development evidence (not receipts)

Everything below was measured while building; the two receipts above are the scored artifact.

1. **Float32 formatting and `std::stof`, differentially against libstdc++** (GCC 16.2.1, the
   version family that built `libhyprlang.so.0.6.8`, which was GCC 16.1.1):
   `compare.py` + `cmp.cpp` — 80,000 cases (40,000 random finite bit patterns across the whole
   binary32 range, 40,000 decimal-operand `a op b` triples), then 40,000 more with another seed,
   then 12,000 through the *delivered file's own* functions (`validate_tool.py`): **0 mismatches**.
   `arithprobe.cpp`: all 2,500 combinations of 25 sign/special values (±0, ±1, ±2, ±0.5, ±inf,
   ±nan, ±min-subnormal, ±max-finite, …) × 4 operators: **0 mismatches**.
   `stofprobe.cpp`: 37 hand-picked strings (`1e-45`, `1e-38`, `3.4028236e38`, `0x1p-148`,
   `0x1.8p-149`, `nan`, `-nan`, `2abc`, `0x`, `.5`, `5.`, `-0x`, …): **0 mismatches**.
2. **Oracle probes** (`probe.py`, ordinary `oracle()` + `run_tool()`): three hand-written trees,
   40 + 29 + 15 binds, covering valid/invalid/escaped/unclosed/nested/multi-pair expressions,
   variable-by-name vs `$var`, variables holding escaped or failing expressions, `inf`/`-nan`,
   `1e+05`/`1e+06`, `16777217`, `1009043392`, `8 - 4.8`, `17 / 4.3`, tabs, unicode, line
   continuations, 1-4 backslashes: **MATCH on all 18 fields**, 3/3 trees.
3. **Randomised stress** (`stress.py`, wider grammar than the counter's `arith_case`: variables,
   escaped variable lines, 1-4 backslashes, nested braces, multiple pairs, odd tokens
   `0x10/1e2/2abc/inf/nan/-2/.5/5./1,`, expression in the mod field): **184 configs, 0 diffs**
   after fixes. The stress found four real defects that the counter's own generator does not
   reach, all fixed and re-verified: the escape pass must still run its loop increment after
   collapsing `\\` (config.cpp:816-819), `std::stof("nan")` is a *positive* NaN and arithmetic
   propagates the operand NaN rather than the default QNaN, a product must not re-apply the sign,
   and `-0 / positive` is `-0`.

## Known gaps

- **Environment variables are not seeded into the variable list.** hyprlang's `clearState`
  copies `environ` (so `{{HOME + 1}}` looks up `HOME`); this tool deliberately does not read
  `os.environ`. The counter's tool sandbox is `--clearenv` with `PATH=/usr/bin`,
  `HOME=/snap/home`, and none of the four config roots references `$PATH`/`$HOME`/`$USER`/
  `$SHELL`/`$XDG*` (grep checked), so the score is unaffected; a tree that references a numeric
  environment variable would differ.
- The ERANGE rule for subnormals ("inexact subnormal throws, exactly representable subnormal
  does not") is inferred from glibc behaviour and validated on the 37 edge strings; it is not
  quoted from a glibc source.
- `# hyprlang noerror` stays a no-op (as in round 25): it suppresses the diagnostic only, never
  makes a rejected line apply — config.cpp:1034, :1038.
- `parseVariable`'s dynamic re-parse of lines that contain a variable
  (`linesContainingVar`, config.cpp:529-537) is not modelled; `parseFile` calls
  `parseLine(line.value())` with the default `dynamic = false` (config.cpp:1032), so Hyprland's
  file parse never triggers it. `parseRawStream`/`hyprctl keyword` (:1059, :1065) do, and are
  out of scope for PRED-C2-r26.
- `_render_magnitude()` reproduces libstdc++'s shortest-string rule empirically (12k+40k+80k
  values); I have no normative quote for the fixed-vs-scientific tie-break, only measurements.
- The tool models the bind table only; it makes no claim about categories, keywords, or any
  non-bind config key.

## Exact commands

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 1b0b91e9:tools/mado-binds.py \
  > /fast/scratch/hyaku/mado-r26/data/ExecArithToolB/mado-binds.py     # round-25 start point
cd /home/vgpnk/Projects/shokunin/mado-shokunin
timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py \
  1b0b91e9 --tool-file /fast/scratch/hyaku/mado-r26/data/ExecArithToolB/mado-binds.py
# … the same command twice more, output kept in receipt-A.txt / receipt-B.txt
cd /fast/scratch/hyaku/mado-r26/data/ExecArithToolB
timeout 600 prlimit --as=4000000000 -- python3 -I compare.py 40000 12345678
timeout 900 prlimit --as=4000000000 -- python3 -I validate_tool.py 6000 c0ffee
timeout 300 prlimit --as=4000000000:8000000000 -- python3 -I probe.py mado-binds.py case1.conf
timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I stress.py mado-binds.py 20 555666
```

## Surfaces

Wrote only `/fast/scratch/hyaku/mado-r26/data/ExecArithToolB/*` (tool, C++ probes, harness
scripts, probe configs, receipts) and this report. No lane file, counter, harness or oracle was
edited; no git/jj write command ran; no package was installed; Hyprland was started only through
`harness/oracle.py` (the counters), and both receipts report `delta=0` Hyprland coredumps.

Report: `.ufo/waves/round-26/w2/reports/ExecArithToolB.md`
