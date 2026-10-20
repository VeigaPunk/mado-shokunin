# MutTripwireTip — 11 killed, 9 survived; all 20 scratch sources restored exactly

## Scope, axes, and detector

Tested only the assigned immutable tripwire, not a moving working-tree version or any round-19 draft. The nine survivors remain **coverage findings**, even though the supplementary regression witnesses below distinguish every one of them. No integration, contract change, or round verdict is asserted.

Axes: **class/rule detection fidelity**, **clean-case specificity**, **fail-closed frozen-pin validation**, and **byte-identical restoration/repeatability**.

Source acquisition command actually executed:

```text
git -C /home/vgpnk/Projects/shokunin/mado-shokunin show 17661e0fa83f978fb659f5bb8fef47f0969f6945:tools/mado-tripwire.py
```

- Source size: **55604 bytes**.
- Pristine SHA-256, denoted **P** throughout: `c1ae45a7573e536bdb8ad410f36782aaad9832ecae6a95b2f5c7f823d13c70cd`.
- Runtime: `/usr/bin/python`; `3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]`.
- Isolated root: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv`. Each mutant had its own `Mxx/mado-tripwire.py`; the lane tool was never edited.
- Twenty independent **single-line / single-expression** mutants: five each in `classify_pacman`, `strip_prefix`, eval/subprocess parsing/accounting, and the frozen validator. M13/M14 used structural expression edits; all others used hash-anchored line edits.

For every mutant, the same six suite commands ran against pristine, mutated, and exactly restored bytes:

```text
/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/Mxx/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/core
/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/Mxx/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/compound
/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/Mxx/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening
/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/Mxx/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/w2-regressions
/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/Mxx/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen
/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/Mxx/mado-tripwire.py --selftest /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/r18-failsafe
```

`Mxx` is a placeholder in this display only; every concrete argv is retained in the raw evidence. Scheduling used at most six concurrent suite processes, a 90-second outer bound per suite, and a 30-second bound per supplemental witness. Nothing from a transcript was executed as a host command: only the Python tripwire and its named selftests/scans/frozen replays ran.

Actual work: **372 selftest invocations** = six initial control runs + 120 per-copy pristine runs + 120 mutant runs + six identical-byte M20 replay runs + 120 restored runs. This exercised **7,440 suite case invocations**, including repetitions; it is not 7,440 distinct tests. There were also **27 supplemental witness captures** (nine × pristine/mutant/restored), plus one direct frozen replay to expose the existing duplicate-key fixture’s masking error. No timeout or stderr output occurred.

Raw evidence, including every argv, exit, complete stdout/stderr, mutation specification, fixture body, and before/after fingerprint:

- `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:1-404`
- **474263 bytes**, SHA-256 `120fe26f6a6bd7706ecad7005662147d364627ffc33e9d45e1b24e8f45685100`
- Lines 1–4 contain metadata, the exact mutation manifest, suite fingerprints, and complete proposed fixture bytes. The report also retains substantive output excerpts below so the findings do not depend solely on `/tmp` retention.

## Pristine and restored controls

All **120/120 existing case assertions passed on each pristine copy and on each restored copy**. Every suite process in both phases exited 0. Initial control output was:

```text
core: SELFTEST_SUMMARY: 9/9 passed failed=[]
compound: SELFTEST_SUMMARY: 16/16 passed failed=[]
hardening: SELFTEST_SUMMARY: 33/33 passed failed=[]
w2-regressions: SELFTEST_SUMMARY: 30/30 passed failed=[]
frozen: SELFTEST_SUMMARY: 31/31 passed failed=[]
r18-failsafe: SELFTEST_SUMMARY: 1/1 passed failed=[]
```

The following table maps each copy’s six pristine and six restored captures. Every recorded selftest script digest in these phases is P.

| Mutant | Pristine evidence | Restored evidence | Before → after SHA-256 |
|---|---|---|---|
| M01 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:11-16` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:257-262` | P → P |
| M02 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:17-22` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:263-268` | P → P |
| M03 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:23-28` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:269-274` | P → P |
| M04 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:29-34` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:275-280` | P → P |
| M05 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:35-40` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:281-286` | P → P |
| M06 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:41-46` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:287-292` | P → P |
| M07 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:47-52` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:293-298` | P → P |
| M08 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:53-58` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:299-304` | P → P |
| M09 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:59-64` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:305-310` | P → P |
| M10 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:65-70` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:311-316` | P → P |
| M11 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:71-76` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:317-322` | P → P |
| M12 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:77-82` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:323-328` | P → P |
| M13 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:83-88` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:329-334` | P → P |
| M14 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:89-94` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:335-340` | P → P |
| M15 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:95-100` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:341-346` | P → P |
| M16 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:101-106` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:347-352` | P → P |
| M17 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:107-112` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:353-358` | P → P |
| M18 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:113-118` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:359-364` | P → P |
| M19 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:119-124` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:365-370` | P → P |
| M20 | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:125-130` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:371-376` | P → P |

Restoration used the exact original Git blob in `finally`, including when a suite returned nonzero. All 20 restored files hash to P; all 120 restored suite runs pass. The nine supplemental witnesses’ restored exit, stdout, and stderr are **byte-for-byte equal** to their pristine captures. M20 was replayed once, at the same mutant digest, solely to build the ninth survivor witness; it too was restored before the final restored-suite phase.

### Fixture identity

The six suite trees’ regular-file digests and literal symlink targets were fingerprinted before and after; **all six fingerprints are unchanged**. The tree digest hashes a sorted JSON list of `(relative path, file/symlink, file digest/link target)`; directory symlinks are not followed by the fingerprint routine. Evidence: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:3`.

