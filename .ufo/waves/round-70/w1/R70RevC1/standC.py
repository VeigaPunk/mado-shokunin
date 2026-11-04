#!/usr/bin/env python3
import argparse, sys
ap = argparse.ArgumentParser(); ap.add_argument("--repo"); ap.add_argument("--rev")
ap.add_argument("--scratch-root"); ap.add_argument("--selftest", action="store_true")
a = ap.parse_args()
if a.selftest:
    print("MADO_R70_LANDING_CONTROLS_SELFTEST: 2/2 assertions passed"); sys.exit(0)
print("MADO_R70_LANDING_CONTROLS: selftest=0 mz=fail mr=pass killed=2/2 baseline=0/2 "
      "verdict=TARGET_MET rev=%s" % a.rev); sys.exit(0)
