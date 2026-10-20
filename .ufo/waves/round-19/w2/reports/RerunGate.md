# RerunGate — holds

Attack target: the wave-1 gate claim "gate jj F6/F9 + walker pin (selftest 443/443) + `--regression` PASS at PIN_MADO `05aea198…`", integrated tip `01b80946d92b26370d3012a7da655d00dd135154`. Every number below was re-measured by this seat; the two named modes were run against the lane gate and against a `/tmp` copy of the tip bytes. One low-severity prose falsity found (F2); one material wave-state event found mid-run (F1); no behavioral claim broke.

## 1. Byte identity and the two permitted modes

First action (before anything else), at ~18:02Z, worktree clean of tracked edits (`git status --porcelain` listed only three `??` wave dirs, `git rev-parse HEAD` = `01b80946…`):

```
$ sha256sum tools/mado-verify.sh
1036d1004e63d80377faa4f905fd8dc1897eb29b64496cbfef647b47cec4f2af  tools/mado-verify.sh
$ git show 01b80946d92b26370d3012a7da655d00dd135154:tools/mado-verify.sh | sha256sum
1036d1004e63d80377faa4f905fd8dc1897eb29b64496cbfef647b47cec4f2af  -
```

Selftest (run 1, same bytes), plus two independent repeats:

```
$ bash tools/mado-verify.sh --selftest
MADO_SELFTEST: 443/443 assertions passed          (exit 0, 13.1 s)
$ env -i HOME=/tmp/rgr-nohome PATH=/usr/bin:/bin /bin/bash tools/mado-verify.sh --selftest
MADO_SELFTEST: 443/443 assertions passed          (exit 0)
$ bash tools/mado-verify.sh --selftest            (output sha256 ceb38a78…)
MADO_SELFTEST: 443/443 assertions passed          (exit 0, byte-identical stdout)
```

The claimed baseline arm `389` also reproduces, and the gate bytes named in the wave-1 report are the same file:

```
$ git show 9c54c56:tools/mado-verify.sh | sha256sum
c9fb0cef3e081dc878d69f8e20c148429bdfbdce949f8afaed705db957ea42b5  -     # = GateFreshJj "OLD 17661e0 (c9fb0cef…)"
$ bash /tmp/rgr-mutants/baseline.sh --selftest
MADO_SELFTEST: 389/389 assertions passed          (exit 0)
```

Regression (run at 18:03:05Z against the tip bytes), exit 0, band applied strictly (no `killed-delta<=1` slack):

```
REGRESSION_TOOL: …/tools/mado-verify.sh sha256=1036d100…cec4f2af
REGRESSION_HARNESS: /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh sha256=fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a (recorded revision b56c6e57… — provenance, not gated)
REGRESSION_SPEC: …/mado-verify.defects.spec sha256=c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8 (recorded pin matches)
REGRESSION_TARGET: … sha256=05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0 (recorded pin 05aea198…; match=yes)
REGRESSION_BAND: all recorded kills required (recorded 10/10 KILLED; flips=0; inconclusive=0; control GREEN; MUTATE_RESTORE OK; target sha unchanged)
REGRESSION_SWEEP mado-verify-hardened: MUTATE: DONE (target=… defects=10 killed=10 survived=0 inconclusive=0 kill-rate=100%)
REGRESSION_TABLE mado-verify-hardened: match=10/10 recorded-killed=10 measured-killed=10 survived=0 inconclusive=0 flips=0
REGRESSION_CASE mado-verify-hardened: PASS (recorded table reproduced: killed=10/10 flips=0 inconclusive=0 control=green restore=ok)
REGRESSION_CLEANUP: removed=3 kept-fixture dir(s) named by this run
MADO_REGRESSION: PASS (case=mado-verify-hardened; target=05aea198…)
```

Re-cut constants and pin, read at the tip:

```
# tools/mado-verify.sh @ 01b80946
1951:PIN_MADO='05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0'
1952:SPEC_SHA='c7ee75b97c38ac8f88410165a574ad1cba7f4653bd09d35e6814267a12df1dd8'
1953:HARNESS_SHA_RECORDED='b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb'
1954:TABLE_MADO='D1:KILLED,…,D9:KILLED,R1:KILLED'
603:    st_eq "R10: derived target equals the recorded gate revision" "$PIN_MADO" "$dsha"
```

Independent re-derivation of the pinned target with my own `sed` (tip source → `/tmp/rgr-mutants/derived.sh`), then its own selftest:

```
05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0  /tmp/rgr-mutants/derived.sh
2745 /tmp/rgr-mutants/derived.sh
138328 /tmp/rgr-mutants/derived.sh
$ bash /tmp/rgr-mutants/derived.sh --selftest
MADO_SELFTEST: 338/338 assertions passed          (exit 0; sha unchanged before/after)
```

