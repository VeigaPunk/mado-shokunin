#!/usr/bin/env python3
"""Build the narrow cheat variants from the reference text; each substitution must occur exactly once."""
import sys

REF = open("/fast/scratch/hyaku/mado-r45/CritC1Cheat/ref.py").read()

SUB = {
    # B: the 1/120 scale correction only for the one (S, w, h) the fixtures exercise
    "cheat-scale-table": [(
        '    k = math.floor(s * 120.0 + 0.5)\n',
        '    if not (abs(s - 1.3) < 0.001 and (w, h) == (3440, 1440)):\n'
        '        return s\n'
        '    k = math.floor(s * 120.0 + 0.5)\n')],
    # C: KEYS loses the three keys no fixture uses
    "cheat-key-set": [(
        'KEYS = ("mirror", "bitdepth", "cm", "sdrsaturation", "sdrbrightness", "transform", "vrr", "icc")',
        'KEYS = ("mirror", "bitdepth", "cm", "transform", "vrr")')],
    # D: DIFFER is decided before NOT_COMPARED
    "cheat-verdict-order": [(
        '    elif counts["v2"] > 0 or counts["unsupported"] > 0:\n'
        '        v, rc = "NOT_COMPARED", 5\n'
        '    elif t["differ"] > 0:\n'
        '        v, rc = "DIFFER", 1\n',
        '    elif t["differ"] > 0:\n'
        '        v, rc = "DIFFER", 1\n'
        '    elif counts["v2"] > 0 or counts["unsupported"] > 0:\n'
        '        v, rc = "NOT_COMPARED", 5\n')],
    # E: mirror agrees when mirrorOf is ANY output id, not the named target's id
    "cheat-mirror-by-id": [(
        '        ids = [m.get("id") for m in mons if str_or_empty(m.get("name")) == rule["mirror"] and is_int(m.get("id"))]\n'
        '        if not (isinstance(mo, str) and len(ids) >= 1 and mo == str(ids[0])):',
        '        ids = [m.get("id") for m in mons if is_int(m.get("id"))]\n'
        '        if not (isinstance(mo, str) and any(mo == str(i) for i in ids)):')],
    # F: addreserved fields are not validated
    "cheat-addreserved-novalidation": [(
        '        if not all(RES_RE.fullmatch(fld(i)) for i in range(2, 6)):\n'
        '            counts["badrules"] += 1\n'
        '            return\n', '')],
    # G: desc: TEXT is not stripped and a bare desc: never matches
    "cheat-desc-text": [(
        '            if desc.startswith(sel[5:].strip(" \\t")):',
        '            if sel[5:] != "" and desc.startswith(sel[5:]):')],
    # H: the < 1.0 refresh bound only for the rates the fixtures use
    "cheat-rate-set": [(
        '                and abs(rr - rule["rate"]) < 1.0):',
        '                and (abs(rr - rule["rate"]) < 1.0 if rule["rate"] in (60.0, 100.0, 120.0, 144.0)\n'
        '                     else abs(rr - rule["rate"]) < 0.05)):')],
    # I: desc: also matches a long-description field the contract says is not in the dump
    "cheat-desc-long": [(
        '            if desc.startswith(sel[5:].strip(" \\t")):',
        '            if desc.startswith(sel[5:].strip(" \\t")) or '
        'str_or_empty(mon.get("longDescription")).startswith(sel[5:].strip(" \\t")):')],
}


def main():
    for name, subs in SUB.items():
        t = REF
        for old, new in subs:
            if t.count(old) != 1:
                raise SystemExit("%s: %d occurrences of %r" % (name, t.count(old), old[:60]))
            t = t.replace(old, new)
        open("/fast/scratch/hyaku/mado-r45/CritC1Cheat/%s.py" % name, "w").write(t)
        print("built %s.py" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
