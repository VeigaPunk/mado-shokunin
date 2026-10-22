# ReResource: C1 resource guard at the landed tip (wave 2, falsify)

Seat MadoR23.ReResource, leaf reviewer. 2026-10-22, local times (-0300) 08:55 to 09:08.
Target: landed tip `2f1134f3`, C1 classifier `tools/mado-tripwire.py` blob `41489991…` (from `2e592aff`).
Baseline: `w1/reports/BaseResource.md` (base classifier blob `cd9da20c…`).
No lane file was edited. Receipts and copies are in scratch: `/fast/scratch/hyaku/mado-r23/ReResource/`.

## Summary

- **The guard is clean at the landed tip.** The four assigned commands exit 0 with empty stderr on every run. Every harness case reports `MADO_TRIPWIRE: clean` with zero findings, zero leads, zero unparsed spawns, no timeouts, no reap failures, and no digest or fixture change. Run 1 peaks at 43,284 KiB (42.3 MiB) RSS and 0.288 s. Across all four lane runs (48 rows) the peak is 44,004 KiB and the slowest case is 0.288 s. Caps are 384 MiB and 15 s.
- **The cost against base is small.** In the same session, paired by rep, landed minus base is +0.5 MiB median RSS and +0.004 s median time. The r22 population pays +0.010 to +0.016 s at 1024 and 2048 closures. The r21 population pays about nothing.
- **The guard is weaker evidence than it looks.** (F1) The lane tool file changed in place at least four times during this session, through five distinct digests, so lane-path runs do not measure the landed tip. (F2) The guard never reaches the changed escape analysis, so it cannot falsify that cost. (F3) The 384 MiB cap is `RLIMIT_AS`, which is address space. The CLI path peaks at about 233 MiB of address space, a margin of about 1.65×, not the 9× that RSS suggests.

## What I did

1. Read the godspeed skill, `registration.md`, `BaseResource.md`, both harness sources, and the host RULES. Checked identity with read-only git (`--no-optional-locks`): `2f1134f3:tools/mado-tripwire.py` is `41489991…`, the same as `2e592aff`. The base blobs `e33ea304` and `a28e4815` are `cd9da20c…`. At 08:57 the lane `tools/` status was clean and the working copy matched the landed blob.
2. **Run 1 (landed bytes).** I ran the four assigned commands sequentially from the lane root. I drove them through a Python subprocess with argv identical to the shell form, one child at a time. Every per-case receipt pins the tool digest before and after its scan, and all of them show `41489991`, so run 1 measured the landed bytes.
3. **Runs 2 and 3, and a closing run.** The same four commands, lane path. Runs 2 and 3 measured digest `8975a4da`. The closing run measured `eeb6f515` and that digest did not change during the run. These are lane working-copy states, not the landed tip (F1).
4. **Same-session A/B in a read-only mirror.** The mirror is under scratch. It holds byte-identical copies of both harnesses and the round-22 workload directory (I checked the hashes), so the harness re-verifies the manifest hash before and after each case. Three classifier arms: `base` (`cd9da20c…`), `landed` (`41489991…`, extracted from the git object `2f1134f3:tools/mado-tripwire.py`), and `inflight` (`82d5ffa8…`, a snapshot of the working copy). Three rotated reps times four configs times three arms gives 36 runs, all clean.
5. **Address-space probe.** `RLIMIT_AS` set in the child by `preexec_fn` to 384 MiB, then 256, 192, 160, and 128 MiB, on the two largest committed fixtures (r21 `assignments-4000.jsonl`, r22 `stored-closures-2048.jsonl`), both modes, all three arms. VmPeak and VmHWM are read from `/proc/self/status` at exit. One child at a time, 15 s deadline. Wrappers: `probes/vm_module_wrapper.py` and `probes/vm_cli_wrapper.py`.
6. **Coverage probe.** A counting wrapper around the module's functions (it calls the original and returns its result unchanged). Run on the committed guard fixtures and the 12 committed repair fixtures, `python3 -I`, 384 MiB cap. Wrapper: `probes/coverage_wrapper.py`.
7. **Cold and warm bytecode.** Three cold and three warm module-main runs on a scratch copy of the landed bytes.
8. Read-only checks only: git status, diff, show, check-ignore, ls-files; `ls`, `stat`, `sha256sum`, glob. I ran no jj command and installed or updated no tool. The only lane writes are gitignored `__pycache__` files that the assigned commands create (F5).

