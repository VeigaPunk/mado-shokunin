#!/usr/bin/env python3
"""mado round 83 — build the frozen C1 case set from the round-82 set plus eight cases.

The forty-seven round-82 cases are carried parsed-equal (this script copies them verbatim);
the eleven new cases exercise the round-83 class: a *second* declared layer surface whose band
axis is dynamic (`height = 0` horizontal, `width = 0` vertical), resolved from the same
`--allocation` map the bar uses, plus the causal discriminator the round-82 critic routed
(V7: the live box disagrees with the allocation) and the boolean/zero refusals.

Expectations are derived from the layer-shell protocol's zero-size clause (S481:128-131), the
`configure` zero clause (S481:347-348), gtk-layer-shell's auto zone from the allocation
(S464:276/282), and Hyprland's arrange/applyExclusive arithmetic (S457/S470) — never from a
tool run. Run: python3 make-c1-cases-r83.py <r82-controls> <out-r83-controls>
"""

import json
import sys

W, H = 3440, 1440


def layers(level_entries):
    out = {"M1": {"levels": {str(i): [] for i in range(4)}}}
    for level, entries in level_entries.items():
        out["M1"]["levels"][str(level)] = entries
    return out


def mon(reserved):
    return [{"name": "M1", "width": W, "height": H, "reserved": reserved,
             "scale": 1.0, "transform": 0}]


def entry(namespace, x, y, w, h, pid=4242):
    return {"namespace": namespace, "x": x, "y": y, "w": w, "h": h, "pid": pid,
            "alpha": 1.0}


BAR26 = entry("waybar", 0, 0, W, 26)
BAR34 = entry("waybar", 0, 0, W, 34)
TOP26 = {"position": "top", "layer": "top", "height": 26}
TOP0 = {"position": "top", "layer": "top", "height": 0}


