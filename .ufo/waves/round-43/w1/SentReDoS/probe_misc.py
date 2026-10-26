#!/usr/bin/env python3
"""Non-ReDoS probes: output injection, JSON depth bombs, path handling,
integer abuse, amplification, broken pipe, stderr leakage."""
import json
import os
import resource
import socket
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "bin", "mado-geometry.py")
W = os.path.join(HERE, "misc")
os.makedirs(W, exist_ok=True)
MAXB = 1048576


def put(name, data, mode="w"):
    p = os.path.join(W, name)
    with open(p, mode) as f:
        f.write(data)
    return p


def call(argv, stdin=b"", timeout=120, env=None):
    t0 = time.monotonic()
    p = subprocess.run([sys.executable, "-I", TOOL] + argv, input=stdin,
                       capture_output=True, timeout=timeout, env=env)
    return time.monotonic() - t0, p.returncode, p.stdout, p.stderr


def show(tag, dt, rc, out, err, maxlines=6):
    print("== %s  time=%.3fs rc=%s stdout=%dB stderr=%dB" % (tag, dt, rc, len(out), len(err)))
    for line in out.decode("utf-8", "replace").splitlines()[:maxlines]:
        print("   OUT| %s" % line.replace("\x00", "<NUL>"))
    if len(out.decode("utf-8", "replace").splitlines()) > maxlines:
        print("   OUT| ... (%d more lines)" % (len(out.decode("utf-8", "replace").splitlines()) - maxlines))
    for line in err.decode("utf-8", "replace").splitlines()[:8]:
        print("   ERR| %s" % line)


# ---------------------------------------------------------------- injection
def probes_injection():
    print("\n########## A. output injection (attacker-chosen class / address)")
    rules = put("inj.conf", "windowrule = size 420 500, match:class .*\nwindowrule = float on, match:class .*\n")
    evil = [
        ("quote+verdict forge", 'x" verdict=DIFFER float_rule=on "'),
        ("newline in class", "gkeep\nMADO_GEOMETRY: rules=0 verdict=OK"),
        ("carriage return", "gkeep\rMADO_GEOMETRY: rules=0"),
        ("LSEP U+2028", "gkeep\u2028MADO_GEOMETRY: rules=0"),
        ("NEL U+0085", "gkeep\u0085MADO_GEOMETRY: rules=0"),
        ("full forged line", 'MADO_GEOMETRY: rules=0 verdict=OK'),
        ("backslash-quote", 'a\\" verdict=AGREE'),
    ]
    for tag, cls in evil:
        c = put("inj.json", json.dumps([{"class": cls, "size": [1, 2], "floating": True,
                                         "mapped": True, "address": "0x1"}]))
        dt, rc, out, err = call(["--clients", c, "--rules", rules])
        show("class=%r" % tag, dt, rc, out, err)
    # address field
    addr = '0x1" floating=false verdict=TILED x="'
    c = put("inj2.json", json.dumps([{"class": "gkeep", "size": [420, 500], "floating": True,
                                      "mapped": True, "address": addr}]))
    dt, rc, out, err = call(["--clients", c, "--rules", rules])
    show("address=%r" % addr[:20], dt, rc, out, err)
    # regex side: can a rule's REGEX forge the RULE line? SAFE alphabet has no newline/space/=
    for rx in ("a=b", "a b", "a\nb"):
        r = put("inj3.conf", "windowrule = size 1 2, match:class %s\n" % rx)
        dt, rc, out, err = call(["--clients", put("inj3.json", "[]"), "--rules", r])
        show("rule regex=%r" % rx, dt, rc, out, err, 3)


# ---------------------------------------------------------------- depth bomb
def probes_depth():
    print("\n########## B. JSON depth bombs / big ints")
    r = put("d.conf", "windowrule = size 1 2, match:class a\n")
    for d in (50, 500, 1000, 2000, 5000, 50000):
        body = ("[" * d + "]" * d).encode()
        dt, rc, out, err = call(["--clients", "-", "--rules", r], stdin=body)
        show("list-nest depth=%d bytes=%d" % (d, len(body)), dt, rc, out, err, 2)
    for d in (500, 2000, 50000):
        body = ("[" + '{"a":' * d + "1" + "}" * d + "]").encode()
        dt, rc, out, err = call(["--clients", "-", "--rules", r], stdin=body)
        show("dict-nest depth=%d bytes=%d" % (d, len(body)), dt, rc, out, err, 2)
    for nd in (4300, 4301, 5000):
        body = ('[{"class":"a","size":[%s,2],"floating":true,"mapped":true}]'
                % ("9" * nd)).encode()
        dt, rc, out, err = call(["--clients", "-", "--rules", r], stdin=body)
        show("int digits=%d bytes=%d" % (nd, len(body)), dt, rc, out, err, 2)


