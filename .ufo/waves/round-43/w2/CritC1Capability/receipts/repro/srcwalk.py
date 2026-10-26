import glob, os, re, sys
root = os.path.expanduser("~/.config/hypr/hyprland.conf")
seen, order = set(), []
def walk(p):
    p = os.path.expanduser(p)
    if p in seen: return
    seen.add(p); order.append(p)
    try:
        txt = open(p, "r", errors="replace").read()
    except OSError:
        return
    for line in txt.split("\n"):
        s = line.strip()
        if s.startswith("source =") or s.startswith("source="):
            tgt = os.path.expanduser(s.split("=",1)[1].strip())
            for q in sorted(glob.glob(tgt)):
                walk(q)
walk(root)
for p in order: print(p)
sys.stderr.write("total=%d\n" % len(order))
