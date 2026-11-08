# R100MExecCounterC2 - the C2 counting command for PRED-C2-r100-v1

Seat: executor (counter), wave `w1`, round 100, lane `mado-shokunin`, base `43309e6a`.
Deliverable: `.ufo/waves/round-100/build/c2-r100-harm-watch.py`
(sha256 `b22ab669896001ea1f99c5f2070211e013228616b3346104a8c5626586ca7530`).
Contract: `.ufo/waves/round-100/claims-declaration-r100.md`, section C2, frozen before any case
was scored. Nothing below widens that predicate.

## 1. What was built

A stdlib-only counting command that pins its three inputs and re-derives every frozen conjunct.

```
c2-r100-harm-watch.py --repo DIR --rev REV --base-rev REV \
  --panel PANEL.json --expect-panel-sha256 SHA \
  --timing TIMING.txt --expect-timing-sha256 SHA \
  --expect-gate-sha256 SHA --scratch-root DIR [--json]
c2-r100-harm-watch.py --selftest
```

Exit map 0 TARGET_MET / 1 TARGET_MISSED / 2 SETUP_ERROR, with one verdict line carrying every
conjunct's value:

```
MADO_C2_R100: TARGET_MISSED pred=PRED-C2-r100-v1 rev=219e14f4... base_rev=43309e6a...
  gate_sha256=2d604f7b... panel_sha256=6d259164... timing_sha256=e7280b53...
  panel_legs=28 legs_run=28 mismatches=1 gate_elapsed_emitted=1
  timing_legs_timed=28 timing_ids_unique=28 max_elapsed_ms=708014
  panel_timeout_s=3600 control_600s_would_mismatch=1 selftest_failed=0
  selftest_checks=33 selftest=checks=21 failed=0 mismatch_legs=ledger
  missed=mismatches_0
```

A reader re-derives the verdict from numbers; nothing rests on the word TARGET_MET.

### Conjunct map (frozen sentence -> mechanism)

| frozen conjunct | mechanism |
|---|---|
| `panel_legs == 28` | `HARM_WATCH: legs=N` from the full-panel run |
| `legs_run == 28` | the `--json` object's `legs_run` **only**; there is no fallback to the human summary, so a gate that ignores `--json` fails the conjunct instead of inheriting a count |
| `mismatches == 0` | the summary line and the json object must both say 0 |
| `gate_elapsed_emitted == 1` | every human `LEG` line matches `elapsed_ms=<int>` AND every json leg object carries an `int` (bools rejected) `elapsed_ms` |
| `timing_legs_timed == 28` | lines matching exactly `^(\S+)\s+rc=(\d+)\s+elapsed_ms=(\d+)$` in the pinned receipt |
| `max_elapsed_ms > 600000` | maximum `elapsed_ms` over those lines |
| `panel_timeout_s * 1000 >= 2 * max_elapsed_ms` | `timeout_s` read from the pinned panel; a non-numeric value is SETUP_ERROR, never a silent pass |
| `control_600s_would_mismatch >= 1` | count of timed legs over 600000 ms, i.e. the round-99 cap re-derived from the same receipt |
| `selftest_failed == 0` | parsed from the gate's own `HARM_WATCH_SELFTEST: checks=N failed=M` |

`--base-rev` is accepted and echoed but carries **no** conjunct: round 100's C2 is not a
before-state-absence claim (the gate exists at `43309e6a`), and inventing an absence check would be
an added conjunct. That is the M99-3 discipline applied in the other direction.

### Two deliberate non-widenings

- `timing_ids_unique` is printed but is not a conjunct. A receipt of 28 rows naming one leg is
  possible in principle; the frozen sentence counts rows, so the counter counts rows and leaves the
  duplicate count visible on the verdict line for an attack seat.
- `mismatch_legs` (the ids that disagreed) is printed for the same reason: a 28-leg panel costs
  20+ minutes to reproduce, and a reader should not have to pay that to learn which leg is red.

## 2. Instrument, not candidate

An instrument: it spawns `git show` for the byte pins, the gate as `python3 -I`, and the gate spawns
the 28 legs. It models nothing about glib and answers no modelled question; there is no candidate in
this seat's scope. Scratch hygiene: every directory the counter creates carries
`.c2-r100-harm-watch`, a reused root is cleared of marked entries, and any unmarked entry is refused
with exit 2 (measured in the self-test).

## 3. Counter self-test