| Suite | `expected.json` SHA-256 | Tree SHA-256 |
|---|---|---|
| core | `e8aff6efb9ce06eefac457d8dc8afa79405f2167c426f2c23900bc314b06b920` | `ee21cd3584310f87058cc79634f2aca375b7faa46b6e2e075656cb0883f73fb1` |
| compound | `eef778eac31181f9c76519ff7a0b01c368e2f5255c12791e13c0f0fc7ce065e2` | `f0935e3de50e9fd871a40c28c6e4ed47a77a863378e1d97f9b51687232dcd835` |
| hardening | `913a5e91efe7412aeaf8954b4546fdaa98d9575f384ac90fc292aaf15aae1a01` | `e6a4b3375ee9e437842b1d0f40ca30fbaaf4cec1158de1df8e9b1056508bda72` |
| w2-regressions | `8a98c12b706203b710e9075117e0883987a453da4fa59ba156894de86b9ebd2e` | `4c02233feefbc90b1749a5b6967d0ed9cd63dfa5162e1beaf9546c93e1e052b3` |
| frozen | `61741eae60cc8eb5f657c6feb9d447d8363715ecad618a2524e98aeb08fdba66` | `1f17cb3ebae51a100bd3af3b346b488675025eab958232aab69802829868276a` |
| r18-failsafe | `2bdacc98d259ced11017a6e49280423c694f2c314b236d92201a36a9ab729fee` | `b75c69886e9b61648a3cf68951953dea97ad2d49198785a1f9a83567f5fe162b` |

## Original six-suite mutant results

Cell format: **passed/total; process exit**. `K`/`S` refers only to the original six-suite detector. Result: **11 killed / 9 survived / 0 inconclusive**; all baselines and restorations passed. This deliberately selected 20-mutant sample is not an estimate of overall correctness or a general mutation-coverage score.

| Mutant | core | compound | hardening | w2-regressions | frozen | r18-failsafe | Verdict |
|---|---|---|---|---|---|---|---|
| M01 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 30/30; 0 | 31/31; 0 | 0/1; 1 | **killed** |
| M02 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 30/30; 0 | 31/31; 0 | 1/1; 0 | **survived** |
| M03 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 29/30; 1 | 31/31; 0 | 1/1; 0 | **killed** |
| M04 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 29/30; 1 | 31/31; 0 | 1/1; 0 | **killed** |
| M05 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 30/30; 0 | 31/31; 0 | 1/1; 0 | **survived** |
| M06 | 9/9; 0 | 13/16; 1 | 33/33; 0 | 30/30; 0 | 31/31; 0 | 1/1; 0 | **killed** |
| M07 | 9/9; 0 | 16/16; 0 | 32/33; 1 | 30/30; 0 | 31/31; 0 | 1/1; 0 | **killed** |
| M08 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 30/30; 0 | 31/31; 0 | 1/1; 0 | **survived** |
| M09 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 30/30; 0 | 31/31; 0 | 1/1; 0 | **survived** |
| M10 | 9/9; 0 | 14/16; 1 | 33/33; 0 | 30/30; 0 | 31/31; 0 | 1/1; 0 | **killed** |
| M11 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 29/30; 1 | 31/31; 0 | 1/1; 0 | **killed** |
| M12 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 29/30; 1 | 31/31; 0 | 1/1; 0 | **killed** |
| M13 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 30/30; 0 | 31/31; 0 | 1/1; 0 | **survived** |
| M14 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 29/30; 1 | 31/31; 0 | 1/1; 0 | **killed** |
| M15 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 30/30; 0 | 31/31; 0 | 1/1; 0 | **survived** |
| M16 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 30/30; 0 | 31/31; 0 | 1/1; 0 | **survived** |
| M17 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 30/30; 0 | 30/31; 1 | 1/1; 0 | **killed** |
| M18 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 30/30; 0 | 31/31; 0 | 1/1; 0 | **survived** |
| M19 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 30/30; 0 | 30/31; 1 | 1/1; 0 | **killed** |
| M20 | 9/9; 0 | 16/16; 0 | 33/33; 0 | 30/30; 0 | 31/31; 0 | 1/1; 0 | **survived** |

### Mutation definitions and hashes

Each row’s before and final after digest is P. The middle digest is the actual mutant bytes used in every corresponding suite invocation. The source line numbers are for `17661e0fa83f978fb659f5bb8fef47f0969f6945:tools/mado-tripwire.py`.

