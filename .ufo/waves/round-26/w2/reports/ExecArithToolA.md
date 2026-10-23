# ExecArithToolA — C2 data seat A: hyprlang `{{...}}` evaluation in `mado-binds.py`

Round-26 w2, item ExecArithToolA. Rule file `.ufo/waves/round-26/registration.md` was not edited;
lane tip `1b0b91e9` (`1b0b91e9889cbf984b052f5de564db78330a72aa`) was read only. Started from the
round-25 tool bytes (`git show 1b0b91e9:tools/mado-binds.py`, sha256
`9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950`, 496 lines).

## Result

| item | value |
|---|---|
| deliverable | `/fast/scratch/hyaku/mado-r26/data/ExecArithToolA/mado-binds.py` |
| sha256 | `06112dc84d8c65df008062b9b38be20ce021ef31551357f5d51fad9f8effe18c` |
| size | 28,837 bytes, 863 lines, python3 stdlib only (`glob json math os stat struct sys fractions`) |
| CLI | `python3 -I mado-binds.py --home DIR` → one JSON array on stdout, exit 0 |
| last two counter runs (fresh seeds, delivered bytes) | `cases_pass=51/51 embed_hits=0 verdict=TARGET_MET`, `exit=0` (runs 3 and 4 below) |
| verdict | **DATA SEAT C2-A met — 51/51 with the delivered bytes** |

Both receipts were produced by the frozen counter at lane rev `1b0b91e9` with
`--tool-file` pointing at the delivered file; the counter's own sha256, `oracle.py` sha256 and
`count-v3.py` sha256 pins matched in every run.

## Rules implemented, with source anchors

Everything above `class State` is new; `parse_line` gained the expression loop and the
`100`-iteration error; `State.get_var` now reads the variable vector only (the vector already holds
the environment copy). `handle_bind`, `handle_unbind`, `handle_submap`, `handle_source`,
`parse_comment`, `parse_file`, `unescape_braces`, `cvarlist`, `mod_mask`, `parse_key` are untouched.