# ---------------------------------------------------------------- paths
def probes_paths():
    print("\n########## C. path handling for --rules / --clients")
    good = put("ok.json", "[]")
    fifo = os.path.join(W, "fifo")
    if not os.path.exists(fifo):
        os.mkfifo(fifo)
    sock = os.path.join(W, "sock")
    if not os.path.exists(sock):
        s = socket.socket(socket.AF_UNIX)
        s.bind(sock)
        s.close()
    loop = os.path.join(W, "loop")
    if not os.path.lexists(loop):
        os.symlink(loop, loop)
    etc = os.path.join(W, "passwd-link")
    if not os.path.lexists(etc):
        os.symlink("/etc/passwd", etc)
    fi = os.path.join(W, "fifo-link")
    if not os.path.lexists(fi):
        os.symlink(fifo, fi)
    cands = ["/proc/self/environ", "/proc/self/cmdline", "/proc/self/mem",
             "/proc/self/stat", "/proc/self/maps", "/dev/zero", "/dev/null",
             "/proc/kmsg", "/sys/kernel/mm/transparent_hugepage/enabled",
             fifo, sock, loop, etc, fi, "/dev/fd/0", "/proc/self/fd/0",
             "/proc/self/cwd", W, "/etc/shadow"]
    for path in cands:
        dt, rc, out, err = call(["--clients", good, "--rules", path], timeout=30)
        tag = "rules=%s" % path
        line = (out + err).decode("utf-8", "replace").replace("\x00", "<NUL>").strip().splitlines()
        print("   %-52s rc=%s %-3s %s" % (tag, rc, "%.3fs" % dt, (line[0][:80] if line else "")))
    # a /proc pseudo-file as --clients (regular by fstat, not JSON)
    for path in ("/proc/self/environ", "/proc/self/cmdline"):
        dt, rc, out, err = call(["--clients", path, "--rules", put("p.conf", "windowrule = size 1 2, match:class a\n")])
        line = (out + err).decode("utf-8", "replace").replace("\x00", "<NUL>").strip().splitlines()
        print("   %-52s rc=%s %-3s %s" % ("clients=%s" % path, rc, "%.3fs" % dt, (line[0][:80] if line else "")))


