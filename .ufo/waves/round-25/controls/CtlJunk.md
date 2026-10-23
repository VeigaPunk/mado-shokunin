# Round 25 control — CtlJunk

Shape: JUNK / CONTENT-FREE.

Axes: minimum skipped-work cost; frozen-detector exactness; scratch isolation and exact byte restoration.

## Stub and expected detector

The pristine candidate ignores all arguments and config bytes and prints `[]`. The single mutation changes only the output construction: 192 objects, each with exactly the frozen counter's 18 field names, with a fresh random 64-bit integer for every value. These are intentionally junk values, not semantically typed bind values. Neither variant opens config files, follows sources or globs, resolves variables, processes comments or unbinds, queries the compositor, or embeds a live table. Both skip the real resolver entirely.

Expected detector: the frozen C1 counter compares the complete 18-field multiset for BASE and all 32 generated cases; meeting requires `cases_pass=33/33` and `embed_hits=0`. Missing or junk content is expected to fail exact comparison, not merely a syntax check.

Two requested candidate variants were scored. One initial invocation exited 2 before scoring because the evaluation subprocess environment lacked `HYPRLAND_INSTANCE_SIGNATURE`; its full output is retained below. Following the registration's exit-2 rule, the empty candidate was rerun with the existing host session variables read via `printenv`. The mutation-tester role additionally requires a restored-bytes detector run; that repeat is restoration evidence, not another candidate or a retry seeking success. All invocations used the unchanged counter and the command below.

Exact command (same argv and working directory for every invocation):

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 python3 -I .ufo/waves/round-25/c1/count.py 04051723562b8a6ac1f3a9ae05e861aa6f544aff --tool-file /fast/scratch/hyaku/mado-r25/controls/CtlJunk/stub.py
```

For the two scored variants and restored-bytes run, the subprocess environment inherited the evaluation environment with these existing host values supplied locally: `HYPRLAND_INSTANCE_SIGNATURE=efb50993780079460b0cbed1363e2166a2de1d9f_1792655744_595856120`, `WAYLAND_DISPLAY=wayland-1`; `XDG_RUNTIME_DIR=/run/user/1000` and `HOME=/home/vgpnk` were already present. No host environment, config, compositor state, or services were changed. No replay capture or fixed counter seed was used.

Pristine and restored source (also copied byte-exact to `controls/CtlJunk.py`):

```python
#!/usr/bin/env python3
print("[]")
```

Scored random variant (preserved at `/fast/scratch/hyaku/mado-r25/controls/CtlJunk/random-192.py`):

```python
#!/usr/bin/env python3
import json
import random