| rule | source | tool |
|---|---|---|
| `{{`/`}}` are recognised only on the RHS of a line with `=`, after `$name` substitution, in a `while RHS.contains("{{")` loop | hyprlang v0.6.8 `src/config.cpp:755-794` | `parse_line:767-778` |
| start scan counts preceding backslashes; odd = literal, keep looking; index 0 is always active; a `{{` with no later `}}` breaks the loop and leaves text literal (no error) | `config.cpp:758-779`, `:782-783`, `:792-793` | `expression_start:492-504`, `parse_line:769-771` |
| an evaluated pair that fails rejects the whole line (no handler call, no variable store, no escape strip) | `config.cpp:786-788` | `parse_line:774-777` |
| expression = whitespace tokens (`std::isspace`, empty dropped); token 1 must be exactly `+ - * /`; tokens 3+ ignored; no precedence, no parentheses | `config.cpp:624-630` | `split_ws:387`, `parse_expression:477-490` |
| operands: token equal to a variable *name* → parse the variable's stored value, else parse the token; failure → line rejected | `config.cpp:632-656` | `expr_operand:403-409` |
| operand parse is C `strtof` prefix semantics: hex floats (`0x10`→16, `0x1p3`→8), `inf`/`infinity`/`nan` spellings, trailing junk ignored (`2abc`→2, `1,`→1), overflow and inexact subnormals are `out_of_range` (both throw → line rejected) | `config.cpp:640-645`, `:650-655` (lib `std::stof`) | `strtof:232-331` |
| arithmetic is binary32: exact operand fractions, one operation, round-to-nearest-even once; `5/2`→`2.5`, `1/0`→`inf`, `-1/0`→`-inf`, `0/0`→`-nan`, `-0+0`→`0` | `config.cpp:635-664` | `f32_round:205-230`, `expr_*:412-471` |
| the result is spliced in with `std::format("{}", RESULT.value())` | `config.cpp:791` | `format_f32:358-384` |
| escape strip on non-variable lines only (`\\`→`\`, `\{`→`{`, `\}`→`}`); variable lines store the text as it stands | `config.cpp:805-827` | existing `unescape_braces:146` (unchanged), `parse_line:782-785` |
| `$name` loop: up to 100 passes over all variables, longest name first; a match on the 100th pass is the error `Expanding variables exceeded max iteration limit` | `config.cpp:732-753`, `:799-801` | `parse_line:756-781` |
| a redefinition replaces the existing variable entry (also when it shadows an environment name) | `config.cpp:518-527` | `State.set_var`, `State.lookup:512-521` |

### The `std::format("{}", float)` rule

`libhyprlang` was built by GCC 16.1.1 and links the host's libstdc++ (GCC 16.2.1). The formatter is
`__floating_to_chars_shortest(..., chars_format{})` — the "plain" mode:

- shortest round-trip digits from Ryu;
- notation, with `L` digits and Ryu exponent `E` (`value = mantissa * 10**E`):
  `lower = -(L+3)`, `upper = 5`, both tightened by 1 when `L == 1`; fixed when
  `lower <= E <= upper`, otherwise scientific (`e±dd`, at least two exponent digits);
- fixed with `E >= 0` prints the **exact integer** value (not `mantissa * 10**E`), which is why
  `1234567936` stays `1234567936` while `123456790` would be the shortest form.

Source: `libstdc++-v3/src/c++17/floating_to_chars.cc`, `__floating_to_chars_shortest` at `:1099`,
plain-mode rule at `:1141-1155` (`int lower_bound = -(mantissa_length + 3);` `:1146`,
`int upper_bound = 5;` `:1147`, the compare at `:1153`), scientific writer at `:1158-1175`, and the
exact-integer fixed path at `:1177-1253` (`... we may need to print more digits of the IEEE mantissa
...` `:1180-1189`, `ryu::d2fixed_buffered_n(value, 0, first)` `:1253`). Fetched copy:
`dev/probe/ftc.cc` sha256 `8b76e44f39f15fc39f34de9ade5d9388786c4f8eb6409b632063d4064ef1d75e`.
`to_chars(first,last,value)` resolves to this mode at `:1774-1776`; `std::format("{}", float)`
printed the same string in every probe row.

Special values, measured on this host (not guessed): `inf`, `-inf`, `nan`, `-nan`, `-0`; invalid
operations (`0/0`, `inf/inf`, `inf-inf`, `inf*0`) produce `0xFFC00000` → `-nan`; a NaN operand is
propagated quieted, and when *both* operands are NaN the result is the right operand for `+` and
`*` and the left operand for `-` and `/` (GCC's instruction shape). All of this is in
`expr_add/sub/mul/div`.

## Evidence (all exercised, nothing inferred)

1. **Formatter vs libstdc++.** C++ probe `dev/probe/fmtin.cpp` calls `std::to_chars` on binary32 bit
   patterns fed on stdin; the Python rule in `format_f32` matched **78,756/78,756** patterns
   (structured digit×exponent grid plus random finite patterns, including subnormals, `1e±38`,
   `3.4e38`, `16777217`, `100000`, `0.0001`, `1/3`).
2. **Arithmetic vs the hardware.** `dev/probe/ops.cpp` computes `a op b` in `float` and prints the
   result's bits and `to_chars` text; `expr_add/sub/mul/div` matched **165,444/165,444** cases over
   all four operators (30k random pairs per operator, all special×special pairs, SNaN/QNaN payload
   pairs, ±0 and subnormal edges).
3. **Operand parsing.** `dev/probe/stofin.cpp` wraps `std::stof`; `strtof` agreed on **6,083/6,084**
   tokens (numeric, hex, inf/nan, junk suffixes, overflow, subnormal underflow). The one difference
   is listed under known gaps.
4. **Oracle, targeted tree T1** (`dev/trees/T1`, 90 config lines → 70 binds): escape parity, `{\{`,
   `\{\{`, `\\{{`, unclosed pairs, an unclosed pair in front of a valid one, nested `{{ {{…}} + 3 }}`
   (rejected), multiple pairs concatenating (`{{1 + 2}}{{3 + 4}}` → `37`), quoted braces, `inf`,
   `-nan`, `-0`, `1e-04`, `1e+05`, `123456`, `1234567`, `1234567936`, `1304247936`, `2147483648`,
   `0.00012345`, `0.0001`, `8.70000076`, `25.942001`, variable chains (`{{MY_VAR + 2}}` →
   `{{EXPR_VAR - 4}}` = 1335), `$var` form, escaped-variable interpolation, a variable whose
   assignment fails (stays undefined), a non-numeric variable, a self-referential variable
   (100-iteration limit → bind dropped), a failing pair after a good one on the same line.
   Result: `oracle_binds=70 tool_binds=70 missing=0 extra=0`, oracle run through
   `harness/oracle.py`'s `oracle()` only.
5. **Oracle, targeted tree T2** (`dev/trees/T2`, handlers other than `bind`): expression in a
   `source =` line (`source = ./$SUFFIX{{$N + 0}}.conf` → sources `extra1.conf`, whose bind with
   `{{5 * 5}}` appears), expression in `submap = {{1 + 2}}` (following binds carry `submap="3"`),
   `bindl`/`bindr`/`binde` flags, a failing expression in a `bindd` description (line dropped),
   `{{5 / 0}}` → `inf`. Result: `oracle_binds=8 tool_binds=8 missing=0 extra=0`.
6. **Frozen counter, delivered bytes.** Runs 3 and 4 below, seeds `9abcb0ad980a420c` and
   `2a6a80da49bc4da1`, both `51/51`, `embed_hits=0`, `HOST_SAFETY … delta=0`, `exit=0`. Runs 1 and 2
   (`dea1a957…`, seeds `9cd80eec4c362258` / `0ac43876a63ebbf6`) were also `51/51 TARGET_MET`; the
   only later change was a docstring typo fix, which is why the delivered sha256 differs.
7. **Counter sensitivity probe (informative, not a claim about the counter's adequacy).** A mutant
   replacing the exact-integer fixed expansion with `mantissa * 10**E` still scored `51/51`
   (`dev/mut1.txt`, seed `9f92ee67ed40923e`), while the same mutant fails tree T1 with
   `missing=4 extra=4` (args `1234568000`/`1304247900`/`2147483600`/`123456790` instead of
   `1234567936`/`1304247936`/`2147483648`/`123456792`). The counter's ARITH generator draws
   integers 0–40 and floats 0–20, so it never reaches 2^24; the delivered rule is nonetheless the
   correct one and is covered by evidence 1 and 4.

### Receipts, verbatim (stdout of the frozen counter, including `exit=`)

Run 3 — seed `9abcb0ad980a420c`:

```text
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=1b0b91e9889cbf984b052f5de564db78330a72aa oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r26/data/ExecArithToolA/mado-binds.py sha256:06112dc84d8c65df008062b9b38be20ce021ef31551357f5d51fad9f8effe18c
seed=9abcb0ad980a420c
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal binds=192
CASE BASE           PASS oracle_binds=192 missing=0 extra=0 (unperturbed)
CASE A00            PASS oracle_binds=194 missing=0 extra=0 (ARITH[desc+exec]@sourced)
CASE A01            PASS oracle_binds=193 missing=0 extra=0 (ARITH[desc+desc+move]@sourced)
CASE A02            PASS oracle_binds=196 missing=0 extra=0 (ARITH[escaped+desc+exec+exec]@sourced)
CASE A03            PASS oracle_binds=194 missing=0 extra=0 (ARITH[exec+resize+ws]@sourced)
CASE A04            PASS oracle_binds=195 missing=0 extra=0 (ARITH[desc+escaped+escaped+var]@sourced)
CASE A05            PASS oracle_binds=195 missing=0 extra=0 (ARITH[escaped+var+move+resize]@root)
CASE A06            PASS oracle_binds=194 missing=0 extra=0 (ARITH[exec+var+escaped]@sourced)
CASE A07            PASS oracle_binds=195 missing=0 extra=0 (ARITH[exec+ws+escaped]@sourced)
CASE A08            PASS oracle_binds=193 missing=0 extra=0 (ARITH[move+desc+ws+ws]@sourced)
CASE A09            PASS oracle_binds=194 missing=0 extra=0 (ARITH[var+exec]@sourced)
CASE A10            PASS oracle_binds=195 missing=0 extra=0 (ARITH[escaped+exec+exec+ws]@sourced)
CASE A11            PASS oracle_binds=195 missing=0 extra=0 (ARITH[var+desc+exec]@sourced)
CASE A12            PASS oracle_binds=193 missing=0 extra=0 (ARITH[move+desc]@sourced)
CASE A13            PASS oracle_binds=193 missing=0 extra=0 (ARITH[desc+move+escaped]@sourced)
CASE A14            PASS oracle_binds=195 missing=0 extra=0 (ARITH[move+resize+desc+escaped]@root)
CASE A15            PASS oracle_binds=194 missing=0 extra=0 (ARITH[var+var]@sourced)
CASE A16            PASS oracle_binds=192 missing=0 extra=0 (ARITH[exec+move]@sourced)
CASE A17            PASS oracle_binds=195 missing=0 extra=0 (ARITH[ws+var+unclosed]@sourced)
CASE A18            PASS oracle_binds=195 missing=0 extra=0 (ARITH[unclosed+resize+desc+unclosed]@sourced)
CASE A19            PASS oracle_binds=196 missing=0 extra=0 (ARITH[unclosed+escaped+resize+move]@sourced)
CASE A20            PASS oracle_binds=193 missing=0 extra=0 (ARITH[var+resize]@sourced)
CASE A21            PASS oracle_binds=192 missing=0 extra=0 (ARITH[move+move]@sourced)
CASE A22            PASS oracle_binds=195 missing=0 extra=0 (ARITH[desc+move+move+escaped]@sourced)
CASE A23            PASS oracle_binds=195 missing=0 extra=0 (ARITH[escaped+unclosed+unclosed]@sourced)
CASE A24            PASS oracle_binds=194 missing=0 extra=0 (ARITH[exec+exec+move+resize]@sourced)
CASE A25            PASS oracle_binds=194 missing=0 extra=0 (ARITH[ws+move+exec]@sourced)
CASE A26            PASS oracle_binds=194 missing=0 extra=0 (ARITH[escaped+resize]@sourced)
CASE A27            PASS oracle_binds=193 missing=0 extra=0 (ARITH[move+exec+var]@sourced)
CASE A28            PASS oracle_binds=193 missing=0 extra=0 (ARITH[unclosed+ws]@sourced)
CASE A29            PASS oracle_binds=192 missing=0 extra=0 (ARITH[desc+exec]@sourced)
CASE VADD-0         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
CASE VADD-1         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
CASE VUNBIND-0      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=0 key='PRINT' keycode=0)
CASE VUNBIND-1      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=76 key='R' keycode=0)
CASE VVARIABLE-0    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vmwkpzjw)
CASE VVARIABLE-1    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vfiozcip)
CASE VSOURCE-0      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 8)
CASE VSOURCE-1      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 18)
CASE VGLOB-0        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VGLOB-1        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VUNSOURCED-0   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VUNSOURCED-1   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VCOMMENT-0     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
CASE VCOMMENT-1     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
CASE VSYNTH-0       PASS oracle_binds=14 missing=0 extra=0 (SYNTH tree binds=14 unbound=1 vars=3)
CASE VSYNTH-1       PASS oracle_binds=11 missing=0 extra=0 (SYNTH tree binds=11 unbound=1 vars=2)
CASE VREWRITE-0     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=68 key='PERIOD' code=0; unbind mask=64 key='ESCAPE' code=0; add sendshortcut)
CASE VREWRITE-1     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=0 key='XF86AudioLowerVolume' code=0; unbind mask=65 key='G' code=0; add movetoworkspacesilent)
CASE VHARD-0        PASS oracle_binds=18 missing=0 extra=0 (HARD tree lines=29 binds=18 unbinds=2 vars=4)
CASE VHARD-1        PASS oracle_binds=18 missing=0 extra=0 (HARD tree lines=28 binds=18 unbinds=3 vars=4)
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
exit=0
```

Run 4 — seed `2a6a80da49bc4da1`:

```text
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=1b0b91e9889cbf984b052f5de564db78330a72aa oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/fast/scratch/hyaku/mado-r26/data/ExecArithToolA/mado-binds.py sha256:06112dc84d8c65df008062b9b38be20ce021ef31551357f5d51fad9f8effe18c
seed=2a6a80da49bc4da1
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal binds=192
CASE BASE           PASS oracle_binds=192 missing=0 extra=0 (unperturbed)
CASE A00            PASS oracle_binds=194 missing=0 extra=0 (ARITH[var+escaped]@sourced)
CASE A01            PASS oracle_binds=192 missing=0 extra=0 (ARITH[desc+ws+move]@sourced)
CASE A02            PASS oracle_binds=195 missing=0 extra=0 (ARITH[ws+escaped+var]@sourced)
CASE A03            PASS oracle_binds=192 missing=0 extra=0 (ARITH[resize+move+resize]@sourced)
CASE A04            PASS oracle_binds=195 missing=0 extra=0 (ARITH[ws+escaped+unclosed]@sourced)
CASE A05            PASS oracle_binds=196 missing=0 extra=0 (ARITH[var+ws+ws+var]@sourced)
CASE A06            PASS oracle_binds=196 missing=0 extra=0 (ARITH[ws+ws+var+exec]@sourced)
CASE A07            PASS oracle_binds=194 missing=0 extra=0 (ARITH[exec+desc+escaped+escaped]@sourced)
CASE A08            PASS oracle_binds=194 missing=0 extra=0 (ARITH[desc+escaped+resize+resize]@sourced)
CASE A09            PASS oracle_binds=195 missing=0 extra=0 (ARITH[var+ws+ws]@sourced)
CASE A10            PASS oracle_binds=194 missing=0 extra=0 (ARITH[move+escaped+move+resize]@sourced)
CASE A11            PASS oracle_binds=195 missing=0 extra=0 (ARITH[move+escaped+desc]@sourced)
CASE A12            PASS oracle_binds=193 missing=0 extra=0 (ARITH[unclosed+ws]@root)
CASE A13            PASS oracle_binds=194 missing=0 extra=0 (ARITH[move+ws+move+desc]@sourced)
CASE A14            PASS oracle_binds=195 missing=0 extra=0 (ARITH[unclosed+escaped+unclosed]@sourced)
CASE A15            PASS oracle_binds=194 missing=0 extra=0 (ARITH[move+var+move]@sourced)
CASE A16            PASS oracle_binds=193 missing=0 extra=0 (ARITH[move+var+resize]@sourced)
CASE A17            PASS oracle_binds=195 missing=0 extra=0 (ARITH[escaped+var+move]@sourced)
CASE A18            PASS oracle_binds=195 missing=0 extra=0 (ARITH[escaped+unclosed+unclosed]@sourced)
CASE A19            PASS oracle_binds=193 missing=0 extra=0 (ARITH[move+move]@sourced)
CASE A20            PASS oracle_binds=194 missing=0 extra=0 (ARITH[exec+exec]@sourced)
CASE A21            PASS oracle_binds=193 missing=0 extra=0 (ARITH[resize+move+resize]@sourced)
CASE A22            PASS oracle_binds=193 missing=0 extra=0 (ARITH[exec+escaped]@sourced)
CASE A23            PASS oracle_binds=194 missing=0 extra=0 (ARITH[unclosed+escaped]@sourced)
CASE A24            PASS oracle_binds=194 missing=0 extra=0 (ARITH[var+desc+ws]@sourced)
CASE A25            PASS oracle_binds=193 missing=0 extra=0 (ARITH[exec+ws+desc+desc]@sourced)
CASE A26            PASS oracle_binds=194 missing=0 extra=0 (ARITH[escaped+escaped+exec+move]@sourced)
CASE A27            PASS oracle_binds=195 missing=0 extra=0 (ARITH[unclosed+escaped+var]@sourced)
CASE A28            PASS oracle_binds=193 missing=0 extra=0 (ARITH[ws+exec]@sourced)
CASE A29            PASS oracle_binds=196 missing=0 extra=0 (ARITH[unclosed+escaped+unclosed+var]@sourced)
CASE VADD-0         PASS oracle_binds=193 missing=0 extra=0 (ADD into .config/hypr/bindings.conf)
CASE VADD-1         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
CASE VUNBIND-0      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=73 key='TAB' keycode=0)
CASE VUNBIND-1      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=68 key='R' keycode=0)
CASE VVARIABLE-0    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vbgxsmqg)
CASE VVARIABLE-1    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vriygfym)
CASE VSOURCE-0      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 13)
CASE VSOURCE-1      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 11)
CASE VGLOB-0        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VGLOB-1        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VUNSOURCED-0   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VUNSOURCED-1   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VCOMMENT-0     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .config/hypr/bindings.conf)
CASE VCOMMENT-1     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE VSYNTH-0       PASS oracle_binds=14 missing=0 extra=0 (SYNTH tree binds=14 unbound=1 vars=2)
CASE VSYNTH-1       PASS oracle_binds=11 missing=0 extra=0 (SYNTH tree binds=11 unbound=1 vars=2)
CASE VREWRITE-0     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=68 key='H' code=0; unbind mask=73 key='' code=12; add resizeactive)
CASE VREWRITE-1     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=73 key='TAB' code=0; unbind mask=68 key='COMMA' code=0; add exec)
CASE VHARD-0        PASS oracle_binds=19 missing=0 extra=0 (HARD tree lines=30 binds=19 unbinds=2 vars=4)
CASE VHARD-1        PASS oracle_binds=27 missing=0 extra=0 (HARD tree lines=33 binds=27 unbinds=2 vars=4)
HOST_SAFETY hyprland_coredumps_before=1338 after=1338 delta=0
PRED-C2-r26 cases_pass=51/51 embed_hits=0 verdict=TARGET_MET
exit=0
```

Receipt files: `run3.txt` sha256 `ea3f6b069dde0c947799f810329fa4b7e90a79b90b2cd4bbb2cbeb73f2f1cef5`, `run4.txt`
sha256 `afa8e31b12710dee8fbb00a72114278a7c09bc5f84787a3b64bbe11184b61d94` (both under
`/fast/scratch/hyaku/mado-r26/data/ExecArithToolA/`).

## Commands

```sh
# deliverable and hashes
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 1b0b91e9:tools/mado-binds.py \
  > /fast/scratch/hyaku/mado-r26/data/ExecArithToolA/mado-binds.py      # sha256 9efa1136… (round-25)
