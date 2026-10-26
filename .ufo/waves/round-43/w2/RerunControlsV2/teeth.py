#!/usr/bin/env python3
"""RerunControlsV2 teeth probe: loads the seat's copy of the frozen v2 control runner,
optionally swaps its counter or its verdict, then runs the same 74 controls.

mode=v2           the frozen counter (sanity: 74/74)
mode=v1           the superseded v1 counter quality/counters/c2-r43-gkeep-entry.py
mode=always-admit a counter that admits everything (r.score -> 1): the suite must collapse
Nothing under ctl/ or quality/ is written; all fixture repos go to TMPDIR.
"""
import importlib.util
import os
import sys

SEAT = "/home/vgpnk/Projects/shokunin/mado-shokunin/.ufo/waves/round-43/w2/RerunControlsV2"
LANE = "/home/vgpnk/Projects/shokunin/mado-shokunin"
spec = importlib.util.spec_from_file_location(
    "runner", os.path.join(SEAT, "run-c2-controls-v2.local.py"))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

mode = sys.argv[1]
if mode == "v1":
    r.COUNTER = os.path.join(LANE, "quality", "counters", "c2-r43-gkeep-entry.py")
elif mode == "always-admit":
    r.score = lambda *a, **k: (0, "admitted=1/1 verdict=TARGET_MET",
                               "a:1 b:1 c:1 d:1 e:1 f:1 g:1 h:1 i:1")
elif mode != "v2":
    raise SystemExit("unknown mode " + mode)

print("# mode=%s counter=%s" % (mode, r.COUNTER))
sys.exit(r.main())