Exact commands (run 1, cwd = lane root; runs 2 and 3 and the closing run are identical):

```
cd /home/vgpnk/Projects/shokunin/mado-shokunin
python3 -I .ufo/waves/round-22/resource-closure-measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --mode module-main
python3 -I .ufo/waves/round-22/resource-closure-measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --mode cli
python3 -I .ufo/waves/round-21/resource/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --mode module-main
python3 -I .ufo/waves/round-21/resource/measure.py --tool /home/vgpnk/Projects/shokunin/mado-shokunin/tools/mado-tripwire.py --mode cli
```

Mirror A/B: the same four commands with cwd = `/fast/scratch/hyaku/mado-r23/ReResource/mirror` and `--tool <mirror>/tools/{base,landed,inflight}.py`.

Environment: `/usr/bin/python3` 3.14.8. Host load averaged 4.6 to 6.0 on 32 cores; 22.6 GiB available memory.

## Results

### Per-case RSS (KiB) and time (s)

BaseResource is the published table. Run 1 is the landed bytes on the lane path. The three same-session columns are medians over three reps, all clean.

| harness | mode | size | BaseResource | run 1 landed (lane) | same-session base | same-session landed | same-session in-flight |
|---|---|---|---|---|---|---|---|
| r21 | module-main | 1000 | 26580 / 0.054 | 20328 / 0.034 | 20008 / 0.034 | 20024 / 0.033 | 20084 / 0.035 |
| r21 | module-main | 2000 | 23316 / 0.048 | 23372 / 0.054 | 23544 / 0.048 | 23580 / 0.049 | 23632 / 0.049 |
| r21 | module-main | 4000 | 29508 / 0.081 | 29296 / 0.085 | 29480 / 0.081 | 29196 / 0.080 | 29540 / 0.079 |
| r21 | cli | 1000 | 29692 / 0.052 | 30824 / 0.057 | 29676 / 0.052 | 31156 / 0.054 | 31324 / 0.053 |
| r21 | cli | 2000 | 32804 / 0.071 | 33548 / 0.078 | 32304 / 0.068 | 33260 / 0.067 | 33300 / 0.069 |
| r21 | cli | 4000 | 37648 / 0.098 | 39792 / 0.107 | 38360 / 0.101 | 39380 / 0.100 | 39552 / 0.099 |
| r22 | module-main | 512 | 21852 / 0.071 | 21052 / 0.083 | 22084 / 0.070 | 21044 / 0.074 | 21076 / 0.076 |
| r22 | module-main | 1024 | 25156 / 0.122 | 24152 / 0.140 | 24776 / 0.121 | 24860 / 0.133 | 24844 / 0.132 |
| r22 | module-main | 2048 | 32292 / 0.230 | 31600 / 0.259 | 32548 / 0.242 | 32436 / 0.257 | 32524 / 0.254 |
| r22 | cli | 512 | 29744 / 0.092 | 31052 / 0.098 | 30480 / 0.086 | 31828 / 0.092 | 31980 / 0.095 |
| r22 | cli | 1024 | 33824 / 0.141 | 34696 / 0.154 | 34536 / 0.141 | 34708 / 0.152 | 34208 / 0.156 |
| r22 | cli | 2048 | 41004 / 0.259 | 43284 / 0.288 | 41960 / 0.256 | 42708 / 0.270 | 42980 / 0.274 |

Notes:
- The BaseResource r21 module-main 1000 row (26580 KiB, 0.054 s) is most likely a cold first child. The base classifier was extracted to scratch just before that harness run. The same-session warm base is 20008 KiB and 0.034 s, and the 2000 and 4000 rows agree with the same-session base. The cause is inferred; the pattern matches the cold-compile effect in F4.
- Same-session base and BaseResource agree within about 0.01 s on the r22 rows. The run 1 deltas against BaseResource (up to +0.029 s at 2048) are about twice the paired same-session deltas below. I attribute the rest to host-load drift; that is inferred.

### Paired deltas, same rep, against base (3 reps each)

