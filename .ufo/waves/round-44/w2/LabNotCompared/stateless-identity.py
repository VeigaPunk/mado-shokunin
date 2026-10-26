#!/usr/bin/env python3
"""w2/LabNotCompared - does the v2 model reduce to the round-42 model on state-free dumps?

The v2 contract adds state verdicts only; for dumps with no matched maximized/fullscreen client
its stdout must be byte-identical to the round-42 model's (the "round-43 output unchanged" arm of
clause r). This loads c1-r42-geometry.py twice: once standalone (its own model_out) and once via
the v2 counter (which rebinds the counter's copy), and diffs the two on fresh random state-free
dumps from the round-42 generator.

usage: stateless-identity.py --repo <lane> [--n 3000] [--seed S]
"""
import argparse
import importlib.util
import json
import os
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--n", type=int, default=3000)
    ap.add_argument("--seed", default="LabNotCompared-r44-w2")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)
    r42 = load(os.path.join(repo, "quality", "counters", "c1-r42-geometry.py"), "r42_standalone")
    v2 = load(os.path.join(repo, "quality", "counters", "c1-r44-geometry-states-v2.py"),
              "c1r44_pair")
    differ = 0
    stated = 0
    for i in range(args.n):
        rng = r42.rng_for("stateless", args.seed, "gen", i)
        texts, wants = r42.gen_texts(rng)
        raw = json.dumps(r42.gen_clients(rng, wants)).encode()
        a = r42.model_out(raw, texts)
        b = v2.model_out_states(raw, texts)
        if b[0] and " fullscreen=" in b[0]:
            stated += 1
        same = a == b
        differ += not same
        if not same:
            print("DIFF case=%d\n  r42=%r\n  v2 =%r" % (i, a, b))
    print("STATELESS_IDENTITY cases=%d mismatches=%d cases_with_state_segment=%d"
          % (args.n, differ, stated))
    return 0 if differ == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
