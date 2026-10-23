#!/usr/bin/env python3
"""Echo root-file workspace selectors without interpreting workspace rules."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", required=True)
    args = parser.parse_args()
    rules = []
    root = Path(args.home) / ".config/hypr/hyprland.conf"
    with root.open(encoding="utf-8", errors="replace") as config:
        for line in config:
            key, separator, value = line.partition("=")
            if separator and key.strip() == "workspace":
                rules.append({"workspaceString": value.split(",", 1)[0].strip(), "enabled": True})
    print(json.dumps(rules))


if __name__ == "__main__":
    main()
