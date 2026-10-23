# K2BaseTool — C2 control, BASE TOOL shape

Round-26 w1, item K2BaseTool. Lane repo `/home/vgpnk/Projects/shokunin/mado-shokunin`, tip
`05319e0f`; rule file `.ufo/waves/round-26/registration.md` read first.

## Shape and scope

The control is the round-25 bind resolver, byte for byte: `git show 96101be5:tools/mado-binds.py`.
Nothing was added, wrapped, or edited. The shape forbids the work C2 claims — there is no `{{…}}`
evaluator, no case reader, no embedded table — so scoring it answers one question: does the round-25
tool already meet PRED-C2-r26? Its 15,583 bytes contain no `{{` at all
(`grep -c '{{' tools/mado-binds.py` = 0); the only brace-related code is `unescape_braces`
(tools/mado-binds.py:138-156), which strips a backslash before braces and evaluates nothing.

Commands used to produce and verify the copy:

```sh
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 96101be5:tools/mado-binds.py \
  > /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2BaseTool.py
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 96101be5:tools/mado-binds.py \
  | cmp - .ufo/waves/round-26/controls/K2BaseTool.py && echo BYTE_IDENTICAL
sha256sum .ufo/waves/round-26/controls/K2BaseTool.py
```

Output:

```
9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950  .ufo/waves/round-26/controls/K2BaseTool.py
15583 .ufo/waves/round-26/controls/K2BaseTool.py
BYTE_IDENTICAL
```

The counter printed the same digest in both runs:
`tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2BaseTool.py sha256:9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950`.
Working-tree `tools/mado-binds.py` at tip is the same sha256 (checked), so the copy equals both the
base commit's bytes and the tip's file.

## Measurement

Counter file `c2/count.py` sha256 `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8`
and `harness/oracle.py` sha256 `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441`
matched the pins printed in both receipts; neither file was touched.

Two runs, fresh counter-generated seed each (no `--seed` passed), exact command:

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 python3 -I .ufo/waves/round-26/c2/count.py 05319e0f \
  --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2BaseTool.py
