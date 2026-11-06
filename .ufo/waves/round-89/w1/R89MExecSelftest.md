# R89MExecSelftest — self-tests and guards of the round-89 instruments on draft bytes

Seat: R89MExecSelftest (leaf). Lane root: `/home/vgpnk/Projects/shokunin/mado-shokunin`.
Lane HEAD at run: `af998dcc41d48618ffe7afe0efc9354755a9244e` (clean for tracked files; only the expected
untracked round-89 files were present). Scratch root: `/fast/scratch/hyaku/mado-r89/R89MExecSelftest` (deleted on exit).
All runs below are DRAFT checks on pre-freeze bytes; no receipt was written under `receipts/`, and no draft run is
claimed as a measurement.

Instrument sha256 observed at run time (lane bytes):

```
de6dfd4f87901d0941836f5f09aa976d46ce5790255dd9619162125b4f2810b1  quality/counters/c1-r89-mako-regex.py
73bd520125b1c63f344776bac506d0fb3ec251261a168641e31c6716803fc0d0  quality/counters/c2-r89-survivor-kills.py
2720922b1b9206549bf20248a20c5b70d7dc445ab2d1815112a2cb524fce229e  .ufo/waves/round-89/build/mado-mako.c1.py
c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237  tools/mado-mako.py (round-88 tool, unchanged)
```

## 1. Selftests

Each ran under `python3 -I` with `TMPDIR` and `--scratch-root` pointing at a fresh subdirectory of the scratch
root. "scratch before/after" is `ls -A | wc -l` of that subdirectory.

| command | rc | last line | scratch before/after |
|---|---|---|---|
| `build/mado-mako.c1.py --selftest --scratch-root $S/st-mako` | 0 | `MADO_MAKO_SELFTEST: checks=58 failed=0` | 0/0 |
| `quality/counters/c1-r89-mako-regex.py --selftest --scratch-root $S/st-c1 --candidate-file <build/mado-mako.c1.py>` | 0 | `SELFTEST: passed=27/27` | 0/0 |
| `quality/counters/c2-r89-survivor-kills.py --selftest --scratch-root $S/st-c2` | 0 | `SELFTEST: passed=18/18` | 0/0 |
| `quality/counters/c2-r89-survivor-kills.py --selftest --scratch-root $S/st-c2tool --tool-file <build/mado-mako.c1.py>` | 0 | `SELFTEST: passed=18/18` | 0/0 |

Notes:
- The C1 selftest's `PASS the tool under selftest carries the libc matcher (pass --candidate-file before landing)` and
  `PASS each python-re forgery anchor occurs once in the working-tree tool` hold only with `--candidate-file`; without it
  the selftest reads the lane's `tools/mado-mako.py`, which is still the round-88 tool (correct pre-freeze). The L1's
  pre-landing run must pass `--candidate-file .ufo/waves/round-89/build/mado-mako.c1.py`.
- The 27-line C1 and 18-line C2 selftest transcripts are reproducible from the commands above; full logs were kept only
  in the (deleted) scratch. The check names cover the pin load, schema, carried set, all five predicate conjuncts,
  the four controls, the forgery anchors, N range, setup errors and "score()/evaluate leaves the scratch root empty".

## 2. Guards in a fixture git repo

Fixture: `D=$(mktemp -d -p $S)` → `/fast/scratch/hyaku/mado-r89/R89MExecSelftest/tmp.5zOK7qwZWy`.
`git -C "$D" init -q`; `git -C "$D" rev-parse --show-toplevel` printed exactly `$D` before any commit.
Two commits, identity supplied with `-c user.name=fixture -c user.email=fixture@invalid` on the commit only:

```
ed09326aa6d1d9e30e6dad76ca6ddc69e8f80369 fixture <fixture@invalid> fixture: C1 candidate as tools/mado-mako.py
b86a38e7f79d156769ae19c2934267158aebade1 fixture <fixture@invalid> fixture: round-89 instruments and pinned machinery
```

