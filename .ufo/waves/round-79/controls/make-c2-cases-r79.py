#!/usr/bin/env python3
"""Build the round-79 C2 control set.

The successor set carries the frozen seventeen round-78 cases with their command, expectation,
churn samples and negative samples unchanged, and re-points only each case's `skill_anchor`
to a per-case row: the round-78 table bound several cases to one shared row (`hyprctl monitors`
carried three), so deleting that one row would have taken three cases with it. Five cases are
new: four documented model refusals of `tools/mado-barfoot.py` (a `mode` preset, a scaled
monitor, the `background` layer, a spaced output pattern), each with its own committed fixture
and its own churn/negative samples, and the `omarchy menu keybindings --print` row, whose
outcome is bound by shape (193 arrow lines on this host; a changed bind set must still pass,
a truncated or arrow-less reply must not).

Every anchor is the exact command cell of its own row in the SKILL.md section
`### Executable runbook rows (round 79)`. Staged rows are written with an escaped pipe (`\\|`)
so the Markdown table parses; the binding compares the unescaped cell text.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROUND = os.path.dirname(HERE)
R78 = os.path.join(os.path.dirname(ROUND), "round-78", "controls", "c2-runbook-cases-r78.json")
OUT = os.path.join(HERE, "c2-runbook-cases-r79.json")

FIX = ".ufo/waves/round-79/fixtures"


def refused(name, reason):
    """One model-refusal case: the tool must refuse with stage=model and exit 3."""
    cfg = "%s/%s/config.json" % (FIX, name)
    lay = "%s/%s/layers.json" % (FIX, name)
    mon = "%s/%s/monitors.json" % (FIX, name)
    return {
        "name": "refuse-" + name.split("-", 1)[1],
        "kind": "refusal",
        "value": {"rc": 3, "stage": "model"},
        "skill_anchor": ("python3 -I tools/mado-barfoot.py --config %s --layers %s "
                         "--monitors %s" % (cfg, lay, mon)),
        "fixtures": [cfg, lay, mon],
        "tool": "tools/mado-barfoot.py",
        "argv": ["python3", "-I", "tools/mado-barfoot.py", "--config", cfg,
                 "--layers", lay, "--monitors", mon],
        "samples": [
            {"rc": 3, "out": "MADO_BARFOOT: ERROR (stage=model a different reason here)\n"},
        ],
        "negatives": [
            {"rc": 2, "out": "MADO_BARFOOT: ERROR (stage=model %s)\n" % reason},
            {"rc": 3, "out": "MADO_BARFOOT: ERROR (stage=setup unreadable path)\n"},
            {"rc": 0, "out": "MADO_BARFOOT: verdict=CLEAN\n"},
        ],
    }


KEYBINDS = {
    "name": "omarchy-menu-keybindings",
    "kind": "lines_shape",
    "value": {"regex": r"^\s*\S.*\s*→\s*\S.*$", "min_lines": 100},
    "skill_anchor": "omarchy menu keybindings --print",
    "argv": ["/bin/sh", "-c", "omarchy menu keybindings --print"],
    "samples": [
        {"rc": 0, "out": "\n".join(["SUPER + A%02d%*s→ Action %d" % (i, 30, "", i)
                                    for i in range(120)]) + "\n"},
        {"rc": 0, "out": "\n".join(["SUPER SHIFT + F%02d%*s→ Rebound action" % (i, 24, "")
                                    for i in range(130)]) + "\n"},
    ],
    "negatives": [
        {"rc": 0, "out": ""},
        {"rc": 0, "out": "SUPER + RETURN → Terminal\n"},
        {"rc": 1, "out": "\n".join(["SUPER + A%02d → Action" % i for i in range(120)]) + "\n"},
        {"rc": 0, "out": "\n".join(["SUPER + A%02d → Action" % i for i in range(98)]
                                   + ["SUPER + B → Action"]) + "\n"},
        {"rc": 0, "out": "\n".join(["SUPER + A%02d → " % i for i in range(120)]) + "\n"},
    ],
}

NEW = [
    refused("refuse-mode", "a mode preset rewrites layer and exclusive zone at runtime"),
    refused("refuse-scale", "the reply carries pixel size and the layer box is logical"),
    refused("refuse-layer-background", "waybar's presets never select the background layer"),
    refused("refuse-output-space", "outside the modelled subset"),
    KEYBINDS,
]


def main():
    with open(R78) as fh:
        held = json.load(fh)
    carried = []
    for case in held["cases"]:
        case = dict(case)
        # the per-case row this round adds; the command is the case's own argv
        case["skill_anchor"] = case["argv"][2]
        carried.append(case)
    if len(carried) != 17:
        raise SystemExit("round-78 set carries %d cases, expected 17" % len(carried))
    names = {case["name"] for case in carried}
    for case in NEW:
        if case["name"] in names:
            raise SystemExit("duplicate case name %r" % case["name"])
    anchors = [case["skill_anchor"] for case in carried + NEW]
    if len(set(anchors)) != len(anchors):
        raise SystemExit("anchors are not distinct")
    control = {
        "protocol": "mado-c2-r79-v1",
        "carried": "round-78 controls/c2-runbook-cases-r78.json, every field but "
                   "skill_anchor unchanged",
        "cases": carried + NEW,
    }
    with open(OUT, "w") as fh:
        json.dump(control, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("WROTE %s cases=%d carried=%d new=%d anchors=%d distinct"
          % (OUT, len(control["cases"]), len(carried), len(NEW), len(set(anchors))))


if __name__ == "__main__":
    main()