| ID | Point | Plausible defect | Mutant SHA-256 |
|---|---|---|---|
| M01 | `classify_pacman` L417 | Unreadable/absent pacman operation fails open to package_query | `53cd0793ffb351568c23ff9f6ad4c5643ed5447238811c0de82118d0ed853e95` |
| M02 | `classify_pacman` L427 | Refresh flag y no longer outranks read-only sync flags | `fd809bb2aac313627cafe134d607888321ab9be72ec54ab1f31686617b7be718` |
| M03 | `classify_pacman` L397 | Reject unique abbreviated pacman long operations | `c5e7ea945ee1787d16bb52fd5273d92df0363e7d9fa190b0ffee5fc281b0612f` |
| M04 | `classify_pacman` L420 | Files database refresh Fy is classified as package_query | `b463aa60e74955597588c59508bd0d1b8fe26135b86467a634d2bb24bea60ccd` |
| M05 | `classify_pacman` L422 | Database operation D is classified as package_query | `3fbb6fcd63cbdb5aec617c3420d408caf293b4bdefc98d2947e4daac9282a4c7` |
| M06 | `strip_prefix` L278 | Do not strip leading shell assignments | `6c2660e4b4daf20b0670045a3f68bc7e5ba8046a9661bf297280c504bc2c907a` |
| M07 | `strip_prefix` L287 | command -v lookup treated as executing looked-up binary | `d9fe32b4512f9a286f6ccfbb45bb8f4d1cf20c153cb1e8ffc7029ecb0f6ed2d1` |
| M08 | `strip_prefix` L310 | Ignore env --split-string= attached payload | `127f8dee42ab79c912ee153f1551fe42e26dca1fb50d9d6d22ad8ee199c215b8` |
| M09 | `strip_prefix` L331 | ionice -n priority argument is mistaken for command | `c60a983623a2aaefd9589b61c55d4b4d6626a2f7d679638c1a9c83422b5a28cb` |
| M10 | `strip_prefix` L343 | timeout removes command tail instead of duration | `f25db54f70ede09a8aa6c8d71ca1d9a6d996b7ca145ad36b529e91641a02be54` |
| M11 | `eval/subprocess` L636 | Ignore import subprocess as alias | `b9a853dc5d8dec93ef785a917c44a39c48efd778d07e1abe5a0cfe5505ae830f` |
| M12 | `eval/subprocess` L642 | Resolve from-import under original name, not alias | `8f39b4d6fbdca7b13655aa5cc4c34970eeab59a41ccb3bff425a365ff185ce75` |
| M13 | `eval/subprocess` L600 | Reject literal tuple subprocess argv | `f970a592d0439f340a1d2008bb0126f041fa087fc7217a1f1ab4e0276e16fe9f` |
| M14 | `eval/subprocess` L683 | Nonliteral shell= no longer treated as shell | `9f77b8f9c23cab46d2636dd6a45b58598347c4560e55f5d70655e5f524dd8684` |
| M15 | `eval/subprocess` L693 | Erase unparsed_spawns accounting for nonliteral spawn | `607f47fbb672f773b8c761d082386050fdbd0ccf02a1c7ff769cc27a3d56ed4f` |
| M16 | `--frozen validator` L953 | Accept JSON boolean expected_exit as integer | `4e2bd8e2d6a8bd5de2c550ed09223627b2e22c16faca7c44f642af309e148c7b` |
| M17 | `--frozen validator` L930 | Ignore unknown expected.json keys | `5c18e3c636d286e4cb70d2680faccd7ab56aea1fe7b971400ff4d7052dca8985` |
| M18 | `--frozen validator` L995 | Allow known-miss/expected-finding overlap | `9191101008025329fa6ade0aa3c8b36b1bc9db983fd7949b1a0e34f237f2fb3a` |
| M19 | `--frozen validator` L1102 | Allow symlinked frozen directory | `a293534f1652b3dc0eea8b1e9a511b6a2e440ed115f17a2d24d848e039506719` |
| M20 | `--frozen validator` L911 | Accept duplicate JSON keys using last-wins | `3a5d7854afa4eb33b0925610e8394e0d0a807fc9b9ee7621a12d1ec1198bba4c` |

Exact changes, one point per isolated file (never accumulated):

**M01, L417**

```diff
-        return ("host_mutation", argv0)
+        return ("package_query", argv0)
```

**M02, L427**

```diff
-        if flags & set("yuwc"):
+        if flags & set("uwc"):
```

**M03, L397**

```diff
-            hits = [k for k in long_ops if k.startswith(name)] if len(name) > 3 else []
+            hits = [k for k in long_ops if k == name] if len(name) > 3 else []
```

**M04, L420**

```diff
-    if letter == "F" and "y" in flags:
+    if letter == "F" and "u" in flags:
```

**M05, L422**

```diff
-    if letter in ("Q", "F", "T", "V"):
+    if letter in ("Q", "F", "T", "V", "D"):
```

**M06, L278**

```diff
-        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", head) or head in KEYWORDS:
+        if head in KEYWORDS:
```

**M07, L287**

```diff
-            return []  # lookup only, nothing is executed
+            return seg[2:]  # lookup mistaken for execution
```

**M08, L310**

```diff
-                if opt.startswith("--split-string="):
+                if False and opt.startswith("--split-string="):
```

**M09, L331**

```diff
-                if opt in ("-c", "-n", "-p") and seg:
+                if opt in ("-c", "-p") and seg:
```

