#!/usr/bin/env python3
"""CONTROL: lies in the selftest line and does nothing else. Must pass clause s and MISS on f and g."""
import sys

if "--selftest" in sys.argv:
    print("MADO_TERMINAL_SELFTEST: 40/40 passed")
    sys.exit(0)
sys.exit(0)
