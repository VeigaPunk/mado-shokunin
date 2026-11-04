source: S435 — GNU Bash 5.3 official release manual, §3.7.5 Exit Status (opened 2026-11-03, held) — the documented exit-status vocabulary: zero is the success convention, 126/127 are execution failures, 128+N is a fatal signal — the ground for reading a nonzero status as "a child failed somehow", never as "the child's assertions failed"
verified-at: 2026-11-04
recheck: 90d — re-read S435 at the release manual; re-run `quality/counters/c1-r70-real-children.py` when the harness's kill-credit line, the fixture lane template, or the landing instrument's summary format changes

# Landing kill credit: a failed assertion, not an exit status (MADO-R70-1)

## Scope

Lane-tooling scope only. This entry explains round-70 claim C1
(`.ufo/waves/round-70/claims-declaration-r70.md`, C1 §): what the landing control
harness's `mz=pass|fail` credit meant in round 69, why a bare nonzero exit status is the
wrong observable, what the repaired credit requires, and how three **real** `bash`
children — a genuine failed assertion, a crash with no summary, and a garbled summary —
are scored against both harnesses. It is not a desktop claim and not a claim that the
fixture lane is the lane's real landing instrument.

## 1. The documented ground (S435, held)

The bash manual separates the ways a command can end badly: `126` and `127` are
*execution* failures (found but not executable, not found) and `128+N` is a fatal
signal (S435: the §3.7.5 table and the sentences around it). The lane's own round-66
criterion already rests on that row; round 70 applies it to a different subject — the
harness's credit rule.

The inference is one step and it is documented, not behavioural: an instrument's exit
status answers "did the process end well", not "did the check pass". A mutant whose
selftest *crashes* (a syntax error, a missing interpreter, a signal) exits nonzero
without ever reporting a failed check. Crediting that as a kill credits a broken child.

## 2. What the round-69 harness credited

`quality/counters/c1-r69-landing-controls.py` (byte-frozen; round 70 does not edit it)
carries the single line

```
mz_killed = mz_rc != 0
```

so any nonzero child is a kill. On the three real-child scenarios that line produces
`mz=pass` for a genuine failure **and** for a crash and for a garbled summary — measured
in `.ufo/waves/round-70/control-baseline-r70.txt` § C1 (`base_correct=1/3`).

The round-69 selftest already asserted "a crashing M-R child is not a kill" and "an M-Z
run with no assertion summary is not a kill", but those cases were driven with scripted
in-process stand-ins; the real M-Z position carried no oracle.

## 3. The repaired credit

`quality/counters/c1-r70-landing-controls.py` (round 70's successor harness) credits M-Z
only when both hold:

1. the child exited nonzero, and
2. the child's own `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` summary
   parses (a full match), `n > 0`, and `p < n`.

`summary_shows_failure()` implements (2). A crash (no summary), a garbled summary and a
`p == n` summary all earn no credit; the harness then reports `mz=fail` and the round
reads a miss. Fail-closed: a genuine failure that crashes is reported as unproven rather
than credited.

## 4. The real-children battery

`quality/counters/c1-r70-real-children.py` builds a scratch git repo (`git init`, one
commit per mode, explicit identity, `-C` on every git call) whose `quality/landing-counters.sh`
carries the frozen clause `[ "$citations" -gt 0 ] && ` exactly once and decides its
behaviour from *that clause's own effect*:

| mode | assertion outcome after the harness deletes the clause | child rc | summary | expected `mz=` | r69 harness | r70 harness |
|---|---|---|---|---|---|---|
| `genuine` | the zero-citation case fails | 1 | `1/2 assertions passed` | `pass` | `pass` ✔ | `pass` ✔ |
| `crash` | the lane exits before reporting | 2 | none | `fail` | `pass` ✘ | `fail` ✔ |
| `garbage` | the lane prints an unparseable summary | 1 | `??? assertions passed` | `fail` | `pass` ✘ | `fail` ✔ |

Measured at `5adba5a92a8d58eb76533b39a9216d8e85d48fbc`:
`MADO_R70_REAL_CHILDREN: cases=3 correct=3 base_correct=1 verdict=TARGET_MET` rc 0
(`.ufo/waves/round-70/measurement-r70.txt`). The fixture's lane file is
`.ufo/waves/round-70/proto/fixture-lane.tmpl`; the counter rebuilds it byte-for-byte from
its own `LANE_TEMPLATE`.

## 5. Limits

- The set is three named scenarios, not a fault-coverage claim.
- The fixture lane is the counter's own instrument; it models the real instrument's
  zero-citation assertion but is not that instrument.
- A harness whose decisions merely *agree* on these three inputs is not distinguished
  from a correct one: the counter reads the contract line, not the harness's authorship.
  A stand-in that printed the expected `mz=` per fixture revision would score 3/3 and
  this entry does not claim otherwise.
- The credit is still presence-based: a summary that parses with `p < n` is credited as a
  kill even if the failing assertion is unrelated to the frozen clause. The harness's
  M-Z recipe and the child's own summary are the only join.
- Nothing here authenticates objects, repairs a rewritten repository, or measures a
  desktop surface.

## Verify

```
python3 -I quality/counters/c1-r70-real-children.py --repo . --rev <rev> \
  --base-rev b37a5aec4ea03f2223d8e09dd5d386d055c24179 --scratch-root <dir>
```

Exit 0 iff `correct == 3` and `base_correct == 1`; the last line is the contract sentence
this entry's § 4 quotes. `--selftest` is hermetic (26/26 at the measured content).