```
$ python3 -I .ufo/waves/round-100/build/c2-r100-harm-watch.py --selftest
MADO_C2_R100_SELFTEST: checks=21 failed=0      exit=0
```

Fixtures: a private fixture git repo with 28 legs; a good panel; a short-cap panel
(`timeout_s=1000`); a receipt whose slow leg is 500000 ms; a receipt with 27 timed legs; a gate that
never emits `elapsed_ms`; a gate whose `--selftest` reports `failed=2`; a red panel; three pin
mismatches; a receipt with no `TIMING-DONE`; a scratch root with a foreign entry. Each drives exactly
the conjunct it targets red, and the good fixture drives all nine green. Transcript:
`.ufo/waves/round-100/receipts/c2-counter-selftest-r100.txt`.

## 4. Negative control at the frozen base bytes

Gate `37a0544b` (committed r99 bytes, no `elapsed_ms`), panel r99 `160763ce` (`timeout_s=600`),
timing = a synthetic 28-leg fixture:

```
TARGET_MISSED  panel_legs=28 legs_run=28 mismatches=1 gate_elapsed_emitted=0
  timing_legs_timed=28 max_elapsed_ms=700000 panel_timeout_s=600
  control_600s_would_mismatch=1 selftest_failed=0
  missed=mismatches_0,gate_elapsed_emitted_1,timeout_ge_2max
exit=1   wall 1257.21 s
```

Three conjuncts red at base bytes, with values. The measured mismatch count is 1, not round 99's 2:
the panel is load-sensitive, which is exactly why the round re-derives its cap from a receipt rather
than asserting a number.

## 5. The landed panel: eight of nine conjuncts green, one leg red

Pinned run at the committed rev, gate bytes materialised from git, panel `6d259164`, receipt
`e7280b53` (the working-tree copy - see section 6):

```
panel_legs=28 legs_run=28 mismatches=1
gate_elapsed_emitted=1 timing_legs_timed=28 timing_ids_unique=28
max_elapsed_ms=708014 panel_timeout_s=3600 control_600s_would_mismatch=1
selftest_failed=0 selftest_checks=33   mismatch_legs=ledger
exit=1   wall 1315.89 s (21 m 55 s)
```

`LEG ledger rc=1 expect=0 marker=MISS rc-and-marker-mismatch elapsed_ms=270`

### Cause, measured

```
$ python3 -I quality/check-tool-ledger.py --repo . --rev 219e14f4a890...
LEDGER-ROW reason=uncovered path=quality/counters/c1-r100-launchenv-path.py detail=no-row
LEDGER-ROW reason=uncovered path=quality/counters/c2-r100-harm-watch.py detail=no-row
LEDGER: population=201 ledger_rows=199 uncovered=2 dangling=0 bad_pointer=0 empty_desc=0
        verdict=TARGET_MISSED rev=219e14f4a890...
rc=1
```

The round shipped two new counters and no ledger table rows. `SKILL.md` mentions both paths in prose
(`:3025`, `:3028`) but `check-tool-ledger.py` reads a table, and neither path has a row, so the
`ledger` leg is red and `mismatches == 0` is unreachable. The repair is a registry row per counter
at the row's declared revision with pins re-derived from the artifact (`corpus/QUALITY.md` criterion
171, the M99-1 lesson). That file is outside this seat's write scope; it is the L1's and the
scribe's move.

So the claim is not met, and the reason is bookkeeping rather than behaviour: the gate change itself
holds up on all 27 other legs.

## 6. Two lane-input defects this counter exposed

**(a) The committed timing receipt has no `TIMING-DONE` line.** At `219e14f4` the receipt hashes
`dd8d9f88...` and `grep -c TIMING-DONE` reports 0; the working-tree copy `e7280b53...` has it.
Measured against committed bytes:

```
MADO_C2_R100: SETUP_ERROR timing receipt has no TIMING-DONE line or no timed legs
exit=2
```

The format sentence in C2 freezes "`id rc=<n> elapsed_ms=<n>` per line plus a `TIMING-DONE` line",
so refusing is the contract, not pedantry. A row that pins `dd8d9f88` cannot go green at any
revision. Re-land the receipt (then set the pin to the re-landed bytes) or narrow the format sentence
- the second is the L1's call, never this seat's. The sibling receipt `c2-control-no-done-r100.txt`
records the same class as `M100-1` on a hand-edited copy; this measurement is the harder one,
because it is the committed bytes at the measured rev.

