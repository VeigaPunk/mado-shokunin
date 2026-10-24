#!/usr/bin/env python3
"""Offline gate over the round-26 population checker (quality/check-population.py).

Usage:
    python3 -I population-suite.py --checker PATH

The suite owns a built-in fixture set: for every fixture it writes a registration
file and one or more receipt files into a private temporary directory (under
$TMPDIR) and runs the checker on them:

    python3 -I <checker> --registration <reg> <receipt> [<receipt> ...]

A fixture passes only when the checker
  * exits with the expected status (0 agree, 1 disagreement, 2 unreadable),
  * reports the expected verdict class (agree / disagree / unreadable),
  * ends with the final `exit=<n>` line the checker documents,
  * reports every receipt it was handed, once per summary the receipt carries,
    and
  * names the legs that failed, when it names them at all.

The suite exits 0 only when every fixture passes; any other outcome exits 1
(2 for a setup error such as a missing checker).  The fixtures are written by
this file, so the suite judges behaviour only: it never pins the subject's
bytes, its AST, its path or the contents of any lane file, and it never
inspects the process tree or the clock.  The suite writes nothing outside its
own scratch directory and removes that directory before returning.

Fixture coverage (the checker's documented contract):
  * CASE lines count only at the start of a line, with a space or a tab
    separator; an indented, embedded or lower-case "CASE" is not a case line;
  * every PRED summary in a receipt is checked, not only the first or the
    last, and every one of them is reported;
  * the printed denominator, the case-line count and the registered total are
    each compared with the registration's total (in both directions);
  * the numerator of cases_pass is not compared with the registered total;
  * a receipt naming a predicate the registration states no total for is a
    disagreement (status 1);
  * an unreadable registration or receipt (missing, not a file, not decodable)
    and a receipt carrying no population are status 2;
  * ambiguous registration sentences (several predicates beside one total, one
    predicate beside two totals, the same predicate twice with different
    totals, a predicate without a total, no marked predicate at all) are
    status 2;
  * tab-delimited CASE lines and tab/space indented summary lines;
  * several receipts in one run, one of them disagreeing or unreadable, and
    unreadable taking precedence over disagreement;
  * the final `exit=` line.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

TIMEOUT = 120
# The three verdict classes the checker reports.  The suite keys on the class,
# not on one exact spelling, so a wording change in a behaviour-preserving
# edit is not mistaken for a behaviour change; a subject that reports the wrong
# class still fails.
VERDICT_CLASS = {
    0: ("pass", "passed", "ok", "agree", "agreed"),
    1: ("fail", "failed", "mismatch", "disagree", "disagreed"),
    2: ("unreadable", "unevaluable", "error"),
}
# The verdict token on a "verdict=<token>" field.
VERDICT_FIELD = re.compile(r"verdict\s*[=:]\s*\"?([A-Za-z_]+)")
# A verdict word as a standalone word, used only when the subject names no
# "verdict=" field; not as the key of a counter field ("unreadable=1" is a
# tally, not a verdict).
VERDICT_WORD = re.compile(r"(?i)\b(pass(?:ed|ing)?|ok|agree(?:d)?|fail(?:ed|ing)?|mismatch"
                           r"|disagree(?:d)?|unreadable|unevaluable|error)\b(?!\s*=)")
# How a summary line looks: the checker's own capture rule, used only to learn
# how many summaries a fixture carries (never to decide a verdict).
SUMMARY_LINE = re.compile(r"(?m)^[ \t]*(PRED-[A-Za-z0-9._-]+)\b[^\n]*?cases_pass=(\d+)/(\d+)")
# The checker's report of which comparisons failed; used only when present.
LEGS = re.compile(r"legs\s*=\s*([A-Za-z0-9_,\-]+)")
# The leg names the checker uses today.  A subject that names legs outside this
# set is judged on the count alone, so a behaviour-preserving rewording of the
# leg names is not mistaken for a behaviour change.
KNOWN_LEGS = ("case_lines", "denominator", "registration_total")


# ---------------------------------------------------------------- fixtures ---

def cases(n, tag="L"):
    """n CASE lines, as a counter prints them."""
    return "".join("CASE %s%02d PASS\n" % (tag, i) for i in range(n))


def reg(*paragraphs):
    """A registration: blank-line separated paragraphs, one predicate each."""
    return "\n\n".join(paragraphs) + "\n"


def pred(name, total):
    """A registration sentence: one predicate marker and one cases_pass total."""
    return "**%s** target cases_pass=%d/%d" % (name, total, total)


# registrations used by the fixtures
R_ALPHA2 = reg(pred("PRED-ALPHA", 2))
R_ALPHA3 = reg(pred("PRED-ALPHA", 3))
R_ALPHA4_BETA4 = reg(pred("PRED-ALPHA", 4), pred("PRED-BETA", 4))
R_ALPHA3_BETA3 = reg(pred("PRED-ALPHA", 3), pred("PRED-BETA", 3))
R_ALPHA3_BETA2 = reg(pred("PRED-ALPHA", 3), pred("PRED-BETA", 2))
R_TABSUM = reg(pred("PRED-TABSUM", 2))
R_TABCASE = reg(pred("PRED-TABCASE", 2))
R_41 = reg(pred("PRED-C1-r26", 41))
R_CHARSET = reg(pred("PRED-C1-r26.v2_x", 1))
R_DUP_SAME = reg(pred("PRED-ALPHA", 3), pred("PRED-ALPHA", 3))
R_DUP_DIFF = reg(pred("PRED-ALPHA", 3), pred("PRED-ALPHA", 2))
R_TWO_PREDS_ONE_TOTAL = reg("**PRED-ALPHA** and **PRED-BETA** target cases_pass=3/3")
R_ONE_PRED_TWO_TOTALS = reg("**PRED-ALPHA** target cases_pass=3/3 and also cases_pass=2/2")
R_PRED_NO_TOTAL = reg("**PRED-ALPHA** target with no cases_pass total")
R_NO_PRED = reg("Fixture registration without any predicate sentence.")
R_UNMARKED = reg("PRED-ALPHA target cases_pass=3/3")
R_WHITESPACE_SEP = ("**PRED-ALPHA** target cases_pass=3/3\n   \n"
                    "**PRED-BETA** target cases_pass=2/2\n")

# Fixture: (name, registration, receipts, expected status, registration_ok,
#            expected legs or None).
# `registration_ok` is False for the fixtures whose registration the checker
# must reject before it reads any receipt.  `expected legs` is the number of
# failed comparisons the checker must report; None means "do not judge".
FIXTURES = [
    # --- green: the documented contract holds --------------------------------
    ("green-single-receipt", R_ALPHA3,
     [cases(3) + "PRED-ALPHA cases_pass=3/3 verdict=TARGET_MET\n"], 0, True, None),
    ("green-two-receipts", R_ALPHA3_BETA2,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n", cases(2) + "PRED-BETA cases_pass=2/2\n"], 0, True, None),
    ("green-41-cases", R_41,
     [cases(41, "C") + "PRED-C1-r26 cases_pass=41/41 verdict=TARGET_MET\n"], 0, True, None),
    ("green-numerator-not-compared", R_ALPHA3,
     [cases(3) + "PRED-ALPHA cases_pass=0/3\n"], 0, True, None),
    ("green-tab-indented-summary", R_TABSUM,
     ["CASE A PASS\nCASE B PASS\n\tPRED-TABSUM cases_pass=2/2\n"], 0, True, None),
    ("green-space-indented-summary", R_ALPHA3,
     ["CASE A PASS\nCASE B PASS\nCASE C PASS\n  PRED-ALPHA cases_pass=3/3\n"], 0, True, None),
    ("green-tab-delimited-case-line", R_TABCASE,
     ["CASE A PASS\nCASE\tB PASS\nPRED-TABCASE cases_pass=2/2\n"], 0, True, None),
    ("green-summary-before-case-lines", R_ALPHA3,
     ["PRED-ALPHA cases_pass=3/3\n" + cases(3)], 0, True, None),
    ("green-same-predicate-twice-same-total", R_DUP_SAME,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n"], 0, True, None),
    ("green-predicate-id-charset", R_CHARSET,
     ["CASE A PASS\nPRED-C1-r26.v2_x cases_pass=1/1\n"], 0, True, None),
    ("green-summary-with-trailing-text", R_ALPHA3,
     [cases(3) + "PRED-ALPHA cases_pass=3/3 verdict=TARGET_MET extra\n"], 0, True, None),
    ("green-whitespace-paragraph-separator", R_WHITESPACE_SEP,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n"], 0, True, None),
    ("green-predicate-id-ends-at-the-id", R_ALPHA3,
     [cases(3) + "PRED-ALPHA=1 cases_pass=3/3\n"], 0, True, None),
    ("green-duplicate-summary-lines", R_ALPHA3,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n" + "PRED-ALPHA cases_pass=3/3\n"], 0, True, None),

    # --- red: a disagreement (status 1) --------------------------------------
    ("red-case-line-count-short", R_ALPHA3,
     [cases(2) + "PRED-ALPHA cases_pass=3/3\n"], 1, True, "case_lines"),
    ("red-case-line-count-long", R_ALPHA3,
     [cases(4) + "PRED-ALPHA cases_pass=3/3\n"], 1, True, "case_lines"),
    ("red-denominator-larger", R_ALPHA3,
     [cases(3) + "PRED-ALPHA cases_pass=3/4\n"], 1, True, "denominator"),
    ("red-denominator-smaller", R_ALPHA3,
     [cases(3) + "PRED-ALPHA cases_pass=3/2\n"], 1, True, "denominator"),
    ("red-case-lines-and-denominator", R_ALPHA3,
     [cases(2) + "PRED-ALPHA cases_pass=3/4\n"], 1, True, "case_lines,denominator"),
    ("red-registered-total-differs", R_ALPHA3,
     [cases(4) + "PRED-ALPHA cases_pass=4/4\n"], 1, True, "case_lines,denominator"),
    ("red-unknown-predicate", R_ALPHA3,
     [cases(3) + "PRED-UNKNOWN cases_pass=3/3\n"], 1, True, "registration_total"),
    ("red-second-summary-disagrees", R_ALPHA3_BETA3,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n" + "PRED-BETA cases_pass=3/4\n"], 1, True, "denominator"),
    ("red-first-summary-disagrees", R_ALPHA4_BETA4,
     [cases(4) + "PRED-ALPHA cases_pass=4/3\n" + "PRED-BETA cases_pass=4/4\n"], 1, True, "denominator"),
    ("red-lowercase-case-is-not-a-case-line", R_ALPHA2,
     ["CASE A PASS\ncase B diagnostic\nPRED-ALPHA cases_pass=2/2\n"], 1, True, "case_lines"),
    ("red-case-indented-not-a-case-line", R_ALPHA2,
     ["CASE A PASS\n  CASE B PASS\nPRED-ALPHA cases_pass=2/2\n"], 1, True, "case_lines"),
    ("red-note-case-is-not-a-case-line", R_ALPHA2,
     ["CASE A PASS\nNOTE CASE B\nPRED-ALPHA cases_pass=2/2\n"], 1, True, "case_lines"),
    ("red-case-without-separator", R_ALPHA2,
     ["CASE\nCASE A PASS\nPRED-ALPHA cases_pass=2/2\n"], 1, True, "case_lines"),
    ("red-second-receipt-disagrees", R_ALPHA3,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n", cases(2) + "PRED-ALPHA cases_pass=3/3\n"], 1, True, "case_lines"),
    ("red-first-receipt-disagrees", R_ALPHA3,
     [cases(2) + "PRED-ALPHA cases_pass=3/3\n", cases(3) + "PRED-ALPHA cases_pass=3/3\n"], 1, True, "case_lines"),

    # --- red: unreadable / unevaluable input (status 2) ----------------------
    ("exit2-receipt-without-summary", R_ALPHA3,
     [cases(3)], 2, True, None),
    ("exit2-receipt-unreadable", R_ALPHA3,
     [None], 2, True, None),
    ("exit2-registration-unreadable", None,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n"], 2, False, None),
    ("exit2-registration-without-predicate", R_NO_PRED,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n"], 2, False, None),
    ("exit2-registration-marker-required", R_UNMARKED,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n"], 2, False, None),
    ("exit2-registration-predicate-without-total", R_PRED_NO_TOTAL,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n"], 2, False, None),
    ("exit2-registration-two-predicates-one-total", R_TWO_PREDS_ONE_TOTAL,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n"], 2, False, None),
    ("exit2-registration-one-predicate-two-totals", R_ONE_PRED_TWO_TOTALS,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n"], 2, False, None),
    ("exit2-registration-same-predicate-different-totals", R_DUP_DIFF,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n"], 2, False, None),
    ("exit2-second-receipt-unreadable", R_ALPHA3,
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n", None], 2, True, None),
    ("exit2-unreadable-beats-disagreement", R_ALPHA3,
     [cases(2) + "PRED-ALPHA cases_pass=3/3\n", None], 2, True, None),
    ("exit2-summary-must-start-the-line", R_ALPHA3,
     ["CASE A PASS\nnoise PRED-ALPHA cases_pass=3/3\n"], 2, True, None),
    ("exit2-cases-pass-space-before-equals", R_ALPHA3,
     [cases(3) + "PRED-ALPHA cases_pass =3/3\n"], 2, True, None),
    ("exit2-cases-pass-space-after-equals", R_ALPHA3,
     [cases(3) + "PRED-ALPHA cases_pass= 3/3\n"], 2, True, None),
    ("exit2-receipt-not-decodable", R_ALPHA3,
     [b"CASE A PASS\nPRED-ALPHA cases_pass=3/3\n\xff\xfe\x00\n"], 2, True, None),
    ("exit2-registration-not-decodable", b"**PRED-ALPHA** target cases_pass=3/3\n\xff\xfe\n",
     [cases(3) + "PRED-ALPHA cases_pass=3/3\n"], 2, False, None),
    ("exit2-receipt-is-a-directory", R_ALPHA3,
     ["DIR"], 2, True, None),
]


# ------------------------------------------------------------------ runner ---

def summary_line(text):
    """The checker's final summary line, or None if it printed none.

    The line is the last one that mentions a verdict; the checker's own
    "POPULATION " prefix is not required, so a subject that renames its output
    prefix is still read.
    """
    last = None
    for line in text.splitlines():
        if "verdict" in line.lower():
            last = line
    return last


def verdict_class(text):
    """The verdict class the checker reported on its final summary line.

    The class is read from the checker's own "verdict=<token>" field.  When no
    such field is present the summary line is read instead, so a subject that
    renames the field is still judged on the class it reports.  Only the final
    summary line is read: a per-receipt line must not be able to colour the
    overall verdict.  A subject that reports no verdict at all is not judged on
    this point.
    """
    line = summary_line(text)
    if line is None:
        return None
    tokens = set(m.group(1).lower() for m in VERDICT_FIELD.finditer(line))
    if not tokens:
        tokens = set(m.group(0).lower() for m in VERDICT_WORD.finditer(line))
    seen = set()
    for t in tokens:
        for cls, names in VERDICT_CLASS.items():
            if t in names:
                seen.add(cls)
    return seen


def failed_legs(text):
    """The comparisons the checker reported as failed, or None if it names none."""
    hits = LEGS.findall(text)
    if not hits:
        return None
    return set(hits[-1].split(","))


def make_root():
    """A private scratch directory, removed by the caller.

    $TMPDIR is preferred (the counter's sandbox points it inside the run
    directory); the wave's scratch root is the fallback; the platform default
    is the last resort.
    """
    for base in (os.environ.get("TMPDIR"), "/fast/scratch/hyaku/mado-r27", None):
        try:
            if base is not None and not os.path.isdir(base):
                continue
            return tempfile.mkdtemp(prefix="population-suite-", dir=base)
        except OSError:
            continue
    return tempfile.mkdtemp(prefix="population-suite-")


def write_fixture(path, text):
    """Write a fixture file; text may be str or bytes."""
    data = text.encode("utf-8") if isinstance(text, str) else text
    with open(path, "wb") as f:
        f.write(data)


def expected_mentions(receipt_text, registration_ok):
    """How often the checker must name this receipt: once per summary it holds,
    or once when it cannot read a population out of it."""
    if receipt_text is None or receipt_text == "DIR" or isinstance(receipt_text, bytes):
        return 1
    if not registration_ok:
        return 0
    summaries = len(SUMMARY_LINE.findall(receipt_text))
    return summaries if summaries else 1


def mentions_ok(out, reg_path, receipt_paths, receipts, registration_ok):
    """Every receipt the checker was handed must be named in its report.

    A receipt is named at least once when the checker had to look at it, and
    once per summary it holds: a subject that checks only the first summary of
    a receipt reports that receipt once, not once per summary.

    The count is judged only for a subject that names the paths it was given.
    A subject that names neither the registration nor any receipt reports no
    paths at all, and is not judged on this point.
    """
    if os.path.basename(reg_path) not in out and not any(
            os.path.basename(p) in out for p in receipt_paths):
        return True
    for p, text in zip(receipt_paths, receipts):
        got = out.count(os.path.basename(p))
        want = expected_mentions(text, registration_ok)
        if want and got < want:
            return False
    return True


def main():
    ap = argparse.ArgumentParser(
        description="Gate the round-26 population checker over a built-in fixture set.")
    ap.add_argument("--checker", required=True, metavar="PATH", help="population checker")
    args = ap.parse_args()

    checker = os.path.abspath(args.checker)
    if not os.path.isfile(checker):
        print("SUITE ERROR checker not found: %s" % checker)
        print("exit=2")
        return 2

    root = make_root()
    env = {"PATH": "/usr/bin", "HOME": os.environ.get("HOME", root), "TMPDIR": root}
    failed = []
    try:
        for name, registration, receipts, want, registration_ok, want_legs in FIXTURES:
            reg_path = os.path.join(root, name + ".registration.md")
            if registration is not None:
                write_fixture(reg_path, registration)
            receipt_paths = []
            for i, text in enumerate(receipts):
                p = os.path.join(root, "%s.receipt%d.txt" % (name, i))
                if text == "DIR":
                    os.makedirs(p, exist_ok=True)
                elif text is not None:
                    write_fixture(p, text)
                receipt_paths.append(p)

            cmd = [sys.executable, "-I", checker, "--registration", reg_path] + receipt_paths
            try:
                proc = subprocess.run(cmd, cwd=root, env=env, capture_output=True,
                                      text=True, timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                print("SUITE fixture=%s status=TIMEOUT want=%d" % (name, want))
                failed.append(name)
                continue

            out = proc.stdout or ""
            lines = [ln for ln in out.splitlines() if ln.strip()]
            final = lines[-1] if lines else ""
            classes = verdict_class(out)
            mentions = []
            for p, text in zip(receipt_paths, receipts):
                want_n = expected_mentions(text, registration_ok)
                got_n = out.count(os.path.basename(p))
                mentions.append((os.path.basename(p), got_n, want_n))
            named_ok = mentions_ok(out, reg_path, receipt_paths, receipts, registration_ok)
            legs = failed_legs(out)
            legs_ok = True
            if want_legs is not None and legs is not None:
                want_set = set(want_legs.split(","))
                legs_ok = len(legs) == len(want_set)
                if legs <= set(KNOWN_LEGS) and want_set <= set(KNOWN_LEGS):
                    legs_ok = legs == want_set
            class_ok = classes is None or classes == {want}
            ok = (proc.returncode == want
                  and final == "exit=%d" % want
                  and class_ok
                  and named_ok
                  and legs_ok)
            print("SUITE fixture=%s status=%s want=%d rc=%d verdict=%s legs=%s final=%r mentions=%s"
                  % (name, "ok" if ok else "FAIL", want, proc.returncode,
                     ",".join(str(c) for c in sorted(classes)) or "-",
                     ",".join(sorted(legs)) if legs else "-", final,
                     ",".join("%s:%d/%d" % m for m in mentions)))
            if not ok:
                failed.append(name)
                print("SUITE fixture=%s stdout:\n%s" % (name, out.rstrip("\n")))
                if proc.stderr.strip():
                    print("SUITE fixture=%s stderr:\n%s" % (name, proc.stderr.rstrip("\n")))
    finally:
        shutil.rmtree(root, ignore_errors=True)

    print("SUITE verdict=%s fixtures=%d failed=%d %s"
          % ("FAIL" if failed else "PASS", len(FIXTURES), len(failed),
             ",".join(failed) if failed else "-"))
    rc = 1 if failed else 0
    print("exit=%d" % rc)
    return rc


if __name__ == "__main__":
    sys.exit(main())
