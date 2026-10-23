CANDIDATE /fast/scratch/hyaku/mado-r27/data/ExecSuiteB2/population-suite.py sha256:99e7d876c1fcf2585354a22eff9d1c674c902ad1108e19ea50c9caa49eb3046c

# ExecSuiteB2 — round 27 wave w2, suite B (C2 data seat)

Suite B of the C2 claim: an offline gate over the round-26 population checker
`.ufo/waves/round-26/quality/check-population.py`. CLI is
`--checker PATH`; the suite writes its own registration and receipt fixtures under
`$TMPDIR`, runs the checker on them, and exits 0 only when every fixture gives its
expected exit code and verdict line.

## What it is

One python3 stdlib file, 19,955 bytes, 46 built-in fixtures, no network, no lane
reads, no pins. It never looks at the subject's bytes, AST or path, never reads the
lane, never inspects the process tree or the clock, and removes its own scratch
directory before returning.

Per fixture it writes a registration file and one or more receipt files into a
private `mkdtemp` directory (created under `$TMPDIR`; the wave scratch root is the
fallback), then runs

```
python3 -I <checker> --registration <reg> <receipt> [...]
```

with a cleared environment (`PATH`, `HOME`, `TMPDIR` only) and cwd inside the
scratch directory. A fixture passes only when all of the following hold:

1. the process exit status equals the expected status (0 agree / 1 disagreement /
   2 unreadable);
2. the verdict class on the checker's final summary line equals the expected class.
   The class is read from the `verdict=<token>` field with a synonym map
   (`pass|passed|ok|agree|agreed` = 0, `fail|failed|mismatch|disagree|disagreed` = 1,
   `unreadable|unevaluable|error` = 2), so a behaviour-preserving rewording of the
   token is not read as a behaviour change while a wrong class still fails. A
   subject that reports no verdict at all is not judged on this point;
3. the last non-empty stdout line is exactly `exit=<n>` (the checker's documented
   final line);
4. each receipt the checker was handed is named in its report — once per summary
   the receipt carries (so a subject that checks only the first summary of a
   two-summary receipt is caught), or once when it can read no population. This is
   judged only for a subject that names the paths it was given: a subject that names
   neither the registration nor any receipt is not judged on this point;
5. where the checker names the failed comparisons, the reported leg set matches the
   failures the fixture induces. The leg names are compared exactly only when both
   sides use the checker's current vocabulary (`case_lines`, `denominator`,
   `registration_total`); otherwise only the number of legs is compared, so a
   rewording of the leg names stays green.

## Fixture coverage (46)

| group | fixtures | what is gated |
|---|---|---|
| green (14) | single receipt, two receipts, 41 cases, numerator `0/3` not compared, tab-indented summary, space-indented summary, `CASE<TAB>`, summary before case lines, same predicate twice with the same total, predicate-id charset `PRED-C1-r26.v2_x`, summary with trailing text, whitespace-only paragraph separator, predicate id ending at a non-id char (`PRED-ALPHA=1`), duplicate identical summary lines | the documented contract holds; each also kills the mutants that break its shape |
| red / disagreement (16) | case-line count short and long, denominator larger and smaller, both legs, registered total differs, unknown predicate, second summary disagrees, first summary disagrees, lower-case `case B` not a case line, indented `  CASE` not a case line, `NOTE CASE` not a case line, bare `CASE` without separator, second receipt disagrees, first receipt disagrees | status 1 and the right failing legs |
| exit 2 (16) | receipt without summary, receipt missing, receipt is a directory, receipt not decodable, registration missing, registration with no `**PRED-**` marker, registration with an unmarked predicate, predicate without a total, two predicates beside one total, one predicate beside two totals, same predicate twice with different totals, second receipt unreadable, unreadable beats disagreement, summary not at line start, `cases_pass =3/3`, `cases_pass= 3/3`, registration not decodable | status 2 and `UNREADABLE`, plus unreadable taking precedence over disagreement |

Tabs are covered at both ends the checker distinguishes: `CASE<TAB>B PASS` counts as
a case line, and a tab- or space-indented `PRED-... cases_pass=N/T` counts as a
summary, while a tab-indented `\tCASE` does not count.

Fixtures live in `FIXTURES` in the candidate as (name, registration, receipts,
expected status, registration_ok, expected legs). Receipts marked `None` are never
written (the path stays missing), `"DIR"` creates a directory, and a `bytes`
registration/receipt exercises the undecodable branches.

## Verification (all commands run by this seat)

