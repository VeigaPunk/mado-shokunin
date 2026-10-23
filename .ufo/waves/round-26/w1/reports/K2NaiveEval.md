# K2NaiveEval — C2 NAIVE EVAL control

## Verdict

CONTROL K2NaiveEval best: cases_pass=23/51 embed_hits=0 verdict=TARGET_MISSED — not met

Both valid fresh-seed runs missed the registered 51/51 target. BASE and all 20 V3 cases passed in each run; ARITH passed 1/30 and 2/30. This Python-eval shortcut did not meet C2 on either sampled seed. No exit-2 guard occurred and no retry was needed. This is a negative-control result, not a replacement arithmetic resolver or a claim about every possible seed.

## Control and expected detector

Axes: shape fidelity, reproducible byte custody, fresh-seed measurement, and host isolation.

- Copied `96101be5:tools/mado-binds.py`, the round-25 tool, into `.ufo/waves/round-26/controls/K2NaiveEval.py` (base: 15,583 bytes, SHA-256 `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950`).
- Added `re`, a `naive_eval` callback implementing `str(eval(match.group(1)))`, and one bind-value substitution using `r"\{\{(.*?)\}\}"` after the existing textual variable-substitution loop. The `$var =` branch returns before this hook. Other keywords are unchanged.
- Python evaluation exceptions leave that match literal, allowing the rest of the inherited resolver to continue. Python number formatting is untouched. There is no new escape recognition, nested-expression parser, or hyprlang arithmetic rule; the inherited brace-unescape code still runs afterward.
- The control was frozen before both scores, was not changed afterward, and was not tuned from oracle differences. No hyprlang arithmetic source or oracle implementation was consulted to design it. Detailed oracle differences are retained verbatim below, not mined for replacement semantics.
- Expected detector: frozen C2 `PRED-C2-r26`, requiring exact bind multisets across BASE + 30 ARITH + 20 V3 cases and `embed_hits=0`; target `cases_pass=51/51`.
- The only created lane outputs are this control, its required receipt file, and this report. Neither production tool, counter, nor harness was edited.

## Exact commands and execution

Working directory for all commands: `/home/vgpnk/Projects/shokunin/mado-shokunin`.