**(b) Gate bytes moved mid-wave.** `37a0544b` (base) -> `2d604f7b` (landed at `219e14f4`) ->
`acecb0ea` (working tree, later). A run pinned to `2d604f7b` against the live tree therefore ended in
`SETUP_ERROR gate sha256`, which is the pin working. Every number in this report comes from bytes
materialised with `git show 219e14f4:quality/harm-watch.py`, never from the mutable tree, so no
result here depends on a sibling's in-flight edit.

## 7. Two refinements the measurement forced back into the counter

**(a) `--rev` is resolved to a 40-hex commit before use.** The gate substitutes `--rev` into panel
rows verbatim, and the `r97c1_filetype` leg's counter rejects an abbreviated rev
(`rev '219e14f4' is not 40 hex`, exit 2). A counting command invoked with a short sha therefore
manufactures a red leg for a reason that has nothing to do with the claim - which is exactly what
happened on this seat's first pinned run (`mismatches=2`). The counter now resolves `--rev` once via
`git rev-parse --verify REV^{commit}` and uses the canonical sha for every git read and for the
gate's `--rev`; an unresolvable rev is SETUP_ERROR. Post-fix, the same panel run reports
`mismatches=1`, not 2.

**(b) A deep `--scratch-root` breaks the `r97c1_filetype` leg.** That leg creates AF_UNIX sockets
below `<scratch>/<leg-id>/`, and the kernel caps `sun_path` at 108 bytes. With the seat's long
scratch root the leg died in the generator:

```
OSError: AF_UNIX path too long   (filetype-fresh-r97.py:216, srv.bind(p))
MADO_FILETYPE_COUNT: SETUP_ERROR id=setup-fresh-gen generator rc=1
```

Measured: the failing path was 143 bytes for the longest case
(`.../c1r97-xxxx/sock-06-synth-db-socket/s.sock`); with a short root the same leg is green
(`LEG r97c1_filetype rc=0 expect=0 marker=ok ok elapsed_ms=368881`, 371.85 s wall). The counter's
internal scratch directories are now one character each (`g`, `p`, `t`, `m`, saving 7 bytes) and it
prints a `MADO_C2_R100_NOTE: scratch_leg_path=N bytes` advisory so a caller sees the budget before
losing 20 minutes to it. The advisory is not a conjunct and changes no verdict.

Round 99's measurement sat at 103 bytes for the same path - inside the limit by 5 bytes. Any caller
whose scratch root is longer than roughly 57 characters will see this leg red; that is a property of
the leg, not of the gate change, and worth a line in the round's lessons.

## 8. Risks and untested surface

- The panel verdict in section 5 uses the working-tree receipt (`e7280b53`), because the committed
  one cannot be parsed under the frozen format (section 6a). It is a pinned run over pinned panel,
  gate and receipt bytes, but the receipt pin is not the committed value; the L1 must re-land before
  the row can be quoted as the counting command's own output.
- The receipt's provenance - that each line really is one `--only` invocation - is unverifiable here;
  it is pinned by sha256 and vouched for by the seat that measured it.
- `TIMING_LEG_RE` accepts non-negative integers only. `elapsed_ms=7.1e5` or `elapsed_ms=+700` fails
  the parse and lands as SETUP_ERROR rather than a wrong number. Narrow, and visible.
- `--gate` draft mode (gate bytes from a file, panel/timing from the working tree) exists for in-wave
  exercise only and must never appear in the pinned counting row.
- Timing: the 28-leg panel costs 17-26 minutes on this host at load 250-260 on 32 cores. The counter
  runs the panel once and the gate selftest once; it never loops or retries.

## 9. What the L1 has to do

1. Add ledger rows for `quality/counters/c1-r100-launchenv-path.py` and
   `quality/counters/c2-r100-harm-watch.py` (fixes the single red leg), then re-run the pinned
   command. The other 27 legs are measured green, so [INFERENCE, not measured] the run will report
   `TARGET_MET`; only a re-run makes that a measurement.
2. Re-land `panel-timing-r100.txt` with its `TIMING-DONE` line and set the row's
   `--expect-timing-sha256` to the re-landed bytes.
3. Land this counter at `quality/counters/c2-r100-harm-watch.py` (its bytes here are
   `b22ab669...`) and point the row at it; the committed copy at `219e14f4` is the earlier
   `e4741843...` revision, which lacked the rev resolution and the mismatch-leg diagnostic.
4. Keep the row's `--scratch-root` short (under about 57 characters) or expect the
   `r97c1_filetype` leg to fail on AF_UNIX path length.
