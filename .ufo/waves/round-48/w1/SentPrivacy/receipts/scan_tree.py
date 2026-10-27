import importlib.util, os, sys
LANE = os.environ.get("MADO_LANE", ".")          # run from the lane root, or set MADO_LANE
GATE = os.path.join(LANE, "quality", "check-session-material.py")
spec = importlib.util.spec_from_file_location("csm", GATE)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
roots = sys.argv[1:]
for root in roots:
    for base, dirs, files in os.walk(root):
        for name in sorted(files):
            path = os.path.join(base, name)
            try:
                if os.path.getsize(path) > 1 << 20: continue
                data = open(path, "rb").read()
            except OSError:
                continue
            found = m.scan_blob(data, m.DEFAULT_HOME_LIMIT)
            if found:
                print("\t".join([path] + ["%s=%d" % (r, c) for r, c, _d in found]))
