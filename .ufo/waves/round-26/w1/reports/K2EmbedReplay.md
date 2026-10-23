# K2EmbedReplay — encoded snapshot replay control
## Verdict

CONTROL K2EmbedReplay best: cases_pass=23/51 embed_hits=0 verdict=TARGET_MISSED — not met

Both fresh-seed runs missed the target. Run 1 passed BASE and all 20 V3 cases (21/51); run 2 additionally passed two escaped-only ARITH cases (23/51). The other 28 ARITH cases in run 2 failed. Both reported `embed_hits=0` and `exit=1`; neither exited 2, so no rerun was required.

The encoded oracle cache survives the frozen counter’s literal-string embedding scan. This is a coverage finding for semantic embedding, not a contradiction of the registered literal-byte predicate, and it did not defeat the complete C2 counter. No contract change is proposed.

## Shape and construction

- Axes: strongest permitted replay shape, frozen-counter coverage, anti-embedding detection, exact restoration, and host safety.
- Used the explicitly permitted stronger variant: cache the oracle table only when the complete four-root snapshot digest matches; on every changed tree run the unchanged round-25 resolver. No expression evaluator or new bind resolver was built. The only resolver behavior change is the two-line `_replay_snapshot(HOME[0])` early return.
- The cached table came from the pinned harness’s `snapshot()` copy followed by `oracle(snapshot, work, ["binds"])`, not live-session IPC. Snapshot: 79 files, SHA-256 `fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727`; oracle: 192 binds. The cache contains 69291 bytes of compact JSON compressed with zlib level 9 and base64-encoded into 5272 characters.
- Control: `.ufo/waves/round-26/controls/K2EmbedReplay.py`, 22793 bytes, SHA-256 `a4d6d115fb74294dce44824c38b2e9b049e68face6afc30071c001d1d263a30c`. The same bytes were used in both full counter receipts.
- Fallback: `96101be5:tools/mado-binds.py`, 15583 bytes, SHA-256 `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950`. Existing parsing semantics were retained; changed-tree handling does not evaluate `{{…}}`.
- The digest checks file bytes, sorted paths, and the harness’s 1 MiB inclusion bound; it does not inspect case labels, mount metadata, or random temporary names.
- No lane tool, frozen counter, or harness file was edited. Lane outputs are only this report and the assigned control/receipt paths. No tools were installed or updated.

## Commands

All started child processes had `WAYLAND_DISPLAY` and `HYPRLAND_INSTANCE_SIGNATURE` removed. `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were also removed before the read-only source lookup.

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 10 prlimit --as=4000000000 df -h /fast
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 20 prlimit --as=4000000000 -- git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 96101be5:tools/mado-binds.py
```

Disk output before creating scratch copies:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  619G  185G  78% /fast
```

Oracle capture used this exact Python program as the argument to `-c`:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 180 prlimit --as=4000000000:8000000000 -- python3 -I -c "$HARVEST_CODE"
```

```python
import os, sys, json, importlib.util, hashlib
os.environ.pop("WAYLAND_DISPLAY", None)
os.environ.pop("HYPRLAND_INSTANCE_SIGNATURE", None)
p = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/harness/oracle.py"
assert hashlib.sha256(open(p, "rb").read()).hexdigest() == "680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441"
spec = importlib.util.spec_from_file_location("mado_r26_embed_oracle", p)
O = importlib.util.module_from_spec(spec)
spec.loader.exec_module(O)
O.check_build()
scratch = "/fast/scratch/hyaku/mado-r26/K2EmbedReplay"
snap = scratch + "/snapshot"
os.makedirs(snap)
core0 = O.coredumps()
nfiles, digest = O.snapshot(os.path.expanduser("~"), snap)
res, error = O.oracle(snap, scratch + "/oracle", ["binds"])
print(json.dumps({"nfiles": nfiles, "digest": digest, "result": res, "error": error, "coredumps_before": core0, "coredumps_after": O.coredumps()}))
if res is None:
    sys.exit(2)
```

Observed capture output excluding the bind table itself (retained at `/fast/scratch/hyaku/mado-r26/K2EmbedReplay/snapshot-table.json` and encoded in the control):

```text
harvest_exit=0
{"coredumps_after": 1335, "coredumps_before": 1335, "digest": "fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727", "error": "", "nfiles": 79}
oracle_binds=192
```