That matches the in-file round-19 re-cut record (`:1912-1937`: 2,745 L / 138,328 B / `05aea198…`, control `338/338`), so `PIN_MADO` is the derived target's sha, not the gate file's sha — a distinction the file states but the wave headline ("gate 443/443 + PASS at PIN_MADO") does not; both values are correct for their own objects (gate `1036d100…`, target `05aea198…`).

## 2. Falsification attempts (all failed to break the claim)

A. **Discriminating power of the 443 assertions.** Three `/tmp` copies of the tip gate, each run only with `--selftest` (host-pause-compliant), targeting the three claimed repairs:

| mutant | one-line mutation | result |
|---|---|---|
| A (F6 revert) | `:3723` `[ -d "$tree/.jj" ] && jcol=1` → `: # jump stays 0` | `FAILED — 434 passed, 9 failed`; OM11 (2 assertions: tag/head name `refs/heads/master`), OM14 (4: `2 branch tips`), OM15 (2: `no branch tip under`) all red |
| B (F9 revert) | `:3687` `git rev-parse --git-dir` → `[ -d "$tree/.git" ]` | `FAILED — 435 passed, 8 failed`; OM12 (4: `.git`-FILE checkout blinded again), OM13 (3: expected UNKNOWNs disappear) red |
| C (pin revert) | `:105` `WALKER_VERSION_PIN="2.17.2"` → `"2.17.0"` | `FAILED — 436 passed, 7 failed`; WL0, WL1 (4, incl. narrowed PASS text), WL2 red |

Each mutant also trips R10 (`:603`), which is a byte detector, so the real evidence is the named OM/WL row failures: the rescues asserted in the report are behaviorally covered, not just named.

B. **Hermeticity (`--selftest` claims "no substrate reads").** `strace -f -e trace=openat,execve` over a full 443/443 run (28.4 s, `/tmp/rgr-mutants/strace.log`, run output still 443/443):

- successful opens of `/home/vgpnk/.config/...`: **0**;
- successful opens/writes under `/home/vgpnk` other than the gate file itself and `O_DIRECTORY` scans of the lane root: **0** (no `O_WRONLY|O_CREAT|O_TRUNC` at all);
- no host `git`, `hyprctl`, `systemctl`, `walker`, `omarchy` exec: fixture stubs only (`$T/*/bin/...`); no `/usr/bin/git` in the execve set;
- PATH candidates under `/home/vgpnk` were probed by bash's normal lookup and every one is absent (`/home/vgpnk/.local/share/omarchy/bin/sha256sum` etc. → ENOENT; `/usr/local/{bin,sbin}/sha256sum` absent); the executed hasher is `/usr/bin/sha256sum`;
- residual ambient dependency: `/usr/bin/python3` loads `/usr/lib/python3.14/site-packages/distutils-precedence.pth` + `_distutils_hack` and enumerates the directory `~/.local/lib/python3.14/site-packages` (986 directory opens, no package file read). No user package is imported; the config plane is untouched.

C. **Stale-pin visibility.** R10 is not decorative: on the currently modified worktree it is the one red assertion (F1 below), exactly as the re-cut note says a moved gate must be visible.