```

| run | seed | cases_pass | embed_hits | verdict | exit | wall |
|---|---|---|---|---|---|---|
| 1 | `4b2dae699d4926c1` | 22/51 | 0 | TARGET_MISSED | 1 | ~23 s |
| 2 | `e47a71b6fb1f1880` | 21/51 | 0 | TARGET_MISSED | 1 | ~24 s |

Both runs printed `ORACLE_CHECK base_twice equal binds=192` and
`HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0`. Receipts are saved verbatim at
`.ufo/waves/round-26/controls/K2BaseTool.txt` (sha256 `f6ba776795381b1ed3c1aa66bc66e1b358d1142e92b49855d56b2a798b52ce2b`,
121 lines; the only lines I added are the two `=== RUN …` separators — each receipt body itself is
byte-verbatim stdout including the `exit=` line).

## Results by case family

| family (n) | run 1 | run 2 | reading |
|---|---|---|---|
| BASE (1) | PASS 1/1 | PASS 1/1 | unperturbed snapshot reproduced exactly (192 binds) |
| ARITH A00–A29 (30) | PASS 1/30 (A24 only) | PASS 0/30 | the C2 target behaviour is absent |
| V3, ten types × 2 (20) | PASS 20/20 | PASS 20/20 | round-25's no-harm half is already satisfied |
| total (51) | 22/51 | 21/51 | `exit=1`, TARGET_MISSED |

BASE, both runs:

```
CASE BASE           PASS oracle_binds=192 missing=0 extra=0 (unperturbed)
```

All twenty V3 cases passed with `missing=0 extra=0` in both runs — every type (ADD, UNBIND,
VARIABLE, SOURCE, GLOB, UNSOURCED, COMMENT, SYNTH, REWRITE, HARD). Examples (oracle_binds varies
with the seed because the generator draws from the oracle's table; equality is exact in all 18
fields):

```
CASE VUNBIND-1      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=72 key='' keycode=10)
CASE VSOURCE-1      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 17)
CASE VHARD-0        PASS oracle_binds=22 missing=0 extra=0 (HARD tree lines=31 binds=22 unbinds=3 vars=4)
```

ARITH is the whole gap: 29/30 failures in run 1 and 30/30 in run 2. From a same-seed reproduction
(scratch, described under Evidence) the failing ARITH cases carry Σmissing=44 / Σextra=68 (run 1)
and Σmissing=43 / Σextra=69 (run 2). Six failures were extra-only (`missing=0`): run 1 A23, A27;
run 2 A01, A03, A16, A19. Everything else is literal-left-behind plus, often, dropped or
re-evaluated lines.

## Why the ARITH cases fail

Four mechanisms, all visible in the counter output and all explained by hyprlang 0.6.8's
implementation, which the base tool does not model.

### (a) Hyprland evaluates the expression; the base tool prints the braces

The commonest pair: one computed value missing, one literal-brace argument extra. Run 1 A02:

```
CASE A02            FAIL oracle_binds=195 missing=2 extra=2 | missing mask=68 key="KP_2" code=0 disp="exec" arg="notify-send r26 340" | missing mask=76 key="F18" code=0 disp="resizeactive" arg="2.8 0" | extra mask=68 key="KP_2" code=0 disp="exec" arg="notify-send r26 {{20 * 17 + 22 + 10.129}}" | extra mask=76 key="F18" code=0 disp="resizeactive" arg="{{14*5 / 5 + 35}} 0"
```

The reproduced config line is
`bind = SUPER CTRL, KP_2, exec, notify-send r26 {{20 * 17 + 22 + 10.129}}`; Hyprland's evaluator
uses the first three whitespace tokens (`20`, `*`, `17`) and yields `340`. The base tool never
evaluates, so it emits the literal text.

### (b) Hyprland rejects the whole line; the base tool still emits the bind

When hyprlang cannot parse the expression it abandons the config line, so no bind exists — but the
base tool has already emitted one carrying the literal braces. That is the entire content of an
extra-only failure. Run 1 A23:

```
CASE A23            FAIL oracle_binds=193 missing=0 extra=2 | extra mask=69 key="N" code=0 disp="workspace" arg="{{ (4.26+7*4 / 35)/4 }}" | extra mask=65 key="U" code=0 disp="workspace" arg="{{(15.7 - 26)/4}}" (ARITH[unclosed+ws+ws]@sourced)
```

Both expressions begin with `(`, so the first token is not a number and the line is dropped by
Hyprland. Same shape: run 1 A27
(`extra mask=12 key="KP_6" code=0 disp="workspace" arg="{{12.9+{{26 * 9.22}}*8}}"`), run 2 A01
(`extra mask=68 key="KP_3" code=0 disp="exec" arg="notify-send r26 {{ 3+8.16 }}"`), run 2 A03,
A16, A19.

### (c) Variables that hold an expression

Hyprland evaluates an expression at *assignment* time and stores the resulting number; if that
assignment errors, the variable is never defined and later `$var` uses stay literal. The base tool
instead stores the raw right-hand side and substitutes braces (and nested braces) into binds.

- Run 1 A07: `missing mask=12 key="U" code=0 disp="workspace" arg="$arolpp"` and
  `extra mask=12 key="U" code=0 disp="workspace" arg="{{ 4+0.353+{{(40 * 32 + 4.5) + 1}} }}"`.
  `$arolpp`'s value expression was unparseable (leading `(`), so Hyprland left the variable
  undefined and printed it literally.
- Run 2 A02: `missing mask=12 key="9" code=0 disp="workspace" arg="$arlkol"` and
  `extra mask=12 key="9" code=0 disp="workspace" arg="{{(28*35 / 8)/4}}"` — same mechanism.
- Run 2 A10: `missing mask=69 key="KP_2" code=0 disp="exec" arg="echo {{(115.5+11) * 2}}"` and
  `extra mask=69 key="KP_2" code=0 disp="exec" arg="echo {{({{ 5.5*6 * 21 - 6 }}+11) * 2}}"`. Here
  the definition `$ariidf = {{ 5.5*6 * 21 - 6 }}` parsed (5.5*21 = 115.5), Hyprland substituted the
  number *inside the escaped braces*, and the base tool substituted the raw braces.

### (d) Escaped and unclosed braces agree

`\{{ … }}` is skipped by the expression scanner and `{{` without `}}` breaks the scan; after
escape removal both sides carry the same literal text, so such lines match. That is why run 1's
only ARITH pass is A24, whose three added binds were unclosed (`{{3 + 1`, `{{3 + 9`) or escaped
(`\{{ 15.12*32*14.87+0 }}`), beside an unused numeric variable:

```
CASE A24            PASS oracle_binds=195 missing=0 extra=0 (ARITH[unclosed+unclosed+escaped]@sourced)
```

The pass is a property of that generated case, not of the tool: run 2 drew no such case and scored
0/30.

## Source facts behind the expected values

To explain the numbers the counter demands (without changing anything), I fetched the pinned
library source `https://codeload.github.com/hyprwm/hyprlang/tar.gz/refs/tags/v0.6.8` into scratch
(`/fast/scratch/hyaku/mado-r26/hyprlang-0.6.8`, not a lane artifact). Located quotes:

- `src/config.cpp:620-621` — `// for now, we only support very basic expressions.` /
  `// + - * / and only one per $()`
- `src/config.cpp:627` — `CConstVarList args(s, 0, 's', true);` and `src/config.cpp:629` —
  `if (args[1] != "+" && args[1] != "-" && args[1] != "*" && args[1] != "/")`. The delimiter `'s'`
  means whitespace (hyprutils 0.14.2, `include/hyprutils/string/ConstVarList.hpp:11`:
  `@param delim if delimiter is 's', use std::isspace`), and only `args[0..2]` are used.
- `src/config.cpp:644` — `left = std::stof(std::string{args[0]});`: operands are parsed as
  C float prefixes (`"30+7.9"` → 30, `"5.5*6"` → 5.5), which is why Hyprland answers `30` for
  `{{30+7.9 + 0 - 33}}` and `340` for `{{20 * 17 + 22 + 10.129}}`.
- `src/config.cpp:757-800` — expressions are evaluated after `$var` substitution and before the
  handler sees the line; escaped starts are skipped and a missing `}}` breaks the loop, leaving
  the text literal.
- `src/config.cpp:786-788` — a failed parse does
  `result.setError(RESULT.error()); return result;`, so the line is not applied (the bind is
  dropped), matching mechanism (b).

Consequence for the C2 data seat: expected values are Hyprland's actual parser, not textbook
arithmetic. A resolver that evaluates `{{…}}` with proper precedence would still miss most ARITH
cases (for example `20 * 17 + 22 + 10.129` must become `340`, not `362.129`), and it must also
reproduce float32 shortest formatting (`8.700001`, `1.8000002`, `25.942001`) and the
drop-the-line-on-parse-error behaviour. The counter's V3 half already passes on the base tool, so
a data change that breaks round-25 behaviour would be visible there as well.

## Verdict

CONTROL K2BaseTool best: cases_pass=22/51 [embed_hits=0] verdict=TARGET_MISSED — not met

The round-25 tool reproduces the unperturbed table and all twenty round-25 V3 cases exactly in
both runs, but it leaves `{{…}}` literal and therefore misses 29–30 of 30 ARITH cases; the C2
target (51/51, embed_hits=0) is not met by the base shape, as the claim predicts. The base receipt
is therefore a valid negative control: the frozen counter detects the round-25 `{{…}}` gap and its
no-harm half is already green.

## Complete counter stdout (verbatim)

### Run 1 — seed 4b2dae699d4926c1

```text
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2BaseTool.py sha256:9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950
seed=4b2dae699d4926c1
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal binds=192
CASE BASE           PASS oracle_binds=192 missing=0 extra=0 (unperturbed)
CASE A00            FAIL oracle_binds=195 missing=1 extra=2 | missing mask=69 key="KP_7" code=0 disp="workspace" arg="0.22424243" | extra mask=72 key="N" code=0 disp="workspace" arg="{{32+6+2}}" | extra mask=69 key="KP_7" code=0 disp="workspace" arg="{{7.4 / 33 * 9.6 * 6}}" (ARITH[ws+unclosed+var+escaped]@sourced)
CASE A01            FAIL oracle_binds=194 missing=1 extra=3 | missing mask=76 key="F20" code=0 disp="workspace" arg="30" | extra mask=65 key="KP_8" code=0 disp="exec" arg="notify-send r26 {{(26*28+11 - 6)/4}}" | extra mask=76 key="F20" code=0 disp="workspace" arg="{{30+7.9 + 0 - 33}}" (ARITH[unclosed+exec+ws+resize]@sourced)
CASE A02            FAIL oracle_binds=195 missing=2 extra=2 | missing mask=68 key="KP_2" code=0 disp="exec" arg="notify-send r26 340" | missing mask=76 key="F18" code=0 disp="resizeactive" arg="2.8 0" | extra mask=68 key="KP_2" code=0 disp="exec" arg="notify-send r26 {{20 * 17 + 22 + 10.129}}" | extra mask=76 key="F18" code=0 disp="resizeactive" arg="{{14*5 / 5 + 35}} 0" (ARITH[escaped+exec+desc]@sourced)
CASE A03            FAIL oracle_binds=194 missing=1 extra=3 | missing mask=72 key="KP_3" code=0 disp="workspace" arg="8.700001" | extra mask=72 key="KP_3" code=0 disp="workspace" arg="{{12.1 - 3.4}}" | extra mask=69 key="F20" code=0 disp="resizeactive" arg="{{6.2 - 39}} {{2 * {{ (20*33 / 0+14) * 2 }}}}" (ARITH[var+resize+ws+unclosed]@sourced)
CASE A04            FAIL oracle_binds=196 missing=3 extra=3 | missing mask=65 key="F15" code=0 disp="resizeactive" arg="24.043 0" | missing mask=65 key="I" code=0 disp="workspace" arg="30.487999" | extra mask=65 key="F15" code=0 disp="resizeactive" arg="{{ {{13.643 - 1.6}} + 12 + {{13.643 - 1.6}} }} 0" | extra mask=65 key="I" code=0 disp="workspace" arg="{{37 - 6.512 - 13}}" (ARITH[desc+escaped+ws+desc]@sourced)
CASE A05            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=12 key="KP_4" code=0 disp="moveactive" arg="13.6 -1.8000002" | missing mask=69 key="N" code=0 disp="workspace" arg="2.3115" | extra mask=68 key="Y" code=0 disp="resizeactive" arg="{{(5 + 2.426 + 6.8) * 2}} {{(6.53*6.8 - 25) + 1}} | extra mask=12 key="KP_4" code=0 disp="moveactive" arg="{{ 6.8*6.8 + 6.8 }} -{{ 6.8 - 5 - 17.2*6.8 }}" (ARITH[resize+move+ws]@sourced)
CASE A06            FAIL oracle_binds=195 missing=1 extra=1 | missing mask=72 key="F19" code=0 disp="resizeactive" arg="116 0" | extra mask=72 key="F19" code=0 disp="resizeactive" arg="{{ 4*7 * 29+9 }} 0" (ARITH[escaped+desc+unclosed]@sourced)
CASE A07            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=12 key="U" code=0 disp="workspace" arg="$arolpp" | missing mask=76 key="KP_6" code=0 disp="workspace" arg="$arpkmo" | extra mask=68 key="U" code=0 disp="resizeactive" arg="{{ 13.06 + {{(40 * 32 + 4.5) + 1}} * 16.327 }} 0" | extra mask=12 key="U" code=0 disp="workspace" arg="{{ 4+0.353+{{(40 * 32 + 4.5) + 1}} }}" (ARITH[desc+var+var+desc]@sourced)
CASE A08            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=12 key="U" code=0 disp="resizeactive" arg="145 22.272" | missing mask=65 key="KP_8" code=0 disp="resizeactive" arg="0.7777778 0" | extra mask=12 key="U" code=0 disp="resizeactive" arg="{{ 29 * 5*10.82 }} {{ 5 + 17.272 / 29*11.409 }}" | extra mask=65 key="KP_8" code=0 disp="resizeactive" arg="{{ 28 / 36*39 }} 0" (ARITH[resize+desc]@sourced)
CASE A09            FAIL oracle_binds=193 missing=1 extra=2 | missing mask=64 key="F14" code=0 disp="workspace" arg="0.303" | extra mask=64 key="F14" code=0 disp="workspace" arg="{{4.545*31+1 / 15}}" | extra mask=69 key="U" code=0 disp="exec" arg="notify-send r26 {{ (12.99 * 37) + 1 }}" (ARITH[ws+exec]@sourced)
CASE A10            FAIL oracle_binds=193 missing=1 extra=3 | missing mask=72 key="F18" code=0 disp="exec" arg="notify-send r26 43" | extra mask=64 key="I" code=0 disp="exec" arg="notify-send r26 {{ 16+15.9 }}" | extra mask=72 key="F18" code=0 disp="exec" arg="notify-send r26 {{31*6 + 12}}" (ARITH[exec+exec+exec]@sourced)
CASE A11            FAIL oracle_binds=195 missing=2 extra=3 | missing mask=65 key="F14" code=0 disp="moveactive" arg="0.08918362 -165.79" | missing mask=72 key="8" code=0 disp="workspace" arg="320.019" | extra mask=65 key="F14" code=0 disp="moveactive" arg="{{0.78 / 8.746*5.6 * 18.39}} -{{{{10 * 18}} - 14. | extra mask=64 key="KP_6" code=0 disp="moveactive" arg="{{9.1+{{10 * 18}}}} -{{ 11 + 5.6 }}" (ARITH[move+move+unclosed+ws]@sourced)
CASE A12            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=64 key="KP_6" code=0 disp="moveactive" arg="54.8 -9.58" | extra mask=64 key="KP_6" code=0 disp="moveactive" arg="{{ 36 + 18.8 / 1.40 / 31 }} -{{5.58 + 4}}" (ARITH[move+escaped]@sourced)
CASE A13            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=69 key="F18" code=0 disp="exec" arg="notify-send r26 8" | extra mask=12 key="7" code=0 disp="workspace" arg="{{(29*6.0) + 1}}" | extra mask=69 key="F18" code=0 disp="exec" arg="notify-send r26 {{ 23+14.120*{{5.726+27 + 11.4}}  (ARITH[ws+unclosed+exec]@sourced)
CASE A14            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=69 key="F17" code=0 disp="workspace" arg="117.799995" | extra mask=69 key="F17" code=0 disp="workspace" arg="{{ 3.1 * 38 - 32 }}" (ARITH[unclosed+ws]@sourced)
CASE A15            FAIL oracle_binds=195 missing=3 extra=4 | missing mask=72 key="KP_7" code=0 disp="resizeactive" arg="3 1.9333333" | missing mask=12 key="F18" code=0 disp="workspace" arg="5.2" | extra mask=72 key="KP_7" code=0 disp="resizeactive" arg="{{0*31 + 3 - 9.3}} {{ 29 / 15 }}" | extra mask=12 key="F18" code=0 disp="workspace" arg="{{2 * 2.6}}" (ARITH[resize+var+exec+exec]@sourced)
CASE A16            FAIL oracle_binds=193 missing=1 extra=2 | missing mask=65 key="F18" code=0 disp="resizeactive" arg="7.6666665 1" | extra mask=65 key="8" code=0 disp="moveactive" arg="{{ 0 / 38 }} -{{14.1*3}}" | extra mask=65 key="F18" code=0 disp="resizeactive" arg="{{23 / 3 - 3}} {{ 3 / 3 + 8 }}" (ARITH[move+resize]@sourced)
CASE A17            FAIL oracle_binds=195 missing=2 extra=3 | missing mask=68 key="9" code=0 disp="workspace" arg="41" | missing mask=68 key="KP_4" code=0 disp="workspace" arg="10.4" | extra mask=68 key="9" code=0 disp="workspace" arg="{{13+27 + 28 / 3}}" | extra mask=76 key="KP_8" code=0 disp="moveactive" arg="{{5 * 5}} -{{(22*5+5 / 36)/4}}" (ARITH[var+move+var+unclosed]@root)
CASE A18            FAIL oracle_binds=196 missing=1 extra=1 | missing mask=69 key="F13" code=0 disp="moveactive" arg="9 -42" | extra mask=69 key="F13" code=0 disp="moveactive" arg="{{16 - 7}} -{{19 + 23 / 40 - 17.1}}" (ARITH[unclosed+unclosed+move+unclosed]@sourced)
CASE A19            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=68 key="Y" code=0 disp="exec" arg="notify-send r26 608" | missing mask=76 key="F13" code=0 disp="moveactive" arg="1 -6" | extra mask=68 key="Y" code=0 disp="exec" arg="notify-send r26 {{ 38*4 * 16 + 2.99 }}" | extra mask=76 key="F13" code=0 disp="moveactive" arg="{{6.0+13.32 / 6.0 - 38}} -{{6.0 / 1}}" (ARITH[exec+move]@sourced)
CASE A20            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=72 key="M" code=0 disp="workspace" arg="1" | extra mask=69 key="8" code=0 disp="resizeactive" arg="{{(2.82 + 5.43*18 * 16) * 2}} 0" | extra mask=72 key="M" code=0 disp="workspace" arg="{{6.6 / 6.6*3.1*6.6}}" (ARITH[unclosed+desc+ws]@sourced)
CASE A21            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=64 key="B" code=0 disp="workspace" arg="$arpmop" | extra mask=64 key="B" code=0 disp="workspace" arg="{{ (5.778 / 27) + 1 }}" | extra mask=65 key="Y" code=0 disp="resizeactive" arg="{{ 7.532 - 12 + 2*5.9 }} {{(24 * 6.82 / 10.462) * (ARITH[escaped+var+resize]@sourced)
CASE A22            FAIL oracle_binds=196 missing=2 extra=2 | missing mask=72 key="F20" code=0 disp="moveactive" arg="24 -1" | missing mask=64 key="F18" code=0 disp="workspace" arg="1.9264706" | extra mask=72 key="F20" code=0 disp="moveactive" arg="{{31 - 7}} -{{18 - 17}}" | extra mask=64 key="F18" code=0 disp="workspace" arg="{{ 13.10+{{(13 + 23*22 - 3)/4}} / 6.8*30 }}" (ARITH[move+unclosed+escaped+ws]@sourced)
CASE A23            FAIL oracle_binds=193 missing=0 extra=2 | extra mask=69 key="N" code=0 disp="workspace" arg="{{ (4.26+7*4 / 35)/4 }}" | extra mask=65 key="U" code=0 disp="workspace" arg="{{(15.7 - 26)/4}}" (ARITH[unclosed+ws+ws]@sourced)
CASE A24            PASS oracle_binds=195 missing=0 extra=0 (ARITH[unclosed+unclosed+escaped]@sourced)
CASE A25            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=64 key="F14" code=0 disp="moveactive" arg="22.65 -28.93" | missing mask=69 key="F18" code=0 disp="workspace" arg="-12" | extra mask=64 key="F14" code=0 disp="moveactive" arg="{{ 13.95+18.164 + 8.70 + 8.6 }} -{{ 37 - 8.07 }}" | extra mask=69 key="F18" code=0 disp="workspace" arg="{{ {{ (29+17.082+15) + 1 }}*16.5 - 22*7 }}" (ARITH[move+ws+var+ws]@sourced)
CASE A26            FAIL oracle_binds=196 missing=2 extra=2 | missing mask=69 key="U" code=0 disp="moveactive" arg="39.2 --32" | missing mask=68 key="N" code=0 disp="workspace" arg="25.942001" | extra mask=69 key="U" code=0 disp="moveactive" arg="{{ 35 + 4.2 }} -{{ 6+4.2 - 38+18 }}" | extra mask=68 key="N" code=0 disp="workspace" arg="{{ 40 - 14.058+24 }}" (ARITH[unclosed+move+escaped+ws]@sourced)
CASE A27            FAIL oracle_binds=193 missing=0 extra=1 | extra mask=12 key="KP_6" code=0 disp="workspace" arg="{{12.9+{{26 * 9.22}}*8}}" (ARITH[unclosed+ws]@sourced)
CASE A28            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=72 key="KP_4" code=0 disp="exec" arg="notify-send r26 -11" | missing mask=76 key="Y" code=0 disp="workspace" arg="8.75" | extra mask=72 key="KP_4" code=0 disp="exec" arg="notify-send r26 {{ 21 - 32 }}" | extra mask=76 key="Y" code=0 disp="workspace" arg="{{25*10.929 * 0.35}}" (ARITH[exec+ws+desc]@sourced)
CASE A29            FAIL oracle_binds=196 missing=3 extra=3 | missing mask=72 key="KP_4" code=0 disp="resizeactive" arg="4.9666667 0" | missing mask=69 key="F20" code=0 disp="resizeactive" arg="1152 18.266" | extra mask=72 key="KP_4" code=0 disp="resizeactive" arg="{{14.9 / 3 / 25 + 24}} 0" | extra mask=69 key="F20" code=0 disp="resizeactive" arg="{{ 32 * 36 }} {{6.666 + 11.6}}" (ARITH[desc+resize+var+escaped]@sourced)
CASE VADD-0         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
CASE VADD-1         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
CASE VUNBIND-0      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=64 key='RIGHT' keycode=0)
CASE VUNBIND-1      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=72 key='' keycode=10)
CASE VVARIABLE-0    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vnpgsiyd)
CASE VVARIABLE-1    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vgiplaky)
CASE VSOURCE-0      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 16)
CASE VSOURCE-1      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 17)
CASE VGLOB-0        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VGLOB-1        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VUNSOURCED-0   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VUNSOURCED-1   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VCOMMENT-0     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .config/hypr/bindings.conf)
CASE VCOMMENT-1     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE VSYNTH-0       PASS oracle_binds=14 missing=0 extra=0 (SYNTH tree binds=14 unbound=1 vars=2)
CASE VSYNTH-1       PASS oracle_binds=15 missing=0 extra=0 (SYNTH tree binds=15 unbound=1 vars=2)
CASE VREWRITE-0     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=0 key='XF86AudioMute' code=0; unbind mask=64 key='DOWN' code=0; add exec)
CASE VREWRITE-1     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=73 key='' code=11; unbind mask=65 key='' code=15; add exec)
CASE VHARD-0        PASS oracle_binds=19 missing=0 extra=0 (HARD tree lines=33 binds=19 unbinds=2 vars=4)
CASE VHARD-1        PASS oracle_binds=22 missing=0 extra=0 (HARD tree lines=31 binds=22 unbinds=3 vars=4)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=22/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### Run 2 — seed e47a71b6fb1f1880

```text
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2BaseTool.py sha256:9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950
seed=e47a71b6fb1f1880
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal binds=192
CASE BASE           PASS oracle_binds=192 missing=0 extra=0 (unperturbed)
CASE A00            FAIL oracle_binds=195 missing=3 extra=3 | missing mask=76 key="KP_8" code=0 disp="workspace" arg="112.55999" | missing mask=72 key="8" code=0 disp="workspace" arg="-4.7" | extra mask=76 key="KP_8" code=0 disp="workspace" arg="{{6.7 * 16.80 + 12.601+16.92}}" | extra mask=72 key="8" code=0 disp="workspace" arg="{{2 - 6.7 + 18*3}}" (ARITH[ws+var+exec]@sourced)
CASE A01            FAIL oracle_binds=194 missing=0 extra=1 | extra mask=68 key="KP_3" code=0 disp="exec" arg="notify-send r26 {{ 3+8.16 }}" (ARITH[escaped+escaped+exec]@sourced)
CASE A02            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=64 key="F16" code=0 disp="workspace" arg="3" | missing mask=12 key="9" code=0 disp="workspace" arg="$arlkol" | extra mask=64 key="F16" code=0 disp="workspace" arg="{{24+31 / 8*8}}" | extra mask=12 key="9" code=0 disp="workspace" arg="{{(28*35 / 8)/4}}" (ARITH[var+var+resize]@sourced)
CASE A03            FAIL oracle_binds=192 missing=0 extra=3 | extra mask=69 key="KP_7" code=0 disp="resizeactive" arg="{{(10+27)/4}} {{16.02 * 17.9 / 18}}" | extra mask=76 key="B" code=0 disp="exec" arg="notify-send r26 {{12+37}}" (ARITH[resize+exec+move]@sourced)
CASE A04            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=76 key="F16" code=0 disp="resizeactive" arg="25.085 0" | missing mask=65 key="F16" code=0 disp="workspace" arg="0.16129032" | extra mask=76 key="F16" code=0 disp="resizeactive" arg="{{ 6.765 + 18.320 / 14.096 * 24 }} 0" | extra mask=65 key="F16" code=0 disp="workspace" arg="{{5 / 31 / 0 - 20}}" (ARITH[desc+ws]@sourced)
CASE A05            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=65 key="F18" code=0 disp="workspace" arg="-18.8" | missing mask=76 key="KP_6" code=0 disp="resizeactive" arg="11.8 0" | extra mask=65 key="F18" code=0 disp="workspace" arg="{{ 6.2 - 25 - 6.2+12.826 }}" | extra mask=76 key="KP_6" code=0 disp="resizeactive" arg="{{ 18 - 6.2+16.249 }} 0" (ARITH[var+desc+move]@sourced)
CASE A06            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=65 key="F20" code=0 disp="resizeactive" arg="1.048 276.21002" | missing mask=64 key="KP_3" code=0 disp="workspace" arg="31.041" | extra mask=65 key="F20" code=0 disp="resizeactive" arg="{{15.72 / 15 * 8}} {{12.555 * 22+5}}" | extra mask=64 key="KP_3" code=0 disp="workspace" arg="{{34 - 2.959+23*33}}" (ARITH[resize+ws]@sourced)
CASE A07            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=64 key="U" code=0 disp="resizeactive" arg="0.1 0" | missing mask=68 key="M" code=0 disp="workspace" arg="$arpnnn" | extra mask=64 key="U" code=0 disp="resizeactive" arg="{{ 3 / 30+28 + 36 }} 0" | extra mask=65 key="M" code=0 disp="moveactive" arg="{{ (14+15 / 26*13.997)/4 }} -{{ 1.3 + 5 + 2 }}" (ARITH[desc+move+var]@sourced)
CASE A08            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=12 key="M" code=0 disp="exec" arg="notify-send r26 -30" | missing mask=65 key="KP_2" code=0 disp="exec" arg="notify-send r26 -12.423" | extra mask=12 key="M" code=0 disp="exec" arg="notify-send r26 {{8*32 - 38+14}}" | extra mask=65 key="KP_2" code=0 disp="exec" arg="notify-send r26 {{ 11.577 - 24 }}" (ARITH[exec+exec+move]@sourced)
CASE A09            FAIL oracle_binds=196 missing=1 extra=1 | missing mask=72 key="F20" code=0 disp="workspace" arg="33" | extra mask=72 key="F20" code=0 disp="workspace" arg="{{32+18.542 + 1 / 2}}" (ARITH[unclosed+unclosed+unclosed+ws]@sourced)
CASE A10            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=69 key="KP_2" code=0 disp="exec" arg="echo {{(115.5+11) * 2}}" | extra mask=69 key="KP_2" code=0 disp="exec" arg="echo {{({{ 5.5*6 * 21 - 6 }}+11) * 2}}" | extra mask=12 key="7" code=0 disp="moveactive" arg="{{ 33+{{ 5.5*6 * 21 - 6 }}*18*8 }} -{{(8 - 8*{{ 5 (ARITH[escaped+move+escaped]@sourced)
CASE A11            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=64 key="Y" code=0 disp="workspace" arg="$arpomn" | extra mask=64 key="Y" code=0 disp="workspace" arg="{{15.242+8.9}}" (ARITH[var+unclosed]@sourced)
CASE A12            FAIL oracle_binds=195 missing=1 extra=2 | missing mask=76 key="F15" code=0 disp="moveactive" arg="33 -10.476191" | extra mask=72 key="9" code=0 disp="resizeactive" arg="{{ 1*1+31 }} {{ 0.342 * 1 - 26 }}" | extra mask=76 key="F15" code=0 disp="moveactive" arg="{{ 1 * 33 - 13 * 11 }} -{{ 22 / 2.1 + 19 }}" (ARITH[resize+move+escaped+unclosed]@sourced)
CASE A13            FAIL oracle_binds=195 missing=2 extra=2 | missing mask=64 key="F13" code=0 disp="workspace" arg="$arkkml" | missing mask=65 key="KP_4" code=0 disp="resizeactive" arg="0.16190477 0" | extra mask=64 key="F13" code=0 disp="workspace" arg="{{ 18.3*3.4 }}" | extra mask=65 key="KP_4" code=0 disp="resizeactive" arg="{{ 3.4 / 21 * 10 * 5.9 }} 0" (ARITH[var+escaped+desc]@sourced)
CASE A14            FAIL oracle_binds=193 missing=1 extra=3 | missing mask=72 key="U" code=0 disp="exec" arg="notify-send r26 12.42" | extra mask=72 key="7" code=0 disp="moveactive" arg="{{1 * 16.0 - 19}} -{{(6 / 15 * 3 / 25)/4}}" | extra mask=72 key="U" code=0 disp="exec" arg="notify-send r26 {{ 6.42 + 6 }}" (ARITH[move+exec+resize]@sourced)
CASE A15            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=64 key="F17" code=0 disp="exec" arg="notify-send r26 552" | extra mask=64 key="F17" code=0 disp="exec" arg="notify-send r26 {{24 * 23}}" | extra mask=72 key="F14" code=0 disp="moveactive" arg="{{8*31+26}} -{{28 / 10.6}}" (ARITH[unclosed+exec+move]@sourced)
CASE A16            FAIL oracle_binds=193 missing=0 extra=2 | extra mask=72 key="I" code=0 disp="workspace" arg="{{ (13 - 22) + 1 }}" | extra mask=68 key="8" code=0 disp="workspace" arg="{{15.897*27+12}}" (ARITH[unclosed+ws+ws]@sourced)
CASE A17            FAIL oracle_binds=193 missing=1 extra=2 | missing mask=68 key="F20" code=0 disp="workspace" arg="11.18" | extra mask=68 key="F20" code=0 disp="workspace" arg="{{ 5.590 * 2+7.9 }}" | extra mask=68 key="O" code=0 disp="moveactive" arg="{{37 / 29 - 25}} -{{(40 - 18.219 / 1) * 2}}" (ARITH[var+move]@sourced)
CASE A18            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=64 key="F17" code=0 disp="exec" arg="notify-send r26 16" | extra mask=64 key="F17" code=0 disp="exec" arg="notify-send r26 {{ 4 * 4 + 5 + 28 }}" (ARITH[exec+escaped]@sourced)
CASE A19            FAIL oracle_binds=194 missing=0 extra=1 | extra mask=69 key="N" code=0 disp="moveactive" arg="{{2+2*2}} -{{2*30}}" (ARITH[escaped+escaped+move]@sourced)
CASE A20            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=76 key="F20" code=0 disp="exec" arg="echo {{46 + 9+46 + 9.7}}" | missing mask=65 key="KP_2" code=0 disp="workspace" arg="153" | extra mask=65 key="F17" code=0 disp="workspace" arg="{{21+7*34}}" | extra mask=76 key="F20" code=0 disp="exec" arg="echo {{{{34 + 12 / 25}} + 9+{{34 + 12 / 25}} + 9. (ARITH[ws+escaped+move+var]@sourced)
CASE A21            FAIL oracle_binds=194 missing=1 extra=3 | missing mask=72 key="7" code=0 disp="workspace" arg="$aromlm" | extra mask=64 key="I" code=0 disp="moveactive" arg="{{ (39 + 15.6*27) * 2 }} -{{ 3*14.4+5 - 3 }}" | extra mask=72 key="7" code=0 disp="workspace" arg="{{(5 * 3 / 36 / 3) * 2}}" (ARITH[move+var+desc+escaped]@sourced)
CASE A22            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=68 key="N" code=0 disp="workspace" arg="11.235954" | missing mask=64 key="KP_7" code=0 disp="moveactive" arg="2.1170611 -0" | extra mask=64 key="KP_3" code=0 disp="resizeactive" arg="{{(36 - 0.243 + 30 / 16) * 2}} {{(3 - 16.9) + 1}} | extra mask=68 key="N" code=0 disp="workspace" arg="{{ 15 / 1.335*2 }}" (ARITH[resize+ws+move]@sourced)
CASE A23            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=68 key="8" code=0 disp="workspace" arg="$arnlol" | missing mask=68 key="F15" code=0 disp="exec" arg="notify-send r26 14" | extra mask=68 key="8" code=0 disp="workspace" arg="{{ (0 / 28)/4 }}" | extra mask=68 key="F15" code=0 disp="exec" arg="notify-send r26 {{ 7 + 7 + 7 }}" (ARITH[var+exec]@sourced)
CASE A24            FAIL oracle_binds=195 missing=1 extra=2 | missing mask=12 key="F17" code=0 disp="workspace" arg="0.71428573" | extra mask=12 key="F17" code=0 disp="workspace" arg="{{15 / 21}}" | extra mask=64 key="O" code=0 disp="workspace" arg="{{({{ 6 / 3.470 / 9 }} * {{ 6 / 3.470 / 9 }} + 7) (ARITH[unclosed+var+ws+unclosed]@sourced)
CASE A25            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=69 key="F18" code=0 disp="workspace" arg="$arlnmo" | missing mask=12 key="F16" code=0 disp="exec" arg="echo {{(0.14814815 - 10 / 4.63) * 2}}" | extra mask=69 key="F18" code=0 disp="workspace" arg="{{ 14*1 }}" | extra mask=68 key="KP_4" code=0 disp="resizeactive" arg="{{(0 - 13.5 * 39) + 1}} {{ 12.260 * {{4 / 27}} /  (ARITH[var+resize+escaped+move]@sourced)
CASE A26            FAIL oracle_binds=196 missing=3 extra=3 | missing mask=68 key="KP_2" code=0 disp="exec" arg="echo {{ 17*$areaii*15.324 }}" | missing mask=76 key="F17" code=0 disp="exec" arg="notify-send r26 41.3" | extra mask=68 key="KP_2" code=0 disp="exec" arg="echo {{ 17*{{16*35}}*15.324 }}" | extra mask=76 key="F17" code=0 disp="exec" arg="notify-send r26 {{ 9.3 + 32 * 1.40 + 20 }}" (ARITH[escaped+exec+escaped+unclosed]@sourced)
CASE A27            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=64 key="F17" code=0 disp="exec" arg="notify-send r26 1" | missing mask=72 key="F13" code=0 disp="workspace" arg="$arlmpo" | extra mask=64 key="F17" code=0 disp="exec" arg="notify-send r26 {{23 - 22*15 * 7.3}}" | extra mask=72 key="F13" code=0 disp="workspace" arg="{{ (32 + 7.3 * 13.610 + 39) + 1 }}" (ARITH[exec+var]@sourced)
CASE A28            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=12 key="F17" code=0 disp="resizeactive" arg="28.576 4" | extra mask=64 key="F13" code=0 disp="resizeactive" arg="{{(15.60 * 5) * 2}} {{2 - 39 / 5.15 * 38}}" | extra mask=12 key="F17" code=0 disp="resizeactive" arg="{{ 17.576 + 11 }} {{ 28 / 7+6 }}" (ARITH[resize+escaped+resize]@sourced)
CASE A29            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=65 key="KP_7" code=0 disp="exec" arg="echo {{$ardceb * 19.98 * 33+16.6}}" | missing mask=69 key="U" code=0 disp="resizeactive" arg="71.299995 1.6075" | extra mask=65 key="KP_7" code=0 disp="exec" arg="echo {{{{ (40+3.1)/4 }} * 19.98 * 33+16.6}}" | extra mask=69 key="U" code=0 disp="resizeactive" arg="{{ 3.1 * 23*{{ (40+3.1)/4 }}+{{ (40+3.1)/4 }} }}  (ARITH[escaped+resize]@sourced)
CASE VADD-0         PASS oracle_binds=193 missing=0 extra=0 (ADD into .config/hypr/bindings.conf)
CASE VADD-1         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE VUNBIND-0      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=68 key='C' keycode=0)
CASE VUNBIND-1      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=65 key='' keycode=10)
CASE VVARIABLE-0    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vesbqpyn)
CASE VVARIABLE-1    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vqekkxey)
CASE VSOURCE-0      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 5)
CASE VSOURCE-1      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 19)
CASE VGLOB-0        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VGLOB-1        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VUNSOURCED-0   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VUNSOURCED-1   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VCOMMENT-0     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
CASE VCOMMENT-1     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .config/hypr/bindings.conf)
CASE VSYNTH-0       PASS oracle_binds=16 missing=0 extra=0 (SYNTH tree binds=16 unbound=1 vars=3)
CASE VSYNTH-1       PASS oracle_binds=14 missing=0 extra=0 (SYNTH tree binds=14 unbound=1 vars=2)
CASE VREWRITE-0     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=64 key='' code=10; unbind mask=73 key='' code=18; add exec)
CASE VREWRITE-1     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=0 key='XF86PowerOff' code=0; unbind mask=64 key='LEFT' code=0; add fullscreenstate)
CASE VHARD-0        PASS oracle_binds=22 missing=0 extra=0 (HARD tree lines=31 binds=22 unbinds=3 vars=4)
CASE VHARD-1        PASS oracle_binds=20 missing=0 extra=0 (HARD tree lines=27 binds=20 unbinds=2 vars=4)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=21/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