The fixture contains the lane `tools/mado-mako.py`, both new counters, the pinned round-88 counters
(`c1-r88-mako-fields.py`, `c2-r88-include-containment.py`), the round-87 counter they pin
(`c1-r87-mako-criteria.py`), and the round-87/88/89 controls files, all at the same relative paths. Every copied file
matched the lane byte-for-byte (`sha256sum` lane vs `git show HEAD:<path>`), except `tools/mado-mako.py` at HEAD, which
is the C1 candidate by design of commit 2.

### 2a. C2 end to end at the first fixture commit (DRAFT)

```
python3 -I "$D/quality/counters/c2-r89-survivor-kills.py" --repo "$D" --rev HEAD \
  --expect-survivors-sha256 9f25df3cac28d9085d2e7d2a89e6002df24f76e6c5264df98f83d4d32c8104f0 \
  --expect-c1side-sha256    c710a3e5a2a0e88692de68c6dec9815f14f5964099ec7ef6fdb8cb20bb743c1a \
  --expect-c2side-sha256    e02e2b4de83410ab16fcf7ad92f5374c5178a3e49c80d6aa2c4994e0d04e612e \
  --scratch-root "$S/c2-e2e"
```

rc 0, scratch 0 before / 0 after. Final line:

```
MADO_MAKO_SURVIVORS: TARGET_MET rev=HEAD cases=95 correct=95 counted=7 killed=7 do_nothing_B_only_killed=0 crash_only=RM6C2-cycle-detected-on-lexical-target tool_sha256=c374d71514f1559a12593b1097cd5e6ccc8ba2c225f2fa2b2d7764ef29192237
```

Supporting lines: `B=61+26 S=4+4 excluded_from_B=c53-summary-tilde-refused`, `tool_sha256=c374d715…`, all 95 case lines
`ok` (0 FAIL). The eight survivor rows: seven `killed` (each `killed_by_B_only=false counted=true`) and
`RM6C2-cycle-detected-on-lexical-target crashed-not-killed killed_by_B_only=false counted=false differs_on=s2-cycle-second-lexical-path crashed_on=s2-cycle-second-lexical-path`.

### 2b. Flipped expect sha → setup error

Same command with `--expect-c1side-sha256 0710a3e5…` (first nibble c→0). rc **2**, scratch 0 before / 0 after:

```
MADO_MAKO_SURVIVORS: SETUP_ERROR c1side set sha256 c710a3e5a2a0e88692de68c6dec9815f14f5964099ec7ef6fdb8cb20bb743c1a != expected 0710a3e5a2a0e88692de68c6dec9815f14f5964099ec7ef6fdb8cb20bb743c1a
```

### 2c. Corrupted pinned round-88 counter → exit 2 at import

A single `\n` was appended to `quality/counters/c1-r88-mako-fields.py` in `$D`'s working tree
(sha256 `063eab73…ab6a8b` vs pin `3678425a…e11cc1f`):

- C1 counter (`--selftest --candidate-file $D/tools/mado-mako.py`): rc **2**, scratch 0,
  `MADO_MAKO_REGEX: SETUP_ERROR round-88 counter sha256 063eab7399ed072ba4baa46cb9378e68b6e6c18a3dbde19a977059ae92ab6a8b != pinned 3678425addb5f661d3f284ef423e3566446b54714cb2148c5696a8cdfe11cc1f`
- C2 counter (`--selftest`): rc **2**, scratch 0,
  `MADO_MAKO_SURVIVORS: SETUP_ERROR c1-r88-mako-fields.py sha256 063eab73…ab6a8b != pinned 3678425a…e11cc1f`

Restored to the pin (`3678425a…e11cc1f`). Then the same newline was appended to
`quality/counters/c2-r88-include-containment.py` (`d89faa9f…13020d` vs pin `f8e18b7c…9e96767`): C2 counter rc **2**,
scratch 0, `MADO_MAKO_SURVIVORS: SETUP_ERROR c2-r88-include-containment.py sha256 d89faa9f…13020d != pinned f8e18b7c…9e96767`.
Restored to `f8e18b7c915fe831e6eaafcd09fad0af9ac23d89514317f131fb1ed409e96767`; `git -C "$D" status --porcelain` was empty
afterwards.

