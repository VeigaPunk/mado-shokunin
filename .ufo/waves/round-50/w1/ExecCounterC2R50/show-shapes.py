#!/usr/bin/env python3
"""show-shapes.py — print one generated instance of every fixture shape.

Imports the counter draft's ``red_shape``/``green_shape`` builders so a reviewer
sees exactly what each nonce-generated fixture repository holds. Every value is
synthetic (``someoneNNN`` home users, ``fixtureNNNN`` accounts, word paths), so
the output never carries the real account or a host path.

Usage:
  python3 -I show-shapes.py [--seed N]
"""

import argparse
import importlib.util
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.dont_write_bytecode = True  # never litter the seat dir with a __pycache__


def main(argv=None):
    parser = argparse.ArgumentParser(prog="show-shapes.py")
    parser.add_argument("--seed", type=int, default=50117)
    args = parser.parse_args(argv)
    spec = importlib.util.spec_from_file_location(
        "counters", os.path.join(HERE, "c2-r50-session-gate.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rng = random.Random(args.seed)
    print("SHAPES: seed=%d red_families=%d green_families=%d"
          % (args.seed, len(module.RED_FAMILIES), len(module.GREEN_FAMILIES)))

    def masked(text, account=None):
        # The receipt shows the structural form with the synthetic identities
        # masked: a lane receipt never carries a /home/<user> prefix verbatim.
        text = re.sub(r"/home/[A-Za-z0-9._-]+", "/home/U", text)
        if account:
            text = text.replace(account, "fixtureN")
        return text

    for family in module.RED_FAMILIES:
        shape = module.red_shape(family, rng)
        account = shape["account"]
        print("RED family=%s rule=%s path=%s account=%s content=%r"
              % (family, shape["rule"], shape["rel"],
                 "own" if account else "neutral", masked(shape["content"], account)))
    for family in module.GREEN_FAMILIES:
        shape = module.green_shape(family, rng)
        print("GREEN family=%s path=%s content=%r"
              % (family, shape["rel"], masked(shape["content"])))
    print("SHAPES: clause_d path=docs/receipt.txt shape=r7-prefix")
    return 0


if __name__ == "__main__":
    sys.exit(main())