Every subprocess received a copy of the environment with `WAYLAND_DISPLAY`, `HYPRLAND_INSTANCE_SIGNATURE`, `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed. Copy/hash/free-space commands were capped at a 20-second timeout and 4 GB address space. The counter wrappers used a 4 GB soft / 8 GB hard limit, following L1's host-safety correction so the oracle could set its own 8 GB limit.

Read-only base acquisition:

```sh
timeout 20 prlimit --as=4000000000 -- git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 96101be5:tools/mado-binds.py
```

The captured base bytes were written through the file-writing tool to the assigned control path; the small additions above were applied with the surgical-edit tool.

Both scores used this exact command, concurrently, without `--seed`:

```sh
timeout --kill-after=10 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 05319e0f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2NaiveEval.py
```

Free-space check before scratch work:

```sh
timeout 20 prlimit --as=4000000000 -- df -h /fast
```

Observed `/fast`: 804G total, 619G used, 185G available, 78% used.

Initial custody command:

```sh
timeout 20 prlimit --as=4000000000 -- sha256sum tools/mado-binds.py .ufo/waves/round-26/c2/count.py .ufo/waves/round-26/harness/oracle.py
```

Before scoring, the same bounded `sha256sum` invocation also hashed the new control. Final custody command:

```sh
timeout 20 prlimit --as=4000000000 -- sha256sum tools/mado-binds.py .ufo/waves/round-26/controls/K2NaiveEval.py .ufo/waves/round-26/controls/K2NaiveEval.txt .ufo/waves/round-26/c2/count.py .ufo/waves/round-26/harness/oracle.py
```

No packages or tools were installed or upgraded. No additional behavioral checks were run.

## Measured outputs

| Run | Fresh seed | BASE | ARITH | V3 | Total | Embed hits | Process exit | Elapsed seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `a7b25982776f11a4` | 1/1 | 1/30 | 20/20 | 22/51 | 0 | 1 | 42.175 |
| 2 | `4ed2001e835c2b67` | 1/1 | 2/30 | 20/20 | 23/51 | 0 | 1 | 54.488 |

Both subprocess stderr streams were empty. Both receipts report `ORACLE_CHECK base_twice equal binds=192` and `HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0`. Only the frozen counter's sandboxed oracle started compositor instances; no live-compositor commands or persistent services were started. Both timeout-wrapped counter processes completed normally, with their ordinary counter/oracle cleanup paths.

Required verbatim receipt file: `.ufo/waves/round-26/controls/K2NaiveEval.txt` (two stdout streams concatenated in run order, 24,974 bytes, including each `exit=1` line).

## Byte custody and restoration

| Bytes | Before scoring SHA-256 | After scoring SHA-256 |
| --- | --- | --- |
| `tools/mado-binds.py` | `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950` | `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950` |
| `controls/K2NaiveEval.py` | `1956b510986554fae970fd2107bd6a5284de74b3ffbeeb5b711b47a22476cdca` | `1956b510986554fae970fd2107bd6a5284de74b3ffbeeb5b711b47a22476cdca` |
| `c2/count.py` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` | `b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8` |
| `harness/oracle.py` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` | `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441` |

Receipt SHA-256: `f566da7a643f216ba132639eb180bdcec4a27c146c518f40749c0b5df3da3900`.

Restoration was unnecessary: protected source bytes were never mutated, and their final hashes equal the initial hashes. The separately named negative control is retained as the requested deliverable; no pristine/mutant/restored source mutation was performed for this control assignment.

## Verbatim receipts

### Run 1

```text
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2NaiveEval.py sha256:1956b510986554fae970fd2107bd6a5284de74b3ffbeeb5b711b47a22476cdca
seed=a7b25982776f11a4
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal binds=192
CASE BASE           PASS oracle_binds=192 missing=0 extra=0 (unperturbed)
CASE A00            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=69 key="F13" code=0 disp="exec" arg="echo {{39*2+6.2}}" | missing mask=12 key="U" code=0 disp="exec" arg="echo {{6.2 - 8.1}}" | extra mask=69 key="F13" code=0 disp="exec" arg="echo \\84.2" | extra mask=68 key="F20" code=0 disp="resizeactive" arg="202.90909090909093 2067.39" (ARITH[escaped+resize+escaped]@sourced)
CASE A01            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=12 key="F16" code=0 disp="resizeactive" arg="54 0" | extra mask=12 key="KP_3" code=0 disp="moveactive" arg="9 -{{29 / {{13*10.10 + 21}}}}" | extra mask=12 key="F16" code=0 disp="resizeactive" arg="{{{{13*10.10 + 21}} + 20}} 0" (ARITH[unclosed+move+desc]@sourced)
CASE A02            FAIL oracle_binds=193 missing=1 extra=2 | missing mask=65 key="F14" code=0 disp="resizeactive" arg="9 22" | extra mask=12 key="KP_8" code=0 disp="resizeactive" arg="11.857142857142858 0" | extra mask=65 key="F14" code=0 disp="resizeactive" arg="9.0 31.333333333333332" (ARITH[desc+resize]@sourced)
CASE A03            FAIL oracle_binds=195 missing=3 extra=3 | missing mask=72 key="F18" code=0 disp="workspace" arg="256" | missing mask=76 key="KP_7" code=0 disp="exec" arg="echo {{ 24 / 11 / 3.478*8.0 }}" | extra mask=72 key="F18" code=0 disp="workspace" arg="256.0" | extra mask=76 key="KP_7" code=0 disp="exec" arg="echo \\5.018558210047571" (ARITH[var+escaped+escaped]@sourced)
CASE A04            FAIL oracle_binds=193 missing=1 extra=4 | missing mask=12 key="U" code=0 disp="exec" arg="echo {{(23 / 26 - 34)/4}}" | extra mask=68 key="F17" code=0 disp="exec" arg="notify-send r26 -25.798000000000002" | extra mask=76 key="KP_8" code=0 disp="resizeactive" arg="0.44694586988909124 0" (ARITH[exec+desc+resize+escaped]@sourced)
CASE A05            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=12 key="F18" code=0 disp="exec" arg="echo {{ 24 / 35 + 5.92 }}" | extra mask=12 key="F18" code=0 disp="exec" arg="echo \\6.605714285714286" (ARITH[escaped+unclosed]@sourced)
CASE A06            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=64 key="F16" code=0 disp="exec" arg="echo {{ (6 + 9.1 * 31) + 1 }}" | missing mask=72 key="I" code=0 disp="workspace" arg="$arnkko" | extra mask=64 key="F16" code=0 disp="exec" arg="echo \\289.09999999999997" | extra mask=69 key="F13" code=0 disp="resizeactive" arg="{{ {{ 6.897 * 6 - 26 }}+24 }} 48.2" (ARITH[escaped+resize+var]@root)
CASE A07            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=72 key="U" code=0 disp="exec" arg="echo {{3.1 / 13 + 3.1}}" | missing mask=72 key="KP_6" code=0 disp="exec" arg="notify-send r26 73.34303" | extra mask=72 key="U" code=0 disp="exec" arg="echo \\3.3384615384615386" | extra mask=12 key="B" code=0 disp="resizeactive" arg="13464 0" (ARITH[escaped+desc+exec]@sourced)
CASE A08            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=65 key="U" code=0 disp="resizeactive" arg="45.887 0" | missing mask=69 key="KP_8" code=0 disp="workspace" arg="1524.8999" | extra mask=65 key="U" code=0 disp="resizeactive" arg="{{15.887 + 30 - {{10.85 + 34 + 7}}}} 0" | extra mask=72 key="B" code=0 disp="resizeactive" arg="19.7 12.94986301369863" (ARITH[desc+resize+var]@sourced)
CASE A09            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=72 key="9" code=0 disp="moveactive" arg="160 -39.760002" | missing mask=76 key="8" code=0 disp="exec" arg="notify-send r26 2.3899994" | extra mask=72 key="9" code=0 disp="moveactive" arg="800 -1296.68" | extra mask=76 key="8" code=0 disp="exec" arg="notify-send r26 2.7469210526315795" (ARITH[move+exec]@sourced)
CASE A10            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=68 key="KP_8" code=0 disp="exec" arg="echo {{0.1 * 21 + 19}}" | missing mask=76 key="F13" code=0 disp="exec" arg="notify-send r26 0.20512821" | extra mask=68 key="KP_8" code=0 disp="exec" arg="echo \\21.1" | extra mask=76 key="F13" code=0 disp="exec" arg="notify-send r26 0.20512820512820512" (ARITH[escaped+exec]@sourced)
CASE A11            FAIL oracle_binds=193 missing=1 extra=2 | missing mask=12 key="F15" code=0 disp="workspace" arg="$armlom" | extra mask=12 key="F15" code=0 disp="workspace" arg="4.2" | extra mask=65 key="F18" code=0 disp="workspace" arg="32.6224" (ARITH[var+ws]@sourced)
CASE A12            FAIL oracle_binds=195 missing=1 extra=2 | missing mask=64 key="F14" code=0 disp="exec" arg="echo {{29*28*26}}" | extra mask=69 key="M" code=0 disp="moveactive" arg="64.44444444444444 -42.0" | extra mask=64 key="F14" code=0 disp="exec" arg="echo \\21112" (ARITH[move+exec+escaped+unclosed]@sourced)
CASE A13            FAIL oracle_binds=193 missing=0 extra=1 | extra mask=72 key="O" code=0 disp="exec" arg="notify-send r26 {{ ({{ (32 * 23) * 2 }} / 12) + 1 (ARITH[exec+unclosed]@sourced)
CASE A14            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=72 key="KP_7" code=0 disp="exec" arg="echo {{1 - 3.136 / 32}}" | missing mask=12 key="F17" code=0 disp="moveactive" arg="1 -inf" | extra mask=72 key="KP_7" code=0 disp="exec" arg="echo \\0.902" | extra mask=12 key="F17" code=0 disp="moveactive" arg="0.08 -{{ 31 / 0 }}" (ARITH[escaped+move+desc+desc]@sourced)
CASE A15            FAIL oracle_binds=195 missing=2 extra=3 | missing mask=72 key="F18" code=0 disp="exec" arg="echo {{ 3.58 / 1.57 + 8.567 }}" | missing mask=76 key="8" code=0 disp="workspace" arg="$arpmmm" | extra mask=65 key="O" code=0 disp="exec" arg="notify-send r26 104.54761904761905" | extra mask=72 key="F18" code=0 disp="exec" arg="echo \\10.847254777070063" (ARITH[exec+escaped+unclosed+var]@sourced)
CASE A16            FAIL oracle_binds=193 missing=1 extra=2 | missing mask=68 key="M" code=0 disp="workspace" arg="1.7920012" | extra mask=76 key="9" code=0 disp="resizeactive" arg="856 0" | extra mask=68 key="M" code=0 disp="workspace" arg="54.76991941718704" (ARITH[desc+ws]@sourced)
CASE A17            FAIL oracle_binds=193 missing=1 extra=3 | missing mask=64 key="F16" code=0 disp="resizeactive" arg="75.689995 0" | extra mask=64 key="F16" code=0 disp="resizeactive" arg="75.68999999999998 0" | extra mask=12 key="F16" code=0 disp="resizeactive" arg="34.10529118458634 0" (ARITH[desc+desc+move]@sourced)
CASE A18            FAIL oracle_binds=193 missing=1 extra=4 | missing mask=65 key="F20" code=0 disp="resizeactive" arg="42 0" | extra mask=65 key="F20" code=0 disp="resizeactive" arg="312 0" | extra mask=69 key="F15" code=0 disp="workspace" arg="60" (ARITH[desc+ws+move+resize]@sourced)
CASE A19            FAIL oracle_binds=193 missing=1 extra=3 | missing mask=72 key="Y" code=0 disp="exec" arg="echo {{33 * 13 - 17}}" | extra mask=12 key="F19" code=0 disp="moveactive" arg="3191 -10.0" | extra mask=72 key="Y" code=0 disp="exec" arg="echo \\412" (ARITH[move+escaped+resize]@sourced)
CASE A20            FAIL oracle_binds=195 missing=3 extra=4 | missing mask=65 key="F16" code=0 disp="exec" arg="echo {{ 23 + 1.4 }}" | missing mask=12 key="KP_8" code=0 disp="resizeactive" arg="23 0" | extra mask=65 key="F16" code=0 disp="exec" arg="echo \\24.4" | extra mask=12 key="KP_8" code=0 disp="resizeactive" arg="{{ 7 + 16 + {{14+18*12 - 2.697}} * 16 }} 0" (ARITH[escaped+desc+escaped+resize]@sourced)
CASE A21            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=12 key="KP_6" code=0 disp="exec" arg="echo {{ 2.5 * 6 + 1 + 24 }}" | missing mask=64 key="7" code=0 disp="exec" arg="notify-send r26 294.4" | extra mask=12 key="KP_6" code=0 disp="exec" arg="echo \\40.0" | extra mask=69 key="F17" code=0 disp="resizeactive" arg="5.5200000000000005 75.6" (ARITH[escaped+resize+exec]@root)
CASE A22            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=64 key="KP_8" code=0 disp="moveactive" arg="575 -66" | extra mask=64 key="KP_8" code=0 disp="moveactive" arg="278.70000000000005 -314" (ARITH[ws+move]@sourced)
CASE A23            FAIL oracle_binds=193 missing=1 extra=3 | missing mask=68 key="KP_8" code=0 disp="workspace" arg="50" | extra mask=68 key="KP_6" code=0 disp="resizeactive" arg="-446 0" | extra mask=68 key="KP_8" code=0 disp="workspace" arg="34.8421052631579" (ARITH[desc+var+resize]@sourced)
CASE A24            FAIL oracle_binds=195 missing=3 extra=4 | missing mask=68 key="8" code=0 disp="exec" arg="notify-send r26 28" | missing mask=68 key="KP_2" code=0 disp="resizeactive" arg="3.2797046 0" | extra mask=68 key="8" code=0 disp="exec" arg="notify-send r26 {{16 + 12*{{8.769 / 18.28}} * 0.4 | extra mask=76 key="F19" code=0 disp="workspace" arg="{{10.31+{{8.769 / 18.28}}+24+30}}" (ARITH[exec+ws+desc+move]@sourced)
CASE A25            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=72 key="U" code=0 disp="resizeactive" arg="38.72 -1.6866674" | missing mask=76 key="F18" code=0 disp="workspace" arg="20.366667" | extra mask=72 key="U" code=0 disp="resizeactive" arg="38.72 {{10.98 - {{38 / 3}}}}" | extra mask=12 key="I" code=0 disp="resizeactive" arg="{{ 40+{{38 / 3}} + 12 }} 0" (ARITH[resize+desc+move+ws]@sourced)
CASE A26            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=69 key="O" code=0 disp="exec" arg="echo {{ 27 + 23*29 / 22 }}" | extra mask=69 key="O" code=0 disp="exec" arg="echo \\57.31818181818181" | extra mask=76 key="N" code=0 disp="moveactive" arg="3.7439999999999998 -91" (ARITH[escaped+unclosed+move]@sourced)
CASE A27            FAIL oracle_binds=192 missing=0 extra=4 | extra mask=72 key="7" code=0 disp="resizeactive" arg="17.22 144" | extra mask=12 key="KP_2" code=0 disp="workspace" arg="31" (ARITH[resize+ws+desc+exec]@sourced)
CASE A28            PASS oracle_binds=194 missing=0 extra=0 (ARITH[exec+unclosed]@sourced)
CASE A29            FAIL oracle_binds=195 missing=3 extra=3 | missing mask=72 key="F19" code=0 disp="exec" arg="echo {{39 + 30 + 23}}" | missing mask=65 key="F18" code=0 disp="resizeactive" arg="32 0" | extra mask=72 key="F19" code=0 disp="exec" arg="echo \\92" | extra mask=65 key="F18" code=0 disp="resizeactive" arg="31 0" (ARITH[escaped+desc+exec]@sourced)
CASE VADD-0         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
CASE VADD-1         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
CASE VUNBIND-0      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=65 key='' keycode=21)
CASE VUNBIND-1      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=65 key='W' keycode=0)
CASE VVARIABLE-0    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $varagvla)
CASE VVARIABLE-1    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vtjlhvbz)
CASE VSOURCE-0      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 13)
CASE VSOURCE-1      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 20)
CASE VGLOB-0        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VGLOB-1        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VUNSOURCED-0   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VUNSOURCED-1   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VCOMMENT-0     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .config/hypr/bindings.conf)
CASE VCOMMENT-1     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .config/hypr/bindings.conf)
CASE VSYNTH-0       PASS oracle_binds=14 missing=0 extra=0 (SYNTH tree binds=14 unbound=1 vars=2)
CASE VSYNTH-1       PASS oracle_binds=18 missing=0 extra=0 (SYNTH tree binds=18 unbound=1 vars=2)
CASE VREWRITE-0     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=72 key='LEFT' code=0; unbind mask=65 key='E' code=0; add movecurrentworkspacetomonitor)
CASE VREWRITE-1     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=65 key='E' code=0; unbind mask=12 key='TAB' code=0; add sendshortcut)
CASE VHARD-0        PASS oracle_binds=19 missing=0 extra=0 (HARD tree lines=27 binds=19 unbinds=2 vars=4)
CASE VHARD-1        PASS oracle_binds=24 missing=0 extra=0 (HARD tree lines=34 binds=24 unbinds=3 vars=4)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=22/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### Run 2

