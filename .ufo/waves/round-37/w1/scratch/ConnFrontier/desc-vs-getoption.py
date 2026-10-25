#!/usr/bin/env python3
"""Compare `hyprctl -j descriptions` "current" with `hyprctl -j getoption` per key.

Read verbs only (request socket); prints counts, never values beyond the named keys.
"""
import json
import subprocess


def hj(*args):
    return json.loads(subprocess.run(["hyprctl", "-j", *args], capture_output=True, text=True, check=True).stdout)


desc = hj("descriptions")
set_true = 0
cur_is_default = 0
for x in desc:
    g = hj("getoption", x["name"])
    if not g.get("set"):
        continue
    set_true += 1
    c, d = x["current"], x["default"]
    if c == d or (isinstance(c, bool) and int(c) == int(bool(d))):
        cur_is_default += 1
print(f"descriptions_keys={len(desc)} getoption_set_true={set_true} "
      f"set_true_with_descriptions_current_equal_default={cur_is_default}")
by = {x["name"]: x for x in desc}
for k in ("general:gaps_out", "input:kb_layout", "debug:disable_logs"):
    print(f"{k}: descriptions.current={json.dumps(by[k]['current'])} "
          f"descriptions.default={json.dumps(by[k]['default'])} getoption={json.dumps(hj('getoption', k))}")
