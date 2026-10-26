#!/usr/bin/env python3
"""Soundness check for the generated clause: the real script must print the same thing for the same generated case in
two different case roots (after the case root is normalized to $ROOT). If it does not, clause g would punish a correct
tool for the instrument's own nondeterminism.

Usage: check-oracle-determinism.py --counter c1-r47-terminal.py --work DIR [--nonce N] [--cases N]
Prints `DET n/N deterministic` and one line per differing case.
"""
import argparse
import importlib.util
import os
import sys
import tempfile

sys.dont_write_bytecode = True


def load_counter(path):
    spec = importlib.util.spec_from_file_location("c1r47det", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--nonce", type=int, default=47)
    ap.add_argument("--cases", type=int, default=150)
    a = ap.parse_args()
    c = load_counter(a.counter)
    src, blob = c.load_script()
    os.makedirs(a.work, exist_ok=True)
    work = tempfile.mkdtemp(dir=a.work, prefix="det-")
    sdir = os.path.join(work, "script")
    os.makedirs(sdir)
    script = os.path.join(sdir, c.SCRIPT_NAME)
    with open(script, "wb") as f:
        f.write(blob)
    os.chmod(script, 0o755)
    fakebin = c.make_fakebin(os.path.join(work, "bin"), os.path.join(work, "no.sock"))
    ro = [sdir, fakebin]
    import random
    rng = random.Random(a.nonce ^ 0x5DEECE66D)
    same = 0
    for k in range(a.cases):
        case = c.gen_case(rng)
        outs = []
        for seed in (1, 2):
            root = tempfile.mkdtemp(dir=work, prefix="c%s%d-" % (seed, k))
            c.load_case(root, case["files"], case.get("exec") or [])
            env = c.case_env(case.get("env"), root, fakebin, False)
            p = c.run_oracle(script, case["args"], root, env, ro)
            outs.append(None if p is None else (p.returncode, c.norm(c.dec(p.stdout), root)))
        if outs[0] == outs[1]:
            same += 1
        else:
            print("DET case=%d differs %r vs %r" % (k, outs[0], outs[1]))
    print("DET %d/%d deterministic" % (same, a.cases))
    return 0 if same == a.cases else 1


if __name__ == "__main__":
    sys.exit(main())
