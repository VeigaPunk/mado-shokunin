#!/usr/bin/env python3
"""Project committed `hyprctl clients -j` dumps to the 7-key receipt shape.

Driver for the ExecPrivacyGate scratch clone (round 45 w1); not part of the
gate. Each input file must be a JSON array of client objects (or an object
with a `clients` array); the output keeps, per client, only

    address, at, class, floating, mapped, monitor, size

which is the projection the round-43 tree already uses at
`.ufo/waves/round-43/fetch/host-clients-r43.json` (round-44 closure D1).
No title, initialTitle, pid, tags or workspace name survives.

Usage: project-d1.py <file> [<file> ...]
"""

import json
import sys

KEYS = ("address", "at", "class", "floating", "mapped", "monitor", "size")


def project(clients):
    if not isinstance(clients, list):
        raise SystemExit("expected a JSON array of client objects")
    out = []
    for client in clients:
        if not isinstance(client, dict):
            raise SystemExit("expected client objects, got %r" % type(client).__name__)
        out.append({key: client[key] for key in KEYS if key in client})
    return out


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    for path in argv[1:]:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, dict) and "clients" in data:
            data = data["clients"]
        projected = project(data)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(projected, handle, indent=1)
            handle.write("\n")
        print("%s clients=%d keys=%s" % (path, len(projected), ",".join(KEYS)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
