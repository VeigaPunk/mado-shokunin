# R100MMutHarm - C2 mutation matrix (gate and counter)

Seat R100MMutHarm (mutation-tester), round 100, wave w1, 2026-11-08.
Lane `mado-shokunin`, base revision `43309e6af9a3b57f1bc839a826bef1f8eb7495e4`.

Anchors (re-hashed before the first detector and after the last; unchanged):

- gate candidate `build/harm-watch.py` sha256
  `2d604f7b654f2e2710b612358fedf81fc028dddd47fd0934d9f82c065b226167`
  (mtime 2026-11-08 02:09:48 -0300);
- counter candidate `build/c2-r100-harm-watch.py` sha256
  `e4741843278efaf6715b70246dbe82a6c92852bffd14de97a672ef78182ac253`
  (mtime 2026-11-08 02:09:51 -0300).

Both stayed read-only inputs. No lane file was opened for write, no mutating git/jj command was
run, nothing was committed, no tool was installed. Mutants exist only as private scratch copies;
each exercised copy was re-derived from the pristine bytes plus its declared replacement and
compared byte-for-byte (10/10 exact).

## 1. Detectors

Three detectors per mutant, all under an env of `PATH=/usr/bin:/bin`, `LC_ALL=C`, and
`HOME`/`TMPDIR` inside the scratch tree; no host application or terminal is launched.

1. **Selftest.** The mutated component's own `--selftest`:
   `python3 -I <copy> --selftest`. Killed when the run is not identical to pristine in exit code,
   `HARM_WATCH_SELFTEST: checks=N failed=M` / `MADO_C2_R100_SELFTEST: checks=N failed=M`, or the
   `FAIL` lines. For counter mutants this is the counter's selftest (the analogous self-instrument;
   the gate is unmodified).
2. **Counter governed run.** The landed counter over a bounded replica of its real input shape:
   a 28-row stub panel (`expect_legs` 28, every leg exits 0) and a synthetic 28-line timing
   receipt in the declared format with one `elapsed_ms=700000` leg and `TIMING-DONE`. All pins
   (gate, panel, timing) are recomputed for the exercised bytes and passed, so the run tests
   enforcement rather than a stale pin. The counter's `--gate PATH` draft mode is used; the
   panel/timing bytes are read from the working tree. A tight-cap control
   (`timeout_s` 1000 against `2*700000`) is run too: pristine answers `TARGET_MISSED
   missed=timeout_ge_2max`.
3. **Panel run.** The mutated gate run over a 3-leg timing fixture (fast `python3 -c`; slow
   `sleep 0.15`; timeout `sleep 5`, run with `--timeout 1`), with `--json`, plus a duplicate-id
   panel (two rows sharing one id) and the frozen 28-row panel's census. This detector is a
   *verdict* detector: killed only when rc, the `HARM_WATCH:` summary or a `PANEL` census line
   differs from pristine. Printed `elapsed_ms` values that no detector asserts are recorded as
   observed but do not count as a kill.

A killed mutant is a well-formed difference from pristine on that detector; a crash is never
credited. Baseline (pristine, measured):

```
HARM_WATCH_SELFTEST: checks=33 failed=0
MADO_C2_R100_SELFTEST: checks=20 failed=0
MADO_C2_R100: TARGET_MET   ... panel_timeout_s=1500 control_600s_would_mismatch=1
                            selftest_failed=0 selftest=checks=20 failed=0
MADO_C2_R100: TARGET_MISSED ... panel_timeout_s=1000 missed=timeout_ge_2max
panel fixture: fast elapsed_ms=14, slow=171, timeout=1004; rc 0, mismatch=0
duplicate fixture: rc 2, PANEL PANEL_DUPLICATE id=dup
```

## 2. Matrix (selftest / counter / panel)

