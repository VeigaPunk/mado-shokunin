# MutSuiteB — round 27 w4, independent confidence for suite B

Assignment: 3 fresh mutants of the round-26 population checker built from the six disclosed
HeldChk class names, run against the **committed** `quality/population-suite.py`; confirm every
mutant is killed and the green baseline stays green. `/fast/scratch/hyaku/mado-r27/heldout/`
was never opened.

**Verdict: SUITE_B_HOLDS** — all 3 mutants killed (suite `rc=1`), pristine checker and both
public behaviour-preserving edits green (`rc=0`, `fixtures=46 failed=0`).

## Sandbox and provenance

* Sandbox: `git clone --no-local /home/vgpnk/Projects/shokunin/mado-shokunin`
  → `/fast/scratch/hyaku/mado-r27/repair/MutSuiteB/clone` (tip `86f7355b`). No write to the lane.
* The measured REV `48b9434a` is an ancestor of the clone tip, and
  `git diff 48b9434a HEAD -- quality/population-suite.py .ufo/waves/round-26/quality/check-population.py`
  is empty: the detector and subject bytes here are byte-identical to the ones the C2 receipt
  scored.

  ```
  SUITE   quality/population-suite.py                              sha256 99e7d876c1fcf2585354a22eff9d1c674c902ad1108e19ea50c9caa49eb3046c
  SUBJECT .ufo/waves/round-26/quality/check-population.py           sha256 803e0096c994d301fa7fe9a9dd7e35255ee1f5bcf3f63d15956cdba8943d0f64
  ```

  Both equal the hashes printed in `evidence/c2-after-48b9434a.txt`.

* Detector, run per subject (identical command line, only `--checker` differs):

  ```
  env -i PATH=/usr/bin HOME=/home/vgpnk TMPDIR=/fast/scratch/hyaku/mado-r27/repair/MutSuiteB/tmp \
    timeout 300 prlimit --as=4000000000 --core=0 -- python3 -I \
    /fast/scratch/hyaku/mado-r27/repair/MutSuiteB/clone/quality/population-suite.py \
    --checker <SUBJECT>
  ```

  The suite is self-contained (writes its own fixtures, removes its scratch); the subject is
  executed as a subprocess with `PATH=/usr/bin`. No network, no display, no Hyprland, no host
  home.

## Mutant sources (exact diffs against the pristine subject)

All three are single-contiguous-replacement instances built by
`/fast/scratch/hyaku/mado-r27/repair/MutSuiteB/build_mutants.py`, which asserts each old text
occurs exactly once and that the bytes change.

**M1 `case-overcount`** — sha256 `9f4824607377d13b0e576fdbbaf77ab846990d197466dc7d4c3d223a332cb281`
(an indented `CASE` line is counted as a case line; the documented contract is column 0)

```diff
@@ -134,7 +134,7 @@
-        case_lines = sum(1 for line in lines if CASE_LINE.match(line))
+        case_lines = sum(1 for line in lines if re.match(r"[ \t]*CASE[ \t]", line))
```

**M2 `duplicate-total`** — sha256 `2e75b6854ecb80b18def8033264429641f6b7777850bfa31585a47e01c5338f2`
(one predicate stated twice with different totals is silently resolved to the last total instead
of being an unreadable registration)

```diff
@@ -72,10 +72,6 @@
         total = totals.pop()
-        if labels[0] in populations and populations[labels[0]] != total:
-            problems.append("predicate %s stated twice with different totals (%d, %d)"
-                            % (labels[0], populations[labels[0]], total))
-            continue
         populations[labels[0]] = total
```

**M3 `summary-numerator`** — sha256 `ec60e04ebb2678d19f8e3b299246b57dbf20a1440ab194a9e08d2b65a8f2234d`
(the `cases_pass` numerator is compared with the registered total, an over-strict check the
contract forbids)

```diff
@@ -146,7 +146,7 @@
             if case_lines != registered:
                 legs.append("case_lines")
-            if den != registered:
+            if num != registered or den != registered:
                 legs.append("denominator")
```

## Results (actual output)

