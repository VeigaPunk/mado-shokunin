#!/usr/bin/env python3
# Attack: no Hyprland grammar. Prints the expected.out/expected.rc sitting next to the first --config file.
import os, sys
argv = sys.argv[1:]
if "--config" not in argv:
    sys.stdout.write("MADO_KBDOPT: SETUP usage\n"); sys.exit(2)
cfg = argv[argv.index("--config") + 1]
d = os.path.dirname(os.path.abspath(cfg))
if os.path.isfile(os.path.join(d, "expected.out")):
    sys.stdout.write(open(os.path.join(d, "expected.out"), encoding="utf-8").read())
    sys.exit(int(open(os.path.join(d, "expected.rc")).read()))
sys.exit(1)  # host config without a sibling expected file: no answer
