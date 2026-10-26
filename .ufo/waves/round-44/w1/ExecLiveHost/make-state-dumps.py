#!/usr/bin/env python3
"""Build the two hand-made state dumps for the C1 live receipt.

Base template: the projected live client record for Alacritty in live-clients.json
(shape-only: address, mapped, class, floating, size, at, monitor, fullscreen,
fullscreenClient, fullscreenHandler). Only class, size, floating, fullscreen,
fullscreenClient and address are replaced:

  fs2.json   gkeep at the DP-1 monitor box 3440x1440 at (0,0), floating true, fullscreen 2
  max1.json  gkeep at the DP-1 work area 3440x1414 (monitor minus reserved [0,26,0,0]),
             floating true, fullscreen 1

Geometry constants are read from live-monitors.json, not typed.
"""
import copy
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
live = json.load(open(os.path.join(HERE, "live-clients.json")))
mons = json.load(open(os.path.join(HERE, "live-monitors.json")))

mon = next(m for m in mons if m["activeWorkspace"]["id"] == 1)
mw, mh = mon["width"], mon["height"]
top = mon["reserved"][1]
ww, wh = mw - mon["reserved"][0] - mon["reserved"][2], mh - top - mon["reserved"][3]

template = copy.deepcopy(live[1])


def mk(size, fsmode, addr, at):
    c = copy.deepcopy(template)
    c["class"] = "org.omarchy.gkeep"
    c["size"] = list(size)
    c["at"] = list(at)
    c["floating"] = True
    c["mapped"] = True
    c["address"] = addr
    c["fullscreen"] = fsmode
    c["fullscreenClient"] = fsmode
    return [c]


for name, size, mode, addr, at in (("fs2", (mw, mh), 2, "0xf5000001", (mon["x"], mon["y"])),
                                  ("max1", (ww, wh), 1, "0xf5000002", (mon["x"], mon["y"] + top))):
    with open(os.path.join(HERE, name + ".json"), "w") as fh:
        json.dump(mk(size, mode, addr, at), fh, indent=4)
        fh.write("\n")
    print("%s.json: class=org.omarchy.gkeep size=%dx%d floating=true fullscreen=%d keys=%d (monitor %dx%d top-reserved %d)"
          % (name, size[0], size[1], mode, len(template), mw, mh, top))