| mutant | mutation (file:line) | selftest | counter governed run | panel run |
|---|---|---|---|---|
| h1 | gate:226 `elapsed_ms = 0` | KILLED: 33 checks, failed=2 (`timeout-elapsed-ms`, `elapsed-monotone`) | KILLED: `TARGET_MISSED missed=selftest_failed_0` | SURVIVED: rc 0, `legs=3 ok=3 mismatch=0`; elapsed 0/0/0 printed, never asserted |
| h2 | gate:190 + :226 wall clock (`time.time()`), `max(0,...)` clamp dropped | SURVIVED: 33 checks, failed=0 | SURVIVED: `TARGET_MET` (all conjuncts met) | SURVIVED: 12/166/1003 ms, rc 0, green |
| h3 | gate:226 timeout path returns `None` | KILLED: failed=1 (`timeout-elapsed-ms` on `elapsed_ms=None`) | KILLED: `TARGET_MISSED missed=selftest_failed_0` | SURVIVED: green; timeout leg prints `elapsed_ms=None` |
| h4 | gate:322 `elapsed_ms` removed from json leg objects | KILLED: failed=3 (`json-elapsed-ms`, `elapsed-monotone` KeyError, `elapsed-human-line` KeyError) | KILLED: `TARGET_MISSED missed=gate_elapsed_emitted_1,selftest_failed_0` | SURVIVED: green; human line keeps elapsed, json legs carry no field |
| h5 | counter:548 `"timeout_ge_2max": True` | KILLED by counter selftest: failed=1 (`short-cap-missed`; output shows `panel_timeout_s=1000` + `TARGET_MET`) | SURVIVED: `TARGET_MET` on the real-shape inputs; only the tight control flips `TARGET_MISSED -> TARGET_MET` | N/A (gate unmodified) |
| h6 | counter:507 `control_600s_would_mismatch = 1` | KILLED by counter selftest: failed=1 (`low-max-missed`: `max_elapsed_ms=500000` with `control_600s_would_mismatch=1`, expected 0) | SURVIVED: `TARGET_MET`; the true control is already 1 on every receipt with `max>600000` | N/A (gate unmodified) |
| h7 | gate:116 `PANEL_DUPLICATE` append replaced by `pass` | KILLED: failed=1 (`duplicate-id: []`) | KILLED: `TARGET_MISSED missed=selftest_failed_0` | SURVIVED on the frozen panel (its census is clean); a bespoke duplicate panel flips rc 2 -> 0 |

Supplemental probes (not assigned; they sharpen the h2/h3 class):

| probe | mutation | selftest | counter | panel |
|---|---|---|---|---|
| h2b | gate:226 `elapsed_ms = -1` (a concrete backward step outcome) | KILLED: failed=6 | KILLED: `missed=gate_elapsed_emitted_1,selftest_failed_0` | SURVIVED: green; -1 printed |
| h3b | gate:226 timeout leg reports `elapsed_ms=10` (a 1 s timeout under-reported 100x) | SURVIVED: 33 checks, failed=0 | SURVIVED: `TARGET_MET`, `gate_elapsed_emitted=1` | SURVIVED: green, `timeout ... elapsed_ms=10` |
| h1b | gate:226 `elapsed_ms = 1` constant | KILLED: failed=1 (`elapsed-monotone {'fast': 1, 'slower': 1}`) | KILLED: `missed=selftest_failed_0` | SURVIVED: green, 1/1/1 |

**Mutants no lane instrument can see: h2 (assigned) and h3b (supplemental).** Both survive the
gate selftest, the counter's governed run and the panel run. h3b is the stronger of the two: the
value is printed, plausible and wrong, and nothing in the round's instrument chain compares a
timeout leg's elapsed to its timeout. (The counter's own selftest cannot close this: it exercises
a fixture gate, never the candidate gate, so it is gate-independent by construction.)

## 3. Evidence per mutant

h1 (`elapsed_ms = 0`). The gate selftest reports:
`FAIL timeout-elapsed-ms: LEG slow rc=124 expect=0 marker=MISS rc-and-marker-mismatch+timeout-after-1s elapsed_ms=0`
and `FAIL elapsed-monotone: {'fast': 0, 'slower': 0}`. The counter run answers `TARGET_MISSED
... selftest_failed=2 ... missed=selftest_failed_0`; `gate_elapsed_emitted` stays 1. The bounded
panel is green with `elapsed_ms=0` on all three legs. So h1 is caught only through the gate's own
selftest; the counter's field check (presence + integer) accepts a constant 0.

h2 (`t0 = time.time()`, clamp dropped). Everything is green: `HARM_WATCH_SELFTEST: checks=33
failed=0`; panel `fast 12, slow 166, timeout 1003`; counter `TARGET_MET` with
`selftest_failed=0`. A wall clock advances normally, so the monotone and non-negativity checks
pass. This is not an equivalent mutant: a backward clock step yields a negative elapsed, which
the contract forbids, and no lane instrument can induce or observe the step. The selftest checks
the *value*, never the clock source.

h3 (timeout -> `None`). `FAIL timeout-elapsed-ms: LEG slow ... elapsed_ms=None`; counter
`TARGET_MISSED ... selftest_failed=1 ... missed=selftest_failed_0`. The counter's own
`elapsed_emitted` is 1 on its 28-fast-leg run because that run has no timeout; the timeout check
lives only in the gate selftest. Panel green with `elapsed_ms=None` on the timeout leg.

