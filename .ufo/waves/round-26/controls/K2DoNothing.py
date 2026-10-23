#!/usr/bin/env python3
"""C2 do-nothing control: emits an empty bind table, never reads the config tree."""
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("--home", required=True)
ap.parse_args()
print(json.dumps([]))