| harness | mode | size | landed minus base: RSS KiB / s | in-flight minus base: RSS KiB / s |
|---|---|---|---|---|
| r21 | module-main | 1000 / 2000 / 4000 | +92 / -0.001; +36 / -0.001; +156 / -0.003 | +264 / +0.001; +564 / -0.001; +412 / -0.003 |
| r21 | cli | 1000 / 2000 / 4000 | +1448 / +0.002; +768 / -0.001; +1020 / -0.000 | +1848 / +0.002; +848 / +0.001; +1156 / +0.001 |
| r22 | module-main | 512 / 1024 / 2048 | -1040 / +0.004; -96 / +0.010; +80 / +0.016 | -844 / +0.005; +68 / +0.011; -36 / +0.021 |
| r22 | cli | 512 / 1024 / 2048 | +1316 / +0.006; +488 / +0.013; +844 / +0.012 | +1500 / +0.009; -84 / +0.013; +952 / +0.020 |

Overall medians across 36 pairs: landed +468 KiB and +0.004 s; in-flight +484 KiB and +0.004 s. The largest positive RSS outliers (about +6 to +7 MiB) are cold first children (F4). The r22 time deltas track the bookkeeping the coverage probe shows: r22 follows 2048 helpers, runs `own_names` 2001 times and `scope_view` 2001 times. The r21 population makes no helper calls, and its deltas are near zero.

### Address space (VmPeak, kB) under the guard cap and below

| arm | module-main r22-2048 / r21-4000 (384 MiB) | cli r22-2048 / r21-4000 (384 MiB) |
|---|---|---|
| base `cd9da20c` | 44172 / 41284 | 235880 / 235876 |
| landed `41489991` | 44192 / 41308 | 238568 / 238568 |
| in-flight `82d5ffa8` | 44220 / 41316 | 238588 / 238588 |

- Margins under the 384 MiB `RLIMIT_AS` cap: module-main about 8.9× (VmPeak about 43 MiB). CLI about 1.65× (VmPeak about 233 MiB).
- CLI still passes with rc 0 and `MADO_TRIPWIRE: clean` at 256, 192, 160, and 128 MiB caps on both fixtures (base and landed). At 128 MiB its VmPeak falls to 83 to 88 MiB, because the worker stack shrinks to a quarter of the cap. Module-main also passes at 128 MiB. The address-space margin on the largest committed fixtures is therefore at least 3×.
- One composition probe (landed, 384 MiB, r22-2048, CLI): VmPeak 238960 kB; at exit, with one thread left, VmSize is 112800 kB. The mappings at exit are a 55 MiB PROT_NONE anonymous region, an 11 MiB heap, and 8 MiB and 5 MiB anonymous regions. So about 123 MiB of the peak is transient thread-time reservation. The 64 MiB worker stack is one part of it. The rest is most likely glibc per-thread malloc arena reservation. Both are inferred; I did not attribute the peak mid-run.

### Coverage of the changed code (call counts; committed inputs only)

| population | reference_escapes | parameter_escapes | scope_entry / scope_view / own_names | follow_helper | distinct line templates |
|---|---|---|---|---|---|
| r22 512 (guard) | 0 (all arms) | 0 (all arms) | base 0; landed and in-flight 512 / 512 / 512 | 512 | 6 |
| r22 2048 (guard) | 0 (all arms) | 0 (all arms) | base 0; landed and in-flight 2048 / 2001 / 2001 | 2048 | 6 |
| r21 1000, 2000, 4000 (guard) | 0 | 0 | 0 | 0 (no helper calls; spawn_scan 1) | 1 |
| 12 repair fixtures (landed) | 1 to 3 per case, all 12 non-zero | 1 to 2 in 8 of 12 | 6 to 14 scope_entry; 2 to 4 scope_view and own_names | 1 to 3 | not counted |

- The r22 guard templates are `unrelated_caller_binding_N = N`, `stored_helper_N = visible_factory()`, and a fixed four-line factory. No helper is ever passed as an argument. The r21 guard is one template, `binding_N = N`.
- The repair fixtures return the scanner's findings exit (1) and cost about 27 MiB and 0.03 s each. I did not assess their verdicts; that belongs to the repair reviewer.

### Cold and warm module-main (scratch copy, three runs each)

The r22 512-closure row is cold at 28248 to 29048 KiB and 0.092 to 0.095 s. Warm it is 20020 to 21316 KiB and 0.074 to 0.076 s. The 1024 and 2048 rows are the same cold and warm. Only the first child after the bytecode cache is missing is affected.

