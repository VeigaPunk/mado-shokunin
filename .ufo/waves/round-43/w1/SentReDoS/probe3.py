#!/usr/bin/env python3
"""Round 3 (tight): ReDoS killing size, >1 MiB stdout broken pipe, rules sources."""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "bin", "mado-geometry.py")
W = os.path.join(HERE, "misc")
os.makedirs(W, exist_ok=True)
J = dict(separators=(",", ":"))


def put(name, data):
    p = os.path.join(W, name)
    with open(p, "w") as f:
        f.write(data)
    return p


def call(argv, stdin=b"", timeout=60):
    t0 = time.monotonic()
    try:
        p = subprocess.run([sys.executable, "-I", TOOL] + argv, input=stdin,
                           capture_output=True, timeout=timeout)
        return time.monotonic() - t0, p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired as e:
        return time.monotonic() - t0, None, e.stdout or b"", e.stderr or b"", True


def P(*a):
    print(*a, flush=True)


def one(rx, cls, timeout=60):
    r = put("k.conf", "windowrule = size 420 500, match:class %s\n" % rx)
    c = put("k.json", json.dumps([{"class": cls, "size": [420, 500], "floating": True}], **J))
    return call(["--clients", c, "--rules", r], timeout=timeout)


P("########## K. ReDoS killing size (class = 'a'*(n-1) + '!'; rule accepted, rules=1)")
for rx in ("(a+)+$", "(a|aa)+$"):
    for n in (28, 29, 30, 31, 33):
        dt, rc, out, err, to = one(rx, "a" * (n - 1) + "!", timeout=45)
        P("  rx=%-9s class_len=%3d  %8.2fs  %s rc=%s" % (rx, n, dt, "TIMEOUT@45s" if to else "", rc))
P("  (a|aa)+$ onset further out (timeout 30):")
for n in (60, 100, 200, 400):
    dt, rc, out, err, to = one("(a|aa)+$", "a" * (n - 1) + "!", timeout=30)
    P("  rx=(a|aa)+$ class_len=%4d  %8.2fs  %s rc=%s" % (n, dt, "TIMEOUT@30s" if to else "", rc))
dt, rc, out, err, to = one("(a|b)+$", "a" * 999, timeout=30)
P("  control rx=(a|b)+$ class_len=1000  %.3fs rc=%s" % (dt, rc))

P("\n########## L. broken pipe with a >1 MiB stdout")
cl = [{"class": "b" * 40000, "size": [1, 2], "floating": True} for _ in range(26)]
c = put("l.json", json.dumps(cl, **J))
r = put("l.conf", "windowrule = size 1 2, match:class .*\n")
dt, rc, out, err, to = call(["--clients", c, "--rules", r], timeout=60)
P("  full run: %.3fs rc=%s stdout=%dB stderr=%dB" % (dt, rc, len(out), len(err)))
p = subprocess.Popen([sys.executable, "-I", TOOL, "--clients", c, "--rules", r],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.stdout.read(4096)
p.stdout.close()
err = p.stderr.read()
rc2 = p.wait()
P("  reader closes after 4 KiB: rc=%r stderr=%dB %r" % (rc2, len(err), err.decode()[:300]))
q = subprocess.run("%s -I %s --clients %s --rules %s | head -c 100 >/dev/null"
                   % (sys.executable, TOOL, c, r), shell=True, executable="/bin/bash",
                   capture_output=True)
P("  via '| head -c 100': bash rc=%r stderr=%r" % (q.returncode, q.stderr.decode()[:300]))

P("\n########## M. rules sources: binary / other files (decode errors replaced)")
m = put("m.json", "[]")
for path in (TOOL, "/bin/ls", "/etc/passwd", "/proc/self/maps"):
    dt, rc, out, err, to = call(["--clients", m, "--rules", path], timeout=30)
    ls = out.decode("utf-8", "replace").splitlines()
    P("  rules=%-22s rc=%s %.3fs %s" % (path, rc, dt, (ls[-1][:70] if ls else "")))
