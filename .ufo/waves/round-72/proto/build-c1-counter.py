#!/usr/bin/env python3
"""One-shot builder for quality/counters/c1-r72-summary-credit.py from the r71 counter."""
import pathlib
import re
import sys

SRC = pathlib.Path("quality/counters/c1-r71-real-children.py")
DST = pathlib.Path("quality/counters/c1-r72-summary-credit.py")
text = SRC.read_text()


def sub(old, new, count=1):
    global text
    n = text.count(old)
    if n != count:
        sys.exit("site %r x%d (want %d)" % (old[:70], n, count))
    text = text.replace(old, new)


DOC = '''#!/usr/bin/env python3
r"""Round-72 C1 counting command: the landing kill credit requires the run's own failure detail
(claim C1, round 72).

    python3 quality/counters/c1-r72-summary-credit.py --repo . --rev REV \\
        --base-rev 976684a27e99c2508037a60eec415f550f53d70e --scratch-root DIR
    python3 quality/counters/c1-r72-summary-credit.py --selftest --scratch-root DIR

What is scored. The round-71 credit line credits any parsed
`MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` with `p < n`. That credits a summary
line no assertion of this run produced (a bare echo) and a summary whose failure count is not
backed by the run's own `SELFTEST FAIL` lines. Round 72's `credit(out)` requires the LAST parsed
summary to report `p < n` with `n > 0` AND the run's own `SELFTEST FAIL` lines to number exactly
`n - p`; both captured streams are read, as in round 71.

Eight scenarios, each a REAL `bash` child built into a scratch git fixture; in every scenario the
harness's M-Z leg deletes the frozen clause `[ "$citations" -gt 0 ] && ` and runs the mutated
lane:

  carried (round-71 set, expectations unchanged):
  liar-success    genuine `1/2` summary, exit 0                          -> pass
  stderr-genuine  the genuine `1/2` summary on stderr only, exit 1       -> pass
  liar-kill       `2/2` summary with an unrelated exit 1                 -> fail
  crash-stderr    exit 2 with stderr noise and no summary                -> fail
  new (round-72 D1):
  bare-failing    a `0/2` summary line and no `SELFTEST FAIL` line       -> fail
  mismatch-detail a `0/2` summary beside three `SELFTEST FAIL` lines     -> fail
  last-wins-pass  a `1/2` block, then `2/2` last                          -> fail
  last-wins-fail  a `2/2` line, then one fail line and `1/2` last         -> pass

Both harnesses run against the same fixture: the candidate at `--rev` (round 72) and the frozen
round-71 harness at `--base-rev` (the do-nothing control). The control must score exactly 6/8;
the candidate must score 8/8. Every write stays under the caller-declared scratch root, which
refuses /tmp-family and symlinked roots.

Printed receipt (last line, exact):

    MADO_R72_SUMMARY_CREDIT: cases=8 correct=<n> base_correct=<m> verdict=<TARGET_MET|TARGET_MISSED> rev=<sha>

Exit 0 iff correct == 8 and base_correct == 6; 1 iff the measurement ran and missed (the
candidate harness absent at `--rev` prints `correct=absent`); 2 on usage/setup error, with the
reason on stderr and no contract line.

Selftest: `--selftest` is hermetic - it spawns nothing, touches only <scratch-root>, and drives
the decision functions (marker parse, scoring, verdict) plus the fixture lane template's
structural invariants. It does not claim that a real bash child behaves as the fixture says; the
measurement itself runs those.

Declared limits: the eight scenarios are fixture lanes, not a fault-coverage claim; the fixture
is the counter's own instrument and is not the lane's real landing instrument; a captured summary
replayed with its own matching detail lines remains byte-indistinguishable from a genuine run -
the rule bounds the summary to the run's own fail lines, it does not authenticate them.
"""'''

start = text.index('#!/usr/bin/env python3')
opener = text.index('r"""', start) + 4
end = text.index('"""', opener) + 3
text = text[:start] + DOC + text[end:]

sub('TOOL = "c1-r71-real-children.py"', 'TOOL = "c1-r72-summary-credit.py"')
sub('CANDIDATE = "quality/counters/c1-r71-landing-controls.py"',
    'CANDIDATE = "quality/counters/c1-r72-landing-controls.py"')
