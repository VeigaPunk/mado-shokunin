import importlib.util, json, os, random, sys, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe2 as P

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m

ref = load(P.REF_PATH, "refx")
simp_path = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-46/w1/SimpContract/mado-devices-simplified.py"
simp = load(simp_path, "simpx")
fx, _ = P.fixture_cases(); gen = P.generated_cases(ref); hand = P.hand_cases()
corpus = fx + gen + hand
bad = [lab for lab, d, t in corpus if P.out(ref, d, t) != P.out(simp, d, t)]
print("in-process: corpus=%d differing=%d %s" % (len(corpus), len(bad), bad[:5]))
fl = P.file_level(P.REF_PATH, simp_path, os.path.dirname(P.VDIR))
fd = [(lab, a, b) for lab, a, b in fl if a != b]
print("file-level: cases=%d differing=%d %s" % (len(fl), len(fd), fd[:3]))