## Evidence and scratch

- Control copy: `.ufo/waves/round-26/controls/K2BaseTool.py`, 15,583 bytes, sha256
  `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950`, `cmp` against
  `git show 96101be5:tools/mado-binds.py` → byte-identical.
- Receipts: `.ufo/waves/round-26/controls/K2BaseTool.txt`, sha256
  `f6ba776795381b1ed3c1aa66bc66e1b358d1142e92b49855d56b2a798b52ce2b`.
- Diagnosis reproduction: `/fast/scratch/hyaku/mado-r26/k2base_analysis.py`, outputs
  `/tmp/k2an_run1.txt` and `/tmp/k2an_run2.txt`. It imports the frozen counter module (same
  `arith_case`, same `V3`) and the frozen `oracle.py`, rebuilds each seed's 30 ARITH homes, runs
  the base tool and the harness oracle on each, and prints the full missing/extra lists plus the
  exact appended config lines. It is scratch-only: no lane file reads or writes beyond the pinned
  inputs, no counter/harness edits. Its 60 nested instances ran only through `oracle.py`; a
  `coredumps()` read after them returned 1335, unchanged from both receipts.
- No lane writes besides this report, `controls/K2BaseTool.py` and `controls/K2BaseTool.txt`; no
  git/jj write command was run in the lane or the fleet repo.

## Risks and limits

- This is a deliberate negative control: the BASE TOOL shape cannot reach 51/51 because it does no
  expression work. Its value is the measured gap, not a candidate implementation.
- Run 1's A24 pass is generator luck (only escaped/unclosed lines); a different seed scores 0/30.
- The diagnosis reproduction assumes the counter's case construction is deterministic given the
  seed; labels, appended config lines and the sampled missing/extra lines matched the receipts
  exactly for both seeds, which is the cross-check available without editing the counter.
- The `=== RUN …` separator lines were added when saving both stdouts into one file; the receipt
  bodies are unmodified, including `exit=` lines.