sub('BASE_HARNESS = "quality/counters/c1-r70-landing-controls.py"',
    'BASE_HARNESS = "quality/counters/c1-r71-landing-controls.py"')
sub('CAND_PREFIX = "MADO_R71_LANDING_CONTROLS:"', 'CAND_PREFIX = "MADO_R72_LANDING_CONTROLS:"')
sub('''MODES = ("liar-success", "stderr-genuine", "liar-kill", "crash-stderr")
EXPECT = {"liar-success": "pass", "stderr-genuine": "pass",
          "liar-kill": "fail", "crash-stderr": "fail"}
FROZEN_CORRECT = 4
FROZEN_BASE_CORRECT = 3''',
'''MODES = ("liar-success", "stderr-genuine", "liar-kill", "crash-stderr",
         "bare-failing", "mismatch-detail", "last-wins-pass", "last-wins-fail")
EXPECT = {"liar-success": "pass", "stderr-genuine": "pass",
          "liar-kill": "fail", "crash-stderr": "fail",
          "bare-failing": "fail", "mismatch-detail": "fail",
          "last-wins-pass": "fail", "last-wins-fail": "pass"}
FROZEN_CORRECT = 8
FROZEN_BASE_CORRECT = 6''')

# fixture lane: swap the mode branch
sub('''    crash-stderr) printf 'fatal: assertion harness collapsed before any summary\\\\n' >&2; exit 2 ;;
  esac
fi
"""''',
'''    crash-stderr) printf 'fatal: assertion harness collapsed before any summary\\\\n' >&2; exit 2 ;;
    bare-failing) printf 'MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\\\\n'; exit 1 ;;
    mismatch-detail) printf 'SELFTEST FAIL 2: a want=1 got=0\\\\nSELFTEST FAIL 3: b want=1 got=0\\\\nSELFTEST FAIL 4: c want=1 got=0\\\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\\\\n'; exit 1 ;;
    last-wins-pass) check 'zero citations refused' 1 0; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\\\\n'; exit 1 ;;
    last-wins-fail) printf 'MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\\\\n'; printf 'SELFTEST FAIL 9: zero citations refused want=1 got=0\\\\n'; printf 'MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\\\\n'; exit 1 ;;
  esac
fi
"""''')

text = text.replace("MADO_R71_", "MADO_R72_")
sub('BASE_PREFIX = "MADO_R70_LANDING_CONTROLS:"', 'BASE_PREFIX = "MADO_R71_LANDING_CONTROLS:"')
text = text.replace("MADO_R72_REAL_CHILDREN_SELFTEST", "MADO_R72_SUMMARY_CREDIT_SELFTEST")
sub('os.path.join(scratch, "r71-c1")', 'os.path.join(scratch, "r72-c1")')
sub('os.path.join(scratch, "r71-c1-selftest")', 'os.path.join(scratch, "r72-c1-selftest")')

sub('''    return ("MADO_R72_REAL_CHILDREN: cases=4 correct=%s base_correct=%d verdict=%s rev=%s"''',
    '''    return ("MADO_R72_SUMMARY_CREDIT: cases=8 correct=%s base_correct=%d verdict=%s rev=%s"''')

i0 = text.index('CONTRACT_RE = re.compile(')
i1 = text.index('\nLANE_TEMPLATE', i0) + 1
old_re = text[i0:i1]
new_re = ('CONTRACT_RE = re.compile(\n'
          '    r"MADO_R72_SUMMARY_CREDIT: cases=8 correct=(?:absent|[0-8]) base_correct=[0-8] "\n'
          '    r"verdict=(?:TARGET_MET|TARGET_MISSED) rev=[0-9a-f]{40,64}")\n')
text = text.replace(old_re, new_re)