### 2d. C1 end to end on fixture bytes (DRAFT run, not a measurement)

Second fixture commit puts the candidate at `tools/mado-mako.py` (`2720922b…ce229e`); `HEAD~1` is the round-88 tool
(`c374d715…92237`).

```
python3 -I "$D/quality/counters/c1-r89-mako-regex.py" --repo "$D" --rev HEAD --base-rev HEAD~1 \
  --cases "$D/.ufo/waves/round-89/controls/mako-cases-r89.json" \
  --expect-cases-sha256     d04e27fccd7b4ffffa820872706c394eb59b96a46e792e0bbb2f30cfb2980431 \
  --expect-mutants-sha256   ed0476ff8aef53eb15dd91406a9cea5dc02c495b6b7e8c2865bec862b02d7c04 \
  --expect-r88-cases-sha256 a0e81b191fb0f80ca352699ede47962c1ac01c1ae8e9e15ccf50b1d7fab4a091 \
  --scratch-root "$S/c1-e2e"
```

rc 0, scratch 0 before / 0 after. Final line:

```
MADO_MAKO_REGEX: TARGET_MET rev=HEAD base_rev=HEAD~1 cases=91 correct=91 carried=61/61 mutants=32 killed=32 naive_correct=22 globals_include_correct=23 base_tool_correct=67 python_re_correct=81 score=10.0000 score_scope=finite-cases tool_sha256=2720922b1b9206549bf20248a20c5b70d7dc445ab2d1815112a2cb524fce229e cases_sha256=d04e27fccd7b4ffffa820872706c394eb59b96a46e792e0bbb2f30cfb2980431
```

All 91 case lines `ok`, 32/32 mutants `killed`, all four controls strictly below N=91. `git -C "$D" status --porcelain`
empty after the run.

## 3. Scratch-root discipline

Every run created its directories under `--scratch-root` and removed them; `ls -A` before/after was 0/0 for
`st-mako`, `st-c1`, `st-c2`, `st-c2tool`, `c2-e2e`, `c2-badsha`, `c1-e2e`; the guard runs left their scratch dirs empty
(`guard-c1-import` 0, `guard-c2-import` 0, `guard-c2-import2` 0). A separate check ran both counter selftests with
`TMPDIR` and `--scratch-root` pointing at two different fresh directories: rc 0 and both directories 0 entries after
(`TMPDIR` stayed empty; the counters' `tempfile.mkdtemp(dir=scratch_root)` calls in both counters and in the pinned
round-88 machinery are the only creation sites). The fixture worktree was byte-clean after all runs, and no lane file
under `tools/` or `quality/` was modified (`find … -newermt "2026-11-06 17:23"` empty; lane `tools/mado-mako.py` still
`c374d715…92237`).

## Result

- All four selftests pass with rc 0 (58/58, 27/27, 18/18, 18/18) and leave their scratch empty.
- C2 fixture end-to-end passes: `TARGET_MET cases=95 correct=95 counted=7 killed=7 do_nothing_B_only_killed=0`; every
  sha guard (three expect pins, both pinned round-88 counters) fails closed with rc 2 and a named `SETUP_ERROR`.
- C1 fixture end-to-end (DRAFT): `TARGET_MET cases=91 correct=91 carried=61/61 mutants=32 killed=32`, controls
  22/23/67/81 < 91, score 10.0000.
- No defects found in the instruments. No tool installs, no dead steps, nothing written outside the scratch root and
  this report; scratch deleted on exit.

Residual notes for the L1:
- The C1 counter has no default `--cases`; the freeze command must pass it explicitly (the r88/r89 sha pins are not
  self-locating). The fixture run used the fixture's own copy, byte-equal to the lane file.
- The fixture `tools/mado-mako.py` at HEAD intentionally differs from the lane (C1 candidate); the lane tool is
  unchanged at the round-88 sha, which is the state C2 must be measured at.
- The C1 e2e `tool_sha256` is the candidate sha because that is the fixture commit under test; a measurement at the
  freeze revision must show the candidate sha at the C1 rev and `c374d715…92237` at the C2 rev.
