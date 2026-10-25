#!/usr/bin/env python3
"""ExecOracleHlInt / round-40 w1 -- the counter's OWN int-form value space.

Drives the frozen counter's Fixture generator (imported, not copied) over many
seeds and collects every distinct `declared` spelling it emits for an INT-form
option (kinds bool / num / colour, plain and quirk). That set -- not a hand
picked sample -- is what the counter's own fixtures can hand to `hl_int`, so it
is the population over which the model has to be exact.
"""
import importlib.util
import random
import sys

COUNTER = "/home/vgpnk/Projects/shokunin/mado-shokunin/quality/counters/c1-r40-live.py"
SEEDS = 500


def load_counter(path):
    spec = importlib.util.spec_from_file_location("c1_r40_live", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    outpath = sys.argv[1]
    mod = load_counter(COUNTER)
    seen = {}
    for i in range(SEEDS):
        rng = random.Random(0xC1 * 1000 + i)
        fx = mod.Fixture(rng, "g%d" % i)
        for kind in ("bool", "num", "colour"):
            for quirk in (False, True):
                _key, opt = fx.make(kind, quirk)
                if opt["form"] != "int":
                    continue
                seen.setdefault(opt["declared"], "%s%s" % (kind, "/q" if quirk else ""))
    rows = []
    for n, (decl, kind) in enumerate(sorted(seen.items())):
        rows.append("s%04d\tgen_%s\tgen\t%s" % (n, kind.replace("/", "_"), decl))
    with open(outpath, "w") as fh:
        fh.write("\n".join(rows) + "\n")
    print("GEN_SPACE: distinct int-form spellings=%d from %d seeds" % (len(rows), SEEDS))


if __name__ == "__main__":
    main()
