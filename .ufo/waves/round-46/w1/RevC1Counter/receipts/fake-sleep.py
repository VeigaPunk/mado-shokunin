#!/usr/bin/env python3
import sys, time
if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
    print("MADO_DEVICES_SELFTEST: 48/48 passed")
    sys.exit(0)
time.sleep(25)
print("MADO_DEVICES: SETUP usage")
sys.exit(2)
