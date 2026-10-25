#!/usr/bin/env python3
"""ExecOracleHlInt / round-40 w1 -- the frozen counter's Python model on the same corpus.

Imports `hl_int` straight out of the frozen counter (no copy, no edit) and
applies it exactly the way `model_equal(..., form="int")` does:

    d = declared.strip()
    return hl_int(d) == live

so `None` here means "the model says this spelling is a parse error".
"""
import hashlib
import importlib.util
import json
import sys

COUNTER = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r40-live.py"


def load_counter(path):
    spec = importlib.util.spec_from_file_location("c1_r40_live", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def read_corpus(path):
    rows = []
    with open(path, "rb") as fh:
        for raw in fh:
            line = raw.decode("utf-8")
            if line.endswith("\n"):
                line = line[:-1]
            if not line:
                continue
            parts = line.split("\t", 3)
            if len(parts) != 4:
                raise SystemExit("bad corpus line: %r" % line)
            rows.append(parts)
    return rows


def main():
    corpus, outpath = sys.argv[1], sys.argv[2]
    mod = load_counter(COUNTER)
    hl_int = mod.hl_int

    with open(COUNTER, "rb") as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()

    with open(outpath, "w") as out:
        for ident, cat, scope, spelling in read_corpus(corpus):
            d = spelling.strip()
            try:
                val = hl_int(d)
            except Exception as exc:  # the model should never raise; record it if it does
                out.write(json.dumps({"id": ident, "cat": cat, "scope": scope,
                                      "decl": spelling, "model": None,
                                      "model_raised": repr(exc)}) + "\n")
                continue
            out.write(json.dumps({"id": ident, "cat": cat, "scope": scope,
                                  "decl": spelling, "model": val,
                                  "model_raised": None}) + "\n")

    print("MODEL_SOURCE: %s sha256=%s" % (COUNTER, sha))


if __name__ == "__main__":
    main()
