# R100MMutPath - mutation probe of the C1 path-default branch (mado round 100, w1)

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`, base
`43309e6af9a3b57f1bc839a826bef1f8eb7495e4`. Seat: mutation tester, leaf member (no dispatch).
Contract read first: `.ufo/waves/round-100/claims-declaration-r100.md` (C1 frozen statement and
`PRED-C1-r100-v1`), `corpus/QUALITY.md` (rounds 90-99), `corpus/lessons/round-99.md`,
`corpus/lessons/round-99-verifier-spotcheck.md`, `SKILL.md` registry, `quality/harm-watch.py`.

## 1. Question this seat answers

Do the six assigned defects die on the round's new `path-default` case class at the frozen bytes -
and if any survives, which case shape is missing? The answer is a kill matrix, not a contract
change: a surviving mutant is a coverage finding routed to the L1.

## 2. Measured objects (re-hashed by this seat)

| object | bytes | sha256 / value |
|---|---|---|
| candidate (primary) | `.ufo/waves/round-100/build/mado-launchenv.py`, 981 lines | `3b29dc65111a2f3efdd5aa282f74493ff53eff840a1c88a92054f0df2e9fb228` |
| base tool | `tools/mado-launchenv.py`, 954 lines | `a63c20c886a2bd840d80966d531e055e9c4f5d3accb431e4b0e317e04523eb16` |
| sibling (unchanged, read by the candidate) | `tools/mado-execargv.py` | `49f7fecdc3bef99a077fe73ac12f5fe211d7ae8c41df5ddc949daf685405f713` |
| frozen cases | `.ufo/waves/round-100/controls/launchenv-cases-r100.json` | `7aba8a0f880b3e59edf7a731f2d2783babea7b275d280588ba2df2c5dd6df4a9` |
| | 77 cases / 35 classes; 10 new (8 with `path` null or `[]`); the first 67 case objects parse equal to the r99 file (67/67 by this seat's comparison) | envelope: `round=r100`, `oracle_sha256=renderer_sha256=cbfff7a4...`, `gio_sha256=d2164260...`, glib2 2.90.1-1 |
| prior cases (blind-spot control) | `.ufo/waves/round-99/controls/launchenv-cases-r99.json` | `14b4cc571a35bb5b4c6996a4a3fde19ff71ce9f26dabe3dd4142eec162f82acd` (67/31) |
| oracle (only renderer) | `.ufo/waves/round-99/controls/launchenv-probe-r99.py` | `cbfff7a4b64e63f3e6861d29d1c5639de2c25abe2f6875088918abb45d129199` |
| gio | `/usr/bin/gio` | `d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462`; glib2 `2.90.1-1`; `gio --version` prints `2.90.1` |
| scratch shapes suite | `suite-shapes-measured.json` (seat scratch) | `491ff2ba0ea33ca057e94cf4cab0e8113ed67cce32c2b9b5e0e7c5d3bbfe2265` |

The build candidate differs from the base tool on 29 lines, **all inside the selftest body**
(`def selftest(` at byte 20214, `def main(` at 44861); the production path is identical, so every
behavioural result below holds for both byte strings (both were run on the frozen set).

## 3. Detector (instrument, not candidate)

The candidate is a model, so the detector is the round-99 counter's case leg, reproduced with the
oracle's own materialiser (importlib, sha-pinned): build the case root with
`build_root`/`path_string`; run

```
python3 -I <private candidate copy> <desktop-arg> <args...> [--path PSTR] --json
```

with `cwd` = case root and `env = {LC_ALL:"C", HOME:<root>/h}` (plus `PATH=""` when `--path` is
passed). **Contract correction:** a `"path": null` case runs the child with **no `PATH` key** and no
`--path` (contract 2's letter). The round-99 leg's `PATH=""` env does not model unset - measured on
a built root with the same bytes: `PATH` absent answers `{root}/./probe`, `PATH=""` answers
`{root}/probe`, and the frozen expect is `{root}/./probe`. A counter that reuses that env cannot
score the new class green (finding F1).

Comparison: `launches`, `argv` as a sorted multiset, `cwd`, `env.GIO_LAUNCHED_DESKTOP_FILE` exact;
a refusal needs rc 2 and the exact cause (`detail` ignored). A kill is a parsed wrong answer on a
case the pristine candidate answered correctly; a crash, timeout or unparsable output is never a
kill.

## 4. Baseline (pristine bytes)

| set | build `3b29dc65` | base `a63c20c8` |
|---|---|---|
| r100 frozen (77) | 77/77 ok, 0 crash | 77/77 ok, 0 crash |
| r99 (67) | 67/67 ok | 67/67 ok |
| scratch shapes (6) | 6/6 ok | 6/6 ok |
| union r99+shapes (73) | 73/73 ok | 73/73 ok |
| restored rerun after the sweep (77) | 77/77 ok, sha unchanged | - |

## 5. Mutants and the kill matrix

Each `find` occurs exactly once in the candidate; each mutant was written to a private copy under
`$HYAKU_SCRATCH/mado-r100/R100MMutPath`, compile-checked (`compile()`), then scored over the whole
frozen set. Mutant copy sha256 (first 16 hex, frozen-set run): m1 `8fd41a7e5beb419c`, m2
`daf6389b08633879`, m3 `7dc62446cd344674`, m4 `eea09070097e8934`, m5 `049a4767ac02227b`, m6
`1f96ea7efbb288ec`.

| mutant | mutation | expected detector | cases failed (frozen r100 set) | first-kill output | verdict |
|---|---|---|---|---|---|
| m1 | `DEFAULT_SEARCH_PATH = '/bin:/usr/bin'` (trailing `.` dropped) | the dot entry's argv[0] shape | `pd-dot-root` | rc 2 `ERROR load`; expect launches=1 argv[0]=`<root>/./probe` | **KILLED** |
| m2 | unset branch yields `''` (candidate form `path = ''`; same behaviour as a helper `return ''`) | unset vs empty separation | `pd-dot-root`, `pd-sysbin-unset` | argv[0]=`<root>/probe`; expect `<root>/./probe` (first) | **KILLED** |
| m3 | early working-directory join removed | `Path=`-relative find | `tx-viawd`, `pd-wd-unset` | rc 2 `ERROR load`; expect launches=1 argv[0]=`<root>/work/bin/probe` | **KILLED** |
| m4 | empty PATH entry treated as `/bin/`+program | empty-entry rule | `pe-empty-str`, `pd-empty-root`, `pd-sysbin-empty` | rc 2 `ERROR load`; expect launches=1 argv[0]=`<root>/probe` | **KILLED** |
| m5 | IS_DIR half of the executable test dropped | directory named as the program | `pd-abs`, `pd-onpath` | rc 2 `ERROR program-not-found`; expect rc 2 `ERROR load` | **KILLED** |
| m6 | relative hit returned via `os.path.normpath` | `{root}/./probe` keeps the `./` | `pe-dot`, `pd-dot-root` | argv[0]=`<root>/probe`; expect `<root>/./probe` | **KILLED** |

`crashed_not_killed = 0` for every mutant. **Killed 6 / counted 6 on the frozen r100 set.**
New-class attribution: m1 (1 case), m2 (2), m3 (1), m4 (2), m6 (1); m5 is killed only by the
pre-existing `prog-dir` cases. The build candidate and the base tool produce row-identical kills.

## 6. Surviving-mutant list and the gap it proved

**On the r99 set alone: m1 SURVIVED, m2 SURVIVED** (0 wrong answers each). That is the round's
declared blind spot: both r99 `path-unset` cases carry an absolute `Exec` and return at
`gutils.c:331-357` before the PATH source is read at `:370`. m3/m4/m5/m6 were killed there
(`tx-viawd`, `pe-empty-str`, `pd-abs`+`pd-onpath`, `pe-dot`).

Gap proof, built in scratch before the frozen file existed: case `dash-unset-root` (PATH absent,
`Exec=probe`, program at the case root, no `Path=`) was measured with the oracle twice, agreeing:
`launches=1 argv[0]={root}/./probe`. With that case, **m1 answers `ERROR load` and m2 answers
`<root>/probe`; both are killed**. Five further measured shapes (all case-private programs, no host
binary) are in the ledger; the frozen file's `pd-dot-root`/`pd-empty-root`,
`pd-private-unset`/`pd-private-onpath` and `pd-sysbin-unset`/`pd-sysbin-empty` are the same pairs.

**On the frozen r100 set: no survivor among the six.**

## 7. Findings routed (no contract change proposed)

1. **Counter env (F1).** A `path:null` case must be scored with no `PATH` key in the child env
   (and no `--path`). Demonstrated: same candidate bytes answer `{root}/./probe` with PATH absent
   and `{root}/probe` with `PATH=""`; the frozen expect is `{root}/./probe`. Routed to the C1
   counter owner; a leg that inherits the r99 env scores the new class wrong.
2. **The `/usr/bin`-only arm of clause 1 is not `Exec`-observable (F2).** A spawned `/bin` or
   `/usr/bin` program writes no probe record, and `Terminal=true` + PATH absent would start a real
   terminal - `/usr/bin/xdg-terminal-exec` exists on this host. The frozen file's `TryExec=sh` +
   absolute `Exec={root}/probe.sh` shape is the safe encoding: load-only, never exec'd, and it
   kills m2 at `pd-sysbin-unset`, so the separation is causal rather than textual.
3. **m5 is carried by the old cases (F3).** The new class alone does not exercise the `IS_DIR`
   half; `pd-abs`/`pd-onpath` do. The frozen file is the whole set, so the kill holds, but an
   audit of "the new class" alone would miss m5.
4. **m6's "or the reverse" reading is not the oracle (F4).** Two oracle runs measure the `./`
   preserved (`{root}/./probe`); a normalising candidate is the wrong direction.
5. **The cwd pair is non-separating for unset-vs-empty but load-bearing for the join (F5).** At
   `pd-wd-unset`/`pd-wd-empty` both PATH states launch `{root}/work/probe` (the empty entry is
   joined to the working dir exactly like `.`), yet `pd-wd-unset` kills m3, so the pair earns its
   row as a control of the working-dir join.

## 8. Restoration evidence

The lane was never written by this seat. Every mutant ran from a private copy; the candidate
sha256 before == after every run: build `3b29dc65...` (all runs), base `a63c20c8...` (all runs).
After the sweep, a fresh copy of the lane bytes answered 77/77 and re-hashed to `3b29dc65...`. The
scratch tree `/fast/scratch/hyaku/mado-r100/R100MMutPath` is removed before this seat yields; the
lane writes are this report and the findings ledger
`.ufo/waves/round-100/controls/launchenv-mutants-r100-probe.txt`.

## 9. Limits

- The kill leg is the seat's reproduction of the counter's case leg over the frozen bytes; the C1
  counter re-scores the same set with its own comparator, and a divergence would show up as a
  counter MISMATCH, not here.
- The six mutations are the seat item's list, not a population freeze; the frozen mutant file
  (`controls/launchenv-mutants-r100.json`) is another seat's artifact. Anchors are pinned to
  `3b29dc65`; a later edit that moves a line makes a `find` miss, which this harness reports as
  `NOT-APPLIED`/`find_occurrences != 1`, never a silent pass.
- The oracle was executed only through its own case env (`LC_ALL`/`HOME`/`PROBE_OUT` plus the
  case's PATH entries or no PATH); no host application and no terminal was launched by this seat.
- Host load ~250 on 32 cores; each matrix run is wall 3-11 s because the candidate leg is cheap and
  the oracle was used only to measure the six scratch shapes (37 s for 12 gio runs, twice each).

## 10. Tooling

No tool was installed or upgraded; no pacman transaction, no sudo, no host-service change, no
host write outside the seat's scratch. Instruments: `/usr/bin/python3` (stdlib only), the r99
oracle (spawns `/usr/bin/gio`), and this seat's `mutate.py` (spawns `python3 -I` on candidate
copies). The candidate itself spawns nothing.
