#!/usr/bin/env python3
"""ExecC2Census: is clause h a derivation from the pinned bytes or a constant?
Import the frozen counter as a module (no side effects: main() is guarded) and call
host_census with mutated receipt bytes."""
import importlib.util
import os
import re

CNT = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c2-r45-monitor-entry.py"
F = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/fetch/"

spec = importlib.util.spec_from_file_location("c2", CNT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

names = m.PINS.keys()
raw = {("S%03d" % (300 + k + 2)): open(F + n, "rb").read() for k, n in enumerate(sorted(names))}
# map ids to the actual receipt path the Gate would name (clause h keys by basename)
gates = {}
for k, n in enumerate(sorted(names)):
    gates["S%03d" % (302 + k)] = [(m.FETCH + n, "", "")]

want0, _ = None, None
CEN = open("/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-45/l1-draft/entry.md").read()
lines = m.unfenced(CEN)
ok, want = m.host_census(set(raw), "x", gates, raw, lines)
print("baseline ok=", ok, "line:", want[0] if want else None)

def probe(label, key, old, new):
    r2 = dict(raw)
    hit = [i for i, b in r2.items() if old.encode() in b]
    if len(hit) != 1:
        print("%-22s SETUP hit=%s" % (label, hit))
        return
    r2[hit[0]] = r2[hit[0]].replace(old.encode(), new.encode(), 1)
    ok2, w2 = m.host_census(set(r2), "x", gates, r2, lines)
    # would the L1 census line still be the exactly-once line?
    emit = sum(1 for l in CEN.splitlines() if l == (w2[0] if w2 else ""))
    print("%-22s ok=%s derived=%s entry_line_still_present=%d" % (
        label, ok2, (w2[0] if w2 else "NONE"), emit))


probe("refresh 60->50", "default_refresh", "m_refreshRate   = 60; // Hz", "m_refreshRate   = 50; // Hz")
probe("tolerance 1->2", "refresh_tolerance", "RULE->m_refreshRate, 1))", "RULE->m_refreshRate, 2))")
probe("scale 120->240", "scale_step", "std::round(m_scale * 120.0)", "std::round(m_scale * 240.0)")
probe("loop 90->75", "scale_search", "for (size_t i = 1; i < 90; ++i)", "for (size_t i = 1; i < 75; ++i)")
probe("decimals 5->3", "json_decimals", '"refreshRate": {:.5f},', '"refreshRate": {:.3f},')
probe("drop one key", "line_keys", '} else if (ARGS[argno] == "icc") {', '} else if (false) {')