D. **PASS-on-nothing check.** `REGRESSION_CASE` requires: every recorded id present (`ABSENT` counts as a flip), measured verdict equal to the recorded `KILLED`, `total` = 10, control GREEN, `MUTATE_RESTORE: OK`, target sha unchanged. A no-op or missing harness yields SETUP/FAIL, never PASS (SETUP path re-demonstrated in F1's second run).

## 3. Findings

**F1 — material, wave state (not a defect in the tip claim): the lane worktree changed under this seat while the wave was running.** My tip receipts are anchored to `1036d100…` (printed by both runs) and remain valid; they also reproduce from a `/tmp` copy of the tip (`18:12:02Z`: `REGRESSION_TOOL sha256=1036d100…`, `target 05aea198… match=yes`, 10/10 KILLED, `MADO_REGRESSION: PASS`, `removed=10`, exit 0). But `tools/mado-verify.sh` was rewritten at `2026-10-20 15:10:48 -0300` (`6c74fa619865524d5f94e6f812dc896a1d8718ce4bb596caf661b7878effde2c`; +2/−1 WL1/WL3 assertions, walker/pin comments) and again at `15:13:49` (`5cdcde5dbfcb2cf3523bedfea395d63decafebb5acccf941827189cd613a282b`):

```
$ bash tools/mado-verify.sh --selftest          # 15:11, 6c74fa…
MADO_SELFTEST: FAILED — 443 passed, 1 failed    # total 444
  - R10: derived target equals … (got '1fbf26e5…' want '05aea198…')
$ bash tools/mado-verify.sh --selftest          # 15:14, 5cdcde5d…
MADO_SELFTEST: FAILED — 451 passed, 1 failed    # total 452
  - R10: derived target equals … (got 'f03e6cab…' want '05aea198…')
$ bash tools/mado-verify.sh --regression --keep # 18:11:32Z
REGRESSION_TARGET: … sha256=1fbf26e5… (recorded pin 05aea198…; match=no)
MADO_REGRESSION: SETUP (target pin mismatch — the gate moved outside the MADO-R7 blocks; re-cut, then update PIN_MADO/TABLE_MADO)   # exit 2
```

`git status --porcelain` now lists 24 modified tracked files (gate, SCORECARD, SKILL, PROVINCE, LOG, corpus/*, .ufo/…) with mtimes 15:07–15:16. Consequence for the main agent: any post-integration verification run in the current worktree will be red on R10 and SETUP on `--regression` until L1 either commits the edits and performs the measured re-cut (`PIN_MADO`/`TABLE_MADO`), or reverts them. The 443/443 and PASS claims are true of the attacked tip, not of the live worktree.

**F2 — low severity: the regression header's excision recipe is false as written.** Tip `:1819-1822` says the target is "THIS file with **the two** MADO-R7 blocks excised". The actual derivation (`mado_r7_target_build`, `:2035-2048`) excises **three** marker pairs — `MADO-R7-REGRESSION-BLOCK`, `MADO-R7-SELFTEST-BLOCK`, and `MADO-R8-BLOCK` (`:2043`). Following the prose literally does not reproduce the pin:

```
$ sed (only the two MADO-R7 pairs) tip-src.sh > derived-two-blocks.sh
e13e8e37906082919a0f657d826c3513832b2cbb49349bc26a661eddaac9456b  derived-two-blocks.sh   # 3432 L
05aea198a2084ea1fd87825fd6183e5afd9a2d95f8cc06476efcaa7e0af6cca0  derived.sh              # 2745 L, correct
```

The value is right; only the recipe sentence is stale (the function comment at `:2036-2040` correctly describes the R8 excision). Documentation fix, no behavioral effect.

**F3 — coordination fact: an external wildcard deletion of `/tmp/w5-mado-m52-selftest.*` occurred at ~18:04:53Z.** My 18:03:05Z regression sweep created ten failing-suite fixtures but its cleanup found only 3 (`removed=3`); the identical pristine-tip run at 18:12:02Z found all ten (`removed=10`). Peer `MadoR19.MutGateR19` independently lost five roots created 18:04:37Z, gone ~16 s later. The gate's deletions are all exact-path/prefix-guarded (`:1802` own `$T` on pass, `:1303-1310` nested child's named path, `:2213-2221` paths named by the run's own sweep evidence, `:2234` own regression root); tameshi's harness `fb6d86d5…` removes only its own `$root` (`:1307`, `:1835`). The only wildcard `/tmp/w5-mado-m52-selftest.*` deletion in lane literature is round-13 `Safety.md:191`'s manual remediation. Actor [UNK]; mechanism [INFERENCE] = that wildcard executed while probes were live. No gate or harness cleanup bug: with no external interference the same bytes clean up 10/10.

## Limits

- Host pause honored: no pacman/sudo/systemctl/hyprctl/walker/omarchy/compositor action; no live (`no-mode`) gate run, so no host config-plane verdict is claimed. No jj command; lane git use read-only; no lane edits (only this report). All gate runs were `--selftest`/`--regression`, including `/tmp` copies.
- Concurrency: `--regression` depends on the sibling harness bytes at `tameshi-shokunin/tools/mutate-and-run.sh`; its sha is printed but explicitly **not gated** (`HARNESS_SHA_RECORDED` is provenance). Control GREEN is an exit-0 requirement, not an assertion-count check; the `338/338` control figure is a re-cut record and I reproduced it independently on the pinned target.
- The gate does not pin its own assertion count; "443" is an external report/recipe number. A silent assertion deletion would print a smaller green `N/N` — true to itself, but the 443 claim would go stale. The current worktree illustrates the drift (444, then 452 assertions) without the pin noticing.
- Selftest hermeticity is proven for the config plane and host binaries; ambient interpreter state (`/usr/lib` `_distutils_hack`, `~/.local/lib` site dir enumeration by `python3`) is host-dependent and not controlled by the gate.
- Scratch retained under `/tmp/rgr-mutants/` (`derived.sh`, `derived-two-blocks.sh`, `A.sh`, `B.sh`, `C.sh`, `tip-gate.sh`, `strace.log`, `st2.txt`, `st3.txt`, `baseline.sh`) and `/tmp/mado-verify-regression.BLkIpP/` (the SETUP workdir demonstrating the mid-wave mutation). My two kept fixture roots from failing worktree selftests (`/tmp/w5-mado-m52-selftest.pYHFHl`, `.0Ixe4N`) were removed by exact path; no other fixture root was touched.

## Installs

none.
