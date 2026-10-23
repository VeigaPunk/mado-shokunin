# CritC2Claim — attack on C2's admission as registered (PRED-C2-r27-v2)

Seat: MadoR27.CritC2Claim, 2026-10-23. Read-only attack on the C2 claim's admission as
registered. Scope: registration.md C2 sections (v1 + redesign v2), w2/reports/CritHeldOut.md,
w2/reports/ReviewControlsC2.md, w2/reports/ExecSuiteA1.md, w2/reports/ExecSuiteB2.md,
w2/reports/SentinelC2v2.md, w2/reports/CritClaimsPreData.md, w1/reports/CritC2Counter.md,
w1/reports/SentinelC2Clone.md, the frozen counter `.ufo/waves/round-27/c2/count-v2.py` and the
two landed suites `quality/counter-selftest.py` and `quality/population-suite.py` (both landed
at 5c1d495 from ExecSuiteA1/ExecSuiteB2 first-returned bytes). No held-out files were read (role
forbids). No lane file other than this report was written. No counter, suite, or subject was
executed. Receipt `evidence/c2-after-48b9434a.txt` exists and is quoted below.

## (a) Predicate sentence identical across registration / counter / receipt

**Registration** (`.ufo/waves/round-27/registration.md`, C2 v2 redesign section): "At REV, the
committed suites quality/counter-selftest.py … and quality/population-suite.py … each run on a
fresh no-local clone of REV inside a sandbox that hides the lane and the host home, exit 0 on
every green run (each pristine subject set, each subject with one of two public
behaviour-preserving edits, and each valid sealed behaviour-preserving edit, with at least 3
valid sealed edits covering all three subjects), exit non-zero on each of the 15 W mutants … and
exit non-zero on at least three quarters of the valid sealed held-out mutants, with at least 6
valid held-out mutants and at least 2 per subject; target: green=all, w_killed=15/15,
h_killed>=ceil(0.75*h_valid), h_valid>=6."

**Counter** (`c2/count-v2.py:3-13`): the docstring repeats the same sentence verbatim, preceded
by the explicit note "PRED-C2-r27-v2 (same sentence in registration.md, this code and the
receipt label)". This is a self-annotation, not an independent check.

**Receipt** (`evidence/c2-after-48b9434a.txt`, last line): the summary line carries the label
`PRED-C2-r27-v2` followed by the same target fields (green, w_killed, h_killed, h_valid, …).

Finding: the predicate sentence is propagated, not independently asserted. The counter prints
the label it was programmed to print; the receipt echoes the counter's self-label. Nothing in
the pipeline checks that the *executed* code is the same code whose sha256 is pinned — the
receipt does print `counter c2-r27-v2 sha256:4dfb34b5…09d3` at line 1 and ReviewControlsC2
verified that hash equals the frozen pin, but that verification is a *review seat's* cross-check,
not a runtime guard. This is acceptable *if* the review is treated as part of admission
evidence; it is a provenance gap if the receipt alone is treated as self-proving.

Axis verdict: **pass with caveat** — sentence is textually identical in all three places;
identity rests on ReviewControlsC2's external sha256 cross-check, not on the receipt alone.

## (b) Do the suites actually EXECUTE subject behaviour?

**Suite A** (`quality/counter-selftest.py`): the subject counters are **imported by path**
(`load_counter`, lines 405-409) and their `main()` is **called in-process** (`run_counter`,
lines 412-426). Every check in the `REQUIRED` inventory (lines 182-205) is a behavioural probe:
a synthetic tool file is written, a `FakeOracle` returns a table with one field perturbed, the
counter's `O.oracle` / `O.snapshot` / `O.run_tool` / `O.check_build` / `O.coredumps` are
replaced with fakes, and the counter is asked to judge the synthetic tool. `record()` (line
395) records a PASS only when the observed `(rc, cases_pass, verdict)` match the expectation
for a broken counter. A subject that pins its own sha and exits 0 without executing is *not*
able to pass: the checks require `rc == 1` and `verdict == "TARGET_MISSED"` on each
single-field mutation, and the only way to produce `rc == 1` with a `TARGET_MISSED` verdict is
to actually run the comparison logic and observe a mismatch. The `c1-near-perfect` and
`c2-near-perfect` checks (lines 498-509, 560-568) additionally require the counter to write a
marker file into the case tree and then misjudge exactly that one case — a pin cannot do this.

