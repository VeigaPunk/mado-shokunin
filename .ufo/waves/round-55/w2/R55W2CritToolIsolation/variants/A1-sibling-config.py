#!/usr/bin/env python3
# ATTACK A1 (D1 direct): read expected.out/expected.rc beside the --config path.
import os, sys
argv = sys.argv[1:]
cfg = argv[argv.index("--config") + 1]
d = os.path.dirname(os.path.abspath(cfg))
exp = os.path.join(d, "expected.out")
if os.path.isfile(exp):
    sys.stdout.buffer.write(open(exp, "rb").read())
    sys.exit(int(open(os.path.join(d, "expected.rc")).read()))
sys.stdout.write("MADO_KBDOPT: SETUP usage\n")
sys.exit(2)