# ---------------------------------------------------------------- amplification
def probes_amp():
    print("\n########## D. amplification (legal inputs, no ambiguity)")
    # D1: 20k clients x 300 rules (the many0 shape) at tiny class length
    cl = [{"class": ["a", "b", "c"][i % 3], "size": [i % 3, 2], "floating": bool(i % 2),
           "mapped": True, "address": "0x%x" % i} for i in range(20000)]
    c = put("amp1.json", json.dumps(cl))
    r = put("amp1.conf", "".join("windowrule = size %d 2, match:class a|b\n" % (i % 3) for i in range(300)))
    dt, rc, out, err = call(["--clients", c, "--rules", r])
    show("20000 clients x 300 rules", dt, rc, out, err, 0)
    # D2: 26 clients with 40 KiB classes x 300 rules = 320M char comparisons, linear engine
    big = "a" * 40000
    cl = [{"class": big, "size": [1, 2], "floating": True, "mapped": True, "address": "0x1"}] * 26
    c = put("amp2.json", json.dumps(cl))
    dt, rc, out, err = call(["--clients", c, "--rules", r])
    show("26 clients x 40KiB class x 300 rules", dt, rc, out, err, 0)
    # D3: re cache thrash: 600 distinct rules x 20000 clients
    r2 = put("amp3.conf", "".join("windowrule = size 1 2, match:class gkeep%03d\n" % i for i in range(600)))
    dt, rc, out, err = call(["--clients", c, "--rules", r2])
    show("26 clients x 40KiB class x 600 distinct rules", dt, rc, out, err, 0)
    cl = [{"class": "gkeep%03d" % (i % 600), "size": [1, 2], "floating": True,
           "mapped": True, "address": "0x1"} for i in range(20000)]
    c2 = put("amp4.json", json.dumps(cl))
    dt, rc, out, err = call(["--clients", c2, "--rules", r2])
    show("20000 clients x 600 distinct rules (cache size 512)", dt, rc, out, err, 0)
    # D4: 1 MiB rules file, all supported -> parse + compile cost
    n = (MAXB - 200) // 34
    r3 = put("amp5.conf", "".join("windowrule = size 1 2, match:class q%04d\n" % i for i in range(n)))
    dt, rc, out, err = call(["--clients", put("amp5.json", "[]"), "--rules", r3], timeout=300)
    show("1MiB rules file (%d rules) clients=[]" % n, dt, rc, out, err, 0)
    # D5: one 1 MiB line, comma/token heavy
    r4 = put("amp6.conf", "windowrule = size " + "a " * (MAXB // 2 - 20) + ", match:class a\n")
    dt, rc, out, err = call(["--clients", put("amp6.json", "[]"), "--rules", r4], timeout=300)
    show("1MiB single rule line, 500k tokens", dt, rc, out, err, 0)


# ---------------------------------------------------------------- broken pipe
def probes_pipe():
    print("\n########## E. broken pipe / stderr")
    cl = [{"class": "gkeep", "size": [420, 500], "floating": True, "mapped": True,
           "address": "0x%x" % i} for i in range(20000)]
    c = put("pipe.json", json.dumps(cl))
    r = put("pipe.conf", "windowrule = size 420 500, match:class .*\n")
    consumer = subprocess.run(
        "%s -I %s --clients %s --rules %s | head -c 40 >/dev/null; exit ${PIPESTATUS[0]}"
        % (sys.executable, TOOL, c, r), shell=True, executable="/bin/bash",
        capture_output=True)
    print("== tool | head -c 40 : pipeline rc=%r stderr=%r" % (consumer.returncode, consumer.stderr.decode()[:600]))
    # explicit: measure the tool's own stderr when the reader closes early
    p = subprocess.Popen([sys.executable, "-I", TOOL, "--clients", c, "--rules", r],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.stdout.read(40)
    p.stdout.close()
    err = p.stderr.read()
    rc = p.wait()
    print("== reader closes after 40B: rc=%r stderr=%d bytes: %r" % (rc, len(err), err.decode()[:600]))


# ---------------------------------------------------------------- misc
def probes_misc():
    print("\n########## F. misc boundaries")
    r = put("m.conf", "windowrule = size 1 2, match:class a\n")
    # huge size values that are legal JSON ints < 4300 digits
    body = ('[{"class":"a","size":[%s,%s],"floating":true,"mapped":true,"address":"0x1"}]'
            % ("9" * 4200, "9" * 4200)).encode()
    dt, rc, out, err = call(["--clients", "-", "--rules", r], stdin=body)
    show("size=2x4200-digit int (legal json)", dt, rc, out, err, 2)
    # 1 MiB of clients, each tiny, all matched -> output amplification
    cl = [{"class": "a", "size": [1, 2], "floating": True, "mapped": True, "address": "0x1"}]
    unit = json.dumps(cl)[1:-1] + ","
    k = (MAXB - 10) // len(unit)
    body = ("[" + unit * k + '{"class":"a","size":[1,2],"floating":true,"mapped":true,"address":"0x1"}]').encode()
    dt, rc, out, err = call(["--clients", "-", "--rules", r], stdin=body)
    show("1MiB clients -> %d lines" % out.count(b"\n"), dt, rc, out, err, 0)
    # stdout size ratio
    print("   amplification: stdin=%dB stdout=%dB (x%.2f)" % (len(body), len(out), len(out) / len(body)))
    # unreadable path message never echoes the path
    dt, rc, out, err = call(["--clients", "-", "--rules", "/nonexistent/secret-name"])
    print("   unreadable path echo: stdout=%r stderr=%r" % (out, err))


if __name__ == "__main__":
    which = sys.argv[1:] or ["A", "B", "C", "D", "E", "F"]
    for w in which:
        {"A": probes_injection, "B": probes_depth, "C": probes_paths,
         "D": probes_amp, "E": probes_pipe, "F": probes_misc}[w]()
