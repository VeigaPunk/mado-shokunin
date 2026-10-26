import importlib.util, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe2 as P

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m

ref = load(P.REF_PATH, "refd")
cases = {
 "D1-rb-conjunct": (["V01-bracket-rb-conjunct"], [
    "device:kb_layout] = fr\n", "device {\n  name = k\n  kb_layout] = fr\n}\n", "device[a]b:kb_layout = fr\n",
    "device][kb_layout] = fr\n", "device[]:kb_layout = fr\n", "device[k]:kb_layout = fr\n",
    "device {\n  name = k\n  kb_layout] = fr\n  kb_variant] = x\n}\n"]),
 "D2-rep-isinstance": (["V03-kb-rep-isinstance"], None),
 "D3-WS-newline": (["V24-WS-no-newline"], None),
 "D4-f32-sign": (["V43b-f32-sign"], ["device[m]:scroll_factor = -1e39\n", "device[m]:scroll_factor = 1e39\n",
                                    "device[m]:scroll_factor = -1e46\n", "device[m]:scroll_factor = 1e-46\n"]),
 "D5-bracket-hoist": (["V12-bracket-hoisted"], ["device[k]:sensitivity = 1\n", "device[k]:name = z\n",
                                                "device[k]:kb_layout = fr\n", "device[k] {\n kb_layout = fr\n}\n",
                                                "device[k][m]:kb_layout = fr\n"]),
}
dumps = [("us-kb", P.dump([P.kb("k")], [P.mouse("m")])), ("mouse0", P.dump([P.kb("k")], [P.mouse("m", 0.0)])),
         ("nonstr", P.dump([{"name": "k", "layout": 5, "variant": None, "options": ["us"], "model": True,
                             "rules": 1.5}])),
         ("nan", b'{"keyboards": [{"name": "k", "layout": NaN}], "mice": []}'),
         ("empty", P.dump([], []))]
for name, (vids, cfgs) in cases.items():
    mod = load(os.path.join(P.VDIR, vids[0] + ".py"), vids[0].replace("-", "_"))
    if cfgs is None:
        cfgs = [c for c in P.HAND_CONFIGS]
    n = same = 0
    bad = []
    for c in cfgs:
        for lab, d in dumps + P.HAND_DUMPS:
            a, b = P.out(ref, d, [c]), P.out(mod, d, [c])
            n += 1
            same += a == b
            if a != b:
                bad.append((c, lab, a, b))
    print("%-22s %s: pairs=%d identical=%d differing=%d %s" % (name, vids[0], n, same, len(bad), bad[:2]))
