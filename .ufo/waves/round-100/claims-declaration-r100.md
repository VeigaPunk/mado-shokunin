# mado round 100 — claim declaration (frozen contract) and the wave's build targets

Lane `/home/vgpnk/Projects/shokunin/mado-shokunin`, branch `master`, base
`43309e6af9a3b57f1bc839a826bef1f8eb7495e4`. L1 `MadoR100`. Round shape: ONE v1 wave `w1`
(band 8–16). This declaration is the contract the wave builds for and attacks. **The predicate
sentences below are frozen before any case is scored**; a wave artifact may narrow them (pre-file
falsification rule, addendum §8) and every narrowing is recorded in `plans/round-100.md`.

## C1 — coverage: the PATH-unset default search path of the launch load gate

**Frozen statement.** At the base revision `43309e6a`, the PATH-unset default search path of
`g_find_program_for_path` (`gutils.c:370-382`: the literal `/bin:/usr/bin:.`, used when the
`PATH` variable is absent from the environment) is modelled by `tools/mado-launchenv.py`
(`DEFAULT_SEARCH_PATH`) and exercised by **zero** frozen cases: both `path-unset` cases in
`.ufo/waves/round-99/controls/launchenv-cases-r99.json` carry an **absolute** `Exec`, which
returns at `gutils.c:331-357` before the PATH source is read at `gutils.c:370`. After this round
the frozen case file `.ufo/waves/round-100/controls/launchenv-cases-r100.json` carries a
`path-default` class of **≥6** cases, every label measured against the installed `/usr/bin/gio`
(`sha256 d2164260…cfc462`, glib2 2.90.1-1) and re-measured twice with agreeing results, and
`tools/mado-launchenv.py` answers **every** case of that set (the whole set, not only the new
class) in agreement with the oracle, including a seeded fresh leg and a counted mutant population.

The class must separate the unset default from all three neighbouring behaviours, or the branch is
not cored:

1. **unset ≠ empty.** With `PATH=""` (an empty variable) the walk is the single empty entry (cwd);
   with `PATH` absent it is `/bin:/usr/bin:.`, so a program that exists only in `/usr/bin` is
   reachable in the second case and not in the first.
2. **unset ≠ the ambient search.** A program that exists only in a case-private bin directory is
   **not** found when `PATH` is unset (the default does not know that directory), while the same
   fixture with `PATH` set to that directory finds it.
3. **the default's trailing `.` is real.** A bare program present only in the launch working
   directory is found with `PATH` unset, and is not found by the same fixture under `PATH=""` when
   the working directory differs from the process cwd.

**Predicate `PRED-C1-r100-v1`** (identical sentence in the plan, the counter's code and the
receipt):

```
TARGET_MET iff  default_cases            >= 6
           AND  default_classes          >= 3
           AND  cases_correct            == cases_total
           AND  fresh_correct            == fresh_total        (fresh_total >= 8, seeded at measurement)
           AND  mutants_killed           == mutants_counted    (mutants_counted >= 4)
           AND  base_set_default_cases   == 0                  (the do-nothing control, measured on the r99 case file)
           AND  control_unset_as_empty_correct < cases_total   (the misreading the branch guards against)
```

rc 0 TARGET_MET · 1 TARGET_MISSED · 2 SETUP_ERROR. No other conjunct, and no conjunct may be added
after a case is scored.

**Counting command** (substituted at measurement; `--rev worktree` for an uncommitted candidate):

```
python3 -I quality/counters/c1-r100-launchenv-path.py --repo . --rev <MEASURED_REV> \
  --base-rev 43309e6af9a3b57f1bc839a826bef1f8eb7495e4 \
  --cases .ufo/waves/round-100/controls/launchenv-cases-r100.json --expect-cases-sha256 <PIN> \
  --mutants .ufo/waves/round-100/controls/launchenv-mutants-r100.json --expect-mutants-sha256 <PIN> \
  --genseed .ufo/waves/round-100/controls/launchenv-fresh-r100.py --expect-genseed-sha256 <PIN> \
  --expect-tool-sha256 <PIN> --expect-execargv-sha256 <PIN> --expect-gio-sha256 d216426080f847bfccdc7c735a4f349dc74f524530a19e8b1c32d04270cfc462 \
  --scratch-root <DIR>
```

**Sourced claim:** S533 (`gutils.c`, opened and quoted again this round).

## C2 — operability: the harm watch's per-leg cap becomes measured and the panel goes green