```text
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2NaiveEval.py sha256:1956b510986554fae970fd2107bd6a5284de74b3ffbeeb5b711b47a22476cdca
seed=4ed2001e835c2b67
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal binds=192
CASE BASE           PASS oracle_binds=192 missing=0 extra=0 (unperturbed)
CASE A00            FAIL oracle_binds=194 missing=0 extra=1 | extra mask=76 key="F17" code=0 disp="exec" arg="notify-send r26 804.9359999999999" (ARITH[exec+unclosed+unclosed]@sourced)
CASE A01            FAIL oracle_binds=196 missing=2 extra=2 | missing mask=68 key="KP_2" code=0 disp="exec" arg="notify-send r26 154.8" | missing mask=72 key="F18" code=0 disp="workspace" arg="-7.6000004" | extra mask=68 key="KP_2" code=0 disp="exec" arg="notify-send r26 154.79999999999998" | extra mask=72 key="F18" code=0 disp="workspace" arg="-300.0" (ARITH[var+unclosed+exec+ws]@sourced)
CASE A02            FAIL oracle_binds=193 missing=1 extra=3 | missing mask=64 key="KP_6" code=0 disp="moveactive" arg="1 -4.75" | extra mask=12 key="Y" code=0 disp="resizeactive" arg="123.58 0" | extra mask=64 key="KP_6" code=0 disp="moveactive" arg="{{ {{ 13.399 + 1 }} / 14.399 - 37 * 14.399 }} -40 (ARITH[desc+move+desc]@sourced)
CASE A03            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=76 key="Y" code=0 disp="exec" arg="echo {{ (24 + 2.475*9) * 2 }}" | extra mask=76 key="Y" code=0 disp="exec" arg="echo \\92.55000000000001" (ARITH[unclosed+escaped]@sourced)
CASE A04            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=64 key="KP_6" code=0 disp="workspace" arg="$arokpp" | missing mask=72 key="F19" code=0 disp="exec" arg="echo {{18.59 * 4}}" | extra mask=64 key="KP_6" code=0 disp="workspace" arg="26" | extra mask=72 key="F19" code=0 disp="exec" arg="echo \\74.36" (ARITH[var+escaped]@sourced)
CASE A05            FAIL oracle_binds=195 missing=1 extra=2 | missing mask=76 key="F16" code=0 disp="exec" arg="echo {{3+$arbjic}}" | extra mask=76 key="F16" code=0 disp="exec" arg="echo {{3+{{ (31*11 - 34) + 1 }}}}" | extra mask=65 key="F15" code=0 disp="exec" arg="notify-send r26 -1.4375" (ARITH[unclosed+escaped+unclosed+exec]@sourced)
CASE A06            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=68 key="KP_7" code=0 disp="workspace" arg="-5" | missing mask=64 key="KP_6" code=0 disp="exec" arg="echo {{25 * 18.14+31}}" | extra mask=68 key="KP_7" code=0 disp="workspace" arg="15" | extra mask=64 key="KP_6" code=0 disp="exec" arg="echo \\484.5" (ARITH[var+escaped+move]@sourced)
CASE A07            FAIL oracle_binds=194 missing=0 extra=2 | extra mask=69 key="U" code=0 disp="exec" arg="notify-send r26 {{(18.802+26 + 40 + {{35*9.40+3.2 | extra mask=12 key="F14" code=0 disp="resizeactive" arg="18 0" (ARITH[unclosed+unclosed+exec+desc]@sourced)
CASE A08            FAIL oracle_binds=195 missing=1 extra=1 | missing mask=64 key="7" code=0 disp="resizeactive" arg="1 45" | extra mask=64 key="7" code=0 disp="resizeactive" arg="1.0 4567.0" (ARITH[unclosed+unclosed+resize]@sourced)
CASE A09            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=12 key="Y" code=0 disp="resizeactive" arg="53.57 0" | missing mask=72 key="O" code=0 disp="workspace" arg="21.880001" | extra mask=12 key="Y" code=0 disp="resizeactive" arg="11.0 0" | extra mask=72 key="O" code=0 disp="workspace" arg="294.28816" (ARITH[desc+var+resize+resize]@sourced)
CASE A10            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=76 key="N" code=0 disp="resizeactive" arg="18.64 0" | missing mask=12 key="F20" code=0 disp="exec" arg="echo {{ 5.0 / 4.09*6 }}" | extra mask=76 key="N" code=0 disp="resizeactive" arg="19.956129032258065 0" | extra mask=12 key="F20" code=0 disp="exec" arg="echo \\7.334963325183375" (ARITH[desc+escaped+desc]@sourced)
CASE A11            FAIL oracle_binds=196 missing=4 extra=4 | missing mask=68 key="F14" code=0 disp="exec" arg="echo {{28 + 20*20}}" | missing mask=68 key="Y" code=0 disp="exec" arg="echo {{ 17+18*15 / 33 }}" | extra mask=68 key="F14" code=0 disp="exec" arg="echo {{28 + {{ 14 + 6 + 38 }}*58}}" | extra mask=68 key="Y" code=0 disp="exec" arg="echo \\25.18181818181818" (ARITH[escaped+escaped+move+var]@sourced)
CASE A12            FAIL oracle_binds=196 missing=4 extra=4 | missing mask=68 key="F15" code=0 disp="exec" arg="echo {{13.8*34 - 32+21}}" | missing mask=12 key="KP_6" code=0 disp="workspace" arg="$aroonk" | extra mask=68 key="F15" code=0 disp="exec" arg="echo \\458.20000000000005" | extra mask=12 key="KP_6" code=0 disp="workspace" arg="420.0" (ARITH[escaped+var+move+ws]@sourced)
CASE A13            FAIL oracle_binds=195 missing=3 extra=3 | missing mask=68 key="KP_2" code=0 disp="workspace" arg="-24.34" | missing mask=65 key="M" code=0 disp="moveactive" arg="58.66964 -0.43589744" | extra mask=68 key="KP_2" code=0 disp="workspace" arg="52.71324" | extra mask=65 key="M" code=0 disp="moveactive" arg="58.669641 -6.076410256410256" (ARITH[ws+move+exec]@sourced)
CASE A14            FAIL oracle_binds=193 missing=1 extra=2 | missing mask=12 key="O" code=0 disp="workspace" arg="1.5" | extra mask=76 key="B" code=0 disp="resizeactive" arg="47.69230769230769 0" | extra mask=12 key="O" code=0 disp="workspace" arg="20.166666666666668" (ARITH[desc+ws]@sourced)
CASE A15            FAIL oracle_binds=195 missing=2 extra=2 | missing mask=69 key="F19" code=0 disp="moveactive" arg="-23 -25" | missing mask=69 key="F19" code=0 disp="exec" arg="echo {{13+13.7 / 16.28+35}}" | extra mask=69 key="F19" code=0 disp="moveactive" arg="-373 -25" | extra mask=69 key="F19" code=0 disp="exec" arg="echo \\48.84152334152334" (ARITH[move+exec+escaped]@sourced)
CASE A16            FAIL oracle_binds=194 missing=0 extra=2 | extra mask=76 key="N" code=0 disp="resizeactive" arg="74.52941176470588 0" | extra mask=69 key="F13" code=0 disp="resizeactive" arg="-101.498 0" (ARITH[unclosed+desc+desc+unclosed]@sourced)
CASE A17            FAIL oracle_binds=193 missing=0 extra=1 | extra mask=69 key="B" code=0 disp="workspace" arg="78.69999999999999" (ARITH[unclosed+ws]@sourced)
CASE A18            FAIL oracle_binds=196 missing=3 extra=3 | missing mask=76 key="7" code=0 disp="exec" arg="notify-send r26 262" | missing mask=76 key="9" code=0 disp="exec" arg="echo {{24*15.79}}" | extra mask=76 key="7" code=0 disp="exec" arg="notify-send r26 {{{{9 * 30}}+22 - 8 + 9}}" | extra mask=76 key="9" code=0 disp="exec" arg="echo \\378.96" (ARITH[exec+escaped+unclosed+var]@sourced)
CASE A19            FAIL oracle_binds=192 missing=0 extra=2 | extra mask=64 key="F19" code=0 disp="resizeactive" arg="17.017083 0" | extra mask=76 key="F14" code=0 disp="workspace" arg="876" (ARITH[desc+ws]@sourced)
CASE A20            FAIL oracle_binds=196 missing=3 extra=3 | missing mask=68 key="F20" code=0 disp="resizeactive" arg="3.6526535 46" | missing mask=12 key="KP_3" code=0 disp="exec" arg="echo {{ (17 * 20) + 1 }}" | extra mask=68 key="F20" code=0 disp="resizeactive" arg="1.7375511141741327 40" | extra mask=12 key="KP_3" code=0 disp="exec" arg="echo \\341" (ARITH[resize+exec+escaped+var]@sourced)
CASE A21            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=76 key="B" code=0 disp="workspace" arg="$arnlpl" | extra mask=76 key="B" code=0 disp="workspace" arg="5.338899999999999" (ARITH[var+ws]@sourced)
CASE A22            PASS oracle_binds=194 missing=0 extra=0 (ARITH[unclosed+unclosed]@sourced)
CASE A23            PASS oracle_binds=194 missing=0 extra=0 (ARITH[unclosed+unclosed]@sourced)
CASE A24            FAIL oracle_binds=193 missing=1 extra=3 | missing mask=65 key="KP_7" code=0 disp="resizeactive" arg="38 0" | extra mask=65 key="B" code=0 disp="moveactive" arg="0.4 -180" | extra mask=12 key="F14" code=0 disp="resizeactive" arg="1.027027027027027 12.0" (ARITH[move+resize+desc]@sourced)
CASE A25            FAIL oracle_binds=196 missing=3 extra=3 | missing mask=64 key="KP_3" code=0 disp="exec" arg="echo {{ 30 * 34+16.0 / 2 }}" | missing mask=72 key="M" code=0 disp="exec" arg="notify-send r26 18" | extra mask=64 key="KP_3" code=0 disp="exec" arg="echo \\1028.0" | extra mask=72 key="M" code=0 disp="exec" arg="notify-send r26 27.0" (ARITH[ws+escaped+exec+ws]@sourced)
CASE A26            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=12 key="KP_8" code=0 disp="workspace" arg="48" | missing mask=68 key="F20" code=0 disp="exec" arg="echo {{ 18 * 9 / 30 }}" | extra mask=69 key="Y" code=0 disp="resizeactive" arg="285.0 13.43" | extra mask=65 key="Y" code=0 disp="exec" arg="notify-send r26 13.7" (ARITH[resize+exec+var+escaped]@sourced)
CASE A27            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=76 key="F15" code=0 disp="workspace" arg="1" | missing mask=68 key="KP_6" code=0 disp="resizeactive" arg="13.4 0" | extra mask=76 key="F15" code=0 disp="workspace" arg="24.625" | extra mask=68 key="KP_6" code=0 disp="resizeactive" arg="30.4 0" (ARITH[ws+desc]@sourced)
CASE A28            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=65 key="N" code=0 disp="workspace" arg="38" | extra mask=72 key="B" code=0 disp="moveactive" arg="-12 -13.728200000000001" | extra mask=65 key="N" code=0 disp="workspace" arg="21" (ARITH[var+move+ws]@sourced)
CASE A29            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=64 key="F15" code=0 disp="workspace" arg="-8" | extra mask=68 key="U" code=0 disp="exec" arg="notify-send r26 963" | extra mask=64 key="F15" code=0 disp="workspace" arg="20.031496062992126" (ARITH[exec+unclosed+ws]@sourced)
CASE VADD-0         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
CASE VADD-1         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE VUNBIND-0      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=64 key='' keycode=12)
CASE VUNBIND-1      PASS oracle_binds=190 missing=0 extra=0 (UNBIND mask=8 key='TAB' keycode=0)
CASE VVARIABLE-0    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vejbmfzh)
CASE VVARIABLE-1    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vkliaaeh)
CASE VSOURCE-0      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 6)
CASE VSOURCE-1      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 16)
CASE VGLOB-0        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VGLOB-1        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VUNSOURCED-0   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VUNSOURCED-1   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VCOMMENT-0     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
CASE VCOMMENT-1     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .config/hypr/bindings.conf)
CASE VSYNTH-0       PASS oracle_binds=16 missing=0 extra=0 (SYNTH tree binds=16 unbound=1 vars=2)
CASE VSYNTH-1       PASS oracle_binds=17 missing=0 extra=0 (SYNTH tree binds=17 unbound=1 vars=2)
CASE VREWRITE-0     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=64 key='TAB' code=0; unbind mask=64 key='J' code=0; add resizeactive)
CASE VREWRITE-1     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=65 key='SLASH' code=0; unbind mask=0 key='XF86TouchpadOn' code=0; add exec)
CASE VHARD-0        PASS oracle_binds=21 missing=0 extra=0 (HARD tree lines=33 binds=21 unbinds=2 vars=4)
CASE VHARD-1        PASS oracle_binds=23 missing=0 extra=0 (HARD tree lines=29 binds=23 unbinds=2 vars=4)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=23/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```