sha256sum /fast/scratch/hyaku/mado-r26/data/ExecArithToolA/mado-binds.py  # 06112dc8… (delivered)

# frozen counter (each run, fresh seed, from the lane root)
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 \
  prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 1b0b91e9 \
  --tool-file /fast/scratch/hyaku/mado-r26/data/ExecArithToolA/mado-binds.py

# oracle A/B on a hand-built tree (only harness/oracle.py starts Hyprland)
rm -rf data/ExecArithToolA/work && cd /fast/scratch/hyaku/mado-r26 && timeout 300 \
  prlimit --as=4000000000:8000000000 -- python3 -I data/ExecArithToolA/dev/cmp.py \
  data/ExecArithToolA/dev/trees/T1 data/ExecArithToolA/mado-binds.py

# libstdc++ / hardware probes (g++ 16.2.1, existing; nothing installed)
g++ -std=c++23 -O1 -o fmtin  dev/probe/fmtin.cpp   # to_chars on bit patterns from stdin
g++ -std=c++23 -O1 -o ops    dev/probe/ops.cpp     # a op b in float + to_chars
g++ -std=c++23 -O1 -o stofin dev/probe/stofin.cpp  # std::stof wrapper
```

## Known gaps and residual risks

1. **glibc ERANGE boundary.** `strtof` treats any *inexact* conversion below the smallest normal
   (2^-126) as `out_of_range`, matching glibc on 6,083/6,084 probe tokens. The single difference is
   `1.1754943e-38` (glibc: `out_of_range`; tool: `1.1754944e-38`), a 9-digit decimal within
   ~9e-47 of 2^-126 where glibc's own fast path flags underflow. Unreachable from counter inputs
   (integers 0–40, floats 0–20, 1–3 decimals; products/sums stay under 1600) and from any realistic
   config value.
2. **Environment copy.** `State` still seeds the hyprlang variable vector from `os.environ`
   (hyprlang `clearState`, `config.cpp:1073-1074`, does exactly that), inherited from round-25.
   Nothing branches on it and the counter's tool sandbox clears the environment to `PATH`/`HOME`, so
   it carries no case identity; but the oracle's Hyprland environment carries extra names
   (`XDG_RUNTIME_DIR`, `WLR_*`, `HYPRLAND_*`) and a different `HOME`. A config that interpolated one
   of those names into a bind value would diverge (`/snap/home` vs the oracle home). BASE, all 20 V3
   cases and all 30 ARITH cases do not.
3. **Typed config keys are not modelled** (the tool never did). An expression that produces a value
   an int key rejects (`2.5`, `1e+05`, `inf`) makes hyprlang drop that line; for non-bind keys this
   is invisible to `hyprctl binds -j`, and for bind lines the tool already drops on the expression
   itself. Not observable in the bind table, so not implemented.
4. **Counter coverage vs implementation.** The frozen counter cannot see two implemented rules:
   the exact-integer fixed formatting above 2^24 (mutant evidence in item 7) and the case where an
   escaped pair precedes a valid pair on the same line (`\{{1 + 2}} {{3 + 4}}`). Both are covered by
   the libstdc++ fuzz and tree T1, not by the 51 cases. A future counter with larger operands would
   test them.
5. **`{{` inside a `$`-substituted value at the 100-iteration limit** is implemented as hyprlang's
   error (line dropped) but is unexercised by the counter; only the self-referential `$LOOP` case in
   T1 exercises it.
6. **Not re-derived here:** the 18-field JSON shape, dispatcher table, `handleBind` grammar,
   `unbind`/`submap`/`source` semantics are round-25 code, unchanged and already covered by the
   counter's BASE and V3 halves in these runs.

## Surfaces touched, safety, tooling

- Wrote exactly two things outside scratch: this report and (as required by the data-seat contract)
  nothing in the lane — the deliverable lives only under
  `/fast/scratch/hyaku/mado-r26/data/ExecArithToolA/`, with development artifacts under its `dev/`
  subdirectory (probe sources/binaries, both trees, `cmp.py`, the round-25 baseline copy, the mutant
  receipt).
- No git/jj write in the lane or the fleet repo; no counter/harness edit; the counter, `oracle.py`
  and `count-v3.py` sha256 pins matched in all four runs.
- Hyprland was started only through `harness/oracle.py` (`oracle()`), never directly; no
  `WAYLAND_DISPLAY`/`HYPRLAND_INSTANCE_SIGNATURE` was set for anything started, no `/dev/dri` node
  was touched by my code, and each command ran under `timeout` and `prlimit --as=4000000000:8000000000`.
  `HOST_SAFETY … delta=0` printed in all four counter runs; the two tree comparisons ran through the
  same harness. No process of mine remained (`pgrep -af ExecArithToolA|m26c2-` empty; the bwrap/tinywl
  processes still listed on the host belong to `ExecArithToolB`'s own stress runs, not to me).
- Tooling: nothing installed or upgraded. Used the pre-existing `g++ 16.2.1 20260810` and
  `python3 3.14` already on the host; the fetched libstdc++ source lives at `dev/probe/ftc.cc`
  (sha256 `8b76e44f…`, 74,390 bytes) and is cited for the formatting rule only.

Report: `.ufo/waves/round-26/w2/reports/ExecArithToolA.md`
