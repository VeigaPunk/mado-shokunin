#!/usr/bin/env python3
"""Build the memorization table for the clause-g overfit probe (seat ExecC1Overfit, mado round 50).

Reads the FROZEN round-49 C1 counter from a scratch clone (read-only import), derives the pinned
judge's stdout + exit status for every frozen fixture through the counter's own Judge class, checks
each against the fixture's recorded (rc, sha256) -- a drift stops the build -- and writes

  table.json : [[keymap_sha256, arg, rc, base64(stdout)], ...]
  table.b85  : base85(zlib(json))  -- the blob the probe tools embed

Usage: build_table.py <counter.py> <work-dir> <out-dir>
"""
import base64
import hashlib
import importlib.util
import json
import os
import sys
import zlib


def load_counter(path):
    spec = importlib.util.spec_from_file_location("frozen_c1", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    counter, work, outdir = argv[1], argv[2], argv[3]
    os.makedirs(work, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    fm = load_counter(counter)
    fixtures = fm.load_fixtures()
    judge = fm.Judge(work)
    rows = []
    drift = []
    keymaps = {}
    total = 0
    for case in fixtures:
        path = judge.keymap(case["rmlvo"])
        blob = open(path, "rb").read()
        sha = hashlib.sha256(blob).hexdigest()
        keymaps[sha] = keymaps.get(sha, 0) + 1
        rc, out = judge.run(path, case["arg"])
        got = hashlib.sha256(out).hexdigest()
        if rc != case["rc"] or got != case["sha256"]:
            drift.append((case["id"], rc, case["rc"], got, case["sha256"]))
            continue
        total += len(out)
        rows.append([sha, case["arg"], rc, base64.b64encode(out).decode("ascii")])
    if drift:
        print("DRIFT %d: %r" % (len(drift), drift[:3]))
        return 1
    payload = json.dumps(rows, separators=(",", ":")).encode("ascii")
    open(os.path.join(outdir, "table.json"), "wb").write(payload)
    blob = base64.b85encode(zlib.compress(payload, 9)).decode("ascii")
    with open(os.path.join(outdir, "table.b85"), "w") as fh:
        for i in range(0, len(blob), 100):
            fh.write(blob[i:i + 100] + "\n")
    print("cases=%d keymaps=%d pairs=%d stdout_bytes=%d json_bytes=%d b85_bytes=%d max_out=%d" % (
        len(rows), len(keymaps), len({(r[0], r[1]) for r in rows}), total, len(payload), len(blob),
        max(len(base64.b64decode(r[3])) for r in rows)))
    depth = {}
    for row in rows:
        out = base64.b64decode(row[3])
        if row[2] != 0:
            kind = "rc%d" % row[2]
        else:
            body = [ln for ln in out.decode("utf-8", "surrogateescape").splitlines()
                    if ln and not ln.startswith(("keysym:", "KEYCODE", "==="))]
            if not body:
                kind = "zero-row"
            else:
                levels = {int(ln.rpartition(" [ ")[0].split()[-1]) for ln in body}
                kind = "level1-only" if max(levels) == 1 else ("level2-max" if max(levels) == 2 else "level3+")
        depth[kind] = depth.get(kind, 0) + 1
    print("fixture classes: " + " ".join("%s=%d" % kv for kv in sorted(depth.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