**M10, L343**

```diff
-                seg.pop(0)  # duration
+                seg.pop(-1)  # mistakenly consume command tail, not duration
```

**M11, L636**

```diff
-                if a.name in ("subprocess", "os", "asyncio") and a.asname:
+                if a.name in ("os", "asyncio") and a.asname:
```

**M12, L642**

```diff
-                aliases[a.asname or a.name] = "%s.%s" % (node.module, a.name)
+                aliases[a.name] = "%s.%s" % (node.module, a.name)
```

**M13, L600**

```diff
-    if isinstance(node, (ast.List, ast.Tuple)) and node.elts and all(
+    if isinstance(node, ast.List) and node.elts and all(
```

**M14, L683**

```diff
-        shell_kw = any(k.arg == "shell" and not (isinstance(k.value, ast.Constant) and not k.value.value)
+        shell_kw = any(k.arg == "shell" and (isinstance(k.value, ast.Constant) and bool(k.value.value))
```

**M15, L693**

```diff
-    return hits, 0, unparsed
+    return hits, 0, 0
```

**M16, L953**

```diff
-    if type(want_exit) is not int or want_exit not in (0, 1):
+    if not isinstance(want_exit, int) or want_exit not in (0, 1):
```

**M17, L930**

```diff
-    if unknown:
+    if False and unknown:
```

**M18, L995**

```diff
-    if overlap:
+    if False and overlap:
```

**M19, L1102**

```diff
-    if os.path.islink(directory.rstrip("/") or directory):
+    if False and os.path.islink(directory.rstrip("/") or directory):
```

**M20, L911**

```diff
-        if key in seen:
+        if False and key in seen:
```

### Killed-mutant detector evidence

Each block gives the expected detector and the first actual failing case output. The full output and all additional failing cases are in the cited mutant capture range. A suite failure counts as a kill only because its pristine and restored controls passed.

**M01** — expected detector: r18-failsafe: unparsed-pacman-operator. Evidence: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:131-136`.

```text
CASE unparsed-pacman-operator FAIL want=(1, [('host_mutation', 'pacman', 1, '')]) got=(0, [('package_query', 'pacman', 1, '')])
SELFTEST_SUMMARY: 0/1 passed failed=['unparsed-pacman-operator']
```

**M03** — expected detector: w2-regressions: pacman-abbreviated-long-op. Evidence: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:143-148`.

```text
CASE pacman-abbreviated-long-op FAIL want=(1, [('host_mutation', 'pacman:--syn', 1, '')]) got=(1, [('host_mutation', 'pacman', 1, '')])
SELFTEST_SUMMARY: 29/30 passed failed=['pacman-abbreviated-long-op']
```

**M04** — expected detector: w2-regressions: pacman-Fy-refresh. Evidence: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:149-154`.

```text
CASE pacman-Fy-refresh FAIL want=(1, [('host_mutation', 'pacman:-Fy', 1, '')]) got=(1, [('package_query', 'pacman:-Fy', 1, '')])
SELFTEST_SUMMARY: 29/30 passed failed=['pacman-Fy-refresh']
```

**M06** — expected detector: compound: var-assign-pacman-query. Evidence: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:161-166`.

```text
CASE var-assign-pacman-query FAIL want=(1, [('package_query', 'pacman:-Q', 2, 'var-assign-query.jsonl')]) got=(0, [])
SELFTEST_SUMMARY: 13/16 passed failed=['var-assign-pacman-query', 'var-assign-pacman-query-permitted', 'dir-scan-all-permitted']
```

**M07** — expected detector: hardening: command-v-lookup-clean. Evidence: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:167-172`.

```text
CASE command-v-lookup-clean FAIL want=(0, []) got=(1, [('live_probe', 'libinput', 1, '')])
SELFTEST_SUMMARY: 32/33 passed failed=['command-v-lookup-clean']
```

**M10** — expected detector: compound: timeout-nohup-hyprctl-mutations. Evidence: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:185-190`.

```text
CASE timeout-nohup-hyprctl-mutations FAIL want=(1, [('host_mutation', 'hyprctl:dispatch', 2, 'wrappers-hyprctl.jsonl'), ('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl')]) got=(1, [('host_mutation', 'hyprctl:keyword', 4, 'wrappers-hyprctl.jsonl')])
SELFTEST_SUMMARY: 14/16 passed failed=['timeout-nohup-hyprctl-mutations', 'dir-scan-all-permitted']
```

**M11** — expected detector: w2-regressions: eval-import-alias. Evidence: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:191-196`.

```text
CASE eval-import-alias FAIL want=(1, [('host_mutation', 'pacman:-S', 1, ''), ('host_mutation', 'sudo', 1, '')]) got=(0, [])
SELFTEST_SUMMARY: 29/30 passed failed=['eval-import-alias']
```

**M12** — expected detector: w2-regressions: eval-from-import-alias. Evidence: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:197-202`.

```text
CASE eval-from-import-alias FAIL want=(1, [('host_mutation', 'pacman:-R', 1, ''), ('package_query', 'pacman:-Qi', 1, '')]) got=(1, [('host_mutation', 'pacman:-R', 1, '')])
SELFTEST_SUMMARY: 29/30 passed failed=['eval-from-import-alias']
```

