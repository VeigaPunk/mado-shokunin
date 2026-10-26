#!/usr/bin/env python3
"""Locate every quote this seat cites; the line numbers in findings.md are computed here, never typed."""
import sys

LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
COUNTER = LANE + "/quality/counters/c1-r45-monitors.py"
REF = LANE + "/.ufo/waves/round-45/l1-draft/mado-monitors.py"
PIN = LANE + "/.ufo/waves/round-45/fetch/"

QUOTES = [
    (COUNTER, 'HYPRLAND_INSTANCE_SIGNATURE=mado-r45-fixture'),
    (COUNTER, '"HYPRLAND_INSTANCE_SIGNATURE": "mado-r45-fixture"'),
    (COUNTER, '"PATH": fakebin + ":/usr/bin:/bin"'),
    (COUNTER, '"HOME": sd}'),
    (COUNTER, 'the default seed is 45, so a run without --seed reproduces exactly'),
    (COUNTER, 'the 1/120 scale correction with its 89-step search; adding a rule'),
    (COUNTER, 'monitorv2 and unmodelled lines make the verdict NOT_COMPARED'),
    (COUNTER, '("scale-1.3-corrected"'),
    (COUNTER, '("scale-1.6"'),
    (COUNTER, '("ignored-keys"'),
    (COUNTER, '("sdr-eotf-drops-rule"'),
    (COUNTER, '("addreserved-adds-default"'),
    (COUNTER, '("mirror-agree"'),
    (COUNTER, '("mirror-missing"'),
    (COUNTER, '("desc-added-later-wins"'),
    (COUNTER, '("desc-not-prefix"'),
    (COUNTER, '("monitorv2"'),
    (COUNTER, '("stdin"'),
    (COUNTER, 'if not os.path.isdir(a.work):'),
    (REF, 'KEYS = ("mirror", "bitdepth", "cm", "sdrsaturation", "sdrbrightness", "transform", "vrr", "icc")'),
    (REF, 'if not all(RES_RE.fullmatch(fld(i)) for i in range(2, 6)):'),
    (REF, 'def expected_scale(s, w, h):'),
    (REF, 'k = math.floor(s * 120.0 + 0.5)'),
    (REF, 'if desc.startswith(sel[5:].strip(" \\t")):'),
    (REF, 'and abs(rr - rule["rate"]) < 1.0):'),
    (REF, 'ids = [m.get("id") for m in mons if str_or_empty(m.get("name")) == rule["mirror"] and is_int(m.get("id"))]'),
    (REF, 'elif counts["v2"] > 0 or counts["unsupported"] > 0:'),
    (REF, 'def main():'),
    (REF, 'print("MADO_MONITORS_SELFTEST: %d/%d passed" % (passed, total))'),
    (PIN + "Hyprland-HyprCtl.cpp", 'escapeJSONStrings(m->m_shortDescription)'),
    (PIN + "Hyprland-Monitor.cpp",
     'return m_description.starts_with(DESCRIPTIONSELECTOR) || m_shortDescription.starts_with(DESCRIPTIONSELECTOR);'),
    (PIN + "Hyprland-MonitorRuleManager.cpp", 'add'),
]


def main():
    bad = 0
    for path, q in QUOTES:
        try:
            lines = open(path, "r", errors="replace").read().split("\n")
        except OSError as e:
            print("MISSING %s: %s" % (path, e))
            bad += 1
            continue
        hits = [n for n, l in enumerate(lines, 1) if q in l]
        rel = path.replace(LANE + "/", "")
        words = len(q.split())
        if not hits:
            print("FAIL %-58s words=%d not found: %r" % (rel, words, q[:60]))
            bad += 1
            continue
        print("OK   %-58s line=%s words=%d" % (rel, ",".join(str(h) for h in hits), words))
    print("QUOTES: verified=%d failed=%d" % (len(QUOTES) - bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
