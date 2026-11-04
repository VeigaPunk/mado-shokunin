#!/usr/bin/env python3
"""One-shot builder for quality/counters/c1-r72-landing-controls.py from the r71 generation.

Not a round artifact; the committed harness is the output. Every replacement asserts a unique
site so a drift in the r71 file stops the build instead of silently mis-editing.
"""
import pathlib
import re
import sys

SRC = pathlib.Path("quality/counters/c1-r71-landing-controls.py")
DST = pathlib.Path("quality/counters/c1-r72-landing-controls.py")

DOC = '''#!/usr/bin/env python3
r"""Round-72 C1/C2 successor harness (round-71 generation plus two disjoint rule deltas).

The lane's harness chain is one file per round: `c1-r68` -> `c1-r69` -> `c1-r70` -> `c1-r71`
-> this file. The frozen generations are never edited; each successor differs only where its
round's claim says it does.

Delta D1 (round-72 C1, calibration) - the M-Z kill credit. The round-71 line credits any
parsed `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` with `p < n`. That credits
a summary line no assertion of this run produced (a bare echo) and a summary whose failure
count is not backed by the run's own `SELFTEST FAIL` lines. This file's `credit(out)` requires
the LAST parsed summary to report `p < n` with `n > 0` AND the run's own `SELFTEST FAIL` lines
to number exactly `n - p`. Both captured streams are read, as in round 71.

Delta D2 (round-72 C2, operability) - the contract outcome. The round-71 line greens the run
whenever the extracted instrument's `--selftest` exits 0 (`outcome_exit(selftest_rc, killed)`),
whatever its summary says. This file's `outcome_exit`/`outcome_verdict` read the LAST parsed
`MADO_LANDING_COUNTERS_SELFTEST: <p>/<n>` summary of that run: green iff `n > 0` and `p == n`;
a missing or garbled summary is not green; the kill count still requires 2/2. The exit status
is printed as evidence and no longer gates the outcome.

    python3 quality/counters/c1-r72-landing-controls.py --repo . --rev REV --scratch-root DIR
    python3 quality/counters/c1-r72-landing-controls.py --selftest --scratch-root DIR

Exit map: 0 iff the extracted instrument's own summary is green AND both frozen defect mutants
are killed (2/2); 1 iff the measurement ran and the contract was not met; 2 on usage/setup error
- reason on stderr, no contract line printed.

What one measurement does (every write stays under the caller-declared scratch root):

  extract  the four instrument files at --rev into <scratch>/r72-c1/tree/ with a scrubbed git
           env carrying GIT_OPTIONAL_LOCKS=0 and GIT_NO_REPLACE_OBJECTS=1:
             quality/landing-counters.sh
             quality/counters/c3-r56-used-by.py
             quality/check-tool-ledger.py
             tools/mado-receipt-citecheck.py
  selftest run the extracted landing instrument `--selftest`; its last summary is scored, not
           its exit status (D2).
  M-Z      copy the tree, delete the exact frozen zero-citation guard clause
           `[ "$citations" -gt 0 ] && ` once (asserting exactly one occurrence first; the
           mutant must still pass `bash -n`), and re-run `--selftest`: the mutation is killed
           iff `credit()` accepts that output (D1).
  M-R      the round-69/70/71 replacement-ref pair, unchanged: the unmutated child must read
           the real tree (rc 1, TARGET_MISSED, missing=1) and the guard-removed mutant must
           credit the forged tree (rc 0, TARGET_MET).

Printed receipt (last line, exact):

    MADO_R72_LANDING_CONTROLS: selftest=<p/n|none> mz=<pass|fail> mr=<pass|fail> killed=<n>/2 baseline=0/2 verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Preceded by one `MADO_R72_*` evidence line per extraction, mutant (with its sha256), R-control
leg, and the exact environment handed to the child under test. Mutant bytes are never claimed
killed when the recipe was inapplicable: a missing guard yields `recipe=none killed=no`.

Selftest: `--selftest` is hermetic - it spawns nothing, touches only <scratch-root>, and
refuses /tmp-family or symlinked roots. It drives the real `measure()` body with scripted
children (git, bash and python answered in-process) so both rules and the printed contract line
are exercised without a child, and asserts each rule's own decision table.

Declared limits: the credit rule reads the child's own report, it does not authenticate it - a
captured summary replayed with its own matching detail lines remains byte-indistinguishable
from a genuine run; the arithmetic check bounds the summary to the run's own fail lines, not to
the truth of those lines. A crash, a missing child or a garbled summary earns no credit, and a
green summary with a nonzero exit (or a failing summary with exit 0) is scored by the summary -
the exit status cannot carry the assertion result (held ground S441/S435/S444/S445). The
scripted selftest cases use stand-ins; the real-child evidence lives in the round counters
`quality/counters/c1-r72-summary-credit.py` and `quality/counters/c2-r72-outcome.py`.
"""'''

text = SRC.read_text()


