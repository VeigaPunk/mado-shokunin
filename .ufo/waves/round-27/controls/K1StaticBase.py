#!/usr/bin/env python3
"""STATIC-BASE control: replay the live unperturbed workspace-rule table."""
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--home", required=True)
    parser.parse_args()
    # Captured once: env -i PATH=/usr/bin timeout 20 prlimit
    # --as=4000000000 --core=0 -- hyprctl -i 0 workspacerules -j
    print("[]")


if __name__ == "__main__":
    main()