**Frozen statement.** At the base revision `43309e6a`, the frozen 28-leg harm panel
(`.ufo/waves/round-99/controls/harm-panel-r99.json`) carries `timeout_s: 600` with no per-leg
timing and no headroom, and on this host two legs (`r92_gate_defects`, `r97c1_filetype`) exceed
that cap, so the panel reports `mismatches=2` (round 99's C2 honest stop; receipt
`.ufo/waves/round-99/receipts/c2-measured-r99.txt`). After this round `quality/harm-watch.py`
reports each leg's measured elapsed milliseconds (`LEG <id> rc=… … elapsed_ms=<n>` on the human
line and an `elapsed_ms` field per leg in `--json`), the frozen panel
`.ufo/waves/round-100/controls/harm-panel-r100.json` carries `timeout_s` equal to at least twice
the largest per-leg elapsed measured on this host at committed bytes (timing receipt
`.ufo/waves/round-100/receipts/panel-timing-r100.txt`, all 28 legs timed), and a full-panel run at
committed bytes reports `HARM_WATCH: legs=28 … mismatch=0`.

**Predicate `PRED-C2-r100-v1`:**

```
TARGET_MET iff  panel_legs == 28 AND legs_run == 28 AND mismatches == 0
           AND  gate_elapsed_emitted   == 1     (human LEG line carries elapsed_ms= AND json legs carry elapsed_ms)
           AND  timing_legs_timed      == 28
           AND  max_elapsed_ms         > 600000 (the frozen 600 s cap is structurally too small on this host: the control is measured, not asserted)
           AND  panel_timeout_s * 1000 >= 2 * max_elapsed_ms
           AND  control_600s_would_mismatch >= 1 (derived from the same timing receipt: legs whose elapsed exceeds 600 s)
           AND  selftest_failed        == 0
```

**Counting command:**

```
python3 -I quality/counters/c2-r100-harm-watch.py --repo . --rev <MEASURED_REV> \
  --base-rev 43309e6af9a3b57f1bc839a826bef1f8eb7495e4 \
  --panel .ufo/waves/round-100/controls/harm-panel-r100.json --expect-panel-sha256 <PIN> \
  --timing .ufo/waves/round-100/receipts/panel-timing-r100.txt --expect-timing-sha256 <PIN> \
  --expect-gate-sha256 <PIN> --scratch-root <DIR>
```

## Harm watch

The C2 counting command **is** the round's full-panel watch (28 legs, per the round-99 panel,
unchanged leg set, re-frozen cap). No axis is harmed by the gate change: the round-99 counter
(`quality/counters/c2-r99-harm-watch.py`) reads its gate bytes from `--rev`, so it still runs
against `3b69f041` and its pinned bytes are untouched.

## Shared contract 1 — the C1 candidate's CLI (unchanged from round 99)

```
mado-launchenv.py DESKTOP [FILE...] [--path PATH] [--json]
mado-launchenv.py --selftest
```

Output `MADO_LAUNCHENV: launches=N terminal=<name|-> cwd=<escaped|-|>` then per launch
`LAUNCH k: argc=M terminal=…`, `ARGV[k][i]=…`, `ENV[k] GIO_LAUNCHED_DESKTOP_FILE=…`; exit 0 ok,
2 on a refusal with `MADO_LAUNCHENV: ERROR <cause> detail=<…>`; `--selftest` prints
`MADO_LAUNCHENV_SELFTEST: checks=N failed=M`. `--path` models the launching process's PATH;
**no `--path` and no `PATH` in the model process's environment = PATH unset** →
`/bin:/usr/bin:.`; `--path ""` = set-but-empty → one empty entry (cwd).

## Shared contract 2 — the C1 oracle and the round-100 case file

The round-99 oracle `.ufo/waves/round-99/controls/launchenv-probe-r99.py` (sha256
`cbfff7a4b64e63f3e6861d29d1c5639de2c25abe2f6875088918abb45d129199`, measured 2026-11-08) is the
only renderer: a case is
`{"id","class","path":[…]|null,"files":{rel:b64},"dirs":[…],"desktop":{…},"args":[…],
"expect":{…}}`; `path: null` means **PATH is absent from the child environment** (the oracle must
launch with `env -i` and no PATH for that case — verify the oracle does this before trusting a
label; if it does not, the case class is `SETUP_ERROR`, never a green). Labels are measured twice,
and a differing label is a refusal.

## Shared contract 3 — the C2 gate and the re-frozen panel

`quality/harm-watch.py`: add `elapsed_ms` (monotonic, integer) to each leg record and to the human
`LEG` line; keep every existing output field, exit map and census finding byte-compatible; add
selftest checks for the elapsed field (present, non-negative, integer, and monotone across a
fixture whose second leg is slower). The panel gains `timeout_s` only — the 28 leg rows, their
`expect_rc`, `expect_marker` and `note` stay byte-identical to the round-99 panel.

## Wave plan (w1)

15 seats: 2 scouts, 5 executors, 1 scribe, 2 reviewers, 1 critic, 2 mutation-testers, 1 connector,
1 labrat. Attack roles (reviewer, critic, mutation-tester, labrat) 6/15 = 40 %.
