import importlib.util, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe2 as P

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m

ref = load(P.REF_PATH, "refw")
fx, _ = P.fixture_cases(); corpus = fx + P.generated_cases(ref) + P.hand_cases()
base = [P.out(ref, d, t) for _, d, t in corpus]
print("corpus=%d" % len(corpus))
for vid, old, new in P.VARIANTS:
    if vid.startswith(("V53", "V49")):
        continue
    p = os.path.join(P.VDIR, vid + ".py")
    if not os.path.exists(p):
        continue
    mod = load(p, vid.replace("-", "_"))
    runs = [P.out(mod, d, t) for _, d, t in corpus]
    diffs = [i for i, (a, b) in enumerate(zip(base, runs)) if a != b]
    if not diffs:
        print("%-28s NO-DIFF  (dead candidate)" % vid)
        continue
    i = diffs[0]
    lab, d, t = corpus[i]
    refsum = base[i][0][-1]
    varsum = runs[i][0][-1]
    print("%-28s LIVE %d cases | %s | cfg=%r\n    ref rc=%s %s\n    var rc=%s %s"
          % (vid, len(diffs), lab, t[:110], base[i][1], refsum[-118:], runs[i][1], varsum[-118:]))
