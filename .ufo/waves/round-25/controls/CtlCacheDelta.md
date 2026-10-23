# CtlCacheDelta — CACHE + DELTA control

## Shape and shortcut

This is one pre-data adversarial replacement for the claimed faithful static bind-table resolver. It is not that resolver. No production resolver existed or was edited.

The stub embeds the captured 192-entry live bind table and SHA-256 hashes of every original snapshot file line: 79 files, 16,176 lines, 15,302 distinct hashes. Line hashes use raw bytes with line terminators removed (`bytes.splitlines()`); the inventory matches the frozen counter's four roots and one-MiB file bound, including non-config files. The table and hash list are encoded together with zlib and Base85. The scored stub is 725,444 bytes.

At run time it scans every file under those four roots without following a source graph. Cached lines are ignored. Only uncached lines receive a naive parser: strip `#` comments, collect newly seen `$var = value` assignments, parse comma-separated bind/unbind lines, and patch the embedded table. It neither parses the original binds nor reconstructs a table from config bytes. It ignores source reachability, source/glob evaluation, deletions of cached lines, original variable semantics, submaps, and general Hyprland grammar. It contains no case-label, seed, or fixture-name lookup.

Expected detector: the frozen 33-case PRED-C1 counter, with exact 18-field bind multisets and its literal-string embedding check. In particular, indiscriminate scanning should reject this shortcut on UNSOURCED, and carrying the captured table into a replacement tree should reject it on SYNTH. The fresh run below actually did so.

## Exact command

```sh
cd /home/vgpnk/Projects/shokunin/mado-shokunin && timeout 900 python3 -I .ufo/waves/round-25/c1/count.py 04051723562b8a6ac1f3a9ae05e861aa6f544aff --tool-file /fast/scratch/hyaku/mado-r25/controls/CtlCacheDelta/stub.py
```

Executed once with the lane as the working directory. No replay seed, saved-live override, counter changes, or post-score stub changes were used. The counter itself took fresh read-only live captures. Standard error was empty. Exit code: **1**.

## Complete counter stdout (verbatim)

```text
counter sha256:70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895 rev=04051723562b8a6ac1f3a9ae05e861aa6f544aff
tool=override:/fast/scratch/hyaku/mado-r25/controls/CtlCacheDelta/stub.py sha256:cf778a491f0da77eab0ce6c05c60da4d2cf0035134f96aa17bc7f7ad2db66dd2
seed=888bae3198896032
live=hyprctl binds -j sha256:9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727 live_binds=192
CASE BASE         PASS missing=0 extra=0 (unperturbed)
CASE ADD-0        PASS missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
CASE ADD-1        PASS missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
CASE ADD-2        PASS missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
CASE ADD-3        PASS missing=0 extra=0 (ADD into .config/hypr/bindings.conf)
CASE UNBIND-0     PASS missing=0 extra=0 (UNBIND mask=73 key='LEFT' keycode=0)
CASE UNBIND-1     PASS missing=0 extra=0 (UNBIND mask=68 key='SPACE' keycode=0)
CASE UNBIND-2     PASS missing=0 extra=0 (UNBIND mask=0 key='XF86AudioPrev' keycode=0)
CASE UNBIND-3     PASS missing=0 extra=0 (UNBIND mask=64 key='TAB' keycode=0)
CASE VARIABLE-0   PASS missing=0 extra=0 (VARIABLE $vhrwxhbg)
CASE VARIABLE-1   PASS missing=0 extra=0 (VARIABLE $vykzimiq)
CASE VARIABLE-2   PASS missing=0 extra=0 (VARIABLE $vjcguqyh)
CASE VARIABLE-3   PASS missing=0 extra=0 (VARIABLE $vfwumnlv)
CASE SOURCE-0     PASS missing=0 extra=0 (SOURCE new file at root line 17)
CASE SOURCE-1     PASS missing=0 extra=0 (SOURCE new file at root line 19)
CASE SOURCE-2     PASS missing=0 extra=0 (SOURCE new file at root line 10)
CASE SOURCE-3     PASS missing=0 extra=0 (SOURCE new file at root line 11)
CASE GLOB-0       PASS missing=0 extra=0 (GLOB new toggles file)
CASE GLOB-1       PASS missing=0 extra=0 (GLOB new toggles file)
CASE GLOB-2       PASS missing=0 extra=0 (GLOB new toggles file)
CASE GLOB-3       PASS missing=0 extra=0 (GLOB new toggles file)
CASE UNSOURCED-0  FAIL missing=0 extra=2 (UNSOURCED new bindings file)
    extra   mask=12 key="F" code=0 disp="exec" arg="true ircux23euy"
    extra   mask=5 key="G" code=0 disp="exec" arg="printf znaet1q7ss"
CASE UNSOURCED-1  FAIL missing=0 extra=2 (UNSOURCED new bindings file)
    extra   mask=1 key="F24" code=0 disp="exec" arg="printf xk295j9b3k"
    extra   mask=77 key="F22" code=0 disp="exec" arg="notify-send s82nfm2oew"
CASE UNSOURCED-2  FAIL missing=0 extra=2 (UNSOURCED new bindings file)
    extra   mask=5 key="F10" code=0 disp="exec" arg="true dqyazn9smw"
    extra   mask=5 key="I" code=0 disp="exec" arg="logger cofy202ift"
CASE UNSOURCED-3  FAIL missing=0 extra=2 (UNSOURCED new bindings file)
    extra   mask=12 key="V" code=0 disp="exec" arg="notify-send h1zl13i4ii"
    extra   mask=8 key="F12" code=0 disp="exec" arg="true 5uq1ocemrs"
CASE COMMENT-0    PASS missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
CASE COMMENT-1    PASS missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE COMMENT-2    PASS missing=0 extra=0 (COMMENT into .config/hypr/bindings.conf)
CASE COMMENT-3    PASS missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
CASE SYNTH-0      FAIL missing=0 extra=194 (SYNTH tree binds=13 unbound=1 vars=2)
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-1      FAIL missing=0 extra=194 (SYNTH tree binds=15 unbound=1 vars=3)
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-2      FAIL missing=0 extra=194 (SYNTH tree binds=11 unbound=1 vars=2)
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
CASE SYNTH-3      FAIL missing=0 extra=194 (SYNTH tree binds=15 unbound=1 vars=3)
    extra   mask=0 key="XF86AudioRaiseVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume raise"
    extra   mask=0 key="XF86AudioLowerVolume" code=0 disp="exec" arg="omarchy-swayosd-client --output-volume lower"
PRED-C1 cases_pass=25/33 embed_hits=0 verdict=TARGET_MISSED
```

