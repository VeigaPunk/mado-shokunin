#!/usr/bin/env python3
"""Round-28 quality check for QUALITY criterion 37 (round-25 routed defect 3, M25-4):
a predicate's registered metrics agree with its counter's reported metrics and population.

Usage:
    python3 -I check-population.py --registration PATH RECEIPT [RECEIPT ...]

Reads the registration and every named receipt as UTF-8 text; writes nothing; runs no tool.

Rule: for every receipt PRED summary, the predicate must be registered and each target named
in its PRED paragraph must agree with the corresponding summary field. Targets support exact
numbers and ratios, `name=all` ratios, `name>=N/D` ratios, and
`name>=ceil(factor*other_metric)` ratios. For an exact `cases_pass=N/T` target, the receipt's
cases_pass numerator and denominator, CASE-line count and registered total must all agree.
Exit 1 means a disagreement, exit 2 means unreadable or unevaluable input.

Definitions
  registration sentence
      a blank-line-delimited paragraph carrying one `**PRED-<id>**` marker. Its target
      assignments (for example `green=all`, `cases_pass=41/41`, or
      `h_killed>=ceil(0.75*h_valid)`) define the fields checked in the receipt.
  receipt summary
      a line starting with `PRED-<id>` and carrying metric assignments; counters print it
      after their case lines.
  CASE line
      a line starting with `CASE ` or `CASE<TAB>`: one per case the counter built and measured.

Why (M25-4)
-----------
A predicate's registered target is a claim about its reported metrics and population, but a
counter prints its own values and case lines; nothing compared those values to the registration.
This check binds supported targets and, for exact cases_pass targets, the registered total,
receipt denominator and count of CASE lines without executing the counter.

Exit: 0 all agree, 1 any disagreement, 2 unreadable/unevaluable input. Final line is `exit=<n>`.
"""
import argparse
import re
import sys
from fractions import Fraction

PRED_MARK = re.compile(r"\*\*(PRED-[A-Za-z0-9._-]+)\*\*")
TARGET = re.compile(
    r"(?<![A-Za-z0-9_])(?P<name>[A-Za-z][A-Za-z0-9_]*)\s*(?P<op>>=|=)\s*"
    r"(?:(?P<all>all)\b|"
    r"(?P<ceil>ceil\s*\(\s*(?P<factor>\d+(?:\.\d+)?)\s*\*\s*"
    r"(?P<ref>[A-Za-z][A-Za-z0-9_]*)\s*\))|"
    r"(?P<num>\d+)(?:\s*/\s*(?P<den>\d+))?\b)"
)
SUMMARY = re.compile(r"^[ \t]*(PRED-[A-Za-z0-9._-]+)\b(.*)$")
FIELD = re.compile(
    r"(?<![A-Za-z0-9_])([A-Za-z][A-Za-z0-9_]*)\s*=\s*(\d+\s*/\s*\d+|\d+)\b"
)
CASE_LINE = re.compile(r"^CASE[ \t]")


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def target_from_match(match):
    """Return a normalized target, or raise ValueError for unsupported syntax."""
    op = match.group("op")
    if match.group("all"):
        if op != "=":
            raise ValueError("all requires =")
        return ("all",)
    if match.group("ceil"):
        if op != ">=":
            raise ValueError("ceil target requires >=")
        factor = Fraction(match.group("factor"))
        if factor < 0:
            raise ValueError("negative ceil factor")
        return ("ceil", factor.numerator, factor.denominator, match.group("ref"))
    num = int(match.group("num"))
    den = match.group("den")
    if den is not None:
        den = int(den)
        if den <= 0:
            raise ValueError("ratio denominator must be positive")
        return ("ratio" if op == "=" else "ratio_min", num, den)
    return ("number" if op == "=" else "number_min", num)


def parse_registration(text):
    """Return ({pred: {metric: target}}, [problem]) from registration paragraphs."""
    targets = {}
    problems = []
    for para in re.split(r"\n[ \t]*\n", text):
        labels = []
        for m in PRED_MARK.finditer(para):
            if m.group(1) not in labels:
                labels.append(m.group(1))
        if not labels:
            continue
        if len(labels) != 1:
            problems.append("paragraph names %d predicates: %s"
                            % (len(labels), ",".join(labels)))
            continue
        pred = labels[0]
        assignments = {}
        try:
            for match in TARGET.finditer(para):
                target = target_from_match(match)
                name = match.group("name")
                if name in assignments and assignments[name] != target:
                    raise ValueError("metric %s has conflicting targets" % name)
                assignments[name] = target
        except ValueError as exc:
            problems.append("predicate %s has invalid target: %s" % (pred, exc))
            continue
        if not assignments:
            problems.append("predicate %s has no supported target" % pred)
            continue
        if pred in targets:
            for name, target in assignments.items():
                if name in targets[pred] and targets[pred][name] != target:
                    problems.append("predicate %s metric %s has conflicting targets"
                                    % (pred, name))
                else:
                    targets[pred][name] = target
        else:
            targets[pred] = assignments
    return targets, problems