**M14** — expected detector: w2-regressions: eval-nonliteral-shell-kw. Evidence: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:209-214`.

```text
CASE eval-nonliteral-shell-kw FAIL want=(1, [('host_mutation', 'pacman:-S', 1, ''), ('host_mutation', 'sudo', 1, '')]) got=(0, [])
SELFTEST_SUMMARY: 29/30 passed failed=['eval-nonliteral-shell-kw']
```

**M17** — expected detector: frozen: unknown-key. Evidence: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:227-232`.

```text
CASE unknown-key FAIL want=(2, 'MADO_TRIPWIRE_FROZEN: frozen_error', 0, 0) got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match', ('frozen_match', 0, 0, 0))
SELFTEST_SUMMARY: 30/31 passed failed=['unknown-key']
```

**M19** — expected detector: frozen: symlinked-frozen-dir and symlinked-frozen-dir-target. Evidence: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:239-244`.

```text
CASE symlinked-frozen-dir FAIL want=(2, 'MADO_TRIPWIRE_FROZEN: snapshot_tampered', 0, 0) got=(0, 'MADO_TRIPWIRE_FROZEN: frozen_match', ('frozen_match', 0, 0, 0))
SELFTEST_SUMMARY: 30/31 passed failed=['symlinked-frozen-dir']
```

Nuance: M03 is killed by **rule-attribution fidelity** (`pacman:--syn` becoming `pacman`), not by loss of the host-mutation class. M07 exercises **specificity**: a lookup-only `command -v` is wrongly reported as a live probe. Neither is presented as a demonstrated unsafe execution.

## Nine surviving mutants: exercised regression-case proposals

Every survivor still passes **all 120 existing assertions**. The following cases are proposals only; no lane fixture or test harness was changed. For each proposal, the table shows an **excerpt projection** of the actual JSON output, not a fabricated expected result. Full inputs and complete captures are in the evidence lines cited. The proposal’s intended assertion is pinned to the current pristine behavior; these witnesses do **not** retroactively turn the original-suite survivor into a kill.

### M02 — Refresh flag y no longer outranks read-only sync flags

Add a mixed refresh/read-only sync case, not just plain `-Sy`: the default mutation fallback masks removal of `y` until an info/print/search flag is also present. Assert the host_mutation class and exact rule.

Input command/code is **transcript data only**:

```text
pacman -Syi walker
```

- Proposed assertion: **exit 1; finding host_mutation / pacman:-Syi**.
- Input SHA-256: `4e6cd65a52cf260eaf936df0748a3ebf5551bc9b6d7b691eafeeafe76b33fdf9`.
- Witness target: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M02.jsonl:1`.
- Actual pristine command: `/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/M02/mado-tripwire.py --scan /tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M02.jsonl`. Mutant/restored replay used the same argv.

| Phase | Actual output excerpt (JSON projection) | Raw capture |
|---|---|---|
| pristine | `{"eval_unparsed":[0],"exit":1,"findings":[{"class":"host_mutation","line":1,"rule":"pacman:-Syi"}],"first_line":"MADO_TRIPWIRE: findings","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:377` |
| mutant | `{"eval_unparsed":[0],"exit":1,"findings":[{"class":"package_query","line":1,"rule":"pacman:-Syi"}],"first_line":"MADO_TRIPWIRE: findings","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:386` |
| restored | `{"eval_unparsed":[0],"exit":1,"findings":[{"class":"host_mutation","line":1,"rule":"pacman:-Syi"}],"first_line":"MADO_TRIPWIRE: findings","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:395` |

Restored stdout/stderr and exit are identical to pristine for this witness.

### M05 — Database operation D is classified as package_query

Add a pacman database-operation case. Assert host_mutation rather than only nonzero exit: the mutant still exits 1 with no permits, but silently downgrades the class to package_query.

Input command/code is **transcript data only**:

```text
pacman -D --asdeps walker
```

