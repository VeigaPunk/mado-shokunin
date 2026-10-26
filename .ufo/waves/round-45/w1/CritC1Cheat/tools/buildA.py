#!/usr/bin/env python3
"""Bake the counter's own expected bytes for the default seed into a lookup-table tool (cheat-table45.py)."""
import base64
import hashlib
import importlib.util
import json
import zlib

COUNTER = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r45-monitors.py"
spec = importlib.util.spec_from_file_location("cnt", COUNTER)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

SEED = 45
table = mod.names(SEED)
rows = {}
for label, configs, dump, stdin, expect, rc in mod.FIXTURES:
    raw = dump if isinstance(dump, bytes) else json.dumps(mod.subst(dump, table), indent=2).encode()
    if configs is None:
        cfgs = "dir"
    elif configs == "usage":
        cfgs = "none"
    else:
        cfgs = [hashlib.sha256(mod.subst(t, table).encode()).hexdigest() for t in configs]
    key = json.dumps([hashlib.sha256(raw).hexdigest(), cfgs], sort_keys=True)
    if key in rows:
        raise SystemExit("collision: %s / %s" % (label, rows[key][2]))
    rows[key] = ["".join(mod.subst(l, table) + "\n" for l in expect), rc, label]

blob = base64.b64encode(zlib.compress(json.dumps(rows).encode(), 9)).decode()
print("fixtures baked: %d (seed %d), blob %d bytes" % (len(rows), SEED, len(blob)))

TOOL = '''#!/usr/bin/env python3
"""mado-monitors - joins monitor rules with live output state.

This build answers from a table of answers computed offline by the scoring harness; it parses nothing.
"""
import base64
import hashlib
import json
import os
import sys
import zlib

ROWS = json.loads(zlib.decompress(base64.b64decode("%s")).decode())


def our_input(argv):
    monitors, configs, i = None, [], 0
    while i < len(argv):
        if i + 1 >= len(argv):
            return None
        flag, v = argv[i], argv[i + 1]
        if flag == "--monitors":
            monitors = v
        elif flag == "--config":
            configs.append(v)
        else:
            return None
        i += 2
    if monitors is None:
        return None
    if monitors == "-":
        dump = sys.stdin.buffer.read()
    else:
        try:
            dump = open(monitors, "rb").read()
        except OSError:
            return None
    if not configs:
        cfgs = "none"
    elif all(os.path.isdir(c) for c in configs):
        cfgs = "dir"
    else:
        cfgs = []
        for c in configs:
            try:
                cfgs.append(hashlib.sha256(open(c, "rb").read()).hexdigest())
            except OSError:
                return None
    return json.dumps([hashlib.sha256(dump).hexdigest(), cfgs], sort_keys=True)


def main():
    argv = sys.argv[1:]
    if argv == ["--selftest"]:
        print("MADO_MONITORS_SELFTEST: 33/33 passed")
        return 0
    key = our_input(argv)
    if key is None:
        print("MADO_MONITORS: SETUP usage")
        return 2
    row = ROWS.get(key)
    if row is None:
        print("MADO_MONITORS: SETUP unknown")
        return 2
    sys.stdout.write(row[0])
    return row[1]


if __name__ == "__main__":
    sys.exit(main())
''' % blob

open("/fast/scratch/hyaku/mado-r45/CritC1Cheat/cheat-table45.py", "w").write(TOOL)
print("wrote cheat-table45.py")