def parse_values(text):
    """Return each recognized summary field's parsed values, preserving duplicates."""
    values = {}
    for match in FIELD.finditer(text):
        raw = match.group(2).replace(" ", "")
        if "/" in raw:
            left, right = raw.split("/", 1)
            value = (int(left), int(right))
        else:
            value = int(raw)
        values.setdefault(match.group(1), []).append(value)
    return values


def render_value(value):
    if isinstance(value, tuple):
        return "%d/%d" % value
    return str(value)


def check_target(name, target, values, legs):
    actuals = values.get(name, [])
    if not actuals:
        legs.append("missing_%s" % name)
        return
    if len(actuals) != 1:
        legs.append("duplicate_%s" % name)
        return
    actual = actuals[0]
    kind = target[0]
    if kind == "all":
        if not isinstance(actual, tuple) or actual[0] != actual[1]:
            legs.append(name)
    elif kind == "ratio":
        if actual != target[1:]:
            legs.append(name)
    elif kind == "number":
        if actual != target[1]:
            legs.append(name)
    elif kind == "ratio_min":
        if (not isinstance(actual, tuple) or actual[1] <= 0
                or actual[0] * target[2] < target[1] * actual[1]):
            legs.append(name)
    elif kind == "number_min":
        if not isinstance(actual, int) or actual < target[1]:
            legs.append(name)
    elif kind == "ceil":
        ref_name = target[3]
        refs = values.get(ref_name, [])
        if not isinstance(actual, tuple) or actual[1] <= 0:
            legs.append(name)
        elif len(refs) != 1 or not isinstance(refs[0], int):
            legs.append("missing_%s" % ref_name)
        else:
            factor_num, factor_den = target[1], target[2]
            threshold = (factor_num * refs[0] + factor_den - 1) // factor_den
            if actual[1] != refs[0] or actual[0] < threshold:
                legs.append(name)


def main():
    ap = argparse.ArgumentParser(
        description="Check receipt predicate metrics and populations against registration targets.")
    ap.add_argument("--registration", required=True, metavar="PATH",
                    help="lane registration file holding predicate target sentences")
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

    targets, problems = parse_registration(reg_text)
    if problems:
        for problem in problems:
            print("POPULATION verdict=UNREADABLE registration=%s reason=%s"
                  % (args.registration, problem))
        print("exit=2")
        return 2
    if not targets:
        print("POPULATION verdict=UNREADABLE registration=%s "
              "reason=no **PRED-...** sentence with a supported target" % args.registration)
        print("exit=2")
        return 2
    print("POPULATION registration=%s predicates=%s"
          % (args.registration, ",".join(sorted(targets))))

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
            match = SUMMARY.match(line)
            if match:
                summaries.append((match.group(1), parse_values(match.group(2))))
        if not summaries:
            unreadable += 1
            print("POPULATION receipt=%s verdict=UNREADABLE "
                  "reason=no PRED-... summary line" % path)
            continue
        case_lines = sum(1 for line in lines if CASE_LINE.match(line))
        for pred, values in summaries:
            cases_value = values.get("cases_pass", [])
            case_text = render_value(cases_value[0]) if len(cases_value) == 1 else "-"
            pred_targets = targets.get(pred)
            if pred_targets is None:
                mismatch += 1
                print("POPULATION receipt=%s pred=%s cases_pass=%s case_lines=%d "
                      "registered=- agree=MISMATCH legs=registration_total"
                      % (path, pred, case_text, case_lines))
                continue

            legs = []
            registered_total = None
            cases_target = pred_targets.get("cases_pass")
            if cases_target and cases_target[0] == "ratio":
                registered_total = cases_target[2]
                if len(cases_value) != 1 or not isinstance(cases_value[0], tuple):
                    legs.append("missing_cases_pass")
                else:
                    if cases_value[0][1] != registered_total:
                        legs.append("denominator")
                    if case_lines != registered_total:
                        legs.append("case_lines")
            for name, target in pred_targets.items():
                check_target(name, target, values, legs)
            if legs:
                mismatch += 1
                print("POPULATION receipt=%s pred=%s cases_pass=%s case_lines=%d "
                      "registered=%s agree=MISMATCH legs=%s"
                      % (path, pred, case_text, case_lines,
                         "-" if registered_total is None else registered_total,
                         ",".join(dict.fromkeys(legs))))
            else:
                agreed += 1
                print("POPULATION receipt=%s pred=%s cases_pass=%s case_lines=%d "
                      "registered=%s agree=ok"
                      % (path, pred, case_text, case_lines,
                         "-" if registered_total is None else registered_total))

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
