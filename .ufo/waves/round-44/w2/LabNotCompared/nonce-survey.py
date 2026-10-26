#!/usr/bin/env python3
"""w2/LabNotCompared - does the 26-fixture lattice pin the top-verdict precedence
DIFFER before NOT_COMPARED, independently of the run nonce?

For a given nonce the counter's fixtures are fixed (12 sgen + 14 fixed, fsmany0 also
nonce-derived). A wrong tool that tests NOT_COMPARED before DIFFER differs from the model
only on dumps with differ>0, agree==0 and maximized+fullscreen>0. This script imports the
counter (main() never runs), captures every fixture's (clients, rules) by monkeypatching
old.case_files, and reports for each nonce whether at least one fixture is precedence
sensitive. usage: nonce-survey.py --repo <lane> --rev <full-hash> --nonces <n>
"""
import argparse
import importlib.util
import os
import re
import sys

SENS = re.compile(r"agree=(\d+) differ=(\d+) tiled=\d+ badsize=\d+"
                  r"(?: maximized=(\d+) fullscreen=(\d+))? verdict=")


def load(repo):
    path = os.path.join(repo, "quality", "counters", "c1-r44-geometry-states-v2.py")
    spec = importlib.util.spec_from_file_location("c1r44_survey", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fixtures_for(mod, rev, nonce):
    """-> list of (name, raw_bytes, texts) for every comparison the 26 fixtures make."""
    out = []

    def cap(tool, tmp, name, clients, texts, via_stdin=False, extra=None):
        raw = clients if isinstance(clients, bytes) else clients.encode("utf-8", "surrogateescape")
        out.append((name, raw, [t if isinstance(t, str) else t.decode("utf-8", "replace")
                                for t in texts]))
        return 1, "ok"

    mod.old.NONCE[0] = nonce
    mod.old.case_files = cap
    for i in range(mod.N_GEN):
        mod.score_sgen(None, None, rev, nonce, i)
    for _name, fn in mod.FIXED:
        fn(None, None, rev, nonce)
    return out


def sensitive(mod, fixtures):
    hits = []
    for name, raw, texts in fixtures:
        out, _rc = mod.model_out_states(raw, texts)
        last = out.rstrip().splitlines()[-1]
        g = SENS.search(last)
        agree, differ = int(g.group(1)), int(g.group(2))
        states = int(g.group(3) or 0) + int(g.group(4) or 0)
        if differ > 0 and agree == 0 and states > 0:
            hits.append(name)
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--nonces", type=int, default=1000)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--first-blind", action="store_true",
                    help="stop at the first nonce with no precedence-sensitive fixture")
    args = ap.parse_args()
    mod = load(os.path.abspath(args.repo))
    import hashlib
    blind = []
    n = 0
    for k in range(args.start, args.start + args.nonces):
        nonce = hashlib.sha256(("probe:%d" % k).encode()).hexdigest()[:16]
        fx = fixtures_for(mod, args.rev, nonce)
        hits = sensitive(mod, fx)
        n += 1
        if not hits:
            blind.append((k, nonce, len(fx)))
            print("BLIND k=%d nonce=%s fixtures=%d" % (k, nonce, len(fx)))
            if args.first_blind:
                break
    print("SURVEY nonces=%d blind=%d rate=%.4f" % (n, len(blind), len(blind) / n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