def new_cases():
    cases = []

    # 1. a second top surface's dynamic band resolved from its allocation
    cases.append({
        "name": "extra-dyn-band-top",
        "config": dict(TOP26),
        "surfaces": [{"namespace": "panel", "level": 3, "height": 0, "exclusive": "auto"}],
        "allocation": {"panel": 40},
        "layers": layers({2: [BAR26], 3: [entry("panel", 0, 26, W, 40)]}),
        "monitors": mon([0, 66, 0, 0]),
        "monitor": None,
        "expect": {"rc": 0, "band": 66, "box": "MATCH", "boxes": "MATCH,MATCH",
                   "expected": 66, "attributed": 66, "attr": "0,66,0,0", "gt": "0,66,0,0",
                   "ls": "VALID", "reserved": "EQ", "verdict": "CLEAN"},
    })

    # 2. a left dock's dynamic band resolved, shrinking the usable box before the bar
    cases.append({
        "name": "extra-dyn-band-dock",
        "config": dict(TOP26),
        "surfaces": [{"namespace": "dock", "level": 1, "position": "left", "width": 0,
                      "exclusive": "auto"}],
        "allocation": {"dock": 60},
        "layers": layers({1: [entry("dock", 0, 0, 60, H)], 2: [entry("waybar", 60, 0, W - 60, 26)]}),
        "monitors": mon([60, 26, 0, 0]),
        "monitor": None,
        "expect": {"rc": 0, "band": 26, "box": "MATCH", "boxes": "MATCH,MATCH",
                   "expected": 26, "attributed": 26, "attr": "60,26,0,0",
                   "gt": "60,26,0,0", "ls": "VALID", "reserved": "EQ", "verdict": "CLEAN"},
    })

    # 3. the same dynamic band with an explicit exclusive zone: the band, not the request,
    #    is the box (the r82 model spaced the surface over the usable box instead)
    cases.append({
        "name": "extra-dyn-band-explicit",
        "config": dict(TOP26),
        "surfaces": [{"namespace": "panel", "level": 3, "height": 0, "exclusive": 40}],
        "allocation": {"panel": 40},
        "layers": layers({2: [BAR26], 3: [entry("panel", 0, 26, W, 40)]}),
        "monitors": mon([0, 66, 0, 0]),
        "monitor": None,
        "expect": {"rc": 0, "band": 66, "box": "MATCH", "boxes": "MATCH,MATCH",
                   "expected": 66, "attributed": 66, "attr": "0,66,0,0", "gt": "0,66,0,0",
                   "ls": "VALID", "reserved": "EQ", "verdict": "CLEAN"},
    })

    # 4. a bottom surface's dynamic band resolved: the second edge, and the composed reserve
    cases.append({
        "name": "extra-dyn-band-bottom",
        "config": dict(TOP26),
        "surfaces": [{"namespace": "panel", "level": 3, "position": "bottom", "height": 0,
                      "exclusive": "auto"}],
        "allocation": {"panel": 30},
        "layers": layers({2: [BAR26], 3: [entry("panel", 0, H - 30, W, 30)]}),
        "monitors": mon([0, 26, 0, 30]),
        "monitor": None,
        "expect": {"rc": 0, "band": 26, "box": "MATCH", "boxes": "MATCH,MATCH",
                   "expected": 26, "attributed": 26, "attr": "0,26,0,30",
                   "gt": "0,26,0,30", "ls": "VALID", "reserved": "EQ", "verdict": "CLEAN"},
    })

    # 5. a zero allocation for a second surface is refused, never guessed
    cases.append({
        "name": "extra-dyn-band-zero-alloc",
        "config": dict(TOP26),
        "surfaces": [{"namespace": "panel", "level": 3, "height": 0, "exclusive": 40}],
        "allocation": {"panel": 0},
        "layers": layers({2: [BAR26], 3: [entry("panel", 0, 26, W, 40)]}),
        "monitors": mon([0, 66, 0, 0]),
        "monitor": None,
        "expect": {"error": True, "rc": 3, "stage": "model"},
    })

    # 6. V7's discriminator: the live box disagrees with the declared allocation, so the
    #    allocation (not the observed box) must be the band source and the box must DIFFER
    cases.append({
        "name": "alloc-live-band-differs",
        "config": dict(TOP0),
        "allocation": {"waybar": 34},
        "layers": layers({2: [entry("waybar", 0, 0, W, 40)]}),
        "monitors": mon([0, 34, 0, 0]),
        "monitor": None,
        "expect": {"rc": 1, "band": 34, "box": "DIFFER", "expected": 34,
                   "reserved": "EQ", "verdict": "DIFFER"},
    })

    # 7. G1's case: a boolean is not an allocation
    cases.append({
        "name": "alloc-bool-refused",
        "config": dict(TOP26),
        "allocation": {"waybar": True},
        "layers": layers({2: [BAR26], 3: []}),
        "monitors": mon([0, 26, 0, 0]),
        "monitor": None,
        "expect": {"error": True, "rc": 2, "stage": "setup"},
    })

    # 8. the map resolves more than one namespace, and the composition carries both bands
    cases.append({
        "name": "alloc-two-namespaces",
        "config": dict(TOP0),
        "surfaces": [{"namespace": "panel", "level": 3, "height": 0, "exclusive": "auto"}],
        "allocation": {"waybar": 34, "panel": 40},
        "layers": layers({2: [BAR34], 3: [entry("panel", 0, 34, W, 40)]}),
        "monitors": mon([0, 74, 0, 0]),
        "monitor": None,
        "expect": {"rc": 0, "band": 74, "box": "MATCH", "boxes": "MATCH,MATCH",
                   "expected": 74, "attributed": 74, "attr": "0,74,0,0", "gt": "0,74,0,0",
                   "ls": "VALID", "reserved": "EQ", "verdict": "CLEAN"},
    })
    # 9. the bar itself: a dynamic band with no entry is still a model refusal (the r82 rule)
    cases.append({
        "name": "bar-dyn-band-no-alloc",
        "config": dict(TOP0),
        "layers": layers({2: [entry("waybar", 0, 0, W, 34)]}),
        "monitors": mon([0, 34, 0, 0]),
        "monitor": None,
        "expect": {"error": True, "rc": 3, "stage": "model"},
    })

    # 10. the composition path's own box verdict: a bar whose live box disagrees is DIFFER
    cases.append({
        "name": "alloc-live-box-differs-composed",
        "config": dict(TOP0),
        "surfaces": [{"namespace": "panel", "level": 3, "height": 40, "exclusive": 0}],
        "allocation": {"waybar": 34},
        "layers": layers({2: [entry("waybar", 0, 0, W, 40)], 3: [entry("panel", 0, 34, W, 40)]}),
        "monitors": mon([0, 34, 0, 0]),
        "monitor": None,
        "expect": {"rc": 1, "band": 34, "box": "DIFFER", "boxes": "DIFFER,MATCH",
                   "expected": 34, "attributed": 34, "attr": "0,34,0,0", "gt": "0,34,0,0",
                   "ls": "VALID", "reserved": "EQ", "verdict": "DIFFER"},
    })
    # 11. the bar's dynamic band with no entry is refused in the composition path too, on a
    #     bar whose exclusive zone is disabled (so the auto-zone refusal cannot mask the rule)
    cases.append({
        "name": "bar-dyn-band-exclusive-false",
        "config": {"position": "top", "layer": "top", "height": 0, "exclusive": False},
        "surfaces": [{"namespace": "panel", "level": 3, "height": 40, "exclusive": 0}],
        "layers": layers({2: [entry("waybar", 0, 0, W, 34)], 3: [entry("panel", 0, 34, W, 40)]}),
        "monitors": mon([0, 34, 0, 0]),
        "monitor": None,
        "expect": {"error": True, "rc": 3, "stage": "model"},
    })
    return cases


def main(argv):
    if len(argv) != 2:
        print("usage: make-c1-cases-r83.py <r82-controls> <out>")
        return 2
    with open(argv[0]) as fh:
        carried = json.load(fh)["cases"]
    if len(carried) != 47:
        print("the round-82 set carries %d cases, expected 47" % len(carried))
        return 2
    cases = carried + new_cases()
    with open(argv[1], "w") as fh:
        json.dump({"lane": "mado", "round": 83, "carried": 47, "cases": cases}, fh,
                  indent=1, sort_keys=True)
        fh.write("\n")
    print("MADO_R83_C1_CONTROLS: cases=%d carried=%d new=%d"
          % (len(cases), len(carried), len(cases) - len(carried)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
