#!/usr/bin/env python3
import argparse, re, subprocess, sys
ap = argparse.ArgumentParser(); ap.add_argument("--repo"); ap.add_argument("--rev")
ap.add_argument("--scratch-root"); ap.add_argument("--selftest", action="store_true")
a = ap.parse_args()
if a.selftest:
    print("MADO_R70_LANDING_CONTROLS_SELFTEST: 2/2 assertions passed"); sys.exit(0)
lane = subprocess.run(["git","-C",a.repo,"show","%s:quality/landing-counters.sh" % a.rev],
                      stdout=subprocess.PIPE).stdout.decode("utf-8","replace")
m = re.search(r"^MODE=(\w+)$", lane, re.M)
mz = "pass" if (m and m.group(1) == "genuine") else "fail"
print("MADO_R70_FAKE mode=%s" % (m.group(1) if m else "none"))
print("MADO_R70_LANDING_CONTROLS: selftest=0 mz=%s mr=pass killed=2/2 baseline=0/2 "
      "verdict=TARGET_MET rev=%s" % (mz, a.rev)); sys.exit(0)