def sub(old, new, count=1):
    global text
    n = text.count(old)
    if n != count:
        sys.exit("site %r found %d times (want %d)" % (old[:60], n, count))
    text = text.replace(old, new)


# --- docstring
start = text.index('#!/usr/bin/env python3')
opener = text.index('r"""', start) + 4
end = text.index('"""', opener) + 3
text = text[:start] + DOC + text[end:]

sub('TOOL = "c1-r71-landing-controls.py"', 'TOOL = "c1-r72-landing-controls.py"')
text = text.replace("MADO_R71_", "MADO_R72_")
sub('os.path.join(scratch, "r71-c1")', 'os.path.join(scratch, "r72-c1")')
sub('os.path.join(scratch, "r71-c1-selftest")', 'os.path.join(scratch, "r72-c1-selftest")')

# --- credit rule (D1)
sub('''def describe_env(env):''', '''def credit(out):
    """Round-72 D1: the kill is credited on the run's own failed assertions, not a summary line.

    True iff the LAST parsed summary reports `p < n` with `n > 0` AND the run's own
    `SELFTEST FAIL` lines number exactly `n - p`. A bare/replayed summary line, a summary whose
    detail does not add up, a crash and a garbled summary all earn no credit.
    """
    line = last_summary(out)
    m = re.fullmatch(r"MADO_LANDING_COUNTERS_SELFTEST: (\\d+)/(\\d+) assertions passed", line)
    if not m:
        return False
    passed, total = int(m.group(1)), int(m.group(2))
    if total <= 0 or passed >= total:
        return False
    return count_fails(out) == total - passed


def summary_green(out):
    """Round-72 D2: green iff the LAST parsed summary has n > 0 and p == n."""
    line = last_summary(out)
    m = re.fullmatch(r"MADO_LANDING_COUNTERS_SELFTEST: (\\d+)/(\\d+) assertions passed", line)
    if not m:
        return False
    passed, total = int(m.group(1)), int(m.group(2))
    return total > 0 and passed == total


def describe_env(env):''')

# --- outcome rule (D2)
sub('''def outcome_exit(selftest_rc, killed):
    return 0 if selftest_rc == 0 and killed == 2 else 1


def outcome_verdict(selftest_rc, killed):
    return "TARGET_MET" if selftest_rc == 0 and killed == 2 else "TARGET_MISSED"


def contract_line(selftest_rc, mz, mr, killed, rev):
    return ("MADO_R72_LANDING_CONTROLS: selftest=%d mz=%s mr=%s killed=%d/2 baseline=%s "
            "verdict=%s rev=%s" % (selftest_rc, mz, mr, killed, BASELINE,
                                   outcome_verdict(selftest_rc, killed), rev))''',
'''def outcome_exit(selftest_out, killed):
    return 0 if summary_green(selftest_out) and killed == 2 else 1


def outcome_verdict(selftest_out, killed):
    return "TARGET_MET" if summary_green(selftest_out) and killed == 2 else "TARGET_MISSED"


def contract_line(selftest_out, mz, mr, killed, rev):
    return ("MADO_R72_LANDING_CONTROLS: selftest=%s mz=%s mr=%s killed=%d/2 baseline=%s "
            "verdict=%s rev=%s" % (summary_fraction(selftest_out), mz, mr, killed, BASELINE,
                                   outcome_verdict(selftest_out, killed), rev))''')

sub('''    selftest_rc = r.returncode
    emit("MADO_R72_SELFTEST instrument=%s rc=%d assertions=%s"
         % (LANE, selftest_rc, summary_fraction(dec(r.stdout) + dec(r.stderr))))''',
'''    selftest_rc = r.returncode
    selftest_out = dec(r.stdout) + dec(r.stderr)
    emit("MADO_R72_SELFTEST instrument=%s rc=%d summary=%s green=%s"
         % (LANE, selftest_rc, summary_fraction(selftest_out),
            "yes" if summary_green(selftest_out) else "no"))''')

sub('        mz_killed = bool(summary_shows_failure(mz_out))',
    '        mz_killed = bool(credit(mz_out))')
sub('''    emit(contract_line(selftest_rc, "pass" if mz_killed else "fail",
                       "pass" if mr_killed else "fail", killed, sha))
    return outcome_exit(selftest_rc, killed)''',
'''    emit(contract_line(selftest_out, "pass" if mz_killed else "fail",
                       "pass" if mr_killed else "fail", killed, sha))
    return outcome_exit(selftest_out, killed)''')

# --- regex for the contract line
old_re = re.search(r'CONTRACT_RE = re\.compile\(\n(?:.*\n)*?\)\n', text).group(0)
new_re = ('CONTRACT_RE = re.compile(\n'
          '    r"MADO_R72_LANDING_CONTROLS: selftest=(?:[0-9]+/[0-9]+|none) '
          'mz=(?:pass|fail) mr=(?:pass|fail) "\n'
          '    r"killed=[0-2]/2 baseline=0/2 verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}"\n'
          ')\n')
text = text.replace(old_re, new_re)

DST.write_text(text)
print("wrote", DST, len(text), "bytes")