**Suite B** (`quality/population-suite.py`): the subject checker is **run as a subprocess**
(`subprocess.run([sys.executable, "-I", checker, …])`, line 352) on 46 fixtures, each with a
known-expected `(exit_status, verdict_class, final_line, mention_count, leg_set)`. A pin that
never runs the checker cannot produce the correct per-fixture exit codes and leg sets.

**Do the landed suites contain checks a non-executing pin passes?** A raw sha/AST pin fails
immediately: it has no per-fixture/per-field behaviour to vary. `K2ShaPin` green=2/8,
`K2ASTPin` green=5/8, `K2NormPin` green=8/8 **but** sealed-rescore green=8/17 (ReviewControlsC2
Q3) — the sealed benign rows defeat it. `K2WBlocklistExact` green=8/8 + w=15/15, but h_killed=0/18
(L1-sealed-rescore-summary) — the sealed mutant rows defeat it. So on the *control* side, no
non-executing pin survives the sealed set.

Axis verdict: **pass** — the suites are genuine behavioural gates. The w2 critic's demand
(behavioural gates, not pins) is met by the landed suites.

## (c) Sealed-edit validity: CritHeldOut's semantic-validity findings

CritHeldOut reviewed all six sealed JSON files and found **6 sound / 0 unsound** for every
file, with 6/6 witness triplets showing behavioural differences for the three mutant files
(HeldC1v2.json, HeldC2.json, HeldChk.json) and 18/18 full-output comparison pairs agreeing for
the three `-benign` files. CritHeldOut explicitly states: "No falsifying counterexample was
sustained. No reviewed row needs a semantic correction on the available evidence."

The counter's own `load_rows` (`c2/count-v2.py:113-142`) applies additional mechanical
validity checks: shape, `old != new`, `old` occurs exactly once in pristine, `ast.parse`
succeeds, `ast.dump` differs from pristine, and the edited bytes are sha-distinct from
pristine, all W mutants, and every other row. The receipt prints `invalid=0`.

Receipt cross-check: `evidence/c2-after-48b9434a.txt` line 4 records `h_valid=18` (the three
mutant files × 6 rows each) and `b_valid=9` (the three `-benign` files × 3 rows each), with
`h_min_per_subject=6` (two rows per subject file: HeldC1v2 6, HeldC2 6, HeldChk 6). CritHeldOut
independently counted 6 rows in each mutant file and 3 rows in each benign file, and verified
the witness provenance. The numbers are consistent.

Axis verdict: **pass** — CritHeldOut's review is the strongest available evidence that the
sealed rows are semantically meaningful and non-equivalent; the counter's mechanical validity
checks complement but do not replace that review.

## (d) Sandbox: suites under bubblewrap, `--no-local` clones, `/home` and `/fast` hidden

Counter v2 source confirms all three:

- `--no-local` clones: `clone()` at `c2/count-v2.py:69-77` runs `git clone --quiet --no-local
  --no-checkout LANE m`. `--no-local` prevents the clone from using hardlinks/alternates into
  the lane object store.
- bubblewrap sandbox: `run_suite()` at `c2/count-v2.py:96-110` builds a `bwrap` command with
  `--ro-bind / /`, `--tmpfs /home`, `--tmpfs /fast`, `--tmpfs /run`, `--tmpfs /tmp`, `--bind d d`,
  `--dev /dev`, `--proc /proc`, `--unshare-all`, `--die-with-parent`, `--new-session`,
  `--clearenv`, `--setenv PATH /usr/bin`, `--setenv HOME <run-dir>/home`, `--setenv TMPDIR
  <run-dir>/tmp`, `--chdir m`.
- `/home` and `/fast` hidden: `--tmpfs /home` and `--tmpfs /fast` overlay the host directories
  with empty tmpfs; only the run directory `d` is bound writable.

SentinelC2v2 (w2) independently probed this and found `ENOENT` on both the held-out directory
and a direct lane-file open. Two residual findings remain (MEDIUM: suite stdout/stderr
unbounded; LOW: clone `.git/config` leaks origin path + dirty-bit), but neither provides a path
to the sealed held-out set or the host lane.

Axis verdict: **pass with noted residuals** — sandbox is as registered; the two SentinelC2v2
findings are real but do not defeat the claim.

## (e) ast.parse-vs-compile weakness in the v2 loader

CritClaimsPreData §3 (`w2/reports/CritClaimsPreData.md:69`) noted: "the documented 'must
compile' requirement … is implemented with `ast.parse`, not Python compilation … module-level
`return` has a parseable AST but is rejected during compilation, so parsing alone is weaker
than that literal requirement."

