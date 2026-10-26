#!/usr/bin/env python3
"""Tier 2: the frozen reference tool executed in the counter's own sandbox vs the counter's model."""
import importlib.util, json, os, random, shutil, sys, tempfile, time

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
S = "/fast/scratch/hyaku/mado-r43/RevC1Counter"
spec = importlib.util.spec_from_file_location("ctr", LANE + "/quality/counters/c1-r42-geometry.py")
ctr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ctr)
ctr.NONCE[0] = "revc1tier2"

sys.path.insert(0, S)
from harness import my_model, rnd_text, rnd_clients, CLS, SIZES, FLOATS, MAPPED  # reuse generator

ref_src = open(LANE + "/.ufo/waves/round-42/c1/ctl-ref-tool.py.txt", "rb").read()
tmp = tempfile.mkdtemp(prefix="tier2-", dir=S)
td = os.path.join(tmp, ctr.opaque("real"), "tool")
os.makedirs(td)
os.chmod(os.path.dirname(td), 0o755); os.chmod(td, 0o755)
tool = os.path.join(td, "mado-geometry.py")
open(tool, "wb").write(ref_src)

def setup_line(reason):
    return "MADO_GEOMETRY: SETUP %s\n" % reason

def S_(w, h, rx="a"):
    return "windowrule = size %d %d, match:class %s\n" % (w, h, rx)

def C_(cls, size, fl=True, **kw):
    d = {"class": cls, "size": size, "floating": fl}; d.update(kw); return d

def js(x): return json.dumps(x)

cases = []
# handcrafted
cases.append(("nan", b'[{"class":"a","size":[NaN,2],"floating":true},{"class":"a","size":[1,Infinity],"floating":true},{"class":"a","size":[1e2,2],"floating":true},{"class":"a","size":[100,2],"floating":true}]', [S_(100, 2)], None))
cases.append(("neginf", b'[{"class":"a","size":[-Infinity,2],"floating":true}]', [S_(1, 2)], None))
cases.append(("bom", b'\xef\xbb\xbf[{"class":"a","size":[1,2],"floating":true}]', [S_(1, 2)], None))
cases.append(("dupkeys", b'[{"class":"zz","class":"a","size":[9,9],"size":[1,2],"floating":false,"floating":true,"mapped":false,"mapped":true}]', [S_(1, 2)], None))
cases.append(("ctlclass", b'[{"class":"a\\nb","size":[1,2],"floating":true},{"class":"a\\tb","size":[1,2],"floating":true},{"class":"a b","size":[1,2],"floating":true},{"class":"a\\x7fb","size":[1,2],"floating":true}]', [S_(1, 2, "a.b")], None))
cases.append(("mapped", b'[' + b",".join(js(C_("a", [1, 2], mapped=m)).encode() for m in (False, True, 0, 1, None, "false", "", [], {})) + b']', [S_(1, 2)], None))
cases.append(("crlf", b'[{"class":"a","size":[1,2],"floating":true}]', ["windowrule = size 1 2, match:class a\r\n", "windowrule = size 1 2, match:class a\r"], None))
cases.append(("nbsp", b'[{"class":"a","size":[1,2],"floating":true}]', ["windowrule = size\u00a01 2, match:class a\n"], None))
cases.append(("files4", b'[{"class":"a","size":[5,6],"floating":true}]', [S_(1, 1, "z"), S_(2, 2, "y"), S_(3, 3, "x"), S_(5, 6, "a")], None))
cases.append(("files5", b'[{"class":"a","size":[5,6],"floating":true}]', [S_(1, 1, "z"), S_(2, 2, "y"), S_(3, 3, "x"), S_(4, 4, "w"), S_(5, 6, "a")], None))
cases.append(("empty", b'[]', [""], None))
cases.append(("emptyobj", b'[{}]', ["windowrule = float off, match:class a\n"], None))
for k, raw in enumerate([b"{}", b"[1]", b"", b"[", b"null", b"\"[]\"", b"[{}, 3]", b"[[]]", b"[] x", b'[{"class":"a\xffb"}]']):
    cases.append(("badjson%d" % k, raw, [S_(1, 2)], None))
