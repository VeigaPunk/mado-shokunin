import json
import os
import subprocess
import sys

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w1/ExecC1ExtraMutants"
W = "/fast/scratch/hyaku/mado-r43/ExecC1ExtraMutants/witness"
REF = os.path.join(SEAT, "ref.py")
MUT = os.path.join(SEAT, "mutants")
MAX = 1048576
OUT = open(os.path.join(SEAT, "witness.txt"), "w")


def say(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    OUT.write(line + "\n")


def run(tool, argv, stdin=None, pre=None):
    cmd = (pre or []) + [sys.executable, "-I", tool] + argv
    p = subprocess.run(cmd, capture_output=True, input=stdin,
                       cwd=W, env={"PATH": "/usr/bin", "HOME": "/nonexistent"})
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


os.makedirs(W, exist_ok=True)
rules = os.path.join(W, "r.conf")
open(rules, "w").write("windowrule = size 1 2, match:class a\n")
cl = os.path.join(W, "c.json")
open(cl, "w").write('[{"class":"a","size":[1,2],"floating":true}]')

say("== C. N01 (stdin.read(MAX_BYTES + 2)) — end-to-end at the stdin size boundary")
say("   both tools: --clients - --rules r.conf; stdin = b'[]' padded with spaces")
for size, label in [(2, "2 (empty list)"), (MAX - 1, "MAX-1"), (MAX, "MAX"),
                    (MAX + 1, "MAX+1"), (MAX + 2, "MAX+2"), (2 * MAX, "2*MAX")]:
    body = b"[]" + b" " * (size - 2)
    a = run(REF, ["--clients", "-", "--rules", rules], stdin=body)
    b = run(os.path.join(MUT, "N01-stdin-read-plus2.py"), ["--clients", "-", "--rules", rules], stdin=body)
    say("  size=%-10s ref=(rc=%d,%r) mut=(rc=%d,%r) same=%s"
        % (label, a[0], a[1][:30], b[0], b[1][:30], a == b))

say("")
say("== D. N54 (os.read(fd, MAX_BYTES) chunk cap) — end-to-end at the file size boundary")
for size, label in [(MAX - 1, "MAX-1"), (MAX, "MAX"), (MAX + 1, "MAX+1"), (2 * MAX, "2*MAX")]:
    body = b"[]" + b" " * (size - 2)
    p = os.path.join(W, "cbig.json")
    open(p, "wb").write(body)
    a = run(REF, ["--clients", p, "--rules", rules])
    b = run(os.path.join(MUT, "N54-read-chunk-cap.py"), ["--clients", p, "--rules", rules])
    say("  clients file size=%-10s ref=(rc=%d,%r) mut=(rc=%d,%r) same=%s"
        % (label, a[0], a[1][:30], b[0], b[1][:30], a == b))
for size, label in [(MAX, "MAX"), (MAX + 1, "MAX+1")]:
    p = os.path.join(W, "rbig.conf")
    open(p, "wb").write(b"windowrule = size 1 2, match:class a\n" + b"#" * (size - 37))
    a = run(REF, ["--clients", cl, "--rules", p])
    b = run(os.path.join(MUT, "N54-read-chunk-cap.py"), ["--clients", cl, "--rules", p])
    say("  rules file size=%-12s ref=(rc=%d,%r) mut=(rc=%d,%r) same=%s"
        % (label, a[0], a[1][:40].replace("\n", "|"), b[0], b[1][:40].replace("\n", "|"), a == b))

say("")
say("== E. N48 (rules decode errors='ignore') — MISSING CHECK witness")
bad = os.path.join(W, "badutf8.conf")
open(bad, "wb").write(b"windowrule = size 1 2, match:class a\xff\n")
a = run(REF, ["--clients", cl, "--rules", bad])
b = run(os.path.join(MUT, "N48-rules-decode-ignore.py"), ["--clients", cl, "--rules", bad])
say("  rules file bytes: b'windowrule = size 1 2, match:class a\\xff\\n'")
say("  ref:  rc=%d stdout=%r" % (a[0], a[1]))
say("  mut:  rc=%d stdout=%r" % (b[0], b[1]))
say("  expectation (model): regex 'a\\ufffd' is outside the SAFE alphabet -> unsupported=1, "
    "rules=0 -> NO_SIZE_RULES, exit 4")

say("")
say("== F. N51 (os.close(fd) -> pass) — MISSING CHECK witness under a low RLIMIT_NOFILE")
fd = os.path.join(W, "fd")
os.makedirs(fd, exist_ok=True)
nr = 300
paths = []
for i in range(nr):
    p = os.path.join(fd, "r%03d.conf" % i)
    with open(p, "w") as fh:
        fh.write("windowrule = size 1 2, match:class a\n" if i == 0 else "")
    paths.append(p)
argv = ["--clients", cl]
for p in paths:
    argv += ["--rules", p]
for lim in (128, 64, 32):
    pre = ["/usr/bin/prlimit", "--nofile=%d:%d" % (lim, lim)]
    a = run(REF, argv, pre=pre)
    b = run(os.path.join(MUT, "N51-close-fd-pass.py"), argv, pre=pre)
    say("  nofile=%-4d files=%d ref=(rc=%d,%r) mut=(rc=%d,%r) same=%s"
        % (lim, nr, a[0], a[1][:34], b[0], b[1][:34], a == b))
say("  expectation (model): 300 rules files of <= 1 MiB each, all readable, one supported size rule "
    "and one client that matches it -> MADO_GEOMETRY: rules=1 float_rules=0 other=0 unsupported=0 "
    "clients=1 matched=1 unmapped=0 agree=1 differ=0 tiled=0 badsize=0 verdict=OK, exit 0")

say("")
say("== G. N68 (sys.stdout.write -> print) — end-to-end byte comparison")
for label, argv, stdin in [
        ("agree", ["--clients", cl, "--rules", rules], None),
        ("differ", ["--clients", os.path.join(W, "cd.json"), "--rules", rules], None),
        ("no-size-rules", ["--clients", cl, "--rules", os.path.join(W, "float.conf")], None),
        ("setup-unreadable", ["--clients", "/dev/null", "--rules", rules], None)]:
    a = run(REF, argv, stdin=stdin)
    b = run(os.path.join(MUT, "N68-stdout-print.py"), argv, stdin=stdin)
    say("  %-16s ref=(rc=%d,stderr=%r) mut=(rc=%d,stderr=%r) same_stdout=%s same_rc=%s"
        % (label, a[0], a[2][:20], b[0], b[2][:20], a[1] == b[1], a[0] == b[0]))

OUT.close()
