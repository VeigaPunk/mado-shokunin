# Counts the scale-model divergences between the reference expected_scale (double) and Hyprland's
# float32 Vector2D arithmetic (Monitor.cpp:996). Needs ref.py = the reference tool; run as
#   cp .ufo/waves/round-45/l1-draft/mado-monitors.py ref.py && python3 receipts/divergence-count.py
import struct, importlib.util, sys
def f32(x): return struct.unpack('<f', struct.pack('<f', x))[0]
spec = importlib.util.spec_from_file_location("ref", "ref.py"); ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
modes = [(1920,1080),(2560,1440),(3440,1440),(2880,1800),(3840,2160),(2880,1920),(1920,1200),(5120,1440),(2560,1600),(1280,720)]
def hypr_keeps(s,w,h):
    qx = f32(w/s); qy = f32(h/s)
    return qx == f32(float(round(qx))) and qy == f32(float(round(qy)))
certain = cond = 0
for cent in range(25, 401):          # two-decimal scales 0.25 .. 4.00
    s = f32(cent/100.0)
    for (w,h) in modes:
        hk = hypr_keeps(s,w,h); E = ref.expected_scale(s,w,h)
        if hk and (E is None or abs(E-s) >= 1e-4): certain += 1
        elif (not hk) and E is not None and abs(E-s) < 1e-4: cond += 1
print("certain(hypr-keeps)=", certain, "conditional(tool-keeps)=", cond, "total=", certain+cond)