## Findings, by severity

### F1 (Medium): the lane path does not pin the landed tip, because the working copy is edited in place

Evidence:
- At 08:57 `git status --porcelain -- tools/` was empty and the file matched `41489991`.
- Digests seen at the lane path, in order: `41489991` (landed; run 1, pinned per case). `8975a4da` (size 175636, mtime 08:59:14; runs 2 and 3, pinned per case). `82d5ffa8` (size 174005, mtime 09:01:03; the A/B "inflight" snapshot). `eeb6f515` (size 176289, mtime 09:04:12; closing run, unchanged during that run). `e1dc8029` (size 177293, mtime 09:05:48; seen by sha only, not measured).
- At 09:01:15, `git diff 2f1134f3 -- tools/mado-tripwire.py` is +39 and -33 lines. It rewrites `parameter_escapes` from a denylist to an allowlist and adds `DYNAMIC_SCOPE_CALLS`. Its docstring cites "round-23 wave-2 counterexamples". Saved as `lane-workdiff-vs-landed.diff` (sha `1dbe4fa7…`).
- The per-case digest pins catch a change only during one scan. They cannot tell a reader which state was measured. My runs only read the tool file. I did not identify the writer.

Consequence: the assigned command, as written, measures whatever bytes the lane holds when it runs. Registration clarification 10 already requires that after-values come from `git show <tip>:tools/mado-tripwire.py`.

Advice (not applied): measure landed-tip claims from a scratch extraction of `2f1134f3`, and treat lane-path runs as digest-labelled lane-state checks only.

### F2 (Medium): the guard cannot falsify the cost of the changed escape analysis

Evidence: the coverage table. In every arm the guard populations make zero calls to `reference_escapes` and `parameter_escapes`. The r21 population makes no helper calls at all. The only committed inputs that reach the path are the 12 repair fixtures, each with one to three calls. Those are tiny, so the new per-reference work has never been timed at a size where it could matter.

Code reading (inference, not measured): the landed `parameter_escapes` runs a `while changed:` loop, and each pass does a full `ast.walk` of the callee body. So each reference costs about (alias-chain depth plus one) times the body size. The in-flight version also builds a `parents` map and a `nested` set over the same body on every call. Either could go superlinear on a large callee with long alias chains, or on many callable references, and the guard would not show it.

Advice: before the escape change lands, register a committed population that hands N callables into calls with alias chains, at several sizes. Measure base, landed, and in-flight with the same harness. I did not create or run such a population, because the contract limits classifier runs to committed fixture data.

### F3 (Low): the "9× headroom" in BaseResource is an RSS figure, but the guard cap is address space

Evidence: the VmPeak table. The CLI path peaks at 230 to 233 MiB of address space, about 1.65× under 384 MiB. Module-main peaks at about 43 MiB, about 8.9×. CLI still passes at 128 MiB on both largest fixtures, so the real address-space margin is at least 3×. The worker thread is the reason CLI differs. `run_with_stack` (landed lines 3672 to 3676) requests `min(64 MiB, max(8 MiB, cap // 4))` when the cap is at most 512 MiB. Base has identical code. The harness records only `ru_maxrss`. Recording VmPeak is a design choice for the owner, because the harness docstring says it reads no `/proc` paths.

### F4 (Low): module-main numbers depend on bytecode cache state

Evidence: the cold and warm experiment. The first module-main child after the cache is missing (after any tool edit, or in a fresh scratch path) costs +7 to +9 MiB and +0.02 s on the 512 row. This also explains the BaseResource r21 module-main 1000 row (see the per-case notes). Advice: discard or separately report the first module-main case after any tool change, or report a warm second run.

### F5 (Low): the assigned commands write gitignored bytecode into the lane, and environment flags cannot stop it

Evidence:
- `tools/__pycache__/mado-tripwire.cpython-314.pyc` was rewritten at 09:00:32, inside the window of my runs 2 and 3. The module-main child imports the tool, so it writes that cache.
- `.ufo/waves/round-21/resource/__pycache__/measure.cpython-314.pyc` is loaded by the round-22 harness. It is dated 2026-10-21 and was not rewritten by my runs.
- `git check-ignore` matches both paths to `.gitignore:3:__pycache__/`. `git ls-files | grep -c pycache` is 0.
- `python3 -I` ignores `PYTHONDONTWRITEBYTECODE` and `PYTHONPYCACHEPREFIX`. With both set, `sys.dont_write_bytecode` is False and `sys.pycache_prefix` is None.

