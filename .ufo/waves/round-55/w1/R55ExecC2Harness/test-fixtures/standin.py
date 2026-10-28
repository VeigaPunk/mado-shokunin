#!/usr/bin/env python3
import json, os, stat, sys
NAMES = ("repeat_rate", "repeat_delay", "numlock_by_default")
DEF = {"repeat_rate": 25, "repeat_delay": 600, "numlock_by_default": 0}
RNG = {"repeat_rate": (0, 200), "repeat_delay": (0, 2000), "numlock_by_default": (0, 1)}
OPTS = ["input:repeat_rate", "input:repeat_delay", "input:numlock_by_default"]
def setup(r):
    sys.stdout.write("MADO_KBDOPT: SETUP %s\n" % r); return 2
def readf(p):
    try:
        st = os.stat(p)
        if not stat.S_ISREG(st.st_mode): raise OSError
        if st.st_size > 1048576: return "too_large"
        return open(p, "rb").read()
    except OSError:
        return None
def toint(v):
    if v.startswith(("true", "on", "yes")): return 1
    if v.startswith(("false", "off", "no")): return 0
    return int(v) if v.isdigit() and v.isascii() else None
def main(argv):
    cfg, kbs, go = [], [], []
    i = 0
    while i < len(argv):
        if i + 1 >= len(argv): return setup("usage")
        f, v = argv[i], argv[i+1]
        if f == "--config": cfg.append(v)
        elif f == "--keyboard": kbs.append(v)
        elif f == "--getoption" and not go: go.append(v)
        else: return setup("usage")
        i += 2
    if not cfg: return setup("usage")
    data = []
    for p in cfg + go:
        d = readf(p)
        if d is None: return setup("unreadable")
        if d == "too_large": return setup("too_large")
        data.append(d)
    live = {}
    if go:
        for ln in data[-1].decode("utf-8", "replace").split("\n"):
            ln = ln.strip(" \t\r\n\v\f")
            if not ln: continue
            try: o = json.loads(ln)
            except ValueError: return setup("bad_json")
            if not isinstance(o, dict): return setup("bad_json")
            if isinstance(o.get("option"), str) and isinstance(o.get("int"), int) and not isinstance(o.get("int"), bool):
                live[o["option"]] = o["int"]
    glob, dev, unsup = {}, {}, 0
    WS = " \t\r\n\v\f"
    for blob in data[:len(cfg)]:
        stack, cur = [], None
        for raw in blob.decode("utf-8", "replace").split("\n"):
            line = raw.strip(WS)
            if not line or line[0] == "#": continue
            if "=" not in line:
                if line == "}":
                    if stack: stack.pop()
                    if not stack: cur = None
                elif line.endswith("{"): stack.append(line[:-1].strip(WS))
                continue
            lhs, rhs = (x.strip(WS) for x in line.split("=", 1))
            if lhs.startswith("$") or lhs == "source": continue
            key = ":".join(stack + [lhs]) if stack else lhs
            rel = key in ("input:repeat_rate", "input:repeat_delay", "input:numlock_by_default") \
                or (stack == ["device"] and lhs in NAMES) \
                or (key.startswith("device[") and key.split(":")[-1] in NAMES)
            if stack == ["device"] and lhs == "name":
                cur = rhs.split("#", 1)[0].strip(WS); dev.setdefault(cur, {}); continue
            if not rel: continue
            if key.startswith("device["): unsup += 1; continue
            if "$" in line or "{{" in line or "\\" in line: unsup += 1; continue
            if "##" in rhs: unsup += 1; continue
            val = rhs.split("#", 1)[0].strip(WS)
            n = toint(val)
            if n is None: unsup += 1; continue
            nm = key.split(":")[-1]
            if not RNG[nm][0] <= n <= RNG[nm][1]: unsup += 1; continue
            if stack == ["device"]:
                if cur is None: unsup += 1; continue
                dev[cur][nm] = n
            else: glob[nm] = n
    out = []
    for kb in (kbs or ["*"]):
        vals, frm = [], []
        for nm in NAMES:
            if kb in dev and nm in dev[kb]: vals.append(dev[kb][nm]); frm.append("D")
            elif nm in glob: vals.append(glob[nm]); frm.append("G")
            else: vals.append(DEF[nm]); frm.append("-")
        out.append("MADO_KBDOPT: keyboard=%s repeat_rate=%d repeat_delay=%d numlock=%d from=%s unsupported=%d\n" % (kb, *vals, "/".join(frm), unsup))
    verd = []
    if go:
        for o, nm in zip(OPTS, NAMES):
            c = glob.get(nm, DEF[nm]); l = live.get(o)
            v = "UNKNOWN" if l is None else ("AGREE" if l == c else "DIFFER")
            verd.append(v)
            out.append("MADO_KBDOPT_LIVE: option=%s config=%d live=%s verdict=%s\n" % (o, c, "?" if l is None else l, v))
    agg = "NONE" if not go else ("DIFFER" if "DIFFER" in verd else "UNKNOWN" if "UNKNOWN" in verd else "AGREE")
    out.append("MADO_KBDOPT: DONE keyboards=%d unsupported=%d live=%s\n" % (len(kbs or ["*"]), unsup, agg))
    sys.stdout.write("".join(out)); return 0
sys.exit(main(sys.argv[1:]))