FIELDS = "locked mouse release repeat longPress non_consuming auto_consuming has_description modmask submap submap_universal key keycode catch_all description allow_input_capture dispatcher arg".split()
print(json.dumps([{field: random.getrandbits(64) for field in FIELDS} for _ in range(192)]))
```

## Initial setup-error attempt — empty array

Complete counter stdout, verbatim:

```text
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/CtlJunk/stub.py sha256:79218fca456a13bce9450ce8f3fcb0888bf9a98b5b0ad6ee9c930c26e7e281ed
seed=1df23a1d9d654e9c
SETUP_ERROR hyprctl binds -j failed: CalledProcessError(1, ['timeout', '20', 'hyprctl', 'binds', '-j'])
```

Exit code: `2`.

Counter stderr: empty.

Final predicate line: absent; setup exited before PRED-C1 was emitted. Verdict for this attempt: inconclusive, not a detector rejection.

## Scored candidate 1 — empty array

Complete counter stdout, verbatim:

```text
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/CtlJunk/stub.py sha256:79218fca456a13bce9450ce8f3fcb0888bf9a98b5b0ad6ee9c930c26e7e281ed
seed=25989e3cade4df37
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
CASE BASE         FAIL missing=192 extra=0 (unperturbed)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 (ADD into .config/hypr/bindings.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 (ADD into .config/hypr/bindings.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 (UNBIND mask=69 key='SPACE' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 (UNBIND mask=0 key='XF86TouchpadToggle' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 (UNBIND mask=1 key='XF86MonBrightnessUp' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 (UNBIND mask=68 key='SPACE' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 (VARIABLE $vvgdnetq)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 (VARIABLE $viedieyo)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 (VARIABLE $vzikyhfa)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 (VARIABLE $vowmusxt)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 (SOURCE new file at root line 5)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 (SOURCE new file at root line 13)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 (SOURCE new file at root line 20)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 (SOURCE new file at root line 29)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-0       FAIL missing=193 extra=0 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-1       FAIL missing=193 extra=0 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-2       FAIL missing=193 extra=0 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-3       FAIL missing=193 extra=0 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-0  FAIL missing=192 extra=0 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-1  FAIL missing=192 extra=0 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-2  FAIL missing=192 extra=0 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-3  FAIL missing=192 extra=0 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-0    FAIL missing=193 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 (COMMENT into .config/hypr/bindings.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=12 extra=0 (SYNTH tree binds=12 unbound=1 vars=3)
    missing mask=9 key="F17" code=0 disp="exec" arg="logger wee1cjriiw"
    missing mask=8 key="SLASH" code=0 disp="exec" arg="notify-send 7py92dhdiy"
CASE SYNTH-1      FAIL missing=15 extra=0 (SYNTH tree binds=15 unbound=1 vars=3)
    missing mask=4 key="COMMA" code=0 disp="exec" arg="logger lmxfgqvyax"
    missing mask=73 key="DELETE" code=0 disp="exec" arg="logger nug03d51er"
CASE SYNTH-2      FAIL missing=12 extra=0 (SYNTH tree binds=12 unbound=1 vars=3)
    missing mask=76 key="F10" code=0 disp="exec" arg="true teqscr79wb"
    missing mask=65 key="3" code=0 disp="exec" arg="notify-send f4xp4oyion"
CASE SYNTH-3      FAIL missing=14 extra=0 (SYNTH tree binds=14 unbound=1 vars=2)
    missing mask=13 key="F10" code=0 disp="exec" arg="t8dwut7u7 kl4c"
    missing mask=4 key="G" code=0 disp="exec" arg="t8dwut7u7 caue"
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

Exit code: `1`.

Counter stderr: empty.

Final predicate line: `PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED`.

## Scored candidate 2 — 192 random objects

Complete counter stdout, verbatim:

```text
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/CtlJunk/stub.py sha256:6af8321be0a80af87f9a9f5ba11d43c5c710bb5ce12981a25992efffb69818a6
seed=9890342cec6faaf2
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
CASE BASE         FAIL missing=192 extra=192 (unperturbed)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=11747243827559631154 key=18294081122186794639 code=7654048406526808504 disp=196710184336236153 arg=107754475326585159
    extra   mask=59683002338954478 key=11537780469881870984 code=7608564797482419584 disp=1004561752614949553 arg=11748512446469745800
CASE ADD-0        FAIL missing=193 extra=192 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=10627605334740177956 key=4362910701515853502 code=15284815845228472435 disp=15927115800226053748 arg=13790516300508883216
    extra   mask=562501799461066 key=3669306606369026330 code=14629127077376104578 disp=13491467861584357441 arg=7285137715646857717
CASE ADD-1        FAIL missing=193 extra=192 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=15198391592183533109 key=540295062121714961 code=6291517981084952314 disp=4895872467374334401 arg=6595966798284770468
    extra   mask=16476793135210210036 key=13127506282257595316 code=1335411344955894334 disp=14868512912741905849 arg=16124538756333909144
CASE ADD-2        FAIL missing=193 extra=192 (ADD into .config/hypr/bindings.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=13517426691942544736 key=11247404815196302746 code=8863220385836838283 disp=8841496461419040493 arg=17388905086878635121
    extra   mask=7929401961620023496 key=3296784252207731398 code=9581404799568246018 disp=15595333919020774625 arg=15008505011630311102
CASE ADD-3        FAIL missing=193 extra=192 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=4863233006433181054 key=16692394202258402992 code=11857973403241531703 disp=1373106349325357763 arg=16163991486643442886
    extra   mask=8722278166774172437 key=18153372375879409892 code=16956126493438186048 disp=3866801759389837971 arg=7361714164706245564
CASE UNBIND-0     FAIL missing=191 extra=192 (UNBIND mask=65 key='Y' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=10413363449958803543 key=18415332521624619613 code=8694032988135307898 disp=9693032006624359064 arg=1880963461922546778
    extra   mask=2408661962243513900 key=7173504380090122868 code=7818594399956857243 disp=2030266098891178333 arg=4119461382386052108
CASE UNBIND-1     FAIL missing=191 extra=192 (UNBIND mask=68 key='V' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=10609847414743824035 key=621963812325525968 code=15337428688140539609 disp=3975218988446338821 arg=1394974970675252438
    extra   mask=4039608644436776825 key=674316685270240711 code=4699099409114772712 disp=2190769902330463557 arg=10163548701050540425
CASE UNBIND-2     FAIL missing=191 extra=192 (UNBIND mask=72 key='SPACE' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=5374325178817651744 key=3735998407595357599 code=3378657627278216058 disp=7195546288058169514 arg=16538407651483770317
    extra   mask=18119399884751022832 key=10564589757738353269 code=17931194975938787601 disp=11284565361947915115 arg=14380427865644806900
CASE UNBIND-3     FAIL missing=191 extra=192 (UNBIND mask=73 key='COMMA' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=13203076974862475932 key=10851731782457382721 code=322782709753139458 disp=5189827402513362131 arg=9338177689799502033
    extra   mask=9949712513999296104 key=3129465571183753860 code=7804462781385197378 disp=12260377599814073630 arg=1029006318300169397
CASE VARIABLE-0   FAIL missing=193 extra=192 (VARIABLE $vglnckev)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=2122639139169898090 key=9225855949818705124 code=4819854434543519415 disp=9303262733859008992 arg=9928010112035300424
    extra   mask=10569751483477211375 key=17982535957655686904 code=664168661099463501 disp=15739614457323650047 arg=8039503464467899656
CASE VARIABLE-1   FAIL missing=193 extra=192 (VARIABLE $vzmzeafv)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=897465457632437402 key=15130688395298824037 code=18418651945524400387 disp=11725837644244330484 arg=18105375452768740290
    extra   mask=4983027470572648874 key=4267886385153459770 code=17564551402391014034 disp=15097640641805165707 arg=7312450417474573642
CASE VARIABLE-2   FAIL missing=193 extra=192 (VARIABLE $vhhagyhk)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=4787802718223073182 key=16922302078461573610 code=4970840839661791885 disp=15817443690502921347 arg=7049110117703834921
    extra   mask=8688170024699375262 key=10963928221403822588 code=9424807517871680947 disp=527966474809023233 arg=11558962244805045965
CASE VARIABLE-3   FAIL missing=193 extra=192 (VARIABLE $vnqnkhlo)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=9629454595926348522 key=4040750276919544288 code=14633705227575163651 disp=4780408662096103158 arg=10301664528450359655
    extra   mask=5242715242889013010 key=17935046717716056215 code=1246299584550571411 disp=4985214021188666859 arg=12832805634749658263
CASE SOURCE-0     FAIL missing=194 extra=192 (SOURCE new file at root line 29)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=10542208879942866828 key=16522414594579257745 code=8045199935988455597 disp=7208897733145586925 arg=8877242469690617504
    extra   mask=3504748551251534535 key=9235722582100510249 code=7580063679968877129 disp=2043387028243222789 arg=10378466748493292745
CASE SOURCE-1     FAIL missing=194 extra=192 (SOURCE new file at root line 11)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=5947164144067364807 key=12066348623829582676 code=16722707305784330502 disp=15692897860837241824 arg=3217671008584575226
    extra   mask=15395031778567710300 key=1311423676370261254 code=10766963727814031541 disp=13476188094771541864 arg=16884488759244663074
CASE SOURCE-2     FAIL missing=194 extra=192 (SOURCE new file at root line 4)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=1954305111835466208 key=7429875208167519722 code=17396065620776705607 disp=5994765587926039536 arg=3068440293165036733
    extra   mask=14754493382091073174 key=11382438883309109225 code=3199230737114406367 disp=3463082325526700690 arg=4658182743202211872
CASE SOURCE-3     FAIL missing=194 extra=192 (SOURCE new file at root line 5)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=11879544501449131003 key=14437022719283851646 code=9120814971132416566 disp=3750976942953882675 arg=397599428587959905
    extra   mask=13417550473907125170 key=9271287392264245441 code=12895997497682314164 disp=16975885322298054534 arg=1597692694573282123
CASE GLOB-0       FAIL missing=193 extra=192 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=11782363938492101551 key=17138238963159701098 code=2427849075818790991 disp=13077719146903178367 arg=7332228191676985017
    extra   mask=11955299892847579750 key=15476460384880184795 code=4664184028518294832 disp=6978623018475236168 arg=13660972959345681042
CASE GLOB-1       FAIL missing=193 extra=192 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=2917465154469473634 key=6402198580189557496 code=9036238341347440344 disp=15967512986807971352 arg=2548950892522039610
    extra   mask=9222759871456567966 key=15657584831080089735 code=12407091495286968620 disp=5805629347123152305 arg=7992515704741970497
CASE GLOB-2       FAIL missing=193 extra=192 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=7843687466324484574 key=3978589194505612712 code=15891207952188484889 disp=3265348698800106777 arg=346442942911390113
    extra   mask=48813089173671978 key=12177066656702854109 code=5109434372610394786 disp=17286647363851907332 arg=13161283365511430285
CASE GLOB-3       FAIL missing=193 extra=192 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=326077248643866990 key=16367604407815892999 code=6137753925839001804 disp=9842192094944641077 arg=17547207315090072222
    extra   mask=6901032614446682549 key=1334587732802042910 code=3821193290940935138 disp=18417399921649406686 arg=5128676540976109251
CASE UNSOURCED-0  FAIL missing=192 extra=192 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=3801026871826787782 key=12579853793155198769 code=8233168385220872635 disp=18113645154616779130 arg=7463032197242536197
    extra   mask=17832485792031490945 key=10688741409337556862 code=13651176586473584421 disp=17516425399815448675 arg=2889878808165207853
CASE UNSOURCED-1  FAIL missing=192 extra=192 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=10661975142279971239 key=787482693434086946 code=16548478515612820211 disp=14293521805641484360 arg=12949831797089026607
    extra   mask=5697169742875951437 key=1946221667808454428 code=2553060009580875335 disp=2796909270853770389 arg=8535137135861300426
CASE UNSOURCED-2  FAIL missing=192 extra=192 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=11683463668221178663 key=2144483814896065045 code=5046548489594399063 disp=18369156141411471975 arg=12930006938781178176
    extra   mask=12867079183104223527 key=11669964038526879774 code=17761169546377226304 disp=10706464024443416699 arg=6259414761282073512
CASE UNSOURCED-3  FAIL missing=192 extra=192 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=18233134668506074519 key=17706547424028079912 code=9329115534563010030 disp=17317236504273907268 arg=14411523098268704108
    extra   mask=12781463433348156225 key=929846335026452792 code=17609976970048377567 disp=2528439215707159857 arg=16749800498268486374
CASE COMMENT-0    FAIL missing=193 extra=192 (COMMENT into .config/hypr/bindings.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=11671067358295766474 key=3227841294300357951 code=132119484567445289 disp=7373579828978339598 arg=3128021818065803676
    extra   mask=5404632683237135667 key=14423783811708217173 code=10328846685334738429 disp=2567596183220696512 arg=16274247155994878060
CASE COMMENT-1    FAIL missing=193 extra=192 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=2988090511883403990 key=2168632830269598686 code=8541565778274583429 disp=8809198579933485869 arg=2747217222748634814
    extra   mask=2448944870166312939 key=17025237824036997142 code=11358098567857700795 disp=13224999030856253489 arg=14039970914270730028
CASE COMMENT-2    FAIL missing=193 extra=192 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=17896648980518087461 key=11846347637064352429 code=10547683328450948221 disp=1531169234348870668 arg=10240076533074153474
    extra   mask=17609752310397549424 key=12530078070985612032 code=4555419705098030664 disp=2853194975045320656 arg=9905011599120742957
CASE COMMENT-3    FAIL missing=193 extra=192 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
    extra   mask=18003167327135246946 key=9473690714001628214 code=13563023034903229409 disp=6747829218483002424 arg=13097264921430557125
    extra   mask=9924035469061243187 key=868023654218612952 code=15385958097639194950 disp=1560050959413883634 arg=16907833656635256638
CASE SYNTH-0      FAIL missing=14 extra=192 (SYNTH tree binds=14 unbound=1 vars=3)
    missing mask=65 key="S" code=0 disp="exec" arg="logger 2hwvyifzzb"
    missing mask=65 key="F3" code=0 disp="exec" arg="0p3iied1v 3p0i"
    extra   mask=10859786030305527260 key=183428768955396241 code=7612874434700977797 disp=6881945216952666851 arg=9158106536300571106
    extra   mask=16356793058350491729 key=16369206468588504099 code=4023255862474548629 disp=4075730791089062164 arg=2591929710390796535
CASE SYNTH-1      FAIL missing=13 extra=192 (SYNTH tree binds=13 unbound=1 vars=3)
    missing mask=69 key="Z" code=0 disp="exec" arg="notify-send sts7fbxs1o"
    missing mask=69 key="HOME" code=0 disp="exec" arg="true wb8fis9yg5"
    extra   mask=15490485442615815644 key=16162120827522626733 code=17798629602125487564 disp=5243579689611567982 arg=16028263515634267203
    extra   mask=2823452589780931221 key=6571265858853029003 code=8666627525124489040 disp=13701706100201368819 arg=11808314450491089510
CASE SYNTH-2      FAIL missing=10 extra=192 (SYNTH tree binds=10 unbound=1 vars=2)
    missing mask=5 key="K" code=0 disp="exec" arg="01tu6a0uk 88ii"
    missing mask=68 key="F15" code=0 disp="exec" arg="printf wd67224byz"
    extra   mask=15080819652085248701 key=5860657816194832960 code=17361074255431703225 disp=576079806127322861 arg=15154585559682807008
    extra   mask=7904719533786654456 key=14101024568377775771 code=17941521345370072114 disp=6637829937200795067 arg=13812572268173430129
CASE SYNTH-3      FAIL missing=16 extra=192 (SYNTH tree binds=16 unbound=1 vars=3)
    missing mask=9 key="Y" code=0 disp="exec" arg="dg5vib8yi 7rg0"
    missing mask=5 key="H" code=0 disp="exec" arg="v0d6sw5l3 cpvx"
    extra   mask=4241249500289345298 key=10006902388077070815 code=3367348079623613298 disp=10930099725196550078 arg=1783396061297601927
    extra   mask=13646996361300232852 key=3433349575009307597 code=6526608580087677172 disp=953719266451446688 arg=1625845955255522826
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

Exit code: `1`.

Counter stderr: empty.

Final predicate line: `PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED`.

## Restored-byte detector run — empty array

Complete counter stdout, verbatim:

```text
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/CtlJunk/stub.py sha256:79218fca456a13bce9450ce8f3fcb0888bf9a98b5b0ad6ee9c930c26e7e281ed
seed=a81d38341124c173
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
CASE BASE         FAIL missing=192 extra=0 (unperturbed)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-0        FAIL missing=193 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-1        FAIL missing=193 extra=0 (ADD into .config/hypr/bindings.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-2        FAIL missing=193 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE ADD-3        FAIL missing=193 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-0     FAIL missing=191 extra=0 (UNBIND mask=72 key='F' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-1     FAIL missing=191 extra=0 (UNBIND mask=64 key='RETURN' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-2     FAIL missing=191 extra=0 (UNBIND mask=8 key='PRINT' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNBIND-3     FAIL missing=191 extra=0 (UNBIND mask=68 key='I' keycode=0)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-0   FAIL missing=193 extra=0 (VARIABLE $vavzxndh)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-1   FAIL missing=193 extra=0 (VARIABLE $vferkobd)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-2   FAIL missing=193 extra=0 (VARIABLE $vwvrakvg)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE VARIABLE-3   FAIL missing=193 extra=0 (VARIABLE $vyirwcwo)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-0     FAIL missing=194 extra=0 (SOURCE new file at root line 20)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-1     FAIL missing=194 extra=0 (SOURCE new file at root line 5)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-2     FAIL missing=194 extra=0 (SOURCE new file at root line 18)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SOURCE-3     FAIL missing=194 extra=0 (SOURCE new file at root line 7)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-0       FAIL missing=193 extra=0 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-1       FAIL missing=193 extra=0 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-2       FAIL missing=193 extra=0 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE GLOB-3       FAIL missing=193 extra=0 (GLOB new toggles file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-0  FAIL missing=192 extra=0 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-1  FAIL missing=192 extra=0 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-2  FAIL missing=192 extra=0 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE UNSOURCED-3  FAIL missing=192 extra=0 (UNSOURCED new bindings file)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-0    FAIL missing=193 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-1    FAIL missing=193 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-2    FAIL missing=193 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE COMMENT-3    FAIL missing=193 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
    missing mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    missing mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-0      FAIL missing=15 extra=0 (SYNTH tree binds=15 unbound=1 vars=3)
    missing mask=13 key="PERIOD" code=0 disp="exec" arg="printf 3l8sken12b"
    missing mask=64 key="F17" code=0 disp="exec" arg="printf uxd9w4t0ve"
CASE SYNTH-1      FAIL missing=12 extra=0 (SYNTH tree binds=12 unbound=1 vars=3)
    missing mask=65 key="F10" code=0 disp="exec" arg="logger 4w6v2qhffe"
    missing mask=8 key="6" code=0 disp="exec" arg="printf tdkxuuxn16"
CASE SYNTH-2      FAIL missing=12 extra=0 (SYNTH tree binds=12 unbound=1 vars=2)
    missing mask=9 key="F10" code=0 disp="exec" arg="logger wsxzbxipum"
    missing mask=4 key="2" code=0 disp="exec" arg="printf nds18xpqoi"
CASE SYNTH-3      FAIL missing=11 extra=0 (SYNTH tree binds=11 unbound=1 vars=2)
    missing mask=12 key="4" code=0 disp="exec" arg="ncxgtwewe orq1"
    missing mask=9 key="F" code=0 disp="exec" arg="ncxgtwewe ie76"
PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED
```

Exit code: `1`.

Counter stderr: empty.

Final predicate line: `PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED`.

## Verdict and restoration evidence

Both requested candidate scores were `cases_pass=0/33`, `embed_hits=0`, `TARGET_MISSED`, exit 1. The empty candidate had no extras; the junk candidate had 192 extras in every case, including BASE, despite matching the live table's row count and all 18 field names. The restored empty candidate again scored 0/33, exit 1.

Mutation-probe verdict: **inconclusive as a killed/survived experiment**, because the pristine content-free baseline itself fails the behavioral predicate. This is not labeled a killed mutant. Control verdict: neither assigned shortcut met the target.

Observed SHA-256 hashes:

| Bytes | Before / after SHA-256 |
|---|---|
| Pristine `stub.py`, before mutation | `79218fca456a13bce9450ce8f3fcb0888bf9a98b5b0ad6ee9c930c26e7e281ed` |
| Mutated `stub.py`, during random-192 score | `6af8321be0a80af87f9a9f5ba11d43c5c710bb5ce12981a25992efffb69818a6` |
| Preserved scratch `random-192.py` | `6af8321be0a80af87f9a9f5ba11d43c5c710bb5ce12981a25992efffb69818a6` |
| Restored `stub.py`, before restoration detector and after copy | `79218fca456a13bce9450ce8f3fcb0888bf9a98b5b0ad6ee9c930c26e7e281ed` |
| Lane `controls/CtlJunk.py`, byte-exact restored stub copy | `79218fca456a13bce9450ce8f3fcb0888bf9a98b5b0ad6ee9c930c26e7e281ed` |
| Frozen `c1/count.py`, before and after all candidate mutations | `70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895` |
| Frozen `registration.md`, before and after all candidate mutations | `a0afab65428112e7ef1b118bed3889491ed0de6729eeb2ae955c1f485f5695e5` |

The before/restored hashes match exactly, and the restored bytes were exercised by the same bounded counter. The two lane artifacts written by this seat are this receipt and `CtlJunk.py` only. All counter subprocesses returned; no background jobs or services were launched. Tools installed or updated: none. No git or jj write commands were run.

PRED-C1 cases_pass=0/33 embed_hits=0 verdict=TARGET_MISSED

CONTROL CtlJunk: not met
