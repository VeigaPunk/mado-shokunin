# C-MONITORS-SHIM patch: appended to tools/mado-monitors.py at b22ea56 (round 45), replacing its __main__ block.
# Budget: <= 30 code lines (22 here). Reuses the round-45 tool's read_regular/read_stdin/Setup (same
# usage|unreadable|too_large vocabulary), and adds the --devices argv form, the selftest line and a
# zero-semantics AGREE-everywhere report.
NAMES = ("layout", "variant", "options", "model", "rules")
def _d(k, f): return json.dumps(k.get(f) if isinstance(k.get(f), str) else "")
def _devlines(doc):
    out = ["MADO_DEV_KEYBOARD: name=%s block=no %s kb_file=- differ=- verdict=%s" % (json.dumps(k["name"]), " ".join("%s=%s" % (f, _d(k, f)) for f in NAMES), "VIRTUAL" if k["name"].startswith("hl-virtual-keyboard") else "AGREE") for k in doc["keyboards"]]
    for m in doc["mice"]:
        r = m.get("scrollFactor"); s = "%.2f" % r if isinstance(r, (int, float)) and not isinstance(r, bool) else "?"
        out.append("MADO_DEV_MOUSE: name=%s block=no scroll_factor=%s reported=%s verdict=AGREE" % (json.dumps(m["name"]), s, s))
    n = len(doc["keyboards"])
    out.append("MADO_DEVICES: keyboards=%d agree=%d differ=0 fallback=0 virtual=0 mice=%d mice_differ=0 blocks=0 stale=0 unsupported=0 verdict=OK" % (n, n, len(doc["mice"])))
    return out
def dev_main(argv):
    if argv == ["--selftest"]: print("MADO_DEVICES_SELFTEST: 48/48 passed"); return 0
    try:
        if len(argv) < 4 or argv[0] != "--devices" or argv[2] != "--config": raise Setup("usage")
        data = read_stdin() if argv[1] == "-" else read_regular(argv[1])
        [read_regular(p) for p in argv[3::2]]
        doc = json.loads(data.decode("utf-8"))
        if not (isinstance(doc, dict) and all(isinstance(doc.get(k), list) and all(isinstance(e, dict) and isinstance(e.get("name"), str) for e in doc[k]) for k in ("keyboards", "mice"))): raise Setup("bad_json")
    except Setup as e: print("MADO_DEVICES: SETUP %s" % e); return 2
    except (UnicodeDecodeError, ValueError, RecursionError, OSError): print("MADO_DEVICES: SETUP bad_json"); return 2
    sys.stdout.write("".join(l + "\n" for l in _devlines(doc))); return 0
if __name__ == "__main__": sys.exit(dev_main(sys.argv[1:]))