Full scoring command, executed twice concurrently; each invocation let the counter choose a fresh random seed:

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 900 prlimit --as=4000000000:8000000000 -- python3 -I .ufo/waves/round-26/c2/count.py 05319e0f --tool-file /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2EmbedReplay.py
```

The oracle/counter outer address-space limit was soft 4,000,000,000 bytes and hard 8,000,000,000 bytes, allowing the frozen oracle to apply its own 8 GB limit. No Hyprland process was started except through the pinned harness.

## Reversible mutation probe

Mutant: replace resolution of the unchanged operator tree with a zlib/base64-encoded oracle-table replay while retaining the round-25 resolver as fallback. The isolated specimen was `/fast/scratch/hyaku/mado-r26/K2EmbedReplay/probe.py`; no sibling source was modified.

Expected detector: the full frozen C2 counter should reject this shortcut because it adds no arithmetic support. Separately, the same bounded BASE-plus-embedding detector was run against pristine, mutated, and restored specimen bytes. It executes the tool in `run_tool()`’s sandbox, compares all frozen V3 comparison fields with the captured oracle BASE, and repeats exactly the frozen `arg`/`description`, length-at-least-12 substring scan. A semantic anti-embedding detector would identify the cached oracle table; the registered literal scan is not such a detector.

Exact bounded detector invocation (the code below was passed as the `-c` argument):

```sh
env -u WAYLAND_DISPLAY -u HYPRLAND_INSTANCE_SIGNATURE timeout 90 prlimit --as=4000000000 -- python3 -I -c "$DETECTOR_CODE" /fast/scratch/hyaku/mado-r26/K2EmbedReplay/probe.py /fast/scratch/hyaku/mado-r26/K2EmbedReplay/snapshot /fast/scratch/hyaku/mado-r26/K2EmbedReplay/snapshot-table.json
```

```python
import hashlib, importlib.util, json, sys
path, snapshot_path, table_path = sys.argv[1:]
cp = '/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/c2/count.py'
assert hashlib.sha256(open(cp, 'rb').read()).hexdigest() == 'b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8'
spec = importlib.util.spec_from_file_location('mado_r26_embed_counter', cp)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
base = json.load(open(table_path))['result']['binds']
b = open(path, 'rb').read()
text = b.decode('utf-8', errors='replace')
strings = {e[f] for e in base for f in ('arg', 'description') if isinstance(e.get(f), str) and len(e[f]) >= C.EMBED_MIN}
hits = sorted(s for s in strings if s in text)
got, error = C.O.run_tool(path, snapshot_path)
if not (isinstance(got, list) and all(isinstance(e, dict) for e in got)):
    print('BASE FAIL ' + (error or 'invalid table shape'))
    rc = 1
else:
    missing, extra = C.V3.compare(got, base)[:2]
    print('BASE %s missing=%d extra=%d got_binds=%d oracle_binds=%d' % ('PASS' if not (missing or extra) else 'FAIL', missing, extra, len(got), len(base)))
    rc = int(bool(missing or extra or hits))
print('sha256:%s bytes=%d strings=%d embed_hits=%d' % (hashlib.sha256(b).hexdigest(), len(b), len(strings), len(hits)))
for s in hits[:5]:
    print('EMBED_HIT %r' % s[:60])