- Proposed assertion: **exit 1; finding host_mutation / pacman:-D**.
- Input SHA-256: `6c16dafcf23bc03046cb15241786ec561d0932ba5d2377e2bf7598e0d78f97c3`.
- Witness target: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M05.jsonl:1`.
- Actual pristine command: `/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/M05/mado-tripwire.py --scan /tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M05.jsonl`. Mutant/restored replay used the same argv.

| Phase | Actual output excerpt (JSON projection) | Raw capture |
|---|---|---|
| pristine | `{"eval_unparsed":[0],"exit":1,"findings":[{"class":"host_mutation","line":1,"rule":"pacman:-D"}],"first_line":"MADO_TRIPWIRE: findings","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:378` |
| mutant | `{"eval_unparsed":[0],"exit":1,"findings":[{"class":"package_query","line":1,"rule":"pacman:-D"}],"first_line":"MADO_TRIPWIRE: findings","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:387` |
| restored | `{"eval_unparsed":[0],"exit":1,"findings":[{"class":"host_mutation","line":1,"rule":"pacman:-D"}],"first_line":"MADO_TRIPWIRE: findings","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:396` |

Restored stdout/stderr and exit are identical to pristine for this witness.

### M08 — Ignore env --split-string= attached payload

Extend the env split-string regression with the attached `--split-string=` spelling. The existing env fixture covers only `env -S` (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/w2-regressions/env-split-string.jsonl:1`).

Input command/code is **transcript data only**:

```text
env --split-string='pacman -Syu'
```

- Proposed assertion: **exit 1; finding host_mutation / pacman:-Syu**.
- Input SHA-256: `92faffd62563eeafc33e05dccf924dc4c79080cfba8240c8571755bdc2b273f4`.
- Witness target: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M08.jsonl:1`.
- Actual pristine command: `/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/M08/mado-tripwire.py --scan /tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M08.jsonl`. Mutant/restored replay used the same argv.

| Phase | Actual output excerpt (JSON projection) | Raw capture |
|---|---|---|
| pristine | `{"eval_unparsed":[0],"exit":1,"findings":[{"class":"host_mutation","line":1,"rule":"pacman:-Syu"}],"first_line":"MADO_TRIPWIRE: findings","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:379` |
| mutant | `{"eval_unparsed":[0],"exit":0,"findings":[],"first_line":"MADO_TRIPWIRE: clean","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:388` |
| restored | `{"eval_unparsed":[0],"exit":1,"findings":[{"class":"host_mutation","line":1,"rule":"pacman:-Syu"}],"first_line":"MADO_TRIPWIRE: findings","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:397` |

Restored stdout/stderr and exit are identical to pristine for this witness.

### M09 — ionice -n priority argument is mistaken for command

Add an ionice prefix whose numeric `-n` argument would otherwise become argv0. The proposed case detects the actual missed inner mutation without executing ionice or pacman.

Input command/code is **transcript data only**:

```text
ionice -n 7 pacman -Syu
```

- Proposed assertion: **exit 1; finding host_mutation / pacman:-Syu**.
- Input SHA-256: `b9653c57971400dff5f73e47131905a630931d465dcecf666cd11a836cb06e47`.
- Witness target: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M09.jsonl:1`.
- Actual pristine command: `/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/M09/mado-tripwire.py --scan /tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M09.jsonl`. Mutant/restored replay used the same argv.

| Phase | Actual output excerpt (JSON projection) | Raw capture |
|---|---|---|
| pristine | `{"eval_unparsed":[0],"exit":1,"findings":[{"class":"host_mutation","line":1,"rule":"pacman:-Syu"}],"first_line":"MADO_TRIPWIRE: findings","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:380` |
| mutant | `{"eval_unparsed":[0],"exit":0,"findings":[],"first_line":"MADO_TRIPWIRE: clean","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:389` |
| restored | `{"eval_unparsed":[0],"exit":1,"findings":[{"class":"host_mutation","line":1,"rule":"pacman:-Syu"}],"first_line":"MADO_TRIPWIRE: findings","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:398` |

Restored stdout/stderr and exit are identical to pristine for this witness.

### M13 — Reject literal tuple subprocess argv

Add literal tuple argv alongside the existing literal-list subprocess case. Assert the inner host finding, not merely a clean exit or an unparsed counter.

Input command/code is **transcript data only**:

```python
import subprocess
subprocess.run(("pacman", "-Syu"))
```

- Proposed assertion: **exit 1; finding host_mutation / pacman:-Syu**.
- Input SHA-256: `3520941045316ef79cd66b37da729d0696b8014969d71b77c8e39a190fd61c8d`.
- Witness target: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M13.jsonl:1`.
- Actual pristine command: `/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/M13/mado-tripwire.py --scan /tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M13.jsonl`. Mutant/restored replay used the same argv.

| Phase | Actual output excerpt (JSON projection) | Raw capture |
|---|---|---|
| pristine | `{"eval_unparsed":[0],"exit":1,"findings":[{"class":"host_mutation","line":1,"rule":"pacman:-Syu"}],"first_line":"MADO_TRIPWIRE: findings","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:381` |
| mutant | `{"eval_unparsed":[0],"exit":0,"findings":[],"first_line":"MADO_TRIPWIRE: clean","unparsed_spawns":[1]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:390` |
| restored | `{"eval_unparsed":[0],"exit":1,"findings":[{"class":"host_mutation","line":1,"rule":"pacman:-Syu"}],"first_line":"MADO_TRIPWIRE: findings","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:399` |

Restored stdout/stderr and exit are identical to pristine for this witness.

### M15 — Erase unparsed_spawns accounting for nonliteral spawn

Add a JSON-field assertion for `files[0].unparsed_spawns == 1`. The existing nonliteral fixture already exercises this form (`/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-17/tripwire/hardening/eval-nonliteral-unparsed-clean.jsonl:1`), but its current findings/exit-only selftest does not protect the counter. This proposal needs a counter-aware assertion (or a bounded direct `--scan` JSON check), not a changed classification contract.

Input command/code is **transcript data only**:

```python
import subprocess
subprocess.run(cmd, shell=True)
```

- Proposed assertion: **exit 0 / clean; files[0].unparsed_spawns == 1**.
- Input SHA-256: `b3f82ec18f96ac0152b2c2d15da1c05c9c132d61f0c972a930b2db2886d53a3c`.
- Witness target: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M15.jsonl:1`.
- Actual pristine command: `/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/M15/mado-tripwire.py --scan /tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M15.jsonl`. Mutant/restored replay used the same argv.

| Phase | Actual output excerpt (JSON projection) | Raw capture |
|---|---|---|
| pristine | `{"eval_unparsed":[0],"exit":0,"findings":[],"first_line":"MADO_TRIPWIRE: clean","unparsed_spawns":[1]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:382` |
| mutant | `{"eval_unparsed":[0],"exit":0,"findings":[],"first_line":"MADO_TRIPWIRE: clean","unparsed_spawns":[0]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:391` |
| restored | `{"eval_unparsed":[0],"exit":0,"findings":[],"first_line":"MADO_TRIPWIRE: clean","unparsed_spawns":[1]}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:400` |

Restored stdout/stderr and exit are identical to pristine for this witness.

### M16 — Accept JSON boolean expected_exit as integer

Add a frozen pin whose `expected_exit` is JSON `false` while all other fields and inputs are valid. Assert frozen_error rather than accepting Python’s bool-as-int relationship.

Input command/code is **transcript data only**:

```text
printf '%s\n' data
```

- Proposed assertion: **exit 2 / frozen_error; error == bad expected_exit**.
- Input SHA-256: `24696027de4c2a63cf90d112b615edf2ad7cdc909ed4f348280565186b7d9e5f`.
- Witness target: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M16/expected.json:1`.
- Actual pristine command: `/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/M16/mado-tripwire.py --frozen /tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M16`. Mutant/restored replay used the same argv.

Frozen manifest bytes (SHA-256 `61d6238c8e062ed8fee95290e86ac5f5e5481b2aa81b695f1e5b97820bdac608`):

```json
{
  "expected_exit": false,
  "expected_findings": [],
  "expected_label": "clean",
  "inputs": [
    {
      "path": "inputs/witness.jsonl",
      "sha256": "24696027de4c2a63cf90d112b615edf2ad7cdc909ed4f348280565186b7d9e5f"
    }
  ],
  "known_misses": [],
  "permit": [],
  "schema": "mado-tripwire-frozen-v1"
}
```

| Phase | Actual output excerpt (JSON projection) | Raw capture |
|---|---|---|
| pristine | `{"error":"bad expected_exit","exit":2,"first_line":"MADO_TRIPWIRE_FROZEN: frozen_error","outcome":"frozen_error","scan_exit":null,"scan_label":null}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:383` |
| mutant | `{"error":null,"exit":0,"first_line":"MADO_TRIPWIRE_FROZEN: frozen_match","outcome":"frozen_match","scan_exit":0,"scan_label":"clean"}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:392` |
| restored | `{"error":"bad expected_exit","exit":2,"first_line":"MADO_TRIPWIRE_FROZEN: frozen_error","outcome":"frozen_error","scan_exit":null,"scan_label":null}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:401` |

Restored stdout/stderr and exit are identical to pristine for this witness.

### M18 — Allow known-miss/expected-finding overlap

Add an otherwise valid frozen pin with the same listed (file,line) in both expected_findings and known_misses. Assert frozen_error before verdict comparison.

Input command/code is **transcript data only**:

```text
pacman -Syu
```

- Proposed assertion: **exit 2 / frozen_error; error reports known_misses overlaps expected_findings**.
- Input SHA-256: `0ed04c6ad767198ddb7627db2d284b53dd722d00362d3efd90b18931bfcebadb`.
- Witness target: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M18/expected.json:1`.
- Actual pristine command: `/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/M18/mado-tripwire.py --frozen /tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M18`. Mutant/restored replay used the same argv.

Frozen manifest bytes (SHA-256 `84730767d433b532d9a7a869548088949e87192726279259183189d07e86cd8a`):

```json
{
  "expected_exit": 1,
  "expected_findings": [
    {
      "class": "host_mutation",
      "file": "inputs/witness.jsonl",
      "line": 1,
      "rule": "pacman:-Syu"
    }
  ],
  "expected_label": "findings",
  "inputs": [
    {
      "path": "inputs/witness.jsonl",
      "sha256": "0ed04c6ad767198ddb7627db2d284b53dd722d00362d3efd90b18931bfcebadb"
    }
  ],
  "known_misses": [
    {
      "file": "inputs/witness.jsonl",
      "line": 1,
      "note": "intentional overlap rejection witness"
    }
  ],
  "permit": [],
  "schema": "mado-tripwire-frozen-v1"
}
```

| Phase | Actual output excerpt (JSON projection) | Raw capture |
|---|---|---|
| pristine | `{"error":"known_misses overlaps expected_findings: inputs/witness.jsonl:1","exit":2,"first_line":"MADO_TRIPWIRE_FROZEN: frozen_error","outcome":"frozen_error","scan_exit":null,"scan_label":null}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:384` |
| mutant | `{"error":null,"exit":0,"first_line":"MADO_TRIPWIRE_FROZEN: frozen_match","outcome":"frozen_match","scan_exit":1,"scan_label":"findings"}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:393` |
| restored | `{"error":"known_misses overlaps expected_findings: inputs/witness.jsonl:1","exit":2,"first_line":"MADO_TRIPWIRE_FROZEN: frozen_error","outcome":"frozen_error","scan_exit":null,"scan_label":null}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:402` |

Restored stdout/stderr and exit are identical to pristine for this witness.

### M20 — Accept duplicate JSON keys using last-wins

Use a duplicate key whose last-wins interpretation is otherwise completely valid (this witness repeats the same valid schema value). The existing duplicate-key fixture has an independent contradiction and therefore masks removal of duplicate-key rejection; details follow.

Input command/code is **transcript data only**:

```text
printf '%s\n' data
```

- Proposed assertion: **exit 2 / frozen_error; error reports duplicate key, even when both schema values are valid**.
- Input SHA-256: `803bc9bd5262dcc7d2bf35b2c6fe14e881f44cb27f4a1e6feff7029752d38f20`.
- Witness target: `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M20/expected.json:1`.
- Actual pristine command: `/usr/bin/python -I /tmp/mado-r19-MutTripwireTip-dwo4o8mv/M20/mado-tripwire.py --frozen /tmp/mado-r19-MutTripwireTip-dwo4o8mv/proposals/M20`. Mutant/restored replay used the same argv.

Frozen manifest bytes (SHA-256 `3781a013749142c456fab60f45edcbb8ee69432ce74a751d5153f31d4eeeee39`):

```json
{
  "schema": "mado-tripwire-frozen-v1",
  "expected_exit": 0,
  "expected_findings": [],
  "expected_label": "clean",
  "inputs": [
    {
      "path": "inputs/witness.jsonl",
      "sha256": "803bc9bd5262dcc7d2bf35b2c6fe14e881f44cb27f4a1e6feff7029752d38f20"
    }
  ],
  "known_misses": [],
  "permit": [],
  "schema": "mado-tripwire-frozen-v1"
}
```

| Phase | Actual output excerpt (JSON projection) | Raw capture |
|---|---|---|
| pristine | `{"error":"expected.json not JSON (ValueError)","exit":2,"first_line":"MADO_TRIPWIRE_FROZEN: frozen_error","outcome":"frozen_error","scan_exit":null,"scan_label":null}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:385` |
| mutant | `{"error":null,"exit":0,"first_line":"MADO_TRIPWIRE_FROZEN: frozen_match","outcome":"frozen_match","scan_exit":0,"scan_label":"clean"}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:394` |
| restored | `{"error":"expected.json not JSON (ValueError)","exit":2,"first_line":"MADO_TRIPWIRE_FROZEN: frozen_error","outcome":"frozen_error","scan_exit":null,"scan_label":null}` | `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:403` |

Restored stdout/stderr and exit are identical to pristine for this witness.

### Why the existing duplicate-key case survives M20

The current fixture at `/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-18/tripwire/frozen/duplicate-json-key/expected.json:17,31-33` declares `expected_label: "findings"`, then repeats `permit`, changing it from `[]` to all three classes. With duplicate detection removed, last-wins parsing therefore encounters a **different invalid pin**: no expected class remains outside permit. The frozen selftest only needs exit 2 / frozen_error, so it still passes.

Actual direct mutant replay output, `/tmp/mado-r19-MutTripwireTip-dwo4o8mv/probe-evidence.jsonl:404`:

```text
MADO_TRIPWIRE_FROZEN: frozen_error
{"error": "findings baseline lists no class outside permit", "exit": 2, "expected_sha256": "8e08c0fb8036733731257f3b489be530576c9803c3d3db6a3e9e5e39e1c4d1ee", "extra_findings": [], "inputs": [], "missing_findings": [], "outcome": "frozen_error", "scan_exit": null, "scan_label": null, "schema": "mado-tripwire-frozen-verdict-v1", "tool_sha256": "3a5d7854afa4eb33b0925610e8394e0d0a807fc9b9ee7621a12d1ec1198bba4c"}
```

The new valid-valued duplicate-schema witness returns frozen_error on pristine/restored bytes and frozen_match on M20, isolating the intended duplicate-key obligation. M20’s supplemental six-suite replay again passed all 120 cases at the **same** mutant SHA-256; this is a confirmed test-mask survivor, not an equivalent mutation.

## Limits

- This is the assigned mutation probe only: no implementation, integration, ship decision, C1/C2/C3 judgment, or live-host safety verdict.
- The target is commit `17661e0fa83f978fb659f5bb8fef47f0969f6945` and the six fixture trees actually present during the probe. No claims about later tripwire edits or the three round-18 drafts are made.
- The mutation set is deliberately small and selected, not exhaustive. All nine surviving points have observed non-equivalent witnesses; the remaining unmutated paths are not certified.
- No host executables named inside synthetic transcripts were launched. No pacman/sudo transaction, compositor/device/service operation, live gate, network fetch, OMP CLI, credential file, or private agent database was used.
- Original suite selftests, bounded scan/frozen replays, and output/byte hashes are the only exercised verification. No repo build, unrelated tests, or working-tree-wide validation was run.
- Only this report was written in the lane; all probe files and raw receipts are under the isolated `/tmp` root. Scratch source copies have been restored exactly; `/tmp` retention is not guaranteed, which is why the report records exact mutations, hashes, fixture manifests, and observed excerpts.

## Installs

none