# --- replace the selftest body wholesale
body_start = text.index('def _selftest_checks(work):')
body_end = text.index('def _refuses(path):')
new_body = '''def _selftest_checks(work):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    want("candidate path is the round-72 harness",
         CANDIDATE.endswith("c1-r72-landing-controls.py"))
    want("base path is the frozen round-71 harness",
         BASE_HARNESS.endswith("c1-r71-landing-controls.py"))
    want("eight scenarios", MODES == (
        "liar-success", "stderr-genuine", "liar-kill", "crash-stderr",
        "bare-failing", "mismatch-detail", "last-wins-pass", "last-wins-fail"))
    want("expectations", EXPECT == {
        "liar-success": "pass", "stderr-genuine": "pass", "liar-kill": "fail",
        "crash-stderr": "fail", "bare-failing": "fail", "mismatch-detail": "fail",
        "last-wins-pass": "fail", "last-wins-fail": "pass"})
    want("frozen totals", FROZEN_CORRECT == 8 and FROZEN_BASE_CORRECT == 6)

    line = ("MADO_R72_LANDING_CONTROLS: selftest=62/62 mz=pass mr=pass killed=2/2 "
            "baseline=0/2 verdict=TARGET_MET rev=" + "a" * 40)
    base_line = ("MADO_R71_LANDING_CONTROLS: selftest=0 mz=pass mr=pass killed=2/2 "
                 "baseline=0/2 verdict=TARGET_MET rev=" + "a" * 40)
    want("candidate line parses pass", parse_mz(line, CAND_PREFIX) == "pass")
    want("base line parses pass", parse_mz(base_line, BASE_PREFIX) == "pass")
    want("prefixes do not cross-parse",
         parse_mz(base_line, CAND_PREFIX) is None and parse_mz(line, BASE_PREFIX) is None)
    want("crash line parses fail",
         parse_mz("MADO_R72_LANDING_CONTROLS: selftest=62/62 mz=fail mr=pass killed=1/2 "
                  "baseline=0/2 verdict=TARGET_MISSED rev=" + "a" * 40, CAND_PREFIX) == "fail")
    want("absent marker is none", parse_mz("boom\\n", CAND_PREFIX) is None)

    want("liar-success pass is correct", score("pass", "pass"))
    want("stderr-genuine pass is correct", score("pass", "pass"))
    want("liar-kill pass is a false credit", not score("fail", "pass"))
    want("bare-failing pass is a false credit", not score("fail", "pass"))
    want("mismatch-detail pass is a false credit", not score("fail", "pass"))
    want("last-wins-fail fail is a false rejection", not score("pass", "fail"))
    want("missing verdict is not correct", not score("pass", None))

    want("8/8 and base 6/8 is met", verdict_met(8, 6))
    want("7/8 is not met", not verdict_met(7, 6))
    want("base 7/8 is not met", not verdict_met(8, 7))
    want("base 5/8 is not met", not verdict_met(8, 5))

    want("contract line parses",
         CONTRACT_RE.fullmatch(contract_line(8, 6, "a" * 40)) is not None)
    want("miss line parses",
         CONTRACT_RE.fullmatch(contract_line(1, 6, "a" * 40)) is not None)
    want("absent line parses",
         CONTRACT_RE.fullmatch(contract_line(None, 0, "a" * 40)) is not None)
    want("met line is TARGET_MET",
         " verdict=TARGET_MET " in contract_line(8, 6, "a" * 40))
    want("base miss line is TARGET_MISSED",
         " verdict=TARGET_MISSED " in contract_line(8, 5, "a" * 40))

    lane = LANE_TEMPLATE.encode("utf-8")
    want("fixture lane carries the frozen clause exactly once", lane.count(Z_CLAUSE) == 1)
    want("fixture lane has one mode slot", lane.count(b"@MODE@") == 2)
    want("fixture lane pins the zero-citation assertion",
         b"check 'zero citations refused'" in lane)
    want("fixture lane carries all eight mode labels",
         all(("    %s)" % m).encode() in lane for m in MODES))
    want("fixture lane never refers to the counter", b"c1-r72-summary-credit" not in lane)

    want("scratch refuses /tmp", _refuses("/tmp/whatever"))
    want("scratch refuses a symlink", _refuses_symlink(work))
    return checks


'''
text = text[:body_start] + new_body + text[body_end:]
DST.write_text(text)
print("wrote", DST, len(text))
