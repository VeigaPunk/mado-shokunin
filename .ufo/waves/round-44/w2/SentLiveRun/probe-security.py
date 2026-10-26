#!/usr/bin/env python3
"""probe-security.py — injection / argument / ReDoS probes on the landed tool vs round 43.

Three receipts in one run, all inside this seat dir:
  injection-probe.txt  untrusted client text and rule text: can either write a line of the
                       tool's own stdout vocabulary, a newline, or a format directive?
  args-probe.txt       argument and path handling: usage, duplicate flags, `-` as a path,
                       directory / char-device / FIFO inputs, `--selftest` with extras.
  redos-probe.txt      pattern acceptance matrix (r43 vs landed) and the cost of the
                       patterns both tools accept; then the documented `timeout 5` guard.

usage: python3 probe-security.py --r43 R43.py --tool TOOL
"""
import argparse, importlib.util, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(tool, args, stdin=b"", timeout=30):
    p = subprocess.run([sys.executable, "-I", tool] + args, input=stdin, capture_output=True,
                       timeout=timeout)
    return p.returncode, p.stdout.decode(), p.stderr.decode()


def injection(a, tmp):
    def w(name, text):
        open(os.path.join(HERE, name), "w").write(text)
        return os.path.join(HERE, name)
    out = ["injection probe: client text and rule text into %s" % a.tool, ""]
    rule_any = w(".probe-any.conf", "windowrule = size 420 500, match:class .*\n")
    cases = [
        ("newline+forged-summary in class",
         "org.omarchy.gkeep\nMADO_GEOMETRY: rules=1 float_rules=1 other=0 unsupported=0 clients=1 "
         "matched=1 unmapped=0 agree=9 differ=0 tiled=0 badsize=0 verdict=OK"),
        ("ESC in class", "a\x1bb"),
        ("quote+percent in class", 'a"b%sc'),
        ("unicode in class", "h\u00e9llo\u00e9"),
    ]
    for label, cls in cases:
        f = w(".probe-d.json", json.dumps([{"mapped": True, "floating": True, "fullscreen": 0,
                                            "size": [420, 500], "class": cls}]))
        rc, o, e = run(a.tool, ["--clients", f, "--rules", rule_any])
        out.append("[%s] rc=%d stderr=%r stdout_lines=%d" % (label, rc, e, len(o.splitlines())))
        for line in o.splitlines():
            out.append("   " + line)
    hostile = ("windowrule = size 420 500, match:class (?=x)y\n"
               "windowrule = size 420 500, match:class (a)\\1\n"
               "windowrule = size 420500, match:class a\n"
               "windowrule = size 999999999 1, match:class a\n"
               "windowrule = size 420 500, match:class a\\d\n"
               "windowrule = size 420 500, match:class a\x01b\n"
               "windowrule = size 420 500, match:class a b\n"
               'windowrule = size 420 500, match:class a"b\n'
               "windowrule = size 420 500, match:class a%sb\n")
    f = w(".probe-hostile.conf", hostile)
    rc, o, e = run(a.tool, ["--clients", os.path.join(HERE, ".probe-d.json"), "--rules", f])
    out += ["", "[hostile rule bodies: lookaround, backref, no-space args, 9-digit arg, \\d, "
                "control char, space, quote, percent]", "   rc=%d stderr=%r" % (rc, e)]
    for line in o.splitlines():
        out.append("   " + line)
    # reader decoy: a client chooses its class, so a naive `grep -o 'verdict=[A-Z]*'` reader
    # can read a token the client wrote before the tool's own verdict field
    f = w(".probe-decoy.json", json.dumps([{"mapped": True, "floating": True, "fullscreen": 0,
                                            "size": [421, 500], "class": "x verdict=OK"}]))
    rc, o, e = run(a.tool, ["--clients", f, "--rules", rule_any])
    out += ["", "[class carrying a decoy verdict token] rc=%d stderr=%r" % (rc, e)]
    for line in o.splitlines():
        out.append("   " + line)
    out.append("   naive reader `grep -o 'verdict=[A-Z]*'` would print: %s"
               % re.findall(r"verdict=[A-Z]+", o))
    f = os.path.join(HERE, ".probe-decoy.json")
    if os.path.exists(f):
        os.unlink(f)
    malformed = [("top-not-list", b'{"a":1}'), ("elem-not-object", b'[1,2,3]'),
                 ("bad-utf8", b'[\xff\xfe]'), ("empty", b'[]')]
    out.append("")
    for label, body in malformed:
        f = os.path.join(HERE, ".probe-bad.json")
        open(f, "wb").write(body)
        rc, o, e = run(a.tool, ["--clients", f, "--rules", rule_any])
        out.append("[%s] rc=%d stderr=%r out=%r" % (label, rc, e, o.strip()))
    big = os.path.join(HERE, ".probe-big.json")
    open(big, "wb").write(b"[" + b" " * 1048576 + b"]")
    rc, o, e = run(a.tool, ["--clients", big, "--rules", rule_any])
    out.append("[too_large 1048577B] rc=%d stderr=%r out=%r" % (rc, e, o.strip()))
    for p in (".probe-d.json", ".probe-any.conf", ".probe-hostile.conf", ".probe-bad.json", ".probe-big.json"):
        try:
            os.unlink(os.path.join(HERE, p))
        except OSError:
            pass
    text = "\n".join(out) + "\n"
    open(os.path.join(HERE, "injection-probe.txt"), "w").write(text)
    print(text, end="")


