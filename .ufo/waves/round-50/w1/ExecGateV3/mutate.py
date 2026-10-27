#!/usr/bin/env python3
"""Mutation harness for the v3 draft: remove one rule, show what fails.

Usage: mutate.py GATE SCRATCH

For each of R7/R8/R9 this writes a copy of *GATE* under *SCRATCH* with that
rule's block in ``scan_blob()`` deleted (the only change), runs the copy's
``--selftest``, and prints which cases flipped. A rule is "able to fail" when
its red cases all fail with the block removed and its green counter-cases all
still pass. Nothing is written outside *SCRATCH*.
"""
import os
import subprocess
import sys

GATE = os.path.abspath(sys.argv[1])
SCRATCH = os.path.abspath(sys.argv[2])

R7 = "R7_HOME_PATH_PREFIX"
R8 = "R8_ACCOUNT_COLUMN"
R9 = "R9_EXEC_CACHE"

BLOCKS = {
    R7: (
        "    forms, paths = scan_home_prefixes(text)\n"
        "    total = sum(forms.values())\n"
        "    if total:\n"
        '        findings.append((R7, total, "forms=prefix:%d,header:%d,diag:%d,row:%d paths=%d"\n'
        '                         % (forms["prefix"], forms["header"], forms["diag"],\n'
        '                            forms["row"], paths)))\n'
    ),
    R8: (
        "    rows = scan_account_columns(text, account)\n"
        "    if rows:\n"
        '        findings.append((R8, rows, "rows=%d" % rows))\n'
    ),
    R9: (
        "    count, keys = scan_cache_fields(text, cache_fields)\n"
        "    if count:\n"
        '        findings.append((R9, count, "fields=%d keys=%s"\n'
        '                         % (count, "+".join(sorted(keys)))))\n'
    ),
}

RED = {
    R7: [
        "r7-grep-prefix-located-lines",
        "r7-detail-names-forms-only",
        "r7-flat-listing-header",
        "r7-quoted-path-in-diagnostic",
        "r7-home-path-in-ls-row",
        "waiver-new-band-fixture-waived",
        "waiver-r7-real-user-rejected",
    ],
    R8: [
        "r8-owner-and-group-column",
        "r8-detail-counts-only",
        "v3-cli-default-scope-and-account-silent",
        "waiver-new-band-fixture-waived",
    ],
    R9: [
        "r9-cache-record-fields",
        "r9-detail-counts-only",
        "waiver-new-band-fixture-waived",
        "waiver-r9-real-title-rejected",
    ],
}

GREEN = {
    R7: [
        "r7-tilde-and-dollar-home-forms-clean",
        "r7-path-quoted-in-prose-clean",
        "r7-diagnostic-shape-in-prose-clean",
    ],
    R8: [
        "r8-numeric-ids-clean",
        "r8-other-owner-clean",
        "r8-unresolved-account-inert",
    ],
    R9: [
        "r9-flag-prose-and-indented-usage-clean",
        "r9-one-field-under-threshold-clean",
        "r9-record-is-not-a-home-listing",
    ],
}


def run_selftest(path, workdir):
    env = dict(os.environ)
    env["TMPDIR"] = workdir
    proc = subprocess.run(
        [sys.executable, "-I", path, "--selftest"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, timeout=600,
    )
    failed, passed, total, summary = set(), set(), 0, ""
    for line in proc.stdout.decode("utf-8", "replace").splitlines():
        if line.startswith("SELFTEST FAIL case="):
            failed.add(line.split("case=", 1)[1].split(" ", 1)[0])
        elif line.startswith("SELFTEST ok case="):
            passed.add(line.split("case=", 1)[1].split(" ", 1)[0])
        elif line.startswith("SELFTEST:"):
            summary = line
    total = len(passed) + len(failed)
    return failed, passed, total, summary, proc.returncode


def main():
    source = open(GATE, encoding="utf-8").read()
    os.makedirs(SCRATCH, exist_ok=True)
    verdicts = []
    for rule in (R7, R8, R9):
        block = BLOCKS[rule]
        if source.count(block) != 1:
            print("MUTANT %s BLOCK-NOT-UNIQUE count=%d" % (rule, source.count(block)))
            verdicts.append(False)
            continue
        mutant = source.replace(block, "    # MUTATION: %s removed\n" % rule)
        path = os.path.join(SCRATCH, "mutant-%s.py" % rule.lower())
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(mutant)
        failed, passed, total, summary, code = run_selftest(path, SCRATCH)
        red_missed = [case for case in RED[rule] if case not in failed]
        green_broken = [case for case in GREEN[rule] if case in failed]
        print("MUTANT rule=%s file=%s" % (rule, os.path.basename(path)))
        print("  %s" % summary)
        print("  red_cases_that_failed=%d/%d" % (len(RED[rule]) - len(red_missed), len(RED[rule])))
        print("  failed_cases=%s" % ",".join(sorted(failed)))
        print("  red_missed=%s" % (",".join(red_missed) or "-"))
        print("  green_broken=%s" % (",".join(green_broken) or "-"))
        print("  ok=%s" % (not red_missed and not green_broken))
        verdicts.append(not red_missed and not green_broken)
    print("MUTATION: rules=3 ok=%d failed=%d"
          % (sum(1 for v in verdicts if v), sum(1 for v in verdicts if not v)))
    return 0 if all(verdicts) else 1


sys.exit(main())
