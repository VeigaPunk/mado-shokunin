#!/usr/bin/env python3
"""Shrink every unmasked divergence of a generated corpus to a minimal repro (drop lines while the
divergence persists) and group the minimal repros. Usage: python3 minimize.py [--profile modelled]
"""
import argparse
import collections
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import diff  # noqa: E402


def diverges(cfg):
    r = diff.compare(cfg)
    return r if r["div"] and not r["masked"] else None


def shrink(cfg):
    lines = cfg.splitlines(keepends=True)
    changed = True
    while changed and len(lines) > 1:
        changed = False
        for i in range(len(lines)):
            cand = "".join(lines[:i] + lines[i + 1:])
            if cand and diverges(cand):
                lines = cand.splitlines(keepends=True)
                changed = True
                break
    return "".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", choices=("modelled", "stress", "clean"), default="modelled")
    ap.add_argument("--configs", type=int, default=3600)
    ap.add_argument("--seed", type=int, default=45)
    ap.add_argument("--out", default=os.path.join(HERE, "receipts"))
    args = ap.parse_args()
    rng = random.Random(args.seed)
    cfgs = diff.gen_configs(args.configs, rng, args.profile in ("modelled", "clean"),
                            args.profile == "clean")
    seen = collections.Counter()
    fields = collections.defaultdict(collections.Counter)
    for cfg in cfgs:
        if not diverges(cfg):
            continue
        m = shrink(cfg)
        seen[m] += 1
        r = diverges(m)
        key = ",".join(d[0] for d in r["div"])
        fields[key][m] += 1

    out = ["# minimal repros of unmasked divergences (profile=%s configs=%d seed=%d)"
           % (args.profile, len(cfgs), args.seed), ""]
    out.append("distinct minimal repros=%d  shrinking configs=%d" % (len(seen), sum(seen.values())))
    out.append("")
    for key, group in sorted(fields.items(), key=lambda kv: -sum(kv[1].values())):
        out.append("-- fields %s: %d configs, %d minimal forms" % (key, sum(group.values()), len(group)))
        for cfg, n in group.most_common(6):
            r = diverges(cfg)
            out.append("   x%-3d %s" % (n, json.dumps(cfg)))
            for d in r["div"]:
                out.append("        %s: %s" % (d[0], d[1]))
        out.append("")
    text = "\n".join(out) + "\n"
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "minimal.txt"), "w", encoding="utf-8") as fh:
        fh.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