cases.append(("devnull", b"", [S_(1, 2)], "DEVNULL"))
cases.append(("missingrules", b"", [S_(1, 2)], "MISSING"))
cases.append(("dirrules", b"", [S_(1, 2)], "DIR"))
cases.append(("bigsize", b'[' + js(C_("a", [99999, 99999])).encode() + b']', [S_(99999, 99999)], None))
cases.append(("bigsize2", b'[' + js(C_("a", [100000, 1])).encode() + b']', [S_(99999, 99999)], None))
cases.append(("rx200", b'[' + js(C_("x" * 150, [1, 7])).encode() + b']', ["windowrule = size 1 7, match:class %s\n" % ("x" * 150 + "|" + "y" * 49)], None))
cases.append(("rx201", b'[' + js(C_("a", [1, 7])).encode() + b']', ["windowrule = size 1 7, match:class %s\n" % ("a" * 201)], None))
cases.append(("longclass", b'[' + js(C_("a" * 60, [1, 2])).encode() + b']', [S_(1, 2, "a.*")], None))
cases.append(("floatrule", b'[' + js([C_("a", [1, 2]), C_("b", [1, 2], fl=False)]).encode() + b']', [S_(1, 2, "a|b") + "windowrule = float on, match:class a\n"], None))
cases.append(("hugeint", b'[' + js(C_("a", [10**30, 2])).encode() + b']', [S_(1, 2)], None))
cases.append(("negzero", b'[{"class":"a","size":[0,-0],"floating":true}]', [S_(1, 2)], None))
cases.append(("stdinbig", b"[]" + b" " * 1048576, [S_(1, 2)], "STDIN"))
cases.append(("stdinok", b"[]" + b" " * 1048574, [S_(1, 2)], "STDIN"))
cases.append(("usage-dup", b"", [S_(1, 2)], "ARGV:--clients X --clients X --rules R"))
cases.append(("usage-eq", b"", [S_(1, 2)], "ARGV:--clients= --rules R"))
cases.append(("usage-selftest-plus", b"", [S_(1, 2)], "ARGV:--selftest --clients X --rules R"))
# randomized
rng = random.Random(0xBEEF)
for i in range(40):
    texts = [rnd_text(rng) for _ in range(rng.randrange(1, 4))]
    clients = js(rnd_clients(rng)).encode()
    cases.append(("gen%d" % i, clients, texts, None))

mism = []
tmax, tsum = 0.0, 0.0
for name, raw, texts, mode in cases:
    d = ctr.prepare(tmp, "t2-" + name)
    rpaths = [ctr.put(d, "r%d.conf" % i, t) for i, t in enumerate(texts)]
    argv, stdin = [], None
    if mode == "STDIN":
        argv += ["--clients", "-"]; stdin = raw
    elif mode == "DEVNULL":
        argv += ["--clients", "/dev/null"]
    elif mode == "MISSING":
        argv += ["--clients", ctr.put(d, "c.json", b"[]"), "--rules", rpaths[0] + ".missing"]
    elif mode == "DIR":
        argv += ["--clients", ctr.put(d, "c.json", b"[]"), "--rules", d]
    elif isinstance(mode, str) and mode.startswith("ARGV:"):
        parts = mode[5:].split()
        for p in parts:
            if p == "X": argv += ["--clients", ctr.put(d, "c.json", b"[]")]
            elif p == "R": argv += ["--rules", rpaths[0]]
            else: argv += [p]
    else:
        argv += ["--clients", ctr.put(d, "c.json", raw)]
    for p in rpaths:
        argv += ["--rules", p]
    want = ctr.model_out(raw if mode not in ("DEVNULL", "MISSING", "DIR") and not (isinstance(mode, str) and mode.startswith("ARGV")) else b"[]", texts)
    if mode in ("DEVNULL", "MISSING", "DIR") or (isinstance(mode, str) and mode.startswith("ARGV")):
        want = (None, "unreadable") if mode in ("DEVNULL", "MISSING", "DIR") else (None, "usage")
    t0 = time.time()
    rc, out, err = ctr.execute(tool, d, argv, stdin=stdin)
    dt = time.time() - t0
    tmax, tsum = max(tmax, dt), tsum + dt
    got = (rc, out.decode("utf-8", "replace"), err.decode("utf-8", "replace"))
    if want[0] is None:
        exp = (2, setup_line(want[1]), "")
    else:
        exp = (want[1], want[0], "")
    if (got[0], got[1], got[2]) != exp:
        mism.append((name, got, exp))
print("TIER2 cases=%d mismatches=%d wall_total=%.1fs wall_max=%.2fs" % (len(cases), len(mism), tsum, tmax))
for name, got, exp in mism[:10]:
    print("  MISMATCH", name)
    print("   got:", repr(got)[:220])
    print("   exp:", repr(exp)[:220])
shutil.rmtree(tmp, ignore_errors=True)
