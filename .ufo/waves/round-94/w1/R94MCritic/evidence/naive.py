import sys, os
mode = sys.argv[1]            # exact | folded
arg = sys.argv[2:]            # dh:
dh = arg[0]; names = arg[1:]
g = os.path.join(dh, "mime", "globs2")
best = {}
if os.path.exists(g):
    for line in open(g, "rb").read().split(b"\n"):
        p = line.split(b":")
        if len(p) < 3: continue
        try: w = int(p[0])
        except ValueError: continue
        mt, pat = p[1], p[2]
        if not pat.startswith(b"*."): continue
        ext = pat[2:]
        if mode == "folded": ext = ext.lower()
        cur = best.get(ext)
        if cur is None or w > cur[0]: best[ext] = (w, mt)
for n in names:
    b = n.encode()
    ext = b.rsplit(b".", 1)[1] if b"." in b else b""
    if mode == "folded": ext = ext.lower()
    hit = best.get(ext)
    print("%s\t%s\t%d" % (n, hit[1].decode() if hit else "application/octet-stream", 0 if hit else 1))
