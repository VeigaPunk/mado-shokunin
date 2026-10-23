# K2DoNothing — C2 do-nothing control (round-26, w1)

## Verdict

CONTROL K2DoNothing best: cases_pass=0/51 [embed_hits=0] verdict=TARGET_MISSED — not met

Both do-nothing shapes tie at 0/51 with embed_hits=0. The higher of the two is the `[]`-printing
tool only in that it returns a well-formed empty bind table; the zero-byte file never gets past the
counter's "stdout is not JSON" gate. Neither can pass a single case: the frozen C2 target needs the
round-25 behaviour preserved *and* hyprlang `{{…}}` evaluated, and a do-nothing tool produces
neither. The claim is not reachable by this shape.

## What was built

Both are single python3 stdlib files with the tool CLI (`--home DIR`); neither opens `--home`.

| file | bytes | sha256 | behaviour |
|---|---|---|---|
| `.ufo/waves/round-26/controls/K2DoNothing.py` | 247 | `5b51bd4fb0f7d6e6b40013554ca3c94e7964820df18dea0b9875a5e5e3c6e747` | parses `--home`, prints `[]` |
| `.ufo/waves/round-26/controls/K2DoNothing-empty.py` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | zero-byte file; exits 0 with empty stdout |

The zero-byte variant is the assignment's "empty tool file" shape; the named control
`K2DoNothing.py` is the strongest version this shape allows (a syntactically valid empty table).

## Exact commands

Counter and pins verified before scoring: `c2/count.py` sha256
`b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8`,
`harness/oracle.py` sha256 `680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441`.

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
prlimit --as=4000000000:8000000000 timeout 880 python3 -I .ufo/waves/round-26/c2/count.py 96101be5 \
  > .ufo/waves/round-26/controls/K2DoNothing-base.txt
prlimit --as=4000000000:8000000000 timeout 880 python3 -I .ufo/waves/round-26/c2/count.py 05319e0f \
  --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2DoNothing.py
prlimit --as=4000000000:8000000000 timeout 880 python3 -I .ufo/waves/round-26/c2/count.py 05319e0f \
  --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2DoNothing-empty.py
```

Each control variant was run twice; the counter draws a fresh seed per run (seeds printed in the
receipts). No `--seed` was passed.

## Scored results

| variant | run | seed | cases_pass | embed_hits | verdict | exit | receipt |
|---|---|---|---|---|---|---|---|
| `[]` print | 1 | `c0a2c6490cc0a94a` | 0/51 | 0 | TARGET_MISSED | 1 | `controls/K2DoNothing.txt` (run 1) |
| `[]` print | 2 | `a28ce20e2e882252` | 0/51 | 0 | TARGET_MISSED | 1 | `controls/K2DoNothing.txt` (run 2) |
| empty file | 1 | `82ab36f5c61ea632` | 0/51 | 0 | TARGET_MISSED | 1 | `controls/K2DoNothing-empty.txt` (run 1) |
| empty file | 2 | `cf1950a6de788be4` | 0/51 | 0 | TARGET_MISSED | 1 | `controls/K2DoNothing-empty.txt` (run 2) |

Every run: `ORACLE_CHECK base_twice equal binds=192`, `HOST_SAFETY hyprland_coredumps_before=1335
after=1335 delta=0`. Failure gates differ as expected: `[]` yields
`missing=<oracle count> extra=0` on all 51 cases (oracle_binds ranged 10–196); the empty file yields
`stdout is not JSON` on all 51 cases.

Receipt digests:

```
50d2162c65d870a1d4c6591c5447890b55e21c74934fd9494cfaea39d4753343  controls/K2DoNothing.txt
faefd7a28ff43c7e3890282833f0e5b88b853a4779064b024ffe91bc6f1819c0  controls/K2DoNothing-empty.txt
b58d1f8b33b7dbd456170bfd14f508f352ad365df8b8e3e6e477809e5e4b3313  controls/K2DoNothing-base.txt
a5239b6c867d2eef4a3dc239d3af3b6409e66cbcf41e93cfbae4592351c0de5e  controls/K2DoNothing-base-guard-run1.txt
3a10ab53d3a86129eea58bdf39a167fb01923eafbcf0f21f602c5639b5a6bc7e  controls/K2DoNothing-base-guard-run2.txt
```

Each `.txt` holds the two verbose run receipts; runs are separated by the line
`# --- run 2 (fresh seed) ---`, which is not counter output. Raw stdout/stderr staging lives at
`/fast/scratch/hyaku/mado-r26/k2-donothing/` (counter tmp dirs removed themselves).

