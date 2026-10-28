"""Mutation driver for tools/mado-kbdopts.py (R55W2MutTool2).

Generates one-edit mutant COPIES (exact, must-match-once replacements) into the seat's mutants/ dir,
scores each against the 26 fixtures (args.json, cwd = scratch root, stdout bytes + rc vs expected.out/expected.rc)
and against the mutant's own --selftest. The lane is never touched: the original is read from the scratch export.
"""
import json
import os
import re
import subprocess
import sys

ROOT = "/fast/scratch/hyaku/mado-r55/R55W2MutTool2"
DELIV = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-55/w2/R55W2MutTool2/mutants"
ORIG = os.path.join(ROOT, "tools", "mado-kbdopts.py")
FIX = os.path.join(ROOT, ".ufo", "waves", "round-55", "fixtures")

# (id, one-line edit description, old exact text, new exact text)
MUTANTS = [
    ("M01", "drop `yes` from true/on/yes prefix list",
     'rhs.startswith(("true", "on", "yes"))', 'rhs.startswith(("true", "on"))'),
    ("M02", "case-fold the true/on/yes prefix test",
     'if rhs.startswith(("true", "on", "yes")):', 'if rhs.lower().startswith(("true", "on", "yes")):'),
    ("M03", "digit class [0-9] -> \\d (Unicode Nd digits)",
     'DIGITS_RE = re.compile(r"[0-9]+")', 'DIGITS_RE = re.compile(r"\\d+")'),
    ("M04", "digit class + -> * (empty value accepted as 0)",
     'DIGITS_RE = re.compile(r"[0-9]+")', 'DIGITS_RE = re.compile(r"[0-9]*")'),
    ("M05", "fullmatch -> match (prefix digits accepted)",
     'if DIGITS_RE.fullmatch(rhs):', 'if DIGITS_RE.match(rhs):'),
    ("M06", "leading zeros not stripped before the 6-digit cap",
     'digits = rhs.lstrip("0")', 'digits = rhs'),
    ("M07", "drop the `or \"0\"` zero fallback (\"0\" crashes)",
     'return int(digits or "0") if len(digits) <= 6 else 10 ** 6',
     'return int(digits) if len(digits) <= 6 else 10 ** 6'),
    ("M08", "over-cap digit run maps to 0 instead of out-of-range",
     'return int(digits or "0") if len(digits) <= 6 else 10 ** 6',
     'return int(digits or "0") if len(digits) <= 6 else 0'),
    ("M09", "cap 6 -> 4 digits (EQUIVALENT: every >4-digit value exceeds all maxima)",
     'len(digits) <= 6', 'len(digits) <= 4'),
    ("M10", "repeat_rate maximum 200 -> 201",
     'MAXIMA = {"repeat_rate": 200, "repeat_delay": 2000, "numlock_by_default": 1}',
     'MAXIMA = {"repeat_rate": 201, "repeat_delay": 2000, "numlock_by_default": 1}'),
    ("M11", "repeat_delay maximum 2000 -> 2001",
     'MAXIMA = {"repeat_rate": 200, "repeat_delay": 2000, "numlock_by_default": 1}',
     'MAXIMA = {"repeat_rate": 200, "repeat_delay": 2001, "numlock_by_default": 1}'),
    ("M12", "numlock_by_default maximum 1 -> 2",
     'MAXIMA = {"repeat_rate": 200, "repeat_delay": 2000, "numlock_by_default": 1}',
     'MAXIMA = {"repeat_rate": 200, "repeat_delay": 2000, "numlock_by_default": 2}'),
    ("M13", "range test > -> >= (boundary rejected)",
     'if value is None or value > MAXIMA[name]:', 'if value is None or value >= MAXIMA[name]:'),
    ("M14", "drop the `##` rule",
     'or "\\\\" in line or "##" in rhs:', 'or "\\\\" in line:'),
    ("M15", "value comment cut at LAST # (rsplit)",
     'value = parse_value(rhs.split("#", 1)[0].strip(WS))',
     'value = parse_value(rhs.rsplit("#", 1)[0].strip(WS))'),
    ("M16", "`$` detection narrowed to `${`",
     'if bracket or "$" in line or', 'if bracket or "${" in line or'),
    ("M17", "drop the backslash check",
     'or "\\\\" in line or "##" in rhs:', 'or "##" in rhs:'),
    ("M18", "drop the `{{` check",
     'or "{{" in line or', 'or'),
    ("M19", "drop full-line `#` comment skip",
     'if not line or line[0] == "#":', 'if not line:'),
    ("M20", "device name not comment-cut",
     'cur = rhs.split("#", 1)[0].strip(WS)', 'cur = rhs.strip(WS)'),
    ("M21", "form feed no longer stripped from raw lines",
     'WS = " \\t\\r\\n\\v\\f"', 'WS = " \\t\\r\\n\\v"'),
    ("M22", "value strip narrowed to spaces only (tab before # survives)",
     'value = parse_value(rhs.split("#", 1)[0].strip(WS))',
     'value = parse_value(rhs.split("#", 1)[0].strip(" "))'),
    ("M23", "JSON boolean accepted as integer live value",
     'and isinstance(val, int) and not isinstance(val, bool):', 'and isinstance(val, int):'),
    ("M24", "remove sys.set_int_max_str_digits(0) guard",
     '    sys.set_int_max_str_digits(0)', '    pass'),
    ("M25", "repeat_rate maximum 200 -> 199",
     'MAXIMA = {"repeat_rate": 200, "repeat_delay": 2000, "numlock_by_default": 1}',
     'MAXIMA = {"repeat_rate": 199, "repeat_delay": 2000, "numlock_by_default": 1}'),
    ("M26", "repeat_delay maximum 2000 -> 1999",
     'MAXIMA = {"repeat_rate": 200, "repeat_delay": 2000, "numlock_by_default": 1}',
     'MAXIMA = {"repeat_rate": 200, "repeat_delay": 1999, "numlock_by_default": 1}'),
]


