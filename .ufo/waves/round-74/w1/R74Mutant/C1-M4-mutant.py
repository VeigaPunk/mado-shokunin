#!/usr/bin/env python3
r"""Round-74 C1 successor rule: the landing kill credit requires the run's own witness of the
counter's per-run challenge (round-74 claim C1).

    python3 quality/counters/c1-r74-witness-rule.py --selftest --scratch-root DIR

The rule, frozen by `.ufo/waves/round-74/claims-declaration-r74.md` § C1:

    credit(out, nonce) is True iff the round-72 arithmetic holds (the LAST parsed
    `MADO_LANDING_COUNTERS_SELFTEST: <p>/<n> assertions passed` line reports `n > 0` and
    `p < n`, and the run's own `SELFTEST FAIL <i>: ` lines number exactly `n - p`) AND the LAST
    parsed `MADO_LANDING_WITNESS: <16 hex>` line equals the caller-supplied `nonce`.

Why a witness. The round-72 rule bounds the summary to the run's own fail lines but cannot tell
a fresh run from a captured block replayed with its own matching detail lines (the rule's own
declared limit). A challenge the caller generates per run and hands to the child cannot appear in
a previously captured block, so requiring the child to echo it separates the two — the same
reason a verifier-chosen token authenticates a response (CPython 3.14.8 `Doc/library/secrets.rst`,
row S450).

Both captured streams are read, as in round 72. The last parsed summary wins over a malformed
trailing marker, and the last parsed witness wins over an earlier one.

Declared limits. The challenge authenticates the run's echo, not the truth of the assertions: a
child that echoes the challenge and reports arithmetic it did not perform still passes the
arithmetic check the rule is built on. The rule is a standalone instrument; the frozen round-72
harness is not edited by this round.

Exit map for --selftest: 0 iff every assertion passes, 2 on usage/setup error.
"""
import argparse
import os
import re
import sys

SUMMARY_RE = re.compile(r"MADO_LANDING_COUNTERS_SELFTEST: (\d+)/(\d+) assertions passed")
WITNESS_RE = re.compile(r"MADO_LANDING_WITNESS: ([0-9a-f]{16})")
FAIL_RE = re.compile(r"SELFTEST FAIL [0-9]+: ")
UNSAFE_ROOTS = ("/tmp", "/var/tmp", "/dev/shm")


class UsageError(Exception):
    pass


def last_parsed_summary(out):
    """The LAST summary line that fully parses; a malformed later marker cannot suppress it."""
    for line in reversed(out.splitlines()):
        if SUMMARY_RE.fullmatch(line.strip()):
            return line.strip()
    return ""


def count_fails(out):
    """The production emitter's own grammar (`SELFTEST FAIL <index>: ...`), not a prefix family."""
    return sum(1 for line in out.splitlines() if FAIL_RE.match(line))


def last_witness(out):
    """The LAST parsed witness token, else None; a malformed later witness line is ignored."""
    token = None
    for line in out.splitlines():
        m = WITNESS_RE.fullmatch(line.strip())
        if m:
            token = m.group(1)
    return token


def credit(out, nonce):
    """Round-74 C1: the round-72 arithmetic plus the run's echo of the caller's challenge."""
    line = last_parsed_summary(out)
    m = SUMMARY_RE.fullmatch(line)
    if not m:
        return False
    passed, total = int(m.group(1)), int(m.group(2))
    if total <= 0 or passed >= total:
        return False
    token = last_witness(out)
    return token is not None and token == nonce


def absolute_scratch(value):
    if not value:
        raise UsageError("--scratch-root is required")
    root = os.path.realpath(os.path.abspath(value))
    if not os.path.isdir(root):
        raise UsageError("--scratch-root is not a directory: %s" % value)
    if os.path.islink(os.path.abspath(value)):
        raise UsageError("--scratch-root must not be a symlink")
    norm = os.path.normcase(root)
    for unsafe in UNSAFE_ROOTS:
        if norm == unsafe or norm.startswith(unsafe + os.sep):
            raise UsageError("--scratch-root under %s is refused" % unsafe)
    return root


