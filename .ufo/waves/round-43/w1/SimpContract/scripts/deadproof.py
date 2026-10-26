"""Proofs for the sentences that no code variant can test: the C14 overlap matrix,
the 'not floats' enumeration, and the fixture free-pass scan."""
import base64, json, os, stat, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lab

S = "/fast/scratch/hyaku/mado-r43/SimpContract/proof"
os.makedirs(S, exist_ok=True)

def W(name, data):
    p = os.path.join(S, name)
    if os.path.exists(p):
        os.chmod(p, 0o644)
    with open(p, "wb") as fh:
        fh.write(data if isinstance(data, bytes) else data.encode())
    if os.path.exists(p):
        os.chmod(p, 0o644)
    return p

R1 = W("r.conf", "windowrule = size 1 2, match:class a\n")
TINY = W("tiny.json", b"[]")
MISS = os.path.join(S, "missing")
ADIR = os.path.join(S, "adir")
os.makedirs(ADIR, exist_ok=True)
FIFO = os.path.join(S, "fifo")
if not os.path.exists(FIFO):
    os.mkfifo(FIFO)
BIG = W("big.bin", b"#" * 1048577)
HUGEBAD = W("hugebad.json", b"{" + b" " * 1048576)
BAD = W("bad.json", b"\xff[]")
NOPERM = W("noperm.json", b"[]")
os.chmod(NOPERM, 0o000)
MAXF = W("max.bin", b"#" * 1048576)
EMPTY = W("empty.bin", b"")
NOPERMBIG = W("nopermbig.bin", b"#" * 1048577)
os.chmod(NOPERMBIG, 0o000)

def kind(p):
    if not os.path.exists(p):
        return "missing"
    st = os.lstat(p)
    fmt = stat.S_IFMT(st.st_mode)
    return {stat.S_IFDIR: "directory", stat.S_IFCHR: "chardev",
            stat.S_IFIFO: "fifo", stat.S_IFREG: "regular"}.get(fmt, "other")

def reason(argv):
    rc, out = lab.cli(argv)
    line = out.decode().strip()
    return rc, line.replace("MADO_GEOMETRY: SETUP ", "SETUP ")

print("== C14 overlap matrix: which conditions hold for one input, and which reason the reference prints ==")
rows = []
for p in (MISS, ADIR, "/dev/null", FIFO, EMPTY, MAXF, BIG, BAD, HUGEBAD, NOPERM, NOPERMBIG, "/proc/kcore"):
    try:
        st = os.stat(p)
        size = st.st_size
        regular = stat.S_ISREG(st.st_mode)
    except OSError:
        size, regular = 0, False
    readable = False
    try:
        fd = os.open(p, os.O_RDONLY | os.O_NONBLOCK)
        if stat.S_ISREG(os.fstat(fd).st_mode):
            readable = True
        os.close(fd)
    except OSError:
        readable = False
    c_rc, c_reason = reason(["--clients", p, "--rules", R1])
    r_rc, r_reason = reason(["--clients", TINY, "--rules", p])
    rows.append({"path": p.replace(S, "S"), "kind": kind(p), "st_size": size,
                 "regular": regular, "openable_as_regular": readable,
                 "condition_unreadable": not readable,
                 "condition_too_large": regular and size > 1048576,
                 "clients_reason": c_reason, "rules_reason": r_reason})
    print("%-22s kind=%-9s size=%-14d reg=%d open=%d | unreadable=%d too_large=%d | clients:%s rules:%s" % (
        rows[-1]["path"], rows[-1]["kind"], size, regular, readable,
        rows[-1]["condition_unreadable"], rows[-1]["condition_too_large"],
        c_reason, r_reason))
json.dump(rows, open(os.path.join(S, "order-matrix.json"), "w"), indent=1)

print("\n== the 'integers, not floats' pair: no JSON token is both ==")
TOKENS = ["1", "1.0", "1e0", "1E0", "1.5", "0.0", "-0.0", "0", "-1",
          "1000000000000000000000000000000", "true", "false", "null", "1.", ".5", "01"]
for tok in TOKENS:
    raw = ('[{"class":"a","size":[%s,8],"floating":true}]' % tok).encode()
    rc, out = lab.cli(["--clients", "-", "--rules", R1], raw)
    line = out.decode().strip().splitlines()[-1]
    verdict = line.split(" verdict=")[-1]
    try:
        parsed = json.loads(raw)[0]["size"][0]
        ptype = type(parsed).__name__
        acc = "yes" if isinstance(parsed, int) and not isinstance(parsed, bool) and parsed >= 0 else "no"
    except ValueError:
        ptype, acc = "(not JSON)", "input is bad_json"
    print("token=%-32s python_type=%-11s accepted_size=%-6s verdict=%s" % (tok, ptype, acc, verdict))

print("\n== the fixture free-pass scan (what no fixture input contains) ==")
fx = json.load(open("/fast/scratch/hyaku/mado-r43/SimpContract/fixscan/fixtures.json"))
seen = {}
def hit(k, tag):
    seen.setdefault(k, []).append(tag)
paths_all = []
for f in fx:
    for r in f["runs"]:
        out = r["out"]
        argv = r["argv"]
        raw_stdin = base64.b64decode(r["stdin_b64"]) if r["stdin_b64"] else b""
        nrule = argv.count("--rules")
        if nrule and "--clients" in argv and argv.index("--rules") < argv.index("--clients"):
            if not (out.startswith("MADO_GEOMETRY: SETUP") and out.strip().endswith("usage")):
                hit("valid run with --rules before --clients", f["fixture"])
            hit("any run with --rules before --clients", f["fixture"])
        if nrule >= 2 and out.startswith("MADO_GEOMETRY: SETUP"):
            hit("setup failure with two or more rules files", f["fixture"])
        for name, ent in r["files"].items():
            if "b64" not in ent:
                continue
            raw = base64.b64decode(ent["b64"])
            if name.endswith(".conf"):
                try:
                    raw.decode("utf-8")
                except UnicodeDecodeError:
                    hit("rules file with invalid UTF-8", f["fixture"] + ":" + name)
                if b";" in raw:
                    hit("rule line containing ';'", f["fixture"] + ":" + name)
                if b"windowrule = size\n" in raw or b"windowrule = size \n" in raw:
                    hit("size effect with zero arguments", f["fixture"] + ":" + name)
                if b'"address"' in raw and raw.count(b'"address"') > 1:
                    pass
            else:
                for m in __import__("re").finditer(rb"\{[^{}]*\}", raw):
                    if m.group(0).count(b'"address"') > 1:
                        hit("duplicate address key", f["fixture"])
                if b'"mapped"' in raw and raw.count(b'"mapped"') > 1 and False:
                    pass
        for a in argv:
            if a.startswith("/") and os.path.exists(a):
                try:
                    if (os.stat(a).st_mode & 0o777) == 0:
                        hit("path with mode 000 (EACCES)", f["fixture"])
                except OSError:
                    pass
            paths_all.append(a)
for k in sorted(seen):
    print("%-46s %d  %s" % (k, len(seen[k]), ",".join(sorted(set(seen[k]))[:5])))
for k in ("valid run with --rules before --clients", "rules file with invalid UTF-8",
          "setup failure with two or more rules files", "rule line containing ';'",
          "size effect with zero arguments", "duplicate address key", "path with mode 000 (EACCES)"):
    if k not in seen:
        print("%-46s 0  (none)" % k)
