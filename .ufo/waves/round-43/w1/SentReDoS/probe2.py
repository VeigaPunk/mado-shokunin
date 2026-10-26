#!/usr/bin/env python3
"""Round 2 probes: legal-size amplification, pipe close, depth bomb at depth
that exceeds json's C recursion guard, and rule-count scaling."""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "bin", "mado-geometry.py")
W = os.path.join(HERE, "misc")
os.makedirs(W, exist_ok=True)
MAXB = 1048576
J = dict(separators=(",", ":"))


def put(name, data):
    p = os.path.join(W, name)
    with open(p, "w") as f:
        f.write(data)
    return p


def call(argv, stdin=b"", timeout=120):
    t0 = time.monotonic()
    try:
        p = subprocess.run([sys.executable, "-I", TOOL] + argv, input=stdin,
                           capture_output=True, timeout=timeout)
        return time.monotonic() - t0, p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired as e:
        return time.monotonic() - t0, None, e.stdout or b"", e.stderr or b"", True


def first(out):
    ls = out.decode("utf-8", "replace").splitlines()
    return ls[0][:120] if ls else ""


print("########## G. legal-size amplification (compact JSON, all inputs < 1 MiB)")
# many0 shape: 20000 tiny clients
cl = [{"class": ["a", "b", "c"][i % 3], "size": [i % 3, 2], "floating": bool(i % 2)} for i in range(20000)]
cj = json.dumps(cl, **J)
print("many0-shape clients json = %d bytes" % len(cj))
c = put("g1.json", cj)
r = put("g1.conf", "".join("windowrule = size %d 2, match:class a|b\n" % (i % 3) for i in range(300)))
dt, rc, out, err, to = call(["--clients", c, "--rules", r])
print("20000 clients x 300 rules        : %.3fs rc=%s out=%dB %s" % (dt, rc, len(out), first(out)))

# long attacker class (app_id) x rule count
for ncl, clen, nrules in ((26, 40000, 300), (26, 40000, 600), (26, 40000, 1200),
                          (26, 4000, 30000), (13, 40000, 12000)):
    cl = [{"class": "a" * clen, "size": [1, 2], "floating": True} for _ in range(ncl)]
    cj = json.dumps(cl, **J)
    c = put("g2.json", cj)
    r = put("g2.conf", "".join("windowrule = size 1 2, match:class q%05d\n" % i for i in range(nrules)))
    dt, rc, out, err, to = call(["--clients", c, "--rules", r], timeout=150)
    print("%5d clients x %5d B class x %5d rules (in=%dB, rules=%dB): %.1fs %s rc=%s"
          % (ncl, clen, nrules, len(cj), os.path.getsize(r), dt,
             "TIMEOUT" if to else "", rc))

print("\n########## H. output amplification from one client")
cl = [{"class": "c" * 900000, "size": [1, 2], "floating": True}]
cj = json.dumps(cl, **J)
c = put("h.json", cj)
r = put("h.conf", "windowrule = size 1 2, match:class .*\n")
dt, rc, out, err, to = call(["--clients", c, "--rules", r])
print("900000-char class, 1 rule: in=%dB out=%dB (x%.2f) %.3fs rc=%s" % (
    len(cj), len(out), len(out) / len(cj), dt, rc))

print("\n########## I. depth bomb past json's C recursion guard (all <= 1 MiB)")
r = put("i.conf", "windowrule = size 1 2, match:class a\n")
for d in (60000, 100000, 200000, 400000, 500000):
    body = ("[" * d + "]" * d).encode()
    if len(body) > MAXB:
        print("depth %d needs %dB > cap, skipped" % (d, len(body)))
        continue
    dt, rc, out, err, to = call(["--clients", "-", "--rules", r], stdin=body, timeout=60)
    ol = out.decode("utf-8", "replace").splitlines()
    el = err.decode("utf-8", "replace").splitlines()
    print("list depth %6d in=%7dB: %.3fs rc=%s stdout=%r stderr_lines=%d %s"
          % (d, len(body), dt, rc, ol[:1], len(el), (el[-1][:90] if el else "")))
for d in (150000,):
    body = ('[' + '{"a":' * d + "1" + "}" * d + ']').encode()
    dt, rc, out, err, to = call(["--clients", "-", "--rules", r], stdin=body, timeout=60)
    el = err.decode("utf-8", "replace").splitlines()
    print("dict depth %6d in=%7dB: %.3fs rc=%s stdout=%r stderr_lines=%d %s"
          % (d, len(body), dt, rc, out.decode()[:30], len(el), (el[-1][:90] if el else "")))

print("\n########## J. broken pipe with a large stdout")
cl = [{"class": "a" * 40000, "size": [1, 2], "floating": True} for _ in range(26)]
c = put("j.json", json.dumps(cl, **J))
r = put("j.conf", "".join("windowrule = size 1 2, match:class q%05d\n" % i for i in range(1200)))
p = subprocess.Popen([sys.executable, "-I", TOOL, "--clients", c, "--rules", r],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.stdout.read(4096)
p.stdout.close()
err = p.stderr.read()
rc = p.wait()
print("reader closes after 4 KiB: rc=%r stderr=%dB %r" % (rc, len(err), err.decode()[:400]))