NONCE = "a1b2c3d4e5f60718"
STALE = "0123456789abcdef"
TABLE = (
    # name, output, expect
    ("genuine-failing", "MADO_LANDING_WITNESS: %s\n"
                        "SELFTEST FAIL 1: zero citations refused want=1 got=0\n"
                        "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n" % NONCE, True),
    ("genuine-green", "MADO_LANDING_WITNESS: %s\n"
                      "MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\n" % NONCE, False),
    ("stale-witness", "MADO_LANDING_WITNESS: %s\n"
                      "SELFTEST FAIL 1: zero citations refused want=1 got=0\n"
                      "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n" % STALE, False),
    ("no-witness", "SELFTEST FAIL 1: zero citations refused want=1 got=0\n"
                   "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n", False),
    ("wrong-witness", "MADO_LANDING_WITNESS: deadbeefdeadbeef\n"
                      "SELFTEST FAIL 1: zero citations refused want=1 got=0\n"
                      "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n", False),
    ("last-witness-wins", "MADO_LANDING_WITNESS: %s\nMADO_LANDING_WITNESS: deadbeefdeadbeef\n"
                          "SELFTEST FAIL 1: zero citations refused want=1 got=0\n"
                          "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n" % NONCE,
     False),
    ("witness-only-detail", "MADO_LANDING_WITNESS: %s\n"
                            "SELFTEST FAIL 1: a\nSELFTEST FAIL 2: b\n"
                            "MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\n" % NONCE,
     True),
    ("detail-mismatch", "MADO_LANDING_WITNESS: %s\n"
                        "SELFTEST FAIL 1: a\nSELFTEST FAIL 2: b\nSELFTEST FAIL 3: c\n"
                        "MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\n" % NONCE, False),
    ("malformed-trailing-summary", "MADO_LANDING_WITNESS: %s\n"
                                   "SELFTEST FAIL 1: a\n"
                                   "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n"
                                   "MADO_LANDING_COUNTERS_SELFTEST: runner cleanup complete\n"
                                   % NONCE, True),
    ("zero-denominator", "MADO_LANDING_WITNESS: %s\n"
                         "MADO_LANDING_COUNTERS_SELFTEST: 0/0 assertions passed\n" % NONCE,
     False),
    ("uppercase-witness", "MADO_LANDING_WITNESS: %s\n"
                          "SELFTEST FAIL 1: a\n"
                          "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n"
                          % NONCE.upper(), False),
    ("witness-substring", "MADO_LANDING_WITNESS: %s\n"
                          "SELFTEST FAIL 1: a\n"
                          "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n"
                          % ("x" + NONCE), False),
)


def selftest(scratch):
    checks = []

    def want(name, cond):
        checks.append((name, bool(cond)))

    want("twelve rule cases", len(TABLE) == 12)
    for name, out, expect in TABLE:
        want("credit %s is %s" % (name, expect), credit(out, NONCE) is expect)
    want("a bare summary with a witness is still refused",
         not credit("MADO_LANDING_WITNESS: %s\n"
                    "MADO_LANDING_COUNTERS_SELFTEST: 0/2 assertions passed\n" % NONCE, NONCE))
    want("a captured block with a witness is refused",
         not credit("MADO_LANDING_WITNESS: %s\nSELFTEST FAIL 1: a\n"
                    "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n" % STALE, NONCE))
    want("the last parsed summary is the decision",
         last_parsed_summary("MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n"
                             "MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed\n")
         == "MADO_LANDING_COUNTERS_SELFTEST: 2/2 assertions passed")
    want("a malformed trailing marker is not a summary",
         last_parsed_summary("MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed\n"
                             "MADO_LANDING_COUNTERS_SELFTEST: cleanup\n")
         == "MADO_LANDING_COUNTERS_SELFTEST: 1/2 assertions passed")
    want("the witness grammar is 16 lowercase hex",
         last_witness("MADO_LANDING_WITNESS: deadbeefdeadbeef\n") == "deadbeefdeadbeef"
         and last_witness("MADO_LANDING_WITNESS: nothex\n") is None
         and last_witness("MADO_LANDING_WITNESS: deadbeefdeadbeef0\n") is None)
    want("the fail grammar is the production emitter's",
         count_fails("SELFTEST FAILURE: wrapper\nSELFTEST FAIL 2: a\n") == 1)
    want("scratch refuses /tmp", _refuses("/tmp/whatever"))
    want("scratch accepts a real directory", absolute_scratch(scratch) == os.path.realpath(scratch))
    passed = sum(1 for _n, ok in checks if ok)
    for name, ok in checks:
        if not ok:
            print("MADO_R74_WITNESS_RULE_SELFTEST FAIL: %s" % name)
    print("MADO_R74_WITNESS_RULE_SELFTEST: %d/%d assertions passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


def _refuses(path):
    try:
        absolute_scratch(path)
    except UsageError:
        return True
    return False


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--scratch-root", dest="scratch_root")
    args = parser.parse_args(argv)
    try:
        scratch = absolute_scratch(args.scratch_root)
    except UsageError as exc:
        sys.stderr.write("c1-r74-witness-rule.py: %s\n" % exc)
        return 2
    if args.selftest:
        return selftest(scratch)
    sys.stderr.write("c1-r74-witness-rule.py: only --selftest is supported here\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
