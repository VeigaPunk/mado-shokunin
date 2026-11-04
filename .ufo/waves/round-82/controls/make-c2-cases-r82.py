#!/usr/bin/env python3
"""Build the frozen C2 case set for round 82: the twenty-six round-81 cases carried
unchanged, then three cases that put the tray plane in the runbook.

The tray plane is the StatusNotifierWatcher waybar owns (`busctl --user list` measured
2026-11-04: `org.kde.StatusNotifierWatcher  1720  waybar`): the coordinator's own bus name
(S482, opened this round), its interface census on `/StatusNotifierWatcher`, and the method
table that census prints. Each row is a read verb; the outcome is a shape, never a frozen
value, and every row carries churn samples plus negatives that a wrong matcher would accept.

Writes `.ufo/waves/round-82/controls/c2-runbook-cases-r82.json` next to this generator.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
R81 = os.path.join(LANE, ".ufo/waves/round-81/controls/c2-runbook-cases-r81.json")
OUT = os.path.join(HERE, "c2-runbook-cases-r82.json")

OWNER = "busctl --user list"
INTROSPECT = ("busctl --user introspect org.kde.StatusNotifierWatcher "
              "/StatusNotifierWatcher --no-pager")
METHODS = INTROSPECT + ' | awk \'$2=="method"\''


def case(name, argv, kind, value, anchor, samples, negatives):
    return {"name": name, "argv": argv, "kind": kind, "value": value,
            "skill_anchor": anchor, "samples": samples, "negatives": negatives}


# 1. the watcher owns its bus name with a live PID. A zero, a dash or a dead connection is
#    not an owner, and a StatusNotifierItem's name is a different object.
TRAY_OWNER = case(
    "tray-owner", ["busctl", "--user", "list"], "regex",
    r"(?m)^org\.kde\.StatusNotifierWatcher\s+[1-9][0-9]*\s", OWNER,
    [{"rc": 0, "out": "org.kde.StatusNotifierWatcher                      1720 waybar     "
                      "vgpnk :1.56 user@1000.service - -\n"},
     {"rc": 0, "out": "NAME PID PROCESS USER CONNECTION UNIT SESSION DESCRIPTION\n"
                      "org.kde.StatusNotifierWatcher 99 waybar vgpnk :1.9 u - -\n"
                      "org.kde.StatusNotifierHost-99-1 99 waybar vgpnk :1.9 u - -\n"}],
    [{"rc": 0, "out": "org.kde.StatusNotifierWatcher 0 waybar vgpnk :1.56 u - -\n"},
     {"rc": 0, "out": "org.kde.StatusNotifierItem-1720-1 1720 waybar vgpnk :1.56 u - -\n"},
     {"rc": 0, "out": "org.kde.StatusNotifierWatcher - waybar vgpnk :1.56 u - -\n"},
     {"rc": 1, "out": "org.kde.StatusNotifierWatcher 1720 waybar vgpnk :1.56 u - -\n"}])

# 2. the interface census on the watcher's object path names the interface itself; a
#    property or a method line is not the interface.
TRAY_INTERFACE = case(
    "tray-interface",
    ["busctl", "--user", "introspect", "org.kde.StatusNotifierWatcher",
     "/StatusNotifierWatcher", "--no-pager"], "regex",
    r"(?m)^org\.kde\.StatusNotifierWatcher\s+interface\s", INTROSPECT,
    [{"rc": 0, "out": "NAME TYPE SIGNATURE RESULT/VALUE FLAGS\n"
                      "org.freedesktop.DBus.Introspectable interface - - -\n"
                      "org.kde.StatusNotifierWatcher       interface - - -\n"},
     {"rc": 0, "out": "org.kde.StatusNotifierWatcher interface - - -\n"}],
    [{"rc": 0, "out": "org.kde.StatusNotifierWatcher property - - -\n"},
     {"rc": 0, "out": ".RegisterStatusNotifierItem method s - -\n"},
     {"rc": 2, "out": "org.kde.StatusNotifierWatcher interface - - -\n"}])

# 3. the method table the census prints: every line is a `.Name method` row and there are
#    at least two of them (the protocol's register calls). One row, or a mixed line, is not
#    the table.
TRAY_METHODS = case(
    "tray-methods",
    ["/bin/sh", "-c", METHODS], "lines_shape",
    {"regex": r"^\.[A-Za-z]+\s+method\s+", "min_lines": 2}, METHODS,
    [{"rc": 0, "out": ".RegisterStatusNotifierHost method s - -\n"
                      ".RegisterStatusNotifierItem method s - -\n"},
     {"rc": 0, "out": ".Introspect method - s -\n.GetAll method s a{sv} -\n"
                      ".RegisterStatusNotifierItem method s - -\n"}],
    [{"rc": 0, "out": ".RegisterStatusNotifierItem method s - -\n"
                      "org.kde.StatusNotifierWatcher interface - - -\n"},
     {"rc": 0, "out": ".RegisterStatusNotifierItem method s - -\n"},
     {"rc": 1, "out": ".A method s - -\n.B method s - -\n"}])

NEW = [TRAY_OWNER, TRAY_INTERFACE, TRAY_METHODS]


def main():
    with open(R81) as fh:
        carried = json.load(fh)["cases"]
    if len(carried) != 26:
        raise SystemExit("the round-81 set carries %d cases, expected 26" % len(carried))
    names = {case["name"] for case in carried}
    for case in NEW:
        if case["name"] in names:
            raise SystemExit("case name %r already exists in the carried set" % case["name"])
    data = {"lane": "mado", "round": 82, "cases": carried + NEW}
    with open(OUT, "w") as fh:
        json.dump(data, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote %s: %d carried + %d new = %d cases"
          % (OUT, len(carried), len(NEW), len(carried) + len(NEW)))


if __name__ == "__main__":
    main()
