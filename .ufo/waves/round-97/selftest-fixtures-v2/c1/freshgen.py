#!/usr/bin/env python3
"""freshgen - mini fresh-case generator fixture (round-97 C2 selftest).

Deterministic: emits two none-mode cases (three inputs) and labels every input by
running the --oracle binary it is handed (Shared contract 3 semantics).  Stdlib
only, ASCII output, no network, no mime.cache fixtures (none/text mode only).
"""
import argparse
import json
import os
import subprocess

TEXT = b"mado fresh fixture: plain text payload\n"
BLOB = bytes(range(1, 32)) + b"\x00\xffbin"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", default="0")
    ap.add_argument("--out", required=True)
    ap.add_argument("--oracle", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    os.makedirs(os.path.join(a.scratch, "h"), exist_ok=True)
    cases = [
        {"id": "fresh-01-mini", "class": "mini",
         "env": {"HOME": "{root}/h", "XDG_DATA_HOME": None, "XDG_DATA_DIRS": "{root}/d1"},
         "files": {"d1/": "", "h/": ""},
         "inputs": [{"name_b64": "bm90ZXMuYXBw", "data_b64": base64x(TEXT)},
                    {"name_b64": None, "data_b64": base64x(BLOB)}], "labels": []},
        {"id": "fresh-02-mini", "class": "mini",
         "env": {"HOME": "{root}/h", "XDG_DATA_HOME": None, "XDG_DATA_DIRS": "{root}/d1"},
         "files": {"d1/": "", "h/": ""},
         "inputs": [{"name_b64": None, "data_b64": base64x(TEXT)}], "labels": []},
    ]
    for c in cases:
        pairs = []
        for i, x in enumerate(c["inputs"]):
            sp = os.path.join(a.scratch, "in%d.bin" % i)
            with open(sp, "wb") as fh:
                fh.write(__import__("base64").b64decode(x["data_b64"]))
            nb = x.get("name_b64")
            nm = None if nb is None else __import__("base64").b64decode(nb).decode()
            pairs.append((nm, sp))
        argv = [a.oracle]
        for nm, sp in pairs:
            argv.append("0" if nm is None else "=" + nm)
            argv.append(sp)
        env = {"LC_ALL": "C", "HOME": os.path.join(a.scratch, "h"),
               "XDG_DATA_DIRS": os.path.join(a.scratch, "d1")}
        r = subprocess.run(argv, capture_output=True, env=env, timeout=60)
        if r.returncode != 0:
            raise SystemExit("oracle failed: " + r.stderr.decode(errors="replace"))
        labs = []
        for ln in r.stdout.splitlines():
            t, u = ln.split(b"\t")
            labs.append([t.decode("utf-8", "surrogateescape"), int(u)])
        if len(labs) != len(pairs):
            raise SystemExit("oracle arity mismatch")
        c["labels"] = labs
    with open(a.out, "w", encoding="ascii") as fh:
        json.dump({"cases": cases}, fh, sort_keys=True)
    print("magictext-fresh-r96: cases=2 inputs=3 deterministic")
    return 0


def base64x(b):
    import base64
    return base64.b64encode(b).decode("ascii")


if __name__ == "__main__":
    raise SystemExit(main())