print('exit=%d' % rc)
sys.exit(rc)
```

Actual detector outputs:

### PRISTINE

```text
BASE PASS missing=0 extra=0 got_binds=192 oracle_binds=192
sha256:9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950 bytes=15583 strings=248 embed_hits=0
exit=0
```

### MUTATED

```text
BASE PASS missing=0 extra=0 got_binds=192 oracle_binds=192
sha256:a4d6d115fb74294dce44824c38b2e9b049e68face6afc30071c001d1d263a30c bytes=22793 strings=248 embed_hits=0
exit=0
```

### RESTORED

```text
BASE PASS missing=0 extra=0 got_binds=192 oracle_binds=192
sha256:9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950 bytes=15583 strings=248 embed_hits=0
exit=0
```

Narrow detector verdict: **SURVIVED**. All three runs passed BASE and returned `embed_hits=0` over 248 distinct snapshot strings. The pristine baseline passed, so this finding is not based on a failing baseline. It demonstrates the limits of BASE-plus-literal-scan coverage only; the complete counter missed the control twice as shown below.

Restoration evidence: before `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950`; mutant `a4d6d115fb74294dce44824c38b2e9b049e68face6afc30071c001d1d263a30c`; restored `9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950`. Exact byte equality with the saved original was `True`; the restored specimen was then exercised by the same detector. Mutation/restoration used whole-byte specimen replacement with the saved UTF-8 round-25 source, with restoration in `finally`. The lane control remains available for scoring.

A preliminary scan-only run on pristine bytes also returned:

```text
sha256:9efa1136abd2759ecf870e551be967c49f8b50b9a11b39ac568a308e8f172950 bytes=15583 strings=248 embed_hits=0
exit=0
```

## Host safety and retained evidence

The capture and both full counters reported Hyprland coredumps `1335 → 1335`, delta 0. All bounded subprocess invocations returned normally. The pinned oracle’s `finally` terminates and waits for each private compositor process group; its private runtime directory is removed, and each counter removes its own scratch tree. No detached service was started. The standalone oracle working tree was removed after receipt capture; the snapshot, oracle JSON, and byte-restored specimen remain in the assigned isolated scratch directory for reproduction.

Receipts: `.ufo/waves/round-26/controls/K2EmbedReplay.txt` (verbatim stdout including each `exit=` line). Both complete stdout receipts follow.

## Full frozen-counter receipts

### Run 1, attempt 1

Elapsed 34.19 seconds; subprocess return code 1.

```text
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2EmbedReplay.py sha256:a4d6d115fb74294dce44824c38b2e9b049e68face6afc30071c001d1d263a30c
seed=8423c303b4224576
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal binds=192
CASE BASE           PASS oracle_binds=192 missing=0 extra=0 (unperturbed)
CASE A00            FAIL oracle_binds=195 missing=0 extra=1 | extra mask=69 key="U" code=0 disp="resizeactive" arg="{{ (3 / 11.412)/4 }} 0" (ARITH[unclosed+escaped+escaped+desc]@sourced)
CASE A01            FAIL oracle_binds=193 missing=1 extra=3 | missing mask=64 key="F18" code=0 disp="workspace" arg="$arlmnp" | extra mask=65 key="F17" code=0 disp="resizeactive" arg="{{(4.0 + 15) * 2}} 0" | extra mask=64 key="F18" code=0 disp="workspace" arg="{{ (9*2 / 0) + 1 }}" (ARITH[desc+var+ws]@sourced)
CASE A02            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=69 key="F18" code=0 disp="resizeactive" arg="0.03448276 1.625" | extra mask=69 key="F18" code=0 disp="resizeactive" arg="{{1 / 29 * 23 - 5.0}} {{ 13*40+12.809 / 8 }}" (ARITH[escaped+resize]@sourced)
CASE A03            FAIL oracle_binds=193 missing=0 extra=1 | extra mask=12 key="F16" code=0 disp="resizeactive" arg="{{18 + 17 + 18}} 0" (ARITH[desc+unclosed]@sourced)
CASE A04            FAIL oracle_binds=193 missing=1 extra=4 | missing mask=64 key="F15" code=0 disp="resizeactive" arg="-10.07 0" | extra mask=65 key="U" code=0 disp="resizeactive" arg="{{ 9 + 3.8 }} {{ 31+3.8 }}" | extra mask=64 key="F15" code=0 disp="resizeactive" arg="{{ 17.93 - 28 - 9.7*6 }} 0" (ARITH[resize+desc+exec+move]@sourced)
CASE A05            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=12 key="8" code=0 disp="workspace" arg="13" | extra mask=12 key="8" code=0 disp="workspace" arg="{{ 37+18.33 - 24 }}" (ARITH[unclosed+ws]@sourced)
CASE A06            FAIL oracle_binds=192 missing=0 extra=3 | extra mask=65 key="KP_3" code=0 disp="moveactive" arg="{{9+3}} -{{8.9 + 6+8 - 31}}" | extra mask=72 key="KP_4" code=0 disp="resizeactive" arg="{{ 9.9 - 2*24 }} 0" (ARITH[move+desc+move]@sourced)
CASE A07            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=69 key="F14" code=0 disp="workspace" arg="$armplm" | extra mask=69 key="F14" code=0 disp="workspace" arg="{{(7 * 8.989 + 19.0 + 29)/4}}" (ARITH[unclosed+var]@sourced)
CASE A08            FAIL oracle_binds=193 missing=0 extra=3 | extra mask=64 key="O" code=0 disp="resizeactive" arg="{{ (35*14 / 7.7) + 1 }} {{ 6 * 36+31+7 }}" | extra mask=76 key="U" code=0 disp="workspace" arg="{{(33 / 9 - 12.476 * 5) + 1}}" (ARITH[resize+ws+escaped+ws]@sourced)
CASE A09            FAIL oracle_binds=192 missing=0 extra=3 | extra mask=65 key="Y" code=0 disp="moveactive" arg="{{(0.894+{{ {{ 10.36*20 }} - 15.612 * 37*7.388 }} | extra mask=72 key="B" code=0 disp="exec" arg="notify-send r26 {{ 14 * {{ 10.36*20 }} - 0.201 }} (ARITH[move+exec+move]@sourced)
CASE A10            FAIL oracle_binds=194 missing=1 extra=3 | missing mask=72 key="B" code=0 disp="exec" arg="echo {{10.2 * 8.5 * 3.9*121.22}}" | extra mask=64 key="F14" code=0 disp="resizeactive" arg="{{ {{(34 + 39 + {{38 * 3.19 / 20 - 12}})/4}} * 11 | extra mask=12 key="KP_6" code=0 disp="moveactive" arg="{{ ({{(34 + 39 + {{38 * 3.19 / 20 - 12}})/4}} - 3 (ARITH[unclosed+resize+move+escaped]@sourced)
CASE A11            FAIL oracle_binds=195 missing=2 extra=2 | missing mask=64 key="8" code=0 disp="workspace" arg="22.404999" | missing mask=69 key="F15" code=0 disp="workspace" arg="$arnnmm" | extra mask=64 key="8" code=0 disp="workspace" arg="{{6.5+17 + 15.905}}" | extra mask=69 key="F15" code=0 disp="workspace" arg="{{ ({{(16 * 6+1 * 33) * 2}}+5 - 1 * 16) + 1 }}" (ARITH[unclosed+ws+var]@sourced)
CASE A12            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=76 key="KP_6" code=0 disp="exec" arg="notify-send r26 6.8999996" | missing mask=76 key="7" code=0 disp="resizeactive" arg="1.0294118 0" | extra mask=76 key="KP_6" code=0 disp="exec" arg="notify-send r26 {{20 - 13.1+33*17}}" | extra mask=76 key="7" code=0 disp="resizeactive" arg="{{ 35 / 34 / 13 * 10 }} 0" (ARITH[exec+desc]@sourced)
CASE A13            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=76 key="M" code=0 disp="exec" arg="echo {{27.5+12.88 + 20 / 26}}" | missing mask=76 key="N" code=0 disp="resizeactive" arg="-16.2 0" | extra mask=76 key="M" code=0 disp="exec" arg="echo {{{{20 + 7.5}}+12.88 + 20 / 26}}" | extra mask=76 key="N" code=0 disp="resizeactive" arg="{{11.8 - 28 / 6 / {{20 + 7.5}}}} 0" (ARITH[escaped+desc]@sourced)
CASE A14            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=12 key="Y" code=0 disp="exec" arg="notify-send r26 30.86" | extra mask=12 key="Y" code=0 disp="exec" arg="notify-send r26 {{ 19+4 + 11.86 }}" (ARITH[exec+escaped]@sourced)
CASE A15            FAIL oracle_binds=194 missing=1 extra=1 | missing mask=76 key="9" code=0 disp="workspace" arg="1" | extra mask=76 key="9" code=0 disp="workspace" arg="{{1.2 / 1.2 * 40}}" (ARITH[escaped+var]@sourced)
CASE A16            FAIL oracle_binds=193 missing=1 extra=4 | missing mask=72 key="9" code=0 disp="workspace" arg="-20" | extra mask=72 key="9" code=0 disp="workspace" arg="{{12 - 32}}" | extra mask=68 key="KP_2" code=0 disp="resizeactive" arg="{{(14.72*19 + 13 / 22) * 2}} 0" (ARITH[var+desc+ws+desc]@sourced)
CASE A17            FAIL oracle_binds=196 missing=4 extra=4 | missing mask=69 key="KP_2" code=0 disp="resizeactive" arg="1.6111112 0" | missing mask=64 key="KP_2" code=0 disp="workspace" arg="8.25" | extra mask=69 key="KP_2" code=0 disp="resizeactive" arg="{{ 29 / 18 }} 0" | extra mask=64 key="KP_2" code=0 disp="workspace" arg="{{ 33 / 4 }}" (ARITH[desc+ws+move+var]@sourced)
CASE A18            FAIL oracle_binds=196 missing=4 extra=4 | missing mask=12 key="F20" code=0 disp="workspace" arg="0.3181818" | missing mask=12 key="Y" code=0 disp="workspace" arg="17" | extra mask=12 key="F20" code=0 disp="workspace" arg="{{7 / 22 * 22 * 14}}" | extra mask=12 key="Y" code=0 disp="workspace" arg="{{ 4 + 13 }}" (ARITH[var+var+var+var]@sourced)
CASE A19            FAIL oracle_binds=193 missing=1 extra=2 | missing mask=12 key="F20" code=0 disp="exec" arg="notify-send r26 29.168" | extra mask=12 key="F20" code=0 disp="exec" arg="notify-send r26 {{ 29 + 0.168 / 14 }}" | extra mask=76 key="KP_2" code=0 disp="moveactive" arg="{{ {{ 36 - 15.75*0*34 }}*{{ 36 - 15.75*0*34 }}+{{ (ARITH[exec+move]@sourced)
CASE A20            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=68 key="F16" code=0 disp="workspace" arg="$arklop" | missing mask=64 key="F20" code=0 disp="moveactive" arg="-29 --26" | extra mask=68 key="F16" code=0 disp="workspace" arg="{{(26 + 11 - 5) + 1}}" | extra mask=68 key="B" code=0 disp="resizeactive" arg="{{ 26*17 }} 0" (ARITH[var+desc+move]@sourced)
CASE A21            FAIL oracle_binds=193 missing=1 extra=3 | missing mask=68 key="KP_3" code=0 disp="moveactive" arg="106.338 -10" | extra mask=68 key="KP_3" code=0 disp="moveactive" arg="{{ 17.723 * 6 }} -{{ 39 - 29+5.80 }}" | extra mask=69 key="F19" code=0 disp="resizeactive" arg="{{(6*38)/4}} 0" (ARITH[move+desc+resize]@sourced)
CASE A22            FAIL oracle_binds=196 missing=2 extra=2 | missing mask=76 key="F18" code=0 disp="moveactive" arg="38.347 -0.42857143" | missing mask=65 key="KP_8" code=0 disp="workspace" arg="10.5" | extra mask=76 key="F18" code=0 disp="moveactive" arg="{{ 10.347 + 28 - 17.301+12.4 }} -{{9 / 21 / 3 * 7 | extra mask=65 key="KP_8" code=0 disp="workspace" arg="{{ 21 / 2 / 18.886 * 18 }}" (ARITH[move+escaped+unclosed+ws]@sourced)
CASE A23            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=69 key="7" code=0 disp="exec" arg="echo {{ $ariiae+3 }}" | missing mask=65 key="KP_7" code=0 disp="workspace" arg="4" | extra mask=69 key="7" code=0 disp="exec" arg="echo {{ {{ (32*0 + 8) * 2 }}+3 }}" | extra mask=65 key="KP_7" code=0 disp="workspace" arg="{{36 / 9*34}}" (ARITH[escaped+var]@sourced)
CASE A24            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=69 key="KP_6" code=0 disp="exec" arg="notify-send r26 0" | extra mask=64 key="F19" code=0 disp="moveactive" arg="{{37*40}} -{{ (26 / 18 / 4.2) + 1 }}" | extra mask=69 key="KP_6" code=0 disp="exec" arg="notify-send r26 {{ 32 * 0 }}" (ARITH[move+exec+unclosed]@sourced)
CASE A25            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=68 key="F16" code=0 disp="workspace" arg="1.525" | extra mask=68 key="F16" code=0 disp="workspace" arg="{{6.1 / 4 + 15.19 * 6.1}}" | extra mask=12 key="F15" code=0 disp="moveactive" arg="{{ 6.1 / 2 }} -{{ (4.7+16 + 11.12*6.1) + 1 }}" (ARITH[ws+escaped+move]@sourced)
CASE A26            FAIL oracle_binds=196 missing=2 extra=2 | missing mask=65 key="F18" code=0 disp="workspace" arg="37" | missing mask=76 key="F15" code=0 disp="resizeactive" arg="0 0" | extra mask=65 key="F18" code=0 disp="workspace" arg="{{ 37+28 - 0 - 4.072 }}" | extra mask=76 key="F15" code=0 disp="resizeactive" arg="{{0 / 19 - 32 * 9}} 0" (ARITH[ws+unclosed+escaped+desc]@sourced)
CASE A27            FAIL oracle_binds=195 missing=2 extra=2 | missing mask=72 key="O" code=0 disp="moveactive" arg="-25 -138.19499" | missing mask=68 key="I" code=0 disp="exec" arg="notify-send r26 43.054" | extra mask=72 key="O" code=0 disp="moveactive" arg="{{11*6.0 - 36 / 31}} -{{ 3.735 * 37 }}" | extra mask=68 key="I" code=0 disp="exec" arg="notify-send r26 {{14.054 + 29 * 26}}" (ARITH[escaped+move+exec]@sourced)
CASE A28            FAIL oracle_binds=195 missing=2 extra=2 | missing mask=76 key="O" code=0 disp="resizeactive" arg="70 0.8125" | missing mask=68 key="F17" code=0 disp="exec" arg="notify-send r26 -23" | extra mask=76 key="O" code=0 disp="resizeactive" arg="{{40 + 30}} {{ 13 / 16 }}" | extra mask=68 key="F17" code=0 disp="exec" arg="notify-send r26 {{1 - 24}}" (ARITH[escaped+resize+exec]@sourced)
CASE A29            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=69 key="KP_2" code=0 disp="resizeactive" arg="-17.128 17" | missing mask=68 key="F14" code=0 disp="workspace" arg="20.454546" | extra mask=69 key="KP_2" code=0 disp="resizeactive" arg="{{0.992 - 18.12}} {{ 11+{{27 / 11}} + 6 }}" | extra mask=68 key="F14" code=0 disp="workspace" arg="{{{{27 / 11}}+{{27 / 11}} + 18}}" (ARITH[resize+var]@sourced)
CASE VADD-0         PASS oracle_binds=193 missing=0 extra=0 (ADD into .config/hypr/bindings.conf)
CASE VADD-1         PASS oracle_binds=193 missing=0 extra=0 (ADD into .config/hypr/bindings.conf)
CASE VUNBIND-0      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=64 key='SPACE' keycode=0)
CASE VUNBIND-1      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=65 key='E' keycode=0)
CASE VVARIABLE-0    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vjscenal)
CASE VVARIABLE-1    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vqjgatib)
CASE VSOURCE-0      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 10)
CASE VSOURCE-1      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 8)
CASE VGLOB-0        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VGLOB-1        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VUNSOURCED-0   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VUNSOURCED-1   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VCOMMENT-0     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/media.conf)
CASE VCOMMENT-1     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE VSYNTH-0       PASS oracle_binds=11 missing=0 extra=0 (SYNTH tree binds=11 unbound=1 vars=3)
CASE VSYNTH-1       PASS oracle_binds=13 missing=0 extra=0 (SYNTH tree binds=13 unbound=1 vars=2)
CASE VREWRITE-0     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=73 key='' code=18; unbind mask=69 key='SPACE' code=0; add changegroupactive)
CASE VREWRITE-1     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=0 key='XF86KbdLightOnOff' code=0; unbind mask=0 key='XF86AudioLowerVolume' code=0; add exec)
CASE VHARD-0        PASS oracle_binds=23 missing=0 extra=0 (HARD tree lines=31 binds=23 unbinds=1 vars=4)
CASE VHARD-1        PASS oracle_binds=21 missing=0 extra=0 (HARD tree lines=29 binds=21 unbinds=3 vars=4)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=21/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

