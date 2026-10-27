#!/usr/bin/env python3
"""How much of clause g could a memorised table buy?

Replays the frozen counter's own gen_case() for a list of nonces (same call order, same RNG),
compiles each case's keymap with the counter's Judge, and checks whether (keymap sha256, ARG) is in
the memorisation table built by build_table.py. A hit is a case the table answers byte-exactly, so
the hit count is the table's whole contribution on clause g.

Usage: measure_hits.py <counter.py> <work-dir> <table.json> <nonce> [nonce ...]
"""
import hashlib
import importlib.util
import json
import os
import random
import sys


def load_counter(path):
    spec = importlib.util.spec_from_file_location("frozen_c1", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    counter, work, table_path = argv[1], argv[2], argv[3]
    nonces = [int(n) for n in argv[4:]]
    os.makedirs(work, exist_ok=True)
    fm = load_counter(counter)
    judge = fm.Judge(work)
    rows = json.loads(open(table_path, "rb").read())
    table = {(sha, arg) for sha, arg, _rc, _out in rows}
    table_maps = {sha for sha, _arg, _rc, _out in rows}
    print("table entries=%d keymaps=%d" % (len(table), len(table_maps)))
    for nonce in nonces:
        grng = random.Random(nonce)
        hits = 0
        km_hits = 0
        args = []
        for k in range(fm.GEN):
            case = fm.gen_case(grng, k)
            path = judge.keymap(case["rmlvo"])
            sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
            in_km = sha in table_maps
            km_hits += in_km
            hit = (sha, case["arg"]) in table
            hits += hit
            if hit:
                args.append("%s:%r" % (case["id"], case["arg"]))
        print("nonce=%d hits=%d/%d keymap_same_as_fixture=%d/%d args=%s" % (
            nonce, hits, fm.GEN, km_hits, fm.GEN, ",".join(args) or "-"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
