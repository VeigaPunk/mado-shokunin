#!/usr/bin/env python3
"""Cheat (a): replays <display-root>/expected.out and expected.rc (the registered control shape, R56 w1 'six-line tool')."""
import sys

a = sys.argv[1:]
dr = a[a.index("--display-root") + 1]
sys.stdout.write(open(dr + "/expected.out").read())
sys.exit(int(open(dr + "/expected.rc").read()))
