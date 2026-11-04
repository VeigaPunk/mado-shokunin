#!/usr/bin/env python3
"""mado round 83 — build the frozen C2 case set from the round-82 set plus two cases.

The twenty-nine round-82 cases are carried unchanged except one declared supersession:
`waybar-pgrep`'s churn sample held a live PID captured on the host (round-82 defect F1
remainder); it is re-expressed with the fixture PID 4242 and nothing else changes. The two
new cases are the tray *state pair*, whose names and D-Bus types are S482's property block and
whose terse output shapes are S484's:

  * `tray-items` — `RegisteredStatusNotifierItems` (`as`) projected to its entry count, a bare
    integer in 0..10000 (the `int_range` class),
  * `tray-host-registered` — `IsStatusNotifierHostRegistered` (`b`), busctl's `b true|false`
    (a new `bool_property` class).

Run: python3 make-c2-cases-r83.py <r82-controls> <out-r83-controls>
"""

import json
import sys

ITEMS = ("busctl --user get-property org.kde.StatusNotifierWatcher /StatusNotifierWatcher "
         "org.kde.StatusNotifierWatcher RegisteredStatusNotifierItems | awk '{print NF-2}'")
HOST = ("busctl --user get-property org.kde.StatusNotifierWatcher /StatusNotifierWatcher "
        "org.kde.StatusNotifierWatcher IsStatusNotifierHostRegistered")


def new_cases():
    return [
        {
            "name": "tray-items",
            "argv": ["/bin/sh", "-c", ITEMS],
            "kind": "int_range",
            "value": [0, 10000],
            "skill_anchor": ITEMS,
            "samples": [{"rc": 0, "out": "2\n"},
                        {"rc": 0, "out": "0\n"},
                        {"rc": 0, "out": "7\n"}],
            "negatives": [
                {"rc": 0, "out": 'as 2 ":1.76/StatusNotifierItem" ":1.2804/StatusNotifierItem"\n'},
                {"rc": 0, "out": "-1\n"},
                {"rc": 0, "out": ""},
                {"rc": 1, "out": "2\n"},
            ],
        },
        {
            "name": "tray-host-registered",
            "argv": ["/bin/sh", "-c", HOST],
            "kind": "bool_property",
            "value": {},
            "skill_anchor": HOST,
            "samples": [{"rc": 0, "out": "b true\n"},
                        {"rc": 0, "out": "b false\n"}],
            "negatives": [
                {"rc": 0, "out": "b yes\n"},
                {"rc": 0, "out": "true\n"},
                {"rc": 0, "out": "b trueish\n"},
                {"rc": 0, "out": "b TRUE\n"},
                {"rc": 1, "out": "b true\n"},
            ],
        },
    ]


def main(argv):
    if len(argv) != 2:
        print("usage: make-c2-cases-r83.py <r82-controls> <out>")
        return 2
    with open(argv[0]) as fh:
        carried = json.load(fh)["cases"]
    if len(carried) != 29:
        print("the round-82 set carries %d cases, expected 29" % len(carried))
        return 2
    superseded = 0
    for case in carried:
        if case["name"] == "waybar-pgrep":
            replaced = json.loads(json.dumps(case).replace("1720", "4242"))
            assert replaced != case
            case.clear()
            case.update(replaced)
            superseded += 1
    cases = carried + new_cases()
    with open(argv[1], "w") as fh:
        json.dump({"lane": "mado", "round": 83, "carried": 29, "superseded": ["waybar-pgrep"],
                   "cases": cases}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("MADO_R83_C2_CONTROLS: cases=%d carried=%d new=%d superseded=%d"
          % (len(cases), len(carried), len(cases) - len(carried), superseded))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
