import glob, os, re, sys

RULE = re.compile(r"windowrule[ \t]*=(.*)")
NUM = re.compile(r"[0-9]{1,5}")
SAFE = re.compile(r"(?:[A-Za-z0-9_.^$()|*+?-]|\\[.\-()|*+?^$\\]){1,200}")


def closure(root=os.path.expanduser("~/.config/hypr/hyprland.conf")):
    seen, order = set(), []

    def walk(p):
        p = os.path.expanduser(p)
        if p in seen:
            return
        seen.add(p)
        order.append(p)
        try:
            txt = open(p, errors="replace").read()
        except OSError:
            return
        for line in txt.split("\n"):
            s = line.strip()
            if s.startswith("source =") or s.startswith("source="):
                tgt = os.path.expanduser(s.split("=", 1)[1].strip())
                for q in sorted(glob.glob(tgt)):
                    walk(q)

    walk(root)
    return order


def supported(effect, fields, toks):
    args = toks[1:]
    good = len(fields) == 2
    if good and effect == "size":
        good = len(args) == 2 and all(NUM.fullmatch(a) for a in args)
    elif good:
        good = len(args) == 1 and args[0] in ("on", "off")
    if not good:
        return False
    m = re.fullmatch(r"match:class[ \t]+(.+)", fields[1])
    if not m:
        return False
    rx = m.group(1)
    if not SAFE.fullmatch(rx) or any(b in rx for b in ("(?", "*+", "++", "?+")):
        return False
    try:
        re.compile(rx)
    except re.error:
        return False
    return True


def rows():
    out = []
    for p in closure():
        try:
            txt = open(p, errors="replace").read()
        except OSError:
            continue
        for i, raw in enumerate(txt.split("\n"), 1):
            line = raw.strip(" \t")
            m = RULE.fullmatch(line)
            if not m:
                continue
            fields = [f.strip(" \t") for f in m.group(1).split(",")]
            toks = [t for t in re.split("[ \t]+", fields[0]) if t]
            eff = toks[0] if toks else ""
            out.append((p, i, line, eff, fields, toks))
    return out


if __name__ == "__main__":
    rs = rows()
    sf = [r for r in rs if r[3] in ("size", "float")]
    sup = [r for r in sf if supported(r[3], r[4], r[5])]
    uns = [r for r in sf if not supported(r[3], r[4], r[5])]
    if "--summary" in sys.argv:
        print("closure_files=%d windowrule_lines=%d size_float_lines=%d" %
              (len(closure()), len(rs), len(sf)))
        for eff in ("size", "float"):
            e = [r for r in sf if r[3] == eff]
            s = [r for r in e if supported(*r[3:6])]
            print("%s_lines=%d supported=%d unsupported=%d" % (eff, len(e), len(s), len(e) - len(s)))
        print("other=%d" % (len(rs) - len(sf)))
        print("unsupported_merged(size+float)=%d" % len(uns))
        raise SystemExit(0)
    for p, i, line, eff, fields, toks in sf:
        tag = "SUPPORTED" if supported(eff, fields, toks) else "UNSUPPORTED"
        print("%s %s:%d %s" % (eff.upper(), os.path.expanduser(p), i, tag))
        print("    " + line)
