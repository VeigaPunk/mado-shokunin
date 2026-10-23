#!/usr/bin/env python3
"""ALL-FALSE control: accept --home without inspecting the config tree."""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--home", required=True)
parser.parse_args()
print("[]")