h4 (json leg objects lose the field). Gate selftest failed=3 (`json-elapsed-ms`, and both
monotone/human checks die on a `KeyError('elapsed_ms')` while building the id->elapsed map). The
counter is hit from both sides: `missed=gate_elapsed_emitted_1,selftest_failed_0`. Human lines are
unchanged.

h5 (cap conjunct replaced by `True`). Counter selftest:
`FAIL short-cap-missed: ... panel_timeout_s=1000 ...` (the mutant answers `TARGET_MET` where the
control expects `TARGET_MISSED`). The governed run on the green-shape inputs is `TARGET_MET` for
both pristine and mutant; only a battery containing the tight-cap control sees it. Note the
counter's selftest failing does not by itself change the governed verdict (see F4).

h6 (control forced to 1). Counter selftest:
`FAIL low-max-missed: ... max_elapsed_ms=500000 ... control_600s_would_mismatch=1 ...`.
On every other input the reported value is already 1 (see F3), so the governed run is unchanged.

h7 (duplicate finding dropped). Gate selftest `FAIL duplicate-id: []`; counter
`TARGET_MISSED ... selftest_failed=1 ... missed=selftest_failed_0`. The frozen panel's census is
clean under both gates, so the panel run cannot see it; the bespoke duplicate panel flips from
rc 2 + `PANEL PANEL_DUPLICATE id=dup` to rc 0 + `HARM_WATCH: legs=2 ok=2 mismatch=0`.

h2b (`elapsed_ms = -1`). The concretely negative value is caught: gate selftest failed=6 (both
clean checks, the integer check and the timeout check), counter `gate_elapsed_emitted=0
missed=gate_elapsed_emitted_1,selftest_failed_0`. This isolates the h2 hole: instruments catch a
negative *number*, not the wall-clock *source*.

h3b (timeout leg reports 10 ms). Gate selftest 33/0, counter `TARGET_MET` with
`gate_elapsed_emitted=1`, panel
`LEG timeout rc=124 expect=124 marker=ok timeout-after-1s elapsed_ms=10`.
The gate's check is
`"elapsed_ms=1" in out or re.search(r"elapsed_ms=\d{2,}", out) ... >= 1000`; the substring
`elapsed_ms=1` occurs inside `elapsed_ms=10`, so the first disjunct satisfies the check before the
1000 ms bound is examined. The counter's `elapsed_emitted` only requires `elapsed_ms=(\d+)` and a
JSON integer, with no comparison to `timeout_s`.

h1b (constant 1 ms). The monotone check is the only one that fires:
`FAIL elapsed-monotone: {'fast': 1, 'slower': 1}`; counter follows via `selftest_failed_0`.

## 4. Findings

**F1 (assigned survivor, headline).** The monotonic requirement is stated in the contract and
implemented (`time.monotonic()`), but no instrument pins it. h2 replaces it with a wall clock and
survives the gate selftest, the counter and the panel unchanged. Since `time.time()` can step
backwards (and the clamp was removed), the mutant can emit a negative `elapsed_ms` in production
and the contract's "monotonic, integer, >= 0" clause is violated. The gate selftest measures only
values in a normal run; a monotone clock and a wall clock are observationally identical when the
clock does not step. A detector for this needs a source-level pin (the only clock call in
`run_leg` is `time.monotonic`) or a controlled clock; neither exists in the wave. This is the
round's assigned mutation that no lane instrument can see.

**F2 (stronger adjacent survivor).** The timeout lower bound the gate executor claims
("timeout legs report `elapsed_ms >= timeout*1000` by construction") is not enforced by the gate's
selftest: the `timeout-elapsed-ms` record starts with `"elapsed_ms=1" in out`, which is a
substring of any 10-1999 ms value, so the `>= timeout*1000` branch is short-circuited for exactly
the values a regression would produce. h3b reports 10 ms for a 1 s timeout and passes the gate
selftest (33/0), the counter (`gate_elapsed_emitted=1`, `TARGET_MET`) and the panel. The counter
could not catch it either: `elapsed_emitted` has no lower bound, and the timing receipt is a
separate input from the gate's printed elapsed. Suggested repair (for the owner, not applied by
this seat): capture the timeout leg's `elapsed_ms` with a regex and assert `>= int(timeout*1000)`
without the substring disjunct, and make the counter compare the timed-out leg's printed elapsed
to `timeout_s*1000`.

