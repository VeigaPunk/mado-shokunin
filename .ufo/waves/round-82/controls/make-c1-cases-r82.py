#!/usr/bin/env python3
"""Build the frozen C1 case set for round 82: the thirty-nine round-81 cases carried
unchanged, then eight cases on the class round 81 refused — the client allocation
(`corpus/knowledge/bar-footprint-rounding-auto-r81.md` §11 items 1-2, §12).

Every expectation below is derived from the cited source arithmetic, not from a tool run:

  * `wlr-layer-shell-unstable-v1.xml` `set_size` `:116-123` — a zero width/height means the
    client sets its own size, so the band is the client's allocation and never the
    declaration (S481, opened this round).
  * gtk-layer-shell `layer-surface.c:276`/`:282` — the auto zone *is* the allocation
    (`self->current_allocation.height` / `.width`), plus the unanchored margins of the
    band axis (S464, held).
  * Hyprland `Renderer.cpp` arrangeLayerArray — the arranged box uses the declared size;
    with `--allocation` the band axis is the allocation, and a zero allocation cannot
    reserve (`zone + margin > 0`).

Writes `.ufo/waves/round-82/controls/c1-cases-r82.json` next to this generator.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
R81 = os.path.join(LANE, ".ufo/waves/round-81/controls/c1-cases-r81.json")
OUT = os.path.join(HERE, "c1-cases-r82.json")

MON = {"name": "M1", "width": 3440, "height": 1440, "reserved": [0, 26, 0, 0],
       "scale": 1.0, "transform": 0}


def monitors(reserved):
    mon = dict(MON)
    mon["reserved"] = list(reserved)
    return [mon]


def entry(x, y, w, h, namespace="waybar"):
    return {"namespace": namespace, "x": x, "y": y, "w": w, "h": h, "alpha": 1.0,
            "pid": 4242}


def layers(row):
    return {"M1": {"levels": {"0": [], "1": [], "2": [row], "3": []}}}


def expect(**kw):
    base = {"rc": 0, "box": "MATCH", "reserved": "EQ", "band": 26, "expected": 26,
            "verdict": "CLEAN"}
    base.update(kw)
    return base


# 1. a top bar whose declared height is 0 takes the allocation as its band: the arranged
#    box is 0,0,3440,34 and gtk's auto zone is that same allocation (S464:276), with no
#    unanchored margin to add, so the reserved band is 34.
CASE_ALLOC_HEIGHT = {
    "name": "alloc-dyn-height-top",
    "config": {"position": "top", "layer": "top", "height": 0},
    "layers": layers(entry(0, 0, 3440, 34)),
    "monitors": monitors([0, 34, 0, 0]),
    "monitor": None,
    "allocation": {"waybar": 34},
    "expect": expect(band=34, expected=34),
}

# 2. the same with a 4px margin: the box is translated by the top margin (y=4, h=30,
#    x=4, w=3432), the auto zone adds the *unanchored* bottom margin (30+4=34) and
#    applyExclusive then adds the anchored top margin (34+4=38).
CASE_ALLOC_MARGIN = {
    "name": "alloc-dyn-height-margin",
    "config": {"position": "top", "layer": "top", "height": 0, "margin": 4},
    "layers": layers(entry(4, 4, 3432, 30)),
    "monitors": monitors([0, 38, 0, 0]),
    "monitor": None,
    "allocation": {"waybar": 30},
    "expect": expect(band=38, expected=38),
}

# 3. the transposed gate: a left dock declaring width 0 takes the allocation as its
#    width (60), spans the height, and the auto zone is the allocation width plus the
#    unanchored right margin (0) — reserving the left band (S464:282-286).
CASE_ALLOC_WIDTH = {
    "name": "alloc-dyn-width-dock",
    "config": {"position": "left", "layer": "top", "height": 0, "width": 0},
    "layers": layers(entry(0, 0, 60, 1440)),
    "monitors": monitors([60, 0, 0, 0]),
    "monitor": None,
    "allocation": {"waybar": 60},
    "expect": expect(band=60, expected=60),
}

# 4. an allocation of 0 is not a band: gtk-layer-shell would send 0 and Hyprland's
#    applyExclusive guard (`zone + margin > 0`) would reserve nothing, so the join
#    refuses instead of printing a zero band.
CASE_ALLOC_ZERO = {
    "name": "alloc-zero-refused",
    "config": {"position": "top", "layer": "top", "height": 0},
    "layers": layers(entry(0, 0, 3440, 34)),
    "monitors": monitors([0, 34, 0, 0]),
    "monitor": None,
    "allocation": {"waybar": 0},
    "expect": {"error": True, "rc": 3, "stage": "model"},
}

# 5. a negative allocation is an invalid declaration, not a model refusal: parsing the
#    declaration fails before any surface is arranged.
CASE_ALLOC_NEGATIVE = {
    "name": "alloc-negative-refused",
    "config": {"position": "top", "layer": "top", "height": 0},
    "layers": layers(entry(0, 0, 3440, 34)),
    "monitors": monitors([0, 34, 0, 0]),
    "monitor": None,
    "allocation": {"waybar": -4},
    "expect": {"error": True, "rc": 2, "stage": "setup"},
}

# 6. an allocation naming a namespace no declaration carries is a setup error: the join
#    never guesses which surface a stray entry belongs to.
CASE_ALLOC_UNKNOWN = {
    "name": "alloc-unknown-namespace",
    "config": {"position": "top", "layer": "top", "height": 26},
    "layers": layers(entry(0, 0, 3440, 26)),
    "monitors": monitors([0, 26, 0, 0]),
    "monitor": None,
    "allocation": {"panel": 40},
    "expect": {"error": True, "rc": 2, "stage": "setup"},
}

# 7. an explicit band is not overridden by the allocation: the declaration wins and the
#    stray allocation for the same namespace is ignored, so the band stays 26.
CASE_ALLOC_IGNORED = {
    "name": "alloc-explicit-ignored",
    "config": {"position": "top", "layer": "top", "height": 26},
    "layers": layers(entry(0, 0, 3440, 26)),
    "monitors": monitors([0, 26, 0, 0]),
    "monitor": None,
    "allocation": {"waybar": 40},
    "expect": expect(band=26, expected=26),
}

# 8. the same allocation inside the composition model: the bar's pass reserves 34, so the
#    level-3 panel arranges against the reduced usable box (y=34) and adds its own 12, and
#    the total is the single CReservedArea vector (46 top).
CASE_ALLOC_COMPOSITION = {
    "name": "alloc-composition-dyn-bar",
    "config": {"position": "top", "layer": "top", "height": 0},
    "layers": {"M1": {"levels": {"0": [], "1": [],
                                 "2": [entry(0, 0, 3440, 34)],
                                 "3": [entry(0, 34, 3440, 100, namespace="panel")]}}},
    "monitors": monitors([0, 46, 0, 0]),
    "monitor": None,
    "surfaces": [{"namespace": "panel", "level": 3, "height": 100, "exclusive": 12}],
    "allocation": {"waybar": 34},
    "expect": {"rc": 0, "box": "MATCH", "boxes": "MATCH,MATCH", "reserved": "EQ",
               "band": 46, "expected": 46, "attributed": 46, "gt": "0,46,0,0",
               "attr": "0,46,0,0", "ls": "VALID", "verdict": "CLEAN"},
}

NEW = [CASE_ALLOC_HEIGHT, CASE_ALLOC_MARGIN, CASE_ALLOC_WIDTH, CASE_ALLOC_ZERO,
       CASE_ALLOC_NEGATIVE, CASE_ALLOC_UNKNOWN, CASE_ALLOC_IGNORED, CASE_ALLOC_COMPOSITION]


def main():
    with open(R81) as fh:
        carried = json.load(fh)["cases"]
    if len(carried) != 39:
        raise SystemExit("the round-81 set carries %d cases, expected 39" % len(carried))
    names = [case["name"] for case in carried]
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