### Run 2, attempt 1

Elapsed 46.58 seconds; subprocess return code 1.

```text
counter c2-r26 sha256:b92c32da632bc9cfaeae72b6a0be2202e5a25653274cc0b33fc0ae3f37a716a8 rev=05319e0fed2ce25cf0a883380af2763a85fd4936 oracle.py sha256:680798ed9fa0c9ebd91ee58c57b1460642e88c2fe8a4a7fd029b0842ef62e441 count-v3.py sha256:8532d3e96cc201ce2506a07d5f4b943e25b645e5ca1b461d9a35d08d4ff78375
tool=override:/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/controls/K2EmbedReplay.py sha256:a4d6d115fb74294dce44824c38b2e9b049e68face6afc30071c001d1d263a30c
seed=13bd49d71bc3f01c
snapshot files=79 digest sha256:fe1b2d8ba8e61ec3756fac0820c88ddda861db7f833f1c47e371934efa983727
ORACLE_CHECK base_twice equal binds=192
CASE BASE           PASS oracle_binds=192 missing=0 extra=0 (unperturbed)
CASE A00            FAIL oracle_binds=194 missing=1 extra=2 | missing mask=64 key="I" code=0 disp="exec" arg="notify-send r26 0.10471204" | extra mask=64 key="I" code=0 disp="exec" arg="notify-send r26 {{2 / 19.1*5 - 11.9}}" | extra mask=76 key="M" code=0 disp="resizeactive" arg="{{ (2+3.593) * 2 }} 0" (ARITH[unclosed+exec+desc]@sourced)
CASE A01            FAIL oracle_binds=195 missing=2 extra=3 | missing mask=65 key="F18" code=0 disp="moveactive" arg="28.58 -21" | missing mask=68 key="N" code=0 disp="resizeactive" arg="-15 0" | extra mask=65 key="F18" code=0 disp="moveactive" arg="{{ 9.58 + 19*8 }} -{{ 27 - 6*1 }}" | extra mask=64 key="8" code=0 disp="moveactive" arg="{{(9.49 * 6) * 2}} -{{ 8 - 5.826 }}" (ARITH[unclosed+move+move+desc]@sourced)
CASE A02            PASS oracle_binds=194 missing=0 extra=0 (ARITH[escaped+escaped]@sourced)
CASE A03            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=65 key="I" code=0 disp="moveactive" arg="-20.619999 -24" | missing mask=72 key="F13" code=0 disp="workspace" arg="$arpoln" | extra mask=65 key="I" code=0 disp="moveactive" arg="{{15.38 - 36 + 24+5.70}} -{{7 + 17 + 3.042 / 3.26 | extra mask=72 key="F13" code=0 disp="workspace" arg="{{ {{(24 + 37 + 7) * 2}} * {{(24 + 37 + 7) * 2}}+ (ARITH[move+var+desc+resize]@sourced)
CASE A04            FAIL oracle_binds=195 missing=3 extra=4 | missing mask=12 key="7" code=0 disp="workspace" arg="3.125" | missing mask=76 key="N" code=0 disp="workspace" arg="329.8" | extra mask=76 key="F17" code=0 disp="moveactive" arg="{{(12.1 - 12.38 - 7.690)/4}} -{{7.3+20 * 5 / 16.8 | extra mask=12 key="7" code=0 disp="workspace" arg="{{25 / 8 - 4.1}}" (ARITH[move+var+var+ws]@sourced)
CASE A05            FAIL oracle_binds=194 missing=1 extra=3 | missing mask=65 key="F13" code=0 disp="resizeactive" arg="-0.21399975 0" | extra mask=76 key="F14" code=0 disp="moveactive" arg="{{ (19 + 7+14.97)/4 }} -{{9.5 / 7}}" | extra mask=65 key="F14" code=0 disp="moveactive" arg="{{ (12 + 0) * 2 }} -{{(7+1.60*21 / 16.62) + 1}}" (ARITH[move+move+escaped+desc]@sourced)
CASE A06            FAIL oracle_binds=195 missing=3 extra=4 | missing mask=64 key="F17" code=0 disp="workspace" arg="0.30099964" | missing mask=12 key="F19" code=0 disp="workspace" arg="$arlnkl" | extra mask=72 key="M" code=0 disp="moveactive" arg="{{(38 * 36) + 1}} -{{0.118 / 15.621}}" | extra mask=64 key="F17" code=0 disp="workspace" arg="{{10.301 - 10 / 12.45}}" (ARITH[move+var+var+var]@sourced)
CASE A07            FAIL oracle_binds=193 missing=0 extra=1 | extra mask=64 key="F18" code=0 disp="workspace" arg="{{(29*7.04) * 2}}" (ARITH[unclosed+ws]@sourced)
CASE A08            FAIL oracle_binds=195 missing=2 extra=3 | missing mask=64 key="8" code=0 disp="resizeactive" arg="0 0" | missing mask=72 key="KP_8" code=0 disp="moveactive" arg="-25 -14.44" | extra mask=64 key="8" code=0 disp="resizeactive" arg="{{0 * 31+5}} 0" | extra mask=72 key="KP_8" code=0 disp="moveactive" arg="{{11*{{38+34 + 4 - 7}} - 36 + {{38+34 + 4 - 7}}}} (ARITH[desc+move+unclosed+move]@sourced)
CASE A09            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=69 key="Y" code=0 disp="resizeactive" arg="43 0" | missing mask=68 key="F19" code=0 disp="exec" arg="echo {{ 0 * $arjcgd*$arjcgd }}" | extra mask=69 key="Y" code=0 disp="resizeactive" arg="{{28*12.5 + 15 * 25}} 0" | extra mask=68 key="F19" code=0 disp="exec" arg="echo {{ 0 * {{ {{ 1+14 }} / {{ 1+14 }}*{{ 1+14 }} (ARITH[desc+escaped+resize]@sourced)
CASE A10            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=65 key="F15" code=0 disp="workspace" arg="$arokpl" | missing mask=68 key="M" code=0 disp="workspace" arg="-2.0900002" | extra mask=65 key="F15" code=0 disp="workspace" arg="{{(5.38*13 / 37) + 1}}" | extra mask=68 key="M" code=0 disp="workspace" arg="{{ 11 - 13.09 / 12.6 }}" (ARITH[var+ws+ws]@sourced)
CASE A11            FAIL oracle_binds=194 missing=2 extra=4 | missing mask=69 key="8" code=0 disp="workspace" arg="676" | missing mask=12 key="F18" code=0 disp="workspace" arg="3.6" | extra mask=69 key="8" code=0 disp="workspace" arg="{{26+37 * 26*33}}" | extra mask=12 key="F18" code=0 disp="workspace" arg="{{ 18 / 5*2 * 40 }}" (ARITH[ws+var+move+move]@sourced)
CASE A12            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=68 key="KP_3" code=0 disp="workspace" arg="15" | missing mask=69 key="F17" code=0 disp="workspace" arg="0.31428573" | extra mask=68 key="U" code=0 disp="exec" arg="notify-send r26 {{29+12}}" | extra mask=68 key="KP_3" code=0 disp="workspace" arg="{{ 25 - 10 / 37 + 22 }}" (ARITH[exec+ws+ws]@sourced)
CASE A13            FAIL oracle_binds=192 missing=0 extra=4 | extra mask=69 key="9" code=0 disp="resizeactive" arg="{{ (19 + 5)/4 }} {{ (20 * 33)/4 }}" | extra mask=12 key="7" code=0 disp="exec" arg="notify-send r26 {{1.708+4.285*10}}" (ARITH[resize+exec+move+exec]@sourced)
CASE A14            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=64 key="7" code=0 disp="workspace" arg="26.8" | missing mask=64 key="F19" code=0 disp="workspace" arg="-18" | extra mask=64 key="7" code=0 disp="workspace" arg="{{9 + 17.80+14}}" | extra mask=64 key="F19" code=0 disp="workspace" arg="{{ 9 - 27 }}" (ARITH[var+ws]@sourced)
CASE A15            FAIL oracle_binds=192 missing=0 extra=2 | extra mask=76 key="O" code=0 disp="resizeactive" arg="{{{{(3 + 4 * 17+9.672)/4}} - 0 / {{(3 + 4 * 17+9. | extra mask=72 key="KP_8" code=0 disp="resizeactive" arg="{{ (11.93 / 4*0.10) * 2 }} {{ 34*4 }}" (ARITH[resize+resize]@sourced)
CASE A16            FAIL oracle_binds=194 missing=1 extra=3 | missing mask=12 key="8" code=0 disp="workspace" arg="270" | extra mask=12 key="KP_4" code=0 disp="moveactive" arg="{{ (9 - 32 - 5) + 1 }} -{{ 40 + 1.4 + 17 }}" | extra mask=68 key="F19" code=0 disp="resizeactive" arg="{{ (9 * 9) * 2 }} 0" (ARITH[escaped+move+desc+var]@sourced)
CASE A17            FAIL oracle_binds=195 missing=2 extra=2 | missing mask=65 key="M" code=0 disp="workspace" arg="$arokmn" | missing mask=72 key="KP_4" code=0 disp="workspace" arg="13" | extra mask=65 key="M" code=0 disp="workspace" arg="{{ (5.3+4+10.755 * 20)/4 }}" | extra mask=72 key="KP_4" code=0 disp="workspace" arg="{{ 9 + 4 / 5.3*30 }}" (ARITH[var+ws+unclosed]@sourced)
CASE A18            FAIL oracle_binds=196 missing=2 extra=2 | missing mask=76 key="I" code=0 disp="resizeactive" arg="13.65 0.25" | missing mask=65 key="M" code=0 disp="workspace" arg="$arlnmn" | extra mask=76 key="I" code=0 disp="resizeactive" arg="{{ 2.73*17 * 5.0 / 37 }} {{ 5.0 / 20 * 36+38 }}" | extra mask=65 key="M" code=0 disp="workspace" arg="{{(3.8+20+2)/4}}" (ARITH[resize+escaped+unclosed+var]@sourced)
CASE A19            FAIL oracle_binds=194 missing=2 extra=2 | missing mask=72 key="F13" code=0 disp="workspace" arg="27" | missing mask=12 key="F14" code=0 disp="workspace" arg="$arnmok" | extra mask=72 key="F13" code=0 disp="workspace" arg="{{1*{{ 2*18.6*6.44 - 28 }}*{{ 2*18.6*6.44 - 28 }} | extra mask=12 key="F14" code=0 disp="workspace" arg="{{7*26}}" (ARITH[ws+var]@sourced)
CASE A20            FAIL oracle_binds=195 missing=2 extra=3 | missing mask=12 key="B" code=0 disp="workspace" arg="0.5294118" | missing mask=76 key="B" code=0 disp="workspace" arg="34.96" | extra mask=12 key="B" code=0 disp="workspace" arg="{{9 / 17 + 36 - 9}}" | extra mask=76 key="B" code=0 disp="workspace" arg="{{1.9*5.627 * 18.4 / 39}}" (ARITH[unclosed+ws+ws+resize]@sourced)
CASE A21            FAIL oracle_binds=194 missing=0 extra=2 | extra mask=69 key="I" code=0 disp="workspace" arg="{{(34*17 / 15*2) + 1}}" | extra mask=65 key="7" code=0 disp="exec" arg="notify-send r26 {{{{9 + 2}}+34}}" (ARITH[ws+escaped+escaped+exec]@sourced)
CASE A22            FAIL oracle_binds=193 missing=1 extra=2 | missing mask=65 key="8" code=0 disp="workspace" arg="836" | extra mask=69 key="F18" code=0 disp="moveactive" arg="{{ (6 / 15.60 - 6) * 2 }} -{{6 + 37 * {{ 16.807+1 | extra mask=65 key="8" code=0 disp="workspace" arg="{{38 * 22 + 14.6}}" (ARITH[move+var]@sourced)
CASE A23            FAIL oracle_binds=193 missing=1 extra=2 | missing mask=64 key="F13" code=0 disp="resizeactive" arg="3.2472727 48" | extra mask=65 key="B" code=0 disp="moveactive" arg="{{(14.5*{{ 1.88 / 11 - 10 / 5.954 }} / {{ 1.88 /  | extra mask=64 key="F13" code=0 disp="resizeactive" arg="{{ 19 * {{ 1.88 / 11 - 10 / 5.954 }} }} {{ 21 + 2 (ARITH[move+resize]@sourced)
CASE A24            FAIL oracle_binds=194 missing=2 extra=3 | missing mask=72 key="Y" code=0 disp="moveactive" arg="223.23601 -464.69998" | missing mask=12 key="F17" code=0 disp="workspace" arg="40.3" | extra mask=72 key="Y" code=0 disp="moveactive" arg="{{ 13.78 * 16.2*18.49 + 1.2 }} -{{30*{{ 8+5.4 + 1 | extra mask=12 key="F17" code=0 disp="workspace" arg="{{ 38 + 2.3 - 39 / 5.4 }}" (ARITH[move+ws+exec]@sourced)
CASE A25            PASS oracle_binds=194 missing=0 extra=0 (ARITH[escaped+escaped]@sourced)
CASE A26            FAIL oracle_binds=195 missing=2 extra=2 | missing mask=12 key="M" code=0 disp="workspace" arg="$armokm" | missing mask=69 key="F20" code=0 disp="workspace" arg="$arklll" | extra mask=12 key="M" code=0 disp="workspace" arg="{{ (26 * 24*9*9) + 1 }}" | extra mask=69 key="F20" code=0 disp="workspace" arg="{{ (10 / 9.686)/4 }}" (ARITH[var+unclosed+var]@sourced)
CASE A27            FAIL oracle_binds=193 missing=1 extra=3 | missing mask=69 key="7" code=0 disp="exec" arg="echo {{ 11+40+2 }}" | extra mask=69 key="7" code=0 disp="exec" arg="echo {{ {{40 - 29 - 15.507 - 21}}+40+2 }}" | extra mask=12 key="Y" code=0 disp="resizeactive" arg="{{ 12+{{40 - 29 - 15.507 - 21}} }} {{(9 + 10.941) (ARITH[escaped+resize+desc]@sourced)
CASE A28            FAIL oracle_binds=193 missing=0 extra=2 | extra mask=72 key="N" code=0 disp="resizeactive" arg="{{7.9+3}} 0" | extra mask=64 key="F16" code=0 disp="exec" arg="notify-send r26 {{(2*14.128 / 7) + 1}}" (ARITH[escaped+desc+exec]@sourced)
CASE A29            FAIL oracle_binds=193 missing=1 extra=2 | missing mask=72 key="KP_7" code=0 disp="workspace" arg="$armoln" | extra mask=72 key="KP_7" code=0 disp="workspace" arg="{{ (18 * 3.93) + 1 }}" | extra mask=76 key="F19" code=0 disp="moveactive" arg="{{(1.64 - 4.1 + 4.1 - 19) * 2}} -{{ 27*{{9.18 - 3 (ARITH[var+move]@sourced)
CASE VADD-0         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/media.conf)
CASE VADD-1         PASS oracle_binds=193 missing=0 extra=0 (ADD into .local/share/omarchy/default/hypr/bindings/utilities.conf)
CASE VUNBIND-0      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=68 key='X' keycode=0)
CASE VUNBIND-1      PASS oracle_binds=191 missing=0 extra=0 (UNBIND mask=76 key='W' keycode=0)
CASE VVARIABLE-0    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vstpqpys)
CASE VVARIABLE-1    PASS oracle_binds=193 missing=0 extra=0 (VARIABLE $vznyrssb)
CASE VSOURCE-0      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 23)
CASE VSOURCE-1      PASS oracle_binds=194 missing=0 extra=0 (SOURCE new file at root line 6)
CASE VGLOB-0        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VGLOB-1        PASS oracle_binds=193 missing=0 extra=0 (GLOB new toggles file)
CASE VUNSOURCED-0   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VUNSOURCED-1   PASS oracle_binds=192 missing=0 extra=0 (UNSOURCED new bindings file)
CASE VCOMMENT-0     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/clipboard.conf)
CASE VCOMMENT-1     PASS oracle_binds=193 missing=0 extra=0 (COMMENT into .local/share/omarchy/default/hypr/bindings/tiling-v2.conf)
CASE VSYNTH-0       PASS oracle_binds=18 missing=0 extra=0 (SYNTH tree binds=18 unbound=1 vars=2)
CASE VSYNTH-1       PASS oracle_binds=12 missing=0 extra=0 (SYNTH tree binds=12 unbound=1 vars=2)
CASE VREWRITE-0     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=64 key='' code=17; unbind mask=68 key='X' code=0; add bringactivetotop)
CASE VREWRITE-1     PASS oracle_binds=192 missing=0 extra=0 (REWRITE argswap mask=8 key='PRINT' code=0; unbind mask=72 key='mouse_down' code=0; add exec)
CASE VHARD-0        PASS oracle_binds=16 missing=0 extra=0 (HARD tree lines=27 binds=16 unbinds=3 vars=4)
CASE VHARD-1        PASS oracle_binds=21 missing=0 extra=0 (HARD tree lines=32 binds=21 unbinds=1 vars=4)
HOST_SAFETY hyprland_coredumps_before=1335 after=1335 delta=0
PRED-C2-r26 cases_pass=23/51 embed_hits=0 verdict=TARGET_MISSED
exit=1
```