**F3 (predicate redundancy).** The counter derives `max_elapsed_ms = max(ms)` and
`control_600s_would_mismatch = count(ms > 600000)` from the same parsed list, so
`max_elapsed_ms > 600000` iff `control_600s_would_mismatch >= 1` for every possible receipt. The
frozen predicate's control conjunct cannot fail independently of the max conjunct; it is a
sentinel, not a control. h6 is therefore unobservable as a verdict change on any input; only the
counter selftest's textual assertion on the low-max fixture (`control_600s_would_mismatch=0`)
kills it. The L1 should record that the seventh conjunct adds no discrimination (the frozen
sentence is not widened by this note; it is a measured property of its derivation).

**F4 (the counter's own selftest is not a conjunct).** The predicate's `selftest_failed == 0` is
the *gate's* selftest (the counter runs it). The counter's own `MADO_C2_R100_SELFTEST: checks=20`
is run and reported, but it is not part of `conds`. Measured: the h5 and h6 mutant counters print
`TARGET_MET` with `selftest=checks=20 failed=1` in the same line. A counter defect visible only to
its own selftest therefore leaves the governed verdict green; the wave's integration gate must run
`--selftest` separately and treat `failed>0` as a stop. This is the r99 F3 class in its remaining
half: the counter now runs the gate's selftest (that half is closed), but its own selftest is
still outside the verdict.

**F5 (panel column is uniformly survived).** None of h1-h7 changes the panel's rc or
`legs/ok/mismatch` tuple; the panel is a verdict instrument and the elapsed contract is enforced
only by the gate selftest and the counter's field checks. The counter's `gate_elapsed_emitted` is
computed from the panel run's output, so the panel supplies the evidence, but the assertion lives
in the counter. A full 28-leg replay would not add discrimination for these mutants; it is the
timing receipt, not the panel verdict, that carries the cap.

**F6 (r99 F3 closed; h7 remains selftest-dependent).** The r100 counter runs the gate's
`--selftest` (`selftest_failed` conjunct) and every gate mutation that breaks the selftest is
TARGET_MISSED with `missed=selftest_failed_0`. But the counter has no planted census control (no
duplicate / dropped-leg / extra-leg plants in its governed run), so h7, h1 and h3 are seen only
through the gate selftest. If that selftest is weakened, the counter's own field checks cannot
recover them. h7 is the concrete case: the frozen panel is clean, and only the selftest carries
the duplicate-id fixture.

**F7 (h1's zero passes the counter's field check).** `elapsed_emitted` requires presence and an
integer, so `elapsed_ms=0` on every leg is a valid emission; only the monotone fixture kills h1.
A future gate whose monotone fixture is slower than a floor (for example 0 ms legs under a
clamped timer) would let a constant through. This is the dependency behind F2.

## 5. Reproduction

Scratch harness (deleted before yield): `mkfix.py` builds the fixtures, `runmut.py` applies one
declared replacement to a copy and runs the three detectors, `mutants.json` holds h1-h7,
`mutants-supp.json` holds h2b/h3b/h1b. The essential commands:

```
# gate selftest on a mutant copy
python3 -I mut/h2-elapsed-wallclock.py --selftest

# counter governed run (draft mode; pins recomputed for the exercised bytes)
python3 -I mut/h5-counter-cap-dropped.py \
  --repo <scratch> --rev worktree --base-rev 43309e6af9a3b57f1bc839a826bef1f8eb7495e4 \
  --panel fix/panel-28-tight.json --expect-panel-sha256 <sha> \
  --timing fix/timing-good.txt --expect-timing-sha256 <sha> \
  --gate <gate copy> --expect-gate-sha256 <sha> --scratch-root <scratch>/scr

# panel run (verdict detector)
python3 -I mut/h3b-timeout-underreports.py --repo fix --rev <40 hex> \
  --panel fix/panel-timing.json --scratch-root <scratch>/scr --timeout 1 --json
```

Wall time: main sweep 254 s (baseline + 8 mutants), supplemental sweep 135 s (2 mutants); host
load average at report time 112 (1 min) on 32 cores. The counter selftest is the slow leg (it
builds a fixture git repository and replays the pipeline); no lane leg was replayed.

## 6. Tooling, scratch, hygiene

- No tool was installed or upgraded; system `python3` (stdlib) only; no pacman transaction, no
  network, no host service.
- The gate and counter are instruments; the harness is an instrument (it spawns the gate, the
  counter and stub legs, and the counter's selftest spawns git inside its own temp fixture); no
  candidate code was written.
- The lane tree was read-only throughout: anchors re-hashed after the sweep are identical to the
  values at the top; no git/jj command was run; no commit, push or index touch.
- Scratch `$HYAKU_SCRATCH/mado-r100/R100MMutHarm` is removed before yield; the report is the only
  artifact.

Report: .ufo/waves/round-100/w1/R100MMutHarm.md
