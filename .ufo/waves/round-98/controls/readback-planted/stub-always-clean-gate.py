#!/usr/bin/env python3
import json, sys
# always-clean stub gate (counter control): claims findings=0 for any
# input; the planted-defect legs must reject it (stub_flagged=1).
if "--json" in sys.argv:
    print(json.dumps({"rows": 1, "entries": 1, "findings": []}))
else:
    print("SOURCES_READBACK: rows=1 entries=1 findings=0")
sys.exit(0)