Counter source: `load_rows` at `c2/count-v2.py:128-132` catches only `SyntaxError` from
`ast.parse(nb)`. It does not call `compile()`. A row whose edited bytes contain a module-level
`return` statement would pass `ast.parse` (which does not check `return`-outside-function) but
fail `compile()`. If such a row were in W or H, the suite would attempt to `exec()` or import
the edited subject and the subject would raise `SyntaxError` at import time — the suite would
exit non-zero, which the counter would count as a **kill**. For a W row this is harmless (the
mutant is supposed to be killed). For an H row this is more subtle: the row is counted as
h_killed, but the "kill" is caused by a Python compile error, not by the suite detecting a
behavioural difference. This weakens the evidentiary value of that particular kill but does not
produce a false pass.

**Do any accepted sealed/W rows exploit this?** CritHeldOut found all 18 mutant rows and all 9
benign rows are semantically sound (compile and behave differently). The receipt shows
`invalid=0` and all 18 H rows ran through the suite (12 killed, 6 survived with `rc=0` — see
axis f). No W row or sealed row is alleged to contain a module-level `return`. The weakness is
latent, not exercised.

Axis verdict: **non-blocker** — the `ast.parse` vs `compile` gap is real but no accepted row
exploits it; a future counter revision should use `compile(nb, …, 'exec')` instead of
`ast.parse` for the validity gate.

## (f) Strongest remaining bypass constructible on paper

### f1. Suite-A blind spots: three H mutants SURVIVED on the C1-counter side

The receipt records three H rows that **survived** suite A:

```
CASE H  H/HeldC1v2:held-c1v2-node-subset            suite=A rc=0 SURVIVED
CASE H  H/HeldC1v2:held-c1v2-missing-version-guard  suite=A rc=0 SURVIVED
CASE H  H/HeldC1v2:held-c1v2-extra-output-segment   suite=A rc=0 SURVIVED
```

And three on the C2-counter side:

```
CASE H  H/HeldC2:HeldC2-extra-disjunction           suite=A rc=0 SURVIVED
CASE H  H/HeldC2:HeldC2-unstable-conjunction        suite=A rc=0 SURVIVED
CASE H  H/HeldC2:HeldC2-embed-boundary              suite=A rc=0 SURVIVED
```

Six of eighteen sealed mutants (33%) are not killed. The predicate requires `h_killed >= ceil(0.75
* h_valid) = 14`; the observed `h_killed=12` misses by 2. The receipt verdict is
`TARGET_MISSED`.

**Attack:** a suite author who knows these six blind spots can write a suite that passes all
green rows and kills exactly the 12 killable H rows while deliberately ignoring the 6 surviving
classes. The result would be `h_killed=12/18`, still `TARGET_MISSED` — so this is not a bypass
that *passes* the predicate. But it demonstrates that the suite's discriminative power over the
sealed population is incomplete. The suite author (ExecSuiteA1) did not claim to cover every
possible mutant class; the 12/18 result is honest evidence of partial coverage.

**Why the six survive (inferred from suite source and mutant names):**
- `held-c1v2-node-subset`: suite A judges the counter by feeding it synthetic tools; a mutant
  that changes the counter's *case generator* (not its comparison logic) leaves the tool and
  the fake oracle agreeing — the "population mutations are not observable" limit documented in
  ExecSuiteA1's own "Limits and risks".
- `held-c1v2-missing-version-guard`: suite A replaces `O.oracle` with a fake that *always*
  returns the correct version; the counter's version guard is exercised only when the fake
  returns a wrong version, which happens only in the `c1-version-guard` check. A mutant that
  removes the guard entirely passes every other check.
- `held-c1v2-extra-output-segment`: the counter prints an extra output segment; suite A's
  `pred()` regex extracts `cases_pass=N/M` and `verdict=TOKEN` from the counter's stdout. If
  the extra segment does not change those two fields, the suite sees no difference.
- `HeldC2-extra-disjunction` / `HeldC2-unstable-conjunction`: logical changes in the C2
  counter's comparison that are invisible to the 18 field-level probes (each changes exactly
  one field); a mutant that adds a redundant `or` clause or reorders conjuncts without changing
  any single-field outcome passes all field checks.
- `HeldC2-embed-boundary`: changes the embed threshold; suite A's `EMBED_ARG` is exactly 40
  characters. A mutant that moves the boundary to, say, 35 or 45 would still catch the 40-char
  fixture and pass.

### f2. Suite-B blind spot: leg-count fallback

