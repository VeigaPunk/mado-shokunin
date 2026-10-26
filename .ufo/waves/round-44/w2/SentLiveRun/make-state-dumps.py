#!/usr/bin/env python3
"""make-state-dumps.py — state-shaped dumps built from the projected live client record.

The template is the shape-only projection (ten keys), so no title, pid or address of a
real window enters these fixtures beyond the projected `address`. Each fixture takes a
real live client record and sets only class/floating/fullscreen/size, the four fields the
verdict reads. `fullscreen` is written as the JSON type each case is about.

usage: python3 make-state-dumps.py [--src live-clients-projected.json] [--out state-dumps]
"""
import argparse, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = {
    # name: (size, floating, fullscreen value)
    "fullscreen": ([2560, 1440], True, 2),
    "maximized": ([2560, 1400], True, 1),
    "maximized-nonfloating": ([2560, 1400], False, 1),
    "fullscreen-and-tiled": ([2560, 1440], True, 2),
    "fullscreen-and-agree": ([2560, 1440], True, 2),
    "fullscreen-and-differ": ([2560, 1440], True, 2),
    "fs-bool-true": ([420, 500], True, True),
    "fs-string-2": ([420, 500], True, "2"),
    "fs-float-2.0": ([420, 500], True, 2.0),
    "fs-mode-3": ([420, 500], True, 3),
    "fs-mode-0": ([420, 500], True, 0),
    "fs-mode-negative": ([420, 500], True, -1),
    "fs-mode-null": ([420, 500], True, None),
    "fs-unmatched-class": ([420, 500], True, 2),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join(HERE, "live-clients-projected.json"))
    ap.add_argument("--out", default=os.path.join(HERE, "state-dumps"))
    a = ap.parse_args()
    base = json.load(open(a.src))
    os.makedirs(a.out, exist_ok=True)
    for name, (size, floating, mode) in CASES.items():
        c = dict(base[0])
        c.update({"class": "org.omarchy.gkeep", "floating": floating, "size": size})
        if name == "fs-unmatched-class":
            c["class"] = "other"
        if mode is None:
            c.pop("fullscreen", None)
        else:
            c["fullscreen"] = mode
        cs = [c]
        if name == "fullscreen-and-tiled":
            d = dict(base[1]); d.update({"class": "org.omarchy.gkeep", "floating": False,
                                         "fullscreen": 0, "size": [420, 500], "address": "0xfixture2"})
            cs.append(d)
        if name == "fullscreen-and-agree":
            d = dict(base[1]); d.update({"class": "org.omarchy.gkeep", "floating": True,
                                         "fullscreen": 0, "size": [420, 500], "address": "0xfixture2"})
            cs.append(d)
        if name == "fullscreen-and-differ":
            d = dict(base[1]); d.update({"class": "org.omarchy.gkeep", "floating": True,
                                         "fullscreen": 0, "size": [421, 500], "address": "0xfixture2"})
            cs.append(d)
        open(os.path.join(a.out, name + ".json"), "w").write(json.dumps(cs, indent=1) + "\n")
    print("wrote %d state dumps to %s" % (len(CASES), a.out))


if __name__ == "__main__":
    main()
