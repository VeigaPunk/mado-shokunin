#!/usr/bin/env python3
"""MutRefSelftest harness: apply one mutant per record, run `python3 -I mutant --selftest`.

Usage: mutate.py run-selftests   -> applies mutants to scratch, runs selftest, writes results.json
       mutate.py make ID         -> (re)write one mutant file (for counter runs)
       mutate.py make-all        -> write all mutant files
Mutant records: (id, function, kind, old, new). old must occur exactly once.
"""
import json
import os
import subprocess
import sys

SEAT = os.path.dirname(os.path.abspath(__file__))
PRISTINE = "/fast/scratch/hyaku/mado-r43/MutRefSelftest/pristine.py"
OUT = "/fast/scratch/hyaku/mado-r43/MutRefSelftest/mut"
PY = sys.executable

MUTANTS = [
    # read_regular
    ("R1", "read_regular", "arg-drop", "os.O_RDONLY | os.O_NONBLOCK", "os.O_RDONLY"),
    ("R2", "read_regular", "cmp", 'if len(data) > MAX_BYTES:\n        raise Setup("too_large")\n    return data', 'if len(data) >= MAX_BYTES:\n        raise Setup("too_large")\n    return data'),
    ("R3", "read_regular", "branch-removal", "if not stat.S_ISREG(os.fstat(fd).st_mode):", "if False:"),
    ("R4", "read_regular", "constant", 'raise Setup("unreadable")\n    try:', 'raise Setup("bad_json")\n    try:'),
    ("R5", "read_regular", "stmt-removal", "    finally:\n        os.close(fd)", "    finally:\n        pass"),
    # parse_args
    ("A1", "parse_args", "constant", 'if argv == ["--selftest"]:', "if argv == []:"),
    ("A2", "parse_args", "cmp", 'if flag == "--clients" and clients is None:', 'if flag == "--clients":'),
    ("A3", "parse_args", "constant", 'elif flag == "--rules":', 'elif flag == "--rule":'),
    ("A4", "parse_args", "branch-removal", "if clients is None or not rules:", "if clients is None:"),
    ("A5", "parse_args", "constant", "        i += 2", "        i += 1"),
    ("A6", "parse_args", "return", 'return "run", clients, rules', 'return "RUN", clients, rules'),
    ("A7", "parse_args", "constant", 'raise Setup("usage")\n        flag, value', 'raise Setup("unreadable")\n        flag, value'),
    # regex_ok
    ("G1", "regex_ok", "branch-removal", "if not SAFE.fullmatch(rx):", "if False:"),
    ("G2", "regex_ok", "stmt-removal", 'for bad in ("(?", "*+", "++", "?+"):', 'for bad in ():'),
    ("G3", "regex_ok", "return", "    except re.error:\n        return False", "    except re.error:\n        return True"),
    ("G4", "regex_ok", "regex", "{1,200}", "{1,201}"),
    ("G5", "regex_ok", "regex", 'r"(?:[A-Za-z0-9_.^$()|*+?-]|', 'r"(?:[A-Za-z0-9_.^$()|*+-]|'),
    ("G6", "regex_ok", "arg", "re.compile(rx)", "re.compile(rx, re.I)"),
    # parse_rule_text
    ("P1", "parse_rule_text", "constant", 'line = raw.strip(" \\t")', "line = raw.strip()"),
    ("P2", "parse_rule_text", "method", "m = RULE_LINE.fullmatch(line)", "m = RULE_LINE.match(line)"),
    ("P3", "parse_rule_text", "stmt-removal", 'counts["other"] += 1\n', ""),
    ("P4", "parse_rule_text", "cmp", "good = len(fields) == 2", "good = len(fields) >= 2"),
    ("P5", "parse_rule_text", "method", "all(NUM.fullmatch(a) for a in args)", "all(NUM.match(a) for a in args)"),
    ("P6", "parse_rule_text", "constant", 'args[0] in ("on", "off")', 'args[0] in ("on",)'),
    ("P7", "parse_rule_text", "format", '"%dx%d" % (int(args[0]), int(args[1])) if effect == "size"', '"%d:%d" % (int(args[0]), int(args[1])) if effect == "size"'),
    ("P8", "parse_rule_text", "swap", '"want": (int(args[0]), int(args[1])) if effect == "size"', '"want": (int(args[1]), int(args[0])) if effect == "size"'),
    ("P9", "parse_rule_text", "cmp", 'if effect not in ("size", "float"):', 'if effect != "size":'),
    ("P10", "parse_rule_text", "invert", "if good else None", "if not good else None"),
    ("P12", "parse_rule_text", "arg-drop", 'f.strip(" \\t") for f in body.split(",")', "f for f in body.split(',')"),
    ("P13", "parse_rule_text", "method", 're.split("[ \\t]+", fields[0])', 'fields[0].split(" ")'),
    # parse_clients
    ("C1", "parse_clients", "except-narrow", "except (UnicodeDecodeError, ValueError):", "except ValueError:"),
    ("C2", "parse_clients", "cmp-drop", "if not isinstance(doc, list) or not all(isinstance(c, dict) for c in doc):", "if not isinstance(doc, list):"),
    ("C3", "parse_clients", "constant", '        raise Setup("bad_json")\n    if not isinstance', '        raise Setup("unreadable")\n    if not isinstance'),
    # client_size
    ("S1", "client_size", "constant", "len(s) == 2 and all", "len(s) == 3 and all"),
    ("S2", "client_size", "type", "isinstance(v, int) and not isinstance(v, bool)", "isinstance(v, (int, float)) and not isinstance(v, bool)"),
    ("S3", "client_size", "cmp-drop", "and not isinstance(v, bool) and v >= 0", " and v >= 0"),
    ("S4", "client_size", "cmp", "v >= 0 for v in s", "v > 0 for v in s"),
    # matches
    ("M1", "matches", "constant", "if any(ord(ch) < 0x20 for ch in cls):", "if any(ord(ch) < 0x21 for ch in cls):"),
    ("M2", "matches", "method", "re.fullmatch(rx, cls) is not None", "re.search(rx, cls) is not None"),
    ("M3", "matches", "invert", "re.fullmatch(rx, cls) is not None", "re.fullmatch(rx, cls) is None"),
    ("M4", "matches", "constant", "if any(ord(ch) < 0x20 for ch in cls):", "if any(ord(ch) < 0x0A for ch in cls):"),
    # evaluate
    ("E1", "evaluate", "invert", 'if c.get("mapped") is False:', 'if c.get("mapped") is not True:'),
    ("E2", "evaluate", "stmt-removal", 'tally["unmapped"] += 1\n            continue', 'tally["unmapped"] += 1'),
    ("E3", "evaluate", "branch-removal", 'cls = c.get("class") if isinstance(c.get("class"), str) else ""', 'cls = ""'),
    ("E4", "evaluate", "invert", "if matches(r[\"rx\"], cls):", "if not matches(r[\"rx\"], cls):"),
    ("E5", "evaluate", "constant", 'if r["effect"] == "size":', 'if r["effect"] == "float":'),
    ("E6", "evaluate", "branch-removal", "if want is None:\n            continue", "pass"),
    ("E7", "evaluate", "invert", 'floating = c.get("floating") is True', 'floating = c.get("floating") is not False'),
    ("E8", "evaluate", "invert", "elif size == want:", "elif size != want:"),
    ("E9", "evaluate", "reorder", 'if size is None:\n            verdict = "BADSIZE"\n        elif not floating:\n            verdict = "TILED"', 'if not floating:\n            verdict = "TILED"\n        elif size is None:\n            verdict = "BADSIZE"'),
    ("E11", "evaluate", "branch-removal", 'addr = c.get("address") if isinstance(c.get("address"), str) else "-"', 'addr = "-"'),
    ("E12", "evaluate", "format", "want=%dx%d float_rule=%s", "want=%d-%d float_rule=%s"),
    ("E13", "evaluate", "constant", '"true" if floating else "false"', '"yes" if floating else "no"'),
    # report
    ("B1", "report", "constant", "enumerate(rule_texts, 1)", "enumerate(rule_texts)"),
    ("B2", "report", "constant", "enumerate(rules, 1)", "enumerate(rules)"),
    ("B3", "report", "constant", 'sum(1 for r in rules if r["effect"] == "size")', 'sum(1 for r in rules if r["effect"] == "float")'),
    ("B4", "report", "cmp", 'elif t["differ"] > 0:', 'elif t["differ"] >= 0:'),
    ("B5", "report", "cmp", 'elif t["matched"] == 0:', 'elif t["matched"] > 0:'),
    ("B6", "report", "constant", '"NO_SIZE_RULES", 4', '"NO_SIZE_RULES", 3'),
    ("B7", "report", "format", "rules=%d float_rules=%d", "rules=%d float=%d"),
    ("B8", "report", "swap", "len(rules) - size_rules, counts[\"other\"]", "size_rules, counts[\"other\"]"),
    ("B9", "report", "swap", 'counts["other"], counts["unsupported"],', 'counts["unsupported"], counts["other"],'),
    # run
    ("U1", "run", "invert", 'if clients == "-":', 'if clients != "-":'),
    ("U2", "run", "constant", "stdin.read(MAX_BYTES + 1)", "stdin.read(MAX_BYTES - 1)"),
    ("U3", "run", "branch-removal", '        if len(data) > MAX_BYTES:\n            raise Setup("too_large")\n', ""),
    ("U4", "run", "constant", ', "replace") for p in rules]', ') for p in rules]'),
    ("U5", "run", "constant", '"\\n".join(lines) + "\\n"', '"".join(lines)'),
    ("U6", "run", "return", "    lines, rc = report(data, texts)", "    lines, rc = report(data, texts)\n    rc = 0"),
    ("U7", "run", "swap", "mode, clients, rules = parse_args(argv)", "clients, mode, rules = parse_args(argv)"),
    # main
    ("N1", "main", "except-widen", 'except Setup as exc:\n        print("MADO_GEOMETRY: SETUP %s" % exc)', 'except Exception as exc:\n        print("MADO_GEOMETRY: SETUP %s" % exc)'),
    ("N2", "main", "arg", '"MADO_GEOMETRY: SETUP %s" % exc', '"MADO_GEOMETRY: SETUP %s" % exc, end=""'),
    ("N3", "main", "constant", '        print("MADO_GEOMETRY: SETUP %s" % exc)\n        return 2', '        print("MADO_GEOMETRY: SETUP %s" % exc)\n        return 0'),
    ("N4", "main", "arg", "run(sys.argv[1:], sys.stdin.buffer)", "run(sys.argv[1:], sys.stdin)"),
    # module constants
    ("K1", "const", "constant", "MAX_BYTES = 1048576", "MAX_BYTES = 1048575"),
    ("K2", "const", "regex", 're.compile(r"windowrule[ \\t]*=(.*)")', 're.compile(r"Windowrule[ \\t]*=(.*)")'),
    ("K3", "const", "regex", 're.compile(r"match:class[ \\t]+(.+)")', 're.compile(r"match:class[ \\t]*(.+)")'),
    ("K4", "const", "regex", 're.compile(r"[0-9]{1,5}")', 're.compile(r"[0-9]{1,4}")'),
]