def args(a):
    out = ["argument and path probe: %s" % a.tool, ""]
    empty = os.path.join(HERE, ".probe-empty.json")
    open(empty, "w").write("[]")
    conf = os.path.join(HERE, ".probe-empty.conf")
    open(conf, "w").write("")
    cases = [["--selftest", "--clients", empty],
             ["--clients", empty],
             ["--rules", conf],
             ["--clients", empty, "--clients", empty, "--rules", conf],
             ["--rules", "-", "--clients", empty],
             ["--clients", "-", "--rules", conf],
             ["--clients", empty, "--rules", conf, "--extra"],
             ["--clients", HERE, "--rules", conf],
             ["--clients", "/dev/null", "--rules", conf],
             ["--clients", "/dev/zero", "--rules", conf]]
    for c in cases:
        rc, o, e = run(a.tool, c, b"[]", timeout=20)
        shown = " ".join(x.replace(HERE, "$SEAT") for x in c)
        out.append("%-72s rc=%d out=%r err=%r" % (shown, rc, o.strip()[:70], e[:30]))
    os.unlink(empty)
    os.unlink(conf)
    text = "\n".join(out) + "\n"
    open(os.path.join(HERE, "args-probe.txt"), "w").write(text)
    print(text, end="")


def redos(a):
    r43, landed = load(a.r43, "r43"), load(a.tool, "landed")
    pats = ["(a+)+", "(a|a)+", "(a*)*", "(a+)*", "(a|aa)+", "a(b+)+c", "(.*a){9}", "(?=x)y",
            "(a)\\1", "a++", "a*+", "^a$", "[a-z]+", "a\x01b", "a b", "a\\d"]
    out = ["ReDoS probe: pattern acceptance (regex_ok) and cost", "",
           "pattern              r43.regex_ok  landed.regex_ok  same?"]
    for p in pats:
        x, y = r43.regex_ok(p), landed.regex_ok(p)
        out.append("%-20r %-13s %-15s %s" % (p, x, y, "SAME" if x == y else "REGRESSION"))
    conf = os.path.join(HERE, ".probe-redos.conf")
    dump = os.path.join(HERE, ".probe-redos.json")
    open(conf, "w").write("windowrule = size 420 500, match:class (a+)+\n")
    out += ["", "cost of the accepted nested quantifier (a+)+, identical shape on both tools:",
            "  n  py.re.fullmatch  r43 wall  landed wall  r43 rc  landed rc"]
    for n in (18, 20, 22, 24, 26):
        s = "a" * n + "b"
        open(dump, "w").write(json.dumps([{"mapped": True, "floating": True, "fullscreen": 0,
                                           "size": [1, 1], "class": s}]))
        t = time.time(); re.fullmatch("(a+)+", s); dt = time.time() - t
        w = []
        for tool in (a.r43, a.tool):
            t = time.time()
            rc, _, _ = run(tool, ["--clients", dump, "--rules", conf], timeout=120)
            w.append((time.time() - t, rc))
        out.append("%3d %14.3fs %10.3fs %11.3fs %8d %10d" % (n, dt, w[0][0], w[1][0], w[0][1], w[1][1]))
    out += ["", "documented guard (SKILL.md:309 `timeout 5`):"]
    for label, n in (("n=31 class", 31), ("1024-byte class", 1024)):
        open(dump, "w").write(json.dumps([{"mapped": True, "floating": True, "fullscreen": 0,
                                           "size": [1, 1], "class": "a" * n + "b"}]))
        t = time.time()
        p = subprocess.run(["timeout", "5", sys.executable, "-I", a.tool, "--clients", dump,
                            "--rules", conf], capture_output=True)
        out.append("  %-16s rc=%d wall=%.2fs stdout_bytes=%d stderr_bytes=%d"
                   % (label, p.returncode, time.time() - t, len(p.stdout), len(p.stderr)))
    os.unlink(conf); os.unlink(dump)
    text = "\n".join(out) + "\n"
    open(os.path.join(HERE, "redos-probe.txt"), "w").write(text)
    print(text, end="")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--r43", required=True)
    ap.add_argument("--tool", required=True)
    a = ap.parse_args()
    injection(a, None)
    args(a)
    redos(a)


if __name__ == "__main__":
    main()
