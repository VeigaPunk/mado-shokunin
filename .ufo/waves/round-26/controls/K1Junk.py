#!/usr/bin/env python3
"""JUNK control: random animation-shaped data, without reading --home."""
import argparse
import json
import os
import random
import string


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", required=True)
    parser.parse_args()
    rng = random.Random(int.from_bytes(os.urandom(32), "big"))

    def name():
        return "".join(rng.choice(string.ascii_letters) for _ in range(rng.randint(1, 24)))

    beziers = [
        {
            "name": name(),
            "X0": rng.random(),
            "Y0": rng.uniform(-1.0, 2.0),
            "X1": rng.random(),
            "Y1": rng.uniform(-1.0, 2.0),
        }
        for _ in range(rng.randint(0, 24))
    ]
    nodes = [
        {
            "name": name(),
            "overridden": bool(rng.getrandbits(1)),
            "bezier": rng.choice(beziers)["name"] if beziers else name(),
            "enabled": bool(rng.getrandbits(1)),
            "speed": rng.uniform(0.1, 20.0),
            "style": name(),
        }
        for _ in range(rng.randint(0, 64))
    ]
    print(json.dumps([nodes, beziers], allow_nan=False))


if __name__ == "__main__":
    main()
