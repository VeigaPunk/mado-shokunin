#!/usr/bin/env python3
"""Classify every unmasked divergence of a corpus by the pinned mechanism it hits.

A = addreserved numbers accepted by std::stoi (prefix) but rejected by the tool's -?[0-9]{1,6}
M = modeline: Hyprland resolves a validated modeline to an explicit mode, the tool never compares it
T = field-1 'transform' value accepted by isNumber+stoi ('03', '007') but rejected by the tool
W = field trimmed by std::isspace in Hyprland, only ' ' and '\\t' by the tool (CRLF configs)
U = unexplained (must be investigated by hand)

Usage: python3 classes.py [--profile modelled|stress]
"""
import argparse
import collections
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import diff  # noqa: E402
import model as M  # noqa: E402
from minimize import shrink, diverges  # noqa: E402

RES_RE = re.compile(r"-?[0-9]{1,6}")
STOI_OK = re.compile(r"[+-]?[0-9]+")


def addreserved_prefix(cfg):
    for lhs, rhs in M.hyprlang_config_lines(cfg):
        if lhs != "monitor" or rhs is None:
            continue
        f = [x.strip(" \t") for x in rhs.split(",")]
        if len(f) > 1 and f[1] == "addreserved":
            for i in range(2, 6):
                v = f[i] if i < len(f) else ""
                if RES_RE.fullmatch(v):
                    continue
                if STOI_OK.match(v):
                    return True
    return False


def modeline(cfg):
    for lhs, rhs in M.hyprlang_config_lines(cfg):
        if lhs != "monitor" or rhs is None:
            continue
        f = [x.strip(" \t") for x in rhs.split(",")]
        if len(f) > 1 and f[1].split() and f[1].split()[0].lower() == "modeline":
            return True
    return False


def classify(cfg):
    if addreserved_prefix(cfg):
        return "A"
    if modeline(cfg):
        return "M"
    if re.search(r"^monitor[ \t]*=[^,\n]*, *transform, *0[0-9]", cfg, re.M):
        return "T"
    if "\r" in cfg:
        return "W"
    return "U"


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
    counts = collections.Counter()
    masked = collections.Counter()
    unknown = []
    for cfg in cfgs:
        r = diff.compare(cfg)
        if not r["div"]:
            continue
        if r["masked"]:
            m = shrink(cfg)
            masked[classify(m)] += 1
            continue
        m = shrink(cfg)
        c = classify(m)
        counts[c] += 1
        if c == "U":
            unknown.append((m, r["div"]))
    total = sum(counts.values())
    lines = ["# divergence classes (profile=%s configs=%d seed=%d)" % (args.profile, len(cfgs), args.seed),
             "unmasked divergences=%d" % total]
    names = {"A": "addreserved std::stoi prefix", "M": "modeline resolution",
             "T": "transform leading-zero value", "W": "field trim is not isspace",
             "U": "unexplained"}
    for k in "AMTWU":
        lines.append("  %s %-34s %4d  (%.1f%% of divergences)" % (k, names[k], counts[k],
                                                                 100.0 * counts[k] / total if total else 0))
    lines.append("masked divergences (tool said NOT_COMPARED)=%d, by class %s"
                 % (sum(masked.values()), dict(sorted(masked.items()))))
    for m, d in unknown[:20]:
        lines.append("U repro=%s %s" % (json.dumps(m), d))
    text = "\n".join(lines) + "\n"
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "classes.txt"), "w", encoding="utf-8") as fh:
        fh.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