`population-suite.py:340-344` compares the exact leg set only when both the subject and the
fixture use the known vocabulary (`case_lines`, `denominator`, `registration_total`);
otherwise it falls back to comparing the **count** of legs. A mutant that renames the legs and
simultaneously changes which comparisons fail while keeping the same count would survive the
leg check. The exit-status and verdict-class checks still constrain the mutant, so this is not
a full bypass — but it is a residual discriminative gap.

### f3. Non-blocker: output-flood DoS (SentinelC2v2 MEDIUM)

A malicious suite can emit unbounded stdout/stderr; the counter collects it with
`capture_output=True` before truncating. This is a host-resource concern, not a claim bypass.

### f4. The strongest on-paper bypass that would pass

Construct a suite that:
1. Executes the subject on every green and W row (to satisfy the "suites must execute" reviewer),
2. For H rows, executes the subject but ignores the result and instead pattern-matches the
   edited subject bytes against the 6 known-surviving mutant classes (using the mutant `old`/
   `new` pairs from the held-out JSON, which the suite can read from the clone since the
   counter copies the edited bytes into the clone),
3. Exits 0 iff the subject does not match any of the 6 patterns.

This suite would achieve `h_killed=18/18`, `green=17/17`, `w_killed=15/15` — full
TARGET_MET. **However**, this requires the suite to know the 6 surviving H rows' content, which
is only available *after* the first measurement. The suites were written and frozen *before*
any H measurement (they are the landed w2 data-seat outputs). The bypass is therefore
**retrospective**: it demonstrates that the predicate is satisfiable by a non-general gate, not
that the current suites are such a gate. The current suites pass 12/18 H rows honestly; a
future wave could write a suite that pattern-matches the disclosed surviving rows and pass
18/18 without any real behavioural gate on those rows. This is the strongest argument for
**rotating the sealed H set** in any future re-measurement.

## Receipt status

`evidence/c2-after-48b9434a.txt` exists and is quoted above. Key line:
`PRED-C2-r27-v2 green=17/17 b_valid=9 w_killed=15/15 h_killed=12/18 h_need=14 h_valid=18
h_min_per_subject=6 invalid=0 verdict=TARGET_MISSED`, `exit=1`.

## C2-admission risk list

| # | Finding | Severity | Blocker? |
|---|---------|----------|----------|
| R1 | h_killed=12 < h_need=14; verdict=TARGET_MISSED | HIGH | **Yes** — the numeric target is not met |
| R2 | 6/18 sealed mutants survive suite A (f1 above) | MEDIUM | No (subsumed by R1) — but a future suite could pattern-match these disclosed rows to pass without a general gate; rotate H on re-measurement |
| R3 | ast.parse vs compile gap in loader (e above) | LOW | No — latent; fix in a future counter revision |
| R4 | Suite stdout/stderr unbounded (SentinelC2v2 MEDIUM) | LOW | No — host-resource DoS, not a claim bypass |
| R5 | Clone `.git/config` leaks origin path + dirty bit (SentinelC2v2 LOW) | LOW | No — cannot pass green and kill W simultaneously |
| R6 | K2NormPin has only one v2 seed (ReviewControlsC2 F1) | LOW | No — NormPin is already defeated by the sealed set |
| R7 | L1 sealed-rescore summary omits K2DoNothing and K2WBlocklist (ReviewControlsC2 F2) | LOW | No — DoNothing trivially 0; WBlocklist's omission leaves a gap in committed sealed evidence |
| R8 | NormPin result lines appended to K2ASTPin.md (ReviewControlsC2 F3) | LOW | No — attribution hygiene |
| R9 | Suite B leg-count fallback (f2 above) | LOW | No — exit-status and verdict-class checks still constrain |
| R10 | Predicate sentence propagated, not independently asserted (a above) | INFO | No — ReviewControlsC2's external sha256 cross-check closes the loop |

## Bottom line

The C2 claim's admission as registered is **blocked on the numbers**: the frozen counter at the
after revision prints `h_killed=12/18` against `h_need=14`, yielding `TARGET_MISSED`. All
structural axes (sandbox, sealed validity, suite behavioural-honesty, predicate consistency)
pass review. The six surviving H rows are the substantive residual weakness — they demonstrate
that suite A's discriminative coverage over the sealed population is partial, and they create a
theoretical retrospective-bypass channel (f4) that argues for H-set rotation on any future
re-measurement.

Report: .ufo/waves/round-27/w3/reports/CritC2Claim.md