1. **Pristine checker, in the lane** (subject at `2fdca5ca`, sha256
   `803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64`):

   ```
   cd /fast/scratch/hyaku/mado-r27/data/ExecSuiteB2 && \
     env -i PATH=/usr/bin HOME=/home/vgpnk timeout 300 prlimit --as=4000000000 --core=0 -- \
     python3 -I population-suite.py --checker \
     /home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-26/quality/check-population.py
   ```

   → `SUITE verdict=PASS fixtures=46 failed=0 -`, `exit=0`, 1.15 s wall. Sample rows:

   ```
   SUITE fixture=green-single-receipt status=ok want=0 rc=0 verdict=0 legs=- final='exit=0' mentions=green-single-receipt.receipt0.txt:1/1
   SUITE fixture=exit2-registration-not-decodable status=ok want=2 rc=2 verdict=2 legs=- final='exit=2' mentions=exit2-registration-not-decodable.receipt0.txt:0/0
   ```

2. **Inside the counter's own bubblewrap sandbox** (`/home` and `/fast` hidden, the
   run directory bound, `HOME`/`TMPDIR` inside it, `--unshare-all`, `--clearenv`) —
   the exact command shape the frozen counter builds:

   ```
   bwrap --ro-bind / / --tmpfs /home --tmpfs /fast --tmpfs /run --tmpfs /tmp \
     --bind $D $D --dev /dev --proc /proc --unshare-all --die-with-parent --new-session \
     --clearenv --setenv PATH /usr/bin --setenv HOME $D/home --setenv TMPDIR $D/tmp \
     --chdir $D python3 -I $D/population-suite.py --checker $D/check-population.py
   ```

   → `SUITE verdict=PASS fixtures=46 failed=0 -`, `exit=0`, 1.14 s.

