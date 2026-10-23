#!/usr/bin/env python3
"""Round-26 quality check for QUALITY criterion 37 (round-25 routed defect 3, M25-4):
a predicate's population equals its counter's population.

Usage:
    python3 -I check-population.py --registration PATH RECEIPT [RECEIPT ...]

Reads the registration and every named receipt as UTF-8 text; writes nothing; runs no tool.

Rule (one sentence): exit 0 only if, for each `PRED-<id> ... cases_pass=<n>/<T>` summary a receipt
prints, the receipt's denominator T, its count of lines starting with `CASE ` and the target total T
stated for the same `PRED-<id>` sentence in the registration are equal; exit 1 when any of the three
disagrees, or when a receipt names a predicate the registration states no total for; exit 2 when the
registration or a receipt cannot be read, or carries no population to compare.

Definitions
  registration sentence
      a blank-line-delimited paragraph of the registration carrying a `**PRED-<id>**` marker; its
      stated total is the denominator T of its unique `cases_pass=<n>/<T>` occurrence. Two different
      totals in one sentence, or one sentence naming several predicates beside one total, cannot be
      attributed and are exit 2.
  receipt summary
      a line starting with `PRED-<id>` and containing `cases_pass=<n>/<T>`; a counter prints one
      such line, after all its case lines (round-26 counters print `CASE <label> PASS|FAIL ...`).
  CASE line
      a line starting with `CASE ` or `CASE<TAB>`: one per case the counter built and measured.

Why (M25-4)
-----------
A predicate's registered target is a claim about its case population, but the counter prints its own
denominator and its own case lines; nothing compared the three, so a generator that built fewer cases
than the registration stated could still print a self-consistent-looking receipt. This check binds the
number the registration promises, the number the counter prints and the number of case lines the
receipt carries to one value, all readable from bytes without executing the counter.

Exit: 0 all agree, 1 any disagreement, 2 unreadable/unevaluable input. Final line is `exit=<n>`.
"""
import argparse
import re
import sys

PRED_MARK = re.compile(r"\*\*(PRED-[A-Za-z0-9._-]+)\*\*")
TOTAL = re.compile(r"cases_pass=(\d+)/(\d+)")
SUMMARY = re.compile(r"^[ \t]*(PRED-[A-Za-z0-9._-]+)\b[^\n]*?cases_pass=(\d+)/(\d+)")
CASE_LINE = re.compile(r"^CASE[ \t]")


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_registration(text):
    """Return ({pred: total}, [problem]) from blank-line-delimited registration paragraphs."""
    populations = {}
    problems = []
    for para in re.split(r"\n[ \t]*\n", text):
        labels = []
        for m in PRED_MARK.finditer(para):
            if m.group(1) not in labels:
                labels.append(m.group(1))
        if not labels:
            continue
        totals = {int(m.group(2)) for m in TOTAL.finditer(para)}
        if len(labels) != 1:
            problems.append("paragraph names %d predicates beside %d total(s): %s"
                            % (len(labels), len(totals), ",".join(labels)))
            continue
        if len(totals) != 1:
            problems.append("predicate %s states %d distinct totals (%s)"
                            % (labels[0], len(totals),
                               ",".join(str(t) for t in sorted(totals)) or "none"))
            continue
        total = totals.pop()
        if labels[0] in populations and populations[labels[0]] != total:
            problems.append("predicate %s stated twice with different totals (%d, %d)"
                            % (labels[0], populations[labels[0]], total))
            continue
        populations[labels[0]] = total
    return populations, problems


def main():
    ap = argparse.ArgumentParser(
        description="Check that each receipt predicate population equals its registration target.")
    ap.add_argument("--registration", required=True, metavar="PATH",
                    help="lane registration file holding the predicate sentence(s)")
    ap.add_argument("receipts", nargs="+", metavar="RECEIPT",
                    help="counter receipt file(s) to check")
    args = ap.parse_args()

    try:
        reg_text = read_text(args.registration)
    except (OSError, UnicodeError) as exc:
        print("POPULATION verdict=UNREADABLE registration=%s error=%s"
              % (args.registration, exc.__class__.__name__))
        print("exit=2")
        return 2

    populations, problems = parse_registration(reg_text)
    if problems:
        for problem in problems:
            print("POPULATION verdict=UNREADABLE registration=%s reason=%s"
                  % (args.registration, problem))
        print("exit=2")
        return 2
    if not populations:
        print("POPULATION verdict=UNREADABLE registration=%s "
              "reason=no **PRED-...** sentence with a cases_pass=N/T total" % args.registration)
        print("exit=2")
        return 2
    print("POPULATION registration=%s predicates=%s"
          % (args.registration, ",".join(sorted(populations))))

    unreadable = 0
    mismatch = 0
    agreed = 0
    for path in args.receipts:
        try:
            text = read_text(path)
        except (OSError, UnicodeError) as exc:
            unreadable += 1
            print("POPULATION receipt=%s verdict=UNREADABLE error=%s"
                  % (path, exc.__class__.__name__))
            continue
        lines = text.splitlines()
        summaries = []
        for line in lines:
            m = SUMMARY.match(line)
            if m:
                summaries.append((m.group(1), int(m.group(2)), int(m.group(3))))
        if not summaries:
            unreadable += 1
            print("POPULATION receipt=%s verdict=UNREADABLE "
                  "reason=no PRED-... cases_pass=N/T summary line" % path)
            continue
        case_lines = sum(1 for line in lines if CASE_LINE.match(line))
        for pred, num, den in summaries:
            if pred not in populations:
                mismatch += 1
                print("POPULATION receipt=%s pred=%s cases_pass=%d/%d case_lines=%d "
                      "registered=- agree=MISMATCH legs=registration_total"
                      % (path, pred, num, den, case_lines))
                continue
            registered = populations[pred]
            legs = []
            if case_lines != registered:
                legs.append("case_lines")
            if den != registered:
                legs.append("denominator")
            if legs:
                mismatch += 1
                print("POPULATION receipt=%s pred=%s cases_pass=%d/%d case_lines=%d "
                      "registered=%d agree=MISMATCH legs=%s"
                      % (path, pred, num, den, case_lines, registered, ",".join(legs)))
            else:
                agreed += 1
                print("POPULATION receipt=%s pred=%s cases_pass=%d/%d case_lines=%d "
                      "registered=%d agree=ok"
                      % (path, pred, num, den, case_lines, registered))

    if unreadable:
        verdict, rc = "UNREADABLE", 2
    elif mismatch:
        verdict, rc = "FAIL", 1
    else:
        verdict, rc = "PASS", 0
    print("POPULATION verdict=%s receipts=%d agree=%d mismatch=%d unreadable=%d"
          % (verdict, len(args.receipts), agreed, mismatch, unreadable))
    print("exit=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