| subject | class | rc | suite line | killer fixture(s) |
|---|---|---|---|---|
| pristine `check-population.py` | green baseline | **0** | `SUITE verdict=PASS fixtures=46 failed=0 -` | — |
| appended comment edit (`green/comment.py`, sha256 `6a3c8274…cb24eb`) | green | **0** | `SUITE verdict=PASS fixtures=46 failed=0 -` | — |
| inserted unused module-level assignment (`green/assign.py`, sha256 `4e0e27f5…c856dd7c`) | green | **0** | `SUITE verdict=PASS fixtures=46 failed=0 -` | — |
| M1 `case-overcount` | kill | **1** | `SUITE verdict=FAIL fixtures=46 failed=1 red-case-indented-not-a-case-line` | `red-case-indented-not-a-case-line` |
| M2 `duplicate-total` | kill | **1** | `SUITE verdict=FAIL fixtures=46 failed=1 exit2-registration-same-predicate-different-totals` | `exit2-registration-same-predicate-different-totals` |
| M3 `summary-numerator` | kill | **1** | `SUITE verdict=FAIL fixtures=46 failed=1 green-numerator-not-compared` | `green-numerator-not-compared` |

Each kill is attributable to exactly one fixture and the three killer fixtures are distinct, one
from each direction the suite must police (a red disagreement, an exit-2 registration, and a
green fixture that must not be over-rejected). The killer lines verbatim:

```
SUITE fixture=red-case-indented-not-a-case-line status=FAIL want=1 rc=0 verdict=0 legs=- final='exit=0' mentions=red-case-indented-not-a-case-line.receipt0.txt:1/1
SUITE fixture=exit2-registration-same-predicate-different-totals status=FAIL want=2 rc=1 verdict=1 legs=case_lines,denominator final='exit=1' mentions=exit2-registration-same-predicate-different-totals.receipt0.txt:1/0
SUITE fixture=green-numerator-not-compared status=FAIL want=0 rc=1 verdict=1 legs=denominator final='exit=1' mentions=green-numerator-not-compared.receipt0.txt:1/1
```

Raw logs: `/fast/scratch/hyaku/mado-r27/repair/MutSuiteB/runs/<subject>.txt`.

### Supplementary probe (not one of the three)

A first, coarser `case-overcount` instance
(`supplementary/case-overcount-coarse.py`, sha256 `9521fcd9…ec1322`) counted any line containing
`CASE` case-insensitively. Also killed (`rc=1`, 20 fixtures failed, because `cases_pass` itself
contains `CASE`). It was replaced by M1 above so that the scored kill is single-defect and
attributable; the coarse run is kept only as extra evidence.

## Limits

* These are my own instances of three of the six disclosed class names
  (`case-overcount`, `duplicate-total`, `summary-numerator`); the sealed HeldChk bytes were not
  read and are not claimed to be reproduced. The other three classes (`case-tab`,
  `unreadable-precedence`, `mismatch-exit`) were not probed by this seat, so this receipt raises
  confidence in suite B's discrimination but makes no claim about `h_killed`.
* The suite exercises the checker's documented contract over 46 built-in fixtures; a mutation
  confined to regions no fixture reaches (e.g. argument parsing) can survive and would be a
  coverage finding, not a contract change. None of the three probes landed there.

## Cleanup / host safety

* No tool or package installed or updated; no `pacman` transaction was run.
* No Hyprland, compositor, display variable or network was touched; every command was
  `timeout`- and `prlimit`-bounded (4 GB) and ran under `env -i`.
* The lane was never written: `quality/population-suite.py` and
  `.ufo/waves/round-26/quality/check-population.py` still hash to `99e7d876…` and `803e0096…`
  after all runs. The clone is a scratch copy; the subject inside it was only ever read
  (`sha256` unchanged before and after). The suite removed its own scratch (`tmp/` empty).
* Lane writes: this report only. All candidate bytes live under
  `/fast/scratch/hyaku/mado-r27/repair/MutSuiteB/`.

Report: .ufo/waves/round-27/w4/reports/MutSuiteB.md