3. **Frozen round-27 C2 counter v2 with the candidate as suite B, two fresh seeds:**

   ```
   cd /home/vgpnk/Projects/shokunin/mado-shokunin && \
     env -i PATH=/usr/bin HOME=/home/vgpnk timeout 1800 prlimit --as=4000000000 --core=0 -- \
     python3 -I .ufo/waves/round-27/c2/count-v2.py 2fdca5ca \
     --suite-b-file /fast/scratch/hyaku/mado-r27/data/ExecSuiteB2/population-suite.py --jobs 6 --seed HEX
   ```

   | seed | suite-B green rows | suite-B W rows | counter line |
   |---|---|---|---|
   | `742dd6b63e4cff61` | 3/3 `rc=0 PASS` | 6/6 `rc=1 KILLED` | `green=3/8 b_valid=0 w_killed=6/15 h_valid=0 verdict=TARGET_MISSED` |
   | `9c1f4d2e77ab0358` | 3/3 `rc=0 PASS` | 6/6 `rc=1 KILLED` | identical |

   The three suite-B green rows are `pristine`, `comment:check-population.py` and
   `assign:check-population.py`. The six kills are `q37-M1-ignore-registered`,
   `q37-M2-case-anywhere`, `q37-M3-drop-denominator`, `q37-M4-first-pred-only`,
   `q37-M5-case-plus-one`, `q37-M6-unreadable-exit-0`. The counter's overall
   `green=3/8` and `w_killed=6/15` are the suite-A shortfall
   (`quality/counter-selftest.py` is missing at this REV — another seat's artefact);
   `h_valid=0` because no held-out set was passed, which the data-seat contract
   forbids this seat from reading.

4. **Mutation battery of my own design** (driver
   `/fast/scratch/hyaku/mado-r27/data/ExecSuiteB2/test-extended.py`, 45 single-defect
   mutants written from the checker's documented contract, all applied to a fresh
   copy of the pristine subject): **42 killed, 3 survived**, and the three survivors
   are semantically equivalent mutants, verified line by line:

   | survivor | why it cannot change behaviour |
   |---|---|
   | `compare-registered-to-case-lines` (`if case_lines != registered:` → `if registered != case_lines:`) | same expression, operands swapped |
   | `count-case-lines-in-whole-text` (`lines` → `text.splitlines()`) | line 126 of the subject already binds `lines = text.splitlines()` |
   | `unknown-predicate-defaults-to-zero` (`populations[pred]` → `populations.get(pred, 0)`) | line 145 is only reachable after line 139's `if pred not in populations: … continue` |

   Killed classes include: numerator-vs-denominator confusion, case-line counting
   (case-insensitive, missing separator, space-only separator, exact-line regex,
   off-by-one, plus-one-per-summary), first-only / last-only / deduped / skipped
   summaries, the unknown-predicate branch and its KeyError form, all three
   registration guards, paragraph splitting, the `**PRED-**` marker, the total
   regex, all four summary-capture variants (column zero, leading spaces, narrower
   and wider id charsets, whitespace before `=`), unreadable exit status, unreadable
   verdict class, the unreadable-precedence branch, a non-`FileNotFoundError`
   except clause, an unreported no-summary receipt, a swallowed missing receipt, a
   swallowed unreadable registration, a removed `exit=` line and a renamed one.

5. **Behaviour-preserving edits stay green** (drivers
   `test-suite.py`, `test-benign.py`). Ten edits of the checker, all output-identical
   to the pristine file, all `SUITE verdict=PASS fixtures=46 failed=0`, `exit=0`:
   appended comment, inserted unused module-level assignment (the counter's two
   public benign shapes, also confirmed through the frozen counter in item 3),
   local-variable renames (`summaries`, `case_lines`), docstring rewrite,
   f-string rewrite of `print("exit=%d" % rc)`, helper extraction above
   `read_text`, blank-line collapse, import reorder, and a trailing `# noqa`
   comment on the `CASE_LINE` line.

## Retained evidence

* Candidate: `/fast/scratch/hyaku/mado-r27/data/ExecSuiteB2/population-suite.py`
  sha256 `99e7d876c1fcf2585354a22eff9d1c674c902ad1108e19ea50c9caa49eb3046c`, 19,955 bytes.
* Drivers retained in the same directory: `test-suite.py` (pristine, the six W
  mutants, the two counter benign shapes), `test-extended.py` (the 45-mutant
  battery), `test-benign.py` (ten behaviour-preserving edits), `probe-pristine.py`
  (pristine behaviour of the newer fixtures, used to pin the expected statuses
  before they were written into the table).
* Counter lines are quoted above verbatim; the counter's own per-run scratch under
  `/fast/scratch/hyaku/mado-r27/c2v2/` is created and removed by the counter.

## Risks and limits

* **Verdict-line strictness.** The suite requires a verdict class on the final
  summary line when the subject reports one, and the exact final `exit=<n>` line.
  Both are documented in the checker's docstring (the docstring says "Final line is
  `exit=<n>`"), and both were confirmed green on ten behaviour-preserving edits,
  but a sealed benign edit that removed or reworded the verdict summary entirely
  would be read as a red. I judged that risk smaller than the loss of
  discrimination: without the class check, a subject that reports `FAIL` while
  exiting 2 survives.
* **Mention counting** assumes the checker names the receipt paths it was given, as
  the pristine one does on every per-receipt report line. If a sealed benign edit
  changed how paths are printed, the check is skipped rather than failed when the
  subject names no path at all — a per-receipt count that drops below the summary
  count is still a failure, which is what kills a first-summary-only subject.
* **Leg-name vocabulary.** Exact leg-set comparison only happens when both sides use
  `case_lines` / `denominator` / `registration_total`; a renamed vocabulary falls
  back to a leg-count comparison. A subject that renames legs *and* changes which
  comparisons fail while keeping the same count would survive that check, but such
  a mutant also has to keep the exit status and verdict class, which the fixtures
  on both sides of each comparison constrain.
* **Held-out performance is unmeasured here.** The held-out directory,
  `HeldChk.json` and `HeldChk-benign.json` were not read (contract); `h_valid=0` in
  both counter runs above is that absence, not a measurement. The 45-mutant battery
  and the ten benign edits are my own design and approximate, but are not, the
  sealed set.
* **Not a general semantic gate.** The suite judges the checker's observable
  behaviour on 46 fixtures. A mutant that changes behaviour only outside those
  fixtures would survive; the fixtures were chosen to exercise every documented
  branch and both directions of every comparison.
* Scratch location: `$TMPDIR` first (the counter sets it inside the run directory,
  which lives under `/fast/scratch/hyaku/mado-r27/`), then
  `/fast/scratch/hyaku/mado-r27`, then the platform default. `HOME` is read only to
  hand the child a home directory; `TMPDIR` is read for the scratch root, as the
  assignment requires. No other environment variable is read.

## Host safety

* No Hyprland, no compositor, no `hyprctl`, no `/dev/dri`, no network was used. The
  checker is a stdlib text comparison; every run used `env -i PATH=/usr/bin
  HOME=/home/vgpnk`, so `WAYLAND_DISPLAY`/`HYPRLAND_INSTANCE_SIGNATURE` were neither
  set nor inherited.
* Hyprland coredumps on the host: **1338 before** this seat's first measurement and
  **1338 after** its last (`coredumpctl list --no-pager --no-legend | grep -c
  /usr/bin/Hyprland`) — delta 0.
* All long commands were `timeout`- and `prlimit --as=4000000000 --core=0`-bounded;
  the suite writes only into its own `mkdtemp` directory and removes it; `df -h /fast`
  showed 56–70 G free throughout.
* No tool or package was installed or updated (none was needed). No subagent was
  dispatched. No git/jj write command was run in the lane; every mutation test
  wrote only into fresh directories under
  `/fast/scratch/hyaku/mado-r27/data/ExecSuiteB2/` and removed them.
* Lane write: this report only. The candidate lives outside the lane and is copied
  in unmodified by the L1.

Report: .ufo/waves/round-27/w2/reports/ExecSuiteB2.md