def fixtures():
    out = []
    for grp in ("c2", "c2-holdout"):
        base = os.path.join(FIX, grp)
        for d in sorted(os.listdir(base)):
            out.append((d, os.path.join(base, d)))
    return out


def run(tool, args):
    p = subprocess.run([sys.executable, "-I", tool, *args], cwd=ROOT, capture_output=True, timeout=120)
    return p.stdout, p.returncode, p.stderr.decode("utf-8", "replace")


def score(tool):
    killed = []
    details = {}
    for fid, fdir in fixtures():
        args = json.load(open(os.path.join(fdir, "args.json")))
        out, rc, err = run(tool, args)
        exp_out = open(os.path.join(fdir, "expected.out"), "rb").read()
        exp_rc = int(open(os.path.join(fdir, "expected.rc")).read().strip())
        if out != exp_out or rc != exp_rc:
            killed.append(fid)
            details[fid] = {"rc": rc, "stdout": out.decode("utf-8", "replace"), "stderr_tail": err[-200:]}
    out, rc, err = run(tool, ["--selftest"])
    m = re.search(rb"MADO_KBDOPT_SELFTEST: (\d+)/(\d+) assertions passed", out)
    st_ok = rc == 0 and m is not None and m.group(1) == m.group(2)
    st = {"rc": rc, "line": out.decode("utf-8", "replace").strip(), "fails": [l for l in err.splitlines() if "FAIL" in l]}
    return killed, (not st_ok), st, details


def main():
    os.makedirs(DELIV, exist_ok=True)
    src = open(ORIG, encoding="utf-8").read()
    results = {}
    targets = [("M00", "ORIGINAL (control)", None, None)] + MUTANTS
    for mid, desc, old, new in targets:
        if old is None:
            text = src
        else:
            n = src.count(old)
            assert n == 1, (mid, n, old)
            text = src.replace(old, new)
        path = os.path.join(DELIV, mid + ".py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        killed, st_killed, st, details = score(path)
        results[mid] = {"desc": desc, "fixtures_killed": killed, "selftest_killed": st_killed,
                        "selftest": st, "details": details, "sha256": None}
        import hashlib
        results[mid]["sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        survivor = (not killed) and (not st_killed)
        print("%s | %s | fixtures_killed=%s | selftest_killed=%s | %s" % (
            mid, desc, ",".join(killed) or "-", "yes" if st_killed else "no",
            "SURVIVOR" if survivor else ("killed" if (killed or st_killed) else "?")), flush=True)
        if st["fails"]:
            print("    selftest FAIL lines:", "; ".join(x.split("selftest FAIL: ")[-1] for x in st["fails"]), flush=True)
    with open(os.path.join(DELIV, "scores.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1, ensure_ascii=False, sort_keys=True)


if __name__ == "__main__":
    main()