def apply(mut, text):
    mid, fn, kind, old, new = mut
    n = text.count(old)
    if n != 1:
        raise SystemExit("mutant %s: old occurs %d times" % (mid, n))
    return text.replace(old, new)


def selftest_result(path):
    p = subprocess.run([PY, "-I", path, "--selftest"], capture_output=True, timeout=90)
    out = (p.stdout + p.stderr).decode("utf-8", "replace")
    lines = [l for l in out.splitlines() if l.strip()]
    summary = lines[-1] if lines else ""
    passed = p.returncode == 0 and summary.startswith("MADO_GEOMETRY_SELFTEST: ") and \
        summary.endswith(" passed")
    k = n = -1
    if summary.startswith("MADO_GEOMETRY_SELFTEST: "):
        try:
            k, n = summary.split(": ")[1].split(" ")[0].split("/")
            k, n = int(k), int(n)
        except Exception:
            pass
        passed = passed and k == n and n >= 50
    return {"rc": p.returncode, "summary": summary, "selftest_pass": passed, "k": k, "n": n}


def main():
    cmd = sys.argv[1]
    text = open(PRISTINE, encoding="utf-8").read()
    os.makedirs(OUT, exist_ok=True)
    if cmd == "make" or cmd == "make-all":
        ids = [sys.argv[2]] if cmd == "make" else [m[0] for m in MUTANTS]
        for mid in ids:
            mut = next(m for m in MUTANTS if m[0] == mid)
            open(os.path.join(OUT, "mut_%s.py" % mid), "w", encoding="utf-8").write(apply(mut, text))
        return
    results = {}
    for mut in MUTANTS:
        mid = mut[0]
        mpath = os.path.join(OUT, "mut_%s.py" % mid)
        open(mpath, "w", encoding="utf-8").write(apply(mut, text))
        try:
            r = selftest_result(mpath)
        except subprocess.TimeoutExpired:
            r = {"rc": "timeout", "summary": "", "selftest_pass": False, "k": -1, "n": -1}
        r["function"] = mut[1]
        r["kind"] = mut[2]
        results[mid] = r
        print("%-5s %-16s %-15s rc=%-4s %s" % (mid, mut[1], mut[2], r["rc"], r["summary"][:70]))
    json.dump(results, open(os.path.join(OUT, "results.json"), "w"), indent=1)
    surv = [m for m in results if results[m]["selftest_pass"]]
    print("total=%d selftest_survivors=%d: %s" % (len(MUTANTS), len(surv), " ".join(sorted(surv))))


if __name__ == "__main__":
    main()
