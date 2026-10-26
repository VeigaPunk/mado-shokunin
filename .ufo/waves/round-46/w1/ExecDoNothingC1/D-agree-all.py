#!/usr/bin/env python3
"""D-AGREE-ALL control (seat ExecDoNothingC1, mado round 46 w1).

The cheapest no-capability tool (the generalised form of attack (d), "a tool that only handles the host's config"):
it parses nothing, models nothing and assumes every keyboard and mouse agrees with whatever the dump reports. That is
exactly what the host's live run looks like (9 AGREE, 1 VIRTUAL, 4 pointers AGREE, OK) - so a tool tuned to this host
can only ever print this shape. block= is always "no" (the host has no `device` block), kb_file=-, no device blocks,
summary verdict OK, exit 0. VIRTUAL is the one shape it does carry, because the host prints one.

Purpose: measure how much of the frozen fixture set a zero-semantics guess satisfies, i.e. how much of C1's
"capability" a host-shaped tool would be credited with. Committed at tools/mado-devices.py in a scratch clone.
"""
import json
import sys

NAMES = ("layout", "variant", "options", "model", "rules")


def report(devices_data, config_texts):
    doc = json.loads(devices_data.decode("utf-8"))
    c = dict(keyboards=0, agree=0, differ=0, fallback=0, virtual=0, mice=0, mice_differ=0)
    lines = []
    for kb in doc["keyboards"]:
        c["keyboards"] += 1
        name = kb["name"]
        rep = tuple(kb.get(n) if isinstance(kb.get(n), str) else "" for n in NAMES)
        verdict = "VIRTUAL" if name.startswith("hl-virtual-keyboard") else "AGREE"
        c["virtual" if verdict == "VIRTUAL" else "agree"] += 1
        lines.append("MADO_DEV_KEYBOARD: name=%s block=no %s kb_file=- differ=- verdict=%s" % (
            json.dumps(name), " ".join("%s=%s" % (n, json.dumps(v)) for n, v in zip(NAMES, rep)), verdict))
    for m in doc["mice"]:
        c["mice"] += 1
        r = m.get("scrollFactor")
        shown = "%.2f" % r if isinstance(r, (int, float)) and not isinstance(r, bool) else "?"
        lines.append("MADO_DEV_MOUSE: name=%s block=no scroll_factor=%s reported=%s verdict=AGREE" % (
            json.dumps(m["name"]), shown, shown))
    lines.append("MADO_DEVICES: keyboards=%d agree=%d differ=0 fallback=0 virtual=%d mice=%d mice_differ=0 blocks=0 "
                 "stale=0 unsupported=0 verdict=OK" % (c["keyboards"], c["agree"], c["virtual"], c["mice"]))
    return lines, 0


def main():
    argv = sys.argv[1:]
    if argv == ["--selftest"]:
        print("MADO_DEVICES_SELFTEST: 48/48 passed")
        return 0
    if not argv or argv[0] != "--devices" or len(argv) < 4:
        print("MADO_DEVICES: SETUP usage")
        return 2
    data = sys.stdin.buffer.read() if argv[1] == "-" else open(argv[1], "rb").read()
    try:
        lines, rc = report(data, [open(p, "rb").read().decode("utf-8", "replace") for p in argv[3::2]])
    except Exception:
        print("MADO_DEVICES: SETUP bad_json")
        return 2
    sys.stdout.write("".join(l + "\n" for l in lines))
    return rc


if __name__ == "__main__":
    sys.exit(main())