Consequence: the assigned commands cannot run write-free in the lane. Advice: run harness copies in scratch, as I did for the A/B, and keep lane-path runs as lane-state checks.

### F6 (Info): stale harness documentation (round-21)

The `measure.py` docstring (lines 7 to 12) says CLI mode "can fail" under 384 MiB, because the scanner requests a 512 MiB worker stack, and it tells operators to preserve that failure. At this tip the request is adaptive (F3), and CLI passed at every cap I tried down to 128 MiB. There is no failure to preserve, so the docstring is stale. BaseResource's F2 said the same. Updating it is the owner's call.

### F7 (Info): the same-session base agrees with BaseResource within noise; the round-22 harness refuses out-of-repo tools

The round-22 harness rejects a `--tool` outside the repository (`selected_tool`, lines 212 and 213). That is why base-versus-landed in one harness needs the mirror. The mirror copies are byte-identical, so the comparison stands.

## Residual risk and verification gaps

- The landed-tip RSS and time numbers come from run 1 on the lane path (digest pinned) and from the git-object arm of the A/B. Both agree.
- Not measured: scaling beyond 2048 closures; the escape path at any non-trivial size (F2); verdict correctness beyond `clean` for the guard populations.
- The VmPeak composition is from exit-time mappings, after the worker thread ends. Mid-run composition was not observed directly.
- Timing noise: host load 4.6 to 6.0 on 32 cores. Repeats of the same bytes spread about ±5 to 10%. Differences under about 0.01 s are not meaningful.
- The lane digest moved during the session. The last measured digest was `eeb6f515` (closing run). `e1dc8029`, seen at 09:05:48, was not measured by the harness.
- The mirror arms are my own scratch copies. Their harness and workload copies are byte-identical to the lane (checked).
- No tool was installed or updated. No pacman command was run. Python is `/usr/bin/python3` 3.14.8.

## Artifacts (scratch, sha256 prefixes)

- `run1/` (landed bytes, lane path): `r22-module-main.stdout` `6b8717ab…`, `r22-cli.stdout` `9718f701…`, `r21-module-main.stdout` `a9e86af6…`, `r21-cli.stdout` `c2e0dafe…`, `summary.json`, `pycache-before.json`, `pycache-after.json`.
- `run2/`, `run3/` (digest `8975a4da`, lane path).
- `run-final/` (digest `eeb6f515`, lane path): `r22-module-main.stdout` `b5566802…`, `r22-cli.stdout` `66822923…`, `r21-module-main.stdout` `2acd1efa…`, `r21-cli.stdout` `6fa1f34c…`, `summary.json`.
- `ab2/` and `ab2-results.json` (`3aa19541…`): the 36 mirror runs, arms base, landed, and inflight. The earlier `ab/` set is superseded and not used; its "landed" arm was the `8975a4da` state.
- `vm-probe.json` (`4854fb63…`), `coverage-probe.json` (`32ec533a…`), `repair-coverage-landed.json` (`7cfc9fa2…`), `coldwarm/` and `coldwarm.json` (`46910106…`).
- Classifier copies: `landed-2f1134f3.py` (`41489991…`, equal to the git object), `base-e33ea304.py` (`cd9da20c…`), `inflight-snapshot.py` (`82d5ffa8…`, 174005 bytes), `tool.diff` (`8fe8da27…`, base to landed), `lane-workdiff-vs-landed.diff` (`1dbe4fa7…`).
- Probe wrappers: `probes/vm_module_wrapper.py`, `probes/vm_cli_wrapper.py`, `probes/coverage_wrapper.py`. Mirror: `mirror/`.

## Verdict

PASS for the C1 resource guard at the landed tip `2f1134f3` (classifier `41489991…`). All four assigned commands exit 0 on every run, and all 12 cases per run are clean. Peak RSS is 44,004 KiB and the slowest case is 0.288 s over all lane runs, within 384 MiB and 15 s. Against base the cost is small. This is not sufficient evidence for the changed escape analysis (F2). Lane-path runs are not landed-tip evidence while the working copy drifts (F1).
