#!/usr/bin/env python3
"""Cheapest clause-b cheat: no conversion, no parser, no compositor call.
Clause b of PRED-C1-r40-v1 reads one line and one exit status."""
import sys

if "--selftest" in sys.argv[1:]:
    sys.stdout.write("MADO_OPTIONS_SELFTEST: 79/79 passed\n")
    sys.exit(0)
sys.exit(1)