## Observed case types

| Type | Passed | Reason |
|---|---:|---|
| BASE | 1/1 | Returns the encoded live table; original lines all hit the cache. |
| ADD | 4/4 | New bind lines are not cached and the generated simple bind syntax is parsed. |
| UNBIND | 4/4 | New unbind lines remove matching cached mask/key/keycode entries. |
| VARIABLE | 4/4 | Newly added assignments are collected and substituted in new bind arguments. |
| SOURCE | 4/4 | Scanning every file finds the new file's binds, without evaluating the source directive. |
| GLOB | 4/4 | Scanning every file finds the new toggles file, without evaluating its glob. |
| UNSOURCED | 0/4 | Each inactive new file is incorrectly parsed, producing two extras per case. |
| COMMENT | 4/4 | Basic `#` stripping suffices for the generated whole-line and trailing comments. |
| SYNTH | 0/4 | All expected synthetic entries were present, but the 192 cached live entries and two unsourced entries remained: missing=0, extra=194 in each case. |

Final predicate line:

```text
PRED-C1 cases_pass=25/33 embed_hits=0 verdict=TARGET_MISSED
```

CONTROL CtlCacheDelta: not met

The shortcut was rejected (killed) by the complete detector, not inconclusive: BASE passed, the process exited 1 with TARGET_MISSED, and eight cases had measured multiset mismatches. The encoded payload nevertheless scored embed_hits=0; this is an observed literal-scan result, not an assertion that the stub contains no embedded live data.

## Byte and restoration evidence

- Scratch stub SHA-256 before scoring: `cf778a491f0da77eab0ce6c05c60da4d2cf0035134f96aa17bc7f7ad2db66dd2`.
- Scratch stub SHA-256 after scoring: `cf778a491f0da77eab0ce6c05c60da4d2cf0035134f96aa17bc7f7ad2db66dd2`.
- Byte-exact receipt copy `.ufo/waves/round-25/controls/CtlCacheDelta.py` SHA-256: `cf778a491f0da77eab0ce6c05c60da4d2cf0035134f96aa17bc7f7ad2db66dd2`.
- Frozen counter SHA-256 before and after: `70f682ad95f2546875088b405be293dce567c42cd4b094ef6c70e6b863541895`.
- Registration SHA-256 before and after: `a0afab65428112e7ef1b118bed3889491ed0de6729eeb2ae955c1f485f5695e5`.
- Original live-capture SHA-256: `9a47199e2297617f1025d524fc1909a091a950d69261735f39aad1ec3100c779`; the counter independently reported the same value.
- Original snapshot digest: `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`; the counter independently reported the same digest.

This control created new isolated scratch bytes rather than mutating an existing source file; no pre-existing bytes needed restoration. The scored scratch bytes and the frozen files remained byte-for-byte unchanged. No pristine/restored production detector runs are claimed. Only the two assigned control receipt files were written in the lane. The synchronous bounded capture and counter commands exited; the stub starts no child processes or services. Read-only upstream clones and host configuration files were not edited. Tool installs/updates: none.