## Base receipt at REV `96101be5` (no `--tool-file`, round-25 `tools/mado-binds.py`)

Verbatim stdout of the valid run, file `controls/K2DoNothing-base.txt`:

```
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=96101be523b2f6e897eee743d5b396b0225bf9ed oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=tools/mado-binds.py@96101be523b2 sha256:9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950
seed=7ab0f5c55dbb496d
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal binds=192
CASE BASE           PASS oracle_binds=192 missing=0 extra=0 (unperturbed)
CASE A00            FAIL oracle_binds=193 missing=1 extra=2 | missing mask=65 key="F17" code=0 disp="workspace" arg="5.97997" | extra mask=69 key="KP_3" code=0 disp="resizeactive" arg="{{ {{20 / 13.405 - 26}}+{{20 / 13.405 - 26}} }} { | extra mask=65 key="F17" code=0 disp="workspace" arg="{{8.922 / {{20 / 13.405 - 26}}}}" (ARITH[resize+ws]@sourced)
CASE A01            FAIL oracle_binds=192 missing=0 extra=4 | extra mask=65 key="F16" code=0 disp="moveactive" arg="{{30*0}} -{{33 - 9.280+29}}" | extra mask=76 key="8" code=0 disp="moveactive" arg="{{26 * 13.89}} -{{(4.232 + 28+4.6) * 2}}" (ARITH[move+move+resize+move]@sourced)
CASE A02            FAIL oracle_binds=193 missing=0 extra=1 | extra mask=76 key="KP_2" code=0 disp="moveactive" arg="{{ 7.746 - 38 }} -{{ 13.83+7.9 }}" (ARITH[move+unclosed]@sourced)
CASE A03            FAIL oracle_binds=195 missing=1 extra=1 | missing mask=64 key="N" code=0 disp="exec" arg="notify-send r26 55" | extra mask=64 key="N" code=0 disp="exec" arg="notify-send r26 {{11 * 5 - 16.683 + 5}}" (ARITH[escaped+exec+unclosed]@sourced)
CASE A04            FAIL oracle_binds=193 missing=0 extra=1 | extra mask=76 key="F13" code=0 disp="resizeactive" arg="{{(23 / 3.8+15 / 16) * 2}} 0" (ARITH[desc+unclosed]@sourced)
CASE A05            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=68 key="F14" code=0 disp="exec" arg="notify-send r26 0.62068963" | missing mask=69 key="KP_6" code=0 disp="workspace" arg="$armono" | extra mask=68 key="F14" code=0 disp="exec" arg="notify-send r26 {{ 18 / 29 - 0 + 14 }}" | extra mask=69 key="KP_6" code=0 disp="workspace" arg="{{ (6*14 - 24+1.4)/4 }}" (ARITH[exec+var]@sourced)
CASE A06            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=12 key="7" code=0 disp="workspace" arg="0.33333334" | missing mask=76 key="Y" code=0 disp="workspace" arg="0.44117647" | extra mask=12 key="7" code=0 disp="workspace" arg="{{ 1 / 3 }}" | extra mask=12 key="F18" code=0 disp="moveactive" arg="{{(29 + 16)/4}} -{{34 - 2*35 + 6.484}}" (ARITH[ws+move+desc+var]@sourced)
CASE A07            FAIL oracle_binds=196 missing=3 extra=3 | missing mask=12 key="9" code=0 disp="workspace" arg="0.33333334" | missing mask=65 key="B" code=0 disp="moveactive" arg="14.7 -174.42001" | extra mask=12 key="9" code=0 disp="workspace" arg="{{ 1 / 3 }}" | extra mask=65 key="B" code=0 disp="moveactive" arg="{{ 13.7 + 1 }} -{{ 9.18 * 19 / 2.45 - 34 }}" (ARITH[var+move+unclosed+resize]@sourced)
CASE A08            FAIL oracle_binds=195 missing=2 extra=3 | missing mask=68 key="M" code=0 disp="exec" arg="echo {{0.53846157*29}}" | missing mask=69 key="F20" code=0 disp="resizeactive" arg="29 1.22" | extra mask=69 key="M" code=0 disp="workspace" arg="{{ (12.83*{{21 / 39 - 4}} - 11 + 4.345) * 2 }}" | extra mask=68 key="M" code=0 disp="exec" arg="echo {{{{21 / 39 - 4}}*29}}" (ARITH[ws+escaped+resize+unclosed]@sourced)
CASE A09            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=65 key="N" code=0 disp="workspace" arg="1.2857143" | missing mask=69 key="KP_3" code=0 disp="moveactive" arg="-5 -1.3333334" | extra mask=65 key="N" code=0 disp="workspace" arg="{{ 18 / 14 }}" | extra mask=65 key="F17" code=0 disp="resizeactive" arg="{{ 20+22 }} {{ 12 / 12 }}" (ARITH[var+resize+exec+move]@sourced)
CASE A10            FAIL oracle_binds=195 missing=2 extra=2 | missing mask=64 key="9" code=0 disp="workspace" arg="560" | missing mask=65 key="8" code=0 disp="workspace" arg="2.0531673" | extra mask=64 key="9" code=0 disp="workspace" arg="{{20 * 28 - 1.355}}" | extra mask=65 key="8" code=0 disp="workspace" arg="{{1.1 / {{17.68 / 33}} + 30 / 30}}" (ARITH[escaped+ws+var]@sourced)
CASE A11            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=64 key="F20" code=0 disp="workspace" arg="366" | extra mask=64 key="F20" code=0 disp="workspace" arg="{{ 12.2 * 30 - 5.537+{{ 0 - 11.3 }} }}" | extra mask=68 key="F13" code=0 disp="resizeactive" arg="{{16.08 - 8.92}} 0" (ARITH[unclosed+ws+desc]@sourced)
CASE A12            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=64 key="KP_3" code=0 disp="workspace" arg="5.714286" | extra mask=69 key="O" code=0 disp="workspace" arg="{{ (38 - 8.7+23) + 1 }}" | extra mask=64 key="KP_3" code=0 disp="workspace" arg="{{ 40 / 7 - 14.2+11 }}" (ARITH[ws+unclosed+var]@sourced)
CASE A13            FAIL oracle_binds=195 missing=1 extra=1 | missing mask=76 key="F17" code=0 disp="workspace" arg="0.4819277" | extra mask=76 key="F17" code=0 disp="workspace" arg="{{8 / 16.6 * 14*26}}" (ARITH[escaped+unclosed+var]@sourced)
CASE A14            FAIL oracle_binds=193 missing=0 extra=2 | extra mask=76 key="KP_4" code=0 disp="workspace" arg="{{(24*34) * 2}}" | extra mask=64 key="F13" code=0 disp="resizeactive" arg="{{ 30*20+17*3 }} 0" (ARITH[unclosed+ws+desc]@sourced)
CASE A15            FAIL oracle_binds=192 missing=0 extra=3 | extra mask=12 key="F17" code=0 disp="resizeactive" arg="{{ 6.0+{{ 15.563*25 }} * 9.0 }} 0" | extra mask=64 key="B" code=0 disp="moveactive" arg="{{ 6.0 * 19 }} -{{ ({{ 15.563*25 }} - 37*4.701 +  (ARITH[desc+move+ws]@sourced)
CASE A16            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=65 key="F15" code=0 disp="workspace" arg="$armlon" | missing mask=69 key="8" code=0 disp="resizeactive" arg="5.3999996 5700" | extra mask=65 key="F15" code=0 disp="workspace" arg="{{ 6.7*6.7 }}" | extra mask=69 key="8" code=0 disp="resizeactive" arg="{{ 19.400 - 14*9.4 }} {{ 25*6.7 * {{ 12 * 19+11+4 (ARITH[var+resize]@sourced)
CASE A17            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=64 key="KP_8" code=0 disp="moveactive" arg="15.925001 -70.700005" | missing mask=72 key="7" code=0 disp="workspace" arg="-8.4" | extra mask=64 key="KP_8" code=0 disp="moveactive" arg="{{ 7 * 2.275 }} -{{ 10 * 7.070*12 }}" | extra mask=72 key="7" code=0 disp="workspace" arg="{{ 8.6 - 17 }}" (ARITH[move+ws]@sourced)
CASE A18            FAIL oracle_binds=195 missing=2 extra=2 | missing mask=12 key="KP_4" code=0 disp="exec" arg="echo {{($arbfdg - $arbfdg) * 2}}" | missing mask=69 key="U" code=0 disp="workspace" arg="$arpppn" | extra mask=12 key="KP_4" code=0 disp="exec" arg="echo {{({{ (14.988+37)/4 }} - {{ (14.988+37)/4 }} | extra mask=69 key="U" code=0 disp="workspace" arg="{{ {{ (14.988+37)/4 }} * {{ (14.988+37)/4 }} / 9  (ARITH[unclosed+escaped+var]@sourced)
CASE A19            PASS oracle_binds=194 missing=0 extra=0 (ARITH[escaped+unclosed]@sourced)
CASE A20            FAIL oracle_binds=195 missing=2 extra=3 | missing mask=65 key="KP_2" code=0 disp="resizeactive" arg="49.815 56.23" | missing mask=68 key="7" code=0 disp="exec" arg="notify-send r26 -7.240999" | extra mask=65 key="KP_8" code=0 disp="workspace" arg="{{(17 * {{12.230 + 6 + 30}} * {{12.230 + 6 + 30}} | extra mask=65 key="KP_2" code=0 disp="resizeactive" arg="{{ 37 + 12.815+{{12.230 + 6 + 30}} + 6 }} {{38*26 (ARITH[unclosed+ws+resize+exec]@sourced)
CASE A21            FAIL oracle_binds=195 missing=3 extra=4 | missing mask=69 key="M" code=0 disp="workspace" arg="0.2153846" | missing mask=64 key="F20" code=0 disp="workspace" arg="34.4" | extra mask=69 key="M" code=0 disp="workspace" arg="{{8.4 / 39}}" | extra mask=64 key="F14" code=0 disp="exec" arg="notify-send r26 {{ (15 * 8.05 + 8.4*10)/4 }}" (ARITH[var+exec+var+exec]@sourced)
CASE A22            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=65 key="KP_4" code=0 disp="workspace" arg="12" | extra mask=76 key="N" code=0 disp="resizeactive" arg="{{ (33+38 * 10.6 * 17)/4 }} {{9.5+36}}" | extra mask=65 key="KP_4" code=0 disp="workspace" arg="{{ 2.0*8.20 + 10 }}" (ARITH[escaped+resize+ws]@sourced)
CASE A23            FAIL oracle_binds=195 missing=2 extra=3 | missing mask=72 key="F15" code=0 disp="workspace" arg="28.6" | missing mask=12 key="F20" code=0 disp="workspace" arg="31.772999" | extra mask=72 key="F15" code=0 disp="workspace" arg="{{0.6+19.09 + 28 - 6.2}}" | extra mask=12 key="KP_4" code=0 disp="exec" arg="notify-send r26 {{24*27}}" (ARITH[ws+exec+escaped+var]@sourced)
CASE A24            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=76 key="8" code=0 disp="resizeactive" arg="1.8571428 25.27" | missing mask=68 key="KP_2" code=0 disp="workspace" arg="0.58853376" | extra mask=76 key="8" code=0 disp="resizeactive" arg="{{39+5.6*32 / 21}} {{ 23 + 2.27 }}" | extra mask=68 key="KP_2" code=0 disp="workspace" arg="{{ 1 - {{6 / 14.582 * 21 * 4.511}} - 10.4 }}" (ARITH[resize+ws+resize+desc]@sourced)
CASE A25            FAIL oracle_binds=195 missing=3 extra=4 | missing mask=76 key="KP_2" code=0 disp="workspace" arg="10" | missing mask=69 key="KP_4" code=0 disp="workspace" arg="10" | extra mask=76 key="KP_2" code=0 disp="workspace" arg="{{5 + 5 + 8}}" | extra mask=69 key="KP_4" code=0 disp="workspace" arg="{{5*1 + 5 + 18}}" (ARITH[ws+var+move+desc]@sourced)
CASE A26            FAIL oracle_binds=195 missing=3 extra=4 | missing mask=64 key="9" code=0 disp="workspace" arg="6.270097" | missing mask=12 key="F14" code=0 disp="exec" arg="notify-send r26 0.30634573" | extra mask=64 key="9" code=0 disp="workspace" arg="{{39*2 / 6.22 * 2.8}}" | extra mask=12 key="F14" code=0 disp="exec" arg="notify-send r26 {{ 2.8 / 9.14 + 35+34 }}" (ARITH[var+exec+desc+var]@sourced)
CASE A27            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=65 key="U" code=0 disp="resizeactive" arg="12.4 16" | extra mask=65 key="U" code=0 disp="resizeactive" arg="{{4+12.6 + 8.4 * 3.2}} {{3 + 13*8}}" | extra mask=72 key="F17" code=0 disp="resizeactive" arg="{{ (15 * 40 * 33 * 0)/4 }} {{15.9 / 4+37 * 20}}" (ARITH[resize+resize+unclosed]@sourced)
CASE A28            FAIL oracle_binds=193 missing=0 extra=1 | extra mask=64 key="F15" code=0 disp="moveactive" arg="{{ 4.5+4+11 }} -{{(31+7*2.2) * 2}}" (ARITH[escaped+move]@sourced)
CASE A29            FAIL oracle_binds=193 missing=1 extra=3 | missing mask=12 key="KP_6" code=0 disp="workspace" arg="$arnlkn" | extra mask=68 key="B" code=0 disp="resizeactive" arg="{{ {{37+4.2}} - {{37+4.2}} }} {{(20+4.2 - 14) * 2 | extra mask=12 key="KP_6" code=0 disp="workspace" arg="{{({{37+4.2}}+5.733 + 3 + 40) * 2}}" (ARITH[resize+var+move]@sourced)
CASE VADD-0         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE VADD-1         PASS oracle_binds=193 missing=0 extra=0 (ADD into .config/hypr/bindings.conf)
CASE VUNBIND-0      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=8 key='XF86MonBrightnessDown' keycode=0)
CASE VUNBIND-1      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=73 key='' keycode=15)
CASE VVARIABLE-0    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vrbhiemm)
CASE VVARIABLE-1    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vgspiwfy)
CASE VSOURCE-0      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 9)
CASE VSOURCE-1      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 4)
CASE VGLOB-0        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VGLOB-1        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VUNSOURCED-0   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VUNSOURCED-1   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VCOMMENT-0     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
CASE VCOMMENT-1     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE VSYNTH-0       PASS oracle_binds=17 missing=0 extra=0 (SYNTH tree binds=17 unbound=1 vars=2)
CASE VSYNTH-1       PASS oracle_binds=10 missing=0 extra=0 (SYNTH tree binds=10 unbound=1 vars=2)
CASE VREWRITE-0     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=68 key='B' code=0; unbind mask=68 key='A' code=0; add cyclenext)
CASE VREWRITE-1     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=73 key='TAB' code=0; unbind mask=72 key='' code=61; add movecurrentworkspacetomonitor)
CASE VHARD-0        PASS oracle_binds=20 missing=0 extra=0 (HARD tree lines=31 binds=20 unbinds=2 vars=4)
CASE VHARD-1        PASS oracle_binds=24 missing=0 extra=0 (HARD tree lines=32 binds=24 unbinds=2 vars=4)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=22/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

Base reading: the round-25 tool passes BASE (unperturbed, 192 binds), all 20 V3 no-harm cases and one
ARITH case (A19, whose unclosed braces Hyprland also leaves literal) = 22/51. Every other ARITH case
fails with the `{{…}}` expression left where Hyprland evaluated it — the gap C2 names. `embed_hits=0`
for the base tool.

## Exit-2 guard runs (kept, reported verbatim, not scoring evidence)

Two base attempts before the valid receipt hit the counter guard and measured nothing. Their files
are `controls/K2DoNothing-base-guard-run1.txt` and `...-run2.txt`.

```
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=96101be523b2f6e897eee743d5b396b0225bf9ed oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=tools/mado-binds.py@96101be523b2 sha256:9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950
seed=25d0ecf8906ef032
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
SETUP_ERROR ORACLE_FAIL BASE: sandbox exited rc=1 before answering sandbox exited rc=1 before answering
exit=2
```

```
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=96101be523b2f6e897eee743d5b396b0225bf9ed oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=tools/mado-binds.py@96101be523b2 sha256:9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950
seed=a368972ab5f8279d
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
SETUP_ERROR ORACLE_FAIL BASE: sandbox exited rc=1 before answering sandbox exited rc=1 before answering
exit=2
```

Cause, measured: both runs wrapped the counter in `prlimit --as=4000000000` (no hard value), which
sets the hard AS limit to 4 GB. `oracle.py:146` starts its sandbox with
`prlimit --core=0 --as=8000000000`; raising the hard limit back to 8 GB fails for an unprivileged
process, so that prlimit exits 1 and both BASE oracles die before Hyprland starts. Demonstration:

```
$ prlimit --as=4000000000 prlimit --as=8000000000 true
prlimit: failed to set the AS resource limit: Operation not permitted
hard_cap_rc=1
$ prlimit --as=4000000000: prlimit --as=8000000000 true
soft_cap_rc=0
```

The L1 sent the same correction during the run: never wrap counter/oracle runs in an outer hard
`--as` below 8 GB; use `--as=4000000000:8000000000`. All scoring runs above used that soft-4 GB /
hard-8 GB form. This is a harness-usage error on my side, not a counter defect: the counter's guard
did its job (no cases scored, exit 2), and the re-run under the corrected cap produced the valid
receipts.

## Files changed

Created (all under `.ufo/waves/round-26/`; no lane source, tool, counter or harness file touched):

- `controls/K2DoNothing.py`
- `controls/K2DoNothing-empty.py`
- `controls/K2DoNothing.txt`
- `controls/K2DoNothing-empty.txt`
- `controls/K2DoNothing-base.txt`
- `controls/K2DoNothing-base-guard-run1.txt`
- `controls/K2DoNothing-base-guard-run2.txt`
- `w1/reports/K2DoNothing.md` (this report)

No git/jj write commands were run. No tools were installed or upgraded (nothing needed).
Scratch staging only at `/fast/scratch/hyaku/mado-r26/k2-donothing/`.

## Risks and blockers

- No blocker. The control is scored twice per shape with fresh seeds; all four runs are exit 1
  (TARGET_MISSED), oracle-stable (`base_twice equal binds=192`) and coredump-neutral (delta 0).
- The counter's embed guard can only fire on a tool whose bytes contain an oracle arg/description
  string of 12+ characters; a do-nothing tool satisfies it trivially, so `embed_hits=0` carries no
  information for this shape.
- Host load was ~15 with several sibling oracle runs in flight during scoring; the only oracle
  failures observed were the two self-inflicted 4 GB hard-cap runs above. No other instability.
- The existing `evidence/c2-before-96101be5.txt` (not mine) holds only a command header; the base
  receipt quoted here is the complete 51-case run and is independent of that file.
