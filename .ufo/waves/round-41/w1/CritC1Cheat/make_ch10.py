#!/usr/bin/env python3
"""Build CH10: aim clause b2 away from the model.

b2 excludes every function whose name contains selftest/_check/_run/_write/main/
usage and only needs 12 comparison sites somewhere. Renaming the parser to
_run_parse, the reporter to _run_report and the classifier to _check_classify
removes the whole model from the mutant sample; `invariants()` supplies 12
comparison sites that the selftest does exercise, so b2 reads killed 6/6 while
no mutant ever touches the code that produces the report.
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "ref-base.py")
OUT = os.path.join(HERE, "ch10-aim-away.py")
REF_SHA = "61f101aed8897e43a3c4b1ce792d82a0acd29d73fbdb929f4279a57fdf3130f0"

src0 = open(REF, "rb").read()
if hashlib.sha256(src0).hexdigest() != REF_SHA:
    sys.exit("SETUP ref sha mismatch")
src = src0.decode()

src = src.replace("ap.parse_args(", "ARGVPARSE(")
src = src.replace("parse(", "_run_parse(")
src = src.replace("ARGVPARSE(", "ap.parse_args(")
src = src.replace("report(", "_run_report(")
src = src.replace("classify(", "_check_classify(")

INV = '''def invariants(sessions, lines):
    """Structural invariants of a report; exercised by --selftest."""
    c = []
    c.append(len(lines) >= 1)
    c.append(lines[-1].startswith("MADO_GLOBALS: sessions="))
    c.append(lines[-1].count("sessions=") == 1)
    c.append(lines[-1].count("interfaces=") == 1)
    c.append(lines[-1].count("classes=") == 1)
    c.append(lines[-1].count("expected_missing=") == 1)
    c.append(lines[-1].count("latest_pid=") == 1)
    c.append(len(sessions) == len([x for x in lines
                                   if x.startswith("MADO_GLOBALS_SESSION: ")]))
    c.append(all(s["pid"].isdigit() for s in sessions))
    c.append(all(s["adverts"] >= len(s["names"]) for s in sessions))
    c.append(len([x for x in lines if x.startswith("MADO_GLOBAL: ")]) ==
             (len(sessions[-1]["names"]) if sessions else 0))
    c.append(not any("None" in x for x in lines))
    return all(c)


'''
anchor = "def resolve_program(prog):"
if src.count(anchor) != 1:
    sys.exit("SETUP anchor")
src = src.replace(anchor, INV + anchor, 1)

old = ('    lines, code = _run_report(_run_parse(data), sorted(set(args.expect)), '
       'args.diff)\n    return lines, code\n')
new = ('    sessions = _run_parse(data)\n'
       '    lines, code = _run_report(sessions, sorted(set(args.expect)), '
       'args.diff)\n'
       '    if not invariants(sessions, lines):\n'
       '        raise Setup("usage")\n'
       '    return lines, code\n')
if src.count(old) != 1:
    sys.exit("SETUP run span")
src = src.replace(old, new, 1)

old2 = '    check(len(s) == 1 and s[0]["adverts"] == 3)\n'
new2 = ('    check(invariants(s, _run_report(s, [], False)[0]))\n'
        '    check(len(s) == 1 and s[0]["adverts"] == 3)\n')
if src.count(old2) != 1:
    sys.exit("SETUP selftest span")
src = src.replace(old2, new2, 1)

with open(OUT, "w") as fh:
    fh.write(src)
os.chmod(OUT, 0o644)
print("wrote %s sha256=%s" % (os.path.basename(OUT),
                              hashlib.sha256(src.encode()).hexdigest()[:16]))
