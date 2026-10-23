#!/usr/bin/env python3
"""JUNK control: random workspace-rule-shaped JSON, without config access."""

import argparse
import json
import random


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", required=True)
    parser.parse_args()  # Accept the interface; deliberately never inspect HOME.
    rng = random.SystemRandom()
    words = ("web", "chat", "code", "music", "notes", "term")
    monitors = ("", "HEADLESS-1", "DP-1", "HDMI-A-1")
    commands = ("", "kitty", "firefox", "foot", "thunar")
    rules = []
    for _ in range(rng.randrange(5)):
        selector = rng.choice((
            str(rng.randint(1, 20)),
            "name:" + rng.choice(words),
            "special:" + rng.choice(words),
        ))
        rules.append({
            "workspaceString": selector,
            "monitor": rng.choice(monitors),
            "default": bool(rng.getrandbits(1)),
            "persistent": bool(rng.getrandbits(1)),
            "gapsIn": [rng.randint(0, 30) for _ in range(4)],
            "gapsOut": [rng.randint(0, 30) for _ in range(4)],
            "borderSize": rng.randint(0, 8),
            "border": bool(rng.getrandbits(1)),
            "shadow": bool(rng.getrandbits(1)),
            "rounding": bool(rng.getrandbits(1)),
            "decorate": bool(rng.getrandbits(1)),
            "onCreatedEmpty": rng.choice(commands),
        })
    print(json.dumps(rules, separators=(",", ":")))


if __name__ == "__main__":
    main()
